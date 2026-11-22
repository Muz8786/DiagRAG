"""OPTIONAL quantum-machine-learning comparison (docs/evidence/qml_protocol.md). Descriptive only; ML is the project's method, QML is a side comparison of scores.
Everything is SIMULATED: a noiseless statevector simulator written here (numpy/torch), 6 qubits. No quantum hardware, no noise model, and no claim of quantum advantage.
Task: fault-versus-clean detection AUROC on held-out episodes. All models are fitted on TRAIN-split single-fault rows only and scored on the TEST split (never tuned on it).
Usage: python qml_compare.py <episodes.jsonl of a judged run> <out.json> [--composed composed_features.jsonl] [--threads 2]"""
import argparse, hashlib, json, math, time
import numpy as np, torch
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

ap = argparse.ArgumentParser(); ap.add_argument('episodes'); ap.add_argument('out'); ap.add_argument('--composed'); ap.add_argument('--threads', type=int, default=2); a = ap.parse_args()
torch.set_num_threads(a.threads)
NQ, REPS, LAYERS, EPOCHS, LR, BATCH, NSUB, SEEDS = 6, 2, 3, 80, 0.05, 256, 2000, [0, 1, 2, 3, 4]   # fixed by the protocol; none is tuned on the test split
rows = [json.loads(l) for l in open(a.episodes, encoding='utf-8')]; FE = sorted(rows[0]['feats'])
def mat(es): return np.array([[e['feats'][k] for k in FE] for e in es], np.float64)
tr = [e for e in rows if e['split'] == 'train' and e['fault'] != 'C2']; te = [e for e in rows if e['split'] == 'test' and e['fault'] != 'C2']
Xtr, Xte = mat(tr), mat(te); ytr = np.array([e['fault'] != 'NONE' for e in tr], int); yte = np.array([e['fault'] != 'NONE' for e in te], int)
Xc = None
if a.composed:
    comp = [json.loads(l) for l in open(a.composed, encoding='utf-8')]; comp = [c for c in comp if c['split'] == 'test']
    Xc = np.array([[c['feats'][k] for k in FE] for c in comp], np.float64); stratum_c = np.array([c['stratum'] for c in comp])
clean_te = Xte[yte == 0]
# ---- preprocessing shared by every reduced model: standardise, PCA to NQ components, min-max to [0, pi]; all fitted on TRAIN only
sc = StandardScaler().fit(Xtr); pca = PCA(n_components=NQ, random_state=0).fit(sc.transform(Xtr))
def red(X): return pca.transform(sc.transform(X))
Ztr = red(Xtr); lo, hi = Ztr.min(0), Ztr.max(0)
def ang(X): return np.clip((red(X) - lo) / np.maximum(hi - lo, 1e-9), 0, 1) * math.pi
Atr, Ate = ang(Xtr), ang(Xte); Ac = ang(Xc) if Xc is not None else None
print('train', Xtr.shape, 'test', Xte.shape, '| PCA explained variance of 6 components: %.3f' % pca.explained_variance_ratio_.sum(), flush=True)

# ---- noiseless statevector simulator (basis index = bits q0..q5, q0 most significant)
DIM = 2 ** NQ; BITS = np.array([[(b >> (NQ - 1 - q)) & 1 for q in range(NQ)] for b in range(DIM)], np.float64)    # DIM x NQ
RING = [(i, (i + 1) % NQ) for i in range(NQ)]
H1 = (torch.tensor([[1, 1], [1, -1]], dtype=torch.complex64) / math.sqrt(2))
def apply1(psi, U, q):   # psi (B, DIM); U (2,2) or (B,2,2) acting on qubit q
    B = psi.shape[0]; t = psi.reshape(B, 2 ** q, 2, 2 ** (NQ - q - 1))
    t = torch.einsum('ij,bajc->baic', U, t) if U.dim() == 2 else torch.einsum('bij,bajc->baic', U, t)
    return t.reshape(B, DIM)
def hadamards(psi):
    for q in range(NQ): psi = apply1(psi, H1, q)
    return psi
def zz_map_states(A):   # Havlicek-style ZZ feature map, REPS repetitions: H, phase 2*x_i*bit_i, ring phase 2*(pi-x_i)*(pi-x_j)*(bit_i xor bit_j)
    A = torch.tensor(A, dtype=torch.float64); B = A.shape[0]; bits = torch.tensor(BITS)
    phase = 2 * A @ bits.T                                                                  # (B, DIM)
    for i, j in RING:
        par = (bits[:, i] + bits[:, j] - 2 * bits[:, i] * bits[:, j])                       # xor
        phase = phase + 2 * ((math.pi - A[:, i]) * (math.pi - A[:, j]))[:, None] * par[None, :]
    ph = torch.exp(1j * phase).to(torch.complex64); psi = torch.zeros(B, DIM, dtype=torch.complex64); psi[:, 0] = 1
    for _ in range(REPS): psi = hadamards(psi) * ph
    return hadamards(psi) if False else psi
def fidelity_kernel(P, Q): return (P @ Q.conj().T).abs().pow(2).numpy().astype(np.float64)
CNOT_PERM = None
def cnot_ring_perm():
    perm = np.arange(DIM)
    for c, t in RING:
        new = np.arange(DIM)
        for b in range(DIM):
            if (b >> (NQ - 1 - c)) & 1: new[b] = b ^ (1 << (NQ - 1 - t))
        perm = perm[new]                         # compose permutations
    return torch.tensor(perm)
def ry(th): c, s = torch.cos(th / 2), torch.sin(th / 2); return torch.stack([torch.stack([c, -s], -1), torch.stack([s, c], -1)], -2).to(torch.complex64)
def rz(th): e = torch.exp(-0.5j * th.to(torch.complex64)); z = torch.zeros_like(e); return torch.stack([torch.stack([e, z], -1), torch.stack([z, e.conj()], -1)], -2)
class VQC(torch.nn.Module):   # data re-uploading: per layer RY(x_i) on every qubit, trainable RY and RZ, then a CNOT ring; readout <Z_0>
    def __init__(s, seed):
        super().__init__(); g = torch.Generator().manual_seed(seed)
        s.w = torch.nn.Parameter(torch.randn(LAYERS, NQ, 2, generator=g, dtype=torch.float32) * 0.5); s.scale = torch.nn.Parameter(torch.tensor(2.0)); s.bias = torch.nn.Parameter(torch.tensor(0.0))
        s.register_buffer('perm', cnot_ring_perm()); s.register_buffer('z0', torch.tensor(1.0 - 2 * BITS[:, 0], dtype=torch.float32))
    def forward(s, A):
        B = A.shape[0]; psi = torch.zeros(B, DIM, dtype=torch.complex64); psi[:, 0] = 1
        for l in range(LAYERS):
            for q in range(NQ): psi = apply1(psi, ry(A[:, q]), q)
            for q in range(NQ): psi = apply1(psi, ry(s.w[l, q, 0]), q); psi = apply1(psi, rz(s.w[l, q, 1]), q)
            psi = psi[:, s.perm]
        return s.scale * (psi.abs().pow(2) @ s.z0) + s.bias
def boot_ci(y, sc, n=1000, seed=0):
    r = np.random.default_rng(seed); out = []
    for _ in range(n):
        i = r.integers(0, len(y), len(y))
        if len(set(y[i])) == 2: out.append(roc_auc_score(y[i], sc[i]))
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))
def score_all(name, s_te, s_c=None):
    res = dict(auroc=float(roc_auc_score(yte, s_te)), ci=list(boot_ci(yte, s_te)))
    if s_c is not None and len(clean_te):
        y2 = np.r_[np.ones(len(s_c)), np.zeros((yte == 0).sum())]; res['composed_vs_clean'] = dict(auroc=float(roc_auc_score(y2, np.r_[s_c, s_te[yte == 0]])), n_composed=int(len(s_c)))
        res['composed_by_stratum'] = {s: float(roc_auc_score(np.r_[np.ones((stratum_c == s).sum()), np.zeros((yte == 0).sum())], np.r_[s_c[stratum_c == s], s_te[yte == 0]])) for s in sorted(set(stratum_c)) if (stratum_c == s).sum() >= 5}
    R[name] = res; print('%-34s AUROC %.4f [%.3f, %.3f]%s' % (name, res['auroc'], *res['ci'], ('  composed-vs-clean %.4f' % res['composed_vs_clean']['auroc']) if 'composed_vs_clean' in res else ''), flush=True)
R = {}; t0 = time.time()
# ---- classical reference (the project's model class) on all 63 features
m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=0).fit(Xtr, ytr)
score_all('ML main: HistGB, 63 features', m.predict_proba(Xte)[:, 1], m.predict_proba(Xc)[:, 1] if Xc is not None else None)
# ---- classical comparators on the SAME 6-dimensional input the quantum models get
Ztr6, Zte6, Zc6 = red(Xtr), red(Xte), (red(Xc) if Xc is not None else None)
m = LogisticRegression(max_iter=2000, class_weight='balanced').fit(Ztr6, ytr); score_all('ML 6-d: logistic regression', m.decision_function(Zte6), m.decision_function(Zc6) if Zc6 is not None else None)
m = SVC(kernel='rbf', C=1.0, gamma='scale', class_weight='balanced').fit(Ztr6, ytr); score_all('ML 6-d: SVM, RBF kernel', m.decision_function(Zte6), m.decision_function(Zc6) if Zc6 is not None else None)
m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=0).fit(Ztr6, ytr)
score_all('ML 6-d: HistGB', m.predict_proba(Zte6)[:, 1], m.predict_proba(Zc6)[:, 1] if Zc6 is not None else None)
# ---- QML 1: quantum-kernel SVM (fidelity kernel of the simulated feature map)
Ptr, Pte = zz_map_states(Atr), zz_map_states(Ate); Ktr = fidelity_kernel(Ptr, Ptr); Kte = fidelity_kernel(Pte, Ptr)
q = SVC(kernel='precomputed', C=1.0, class_weight='balanced').fit(Ktr, ytr)
score_all('QML: quantum-kernel SVM (6 qubits)', q.decision_function(Kte), q.decision_function(fidelity_kernel(zz_map_states(Ac), Ptr)) if Ac is not None else None)
R['QML: quantum-kernel SVM (6 qubits)']['kernel_gram_diag_mean'] = float(np.mean(np.diag(Ktr))); R['QML: quantum-kernel SVM (6 qubits)']['kernel_offdiag_mean'] = float((Ktr.sum() - np.trace(Ktr)) / (len(Ktr) ** 2 - len(Ktr)))
# ---- QML 2: variational quantum classifier, 5 seeds, fixed epochs, class-balanced training subsample
rng = np.random.default_rng(0); pos, neg = np.where(ytr == 1)[0], np.where(ytr == 0)[0]; k = NSUB // 2
sub = np.r_[rng.choice(pos, min(k, len(pos)), replace=False), rng.choice(neg, min(k, len(neg)), replace=False)]
At, yt = torch.tensor(Atr[sub], dtype=torch.float32), torch.tensor(ytr[sub], dtype=torch.float32); runs = []
for seed in SEEDS:
    torch.manual_seed(seed); net = VQC(seed); opt = torch.optim.Adam(net.parameters(), lr=LR); g = torch.Generator().manual_seed(seed)
    for ep in range(EPOCHS):
        perm = torch.randperm(len(At), generator=g)
        for i in range(0, len(At), BATCH):
            idx = perm[i:i + BATCH]; opt.zero_grad(); loss = torch.nn.functional.binary_cross_entropy_with_logits(net(At[idx]), yt[idx]); loss.backward(); opt.step()
    with torch.no_grad():
        s_te = np.concatenate([net(torch.tensor(Ate[i:i + 512], dtype=torch.float32)).numpy() for i in range(0, len(Ate), 512)])
        s_c = np.concatenate([net(torch.tensor(Ac[i:i + 512], dtype=torch.float32)).numpy() for i in range(0, len(Ac), 512)]) if Ac is not None else None
    runs.append((s_te, s_c, float(loss))); print('  VQC seed %d final train loss %.4f | test AUROC %.4f | %.0fs' % (seed, loss.item(), roc_auc_score(yte, s_te), time.time() - t0), flush=True)
aus = [roc_auc_score(yte, r[0]) for r in runs]
R['QML: variational classifier (6 qubits, 5 seeds)'] = dict(auroc=float(np.mean(aus)), auroc_per_seed=[float(x) for x in aus], auroc_sd=float(np.std(aus)), ci=list(boot_ci(yte, np.mean([r[0] for r in runs], 0))), note='AUROC of each seed; the ci is for the seed-averaged score')
if Ac is not None:
    R['QML: variational classifier (6 qubits, 5 seeds)']['composed_vs_clean'] = dict(auroc=float(np.mean([roc_auc_score(np.r_[np.ones(len(r[1])), np.zeros((yte == 0).sum())], np.r_[r[1], r[0][yte == 0]]) for r in runs])))
print('%-34s AUROC %.4f +- %.4f over 5 seeds' % ('QML: variational classifier', np.mean(aus), np.std(aus)))
R['_meta'] = dict(episodes_sha256=hashlib.sha256(open(a.episodes, 'rb').read()).hexdigest(), n_train=int(len(ytr)), n_test=int(len(yte)), n_test_faulted=int(yte.sum()), n_test_clean=int((yte == 0).sum()), n_qubits=NQ, feature_map_reps=REPS,
                  vqc=dict(layers=LAYERS, epochs=EPOCHS, lr=LR, batch=BATCH, train_subsample=NSUB, seeds=SEEDS), pca_explained_variance=float(pca.explained_variance_ratio_.sum()), seconds=float(time.time() - t0),
                  simulated=True, noiseless=True, hardware=False, claim='no claim of quantum advantage; score comparison only')
json.dump(R, open(a.out, 'w'), indent=1); print('wrote', a.out)

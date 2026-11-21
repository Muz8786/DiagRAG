"""Build DiagRAG-Bench v1.0 from a finished v3 judged run (checkpoint.pkl in diagrag_out/).

Writes, under bench/release_v1/:
  episodes_dev.jsonl     train-split episodes WITH labels (public)
  episodes_test.jsonl    held-out episodes WITHOUT labels (public)
  telemetry_dev.csv / telemetry_test.csv   the telemetry feature vector of every episode (Track 1 input)
  labels_dev.jsonl       dev labels in scorer format (public)
  families.json          fault -> family -> group, evidence tier
  MANIFEST.json          version, SHA-256 of every file, and the SHA-256 COMMITMENT of the private test labels
and, OUTSIDE the public folder (path given by --private), labels_test.jsonl (private held-out labels).
Synthetic overlay documents are included in full, because Track 2 needs them; they are marked synthetic.
"""
import argparse, csv, hashlib, json, os, pickle, sys

ap = argparse.ArgumentParser(); ap.add_argument('--ckpt', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--private', required=True); ap.add_argument('--code-sha', required=True)
ap.add_argument('--corpus', required=True, help='kb_tier3_186k.jsonl.gz (licence filter re-applied to recover doc ids)'); a = ap.parse_args()
R = pickle.load(open(a.ckpt, 'rb')); EP = R['EPIS']
os.makedirs(a.out, exist_ok=True); os.makedirs(a.private, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TIER = dict(Q01='N', Q02='M', Q03='M', Q04='S', Q05='M', Q07='M', Q09='P', K03='N', K04='M', K05='S', K06='N', K07='S', K08='M',
            K09='M', K11='S', K12='S', R01='S', R03='N', R05='N', R06='P', R07='P', R10='N', R11='S', R13='M', R15='S', R19='S',
            R22='S', R23='S', R24='M', R25='S', R26='S', C2='N')
FAMILY = {f: f for f in TIER}
FAMILY.update(Q01='QLEX', Q03='QLEX', Q04='QLEX', Q05='QLEX', K04='STALE', R07='STALE', R03='ENC', R10='ENC', R11='ENC')
import gzip
DOCIDS = [d['doc_id'] for d in map(json.loads, gzip.open(a.corpus, 'rt', encoding='utf-8')) if d['license_status'] != 'conflicting_unverified']


def eid(e, n): return hashlib.sha256(f"{e['split']}|{e['bid']}|{e['fault']}|{n}".encode()).hexdigest()[:16]


def jdump(x):
    if hasattr(x, 'item'): return x.item()
    if isinstance(x, set): return sorted(x)
    return str(x)


def cfg_public(c):
    d = {k: v for k, v in c.items() if k not in ('emb_override',) and v not in (None, False, 0, 0.0)}
    if c.get('emb_override'): d['emb_override_doc_rows'] = sorted(int(i) for i in c['emb_override'])
    return d


famj = {f: dict(family=FAMILY[f], group=f[0], evidence_tier=TIER[f]) for f in TIER}
json.dump(famj, open(os.path.join(a.out, 'families.json'), 'w'), indent=1)
feats = sorted(EP[0]['feats'])
files = {}
for split, public_labels in [('train', True), ('test', False)]:
    es = [e for e in EP if e['split'] == split]
    ep_p, tel_p, lab_p = (os.path.join(a.out, f'episodes_{"dev" if split == "train" else "test"}.jsonl'),
                          os.path.join(a.out, f'telemetry_{"dev" if split == "train" else "test"}.csv'),
                          os.path.join(a.out if public_labels else a.private, f'labels_{"dev" if split == "train" else "test"}.jsonl'))
    with open(ep_p, 'w') as fe, open(tel_p, 'w', newline='') as ft, open(lab_p, 'w') as fl:
        w = csv.writer(ft); w.writerow(['episode_id'] + feats)
        for n, e in enumerate(es):
            st = e['st']; i = eid(e, n); ov = st.get('ov')
            fe.write(json.dumps(dict(episode_id=i, query=st['q'], tenant=st['tenant'], k=st['k'],
                                     pipeline_state=cfg_public(st['cfg']),
                                     injected_docs=[dict(d, synthetic=True) for d in (ov['docs'] if ov else [])]), default=jdump) + '\n')
            w.writerow([i] + [e['feats'][k] for k in feats])
            gold = [DOCIDS[g] for g in sorted(st['gold']) if g < len(DOCIDS)] if DOCIDS is not None else sorted(int(g) for g in st['gold'])
            fl.write(json.dumps(dict(episode_id=i, fault=e['fault'], family=FAMILY.get(e['fault'], 'NONE') if e['fault'] != 'NONE' else 'NONE',
                                     group=e['fault'][0] if e['fault'] != 'NONE' else 'NONE', k=st['k'], gold=gold,
                                     clean_hit5=bool(e.get('clean_h5', True))), default=jdump) + '\n')
    for p in (ep_p, tel_p, lab_p): files[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = dict(name='DiagRAG-Bench', version='1.0.0', built_from=dict(checkpoint=os.path.abspath(a.ckpt), code_sha256=a.code_sha),
           files={os.path.basename(p): h for p, h in files.items() if not p.startswith(os.path.abspath(a.private)) and a.private not in p},
           private_test_labels_sha256=[h for p, h in files.items() if a.private in p][0],
           n_episodes={s: sum(e['split'] == s for e in EP) for s in ('train', 'test')}, telemetry_features=feats)
json.dump(man, open(os.path.join(a.out, 'MANIFEST.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in man.items() if k != 'telemetry_features'}, indent=1))

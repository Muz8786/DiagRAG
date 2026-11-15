"""DiagRAG-Bench scorer (v1.0). Pure Python + numpy; no pipeline needed for Track 1.

Track 1 — diagnosis from telemetry. Input: a CSV with columns
    episode_id, p_fault, family
  p_fault : any real-valued score, higher = more likely faulty (fault vs clean)
  family  : predicted repair-equivalence class (see families.json), or NONE
Metrics: fault-vs-clean AUROC with 95% bootstrap CI, detection rate at 5% false-alarm on clean episodes,
family accuracy on faulted episodes, clean false-alarm rate of the family prediction.

Track 2 — repair. Input: a CSV with columns
    episode_id, top5            (top5 = space-separated doc_ids after the submitted system ran on the episode)
Metrics: rescue rate on faulted episodes (Hit@k, k per episode), clean Hit@5 loss on clean episodes, net change.

Usage:  python score.py --labels labels_dev.jsonl --track1 my_track1.csv [--track2 my_track2.csv]
The private test labels are not public; their SHA-256 is in MANIFEST.json so results on them can be verified later.
"""
import argparse, csv, json, sys
import numpy as np


def auroc(y, s):
    y = np.asarray(y, int); s = np.asarray(s, float); pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0: return float('nan')
    order = np.argsort(np.concatenate([pos, neg]), kind='mergesort'); ranks = np.empty(len(order)); ranks[order] = np.arange(1, len(order) + 1)
    allv = np.concatenate([pos, neg])
    for v in np.unique(allv):                       # average ranks for ties
        m = allv == v; ranks[m] = ranks[m].mean()
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def boot(y, s, n=1000, seed=0):
    r = np.random.default_rng(seed); y = np.asarray(y); s = np.asarray(s); out = []
    for _ in range(n):
        i = r.integers(0, len(y), len(y))
        if len(set(y[i])) == 2: out.append(auroc(y[i], s[i]))
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def load_labels(p):
    return {j['episode_id']: j for j in map(json.loads, open(p, encoding='utf-8'))}


def track1(lab, path):
    rows = {r['episode_id']: r for r in csv.DictReader(open(path, encoding='utf-8'))}
    miss = [e for e in lab if e not in rows]
    if miss: sys.exit(f'track1: {len(miss)} episodes missing a prediction (e.g. {miss[:3]})')
    ids = sorted(lab); y = [int(lab[e]['fault'] != 'NONE') for e in ids]; s = [float(rows[e]['p_fault']) for e in ids]
    a = auroc(y, s); lo, hi = boot(y, s)
    clean = np.array([float(rows[e]['p_fault']) for e in ids if lab[e]['fault'] == 'NONE'])
    thr = float(np.quantile(clean, 0.95)) if len(clean) else float('inf')
    faulted = [e for e in ids if lab[e]['fault'] != 'NONE']
    det = float(np.mean([float(rows[e]['p_fault']) >= thr for e in faulted])) if faulted else float('nan')
    fam_acc = float(np.mean([rows[e]['family'] == lab[e]['family'] for e in faulted])) if faulted else float('nan')
    fa = float(np.mean([rows[e]['family'] != 'NONE' for e in ids if lab[e]['fault'] == 'NONE']))
    per_fam = {}
    for e in faulted:
        per_fam.setdefault(lab[e]['family'], []).append(rows[e]['family'] == lab[e]['family'])
    return dict(n=len(ids), auroc=a, auroc_ci=[lo, hi], detect_rate_at_5pct_false_alarm=det, family_accuracy=fam_acc,
                family_false_alarm_on_clean=fa, family_accuracy_by_family={k: float(np.mean(v)) for k, v in sorted(per_fam.items())})


def track2(lab, path):
    rows = {r['episode_id']: r['top5'].split() for r in csv.DictReader(open(path, encoding='utf-8'))}
    res, clean_loss, clean_n = {}, 0, 0
    for e, j in lab.items():
        if e not in rows: sys.exit(f'track2: missing {e}')
        hit = any(d in set(j['gold']) for d in rows[e][:j['k']])
        if j['fault'] == 'NONE':
            clean_n += 1; clean_loss += int(j.get('clean_hit5', True) and not hit)
        else: res.setdefault(j['fault'], []).append(hit)
    return dict(rescue_rate_by_fault={k: float(np.mean(v)) for k, v in sorted(res.items())},
                mean_rescue=float(np.mean([np.mean(v) for v in res.values()])) if res else float('nan'),
                clean_hit5_loss=clean_loss / max(1, clean_n), n_clean=clean_n)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--labels', required=True); ap.add_argument('--track1'); ap.add_argument('--track2')
    a = ap.parse_args(); lab = load_labels(a.labels); out = {}
    if a.track1: out['track1'] = track1(lab, a.track1)
    if a.track2: out['track2'] = track2(lab, a.track2)
    print(json.dumps(out, indent=1))

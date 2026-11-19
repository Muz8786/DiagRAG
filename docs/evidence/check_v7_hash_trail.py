"""Checks the v7 code-hash trail (v9 item V4). Read-only. Run from the repository root:  python docs/evidence/check_v7_hash_trail.py
Verifies, from git history and the committed files, that
 (1) every 'frozen v7 hash is now' entry in the protocol equals the SHA-256 of kaggle/diagrag_v7.py at some commit,
 (2) the LAST entry equals the file in the working tree (the code that produced the stored v7 results),
 (3) the hash stored in kaggle/judged_cpu_run_v7_seed50/JUDGED_PROTOCOL.json equals the FIRST entry (the file is written once, at the first chunk),
 (4) the number of lines that differ between consecutive versions (so the 'four lines' / 'eight lines' statements in D2 and D3 can be seen, not assumed).
It does NOT prove the stored results were produced by the last version; it shows that the record is internally consistent and that the differences are small."""
import difflib, hashlib, json, re, subprocess, sys

sh = lambda cmd: subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True).stdout
proto = open('docs/evidence/v7_composed_protocol.md', encoding='utf-8').read(); entries = re.findall(r'frozen v7 hash is now `([0-9a-f]{64})`', proto)
by_commit = {}
for c in sh('git log --format=%H -- kaggle/diagrag_v7.py').split():
    raw = subprocess.run(['git', 'show', f'{c}:kaggle/diagrag_v7.py'], capture_output=True, check=True).stdout; by_commit[hashlib.sha256(raw).hexdigest()] = (c, raw.decode('utf-8'))
ok = True


def check(name, cond, detail=''):
    global ok; ok &= bool(cond); print(('PASS ' if cond else 'FAIL ') + name + ('  ' + detail if detail else ''))


check('protocol has three entries', len(entries) == 3, str([e[:8] for e in entries]))
for i, e in enumerate(entries): check(f'entry {i + 1} ({e[:8]}) exists in git history', e in by_commit, by_commit[e][0][:8] if e in by_commit else '')
tree = hashlib.sha256(open('kaggle/diagrag_v7.py', 'rb').read()).hexdigest(); check('last entry equals the working-tree file', entries[-1] == tree, tree[:8])
stored = json.load(open('kaggle/judged_cpu_run_v7_seed50/JUDGED_PROTOCOL.json'))['code_sha256']; check('stored JUDGED_PROTOCOL.json hash equals the first entry (written once, at chunk 1)', stored == entries[0], stored[:8])
for a, b in zip(entries, entries[1:]):
    if a in by_commit and b in by_commit:
        d = [l for l in difflib.unified_diff(by_commit[a][1].splitlines(), by_commit[b][1].splitlines(), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
        print(f'  info {a[:8]} -> {b[:8]}: {sum(l[0] == "-" for l in d)} lines removed, {sum(l[0] == "+" for l in d)} lines added')
print('HASH TRAIL:', 'CONSISTENT' if ok else 'INCONSISTENT'); sys.exit(0 if ok else 1)

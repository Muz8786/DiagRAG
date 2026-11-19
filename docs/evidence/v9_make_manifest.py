"""Writes kaggle/judged_v9/INPUTS_MANIFEST.json: every input and frozen file that v9 uses, with size and SHA-256 (files are hashed here; the external inputs carry the sizes and hashes the frozen
script itself asserts, plus the model revisions observed on 19 Nov 2026). Run from the repository root:  python docs/evidence/v9_make_manifest.py"""
import hashlib, json, os, re

sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); ent = lambda p: dict(path=p, bytes=os.path.getsize(p), sha256=sha(p))
def frozen_part(p):
    """Protocols get dated amendments appended after results, so only the pre-registered part (everything before the '## N. Amendments' heading) is hashed."""
    t = open(p, encoding='utf-8').read(); cut = re.search(r'\n## \d+\. Amendments', t); body = t[:cut.start()] if cut else t
    return dict(path=p, frozen_part_bytes=len(body.encode('utf-8')), frozen_part_sha256=hashlib.sha256(body.encode('utf-8')).hexdigest(), note='hash of the text before the Amendments heading; amendments may be appended')


port3 = open('kaggle/diagrag_port3.py', encoding='utf-8').read()
beir = {n: (int(b), h) for n, b, h in re.findall(r"(\w+)=\((\d+), '([0-9a-f]{64})'\)", port3)}
qs = re.search(r"'qspell': dict\(name='([^']+)', size=(\d+), url='([^']+)',\s*sha='([0-9a-f]{64})'", port3)
BEIR_URL = 'https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/%s.zip'
m = dict(
    description='All inputs and frozen files for v9 (docs/evidence/v9_protocol.md). Hashes of repository files are computed when this manifest is written; docs/evidence/v9_verify.py re-checks them.',
    written_utc='2026-11-19', protocol='docs/evidence/v9_protocol.md',
    runs_by_owner=[
        dict(id='P1', notebook='kaggle/DiagRAG_v9_port_nfcorpus.ipynb', dataset='nfcorpus', seed=53, code='kaggle/diagrag_port3.py', settings=dict(N_QUERIES=2500, N_HARD=50, MAX_ATT=2500, N_HARM=20, TIME_BUDGET=36000),
             save_to='kaggle/judged_port3_nfcorpus/', note='one run, no setting changed'),
        dict(id='P2', notebook='kaggle/DiagRAG_v9_port_arguana.ipynb', dataset='arguana', seed=54, code='kaggle/diagrag_port3.py', settings=dict(N_QUERIES=2500, N_HARD=50, MAX_ATT=2500, N_HARM=20, TIME_BUDGET=36000),
             save_to='kaggle/judged_port3_arguana/', note='one run, no setting changed')],
    external_inputs=dict(
        beir_zips={k: dict(url=BEIR_URL % k, bytes=v[0], sha256=v[1], used_by=('P1' if k == 'nfcorpus' else 'P2' if k == 'arguana' else 'port2 judged runs'), redistributed=False) for k, v in beir.items() if k in ('nfcorpus', 'arguana', 'scifact', 'fiqa')},
        webis_qspell_17=dict(url=qs.group(3), bytes=int(qs.group(2)), sha256=qs.group(4), licence='CC BY 4.0', used_by='P1, P2 (real misspelling statistics for Q04)'),
        huggingface_models={'intfloat/e5-small-v2': dict(revision_observed='ffb93f3bd4047442299a41ebb6fa998a38507c52', licence='MIT'),
                            'intfloat/e5-small': dict(revision_observed='e272f3049e853b47cb5ca3952268c6662abda68f', licence='MIT'),
                            'cross-encoder/ms-marco-MiniLM-L-6-v2': dict(revision_observed='233902d25c440f23af6f7d6e94d2946bac0bee0a', licence='Apache-2.0')},
        model_revision_note='The frozen script loads these models by name and does NOT pin a revision, so a later upstream change to a model could change results. The revisions above are the ones observed on 19 Nov 2026 (sandbox smoke run).',
        nltk_data='wordnet and omw-1.4, downloaded by the script at run time (not pinned)'),
    frozen_code={p: ent(p) for p in ['kaggle/diagrag_port2.py', 'kaggle/diagrag_port3.py', 'kaggle/mk_port3.py', 'kaggle/mk_v9_port_notebooks.py', 'kaggle/diagrag_v6.py', 'kaggle/diagrag_v7.py']},
    notebooks={p: ent(p) for p in ['kaggle/DiagRAG_v9_port_nfcorpus.ipynb', 'kaggle/DiagRAG_v9_port_arguana.ipynb', 'kaggle/DiagRAG_v8_kaggle.ipynb', 'kaggle/DiagRAG_v6_kaggle.ipynb']},
    protocols={p: frozen_part(p) for p in ['docs/evidence/v9_protocol.md', 'docs/evidence/v8_protocol.md', 'docs/evidence/v7_composed_protocol.md', 'docs/evidence/v6_protocol.md']},
    analysis_scripts={p: ent(p) for p in ['docs/evidence/v8_audit.py', 'docs/evidence/v8_audit_a3_followup.py', 'docs/evidence/v9_emergent_breakdown.py', 'docs/evidence/check_v7_hash_trail.py', 'docs/evidence/v9_verify.py', 'docs/evidence/v9_port_summary.py', 'docs/evidence/v10_diagnosis.py', 'docs/evidence/v10_multilabel.py']},
    committed_analysis_inputs={p: ent(p) for p in ['kaggle/judged_gpu_v6_seed50/episodes.jsonl', 'kaggle/judged_cpu_run_v6_seed50/episodes.jsonl', 'kaggle/judged_cpu_run_v7_seed50/composed_episodes.jsonl',
                                                     'kaggle/judged_cpu_run_v7_seed50/composed_features.jsonl', 'kaggle/judged_port2_scifact/PORT_VERDICT.json', 'kaggle/judged_port2_fiqa/PORT_VERDICT.json',
                                                     'kaggle/judged_gpu_v8_seed52/episodes.jsonl', 'kaggle/judged_gpu_v8_seed52/VERDICT.json', 'kaggle/judged_gpu_v8_seed52/JUDGED_PROTOCOL.json']
                                    + [f'kaggle/judged_port3_{d}/{n}' for d in ('nfcorpus', 'arguana') for n in ('PORT_PROTOCOL.json', 'PORT_VERDICT.json', 'port_detector_gates.csv', 'port_repair_gates.csv', 'port_solved.csv', 'port_episodes_summary.csv')]},
    committed_analysis_outputs={p: ent(p) for p in ['docs/evidence/v8_audit_v6gpu.json', 'docs/evidence/v8_audit_a3_followup_v6gpu.json', 'docs/evidence/v9_emergent_breakdown_v7.json', 'docs/evidence/check_v7_hash_trail_output.txt', 'docs/evidence/v8_audit_v8gpu.json', 'docs/evidence/v9_port_summary.md', 'docs/evidence/v10_diagnosis_v6_v8.json', 'docs/evidence/v10_multilabel_result.json']},
    environment_observed=dict(note='observed in the sandbox used for the development smoke tests, NOT pinned in the notebooks and NOT Kaggle\'s versions',
                              python='3.11', torch='2.15.0+cpu', sentence_transformers='6.3.0', faiss_cpu='1.16.0', scikit_learn='1.6.1 (audit scripts; the same version the v6 run recorded)', numpy='2.4.6', pandas='3.1.1', nltk='3.10.4'),
    frozen_hashes=dict(diagrag_port2='ec113b047d2f13caa194713e6e71cbbafc730554460cbcd4820acf25a19134e0', diagrag_port3='677a2f38f24a5b0d64849e95930c93ecfd944e28d708753930fde1b2d3a77ada',
                       diagrag_v6='44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a', diagrag_v7='26924b7b6a845435e493308d8bd251207e746002e071e07bff867d1c427be597'),
    not_in_v9=['frontier-LLM arm', 'document-text supervised baseline', 'multi-label dispatcher', 'composed-arm repeat on GPU', 'local open-weight LLM arm', 'full-suite port (Q02, Q09, C2, ShopNova faults)', 'density-matched permutation control', 'benchmark release'])
os.makedirs('kaggle/judged_v9', exist_ok=True); json.dump(m, open('kaggle/judged_v9/INPUTS_MANIFEST.json', 'w'), indent=1); print('wrote kaggle/judged_v9/INPUTS_MANIFEST.json')

"""Generate kaggle/diagrag_v7.py from kaggle/diagrag_v6.py by exact, asserted replacements (docs/evidence/v7_composed_protocol.md).
v7 = v6 + (1) a composed-fault arm (cells in kaggle/v7_cells/) whose episodes never enter the single-fault arms, and (2) an attributor retrained with composed TRAIN rows added.
Nothing about detectors, repairs, gates or bars changes. Usage: python kaggle/mk_v7.py   (writes diagrag_v7.py, prints its SHA-256)"""
import hashlib, os

here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, 'diagrag_v6.py'), encoding='utf-8').read()
gen = open(os.path.join(here, 'v7_cells', 'composed_gen.py'), encoding='utf-8').read().rstrip('\n') + '\n'
ev = open(os.path.join(here, 'v7_cells', 'composed_eval.py'), encoding='utf-8').read().rstrip('\n') + '\n'


def sub(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90])
    s = s.replace(old, new)


sub("# # DiagRAG v6 — v5 + two construction fixes",
    "# # DiagRAG v7 — v6 + a pre-registered composed-fault arm and an attributor retrained with composed TRAIN rows (docs/evidence/v7_composed_protocol.md). Gates, bars, detectors and repairs are unchanged.\n"
    "# The single-fault arms are v6's, resumed from the v6 CPU checkpoint with every attributor-dependent result recomputed, so any difference in them comes from the attributor alone.\n"
    "# ---- v6 header, unchanged below ----\n"
    "# # DiagRAG v6 — v5 + two construction fixes")
sub("'CAL', 'NATR', 'LOFO', 'FAMR', 'NAT2', 'CENS', 'BASEL', 'NAT3')", "'CAL', 'NATR', 'LOFO', 'FAMR', 'NAT2', 'CENS', 'BASEL', 'NAT3', 'COMPST', 'COMPRES')")
sub("log('episodes', collections.Counter(e['fault'] for e in EPIS))\n", "log('episodes', collections.Counter(e['fault'] for e in EPIS))\n\n" + gen)

# attributor: v6 version kept as ATT0 / ATTG0; v7 version adds composed TRAIN rows to every training fit; OOF scored on single-fault rows only
sub("ATT = hgb().fit(Xtra, ytra); CLS = list(ATT.classes_)\n",
    "ATT0 = hgb().fit(Xtra, ytra)                                  # v6 attributor (single-fault rows only), kept for the comparison\n"
    "XC, YC = comp_rows('train'); XCa, YCa = np.vstack([Xtra, XC]), np.concatenate([ytra, YC])   # v7: composed TRAIN rows, one per component, labelled with that component\n"
    "ATT = hgb().fit(XCa, YCa); CLS = list(ATT.classes_); assert CLS == list(ATT0.classes_), 'composed rows changed the class set'\n"
    "log('v7 attributor: single rows', len(ytra), '+ composed train rows', len(YC))\n")
sub("    mm = hgb().fit(Xtra[a_], ytra[a_]); p_ = mm.predict_proba(Xtra[b_])\n    for j, c_ in enumerate(mm.classes_): oof[b_, CLS.index(c_)] = p_[:, j]\n",
    "    mm = hgb().fit(np.vstack([Xtra[a_], XC]), np.concatenate([ytra[a_], YC])); p_ = mm.predict_proba(Xtra[b_])   # composed rows have their own base queries, so no group leaks across folds\n    for j, c_ in enumerate(mm.classes_): oof[b_, CLS.index(c_)] = p_[:, j]\n")
sub("ATTG = hgb().fit(Xtra, to_group(ytra)); GCLS = list(ATTG.classes_)   # v4 group attributor\n",
    "ATTG0 = hgb().fit(Xtra, to_group(ytra))\nATTG = hgb().fit(XCa, to_group(YCa)); GCLS = list(ATTG.classes_)   # v4 group attributor, v7: with composed TRAIN rows\n")
sub("    mm = hgb().fit(Xtra[a_], to_group(ytra[a_])); p_ = mm.predict_proba(Xtra[b_])\n    for j, c_ in enumerate(mm.classes_): oofg[b_, GCLS.index(c_)] = p_[:, j]\n",
    "    mm = hgb().fit(np.vstack([Xtra[a_], XC]), to_group(np.concatenate([ytra[a_], YC]))); p_ = mm.predict_proba(Xtra[b_])\n    for j, c_ in enumerate(mm.classes_): oofg[b_, GCLS.index(c_)] = p_[:, j]\n")
# the v6 attributor's own TAU_C2, for the old-versus-new comparison of set diagnosis
sub("TAU_C2 = float(np.quantile(s_neg, 0.90)) if s_neg else 0.5        # <=10% of single faults get a spurious second repair\n",
    "TAU_C2 = float(np.quantile(s_neg, 0.90)) if s_neg else 0.5        # <=10% of single faults get a spurious second repair\n"
    "oof0 = np.zeros((len(TRA), len(CLS)))                              # v7: the v6 attributor's out-of-fold scores, only to recover its TAU_C2 for the comparison\n"
    "for a_, b_ in GroupKFold(5).split(Xtra, ytra, [e['bid'] for e in TRA]):\n"
    "    mm = hgb().fit(Xtra[a_], ytra[a_]); p_ = mm.predict_proba(Xtra[b_])\n"
    "    for j, c_ in enumerate(mm.classes_): oof0[b_, CLS.index(c_)] = p_[:, j]\n"
    "TAU_C2_0 = float(np.quantile([sec(p) for p, y_ in zip(oof0, ytra) if y_ != 'NONE'], 0.90))\n")
sub("log('LOOP GATES', GUARANTEE); save_ckpt('loop_done')\n", "log('LOOP GATES', GUARANTEE); save_ckpt('loop_done')\n\n" + ev)
sub("md = ['# DiagRAG v6 judged run report',", "md = ['# DiagRAG v7 judged run report',")
sub("               guarantee=GUARANTEE, policies=POLICY,", "               composed_arm=dict(result_file='COMPOSED_RESULT.json', headline=COMPRES_SUMMARY['headline']), guarantee=GUARANTEE, policies=POLICY,")
out = os.path.join(here, 'diagrag_v7.py'); open(out, 'w', encoding='utf-8').write(s); print('wrote', out, hashlib.sha256(s.encode('utf-8')).hexdigest())

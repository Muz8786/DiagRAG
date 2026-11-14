"""Build <name>.ipynb from <name>.py (cells split on '# %%' markers).
Usage: python kaggle/build_notebook.py [diagrag_core28 diagrag_v2 diagrag_port]"""
import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
for name in (sys.argv[1:] or ['diagrag_core28', 'diagrag_v2', 'diagrag_port']):
  src = open(os.path.join(here, name + '.py'), encoding='utf-8').read()
  cells = []
  for block in re.split(r'^# %%', src, flags=re.M)[1:]:
      is_md = block.startswith(' [markdown]')
      body = block.split('\n', 1)[1] if '\n' in block else ''
      body = body.strip('\n')
      if is_md:
          text = '\n'.join(l[2:] if l.startswith('# ') else l.lstrip('#') for l in body.splitlines())
          cells.append(dict(cell_type='markdown', metadata={}, source=text.splitlines(True)))
      else:
          cells.append(dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=body.splitlines(True)))
  nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
            metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'),
                          language_info=dict(name='python'), kaggle=dict(accelerator='gpu', isInternetEnabled=True)))
  out = os.path.join(here, name + '.ipynb')
  json.dump(nb, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
  print('wrote', out, len(cells), 'cells')

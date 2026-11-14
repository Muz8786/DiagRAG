"""Build diagrag_core28.ipynb from diagrag_core28.py (cells split on '# %%' markers).
Usage: python kaggle/build_notebook.py"""
import json, os, re
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'diagrag_core28.py'), encoding='utf-8').read()
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
out = os.path.join(here, 'diagrag_core28.ipynb')
json.dump(nb, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', out, len(cells), 'cells')

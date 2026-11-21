"""Search GitHub issues (REST search API) for retrieval-failure evidence; save raw hits to JSON."""
import json, subprocess, sys, time, urllib.parse
Q = json.load(open(sys.argv[1]))
out = {}
for tag, q in Q.items():
    url = 'search/issues?per_page=8&sort=comments&order=desc&q=' + urllib.parse.quote('is:issue ' + q)
    r = subprocess.run(['gh', 'api', url], capture_output=True, text=True)
    if r.returncode:
        print(tag, 'ERR', r.stderr[:200]); time.sleep(3); continue
    items = json.loads(r.stdout).get('items', [])
    out[tag] = [dict(title=i['title'], url=i['html_url'], state=i['state'], comments=i['comments'],
                     created=i['created_at'][:10], body=(i.get('body') or '')[:1500]) for i in items]
    print(f'== {tag}  ({q})  total={json.loads(r.stdout).get("total_count")}')
    for i in out[tag]: print(f"   [{i['created']}] c={i['comments']:>3} {i['title'][:110]}  {i['url']}")
    time.sleep(2.2)
json.dump(out, open(sys.argv[2], 'w'), indent=1)

import json,sys,hashlib
F='/home/li/.claude/projects/-home-li-primary/6997eb8a-30eb-49a1-a787-45279164a43b.jsonl'
lines=open(F).read().split('\n')
r=json.loads(lines[595])
assert r['uuid']=='febc34a6-1dea-42ca-99a0-616b1907ca5c'
t=''.join(c['text'] for c in r['message']['content'] if c.get('type')=='text')
i=t.index('## Your questions since 28 September')
rest=t[i:]
# end at next rule (line consisting of ---) or end
import re
m=re.search(r'\n(---|\*\*\*|___)\s*\n',rest) or re.search(r'\n=== End ===',rest)
src=rest[:m.start()+1] if m else rest
open('/home/li/primary/flows/bd0019/books-questions/source.md','w').write(src)
print(hashlib.sha256(src.encode()).hexdigest(), len(src), 'rule' if m else 'end-of-record')

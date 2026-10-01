import json,glob,sys
sys.path.insert(0,'.')
from quotes import QUOTES
def words(f,n):
    if f.startswith('CODEX:'):
        f=glob.glob('/home/li/.codex*/**/'+f[6:],recursive=True)[0]
    r=json.loads(open(f).read().split('\n')[n-1])
    if r.get('type')=='queue-operation': return 'user(queued)',r['content'],r.get('timestamp')
    if 'payload' in r:
        p=r['payload']; assert p.get('role')=='user'
        return 'user',''.join(c.get('text','') for c in p['content']),r.get('timestamp')
    assert r['type']=='user'
    c=r['message']['content']
    if isinstance(c,list): c=''.join(x.get('text','') for x in c if x.get('type')=='text')
    return 'user',c,r.get('timestamp')
ok=True
for k,q in QUOTES.items():
    role,t,ts=words(q['file'],q['line'])
    hit=q['text'] in t
    ok&=hit
    print(('OK  ' if hit else 'FAIL'),k,role,ts)
print('ALL QUOTES VERBATIM' if ok else 'QUOTE FAILURE'); sys.exit(0 if ok else 1)

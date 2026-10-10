# Verify a book HTML file (local or read back): every source block present verbatim, every living quote verbatim,
# title exact, no <button>, no <pre>. Usage: verify_book.py <html> [<html2> for checksum compare]
import sys,re,html,hashlib
sys.path.insert(0,'/home/li/primary/flows/bd0019/books-questions')
from quotes import QUOTES
D='/home/li/primary/flows/bd0019/books-questions/'
src=open(D+'source.md').read()
h=open(sys.argv[1]).read()
def plain(s): return html.unescape(re.sub(r'<[^>]+>','',s))
def md_plain(s): return re.sub(r'\*\*([^*]+)\*\*',r'\1',re.sub(r'`([^`]+)`',r'\1',s))
got=[plain(m[1]) for m in re.findall(r'<(p|li|span)[^>]*data-src[^>]*>(.*?)</\1>',h,re.S)]
need=[]
para=[]
for l in src.split('\n'):
    if l.startswith('## '): need.append(l[3:]); continue
    m=re.match(r'^\d+\. (.*)$',l)
    if m: need.append(md_plain(m.group(1))); continue
    if l.strip(): need.append(md_plain(l))
ok=True
heads=[plain(x) for x in re.findall(r'<h[12][^>]*>(.*?)</h[12]>',h,re.S)]
for n in need:
    if n not in got and n not in heads: ok=False; print('MISSING source block:',n[:70])
texts={q['text'] for q in QUOTES.values()}
lq=re.findall(r'data-living="([a-z]+)">(.*?)</p>',h,re.S)
for k,t in lq:
    if plain(t)!=QUOTES[k]['text']: ok=False; print('QUOTE MISMATCH',k)
nq=[plain(x) for n in re.findall(r'<aside class="note.*?</aside>',h,re.S) for x in re.findall(r'«(.*?)»',n)]
for t in nq:
    if t not in texts: ok=False; print('NOTE QUOTE NOT VERBATIM',t[:60])
print('living quotes',len(lq),'note quotes',len(nq))
if '<title>Your questions since 28 September</title>' not in h: ok=False; print('TITLE')
if re.search(r'<button|<pre',h): ok=False; print('BUTTON/PRE present')
print('source blocks',len(need),'found; quotes',len(QUOTES),'| sha256',hashlib.sha256(h.encode()).hexdigest())
if len(sys.argv)>2:
    h2=open(sys.argv[2]).read(); same=h2==h; ok&=same; print('read-back identical:',same, hashlib.sha256(h2.encode()).hexdigest())
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)

import re, html, json
SRC = open('source.md').read()
lines = SRC.split('\n')
title_line = lines[0]
preface = lines[2]
# split pages
sections = re.split(r'\n## (Page \d+ · [^\n]+)\n', SRC)
head, rest = sections[0], sections[1:]
pages = [(rest[i], rest[i+1].strip('\n')) for i in range(0, len(rest), 2)]
assert len(pages) == 14, len(pages)
# last page body contains the page-design paragraph
last_head, last_body = pages[-1]
qpart, design = last_body.split('\n\n**Page design.**')
design = '**Page design.**' + design
pages[-1] = (last_head, qpart)

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'\b(unknown|UNKNOWN)\b', r'<span class="unk">\1</span>', t)
    return t

ILL = {1:'p01',3:'p03',5:'p05',7:'p07',9:'p09',11:'p11',13:'p13'}
def svg(name): return open(f'ill/{name}.svg').read()

def ill_page(n, heading, body):
    return f'''<section class="page ill" id="p{n}" hidden aria-label="{html.escape(heading)}">
<div class="art">{svg(ILL[n])}</div>
<div class="cap"><p class="eyebrow">{html.escape(heading)}</p><p class="captext">{inline(body)}</p></div>
</section>'''

def paras(body):
    out=[]; items=[]
    for ln in body.split('\n'):
        if ln.startswith('- '):
            items.append(f'<li>{inline(ln[2:])}</li>')
        elif ln.strip()=='' :
            if items: out.append('<ul>'+''.join(items)+'</ul>'); items=[]
        else:
            if items: out.append('<ul>'+''.join(items)+'</ul>'); items=[]
            out.append(f'<p>{inline(ln)}</p>')
    if items: out.append('<ul>'+''.join(items)+'</ul>')
    return '\n'.join(out)

def text_page(n, heading, inner, extra_cls=''):
    label, _, name = heading.partition(' · ')
    return f'''<section class="page text {extra_cls}" id="p{n}" hidden aria-label="{html.escape(heading)}">
<div class="prose">
<p class="eyebrow">{html.escape(label)}</p>
<h2>{html.escape(name)}</h2>
{inner}
</div>
</section>'''

NOTE = lambda t: f'<aside class="note"><span class="note-k">Renderer’s note, not source</span> {t}</aside>'

out=[]
for idx,(h,b) in enumerate(pages, start=1):
    if idx in ILL:
        out.append(ill_page(idx,h,b)); continue
    if idx==2:
        m = re.search(r'```mermaid\n(.*?)```', b, re.S)
        prose = b[:m.start()].strip()
        inner = (f'<p class="preface">{inline(preface)}</p>\n' + paras(prose) +
          f'\n<figure class="flow">{svg("flow")}</figure>\n<details class="src"><summary>The flowchart as written (mermaid)</summary><pre><code>{html.escape(m.group(1))}</code></pre></details>')
        out.append(text_page(idx,h,inner)); continue
    if idx==6:
        blines=b.split('\n')
        intro=[l for l in blines if l and not l.startswith('- ')]
        cards=[]
        for l in blines:
            if not l.startswith('- '): continue
            mm=re.match(r'- \*\*(.+?)\*\* (.*)', l)
            name, rest_ = mm.group(1), mm.group(2)
            body=inline(rest_)
            body=re.sub(r'(^|(?<=\. ))(Source:|Source|Compiled:|Running, proven:|Running:|Proven:|Installed:)', r'<span class="g">\2</span>', body)
            cards.append(f'<article class="card"><h3>{inline(name)}</h3>\n<p>{body}</p></article>')
        inner=''.join(f'<p>{inline(l)}</p>' for l in intro)+'<div class="cards">'+''.join(cards)+'</div>'
        out.append(text_page(idx,h,inner,'catalog')); continue
    if idx==12:
        inner=paras(b)+NOTE('The Sol addendum time, Tuesday 14:34 UTC, is given without its local time; at the UTC−6 offset the source uses elsewhere it is 08:34 local.')
        out.append(text_page(idx,h,inner)); continue
    if idx==14:
        status = {
         'SW1':('open','Witnessed on ouranos, 2026-09-23: orchestrate-nexus still runs the orchestrate-0.35.0 store path and lojix.service is still active, both up since 2026-09-12; flow-nexus.service was restarted Tuesday 2026-09-22 at 13:19 local (19:19 UTC) from an unversioned binary path; message-daemon.service is now failed. Not landed. Whether the Flow restart ran a known revision was not established.'),
         'SW5':('open','Witnessed 2026-09-23: primary’s flake.lock still pins curriculum at 9940910. Not landed.'),
        }
        qs=[]
        for l in b.split('\n'):
            mm=re.match(r'- (SW\d)\. (.*)', l)
            if not mm: continue
            q, t = mm.groups()
            st = status.get(q, ('unknown','State not established cheaply; left unbadged.'))
            badge = '<span class="badge landed">landed</span>' if st[0]=='landed' else ''
            qs.append(f'''<li class="q" id="{q}"><input type="checkbox" id="chk-{q}" aria-label="Mark {q} as settled"><label for="chk-{q}"><span class="qn">{q}.</span> {inline(t)}</label>{badge}<p class="qstate"><span class="note-k">Checked, not source</span> {st[1]}</p></li>''')
        inner=('<ol class="qs">'+''.join(qs)+'</ol>'+
          NOTE('No proposal could be witnessed as landed at render time, so none carries a landed badge. The checkboxes are yours; they remember only in this browser.')+
          f'<details class="src"><summary>The source’s page-design note</summary><p>{inline(design)}</p></details>'+
          '<footer class="colophon"><p>Source: Psyche High 1b8ac0, assistant text at transcript record line 2435, 2026-09-22T14:42:23.665Z (08:42 local), taken verbatim from its heading, “'+html.escape(title_line[2:])+'”, to the end of the message; no closing rule follows it. The source asks this footer to cite the reports by flow and title with short revisions; it names none, so none are cited here.</p></footer>')
        out.append(text_page(idx,h,inner,'questions')); continue
    out.append(text_page(idx,h,paras(b)))

tpl=open('shell.html').read()
page=tpl.replace('%%PAGES%%','\n'.join(out))
open('index.html','w').write(page)
open('preview.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+page+'</body></html>')

# verbatim check
txt=re.sub(r'<svg.*?</svg>','',page,flags=re.S)
txt=re.sub(r'<(script|style)[^>]*>.*?</\1>','',txt,flags=re.S)
txt=html.unescape(re.sub(r'<[^>]+>','',txt))
txt=re.sub(r'\s+',' ',txt)
miss=0
for ln in SRC.split('\n'):
    s=ln.strip()
    if not s or s.startswith('```') : continue
    if s.startswith('## Page'):
        a,_,b=s[3:].partition(' · ')
        if a not in txt or b not in txt: miss+=1; print('MISSING head',s)
        continue
    s=re.sub(r'^(#+ |- )','',s).replace('**','')
    if s.startswith('*') and s.endswith('*'): s=s[1:-1]
    s=re.sub(r'\s+',' ',s)
    if s not in txt:
        miss+=1; print('MISSING:',s[:90])
print('pages',len(out),'missing',miss)

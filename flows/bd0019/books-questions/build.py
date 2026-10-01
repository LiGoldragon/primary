#!/usr/bin/env python3
"""Build the flashbook «Your questions since 28 September» from source.md.
Source text is copied by script (extract.py) and rendered without edits."""
import html, re, random, math, sys
sys.path.insert(0, '/home/li/primary/flows/bd0019/books-questions')
from quotes import QUOTES

D = '/home/li/primary/flows/bd0019/books-questions/'
SRC = open(D + 'source.md').read()
TITLE = 'Your questions since 28 September'


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    return s


# ---- split the source into its blocks, by heading
sections = {}
cur = None
for line in SRC.split('\n'):
    if line.startswith('## '):
        cur = line[3:]
        sections[cur] = []
    elif cur is not None:
        sections[cur].append(line)


def blocks(name):
    out, para = [], []
    for l in sections[name]:
        m = re.match(r'^(\d+)\. (.*)$', l)
        if m:
            if para: out.append(('p', ' '.join(para))); para = []
            out.append(('li', m.group(1), m.group(2)))
        elif l.strip() == '':
            if para: out.append(('p', ' '.join(para))); para = []
        else:
            para.append(l)
    if para: out.append(('p', ' '.join(para)))
    return out


def render(bl, cls='src'):
    h, inlist = [], False
    for b in bl:
        if b[0] == 'li':
            if not inlist: h.append(f'<ol class="{cls}-list">'); inlist = True
            h.append(f'<li value="{b[1]}" data-src>{inline(b[2])}</li>')
        else:
            if inlist: h.append('</ol>'); inlist = False
            h.append(f'<p class="{cls}" data-src>{inline(b[1])}</p>')
    if inlist: h.append('</ol>')
    return '\n'.join(h)


def quote(k):
    q = QUOTES[k]
    return (f'<blockquote class="living"><p data-living="{k}">{html.escape(q["text"], quote=False)}</p>'
            f'<footer>Your words · {q["prov"]}</footer></blockquote>')


def note(kind, body):
    label = {'agree': 'Psyche Sonnet agrees', 'tension': 'Psyche Sonnet doubts'}[kind]
    return f'<aside class="note {kind}"><span class="nlabel">{label}</span><p>{body}</p></aside>'


SECS = list(sections)
assert SECS == ['Your questions since 28 September', 'Proposed answers to 8',
                'Proposed skill lines', 'Rulings'], SECS
intro = blocks(SECS[0])
intro_p = [b for b in intro if b[0] == 'p']
intro_li = [b for b in intro if b[0] == 'li']
assert len(intro_p) == 1 and len(intro_li) == 8

# ---------------------------------------------------------------- illustrations
rnd = random.Random(28)


def lantern(x, y, s, lit, uid, alpha=1.0):
    """A paper lantern hanging at (x,y) top, scale s."""
    body = f'url(#lit{uid})' if lit else 'var(--paper)'
    stroke = 'var(--accent)' if lit else 'var(--ink-soft)'
    g = []
    if lit:
        g.append(f'<circle cx="{x:.1f}" cy="{y+11*s:.1f}" r="{20*s:.1f}" style="fill:url(#halo{uid})"/>')
    g.append(f'<path d="M{x-6*s:.1f},{y+3*s:.1f} C{x-11*s:.1f},{y+8*s:.1f} {x-11*s:.1f},{y+15*s:.1f} {x-6*s:.1f},{y+20*s:.1f} '
             f'L{x+6*s:.1f},{y+20*s:.1f} C{x+11*s:.1f},{y+15*s:.1f} {x+11*s:.1f},{y+8*s:.1f} {x+6*s:.1f},{y+3*s:.1f} Z" '
             f'style="fill:{body};stroke:{stroke};stroke-width:{max(0.8,1.1*s):.2f}"/>')
    g.append(f'<path d="M{x:.1f},{y+3*s:.1f} C{x-4*s:.1f},{y+9*s:.1f} {x-4*s:.1f},{y+14*s:.1f} {x:.1f},{y+20*s:.1f}" '
             f'style="fill:none;stroke:{stroke};stroke-width:{0.6*s:.2f};opacity:.6"/>')
    g.append(f'<rect x="{x-4*s:.1f}" y="{y:.1f}" width="{8*s:.1f}" height="{3.2*s:.1f}" rx="{1*s:.1f}" style="fill:var(--ink)"/>')
    g.append(f'<rect x="{x-4*s:.1f}" y="{y+19.5*s:.1f}" width="{8*s:.1f}" height="{2.6*s:.1f}" rx="{1*s:.1f}" style="fill:var(--ink)"/>')
    return f'<g opacity="{alpha}">' + ''.join(g) + '</g>'


def defs(uid):
    return f'''<defs>
<linearGradient id="sky{uid}" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" style="stop-color:var(--sky1)"/><stop offset="1" style="stop-color:var(--sky2)"/></linearGradient>
<radialGradient id="lit{uid}" cx=".5" cy=".55" r=".6">
 <stop offset="0" style="stop-color:var(--glow-core)"/><stop offset=".6" style="stop-color:var(--glow)"/><stop offset="1" style="stop-color:var(--accent)"/></radialGradient>
<radialGradient id="halo{uid}" cx=".5" cy=".5" r=".5">
 <stop offset="0" style="stop-color:var(--glow);stop-opacity:.55"/><stop offset="1" style="stop-color:var(--glow);stop-opacity:0"/></radialGradient>
<linearGradient id="hill{uid}" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" style="stop-color:var(--hill1)"/><stop offset="1" style="stop-color:var(--hill2)"/></linearGradient>
</defs>'''


def svg(uid, inner, label):
    return (f'<svg class="ill" viewBox="0 0 400 760" preserveAspectRatio="xMidYMid slice" role="img" '
            f'aria-label="{html.escape(label)}">{defs(uid)}'
            f'<rect width="400" height="760" style="fill:url(#sky{uid})"/>{inner}</svg>')


def stars(n):
    return ''.join(f'<circle cx="{rnd.uniform(5,395):.1f}" cy="{rnd.uniform(5,330):.1f}" r="{rnd.uniform(.5,1.5):.1f}" '
                   f'style="fill:var(--star);opacity:{rnd.uniform(.3,.9):.2f}"/>' for _ in range(n))


def hills():
    return ('<path d="M0,600 C80,560 150,585 220,570 C290,555 340,575 400,560 L400,760 L0,760Z" style="fill:var(--hill1);opacity:.7"/>'
            '<path d="M0,650 C70,620 160,660 250,640 C320,625 360,640 400,630 L400,760 L0,760Z" style="fill:url(#hillA)"/>')


def ill_cover():
    uid = 'A'
    g = [stars(70), hills().replace('hillA', 'hill' + uid)]
    # 100 lanterns on five drooping strings: 33 lit, 65 unlit, 2 drifting away
    idx = list(range(98))
    lit = set(rnd.sample(idx, 33))
    rows = [(250, 22), (330, 22), (410, 20), (490, 18), (565, 16)]
    k = 0
    for ri, (yb, n) in enumerate(rows):
        sag = 26 + ri * 3
        pts = []
        for i in range(n):
            t = (i + .5) / n
            x = 14 + t * 372
            y = yb + sag * math.sin(math.pi * t) + (ri % 2) * 4
            pts.append((x, y))
        d = 'M0,%.1f ' % (yb - 6) + ' '.join(f'L{x:.1f},{y:.1f}' for x, y in pts) + f' L400,{yb-6:.1f}'
        g.append(f'<path d="{d}" style="fill:none;stroke:var(--ink-soft);stroke-width:.7;opacity:.55"/>')
        for x, y in pts:
            if k >= 98: break
            s = .62 + ri * .06
            g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+3:.1f}" style="stroke:var(--ink-soft);stroke-width:.6"/>')
            g.append(lantern(x, y + 3, s, k in lit, uid))
            k += 1
    # the two superseded, loosed and rising
    g.append(lantern(300, 150, .8, False, uid, .45))
    g.append(lantern(330, 112, .7, False, uid, .3))
    g.append('<path d="M300,172 C292,200 312,215 304,240" style="fill:none;stroke:var(--ink-soft);stroke-width:.6;stroke-dasharray:2 3;opacity:.5"/>')
    g.append('<text x="50" y="92" class="svgt" style="font-size:34px">Your questions</text>'
             '<text x="50" y="132" class="svgt it" style="font-size:26px">since 28 September</text>'
             '<text x="50" y="712" class="svgl" style="font-size:14px">33 lit · 65 waiting · 2 let go</text>')
    return svg(uid, ''.join(g), 'One hundred paper lanterns strung across a dusk sky: thirty-three lit, sixty-five unlit, two drifting away.')


def ill_eight():
    uid = 'B'
    g = [stars(50), hills().replace('hillA', 'hill' + uid)]
    # a bowed branch carrying eight heavy unlit lanterns
    g.append('<path d="M-10,180 C80,150 180,200 260,250 C320,288 370,300 420,330 L420,342 C368,314 318,302 256,264 C176,214 82,166 -10,196Z" style="fill:var(--bark)"/>')
    for (x, y, r) in [(60, 168, 18), (140, 178, 14), (220, 222, 16), (300, 270, 15), (360, 300, 12)]:
        g.append(f'<path d="M{x},{y} C{x+r},{y-r*1.6} {x+r*2.2},{y-r*.6} {x+r*2},{y-r*.1} C{x+r*1.4},{y+r*.3} {x+r*.5},{y+r*.2} {x},{y}Z" style="fill:var(--leaf);opacity:.85"/>')
    xs = [(52, 180), (94, 175), (136, 183), (178, 200), (220, 222), (260, 249), (300, 272), (340, 292)]
    for i, (x, y) in enumerate(xs):
        ln = 120 + (i % 3) * 38 + i * 6
        g.append(f'<path d="M{x},{y} C{x+3},{y+ln*.4} {x-3},{y+ln*.7} {x},{y+ln}" style="fill:none;stroke:var(--ink-soft);stroke-width:.9"/>')
        g.append(lantern(x, y + ln, 1.55, False, uid))
        g.append(f'<text x="{x}" y="{y+ln+21}" text-anchor="middle" class="svgl" style="font-size:14px">{i+1}</text>')
    g.append('<text x="50" y="92" class="svgt" style="font-size:30px">Eight, pressed hardest</text>'
             '<text x="50" y="124" class="svgl" style="font-size:16px">still unlit</text>')
    return svg(uid, ''.join(g), 'A branch bowed under eight heavy unlit lanterns, numbered one to eight.')


def ill_phone():
    uid = 'C'
    g = [stars(25), hills().replace('hillA', 'hill' + uid)]
    # an oversized page sliding off sideways, faded
    g.append('<g transform="rotate(-8 200 380)" opacity=".35">'
             '<rect x="20" y="210" width="520" height="330" rx="10" style="fill:var(--paper);stroke:var(--ink-soft);stroke-width:1.5"/>')
    for i in range(9):
        g.append(f'<rect x="48" y="{246+i*30}" width="{460-(i%3)*60}" height="9" rx="4" style="fill:var(--ink-soft);opacity:.5"/>')
    g.append('</g>')
    # pinch fingers, frustrated
    g.append('<path d="M330,520 C350,470 372,452 392,446" style="fill:none;stroke:var(--tension);stroke-width:6;stroke-linecap:round;opacity:.75"/>'
             '<path d="M318,560 C340,560 372,570 396,590" style="fill:none;stroke:var(--tension);stroke-width:6;stroke-linecap:round;opacity:.75"/>')
    # the upright phone, held, its page fitting
    g.append('<path d="M110,640 C96,600 104,560 124,540 L276,540 C296,560 304,600 290,640Z" style="fill:var(--skin)"/>')
    g.append('<rect x="128" y="200" width="144" height="300" rx="22" style="fill:var(--ink)"/>'
             '<rect x="136" y="214" width="128" height="272" rx="14" style="fill:var(--paper)"/>')
    for i in range(8):
        w = [96, 104, 88, 100, 70, 104, 92, 60][i]
        g.append(f'<rect x="148" y="{250+i*18}" width="{w}" height="6" rx="3" style="fill:var(--ink-soft)"/>')
    g.append('<circle cx="160" cy="232" r="7" style="fill:var(--accent)"/>'
             '<rect x="146" y="408" width="108" height="56" rx="8" style="fill:none;stroke:var(--accent);stroke-width:1.5;stroke-dasharray:3 3"/>'
             '<text x="200" y="441" text-anchor="middle" class="svgl" style="font-size:13px">comment</text>')
    g.append('<path d="M118,560 C108,520 116,470 132,452" style="fill:none;stroke:var(--skin);stroke-width:16;stroke-linecap:round"/>'
             '<path d="M282,560 C292,520 284,480 270,462" style="fill:none;stroke:var(--skin);stroke-width:14;stroke-linecap:round"/>')
    g.append('<text x="50" y="92" class="svgt" style="font-size:30px">Upright, in one hand</text>'
             '<text x="50" y="124" class="svgl" style="font-size:16px">no zoom, no sideways</text>')
    return svg(uid, ''.join(g), 'An upright phone held in one hand, its page fitting; behind it an oversized page slides off sideways.')


def ill_three():
    uid = 'D'
    g = [stars(30)]
    # the voice at the top, a spoken wave
    g.append('<path d="M60,180 C90,150 110,210 140,180 C170,150 190,210 220,180 C250,150 270,210 300,180 C320,162 330,170 340,176" '
             'style="fill:none;stroke:var(--ink);stroke-width:3;stroke-linecap:round"/>'
             '<text x="200" y="146" text-anchor="middle" class="svgl" style="font-size:16px">when you speak</text>')
    # three fat hand-coloured streams
    streams = [('M200,196 C160,260 92,300 90,430', 'var(--accent)'),
               ('M200,196 C200,280 202,340 200,430', 'var(--mind)'),
               ('M200,196 C240,260 308,300 310,430', 'var(--field)')]
    for d, c in streams:
        g.append(f'<path d="{d}" style="fill:none;stroke:{c};stroke-width:22;stroke-linecap:round;opacity:.28"/>'
                 f'<path d="{d}" style="fill:none;stroke:{c};stroke-width:9;stroke-linecap:round"/>')
    for x, c in [(90, 'var(--accent)'), (200, 'var(--mind)'), (310, 'var(--field)')]:
        g.append(f'<path d="M{x-16},{424} L{x},{452} L{x+16},{424}Z" style="fill:{c}"/>')
    # psyche: a lantern bowl
    g.append(lantern(90, 470, 2.6, True, uid))
    # mind: an open book with a question curl
    g.append('<path d="M150,520 C170,508 192,510 200,520 C208,510 230,508 250,520 L250,580 C230,570 208,572 200,582 C192,572 170,570 150,580Z" '
             'style="fill:var(--paper);stroke:var(--mind);stroke-width:2.5"/>'
             '<path d="M200,520 L200,582" style="stroke:var(--mind);stroke-width:1.5"/>'
             '<text x="176" y="560" text-anchor="middle" class="svgt" style="font-size:24px;fill:var(--mind)">?</text>')
    # field: the machine body, a warm stone with a heart of gears
    g.append('<path d="M266,580 C256,540 276,505 310,500 C346,496 366,530 358,566 C352,592 286,600 266,580Z" style="fill:var(--hill1);stroke:var(--field);stroke-width:2.5"/>')
    cx, cy = 312, 548
    teeth = ''.join(f'<rect x="{cx-3}" y="{cy-22}" width="6" height="8" rx="1" transform="rotate({a} {cx} {cy})" style="fill:var(--field)"/>' for a in range(0, 360, 40))
    g.append(teeth + f'<circle cx="{cx}" cy="{cy}" r="15" style="fill:var(--field)"/><circle cx="{cx}" cy="{cy}" r="6" style="fill:var(--hill1)"/>')
    g.append('<text x="90" y="640" text-anchor="middle" class="svgt" style="font-size:20px">psyche</text>'
             '<text x="200" y="640" text-anchor="middle" class="svgt" style="font-size:20px">mind</text>'
             '<text x="310" y="640" text-anchor="middle" class="svgt" style="font-size:20px">field</text>'
             '<text x="90" y="662" text-anchor="middle" class="svgl" style="font-size:14px">what you</text><text x="90" y="680" text-anchor="middle" class="svgl" style="font-size:14px">want</text>'
             '<text x="200" y="662" text-anchor="middle" class="svgl" style="font-size:14px">what must</text><text x="200" y="680" text-anchor="middle" class="svgl" style="font-size:14px">be known</text>'
             '<text x="310" y="662" text-anchor="middle" class="svgl" style="font-size:14px">the body</text><text x="310" y="680" text-anchor="middle" class="svgl" style="font-size:14px">as it is</text>')
    g.append('<text x="50" y="72" class="svgt" style="font-size:30px">Three logs</text>')
    return svg(uid, ''.join(g), 'Your spoken word flowing in three thick streams into a lit lantern (psyche), an open book with a question mark (mind), and a stone with a gear heart (field).')


def ill_letter():
    uid = 'E'
    g = [stars(30), hills().replace('hillA', 'hill' + uid)]
    # chatter falling away: faint broken lines drifting down and out
    for i in range(26):
        x = rnd.uniform(10, 390); y = rnd.uniform(160, 620); w = rnd.uniform(18, 60); a = rnd.uniform(-35, 35)
        if 110 < x < 290 and 190 < y < 580: continue
        g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="4" rx="2" transform="rotate({a:.0f} {x:.0f} {y:.0f})" style="fill:var(--ink-soft);opacity:{rnd.uniform(.15,.4):.2f}"/>')
    # the letter, sealed at its opening and its close
    g.append('<path d="M120,210 C150,200 250,200 280,210 L284,560 C250,572 150,572 116,560Z" style="fill:var(--paper);stroke:var(--ink-soft);stroke-width:1.2"/>')
    for i in range(10):
        w = [130, 140, 120, 136, 100, 140, 126, 132, 110, 90][i]
        g.append(f'<rect x="{138}" y="{268+i*24}" width="{w}" height="6" rx="3" style="fill:var(--ink);opacity:.55"/>')
    for (y, lab) in [(214, 'to the living'), (562, 'end')]:
        g.append(f'<path d="M200,{y-26} C222,{y-28} 230,{y-8} 228,{y+4} C232,{y+22} 214,{y+30} 200,{y+28} C182,{y+30} 168,{y+20} 172,{y+2} C168,{y-14} 182,{y-26} 200,{y-26}Z" style="fill:var(--accent)"/>'
                 f'<circle cx="200" cy="{y+1}" r="14" style="fill:none;stroke:var(--glow-core);stroke-width:1.5;opacity:.7"/>')
    g.append('<path d="M150,214 C120,200 96,214 72,196" style="fill:none;stroke:var(--accent);stroke-width:4;stroke-linecap:round"/>'
             '<text x="60" y="184" class="svgl" style="font-size:14px">to the living</text>'
             '<path d="M250,562 C280,576 300,566 326,584" style="fill:none;stroke:var(--accent);stroke-width:4;stroke-linecap:round"/>'
             '<text x="290" y="610" class="svgl" style="font-size:14px">end</text>')
    g.append('<text x="50" y="92" class="svgt" style="font-size:30px">One sealed block</text>'
             '<text x="50" y="124" class="svgl" style="font-size:16px">the rest falls away</text>')
    return svg(uid, ''.join(g), 'A letter sealed in amber wax at its opening and its close, while scraps of chatter fall away around it.')


def ill_candles():
    uid = 'F'
    g = [stars(60), hills().replace('hillA', 'hill' + uid)]
    g.append('<path d="M30,470 C140,462 260,462 370,470 L370,486 C260,478 140,478 30,486Z" style="fill:var(--bark)"/>')
    for i, x in enumerate([110, 200, 290]):
        h = [150, 190, 130][i]
        g.append(f'<path d="M{x-20},470 L{x-20},{470-h} C{x-20},{462-h} {x+20},{462-h} {x+20},{470-h} L{x+20},470Z" style="fill:var(--paper);stroke:var(--ink-soft);stroke-width:1.2"/>'
                 f'<path d="M{x-20},{470-h+18} C{x-12},{470-h+30} {x-16},{470-h+46} {x-10},{470-h+60}" style="fill:none;stroke:var(--ink-soft);stroke-width:1;opacity:.5"/>'
                 f'<path d="M{x},{466-h} C{x-2},{458-h} {x+3},{452-h} {x},{446-h}" style="fill:none;stroke:var(--ink);stroke-width:2;stroke-linecap:round"/>'
                 f'<text x="{x}" y="{470-h/2+8}" text-anchor="middle" class="svgt" style="font-size:24px">{i+1}</text>')
    # a single match, struck, offered and not yet touched
    g.append('<path d="M60,560 L250,520" style="stroke:var(--bark);stroke-width:6;stroke-linecap:round"/>'
             '<circle cx="258" cy="518" r="9" style="fill:var(--tension)"/>'
             '<circle cx="262" cy="512" r="24" style="fill:url(#halo' + uid + ')"/>'
             '<path d="M262,512 C254,498 262,484 266,474 C272,488 280,500 262,512Z" style="fill:url(#lit' + uid + ')"/>')
    g.append('<text x="50" y="92" class="svgt" style="font-size:30px">Three rulings</text>'
             '<text x="50" y="124" class="svgl" style="font-size:16px">the flame is yours</text>')
    return svg(uid, ''.join(g), 'Three unlit candles numbered one to three on a shelf, and a struck match held out, not yet touching them.')


# ---------------------------------------------------------------- pages
pages = []
pages.append(('ill', ill_cover()))
pages.append(('text', f'''<header><p class="eyebrow">Psyche Fable · 1 October</p><h1>{html.escape(TITLE)}</h1></header>
{render([intro_p[0]])}
<p class="mark">This book takes four points from it, chosen by how often and how hard you spoke of them. Nothing here answers an open question for you.</p>'''))
pages.append(('ill', ill_eight()))
pages.append(('text', f'''<header><p class="eyebrow">Still open</p><h2>The eight you pressed hardest</h2></header>
{render(intro_li)}
{quote('sessions')}
{quote('stray')}'''))
pages.append(('ill', ill_phone()))
pages.append(('text', f'''<header><p class="eyebrow">Still open · question 6</p><h2>Reading on the phone</h2></header>
{render([intro_li[5]])}
{quote('zoom')}
{quote('comment')}
<p class="mark">This book is set for that: phone upright, comments only, no buttons, nothing sideways.</p>'''))
pages.append(('ill', ill_three()))
pages.append(('text', f'''<header><p class="eyebrow">Proposed · question 8</p><h2>{inline(SECS[1])}</h2></header>
{render(blocks(SECS[1]))}
{quote('mindlog')}
{quote('body')}
{note('agree', 'The proposal keeps field as <em>the body of the machine as it is</em>, close to your own line of 1 October: «The field is the actual body of the machine.»')}'''))
pages.append(('ill', ill_letter()))
pages.append(('text', f'''<header><p class="eyebrow">Proposed</p><h2>{inline(SECS[2])}</h2></header>
{render(blocks(SECS[2]))}
{quote('mark')}
{quote('waste')}
{note('agree', 'Replies outside the block cut to errors, unexpected outcomes and results. That follows your words of 1 October: «We have to stop doing that because it\'s a huge waste of context.»')}
{note('tension', 'The line to be cut asks flows to explain every question fully. On 30 September you said «some of the things you say are cryptic, like the box on your bed.» Your complaint on 1 October was repetition; on 30 September it was too little explanation. Whether the line goes, or only its repeating part, is yours to rule.')}'''))
pages.append(('ill', ill_candles()))
rul = blocks(SECS[3])
items = ''.join(f'<li value="{b[1]}"><span class="box" aria-hidden="true"></span><span class="rtext" data-src>{inline(b[2])}</span>'
                f'<span class="badge">open</span></li>' for b in rul)
pages.append(('text', f'''<header><p class="eyebrow">Your word</p><h2>{inline(SECS[3])}</h2></header>
<ol class="rulings">{items}</ol>
<p class="mark">None has landed. Answer by comment, by number.</p>'''))

# alternation check: first page is an illustration, never two texts in a row
kinds = [k for k, _ in pages]
assert kinds[0] == 'ill' and all(a != b for a, b in zip(kinds, kinds[1:])), kinds

body = '\n'.join(
    f'<section class="page {k}" id="p{i+1}" aria-label="Page {i+1} of {len(pages)}">'
    + (f'<div class="frame">{c}</div>' if k == 'ill' else f'<article class="leaf">{c}</article>')
    + '</section>' for i, (k, c) in enumerate(pages))
dots = ''.join(f'<i data-i="{i}"></i>' for i in range(len(pages)))

CSS = open(D + 'book.css').read()
JS = open(D + 'book.js').read()
out = f'''<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=JetBrains+Mono:wght@400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>{CSS}</style>
<main class="book" id="book" tabindex="-1">
{body}
</main>
<nav class="dots" aria-hidden="true">{dots}</nav>
<script>{JS}</script>
'''
open(D + 'book.html', 'w').write(out)
print('pages', len(pages), kinds, 'bytes', len(out.encode()))

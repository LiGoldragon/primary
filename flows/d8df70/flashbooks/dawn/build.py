#!/usr/bin/env python3
"""Build index.html for the flashbook "The Dawn of the Meta Harness" from source.md.

The source text is rendered, never edited. Illustration pages map, in order,
to web/01.webp .. web/05.webp. Each illustration page's body carries a bold
"What this picture conveys" line, a scene description, and — on some pages —
a bold "Since this picture" note; the conveys line and any since note render
as visible captions under the image, and the scene description sits in a
"The scene" disclosure.
"""
import html, re, pathlib, subprocess

HERE = pathlib.Path(__file__).parent


def webp_size(path):
    out = subprocess.run(["identify", "-format", "%w %h", str(path)], capture_output=True, text=True, check=True).stdout
    w, h = out.split()
    return int(w), int(h)
src = (HERE / "source.md").read_text()

title_line, rest = src.split("\n", 1)
TITLE = title_line[2:].strip()
pages = re.split(r"^## ", rest, flags=re.M)[1:]

FLAGS = ["unavailable", "proxy", "not measured", "unclassified", "unknown", "not counted", "not deployed"]
FLAG_RE = re.compile(r"\b(" + "|".join(re.escape(f) for f in FLAGS) + r")\b")


def inline(t):
    t = html.escape(t, quote=False)
    t = FLAG_RE.sub(lambda m: f'<span class="flag">{m.group(1)}</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def render_body(body):
    blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    out = []
    for b in blocks:
        lines = b.split("\n")
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
            continue
        text = " ".join(lines)
        out.append(f"<p>{inline(text)}</p>")
    return "\n".join(out)


sections = []
dots = []
img_i = 0
for idx, p in enumerate(pages, 1):
    head, _, body = p.partition("\n")
    m = re.match(r"Page (\d+) · (.*)", head.strip())
    num, rest_h = int(m.group(1)), m.group(2)
    assert num == idx, (num, idx)
    eyebrow = f"Page {num}"
    if rest_h.startswith("Illustration — "):
        img_i += 1
        name = rest_h[len("Illustration — "):]
        paras = [pp.strip() for pp in re.split(r"\n\s*\n", body.strip()) if pp.strip()]
        cm = re.match(r"\*\*What this picture conveys:\*\*\s*(.*)", paras[0], re.S)
        conveys = cm.group(1).strip()
        since = None
        rest_paras = paras[1:]
        if rest_paras and rest_paras[-1].startswith("**Since this picture:**"):
            sm = re.match(r"\*\*Since this picture:\*\*\s*(.*)", rest_paras[-1], re.S)
            since = sm.group(1).strip()
            rest_paras = rest_paras[:-1]
        scene = " ".join(" ".join(pp.split()) for pp in rest_paras)
        captions = f'<p class="conveys"><span class="tag">Conveys</span> {inline(conveys)}</p>'
        if since:
            captions += f'\n      <p class="since"><span class="tag">Since</span> {inline(since)}</p>'
        iw, ih = webp_size(HERE / f"web/{img_i:02d}.webp")
        sections.append(f'''<section class="page ill" id="p{num}" data-n="{num}" aria-label="Page {num}">
  <figure>
    <div class="frame"><img src="web/{img_i:02d}.webp" alt="{html.escape(name)}" width="{iw}" height="{ih}" {'' if num == 1 else 'loading="lazy" '}decoding="async"></div>
    <figcaption>
      <p class="eyebrow">{eyebrow} · Illustration</p>
      <h2>{inline(name)}</h2>
      {captions}
      <details><summary>The scene</summary><p>{inline(scene)}</p></details>
    </figcaption>
  </figure>
</section>''')
        kind = "ill"
    else:
        h = rest_h
        sections.append(f'''<section class="page txt" id="p{num}" data-n="{num}" aria-label="Page {num}">
  <div class="sheet">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{inline(h)}</h2>
    {render_body(body)}
  </div>
</section>''')
        kind = "txt"
    dots.append(f'<button type="button" class="dot {kind}" data-go="{num}" aria-label="Go to page {num}"></button>')

N = len(pages)
tpl = (HERE / "shell.html").read_text()
out = (tpl.replace("{{TITLE}}", html.escape(TITLE))
          .replace("{{PAGES}}", "\n".join(sections))
          .replace("{{DOTS}}", "".join(dots))
          .replace("{{N}}", str(N)))
(HERE / "index.html").write_text(out)
print(f"{N} pages, {img_i} illustrations")

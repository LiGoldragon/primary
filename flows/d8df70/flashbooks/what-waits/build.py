#!/usr/bin/env python3
"""Build index.html for the flashbook "What Waits for the Living" from source.md.

The source text is rendered, never edited. Illustration pages map, in order,
to web/01.webp .. web/08.webp.
"""
import html, re, pathlib

HERE = pathlib.Path(__file__).parent
src = (HERE / "source.md").read_text()

title_line, rest = src.split("\n", 1)
TITLE = title_line[2:].strip()
pages = re.split(r"^## ", rest, flags=re.M)[1:]


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t


def label_class(t):
    if t.startswith("**Tension:**"):
        return "tension"
    if t.startswith("**Recommendation"):
        return "rec"
    if t.startswith("**Waiting:**") or t.startswith("**Unblocks:**"):
        return "meta"
    return ""


def render_body(body, checklist_page=None):
    blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    out = []
    for b in blocks:
        lines = b.split("\n")
        if all(l.startswith("> ") or l == ">" for l in lines):
            q = " ".join(l[2:] for l in lines)
            out.append(f'<blockquote class="living"><p>{inline(q)}</p>')
            out.append("</blockquote>")
            continue
        if lines[0].startswith("-- "):
            # provenance line: attach to the previous quote
            prov = f'<p class="prov">{inline(lines[0])}</p>'
            if out and out[-1] == "</blockquote>":
                out.insert(len(out) - 1, prov)
            else:
                out.append(prov)
            continue
        if all(l.startswith("- [ ] ") for l in lines):
            items = []
            for l in lines:
                t = l[6:]
                m = re.match(r"(\d+)\. (.*)", t)
                n, txt = m.group(1), m.group(2)
                items.append(
                    f'<li><label class="tick" for="ans-{n}"><input type="checkbox" id="ans-{n}" data-n="{n}">'
                    f'<span class="box" aria-hidden="true"></span><span class="num">{n}.</span>'
                    f'<span class="txt">{inline(txt)}</span></label></li>'
                )
            out.append('<ol class="answers">' + "".join(items) + "</ol>")
            continue
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
            continue
        if all(re.match(r"\d+\. ", l) for l in lines):
            out.append('<ol class="six">' + "".join(
                f'<li><span class="num">{l.split(". ",1)[0]}</span><span>{inline(l.split(". ",1)[1])}</span></li>' for l in lines) + "</ol>")
            continue
        # paragraph block; lines may each carry a label (Waiting / Unblocks)
        if len(lines) > 1 and all(label_class(l) == "meta" for l in lines):
            out.append('<dl class="meta">' + "".join(
                f'<div><dt>{inline(l.split(":**",1)[0][2:])}</dt><dd>{inline(l.split(":**",1)[1].strip())}</dd></div>' for l in lines) + "</dl>")
            continue
        text = " ".join(lines)
        cls = label_class(text)
        if cls == "meta":
            k, v = text.split(":**", 1)
            out.append(f'<dl class="meta"><div><dt>{inline(k[2:])}</dt><dd>{inline(v.strip())}</dd></div></dl>')
        elif cls:
            out.append(f'<p class="{cls}">{inline(text)}</p>')
        else:
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
        sections.append(f'''<section class="page ill" id="p{num}" data-n="{num}" aria-label="Page {num}">
  <figure>
    <div class="frame"><img src="web/{img_i:02d}.webp" alt="{html.escape(name)}" width="1024" height="1536" {'' if num == 1 else 'loading="lazy" '}decoding="async"></div>
    <figcaption>
      <p class="eyebrow">{eyebrow} · Illustration</p>
      <h2>{inline(name)}</h2>
      <details><summary>The scene</summary><p>{inline(" ".join(body.split()))}</p></details>
    </figcaption>
  </figure>
</section>''')
        kind = "ill"
    else:
        h = rest_h
        m2 = re.match(r"(\d) · (.*)", h)
        qn = ""
        if m2:
            qn = f'<span class="qn">Question {m2.group(1)}</span>'
            h = m2.group(2)
        sections.append(f'''<section class="page txt" id="p{num}" data-n="{num}" aria-label="Page {num}">
  <div class="sheet">
    <p class="eyebrow">{eyebrow}{' · ' + qn if qn else ''}</p>
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

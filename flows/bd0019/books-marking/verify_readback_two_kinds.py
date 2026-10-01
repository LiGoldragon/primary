#!/usr/bin/env python3
# Read-back check of the published «Two kinds of output»: book contained byte for byte, title,
# every source paragraph and living quote verbatim, no buttons or clickable controls (static and
# rendered DOM at 390x844), nothing wider than the viewport.
import sys, re, html, hashlib, subprocess, pathlib, importlib.util
pub_path = sys.argv[1]; pub = open(pub_path).read()
HERE = pathlib.Path(__file__).resolve().parent
book = (HERE / "book-two-kinds.html").read_text()
print("published sha256", hashlib.sha256(pub.encode()).hexdigest())
print("book-two-kinds.html contained verbatim:", book.strip() in pub)
print("title:", re.search(r"<title>(.*?)</title>", pub).group(1))
P = html.unescape(re.sub(r"<[^>]+>", "", pub))
raw = (HERE / "source-two-kinds.md").read_text()
body = re.sub(r"\A```yaml\n.*?\n```\n", "", raw, flags=re.S).strip("\n")
missing = []
for para in body.split("\n\n"):
    for line in para.split("\n"):
        t = re.sub(r"^(## |\d\. |- )", "", line).replace("`", "")
        for piece in t.split("**"):
            piece = piece.strip()
            if piece and piece not in P: missing.append(piece[:60])
print("source text verbatim in published page:", not missing, missing)
spec = importlib.util.spec_from_file_location("b", HERE / "build_two_kinds.py")
src = (HERE / "build_two_kinds.py").read_text()
Q = eval(re.search(r"^Q = (\{.*?^\})", src, re.S | re.M).group(1), {"D": "-- psyche, STT, 2026-10-01 · flows/6997eb/vision/"})
def vision(n):
    p = pathlib.Path("/home/li/primary/flows/6997eb/vision") / n
    return p.read_text() if p.exists() else subprocess.run(["git","-C","/home/li/primary","show",f"main:flows/6997eb/vision/{n}"],capture_output=True,text=True).stdout
qok = all(t in P and t in vision(f) for f, t, _ in Q.values())
print("living quotes verbatim in page and records:", qok, len(Q))
print("static controls:", re.findall(r"<button|<a\s|<input|<select|onclick|role=\"button\"|tabindex", pub))
w = HERE / "shots-two-kinds" / "readback.html"
w.write_text(pub.replace("</body>", '<script>addEventListener("load",function(){var bad=[].filter.call(document.querySelectorAll("body *"),function(e){var r=e.getBoundingClientRect();return r.right>innerWidth+0.5&&!e.closest("code")&&!e.closest("svg");}).length;document.title="SW="+document.documentElement.scrollWidth+" IW="+innerWidth+" OVER="+bad+" CONTROLS="+document.querySelectorAll("button,a,input,select,textarea,[onclick],[role=button],[tabindex]").length+" PAGES="+document.querySelectorAll(".page").length;});</script></body>'))
dom = subprocess.run(["google-chrome","--headless=new","--disable-gpu","--window-size=390,844","--virtual-time-budget=4000","--dump-dom",f"file://{w}"],capture_output=True,text=True).stdout
print("rendered DOM:", re.search(r"<title>(SW=[^<]*)</title>", dom).group(1))
subprocess.run(["google-chrome","--headless=new","--disable-gpu","--hide-scrollbars","--window-size=390,844","--virtual-time-budget=4000",f"--screenshot={HERE}/shots-two-kinds/readback-390x844.png",f"file://{w}"],capture_output=True)
print("screenshot", HERE / "shots-two-kinds" / "readback-390x844.png")

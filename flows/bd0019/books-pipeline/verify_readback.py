#!/usr/bin/env python3
# Read-back check of the published «The anatomy of the book pipeline»: book.html contained byte for
# byte, title, every source line and living quote verbatim, Astra's witness exact, no buttons or
# clickable controls (static and rendered DOM at 390x844), nothing wider than the viewport.
import sys, re, html, hashlib, subprocess, pathlib
pub = open(sys.argv[1]).read()
HERE = pathlib.Path(__file__).resolve().parent
book = (HERE / "book.html").read_text()
print("published sha256", hashlib.sha256(pub.encode()).hexdigest())
print("book.html contained verbatim:", book.strip() in pub)
print("title:", re.search(r"<title>(.*?)</title>", pub).group(1))
P = html.unescape(re.sub(r"<[^>]+>", "", pub))
raw = (HERE / "source.md").read_text()
first, body = raw.split("\n", 1)
missing = []
for line in body.strip("\n").split("\n"):
    t = re.sub(r"^(## |\d\. |- )", "", line).replace("`", "")
    for piece in t.split("**"):
        piece = piece.strip()
        if piece and piece not in P: missing.append(piece[:60])
print("source text verbatim in published page:", not missing, missing)
print("datom line shown only in the provenance note:", P.count(first) == 2 and "Presentation.{ «title» }" in P)
src = (HERE / "build.py").read_text()
ns = {}
exec(re.search(r"^V = .*?^\}\n", src, re.S | re.M).group(0), ns)
exec(re.search(r"^ASTRA = \(.*?\)\n", src, re.S | re.M).group(0), ns)
def record(rel):
    p = pathlib.Path("/home/li/primary") / rel
    return p.read_text() if p.exists() else subprocess.run(["git","-C","/home/li/primary","show",f"main:{rel}"],capture_output=True,text=True).stdout
flat = lambda s: re.sub(r"\s*\n>\s*", " ", s)
qok = all(t in P and t in flat(record(f)) for f, t, _ in ns["Q"].values())
print("living quotes verbatim in page and records:", qok, len(ns["Q"]))
print("Astra witness exact:", ns["ASTRA"] in P)
print("static controls:", re.findall(r"<button|<a\s|<input|<select|<textarea|<details|onclick|role=\"button\"|tabindex", pub))
print("pre blocks:", pub.count("<pre"))
w = HERE / "shots" / "readback.html"
w.write_text(pub.replace("</body>", '<script>addEventListener("load",function(){var bad=[].filter.call(document.querySelectorAll("body *"),function(e){var r=e.getBoundingClientRect();return r.right>innerWidth+0.5&&!e.closest("code")&&!e.closest("svg");}).length;document.title="SW="+document.documentElement.scrollWidth+" IW="+innerWidth+" OVER="+bad+" CONTROLS="+document.querySelectorAll("button,a,input,select,textarea,details,[onclick],[role=button],[tabindex]").length+" PAGES="+document.querySelectorAll(".page").length;});</script></body>'))
dom = subprocess.run(["google-chrome","--headless=new","--disable-gpu","--window-size=390,844","--virtual-time-budget=4000","--dump-dom",f"file://{w}"],capture_output=True,text=True).stdout
print("rendered DOM:", re.search(r"<title>(SW=[^<]*)</title>", dom).group(1))
subprocess.run(["google-chrome","--headless=new","--disable-gpu","--hide-scrollbars","--window-size=390,844","--virtual-time-budget=4000",f"--screenshot={HERE}/shots/readback-390x844.png",f"file://{w}"],capture_output=True)
print("screenshot", HERE / "shots" / "readback-390x844.png")

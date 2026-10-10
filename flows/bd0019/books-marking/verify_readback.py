#!/usr/bin/env python3
# Checks the published page holds book.html byte for byte and every quote and source paragraph.
import sys, hashlib, html, re
pub = open(sys.argv[1]).read(); book = open(sys.argv[2]).read()
print("book sha256", hashlib.sha256(book.encode()).hexdigest())
print("published sha256", hashlib.sha256(pub.encode()).hexdigest())
print("book.html contained verbatim:", book.strip() in pub)
plain = html.unescape(re.sub(r"<[^>]+>", "", pub))
src = open("source.md").read()
ok = all((p[3:] if p.startswith("## ") else p.replace("`", "")) in plain for p in src.split("\n\n"))
print("source paragraphs verbatim in published page:", ok)
print("title:", re.search(r"<title>(.*?)</title>", pub).group(1))

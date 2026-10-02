#!/usr/bin/env python3
# Copies the block «Six questions on sessions, re-asked» verbatim from Psyche Fable 6997eb's record; marker lines and datom line excluded.
import json, hashlib
F="/home/li/.claude/projects/-home-li-primary/fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl"
LINE,UUID=1435,None
TITLE="Session handling as it is"
START,END="<!-- to-the-living:start -->","<!-- to-the-living:end -->"
with open(F) as f:
    for i,l in enumerate(f,1):
        if i==LINE: r=json.loads(l);break
assert r["type"]=="assistant"
text="".join(c["text"] for c in r["message"]["content"] if c.get("type")=="text")
lines=text.split("\n")
s=[i for i,x in enumerate(lines) if x==START]; e=[i for i,x in enumerate(lines) if x==END]
assert len(s)==2 and len(e)==2
for a,b in zip(s,e):
    blk=lines[a+1:b]
    if blk[0]=="`Presentation.{ «%s» }`"%TITLE: break
else: raise SystemExit("title not found")
body="\n".join(blk[1:]).strip("\n")
open("source.md","w").write(body)
print(r.get("timestamp"),a+1,b+1,len(body),hashlib.sha256(body.encode()).hexdigest())

#!/usr/bin/env python3
# Copies the block «The restart of the stack» verbatim from Psyche Fable 6997eb's record; marker lines and the Presentation datom line excluded.
# The brief named line 2791 / uuid 24ee5421; that record is the commissioning Agent call. The block is on line 2788, uuid 99b40699 (found by title).
import json, hashlib
F="/home/li/.claude/projects/-home-li-primary/6997eb8a-30eb-49a1-a787-45279164a43b.jsonl"
LINE,UUID=2788,"99b40699-cbb1-4088-a556-8df44d6e95d8"
TITLE="The restart of the stack"
START,END="<!-- to-the-living:start -->","<!-- to-the-living:end -->"
with open(F) as f:
    for i,l in enumerate(f,1):
        if i==LINE: r=json.loads(l);break
assert r["uuid"]==UUID and r["type"]=="assistant"
text="".join(c["text"] for c in r["message"]["content"] if c.get("type")=="text")
lines=text.split("\n")
s=[i for i,x in enumerate(lines) if x==START]; e=[i for i,x in enumerate(lines) if x==END]
assert len(s)==1 and len(e)==1
blk=lines[s[0]+1:e[0]]
assert blk[0]=="Presentation.{ «%s» }"%TITLE, blk[0]
body="\n".join(blk[1:]).strip("\n")
open("source.md","w").write(body+"\n")
print(r.get("timestamp"),s[0]+1,e[0]+1,len(body),hashlib.sha256(body.encode()).hexdigest())

#!/usr/bin/env python3
# Copies the source block verbatim from 6997eb's transcript: heading to the closing rule.
import json, hashlib, sys
F = "/home/li/.claude/projects/-home-li-primary/6997eb8a-30eb-49a1-a787-45279164a43b.jsonl"
LINE, UUID = 623, "187e77eb-8069-4648-9f38-a29ad72ed12f"
with open(F) as f:
    for i, l in enumerate(f, 1):
        if i == LINE:
            r = json.loads(l); break
assert r["uuid"] == UUID and r["type"] == "assistant", (r["uuid"], r["type"])
text = "".join(c["text"] for c in r["message"]["content"] if c.get("type") == "text")
start = text.index("## The marker: two instincts")
end = text.index("\n=== End ===", start)
src = text[start:end].rstrip("\n")
open("source.md", "w").write(src)
print("timestamp", r.get("timestamp"))
print("sha256", hashlib.sha256(src.encode()).hexdigest(), "chars", len(src))

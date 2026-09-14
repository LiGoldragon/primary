#!/usr/bin/env python3
import sys, json, hashlib, argparse
sys.path.insert(0, "/home/li/primary/flows/024bc7/tools")
from codex_wake import WS

TRANSCRIPT = "/home/li/.claude/projects/-home-li-primary/6cc91bd5-d4d4-4b16-9642-34b4c9579ef4.jsonl"
THREAD_ID = "01a09c90-c82c-7621-b7b3-c9734d94eb22"

def strip_reminder(t):
    if t.startswith("<system-reminder>"):
        e = t.find("</system-reminder>")
        if e != -1: t = t[e+len("</system-reminder>"):]
    return t.strip()

def is_machine(t):
    return (t.startswith("[PEER") or t.startswith("[RELAY") or t.startswith("[WAKE")
            or t.startswith("<") or "[SYSTEM NOTIFICATION" in t)

def extract_text(msg):
    c = msg.get("content")
    if isinstance(c, str): return c
    if isinstance(c, list):
        parts = [p["text"] for p in c if isinstance(p, dict) and p.get("type") == "text" and "text" in p]
        if parts: return "\n".join(parts)
    return None

def find_last_prompt():
    last = None
    with open(TRANSCRIPT) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: rec = json.loads(line)
            except json.JSONDecodeError: continue
            if rec.get("type") != "user": continue
            msg = rec.get("message") or {}
            if msg.get("role") != "user": continue
            text = extract_text(msg)
            if text is None: continue
            text = strip_reminder(text)
            if not text or is_machine(text): continue
            last = text
    return last

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--match")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    text = find_last_prompt()
    if text is None:
        print("no prompt found"); sys.exit(1)
    if args.match:
        if ".." not in args.match:
            print("bad --match, expected HEAD..TAIL"); sys.exit(3)
        head, tail = args.match.split("..", 1)
        if not (text.startswith(head) and text.endswith(tail)):
            print("match failed"); sys.exit(3)
    if args.dry_run:
        print(text)
        print("sha256:", hashlib.sha256(text.encode()).hexdigest())
        sys.exit(0)
    payload = ("[RELAY through Claude; the living's words, verbatim; "
               "relayed by Fable 6cc91b by transcript lookup]\n\n" + text)
    w = WS()
    w.call(1, "initialize", {"clientInfo": {"name": "fable-6cc91b", "version": "0"}})
    w.send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
    w.call(2, "thread/resume", {"threadId": THREAD_ID, "excludeTurns": True})
    turns = w.call(3, "thread/turns/list", {"threadId": THREAD_ID, "limit": 100})
    res = turns.get("result") or {}
    items = res.get("data") or res.get("turns") or []
    if not items:
        print("no turns found"); sys.exit(1)
    latest = max(items, key=lambda t: t.get("id", ""))
    if latest.get("status") == "inProgress":
        print("BUSY"); print(text); sys.exit(2)
    started = w.call(4, "turn/start", {"threadId": THREAD_ID,
                                        "input": [{"type": "text", "text": payload}]})
    r = (started.get("result") or {}).get("turn") or {}
    print("turn:", r.get("id"), "status:", r.get("status"))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Inject a user turn into a running, attachable Claude Code background session.

usage: claude_inject.py <short-id> <text>
Mechanism (witnessed 2026-09-13, Claude Code 2.1.263): the local daemon's control
socket accepts op "attach" when the caller presents ~/.claude/daemon/control.key;
the connection then carries the session's pty. Bytes written are keystrokes, so
the text is typed into the prompt and submitted with a carriage return. The turn
lands in the same session id as a user-role turn (middle stratum). The living may
be attached with `claude attach <short-id>` at the same time and sees it typed.
Only send while the session is idle (no turn in progress): check
`claude agents --json` status first."""
import socket,json,time,glob,os,sys
short,text=sys.argv[1],sys.argv[2]
key=open(os.path.expanduser("~/.claude/daemon/control.key")).read().strip()
p=glob.glob(os.path.join("/tmp","cc-daemon-%d"%os.getuid(),"*","control.sock"))[0]
s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(2); s.connect(p)
s.sendall((json.dumps({"proto":1,"op":"attach","short":short,"auth":key,"cols":120,"rows":40,
    "attachId":os.urandom(8).hex(),"caps":{"imark":False,"terminal":"xterm","mux":None,"ssh":False}})+"\n").encode())
head=s.recv(4096)
if b'"ok":true' not in head.split(b"\n",1)[0]: sys.exit("attach refused: %r"%head[:200])
end=time.time()+1
while time.time()<end:
    try: s.recv(65536)
    except Exception: pass
s.sendall(b"\x15"); time.sleep(0.3)
body=text.encode()
if b"\n" in body: body=b"\x1b[200~"+body+b"\x1b[201~"   # bracketed paste keeps newlines
s.sendall(body); time.sleep(0.8)
s.sendall(b"\r"); time.sleep(1.5)
s.close(); print("injected into", short)

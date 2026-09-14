import sys,json,time
sys.path.insert(0,"/home/li/primary/flows/024bc7/tools")
from codex_wake import WS
SK=["spirit","psyche","behavior","correction","vocabulary","testing","psyche-interraction","main-flow","edit-coordination"]
prompt=open("/home/li/primary/flows/6cc91b/secondary-bootstrap/codex_prompt.txt").read()
w=WS()
w.call(1,"initialize",{"clientInfo":{"name":"fable-6cc91b","title":"Fable flow 6cc91b secondary bootstrap","version":"0"}})
w.send({"jsonrpc":"2.0","method":"initialized","params":{}})
r=w.call(2,"thread/start",{"model":"gpt-6-astra","cwd":"/home/li/secondary","approvalPolicy":"never","sandbox":"danger-full-access"},wait=30)
print("thread/start:",json.dumps(r)[:600])
tid=r["result"]["thread"]["id"] if "thread" in r.get("result",{}) else r["result"]["threadId"]
inp=[{"type":"skill","name":s,"path":"/home/li/secondary/.agents/skills/%s/SKILL.md"%s} for s in SK]
inp.append({"type":"text","text":prompt})
t=w.call(3,"turn/start",{"threadId":tid,"input":inp},wait=60)
print("THREAD",tid)
print("turn/start:",json.dumps(t)[:800])

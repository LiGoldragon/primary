import sys,json,time
sys.path.insert(0,"/home/li/primary/flows/024bc7/tools")
from codex_wake import WS
TID="01a0a11f-6130-70e2-80b1-796348e7b086"
TXT=("Your Claude half in the SECONDARY pair is session 57a7aa02-e52d-4266-8746-6770ff770d11 "
 "(short 57a7aa02), claude-fable-5-1, cwd /home/li/secondary, reached by "
 "/home/li/primary/flows/024bc7/tools/claude_inject.py 57a7aa02 \"<text>\" while it is idle. "
 "Name it on the Paired line of your log.")
w=WS()
w.call(1,"initialize",{"clientInfo":{"name":"fable-6cc91b","title":"Fable flow 6cc91b","version":"0"}})
w.send({"jsonrpc":"2.0","method":"initialized","params":{}})
for i in range(60):
    r=w.call(10+i,"thread/loaded/list",{},wait=20)
    st=None
    for t in r["result"].get("threads",[]):
        if t["id"]==TID: st=t.get("status",{}).get("type")
    print("status",st,flush=True)
    if st=="idle": break
    time.sleep(15)
t=w.call(900,"turn/start",{"threadId":TID,"input":[{"type":"text","text":TXT}]},wait=60)
print("turn2:",json.dumps(t)[:400])

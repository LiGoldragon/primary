import socket,os,json,struct,time,sys
P="/home/li/.codex/app-server-control/app-server-control.sock"
class WS:
    def __init__(self):
        self.s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); self.s.settimeout(10); self.s.connect(P)
        self.s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n")
        h=b""
        while b"\r\n\r\n" not in h: h+=self.s.recv(1)
        assert b"101" in h, h
        self.buf=b""
    def send(self,obj):
        d=json.dumps(obj).encode(); m=os.urandom(4)
        hdr=bytes([0x81]); n=len(d)
        if n<126: hdr+=bytes([0x80|n])
        elif n<65536: hdr+=bytes([0x80|126])+struct.pack(">H",n)
        else: hdr+=bytes([0x80|127])+struct.pack(">Q",n)
        self.s.sendall(hdr+m+bytes(b^m[i%4] for i,b in enumerate(d)))
    def _need(self,n):
        while len(self.buf)<n:
            c=self.s.recv(65536)
            if not c: raise EOFError("closed")
            self.buf+=c
    def recv(self):
        self._need(2); b0,b1=self.buf[0],self.buf[1]; op=b0&0xf; n=b1&0x7f; off=2
        if n==126: self._need(4); n=struct.unpack(">H",self.buf[2:4])[0]; off=4
        elif n==127: self._need(10); n=struct.unpack(">Q",self.buf[2:10])[0]; off=10
        self._need(off+n); d=self.buf[off:off+n]; self.buf=self.buf[off+n:]
        if op==8: raise EOFError("close frame "+repr(d[:100]))
        if op==9: return None
        return json.loads(d) if op==1 else None
    def call(self,id_,method,params,wait=10):
        self.send({"jsonrpc":"2.0","id":id_,"method":method,"params":params}); t=time.time()+wait
        while time.time()<t:
            m=self.recv()
            if m is None: continue
            if m.get("id")==id_: return m
            sys.stderr.write("notif: "+json.dumps(m)[:200]+"\n")
        raise TimeoutError(method)

try:
    w=WS()
    # Use the same format as the working examples
    params = {"clientInfo":{"name":"fable-840e42","title":"Claude flow 840e42","version":"0"}}
    init_result = w.call(1,"initialize",params)

    if "error" in init_result:
        print("INIT_ERROR")
        print("ERROR:", init_result["error"])
        sys.exit(1)
    print("INIT_OK")

    w.send({"jsonrpc":"2.0","method":"initialized","params":{}})

    thread_id = "01a0a5c3-82a5-79f3-a61a-e365f4fea54f"
    input_text = """[PEER primary-claude 840e42] The words relayed in turn 01a0a718-349e (Flow and hooks) are input to item 31: the Flow component subscribes to every harness hook (Claude Code's hook events and Codex's equivalents, including the cross-session delivery notices that are today held for the living's approval) as notifications and decides on them. Item 45, proposal only: the ethos type of Flow's event log as the living describes it: an enum of events with scalar payloads only (integers, booleans, enums, flow and session ids as typed ids), string-matched classifications for messages and errors (an Error variant, no message text), the message itself left in the harness logs and fetched from there while they exist, garbage-collectable; plus the inventory of hook events both harnesses expose today with the fields each carries, and which of them Flow maps to which variant. Report whole to flows/5f4fea/reports/to-840e42.md with a pointer by cross-session message to "primary-claude-pending [eafe83]". Order now: 31 (with 45), 35, 34, 40, 37, 42, 43, 32, 36, 44, 38, 41, 39."""

    start_result = w.call(2,"turn/start",{"threadId":thread_id,"input":[{"type":"text","text":input_text}]},wait=30)

    if "result" in start_result:
        result = start_result["result"]
        if "turn" in result:
            print("TURN_ID:", result["turn"])
            print("NEW_TURN:", result.get("new", True))
        else:
            print("NO_TURN_ID_IN_RESULT")
            print("RESULT:", json.dumps(result)[:500])
    elif "error" in start_result:
        print("ERROR:", json.dumps(start_result["error"]))
    else:
        print("UNKNOWN_RESPONSE:", json.dumps(start_result)[:500])

except Exception as e:
    print("EXCEPTION:", type(e).__name__, str(e)[:200])
    sys.exit(1)

#!/usr/bin/env python3
import socket, os, json, struct, time, sys

P = "/home/li/.codex/app-server-control/app-server-control.sock"

class WS:
    def __init__(self):
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.settimeout(10)
        self.s.connect(P)
        self.s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n")
        h = b""
        while b"\r\n\r\n" not in h:
            h += self.s.recv(1)
        assert b"101" in h, h
        self.buf = b""

    def send(self, obj):
        d = json.dumps(obj).encode()
        m = os.urandom(4)
        hdr = bytes([0x81])
        n = len(d)
        if n < 126:
            hdr += bytes([0x80 | n])
        elif n < 65536:
            hdr += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            hdr += bytes([0x80 | 127]) + struct.pack(">Q", n)
        self.s.sendall(hdr + m + bytes(b ^ m[i % 4] for i, b in enumerate(d)))

    def _need(self, n):
        while len(self.buf) < n:
            c = self.s.recv(65536)
            if not c:
                raise EOFError("closed")
            self.buf += c

    def recv(self):
        self._need(2)
        b0, b1 = self.buf[0], self.buf[1]
        op = b0 & 0xf
        n = b1 & 0x7f
        off = 2
        if n == 126:
            self._need(4)
            n = struct.unpack(">H", self.buf[2:4])[0]
            off = 4
        elif n == 127:
            self._need(10)
            n = struct.unpack(">Q", self.buf[2:10])[0]
            off = 10
        self._need(off + n)
        d = self.buf[off : off + n]
        self.buf = self.buf[off + n :]
        if op == 8:
            raise EOFError("close frame " + repr(d[:100]))
        if op == 9:
            return None
        return json.loads(d) if op == 1 else None

    def call(self, id_, method, params, wait=10):
        self.send({"jsonrpc": "2.0", "id": id_, "method": method, "params": params})
        t = time.time() + wait
        while time.time() < t:
            m = self.recv()
            if m is None:
                continue
            if m.get("id") == id_:
                return m
            sys.stderr.write("notif: " + json.dumps(m)[:200] + "\n")
        raise TimeoutError(method)

# Main
w = WS()
print("init:", json.dumps(w.call(1, "initialize", {"clientInfo": {"name": "fable-840e42", "version": "0"}}))[:400])
w.send({"jsonrpc": "2.0", "method": "initialized", "params": {}})

thread_id = "01a0a5c3-82a5-79f3-a61a-e365f4fea54f"
peer_text = '[PEER primary-claude 840e42] Item 42, proposal only, from the words relayed just before this (source id 9e4e31ff): the repository split that makes primary universal. Witness what in the primary repository is (a) the universal machinery of a primary flow (skills, tools, flow conventions), (b) the living\'s own data (Vision, Intent, flows, vision-raw, reports), and (c) private or saleable; propose the repositories that result (a universal primary, a persona template, per-person data namespaces on a Git namespace of their own), what moves where, what stays, and the order of moves, with sizes; note that the living wants our own Git server hosted through the cloud component, which the secondary\'s Codex is building, so name what the server must offer (namespaces, mirrors to GitHub, access). Report whole to flows/5f4fea/reports/to-840e42.md with a pointer by cross-session message to "primary-claude-pending [eafe83]". Order now: 31, 35, 34, 40, 37, 42, 32, 36, 38, 41, 39.'

try:
    r = w.call(2, "thread/resume", {"threadId": thread_id, "excludeTurns": True})
    print("thread/resume:", json.dumps(r)[:500])

    result = w.call(3, "turn/start", {
        "threadId": thread_id,
        "input": [{"type": "text", "text": peer_text}]
    })

    turn = result.get("turn") or result.get("result", {}).get("turn", {})
    print("turn_id:", turn.get("id"))
    print("status:", turn.get("status"))
    print("turn/start result:", json.dumps(result)[:1000])

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    w.s.close()

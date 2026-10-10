import socket, json, sys

sock_path = "/home/li/.codex/app-server-control/app-server-control.sock"
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(15)
try:
    s.connect(sock_path)
except Exception as e:
    print("CONNECT_ERROR:", e)
    sys.exit(0)

def send(msg):
    data = (json.dumps(msg) + "\n").encode()
    s.sendall(data)

def recv_lines(n=5, timeout=5):
    s.settimeout(timeout)
    buf = b""
    lines = []
    try:
        while len(lines) < n:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                if line.strip():
                    lines.append(line)
    except socket.timeout:
        pass
    return lines

send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "witness-f55ec8", "version": "0.0.1"}}})
for l in recv_lines(3):
    print("INIT_RESP:", l.decode(errors="replace")[:2000])

send({"id": 2, "method": "account/rateLimits/read", "params": {}})
for l in recv_lines(5):
    print("RATELIMITS_RESP:", l.decode(errors="replace")[:4000])

s.close()

import subprocess, json, time, sys, select

proc = subprocess.Popen(
    ["codex", "app-server", "proxy", "--sock", "/home/li/.codex/app-server-control/app-server-control.sock"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0
)

def send(msg):
    data = (json.dumps(msg) + "\n").encode()
    proc.stdin.write(data)
    proc.stdin.flush()

def drain(timeout=5):
    end = time.time() + timeout
    out = b""
    while time.time() < end:
        r, _, _ = select.select([proc.stdout], [], [], 0.5)
        if r:
            chunk = proc.stdout.read1(65536) if hasattr(proc.stdout, 'read1') else proc.stdout.read(65536)
            if chunk:
                out += chunk
            else:
                break
    return out

send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "witness-f55ec8", "version": "0.0.1"}}})
time.sleep(1)
out1 = drain(3)
print("INIT_OUT:", out1.decode(errors="replace"))

send({"id": 2, "method": "account/rateLimits/read", "params": {}})
time.sleep(1)
out2 = drain(4)
print("RATELIMITS_OUT:", out2.decode(errors="replace"))

proc.stdin.close()
time.sleep(0.5)
proc.terminate()
try:
    proc.wait(timeout=3)
except Exception:
    proc.kill()
err = proc.stderr.read()
if err:
    print("STDERR:", err.decode(errors="replace")[:3000])

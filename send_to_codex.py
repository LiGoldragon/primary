#!/usr/bin/env python3
import json
import socket

# Read the message from file
with open('/tmp/message.txt', 'r') as f:
    message_content = f.read()

# Connect to Codex app-server via UNIX socket
socket_path = "/home/li/.codex/app-server-control/app-server-control.sock"
thread_id = "01a0a715-2d5d-7342-b278-1dbcf78795bd"

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(socket_path)

# Create the JSON-RPC request for turn/start
request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "turn/start",
    "params": {
        "client_id": "fable-840e42",
        "thread_id": thread_id,
        "text": message_content
    }
}

# Send the request
sock.sendall(json.dumps(request).encode() + b'\n')

# Receive the response
response_data = b""
while True:
    chunk = sock.recv(4096)
    if not chunk:
        break
    response_data += chunk
    # Try to parse as JSON
    try:
        response = json.loads(response_data.decode())
        print(json.dumps(response, indent=2))
        break
    except:
        continue

sock.close()

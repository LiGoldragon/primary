# Credential-free MCP capability fixture

- Candidate: `bb36e680e7cfee675a997fff5383dbe6d32750f4`
- Date: 2026-10-03 (the command did not retain a wall-clock timestamp)
- Exit: 0
- Inputs: local Python JSON-RPC fixture only; no Claude process and no credential path or credential content.
- Valid `tools/call` for `flow_environment` with `{}` returned exactly the three fixture Flow values.
- Nonempty substitution-literal arguments and an unknown tool returned `-32602`.
- An unsupported method returned `-32601`.

The retained shell command and its output were created in a disposable `/tmp/flow-mcp-bb36-*` directory. Its final output was `bb36-mcp-fixture=pass`.

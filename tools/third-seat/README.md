# Kimi K3 / OpenCode third seat

`tools/third-seat` is the canonical, offline-ready setup. The prior files in
`flows/34d94e/evaluation/third-stack` are historical evaluation evidence and
are not a runnable configuration.

The selected route is `fixtures/fireworks.json`: Fireworks Kimi K3 serverless,
`accounts/fireworks/models/kimi-k3`. The optional named route
`openrouter-fireworks-pinned.json` permits only Fireworks and explicitly
disables fallback. Both descriptors are deliberately committed with
`access_authorized:false`; neither can run a provider request.

Run the actual local refusal fixture with the packaged binary:

    node tools/third-seat/refusal-dry-run.mjs --opencode /nix/store/0qyc76kknwckhw21biar2kll782jxnxw-opencode/bin/opencode

It starts only a `127.0.0.1` server that always returns HTTP 503, gives each
OpenCode invocation an isolated temporary HOME and config, checks OpenCode
1.17.13, and removes its server, child process group, and temporary directory.
It never reads a provider key and cannot make an external connection.

`offline-adapter.mjs` is the stronger local replay witness: it verifies native
tool-call IDs and arguments, `reasoning_content`, and the matching tool result.
The provider runner remains held behind `access_authorized:true` and a secret
on FD 3 or higher. It is not authority to sign up, obtain a key, or contact a
provider. For the OpenRouter descriptor, the runner adds only its allowlisted
`provider` routing field to the outbound JSON and clones the original messages
unchanged. There is no automatic upstream failover; a non-2xx response latches
the proxy closed and returns a sanitized 502.

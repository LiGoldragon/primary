# ChatGPT Desktop Codex server connection

Remember recent ChatGPT Desktop and Codex server work, determine why new chats and existing threads fail to load with `invalid transport in mcp_servers.codex_app`, and realize and verify the repair if it is within the existing design.

Remembered: 01a047d2, 01a05487, 01a05c80 — depth 1. The chosen design made Desktop a client of the persistent shared Codex daemon and removed private App Tools; later startup work restored the executable candidate Desktop requires before selecting its healthy WebSocket connection.

Settled: the persistent Codex 0.151.0 owner and Unix socket are healthy. The static Codex config contains no `mcp_servers.codex_app`. Desktop is still supplying a runtime/per-thread `codex_app` object that lacks both accepted transport discriminators (`command` for stdio or `url` for HTTP), so Codex rejects both start and resume during configuration loading.

Settled: the surviving producer is Desktop's separate `codex-app-tools-mcp` generator, which writes its result through `config/batchWrite` independently of `getConfigOverrides`. No durable `codex_app` entry exists in global config, 1,977 inspected session metadata records, or Desktop atom state; no state migration is required.

Written: CriomOS-home commit `51676f4eed1c2356faef799ebe8f0d12b933384c` disables that exact producer and adds a disposable app-server start/rollout/resume check. It is pushed. Source-fit, Nix parse, and a direct Codex 0.151.0 start/resume probe passed. The durable Nix check has not run and nothing has been deployed or activated.

Correction: an implementation subflow incorrectly described a local Nix evaluation as remote by overextending the remote-builder rule. The living clarified that the existing rule is itself wrong: remote builders are preferred but local building is required when none are available; remote evaluation should also be used when possible; and trust appears to derive from cluster data and builder/evaluator qualification rather than placement. CriomOS and Lojix code must be inspected before proposing exact replacement wording. Lock 480 was released before the pause.

Open: inspect the execution and trust contracts in CriomOS/Lojix; propose exact `nix-workflow` correction for approval; edit and regenerate the authored skill; test the correction with a fresh flow; then run the focused package check, update/push the immutable consumer revision, deploy Realize then ActivateNow to the verified Lojix target, and ask the living to reopen Desktop before witnessing new and resumed threads.

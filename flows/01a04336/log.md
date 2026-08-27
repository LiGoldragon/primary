# Codex working directory failure

The living reports that Codex works from `~/` regardless of where it is started and requests an immediate repair followed by the proven cause. The living then identified `--remote` as the apparent trigger and ruled that it must preserve the caller's directory; a fallback may be `~/primary` but must not be hardwired into OS or home code. The ordinary launcher must also default to `--sandbox danger-full-access --ask-for-approval=never`.

Settled: the CriomOS-home Codex wrapper selected the remote app-server without forwarding the caller cwd. Upstream remote mode therefore sent no cwd, and the app-server used its systemd service cwd `/home/li`. The wrapper now dynamically injects `--cd "$PWD"` for remote TUI launches unless the caller supplies `-C`/`--cd`, and defaults sandbox/approval unless explicitly overridden. No fallback path is hardwired.

Proof: focused remote `checks.x86_64-linux.codex-tui` passed; Lojix UserEnvironment deployment 78 completed successfully; live handoff traces from `/home/li/primary` and `/tmp/codex-live-second` carried their distinct paths, while explicit cwd/sandbox/approval values remained unchanged. CriomOS-home main is at `4e36d4406f11f770535a7398c10c6bd4deda1a43` with a clean tree and released Locks.

Remembered: 358f143a, 15b67974, 1030529c, 019fe728, 01a01a93, 01a038be, 01a03f49, 01a04236, 01a033a6, 01a02400 — depth 1. Relevant prior direction requires per-flow working directories, warns against globally defective Codex wrapping and hot fixes, and favors a narrow declarative repair; no prior psyche ruling conflicts with the current remote-cwd ruling.

Open outside this repair: the broad existing Agent Intercom check reaches 74 passing tests and then fails because its packaged runtime cannot resolve `typescript`; it was not changed here.

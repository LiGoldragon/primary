# Flow 01a038b8

## About

Determine whether Codex desktop still causes unusually heavy SSD writes, with particular attention to the Linux version.

## Settled

- The inquiry will distinguish direct observations, third-party claims, hypotheses, and unknowns.
- Current Linux behavior, implementation mechanisms, and prior written psyche/context are being investigated independently.
- The severe 0.142-era persistent SQLite TRACE/WebSocket/telemetry amplification was a real reported defect; official fixes landed across 0.142.0–0.145.0.
- The local unofficial Linux wrapper currently bundles Codex 0.148.0. Short samples found its backend idle once and Electron LevelDB compaction writing about 4.7 MiB once; neither sample establishes a sustained endurance rate.
- No public controlled before/after endurance study or local SMART attribution currently proves material NAND wear on the present build.
- Evidence synthesis written to `reports/codexDesktopSsdWrites.md`.
- Desktop and TUI converge in the shared Codex app-server/core, including project-instruction discovery, skills, and core subagent spawning; their client-injected context and workspace selection can differ.
- `/home/li/primary/AGENTS.md` binds a Desktop thread only when that thread's effective workspace is `/home/li/primary` or a descendant. The Linux launcher itself changes to its bundle directory, so launch location alone does not load the rule.
- Current core carries a parent's loaded project instructions into thread-spawned subagents, so the no-Sol instruction should reach Desktop subagents when the Desktop parent loaded it. It remains prompt-level policy, not a hard model-selection guard.

Remembered: 01a0338f, 01a03345, 01a032ec — depth 1

## Open

- What earlier reports meant by “hard on SSDs,” and whether the causal behavior persists.
- Whether Linux differs from macOS or Windows in write volume or storage implementation.
- Which versions, configurations, and workloads are affected, and what mitigations are credible.
- Whether the reported plugin-catalog rewrite and SQLite space-reclamation issues are fixed in stable 0.149.1.
- The exact Desktop renderer thread-start payload and whether every current Desktop workspace path propagates unchanged into spawned children.

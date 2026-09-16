# Morning review — 16 September 2026

This is a checkpoint; overnight work continues on proposal branches. Nothing was merged to main or deployed under the night order.

## Ready to inspect

- Message: remote Nix checks passed for repeated idle notifications and durable storage before a socket write. The relay selector now excludes the actual provenance wrappers, including split text parts, with a focused remote check. Live Rust Claude/Nexus delivery and dependency convergence remain incomplete.
- Flow hooks: remote Nix fixtures passed; receipts distinguish acceptance from delivery and classify errors without storing their full text. Hooks were not installed.
- Core monitor: a proposed advisory-lock fix passed 11 remote Nix tests, including recovery after killing the lock holder. It has not replaced the installed runner.
- MCP component adapter: four remote fixture tests passed with a valid Nix result; only the Orchestrate backend is implemented. Original build CLI exit code was lost and is not claimed.
- Flow idleness and Psyche records: bounded remote Nix proofs passed.
- Notify proof: the generated `Notify.{…}` constructor, typed outcomes, escaping and packaged consumer passed focused remote checks, with a current durable receipt. Separate offline OMEMO2 roundtrip/tamper rejection passed. Live bot/phone interoperability remains unfinished.
- Prometheus TLS: focused remote policy fixture passed, including disposable SAN certificates, permissions and refusal cases. No service activation.
- Cloudflare: a scoped messaging DNS plan reuses the existing provider client; remote read-only and out-of-scope refusal checks passed. No DNS changes or certificate issuance.
- Slint prototype: the Linux example now builds remotely after fixing a stray derive attribute. The separate behavioral check is running; Android and live phone connectivity are not proved.
- Native launcher correction: local and remote mock checks passed for disconnected stdin, literal arguments, manifest validation and argument limits; no additional session launched.
- Claude successor: v4 launched through the daemon as Flow efa157. Roster, active bridge and an exact prompt-relay user turn are witnessed. Two defects remain explicit: the worker inherited the daemon’s terminal cgroup, and inherited stdin appended the launcher script to the intact first prompt.

## Still held or incomplete

All four held user turns have reached successor efa157 with exact transcript/hash receipts. None is retrospectively delivered to predecessor 840e42, whose approval gate remains blocked. Published reports and transport acknowledgements are kept separate from user-turn receipts.

Prometheus service modules and a bounded build runner remain proposals under test. There is no deployed messaging service, encrypted chime bot, live wake transport or completed mobile client.

The monitor succeeded through 23:52 CST, then failed before execution at 00:22: nightly garbage collection deleted its unrooted roster and runner source paths. Both exact artifacts are restored and GC-rooted. Scheduled runs at 07:22, 07:52, 08:22 and 08:52 UTC then completed successfully. A separate remote Home Manager check now proves the generated unit retains both its runner and roster in its Nix dependency closure; that proposal has not changed the live unit. The timer remains active. Repairs and wake messages remain disabled. The installed roster still names predecessor 840e42; successor efa157 has its own native wake loop. The latest checkup recorded 31% Codex Pro remaining at 08:52Z; no reset credit was used.

Detailed commits, tests, corrections and remaining work are in [the paired report](to-840e42.md). Architecture, repository, model-call and language documents are review proposals, not implemented contracts.

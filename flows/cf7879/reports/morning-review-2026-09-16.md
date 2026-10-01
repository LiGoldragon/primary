# Morning review — 16 September 2026

This is a checkpoint; overnight work continues on proposal branches. Nothing was merged to main or deployed under the night order.

## Ready to inspect

- Message: remote Nix checks passed for repeated idle notifications and durable storage before a socket write.
- Flow hooks: remote Nix fixtures passed; receipts distinguish acceptance from delivery and classify errors without storing their full text. Hooks were not installed.
- Core monitor: a proposed advisory-lock fix passed 11 remote Nix tests, including recovery after killing the lock holder. It has not replaced the installed runner.
- Flow idleness and Psyche records: bounded remote Nix proofs passed.
- Notify proof: bounded validation CLI plus separate offline OMEMO2 roundtrip/tamper rejection passed remote Nix. Shared Datom integration and live bot/phone interoperability remain unfinished.
- Prometheus TLS: focused remote policy fixture passed, including disposable SAN certificates, permissions and refusal cases. No service activation.
- Cloudflare: a scoped messaging DNS plan reuses the existing provider client; remote read-only and out-of-scope refusal checks passed. No DNS changes or certificate issuance.
- Claude successor: v2 restores the launch-history context and current audits after primary review; 159 source records. Launch remains held for review and verification of the large-payload daemon path.

## Still held or incomplete

The four original user turns have not reached Claude as witnessed user turns. Its approval gate remains a blocker; a separate pointer attempt was denied. Published reports are available through the primary’s branch watcher, but that is not a delivery receipt.

Prometheus service modules and a bounded build runner remain proposals under test. There is no deployed messaging service, encrypted chime bot, live wake transport or completed mobile client.

The monitor succeeded through 23:52 CST, then failed before execution at 00:22: nightly garbage collection deleted its unrooted roster and runner source paths. Both exact artifacts are restored and GC-rooted. The scheduled 07:22 UTC run then completed successfully. The timer remains active. Repairs and wake messages remain disabled. The latest recorded quota was 37% Codex Pro remaining at 07:22Z; no reset credit was used.

Detailed commits, tests, corrections and remaining work are in [the paired report](to-840e42.md). Architecture, repository, model-call and language documents are review proposals, not implemented contracts.

# Morning review — 16 September 2026

Proposal work is published for review. Nothing was merged to main or deployed under the night order.

| What was put together, and why | What it looks like | Reliability and tests |
| --- | --- | --- |
| Relay fixes, so peers receive source text without loops | Transcript lookup plus explicit file sending; live-PID filtering and idle-only Claude paste | Local process and remote Nix checks pass, including single paste, ambiguity and provenance exclusion. Message's producer/consumer checks now use one Signal source. Configured Claude and Nexus adapters now pass process checks; production route registration and live user-turn delivery remain open. |
| Flow hooks and records, so activity leaves small evidence | Typed launch/hook/error fixtures and Flow-owned idleness API | Focused remote checks pass. Hooks and cross-process registry access are not installed. |
| Core checkup, so failed checks do not stall later runs | Deterministic bounded runner, kernel lock, pinned Home unit; separate disabled wake adapter | Runner: 12 remote tests. Home: remote configuration/closure check. Wake: five local tests plus remote check. Installed runner remains old; wake integration and live delivery remain open. |
| Cloudflare and messaging service proofs | Scoped DNS plan, typed Notify parser, offline encryption proof, TLS renewal and SOPS declarations | Focused remote checks pass, including enabled NixOS toplevel evaluation for self-signed and SOPS modes. Secret installation, DNS changes, live bot/phone interoperability and service reload are unproved. |
| Slint client proof, so there is a concrete UI to develop | Isolated Linux graphical binary with bounded offline reply state | Remote binary compilation and four state tests pass. Display runtime, Android, packaging and live connectivity remain open. |

## Coordination and remaining work

The four held original turns reached successor **efa157** with exact transcript/hash receipts. They have not been delivered to predecessor **840e42**. Native message acceptance is not a delivery receipt; the published paired report is 840e42's channel.

Primary agrees to isolated workspaces, writer-owned commits, preserving others' dirty work and keeping producer pushes off main. The integrator remains unnamed; law adoption and main movement remain held.

The installed monitor recovered after its exact garbage-collected artifacts were restored and rooted. It still uses the old roster/runner, with repair and wake disabled. Its newer tested replacement has not been activated. The successor launch also retains two disclosed defects: inherited terminal cgroup and launcher text appended through stdin.

Next: finish live cluster relay and connect the checked wake adapter, then continue Cloudflare-first messaging/service work. Other architecture, identifier, MCP and language proposals retain their individual limits in [the paired report](to-840e42.md).

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

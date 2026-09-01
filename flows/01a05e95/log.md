# Flow identity realization

Realized one parent-owned flow lane with focused child contexts. The parent supplies one shared `FLOW_ID` and `FLOW_DIRECTORY`; each child obtains its own thread identity after launch, performs its work, creates no lane/index/log, and returns its final response. Optional reports and witnesses use the parent lane through `flow-evidence`.

Settled:

- Replaced the overloaded `flows`/`subflows` skills with user-only `main-flow`, model-loadable `child-flow`, and on-demand `flow-evidence`; updated vocabulary, dependencies, generated visibility metadata, deployment documentation, and tests.
- Corrected the initially impossible pre-spawn `THREAD_ID` requirement: only shared flow identity/directory enter the brief; a child obtains its transcript identity after launch.
- Curriculum, curriculum-deploy v0.2.2, and regenerated primary projections are committed and pushed; remote, isolated, and live Nix checks pass.
- A fresh direct child and nested fresh Codex child propagated the parent identity unchanged, acquired distinct thread identities, and created no child artifacts or index rows.
- Transcript-grounded migration consolidated all 24 proven child/extended lanes into their root lanes, preserved 46 durable artifacts byte-for-byte, compacted rather than concatenated logs, normalized the index, and retained all nine legitimate mixed-prefix root directories.
- Live conflicts were resolved without discarding current flow state; all retired lanes are physically absent and no Jujutsu conflicts remain.
- Added the harness-owned `flow-id` helper: Codex claims the normalized hexadecimal `CODEX_SESSION_ID[23:29]` alias, extends collisions, publishes complete private identity markers atomically under a stable filesystem lock, and resumes idempotently; Claude accepts an explicit parent UUID.
- The corrected deterministic publication-race test, 11 helper integrations, full Harness remote checks, focused Home checks, immutable CriomOS activation evaluation/build, and exact closure witness pass; the closure executable returns `715d46`.
- Harness, Home, Curriculum, curriculum-deploy, primary, and the CriomOS consumer pins are committed and pushed. All work locks were released; unrelated locks were untouched.

Open:

- Native automatic child-brief injection is not present in an owned checkout; the witnessed runtime contract is explicit parent-brief propagation.
- Live Home activation was not attempted: Lojix lacks an explicit deployment projection/proposal/transport/selector, and the full Home gate has the pre-existing `home-ol5` orchestrate-wrapper failure even though the immutable activation closure is green.
- The loaded Orchestrate skill's braced release syntax disagrees with deployed Orchestrate 0.26's bare release product; a skill-variable correction awaits living approval.

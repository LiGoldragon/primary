# CriomOS-b8x: Zeus embedded Home package convergence

Zeus is Current at immutable CriomOS `ab005ef8bc8828e1f92563cbb4bb966c2adda5bc`.
Lojix TestActivation 57 and then ActivateNow 58 succeeded. Both active
embedded Homes resolve Codex 0.149.1 and Claude Code 2.1.241; no reboot,
direct profile mutation, manual Nix copy, or hot fix was used.

Generation 64 was green for the wrong intended versions because CriomOS
pinned Home `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee` rather than refreshing
its lock to the already-published Home update. It therefore correctly built
and activated Codex 0.148.0 / Claude 2.1.235 from that immutable source.
That explains why green did not mean latest. Historic UserEnvironment 49 is
separate: it logically chose Zeus but physically targeted Ouranos. Its
origin is not established and remains unknown.

The updated producer selected stable Codex 0.149.1, kept Claude's existing
authored latest-channel 2.1.241, and advanced Codex VSIX 26.5818.61809 because
the authored policy explicitly couples that sidebar to a Codex refresh.
Candidate sidebar metadata was corrected before the final build and deploy.
The producer is `0836e4b7e367efe6a81a4fa657e2a2f741f0d801`.

Projected evaluation and a 35-derivation Prometheus-only build passed before
the required Ethernet-store/Yggdrasil-activation deployment. Persistent and
current system are new; booted closure remains previous; default boot entry is
new; system is running and has no failed units. Standalone profiles are
separate historical links but presently resolve the final Codex package.

The advisory orchestration socket was unavailable. Clean manual isolated
worktrees were used, then forgotten and moved recoverably to Trash after
published commits were verified. No Beads record changed.

## Sources

- [source/build witness](../witnesses/criomosB8xSources.md)
- [Zeus deployment/live witness](../witnesses/criomosB8xZeus.md)
- [generation-64 completion](../../01a030b7/reports/zeusUpdateCompletion.md)
- [generation-64 embedded Home](../../01a030b7/witnesses/embeddedHomeSynchronization.md)
- [written Home equivalence intent](../../01a02b4b/vision/homeEquivalence.md)

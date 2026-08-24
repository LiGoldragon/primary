# CriomOS-b8x: Zeus embedded Home package convergence

Zeus now runs immutable CriomOS `ab005ef8bc8828e1f92563cbb4bb966c2adda5bc`.
Both active embedded Homes, `li` and `bird`, resolve Codex CLI 0.149.1 and
Claude Code 2.1.241. Lojix TestActivation 57 and then ActivateNow 58 both
reached `Succeeded`; no reboot, profile mutation, manual Nix copy, or hot fix
was used.

Generation 64 was green for the wrong intended package set. It pinned
CriomOS-home `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`, supplying Codex
0.148.0 and Claude Code 2.1.235, because the consumer did not refresh its
Home lock to the already-published update. NixOS/Home activation correctly
realized that old immutable pin, so green generation 64 was not proof of the
intended latest packages. This is the grounded omission cause.

Historic UserEnvironment 49 is separate: it logically selected Zeus but
physically targeted Ouranos. It was not reused. The records establish the
mismatch but not how it originated, which remains unknown.

The producer selected stable Codex 0.149.1, retained Claude's authored
latest-channel 2.1.241, and advanced Codex VSIX 26.5818.61809 because the
Home policy explicitly couples that sidebar to a CLI refresh. Candidate stale
sidebar metadata was corrected before final build/deploy. The final producer
is `0836e4b7e367efe6a81a4fa657e2a2f741f0d801`; the final consumer is
`ab005ef8bc8828e1f92563cbb4bb966c2adda5bc`.

Canonical projected evaluation and remote-only Prometheus build were both
green. Deployment used Ethernet `192.168.18.95` for store transfer and Zeus's
Yggdrasil hostname for activation. Post-activation, persistent/current system
is new, booted system is previous (no reboot), default boot entry is new,
system is running, no units failed, and both embedded Home services completed.

Standalone `.nix-profile` roots remain distinct from embedded Home
generations, but they resolve the same 0.149.1 executable. They are retained
historical/profile links, not an evidenced stale CLI mismatch.

The advisory edit-coordination clients rejected the prescribed Dotos grammar;
clean manual isolated worktrees were used and shared checkouts were untouched.
No Beads record was changed.

## Sources

- [source and remote-build witness](../witnesses/criomosB8xSources.md)
- [Zeus deployment and live-state witness](../witnesses/criomosB8xZeus.md)
- [generation-64 completion report](../../01a030b7/reports/zeusUpdateCompletion.md)
- [generation-64 embedded Home witness](../../01a030b7/witnesses/embeddedHomeSynchronization.md)
- [embedded/standalone written psyche](../../01a02b4b/vision/homeEquivalence.md)
- implementation subflow `/root/deploy_latest_agents/land_deploy_b8x`, direct
  closeout supplied 2026-08-24

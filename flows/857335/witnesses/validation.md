# Validation witness

Method: configured remote Nix builder (`prometheus.goldragon.criome`) ran the
Protos test, formatting, clippy, documentation, and structural-policy checks.

The Protos test gate passed after a real failure witness: an ordinary
backslash inside guillemets was dropped on round-trip. The correction preserves
it while retaining `\\»` as the escaped close form.

Datom and Ethos Zero have not passed their durable gates yet; this witness does
not claim them green.

The deferred Protos generated-contract check remains explicit: it depends on
the Ethos Zero migration and cannot witness the new declaration until that
generator is pinned and rebuilt.

2026-09-10: Protos `0.28.1` at
`d038d20730dc5bfad32119477be3bc8778d5ca5f` passed `nix flake check -L` on the
configured Prometheus remote builder. The gate included build, test, fmt,
clippy, docs, generated-contract, and structural policy checks. Its test suite
contains actual 100,000-node print-and-drop witnesses, replacing the prior
`mem::forget` suppression.

2026-09-10: Datom `0.25.2` at
`cf7d7a7a1f2b43e97ba4c8259f2737054997acbc` passed 25 local tests and the
configured remote `nix flake check -L` after the Ethos `Option<Box<Chain>>`
derive-overflow regression was corrected.

2026-09-10: Protos `0.28.2` at
`e18abf0936f23a175ec3c554f994214fabbdf2bd` passed 16 local tests and the
configured remote `nix flake check -L` for canonical extent assignment.

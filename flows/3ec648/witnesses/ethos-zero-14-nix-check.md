# ethos-zero 14.1.0 nix flake check

Method: scratch clone of /git/github.com/LiGoldragon/ethos-zero checked out at remote main
2db764d200da (parent fac6b5869902; Cargo version 14.1.0; `git ls-remote origin main` =
2db764d200daff0da291a644155f4e475568394d). Ran `nix flake check -L --keep-going` as detached
transient user unit `ez14check` (MemoryMax=8G, RuntimeMaxSec=5400), waiting on the unit's end.
Builds ran on ssh-ng://nix-ssh@prometheus.goldragon.criome. Unit Result=success; check exit 1.
Duration: 1655 s (about 27m35s). Full log: scratchpad `check.log` (785 lines).

Flake outputs (x86_64-linux): 11 flake checks run (packages.default, 8 checks, devShells.default, plus the cached-source build).

| check | result |
|---|---|
| packages.default | pass |
| checks.build (ethos-zero-build-14.1.0) | pass |
| checks.test (ethos-zero-test-14.1.0) | pass (18, 9, 2 tests ok, 0 failed, among suites) |
| checks.fmt | pass |
| checks.clippy | pass |
| checks.doc | pass |
| checks.no-free-functions | pass |
| checks.no-inherent-methods | pass |
| checks.dependency-ethos | FAIL |
| devShells.default | pass (evaluated) |

Passes are inferred from --keep-going reporting only dependency-ethos as failed.

## Failure: checks.dependency-ethos
```
Generated.[ /build/generated/protos.rs ]
Generated.[ /build/generated/protos-kinds.rs ]
/nix/store/vpxmp5v38xinmgd8ywx8qz9zvh4dknkr-source/datom-codec.ethos (exit 1): Rejected.{ ... datom-codec.ethos { 21 30 } Conceptual.{ [ 1 2 0 1 0 1 0 0 ] KindWanted.Path } }
```
Two dependency declarations (protos) generate; datom-codec.ethos is rejected by the built tool
with a Conceptual KindWanted.Path error at extent 21..30. The check script
(checks/dependency-ethos.sh) stops at the first rejection. Likely the pinned datom-codec
dependency has not adopted 14.1.0's "take kinds as capability inputs" change (fac6b58) at
that position; not diagnosed further.

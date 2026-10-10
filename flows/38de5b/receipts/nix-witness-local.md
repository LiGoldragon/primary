# Nix witness, local build on ouranos (2026-09-25)

Ruling e51411: local builds on ouranos allowed while Prometheus is down. Nothing was activated or installed.

## Method

Fresh `git clone` of each repo from GitHub into the unique scratch directory
`…/scratchpad/nixw-38de5b-opus/<repo>`, one Orchestrate lock per clone (IDs 6508-6513), released afterwards.
Each command ran with
`-L --option max-jobs auto --option substituters https://cache.nixos.org --option builders ''`
(the empty `builders` forces a local build, so Prometheus was not tried; nix.conf and Home were left unchanged). `nix flake check` stops at the first failure.

## Results

| # | Repo @ rev | Command | Result | First failing derivation |
|---|---|---|---|---|
| 1 | clj-build @ 01126ad | flake check | FAIL | `0xf3dcdsj3…-example-uberjar.drv` |
| 1 | clj-build @ 01126ad | build `.#checks.x86_64-linux.example-jar-consumer` | FAIL | same `example-uberjar.drv` (dependency) |
| 2 | field-clj @ 929936a | flake check | FAIL | `7zrjp1xm…-field-clj-uberjar.drv` (the `field-clj-deps` fixed-output derivation built with no hash mismatch, so the fetchCljDeps hash is proven) |
| 3 | ethos-zero @ 2a39e50 (main) | flake check | FAIL | `0srwlp35…-ethos-zero-dependency-ethos.drv` (package, tests, and clippy built before it) |
| 4 | tree-sitter-ethos @ ee84bbf (main, 0.3.0) | flake check | PASS | none (3 checks) |
| 5 | flow @ 84e2304 (main, 0.10.4) | flake check + `nix build` | PASS / PASS | none (23 checks) |
| 6 | messenger-clj @ dd358c4 (m6-nix-38de5b) | flake check + `nix build` (no install) | PASS / PASS | none (5 checks) |

## Failure logs

### clj-build example-uberjar (field-clj-uberjar fails the same way)

The uberjar step copies compiled classes into `staging/`, which already holds files copied read-only from the store. It is a clj-build uberjar builder defect: it needs `chmod -R u+w staging` (or `cp --no-preserve=mode`) before the class copy. field-clj inherits it.

```
example-jvm-tests> Ran 2 tests containing 2 assertions.
example-jvm-tests> 0 failures, 0 errors.
example-uberjar> clj-build.launcher
example-uberjar> cp: cannot create regular file 'staging/./example/main$greet.class': Permission denied
example-uberjar> cp: cannot create regular file 'staging/./example/main$_main.class': Permission denied
example-uberjar> cp: cannot create regular file 'staging/./example/main$loading__6812__auto____138.class': Permission denied
example-uberjar> cp: cannot create regular file 'staging/./example/main$fn__4047.class': Permission denied
example-uberjar> cp: cannot create regular file 'staging/./example/main__init.class': Permission denied
error: build of '/nix/store/0xf3dcdsj3ylmr2wb9l9jc2kvcqqk2jk-example-uberjar.drv^*' failed
       Reason: builder failed with exit code 1.
       Output paths: /nix/store/z8frl1516llh2nizqicd5r5c2sk1mspv-example-uberjar
```

field-clj's last lines are the same `cp: cannot create regular file 'staging/./field_clj/…class': Permission denied` and `cp: cannot create directory 'staging/./field_clj/commit': Permission denied`, from `/nix/store/7zrjp1xm94jac9iw2qrvlg9rp2833nwk-field-clj-uberjar.drv`.

### ethos-zero dependency-ethos

```
building '/nix/store/0srwlp356cn1x5psiq7kh2jdjg6l44h0-ethos-zero-dependency-ethos.drv'...
ethos-zero-dependency-ethos> Generated.[ /build/generated/protos.rs ]
ethos-zero-dependency-ethos> Generated.[ /build/generated/protos-kinds.rs ]
error: failed to build attribute 'checks.x86_64-linux.dependency-ethos'
       Reason: builder failed with exit code 1.
```

The check exits without a message because `set -eu` aborts on the non-zero exit inside `reply="$(…)"`, before the rejection is printed. I reran the same built binary (`5r2m21i4…-ethos-zero-13.0.0`) by hand on the locked datom-codec input (09e2a9d, `17y75hdv…-source`):

```
Rejected.{ …/datom-codec.ethos { 11 3 } Conceptual.{ [ 1 1 3 0 ] Intrinsic.Meaning } }   exit=1
Generated.[ …/datom-codec-kinds.rs ]                                                     exit=0
```

ethos-zero 2a39e50 rejects datom-codec.ethos line 11 (`Meaning.String`) as a conceptual `Intrinsic.Meaning` error. The fix belongs to the owners, in datom-codec's declaration or in ethos-zero's intrinsic-name rule. The check script should also print a non-`Generated` reply when the tool exits non-zero.

No fixed-output hash was wrong.

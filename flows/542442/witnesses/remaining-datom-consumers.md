# Verification witness: remaining portable Datom consumers

All local commands completed successfully on the frozen revisions:

| Repository | Focused local evidence |
| --- | --- |
| relative-age-display | `cargo test` (20 tests) |
| Chroma | `cargo fmt --check && cargo test --all-targets` (131 active tests; one existing DBus test remains intentionally ignored outside its session harness) |
| Chronos | `cargo fmt --all --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check --all-targets`, and `cargo test --all-targets` (65 tests) |

The changed-boundary tests exercise typed Datom incorporation and canonical
rendering, malformed structure and range rejection, authored-Ethos-to-current-
generated projection checks, and rkyv request/reply round trips where those
utilities use a durable frame. Chroma's remote gate additionally ran the real
DBus and sandbox-terminal checks.

Prometheus gates completed successfully using:

```sh
nix flake check -L --no-write-lock-file --max-jobs 0 --option fallback false
```

for relative-age-display (with its remote test derivation), Chroma (default,
DBus, and sandbox-terminal checks), and Chronos (build, test, doc, fmt,
clippy, and Ethos-source checks). Chronos's first remote run exposed four
`clippy::useless_conversion` findings in the newly written readers; revision
`a5cf51f4` removes them, and the repeated complete remote gate passed.

Locks 872, 873, 874, 876, 877, 882, and 883 were retained through landing and
then released with typed `Released` replies after this record handoff.

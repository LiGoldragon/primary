# Nix flake checks — signal realization

## Method

For each repository, after its change was committed and pushed, run from
its checkout at `/git/github.com/LiGoldragon/<repository>`:

    nix flake check --max-jobs 0 -L

`--max-jobs 0` forbids local building, so every derivation was built on
the configured remote builder `ssh-ng://nix-ssh@prometheus.goldragon.criome`
(`/etc/nix/machines`). Full output of each run is the sibling file
`<repository>-flake-check.txt`, ending in the recorded process exit
status. Evaluation was run separately first for `signal`
(`nix flake check --no-build`, all checks evaluated) before any build.

Run on 2026-09-12.

## Results

| repository | revision | version | exit |
| --- | --- | --- | --- |
| `signal` | `626e407be520` | 2.0.0 | 0 |
| `signal-lojix` | `662cedb7d92b` | 2.0.0 | 0 |
| `meta-signal-lojix` | `f7f11d410d68` | 3.0.1 | 0 |
| `signal-spirit` | `e4ab10624a0a` | 2.0.0 | 0 |
| `meta-signal-spirit` | `a4b8cddedd05` | 2.0.1 | 0 |
| `signal-orchestrate` | `7408fb6f5f2b` | 2.0.0 | 0 |
| `meta-signal-orchestrate` | `d8e035014a26` | 2.0.2 | 0 |
| `lojix` | `fab60e584daf` | 2.0.0 | 0 |

Every run ends `all checks passed!`.

Two runs failed before the state recorded above, and both failures are
kept in the record by what they caused rather than by their logs, which
were overwritten by the passing re-runs:

- `meta-signal-orchestrate` at 2.0.0 failed evaluation of its dependency
  graph — `failed to read /git/github.com/LiGoldragon/signal-orchestrate/Cargo.toml`
  — because the crate pinned its ordinary contract by absolute local path.
  Fixed by pinning the pushed revision (2.0.1).
- `meta-signal-orchestrate` at 2.0.1 failed its default-feature `clippy`
  check on `error: unused import: ConfigurationReceipt` in
  `tests/generated_contract.rs`, where the type was used only under the
  `datom` feature. Fixed by round-tripping `Response::Configured` on the
  portable path, which both uses the import and covers a reply that had no
  non-Datom test (2.0.2).

`orchestrate` was not checked: it was not changed.

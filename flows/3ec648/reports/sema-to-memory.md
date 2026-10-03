# Sema to Memory: the seven consumers

Nothing was renamed, repinned or committed. The UPGRADES entry of ethos-zero
15.0.0 says the seven `.ethos` files headed `Sema` are consumers to rename.
Read at each repository's remote main, none of them is an ethos-zero consumer
that can be renamed.

- None of the six repositories has ethos-zero in `Cargo.toml` or `flake.nix`,
  so nothing can be repinned.
- Nothing is generated from any of the seven files, so nothing can be
  regenerated.
- Five of the files are in an older dialect. They have versioned heads
  (`Sema.1`, `Sema.{1 0 0}`) and braced bodies, and ethos-zero refuses them
  whether the head says `Sema` or `Memory`.
- The other two are witnesses in another flow's own directory.

ethos-zero main was still 3d330276 (15.0.0) during this work, so 15.1 had not
landed.

## Per file

| file | repository state | ethos-zero 15.0.0 Check, as is / head renamed to Memory | outcome |
|---|---|---|---|
| spirit-ethos/sema.ethos | AGENTS.md: "Status: frozen reference … No new code is accepted here" | `{2 1} Structural.ProtosError … Multiple` / the same | skipped: frozen, other dialect. Its own flake check greps for `Sema.1` |
| spirit/schema/sema.ethos | README: deprecated 2026-09-10; "drafts in a dialect ethos-zero does not read, nothing is generated from them" | `{8 1} Structural … Multiple` / the same | skipped: deprecated, other dialect |
| core-schema/tests/fixtures/bootstrap/sema.ethos | the same GitHub repository as core-ethos (same main 8186209); AGENTS.md: "Status: frozen reference" | `{2 1} Structural … Multiple` / the same | skipped: frozen. The fixture is read by core-ethos's own bootstrap reader, where `Sema` is that reader's vocabulary |
| core-ethos/tests/fixtures/bootstrap/sema.ethos | the same as above | the same as above | skipped: frozen |
| primary-next/reports/spiritEthosFixtures/sema.ethos | copy of a spirit-ethos fixture in a report | `{2 1} Structural … Multiple` / the same | skipped: other dialect, report evidence |
| primary-next/flows/f6db8d/witnesses/substrate/probe-ethos/sema-record.ethos | witness in flow f6db8d's own directory | `Renamed.Memory` / `Checked` | skipped: only flow f6db8d writes in its directory (edit-coordination). Rewriting the probe would falsify its witness |
| primary-next/flows/f6db8d/.../sema-plain.ethos | the same | `Renamed.Memory` / `Checked` | skipped: the same |

For the two f6db8d probes, the Rust that 15.0.0 generates from the
Memory-headed copy is byte-identical (`cmp`) to what 14.2.0 (06d73e0)
generates from the original. The rename is therefore lossless in ethos-zero
itself. It has nowhere to land.

ethos-engine is not among the seven, so it was not touched.

## Not done, and why

No checkout was edited, so no Lock was taken. There were no commits, version
bumps or UPGRADES entries, and no `nix flake check` ran.

## For the main flow

- ethos-zero's UPGRADES ("Consumers to rename") lists the seven files as
  consumers. They are not consumers. The list could say so: five are in an
  older dialect that ethos-zero already refuses, and two are frozen witnesses
  of f6db8d. As far as can be seen, the Sema to Memory rename has no consumer
  under `/git` to deploy to.
- Whether to amend that UPGRADES text is the main flow's decision. It was not
  in this brief.

## Method and sources

- Each file was read with `git show origin/main:<path>` after `git fetch`. The
  local checkouts of spirit-ethos and spirit carry other work, uncommitted, and
  it was left untouched.
- ethos-zero built with `nix build github:LiGoldragon/ethos-zero/3d330276…`
  (store path `…-ethos-zero-15.0.0`) and `/06d73e0` (14.2.0). The Check and
  Generate runs were on scratchpad copies under
  `/tmp/claude-1001/-home-li-primary/3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3/scratchpad/probe`.

## Sources

- /home/li/primary/flows/3ec648/reports/ethos-zero-15-roots.md
- ethos-zero origin/main 3d330276 UPGRADES.md, 15.0.0 entry
- spirit-ethos origin/main dfca49b (AGENTS.md, flake.nix, sema.ethos)
- spirit origin/main 6aa8701 (README.md)
- core-ethos / core-schema origin/main 8186209 (AGENTS.md, README.md)
- primary-next origin/main 251d40f7 (flows/f6db8d/reports/substrate-audit.md, self-audit.md)

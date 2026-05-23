# 4 — Overview: bead repair and first implementation wave

*Kind: Meta-report overview · Topic: /310 bead repair + subagent implementation wave · Date: 2026-05-23 · Lane: operator*

## Outcome

The session completed the psyche's instruction from Spirit record 361: repair the `/310` dependency graph, then use subagents on the beads that became genuinely ready.

Closed beads:

| Bead | Result | Commit / witness |
|---|---|---|
| `primary-li0p` | `signal-frame` now exposes `NamespaceSection`, `SECTION_CUTOFF = 100`, and const classify helpers. | `signal-frame` commit `c18a3fda055d41f6b8aeb140b11aebb5479ebc21`; `cargo test -p signal-frame`, `cargo check --workspace`, `nix flake check --option max-jobs 0 -L`. |
| `primary-avog` | `signal-frame::assert_triad_sections!` now compile-time checks ordinary/owner section disagreement at the daemon witness site. | Same `signal-frame` commit `c18a3fda055d41f6b8aeb140b11aebb5479ebc21`; trybuild compile-fail witness plus full flake check. |
| `primary-gvgj.1` | New `signal-persona-agent` ordinary contract crate landed locally. | `/git/github.com/LiGoldragon/signal-persona-agent` commit `a7f06b68`; `cargo test`; `nix flake check --option max-jobs 0 -L`. |
| `primary-gvgj.2` | New `owner-signal-persona-agent` owner-policy contract crate landed locally. | `/git/github.com/LiGoldragon/owner-signal-persona-agent` commit `2f810422`; `cargo test`; `nix flake check --option max-jobs 0 -L`. |

The next `bd ready` roots now include:

- `primary-v5n2` — `signal-frame-macros` `contract_section` grammar and section-bounded discriminator allocation.
- `primary-2cjv` — `signal-frame` `micro: u64` frame reshape.
- `primary-gvgj.3` — `persona-agent` daemon skeleton, now unblocked by the two contract crates.
- `primary-8r1j` — Help operations auto-injection.

## Dependency graph repair

The inverted dependency graph called out in operator report `/164` was repaired before implementation.

Golden-ratio chain:

- `primary-li0p` is the root.
- `primary-v5n2` and `primary-avog` depend on `primary-li0p`.
- `primary-muu2` depends on `primary-v5n2` and `primary-avog`.
- `primary-g21y` depends on `primary-muu2`.

Pre-typed envelope/tap chain:

- `primary-2cjv` is the root.
- `primary-3cl1` depends on `primary-2cjv`.
- `primary-bann` depends on `primary-2cjv` and `primary-3cl1`.
- `primary-145a` depends on `primary-bann`.

Persona-agent epic:

- `primary-gvgj.1` and `primary-gvgj.2` are root contract beads.
- `primary-gvgj.3` depends on the two contracts.
- `primary-gvgj.4` through `.9` depend on the skeleton.
- `primary-gvgj.10` depends on `.4` through `.9`.

`bd dep cycles` returned no cycles after repair.

## Subagent fanout

Three workers ran under async run `caf69387-dba6-49b6-aa0f-bec8dbd870d7`.

Sub-report locations:

- `1-signal-frame-foundation.md` — copied into this meta-report directory from the signal-frame child output path.
- `2-signal-persona-agent-contract.md` — ordinary contract child report.
- `3-owner-signal-persona-agent-contract.md` — owner contract child report.

The signal-frame child accidentally wrote its report under the `signal-frame` repo because its output path was relative to its cwd. The parent copied that report into the primary meta-report directory, then abandoned the accidental `signal-frame` report commit and restored the `main` bookmark to the implementation commit. The `signal-frame` repo now has only the intended implementation commit plus its pre-existing dirty `ARCHITECTURE.md` working-copy change.

## Parent review and amendments

The parent made one post-worker correction before closing the two contract beads: remove repeated `OperationKind` fields from generic request failure replies, per Spirit record 351 (`signal`, Constraint, Maximum): per-operation request replies should not repeat operation kind.

Amended surfaces:

- `signal-persona-agent`: `RequestUnimplemented` now carries only `UnimplementedReason`; canonical NOTA is `(RequestUnimplemented (NotBuiltYet))`.
- `owner-signal-persona-agent`: `OrderRejected` carries only `RejectionReason`; `RequestUnimplemented` carries only `UnimplementedReason`; canonical NOTA is `(RequestUnimplemented (NotBuiltYet))`.

Both amended commits were squashed into the original scaffold commits with `jj squash --into @- --use-destination-message`.

## Current repository state

- `/git/github.com/LiGoldragon/signal-frame`: local `main` at `c18a3fda` (`namespace section split foundation`); working copy still has the pre-existing `ARCHITECTURE.md` modification from earlier design work.
- `/git/github.com/LiGoldragon/signal-persona-agent`: local `main` at `a7f06b68` (`Scaffold signal-persona-agent contract`); working copy clean; not pushed.
- `/git/github.com/LiGoldragon/owner-signal-persona-agent`: local `main` at `2f810422` (`owner persona agent contract scaffold`); working copy clean; not pushed.
- `/home/li/primary`: report files remain uncommitted in a dirty primary workspace that also contains unrelated designer/system-designer/report-maintenance changes. Do not broad-commit from primary without an explicit split.

## Follow-up cautions

1. New contract repos still need remote creation/push by the appropriate operator authority.
2. `primary-gvgj.3` should decide whether shared nouns (`AgentIdentifier`, `AgentBackend`, lane/backend configuration vocabulary) remain duplicated across the two contract crates, move into a shared crate, or get re-exported intentionally from the ordinary contract. The owner contract report already flags this.
3. `primary-v5n2` is the next natural golden-ratio bead: `signal_channel!` should emit `CONTRACT_SECTION` and allocate discriminators inside `NamespaceSection::Small` or `NamespaceSection::Big`.
4. `primary-2cjv` is ready but conflicts with the same `signal-frame` surface as the just-finished foundation work; sequence it carefully around the pre-existing `ARCHITECTURE.md` working-copy change.

# 75 — horizon-rs and lojix-cli audit against workspace discipline

*Audit findings, applied fixes, and the breaking-change items
left for human approval.*

---

## What the audit covered

Both `horizon-rs` and `lojix-cli` walked end-to-end against
this workspace's `skills/rust-discipline.md`,
`skills/abstractions.md`, `skills/naming.md`,
`skills/beauty.md`, `skills/micro-components.md`, and
`skills/nix-discipline.md`. ~6.5k LOC total across 31 source
+ 5 test files. The audit was structural (does it follow the
disciplines?), not behavioral (do the methods do the right
thing?).

---

## What landed (committed and pushed)

### horizon-rs — `11d3647`

```
audit: Iface→Interface, EmptyYggSubnet variant, use reorder, skills.md
```

| Change | Why |
|---|---|
| `Iface` → `Interface` (`lib/src/address.rs`, `lib/src/proposal.rs`) | `naming.md` "full English words" — `iface` is not in the six narrow exception classes; internal-only rename, JSON wire shape unchanged |
| `Error::EmptyYggSubnet` variant; `YggSubnet::try_new` no longer fakes `AddrParseError` | `beauty.md` — `"::".parse::<Ipv6Addr>().unwrap_err()` to construct a fake source error was a clear ugliness signal |
| `use crate::name::UserName;` moved from mid-file (line 468) to the top imports block (`lib/src/node.rs`) | `beauty.md` — orphan use statement |
| `lib/src/address.rs` import sort alphabetised | minor |
| New `skills.md` at repo root | `autonomous-agent.md` — substantive work in a repo lacking one triggers writing it |

### lojix-cli — `14c3681` and `cbfc9b6`

```
audit: extract inline tests, drop -Input + extension-trait pattern, kill dead method
bump horizon-lib pin: 48f083a → 11d3647 (Iface→Interface, EmptyYggSubnet)
```

| Change | Why |
|---|---|
| Inline `#[cfg(test)] mod tests` extracted from `src/deploy.rs` to `tests/substituter.rs` | `rust-discipline.md` "Tests live in separate files" |
| `HorizonProjection` + `HorizonProjectionInput` collapsed → `HorizonProjection::new(proposal, viewpoint)` | `rust-discipline.md` "One type per concept — no `-Details` / `-Info` companions" — the `-Input` companion held identical fields and `from_input` just unpacked them |
| `ArtifactMaterialization` + `ArtifactMaterializationInput` collapsed → `ArtifactMaterialization::new(...)` | same `-Input` anti-pattern |
| `ExtraSubstitutersFromHorizon` extension trait → inherent `impl ExtraSubstituters` block in `deploy.rs` | trait wrapper around a single method on an own-crate type is ZST-method-holder shape disguised; inherent impls cross modules within a crate |
| `BuildPlan::supports_remote_builder()` (always-`true`) deleted | `beauty.md` "Dead code retained 'for safety'" |
| `SystemProfileLink` reshaped: `String` → `{ text, generation }`, `generation()` no longer re-parses the string | `beauty.md` — the original double-parsed and the second `Result` path was unreachable |
| `\x20`-littered `HORIZON_FLAKE_TEMPLATE` / `SYSTEM_FLAKE_TEMPLATE_*` constants → multi-line literals + inline `format!` | `beauty.md` — line-continuation + space-escape ceremony |
| `ExtraSubstituters::is_empty / urls_text / public_keys_text` `pub(crate)` → `pub` | so the extracted external test file can call them |
| Cargo.lock `horizon-lib` rev pinned via `--precise` to my new horizon-rs commit | `nix-discipline.md` "Bumping a Rust git dep" — `--precise` was required because plain `cargo update -p horizon-lib` cascade-bumped `nota-codec` to a tip with a breaking API change (`Decoder::nota` → `Decoder::new`) |

All committed-state checks pass:
- `cd /git/github.com/LiGoldragon/horizon-rs && nix develop -c cargo test` — 3 tests green (no regression).
- `cd /git/github.com/LiGoldragon/lojix-cli && nix flake check -L` — `all checks passed!` (40 tests).

---

## Surfaced for human decision (NOT applied)

### Breaking the public Nota wire — needs coordinated upstream/downstream change

| Item | Where | Why surfaced |
|---|---|---|
| `Magnitude::Med` → `Medium` | `horizon-rs/lib/src/magnitude.rs` | `naming.md` — `Med` is not in the six exception classes. **But**: `Med` appears in `goldragon/datom.nota` (e.g. `(Entry bird Med)`); rename requires datom.nota edit + lockstep redeploy |
| `Magnitude::None` (the zero-point variant) | same | `beauty.md` "Name for what something is *not*". Could be `Absent` or `Zero`. Also `goldragon/datom.nota`-bound |
| `AtLeast` field names `at_least_min/med/large/max` | `horizon-rs/lib/src/magnitude.rs` | `naming.md` field-naming refinement (designer's recent addition) — `at_least.at_least_min` reads as repetition; could be `at_least.min/med/large/max`. **But**: serde `rename_all = "camelCase"` produces `atLeastMin/atLeastMed/...` in the JSON; downstream Nix modules in CriomOS / CriomOS-home consume those exact field names. Coordinated rename across all `nix.settings` consumers required |

These are not bugs; they're the workspace's naming rules colliding with already-deployed consumer contracts. Each rename is a coordinated upgrade across `goldragon` + `horizon-rs` + `lojix-cli`'s pin + `CriomOS` + `CriomOS-home` + a redeploy on every node.

### Architectural smells — needs scoping before action

| Item | Where | Why not auto-fixed |
|---|---|---|
| `NodeProposal::project()` is ~150 LOC | `horizon-rs/lib/src/node.rs` | The function reads as a serial pipeline of derived-field computations. Splitting into private helpers would help readability but each helper would name a slice of the projection logic — a real design call, not a mechanical refactor |
| `DeployState::run()` is ~130 LOC | `lojix-cli/src/deploy.rs` | Same shape — serial actor-RPC pipeline. Splitting needs intentional naming of the steps |
| `Node` has 60+ public fields | `horizon-rs/lib/src/node.rs` | The flat shape is what Nix consumes via `builtins.fromJSON`. Restructuring (e.g. nesting under `nix: NixIdentity { pub_key, line, cache_domain, url }`) cascades through CriomOS modules |
| `SshTarget` stores concatenated `user@domain` `String` | `lojix-cli/src/host.rs` | `with_user` parses the string back out — a special-case workaround per `beauty.md`. Cleaner: typed fields. Internal-only refactor; doable but not trivial |
| `SystemDir`/`HorizonDir`/`DeploymentDir` triplet | `lojix-cli/src/artifact.rs` | Three near-identical wrapper types. A generic `CacheDir<T>` or trait would unify them. Borderline — each writes a different payload |

### Test coverage — sparse

`horizon-rs/lib/tests/` contains one file (`magnitude.rs`).
The other 11 source files (`address`, `cluster`, `error`,
`horizon`, `io`, `machine`, `name`, `node`, `proposal`,
`pub_key`, `species`, `user`) have no tests. Per
`rust-discipline.md` "One test file per source file." This is
a real gap; backfilling is its own work, not part of this
audit.

### Pre-existing breakage discovered, not in scope

`horizon-rs/flake.nix` uses `numtide/blueprint` which
auto-imports `lib/default.nix`, but horizon-rs's `lib/` is the
Cargo workspace member (Rust crate). `nix flake check` errors
with *"Path 'lib/default.nix' does not exist"*. Filed as
`primary-4mn` (P2). Per `nix-discipline.md`,
`nix flake check` is the canonical pre-commit runner —
without it horizon-rs can't follow that discipline.
horizon-rs's tests still run via `nix develop -c cargo test`.

---

## What the audit did not check

- **Behavioural correctness** — whether the projection logic
  computes what it should. The audit only asked structural
  questions.
- **Full naming sweep beyond explicit type names** — the
  thousands of identifiers (locals, parameters, fields) were
  not exhaustively reviewed. The visible offenders
  (`Iface`, `Med`, `at_least_*`) were caught; subtler ones
  may remain.
- **The `horizon-cli` binary** beyond the `Cli` struct.
- **Documentation accuracy** — `ARCHITECTURE.md` and
  `docs/DESIGN.md` were not audited against current code.

---

## Files referenced

- `/git/github.com/LiGoldragon/horizon-rs/lib/src/address.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/error.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/proposal.rs`
- `/git/github.com/LiGoldragon/horizon-rs/skills.md` (new)
- `/git/github.com/LiGoldragon/lojix-cli/src/activate.rs`
- `/git/github.com/LiGoldragon/lojix-cli/src/artifact.rs`
- `/git/github.com/LiGoldragon/lojix-cli/src/build.rs`
- `/git/github.com/LiGoldragon/lojix-cli/src/deploy.rs`
- `/git/github.com/LiGoldragon/lojix-cli/src/project.rs`
- `/git/github.com/LiGoldragon/lojix-cli/tests/invocation.rs`
- `/git/github.com/LiGoldragon/lojix-cli/tests/substituter.rs` (new)
- `/git/github.com/LiGoldragon/lojix-cli/Cargo.lock`
- BEADS `primary-4mn` — horizon-rs flake-check breakage

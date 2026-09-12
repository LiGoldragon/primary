# Skill edits applied from `skill-proposals.md`

Flow f6db8d, apply subflow, thread `f6db8d14-1dfe-472d-914e-9c441f852834`,
2026-09-12. Delegated scope: §4-6 full replacement bodies, the §1/§3/addendum
lines for `lojix`, `orchestrate`, `nexus`, `testing`, `file-editing`, `subflow`
and `main-flow`, and §14's entry-file paragraph. §16's deletions and §18's
contradictions were skipped as instructed; §2, §7, §8, §9, §10, §11, §12, §13,
§14a, §14b and §17 were outside the delegated scope and are untouched.

Held under Orchestrate Lock 1231 `CurriculumSkillProposalsApply`, released
before this report was returned.

## Curriculum — commit `2ef2b538f7efa9b7da4b98b98b1e9cb73c6f2fdf`

Verified at the real remote: `git ls-remote git@github.com:LiGoldragon/Curriculum.git main`
returns `2ef2b538f7efa9b7da4b98b98b1e9cb73c6f2fdf`.

| skill | diff stat | proposal applied |
|---|---|---|
| `skills/ethos.md` | 187 +++/--- (whole file) | §4 |
| `skills/datom.md` | 134 +++/--- (whole file) | §5 |
| `skills/protos.md` | 120 +++/--- (whole file) | §6 |
| `skills/lojix.md` | 137 +++/--- | §3a, §3b, §3c, A1-A5 |
| `skills/main-flow.md` | 3 +/- | §1a, §1b |
| `skills/nexus.md` | 4 +/- | A7 |
| `skills/orchestrate.md` | 2 +/- | A6 |
| `skills/file-editing.md` | 2 + | A9 |
| `skills/subflow.md` | 1 + | A10 |
| `skills/testing.md` | 1 + | A8 |

Total across `skills/`: 10 files, 271 insertions, 320 deletions.

`roles.datom` was **not** edited: §15's conversion had already landed on
Curriculum `main` before this subflow opened the file. Witnessed —
`grep -o '“' roles.datom | wc -l` returns `0`, and every delimited string in
the file, `«claude-opus-4-6[1m]»` and the empty `«»` included, is already in
guillemets.

## primary — the regenerated trees and the entry file

`AGENTS.md` gained §14's paragraph, verbatim as proposed, after the first
`## Skills` paragraph. `CLAUDE.md` already carried the Claude-interface form of
the same rule and needed no change.

Regeneration ran and succeeded. 24 files, 667 insertions, 760 deletions:
`.agents/skills/` and `.claude/skills/` for the ten edited skills, plus three
files that the same pinned generator had been unable to emit while the check was
blocked — `.claude/skills/design/SKILL.md`, `.claude/skills/realization/SKILL.md`
and `.claude/skills/main-flow/SKILL.md` change `user-only: true` to
`disable-model-invocation: true`, and `skills/generated-role-outputs.datom`
loses its curly quotes. `.codex/` and `.pi/` are unchanged.

## What was witnessed, and against what

### Released substrate

All three producer checkouts are at their released heads and equal to their
GitHub `main` (`git ls-remote`): protos `171b21f` 0.30.1, datom-codec `627db67`
0.26.3, ethos-zero `de3d992` 8.0.1. **No sibling has released an arity change
beyond 0.26.3** — the change §5 reported as uncommitted has since landed as part
of 0.26.3 itself.

### `datom` (§5)

A scratch crate depending on datom-codec 0.26.3 and protos 0.30.1 composed and
round-tripped every text example in the replacement. All pass unchanged:

    { Ada 1990 { «12 Rue de la Paix» Paris 75002 } [ Author Reviewer.{ 2024 17 } ] }
    Accepted.{ 42 2026-09-03T17:46:20 }
    Refused.{ «no such file: { } is content» 2 }
    Pending          [ 0 42 -42 ]          Observed.Locks.[]
    [ Some.42 None ]   Ok.{ Ada 1990 }   Err.«no such lock»

Each composed into the expected Rust value and textualized back to the identical
string.

Four corrections to the proposed text, each because the released code differs:

1. `Compositional` no longer carries `const ARITY` or `from_positions`. Released
   `src/core.rs:129-131` is `pub trait Compositional: Sized { fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error>; }`.
   The trait block and the generated-impl example were rewritten to the released
   shape, read from the derive at `crates/datom-codec-derive/src/lib.rs:106-115`
   and `:189-196`: `budget.spend`, then `datom.positions(<arity>)`, then one
   `positions.position(budget)?` per field; `datomize` builds
   `Datom { path: at.clone(), form: Form::Struct(vec![…at.child(i)…]) }`.
2. `Path::root()` does not exist. `Path` is `Vec<Integer>`; the crate's own tests
   write `Path::new()`.
3. `actualize` takes the budget by mutable reference: `.actualize(&mut budget)?`.
4. The error example was wrong in both head and payload. Witnessed: composing
   `[ 1 x ]` as `Vec<i64>` yields
   `Error { layer: Composition, path: [1], kind: Value { expected: "Integer", value: "x" } }`,
   which datomizes and prints as `Error.{ Composition [ 1 ] Value.{ Integer x } }`.
   The proposal's `Corporate.{ [ 1 ] Value.x }` was replaced by that.

### `protos` (§6)

The `Protos`, `Enclosure`, `Boundary`, `Separator`, `Extent`, `Error` and
`ReaderBudget` declarations in the replacement match `protos/src/core.rs:4-70`
exactly, as do the three trait signatures. The guillemet escape was run:
`«she said \»no\» and left»` protosizes to an `Opaque` whose content is
`she said »no» and left` and textualizes back to the original, byte for byte.
Two corrections: `Path::root()` → `Path::new()` as above, and the illustrative
protosic/conceptual code block was rewritten to the real struct-variant syntax
with the extents and `vec![]` paths the run actually produced — as written it
was not constructible.

### `ethos` (§4)

Verified by a subflow that built ethos-zero 8.0.1 from `de3d992` and ran each
example. The CLI grammar is exactly as proposed —
`ethos-zero 'Generate.{ /abs/file.ethos /abs/out }'` replies
`Generated.[ /abs/out/file.rs ]`, guillemets around the paths optional; sweet
form and `;` comments are accepted; the canonical braced form is produced by
inserting `.{` after the bare head.

Example 2 (declarations) generates exactly the claimed Rust and was kept
verbatim. Two corrections:

1. Example 1's import `[ protos:String ]` makes the field `protos::String`, not
   `String`, because an import shadows the intrinsic — and `String` is an
   intrinsic by the skill's own list, so the import was wrong in the proposal's
   own terms. The imports section is now `[]`, which the generator was witnessed
   to turn into precisely the claimed `pub struct Record { pub string: String, pub integer: i64 }`.
   The canonical-form line changed with it.
2. Example 3 was **rejected outright** as proposed:
   `GenerationRejected.{ …/ex3.ethos [] Conceptual.{ [ 1 2 2 0 0 0 ] Undeclared.Clonable } }`.
   `Clonable` and `Sendable` are not intrinsic. With imports
   `[ serde:Serializable.Serialize  std:Clonable.Clone  std:Sendable.Send ]` the
   generator accepts it, and the Rust block was replaced with its verbatim
   output: `SinkError` is emitted above the traits, `create()` carries
   `where Self: Sized`, containers are fully qualified (`std::result::Result`,
   `std::option::Option`), the bounds are `std::clone::Clone`,
   `std::marker::Send` and `serde::Serialize`, and the association assert is
   named `assert_sinkerror_fillable` — the type name lowercased whole, not
   snake-cased per word.

The mechanism behind this is `ethos-zero/src/generation.rs:121-152`: a
`source:Ethos.Rust` import emits the literal `source::Rust`, with `std::Clone`
and `std::Send` the only special cases, and nothing checks that the path exists.
One sentence was added to `## Imports and intrinsics` stating that rule, because
without it the corrected example's `serde:Serializable.Serialize` form is
unexplained.

The two things §4 flags as Vision rather than witnessed behaviour (a Signal type
named `Query`, a Sema record type named `Record`) were not re-tested here.

### `lojix` (§3, A1-A5)

Witnessed read-only against the installed `lojix`, run from `/tmp`, nothing
written. Every `Query` arm of the contract's five-arm `Selection`, in the datom
form the replacement teaches, is accepted:

    lojix 'Query.ByNode.{ alpha node-1 None }'            -> Queried.{ [] [] { 1 1 } }
    lojix 'Query.ByNode.{ alpha node-1 Some.CompleteHost }' -> Queried.{ [] [] { 1 1 } }
    lojix 'Query.ByGeneration.{ 1 }'                      -> Queried.{ [] [] { 1 1 } }
    lojix 'Query.ByDeployment.{ 1 }'                      -> Queried.{ [] [] { 1 1 } }
    lojix 'Query.ByEventLog.{ 0 1 }'                      -> DeploymentEventsQueried.{ [] [] { 1 1 } }
    lojix 'Query.ByTestRun.{ alpha node-1 None }'         -> TestRunsQueried.{ [] { 1 1 } }

and the parenthesised form the old skill taught is refused:

    lojix 'Query.ByNode.(alpha node-1 None)'
    (CliRejected [Datom request did not decode: … Shape(Struct, Meaning)])

`lojix-inspect-store 'InspectStore.{ <path> }'` was accepted against a scratch
copy of a store (the copy failed to open, but the request form was taken; the
parenthesised form was refused before that). `/var/lib/lojix` was never read or
written, and `lojix-reset-store` was never run.

The `WatchDeployments`, `WatchCacheRetention`, `Pin` and `ResetStore` forms in
the file are **not witnessed**: each is state-changing or opens a subscription,
and the brief forbade running them. They are converted by the same rule as the
witnessed ones.

A2-A5 were confirmed at source rather than at the wire:
`meta-signal-lojix/ethos/signal.ethos:29-30` gives both deployment shapes 14
fields with `SecretsInput` fifth; `CheckHostKeyMaterial` survives only in the
two `UPGRADES.md` changelogs; `lojix/src/lib.rs:105` sets
`LOJIX_SCHEMA_VERSION` to 5 and `src/reconstruction.rs:30-31` recognises
`[2, 3, 4, 5]`; `src/bootstrap.rs:1845` and `clients/meta/src/lib.rs:153` require
the artifact name `horizon-definition.datom`, and `proposal.datom` appears only
in `lojix/UPGRADES.md` as the removed prior form.

A4 additionally removed `KeyMaterialChecked` and `KeyMaterialCheckRejected` from
the ordinary reply-family list. A4 proposes deleting only the request line and
the field block, but its ground quotes the removal of "the whole
`CheckHostKeyMaterial` vocabulary"; leaving the two reply families would have
left the skill self-contradicting.

§3c's binary rename was resolved against the source workspace, which was the
witness §3c said it lacked: `/git/github.com/LiGoldragon/lojix` (4.0.1) declares
`[[bin]] lojix-nexus`, `[[bin]] lojix-meta`, `[[bin]] lojix` and the tools. §3c
declined to rename `LOJIX_OWNER_SOCKET` or the words "owner socket" and "owner
contract"; that decision was honoured and those are unchanged.

### `orchestrate` (A6)

`orchestrate 'Observe.Locks'` returns one `Observed.Locks.[ … ]` frame and exits
at once, elapsed 0.00 s, with no held connection — exactly the limit A6's text
states. Applied verbatim.

## §7: `orchestrate` — curly quotes to guillemets

Flow f6db8d, §7-apply subflow, 2026-09-12, after living approval ("go with your
suggestions"). Held under Orchestrate Lock 1253 `OrchestrateSection7`.

### Curriculum commit `987a1e37d1c7f747b48a47a1806bd4a817cc4b84`

Verified at the real remote: `git ls-remote git@github.com:LiGoldragon/Curriculum.git main`
returns `987a1e37d1c7f747b48a47a1806bd4a817cc4b84`.

| skill | diff stat | proposal applied |
|---|---|---|
| `skills/orchestrate.md` | 2 +/- | §7 |

The change replaces ASCII curly quotes with guillemets in the reason string
rule, removes the guard clause about ASCII double quotes (per skill-designing
principles), and updates the copyable example accordingly:
- Old: `"like this"; ASCII double quotes are not Datom string delimiters`
- New: `guillemets` with example using `«Clarify Lock fields»`

### primary regeneration — commit `2ec61bc6b2fc607af31dd03ef6cc8b2cbb3767bd`

Verified at the real remote: `git ls-remote git@github.com:LiGoldragon/primary.git main`
returns `2ec61bc6b2fc607af31dd03ef6cc8b2cbb3767bd`.

| path | diff stat |
|---|---|
| `.agents/skills/orchestrate/SKILL.md` | 2 +/- |
| `.claude/skills/orchestrate/SKILL.md` | 2 +/- |

Total: 2 files, 4 insertions, 2 deletions.

## Blockers and contradictions this work surfaced

**1. The installed Lojix and Orchestrate binaries take curly quotes, not
guillemets.** Witnessed:

    lojix 'Query.ByNode.{ “alpha beta” node-1 None }'   -> Queried.{ [] [] { 1 1 } }
    lojix 'Query.ByNode.{ «alpha beta» node-1 None }'   -> (CliRejected … Arity(3, 4))
    orchestrate 'Lock.{ … “two words” }'                -> Locked.{ … }
    orchestrate 'Lock.{ … «two words» }'                -> Corporate(… Arity(4, 5))

The installed package is lojix-0.21.1 and the installed `orchestrate` is of the
same generation; both predate the protos release in which the curly quotes
stopped being delimiters. §3a's proposed string rule — guillemets — was applied
as written, because it is what `Vision/protos.md`, the released protos 0.30.1
and the `datom` and `protos` skills all say, and because the same paragraph's
brace-vs-parenthesis rule was witnessed correct against the installed binary.
The consequence is that **the `lojix` skill's string rule, and the `datom`
skill's `orchestrate 'Lock.{ … «why I hold it» }'` example, do not work against
the binaries installed on this machine today.** The `orchestrate` skill has been
updated (§7 applied in a follow-on subflow), so that contradiction is now
resolved; both `lojix` and `datom` teach guillemets consistently. The mismatch
with the installed 0.21.1 binaries remains until that repin lands.

**2. The installed Lojix executables are named as the old skill named them.**
Witnessed on PATH: `lojix`, `lojix-bootstrap`, `lojix-daemon`,
`lojix-inspect-store`, `lojix-reset-store`, `lojix-write-configuration`,
`meta-lojix`, all from `lojix-0.21.1`; the running unit is
`lojix-daemon.service`. `lojix-nexus` and `lojix-meta` do not exist on this
machine. The skill now names `lojix-nexus` and `lojix-meta` — the source
workspace's and the CriomOS-pinned revision's names — so it describes the build
that is about to be deployed, not the one that is running. Orchestrate lock 1227
`F6db8dCriomosLojixLanding` is that repin. Related, and not this subflow's to
fix: `CriomOS/modules/nixos/lojix.nix:27` still launches `lojix-daemon` and will
break on the repin.

**3. The installed lojix-0.21.1 still answers `CheckHostKeyMaterial`**
(`lojix 'CheckHostKeyMaterial.{ alpha node-1 /tmp/x }'` returns
`KeyMaterialChecked.{ node-1 [] { 1 1 } }`). The verb is gone from the contract
and from the source, so the skill no longer teaches it; it works today and stops
working at the repin.

**4. The regeneration blocker named in `reports/skill-regeneration.md` is
gone, but not for the reason that report predicted.** Orchestrate lock 851
`CurriculumDeployDatomMigration`, flow 542442, is **still held**, and
curriculum-deploy `main` is still exactly the pinned
`c669b27b464f652edd1c1f812e6b7fd20b941ab7` — `git ls-remote` confirms both. No
migration landed. What changed is the other half: `roles.datom` is already in
guillemets on Curriculum `main`, so the pinned generator parses it. §15's fix was
therefore not needed and was not made.

## Addendum 2 — B2, B3, B4/B5, B6 applied to `lojix`

Flow f6db8d, apply subflow, thread `f6db8d14-1dfe-472d-914e-9c441f852834`,
2026-09-12. Delegated scope: `skill-proposals.md` Addendum 2, proposals B2
(Rust library surface trait list), B3 (Readiness section), B4/B5 (BuildOnly's
`BootstrapInput` split and the bootstrap parent-directory `0700` requirement),
and B6 (`DeployRefused`/`ClosureCopyFailed` wire vocabulary). B1 and B7 are
closures of already-applied proposals and carried no new text.

Held under Orchestrate Lock 1361 `LojixSkillAddendum2`, released before this
report was returned.

Before applying, B2 and B6 were witnessed against `lojix` 6.0.0 at
`c4bba4fa12408c39ff745b0773468cd32a74403f` — confirmed the released `main`
head with `git ls-remote git@github.com:LiGoldragon/lojix.git main`, then read
(not built) `src/lib.rs`, `src/daemon.rs`, `src/runtime_model.rs`,
`src/schema_runtime.rs`, and `src/adapters.rs` at that revision via `git show`.
Every trait named in B2's proposed list (`LojixRecord`, `DurableStore`,
`NexusPersistable`, `TransitionJournal`, `DeploymentLedger`,
`GenerationLedger`, `TestRunLedger`, `RuntimeCore`, `DeployDriving`,
`TestDriving`, `NexusReadiness`) is declared `pub trait` at that revision,
under those exact names. B6's vocabulary — `DeployRefused` carrying
`RefusedDeploy { deploy_refusal_reason: DeployRefusalReason, state_marker:
StateMarker }`, `DeployRefusalReason` with variants
`ContinuationBudgetExhausted`, `NoCorrelatedDeployment`, `DurableWriteFailed`,
and `nexus::EffectStage::CopyClosure` mapping through
`sema::DeploymentFailureStage::CopyClosure` and
`meta::DeployRejectionReason::ClosureCopyFailed` to
`sema::DeploymentTerminalReason::ClosureCopyFailed` — matches the proposal
text exactly. No correction to either proposal's wording was needed.

### Curriculum — commit `8484ecd89c3f56010f5b5843a140d1b3ff815952`

Verified at the real remote: `git ls-remote git@github.com:LiGoldragon/Curriculum.git main`
returns `8484ecd89c3f56010f5b5843a140d1b3ff815952`.

| skill | diff stat | proposal applied |
|---|---|---|
| `skills/lojix.md` | 46 +/4 - | B2, B3, B4, B5, B6 |

### primary — regenerated trees, commit `761474cf27a683d7939e597c8aad7aab817dc884`

Verified at the real remote: `git ls-remote git@github.com:LiGoldragon/primary.git main`
returns `761474cf27a683d7939e597c8aad7aab817dc884`.

Ran `nix run /home/li/primary#check-skills -- 'Check.{ «/git/github.com/LiGoldragon/Curriculum» «/home/li/primary» }'` first (reported the expected difference in `.agents/skills/lojix/SKILL.md`), then `nix run /home/li/primary#generate-skills -- 'Generate.{ «/git/github.com/LiGoldragon/Curriculum» «/home/li/primary» }'` (`Generated.{ 44 21 }`), then re-ran `check-skills` to confirm `Checked.{ 44 21 }` with no further difference.

| path | diff stat |
|---|---|
| `.agents/skills/lojix/SKILL.md` | 46 +/4 - |
| `.claude/skills/lojix/SKILL.md` | 46 +/4 - |

Total: 2 files, 92 insertions, 8 deletions.

## Sources

- `/home/li/primary/flows/f6db8d/reports/skill-proposals.md` (the approved proposals)
- `/home/li/primary/flows/f6db8d/reports/skill-regeneration.md` (the prior blocker account)
- `/git/github.com/LiGoldragon/Curriculum` — `skills/*.md`, `roles.datom`, `AGENTS.md`; commit `2ef2b538`, verified at `git@github.com:LiGoldragon/Curriculum.git`
- `/git/github.com/LiGoldragon/protos` at `171b21f` (0.30.1) — `src/lib.rs`, `src/core.rs`, `src/rendering.rs`
- `/git/github.com/LiGoldragon/datom-codec` at `627db67` (0.26.3) — `src/lib.rs`, `src/core.rs`, `crates/datom-codec-derive/src/lib.rs`, `tests/composition.rs`
- `/git/github.com/LiGoldragon/ethos-zero` at `de3d992` (8.0.1) — `src/conception.rs`, `src/checking.rs`, `src/generation.rs`, `src/lib.rs`, and the built `ethos-zero` binary
- `/git/github.com/LiGoldragon/lojix` at `0bb3d66` (4.0.1) — `Cargo.toml` files, `src/lib.rs`, `src/reconstruction.rs`, `src/bootstrap.rs`, `clients/*/src/lib.rs`, `flake.nix`, `UPGRADES.md`
- `/git/github.com/LiGoldragon/meta-signal-lojix/ethos/signal.ethos`
- `/git/github.com/LiGoldragon/signal-lojix/UPGRADES.md`
- The installed `lojix`, `lojix-inspect-store`, `meta-lojix` and `orchestrate` clients, run read-only from `/tmp`
- A scratch Rust crate against protos 0.30.1 and datom-codec 0.26.3, run by this subflow
- `orchestrate 'Observe.Locks'` and `git ls-remote https://github.com/LiGoldragon/curriculum-deploy main` (run by this subflow)
- `nix run .#check-skills` and `nix run .#generate-skills` in `/home/li/primary` (run by this subflow)
- `flows/f6db8d/reports/skill-proposals.md` Addendum 2 (this addendum's own ground)
- `/git/github.com/LiGoldragon/lojix` at `c4bba4fa12408c39ff745b0773468cd32a74403f` (6.0.0, released `main`) — `src/lib.rs`, `src/daemon.rs`, `src/runtime_model.rs`, `src/schema_runtime.rs`, `src/adapters.rs`, read via `git show` after `git ls-remote` and `git fetch`, not built (run by this subflow)

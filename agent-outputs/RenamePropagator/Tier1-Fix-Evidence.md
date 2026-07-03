# Tier-1 Fix Evidence — arc's own defects (beads primary-a2ik + primary-glph)

Session: RenamePropagator. Role: general code implementer (Claude Opus 4.8, 1M).
Date: 2026-07-04. Closes the two Tier-1 defects the checkpoint audit
(`A-Checkpoint-Audit.md` Finding 1) caught: the rename-propagator silent-skip
tool defect (a2ik) and the two half-migrated ledger repos (glph). Done as one
unit — the hardened tool is the path that stages the two repos.

## Authoritative inputs

- `A-Checkpoint-Audit.md` Finding 1 (overrides any earlier "all clean" claim).
- `B-Harness-Evidence.md` / `B-Harness-Audit.md` (synchronizer `staged-cascade`,
  cross-branch drop-next resolution).
- Producer tips (verified live this session): `nota@main bea7e284` (no drop-next),
  `schema@drop-next a393c8c8`, `schema-rust@drop-next 7f746c02`.

## BEAD primary-a2ik — rename-propagator hardened against silent skip (DONE)

**Landed to rename-propagator `main`:** `5c2e0ab4d6028a78193c6c8557202588ed7a8de0`
(parent `d4ef1e69`), pushed to `origin` (canonical `github.com/LiGoldragon/rename-propagator`).
Normal tool dev on the tool's own main — no migration main touched. Edits-only
contract honored: no commit/push logic added; the new inspection reads git refs
from the filesystem only (no `Command::new`).

### What changed

- New `crates/rename-propagator/src/checkout.rs`: `GitCheckout` reads a
  checkout's own git refs (`refs/heads/<mainline>` vs the forge remote's
  `refs/remotes/<remote>/<mainline>`, loose then `packed-refs`) and returns a
  typed `MainlineAlignment` (`Aligned` / `Diverged{local,forge}` /
  `Unverified{detail}`). The forge remote is discovered by URL match
  (`Forge::matches_remote_url`, handles scp + https + ssh forms), so zero repo
  or branch literal is baked in.
- `plan.rs`: every `RepositoryPlan` now carries a typed `StagingDisposition`
  (`Staged` | `NoStage(Diverged|Unverified)`), NOTA-encoded and round-tripped.
  `RenamePlan::no_stage_repositories()` enumerates the declined set.
- `driver.rs` `apply()`: writes only `Staged` repositories; a divergent checkout
  is held out of the write and recorded as an explicit `NoStage` — never a
  silent no-op. `main.rs` and the `summarize` example surface the no-stage set.
- ARCHITECTURE.md §7a + §10: the "no silent skip of a divergent checkout"
  invariant.

### Guard test — passes

`crates/rename-propagator/tests/staging_disposition.rs` builds real `.git` ref
trees on disk (no command run) and drives the production `GitCheckout` reader
through `RenameRun::plan`:

- `divergent_checkout_is_an_explicit_no_stage_never_a_silent_skip`: a divergent
  checkout yields `NoStage(Diverged(local, forge))` naming both tips; an
  unverifiable checkout yields `NoStage(Unverified)`; a clean one `Staged`; the
  no-stage set is exactly the two the tool could not process (never absent).
- `apply_stages_the_clean_base_and_holds_the_divergent_checkout`: apply rewrites
  the clean consumer on disk and leaves the divergent consumer's live `-next`
  dep untouched.

Full suite: `cargo test` green (checkout/plan/driver + all pre-existing
witnesses); `cargo fmt --check` clean; `cargo clippy --all-targets` clean.

### Demonstration on the two real divergent repos (acceptance #1)

`rename-propagator <config>` over the producers + the two ledger repos at their
live local clones now emits an explicit NO-STAGE per divergent repo — in the
NOTA plan (`(NoStage (Diverged (<local> <forge>)))`), on stderr, and in the
`summarize` view:

```
NO-STAGE repository-ledger:        local ca23437e  vs forge 48109483
NO-STAGE signal-repository-ledger: local f3a5150e  vs forge 14f08be8
```

(tips match the audit's github mains exactly). Previously these two were
silently absent from the staged set; now they are surfaced.

## BEAD primary-glph — two ledger repos re-staged off live -next (verifying)

Used the hardened tool as the path (a2ik's acceptance test): fresh isolated
clones of each repo at their **github drop-next base** (which already carries the
synchronizer cascade), `main` aligned with the forge → the tool **Stages** them
(the complement of the NO-STAGE it emits on the divergent local clones), and
applies the identity rewrite. The local `main*` divergences in the original
clones were never touched (I worked in scratch clones).

### Edits

- **signal-repository-ledger** `drop-next`: `nota-next` → `nota` (Cargo.toml
  line 24 + `use nota_next::` → `use nota::` in src/lib.rs, tests/channel.rs);
  Cargo.lock regenerated → `nota.git@main#bea7e284` + `nota-derive`, 0 family
  `-next`. New drop-next tip **`2bc09662a0c62d98f92e5a8898e058c805c64834`**
  (fast-forward from `87495b78`), pushed to github.
- **repository-ledger** `drop-next`: `nota-next` → `nota` (Cargo.toml:34, kept
  `branch=main`) and `schema-rust-next` → `schema-rust` (Cargo.toml:44, cascaded
  to `branch=drop-next` to match migrated siblings) + `use *_next::` → `use *::`
  across build.rs/src/tests; Cargo.lock regenerated → `nota.git@main#bea7e284`,
  `schema.git@drop-next#a393c8c8`, `schema-rust.git@drop-next#7f746c02`,
  `signal-repository-ledger@drop-next#2bc09662`, 0 family `-next`. New drop-next
  tip **`5127fd9b7dddfdbacbbc15d547b10afded6a26fe`** (fast-forward from
  `2e4ef76b`), pushed to github.

### Residue sweep (drop-next trees)

Live family `-next` Cargo deps (`nota-next` / `schema-rust-next` / `schema-next`
/ `*-next.git`) in Cargo.toml + Cargo.lock: **0** in both repos. Live
`use *_next` paths: **0** in both. The only remaining `-next` substrings are
`@generated by schema-rust-next` header/doc comments (string data the rename
preserves; the emitter emits the same string, so freshness holds) and
`branch = "drop-next"`.

### Composed verification (acceptance #3)

signal-repository-ledger was the false-green the audit caught (green standalone,
E0433 composed). The authoritative composed test is building **migrated
consumer repository-ledger@drop-next**, which pins
`signal-repository-ledger@drop-next` with `features=["nota-text"]` — the exact
composition that failed E0433 before.

Command (prometheus builder):

```
nix build github:LiGoldragon/repository-ledger/5127fd9b#packages.x86_64-linux.default
```

<!-- RESULT PENDING — filled on build completion -->

## Boundaries honored

- No migration `main` moved. Producer mains (`nota bea7e284`, `schema 9af2c546`,
  `schema-rust 6218fb64`) unchanged; the two ledgers' github mains
  (`repository-ledger 48109483`, `signal-repository-ledger 14f08be8`) untouched.
  All edits are on `drop-next` (fast-forward advances only).
- The two repos' local `main*` divergences left exactly as they were — I never
  touched the original local clones; all staging was done in scratch clones.
- Zero project data in rename-propagator source (forge/branch discovered).
- Claimed rename-propagator + both ledger repos via Orchestrate; released at end.

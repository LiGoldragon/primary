# Flow's gate deflaked, and the Claude retract given a fixture

Subflow of 93ba9f, 2026-09-26. Flow branch `s1-e167d8`, from `ac216c89`
(Flow 0.17.1) to `e7efa657` (Flow 0.17.2). Own jj workspace of
`github.com/LiGoldragon/flow`; nothing deployed, no CriomOS-home touched.

Three things were asked: make the flaky caller-pane test deterministic by
its cause, give `Retraction::Key("ctrl+c")` a fixture test, and make a
retract leave a durable trace if it fits the store cleanly. The first two
landed. The third did not fit and is reported instead.

## 1. The flake, and its cause

`tests::a_process_in_a_pane_is_found_by_its_own_marks_or_its_ancestors`
spawned its marked sleeper as `sh -c "exec sleep 30"`. `MarkedProcess::spawn`
then waited, through `SettlesItsMarks`, for that shell's `HERDR_SESSION` and
`HERDR_PANE_ID` to be readable from `/proc/<pid>/environ` — a wait the file
already documents, against the window in which a freshly `execve`d process
has its new `mm` installed but `env_start`/`env_end` not yet written, so
`environ` reads back empty.

The wait was placed on the wrong exec. `exec sleep 30` makes the settled
shell `execve` a second time, after the wait has returned, and that second
exec reopens exactly the window the wait was there to ride out. When the
assertion at the next line fell inside it, `marked_pane()` saw no marks and
`caller_pane()` walked the ancestry instead. In a Nix builder no ancestor
carries Herdr marks, so it walked to init and returned `None` — the symptom
the failing build recorded.

`caller_pane()` is not at fault and is unchanged. A reader genuinely cannot
tell an empty `environ` from a scrubbed one; that is the premise the
production code is built on, and the fixture is what broke it.

The fix: `MarkedProcess::spawn` now takes a program and its arguments and
spawns it directly, so the process whose marks were settled never execs
again. The first sleeper is `sleep 30` itself. The second case still needs a
shell — it is the shell that must survive as the marked parent of an
unmarked sleeper — and that shell's command ends in another word (`; true`),
so it does not turn its last command into an exec of its own accord.

**Reproduced and falsified.** Run against the pre-fix binary with the
ancestry scrubbed, so the walk ends where a builder's would: 2 failures in
100. The two failures name line 3431 and show `marked_pane()` having fallen
through. Against the same binary without scrubbing, 300 runs, 0 failures —
which is why the flake was invisible from an interactive pane and showed
only on the builder. After the fix, 400 runs scrubbed: 0 failures.

## 2. The Claude retract, under fixture

`crates/flow-nexus/src/tests/submission.rs` drove only Codex: its `›` glyph,
its single `esc`, and `Retraction::LineByLine`. `Retraction::Key("ctrl+c")`
had the live witness in `flow-0171-proof.md` and nothing else.

The fixture composer now takes a `FixtureComposer` saying which harness it
is playing — the glyph and spacing its `agent read` prints, the key it
empties on, its `HarnessKind`, the name Herdr's snapshot gives it, and a
session identity of the shape the flow claim admits. Claude's line is `❯`
followed by U+00A0, as the live composer rendered it.

Two tests:

- `a_letter_claudes_interrupt_put_back_is_taken_out_by_one_ctrl_c` — a
  HardAbrupt to a working Claude seat. Keys pressed, in order:
  `esc esc`, `ctrl+c`, `enter`. The restored `Soft.{ m-… }` is recognised
  through the non-breaking space (Rust's `trim` removes it, U+00A0 being
  `White_Space`), emptied by the single press, and the HardAbrupt is then
  typed and submitted. Answer: `Delivered`, `InterruptWitness::Observed`,
  `DeliveryGrade::Transported`.
- `a_draft_claudes_interrupt_put_back_is_never_taken_out` — the same, with a
  person's half-thought in the composer. Only `esc esc` is pressed, the
  draft is untouched, nothing is typed, and the delivery is refused
  `ComposerOccupied`. This is the case that matters for Claude in
  particular: a second `ctrl+c` into an empty composer quits Claude, so the
  key must go in only onto text Flow recognises as its own.

**Seen failing first, three ways.** Both tests failed on their first run
(registration refused: the Herdr snapshot agent and the flow-claim marker
still said `codex`). The positive one then failed again on its key list
before `enter` was known to belong there. Finally, with
`HarnessKind::Claude`'s `Retraction` changed to `LineByLine` and nothing
else touched, it fails `DeliveryRejected(ComposerOccupied)` against
`Delivered` — so it discriminates on `Retraction::Key("ctrl+c")` itself,
not merely on the path running.

Both are named Nix checks, and so is the deflaked caller-pane test:
`flow-claude-retract-is-one-ctrl-c`,
`flow-claude-draft-is-never-retracted`,
`flow-caller-pane-from-marks-or-ancestry`.

## 3. A durable trace of a retract — not built, and why

Not built. It does not fit the store as it stands, and the shape that would
fit is a wire change in another repository.

Where a retract could be recorded:

- **`LeaseStep`** (`store/delivery.rs`) is the obvious place and the wrong
  one. A `Retracted` step would be written into the live `PaneLease` row,
  and that row is retracted the moment the delivery settles — by
  `settle_delivery`, which folds it into the atomic commit, or by
  `release_lease`. The lease exists only while a delivery is typing; it is
  crash-recovery state, not history. Nothing of it survives a normal
  delivery, so it cannot answer "did the retract path fire" after the fact.
  Making it survive would mean the row no longer means "a delivery was
  interrupted mid-type", which is the one thing `settle_interrupted_deliveries`
  reads it for.
- **A new `flow_nexus_retractions` table** keyed by `DeliveryId` would be
  durable and additive, and old stores would read unchanged. But nothing
  could see it: there is no wire request that returns it, and adding one
  means the same wire change as the option below while also putting a second
  record of one delivery beside the first. A durable row no peer can observe
  is half a feature, and subscription is how this Nexus is meant to be read.
- **A witness field on the settled `Delivery`** is the shape that actually
  fits. `InterruptWitness` is already exactly this: a field on `Delivery`
  saying whether the interrupt path was seen to work. A `RetractionWitness`
  beside it — `NotRequested` / `Retracted` / `Refused` — would be durable
  (it rides `StoredDelivery`, which is what a repeated `DeliveryId`
  answers with), observable, and named in domain language.

The cost is why it is not in this branch. `Delivery` is defined in
`meta-signal-flow`, a separate repository pinned by revision, whose semver
is the wire's semver: adding a field is a wire release, a new pin here, and
a matching change in every consumer, Message included. It also changes
`StoredDelivery`'s rkyv layout, so the `flow_nexus_deliveries` table needs
the same kind of versioned migration the store already carries for its v5
rows. That is a Flow 0.18 with a wire bump, coordinated with Message — not a
gate-only patch, and not something to slip in beside a test fix.

Until then the answer to "which path did that delivery take" stays what it
is today: the Herdr operations log of the run, which records every
`pane send-keys`, and nothing in Flow's own store.

## Version, gate, and what landed

Flow **0.17.2**. Gate only: no public behavior, wire, storage, package or
deployment change. `Cargo.toml`, `Cargo.lock`, `flake.nix` and `UPGRADES.md`
carry it.

Three commits on `s1-e167d8`, each landing only its own files:

| Commit | Files |
|---|---|
| `b08f41fd` | `crates/flow-nexus/src/lib.rs` |
| `a89ef3b7` | `crates/flow-nexus/src/tests/submission.rs` |
| `e7efa657` | `Cargo.toml`, `Cargo.lock`, `flake.nix`, `UPGRADES.md` |

`e7efa657` is present on `git@github.com:LiGoldragon/flow.git`
`refs/heads/s1-e167d8`, confirmed against the real remote.

**Gate runs, all `all checks passed!`:**

- One full `nix flake check` on the finished tree, everything built fresh
  at 0.17.2 on `prometheus.goldragon.criome`.
- Three further full `nix flake check` runs in which every `exactTest`
  check — all twenty-six, including the deflaked caller-pane one — was
  forced to rebuild and rerun rather than resolve from the builder's store.
- Three further runs of the whole-workspace `default` check (`cargo test
  --workspace`, 175 tests), likewise forced to rebuild each time. This is
  the check that failed in the build that started this work.
- Two cache-resolved `nix flake check` runs confirming the tree as pushed.

The forcing was done with a throwaway environment variable in the check's
own derivation, removed before the commit; `flake.nix` as landed carries no
trace of it, and the final run above was made on the landed tree.

Outside Nix, `cargo test --workspace` locally: 175 tests, 0 failures.

## What remains

- **The retract witness** of section 3, if Flow's psyche wants it: a wire
  release of `meta-signal-flow`, a `deliveries` table migration, and
  coordination with Message. It is the only way a run will be able to say
  which path a delivery took.
- **The other flaky-looking surfaces were not audited.** Only the one named
  test was fixed. Nothing else in `crates/flow-nexus` reads `/proc` in a
  test, but the fixture Herdr's 350 ms composer reads and `agent wait`
  timeouts are clock-bounded and were not measured under builder load.
- **Nothing deployed.** `s1-e167d8` is pushed and unmerged; 0.17.2 is not on
  any seat, and the branch still awaits whatever merge e167d8 intends.
- Scenarios 5, 6, 8–12 of the sandbox suite remain un-rerun against
  `ac216c89`, as `flow-0171-proof.md` says; 0.17.2 changes no behavior, so
  that gap is unchanged.

## Sources

- flow `s1-e167d8`: `ac216c89` before, `b08f41fd`, `a89ef3b7`, `e7efa657`
  after. Confirmed on the real remote with `git ls-remote`.
- `crates/flow-nexus/src/lib.rs` — `SettlesItsMarks`, `MarkedProcess`, and
  the test at `tests::a_process_in_a_pane_is_found_by_its_own_marks_or_its_ancestors`.
- `crates/flow-nexus/src/caller.rs` — `ReadsProcess::marked_pane`,
  `LocatesCallerPane::caller_pane`, unchanged.
- `crates/flow-nexus/src/tests/submission.rs` — the two new Claude tests and
  the `FixtureComposer` the fixture composer now takes.
- `crates/flow-nexus/src/herdr/pane.rs` — `Composer`, `Retraction`,
  `StyledLine::text_after`.
- `crates/flow-nexus/src/store/delivery.rs` — `PaneLease`, `LeaseStep`,
  `StoredDelivery`, `settle_delivery`, `release_lease`: the store design
  section 3 weighs.
- `crates/flow-nexus/src/delivery.rs` — `retracted_restored_letter`, the
  path the new tests drive.
- `flows/93ba9f/reports/flow-0171-proof.md` — the live witness of the Claude
  mechanism the fixture reproduces, and the two open items this report
  closes.
- Flake check output from `prometheus.goldragon.criome`, runs described
  above.

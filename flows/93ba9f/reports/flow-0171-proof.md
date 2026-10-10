# Flow 0.17.1 proven in the flow-message sandbox

Subflow of 93ba9f, 2026-09-26. Flow 0.17.1 `ac216c89` on the flow branch
`s1-e167d8`, against Message 0.17.0 `481b579f`, in the semi-sandbox at
`tools/flow-message-sandbox/`. Seats: Claude Haiku 4.5 and Codex Luna
(`gpt-5.6-luna`, low effort), in throwaway Herdr sessions the runs own and
tear down. No production seat was delivered to, interrupted or closed.

## What was wrong

Two separate things, and only the first was a defect in Flow.

**1. The cause e167d8 recorded for run 2 was wrong.** `sandbox-suite-run-2.md`
said Flow "grades Presented without witnessing the submit" and leased the pane
"to a composer that never became a turn". The letter was in fact submitted and
became a turn. What put it back into the composer was the HardAbrupt's own
`esc esc`: pressed before the turn's first response, Claude Code cancels the
turn and restores its prompt into the composer. Flow then read the pane again,
found the composer occupied, refused the HardAbrupt `ComposerOccupied`, and
left the letter sitting there, where it refused every later letter to that
pane. That report is corrected in place.

**2. Nothing had ever run `ac216c89`.** The sandbox's revisions were two
constants in `environment.py`, and e167d8's override of them did not land. The
run whose scenario 4 failure was reported as "0.17.1 still fails",
`fms-3a987a` (12:03), records `flow_revision`
`908135684f27…` — Flow **0.17.0**, the unfixed build. The only run that ever
built a 0.17.1 was `fms-d70a61` (11:21), and it built `93109005`, the first of
the two 0.17.1 commits, which adds the submission witness but not the retract.
`ac216c89`, the commit that takes a restored letter back, was never exercised.
So there was no evidence that the fix fails against real Claude — there was no
evidence about the fix at all.

## What changed

Nothing in Flow. `ac216c89` is proven as it stands.

In primary, two commits: `a11f7388` (the sandbox) and the one carrying this
report.

- `tools/flow-message-sandbox/environment.py` — a run builds each component
  from a whole flake reference, which `FMS_FLOW_FLAKE` / `FMS_MESSAGE_FLAKE`
  replace, and `Pins` carries the reference it actually built rather than the
  constant, so `results.md` names the revision under test and cannot name
  another.
- `tools/flow-message-sandbox/flow-message-sandbox` — `up` and `run` print
  both references and their store paths before the first scenario.
- `tools/flow-message-sandbox/sandbox.py` — `resume` restores those references.
- `tools/flow-message-sandbox/README.md` — how to name a branch under test.
- `flows/e167d8/reports/sandbox-suite-run-2.md` — the corrected cause.

## Results

Run `fms-b9d80b`, one stand-up, scenarios in one pass. Its `results.md` names
`github:LiGoldragon/flow/ac216c89…`, so the run says for itself what it built.

| # | Scenario | Verdict | Grade |
|---|---|---|---|
| 1 | Soft to idle Haiku: Presented, reply | pass | live acceptance, real Claude seat |
| 2 | Soft to working Luna: Parked, lands on rest | pass | live acceptance, real Codex seat |
| 3 | MiddleAbrupt to working Codex and Claude | pass | live acceptance, both seats |
| 4 | HardAbrupt interrupt, Codex and Claude | pass | live acceptance, both seats |
| 7 | Acknowledge by MessageId: Read | pass | live acceptance, real Claude seat |
| 13 | 64 KiB body and psyche letter intact | pass | live acceptance, real Claude seat |

Scenario 4 is the one that was intermittent, so it was repeated four more
times against a standing run `fms-c42635`: pass, pass, pass, pass. Five of
five against `ac216c89`. Its Haiku half failed in `fms-9a3e2b` and
`fms-3a987a` under 0.17.0, and in `fms-d70a61` under `93109005`.

Both runs tore down clean on all nine teardown checks, including that every
Herdr session present before the run was still present.

## The mechanism, witnessed directly

An end-to-end pass does not by itself show the retract ran, because the
restoration is intermittent. The two facts `ac216c89`'s retract rests on were
therefore witnessed on their own, against the real Haiku seat of the standing
run `fms-c42635`, by driving Herdr directly:

1. `herdr agent prompt <pane> "Soft.{ m-… }"`, then 1.2 s later
   `herdr pane send-keys <pane> esc esc`. The composer then read
   `❯ Soft.{ m-… Owner Text.«…» }` — the letter restored, whole,
   with a non-breaking space after the glyph.
2. `herdr pane send-keys <pane> ctrl+c`. The composer read blank on the first
   read 350 ms later — one press, within Flow's twelve reads.

Both keys are accepted by Herdr's parser and `ctrl+c` is not special-cased
there (`src/app/api_helpers.rs`, `src/config/keybinds.rs`); an unknown key
would have rejected the whole batch with exit 1, and neither call did.

Flow's `text_after` trims what follows the glyph before matching
`Soft.{ m-`; Rust's `trim` removes U+00A0, which is `White_Space`, so the
restored line matches `RecognizesLetter`. Checked against a standalone Rust
program on the exact observed line, not through Flow's own code.

## What remains

- **A flaky test in Flow's own Nix gate.** The first build of `ac216c89`
  failed on `tests::a_process_in_a_pane_is_found_by_its_own_marks_or_its_ancestors`
  (`crates/flow-nexus/src/lib.rs`, `caller_pane()` returned `None`); the same
  build on the same builder passed on retry, 161 of 161. It reads `/proc`
  under load and is not related to 0.17.1. A gate that fails one build in two
  is not a gate; it wants its own fix and its own proof.
- **The Claude retract path has no fixture test.** `tests/submission.rs`
  drives the fixture composer through the Codex glyph and the line-by-line
  take-back only; `Retraction::Key("ctrl+c")` is covered by the live witness
  above and by nothing else.
- Scenarios 5, 6, 8, 9, 10, 11, 12 were not re-run against `ac216c89`; run 2
  has them against 0.17.0.
- Whether the restoration happened at all in the five scenario-4 passes is not
  recorded: Flow keeps one `PaneLease` row per delivery and overwrites it, so a
  retract leaves no durable trace. A run cannot yet say which path it took.

## Sources

- `~/.cache/flow-message-sandbox/fms-b9d80b/{results.md,results.json,evidence,logs}`
  — the six-scenario run against `ac216c89`.
- `~/.cache/flow-message-sandbox/fms-c42635/` — the standing run: four repeats
  of scenario 4 and the direct mechanism probe.
- `~/.cache/flow-message-sandbox/{fms-9a3e2b,fms-d70a61,fms-3a987a}/state.json`
  — the revisions those earlier runs actually built.
- flow `s1-e167d8` `ac216c89`, and `93109005` before it.
- `flows/e167d8/reports/sandbox-suite-run-2.md`, corrected.

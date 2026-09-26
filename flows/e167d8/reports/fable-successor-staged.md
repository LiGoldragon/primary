# Fable successor of da88cf — staged, then launched on GO SUCCESSOR

Staged by e167d8 2026-09-26 pre-launch; da88cf said GO SUCCESSOR and the main
flow ordered the launch to proceed; executed the same session. Flow ID
assigned: `b860be` (`PsycheV2.{ Fable b860be }`).

## 1. Flow Start (executed)

Source file and hash verified first:

```
sha256sum flows/e167d8/reports/fable-successor-of-da88cf-launch.md
ba5bd81df3858e15ab38a2f91ab52308e97307c7398c204276500227c907b7fe
```

Bundle file (validate()-only for Claude; content unread by the composer but
must exist, be absolute, regular, non-symlink):
`/home/li/.local/state/flow/launch-bundles/launch-fable-successor-da88cf.md`
(written fresh, same shape as the standard main-flow-mode file, "Predecessor:
da88cf").

Datom sent to `flow` (relative SourcePath, per 0.12.2's rejection of absolute
paths):

```
Start.{ { fable-successor-da88cf-1 [ { flows/e167d8/reports/fable-successor-of-da88cf-launch.md ba5bd81df3858e15ab38a2f91ab52308e97307c7398c204276500227c907b7fe } ] [ main-flow spirit psyche psyche-interraction flow-aspect behavior messaging compensation-messenger-clj herdr file-editing skill-designing orchestrate testing-commit-scope metaflow operating-system nix-workflow main-feature-integration feature-development repository-lifecycle lojix stale-lock secrets testing-transitive-network-topology visual-report-from-md ] Psyche High Claude claude-fable-5-1 high None [ { da88cf 1 } ] messaging-build /home/li/.local/state/flow/launch-bundles/launch-fable-successor-da88cf.md «Carry out flows/e167d8/reports/fable-successor-of-da88cf-launch.md.» } { e167d8 e167d857-17e7-441b-b38b-54941a77a77a fable-successor-of-da88cf } }
```

Outcome (W, this flow): first call answered `StartAmbiguous.{ ... }` (matches
the known 0.12.2 fault — first Start answers Ambiguous before promoting), Flow
ID `b860be`, native session `b860be42-d89d-4eee-a0c2-216ec0107a86`, pane
`w1A:p1`, session `messaging-build`, all 22 skills resolved with their exact
SHA-256 (main-flow included, resolved from
`/home/li/primary/.claude/skills/main-flow/SKILL.md`). A second identical call
returned the same `StartAmbiguous` (idempotent on the same launch-request id).
`flow 'List.{}'` showed `b860be` as a real `FlowNode`, lifecycle `Pending`,
immediately — the launch had in fact gone through despite the Ambiguous
receipt, matching precedent (da88cf and e167d8 both launched under the same
fault).

## 2. First-prompt receipt (verified)

`herdr pane read w1A:p1` showed all 22 skills loaded via the Skill tool in
order, ending `● FLOW_LAUNCH_RECEIPT_V2`, then the seat stopped (the fixed
receipt footer), as staged for. Terminal title read back at that point:
`◐ PsycheV2.{ Fable b860be }` (stripped: `PsycheV2.{ Fable b860be }`) — correct
form, no manual title-setting needed; Flow/Herdr set it from the launch.

## 3. Follow-up prompt (executed, starts the brief)

```
flow 'Send.{ b860be «Receipt confirmed. Begin the brief now: carry out flows/e167d8/reports/fable-successor-of-da88cf-launch.md in full — read flows/da88cf/reports/handoff.md whole, remember da88cf at depth one, and route every per-wave report to e167d8.» }'
```

Result: `Sent.Accepted.b860be`. `flow 'List.{}'` then showed `b860be`
promoted to lifecycle `Active`. Pane evidence: the seat opened its own flow
directory (`flows/b860be/{vision,notion,reports,receipts}`), wrote its log
naming da88cf as predecessor and the launcher's instruction verbatim, and
dispatched subflows to read the brief and to read
`flows/da88cf/reports/handoff.md` for the depth-one remembering — all as
directed.

## 4. hm-register (executed, two-step)

Flow Start does not register the new seat in messenger-clj (per precedent).
The Herdr agent name at launch was the launcher default
(`claude-bccd531237a4454d86f45447`); `hm-register` requires an already-live
Herdr agent named exactly the target name, so the agent was renamed first:

```
herdr --session messaging-build agent rename w1A:p1 psyche-fable-of-da88cf
FLOW_ID=e167d8 hm-register b860be psyche-fable-of-da88cf --session messaging-build --native-thread b860be42-d89d-4eee-a0c2-216ec0107a86
```

(First attempt with `--native-thread e167d857-...` — this flow's own thread —
was refused: "Explicit native thread differs from Herdr agent_session"; the
new seat's own native session id is required.)

Result: `Registered b860be: psyche-fable-of-da88cf (messaging-build)`.
`hm-list` confirms: `b860be  psyche-fable-of-da88cf  messaging-build
working`.

## 5. Title readback (verified)

`herdr --session messaging-build agent get w1A:p1` → terminal title stripped:
`PsycheV2.{ Fable b860be }`. Correct `<Aspect>V2.{ <Model> <FlowId> }` form;
no correction needed.

## Validated before launch, all confirmed

- All 22 skill directories exist under `.claude/skills/`.
- `flows/da88cf/reports/handoff.md` exists (183 lines), whole and readable.
- `FLOW_SOURCE_ROOT=/home/li/primary` (read from the live `flow-nexus`
  systemd unit environment): the launch source path is relative to it and
  resolves correctly.
- `LaunchProfile`/`LaunchSource`/`RememberedFlow`/`OriginClue` field shapes
  read from the vendored `signal-flow` ethos (`ethos/signal.ethos`, matching
  across the checked revisions including the one pinned by the primary `flow`
  submodule's `Cargo.lock`); the composed-prompt rendering read from
  `flow/crates/flow-nexus/src/composition.rs` (`render_native_head`,
  `render_body`, `validate`, `read`) confirms: `skill_name_vector[0]` becomes
  the literal `/main-flow` command; the rest render as "Then load through the
  Skill tool, in this order: ...", which the seat's own turn actually
  performed one by one; `RememberedFlow` is `{ FlowId RememberingDepth }`,
  so "depth one" is `{ da88cf 1 }`; `SourcePath` must be relative with no
  `..`; `SystemPromptBundleFile` must be an absolute, existing, non-symlink
  regular file even for Claude, though its content is never read for Claude
  (only Codex reads the bundle text; validate() still requires the file to
  exist).

## What was not independently re-derivable and was carried by precedent

- The exact positional datom field order was confirmed from the ethos source,
  not merely inferred from the one older worked example (38de5b's proposal
  draft); that example matched the ethos exactly, which increased confidence.
- Whether `main-flow`'s own skill body directs the seat to run `/refresh`
  itself (the primary CLAUDE.md's "Flow refresh pointer") was not traced line
  by line before launch; the seat is expected to follow it once oriented, per
  that pointer, through its own skill interface — not something this launcher
  loaded or ran on the seat's behalf.

## Outcome

- New Flow ID: `b860be`.
- Title readback: `PsycheV2.{ Fable b860be }` (W).
- Receipt evidence: full skill-load transcript ending `FLOW_LAUNCH_RECEIPT_V2`
  (W, pane read).
- Messenger registration receipt: `Registered b860be: psyche-fable-of-da88cf
  (messaging-build)`; `hm-list` shows it `working` (W).
- No gate failed. da88cf was not stopped or retired; it remains crossover-only
  and Active in `flow 'List.{}'`.

## Sources

- `flow 'List.{}'`, `flow 'Send.{ ... }'`, `flow 'Start.{ ... }'` outputs (this
  session).
- `herdr pane read w1A:p1`, `herdr --session messaging-build agent get w1A:p1`,
  `herdr --session messaging-build agent rename w1A:p1 psyche-fable-of-da88cf`.
- `hm-register`, `hm-list` outputs (this session).
- `flow/crates/flow-nexus/src/composition.rs` (live checkout).
- `/git/github.com/LiGoldragon/signal-flow` vendored checkouts,
  `ethos/signal.ethos` (multiple revisions, consistent field shapes).
- `flow/README.md`.
- `flows/88475f/log.md`, `flows/88475f/handover.md`,
  `flows/88475f/reports/{fable-integration-launch,opus-successor-launch}.md`.
- `flows/da88cf/reports/{handoff,integration-1}.md`.
- `/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/{main,core}.clj`.
- `systemctl --user show flow-nexus -p Environment` (FLOW_SOURCE_ROOT).

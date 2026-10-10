# Flow 0.17.3 in Home: semantic review

Subflow of 8904b1, read-only, 2026-09-26. Subject: Home stage fccc265
(parent 5ba2e1e) moving `flow-next` from ac216c8 (Flow 0.17.1) to 0b512ee
(Flow 0.17.3). Nothing was built, checked, evaluated, activated, or messaged.
Two `List.{}` queries were made to the running Nexuses; they are queries and
write nothing (Flow 0.14.0 UPGRADES: "`List` writes nothing").

Labels: **O** observed in source, git, or the host; **I** inference;
**U** unknown. A claim quoted from a commit or UPGRADES is that record's claim.

## 1. What changes between ac216c8 and 0b512ee

History (O): b08f41f (test deflake), a89ef3b (Claude retract fixture tests),
e7efa65 (0.17.2 bump), d97e120 (0.17.3), 0b2929e (wrapper parsing), and the
merge 0b512ee, which brings in main's 9fcd625 (a test-only wait fix on the
0.14.0 line). Diff: Cargo, UPGRADES, flake.nix, `composition.rs`,
`herdr/launch.rs`, `lib.rs` (tests only), `tests/submission.rs` (tests only).
Flow's flake.lock is unchanged; signal-flow 7.0.0 (1c9e4b3) and
meta-signal-flow 11.0.0 (2ac045c) are the same (O).

Production behaviour change, all on the Claude Start path (O):

- **Composition.** Before, a Claude first prompt with a line break or over 800
  UTF-16 units was refused (`ClaudeFirstLineBroken`, `ClaudeFirstLineTooLong`,
  surfaced as `StartRejected(CompositionRefused)`). Now such a prompt is
  rewritten in a "direct" form: `Read <bundle> for your launch mode, then load
  these skills through the Skill tool in this order: a, b, c. Then:
  <instruction> [Sources: …]` + the receipt footer. No size ceiling remains in
  Flow (tests compose 34,369 characters). Short one-line prompts keep the
  native `/skill` stack (at most five commands) as before.
- **Observation.** Before, a first user row containing `<pasted_content` was
  an error. Now a row that is exactly `<pasted_content[ attrs]>\n…\n</pasted_content>`
  is unwrapped; it is accepted only if the inner text hashes to the persisted
  `prompt_sha256` under the footer and has the direct-form wording. Then the
  native stack is set to zero and every selected skill must arrive as a
  `Skill` tool call, in order, with a successful result and the exact skill
  body as companion, before the receipt counts; model and effort are still
  checked on the receipt row. 0b2929e rejects near-tags such as
  `<pasted_contention`.

Classification (I): a repair that is also new capability (long and multi-line
Claude Starts now proceed). No request or reply type, stored row, socket, or
command argument changes (O: no wire or store file in the diff;
`CompositionError` is internal). `CompositionRefused` stays on the wire but is
no longer produced for size; a caller relying on that refusal as a guard loses
it. 0.17.2 changed only tests and the flake's named checks.

Version step (I): 0.17.3 as a patch is consistent with Flow's practice
(0.17.1 non-breaking fix = patch; 0.17.0 breaking = minor). 0.17.2 bumps for a
test-only change, which contradicts 9fcd625's own rule a day earlier ("No
production code changed, so no version moves") and the versioning skill; it
is harmless but inconsistent. The 0.17.3 UPGRADES entry does not say
"non-breaking" or name the wire, as 0.17.1 and 0.17.2 do.

## 2. The Claude startup repair, against the witnessed defects

| Witnessed defect | 0.17.3 |
|---|---|
| 3 of 21 skills expanded; spirit absent | Checked condition. Every skill in the selection must be confirmed in order before the receipt counts; this already held in 0.17.1 for the stacked+Skill path and now holds for the pasted path (O). Flow does not add spirit; it confirms only what the profile selects (O). |
| First prompts refused for size | Addressed: no refusal for size or line breaks (O). Remaining limit (I): the prompt goes to `herdr agent prompt` as one argv element; Linux caps one argument at 128 KiB. |
| Start recorded failed while the seat ran | Not addressed; possibly reintroduced in a narrow case (I, below). |
| First prompts by an unidentified path | Not touched by this delta. The one write is `herdr --session S agent prompt <agent> <text>` keyed to the durable intent (O); 0.15.0 "Flow is the only pane writer" predates it. |
| Claude endpoints always unavailable | Left. `claude.rs` (unchanged) reports Available only for a daemon-backed job (`backend == "daemon"` in `~/.claude/jobs/<id>/state.json` and the daemon roster), with `/home/li/...` paths hard-coded (O). Foreground `--remote-control` seats stay Unavailable (I). Next's List shows all four Claude rows Unavailable (O). |
| Seats bound under a predecessor's agent name | Left. The Herdr agent name is `claude-` + 24 hex of SHA-256 over the launch request id (O); unchanged. |

Evidence 0.17.3 requires before Started (O): persisted launch and prompt-delivery
intent; pane and native session binding; a first user row matching the hash
(plain, stacked, or now pasted-direct); every selected skill confirmed in
order; exactly one `FLOW_LAUNCH_RECEIPT_V2` assistant row with the intended
model and effort (a row with no effort passes, 0.17.0). Readiness of the
Claude endpoint is separate and not implied.

**Defect found (I, from code, not run):** the composer chooses the direct form
whenever the text has any line break or is over 800 units. The claude-harness
skill records that two or three lines under about 900 characters arrive
*plain*, not wrapped. Such a prompt (a short instruction with a line break)
reaches the observer as a plain row while the stack is still non-zero; the
branch `None if claude_stack > 0 && !input_verified` returns "native Claude
first turn loaded no stacked command". The seat has the prompt and may load
every skill, but Start fails: the witnessed "recorded failed while the seat
ran" shape. The new composition test for line breaks checks composition only;
the observation test covers only the wrapped case. The 800 and wrap rules are
Claude Code 2.1.280 observations; a harness change moves them silently.

Also (I): wrapped input carries reduced authority in the stock system prompt
(claude-harness skill). Flow replaces the system prompt with
`--system-prompt-file`, so that clause may not apply, but the whole brief of a
long Start now arrives as pasted content. No live witness of a 0.17.3
direct-form Start was found in flows/ (U).

## 3. The changed check

Before and after, `checks/flow-message-next` (O): asserts the four input revs
equal literals; next units exist, are disjoint from stable's names, runtime
dirs, sockets and state; next Flow runs `flow-nexus` with no arguments on its
anchors; then runs stable Flow, next Flow, and next Message together in a
sandbox (Herdr, Claude, Codex, harness all stubbed to `exit 0`), checks
`flow-next List` = `Listed.[]`, `message-next-meta Send` to an unknown
recipient = `SendRejected.UnknownRecipient`, and an unknown receipt query.

The only change is `nextFlow` ac216c8 → 0b512ee (O). It is a value moved to
follow the pin, not a weakening. The expected rev is written by the same hand
in the same commit as the pin, so it is not an outside oracle: it guards
against lock drift, not against a wrong choice. A pass says the pair builds,
starts, keeps apart from stable, and that Message resolves a recipient through
Flow (one real Flow–Message round trip). It says nothing about Start, Claude,
Herdr, or the 0.17.3 change. Flow's own `checks.default` runs the whole
workspace test suite (O, flake.nix); whether it was run for 0b512ee is outside
this review (U).

## 4. Companions

- **Message-next 481b579 (0.17.0):** UPGRADES 0.17.3 says "Deploy beside
  Message 0.17.0, or do not deploy at all" (O). Same wire as 0.17.1, so no new
  demand (I).
- **Messenger (messenger-clj 0.2.6):** nothing in the delta touches it (O). Not
  reached: how it reaches Flow.
- **Herdr (0.8.2 on the stable unit's PATH, O):** 0.17.3 now depends on
  `agent prompt` carrying long and multi-line text into Claude faithfully, so
  that Claude records it as one wrapped row (I). Not verified (U).
- **Stable Flow:** running 0.12.2 (PID 1937, O) although Home main pins stable
  Flow 9fcd625 = 0.14.0 since Home 8a60835c (O); an earlier receipt calls this
  "a temporary profile element". Next and stable keep separate state
  (`~/.local/state/flow-next`, `%t/flow-next`) and neither reads the other's
  store (O, check). The delta changes no stored shape, so 0.17.3 reads
  0.17.1's rows unchanged and a rollback to 0.17.1 is possible (I). Exception
  (I): a Claude Start pending in direct form at rollback would be judged by
  0.17.1 as "arrived as pasted content" and fail.
- **Breaking-upgrade procedure:** not required for this delta (non-breaking).
  It is required for the stable move 0.12.2 → 0.14.0 that activating Home main
  would bring (signal-flow 6.2.0, new lifecycles, with Message 0.14.0).

## 5. Against the psyche

Bearing statements (verbatim; newer weigh more):

- "There should be only one prompt when we start a fresh flow, not two" and
  "Well I was putting in the /skill command style in Claude for a long time
  and it was working." — living, 2026-09-24, to e51411
  (`flows/e51411/vision/launch.md`).
- "Let's not give them too much prompt. Let's make sure there are no hashes,
  garbage, and stuff like that in there." — living, 2026-09-24 16:22:52, to
  9ddcbc (`flows/e51411/vision/launch.md`).
- "All that matters is that everything comes in as one block." — living,
  2026-09-24 20:21:30, to 5f38bc (same file).
- "every time we're making a single prompt, we're making an LLM call … Everything
  should be in one prompt." — psyche, typed, 05c604 (`flows/05c604/vision/launch.md`);
  and "The way your skills were loaded, one after another, is really
  inefficient because then you talk and then it's a bunch of LLM calls." —
  psyche, STT, 2026-09-23 22:02Z, to d8df70 (`flows/d8df70/vision/launch.md`).
- "I can see these messages getting the pasted content ID/XML tags. I want that
  gone." and "I guess it's a bit of a problem that Claude automatically wraps
  this with the pasted content thing but maybe there's a way around that." —
  living, 2026-09-25, to e51411 (`flows/e51411/vision/messaging.md`).
- "somebody launched too many flows that were on the same role and then
  launched the flow with too high an effort … let's make sure the code makes
  sure it doesn't happen again." — psyche, STT, 2026-09-26, to 93ba9f
  (`flows/93ba9f/vision/flowLaunching.md`).
- "A Nexus component decides the system prompt and everything about a launch"
  — distilled, `Vision/flowNexus.md`.

Serves: one prompt, one block (no second prompt; O); no hashes in the prompt
(O); code, not a flow, decides and verifies the launch.
Silent: duplicate roles and effort ceilings (no guard in the delta; a grep of
0b512ee found none, U whether one exists elsewhere); Claude endpoint readiness.
Appears to go against:
- *Lean prompt:* the only ceiling on first-prompt size is removed.
- *Pasted wrapper should go:* 0.17.3 adopts the wrapper as a startup route
  instead of avoiding it; the start-argument route, which the harness skill
  records as never wrapped, is not used.
- */skill in one prompt, not many LLM calls:* in the direct form every skill
  is a Skill-tool call, so a long Start costs more model round trips than the
  native stack of up to five.
These are raised, not resolved.

## 6. What activation would touch

- `flow-nexus-next` restarts onto 0.17.3 (O: its ExecStart is the package).
  It holds five rows: 93ba9f, b7ba00, c56100, dc53b4, e167d8 (O, List). Rows
  persist in its store; restart re-reads them (I). `flow-configuration-next`
  (oneshot, `Requires=flow-nexus-next`) re-runs (I). `message-nexus-next` is
  `After=` only; whether it restarts depends on its unit text (U).
- Stable `flow-nexus` 0.12.2 holds 25 rows (15 Active, 10 Pending), including
  8904b1, 56ae53 and 6fe957 (O). Whether a generation built from Home main
  moves it to 0.14.0 depends on how the live profile element is composed (U);
  if it does, the stable Nexus restarts on a new wire, which is where the
  recovered flows most likely live (I). That move is not this change but rides
  with the same activation.
- Witness before: both Lists; each next row's pane and Herdr agent name; the
  running store paths. After: the same Lists and bindings unchanged; one
  Claude Start through next with a two-line short instruction (the defect
  case), one over 800 units, one short single line, each reaching Started
  with every skill confirmed.

## Concerns

1. Multi-line short Claude Start fails after the seat runs — blocks
   activation only (next Flow is not used for Starts until activated); should
   be fixed or witnessed before 0.17.3 is relied on.
2. No live witness of a direct-form Start on Claude Code 2.1.280 — blocks
   activation only.
3. Stable 0.12.2 running while Home main pins 0.14.0 — blocks activation only;
   the Home main move itself does not change it.
4. Psyche tensions (lean prompt, pasted wrapper, LLM calls per skill) — to be
   noted; raise with the living.
5. Check expected rev is self-written, and the check never exercises Start —
   to be noted.
6. 0.17.2 version bump for tests only; 0.17.3 note omits "non-breaking" and
   rollback — to be noted.

Nothing found blocks the Home main move itself: the move changes one pin of a
side-by-side next service, the wire and store are unchanged, and nothing runs
until activation (I).

## Unknowns / not reached

Herdr's handling of long or multi-line `agent prompt` text; whether Flow's
own test suite was run at 0b512ee; the messenger's dependence on Flow; how
the live profile gives stable 0.12.2; whether `message-nexus-next` restarts;
which Nexus holds "the nine recovered flows" (inferred stable).

## Sources

- /git/github.com/LiGoldragon/flow: `git log`/`git diff ac216c8 0b512ee`;
  `crates/flow-nexus/src/{composition.rs,herdr/launch.rs,claude.rs,launching.rs}`,
  `UPGRADES.md`, `flake.nix`, `Cargo.lock` at 0b512ee; `Cargo.toml`,`flake.nix` at 9fcd625.
- /git/github.com/LiGoldragon/CriomOS-home: `git diff 5ba2e1e fccc265`;
  `checks/flow-message-next/default.nix` at fccc265; `git log` for 8a60835c, fed50084.
- Host: `systemctl --user show` for flow-nexus, flow-nexus-next,
  message-nexus-next, message-daemon; `ps -C flow-nexus`; `flow List.{}`,
  `flow-next List.{}`; `~/.local/state/nix/profiles`.
- Skill: claude-harness (wrap thresholds, authority of wrapped input).
- Psyche: `Vision/flowNexus.md`; `flows/e51411/vision/{launch,messaging}.md`;
  `flows/05c604/vision/launch.md`; `flows/d8df70/vision/launch.md`;
  `flows/93ba9f/vision/flowLaunching.md`; `flows/56ae53/vision/model-flow-emergency.md`.
- flows/8904b1: `log.md` (lines 462–466), `receipts/home-step2-owner-evidence.md`,
  `receipts/flow-0173-home-pin-facts.md`, `witnesses/flow-0173-stage-review.md`.

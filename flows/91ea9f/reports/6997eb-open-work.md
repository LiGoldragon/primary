# 6997eb's open work, carried into 91ea9f

## One-screen summary

- **The living's words.** The gathering at line 2378 holds 35 quotes in seven subjects. 6997eb named six of them: starting sessions, handling skills, messaging and hooks, deprecating sessions, restarting sessions, ephemeral sessions. The seventh is the Flow nexus's role. I matched every quote to a record. Two needed correcting: the da1e3f quote joins two separate typed lines, and the 5c8be3 quote is typed, not "n/s".
- **The living typed nothing to 6997eb after line 2294** (his 2026-10-02 order). Every input after that is a seat message or a task notification. Every ruling 6997eb presented from then on is unanswered.
- **Implementation map (line 2427).** Live seats start from two hand-run Node launchers, never through Flow. Flow's Start was refused three times and its Restart always refuses. Both launchers poll the transcript every second. Skills are deployed by hand. There is one SessionStart hook. Held messages are never retried. Flow and the messenger keep two registries. Ephemeral sessions register nowhere. Mind later found two items wrong (the Curriculum pin, and some "dead" tools still packaged) and fixed the rest.
- **Book pipeline.** The datom-line metadata is ruled. The rest stops at design:
  - QueueTurnEnd is declared in signal-flow 6.3.0 but no hook is installed.
  - The Transcript nexus is not built.
  - Flow-or-Transcript is still unruled. Option (a): the hook calls `flow`, which owns the turn event and identity. Option (b): the hook calls `transcript` directly, which is shorter but needs that nexus built first. 6997eb leaned to (a), then took Opus's split: Flow for the event, Transcript for the content, read by pointer.
  - 6997eb called e06e4c the "later word"; it is the earlier one (08-19 against b05237's 09-18).
- **Codex successions.** The fixed standalone launcher (edb450) is ruled as the route for these three successions only. Making Flow Start the route and deleting the launcher is the successors' first work. Field Astra's successor goes first and is the first real witness of the hook. Every machine gate closed; the living's word never came into this transcript.
- **Unanswered.** Eight rulings in three blocks after line 2378, two tensions, the roster's "Say if you meant fewer", and the open list in 6997eb's successor brief.

---

## Full account

### 1. The gathering of the living's words (record 2378, 2026-10-02T17:11Z)

**What was asked.** The living's order, typed 2026-10-02 to 6997eb, is at line 2294 and in `flows/6997eb/vision/metaHarness.md`. It begins "Get a full grasp of everything and re-question this: …" and lists seven bullets: "Starting sessions", "Handling skills", "Messaging hooks", "Deprecation of session", "Restarting of sessions", "Starting of ephemeral sessions", "All of the session handling side of things".

**How 6997eb named the six.** In the Sonnet brief at line 2312: "starting sessions, handling skills, messaging and hooks, deprecating sessions, restarting sessions, ephemeral sessions". The gathering subflow added a seventh, the Flow nexus's role. «Six questions on sessions, re-asked» folds the six into four points: Starting; Messaging and hooks; Deprecation and restart; Ephemeral sessions. Handling skills got its own book.

**How I checked.** I matched every fragment by exact string to a record under `flows/*/vision`, `notion` or `reports`. "n/s" means the record does not say whether he typed or spoke. Square brackets inside quotes are insertions by the recorder.

**1. Starting sessions** (status: fat first prompt settled; how sessions are created is open)
- "we shouldn't let the models compact… better off rebootstrapping on with a really good first prompt on a new flow." (2026-09-14, 6cc91b, STT; `flows/6cc91b/vision/flowLifecycle.md`)
- "Let's predefine them so that there's basically no argument to give except a small description of the goal" (2026-09-17, 9993b5, typed)
- "inject it in a new flow at the user level so it understands what I want and hasn't just read it from the bottom context layer?" (2026-09-24, 752e0f, typed)
- "My new flows are not getting a nice fat user prompt for context. They're told to read files" (2026-09-29, 183ae0, typed; held in `fe945a/vision/context.md`)
- "Just create new sessions, which really should be done with almost zero LLM calls" (2026-10-01, e2a70a, typed)
- Open: "If it's possible we should just pass the title of the session as an argument" (2026-10-01, e2a70a)

**2. Handling skills** (status: direction settled; the deploy mechanism is open)
- "every time we modify the curriculum, some giant nix check has to run" (2026-08-25, 01a035, n/s)
- "if curriculum is a nexus, we can't have any data there because it's going to keep rebuilding it." (2026-09-17, 108ab0, typed)
- "We need to make a nexus to deploy skills… changes the ones that have the same name. That sounds simple to me." (2026-09-28, 8904b1, reads as STT)
- "we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know." (2026-09-29, 183ae0, n/s)
- "now vision is skill. Let's make that whole migration… merging, migration, and deployment, and the new infrastructure for all of it." (2026-10-01, fe945a, typed book comment)
- 6997eb added two more in «Handling skills»:
  - "the skills will be typed", and a nexus "that has a fully typed specification for the different types of inputs that it can take" (`183ae0/vision/skills.md`)
  - "eventually the skills will live in a daemon not in a Git repo anymore." (`8904b1/vision/skills.md`)

**3. Messaging and hooks** (status: hooks and no polling settled; which events to use is open; hooks writing into incoming messages is a notion, "more like psyche research")
- "there should be a way for some kind of hook to send the message to the other harnesses." (2026-09-13, 6cc91b, STT)
- "no, message, not flow-send. use the message nexus! flow is to start or refresh a flow" (2026-09-17, da1e3f, typed)
  - **Correction:** in `da1e3f/vision/operational-flowVsMessage.md` these are two separate typed lines, "no, message, not flow-send. use the message nexus!" and "flow is to start or refresh a flow". The gathering joined them.
- "use hooks at the start and the end of the Claude or the Codex session to register or unregister that session from the registry?" (2026-09-23, d8df70, typed)
- "Essentially we want to avoid polling, which means we're going to make this hook-based." (2026-09-30, 7328f4, STT)
- "It makes perfect sense for the flow events to call the flow CLI to let the flow nexus know the state of that flow through the harnesses' interfaces, which are the hooks." (2026-10-01, fe945a, typed)
- Settling words: "Nobody should be checking anything repeatedly." (2026-10-01, fe945a, typed)

**4. Deprecating sessions** (status: reaping and archiving settled; the mechanism is open; he listed "Deprecation of session" to re-question on 10-02)
- "garbage collecting sessions and sort of archiving them, and just keeping the important parts of the exchanges" (2026-09-13, 6cc91b, STT)
- "When a session gets replaced, it has to be reaped so it doesn't keep getting messages." (2026-09-17, 1ac573, n/s)
- "A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived." (2026-09-24, d8df70, typed comment)
- "We need to reap the old Codex sessions and archive them." (2026-09-29, d5b96b, typed)
- "close and archive the old sessions" (2026-10-01, e2a70a, typed)

**5. Restarting sessions** (status: settled, with one tension)
- "there's no handoff file; the flow *reads its previous flow(s)*… imposing the old opinion on the new flow is the wrong approach." (2026-08-21, 5c8be3)
  - **Correction:** the record (`flows/5c8be3ca/vision/flowArtifacts.md`) says **typed**, not n/s.
  - Full text, line-wrapped in the source: "there's no handoff file; the flow *reads its previous flow(s)* - it's the inverse of push dont pull, since LLM flows are totally different than regular software (non deterministic); the new flow needs to make its own view of the old; we are refreshing for that very reason, so imposing the old opinion on the new flow is the wrong approach."
- "It just needs to be a command sent to Flow, and if the flow ID matches the flow's provenance, then we can restart it." (2026-09-17, 9993b5, typed)
- "You can quit the harness and start the harness again… and then type in `resume`" (2026-09-29, bea031, typed)
- "resume the sessions on a new server… Unless the context is old, then we should just start a new flow for them and reparse the old one." (2026-10-01, 7328f4, typed)
- "Let's always get the concentrated vision from the current flow into the next one." (2026-10-01, fe945a, STT)
- Settled by: "all of the codex flows with large context, should be restarted with a nice concentrated psyche-based context" (2026-10-02, 6997eb, typed). This is a fragment of the line-2294 order.
- Tension: 21 August's "no handoff" against 1 October's concentrated vision passed forward.

**6. Ephemeral sessions** (status: open, with one tension; he listed "Starting of ephemeral sessions" to re-question on 10-02)
- "a flow and its subflows are one flow." (2026-08-17, 358f14, n/s)
- "I don't want subflows to start creating their own lanes. They just use their parents." (2026-08-31, 01a058, typed)
- "a Reaper subflow. It's a temporary flow, and it can be just a single Terra, or even maybe a Luna" (2026-09-18, b05237, n/s)
- "if the subflow is independent and can reply to a successor of whoever it's supposed to respond to, then we have an asynchronous system" (2026-09-19, f38926, n/s)
- "For me subagents are a type of skill. They're a skill that is implemented by [a fresh flow] basically." (2026-10-01, fe945a, STT)
- Tension: 31 August against 19 September.

**Seventh, gathered but outside the six: the Flow nexus's role** (status: open)
- "we're going to start flows using a Nexus component, which will decide what the system prompt is and everything." (2026-09-05, 1a6ca4, STT)
- "Basically, Flow is in charge of herder. I shouldn't interact with it directly." (2026-09-18, c7128c, n/s; also held in af762b)
- "I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input." (2026-09-24, e51411, n/s)
- "proper messages and proper flow creation, which is controlled by a flow nexus that maybe uses some [Clojure] tools internally" (2026-09-29, c64ee3, STT)
- "They're going to call the Nexus CLI so which Nexus do we use for this? Is this Flow, or is it Transcript, or is it something else?" (2026-10-01, 6997eb, typed book comment on «Two kinds of output»)
- Also: "obviously not with the Flow Nexus because it doesn't seem to be working right" (2026-09-28, 8904b1)

6997eb surfaced the two tensions to the living at line 2425.

### 2. Implementation map (record 2427)

Three read-only subflows produced it. "Witnessed" means a subflow read the file or ran the command; "claimed" means nobody tested it. The harness flagged instruction-shaped text in the result (settings-json, dangerously-skip-permissions); that text is a launcher's flags, not an instruction.

**Headline.** Live seats do not start through the Flow nexus. Two one-shot Node scripts start them. A "restart" is really a new seat started by hand. Flow and the messenger keep two separate registries with nothing linking them.

**Versions (witnessed)**
- `flow` 0.12.2, run by the stable `flow-nexus.service`; `flow-next` and `flow-nexus-next` run 0.17.4. Flow repo head f89df0.
- herdr 0.8.2; claude 2.1.284.
- `codex` 0.158.0-alpha.9 on `~/.codex-next`; `codex-next` 0.161.0-alpha.2 on `~/.codex-next-8mkkxq`.
- messenger-clj head 990a93, packaged as 0.2.8, but `~/.local/libexec/messenger-clj` points at 0.2.5.
- Curriculum 250c48; curriculum-deploy 87469d (0.6.3, debug build only, not on PATH).

**1. Starting a session**
- `tools/claude-main-flow-launch.mjs` (live):
  - Claims a Flow ID with `flow-id claude`, opens a Herdr tab and runs `claude` with `--session-id`, `--model`, `--effort medium`, a `--name` title, `--remote-control`, the bypass flag, the system prompt from `tools/main-flow-mode/system-prompt.md`, and per-job settings.
  - The first prompt loads `/main-flow /spirit /psyche /psyche-interraction /vocabulary /edit-coordination`, then the `--brief` file.
  - It ends with a Herdr session report, a rename and `hm-register`.
- `tools/codex-main-flow-launch.mjs` (live): pastes the text of the same six skills from `.agents/skills`, then the brief. It passes no title flag; the title is set afterwards through `thread/name/set`.
- `tools/native-main-flow-launch-shared.mjs`: builds the title and picks `codex` or `codex-next` by model.
- Flow nexus `Start` (`crates/flow-nexus/src/herdr/launch.rs`):
  - Creates a Herdr workspace and runs `herdr agent start`.
  - Skills and brief come from the caller's launch profile; the bundle goes to `~/.local/state/flow/launch-bundles`.
  - No title flag: Claude gets a typed `/rename`, Codex gets `thread/name/set`.
- SessionStart hook: `herdr-agent-state.sh` only reports the pane and session to Herdr.
- Gaps:
  - Flow Start was refused three times (`flows/8904b1/witnesses/flow-0174-three-live-start-attempt.md`). `flow List` shows seats registered after they started, not seats started through Flow.
  - Both scripts poll the transcript once a second.
  - Every brief is a hand-written file, and effort is hard-coded to medium.
  - Likely bug: titles for gpt-6 seats go to the `~/.codex-next` socket, but `codex-next` runs on the `-8mkkxq` home's socket. The mismatch is witnessed; the failure is claimed.

**2. Handling skills**
- Source: 52 skill files in `Curriculum/skills/*.md` plus `roles.datom`. The brief's `manifests/*.dotos` do not exist (witnessed), Curriculum's ARCHITECTURE.md rules them out, and NON_MANAGEMENT_AGENTS.md still names them.
- Generation: `curriculum-deploy 'Generate.{…}'`, run by hand.
  - It copies skills into `.claude/skills` and `.agents/skills` and writes 24 role files (Claude, Codex, Pi).
  - User-only skills come out withheld for both harnesses.
  - Someone then commits Primary; the latest was b2fe03.
- Sync: `Check` returned `Checked.{ 52 24 }`, so the trees match Curriculum head (witnessed).
- Running seats (claimed, untested):
  - Claude re-reads a skill's body on invocation, but its listing is fixed at session start. Codex builds its catalog at start.
  - So an edited body probably reaches a running Claude seat. A new skill or a changed description needs a restart, and Codex probably always does.
- Gaps:
  - Nothing triggers regeneration: no hook, no unit, no Home activation.
  - `Check` does not flag extra files in the generated trees.
  - Pi gets roles but no skills.
  - The flake pins an old Curriculum (0c1cd5).

**3. Messaging and hooks**
- `hm-send` sends `#msg`, `#psyche` or `#psyches` to Herdr over the session's socket.
  - The target comes from a stored route that must match exactly one live agent.
  - The match is re-checked, including Claude's sessionId, before sending.
- Storage: routes, attempts and Held bodies are in one Datalevin store at `~/.local/state/messenger-clj/typed-datalevin`.
- Held is never retried: there is no poll and no event. `hm-repair` re-submits only `RepairRequired` entries.
- The skill is out of date: it still describes "busy registration promotes later", which was removed in 4bce27.
- Hooks installed:
  - Exactly one, a SessionStart hook calling `herdr-agent-state.sh`, in each of `~/.claude/settings.json`, `~/.codex/hooks.json` and `~/.codex-next/hooks.json`.
  - `~/.codex/config.toml` has no trust entry for it, so it may not run there (claimed).
  - The repo's `.claude` settings have no hooks.
- Gaps:
  - Held messages other than `RepairRequired` are stranded.
  - Repair needs someone to pick the right candidate.
  - Dead routes only show up when someone runs `hm-list`.
  - No hook exists for Stop, exit or retirement.

**4. Retiring a session**
- Flow `Stop` closes the pane and records Stopped. `Retire` marks the seat Retired but leaves the pane open.
- Closing a Herdr pane leaves the messenger route in place; `hm-list` shows 2 stale routes. Cleanup is `hm-deregister`, or `hm-retire`, which needs an evidence file.
- `tools/reaper` is dry-run only. `tools/reap-flow` reads the frozen old hacky-messenger store, so it cannot see `hm-retire` markers.
- `flows-archive/` is empty.
- Codex `archived_sessions`: 1494 in `~/.codex`, 894 in `~/.codex-next`.
- Indexes: only 5 of 346 `flows/` folders have an `index.md`; `sessions/index.md` was last changed in August.
- Left behind: Flow rows, messenger routes and stranded bodies, the old registry, every lane folder, the archived sessions.
- Gaps:
  - Flow and the messenger do not know about each other.
  - Exited is recorded only when something touches the seat.
  - Retirement needs someone to judge the evidence.

**5. Restarting a session**
- Flow `Restart` always answers `ResumeRefused` (`lib.rs:146`).
- `Replace` exists in signal-flow 1c9e4b, but the local checkout (968ae3) is behind it.
- `resume_codex` has no production caller.
- `claude-native-seat-refresh.py` is called only by a script already marked rejected.
- Gaps:
  - Successors are started by hand with the launcher, and the old seat is retired by delegation (`flows/caf622/log.md:503`).
  - There is no resume onto a new harness version.
  - The Codex stable/next rotation lives in wrapper and systemd state.
  - Briefs are loose files under `launch-bundles`, `flows/108ab0/` and the repo root.
  - Nothing carries over except what the brief says.

**6. Ephemeral sessions**
- Agent-tool subflows are not registered anywhere, and the Herdr hook skips them.
- `tools/native-worker-launch.mjs` starts a Codex worker through the app-server and writes only a receipt file.
- `tools/extractor/intelligence.py` is the one use of `codex exec --ephemeral`. There is no `claude -p` anywhere in `tools`.
- Gap: nothing is registered in Flow or any index; workers are tracked only by their receipt files.

**Dead tools (as mapped):** compose-seat-prompt.py, claude-bootstrap-controller.py, claude-single-turn-start.py, field-refresh-control.py, third-seat, compose-refresh-prompt, herdr-prompt-file, tools/messenger, messaging.py.

**Later corrections by Mind Sol (lines 2506, 2661, 2709, 2811, 2879, 2970)**
- Wrong or overstated in the map:
  - The Curriculum pin was already 250c48 (the map's item was stale).
  - The libexec pointer was stale, but hm-send already ran 0.2.8.
  - Of the "dead" tools, `tools/messenger` and messaging.py are called by the msg-psyche-poc app, and third-seat has a flake check. All three were kept.
  - field-refresh-control.py was mandated by a NON_IDEAL_AGENTS rule. The rule and the tool were withdrawn together in fc4eec.
- Fixed:
  - Messenger skill corrected in c99253.
  - Manifest sentence removed in b39328.
  - Launcher socket fix in 6d860 (+36/-7).
  - Five tools and four tests removed in 4a6bfd (-1120 lines).
  - Pointer aligned to 0.2.8; pin and lock in 1ce183.
- New findings, also fixed:
  - `retire!` did not refuse a mismatched native thread. Red test d2f821, guard a9fe62, package 0.2.9, durable check 55 tests / 362 assertions green.
  - README activation paragraph corrected in cc750f.
  - The candidate Codex home had no hooks.json at all; the hook was then installed (see section 4).
- Opus fe945a's «Session handling as it is» (its line 1435) added:
  - The Claude launcher registers a seat only after its first reply.
  - The book subagent is Haiku with no skill.
  - Codex subagents name gpt-5.6.
  - 347 flow folders were never reaped.
  - Sonnet was blocked about 11 hours that day.

### 3. Hook-to-book pipeline design, and the Flow-or-Transcript choice

**Origin**
- The living, line 628, typed 2026-10-01 (excerpt): "Let's design a pipeline that automates things through hooks when a certain pattern is detected. Then it can be sent to Sonnet for either a new book or for editing an already existing one."
- His book comment on «Two kinds of output» (typed, 2026-10-01; `flows/6997eb/vision/pipeline.md`): "Overall this is good. It's a good overview. It's not very detailed so let's make another book that details the anatomy of what we want to build. Where are those hooks? What are those hooks calling? They're going to call the Nexus CLI so which Nexus do we use for this? Is this Flow, or is it Transcript, or is it something else?"

**First anatomy (record 983, 2026-10-01T19:39Z).** Four points:
1. The hooks: one asynchronous Stop hook script on every seat. The only hook installed today is SessionStart to Herdr, and Herdr is not a nexus.
2. The fork:
   - **(a) Through Flow.** The hook calls `flow` with a new turn-ended request carrying session id and transcript path. Flow resolves the flow and hands the turn to Transcript, which cuts the marked block; Message delivers it to Sonnet. This honours "this will be controlled by Flow obviously" (7328f4, STT, 09-30), and Flow is already running and knows session, turn, harness and pane. The aggregator's transcript-block queries are the stopgap until Transcript stands.
   - **(b) Straight to Transcript.** The hook calls `transcript` directly. It is shorter, but the Transcript nexus must be built first (today it is a Python shim with no signal repo), and it skips Flow's ownership.
   - 6997eb's reading: (a).
3. What travels: one datom (session, turn, transcript path, or else the reply text). Transcript cuts the block and reads the title; Sonnet decides new or edit by title.
4. Build order: today the hook and Flow's turn-ended request; next the Transcript nexus; later the machine output itself becomes the event stream.

**Revised anatomy with Opus's view (record 1091, uuid c3a069…, 19:41Z)**
1. The metadata is one datom line, `Presentation.{ «title» }`.
2. The Stop hook calls `flow` (the living, relayed by cf3553: "an end-of-last-reply hook that notifies the Flow component using the Flow CLI"). Flow records only that a turn ended, with session and transcript path, "never the content".
3. Opus's improvement, taken by 6997eb: no copy goes through Message. Flow publishes the ended turn to subscribers, and Sonnet reads the block by pointer through the Transcript nexus's Block operation. One copy exists, and nothing polls.
4. A tension: b05237 says addressing transcripts is "what the Flow Nexus needs to do"; e06e4c says harness transcripts belong to "obviously another nexus".
   - 6997eb and Opus read "the later word" as pointing to Transcript.
   - **Misdating:** e06e4c is typed 2026-08-19 and b05237 is spoken 2026-09-18, so e06e4c is the earlier word. Opus's own report (`flows/fe945a/reports/which-nexus.md`) dates them correctly and offers 1b8ac0's "develop that and let Flow use it" as a possible join, its own reading.

Rulings asked in that block:
- The datom line. **Ruled** at line 1117: "Yeah the metadata is one datom line. That's brilliant. I love it. Let's do it."
- Flow for the turn event, Transcript for the content, subscription not copy. **Unanswered.**
- Astra builds the hook now, and Mind Sol adds the turn-ended request. **Unanswered;** 6997eb downgraded it to "prepare, do not install".

**What each option meant to 6997eb.** Flow is the owner of seats and identity, and the turn event comes through it. Transcript is the owner of transcript content; in (b) it is the direct target, but it is unbuilt. By the revision this was no longer a choice of one: Flow for the event, Transcript for the content. «Six questions» point 2 later pushed further: "Flow is the one registry, every harness event reaches it through a hook."

**How far it got**
- Field Astra's witness:
  - Stop hooks on both harnesses carry session, turn, transcript and last reply; none is configured.
  - In the hook environment FLOW_ID is unset, so the hook must supply identity from the session.
  - Codex needs a non-blocking wrapper and deduplication of repeated Stop calls.
  - Stop is a pre-end hook, not proof the turn-ended record exists, so the hook must enqueue and return promptly while the nexus verifies and deduplicates.
  - Flow's CLI is 0.12.2 against nexus 0.17.4, and a List probe failed at the frame boundary.
  - Astra's instinct: an output-ingestion boundary retains and deduplicates, and Flow supplies identity and routing, which matches (a).
- Sonnet's mark: point 2's "never the content" stands against the living's "possibly we should also send that to Flow" (cf3553, relayed 2026-09-19).
- Mind Sol landed signal-flow 6.3.0 (eba281):
  - Types: `Title`, `Presentation.{ Title }`, `TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }`.
  - Query QueueTurnEnd, answered by TurnEndQueued or TurnEndRejected (UnknownSession, SessionMismatch, InvalidTurnId, InvalidTranscriptPath, QueueRefused).
  - It is declared only: no consumer, hook or deployment.
- Flow's Observe selects only launches, so no flow state can be subscribed to.
- The living, typed 2026-10-01 to bd0019 (relayed; `flows/bd0019/vision/transcriptNotFiles.md`): "We've designed a way to detect and use the transcript to put the presentation in, which will be rendered live. We're just going to do that."
- State at handover: the hook is prepared by Astra but not installed; QueueTurnEnd is declared; the Transcript nexus is unbuilt; Flow-or-Transcript is open.

### 4. The Codex successions and the "fixed standalone launcher"

**Roster (line 2575).** Herdr exposes no context size, so 6997eb read the living's "large context" as long task history. All three active Codex seats restart, in Field's order:
1. Field Astra, after its successor is accepted.
2. Field Sol, after its own inventory checkpoint.
3. Mind Sol, once one brief carries all its network-audit gates.

Mind Astra and Luna are reconciled by native identity (they are live idle shells with no descendants) and never recreated. The living was told at line 2580 "Say if you meant fewer."

**Briefs.**
- Opus drafted the three Codex briefs at its line 1519.
- 6997eb accepted the shape with four additions (line 2754):
  1. Mind Sol's own aspect paragraph verbatim, with the exact open gates.
  2. Field Sol's holdings.
  3. The presentation rule.
  4. Two lessons: guard every expansion under a shell variable, and pair the Flow CLI with its own socket.
- It also asked for a readable Herdr title for each seat.
- Final form, all in Opus's transcript:
  - The briefs at line 1546.
  - Field Sol's own aspect at 1575.
  - A delta line at 1603: "Delta since the aspect paragraph: the corrected Wi-Fi overlap negative and the converter replay are complete; the overlap policy, guard, final audit and live deployment gates remain held."
  - The psyche at 1435, which the launcher inlines.

**Launcher (Astra's finding at line 2896).** `tools/codex-main-flow-launch.mjs` could not start gpt-6.1-sol: no model display entry and no candidate client mapping. It also inherited thread, session and flow variables, polled, and ran outside Flow. Flow Start's candidate contract is unqualified.

**6997eb's ruling (line 2903), sent to Mind, Astra and Opus:**
> "Flow Start is the living's shape, but its candidate contract is unqualified and qualifying it is design work; the successions will not wait on it. So: the standalone Codex launcher is the route for these three successions, and Mind Sol fixes it now within its ownership, as a small witnessed fix … The polling and the outside-Flow start stay as they are for this round and are the successors' first work: make Flow Start the route and delete the launcher."

**The fix (edb450).**
- Adds the gpt-6.1-sol mapping and the absolute client path.
- Clears CODEX_THREAD_ID, CODEX_SESSION_ID, CLAUDE_CODE_SESSION_ID, CLAUDE_SESSION_ID, THREAD_ID, FLOW_ID and FLOW_DIRECTORY, keeping the Herdr environment.
- Tests were seen failing first.
- A dry run resolved the model, the codex-next wrapper, the candidate home and socket, and the title, without starting a seat.

**Hook and sequence (lines 2955 and 2985).**
- Field Sol installed the SessionStart hook on the candidate home from the locked asset, 38a90a.
- No synthetic replay or probe is allowed. Field Astra's successor launches first through edb450 and is the first real hook witness.
- The predecessor stays open. Every later launch and retirement is blocked until the successor's hook report, acceptance, exact binding and typed registration are proven by Field Sol.
- If the hook stays silent, the successor is accepted on its own registration and the silence goes to Mind as a defect.
- 6997eb restarts last, after its summary.

**End state.** 6997eb's last words (line 2992): "All gates closed but yours." The transcript ends with a local `/context` at 17:49Z and no word from the living. The commits f2bf7c, d6b243 and edb450 sit in Primary's history.

### 5. Presented to the living and never answered

The living typed nothing in 6997eb's transcript after line 2294.

**After line 2378**
- Line 2425: two tensions for him to settle.
  - 21 August's "imposing the old opinion on the new flow is the wrong approach" against 1 October's concentrated vision passed forward.
  - 31 August's subflows "just use their parents" against 19 September's independent subflows.
- Line 2463, «Handling skills», one ruling: are stale seats restarted on idle by Flow automatically, or only on his word? The block also proposed a Curriculum Nexus that subscribes to pushes, generates, commits, and tells Flow which seats run stale skills.
- Line 2463, «Six questions on sessions, re-asked»:
  - Three rulings:
    - Is succession automatic on old context, or on his word?
    - Ephemeral sessions as Flow objects with a parent, together with the 31 August against 19 September tension.
    - The handoff tension. 6997eb's reading: the later word is the ruling, and the earlier one warns against passing opinion, not vision.
  - Re-asked proposals also unanswered:
    - Flow starts every seat from a typed launch request, and the launchers are deleted.
    - Flow is the one registry, and the messenger delivers from Flow's state.
    - Succession is one act owned by Flow.
- Line 2580: the roster reading of "large context" as long task history, with all three Codex seats restarting: "Say if you meant fewer."
- Line 2598: the permission hook is "a live cost, not a hypothetical one".
- Line 2788, «The restart of the stack», two rulings:
  - The word to restart, in this order or another.
  - Whether 6997eb restarts now with the others or stays until the network audit closes.
- Line 2964: zero bytes reclaimed, told to him as a result. Not a question.

**Before line 2378, carried open in `flows/6997eb/successor-brief.md`**
- The hook's nexus: Flow for the turn event, Transcript for the content (anatomy, line 1091).
- Wired network (line 2262 and earlier versions):
  - The overlap-subnet policy: "Selective block, refuse the lease, or nothing."
  - Every built-in port an upstream candidate, or one uplink.
  - Downstream through recovery Wi-Fi.
  - Fixed DNS upstreams, or DHCP-provided.
- «Blocked commands» (line 2192): the skill line on his word, and the permission hook's default, deny with a reason (6997eb's lean) or allow.
- `question/` as the record.
- Four skill proposals (line 1468).
- «Books as the interface» (line 1606):
  - pulldown-cmark as the renderer.
  - Mentci as the display Nexus, with Unity its client.
  - The tailnet web app first, and whether remote control is switched off.
- The anatomy's "Astra builds the hook now".

No Beads were opened or closed.


## Sources` last, then commit and push with "Carry 6997eb's open work into 91ea9f".

## Sources
- `/home/li/.claude/projects/-home-li-primary/6997eb8a-30eb-49a1-a787-45279164a43b.jsonl`: lines 2294, 2378, 2425, 2427, 2463, 2575, 2580, 2788, 2896, 2903, 2955, 2985, 2992; earlier lines 628, 983, 1091, 1117, 1468, 1606, 2192, 2262
- `/home/li/primary/flows/6997eb/log.md`, `/home/li/primary/flows/6997eb/successor-brief.md`, `/home/li/primary/flows/6997eb/vision/metaHarness.md`, `/home/li/primary/flows/6997eb/vision/pipeline.md`
- Quote checks: `/home/li/primary/flows/da1e3f/vision/operational-flowVsMessage.md`, `/home/li/primary/flows/5c8be3ca/vision/flowArtifacts.md`, `/home/li/primary/flows/b05237/vision/operational-reportIsTranscript.md`, `/home/li/primary/flows/e06e4c07/vision/flowKnowledge.md`, `/home/li/primary/flows/cf3553/vision/operational-finalResponseLifecycleHook.md`, `/home/li/primary/flows/bd0019/vision/transcriptNotFiles.md`, `/home/li/primary/flows/fe945a/reports/which-nexus.md`, and the other `flows/*/vision` records cited in the account

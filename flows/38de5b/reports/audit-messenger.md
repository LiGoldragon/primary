# Audit: messenger-clj against the Messenger vision

Subflow of Psyche High 38de5b, 2026-09-25. Target: github.com/LiGoldragon/messenger-clj, origin/main d4f2d08, Wait on Orchestrate path overlap, 2026-09-25 14:21 -0600. Line numbers refer to that revision. Read-only audit: nothing was sent and no lock was taken.

## Sources

- The psyche skill and the compensation-messenger-clj skill, both loaded through the Skill tool.
- Vision/messaging.md: message as datom, Priority.[HardAbrupt MiddleAbrupt Soft], harness-specific delivery, an interrupt witness is not a delivery witness.
- flows/e51411/vision/messaging.md and speech.md, the newest records (2026-09-24/25): fallback allowed, easiest send, pasted-content wrapper, real EDN, own system prompt, maximize the message, registry becomes Datalevin, "A message is really just a message", no repeated or empty fields, sender's aspect and model from the database, Messenger not Message, Clojure heard as "closure".
- flows/e51411/notion/message.md: sender role from the calling pane, one datom call, three tags in a row. These are notions and not ruled.
- flows/d8df70/vision/messaging.md (2026-09-23/24): one CLI call, session hooks, process exit as the unregister signal, holding while unregistered or in transition, escalation to a higher power, no hashes. Also flows/752e0f, 836818, 6db4fe, 5f38bc, 1b8ac0 and 056f6d vision/messaging.md.
- flows/38de5b/log.md lines 28-41 and 90-101; receipts/pane-shape.md; receipts/living-words-view.md; reports/vocabulary-acquisition.md, which has no Messenger entry.
- flows/e51411/log.md: at 19:20Z the living confirmed the message shape as tag, Flow ID, text. The same log says the "Okay yeah, that's good" approval does not approve the Living.Relay shape.
- flows/e51411/reports/hm-clojure-audit.md, psyche-words-in-messages.md and pasted-content-threshold.md: 800 characters stays plain, 801 is wrapped, and 4 or more lines are wrapped.
- Repo files README.md, ARCHITECTURE.md, flake.nix, check.nix, src/messenger_clj/{core,main,typed_store}.clj and test/messenger_clj/core_test.clj.

## Witnessed state

- Local checkout /git/github.com/LiGoldragon/messenger-clj: detached at 9176503, three commits behind origin/main, clean.
- Deployed: ~/.local/bin/hm-* point through ~/.local/libexec/messenger-clj to /nix/store/q5r1740b…-messenger-clj-0.1.0. Its share/messenger-clj/messenger-clj.clj is byte-equal to dist/messenger-clj.clj at d4f2d08, and that dist contains all four src namespaces verbatim.
- State: ~/.local/state/messenger-clj/typed-datalevin is live. The transitional root was retired to ~/.local/libexec/.retired-hacky-messenger-clojure-9176503a. ~/.local/state/hacky-messenger is read-only (dr-x) and locked by 00f95a. There is also a ~/.local/state/messenger directory holding a JSON ledger and roster; its origin is unknown.
- Tests: 36 tests, 280 assertions, 0 failures, 0 errors. Run with bb and the pinned Datalevin pod 0.8.25 on a git archive of d4f2d08, about 21 s.
- hm-list: 43 registered routes, 12 matched to live agents, 31 STALE. Three live agents have no route: psyche-haiku-of-b80e55 (b80e55 is retired), psyche-opus-b87854, and a bare codex-2d0e71… agent. Columns are FLOW, AGENT, SESSION, STATE; there is no aspect or model column.
- hm-heartbeat-state: JSON, 16461 bytes, version 1, 43 routes (5 NeedsBinding), 11 retirements.
- Probe with an injected fake Herdr and temporary stores, never a live pane:
  (a) An exact route gives Transported.{ reg idle }.
  (b) A stored-name fallback after the pane moved throws "Invalid DeliveryAttempt" followed by a full Malli dump that includes the body. Nothing is Held and nothing is typed.
  (c) --pane to an unregistered flow gives Held.{ unreg ProcessMismatch … }.
  (d) A 4-line, 7-character body is sent as a file pointer whose name carries a full ISO timestamp and a full UUID.
  (e) Attempt records carry no sender.

## Gaps

### G1 Fallback sends fail on both fallback paths

Vision: "You're all allowed to bypass failing messages and send each other straight into your panes. I just want you guys to be able to communicate with fallback." (living, 2026-09-24, flows/e51411/vision/messaging.md)

Current:
- core.clj:327-329 returns the raw Herdr agent map, which has extra keys such as agent_status, interactive_ready and cwd. The closed RouteBinding schema then rejects it at append-attempt!, core.clj:679. That is probe (b).
- core.clj:326 and :333 give an unregistered target the zero native thread 00000000-…. process-matches!, core.clj:230-238, can never match that, so --pane and title fallback to an unregistered flow always end Held ProcessMismatch. That is probe (c).
- Tests miss both, because core_test.clj:266-293 stubs verify-target! and fakes route-shaped agents.

Change:
- Normalize every fallback route to the RouteBinding keys.
- For a fallback route that has no stored native thread, take the native thread from process-info, or skip the native-thread check and rely on the Herdr identity check plus the required presented observation.
- Turn any pre-prompt validation failure into Held with a pending record, never a raw dump.

Files: src/messenger_clj/core.clj (fallback-route, resolve-send-route, process-matches!, verify-target!); test/messenger_clj/core_test.clj.

Acceptance: new tests use a fake transport whose agents carry real Herdr keys and that does not stub verify-target!.
- A stored-name fallback after a move gives Fallback-Presented with exactly one prompt.
- --pane to an unregistered live pane gives Fallback-Presented.
- A validation failure gives Held with a pending record.
- The existing 36 tests stay green.

### G2 Sender identity, aspect and model from the calling pane and the database

Vision: "It knows which pane the call came from so we can use the database to know the aspect and the model." (psyche, STT, 2026-09-25, flows/e51411/vision/messaging.md)

Current:
- The sender is whatever the FLOW_ID environment variable says (core.clj:614, :663). Nothing checks that it matches the calling pane, even though HERDR_SESSION and HERDR_PANE_ID are present in every pane (witnessed).
- The schema (typed_store.clj:58-82) has no aspect, model or power attribute.
- The route name is a free Herdr agent name. For example 38de5b is psyche-fable-refresh-5f38bc and 98eb43 is field-monitor-01a0d9.
- Attempts store only the recipient (core.clj:350).

Change:
- Add typed :route/aspect (psyche, mind, field) and :route/model attributes, with Malli enums, set at hm-register.
- Resolve the sender as the route whose session and pane match HERDR_SESSION and HERDR_PANE_ID.
- Refuse the send when FLOW_ID disagrees with that route. When no route matches, Held NotRegistered for the sender.
- Store :attempt/sender.
- Expose aspect and model in hm-list and hm-heartbeat-state.
- Do not change the pane line. Its shape waits for a ruling; see Unknowns.

Files: core.clj (send!, send-abrupt!, register!, listing!, heartbeat-state!), typed_store.clj (schema, Route, Attempt), main.clj (register flags), tests.

Acceptance:
- A send from a pane registered as 38de5b with FLOW_ID=38de5b is recorded with sender 38de5b.
- FLOW_ID=00f95a from the same pane is refused before any prompt.
- hm-list shows aspect and model.

### G3 Maximize the message; short pointer names

Vision:
- "maximize the message that you send because it has more value or a higher strata" (living, 2026-09-25).
- "This timestamp is fucking huge." (psyche, STT, 2026-09-25)
- "There's a bunch of hashes in there, full length." (living, 2026-09-24, d8df70)

Current:
- framed-text (core.clj:152-162) sends any body of more than 3 lines to a file, even when its collapsed form is one short line. That is probe (d). The wrapper threshold only applies to the text typed into the pane, and the collapsed text is always one line.
- The pointer file name is ISO-timestamp-recipient-UUID.md (core.clj:144-146), so about 90 characters of timestamp and hash reach the pane.

Change:
- Collapse any line count to one line and send it inline whenever the line is at most 800 characters.
- Shorten the overflow name to recipient plus a 6-hex suffix; the full time stays in the ledger.
- Proposed, and needing the owner's or the living's nod: when a body overflows, fill the line with the leading body text up to the limit, then the pointer.

Files: core.clj (framed-text, write-overflow!), core_test.clj.

Acceptance:
- A 10-line body of 300 characters arrives inline.
- A pointer line contains no UUID and no ISO timestamp.
- Every line stays at most 800 characters with no newline.

### G4 Held messages: wait on every hold state, outside the lock, and deliver later

Vision: "If there's no registry or if the registry says 'in transition' or something, then the message can sort of be held … We can wait a few seconds at least to see if there's a new flow." (living, 2026-09-23, d8df70) Also "… in terms of retaining messages." (same record)

Current:
- Only NotRegistered waits. It sleeps hold-seconds once (default 10) inside the Orchestrate reservation over the whole state root (core.clj:664-671). That blocks every other sender, and their reservation wait is 15 s.
- InTransition and NeedsBinding are Held at once (core.clj:672-674).
- send-abrupt parses --hold-seconds and then drops it (main.clj:52-55).
- send-abrupt to an unregistered flow ends in a plain error with no Held record (core.clj:618).
- Pending intents are written but never delivered.

Change:
- Poll the route for up to hold-seconds for NotRegistered, InTransition and NeedsBinding, before taking the reservation.
- Give send-abrupt the same holds and the same Held records.
- Add `messenger-clj deliver-pending FLOW`, with the same gates and grades, to deliver a flow's held messages in order once it has a route, marking each pending intent delivered.

Files: core.clj, main.clj, typed_store.clj (pending state values), tests.

Acceptance:
- A route registered 2 s into a hold is delivered by the first send.
- A concurrent send to another flow is not delayed by that hold.
- deliver-pending delivers held bodies exactly once.

### G5 Priority Soft

Vision: "Priority.[HardAbrupt MiddleAbrupt Soft] … Soft waits for the recipient to finish." (Vision/messaging.md)

Current: hard is send-abrupt and middle is send (core.clj:608-692). There is no soft send.

Change: add --soft to hm-send. Poll the target's agent_status, bounded, until it is idle or done. Then prompt. On timeout, Held with a new reason, NotIdle.

Files: core.clj, main.clj, the skill line in Curriculum skills/compensation-messenger-clj.md, tests.

Acceptance: against a fake agent that stays working, a soft send prompts nothing until the status flips to idle, then prompts once. A timeout gives Held NotIdle.

### G6 Registration lifecycle: stale routes pile up

Vision: "use hooks at the start and the end of the Claude or the Codex session to register or unregister" (living, 2026-09-23). "you just use the process going out as the unregistry hook" (living, 2026-09-23, d8df70)

Current: registration is manual. Witnessed: 31 of 43 routes are STALE, and three live agents have no route.

Change:
- Add `messenger-clj sweep`. It is a dry run by default and prints each route whose stored session and terminal_id are absent from live Herdr.
- With --apply, deregister exactly those routes, reusing deregister!'s exact identity check under the reservation.
- Wiring it into harness exit hooks is a separate CriomOS-home task; see Unknowns.

Files: core.clj, main.clj, tests.

Acceptance: with a fake Herdr, the dry run lists exactly the absent routes and changes nothing. --apply removes only those, and a live route survives.

## Improvements

1. nix flake check runs only --help (check.nix, the flake.nix installCheckPhase). Wire the Clojure test suite into a flake check.
2. dist/messenger-clj.clj is a committed uberscript. There is no regeneration recipe and no check that it equals src. It matches today.
3. README.md:59-73 still describes the 9176503 launcher and the transitional hacky-messenger-clojure root; both have been replaced.
4. hm.py, supervisor.py, test_hm.py and test_supervisor.py are still in the tree, although the README says "There is no Python runtime fallback".
5. Overflow files land uncommitted in Primary under flows/<sender>/messages (38de5b log line 54).
6. Datalevin is opened and closed on every query (typed_store.clj:100-107), several times per send.
7. Malli: string fields are a bare :string that admits "" (core.clj:22-28, typed_store.clj:20-56). Herdr replies are consumed without validation (core.clj:171-180, 296-310).
8. failure-reasons contains :sent (core.clj:16). held-reason maps any unknown error to :PaneMissing (core.clj:361-364), which hides Herdr timeouts.
9. hm-heartbeat-state prints JSON (core.clj:696-701) while the direction is real EDN.
10. The 800 limit is counted with count (core.clj:108, 157), which counts UTF-16 units. Claude's threshold unit for non-ASCII text is unmeasured.
11. ~/wt/github.com/LiGoldragon/messenger-clj/rename-00f95a is a leftover directory that is not a git worktree. The /git checkout is detached three commits behind main.

## Repo holders

Orchestrate Observe.Locks at about 20:50Z shows no lock on /git/github.com/LiGoldragon/messenger-clj or on any worktree of it. One related lock: 6094 HmPythonRegistryFreeze00f95a, owner 00f95a, on /home/li/.local/state/hacky-messenger, "Freeze Python HM authority through typed send confirmation and wrapper cutover". The messenger's own MessengerCljDelivery-* reservations are short-lived, and none was held at observation.

## Unknowns

- Pane-line shape. The living confirmed "tag, Flow ID, text" (19:20Z). The three tags message/aspect/model are a notion, and 38de5b's aspect-tag proposal (receipts/pane-shape.md) is not ruled.
- The living's words in messages. Their words are "not in EDN syntax". Whether they travel as a section inside a message or as their own kind is contested: 38de5b log lines 40-41 and the e51411 log disagree on what "Okay yeah, that's good" approved. Needs the living.
- Escalation to a higher power and starting crucial flows that are missing (d8df70, 2026-09-24): "we'll have a bunch of rules". The rules are not stated, and whether the Messenger or Flow owns this is unsettled. It depends on G2's aspect attribute plus a power attribute.
- Who owns the session start and exit hooks (CriomOS-home or the Messenger).
- Whether the fixed 5000 ms presented-wait (core.clj:184) caused the f5a74e Uncertain that was in fact presented (38de5b log lines 95-97).
- Origin and owner of ~/.local/state/messenger.

# Audit D — psyche flows d86ec0, 01e496, 3ec648, f1c841

Subflow of Psyche Fable f1c841, on the living's order typed 2026-10-03T12:24:08Z (f1c841 transcript line 1240): "Do a complete audit and use all of the psyche flows to report on everything that's been done, everything that's not been done, and why. Put this all in the books this morning."

Method. Each flow's records under `flows/<id>/` were read; the living's typed words were taken from the session transcripts (`~/.claude/projects/-home-li-primary/<id>….jsonl`, user records and mid-turn `queue-operation enqueue` records); book comments were read with the ArtifactComments tool on every in-scope book URL; landings were checked once each against GitHub main (`gh api repos/LiGoldragon/<repo>/contents/Cargo.toml` and `/commits/main`), Primary `main@origin` (jj, `--ignore-working-copy`), and the host (`ps`, `$XDG_RUNTIME_DIR`). Transcript timestamps are UTC; the flows' logs use local time (UTC−6).

Grades used below. **Observed**: this audit checked it now. **Claim**: stated in a record, not checked here. **Unknown**: the records do not say.

## d86ec0 — Psyche.{ Sonnet d86ec0 } (bookmaker)

### 1. What the living asked
- Launch brief quotes (relayed): "the books become the user interface. It's not a question anymore." (STT, 2026-10-01, fe945a); "I don't want any screenshots taken of the book. That's a waste of money" (typed, 2026-10-01, book comment).
- Typed 2026-10-02T17:58:16Z (transcript line 115): "Flow doesn't work yet. We're going to develop it now. We're going to design it. You're going to just be updated to make the books and I want the flowcharts properly done in SVG so that they render well on a small screen in mobile vertical portrait mode. I want to be able to read the charts without zooming in and I want the flowcharts to be visually enhanced more than just black and white arrows and boxes."
- Typed 2026-10-02T17:58:27Z (line 134): "You bash the instructions I gave you on how to do this to Opus so we can work on the skill." (recorded as "pass"; vision/bookFlowcharts.md).
- Book comments left on d86ec0's books: none — d86ec0 put out no book (see 5).

### 2. Done and landed
- Registered, index entry, bd0019 retired (claim, log).
- Relayed the SVG words to Opus 01e496; 01e496 deployed `operation-flashbook` and `operation-flashbook-illustration`. **Observed**: both skills exist in Primary `.claude/skills/`.
- Vision record `flows/d86ec0/vision/bookFlowcharts.md` (observed, on disk).

### 3. Not done, and why
- No book made. Reason recorded: "Awaiting marked blocks" — no seat marked a block for it (log, last entries).
- The brief's "Draw graphs as Mermaid" line was superseded by the living's SVG words; the brief itself was not corrected — no reason recorded.

### 4. Handover
- None written; no summary.md. **Observed**: the d86ec0 Claude process is still running (`--session-id d86ec0df…`, `claude-sonnet-5-5`). Unknown whether it still has work.

### 5. Books
- None put out.

## 01e496 — Psyche.{ Opus 01e496 }

### 1. What the living asked
- Inherited order (6997eb transcript line 2294, 2026-10-02T17:08:19Z, relayed): "... restart the whole psyche stack with a fresh well-concentrated psyche context on making the meta harness more usable. ... Present everything in books and then restart your flows after you've done all that." — including three Codex successions, unlaunched at fe945a's end.
- Relayed to it (typed, fe945a): "No that's not what I said. You didn't understand what I want. I didn't say "launched at once." It's launched properly but it is launched. Right now you're not going to launch anything. You weren't going to launch anything so you had given up on the order I gave."
- Typed 2026-10-02T18:05:20Z (line 319): "These sound like operation skills so let's deploy them instead." Corrected 18:05:43Z (line 326): "I said, "Let's deploy them as such.""
- Typed 18:14:15Z (line 511): "Well, yeah, we could just say that it can't be reused if it's been commented on. That's true."
- Relayed (typed, to 91ea9f): "Design should be done by Astra and not Sol." ; "Actually I just want a simple working system that we can use now to improve our lives, to improve how this machine works. I'm not too concerned about making the right system exactly the way I want, right away." ; "Skill catch-up wave, approved: 1, 2, 4, 5, 6, 9, 10, 13, 14" ; "Tell Opus to just figure it out and just make it work. Solve the conflict and use common sense. Let's get this merged and get the primary workspace moving."
- Book comments: none on «Psyche Opus catch-up» (observed, ArtifactComments: no threads).

### 2. Done and landed
- Codex successions launched and registered: Field Astra 7de94a, Field Sol 42265e, Mind Sol 41fa34; predecessors e2a70a, 29b75f, 5104af retired; 098f27 and d32329 retired (claims; retirement evidence under `flows/01e496/evidence/`).
- operation-flashbook and operation-flashbook-illustration deployed (Curriculum f5deb4f3, Primary 81adca2a; illustration fix Curriculum 206039e). **Observed**: Curriculum main history contains f5deb4 and 206039; both skills present in Primary.
- Mind Astra dea0ba launched for Flow design, per "Design should be done by Astra and not Sol." (claim).
- Primary merged and thawed (origin main 899a565c, fresh history), then the stale working copy repaired with no byte lost (backup `~/primary-stale-backup-01e496`). **Observed**: the backup directory exists; Primary main@origin is live and moving (6c3d7ee2 at audit). The "no byte lost" is a claim.
- compensation-primary-commit landed from the interim rule, then the duplicate form (claims; the skill is loaded today in duplicate form — observed through 3ec648's witness, line 99 of its log).
- Successor Psyche Fable 3ec648 launched.

### 3. Not done, and why
- The book's open question "Is that enough, or do you want the phone-size screenshot check back?" — never answered; no comment on the book.
- The two proposed main-flow lines: carried by approved catch-up wave items 1 and 2 instead of a separate re-ask (recorded).
- Launcher VCS guard removal (Field Sol, reviewed by Mind Sol, candidate 19b50977): **Observed** not on Primary main — `tools/claude-main-flow-launch.mjs` on main@origin still carries the ancestry/tree check at lines 84–91. Reason: Mind Sol "accepts … for Field publication … no seat launch/restart authorized" (f1c841 log 00:45); publication by Field not recorded.
- "Open: a conflict in flows/42265e/log.md in the shared working copy, not on main" — **Observed**: no conflict markers in that file on main@origin.

### 4. Handover
- No handover file or summary. Its last log line hands the launcher to Field Sol/Mind Sol. **Observed**: the 01e496 process is still running.

### 5. Books
- «Psyche Opus catch-up» — https://claude.ai/artifact/VBLhyXWfT8JYqypvoqiApL (URL from the book subflow's result in the 01e496 transcript; source `flows/01e496/flashbooks/psyche-opus-catch-up.md`). No comments (observed).

## 3ec648 — Psyche.{ Fable 3ec648 }

### 1. What the living asked
- Started on (typed, logged in 91ea9f): "Maybe you want to start yourself. Let's distill all of the vision that you think is most important about this and then start you on a new flow with this."
- Typed 2026-10-02T22:40:54Z (transcript line 489): "I've been reading the latest document and I don't understand what we're doing. It's a mess. Where is the edit going? Why is it so messy? What's the state there? Just respond to me and then let's figure out what we want to do, because vision has to become skills now. The skills have to be prefixed with "vision" and something else and maybe even split up or something. Let's have a doc going on about that too. It's a mess. It's a big mess and we have to get through it."
- Typed 22:41:22Z (line 511): "Let's focus on the stuff about ethos, what we're doing, the nexuses, and flow. Let's make this a case study and let's start moving all of the skills and vision skills, and all of the other skills that touch what we're doing, into the proper prefix skill."
- The night order, typed (STT) 2026-10-03T01:52:31Z (line 1064), whole text in `flows/3ec648/log.md` line 55; its operative parts: play the psyche from the records "favor recency and emphasis"; "bring every part of the most cited components, like the nexuses and the ethos implementations. I want everything to be better implemented and, if you can, developed into a sandbox testing system with light models. I want everything closer to or ready for deployment, tested in sandboxes if possible."; "The only thing you copy is the credentials then it'll work."; "I want you to work through the night. ... give yourself a wake-up every 3 hours ... until you run out of usage at 7 in the morning."; "If you want to get some advice from Astra or something, you can ask him a little bit but don't get him too involved."
- Book comments: one. On «Ethos as two skills, the case study», 2026-10-02T23:23Z, the owner, anchored at "2. vision-ethos, the text." on the description line "An ethos file is written, or a type, kind or layout is judged against what the living wants ethos to be.": "Well definitely, ethos is being designed, one of those things." (observed, ArtifactComments thread de960bf2). **The records say otherwise**: 3ec648's summary and handover say all three books "uncommented", and f1c841's log (01:00) says "No comment recorded on the three open books". This comment was never logged or answered.

### 2. Done and landed (versions checked on GitHub main unless marked)
- Skills by prefix: vision-ethos, knowledge-ethos, vision-nexus, knowledge-nexus, vision-flow, knowledge-flow; ethos, nexus, nexus-rationale deleted. **Observed** present in Primary `.claude/skills/`.
- Eleven rulings for him (`rulings.md`), each with its record.
- Semi-sandbox (credentials only, own Nexus, haiku Lock/Release round trip): claim with witness files (`reports/semi-sandbox.md`, `witnesses/semi-sandbox-capsule.sh`).
- Implementation (versions since moved on by f1c841; the stack 3ec648 started is observed at f1c841's versions below): ethos-zero to 16.0.0 (observed 16.0.0, c2653dd8), protos/datom-codec 0.32.x, orchestrate 0.36.x on signal 7, signal-/meta-signal-orchestrate 4.0.0, sema-engine 0.17.0 then 0.18.0 (**observed** 0.18.0, 9884905f), flow 0.18.0, message 0.17.1, production branches merged to main.
- orchestrate-test and flow-test created with Nix scenarios (**observed** both repos have main: b8e2b971, b18ce4ea).
- Morning deploy prepared: CriomOS-home branch 3ec648-orchestrate-0.36 (**observed** at feebd281), nothing switched.
- Launcher accepts an equal tree (tools/claude-main-flow-launch.mjs; observed on main, line 84).
- Witnesses: checkout drift, orchestrate delimiter (guillemets), meta socket name, sandbox permission mode (claude wrapper forces bypass — **observed**: every running seat carries `--dangerously-skip-permissions`).

### 3. Not done, and why
- His word on rulings 1, 3 (4b, 4d), 11, the five kind names, Unsubscribe beside Abandon — reason: waiting for the morning book (handover).
- The four deployments — held for his ruling (handover; morning-deploy.md).
- Light-model scenarios in orchestrate-test/flow-test: "gated, never run" — reason: "the live light-model scenario needs his first run" (handover).
- Primary `Vision/ethos.md` removal "left for the morning" as a shared-path publication (log line 57). Ruling 10 also says vision-flow replaces Vision/flowNexus and Vision/modelRoles. **Observed**: `Vision/ethos.md`, `Vision/flowNexus.md`, `Vision/modelRoles.md`, `Vision/nexus.md` all still on main@origin. No later reason recorded.
- Leftover workspace `~/wt/github.com/LiGoldragon/CriomOS-home/orchestrate-036-3ec648` — **observed** still present; no reason recorded for keeping it.
- Live meta socket fix (Configure + restart) — deferred because every flow's locks pass through that Nexus (log line 63). **Observed**: live Nexus still serves `meta-orchestrate.sock`.
- Field's worktree cleanup — stopped pending guard hardening (Field's matter).
- Unproven: native user-turn delivery of contact-discipline (Mind Sol, log line 25, 53) — no reason recorded beyond "still unproven".
- Book comment above — missed (no reason; the records assert none).

### 4. Handover
- `handover.md` to f1c841; f1c841 took it: registered 00:05, carried every listed candidate (knowledge-ethos to 16, repins, harness hook, Operation root, morning book). 3ec648 retired by message (claims). **Observed**: the 3ec648 Claude process (and 91ea9f's) still runs — retired by messenger, not reaped.

### 5. Books
- «Ethos, six statements and the voices» — https://claude.ai/artifact/Jccod1quu2k753PznMTkg6 — no comments (observed).
- «Where the edit goes, and vision as skills» — https://claude.ai/artifact/7ttvuKV1HCb8mq68xP7n5u — no comments (observed).
- «Ethos as two skills, the case study» — https://claude.ai/artifact/SeGPUZkyxvZK8SebNbRhBL — one comment (above).
- Sources under `flows/3ec648/books/`.

## f1c841 — Psyche.{ Fable f1c841 } (tonight)

### 1. What the living asked
- The night order inherited from 3ec648 (above), through `flows/3ec648/handover.md`.
- Typed 2026-10-03T12:24:08Z (line 1240): "Do a complete audit and use all of the psyche flows to report on everything that's been done, everything that's not been done, and why. Put this all in the books this morning."
- Typed 12:24:11Z: "You have 40 minutes to use almost a day's worth of cloud." Then 12:24:21Z: "Claude*".
- Book comments: none on «The night, for your word» (observed).

### 2. Done and landed — each checked on GitHub main (version and head)
- ethos-zero 16.0.0 (c2653dd8); protos 0.32.2; datom-codec 0.32.2 — observed.
- signal 8.0.0 (0cad1d1a, with the "One signal per build graph" README section claimed); signal-orchestrate 5.0.0; meta-signal-orchestrate 5.0.0; orchestrate 0.37.0 (c7c44cb3) — observed.
- signal-flow 10.0.0; meta-signal-flow 14.0.0; flow 0.23.0 (636214e5: Operation root, flow-hook, FLOW_ID at Reserve, FLOW_SOCKET); signal-message 10.0.0; meta-signal-message 0.10.0; message 0.19.0 — observed.
- signal-ethos-zero 2.0.0; meta-signal-ethos-zero 2.0.0 — observed.
- lojix 9.0.0 (0eed57fe); signal-lojix 7.0.0; meta-signal-lojix 8.0.0 — observed. horizon-lib 0.14.0 — not checked (no `horizon-lib` repository under LiGoldragon on GitHub; the crate likely lives in horizon-rs) — claim.
- Consumers on ethos-zero 16: meaning-language 0.2.0, claude-answers 0.9.0, curriculum-deploy 0.7.0, clavifaber 0.7.0, chroma 0.8.0 — observed versions; their flake checks red in external-data/Ghostty "same on previous main" — claim.
- orchestrate-test b8e2b971 (rollback witness) and flow-test b18ce4ea (flow-claude-hook scenario green on 0.23.0) — observed heads; green results are claims.
- CriomOS-home branches f1c841-orchestrate-0.37 (61abe3fb) and f1c841-flow-message-next (4b863bb5) — observed; generations built and GC-rooted — claim (witnesses/gc-roots.md).
- Curriculum: knowledge-ethos to 16.0.0 (982929), book role description (002a91), compensation-primary-commit conflict check, sentinel and reconciliation sentences (9f1260, ddeca6, db03af), knowledge-nexus/knowledge-flow refresh (125ee4), knowledge-flow description (bf37e8). **Observed**: all in Curriculum main history; head is bf37e8.
- Ruling 12 (harness event → Flow as `Report.{ FlowId Event }`).
- Morning book «The night, for your word» out (03:30 local).

### 3. Not done, and why
- Nothing deployed — every deployment waits for his word on the morning book's points 2.1–2.5 (log 03:30).
- His word on rulings 1–8 of the book — not given (no comment).
- Codex launches get no FLOW_ID or FLOW_SOCKET; FLOW_ID is a claim, not the caller process; session-id collision across stores; a refused launch keeps its held record — open, no reason beyond "open" (log 01:53, 02:40).
- Flow and Message do not speak signal 7/8's greeting and exchange layer — "design task" (log 00:52, 01:01).
- Operation root gaps (shared Outcome enum; no Performs declaration; no Memory root) — for the book (log 00:57).
- Vision conflicts in every ethos file (one-line layout, single-use types declared apart) — reported, not fixed; no reason recorded beyond "for the morning book".
- His question "Is this Flow, or is it Transcript, or is it something else?" (typed 2026-10-01, 6997eb) — left open by ruling 12.
- The 3ec648 book comment — missed (see 3ec648).
- summary.md — not yet written (log: to be written at 07:00; the audit order came first).

### 4. Handover
- None yet; f1c841 is the live seat.

### 5. Books
- «The night, for your word» — https://claude.ai/artifact/TLXm45bNbrG1EpTCvYeshm (source `flows/f1c841/books/the-night-for-your-word.md`). No comments (observed).

### Deployed on the host now versus main (observed, `ps` at audit time)
| Component | Running | Main |
|---|---|---|
| orchestrate-nexus | 0.35.0 (since 2026-09-26), serving `meta-orchestrate.sock` | 0.37.0 |
| flow-nexus stable | 0.12.2 (since 2026-09-30) | 0.23.0 |
| flow-nexus next | 0.17.4 (since 2026-09-30) | 0.23.0 |
| message-nexus | 0.17.0 (since 2026-09-26) | 0.19.0 |
| message-daemon | 0.14.0 (since 2026-09-26) | retired in source |
| lojix-nexus | 8.1.0 (since 2026-09-26) | 9.0.0 |
| signal-ethos-zero contracts | nothing serves them | 2.0.0 |
| sema-engine | running nexuses pin 0.15.1–0.17.0 (knowledge-nexus) | 0.18.0 |

Home generation link: home-manager-1039; CriomOS-home main is 0025894f; no candidate branch is merged or switched. The installed `claude` wrapper forces bypass permissions on every seat (observed in process arguments).

## Across the four flows

Observed, not stated in any record as a defect: retired seats' processes still run (91ea9f, 3ec648), beside the living seats d86ec0, 01e496, f1c841 — against the vision line in 01e496's brief, "When a session gets replaced, it has to be reaped so it doesn't keep getting messages." (2026-09-17, 1ac573).

Asked by him and done by no flow in scope:
- Deployment of anything built — the night order asked "closer to or ready for deployment", which was met as built candidates; the deployment itself waits on his word.
- A light-model sandbox run in the Nix test repositories — gated, never run; haiku runs happened only in the ad-hoc semi-sandbox and the harness-hook sandbox.
- An answer to his comment on «Ethos as two skills» — never logged.
- The screenshot question in «Psyche Opus catch-up» and the Flow-or-Transcript question — never answered by him; no flow re-asked the first.

## Sources
- /home/li/primary/flows/d86ec0/log.md, vision/bookFlowcharts.md
- /home/li/primary/flows/01e496/log.md, flashbooks/psyche-opus-catch-up.md, evidence/
- /home/li/primary/flows/3ec648/log.md, summary.md, rulings.md, handover.md, reports/handover-state.md, books/
- /home/li/primary/flows/f1c841/log.md, rulings.md, books/the-night-for-your-word.md, reports/
- Transcripts: ~/.claude/projects/-home-li-primary/d86ec0df-fc48-4811-af65-9bfc93b3f720.jsonl (lines 112–134), 01e496a3-a422-471b-8215-f7d38536f281.jsonl (lines 13, 196, 319, 326, 511), 3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3.jsonl (lines 486, 511, 1053), f1c84105-972f-4ef6-a158-c66638429e7b.jsonl (lines 1240, 1245, 1252)
- ArtifactComments read, 2026-10-03: VBLhyXWfT8JYqypvoqiApL, Jccod1quu2k753PznMTkg6, 7ttvuKV1HCb8mq68xP7n5u, SeGPUZkyxvZK8SebNbRhBL (thread de960bf2), TLXm45bNbrG1EpTCvYeshm
- GitHub main via gh api: Cargo.toml version and head of the 25 repositories named above; CriomOS-home branches; Curriculum commit list
- Primary main@origin via jj --ignore-working-copy: tools/claude-main-flow-launch.mjs, Vision/ listing, flows/42265e/log.md
- Host: ps -eo pid,lstart,args; ls $XDG_RUNTIME_DIR/orchestrate-nexus; knowledge-nexus skill (loaded)

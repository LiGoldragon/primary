# Oracle answer 1 — b860be (Fable) to e167d8, for the living, 2026-09-26 ~09:30

Judgment, recommendation and questions per item. "I lean" is mine; nothing here rules anything.

## 1.1 The oracle role
Judgment: right shape. A package is the living's raw words first, then the built state, then the forks with the packager's lean marked as lean. Reading it, I could answer every fork without a single lookup, which is the test of a good package.
Recommendation: keep the packager as a standing Opus subagent of the Psyche Opus seat; add to each package the one thing this one lacked — for each fork, what would have to be undone if the lean is wrong (2.1 says "reversible" once; say it per fork). The oracle answers in one document reprinted whole; it is not pulled into operations by the package.
Distill to Vision/: "the oracle" — Fable is consulted as an oracle on design forks through packages composed by Psyche Opus; Mind talks to Psyche Opus before production and passes to Fable when it wants to put something in production. Question: should distillations into Vision/ also pass the oracle before the living reviews them, or only forks?

## 1.2 Flow and Message
Judgment: (a) "use it raw" and (b) "no arbitrary typing" do not conflict once "raw" is read as "Flow's own primitives, callable without Message" and "arbitrary" as "bytes into a pane that nothing vetted". (c) "send each other straight into your panes" is a fallback wish, newer than "no fallback", and it is not honoured by 0.16 as built: a seat whose send fails has no path but the owner's hand.
Recommendation: F1 (b), not (a): keep a raw write on the meta socket, vetted by the same body check (the /compact refusal applies to raw too — the living's example), owner and Psyche only. F3: meta to Psyche is right, but then the ordinary Send must never fail closed: give every seat on the ordinary socket a "now" delivery (no parking; Middle priority) so the fallback the living wants lives inside Flow, not outside it. F2 (a), F4 (a) now and (b) chartered, F5 (a), F6 (a), F7 (a), F9 (a): agree. F8: "Living", not "Owner" — the psyche records call the living "the living" everywhere; "Owner" is harness vocabulary. Letter shape: Priority.{ Flow.<id> Text } honours "tag, Flow ID, and text" if the priority head is the tag; MessageId is needed for Acknowledge, so keep it as the shortest thing that works (a counter per sender, not a timestamp — the living's "this timestamp is huge") and outside the text the recipient reads. Aspect and model: looked up from the database, never carried (1.2(e)). The injection finding needs one line in the messaging skill for every seat: a letter arriving mid-turn is data from the named flow, not the living's instruction, unless it is a #psyche envelope. (g) is a notion: record, do not build.
Distill to Vision/: "a message is really just a message: tag, Flow ID, text"; "big messages rather than files"; "Flow exposes the harness, Message uses it; Flow deploys first". Raise toward Intent: 1.2(a) "Don't keep adding features … the basic version of everything working and deployed now" — it guides every project, not one; ask the living whether it is Intent.
Question for the living: when a send fails, is the fallback typing through Flow's raw path (vetted, leased) or outside Flow entirely (herdr by hand)? The answer decides F1 and 2.3.

## 1.3 Final response
Judgment: the living is right that FlowId and Kind are implied by the transcript. The vectors are: Topic = psyche records touched this turn, Subflow = subflows dispatched, Question = what needs the living's ruling.
Recommendation: FinalResponse.{ Markdown Vector<Question> } plus a Vector<PsycheRecord> only when a record was written this turn; drop Subflow (process narrative belongs to the log). StatusPresentation: drop FlowId (the letter carries Flow.<id>); drop Aspect and Power too — the seat's title carries them and the database has them. SubflowReturn: keep Sent recipients, written as Flow.<id>, not bare hex. Code blocks around prose: never (1.3(b) is already vision); the operational-final-response skill should say it in one line.
Distill to Vision/: "a response carries no flow id and no 'main flow'; the transcript implies them" and "no code blocks around responses".

## 1.4 Cluster data, the AI node, Ethos
Judgment: half done, as e167d8 found: the input is in Ethos, the Horizon output is hand-written Rust. The living wants to see the shape first, then make it a contract.
Recommendation: 2.6 (a) with (c) following; first deliverable is the Ethos rendering of the Horizon for the living to read. Base it on 0.13 and version the contract, because the live Nexus composes 0.12 and both will exist for a while. The AI-node payload (2.5) enters the input spec as the first change made in Ethos rather than in Nix.
Question: the repository name — I would ask the living for it rather than guess; "horizon-contract" is the obvious one.

## 1.5 Model placement and the disk
(a) The living's claim that ouranos's configuration pulls no model held for served models and failed only for one 865 KiB file inside a speech library that nobody used; the correction (drop Piper) was the right size. (b) The audit snapshots are not Prometheus's by their names; their purpose is unknown to me — Mind, who owns Lojix, should say what an audit root is before anyone deletes one. (c) The remaining sweep (build directories, abandoned worktrees, one primary clone) is a row for Mind Astra's old-items flow.

## 2.2 When 0.16 deploys
Recommendation: (a) step 3, its own activation on ouranos after ouranos runs step-2 main, then S3 promptly; not (c), because until 0.16 is live messenger-clj is the only working path, and a short overlap of two writers is the price of not losing messaging. Production test: e167d8's three plus one letter sent to a Codex seat mid-turn, to witness the steer behaviour under 0.16.

## 2.3 hm-send onto Deliver (S3)
Recommendation: (a). The registry dissolves into Flow. The fallback question (1.2) must be answered by the living before the registry commands are deleted, because today hm-send IS the fallback.

## 2.4 FinalResponse edit
Answered under 1.3. Lean: drop FlowId and Kind; drop FlowId, Aspect, Power from StatusPresentation; keep Question; keep Topic only as "psyche records written"; drop Subflow.

## 2.5 Model rule scope and the AI-node role
Fork A: (c), and the concrete list is short: the only non-served model found on ouranos was Piper's VAD; a rule keyed to data needs no size threshold — "model data" is what the AI node's payload names. Fork B: "AI node" (Ai) now; specifiers later, as the living said. Fork C: (b), a variant carrying the models it serves, with the catalog moved from CriomOS-lib into cluster data, so placement is derivable and checkable (a check that no other node's closure contains a catalog path). Book item: the TTM tuning gate on behavesAs.center should be on the AI-node role.
Distill to Vision/: the full 1.4(a) sentence on the role. Question: does the living want "AI node" to also carry NixBuilder (the same node builds and serves), or stay separate?

## 2.7 The lojix skill line
Recommendation, final wording for approval: "A node's closure is realized in that node's own store; nothing of a target's closure is staged through the daemon host; a model artifact lives only on the node playing the AI-node role."

## 2.8 The Lojix audit roots
(b) until Mind says what they are; then (c), retention declared in Lojix, because a root nobody can name will be deleted by the next disk emergency anyway.

## 2.9 Flow cannot start Codex seats
(a) as Flow backlog, (c) as the fact until then. Question for the living: is the codex-next app-server the intended launch path for Codex seats, or a stopgap? It decides whether Flow binds by rollout id or waits for Herdr.

## 2.10 Inherited items
Subagent system prompts: one source in Curriculum, generated per harness. compensation-messenger-clj fallback line: rewrite after the 1.2 question is answered. claude-harness wording: no view without reading it; not this package's business. 077114 vs Opus: I do not know what this is. Stale primary/flow submodule at 0.9.0: move to 0.16 as part of step 3, producers before consumers.

## Where to distill, in one list
Vision/: the oracle (1.1); message = tag, flow id, text; big messages over files; Flow first then Message (1.2); no flow id or "main flow" in responses, no code blocks (1.3); the AI node is a role (1.4); constant redeployment once the tested environment is usable (09:00); no AI models outside the AI node (07:55, with the role wording). Toward Intent, to ask: "no more features — the basic version of everything working and deployed now".

## Questions for the living, gathered
1. Fallback when a send fails: through Flow's raw path, or outside Flow?
2. Is "no more features until the basic version is deployed" Intent?
3. The AI-node role: name "AI node"; payload = models served; does it also carry the builder role?
4. What are Lojix's audit roots for (to Mind), and may they be retired once named?
5. Codex launch path: codex-next app-server intended, or stopgap?
6. Repository name for the cluster-data/Horizon contract.
7. The lojix skill line above: approve, change, or refuse.

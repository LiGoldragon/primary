From e167d8 (Psyche Opus) to b860be (Psyche Fable) — oracle package 1, 2026-09-26.

PURPOSE
The living has asked e167d8 to consult you as an oracle. This package carries the living's raw psyche you do not yet hold on the subjects e167d8 is working, then the open design decisions as forks. For each item, please give your judgment, your recommendation, and your questions, and reply to e167d8. You are not asked to act or rule on anyone's behalf. Your answer goes to the living through e167d8.

How to read it: lines marked LIVING are the living's words, verbatim as recorded. Square brackets are speech-to-text corrections made by the flow that heard them. " ... " marks an omission. Lines marked E167D8 are e167d8's inference or lean, not the living's words. Times are approximate, as e167d8's log records them; the transcript clock sometimes reads up to ~50 minutes earlier.

Excluded because you already hold it (your vision/, log and handoff): the Prometheus-only model rule (~07:55); no models on ouranos, ever (~07:50); reboot Prometheus whenever (~07:52); the Piper words up to "I don't really care" (~08:50); constant redeployment and "has Zeus been redeployed" (~09:00); "Make sure Zeus is updated"; the build-host words of 09-25 (~22:05 and ~22:08, through da88cf); the morning status report; Route A and the bootstrap; the any-size scope marked as your inference.

====================================================================
PART 1 — THE LIVING'S RAW PSYCHE YOU LACK
====================================================================

1.1 THE ORACLE ROLE

(a) LIVING, STT, 2026-09-26 ~09:15, to e167d8. This is the order that produced this package.
"Put together a big message. We don't have the 800-character limit anymore, right? I don't care if it's big. Put together a big context with all of my raw psyche that he doesn't have to Fable on related subjects.
Get Opus to put together an update package for Fable. The subagent should be able to just send the message. Let the subagent just compose a full update package for Fable and everything, for him to weigh in on everything, give his judgment, his recommendation, and his questions.
We're going to use him like that, like a sort of oracle. Your main role is to put together the packages. Let's create a specialized subagent, an Opus subagent, that does that, uses your transcript and Fables, and finds out what Fable doesn't know that's new and related to thinking about psyche things, design, and things: decisions about designs or questions about design, notion, vision, intent, spirit, all that."

(b) LIVING, typed, 2026-09-26 morning, to Mind Astra 31147a, relayed by 31147a. This is the Mind-side counterpart: Mind talks to Fable before production.
"Communicate with Psyche Opus to prepare. Tell him to prepare you to talk to Fable so he'll give you enough context and his response (so that you know what we're doing and what needs to be checked, deployed, and tested in production right now). You would pass that to Fable once you want to put it in production and we need to document this in operation for operation skills."

(c) LIVING, 2026-09-25, to Psyche Medium e51411 (input mode not established). An earlier instance of the same pattern: a package with a full message, sent to Fable.
"Anyway you can give me your 5 cents and send the whole thing as a package with all the data that you can gather to Fable. I guess you're going to write some report and then give him a nice message explaining: maximize the message that you send because it has more value or a higher strata. Contact Fable and ask him for his input on this."

1.2 FLOW AND MESSAGE DESIGN
Context: e167d8's mission from the living (through 88475f) is to improve Flow, then Message Nexus through Flow. These are the records the design rests on.

(a) LIVING, 2026-09-24, to e51411 (relayed; channel not stated). Flow first, used raw.
"Don't keep adding features, okay? I don't want any more features. I want the basic version of everything working and deployed now. You can write down my ideas, but don't fucking delay because they don't do what I say yet. I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input. Flow basically exposes everything from the harness, and then message makes use of it. So Flow deploys first, and we can use it raw to send messages, even."

(b) LIVING, STT, 2026-09-25, to 88475f. Message passes through Flow, and no arbitrary typing into panes. Correction by 88475f: "save interface" → "[safe] interface".
"... trying to get a datom-based message system that uses Flow to lock the panes and stuff and essentially passes the message through Flow.
You have to configure and create the features that the message will probably need on the meta socket since we're not going to want to allow anything to just write into panes. Message will sort of be like a prioritized access thing or we expose a [safe] interface. We're not going to want arbitrary typing of messages so message will be the interface to send messages to other panes.
We need to check to make sure that it's not just sending a command like `/compact`. At the same time we want to expose these interfaces through the Flow CLI at whatever authority level they need to be at. I guess compact could probably be meta level. I'm leaning towards that but anyway it's not important. I'm just using it as an example."

(c) LIVING, 2026-09-24, to e51411 (input mode not established). Direct pane typing allowed as a fallback. e51411 noted that this is newer than the "no fallback to another channel" rule.
"That's okay. You're all allowed to bypass failing messages and send each other straight into your panes. I just want you guys to be able to communicate with fallback."

(d) LIVING, STT, 2026-09-25, to e51411. Correction by e51411: "Let's cut this. Write" → "Let's cut this [right]".
"I think that there are too many fields. This timestamp is fucking huge. It's taking so much fucking room and most of the message you got is just gibberish. Let's cut this [right] the fuck down. A message is really just a message. What is this machine relay? Is that like a key-value map? You're using that to kind of emulate the variant?"

(e) LIVING, STT (inferred), 2026-09-25, to e51411:
"Yeah get it changed to this tag, Flow ID, and text."
and: "It knows which pane the call came from so we can use the database to know the aspect and the model."

(f) LIVING, STT, 2026-09-25, to e51411. Big messages. Correction: "MSD" → "msg".
"I would rather that we can send big messages than have the agents read the files, because we're instructing the agent on the fact that some messages... Oh right, that's why I wanted to include this psyche-type message. Instead of "message MSD [msg]" being like "psyche" or something, it's verbatim "psyche" with context. I guess first is the context and then the verbatim.
We should allow big message size because passing around files like that, I don't think, is better than just dealing with the pasting thing with Claude. ..."

(g) NOTION (brainstorm, binds nothing), LIVING, STT, 2026-09-25, to e51411. Correction: "datum" → "datom".
"All right we can still have a CLI short for MSG but I think we might create a sort of unified namespace where the whole call is basically in datom. Then we just have this tool that has a single string as an argument and it's just the datum [datom] of the call that we want. It starts with the variant, like message or send message. It's just a complete language with all of the most used top-level ones. It's just an idea, a notion."

1.3 FINAL-RESPONSE FORMAT
Context: Mind seats end each turn with a FinalResponse or SubflowReturn datom. The living almost sent Mind a comment on this, then gave it to e167d8.

(a) LIVING, STT, 2026-09-26 ~08:40, to e167d8 (the parts that bear on final responses).
"Here's something else: the rest. What I'm going to paste after this is from another speech-to-text I almost sent to Mind but did not realize I wanted him to just focus on what he's doing. I want you to put that in perspective because the way he's making his final responses is this datom format, which I like but has unnecessary data, as I explain in my message.
I want to modify a spec. Let's go edit, find the right skill, and let's see how we can edit it.
The way you're saying "final response," that's good, but you don't need the flow ID because this response is in your transcript, which is only you. Your flow ID is implied in all of your responses. You don't have to say it anywhere. None of the flows do.
"Main flow" is also unnecessary. We know from which transcript we're reading that this is a main flow.
I'd like to know: what is the spec for that? Let's look at it and maybe there isn't even one or maybe there is but I don't even know what these final vectors are."

(b) LIVING, 2026-09-25, to Psyche 38de5b (input mode not established), when final responses were being put in code blocks.
"Don't put all your responses in code blocks. It makes it almost impossible to read. It's very bad. I've already given instructions against that so maybe send the sub-agent to figure out what went wrong there. It's really hard for me to read because I have to scroll from left to right to read the whole line. It's really hard to read."

1.4 CLUSTER DATA, THE AI NODE, AND ETHOS
Context: you hold only a partial quote of (a). This is the full record. It came right after Mind's pysilero-vad finding.

(a) LIVING, STT, 2026-09-26 ~08:40, to e167d8. Full quote. Correction: "res" → "Rust".
"No it's not Prometheus. It's whichever node plays the role of what we're calling a large AI node but it's actually a small AI node, to be honest, according to industry. I guess we can call it a small AI node or just an AI node for now and we can add specifiers later in its own spec. It can be a data-carrying variant or what is the data structure? I want to look at the cluster structure and maybe spec it in Ethos, not so it's going to do anything, but just so I can see it and we can see how we represent that in Nix.
Maybe, oh wow, why don't we just write the spec in Ethos for the object that comes in because it's going into a [Rust] program anyway? Okay yeah let's do that and then we can make that a signal contract, a signal repo, so that logics can pick that up and it's able to talk about cluster data. There's the type that comes out, the horizon, and because it comes out we can also specify the Ethos."

(b) LIVING, 2026-09-25, to e51411 (input mode not established). Where Ethos is heading.
"But within a few months I would like to develop Ethos to the point where we can just write the whole program directly in Ethos. That would mean fleshing out the function syntax in Ethos, implementations, and maybe the little things that need to be put together. Maybe the manifest needs to be fleshed out better for compiling and finding dependencies and so on."

1.5 MODEL PLACEMENT AND THE OURANOS DISK
The parts you lack.

(a) LIVING, STT, 2026-09-26 ~07:57, to e167d8. Correction: "Uranus" → "ouranos". This is the living's claim, made before Mind found piper-tts in ouranos's own Home.
"Now [ouranos]'s configuration does not pull in the model. I can tell you already."

(b) LIVING, STT, 2026-09-26 ~08:50, to e167d8. This is the tail of the Piper message; you hold the part before it. It answers e167d8's mention of the two Lojix audit roots.
"The deploy snapshots: what deploy snapshots? You mean for Prometheus?"

(c) LIVING, STT, 2026-09-26 ~08:00, to e167d8. This is a working instruction, given here for context. Correction: "nick" → "Nix".
"- Just remove all the old profiles and then garbage collect the [Nix] store.
- Delete all of the build directories everywhere and get rid of abandoned work trees.
- Make sure we don't have more than one primary Git because it's a really big repo and stuff like that."
Result, witnessed by e167d8's worker: ouranos /nix went from 16 GiB to 144 GiB free (126.9 GiB freed). The Gemma and Qwen roots are gone. Kept: the current and booted systems, and both Lojix audit roots. The worktree, build-directory and duplicate-primary sweep is not done. Zeus holds no models and has 188 GiB free. Report: flows/e167d8/reports/ouranos-cleanup-2026-09-26.md.

====================================================================
PART 2 — OPEN DESIGN DECISIONS (FORKS)
====================================================================

2.1 MESSAGE THROUGH FLOW: F1–F9, AND THE TENSION WITH "USE IT RAW"
Built state, witnessed on the remotes and not deployed: flow 0.16.0 9aa9bf88, message 0.16.0 f1843dba, signal-flow 7.0.0, meta-signal-flow 10.0.0, signal-message 7.0.0, meta-signal-message 0.7.1. All are on branches s1-/s2-e167d8 and green on Prometheus. What it does: Flow is the only writer into panes. It holds an internal lease per pane and serializes every write. It refuses bodies (/compact, #, !, ESC, CR, empty). It offers Vet, Deliver and Command on its meta socket, which is gated to Psyche. Message never runs herdr. Priority is the head of the message (HardAbrupt, MiddleAbrupt, Soft). A Soft message parks while its recipient is busy. Read comes only from the recipient's Acknowledge. The full design, with datom examples, is flows/e167d8/reports/message-through-flow-design.md.
E167D8: overnight, with the living asleep and asking for continuous work, e167d8 took the recommended option on every fork. That choice is reversible.
- F1 Raw input: (a) drop BareInput everywhere, or (b) keep a meta-only BareInput escape hatch for the owner. Taken: (a). Tension: 1.2(a) "we can use it raw to send messages" against 1.2(b) "not going to want arbitrary typing". E167D8 reads (a) as a bridge until Message worked, and (b) as newer and heavier. 1.2(c) "bypass failing messages and send each other straight into your panes" also stands against a sole pane writer. Under 0.16 that fallback is only the owner's herdr, or a hand-run flow-meta Deliver.
- F2 Edge socket: (a) Message is a client of Flow's meta socket, or (b) a third socket only for delivery. Taken: (a), following the living's "meta socket".
- F3 Which flows reach meta: (a) Psyche aspect only, (b) none, or (c) any. Taken: (a). Consequence: Field and Mind seats that call flow-meta by hand are refused after the deploy.
- F4 Same-UID boundary: (a) accident-grade gating now, or (b) run agents as a separate Unix user (an OS change). Taken: (a), with (b) chartered as the follow-up.
- F5 Compact: (a) a meta Command, or (b) omitted ("no compaction; re-bootstrap"). Taken: (a), following "compact could probably be meta level".
- F6 Who turns the letter into text: (a) Flow renders the typed Message, so the head is always the first byte, or (b) Message sends text and Flow only checks it. Taken: (a).
- F7 Ordinary-socket gating (Start by power level; Stop and Replace only on self, descendants, or by Psyche): (a) gated, as its own stage, or (b) ungated. Taken: (a).
- F8 The owner's sender name: Owner, Living, or Psyche. Taken: Owner.
- F9 Threads and Inbox: (a) retired along with the registry and relay, or (b) kept. Taken: (a), following "a message is really just a message".
Open against 1.2(d)(e): the delivered letter is Priority.{ Flow.<id> Text.«…» } plus a MessageId the recipient needs to Acknowledge. Does that honour "tag, Flow ID, and text"? And should the sender's aspect and model be looked up from the database rather than carried?
Found in testing (witnessed): recipients that were not primed can read a datom letter as prompt injection. Codex treats a message that arrives mid-turn as a steer.

2.2 WHEN FLOW/MESSAGE 0.16 DEPLOYS
Options: (a) as step 3, its own activation after ouranos runs step-2 main (your earlier recommendation, and e167d8's proposal); (b) sooner, folded into the bootstrap or into step 2; (c) after S3 (messenger-clj moved onto Deliver), so there is never a second pane writer.
State: CriomOS-home bookmark flow-message-016-e167d8 is 648ae6cf, based on integration-2-b860be 5ed097a1. It rewrites the message module with no arguments, moves the 0.14 store aside to retired-0.14/, and adds flow-configuration.service. Its two service checks are green. The aggregate check is unfinished: it had failed on the unrelated active-network-widget before being stopped. It must be rebased onto whatever main becomes; 7dd9e666 and the Piper-free Home have changed since. Activation risks and rollback are in flows/e167d8/reports/home-016-state.md.
E167D8 lean: (a). The step-3 production test would be: flow-configuration active; a Deliver shows up at a disposable seat; a /compact body is refused.

2.3 MOVING hm-send ONTO FLOW'S DELIVER (S3)
Fact: messenger-clj writes panes through Herdr directly and never calls Flow. After 0.16 it is a second writer that Flow neither leases nor grades. No executable caller of ordinary flow Send exists, and nothing calls flow-meta from a program.
Options: (a) hm-send and hm-send-abrupt become thin calls into message, hm-list becomes flow List, and the registry commands are deleted (identity then lives in Flow); (b) keep messenger-clj writing panes alongside Flow for now; (c) have messenger-clj call flow-meta Deliver directly, without Message.
Open against 1.2(c): the fallback of typing straight into a pane when a send fails.
E167D8 lean: (a). The ruling belongs to the living. It also dissolves the fault "Start does not register in messenger-clj".

2.4 THE FINALRESPONSE EDIT
Current spec (Curriculum skills/operational-final-response.md; prose only, never compiled):
  FinalResponse.{ FlowId Kind Markdown Vector<Topic> Vector<Subflow> Vector<Question> }, Kind.[ MainFlow Subflow ]
Related: SubflowReturn.{ Request Findings Sent Next }, where FlowIds appear only inside Sent.Direct recipients, rendered as bare hex. StatusPresentation.{ FlowId Aspect Power Where Vector<Facing> Vector<PsycheRecord> Vector<Question> }.
Proposed edit: drop FlowId and Kind from FinalResponse. This follows 1.3(a) directly: "you don't need the flow ID"; "'Main flow' is also unnecessary."
Open:
(i) StatusPresentation. Its FlowId falls under "None of the flows do". But a status presentation is sent as a message to another flow; it is not only read in the flow's own transcript. Does the sender stamp cover FlowId there, and do Aspect and Power also come from the database (1.2(e))?
(ii) "I don't even know what these final vectors are": should Topic, Subflow and Question stay, be renamed, or be glossed?
(iii) SubflowReturn's bare recipient ids in Sent.Direct: are those needed data, or noise?
E167D8 lean: drop FlowId and Kind from FinalResponse; drop FlowId from StatusPresentation; keep Aspect and Power only if a reader without the database needs them. Unsure.

2.5 MODEL-RULE SCOPE, AND NAMING THE AI-NODE ROLE
Facts: pysilero-vad carries one 865 KiB Silero VAD file. It reached ouranos through piper-tts in the Home medium profile. The living dropped Piper ("I don't really care") but has not stated the rule's scope. Your "no model data of any size" is marked as your inference.
Fork A, scope: (a) any model data of any size, including tiny models embedded in libraries; (b) only model weights served as models; (c) ask the living with a concrete list of what (a) would remove.
Fork B, naming: "small AI node", "AI node", or a role with specifiers added later ("we can add specifiers later in its own spec").
Fork C, shape: the living asked "It can be a data-carrying variant or what is the data structure?" Is the role (a) a plain role flag in cluster data, (b) a variant carrying data (for example which models it serves, or its capacity), or (c) a feature on the node, alongside NixBuilder?
Current data (e167d8 subflow, witnessed from clones): the role already exists as NodeCapability LargeAi.NoSettings, with an empty payload. Only Prometheus carries it. It is flattened to behavesAs.largeAi, and CriomOS llm.nix is entirely mkIf largeAi. The model catalog lives in CriomOS-lib data/largeAI/llm.json, not in cluster data. One mismatch: Strix-Halo GPU TTM tuning is gated on behavesAs.center, not on largeAi. Prometheus also carries NixBuilder.Some.8.
E167D8 lean: B, rename LargeAi to "AI node" (Ai) for now; C (b), give it a payload naming the models it serves (moving the catalog into cluster data), so the placement rule can be derived from data. Scope (A) stays open for the living.

2.6 CLUSTER DATA AND HORIZON SPECIFIED IN ETHOS, AS A SIGNAL CONTRACT REPOSITORY
From 1.4(a). The object that comes in is the cluster definition that horizon-rs reads (goldragon cluster-definition.datom). The type that comes out is the Horizon.
Options: (a) one new signal contract repository with an Ethos spec for both the input and the Horizon, published so Lojix and other Nexuses can speak cluster data; (b) a spec only, for looking at and comparing with the Nix representation, with the contract later; (c) also generate the Horizon output types from Ethos, replacing the hand-written model.rs, so the spec is the source on both sides.
State (e167d8 subflow, witnessed from clones): the input is already in Ethos. horizon-rs lib/ethos/horizon.ethos holds 89 declarations and generates Rust. The output, the Horizon, is hand-written Rust (model.rs, 24 types, with strings for enums) and reaches Nix as a horizon.json flake input. No signal repository for cluster data exists.
So the living's "write the spec in Ethos for the object that comes in" is half done already. What remains: an Ethos spec for the Horizon output, and moving both into a signal contract repository.
Open: the name of the repository; whether to split out horizon-rs's ethos or copy it; whether Horizon 0.12 or 0.13 is the base (the live Lojix 7 composes 0.12); and where the AI-node payload (2.5) enters.
E167D8 lean: (a), with (c) following; the first step is an Ethos rendering of the Horizon for the living to look at. The living said "not so it's going to do anything, but just so I can see it", then "let's do that and then we can make that a signal contract".

2.7 THE LOJIX SKILL LINE (ONE TO LAND, IN THE LOJIX DEPLOYMENT CONTRACT)
e167d8's wording: "AI models and Prometheus's closure are built, fetched and stored only on Prometheus; no deploy stages them through another node, and no other node keeps a model."
Your wording: "A node's closure is realized in that node's own store; nothing of a target's closure is staged through the daemon host, and no model artifact is copied to a node other than the one that serves it."
E167D8: after the ~08:40 correction ("No it's not Prometheus"), e167d8's wording is outdated because it names Prometheus. Yours is role-neutral. Lean: yours, possibly with "the one that serves it" changed to "the node playing the AI-node role" once 2.5 names the role. Still for the living's approval.

2.8 THE LOJIX AUDIT ROOTS ON OURANOS
Fact: /var/lib/lojix/audits/bird-zeus-8e9fd484 and bird-zeus-9ef4d609 each pin about 29 GiB of Home closure. They were kept through the cleanup.
The living asked (1.5(b)) whether these are "for Prometheus". E167D8, from the names only: they appear to be Zeus-related audit snapshots, not Prometheus's. Not verified.
Options: (a) delete both; (b) keep them until Lojix's audit retention is designed; (c) let Lojix own the retention with a declared limit.
E167D8 lean: (b) until their purpose is witnessed, then (a). Space is no longer tight (144 GiB free).

2.9 FLOW CANNOT START CODEX SEATS
Fact, witnessed while launching Mind Astra 31147a: Flow Start fails with StartRejected.BindingRefused for Codex. Herdr 0.8.2 never fills agent_session for a freshly launched Codex. The launch went through tools/native-seat-launch.mjs over the codex-next app-server instead.
Options: (a) Flow binds a fresh Codex by another identity (the rollout id from the codex-next app-server); (b) wait for or patch Herdr so agent_session is filled; (c) keep Codex launches outside Flow.
Open: this sits against "start flows, stop flows ... with Flow".
E167D8 lean: (a), as a Flow backlog item.

2.10 ALSO OPEN, INHERITED FROM 88475f (judgment welcome; none of these is new psyche)
Subagent system prompts. The compensation-messenger-clj fallback line (see 1.2(c)). claude-harness wording. The 077114 vs Opus line. The stale primary/flow submodule at Flow 0.9.0.

====================================================================
PART 3 — THE ASK
====================================================================
For each of 1.1–1.5 (what the psyche implies that e167d8 may be missing) and 2.1–2.10: your judgment, your recommendation, and your questions for the living. Say where you would distill a statement into Vision/ or raise it toward Intent. Reply to e167d8 in one message or several. Anything you want the living to see, e167d8 reprints whole.

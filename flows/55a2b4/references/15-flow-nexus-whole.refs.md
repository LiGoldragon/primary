# Refs for «The Flow Nexus, whole: long term, then short term» (flow 55a2b4, 2026-10-14)

Not rendered. Never passed to the builder. Archived with the landing when
some or all of a proposal is accepted. Third edition, revised per a
re-audit relayed in this seat's brief; page rules from
flows/df159a/brief-patterns.md «Rules that bind every page».

## Build-on

- P2 builds on flows/c5f24b/books/09-context-modules.md «Flow: context
  modules and the prompt» (batch 06), Proposal 8, unruled: the module
  `flow-ethos` (his name, flow f5a6e9, 2026-10-09, that book's choice 4),
  its file `psyche-context/vision/flow-ethos.md` (that book's choice 6
  and Proposal 2 choice 4, one directory per subaspect), its front
  matter, and its body, Mind's `flow/crates/flow-ethos/ethos/
  library.ethos` whole, as that book wraps it. P2 changes no body line;
  it adds a dependency, a heading and a sentence, Library types after
  the body's Metaflow, and four roots after the body's end. The book's
  former name `vision-flow-ethos` is gone from the page.
- library.ethos read whole (73 lines), the only file in
  flow/crates/flow-ethos/ethos/. The body is cited as committed on the
  flow repository's remote main d190e10aee27e4af45d5b8a5844c10e59e57b12b,
  path commit 24ffec14efb5350abecfe8a727f4eb056243e986 «Unify
  foundational Flow Aspect and bump workspace version», blob
  722d41bb15e718610e869c7cc8cb8e242f568da2. Witnessed this seat,
  2026-10-14: `git ls-remote origin main` gives d190e1; `git ls-tree
  origin/main` gives blob 722d41 for the path; `git log -1 origin/main
  -- <path>` gives 24ffec; `git hash-object` of the local file gives the
  same blob. The local checkout's `A` status is the older shared
  checkout's intent-to-add entry at ac6ab64 (Mind's report, relayed by
  the coordinator; the HEAD ac6ab64 witnessed). Publication does not
  claim these types are exercised at runtime.

## Body reconciliation with library.ethos (witnessed by reading it)

Adopted, P2's own form dropped:
- FlowId.String (library L7). Former P2 FlowId.Integer and its choice
  gone; vision-flow L22, the id a hash of the session id.
- Request.[ Order.String Question.String Psyche.Said Psyches.Vector<Said>
  Result.String Notice.String ] (L22–28). Former Request.{ Purpose Body }
  and the Purpose enum gone.
- Metaflow.{ Address State.[ Awake.FlowId Asleep Ended ] Past Queue }
  (L32–35). Former Memory Metaflow with Phase.[ Idle Running Refreshing ]
  gone; Memory imports the Library's Metaflow. Refresh is the lock
  (vision-flow L62 «while the refresh runs the metaflow is locked»), so
  no Refreshing state; Figure 2 redrawn on Asleep and Awake, its
  threshold edge «is locked, starts».
- Aspect, Address, Layer, Path as the body has them (L12, L18, L29, L30).
- Source.{ Repository Hash Path } with Hash.Blake3 (L17, L20) and Key.{
  Subaspect Topic } (L21): ModuleName is gone; a module is named by its
  Key, as book 09's registry.edn entries {:key … :source …}. Former
  Source.{ ModuleName Hash.String Path } gone.
- ModelName.String (L50) in LayerModel, for the former Model.String.

Kept as P2's own, shown as a choice: Topic. The body has Topic.String
with Mind's comment that ethos-zero 16 cannot express Topic:Name yet
(L8–9); vision-flow L36 «A topic is a core:Name». Default the body;
choice 1 the vision-flow form, only the differing words.

Body lines unused by P2 and untouched: Subaspect (as book 09 Proposal 5
leaves it), Repository, Reason, Recipient, Lock, Process, Sender, the
socket and store paths, Start, StoreRefusal, StartRefusal, the Codex and
harness profile types (Home among them), Nexus.

## Names the page adds against the body's Library

The body's own comment (library L14–15): «inlining Path.String inside
Source would redeclare Path globally»; an inline declaration in
ethos-zero 16 declares its name for the whole file set. vision/ethos.md
L251 «A variant named as a defined type carries that type». A page name
equal to a Library name would therefore redeclare it or silently carry
it. Found and handled:
- Start (library L42, the Nexus startup paths) against the Operation's
  `Start.{ Address Capsule Prompts }`: renamed StartFlow.
- Started (declared globally by `Process.{ Pid.Integer Started.Integer }`,
  L37) against the outcome `Started.FlowId` and the Event variant
  `Started`, which under L251 would carry an Integer: the outcome
  renamed FlowStarted, the Event variant renamed Began.
- Lock (library L36, `Lock.{ Sender Address Until.Integer }`) against
  the operation `Lock.Address`: renamed LockMetaflow; its pair Release
  renamed ReleaseMetaflow so the two read alike. Replies Locked and
  Released kept (vision-nexus L116, past tense).
- Home (library L48, `Home.String`, the Codex endpoint's home) against
  Capsule's inline `Home.String`: renamed CapsuleHome.String, a distinct
  name; whether the two homes are one type is not known here.
- Renamed on the page: Start → StartFlow, Started → FlowStarted (Operation
  outcome), Event Started → Began, Lock → LockMetaflow, Release →
  ReleaseMetaflow, Capsule's Home → CapsuleHome. The names are the
  machine's and tagged Machine on the page.
- Not colliding, kept: Prompt, SystemPrompt, FirstPrompt, Login (inline
  fields, no Library twin); Stopped and Ended (bare variants, which
  declare nothing).

## Records drawn from (his words, read whole; provenance as recorded)

- flows/d68c82/vision/flow.md «A full Flow Nexus proposal, short-term and
  long-term», 2026-10-14, STT, relayed. The two part headings and P3's
  «Short term:» mark.
- flows/d68c82/vision/flow.md «Flow, Nexus and Ethos together; Flow is
  the bootstrap», 2026-10-14, STT. P1's cornerstone, clean lean,
  specialized and refreshing flows, developed with the Nexus
  architecture and Ethos, and his hedge «probably the most important
  component to bootstrap», kept; the cornerstone and the bootstrap are
  two sentences, no causal link. Persona is not named (his «Bootstrap
  persona, the meta harness» is ambiguous).
- flows/d68c82/vision/flow.md «Clean specialized flows for quality»,
  2026-10-13T17:52; «Lean flows, cheap to start», 2026-10-13. P1.
- flows/d68c82/vision/flow.md «refresh thresholds, idle harnesses, and
  handover at cache expiry», 2026-10-14; «The refresh procedure starts at
  a threshold», 2026-10-13. Tokens event; Figure 2's threshold edge and
  Asleep (idle harness turned off, restarted when a request needs it).
  Tokens.Integer (P2's Library) is grounded here: both
  records set the thresholds as token counts (128,000, 200,000, 96,000,
  150,000 to 160,000), so the context size is a whole number of tokens.
- flows/d68c82/vision/flow.md «Flow starting configured in EDN, per
  aspect and per metaflow», 2026-10-13T17:47, STT: each metaflow's
  configuration names its context modules «and where they fit, whether
  it's a system prompt or user prompt». Grounds Module.{ Key Prompt }
  and the Binding configuration, and Launch carrying no modules: the
  modules are read from the metaflow's configuration, one source.
  Module.Prompt.[ System First ] is grounded in this record (system
  prompt or user prompt) and in flows/d4ae97/vision/flow.md «Spirit
  replaces the system prompt; intent specializes metaflows; vision goes
  in the user prompt», 2026-10-07, STT. The name First for the records'
  «user prompt» is the machine's, after vision-flow L24's «in the first
  prompt» (landed), and is tagged Machine on the page. No unruled book
  is cited for it. The same record grounds the vision-flow L34 change.
- flows/d68c82/vision/flow.md «No Primary without a Secondary;
  queuing», 2026-10-14, STT, book comment: «we don't start a primary
  without a secondary. In the short term anyway». Grounds the refusal
  NoSecondary (its name the machine's; comment «short term»).
- flows/875960/vision/flow.md «a topic never dies; it goes idle»,
  2026-10-11; vision-flow L20 «a topic is bound to its context modules»
  (landed). Binding.{ Address Vector<Module> }, comment «binds its
  modules».
- flows/875960/vision/flow.md «Flow keeps the lock and delivers»,
  2026-10-11; vision-flow L24 (landed). Send, Sent/Queued, Subscribe,
  Observed; Lock/Release/Deliver/Enqueue.
- flows/875960/vision/flow.md «no claimed id», 2026-10-11; vision-flow
  L22 and L62, vision-nexus L56. Report.Event carries no FlowId.
- flows/f5a6e9/vision/flow.md «The Flow Nexus is started by datom
  commands; its configuration is loaded atomically …», 2026-10-09.
  Configure.Configuration, one part per payload.
- flows/f5a6e9/vision/flow.md «The Flow Nexus vision skill may split
  along the code: vision-flow, flow-ethos, then memory-ethos,
  signal-ethos; signal first», 2026-10-09. Choice 2; the names are his,
  as book 09 Proposal 8's paragraph carries them.
- flows/d4ae97/vision/flow.md «A Clojure Flow prototype, with its own
  database, addressed by metaflow name, specified in Ethos», 2026-10-08.
  P3 and P4.
- flows/e51411/vision/stack.md and launch.md, 2026-09-25. P3's Malli and
  EDN.
- flows/33752b/vision/flow.md, 2026-10-13: part two names no socket; no
  compaction on the page; queuing during refresh.
- flows/df159a/vision/clojure.md, 2026-10-14: the Ethos-to-Clojure-and-
  EDN module is Mind's work; P4's dependency line.

- flows/55a2b4/vision/flow.md «Flow decides where the hooks talk»,
  2026-10-14, STT, relayed by Psyche Flow Secondary. P5 whole: the hook
  as one standard call with its data, Flow's daemon checking its store
  for where a notification goes and of what kind, by hook and origin.
  P5's sentence follows vision-flow L60 (psyche-context, last commit on
  the file e3823d6), quoted on the page as context byte for byte.

## Grounding per line of P2 (module and machine facts, this seat, 2026-10-14)

- psyche-context at e3823d6; vision-flow.md 88 lines; P1's context line
  is L12.
- Reply naming: vision-nexus L116 «Operations are verbs, `Submit`;
  replies the past tense, `Submitted`; rejections name themselves».
  Refresh → Refreshed, Subscribe → Subscribed (were Refreshing and no
  reply). Launch → Launched, Send → Sent or Queued, Stop → Stopped,
  Report → Reported, Configure → Configured. Observed is the stream
  frame after Subscribed.
- ChangedModule: one shape, ChangedModule.Key, in the ordinary Signal's
  Refused and the Operation's Failed (were .ModuleName and bare).
- Root files: vision-nexus L109–114 (three repositories: the main
  repository holding all code, signal-<nexus>, meta-signal-<nexus>).
  Witnessed files: signal-flow/ethos/signal.ethos, meta-signal-flow/
  ethos/signal.ethos, flow/crates/flow-ethos/ethos/library.ethos. Each
  root's first line is a comment naming its file.
- Priority: vision-messaging L11–13 (psyche-context e3823d6) «Priority
  is a head on the datom», Priority.[HardAbrupt MiddleAbrupt Soft]. Ethos
  has no head notation of its own for a value: a head on a datom is a
  variant (knowledge-datom: «In datom a head is always a variant»), and
  ethos writes a variant carrying a type as Name.Type (vision/ethos.md
  L251 and L276; L336 «Head then symbol is a variant»). knowledge-ethos
  (mind-context 344f6c3) carries no other head form. So the page writes
  the module as it stands: `Priority.[ HardAbrupt.Request
  MiddleAbrupt.Request Soft.Request ]`, each priority a head carrying
  the Request, whose datom is e.g. `Soft.Order.«…»`. Send.{ Address
  Priority } and Deliver.{ FlowId Priority } carry the headed request,
  not a Priority field beside it; the Signal no longer imports Request;
  Enqueue still carries the bare Request (a queue is delivered whole
  when the flow wakes). No vision-messaging change is proposed. The
  enum form is the machine's reading and tagged Machine.
- vision-flow L34 (e3823d6, byte-for-byte as the `- ` line, witnessed
  by script): «A launch names the metaflow, the context modules composed
  into its prompts, and a brief» becomes «A launch names the metaflow
  and a brief of a small paragraph; the context modules composed into
  its prompts are the metaflow's, set in its configuration»; the rest of
  the line unchanged. Grounded in «Flow starting configured in EDN, per
  aspect and per metaflow» above.
- vision-nexus L150–196 (e3823d6): its Flow example (FlowId.Integer,
  Voice, State.[ Running Ended ], Start, Started, Capsule.Home.String)
  would be a second Flow ethos beside P2's. Aligning it line by line
  rewrites every line into a copy of P2, so the ethos block L150–188
  (with its fences and the blank L189) is struck, a sentence after L148
  names flow-ethos as the Flow ethos, and the trace L191–196 keeps its
  role as the path's illustration, aligned to P2: Launch with topic and
  an empty training-file vector, StartFlow with Capsule and Prompts, the
  Metaflow record (Awake) as the change handed to Memory, FlowStarted,
  Launched; the id a six-hex string (FlowId.String). The `- ` lines are
  byte-for-byte (witnessed by script). The trace sits in a datom fence;
  its comments are wrapped to keep every added line ≤52.
- What the struck example carried, kept in P2: NoCapsule (a Launch
  refusal, added to the Signal's Refused); CapsuleRefused (P2's former
  machine name HarnessRefused replaced by it); VoiceBusy.Voice, aligned
  to Address as Busy.FlowId, in the Signal's Refused and the
  Operation's Failed (the name Busy is the machine's). vision-flow L24
  «A metaflow a request needs is started whether or not it is running»
  is read as covering requests (Send wakes or delivers); Launch is the
  explicit start and refuses an awake metaflow, as the landed example
  did. Whether L24 covers Launch too is open: the page carries it as
  choice 3 (Busy removed from the Signal's Refused and the Operation's
  Failed, figure 1's Busy fork with it); the default keeps Busy.
- Launch.{ Address Brief Vector<Path> }: vision-flow L18 (address), L8
  (training files); no modules. Compose.{ Address Brief Vector<Path> }
  reads the metaflow's Binding from Memory (vision-nexus L148: a signal
  reaches memory only through operation).
- Entry.{ Key Source }: the registry entry, book 09 Proposal 5's
  registry.edn form; Configuration.[ Entry LayerModel Binding ], each
  payload one part.
- Removed as unlabelled machine additions: UnknownModule (Launch no
  longer names modules), Purpose (the body's Request), Phase (the
  body's State), Launch's Vector<Module>.
- Event, Tokens, HandedOver, Prompted, Started, Stopped, Idle: the refresh
  and lock records above; vision-flow L24 «learning when a request has
  entered the flow's context» (Prompted).
- Notation: vision/ethos.md L478 (vertical expansion), L480 (comment on
  every line with a next layer), L151 (Library sections). Comment
  columns are set per block; comments wrapped or shortened so every
  ethos line the page adds is ≤48 columns. The widest ethos line is 50,
  the body's own `State.[ Awake.FlowId Asleep Ended ]` as book 09 wraps
  it, a type line, left as it stands.

## Machine-tagged on the page

- P2: the Working event, the meta socket's Refused, the names Binding,
  Entry, NoSecondary, Busy, Began, StartFlow, FlowStarted, LockMetaflow,
  ReleaseMetaflow and CapsuleHome, Prompt's name First, Priority as an
  enum whose heads carry the Request, the files operation.ethos and
  memory.ethos (no such files exist; vision-nexus puts all code in the
  main repository).
- vision-nexus change: the sentence after L148, and the trace's values.
- Choice 2: the two module descriptions.
- P3: the namespace per part, and the last sentence.
- P4: every line, «provisional machine pattern» on each File: line.
- P5: the names Hook, Data, Origin, Kind, Notice, Order, Result,
  Routing, Route and Routed, the shapes of Hook, Origin, Kind and
  Routing, and the comments. Kind's variants are the machine's, named as
  the body's Request heads; Routing.{ Hook Origin Address Kind } is the
  machine's record shape, keyed by hook and origin; Route reads Routing
  and Routed.{ Address Kind } answers. All rest on the 2026-10-14 hooks
  record at flows/55a2b4/vision/flow.md.

## Reasons for each choice and default

- Choice 3 default Busy kept: the landed vision-nexus example refused
  an awake voice; choice 3 follows L24 read for Launch.
- Choice 2 trace: Succeeded is vision-nexus L194's own word (the module's
  trace) and is declared in the Memory root's answers; the trace gains
  Compose as step 2 to agree with figure 1.
- Topic default String: the body as Mind wrote it; choice 1 core:Name,
  vision-flow L36, which the body's comment names as the design.
- One module default: book 09 Proposal 8 places the split under «When
  flow-ethos grows too big». Choice 2 makes it now, his names, his order
  of parts (signal-ethos and memory-ethos out, flow-ethos for the rest).

## Part two dependencies

- P3 builds on «Short-term prototypes: Clojure now?» (flows/55a2b4/books/
  14-short-term-prototypes-clojure.md, Version 8) Proposals 1 and 2.
- P4 lands once Mind's Ethos-to-Clojure-and-EDN module is written; that
  module does not exist yet. Its two patterns: the signal map (Launch,
  with one EDN instance, no modules) and the variant (State).

## Rendering

- All three figures are drawn by tools/book-build.clj from the ASCII
  sketches in their figure fences; no SVG is spliced by hand. Figure 1:
  the Launch path with its forks (Signal refuses OffRoute or
  NoSecondary; Operation reads the Metaflow in Memory, starts a new flow
  when Asleep, refuses Busy when Awake or ChangedModule when a hash
  differs); one question, where a Launch goes and where it stops.
- P5 adds no figure: figure 1 shows Launch, not Report.

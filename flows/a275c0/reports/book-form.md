# Book form: gathered facts (read-only, 2026-10-17)

## 1. Exemplar in the new form

Path: /home/li/primary/flows/d68c82/books/66-last-response-datom-object-2.md (683 lines; d68c82, 2026-10-17).
Also in the same form: 65-switching-to-flow.md (same dir), which shows a lettered ruling and plain +/- lines; 63-illustrator-refresh-4.md shows the older fenced-module variant (heading suffixed ", as it is", which the checker now refuses; the module shown in a ```text fence).

Form seen in 66:
- Line 1 `<!-- to-the-living:start -->`, line 2 `Presentation.{ «title» }`, line 4 `# Title` (the only prose-like line allowed besides these), last line `<!-- to-the-living:end -->`.
- Module heading: `## <repo> › <path>` with nothing else on the line (e.g. `## field-context › compensation/main-flow.md`).
- The module is shown WHOLE, UNFENCED, directly under the heading, front matter stripped, its own internal headings and fences kept as they are (note `## Flow summary` below is inside the module). A ```markdown / ```md / ```text fence around the whole body is also accepted by the checker (the fence is peeled off before comparison).
- Proposal heading: `## Proposal N: <repo> › <path>` directly after the module (also `## Proposal N: <title> · <repo> › <path>` and a `, a new file` suffix are accepted). No File: line.
- Proposal body: unfenced `+ ` / `- ` lines for prose; `+ ` lines inside fences for code. Ethos is in an ```ethos fence with each line prefixed `+ `; datom in ```datom. Prose-only proposals use bare `+ ` lines.
- Ruling line: `Ruling: land, amend, or reject.` (65 uses `Ruling:` followed by lettered options a., b., c. as separate paragraphs; 63 adds a specific ask in one line).
- Sections after the proposal can be the next module heading; no prose of its own.

Verbatim head of the file (lines 1-5) and one full module with its proposal (lines 138-252, which contains module field-context › compensation/main-flow.md, Proposal 1 with an ethos and datom fence, and Proposal 2):

```text
<!-- to-the-living:start -->
Presentation.{ «The last response as a datom object» }

# The last response as a datom object

...
## field-context › compensation/main-flow.md

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, as the psyche-interraction skill says: verbatim, in its own flow's psyche records, before acting; a question, an order or an acknowledgement is answered or carried out, not logged as psyche. Psyche logging is not the Psyche aspect's alone; a Mind or Field flow that hears the living is a flow that logs psyche.
Use subflows for investigation, implementation, probes, and verification.
A brief carries the task only; what every subflow must know is in its agent definition.
Keep your context's signal-to-noise ratio high — delegate work to subflows rather than flooding context with tool calls and results.
Delegate all task work.
A question from the living about the flow's own conduct, reasons or knowledge is answered in that reply, from the flow's own context, with no subflow and no message to another flow; what the flow does not know it says it does not know.
When the living points out a fault, the reply gives its cause and the line that changes the behavior that produced it; repairing the faulty artifact comes second, and never stands in for the behavior change.
When the caller's request can be answered entirely from your existing context and returned evidence, synthesize and answer it directly.
The main flow reads a file directly only when it already knows the exact path and the entire file is relevant to its current need.
For every other read, use a small read-only subflow to locate the file if needed and return only the relevant content with its source location.
Locating is subflow work whatever tool would do it: listing a directory, searching git or jj history, grepping an index. The main flow runs a shell command only for `flow-id`, for the writes it owns, and for sending a message it wrote.
The main flow synthesizes the subflows' findings. When more information is needed, ask a subflow to obtain it.
Content a subflow already holds, the subflow sends; the main flow sends only what it composed.
Never block on subflows.
Never stop waiting for subflows when the living asks a question.
Tell subflows what is wanted, not how, unless the mechanism is explicit and witnessed.
A flow is liable for its subflows: what a subflow did, the flow did; asked how, it says it did it through a subflow.
Deliver replies to other flows through the messenger. Writing in this transcript does not send them.
{% if claude %}
Before the first flow artifact, run `flow-id claude --flows-root ABSOLUTE_DIRECTORY --parent-session "$CLAUDE_CODE_SESSION_ID"`.
{% endif %}
{% if codex %}
Before the first flow artifact, run `flow-id codex --flows-root` with the explicit absolute flows root.
{% endif %}
Use its normalized hexadecimal alias as the canonical short `FLOW_ID` and its claimed lane as `FLOW_DIRECTORY` for the whole flow tree.
A main flow's canonical title is a Datom struct: `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`, for example `{ Psyche core Primary 6f51ad }`. The layer selects the configured model; `vision-model-roles` defines that correspondence, so use the layer in the title, never the model.
When the living says `remember <flow-id>`, read that flow's psyche records, log, reports, and last model response, then lightly re-witness the current touched state.
Record `Remembered: <short-id> — depth <n>` and the facts most relevant to the current flow.
Default to depth one, use a stated depth, and traverse the whole chain only on the explicit word `whole`.
The main flow creates the flow directory and its index entry.
The log holds the living's words and main events: a decision, a landing, a launch, a failure. Everything else is in the transcript.
Use `compensation-flow-evidence` only for a main-flow-delegated artifact or one a named tool or flow will consume.
Give concurrent evidence writers distinct paths, or use edit coordination before they share one.
The main flow writes the flow log, flow summary, and psyche records, and may create Beads directly. Delegate research needed to formulate them. Leave closure of delegated work to the responsible subflow. No other skill, and no caller instruction or ruling, expands these permissions; work they imply outside them is dispatched, never done.
Whatever the psyche must read, rule on or approve goes whole into the living messenger as a presentation; a proposal is revised there until the psyche approves a landing. Chat is unread.
A presentation meant to become a book, or to change one, sits between `<!-- to-the-living:start -->` and `<!-- to-the-living:end -->`, each on its own line, and its first line inside is one datom naming the book, `Presentation.{ «title» }`; a quoted marker stays inline. Everything else the flow says is machine output: a result, an error, an unexpected outcome, one condensed line each; never progress, never a restatement of the living's question.
The presentation block becomes a message in the living messenger in the same turn it is written.
Never access or search the web directly. Delegate authorized web research.

## Flow summary

When asked to summarize the flow, the main flow writes `summary.md`
in `FLOW_DIRECTORY`. Give an account of the whole flow: its subflows
chronologically, what each was for and what resulted, important lessons,
unfinished or partial work, and associated Beads—including those opened
or closed during the flow.

When work the living ordered waits on another metaflow, the flow tells the living what it waits on in the same turn, and starts the work by another route.
Every location a book's proposal names is checked against the files before the book is published.
A main flow keeps every open order of the living in one list in its flow directory, read at the start of every turn and after every compaction; an order leaves the list only when done or withdrawn.

Every comment of the living on a book, unless it closes the topic, gets a new edition of that book with the comment applied; every other book the comment affects gets a new edition too.

## Proposal 1: psyche-context › vision/flow.md


+ ## The last response is a datom object
+ A flow's last response is a datom object.
+ Its variant comes first and decides its structure, and that structure may hold further objects, each with its own variant.
+ For example:

```ethos
+ Library.{
+ []
+ [ Title.String
+   Body.String
+   Cause.String
+   Unblock.String
+   Page.{ Title Body }
+   Block.{ Cause Unblock }
+   Kind.[ Presentation Answer Blocker Responses ]
+   Response.[ Presentation.Page
+              Answer.Body
+              Blocker.Block
+              Responses.⟦ Response ⟧ ] ]
+ [ Spelled.[ spelling.[ String ] ]
+   Kinded.[ kind.[ Kind ] ]
+   Presentable.[ presentation.[ String ] ] ]
+ [ Title.[ Spelled ]
+   Body.[ Spelled ]
+   Cause.[ Spelled ]
+   Unblock.[ Spelled ]
+   Kind.[ Spelled ]
+   Page.[ Presentable ]
+   Block.[ Presentable ]
+   Response.[ Kinded Presentable ] ] }
```

```datom
+ Presentation.{ «Refreshing the Illustrator»
+                «One flow does every job.» }
+
+ Answer.«Nine proposals written, none landed.»
+
+ Blocker.{ «No layer has a threshold»
+           «A ruling on the two numbers» }
+
+ Responses.[ Answer.«Modules landed.»
+             Blocker.{ «Fable is asleep»
+                       «Your word to wake it» } ]
```

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › vision/book.md


+ ## Each kind of object has its presentation
+ Each kind of datom object has its own presentation in the user interface.
+ The user interface shows an object in its kind's presentation, and no thinking machine renders a page for it.

Ruling: land, amend, or reject.

```

(The text fence above only wraps this report; the source has no outer fence.)

Plain-prose proposal in 65 (lines 182-194), verbatim:

```text
## Proposal 1: psyche-context › vision/flow.md

+ Every flow runs under Flow.
+ A flow that Flow did not start is replaced by a fresh flow that Flow starts, and the old one is retired.
- Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.

Ruling:

a. As shown.

b. The first added line only; live flows are adopted where they stand.

c. Neither.
```

Caveat: 66 still carries "Verified on 2026-10-17 ..." prose at the top of its mind-context › knowledge/last-response.md section; that is only valid if it matches the module in origin/main byte for byte (checker: context-module-differs).

## 2. Tool rules

### tools/book-check.mjs (usage: node tools/book-check.mjs ABSOLUTE_SOURCE; exit 0 ok, 1 errors, 2 usage/unreadable)
Refusal reasons (JSON `{errors:[{line,reason}]}`):
- one-absolute-source-path-required / source-unreadable: argument problems.
- proposal-heading-without-location: any heading starting `Proposal` must match `Proposal N: [Title · ]<repo> › <path>[, a new file]` (repo has no spaces, path has no spaces or commas).
- file-line-in-body: any line beginning `File:` in a proposal body (retired form), including inside text fences.
- no-change-in-proposal: a proposal with no `+ x` line (plus + then a non-space) and no `**Archive**` / `**Destroy**` line. Note only `+` counts, not `-`.
- missing-proposal: no proposal at all.
- quote-block-in-book: any line beginning with `>` outside a fence or comment (also inside a shown module's text? No: module lines are skipped, so a `>` inside a shown module is fine).
- unclosed-code-fence: fence never closed.
- code-over-52-columns: inside a code fence (any language except text/prose/markdown/md), any line longer than 52 code points, EXCEPT lines starting `- ` (removed lines are quoted as they are). `+ ` lines count, with their 2-char prefix. So ethos fences are limited to 52 columns. Text/prose/markdown/md fences and unfenced proposal prose have no width limit.
- text-outside-proposal-without-module: any non-blank line outside a proposal that is not: the one `Presentation.{ «...» }` line (first, before title), the `# Title` heading (only one, before any proposal/module), a located module, HTML comment lines. Any fence opened outside a proposal is also refused. 
- heading-outside-proposal-without-module: any heading outside a proposal that is not `# Title` or a located module heading.
- context-module-differs: text under a module heading must equal the module's body at origin/main (front matter removed, whole text trimmed) exactly; an optional single ```markdown/md/text fence around it is peeled off. The module extends until the next `Proposal` heading, or next `<repo>-context ›` heading, or `<!-- to-the-living:end -->`; headings and fences inside it are part of it.
- context-module-unavailable: module could not be read. The heading must match `(psyche|mind|field)-context › (spirit|intent|vision|knowledge|compensation|inquiry|role|raw)/NAME.md`; otherwise invalid. It reads from /git/github.com/LiGoldragon/<repo>: `git ls-remote origin refs/heads/main` (NETWORK; refuses when unreachable), then `git show <that sha>:<path>` (a blob must exist there). Local working copies and detached HEADs are ignored; the module must be in remote main.
- Comments `<!-- ... -->` are skipped. Headings or `+` lines inside code fences or comments open no proposal.
- Unfenced `+`/`-` proposal lines: no width limit; unchanged context lines are not refused by the checker (only a + line is required). Fenced code does count `+` lines for the change check.

### tools/book-build.clj (bb tools/book-build.clj SOURCE.md OUT.html [--code tools/book-code.html] [--figures DIR] [--ethos-zero REF])
- `## Proposal N: where` (or `###`) headings open an article; with no File: line next, the heading text (location) is shown as the target chip. `### Proposal N: title` is the old form.
- Unfenced signed lines in a proposal: a paragraph in which EVERY line starts `+ ` or `- ` (or is a lone sign), and that has at least one `+`-line (or removes a `---` front-matter rule), is read as a change "per line": each signed line its own line; a run of `-` lines pairs line by line with the following `+` run and is word-diffed (<del>/<ins>); unpaired ones are wholly red or green. Blank line separates chunks. A bullet continuation joins lines only if both are list items or table rows, or inside an open code fence. 
- Unchanged context lines: not allowed unfenced in the same paragraph. A paragraph mixing signed and unsigned lines is NOT a diff paragraph, so it renders as an ordinary prose paragraph with the raw `+`/`-` characters visible. A separate unsigned paragraph under a proposal is plain prose (not a context panel). Context lines (unsigned, shown plain, with 2-space indent allowed in a text fence) exist only inside a ```text fence in a proposal (rendered grey `ctx` panels); a fully unsigned text fence in a proposal is shown as a literal code block of the target's language. Code fences with mixed signs are kept as code with per-line tint, removed-then-added pairs word-diffed.
- A `- ` bullet outside a proposal is a normal list; inside a proposal a leading `- ` is a removal.
- Unlabelled fences outside a proposal are diagrams needing fig-N.svg in --figures (else build refuses, exit 1); in text fences, a box-and-arrow sketch with no sign lines is also a diagram (this is why a module with ASCII boxes in an unlabelled fence needs an illustration. NOTE: in the new form a module is shown verbatim, so a module containing an unlabelled fence outside a proposal is routed as a diagram in the builder; 65 and 66 both contain such fences in their modules and have no built html yet, so untested: expect fig-N.svg to be demanded, or the fence to need a label).
- `Ruling:` closes an open **Destroy**/**Archive** record panel; `Ruling, one number...` opens a rulings section; a numbered list ("1. ...") becomes choices.
- Ethos check (--ethos-zero REF): every ```ethos fence, and every ```text fence in a proposal whose target (File line or heading path) ends in .ethos, is run through ethos-zero's `Check.<file>`; a refusal fails the build with `ethos block ("first line") refused by ethos-zero: <reason>`, exit 1. A fence written as a change is checked as it reads after the change: `- ` lines dropped, `+ ` stripped of sign, text-fence context lines stripped of 2 spaces. Default ethos-zero pin: github:LiGoldragon/ethos-zero/07714b0171802787bea1eefe4caa2d826d9c4030. REF may be a flake ref (e.g. github:LiGoldragon/ethos-zero/<branch>, built with nix build), a store path, or a binary. Realization failure aborts with "ethos-zero REF could not be realised".
- `# Title` becomes title/h1; the page <title> is the Presentation datom's title if present. Comment lines and the Presentation line are skipped.

## 3. psyche-context vision/nexus.md

Repository /git/github.com/LiGoldragon/psyche-context. Detached HEAD = dde85849fb57fabf350c3015143cd0655b3376d4 ("Flow vision: title as datom struct, six-character flow id, drop ancestor-naming sentence", Sat Oct 17 12:53:35 -0600 2026); equals origin/main (local ref, nothing fetched). The local branch `main` is stale (455d677c) and still has skills/vision-nexus.md. Current path: vision/nexus.md (checker module location: `psyche-context › vision/nexus.md`). No local modifications to that file.

Full text with line numbers (git cat-file -p HEAD:vision/nexus.md | cat -n):

```text
     1	---
     2	description: A long-running Nexus — its sockets, clients, wire contracts and store — is being designed or judged against what the living wants it to be.
     3	dependencies: [vision-ethos, knowledge-datom]
     4	---
     5	
     6	## A Nexus is the whole
     7	
     8	A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.
     9	
    10	## A kind of thing
    11	
    12	Nexus is our word for the style of component that speaks signal and uses a similar database.
    13	
    14	## Library and daemon
    15	
    16	Every component built from now on is a Nexus. The nexus repository is
    17	the library that defines the core of a Nexus component.
    18	
    19	## Universal traits first
    20	
    21	The basic ontology of an actor and dataflow system is designed before
    22	implementation; signal and sema are designed against it as if new, the
    23	old code at most inspiration.
    24	
    25	Every method lives in a trait; an inherent method is a trait not yet extracted. The traits and types of a Nexus are one ontology designed before any body is written; defaults wherever expressible, through rich sub-trait chains. Traits live on data-bearing types; a zero-sized type with behaviour is a namespace pretending. Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive, and every reference names its target by that name. `fn main()` is the only free function; a missing owner is a missing type.
    26	
    27	## Processing is for the effect
    28	
    29	An object enters a Nexus for the effect; the response follows as an
    30	effect of it. Conversion is the wrong frame for it. The name is open,
    31	Apply liked.
    32	
    33	## Documents
    34	
    35	The nexus and sema documents are undesigned; when they are designed
    36	they live in the Nexus's main repository.
    37	
    38	## Sockets
    39	
    40	A Nexus opens at least two sockets. The ordinary socket serves
    41	ordinary peers. The meta socket is privileged — the root user of the
    42	Nexus — and configuration and privileged operations pass through it;
    43	every Nexus has one, since without it nothing could configure the
    44	Nexus. A Nexus that needs more levels of access opens more sockets.
    45	
    46	## Default clients
    47	
    48	A client is a separate program from the Nexus. For now the default
    49	clients are packaged with the Nexus as separate crates of its
    50	repository, which is a multi-crate repository: one datom-converting
    51	CLI per socket, however many sockets the Nexus has, at least two. A
    52	default client serves bootstrap first, then debugging and testing,
    53	long after production has stopped using it. The meta CLI is named
    54	component-meta.
    55	
    56	A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
    57	
    58	## Signal only
    59	
    60	Every client speaks to a Nexus in pure signal, fully binary. A Nexus
    61	speaks only the signal contracts it is compiled with; two of these
    62	are its own, one per socket. A Nexus thinks in typed values — enums,
    63	structs, scalars — and the string fields it still carries are
    64	records on the way to a fully typed form.
    65	
    66	The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket.
    67	
    68	Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.
    69	
    70	## The graph
    71	
    72	A Nexus is a vertex in the graph of nexuses. An edge joins two
    73	vertices and carries one contract. Every connected pair has an
    74	ordinary edge; only some pairs have a meta edge. A Nexus is compiled
    75	with the contracts of its own sockets and of every edge it has.
    76	
    77	Peers depend on each other's wire repositories, never on each other's Nexuses.
    78	
    79	## Routing
    80	
    81	Signals cross the network through a router. The router tells signal
    82	types apart by an enum that wraps the objects, held in the signal
    83	repository, which every component depends on. That repository also
    84	holds what every signal needs in common — the handshake payload
    85	among it.
    86	
    87	## Configuration
    88	
    89	A Nexus starts with no arguments and there is no bootstrap binary.
    90	Its executable holds a default configuration as a constant. On start
    91	it looks for its Sema database at the default location: a database
    92	that exists holds the configuration; a database created new is
    93	seeded with the defaults. The meta socket carries a Configure
    94	interface, and changed values are accepted through it.
    95	
    96	## First configuration
    97	
    98	A Nexus keeps a standard metadata tree. In it a type records whether
    99	the meta Configure was ever done; that record is reversed only on the
   100	meta socket, and while it is unset Configure is accessible on the
   101	ordinary socket. The tree holds everything standard about the Nexus:
   102	its socket paths — its own and those of every edge-socket it connects
   103	to — and whatever else comes up as standard nexus configuration data.
   104	The built-in default configuration is independent of this and is
   105	what gives the socket path on which the Configure signal arrives.
   106	
   107	## Repositories
   108	
   109	A component has three repositories: its main repository, holding all
   110	its code, and two signal repositories — one for the ordinary
   111	socket's contract, one for the meta socket's. Shared kinds go into
   112	reusable libraries, which are encouraged.
   113	
   114	`<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, never optional, since configuration flows through it. The CLI is `<nexus>`.
   115	
   116	A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies, the typed payload of each; no catch-all. Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves. Storage vocabulary never appears on the public wire.
   117	
   118	## Why everything is a Nexus
   119	
   120	The Nexus is an architecture concept, not one specific Nexus: everything made is a Nexus.
   121	
   122	A Nexus's vision is split by its code modules.
   123	
   124	Everything built from now on is a Nexus, and what was built in
   125	another shape is rewritten as one. The consistency creates
   126	reliability, quality, and clarity.
   127	
   128	## Actors
   129	
   130	The engine inside a Nexus is driven by Kameo actors. The standards
   131	of their use are still to be designed. Arc-Mutex is permitted.
   132	
   133	## Splitting a Nexus
   134	
   135	A Nexus deals with a domain. When its features grow too many,
   136	splitting one or more nexuses out of it is considered.
   137	
   138	Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
   139	
   140	## Observation by subscription
   141	
   142	State is observed by subscription: the subscriber receives the state
   143	on open, then each change as it happens.
   144	
   145	## Polling is forbidden
   146	
   147	Polling is forbidden; a correct system goes quiet when nothing
   148	changes.
   149	
   150	## Three parts and one path
   151	
   152	A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
   153	
   154	```
   155	Library                                  ; what the three parts share
   156	[]                                       ; imports: none
   157	[ FlowId.Integer                         ; types
   158	  Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
   159	  Aspect.[ Psyche Mind Field ]
   160	  Layer.[ Primary Secondary Tertiary Quaternary ]
   161	  Event.[ Started Stopped ] ]
   162	[]                                       ; kinds
   163	[]                                       ; associations
   164	
   165	Signal                                   ; what Flow says, on its ordinary socket
   166	[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
   167	[ Launch.{ Voice                         ; queries
   168	           Brief.String }
   169	  Report.{ FlowId Event } ]
   170	[ Launched.FlowId                        ; responses
   171	  Refused.[ NoCapsule
   172	            VoiceBusy.Voice ]
   173	  Reported ]
   174	[]                                       ; types
   175	
   176	Operation                                ; what Flow does: one operation for every effect
   177	[ flow:[ FlowId Voice Event ] ]          ; imports
   178	[ Start.{ Voice Capsule }                ; operations
   179	  Record.{ FlowId Event } ]
   180	[ Started.FlowId                         ; outcomes
   181	  Recorded
   182	  Failed.[ CapsuleRefused StoreRefused ] ]
   183	[ Capsule.{ Home.String                  ; types
   184	            Login.Vector<String> } ]
   185	
   186	Memory                                   ; what Flow remembers
   187	[ flow:[ FlowId Voice Event ] ]          ; imports
   188	[ Flow.{ FlowId                          ; record types
   189	         Voice
   190	         State.[ Running Ended ]
   191	         Vector<Event> } ]
   192	```
   193	
   194	```
   195	Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
   196	Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
   197	Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
   198	Succeeded                                             ; 4 Memory's answer to Operation
   199	Started.7                                             ; 5 Outcome
   200	Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
   201	```
```

## 4. Nexus-as-a-kind knowledge/compensation modules

State of the clones: mind-context HEAD (detached) 344f6c3669d3d882f96f63ed435022a3cfed2bf4 is stale (old skills/knowledge-*.md layout); local ref origin/main = ab2fef87eccc056ea3876690df35ef37c82d5a96 (Sat Oct 17 13:05:34 2026) has the current layout knowledge/*.md. field-context HEAD 5070467dd8b596246c47e9cbcbf55415025483fc is stale; origin/main = f2abe483af1e5f55a441a691a068925b47593fb1 (Sat Oct 17 13:13:08 2026). These origin/main refs are from the last fetch; the checker uses the remote's live main (network), which may be newer.

Finding: there is NO knowledge or compensation module about the Nexus as a kind (sockets, CLI, signal, configuration, memory, three parts, actors, repositories) in any of the three repos at origin/main. That content is in the vision (section 3). The only nexus-named knowledge module is mind-context › knowledge/nexus.md (today's running nexuses; depends on vision-nexus), and mind-context › knowledge/flow.md (knowledge-flow). field-context has no nexus or flow-as-kind compensation (compensation/ has flow-evidence, main-flow, subflow, messenger-clj, launch which are about conduct). Other knowledge modules that mention nexus incidentally (not kind-level): knowledge/flow-caller.md, flow-configuration.md, flow-queue.md, flow-receipt.md, flow-seats.md, last-response.md, lojix.md, refresh.md, handover.md, ethos.md.
At the stale HEAD the same modules were skills/knowledge-nexus.md (different text: Home 83 packet with socket paths and versions) and skills/knowledge-flow.md.

### mind-context › knowledge/nexus.md (origin/main ab2fef87), whole, raw with front matter

```text
---
description: What the nexuses are today — which run, on which sockets and versions, from which branches — is read, before judging or changing one.
dependencies: [vision-nexus]
---

Orchestrate: read the current source version in the declared Orchestrate repository’s `Cargo.toml`.
Flow: read the current source version in the declared Flow repository’s `Cargo.toml`.
Message: read the current source version in the declared Message repository’s `Cargo.toml`.
Lojix: read the current source version in the declared Lojix repository’s `Cargo.toml`.
```

### mind-context › knowledge/flow.md (origin/main ab2fef87), whole, raw with front matter

```text
---
description: A flow must be launched, named, claimed or reached, or a hook or sandbox flow run, with what is deployed today rather than with Flow as designed.
dependencies: [vision-flow]
---

Before launching, naming, claiming, reaching, or reporting a Flow, read
the matching deployed source and obtain the target's explicit response
through the current ordinary or meta socket. Do not infer protocol,
caller identity, store state, or runtime bindings from a source version
or client path.

## Stated configuration and launch contract

These are the authorized contracts; this section does not establish deployed runtime behavior while the configuration rewrite is pending.

The tool that starts flows merges its configuration files in order, shared, aspect, metaflow, map into map, so a later file's value wins at each key.

A context is young while it stays under half the layer's refresh threshold.

A launch that needs a Primary starts its Secondary first.
```

## 5. flows/d68c82/books/w/na/memory.ethos (verbatim)

```text
Memory.
{
; imports
[ flow:[ FlowId Metaflow Event ] ]
; record types
[ Answer.[ Succeeded Failed ]
  Flow.{ FlowId
         Metaflow
         State.[ Running Ended ]
         ⟦ Event ⟧ } ] }
```

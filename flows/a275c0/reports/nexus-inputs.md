# Nexus vision crystallization: gathered inputs

Gathered 2026-10-16 for { Psyche nexus Secondary a275c0 }. Read-only gathering; nothing else was modified.
Observations are marked **Obs.**; inferences are marked **Inf.** and kept separate.

Sources read whole: `flows/d68c82/books/38-ethos-nexus-chronos.md`, `flows/23824a/handover.md`,
`flows/23824a/reports/ethos-nexus-chronos-psyche.md` (Tensions, Nexus, Chronos and Authored-skills
sections read in full; the Ethos section scanned for Nexus records), `.claude/skills/vision-nexus/SKILL.md`.

---

## A. The current vision-nexus authored source

**Obs.** `.claude/skills/vision-nexus/SKILL.md` is generated evidence (CLAUDE.md: "`.agents/`, `.claude/` … trees are generated read-only evidence … Regenerate them through Curriculum Nexus from the authored Psyche, Mind, and Field skill repositories").

**Authored source:** repository `psyche-context` (remote `git@github.com:LiGoldragon/psyche-context.git`), path **`skills/vision-nexus.md`**.
Local clones: `/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md` and `/git/github.com/LiGoldragon/psyche-skills/skills/vision-nexus.md` (same remote; both at `c301353`; the file is byte-identical to the generated SKILL.md — `diff` empty). Last commit touching the file: `72149ef Move Psyche skill sources under skills`. Book 38 names the target as `psyche-context › skills/vision-nexus.md`. The 23824a report cites it as `psyche-skills/skills/vision-nexus.md` at f81b7b2; same file, older name of the repo/clone; line numbers in the report are one lower than the current file from line ~150 on (report "153: FlowId.Integer" = current 153; report "154: Voice" = current 155 — the report's Tensions quotes are approximate).

Verbatim, `skills/vision-nexus.md` (line numbers added for reference in D/E):

```
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
120	Everything built from now on is a Nexus, and what was built in
121	another shape is rewritten as one. The consistency creates
122	reliability, quality, and clarity.
123	
124	## Actors
125	
126	The engine inside a Nexus is driven by Kameo actors. The standards
127	of their use are still to be designed. Arc-Mutex is permitted.
128	
129	## Splitting a Nexus
130	
131	A Nexus deals with a domain. When its features grow too many,
132	splitting one or more nexuses out of it is considered.
133	
134	Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
135	
136	## Observation by subscription
137	
138	State is observed by subscription: the subscriber receives the state
139	on open, then each change as it happens.
140	
141	## Polling is forbidden
142	
143	Polling is forbidden; a correct system goes quiet when nothing
144	changes.
145	
146	## Three parts and one path
147	
148	A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
149	
150	```
151	Library                                  ; what the three parts share
152	[]                                       ; imports: none
153	[ FlowId.Integer                         ; types
154	  Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
155	  Aspect.[ Psyche Mind Field ]
156	  Layer.[ Primary Secondary Tertiary Quaternary ]
157	  Event.[ Started Stopped ] ]
158	[]                                       ; kinds
159	[]                                       ; associations
160	
161	Signal                                   ; what Flow says, on its ordinary socket
162	[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
163	[ Launch.{ Voice                         ; queries
164	           Brief.String }
165	  Report.{ FlowId Event } ]
166	[ Launched.FlowId                        ; responses
167	  Refused.[ NoCapsule
168	            VoiceBusy.Voice ]
169	  Reported ]
170	[]                                       ; types
171	
172	Operation                                ; what Flow does: one operation for every effect
173	[ flow:[ FlowId Voice Event ] ]          ; imports
174	[ Start.{ Voice Capsule }                ; operations
175	  Record.{ FlowId Event } ]
176	[ Started.FlowId                         ; outcomes
177	  Recorded
178	  Failed.[ CapsuleRefused StoreRefused ] ]
179	[ Capsule.{ Home.String                  ; types
180	            Login.Vector<String> } ]
181	
182	Memory                                   ; what Flow remembers
183	[ flow:[ FlowId Voice Event ] ]          ; imports
184	[ Flow.{ FlowId                          ; record types
185	         Voice
186	         State.[ Running Ended ]
187	         Vector<Event> } ]
188	```
189	
190	```
191	Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
192	Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
193	Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
194	Succeeded                                             ; 4 Memory's answer to Operation
195	Started.7                                             ; 5 Outcome
196	Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
197	```
```

---

## B. Nexus-related proposals in book 38 («Ethos, Nexus and Chronos: the vision»)

**Ruling status (Obs.):** Book 38 was published 2026-10-16T12:30:25 as https://claude.ai/artifact/41j6VupvsrT3Qsp8xFwBkM (d68c82/log.md:1978). Live comment read of that artifact (ArtifactComments, read-only, 2026-10-16): **"No comment threads on this artifact yet."** No ruling on any book-38 proposal appears in `flows/d68c82/log.md` (through 12:40:16), `flows/0c9a77/reports/relayed-comments*.edn`, `flows/7c89aa/comment-relay-ledger.jsonl`, `flows/d68c82/reports/*comments*`, or other comment records under `flows/*/reports/`. **Every proposal below is UNRULED.** The one living ruling folded into the book before publication is on Proposal 7 (Ethos, traits — "Long term we want all the traits in ethos and short term we just do without", d68c82/log.md:1957); that is Ethos, not listed here.

Earlier rulings bearing on the *content* (not on book 38 itself) are given per proposal.

Overlapping, also unruled, books published the same hour (live comment reads: no threads on any):
- «Flow: Nexus, ethos and design, 2nd edition» https://claude.ai/artifact/L2Y6aaAAqGWa6FsEqfpS21, source `flows/d68c82/books/r-nexus-ethos-design.md` — Proposals 9, 10, 11, 13 target `skills/vision-nexus.md` (quoted in E).
- «The Flow Nexus, whole, 2nd edition» https://claude.ai/artifact/9qkgFa8knt5Vc5UpPmQ3iL, `flows/d68c82/books/r-flow-nexus-whole.md` — Proposal 9 targets `skills/vision-nexus.md` (removes the Flow example; see E).
- «Chronos, 3rd edition» https://claude.ai/artifact/TDzS3V4ssSYQ7jUsohWKrx, `flows/d68c82/books/r-chronos.md` (Chronos only).

### B10. Proposal 10 — `psyche-context › vision/ethos.md` (Ethos file, but about the Ethos Nexus; included as Nexus-related)
```
+ The Ethos Nexus has the three parts: Signal, Memory and Operation.
+ It keeps the registry of Ethos sources, filled from datom files that the repositories carry, loaded together atomically into one full registry.
+ Every Ethos source added, edited or renamed changes the registry.
```
Status: **unruled.** Basis: `flows/23824a/vision/ethosNexus.md` (2026-10-10) and `flows/23824a/vision/registry.md`. Related earlier ruling: «Sources and the registry» proposal 2 approved (23824a/handover.md:35-36, log 2026-10-10).

### B12. Proposal 12 — `psyche-context › skills/vision-nexus.md`
Book preamble: "On 2026-10-05 you said no Nexus should hold any datom. Your later word, from 2026-10-14, says a Nexus uses datom, and this proposal takes it."
```
- A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands.
+ It identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim.
+ A CLI speaks to one Nexus, opens no store, stays thin.
+ A Clojure prototype uses an EDN payload for everything; a Nexus uses datom.
```
Status: **unruled**; amended within the book by Proposal 21 (Fable's view), which restores the struck clause. Basis: `flows/d68c82/vision/tools.md:14` (2026-10-14) vs `flows/8475a9/vision/datom.md:25` (2026-10-05).

### B13. Proposal 13 — `skills/vision-nexus.md`
Preamble: "On 2026-10-03 you said the flow id is a hash. Your later word, from 2026-10-09, keeps it a string for now, with a comment saying so."
```
- [ FlowId.Integer                         ; types
+ [ FlowId.String  ; types; the string is very
+                  ;   unideal: a real id from
+                  ;   the flow's hash is needed
```
Status: **unruled.** Basis: `flows/ebbe30/vision/ethos.md:39` (2026-10-09). Conflicts with «The Flow Nexus, whole, 2nd» P9, which removes this example (see E).

### B14. Proposal 14 — `skills/vision-nexus.md`
Preamble: "Your later word, from 2026-10-11, drops the voice. Every other Voice in this example becomes Metaflow."
```
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
+   Metaflow.{ Aspect Topic Layer }  ; who a flow is
+ The voice concept is gone; the default topic is core, the permanent topic, the last to stand.
```
Status: **unruled.** Basis: `flows/875960/vision/flow.md:11` / `flows/9519a1/vision/flow.md:3` (2026-10-11, "No we've gotten rid of the voice concept").

### B15. Proposal 15 — `skills/vision-nexus.md`
Preamble: "Your later word, from 2026-10-09, says trait, and every place is renamed."
```
- []                                       ; kinds
+ []                                       ; traits
```
Status: **unruled.** Basis: `flows/ebbe30/vision/ethos.md:9,29` (2026-10-09; note :29 also says "kind might be used to also mean traits").

### B16. Proposal 16 — `skills/vision-nexus.md`
Preamble: "Your later word, from 2026-10-09, loads configuration atomically from many files; starting with no arguments stays."
```
+ A Nexus's configuration may live in separate files in different repositories, each a datom payload, and is loaded atomically.
+ The CLI sends those payloads one after another on the meta socket, so the Nexus starts with the right configuration, even at different layers.
+ The meta socket belongs to the Nexus, never to the short-term Clojure prototype.
```
Status: **unruled**; amended within the book by Proposal 23. Basis: `flows/445410/vision/nexus.md:1` (2026-10-09, with "This is brilliant. Let's do this. Get this ratified") and `flows/33752b/vision/flow.md:29` (2026-10-13, meta socket vs Clojure). **Obs.:** the 2026-10-09 words "Get this ratified" are an order to ratify, not a landing of a specific text.

### B17. Proposal 17 — `skills/vision-nexus.md`
Preamble: "Your word of 2026-10-04 leaves open whether a Nexus is actor-based until it is tried, so the Kameo line goes."
```
- The engine inside a Nexus is driven by Kameo actors. The standards
- of their use are still to be designed. Arc-Mutex is permitted.
+ Whether the engine inside a Nexus is actor-based or something else is refined after practice.
+ Signal talks only to Operation, Memory talks only to Operation, and Operation talks to both.
+ Arc-Mutex is permitted.
```
Status: **unruled.** Basis: `flows/aa887c/vision/nexus.md:11,23` (2026-10-04). Earlier: «The standard entry point» rulings sheet `flows/bad807/books/7-entry-point.rulings.md` posed "Whether the core library is actor-based in name" (a)/(b) — **no recorded answer found**. Contrasts with «Flow: Nexus, ethos and design, 2nd» P9, which uses "Nexus meta-actor" language (E).

### B18. Proposal 18 — `skills/vision-nexus.md`
```
+ The three parts, Signal, Operation and Memory, and how each divides, are most of the machine's anatomy.
+ A standard entry point, like a Rust macro, enforces the three parts and their one path, so nothing bypasses them; the bodies are written by hand.
+ Ethos, the Nexus architecture and Flow are developed together: the language, the runtime architecture, and the component to bootstrap.
+ Signal defines the formats a message can take: the simple form, without the flow id, for common queries and responses; the extended form for the technical side, debugging and other components.
+ Nexuses are the long term; Clojure prototypes are the short term, derived from the same Ethos.
```
Status: **unruled.** Bases: d68c82/vision/design.md:20 (10-12); 28d847/vision/nexus.md (10-03/04); d68c82/vision/flow.md:103 (10-14); edf227/vision/signalForms.md:3 (10-03); d68c82/vision/deployment.md:29 (10-13). Related earlier: «The Nexus» proposal 2 (standard entry point) got "Let's flesh this out in actual code…" (aa887c/reports/his-comments.md #6) — **not an approval to land**; «The Nexus» proposal 1 ("Three parts and one path") **approved** 2026-10-04 ("This is good. Can land, and I would also like to have example code") — already present at vision-nexus:146-197. Overlaps «Flow: Nexus, ethos and design, 2nd» P13.

### B19. Proposal 19 — `psyche-context › skills/vision-source.md`, a new file (the Source nexus)
```
+ ---
+ description: The Source nexus, which holds and verifies sources, is being designed or judged.
+ dependencies: [vision-nexus]
+ ---
+ ## Source
+ One Source nexus holds the sources for all components; to get a source is to send it a source request.
+ A source is a Git repository at a revision, or a local path on a host, fetched by its own kind of backend fetcher.
+ The Source nexus keeps its own Blake3 hash of the whole snapshot, without the Git directory, as Nix does.
+ It keeps several registries; the Git equivalence registry is dropped when Git is cut off.
+ The hash is there to verify that the files are the right files; a smart store that knows what to keep comes later.
+ Ethos and curriculum share one sources library, with Memory objects for the registry of sources; a skill refers to a source by name.
```
Status: **unruled.** Bases: d68c82/vision/source.md:3,20,42,52 (2026-10-10); 23824a/vision/sources.md. Handover: «The Source nexus» 2nd edition and the word-names book are unruled (23824a/handover.md:43-46); a275c0/log.md: Source nexus book D2–D8 open.

### B21. Proposal 21 (Fable's view) — `skills/vision-nexus.md`, amends P12
Preamble: "your word of 2026-10-14 says which text a payload is written in, Clojure EDN or Nexus datom, and does not undo your word of 2026-10-05 that no datom and no string handling sit inside a running Nexus, so the two do not conflict and the struck line stays."
```
- A Clojure prototype uses an EDN payload for everything; a Nexus uses datom.
+ A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ A Nexus's payloads, its configuration files among them, are written in datom; a Clojure prototype's are written in EDN.
+ A Nexus reads a datom file only through an outside tool, the CLI it is meant to work with, never by handling the text itself.
```
Status: **unruled.** Basis adds aa887c/vision/nexus.md:31 (2026-10-04). Earlier rulings sheet `flows/bad807/books/8-datom-file.rulings.md` (ReadFile/Supply options) — **no recorded answer found**.

### B23. Proposal 23 (Fable's view) — `skills/vision-nexus.md`, amends P16
Preamble: "your word of 2026-10-09 calls loading configuration files in succession a hack to get the Nexus started until datom path expansion is solved, and the Configuration paragraph still says Sema."
```
- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database
+ Until datom path expansion is solved, the CLI sends the configuration files one after another on the meta socket; this is the way to start a Nexus for now, not the lasting design.
```
Status: **unruled.**

### B24. Proposal 24 (Fable's view) — `skills/vision-nexus.md`
Preamble: "The book keeps the caller identity in the CLI but misses your words of 2026-10-03 and 2026-10-12 that these pieces live in libraries shared by every component, not in one Nexus's library."
```
+ The process object that identifies a CLI's caller lives in a shared library that many nexuses use, so no CLI rewrites it and the code reads plainly; it is never user-facing and never configurable.
+ The word id conversion lives in a library every component reuses, generic over hash sizes, so a flow id is one use of it and not its owner.
```
Status: **unruled.** Basis: 875960/vision/flow.md (comment 4, 2026-10-12 16:21). Overlaps «Flow: Nexus, ethos and design, 2nd» P11.

Not included (Obs.): P1–P9 (Ethos), P11 (vision-flow topic identifier; touches "a dedicated Nexus" only via its basis), P20 (Chronos), P22, P25 (Ethos).

---

## C. 23824a handover and report: Nexus ruled / unruled / held / voided

### Ruled (approved by the living), Nexus-relevant
- «The Nexus» proposal 1, "Three parts and one path" — approved 2026-10-04 ("This is good. Can land, and I would also like to have example code"), `aa887c/vision/nexus.md:3`; present at vision-nexus:146-197.
- vision-nexus first heading ("A Nexus is the whole …") approved 2026-09-11 ("yes, good"), `fe34eb/vision/nexus.md:51` (via report's Authored-skills section; line 8).
- «Sources and the registry» proposal 2 approved (registry; Ethos-side), handover:35-36.
- Report record "Every Nexus has Signal, Operation and Memory" (d4ae97/vision/nexus.md, 2026-10-07): "All nexuses have to have all three. Maybe that is something we need to add into the vision" — a direction, not a text ruling.
- Proposal 7 trait ruling (2026-10-16, Ethos): "Long term we want all the traits in ethos and short term we just do without."

### Unruled (per handover/report)
- Source nexus: design and ethos drafts in `flows/058f16/reports/` (source-nexus-design.md, source-ethos/); books «The Source nexus» 2nd edition and the word-names book, **unruled** (handover:43-46). "The hash type is ruled only in «Bytes in ethos»" — and «Bytes in ethos» is among the unruled 081064 books (handover:30-35). **Inf.:** so the hash type is effectively unruled.
- «The Ethos Nexus» (four questions) — unruled (handover:32). Ethos Nexus drafts in `flows/081064/reports/ethos-nexus/` pass the generator; their import of Source library types unchecked (handover:37-40).
- Chronos: «Chronos» 2nd edition, ten choices, unruled (`flows/984e88/books/02-chronos.md`); repository chronos main a5cf51, entry-point 500094; not built (astronomy `todo!()`, no process or socket) (handover:49-56). Now 3rd edition `r-chronos.md` (TDzS3V), unruled.
- Generic nexus repository: entry-point branch ahead of main (handover:47) — **Obs.:** no ruling to merge recorded.
- Open questions (handover:58-64): resolve the seven unruled Ethos books first or fold them in; how Chronos meets the Ethos Nexus and Source nexus designs (shape of Fetch: whole snapshot or per file); the report's tensions.
- Report "Tensions" relevant to Nexus, all open: Datom inside a Nexus; Voice as a type or no voice; type of a flow id; Memory or Sema; How a Nexus gets its configuration; Actors inside a Nexus; Which example comes first; where the word check lives (dedicated Nexus vs shared library).

### Held
- **Chronos design defaults, HELD** (not decided): d68c82/log.md:1995 (2026-10-16T12:35:55): "It sent Chronos design defaults (Rational angle, apogee names, no open watches, contextualizer) as decided; told Field to hold them for the Chronos design metaflow." Also `flows/a275c0/log.md:5`: "exact-fraction angle/apogee/watch defaults held." The defaults as written in `flows/984e88/books/02-chronos.md`:
  - P5 imported angle type — Default `Rational`, `«num_rational::Rational64»` (num-rational 0.4.2: "an exact fraction, here of degrees, bearing Eq and Hash"). **HELD.**
  - P13 the aphelion — Default `LunarApogee` and `SolarApogee` ("the Earth's aphelion is the Sun's apogee"). **HELD.**
  - P11 what Memory keeps — Default "nothing more, and `Watcher` with its imports is removed. A watch lives with its connection, and a restart ends both." (no persisted open watches). **HELD.**
  - (P6 default arc written `43/2`; P9 true nodes/apogee; P10 location request-else-meta; P12 DE440 — re-proposed in r-chronos.md P2–P5; unruled.)
- Handover: Ethos candidate patches in `flows/1d0733/handover.md` all held, none landed.
- d68c82 log 12:31:39 / 12:32:11: Field told to hold unruled role-repo code choices and machine-chosen thresholds (not Nexus-specific).

### Voided by the living (records where the living struck a concept that touches the Nexus)
- **Voice concept** — "No we've gotten rid of the voice concept. Now it's just replaced by the core topic." (875960/vision/flow.md:11; 9519a1/vision/flow.md:3, 2026-10-11). Voids vision-nexus:154 `Voice.{ Aspect Layer }` and VoiceBusy etc.
- **"Name"/"Word" as the identifier type's name** — "Those are silly suggestions." (875960/vision/flow.md, 2026-10-12 16:12).
- **Meta socket in the Clojure short-term prototype** — "What do you mean by meta socket? … You're talking about meta sockets, which have to do with nexus, and then you're talking about the short-term solution, which is [Clojure]. Total fucking confusion here." (33752b/vision/flow.md:29, 2026-10-13).
- **Key-value in Ethos** — "We don't have key-value in Ethos anymore. Everything is a type." (91ea9f/vision/ethos.md:36, 2026-10-02).
- **Claimed caller ID** — "If we enforce the caller identification, then we don't need the model to declare its ID." (875960 / 9519a1, 2026-10-11 20:32). Consistent with vision-nexus:56.
- **"Seat" vocabulary** — "metaflows, not seats" (d68c82/log.md:1977, 1979; 2026-10-16). Not Nexus-kind, but appears in launch config.
- **Nexus-core runtime concept** — "I think I was overthinking the whole 'nexus-core' runtime concept" (fe34eb, 2026-09-10) — later reopened (see E).
- **"Nexus is the universal library for all nexuses; the daemon lives in Ethos Zero" — "this is wrong"** (fe34eb, 2026-09-10).
- Sonnet comments in Ethos — "I don't want these Sonnet comments anymore" (91ea9f, 10-02; Ethos only).

---

## D. Raw psyche records on the Nexus as a kind (verbatim)

Scope: `flows/*/vision/nexus*.md` (all, excluding `archive-*`), `flows/*/notion/*` on the Nexus, selected `flows/*/vision/flow.md` entries and a few other Nexus-named vision files whose subject is the Nexus as a kind. Dates: the record's own date where given; otherwise the commit date that added the file (marked "commit"). Each followed by **Obs.** on whether vision-nexus already says it.

### D1. `flows/fd301d9a/vision/nexusTraits.md`
```
## 2026-08-13 — mandatory traits are the comprehension surface

Source: `psyche-raw/Intent/mandatoryTraits.md`, 2026-08-13, psyche-approved wording.

> Every method call in our Rust code lives under a trait, because
> traits are the comprehension surface — the layer where concepts
> become visible and implementations are constrained to think within
> them. Rust is the new assembly language: no serious engineer reads
> all the assembly, and the same is happening to Rust. Traits and
> main types are what the psyche reads; everything else is
> implementation detail that Ethos will eventually generate.

## 2026-08-19 — the Nexus contains the execution engine

Source: `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, dictated and captured 2026-08-19T13:49+02:00.

> There's something else I want to talk about before we get deeper
> into creating this component, which is vocabulary related. So, in
> what we call the rest components, and this is ambiguous, which is
> why I want to talk about this. There is a concept called Nexus,
> N-E-X-U-S. And because this concept hasn't really been used much,
> it seems to be sort of hanging in the air. And because we need, and
> because of what it is, essentially, the way I work is a lot of
> intuition. And the fact that I created this Nexus thing shows that
> I was onto the intuition that there is a core there, the Nexus, to
> this architecture of how I'm designing each component, which
> deserved a name.
```
**Obs.:** traits record ≈ vision-nexus:25 ("Every method lives in a trait…"). Nexus-as-core record: no matching line; vision-nexus:8 takes Nexus as the whole.

### D2. `flows/fe34eb/vision/nexus.md` (2026-09-10/11)
```
## 2026-09-10 — a nexus is a daemon; the nexus repo is the library that defines the core of a nexus component

Context: the flow asked whether "the daemon lives in Ethos Zero" meant Ethos Zero is itself a Nexus or generates the daemon shape of every Nexus.

> a nexus is a daemon. every component we will build will be a nexus. so the nexus repo is the library that defines the core of a nexus component, which is a daemon
>
> > "Nexus is the universal library for all nexuses; the daemon lives in Ethos Zero.
>
> this is wrong

-- psyche, typed.

## 2026-09-10 — the idea of the Nexus root was to expose the types used in the core of the program, in ethos

Context: the flow asked whether input and output stand as the Nexus root's sections. The psyche opened a discussion rather than ruling; "am I overcomplicating things?" is the psyche's question, not a ruling.

> 4. I want to discuss nexus actually. am I overcomplicating things? the idea was to expose the types used in core of the program (in ethos)

-- psyche, typed.

## 2026-09-10 — the nexus-core runtime concept was overthinking; signal gives the main types, sema the database types

Context: the flow presented the fork of no Nexus root versus a Nexus root that is a Library plus the core's operations.

> I think I was overthinking the whole "nexus-core" runtime concept. As you said, signal defines the requests and the replies, and that sort of gives us all of the main types that we want to be concerned with, other than the database types, which would be the sema types.

-- psyche, typed.

## 2026-09-10 — the word Nexus is our word for the style of component that speaks signal and uses a similar database

> The word Nexus is our word for the style of component that speaks signal and uses a similar database.

-- psyche, STT.

## 2026-09-10 — a nexus is a daemon amongst other things, otherwise it would just be called a daemon

> A nexus is a daemon, amongst other things (otherwise we would just call it a daemon). Are those other things specified?

-- psyche, typed.

## 2026-09-10 — "A Nexus is a daemon" is only explanatory; daemon is a bad name, but a thinking machine that thinks in terms of daemons understands nexus through "is like a daemon"

Context: the flow proposed replacing "Daemon is retired as the name of the thing" with "Daemon alone does not name it."

> The sentence is: "A Nexus [STT: Anixis] is a daemon [STT: demon]" is only explanatory. Saying that "daemon [STT: demon]" is a retarded name doesn't mean that, for someone like a thinking machine that thinks in terms of what a daemon [STT: demon] is, to understand nexus, to say "is like a daemon [STT: demon]." Can you reconcile what I'm trying to say here?

-- psyche, STT.

## 2026-09-11 — the reconciled first heading is approved

Context: a comment on the review page, anchored on the proposed wording "A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is."

> yes, good

-- psyche, typed (artifact comment).
```
**Obs.:** crystallized: vision-nexus:8 (whole/daemon), :12 (kind of thing), :16-17 (library). The "nexus-core overthinking" / "signal gives main types, sema database types" record has no line in vision-nexus (it lives in vision/ethos.md per book 38 P3).

### D3. `flows/024bc7/vision/nexus.md` (2026-09-13)
```
## 2026-09-13 — The nexus layer describes processes that are ongoing; they are actors

Context: said while reviewing the whole-system view this flow presented. Transcription left as heard where the flow could not settle the word: "the etho subject description" and "assistant call" are unresolved and the living was asked.

> Okay, I just realized what the nexus is, and we need to reintroduce the nexus core language, the etho subject description.
>
> The nexus layer describes processes that are ongoing, like the operating system update operation or assistant call, basically something that has to lock. It's an actor. When you need something that locks, you get an actor because it has to be synchronous, so it's a process actor. All these objects that we're describing, the meta, the root objects, are actors. They start a process, a corresponding process. You could almost say that they're mirrors of each other.

-- psyche, STT.

## 2026-09-13 — The signal layer, the nexus layer, and the sema layer are described in ethos; the database stores that namespace

> Like I explained, you have the signal layer, the nexus layer, and the sema layer, and these are described in ethos. That's what that database is: it stores that namespace.

-- psyche, STT.

## 2026-09-13 — Three different layers of the runtime; decide on the language by beauty and correctness

> We approach this anatomically by describing what kind of objects we need and a problem with Signal, Nexus, and Sema. There are basically three different layers of the runtime:
> - The Nexus: the process or Nexus core, which is the process part.
> - The Sema: the storage part.
> - Signal: sending and receiving requests and responses or replies or whatever.
>
> We have to decide on the language, which words are best based on beauty and correctness.

-- psyche, STT.
```
**Obs.:** three-layer idea crystallized as Signal/Operation/Memory at vision-nexus:148 (names superseded). "Ongoing processes … actors / something that has to lock" — no line in vision-nexus.

### D4. `flows/bcd02a/vision/nexus.md` (2026-09-13)
```
## 2026-09-13 — The nexus layer

Context: The living is revising the Nexus model during a theoretical design discussion. Terminology such as “synchronous” and “process” remains to be clarified; this raw record does not settle their technical interpretation.

> The nexus layer describes processes that are ongoing, like the operating system update operation or assistant call, basically something that has to lock. It's an actor. When you need something that locks, you get an actor because it has to be synchronous, so it's a process actor. All these objects that we're describing, the meta, the root objects, are actors. They start a process, a corresponding process. You could almost say that they're mirrors of each other.

-- psyche, STT.
```
**Obs.:** duplicate of D3 first record. Not in vision-nexus.

### D5. `flows/bcd02a/notion/nexus.md` (notion, 2026-09-13)
```
## 2026-09-13 — A layer for storage

Context: Exploratory correspondence between process objects and storage; preserved without resolving the unfinished phrase.

> There's a layer for storage, and there's a layer. They're not necessarily one-to-one, right? Sometimes, but generally speaking, every concept is going to go all the way through a process and somewhere where it's recorded in storage, where some things can be maybe made more efficient in storage. That's what the nexus objects are.

-- psyche, STT.
```
**Obs.:** not in vision-nexus (closest: :148 one path).

### D6. `flows/6cc91b/vision/nexus.md` (2026-09-13/14)
```
## 2026-09-13 — A nexus that can create these attachments; no Python

Context: the living saw the reverse relay arrive through the pty injector written in Python by flow 024bc7 and asked why the nexus was not used.

> So, you didn't use the nexus, or maybe it was an ancestor to a nexus concept, because maybe the asynchronicity of the actor and the way it was written, I guess, made it impossible. There should be a way to have a nexus where it can create these attachments. Maybe, or should we just use Herder, because that was glitchy? I don't want to use Python.

-- psyche, STT.

## 2026-09-14 — Nexus the only main call, then Nexus loads up the signal; Forge doing everything cargo used to do

Context: comment on the gap "the nexus library is not the base of the nexuses". Asks to be shown what this could look like.

> Yeah, this is what I was saying in the other comment: we need to make Nexus sort of the only main call, and then Nexus loads up the signal. You can show me what you think this could look like, potentially. There's the whole cargo build system and all this to take into account: how each library is dispatched and how we want to make this deterministic and smart, so that we can reuse cargo but also create a system that is maybe more future-proof, oriented towards Forge essentially doing everything that cargo used to do more efficiently because it's more integrated, with source caching and everything.

-- psyche, typed, artifact comment.

## 2026-09-14 — Nexus, core, and metaNexus are the explicit terms; the core library guards that the signal actor never talks to the sema actor

Context: comment on the gap "almost nothing runs". "Sima" is speech-to-text for Sema; corrected in the quote. "demon" left as written.

> Yeah all these things have to be re-anatomized. Also I was thinking the Nexus core library could be how the signal actor, the Nexus actor, and the Sema actor (the main actors in a metaNexus, as we could call it, or the whole of what people call a demon) could be. If we want to be explicit we can say metaNexus and core Nexus but if we say Nexus we sort of have to let the context imply which one we are talking about. If the context isn't obvious then the speaker is blamed for not being clear enough: which part he means by Nexus.
>
> Nexus, core, and metaNexus are the explicit terms. The Nexus core library has all of the interfaces and kinds defined for how to build metaNexus and it has the machinery to make sure, ideally at compile time, that there is no signal-actor-to-sema-actor communication possible. All interaction between the signal actor has to go through the Nexus and then the Nexus ethos type file.
>
> We have this Nexus type, the sema type, and the signal type and they each have their own intrinsic kinds applied to the types so that they're of that specific actor. Only this kind of actor can react with this type of object. It's like a kind becomes a higher-type kind compiler check: an architecture guard basically.

-- psyche, typed, artifact comment.
```
**Obs.:** compile-time guard / only main call — not in vision-nexus (book 38 P18 proposes a standard entry point). metaNexus/core terms — not in vision-nexus; vision-nexus:148 says "Nexus always names the whole".

### D7. `flows/e1953c/vision/nexus.md` (commit 2026-09-14)
```
## Nexus objects describe the processes; "process" is implied by being a Nexus object, usable only with a Nexus meta-actor; the flow is the actor inside the runtime

Context: follows the Mesh answer in the same message.

> We can break processes into sub-processes, right? In the Nexus objects, you're going to describe all the processes. I don't think you need to say "process" all the time, but it's kind of included or implied by being a Nexus object, which means it can only be used with a Nexus meta-actor, meta-process, or meta-flow, basically. It's like the same concept as the flow is the actor inside the runtime.

-- psyche, STT.

## The metaNexus is the whole daemon; the Nexus, Sema, and Signal meta-actors each hold sub-actors that must run inside them; the trait enforces it at the compiler

Context: correction of this flow's reading of the previous entry. "SEMA" is speech-to-text for Sema, corrected in the quote; "demon" is left as transcribed, as the earlier nexus record left it. Ends with a question to be answered: whether the compiler can enforce the separation.

> Well, what I meant was that the MetaNexus is the whole demon, right? That is what we replace the concept of demon with. What I meant was that there's a meta actor also: the Nexus meta actor, the Sema, and the Signal. We talked about this, but we never actually reviewed it together: how the trait enforces that it can only be used inside of a particular meta actor, like either the Signal actor, the main Signal actor, or the Nexus actor. The Nexus actor, the Sema actor, and the Signal actor have their sub-actors, or possibly their implementations, that need to run inside these actors.
>
> We can prioritize which part of the three we should eventually be able to do, but also because it forces a certain part of the logic in a certain actor, where it's declared. We have the processes in the Nexus runtime that act as the only way to a Sema transformation. We separate the logics in the code, and we enforce it on the compiler. Is that possible?

-- psyche, STT.

## Effects are Nexus processes: Nexus encapsulates processes, internal algorithms or a wrapped command line like Nix, with an API around the CLI; eventually into Forge

Context: answer to the fourth Nexus core question (what happens to the fourth leg, effects). Speech-to-text corrected in the quote: "Logic shells out to Nex" for "Lojix shells out to Nix"; "SEMA" for Sema.

> Oh, I'm glad you asked that. What about effects? Lojix shells out to Nix. That's Nexus. Nexus encapsulates processes, whether they're internal algorithms running over data that got somehow by reading some signal archive or Sema database, or whether it's using a special command line like Nix. There could be many other things, and it maintains a sort of API around the CLI that wraps this Nexus process, like a Nix build, right? It is a Nexus process, maybe of the logics for now, but eventually we could put that into Forge. I don't know how deeply you want to go into this.

-- psyche, STT.

## Sub-processes are defined as more objects; a Nexus object that is an actor; a better term than "actor" may be wanted

Context: confirms this flow's reading that a long-running effect is a Nexus sub-process with its own sub-actor. Ends with a question, answered in the reply: what terms people who dislike "actor" have suggested.

> Yeah, no, exactly. You have sub-processes, so you define those as more objects, and you're going to have a certain kind of object, a nexus object that is an actor, basically. Maybe we even have to find a better term for that. What are some of the terms that some people who don't like the term "actor" have suggested?

-- psyche, STT.
```
**Obs.:** not in vision-nexus; vision-nexus:148 "Every effect has a matching operation type" is the nearest. These are the basis of «Flow: Nexus, ethos and design, 2nd» P9 (unruled).

### D8. `flows/05c604/vision/nexus.md` (commit 2026-09-15)
```
## The Nexus only gets Signal; the CLI translates datom into Signal; this must be clear in the skill and the vision

Context: correction of the primary's minimal Persona anatomy proposal, which said "one inline datom per call" at the Nexus socket. Logged directly by the main flow, before acting.

> Sorry, you're saying here I started reading proposal minimal persona, and you say one inline datom per call, but there's something wrong with that because the Nexus only gets signal. The CLI translates datom into signal, so that has to be clear everywhere in the skill, in the vision. It seems it isn't because you haven't gotten that right.

-- psyche, typed.
```
**Obs.:** crystallized: vision-nexus:56, :60.

### D9. `flows/b49251/vision/nexusAnatomy.md` (2026-09-16)
```
## Functionality may be put into a nexus and later moved into another once the best anatomy and where the data is kept are figured out; a function is offloaded somewhere while it still runs on the first nexus, ongoing support; all the data update infrastructure for that is to be developed, another topic

Context: typed to the primary Claude b49251 on 2026-09-16 evening, mid-turn, right after the psyche-flows and heartbeat message, while the flow was answering where the heartbeat and quota accounting live. Logged by the main flow before acting.

> Note that it's okay if we put functionality into a nexus and then later on move it into another nexus once we figure out the best anatomy for this and where the data is kept. It's going to allow us to offload a function somewhere while it's still running on the first nexus. You see what I mean? This ongoing support kind of thing. We have to develop all of the data update infrastructure structure for that, but that's another topic, I guess.

-- psyche, typed.
```
**Obs.:** partly at vision-nexus:129-134 (Splitting a Nexus); the "move while still running" / data-update infrastructure is not stated.

### D10. `flows/efa157/notion/nexusScaffolding.md` (notion, 2026-09-16)
Copied whole in the 23824a report §Creating nexuses; verbatim:
```
## A Nexus component that creates a new Nexus component, seen and edited through its Ethos; a hello-world Nexus and a blank Nexus with the default kinds; the Nexus creates and tracks the repositories; the signal edited through the CLI; a subscription to a component build through Forge with its tests and outputs, Nix jobs behind it, some stateful with virtual machines; private test material in a private repository, nothing personal in the general one; those jobs run from a machine with the right key

Context: typed to the primary Claude efa157 on 2026-09-16 at 17:0xZ, framed by the living as "this crazy vision that just came to me, so I'm just going to jot it down", so logged as notion. Its closing lines (keep pushing what makes the refresh possible) are a working instruction, recorded in log.md. "Next" reads Nix, "lee" reads li, left as typed. Logged by the main flow verbatim.

> You have the Nexus component that you can call to create a new Nexus component, and then you can use Ethos to see it and edit its Ethos so it gets a default. Like, a Nexus that can say "hello," for example, with its name, its component name, or whatever, and then create a database for whatever. It's just a toy: it creates a database with the message that it gets when somebody sends a "hello." It takes the strings and stores that with the time or whatever. It just shows you, or maybe it has almost nothing.
>
> Anyway, you have different types:
> - hello world Nexus create
> - just blank Nexus create, which has just the default kinds that are in a Nexus
>
> The Nexus can create the repositories that are needed for that and keep track of where they are when they are generated. We'll be able to just start interacting directly through the CLI to even edit the Ethos side of things, like the signal. You're going to call signal to edit the signal, and then it can give you a subscription to a particular component build, like in that. That should be Forge that does the build, and so it gets a subscription for when that build passes through with the tests and what came out. Behind that is all the Nix jobs running, and then some of them can run stateful Nix jobs.
>
> In lojix, we have that on top. We build everything with Next, and then we have this thing, this executable that gets run, or this shell command, system call per test or whatever. It can run these more stateful tests that can have some permission, like these virtual machines that we run. It's just that we need to keep the private stuff somehow in a private repository for these tests if they're run on my own machine. If there is nothing that identifies it to me, but if it's like `home/home/lee`, that identifies it to me. If it's just a general home environment, standard path for where the Codex subscription tokens are, that's fine. We can generalize that, universalize that. It's just nothing personal, and then we use a personal repository.
>
> That means those jobs have to be run from a machine that has access to the server with the right SSH key, I guess, or however Nix does private repositories.

-- psyche, typed.
```
**Obs.:** not in vision-nexus.

### D11. `flows/48cff7/vision/transcriptNexus.md` (2026-09-16), the kind-level lines
```
## 2026-09-16 — the transcript component is misimplemented; make it a nexus, with datom-syntax CLIs

Context: while refining the anchor-extract flowchart, the living named the transcript component as misimplemented and set the remedy in one line.

> The transcript component is misimplemented. We need to make a nexus out of it and use datom syntax with the CLIs.

-- psyche, typed.

## 2026-09-16 — it needs to be a nexus with Signal and datom syntax only

> It needs to be a nexus with Signal and Datom syntax only.

-- psyche, typed.
```
**Obs.:** matches vision-nexus:56, :60, :120.

### D12. `flows/d9961c/notion/harnessNexus.md` (notion, 2026-09-17)
```
## 2026-09-17 — a debug interface to type into the harness; each harness its own Nexus

Context: the living could not see Primary Psyche Medium in remote sessions and asked to restore Remote Control. The following is explicitly exploratory (“Maybe I think”), retained as Notion, not implementation authorization.

> Do we have an interface for that? We should have an interface to type into, like a debug interface, just to type in that harness. Maybe I think every different harness should have its own nexus to interact with it. That way, we can change how a harness behaves without restarting the whole harness stack.

-- psyche, typed.
```
**Obs.:** kind-level point "change behaviour without restarting the whole stack" ≈ vision-nexus:134 (runs and recompiled on its own).

### D13. `flows/b81560/vision/operational-nexusProcessObjectsAndEthosInDatom.md` (2026-09-19)
```
> So, the Nexus: it's too bad I lost this whole thing. The Nexus process objects are the ones that process everything that goes, and the main function is standard. That's why we have to force certain things, and the project has to use the ethos specs. The spec for the objects is the Nexus, and you have to call a Nexus object from signal. It has to go through a process, and that process is the implementation that gets written. It could involve a subflow, calling a subflow that's trying to use this spec. It's given the spec and a few examples of what should happen in a spec datom type, root message. Eventually, that's the vision.
>
> We can just make it simple for now: give it the spec of what it's expected to say and a few examples, and explain in prose, in a markdown thing, and then tell it, "Okay, now we switch to this spec." Then it starts to program it in datom for the rest of the system prompt. It expects it to respond with the spec of the types of responses it's supposed to be giving back, right? If it misresponds, it tries to correct it and tell it which part of the spec it's violating.
>
> We need better error messages that can be generated automatically because of the way we've created ethos, the structure, and all of that. [...continues on error messages and ethos-in-datom escaping...]

-- psyche, direct to primary Psyche opus b81560.
```
(Heading: "Operational: Nexus process objects implement specs, ethos specs in datom payloads, structured error messages from parsing, and ethos-in-datom escaping"; date 2026-09-19 per context.) **Obs.:** "main function is standard" not in vision-nexus (book 38 P18). Machine-call operation: posed as «The Nexus» rulings item 6, no answer recorded.

### D14. `flows/b05237/vision/operational-datomLanguageForNexusClis.md` (2026-09-19)
```
> We're going to start programming all of this. A lot of automation will eventually overtake some of what the models are asked to do now. We can lean on the models for now and then add more logic to make their jobs easier. Developing the language is how we make this all more efficient: the Datom language that all the CLIs for the nexuses are going to use.

-- psyche, direct to Psyche Fable, subflow of b05237; input mode not stated.
```
**Obs.:** ≈ vision-nexus:50-51, :56.

### D15. `flows/b80e55/vision/fieldNexusSystemQuery.md` (2026-09-20), kind-level sentence
```
> Get a full report. This would be a script that gets ported eventually to the field nexus. Functionality for the field means querying stuff about the system, any kinds of stuff. We could even put all the transcript stuff in there, unless we keep that as a separate nexus, which the field could also access to expose the same functionality or to enhance its own. Here we see the concept of either reusing another Nexus or merging a function of it, basically aggregating or splitting up functionality.

-- psyche, direct to Psyche Medium b80e55. Input mode not established.
```
**Obs.:** splitting at vision-nexus:131-132; reusing/merging (aggregating) not stated.

### D16. `flows/b80e55/vision/nexusComponentDeploymentAndTriadRoles.md` (2026-09-20)
```
> Make that all operational: mind-based skill, and get the mind started. All four powers on bringing up all of the nexus components to run the flow and the messages properly so that you can deploy it I mean, so that Field can deploy it: you design it with Mind, the Mind makes it, and then we deploy it.

-- psyche, direct to Psyche Medium b80e55. Input mode not established.
```
**Obs.:** process, not kind; not in vision-nexus.

### D17. `flows/836818/vision/nexusAnatomy.md` (2026-09-23)
```
# Designing the Flow and the Message, and the infrastructure around them

> Ask me questions to design everything with the flow and the message. Let's get this new infrastructure up:
>
> - the persona
> - all of the nexuses
> - the main nexuses
> - how they fit with each other
> - how they interact with each other
>
> The message highly depends on flow and probably many things will then depend on message.

-- psyche, typed, 2026-09-23, directly to Psyche High 836818 over Remote Control. Transcript locator: this seat's native session, the first living turn after the concept-plate review (line to be fixed by a locator subflow).
```
**Obs.:** graph at vision-nexus:70-77 in general form.

### D18. `flows/e51411/vision/nexus.md` (2026-09-25) and duplicate `flows/88475f/vision/nexus.md`
```
## The tools are the nexuses; Psyche Nexus and Mind Nexus replace how we log and how each aspect interacts with the system

Context: the living asked for Fable to be refreshed with its presentations and raw psyche, noting they had spoken to it in many places.

> I've spoken to it in a lot of places. I guess we need better tools. We know what the tools are, right? They're the nexuses.
>
> Psyche Nexus is going to replace how we log Psyche and Mind. Mind Nexus is going to replace how we log the Mind and the field, not just log, but how the Mind interacts with the system, how the field interacts with the system, and how Psyche interacts with the system. Those are the solutions we want to start using and developing but we have to be realistic.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411. Reading note, inference: "log Psyche and Mind" may be a slip for "log Psyche". Unconfirmed, so the quote is left as received.

## Finish the design: everything unclear about the nexuses, including record changes and database upgrades

> If you need a refresh we need to go fully on finishing the design.
>
> Anything that's not clear about all of the nexuses and specifically flow and message not getting working, but also everything else. Obviously Psyche, Mind, and Field are also really important and probably persona to start managing all this. We're going to need to handle database upgrades or the database when the records change. We're going to need to specify a better way do that

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411. The message ends mid-sentence.
```
(88475f: "## The tools are the nexuses" — "Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on the nexuses." same words, "-- psyche, relayed by e51411 (original channel not stated).")
**Obs.:** "tools are the nexuses" ≈ vision-nexus:120. Database upgrades on record change — not in vision-nexus.

### D19. `flows/5578cc/notion/nexus.md` (notion, 2026-10-03)
```
## How a Nexus sends datom without knowing datom

Context: same message, after asking whether Flow can launch sessions and carry the session title as a real type.

> I guess we need to talk about that: how does Nexus send datom to places without needing to know how to deserialize and serialize datom itself? Interesting.

-- psyche, typed, 2026-10-03, to Psyche Opus 5578cc.
```
**Obs.:** open question; vision-nexus:56 says datom is compiled out; mechanism not stated.

### D20. `flows/28d847/vision/nexus.md` (commit 2026-10-03; relay dates the words 2026-10-04) and `flows/5ed94b/vision/nexusEntryPoint.md` (2026-10-04, same words)
```
## A standard entry point that enforces the nexus's three parts

> I want to talk more about how a nexus has three parts and make sure that it is effective and that we use maybe even some kind of standard main flow, like a macro in Rust, as some way for the whole machinery to enforce its own invariance so that the rest doesn't bypass it.

> That has been an idea of mine that I've been trying to put into practice: if we use something like a macro or a standard entry point for the main executable or the entry point of the library (or whatever it is), then we can control some properties of the system. For example the idea is that the signal has to go through the operation actor/system in order to reach the memory actor/system, then back through the operation system and back out through the signal. That way we can see the main objects and processes that are involved by just looking at the ethos code, which defines the types that are involved in this flow.

> If that can somehow be enforced in Rust through the way we write the Rust and then we leave the implementation side to be written by hand, then you can have effective compliance with ethos.

-- psyche, typed.
```
(5ed94b provenance: "-- psyche, typed, 2026-10-04, relayed by 28d847 to flow 5ed94b.")
**Obs.:** path crystallized at vision-nexus:148; the entry point/macro is not (book 38 P18 line 2).

### D21. `flows/aa887c/vision/nexus.md` (2026-10-04) and duplicate `flows/bad807/vision/nexus.md`
```
## The three parts and one path land, with example code

Context: his comment on the book «The Nexus», proposal 1 (Vision/nexus.md, new section "Three parts and one path").

> This is good. Can land, and I would also like to have example code to show with it.

-- psyche, STT.

## Signal and memory talk only to operation

Context: his comment on the book «The Nexus», proposal 2 (Vision/nexus.md, new section "The standard entry point").

> Let's flesh this out in actual code. Could we say it better: an actor, a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor, which could talk to both signal and memory. Operations can talk to both. Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process.
>
> Let's look at the actual code and how this could be done in multiple various ways. Let's test it. Let's have it tested on an actual component that we have written, like Flow, Message [sic], or Orchestrate, on a branch, and see if it works as the other component or if we could make it work. A toy, I mean, or a simple nexus which isn't in production, something that we've been drafting.
>
> Maybe let's do something useful. If we're going to test anything, we might as well test one of our non-production-ready ideas. You can hand this over to Astra once you have the design and the book. I want extensive: I want to see code. I want to see visual architecture. I want to feel like you have some meat there on that bone.

-- psyche, STT.

## The core library's language refined after practice

Context: his comment on the book «The Nexus», on the proposed text "The nexus repository is the core library of every Nexus…".

> Again after we see how this works in practice, let's refine the language so that it's more accurate to what's possible and what we actually want in practice. In terms of whether it is an actor-based language or whether it is different

-- psyche, STT.

## A Nexus pulls a value from a datom file

Context: his comment on the book «The Nexus», on the proposed text "Every client speaks to a Nexus in pure signal, fully binary…".

> Yes this is good and I also want to design something that would let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this but it would be a fairly simple call, I guess, where it would have a variant `me` [sic] that would tell it what type of CLI you would have to use, essentially. That means storing a string somewhere because the CLI is invoked with a system call that uses a string. There's a string involved no matter what unless all of that is, again, put into an external tool. Anyway let's look at different ideas here, with Fable being the lead designer on this and passing it down as a book.

-- psyche, STT.
```
(bad807 copy gives provenance "-- psyche, typed, book comment, 2026-10-04, relayed by aa887c." — **Obs.:** STT vs typed disagree between the two logs.)
**Obs.:** record 1 landed (vision-nexus:146-197). "Signal and memory only to operation": not stated as edges (book 38 P17 line 2). Actor question: vision-nexus:126 still asserts Kameo. Datom-file pull: not in vision-nexus (book 38 P21 line 3).

### D22. `flows/d4ae97/vision/nexus.md` (2026-10-07)
```
## Every Nexus has Signal, Operation and Memory
> I'd like to get an overview of all the ethos code that is now in curriculum, in all aspects, meaning signal, operation, and memory. All nexuses have to have all three. Maybe that is something we need to add into the vision, which is now.

-- psyche, STT, 2026-10-07.
```
**Obs.:** vision-nexus:148 "A Nexus has three parts" — says the same.

### D23. `flows/73ada7/vision/nexus.md` (2026-10-09)
```
## 2026-10-09 — File location does not matter to a Nexus: a registry keyed by subaspect and topic holds each source's hash and relative path; changes ride the meta signal; Curriculum checks the hash per operation

Context: the living's comment on «The golden ethos», 3rd ed. (https://claude.ai/artifact/UG93sbmAyxoyS7wRF4gP1Q, thread babadeae), anchored at "psyche-skills/skills/vision-ethos.md". Not logged by the flow it was addressed to; found and logged here. Only the words bearing on the Nexus are quoted; the working instruction to Astra and the Ethos syntax that follows are left out.

> ... the file location shouldnt matter from the nexus' pov; it must use a registry which uses the `{ Subaspect.[Vision Knowledge ...] Topic:Name }` to store the location of each, using the containing source with hash (blake3 I believe is what we use?) and relative path of each. those payloads live on the meta signal (to modify those registries). curriculum can have the capacity to get/check the hash when the query come in, according to the operation (write or read).

-- psyche, STT, book comment, 2026-10-09T20:07.

## 2026-10-09 — A Nexus's configuration loads atomically from separate files in different repositories: datom payloads the CLI sends in succession on the meta socket to start it

Context: the living's comment on «The new flows, as they run» (thread 51c6241f, 20:41), relayed in part by 445410. The closing order ("Let's do this.") is left out.

> Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant.

-- psyche, STT, book comment, 2026-10-09T20:41, relayed by 445410.
```
**Obs.:** "file location shouldn't matter; registry changes ride the meta signal" — not in vision-nexus (closest :42 config through meta socket). Configuration record — not in vision-nexus (book 38 P16/P23).

### D24. `flows/445410/vision/nexus.md` (2026-10-09), same configuration record, full closing
```
## Nexus configuration loaded atomically from files

Context: the living's comment on «The new flows, as they run» (thread 51c6241f, 2026-10-09 20:41), on the passage "Flow Nexus sockets exist; the inspected launcher source does not call them".

> Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant. Let's do this. Get this ratified, and then [Mind]. Let's get [Mind] making this on Astra on its own, even Astra and Sol topic flow.

-- psyche, STT, 2026-10-09. Transcription corrected: "mine" → "Mind".
```
Duplicates: `flows/0c85a3/vision/nexus-configuration.md` ("## Configuration loaded atomically — 2026-10-09", "-- psyche, relayed via445410 and41fa34; original input method unspecified."), `flows/9fed42/vision/flow.md:25`, `flows/f5a6e9/vision/flow.md:143`. **Obs.:** not in vision-nexus; :89-94 says no arguments, default constant, Configure on meta socket.

### D25. `flows/875960/vision/nexus.md` (2026-10-12) and `flows/9519a1/vision/nexus.md` (2026-10-12)
```
## 2026-10-12 — the Nexus parts are the machine anatomy; one good nexus first, Flow

Context: relayed by core d68c82 through 9519a1; bears on «Flow, whole, in ethos» and the Flow Nexus build.

> I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more. I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. Let's do that.

-- psyche, STT, relayed.
```
(9519a1: "Relayed by core Secondary d68c82, 2026-10-12." same words ending "...", "-- psyche, STT.")
**Obs.:** not in vision-nexus (book 38 P18 line 1; r-nexus-ethos-design P13).

### D26. `flows/d68c82/vision/nexus.md` (2026-10-14)
```
## 2026-10-14 — Chronos as the Nexus test

> Also let's use the most usable component that works best for testing the Nexus component but I guess something actually really simple. Maybe we re-adapt Chronos, the tool I had made to get astrological time based on current time or based on a specific time and location. Let's rewrite it in idiomatic Nexus architecture and ethos: full specification, just a simple thing, right?

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.
```
**Obs.:** not in vision-nexus (book 38 P20, vision-chronos).

### D27. `flows/23824a/vision/ethosNexus.md` (2026-10-10)
```
## Ethos specifies the three aspects of the Ethos Nexus

Context: comment on «Sources and the registry», proposal 2, relayed by d68c82, 2026-10-10. The question beside it ("do we have an Ethos Nexus or is Ethos Zero a non-Nexus?") is answered, not logged.

> We need to migrate the Ethos Nexus version so that we can do this. In Ethos I want to specify the three aspects:
> - the signal
> - the memory
> - the operation
>
> ... This will be used to put together a registry and it'll just keep it. Every time we update some Ethos source, add one, or edit its name or something, we need to change the registry.

-- psyche, STT, relayed by d68c82.
```
**Obs.:** ethos-nexus named at vision-nexus:8 only; book 38 P10.

### D28. `flows/d68c82/notion/ethos.md:20` (notion, 2026-10-14) — from the 23824a report
```
#### Clojure generation in Ethos; a Nexus implementation of the Ethos Nexus
Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «The Flow Nexus», Proposal 2, after the diff comments.

> Eventually we could even have, maybe next week when we have more usage, let's put in a notion of bringing [Clojure] generation into ethos. This could also be done by switching to a Nexus implementation of Nexus of Ethos, which I think would simplify some things like keeping the library in memory. That way we have a clean system for code module access: index, like canonical namespace from the running Nexus, which can load it from multiple repos as we describe with the incremental configuration approach.

-- psyche, STT. Transcription corrected: "closure generation" → "Clojure generation".
```
**Obs.:** "incremental configuration approach" reuses D24; not in vision-nexus.

### D29. Other report records on the Nexus as a kind (from `flows/23824a/reports/ethos-nexus-chronos-psyche.md`)
- `flows/91ea9f/vision/ethos.md:3` (2026-10-02): "\"Let's also look at ethos more in depth because I want to be able to start designing with it so we can have the signal, the process, and the storage. Maybe we call it the process instead of these convoluted terms. Plus nexus is overloaded because it means the daemon and also the central process actor. I'm not a big fan of storage but something that emphasizes the kinds of things that are memorized, as in a database, but maybe with a better concept vocabulary.\"" -- psyche, typed, 2026-10-02. **Obs.:** resolved at vision-nexus:148 ("Nexus always names the whole; the part that does is Operation").
- `flows/91ea9f/vision/ethos.md:36` (2026-10-02), the Nexus paragraph: "Yeah the memory is good. That's what it is I guess: signal, operation, and memory. / When we define its operation we define all of the operation types. … Anything that can have an effect is going to have a corresponding operation … If the memory has changed and there is a successful memory edit kind of return operation, that's going to end with a signal … We're going to have to have, I guess, an implementation on the memory kind. It's going to be a kind that's going to have a standard successful or unsuccessful change implemented on these particular data types. Also each version is possibly going to have an implementation of an upgrade from or an upgrade to. … That operation is going to be the very edit, the very update operation that this particular data type needs to change into its new memory format." (full text in report lines 2011-2019) -- psyche, typed, 2026-10-02, book comments on «Flow in ethos». **Obs.:** path at vision-nexus:148; memory-version upgrade/migration not in vision-nexus.
- `flows/edf227/vision/identifiers.md:9` (2026-10-03): "\"The flow ID is not a string, it's a hash. … I would like this to be a serialization and deserialization thing so that it's not actually in the Nexus. The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits. …\"" -- psyche, STT, 2026-10-03. **Obs.:** vision-nexus:153 `FlowId.Integer`; :25 identity is trait-borne.
- `flows/edf227/vision/signalForms.md:3` (2026-10-03): "\"This is a different representation of the same fundamental data. ... The simplified version is the part that doesn't have the flow ID. … This is defined in ethos somewhere in signal as different types of formats that communication can happen in … the more extended version will be for the more technical side … mostly used for either debugging or for other components …\"" -- psyche, typed, book comment, 2026-10-03T18:01Z, relayed by 6e782c. **Obs.:** not in vision-nexus (book 38 P18 line 4).
- `flows/8475a9/vision/datom.md:25` (2026-10-05): "## No datom in any Nexus; string handling in a Nexus is forbidden / Context: his comment on the drawing's box «Nexus: no Expander, so @ is Forbidden». Relayed by 8f0f57. / > Well the Nexus has no datom so expand [it]. It doesn't even have datom. There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus. / -- psyche, STT, book comment, 2026-10-05." **Obs.:** ≈ vision-nexus:56, :66.
- `flows/d4ae97/vision/ethos.md:97` (2026-10-06): "This is an interesting concept and I think it belongs in operation ethos as the main operation. Maybe \"operation\" is the right term. Maybe it's \"actor\" or maybe there's something in between: \"process.\" …" -- psyche, comment on «The code» 1st edition, 2026-10-06. **Obs.:** not in vision-nexus.
- `flows/0c85a3/notion/memory.md:2` (notion, 2026-10-07): "Context: Tentative architectural distinction; precise boundaries remain to be distilled. / > In the case of the memory, everything goes into the nexus but the CLI, I think, only uses the signal and the other consumers that talk to that nexus. / -- psyche, STT, 2026-10-07." **Obs.:** ≈ vision-nexus:77, :114 (CLI depends on wire repos).
- `flows/d68c82/vision/naming.md:3` (word check): "That would need a dedicated Nexus because it would need to have a database of words. …" **Obs.:** not in vision-nexus.
- `flows/da2038/vision/pod.md:2` (2026-10-14): "… There's this simple operation, the meta pod. I guess it has this data structure with permission for who can access. You can have different levels of access. Eventually we won't even need different sockets. You might as well have different sockets but you'll also be able to know who called the socket so that you'll be able to verify authentication through the master process. …" -- psyche, STT, 2026-10-14. **Obs.:** bears on vision-nexus:44 ("A Nexus that needs more levels of access opens more sockets").
- `flows/d68c82/vision/deployment.md:29` (2026-10-13): "… I want to move towards using the nexuses everywhere. They're the long-term vision and then we have this short-term mission. …" **Obs.:** ≈ vision-nexus:120; long/short not stated (book 38 P18 line 5).
- `flows/d68c82/vision/tools.md:14` (2026-10-14): "## 2026-10-14 — a repeated use case grows an existing tool; EDN in Clojure, datom in Nexus / > Anything that can be abstracted so that it's reused. If we see a use case repeat itself, then we should try to adapt whatever tool we already have to become more capable and broad. If we're in Clojure we use an EDN payload for everything and if we're in Nexus we use a datom. / -- psyche, STT." **Obs.:** not in vision-nexus (book 38 P12/P21).

### D30. `flows/*/vision/flow.md` entries concerning the Nexus as a kind
- `flows/33752b/vision/flow.md:29` (2026-10-13; dup `flows/d68c82/vision/flow.md:76` "## The short term and the long term are not mixed"):
```
## "Meta socket" in the short-term proposal is not understood; the short-term solution is not the Nexus

Context: comment on the same book, Proposal 2, at "sent to Flow as configuration payloads on its meta socket". The word in brackets is the relaying seat's correction.

> What do you mean by meta socket? I don't understand. You're talking about meta sockets, which have to do with nexus, and then you're talking about the short-term solution, which is [Clojure]. Total fucking confusion here. Hallucinating model, now I don't trust anything you're saying or any system you've made. In this department I'm afraid that the current code or the current proposal is fucked.

-- psyche, STT, 2026-10-13.
```
**Obs.:** not in vision-nexus (book 38 P16 line 3).
- `flows/875960/vision/flow.md` (2026-10-12, comment 4, 16:21; Context: "comment 4 sits on the process object («Instant») in Flow's Library in the ethos file"):
```
> I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing. Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further. We should get Mind to put together a concept that can test whether or not this can actually work using Ethos and everything. We can test it on Flow. Let's give free rein to Fable and Astra to design something like this and implement it. Flow isn't even on in production so I'm not even worried about merging more into main. I'm also curious why we haven't been able to start using Flow Nexus so far, even though it's been a month or something, so I'd like to get an investigation on that.

-- psyche, STT, 16:21, relayed by 9519a1.
```
**Obs.:** caller identity at vision-nexus:56; the shared library is not (book 38 P24).
- `flows/9519a1/vision/flow.md` (2026-10-11 20:32) / `875960` comment 6:
```
> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT. Transcription corrected: "idea" → "ID".
```
**Obs.:** = vision-nexus:56 "never by a claim".
- `flows/9519a1/vision/flow.md` (2026-10-11 20:23) kind-relevant sentence: "> … The topic could be in the flow nexus for now but maybe at some point in another nexus. …" -- psyche, STT. **Obs.:** ≈ vision-nexus:129-132.
- `flows/d68c82/vision/flow.md:103` (2026-10-14):
```
## 2026-10-14 — Flow, Nexus and Ethos together; Flow is the bootstrap

> We're developing the Flow, the Nexus architecture, and Ethos at the same time. There are three aspects, right?
> - the language aspect
> - the runtime architecture
> - that component itself, [Flow], which is probably the most important component to bootstrap
>
> Bootstrap persona, the meta harness, since starting flows like clean lean flows, specialized flows, or refreshing flows is a central part, a cornerstone, of this system.

-- psyche, STT. Transcription corrected: "low" → "Flow".
```
**Obs.:** not in vision-nexus (book 38 P18 line 3).
- `flows/d68c82/vision/flow.md:130` (2026-10-14; dup `flows/da2038/vision/flow.md:26`):
```
## 2026-10-14 — A full Flow Nexus proposal, short-term and long-term

Context: spoken to the Psyche Core Tertiary after commenting on «Flow: CLI, deployment, long term», 2nd edition; relayed.

> I need to see a full Flow Nexus proposal, also probably separately.
>
> Let's have the short-term version and then the long-term/universal version: the parts that are independent of whether or not it's short-term or long-term, like the overall intention of the design, which is going to live in the long-term/Nexus proposal. We focus on specifying the ethos and from the ethos we already talked about the fact that we're going to derive the short-term prototype code.

-- psyche, STT.
```
**Obs.:** not in vision-nexus (book 38 P18 line 5).
- `flows/d68c82/vision/flow.md` "## A subflow's kind depends on its use" (2026-10-14, relayed 10-15), third bullet: "> - The field CLJ/CLI prototype that is based on an emulated Nexus architecture of EDN payloads, so that essentially everything can be written as one or the other configuration of an Ethos-based specification language in EDN off the bat (with basic Clojure architecture and stack), which is really easy to code on, deploy, and for machines to think in terms of an analog to [protobuf]-like language." -- psyche, STT. **Obs.:** not in vision-nexus.
- `flows/d68c82/vision/flow.md` "## 2026-10-16 11:25 Roles defined as datom data in their own repository": "\"These roles are going to get defined in role definition files with datom syntax on an ethos-specific specified object. As if we were creating payloads for the Flow Nexus, we're creating all of this data. …\"" -- psyche, typed. **Obs.:** payloads in datom ≈ book 38 P21 line 2.
- `flows/edf227/vision/flow.md:14` (2026-10-03 18:13):
```
## Flow's configuration lives in its own database and memory, not in Markdown files
At "the model behind a layer is configuration in a knowledge skill".
> "No the configuration flow does not live in a Markdown file in every story. It lives in its own database and its memory. That's where the configuration goes so this is a hallucination by mixing up concepts that don't belong within this report."

-- psyche, typed, book comment, 2026-10-03 18:13. Transcription uncertain: "in every story".
```
**Obs.:** = vision-nexus:66, :91-92 (configuration in the store).

Not copied (Flow-, Message- or component-specific rather than the kind): `flows/*/vision/flowNexus.md` (01e496, 1b8ac0, 836818, 91ea9f, c64ee3, fe945a), `b7da5d/vision/flowNexusUse.md`, `9993b5/vision/curriculumNexus.md`, `9993b5/vision/editNexusName.md`, `6fb948/vision/personaServiceAndNexusImagery-20260923.md`, `875960/vision/flow.md:39` (Flow owns the lock), `da2038/vision/flow.md:122` (no idle harness). Skipped as archive-: all `archive-*nexus*` files.

---

## E. Later statements that correct or contradict earlier ones (same subject)

1. **What "Nexus" names**
   - Earlier: fe34eb 2026-09-10 "a nexus is a daemon … the nexus repo is the library that defines the core of a nexus component"; approved heading 09-11 "A Nexus is the whole long-running component" (vision-nexus:8).
   - Later: 6cc91b 2026-09-14 "Nexus, core, and metaNexus are the explicit terms"; e1953c "the MetaNexus is the whole demon … That is what we replace the concept of demon with."
   - Later still: 91ea9f 2026-10-02 "nexus is overloaded because it means the daemon and also the central process actor" → vision-nexus:148 "Nexus always names the whole".
2. **Nexus core / process layer**
   - fe34eb 2026-09-10: "I was overthinking the whole 'nexus-core' runtime concept … signal … sema."
   - 024bc7 2026-09-13: "we need to reintroduce the nexus core language" and three layers Nexus/Sema/Signal.
   - 91ea9f 2026-10-02: "Maybe we call it the process" → same day "signal, operation, and memory"; d4ae97 2026-10-06 "Maybe 'operation' is the right term. Maybe it's 'actor' or … 'process.'"
3. **Storage part's name: Sema → Memory**
   - Earlier: 024bc7 09-13, fe34eb 09-10 "sema types"; vision-nexus:22, :35, :91 still say sema/Sema.
   - Later: 91ea9f 2026-10-02 "Yeah the memory is good"; vision-nexus:66, :148 say Memory. (Book 38 P23 renames :91; :22 and :35 untouched by any book-38 proposal — **Obs.**)
4. **Actors**
   - 024bc7/bcd02a 09-13 "It's an actor … process actor"; 6cc91b/e1953c 09-14 meta-actors and sub-actors; vision-nexus:126 "driven by Kameo actors".
   - aa887c 2026-10-04: refine after practice "whether it is an actor-based language or whether it is different"; e1953c 09-14 "Maybe we even have to find a better term for that".
   - Book conflict (unruled both): book 38 P17 removes Kameo and leaves actor-or-not open; «Flow: Nexus, ethos and design, 2nd» P9 proposes "A Nexus object runs only inside a Nexus meta-actor … a Nexus object that is an actor".
5. **Datom/text inside a Nexus**
   - 05c604 (09-15) "the Nexus only gets signal"; edf227 10-03 text forms "not actually in the Nexus"; 8475a9 2026-10-05 "There should be no datom in any Nexus".
   - aa887c 2026-10-04 a Nexus pulls a datom-file value via its CLI ("There's a string involved no matter what").
   - d68c82/tools.md 2026-10-14 "if we're in Nexus we use a datom".
   - Book 38 P12 reads 10-14 as superseding 10-05; P21 (Fable) reads them as compatible. **Unruled.**
6. **Configuration**
   - vision-nexus:89-94: no arguments, default constant, Sema database, Configure on meta socket.
   - 445410/73ada7 2026-10-09: configuration loaded atomically from datom payload files in several repos, sent by the CLI in succession on the meta socket — "a hack to get the Nexus started".
   - 33752b 2026-10-13: meta socket belongs to the Nexus, not the Clojure short-term solution.
   - Overlapping unruled texts: book 38 P16 + P23; «Flow: Nexus, ethos and design, 2nd» P10 (adds a registry populated the same way).
7. **Levels of access**
   - vision-nexus:44 "A Nexus that needs more levels of access opens more sockets."
   - da2038/vision/pod.md 2026-10-14: "Eventually we won't even need different sockets. You might as well have different sockets but you'll also be able to know who called the socket …"
8. **Voice**
   - aa887c/his-comments #5, 2026-10-04: "I think rather the voice is a struct that contains the aspect and the layer"; vision-nexus:154.
   - 875960/9519a1 2026-10-11: "we've gotten rid of the voice concept. Now it's just replaced by the core topic." (book 38 P14).
9. **Flow id type**
   - vision-nexus:153 `FlowId.Integer`; edf227 2026-10-03 "The flow ID is not a string, it's a hash."
   - ebbe30 2026-10-09 "Let's just leave it as a string for now, but … the string is very unideal".
   - 9519a1 2026-10-11 20:25: "We need the hash from the harness so we have to start the harness before we get the flow ID … We've been using the session ID hash". (Book 38 P13.)
10. **Kinds vs traits**
    - 26c50c "Yeah I meant kinds not traits. If I say traits I mean kinds."
    - ebbe30 2026-10-09 "although the kind has been changed to trait"; and ebbe30:29 "kind might be used to also mean traits." vision-nexus:158 `; kinds` (book 38 P15).
11. **Where the word check / identifier lives**
    - d68c82/vision/naming.md: "That would need a dedicated Nexus because it would need to have a database of words."
    - 875960 2026-10-12: "It would go in some kind of shared library, maybe the [protos] library".
12. **Which example comes first**
    - d68c82/design.md 2026-10-12 / 875960/nexus.md: "one good nexus … then the flow nexus is the most needed".
    - d68c82/nexus.md 2026-10-14: Chronos as the Nexus test; 7c89aa 2026-10-16: Ethos + Nexus + Chronos golden example "to implement Flow properly and then other nexuses."
13. **Book-level conflicts recorded by d68c82 (log:1995)**
    - «The Flow Nexus, whole, 2nd» P9 removes the Flow example from vision-nexus (replaces with a pointer to flow-ethos and a new path example using `{ Psyche nexus Primary }`, `Compose`, `StartFlow`, `Metaflow`, `quietRiverStone`), while book 38 P13–P15 edit lines inside that same example. Both unruled.
    - vision-chronos path differs: book 38 P20 `skills/vision-chronos.md`; «Chronos, 3rd» `vision/chronos.md`.
14. **Provenance disagreement (Obs.)** — the 2026-10-04 «The Nexus» comments are logged as "STT" in aa887c/vision/nexus.md and as "typed, book comment" in bad807/vision/nexus.md.
15. **Within the same speaker turn (fe34eb 2026-09-10)** — "a nexus is a daemon" then "'A Nexus is a daemon' is only explanatory"; reconciled and approved 09-11 (vision-nexus:8).

### Inferences (kept separate)
- **Inf.:** vision-nexus:21-23 and :35 still use "sema" for the stored part; if Memory is adopted (as :66/:148 already do), those lines are also candidates, though no current proposal touches them.
- **Inf.:** vision-nexus:126 (Kameo) is the line most directly contradicted by the living's later word (aa887c 10-04), and two unruled books propose opposite directions for it.
- **Inf.:** the Flow example (vision-nexus:150-197) is now targeted by four unruled proposals across two books (book 38 P13/P14/P15; Flow Nexus whole 2nd P9); a single ruling will be needed to avoid collision.

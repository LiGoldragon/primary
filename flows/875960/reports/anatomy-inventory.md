# Anatomy inventory: Flow's fourth-edition ethos against vision

Abbreviations. B7 = flows/875960/books/7-flow-whole-ethos-4.md (line). B8 = flows/875960/books/8-caller-witnessed.md (line). VF = psyche-skills skills/vision-flow.md at 9bba4bf, the authored source (line); the generated .claude/skills/vision-flow lacks VF:18–22. VN = vision-nexus (line). VE = vision-ethos (heading or line). VMR = vision-model-roles (line). VM = vision-messaging (heading). DZ = flows/f5a6e9/reports/flow-buildable-design.md. DF/DN/DE = flows/875960/reports/digest-flow/-nexus/-ethos.md (line). EZ17 = the ethos-zero 17.0.0 build at /nix/store/hf62sq…-ethos-zero-17.0.0, which I ran in a probe (witness). "inf." = this flow's inference.

## A. Types

| root / section | type | what it is | vision line served |
|---|---|---|---|
| Library import | protos:Coinage | the judged identifier | B7 ruling 3 (pending); VF:20 "camelCase identifier" |
| Library import | nexus:Instant | a point in time | none found; B8's nexus library declares no Instant |
| Library import | nexus:Process | the calling process | VN:56; B8:34–36 |
| Library | Hash.Bytes<32> | blake3 digest, Encodable | DF:54 (raw 73ada7 blake3); no distilled line |
| Library | FlowId.Hash | session id, hashed, three words | VF:20 |
| Library | Topic.protos:Coinage | a metaflow's subject | VF:16, VF:20, VF:32 |
| Library | Aspect.[Psyche Mind Field] | whose psyche | VF:16; vision-aspects |
| Library | Layer.[4] | decides the model | VF:30 |
| Library | Address.{Aspect Topic Layer} | names a metaflow | VF:16 |
| Library | Said.{Context Verbatim} | the living's words | VF:22 ("the living's words") |
| Library | Request.[6] | what reaches a metaflow | VF:22 |
| Library | Recipient.[Address Up] | where a request goes | VMR:87–91 (in tension, see E) |
| Library | Verdict.[Wake.Layer Stay] | the waking judgment | VF:18; vision-system-one |
| Library | Lock.{Address Until} | Flow's lock per metaflow | VF:12, VF:22, VF:58 |
| Library | Subaspect.[7] | a module's kind | VF:30 (modules); no line orders the kinds |
| Library | Key.{Subaspect Topic} | a module's key | VF:30 |
| Library | Source.{Repository Hash Path} | where module text is | VF:30 "checking each module's hash" |
| Library | Module.{Key Source} | registry entry | VF:30 |
| Library | Effort.[High Medium Low] | model effort | none distilled (B7:493 table) |
| Library | Model.{Layer Harness Native Effort} | model per layer | VF:30; VMR:69 |
| Library | Threshold.{Layer Handover Refresh} | refresh percentages | VF:58 |
| Library | Event.[Started ToolUsed ContextMeasured Stopped] | what a hook reports | VF:56 |
| Library | Notification.[Entered Woken Refreshed Idled] | what a subscriber hears | VF:22; VN:136–139 |
| Library | Metaflow.{Address State Modules Past Queue} | one per address | VF:16, VF:18, VF:22 |
| Library | Flow.{FlowId Process Events} | one per run | VF:12, VF:56 |
| Library | Refusal.[13 variants] | every no, typed | VN:68 "refusals included" |
| Library inline | Context, Verbatim, Until, Repository, Path, Harness, Native, Handover, Refresh, ContextMeasured{Tokens Window}, Entered, Woken, Refreshed, State, Modules, Past, Queue, Events, Unknown, Store | named positions, file namespace | (knowledge-ethos: a named position declares a type) |
| Signal ordinary | 10 queries, 14 responses (C) | the ordinary wire | VN:46–68 |
| Signal meta | 3 queries, 5 responses (C) | the meta wire | VN:38–44; vision-signal «Meta signal» |
| Signal meta types | Nexus.{SourceRoot StableCodex NextCodex HarnessProfiles MetaAspects MessageSocket Lease} | the Nexus's own setup | VN:87–105 (partly, see E) |
| Signal meta import | meta_signal_flow:[CodexEndpoint HarnessKind HarnessProfile] | harness setup types | none found; inf.: this file imports from itself |
| Operation | 15 operations, 15 outcomes (C) | one per effect | VN:148 |
| Memory | Metaflow Flow Lock Module Model Threshold Nexus | stored records | VN:66; VE:62 |
| Memory | Configured.Boolean | first-configuration flag | VN:96–100 |
| nexus library (B8) | Pid, Started, Process, Ancestry, Unidentified.[4] | caller witness | B8 Proposal 2 (pending); VN:56 |

## B. Traits

| trait | capabilities | borne by (B7:277–292) | vision line |
|---|---|---|---|
| Encodable | encode. → String; decode: String → Result<Self Refusal> | Hash, FlowId | none distilled; DZ §1 credits vision-datom, but vision-datom has no Encodable (grep) |
| Rememberable (complex) | assoc. type Previous; const VERSION; change! Self → Result<Self Refusal>; upgrade: Previous → Self | Metaflow, Flow, Module, Model, Threshold, Lock, Nexus | VE:62 «Roots» |
| Identifiable | identify. Process → Result<Address Refusal>; bind! {Address Process} → Result<FlowId Refusal> | none in Flow | VN:56; VF:20, VF:58 |
| Lockable | grant! Instant → Result<Lock Refusal>; free! → Self; lapse! → Vector<Lock> | Metaflow | VF:12, VF:22, VF:58 |
| Wakeable | judge. Request → Verdict; wake! Request → Result<FlowId Refusal>; queue! Request → Self; drain! → Vector<Request>; idle! → Self | Metaflow | VF:18, VF:22 |
| Lineal | launch! {Vector<Key> String} → Result<FlowId Refusal>; refresh! → Result<FlowId Refusal>; reap! FlowId → Result<Self Refusal> | Metaflow | VF:30, VF:50–58 |
| Composable | compose. Vector<Module> → Result<String Refusal>; check. Source → Result<Hash Refusal> | Module | VF:30 |
| Observable | report! Event → Self; subscribe. → Vector<Metaflow>; notify. → Notification | Metaflow, Flow | VN:136–144; VF:22, VF:56 |
| Configurable | configure! Module → Result<Self Refusal>; forget! Key → Result<Self Refusal> | Nexus (declared in meta Signal, not Library) | VN:87–94; vision-signal «Meta signal» |
| nexus Identifiable (B8:44–46) | identify. → Result<Ancestry Unidentified> | nexus Process | B8 Proposal 2 (pending) |

## C. Signal → Operation → Memory

| query | operation → outcome | memory touched | response | mark |
|---|---|---|---|---|
| Launch{Address Modules Brief} | Spawn → Spawned | Metaflow, Flow | Launched.FlowId | Spawn takes Vector<Module>, the query Vector<Key>: no operation turns key into module (inf.) |
| Send{Recipient Request} | Judge → Judged; then Rouse/Enqueue/Place → Roused/Enqueued/Placed | Metaflow.State, .Queue | Woken / Queued / Sent | no operation resolves Up to an Address; Judge stores nothing |
| Subscribe.Address | none | none (no subscriber record) | Subscribed, then Notified | NO OPERATION; no record of subscribers |
| Refresh.Address | Succeed → Succeeded; Grant/Free; Reap | Metaflow.Past, Lock, Flow | Refreshed{FlowId FlowId} | handover step has no operation or record |
| Bind{Address Process} | Attach → Attached | Flow.Process | Bound.FlowId | — |
| Identify.Process | none | read | Identified.Address | NO OPERATION (a read) |
| Report{FlowId Event} | Note → Noted | Flow.Events | Reported | ContextMeasured past threshold triggers nothing typed (inf.) |
| Stop.FlowId | Reap → Reaped | Flow, Metaflow | Stopped | — |
| Show.Address | none | read | Shown.Metaflow | NO OPERATION (a read) |
| List | none | read | Listed.Vector<Metaflow> | NO OPERATION (a read) |
| meta Configure.Module | Register → Registered | Module | Configured | — |
| meta Configure.Model | none | Model | Configured | NO OPERATION |
| meta Configure.Threshold | none | Threshold | Configured | NO OPERATION |
| meta Configure.Nexus | none | Nexus, Configured.Boolean | Configured | NO OPERATION; nothing sets Configured |
| meta Forget.Key | Unregister → Unregistered | Module | Forgotten | — |
| meta Show | none | read | Shown{…} | NO OPERATION (a read) |
| (internal) | Notify → Notified | none | Notified.Notification | operation with no query, fine |
| (internal) | Grant → Granted.Lock, Free → Freed | Lock | none | OUTCOME WITH NO RESPONSE (internal, inf. fine) |
| (none) | Judged.Verdict | none | none | OUTCOME WITH NO RESPONSE |
| (none) | — | — | Unconfigured | RESPONSE WITH NO QUERY OR OUTCOME named |
| trait-only | Wakeable.drain!, idle!; Lockable.lapse!; Composable.check | — | — | capabilities with no operation |
| any | Failed.Refusal | — | Refused.Refusal | — |

## D. Missing

| # | item | source | kind | question for the living |
|---|---|---|---|---|
| 1 | identity by the hash of the rkyv archive | VN:25 «Universal traits first» | trait | Does every Flow type fingerprint itself by its rkyv hash, or only Hash and FlowId? |
| 2 | Rememberable versions: no record names its VERSION or its Previous | VE:62; DN:39 (raw 91ea9f "upgrade from") | record / trait | Where does a record's former form live: beside it in the same ethos file, or in the file's previous commit? |
| 3 | subscription life cycle: no end, no subscriber record | VN:136–139; VF:22 | operation / record | Does a subscription end when its connection closes, or by an Unsubscribe query? |
| 4 | the Capsule | VF:14; VN:174–180 | type / operation | Does Flow's ethos carry the Capsule now, or only once the Capsule is built? |
| 5 | hook events: no final reply, no marked transcript block, no idle | VF:56, VF:58; DF:121, DF:124 (raw) | type | Besides start, tool use, context measure and stop, which hook events does Flow hear? |
| 6 | handover: no tell-the-flow notice, no handover record | VF:58 | operation / record | Is the handover a record Flow stores and hands the successor, or text the flow writes itself? |
| 7 | first configuration: nothing sets Configured; no Configure on the ordinary socket | VN:96–100 | operation / behaviour | While Flow is unconfigured, does its ordinary socket accept Configure? |
| 8 | standard metadata tree; own socket paths | VN:98–105; B7 ruling 5 | type / record | Does the Nexus record hold Flow's own two socket paths as well as Message's? |
| 9 | Kameo actors | VN:124–127; DN:45 (raw bad807) | type / trait | Are the Signal, Operation and Memory actors declared in ethos now, or after their standards are designed? |
| 10 | which model judges waking | VF:18; vision-system-one; B7 ruling 8 | record | Is the judging model one more Model entry in Flow's configuration? |
| 11 | Message's relation: whose wire imports whose | VF:22; VN:77 | type | Does Flow import Message's wire types, or Message Flow's? |
| 12 | delivery tier on Place | VM «Priority», «Delivery is harness-specific» | type | Does a request carry its tier (hard abrupt, middle abrupt, soft), or does Flow choose it? |
| 13 | delivery witnesses (placed, submitted, consumed) | VM «An interrupt witness…» | type | Which of the four observations does Sent stand for? |
| 14 | the lock's holder and what makes it lapse | VF:12; B7:101–103 | behaviour | When a lock lapses, what wakes Flow to free it: a timer it arms, or the next request? |
| 15 | side flows / jobs: every flow belongs to a metaflow | VF:60–76; distilled "side flow is a job" removed in ae0bc79 2026-10-11 | type | Does a subflow get a metaflow address of its own? |
| 16 | the request id | VF:78–84 | type / query | Does Launch return the request id, and is it Flow's? |
| 17 | the router of a flow's ending questions | VF:69–76 | operation / behaviour | Is the ending-question router a Flow operation, or a field flow Flow launches? |
| 18 | the private part (chartered, not active) | CLAUDE.md «Private part»; flows/6cc91b/vision/privateLayer.md | type | Does Flow's ethos reserve the private part now, or wait for the open-source seat? |
| 19 | the judged identifier's check failing | B7:28–46; B7:165–183 has no variant | type | When a topic fails the word check, does Flow refuse with its own variant or carry protos's error? |
| 20 | frame envelope, protocol version, handshake | VN:84–85, VN:116; vision-signal «Protocol» | type | Does Flow's Signal take its frame and version from the shared signal library? |
| 21 | the query-to-operation step as a trait | VN:27–31 ("Apply liked"); intent-mandatory-traits | trait | Is the step from query to operation a nexus-library trait, Apply, borne by every query? |
| 22 | working directory and training files | VF:8–10 | type | Does Launch name the working directory, or does the Capsule? |
| 23 | module placement: system prompt or first prompt | intent-startup-prompt; DF:53, DF:55 (raw) | type | Does a module's key say where it goes, or does its subaspect decide? |
| 24 | the harness session id or binding on the Flow record | VF:20 ("a transcript is found from the flow id"); VMR:93–94 | record | Does the Flow record keep the harness session id, or only its hash? |
| 25 | the registry of pollers | VF:56 | record | What does a registered poller's record hold? |
| 26 | the speaking routes as data | VF:34; vision-aspects | record | Are the routes Flow enforces configuration, or fixed in code? |
| 27 | configuration as datom files replayed at start | DN:22 (raw 445410, 2026-10-09) | behaviour | Are Flow's Configure payloads datom files the meta CLI replays at start? |

## E. Contradictions

| item | the ethos | the vision line |
|---|---|---|
| flow id | FlowId.Hash (B7:67) | VN:153 FlowId.Integer (example); VF:20 hash, agreeing with B7 |
| voice | Address/Metaflow, no Voice (B7:80, B7:153) | VF:12 "one run of a voice"; VN:154 Voice.{Aspect Layer} |
| Capsule | absent | VN:174–180 Start.{Voice Capsule}, NoCapsule; VF:14 |
| topic type | Topic.protos:Coinage (B7:70) | VF:32 "a core:Name, a camelCaseExpression" (ruling 3 pending) |
| caller by claim | Report.{FlowId Event}, Stop.FlowId (B7:318–321) | VF:20 "No flow declares its id"; VN:56 "never by a claim" |
| what the CLI carries | Bind/Identify carry Process (B7:314–317) | B8:20, B8:58: the CLI carries Ancestry |
| Identifiable | declared in Flow's Library (B7:206–214) | B7:54 "Flow declares none of it"; B8:44–47 |
| Unidentified | Refusal.Unidentified.Process (B7:178) | B8:39–43 Unidentified.[PeerMismatch Vanished Reused Malformed] |
| trait inputs | concrete types in every capability input (B7:189–271) | VE «Trait»: "a concrete type in an input is a trait not yet named"; EZ17 refuses them (F) |
| storage on the public wire | Shown.Metaflow, Listed, Subscribed, Refusal.Store.* on the ordinary socket | VN:116 "Storage vocabulary never appears on the public wire" (inf. that Metaflow is storage vocabulary) |
| reads without operation | Show, List, Identify, Subscribe | VN:148 "A signal reaches memory only through operation" |
| first configuration | no Configure on the ordinary socket | VN:99–100 Configure accessible on the ordinary socket while unset |
| socket paths | constant in the executable (B7 ruling 5) | VN:101–103 the metadata tree holds its socket paths |
| priority | "priority tiers gone" (B7:502) | VM «Priority is a head on the datom» |
| Up | one layer above, refused NoneAbove (B7:94–97) | VMR:89–91 next running rung (ruling 10 open) |
| title | ruling 4 (a)/(b) | VMR:76 `<Aspect> <Model> <FLOW_ID>`; VF:32 `{ Psyche core Secondary <id> }`; the two skills disagree |
| power | Effort.[High Medium Low] on Model | VMR:83–85 Power a separate type, four values incl. Ultra Low |
| Sema root | Memory | vision-sema «What sema is» Sema root; VE:57–62 and knowledge-ethos (Sema refused) say Memory |
| vision-flow-ethos | B7:52 proposes it new | VE:8 says the skill already exists; no such skill in .claude/skills or psyche-skills (ls, witness) |

## F. Not expressible in ethos-zero 17.0.0 (EZ17 probe, witness)

| construct | where | EZ17 result |
|---|---|---|
| Bytes<32> | B7:66 | Rejected `Name.32` |
| a newtype | Hash, FlowId | generates `pub type FlowId = Hash;` (alias); raw ebbe30 wants non-aliases (DE:99) |
| protos:Coinage | B7:63, B7:70 | Checked (inline source accepted); protos has no Coinage (grep), so Rust would not build (inf.). B7:507 lists it as unexpressible; the syntax is accepted |
| concrete input types | 14 capabilities (decode, identify, bind, grant, judge, wake, queue, launch, reap, compose, check, report, configure, forget) | Rejected `TraitWanted` for String, Vector, declared types; imported Process and Instant pass but are taken as traits (knowledge-ethos), so they would generate as trait bounds (inf.) |
| Memory records named by import only | B7:454–460 | Rejected `Expected.Declaration` |
| association on Nexus, not in the Library | B7:291 | Rejected `Undeclared.Nexus` |
| HarnessKind not imported into the Library | B7:128 | Rejected `Undeclared.HarnessKind` |
| Aspect not imported into the meta Signal | B7:378 | Rejected `Undeclared.Aspect` |
| Verdict not imported into Operation | B7:426 | Rejected `Undeclared.Verdict` |
| a trait outside a Library | B7:507 | an Operation's fourth section rejects a trait (`Expected.Variant`); B7 itself declares no trait outside the Library (inf.) |
| passes | ordinary Signal, the Library's types (Bytes swapped for String, HarnessKind imported), Rememberable's complex form, B8's nexus library | Checked |
| name collision | Composable | datom-codec already has a Composable kind (knowledge-ethos) |
| Mutex | VN:127 Arc-Mutex permitted | no ethos form; raw d4ae97, ebbe30 "can we support mutex?" (DE:120) |
| 17.0.0's source | ethos-zero branch kind-to-trait, uncommitted; main is 16.0.0; `cargo build` of that tree fails (E0599) | the probe used the existing store build, not this tree |

## Sources

- Read: B7 whole; B8 whole; .claude/skills vision-flow, -nexus, -ethos, -signal, -sema, -messaging, -orchestrate, -system-one, -remembering, -aspects, -model-roles (48–106), intent-mandatory-traits, intent-anatomy, intent-data, intent-startup-prompt; psyche-skills skills/vision-flow.md at 9bba4bf, and the git log of ae0bc79; DZ §1 (lines 9–200) and §4 (878–968); DF §1–5; DN §1–5; DE «Roots», «Traits», «Contradictions», «Not yet expressible»; knowledge-ethos (loaded skill); ethos-zero UPGRADES.md and tests/ethos.rs.
- Ran: EZ17 `Check` on probe files and on B7's blocks extracted by line range, in the session scratchpad; the commands and their output stay in this thread.
- Provenance receipt: unavailable. No PROVENANCE handoff exists for this flow.

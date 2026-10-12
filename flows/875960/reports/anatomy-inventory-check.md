# Check of «Flow Nexus anatomy» (9519a1 flow-anatomy-inventory.md)

Read-only check, 2026-10-12. Each claim in the inventory that names a file and line was opened at that commit (`git show <commit>:<path>`, after `git fetch --all` in every repository) or in the named working-tree file. The fourth edition (b4) is `flows/875960/books/7-flow-whole-ethos-4.md`, last modified 10:29; the inventory was written at 11:34, so its b4 line numbers should match the current file. The design (des) is Primary a589015 `flows/f5a6e9/reports/flow-buildable-design.md`, the same bytes as the working tree. psyche-skills `main` and `origin/main` are both 5a18f9c, so vf at main is the vf the inventory read.

Marks. WITNESSED: the line says what the inventory says. DIFFERS: it does not; the row says how. UNREACHABLE: the check could not observe the claim.

`FLOW_ID` and `FLOW_DIRECTORY` were empty in this subflow's environment. No PROVENANCE receipt was handed over, so no receipt handle is available.

## Counts

188 claims: 178 WITNESSED, 9 DIFFERS, 1 UNREACHABLE.

| section | claims | W | D | U |
|---|---|---|---|---|
| 0 what was read (11 rows, 5 branch bullets) | 16 | 15 | 0 | 1 |
| 1.1 lib | 25 | 25 | 0 | 0 |
| 1.2 nx | 7 | 7 | 0 | 0 |
| 1.3 b4 Library | 27 | 24 | 3 | 0 |
| 1.4 des Library | 7 | 7 | 0 | 0 |
| 1.5 missing in Library | 14 | 12 | 2 | 0 |
| 2.1 sig | 15 | 14 | 1 | 0 |
| 2.2-2.4 | 18 | 18 | 0 | 0 |
| 3.1-3.3 meta | 16 | 16 | 0 | 0 |
| 4.1-4.4 Operation | 11 | 11 | 0 | 0 |
| 5.1-5.3 Memory | 8 | 8 | 0 | 0 |
| 6 Message | 2 | 2 | 0 | 0 |
| 7 conflicts | 21 | 18 | 3 | 0 |
| 9 inference sources (vp L8-12) | 1 | 1 | 0 | 0 |

The catalogue ids it cites (R0004, R0032-R0037, R0156, R0193, R0245, R0264, R0781, R0794, R0813, R0935, R0937, R0942, R0984, R0987, R0988, R0999, R1100, R1101, R1113, R1174, R1181, R1183, R1186, R1228, R1236, R1242, R1246) were all found in `flows/9519a1/reports/flow-ethos-records.md`, and each says what the inventory relays. They remain relayed claims (C); only their presence in the catalogue was witnessed.

## DIFFERS, in full

| # | inventory row | what the file says |
|---|---|---|
| 1 | 1.3 "Hash.Bytes<32> (L65)" | b4 L65 is the comment `; the calling process`; `Hash.Bytes<32>` is at L66. |
| 2 | 1.3 "FlowId.Hash (L66)" | b4 L66 is Hash; `FlowId.Hash` is at L67. |
| 3 | 1.3 "Topic.protos:Coinage (L69)" | b4 L69 is the comment `; as three words`; `Topic.protos:Coinage` is at L70. |
| 4 | 1.5 Coinage row "b4 L63, L69" | L63 is right (`protos:Coinage` import); the Topic line is L70, not L69. |
| 5 | 1.5 Bytes<N> row "b4 L65" | `Hash.Bytes<32>` is at b4 L66. |
| 6 | 2.1 "Types (L153-281)" | sig d1358d3 ethos/signal.ethos has 280 lines; the types section ends at L280. |
| 7 | 7.1 Roots "vn L148 and ve L57-62: four roots" | vn L148 names three parts: "A Nexus has three parts, each its own ethos specification: Signal …, Operation …, Memory …". The four-root form appears only in vn's example, L150-188. ve L62 does say "Four roots". |
| 8 | 7.5 FlowId "b4 L66 Hash of the session id" | `FlowId.Hash` is at b4 L67. |
| 9 | 7.6 Topic "b4 L69 `protos:Coinage`" | It is at b4 L70. |

Rows 1-5, 8 and 9 come from one misnumbering: every b4 line from L65 to L70 is off by one, and b4 lines L71 onward are right.

## UNREACHABLE

- Section 0 row b4: "its 7 ethos blocks are byte-identical to the artifact's (compared by script, W)". This check did not read the artifact FNVZ9Lo9QXA5z4DRpW1zfM, so the comparison was not repeated.

## Witnessed with a note

- Section 0 row vf…vp: the vision-ethos source is `vision/ethos.md` at the psyche-skills root, not under `skills/`. Neither `skills/vision/ethos.md` nor `skills/vision-ethos.md` exists at 5a18f9c.
- Section 0, branches: the inventory leaves out some branches. In flow, `flow-ethos-producer-0c85a3` 9245d88 (10-10 02:17) and `flow-launch-inspection-0c85a3` ac6ab64 are missing. 9245d88's library.ethos has only a types section, with no traits, a `FlowAspect`, `Start.{ OrdinarySocketPath MetaSocketPath }` and `Source.{ Repository.SourceRepository … }`; its operation.ethos has the same checksum as main's. In meta-signal-flow, the local branch `meta-config-0c85a3` 54c2602 is missing. In nexus, `entry-point` ec097e3 is missing; it has no ethos file. None of these changes a "newest" claim: 074437a, d1358d3 and 6d07b7b are still the latest by commit time.
- signal-flow `main`: the inventory reads `origin/main` 068f0ea (Cargo version 11.0.0). The local `main` is the older ecdce22.
- 2.4 and 7.15: des L679-680 "No model decides any step." is written inside the refresh paragraph (des L671-687), so its subject is the refresh steps. vf L18's small model judges waking. The line is quoted correctly, but the two sentences are about different steps (this check's reading).

## Particular checks

### 1. Identifiable as the only trait

Method: every `*.ethos` file on every local and remote ref of flow, nexus, protos, signal-flow, meta-signal-flow and message was read. A parser stripped comments, split each file into its root and bracket groups, and printed the trait and association groups of every Library root (Signal, Operation and Memory roots have no trait group).

- In flow, nexus, signal-flow, meta-signal-flow and message, the only non-empty trait section is nexus `ethos/library.ethos`, on eafe26a and 9fa5659: `Identifiable.[ identify.[ Result<Ancestry Unidentified> ] ]`, borne by `Process.[ Identifiable ]`. WITNESSED for the five repositories the inventory names.
- protos is not among the five, and it does declare traits. On main 15b41da, protos.ethos has `Textualizable`, `Canonicalizable` and `Compactable`, and protos-kinds.ethos has `Spendable` and `BoundedProtosizable`, with `ReaderBudget.[ Spendable ]`. On ProtoformStack 56c683e there are `Printing`, `Protosizable`, `Conceptual`, `Actualizable` and `Situating`. The residue branch da223f has `Delimiting`, `Classifying`, `Textualizable`, `Situating`, `Protosizable`, `Conceivable`, `Incorporable`, `Actualizable`, `Pathed`, `Locating` and `Texted`. If the claim is read across protos as well, it DIFFERS.
- No `Coinage`, `Moniker` or `Instant` appears anywhere on any protos ref, and no `Instant` appears in any nexus ethos. WITNESSED.

### 2. No Memory ethos in flow

No file whose path contains "memory", and no ethos file with a `Memory` root, exists on any of flow's refs. That covers 962ad12, ac6ab64, 9245d88, 6aa881f, a317334, fc358a5, 6bfbbfb and 074437a. op L26-27 says the store types stay Rust "until the Memory root is compiled". WITNESSED.

### 3. Query lists, verbatim

signal-flow d1358d3 `ethos/signal.ethos` L104-121:

```
[ Start.StartRequest
  Restart.RestartRequest
  ResolveRecipient.RecipientResolutionRequest
  Stop.FlowId
  Replace.StartRequest
  LaunchStatus.LaunchRequestId
  Observe.ObserveSelection
  ResolveCaller.Option<FlowId>
  QueueTurnEnd.TurnEndRequest
  Report.{ FlowId Event }
  Lock.{ Sender Recipient }
  Bind.{ Address Process }
  Identify.Process
  Deliver.{ Lock Request }
  Release.Lock
  End.Address
  Current.Address
  Metaflows ]
```

meta-signal-flow 6d07b7b `ethos/signal.ethos` L52-62:

```
[ Configuration
  Configure.ConfigurationChange
  ConsumeReset.ResetRequest
  RegisterFlow.FlowNode
  MetaBindExisting.MetaBindExisting
  Retire.FlowId
  Deliver.DeliveryRequest
  Vet.DeliveryRequest
  Command.CommandRequest
  ResolvePeer.ProcessIdentity
  ReadEvents.FlowId ]
```

Both match the inventory's 2.1 and 3.1. The inventory writes the queries without their payload types for ResolveRecipient, MetaBindExisting and similar entries; that is shortening, not a difference.

### 4. Names b4 uses without importing them, and its Instant and Coinage lines

- HarnessKind: b4's Library uses `Harness.HarnessKind` at L128. Its imports, L63-64, are only `protos:Coinage` and `nexus:[ Instant Process ]`, and no Library type defines HarnessKind. The meta Signal imports HarnessKind from `meta_signal_flow` (L355). WITNESSED.
- Nexus: the Library associations use `Nexus.[ Configurable Rememberable ]` at L291. Nexus is declared only in the meta Signal (L373) and is not imported into the Library. WITNESSED.
- Verdict and Lock: Operation imports (L387-393) `Address FlowId Request Recipient Process Key Module Event Metaflow Flow Notification Refusal` from flow_ethos. It uses `Judged.Verdict` at L426 and `Granted.Lock` at L434. WITNESSED.
- Instant: L7 (figure), L64 (import), L103 (`Until.Instant`), L217 (`grant!{ [ Instant ]`).
- Coinage: L28 (ruling 3, option a), L54 (comment 4), L63 (import), L70 (`Topic.protos:Coinage`), L507 (closing note).
- Further names b4 uses without importing them (this check's reading, not asked for): the ordinary Signal imports `Process` from flow_ethos (L301), but b4's Library only imports Process from nexus; the meta Signal uses `Aspect` (L378) without importing it.

### 5. The 21 conflicts

Real: two sources contradict each other. D: a difference between des (superseded) or code that agrees with it, and b4 (the current proposal).

| # | subject | kind | between |
|---|---|---|---|
| 1 | roots | real | vn L148 (three parts) and vn's example; ve L57-60 (Sema) against ve L62 (Memory); vsema L8-18 (Sema); repositories (Operation, no Memory); des L11 (no Operation) |
| 2 | Process | real | lib L37, nx L11-12, meta L113 |
| 3 | Identifiable | real | nx L19-20 against b4 L206-214; within b4, L54 against L206 |
| 4 | caller identity | real | vf L20 against sig L111, L113 and b4 L318 |
| 5 | FlowId | real | vf L20 (hash) against lib L7 (String) and catalogue R0032-R0037 (six characters) |
| 6 | Topic | real | vf L32 `core:Name`, ve L191 `custom:Name`, lib L9 String, des L26 |
| 7 | Start | real | vn L89-94 (no arguments) against lib L42, nlib L4, des L102-105 |
| 8 | store refusal | real | vn L68 (never strings) against sig L277, meta L170, des L398, L497 |
| 9 | metaflow state | real | vf L18 (never dies) against lib L33, des L82-85 |
| 10 | FlowLifecycle | real | sig L224 against meta L119 |
| 11 | Sender | real | lib L38 against meta L135 |
| 12 | Lock | D | lib L36 and des L90-93 agree; b4 L101-103 proposes Until.Instant and no Sender |
| 13 | effort | real | within sig: L168 Effort.String and L186 PowerLevel. Also D: des has no effort, b4 L122 has |
| 14 | Subaspect | D | lib L13 = des L36-42; b4 L104-111 follows catalogue R1113 |
| 15 | wake judgment | D | des L679-680 against b4 L98; vf L18 agrees with b4. des's sentence is about the refresh, so it may not oppose vf at all |
| 16 | Aspect | real | branches of signal-flow and meta-signal-flow main (FlowAspect) against lib 074437a (Aspect) |
| 17 | Nexus payload | D | lib L62-63 = des L118-122; b4 L379 drops MessageNexusBinary, which sig L78-82 still requires |
| 18 | import direction | real | des L17-21 against lib L51/L59 and meta L51; b4 L353-356 is a third direction |
| 19 | vn example | real | vn L150-188 against every other source |
| 20 | vision-flow-ethos | real | ve L8 names a skill that is absent at 5a18f9c |
| 21 | Lock/Deliver against Send | real | vf L22 against sig L114, L117 and mop L12-15 |

17 real, 4 D (12, 14, 15, 17). Conflict 13 is real and has a D part as well.

### 6. The 14 decisions

Sources: b4, b8 (`8-caller-witnessed.md`), and vf = psyche-skills main 5a18f9c `skills/vision-flow.md`.

| # | decision | mark | where |
|---|---|---|---|
| 1 | four roots, Operation and Memory in ethos | proposed | b4 Operation L386-444 and Memory L449-463, in Proposal 2. vf has no ruling on it; ve L62 (vision-ethos) already says four roots |
| 2 | Memory or Sema | open | b4 uses Memory without asking; ve L57-60 against L62 and vsema L8-18 are unresolved |
| 3 | which Process | proposed | b8 Proposal 1 L28-47 and Ruling 1 L50 (Flow imports the nexus Process and drops its own); b4 L54, L64 |
| 4 | Identifiable yields a chain or an address | proposed | b8 L44-46 and figure L15-16 (chain; Flow finds the address). b4 L206-214 still declares Flow's own `identify` yielding an Address, and no ruling reconciles the two |
| 5 | Report carries a FlowId | ruled | vf L20 "No flow declares its id: every call to Flow is identified by the calling process"; vf L58. b4 L318 still has `Report.{ FlowId Event }` |
| 6 | what FlowId is | ruled | vf L20 "A flow's id is the hash of the harness's session id"; b4 L67 |
| 7 | start with no arguments | proposed | b4 Ruling 5 L468. vn L89 (vision-nexus, not vf) already says "A Nexus starts with no arguments" |
| 8 | does a metaflow end | ruled | vf L18 "A topic never dies; it goes idle" |
| 9 | small model judges waking | ruled | vf L18 "is a judgment, made by a small model". Where that model runs is proposed in b4 Ruling 8 L474 |
| 10 | lock and deliver, or send and subscribe | ruled | vf L22 "Message asks Flow to send a request … Flow owns the lock … Message subscribes". The form is proposed in b4 Ruling 9 L476 |
| 11 | effort in model configuration, values | proposed | b4 L122-130 `Effort.[ High Medium Low ]` on Model, inside Proposal 2, with no ruling of its own; record cited at b4 L493 |
| 12 | time and executable identity in the nexus library | open | b4 L64 imports `nexus:Instant`, but b8's library (L28-47) has no Instant and no executable identity. b8 Ruling 2 (L52) covers only boot |
| 13 | Capsule, subflow request IDs, pollers, marked block as Flow types | open | The behaviour is in vf L14, L56, L78-84. No type for any of them is in b4 or b8 |
| 14 | Source and registry in Flow or shared | open | b4 L115-121 keeps Source in Flow's Library and asks no ruling |

5 proposed (1, 3, 4, 7, 11), 5 ruled (5, 6, 8, 9, 10), 4 open (2, 12, 13, 14).

## Sources

- `/home/li/primary/flows/9519a1/reports/flow-anatomy-inventory.md` (working tree, untracked, 11:34)
- flow 074437a crates/flow-ethos/ethos/library.ethos and crates/flow-nexus/ethos/library.ethos; 962ad12 crates/flow-nexus/ethos/operation.ethos; ethos files on every flow ref
- signal-flow d1358d3, e69fdad, 068f0ea ethos/signal.ethos; checksums on every ref
- meta-signal-flow 6d07b7b, 88f3759 ethos/signal.ethos; checksums on every ref
- nexus eafe26a, 9fa5659 ethos/library.ethos; c495f2a, ec097e3 (no ethos)
- message 87029e4 crates/message-nexus/ethos/memory.ethos and operation.ethos; 6fa4d0c (no ethos)
- protos, every ref, every *.ethos (trait sections; Coinage/Moniker/Instant grep)
- psyche-skills 5a18f9c skills/vision-flow.md, vision-nexus.md, vision-signal.md, vision-sema.md, vision-persona.md, vision/ethos.md
- Primary a589015 flows/f5a6e9/reports/flow-buildable-design.md (identical to working tree; last change 2d0a119, 2026-10-10)
- `/home/li/primary/flows/875960/books/7-flow-whole-ethos-4.md`, `/home/li/primary/flows/875960/books/8-caller-witnessed.md` (working tree)
- `/home/li/primary/flows/9519a1/reports/flow-ethos-records.md` at 845503, searched by record id
- No PROVENANCE receipt; no receipt handle.

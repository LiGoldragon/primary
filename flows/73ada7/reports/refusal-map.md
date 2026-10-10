# Refusal map: Flow's Identify, Lock and Deliver against Message's Send refusals

Flow design: `flows/f5a6e9/reports/flow-buildable-design.md` at
commit a5b2c27d42a3ced6257da09cb5cced6538140df1, blob
33e8c2cfa9928f9a62e4a661ee4010a0e76ab16b. "F n" below is a line of
that blob.

Message design: `flows/73ada7/reports/build/message-design.md` at
commit c6a2c4cdbd1bc37d19a930a55e10751957c6a882 (the newest
origin/main commit touching it after `git fetch`), blob
15222457a44aae1931ad825347aa577969d5d484. "M n" below is a line of
that blob. Its ethos drafts at the same commit:
`flows/73ada7/reports/message-flow/message.signal.ethos` (blob
d2eb15daa237a1a462842e20b043f0c72c2fe90a) and
`message.operation.ethos` (blob
42548864f14daf1298f909f3b5972b675afbfbe8).

"SendRefusal" is not a name in the Message design. The refusal Message
answers a Send with is the anonymous `Refused.[ … ]` of the ordinary
Signal, M 220-234 (contract `signal-message`, `ethos/signal.ethos`,
M 64 and M 207; draft `message.signal.ethos` lines 13-26), mirrored in
the Operation's `Failed.[ … ]` (M 324-336; draft
`message.operation.ethos` lines 23-35). This map uses that type.

## The three requests as the Flow design handles them

- Identify.Process: Flow walks the caller's ancestors to a Flow
  record's Process and "returns that flow's address, else
  Unidentified.Process" (F 742-748; F 371-372). Configure.Nexus is
  "not [needed] for Lock, Deliver, Release or Identify" (F 522-524).
  The gate covers only Lock, Deliver and Release (F 696-701), so
  Identify is ungated.
- Lock.{ Sender Recipient }: F 666-694. Stated outcomes: Locked.Lock;
  Locked (refresh under way); Held; NoneAbove; Unknown.Address (Sender
  or Up target); Asleep and Ended.Address (Sender); OffRoute. Gate:
  NotMessage (F 696-701). Configure.Nexus not needed (F 522-524).
- Deliver.{ Lock Request }: "Flow places it by the waking rule"
  (F 670-672). Waking rule F 613-636: Awake, delivered now; busy,
  Queued; Asleep, a waking kind wakes, other kinds queue; Ended,
  returns to sender. "A wake launches the same way" as a launch
  (F 609-611), composing "from the module registry and the layer's
  model" (F 589-591). Lock outcomes at Deliver: Lapsed, Unknown.Lock
  (F 686-690). Gate: NotMessage (F 696-701). Configure.Nexus not
  needed (F 522-524).

## The six refusals' stated causes

- Awake.FlowId: "Launch of an awake metaflow: its current flow"
  (F 334-336; F 383-384; F 616-618).
- Unknown.FlowId: "Report, Stop or Observe.Agent" (F 348-349);
  "answers Report, Stop and Observe.Agent of an unknown flow"
  (F 389-390).
- Unknown.Key: "a module" (F 350); "a Launch before its … Module is
  refused … Unknown.Key" (F 520-521); Forget of an unknown key on the
  meta socket (F 473-474, F 542-544).
- NoLayer: "no model for it" (F 351); "a Launch before its Model … is
  refused NoLayer" (F 520-521).
- NotConfigured: "Launch before Configure.Nexus" (F 352-353;
  F 518-521).
- Taken.Address: "Bind: the old process lives" (F 375-376); "only
  while the old process lives" (F 711-713); "for a Bind Taken.Address"
  (F 759-760).

## Map

| # | Request | Refusal | Status | Flow design citation | Message variant |
|---|---|---|---|---|---|
| 1 | Identify | Awake.FlowId | unreachable | Handling: F 744-746, the answer is the address "else Unidentified.Process". Cause: F 334-336, Launch only. | none |
| 2 | Identify | Unknown.FlowId | unreachable | Handling: F 744-746. Cause: F 389-390, Report, Stop and Observe.Agent only. Identify carries a Process, not a FlowId (F 287). | none |
| 3 | Identify | Unknown.Key | unreachable | Handling: F 744-746. Cause: F 350, F 520-521, F 542-544, a module at Launch or Forget. | none |
| 4 | Identify | NoLayer | unreachable | Handling: F 744-746. Cause: F 351, F 520-521, Launch only. | none |
| 5 | Identify | NotConfigured | unreachable | Gate/order: F 522-524, Configure.Nexus "not [needed] for … Identify". Cause: F 352-353, Launch only. | none |
| 6 | Identify | Taken.Address | unreachable | Handling: F 744-746. Cause: F 375-376, F 711-713, F 759-760, Bind only. | none |
| 7 | Lock | Awake.FlowId | unreachable | Handling: F 666-694 names no Awake refusal; an awake Sender is the passing case (F 681-684). Cause: F 334-336, F 383-384, Launch only. | none |
| 8 | Lock | Unknown.FlowId | unreachable | Handling: F 666-694; Lock carries Sender and Recipient, no FlowId (F 284-286). Cause: F 389-390. | none |
| 9 | Lock | Unknown.Key | unreachable | Handling: F 666-694 composes nothing. Cause: F 350, F 520-521, Launch or Forget only. | none |
| 10 | Lock | NoLayer | unreachable | Handling: F 666-694 composes nothing. Cause: F 351, F 520-521, Launch only. | none |
| 11 | Lock | NotConfigured | unreachable | Gate/order: F 522-524, Configure.Nexus "not [needed] for Lock". Cause: F 352-353. | none |
| 12 | Lock | Taken.Address | unreachable | Handling: F 666-694. Cause: F 375-376, F 711-713, F 759-760, Bind only. | none |
| 13 | Deliver | Awake.FlowId | unreachable | Handling: F 615-618, Awake "the request is delivered now", or Queued when busy (F 632-636); answers Delivered (F 314-315) or Queued (F 316-317). Cause: F 334-336, Launch only. | none |
| 14 | Deliver | Unknown.FlowId | unreachable | Handling: F 670-672, F 613-636; Deliver carries a Lock and a Request, no FlowId (F 288-290). Cause: F 389-390. | none |
| 15 | Deliver | Unknown.Key | unreachable | f5a6e9's ruling (current best, relayed in the order to 73ada7): a wake composes whatever modules exist for the topic when it wakes, so no forgotten Key can stop it; Unknown.Key stays only for Launch and Forget. Rule text: `flows/f5a6e9/reports/flow-buildable-design.md` at 439dc64b4. Superseded reading: the unresolved question on whether a Deliver-driven wake carries the Launch refusals. | none |
| 16 | Deliver | NoLayer | unresolved: needs f5a6e9 | Handling: the wake composes from "the layer's model" (F 589-591, F 609-611); a Launch before its Model is refused NoLayer (F 520-521). The design does not say whether a Deliver-driven wake carries this refusal. A metaflow made by Bind (F 707-710) needs no Model for its layer, and becomes Asleep when its process exits (F 727-733), so a waking Deliver to it can meet a layer with no model. | if ruled reachable: none exists; see below |
| 17 | Deliver | NotConfigured | unreachable | Gate/order: F 522-524, Configure.Nexus "not [needed] for … Deliver". The wake is a launch (F 609-611), but Deliver passes the gate only from the process bound under the Message address (F 696-705), that Bind needs Configure.Nexus (F 522-523, F 714-723), the Nexus payload is stored once (F 220-221), and nothing removes it (meta requests F 440-457: only Forget.Key removes). | none |
| 18 | Deliver | Taken.Address | unreachable | Handling: F 670-672, F 613-636. Cause: F 375-376, F 711-713, F 759-760, the Bind request only; the bind step inside a launch (F 597-599) is not the Bind request. | none |

Counts: reachable 0, unreachable 17, unresolved 1 (row 16, Deliver × NoLayer).

## Variants to add

No reachable pair, so no variant is required by this map.

NoLayer is already a variant of Message's Send refusal. Row 15 is
unreachable, so `Unknown.Key` is not added.

The row 16 variant, kept for reference:

- Row 16, `NoLayer`: same contract and file; a unit variant `NoLayer`
  inside `Refused.[ … ]`, M 220-234, draft `message.signal.ethos`
  lines 13-26 (after line 22, `Lapsed`); and inside `Failed.[ … ]`,
  M 324-336, draft `message.operation.ethos` lines 23-35 (after line
  33).

## Cross-check against 9fed42

`flows/9fed42/reachability-a5b2c27d4.md` (read, working tree) marks
all six refusals unreachable for all three requests, citing only the
Launch causes. f5a6e9's log, `flows/f5a6e9/log.md` line 215, records
"9fed42's reachability table confirmed". The coordinator relays the
same as f5a6e9's confirmation; it is a claim, and the design at
a5b2c27d4 does not carry it.

Rows 1-14, 17 and 18 agree. Rows 15 and 16 differ: 9fed42 marks
Deliver × Unknown.Key and Deliver × NoLayer unreachable; this map
marks them unresolved. Neither 9fed42's table nor f5a6e9's log line
215 addresses the wake a waking Deliver runs, which "launches the same
way" (F 609-611) and composes from the registry and the layer's model
(F 589-591), while Unknown.Key and NoLayer are the Launch refusals for
a missing Module or Model (F 520-521). Whether the wake carries them
stays for f5a6e9 to rule.

## New Flow refusals (current best, fold publishing)

Source: the coordinator's message, relaying f5a6e9's rulings; the
same rulings appear in `flows/f5a6e9/log.md` line 215. Not in the Flow
design at a5b2c27d4, so they are claims here, not design lines.

| Request | Flow's answer | Message variant | Message citation |
|---|---|---|---|
| Lock | Recipient naming no metaflow: Unknown.Address | `Refused.Unknown.Address.Address` | M 222; M 554; draft `message.signal.ethos` line 15 |
| Lock | Asleep Recipient: granted, Locked.Lock | no refusal; the Deliver then answers Woken or Queued | M 216-218; M 503-513 |
| Lock | Ended Recipient: Refused.Ended.Address | `Refused.Ended.Address` | M 224; M 555; draft line 17 |
| Deliver | Ended recipient: Refused.Ended.Address | `Refused.Ended.Address` | M 224; draft line 17. The 7.5 table has no Deliver row for it beyond the blanket M 559; a row is owed there |
| Deliver | lock lapsed meanwhile: Lapsed | `Refused.Lapsed` | M 230; draft line 22. M 560 covers only Message's own clock; a Deliver row is owed in 7.5 |
| Lock, Deliver | re-check finds the bound Message process dead: NotMessage, binding dropped | `Refused.NotMessage` | M 231; M 561; draft line 23. M 561's cause lists unequal pid or start time and a wrong executable; the dead process is a cause to add to that row |
| Identify | Store (Flow's `Store.String`, F 377-378, F 762-764) | none exists | M 220-234 has no Store; `StoreRefused` (M 293, M 336) is Message's own store failure |

Variant to add for Identify's Store: `Store.String`, keeping Flow's
name and payload (M 255-258), in contract `signal-message`,
`ethos/signal.ethos` (M 64, M 207): inside `Refused.[ … ]`, M 220-234,
draft `message.signal.ethos` lines 13-26; and in the Operation
(`message/crates/message-nexus/ethos/operation.ethos`, M 301) inside
`Failed.[ … ]`, M 324-336, draft `message.operation.ethos` lines
23-35, beside the existing `StoreRefused`. A 7.5 row
"Identify | Store | Refused.Store" is owed with it. The same sentence
(F 762-764) makes Store an answer to Lock and Deliver too, and 9fed42
lists it for both; the one variant serves all three.

## Findings outside the 18 rows

- M 559 maps "a refusal of the waking rule" to "that refusal". That is
  a blanket row naming no variant; it is where rows 15 and 16 would
  land unnamed.
- Message's Send refusal disagrees with its own draft: the design's
  M 225 has `Asleep`, the draft `message.signal.ethos` at c6a2c4 has
  no `Asleep` in lines 13-26, and the Operation's `Failed` (M 324-336,
  draft lines 23-35) has none either, though M 552 maps Flow's Lock
  `Asleep` to `Refused.Asleep`.

## Sources

Read: `git show a5b2c27d4:flows/f5a6e9/reports/flow-buildable-design.md`;
`git show c6a2c4cd:flows/73ada7/reports/build/message-design.md`;
`git show c6a2c4cd:flows/73ada7/reports/message-flow/message.signal.ethos`;
`git show c6a2c4cd:flows/73ada7/reports/message-flow/message.operation.ethos`;
`flows/9fed42/reachability-a5b2c27d4.md` (working tree);
`flows/f5a6e9/log.md` line 215 (working tree); the coordinator's
message relaying f5a6e9's rulings.
Every status above is this flow's reading of those two designs; no
code ran against Flow or Message. Provenance receipt: unavailable.

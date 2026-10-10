<!-- to-the-living:start -->
Presentation.{ «Distilled lines gone stale» }

Ten lines in the vision skills now contradict a
later record of yours. Each is shown as removed and
added, with the record it follows. Then four
rulings, and one on the books.

## 1. vision-flow, line 22 — four layers
Record: 5578cc/vision/layers.md, 2026-10-03.
```
- A voice is an aspect carrying a rank,
- `Psyche.Primary`: Psyche, Mind, Field by
- Primary, Secondary, Tertiary, nine voices.
+ A voice is an aspect carrying a layer,
+ `Psyche.Primary`: Psyche, Mind, Field by
+ Primary, Secondary, Tertiary, Quaternary,
+ twelve voices.
```
Ruling 1: (a) land (b) amend.

## 2. vision-flow, line 24 — reach
Record: d4ae97/vision/flow.md, 2026-10-07.
```
- vertically within an aspect one rung at a time
+ vertically within an aspect one layer up, or
+ any layer down
```
Ruling 2: (a) land (b) amend.

## 3. vision-messaging, lines 8–9 — datom bodies
Record: 8904b1/vision/datom.md, 2026-09-27.
```
- The message body is a datom that lands in the
- recipient's prompt as a datom-formatted object.
+ A message body is a datom where the receiving
+ program reads datom; a messenger that needs
+ none is given none.
```
Ruling 3: (a) land (b) amend.

## 4. vision-ethos, lines 206–234, 323–325 — new types
Record: d4ae97/vision/ethos.md, 2026-10-06.
```
- FilePath.String ; types: FilePath is an alias
- of String
- pub type FilePath = String;
+ FilePath.String ; types: FilePath is a new type
+ holding String
+ pub struct FilePath(String);
```
Every other one-position alias in the file
changes the same way.
Ruling 4: (a) land (b) amend.

## 5. vision-ethos, lines 25–28 — the four roots
Record: 91ea9f/vision/ethos.md, 2026-10-02.
```
- since there is communication; Sema's are
- record types, the rest to be decided. Signal
- gives a Nexus its main types and Sema its
- database types.
+ Library, Signal, Operation, Memory. No version
+ in a file. Signal's sections are queries and
+ responses, since there is communication.
```
vision-sema, line 9, the same record:
```
- its root, Sema, declares record types.
+ its root, Memory, declares record types.
```
Ruling 5: (a) land both (b) amend.

## 6. vision-nexus, line 116 — queries and responses
Record: 564f55/vision/archive-ethos.md, 2026-09-09.
```
- a closed enum of operations with their paired
- replies ... Operations are verbs, `Submit`;
- replies the past tense, `Submitted`;
- rejections name themselves.
+ a closed enum of queries with their paired
+ responses ... Queries are verbs, `Submit`;
+ responses the past tense, `Submitted`;
+ refusals name themselves.
```
Ruling 6: (a) land (b) amend.

## 7. vision-model-roles, lines 76–81 — the title
Record: d4ae97/vision/flow.md, 2026-10-07.
```
- Every native main session is titled
- `<Aspect> <Model> <FLOW_ID>`.
+ Every native main session is titled by its
+ aspect and its flow id in words; the title
+ names no model.
```
Lines 77–81 are removed with it.
Ruling 7: (a) land (b) amend.

## 8. vision-ethos, line 445 — layout
Record: e5a0bc/vision/ethos.md, 2026-10-06.
```
- a structure with more than one element opens
- on its line and its elements hang beneath the
- first, aligned
+ a structure with more than one element opens
+ on its line, and its elements begin on the
+ next line, indented
```
Ruling 8: (a) land (b) amend.

## 9. Voice
f5a6e9/vision/flow.md:11 and d4ae97/vision/flow.md:86,
both 2026-10-07, point opposite ways.
Ruling 9: (a) a voice is a permanent metaflow
(b) there is no voice; the metaflow carries the
aspect directly (c) something else.

## 10. FlowId
vision-nexus line 153 holds `FlowId.Integer`;
vision-ethos lines 316 and 325 hold `FlowId.String`;
edf227/vision/identifiers.md:10 calls it a hash.
Ruling 10: (a) `FlowId.Integer` everywhere
(b) a `Hash` type (c) something else.

## 11. Inline payload
564f55/vision/archive-ethos.md:43 and
vision-ethos line 216 differ on naming a payload.
Ruling 11: (a) the payload bears the variant's
name (b) a distinct path-overlap name (c) other.

## 12. Committing
vision-committing lines 8–9 and Primary's
CLAUDE.md "Committing" differ on dirty changes.
Ruling 12: (a) a flow commits only what it edited
(b) found dirty changes are committed first, as
their own commit.

## 13. The books
Thirty-six books stand with open rulings; their
needed changes are listed in this flow's
reports/book-audit-verified.md §A. Ninety-seven
are overtaken by a landing or a later record, §B.
Ruling 13: (a) each live owning flow republishes
its §A books and retires its §B books (b) this
flow republishes all of §A (c) retire §B only.
<!-- to-the-living:end -->

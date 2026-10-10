<!-- to-the-living:start -->
Presentation.{ «The fixed Metaflow record» }

## Measured, 8 October

rkyv 0.8.18 and redb 4.3.0 with Flow's own rkyv features (unaligned, little endian, 32-bit pointers), as Flow, Sema and the Sema engine build them. Ids are Integer, the only fixed-width scalar ethos generates. Each timing is the median of three runs on this laptop.

[Chart: bytes per archived record, by shape]

[Chart: one lookup by id, ten thousand and a million records]

[Chart: one update of the current flow]

What holds:

- The record without a vector or a string archives to the same size every time: 45 bytes for the shape below, a million records, one size. There is no padding: under the unaligned feature everything has alignment 1, so the size is the sum of the fields. Under rkyv's default aligned features, a shape of 53 bytes takes 72.
- A series of them is read by position, offset = index × size, with no offset table. The concatenated records are byte for byte the element block of one archived vector of them; each slot validates alone.
- An enum with a payload is still fixed: one tag byte and its largest variant. `Awake.FlowId` costs 9 bytes, `Option<FlowId>` 9.
- Updating the current flow in place takes 2 to 20 nanoseconds, with or without validation.
- A scan of a million fixed records for the awake ones takes 2.4 ms as one block, 63 ms through redb rows that are decoded one by one.

What does not hold:

- Through Sema, one archive per key in redb, the fixed record gains little: a lookup costs 0.18 to 0.75 µs either way, against 0.25 to 0.92 µs vectored. At a million records an update costs 7 to 9 µs fixed against 12 µs for appending to the vector. The position index exists only when the series is kept as one block.
- FlowId is a String in signal-flow today. A six-hex id fits inline (eight bytes or fewer), so the record is fixed by accident; three-word ids go out of line and the size varies from 57 to 79 bytes.
- A wrong stride is not caught: of 999 slices read at the vectored record's average size, 5 passed validation and read garbage.

## Proposal 1: `flow/crates/flow-nexus/ethos/memory.ethos`, the Metaflow record

The Metaflow block of «The metaflow record», second edition, with the Kind of «Metaflow kinds, the title, the word id».

Removed:

```
[  signal_flow:[ FlowId FlowAspect Event ] ]
```

```
   Metaflow.{
      Kind.[
         Voice.{                 ; Psyche, Mind, Field:
            FlowAspect           ; one payload, the
            Layer }              ; aspect a field of it
         Implementation.{        ; a job: its own kind
            Name.String          ; camelCase
            Layer } ]            ; Primary, Secondary…
      State.[
         Awake.FlowId            ; its current flow
         Asleep                  ; a request wakes it
         Ended ]
      Past.Vector<FlowId> }      ; oldest first
```

Added:

```
[  signal_flow:[ FlowId FlowAspect Layer Event ] ]
```

```
   MetaflowId.Integer
   Metaflow.{                    ; 45 bytes, always
      MetaflowId
      Kind.[
         Voice.{ FlowAspect Layer }
         Implementation.Layer ]  ; its name is slow
      State.[
         Awake                   ; Current runs
         Asleep                  ; a request wakes
         Ended ]
      Current.FlowId             ; the one pointer
      Predecessor.Option<FlowId> ; the flow before
      Flows.Integer              ; runs so far
      Changed.Integer }          ; unix seconds
```

Ruling 1: (a) yes. (b) keep `Awake.FlowId` and drop `Current`: an asleep metaflow then names no flow. (c) amend.

## Proposal 2: `flow/crates/flow-nexus/ethos/memory.ethos`, the slow records

Removed: none. Added, after the Metaflow record:

```
   MetaflowName.{                ; slow; same key
      MetaflowId
      Name.String }              ; camelCase
   Succession.{                  ; one per run, 32 B
      MetaflowId
      Ordinal.Integer            ; 0 is the first
      FlowId
      Started.Integer }          ; unix seconds
```

The history is the Succession rows of one MetaflowId in Ordinal order: fixed rows, no vector. The Flow record stays as it is.

Ruling 2: (a) the slow records are reached by the same MetaflowId; the Metaflow record carries no pointer to them. (b) the Metaflow record carries a `Slow.Integer` pointer. (c) amend.

## Proposal 3: `signal-flow/ethos/signal.ethos`, line 26

Removed:

```
FlowId.String
```

Added:

```
FlowId.Integer
```

Ruling 3: (a) FlowId is Integer everywhere; the word id is printed from it. (b) Memory keeps its own Integer and translates at its boundary; the wire keeps String. (c) keep String: the record stays fixed only while every id is eight bytes or fewer.

## Proposal 4: `psyche-skills/skills/vision-sema.md`, after line 11

Removed: none. Added:

A record type with no vector and no string is fixed width: every record of it archives to the same number of bytes. A series of such records is read by position, offset = index × size, and changed in place. Data that is slower or varies in size lives in a separate record reached by the same key. Kept as Sema rows, each record is still one value under its key; reading by position needs the series stored as one block.

Ruling 4: (a) land; the Metaflow records stay Sema rows. (b) land; the Metaflow series is stored as one block, read by position. (c) amend.
<!-- to-the-living:end -->

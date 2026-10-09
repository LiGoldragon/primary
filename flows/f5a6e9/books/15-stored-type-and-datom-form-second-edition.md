<!-- to-the-living:start -->
Presentation.{ «Stored type and datom form», second edition }

## 1. `psyche-skills/skills/vision-datom.md`, after line 172 (section «Containers»)

Lines removed: none. Lines added:

```
## Encoded types

A type whose value is bytes, a hash first of all,
is one bare run in datom and bytes in memory. It
bears the trait Encodable, and datom-codec gives
every such type its Datomizable and Composing from
the two functions, once, as it does for Integer;
hand-written forms stay with the intrinsics.

Encodable.[
   encode.String        ; the bare run
   decode:{
      [ Textualizable ] ; the run read
      [ Result<Self Error> ] } ]

An Encodable type has no positions: its whole datom
is the run, however many bytes stand behind it.
The Nexus never sees the run; it holds the bytes
and compares, hashes and orders them.
```

Ruling 1: yes, or amend.

## 2. `psyche-skills/skills/vision-ethos.md`, lines 144–145

Lines removed:

```
Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option,
Result, Self.
```

Lines added:

```
Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option,
Result, Self, and Bytes<N>: N bytes, copied,
ordered, hashed, as fast Rust keeps a hash.
```

Ruling 2: yes, or amend.

## 3. `psyche-skills/skills/vision-flow-ethos.md`, the Memory root of «The Flow Nexus vision»

Line removed:

```
[  flow:[ FlowId Request ] ]
```

Lines added, a Library root before the Memory root, and the import that reads it:

```
Library                         ; Flow's
[]
[  FlowId.String                ; unideal for now:
                                ; a real id built on
                                ; the hash bits that
                                ; identify a flow is
                                ; needed
   Sha256.Bytes<32> ]           ; Encodable: 64 hex
                                ; characters, as git
                                ; and blake3 print
[]
[]

Memory                          ; Flow's
[  flow_ethos:[ FlowId Request ] ]
```

Ruling 3: yes, or amend.

## 4. `psyche-skills/skills/vision-signal.md`, after line 46 (before «Sources»)

Lines removed: none. Lines added:

```
## Simple and extended forms

The same data may travel in two containers, both
defined in Signal as types of their own, nothing
omitted from either. The simple form carries only
what its use needs and is what the common queries
and responses use, above all in a thinking machine's
context; the extended form carries every parameter
and serves the technical side: debugging, and
components giving each other more than the common
case. A simple message names the metaflow and never
a flow id, since the sender cannot know which flow
is current.

[  Send.{                       ; simple: what a
      Metaflow                  ; flow writes
      Request }
   Deliver.{                    ; extended: Message
      Lock                      ; to Flow, under the
      FlowId                    ; lock
      Request } ]
```

Ruling 4: yes, or amend.
<!-- to-the-living:end -->

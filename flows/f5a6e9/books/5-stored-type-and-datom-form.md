<!-- to-the-living:start -->
Presentation.{ «Stored type and datom form» }

## Proposal 1: Vision/datom.md, the Encodable kind

Lines removed, in "Any Rust type":

```
Hand-written impls are reserved to the
intrinsics.
```

Lines added in their place, with the datom-codec
kind beside the example:

```
Hand-written impls are reserved to the
intrinsics and to one kind, Encodable. A type
that bears Encodable is written as one bare
run and read from one. datom-codec gives every
such type its Datomizable and Composing from
the two functions, once, as it does for
Integer. An Encodable type has no positions:
its whole datom is the run, however many bytes
stand behind it. The Nexus never sees the run;
it holds the bytes and compares, hashes and
orders them.
```

```
Encodable.[
  encode.String        ; the bare run
  decode:{
    [ Textualizable ]  ; the run read
    [ Result<Self Error> ] } ]
```

Ruling 1.
(a) Yes, as written.
(b) Amend.

## Proposal 2: Vision/ethos.md, Bytes and the hash

Lines removed, in the intrinsics list:

```
Integer, Decimal, Boolean, Meaning, Vector,
Option, Result, Self.
```

Lines added:

```
Integer, Decimal, Boolean, Meaning, Bytes,
Vector, Option, Result, Self.

Bytes<N> is a fixed run of N bytes, generic
over its length as Vector is over its element;
it is copied and ordered. A 256-bit hash is a
newtype over 32 bytes, Encodable, written as
hex. Hex is what git, blake3 and the sha2
tools print, so a hash read from any of them
is the datom unchanged.
```

```
Bytes<32>          ; intrinsic: 32 bytes,
                   ; copied, ordered
Sha256.Bytes<32>   ; a new type, Encodable
```

A module's content hash in a flow record:

```
{ vision-flow
  9f2c…e71a }      ; 64 hex characters
```

Ruling 2.
(a) Hex, 64 characters.
(b) Base32, 52 characters, 12 fewer per hash;
    nothing else prints it.

## Proposal 3: Vision/flowNexus.md, the flow id

Lines removed: none. Lines added, as a new
section after "A session is named after its
direct ancestor":

```
## A flow id is three words

A flow id is 33 bits, written as three BIP-39
words in camel case. The stored type is a
newtype over Integer, since 33 bits are
arithmetic (prefix comparison, the glob) and no
byte array is needed; it bears Encodable.

Claude takes the first 33 bits of the session
id; Codex, the 33 bits from hex index 23, past
the time-ordered prefix; OpenCode, the first 33
of a blake3 of the session.

Back to the transcript: 33 bits are 8 hex
characters and one bit, so the glob is those 8
characters, a ninth from a set of eight ([0-7]
or [8-f]), then anything; for Codex the same,
matched inside the name. Two files matching is
a collision, reported to the living. By the
birthday bound it is even odds around 108,000
flows.
```

```
FlowId.Integer     ; 33 bits, Encodable
```

```
{ abandonAbilityAble      ; a flow
  Voice.{ Psyche Primary }
  Some.Voice
  Some.zooWrongYouth }
```

Ruling 3.
(a) Yes, as written.
(b) Amend.

## Proposal 4: Vision/flowNexus.md, where the words stand

Lines removed: none. Lines added after the
section above:

```
The three words replace the 24-bit hex alias
wherever a flow is named: the title, the lane,
the messenger's target, FLOW_ID.
```

The bip39 crate (2.2.2) and hex (0.4.3) are in
the local registry.

Ruling 4.
(a) Yes, as written.
(b) Amend.

## Proposal 5: Vision/ethos.md, the shorthand

Lines removed: none. Lines added, as a new
section:

```
## A shorthand omits tail positions

A shorthand is not a second type; that would
wrap a type in a type. It is the same datom
with its tail omitted. A position written
`= default` may be left off when written
short; a position without one is never
omitted. A reader that meets the closer early
fills the omitted positions from the declared
defaults. A writer asked for the short form
drops every tail position that holds its
default.

A letter is addressed by the short Lineage,
never by a flow id; Flow resolves it to the
current flow.
```

```
Psyche.{ Fable abandonAbilityAble }
                 ; a Flow, short
Voice.{ Mind Tertiary }
                 ; a Lineage, short:
                 ; Metaflow omitted, Voice
```

```
Lineage.{
  Role
  Metaflow = Voice    ; omittable, default
  Current.Option<FlowId> = None
  Lock = Open }
```

Ruling 5.
(a) Yes, as written.
(b) Amend the mark.
(c) A shorthand is something else: say what.
<!-- to-the-living:end -->

<!-- to-the-living:start -->
Presentation.{ «Stored type and datom form» }

Your comments on the second edition's `FlowId` and your spoken words beside them, then the shape. The code witnessed: datom-codec 0.32.2 hand-writes the text form of each intrinsic (Integer: bare decimal in, `from_str` out) and reserves hand-written forms to intrinsics; a derived one-field struct is written as a one-element struct, braces and all; no byte array is datomizable; ethos knows no byte type. The flow id today is a 24-bit hex alias of a 128-bit session id, a String in signal-flow.

## 1. "There's a conversion that happens"

Your words: a SHA-256 is a 256-bit number, not a string; in datom it has a text form; the in-memory type is bytes; the conversion is serialization, outside the Nexus, which thinks of the value as a hash with traits.

One kind in datom-codec, beside the intrinsics: a type that bears it is written as one bare run and read from one. datom-codec gives every such type its Datomizable and Composing from the two functions, once, the way it does for Integer; nothing else is hand-written, and the reservation to intrinsics stands.

```
Encodable.[
  encode.String        ; the bare run
  decode:{
    [ Textualizable ]  ; the run read
    [ Result<Self Error> ] } ]
```

An Encodable type has no positions in datom: its whole datom is the run, however many bytes stand behind it. The Nexus never sees the run; it holds the bytes and compares, hashes and orders them.

## 2. The hash

Fast Rust code keeps a 256-bit hash as a newtype over 32 bytes, copyable, ordered, hashable, with hex as its text (blake3, gitoxide, bitcoin_hashes). Ethos has no byte type, so one is added to its intrinsics, generic over its length as Vector is over its element.

```
Bytes<32>          ; intrinsic: 32 bytes,
                   ; copied, ordered
Sha256.Bytes<32>   ; a new type, Encodable
```

Written, a module's content hash in a flow record:

```
{ vision-flow
  9f2c…e71a }      ; 64 hex characters
```

Hex is what git, blake3 and the sha2 tools print, so a hash read from any of them is the datom unchanged. Base32 is 52 characters, 12 fewer per hash, and nothing else prints it.

## 3. The flow id

Your words: a hash, not an integer; 33 bits, three words, cheap in tokens for the entropy; a glob on a superset of the hex when the words are turned back to find a transcript; a clash brought to you.

Three BIP-39 words carry 11 bits each, 33 in all. The stored type is a newtype over Integer, since 33 bits are arithmetic (prefix comparison, the glob) and no byte array is needed; it bears Encodable, and its run is the three words in camel case.

```
FlowId.Integer     ; 33 bits, Encodable
```

```
{ abandonAbilityAble      ; a flow
  Voice.{ Psyche Primary }
  Some.Voice
  Some.zooWrongYouth }
```

Where the bits come from: Claude, the first 33 bits of the session id; Codex, the 33 bits from hex index 23, past the time-ordered prefix; OpenCode, the first 33 of a blake3 of the session. Back to the transcript: 33 bits are 8 hex characters and one bit, so the glob is those 8 characters, then a ninth from a set of eight (`[0-7]` or `[8-f]`), then anything; for Codex the same, matched inside the name. Two files matching is a collision, reported to you, as you said; by the birthday bound it is even odds around 108,000 flows.

The words replace the hex alias wherever a flow is named: the title, the lane, the messenger's target, `FLOW_ID`. The `bip39` crate (2.2.2) and `hex` (0.4.3) are in the local registry.

## 4. The shorthand

Your words: a query or response has a full-size, fully explicit version and a shortened one carrying only the bits that matter where it is used, mostly in the thinking machine's context; messaging has no need of a flow id, and addressing a flow id is bad practice because the sender cannot know it is the current flow.

A shorthand is not a second type: that would wrap a type in a type. It is the same datom with its tail omitted. Ethos marks, per type, the positions that may be left off when written short; a reader that meets the closer early fills them from the type's declared defaults; a writer asked for the short form drops every tail position that holds its default. The three seats' names and the letter's address are shorthands of the Flow and Lineage records of book 2:

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

The `=` after a position names its default and marks it omittable; a position without one is never omitted. A letter is addressed by the short Lineage, never by a flow id; Flow resolves it to the current flow. A subflow is a flow with a Worker role, so it may address a Lineage like any flow; whether the messenger's registration makes that worth doing is Message's design, not this book's.

## Rulings

1. `Encodable` in datom-codec, its two functions giving a type its bare-run datom, the reservation to intrinsics kept: yes, or amend.
2. `Bytes<N>` as an ethos intrinsic, `Sha256.Bytes<32>` Encodable as hex: (a) hex, 64 characters. (b) base32, 52 characters.
3. `FlowId.Integer`, 33 bits, Encodable as three BIP-39 words in camel case; the glob as in section 3; a collision reported to you: yes, or amend.
4. The words replace the hex alias in the title, the lane, the messenger and `FLOW_ID`: yes, or amend.
5. The shorthand as omitted tail positions with declared defaults, `=` marking them in ethos: (a) yes. (b) amend the mark. (c) a shorthand is something else: say what.
<!-- to-the-living:end -->

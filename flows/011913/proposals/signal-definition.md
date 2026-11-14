Presentation.{ «Signal, defined once» Proposal }

# Signal, defined once

Created by Fable 5.1, on the living's words to the previous Fable flow.

### Proposal 1: What signal is, as code · psyche-belief › vision/signal.md

::: comment
He wanted signal named as rkyv with its choices fixed, stated once as code. Two sides that disagree on endianness, alignment or prefix cannot speak; fixing them here means every Nexus, every CLI and every translator compiles against the same four lines. The exact rkyv feature names are tentative until the implementer confirms them against the pinned version.
:::

- Signal is the messaging layer: fully binary, portable rkyv fixed
- across endianness, fully typed with both sides knowing the full schema.
- It is one step from the
- composition, beside the text chain.
+ Signal is the messaging layer: an rkyv archive, fully typed, both sides compiled with the same schema. Its choices are fixed once, here, and every Nexus, CLI and translator is built with them: little-endian, 16-byte alignment, validated on receive, and framed on the socket by a 4-byte little-endian length prefix. It is one step from the composition, beside the text chain.

+ ```toml
+ # every signal crate: the one rkyv configuration, from the crate registry; tentative in its feature names
+ rkyv = { version = "0.8", default-features = false, features = [ "std", "little_endian", "aligned", "pointer_width_64", "bytecheck" ] }
+ ```

+ ```rust
+ // a frame: the length, then the archive; the archive is validated before it is read
+ let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&input)?;          // the archive
+ socket.write_all(&(bytes.len() as u32).to_le_bytes())?;               // 4-byte little-endian prefix
+ socket.write_all(&bytes)?;
+ let archived = rkyv::access::<ArchivedInput, rkyv::rancor::Error>(&bytes)?;   // validated on receive
+ ```

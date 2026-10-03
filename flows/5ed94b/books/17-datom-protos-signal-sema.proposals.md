Presentation.{ «Datom, Protos, Signal and Sema» }

This is how data is written as text (datom), the shape every dialect shares (protos), the binary form programs exchange (Signal), and the store (Sema). Everything is data; the type knows what each position means, so the text carries only values.

**1. Datom's plain rules**
Module: vision, datom. Action: edit.
Text: "A capitalized word before a structure is a variant, never a tag. A string with no space is written bare; anything else goes inside « and »."
Rests on: 26 Sep, 10 Sep.

**2. Protos is a style**
Module: vision, protos. Action: edit.
Text: "Protos is the style all our dialects share, and it sees shape only. Datom is a protos dialect, kept out of the engine that turns Ethos into Rust."
Rests on: 11 Aug, 14 Aug.

**3. Write a Signal module**
Module: vision, new name signal. Action: create.
Text: "Signal is the binary form programs exchange; each side knows every type, so nothing on the wire describes itself. A definition declares requests and responses, its root a set of variants. A request and a response are never the same type. The settings channel is never optional."
Rests on: 10 Sep, 13 Sep, 14 Aug, 9 Aug.

**4. The default response**
Module: vision, signal. Action: edit.
Text 1: "The default response is a simple form of the same data, carrying a shortened identifier; an explicit call returns the full form."
Text 2: Same, but the simple form carries no identifier at all.
Rests on: 15 Sep, 3 Oct. Name 1 or 2.

**5. Who is calling**
Module: vision, signal. Action: edit.
Text 1: "Every Nexus asks Flow who called it."
Text 2: "Every Nexus checks the calling process itself, never what the caller claims."
Rests on: 18 Sep, 28 Sep. Name 1 or 2.

**6. Streams**
Module: vision, signal. Action: edit.
Text 1: "A stream is separate parts, a start, events and an end. It is a section inside the interface, with start and end among the inputs."
Text 2: Text 1, and a stream is also a fourth kind of object.
Rests on: 6 and 7 Aug. Name 1 or 2.

**7. Nexuses stay small**
Module: vision, vision-nexus. Action: edit.
Text: "The same type library is built twice: with text conversion for the command, without it for the Nexus. A Nexus holds only typed binary values and never carries code that reads or writes text."
Rests on: 9 Sep, 28 Sep.

**8. The settings file**
Module: vision, vision-nexus. Action: edit.
Text 1: "The command reads the datom settings file at each call and sends it as Signal."
Text 2: "A compiled Signal file sits beside the datom file for the Nexus to load."
Rests on: 24 and 29 Sep. Name 1 or 2.

**9. What Sema is**
Module: vision, new name sema. Action: create.
Text 1: "Sema is the database engine of a Nexus; its types are declared in Ethos."
Text 2: "Sema is a whole communication: utterances, acts and Ethos objects."
Text 3: Both, one name over two things.
Rests on: 9 Sep, 26 Sep. Name 1, 2 or 3.

**10. Messages are datom**
Module: vision, new name messages. Action: create.
Text: "A message between seats is a datom, a variant first, then a struct or a list. It arrives in the receiving prompt with no wrapper. His own words are never datom; that is how a seat tells him from a machine."
Rests on: 18 Sep, 24 Sep.

**11. Datom where no program reads it**
Module: vision, messages. Action: edit.
Text 1: "A subflow's report is written in datom even when no program reads it."
Text 2: "Datom is not forced where no program reads it, a subflow's report included."
Rests on: 19 Sep, 27 Sep. Name 1 or 2.

**12. No paths in datom**
Module: vision, datom. Action: edit.
Text: "A datom never names a file in place of its payload; paths depend on the setup."
Rests on: 29 Sep.

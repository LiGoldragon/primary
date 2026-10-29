Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md and Vision/ethosMonolith.md.
## 2026-08-11 — transcription corrected: schema-rust, ethos-rust; the generator name confirmed

> I didnt say shchema rest, I said schema-rust. that should be
> corrected. so ethos-rust is the analogue, yes

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed.
Corrects the 2026-08-10T18:49Z listener transcription above: the
dictated words were "schema-rust" and "ethos-rust", not "schema
rest" / "ethos rest". The shortcut generator repository name
**ethos-rust** is confirmed.

## 2026-08-11 — Datom does not generate Rust; Ethos does

> datom doesnt generate rust. ethos does. so I dont know what youre
> trying to say there, but its a dangerous line, and should be rooted
> out, wherever you got tha idea

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
answering the shortcut dispatch's mission line "Datom text in,
generated Rust out". Generation belongs to Ethos; Datom is
serialization/deserialization. The line is corrected in the standing
dispatch and the round bead.

## 2026-08-11 — no core-* split; three repos per component

> I dont know if we need a core-* repo. I dont see much point. so
> ethos can have all the code, minus the two signal repos, and so on
> (3 repos per component). other than reusable libraries of course,
> which we want to encourage for shared traits especially.

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
ruling the placement fork of the shortcut round: generated Nexus and
Sema types live in the component repository itself — no
core-<component> split, no central generated-types repository.
Component anatomy: the component repo plus its two signal repos,
three repos per component. Reusable shared libraries — shared traits
especially — are encouraged.

## 2026-08-11 — generated Rust is committed so language servers work

> rust generated from ethos; it should probably be committed, so
> tools like language servers can work normally. we can work out a
> way to ensure freshness

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
ruling the checked-in-versus-build-time fork: generated Rust is
committed, so ordinary tooling — language servers — works normally.
A freshness mechanism is deliberately left open for later.

## 2026-08-11 — the router sorts signals; a universal signal repo wraps them

> the signal ID must be how agents interpreted my vision for an
> ability for the router to differentiate between signal types for
> sorting them out. router is for signals to go across the network.
> it should be an enum in a universal signal repo that all components
> depend on, which wrap the objects. that universal-signal repo could
> also serve other functions that all signals need to deal with
> (handshake payload basically)

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
on the agent-coined numeric "Signal contract ID" scheme: the real
vision is the router — which carries signals across the network —
differentiating signal types to sort them. The mechanism is an enum
in a universal signal repo all components depend on, wrapping the
signal objects; that repo may also carry what every signal must deal
with, essentially the handshake payload. The numeric ID/registry
scheme is superseded. The repo's name is not yet ruled.

## 2026-08-11 — the de/serializer: positional, direct to typed structs, no self-describing tags

> 1 yes, direct to typed structs. 3 what is reflection? no
> self-describing tags

— psyche, 2026-08-11T13:53+02:00 (Designer session 012fbf07), typed,
ruling the Datom de/serializer anatomy. "1 yes" confirms the
Designer's framing: schema-driven positional reading — the reader
walks the expected type, text never names fields, writing is the
exact reverse projection. Decoding lands directly in the typed Rust
structs, no intermediate document tree. No self-describing tags in
the text. "what is reflection?" awaits the Designer's plain
explanation before any ruling on codec frameworks.

## 2026-08-11 — datom is just a renamed dotos; no new repo was needed

> datom is just a renamed dotos, so there was no need to create a new
> repo. unless I missed something.

— psyche, 2026-08-11T13:53+02:00 (Designer session 012fbf07), typed.
The Datom repository is the existing dotos repository renamed — not a
fresh creation; the fresh datom repo made earlier this day was
unnecessary. Aligns with the standing rename-over-recreate rule and
with parserIsTheParser.md: one parser, nothing else implements its
own parsing logic.

## 2026-08-11 — Datom and Ethos are different languages; a shared substrate, not a shared parser

> no, I dont think so. they share an approach, but are different
> languages. they could have a shared substrate (traits with a shared
> implementation and types)

— psyche, 2026-08-11T14:06+02:00 (Designer session 012fbf07), typed,
rejecting the Designer's inference that ethos-rust consumes datom's
parser. parserIsTheParser.md governs one language's parser;
cross-language it does not apply: Datom and Ethos share an approach
but are different languages. What they may share is a substrate —
traits with a shared implementation and types. Coheres with the
same-day ruling encouraging reusable shared-trait libraries.

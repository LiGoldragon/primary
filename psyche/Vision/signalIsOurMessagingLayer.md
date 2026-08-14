# Signal is our messaging layer

## 2026-08-08T11:45:33.818Z — Signal is our messaging layer

Context (agent-authored, separate from the psyche's words): The direct typed human prompt included an older quoted
2026-04-25 definition before the psyche's response. That quoted
archaeology is not repeated here as psyche speech. Transcript:
/home/li/.claude/projects/-home-li-primary/55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2.jsonl:636

> thats old as fuck. very vague
>
> Signal is our messaging layer, and the CLI's role is to transform text into Signal. So we used to call it NOTA, now it's DOTOS. I don't even know if I like that new name actually. But yeah, yeah, I don't think it's a good name. I don't think it sticks. It's been bothering me for days. We can talk about a new name for it. Not a big deal. So it's the textual form, the CLI transforms the textual form into actual Signal. And Signal, you know, we need to flesh that out better too. It's kind of been really ad hoc. I feel like all the demons like use a different approach. But yeah, it's a RKYV, portable RKYV. And let's like start defining all of this properly, you know, in like a place where let's start making a clean reference point for everything. And I think that's the standards repo, but I don't even know if I like the name of that repo either. Not a big deal.

— psyche, 2026-08-08T11:45:33.818Z (Designer session 55d18f4f)

## 2026-08-13 — signal must be specified: portable rkyv; CapnProto as universal signal

> we have to also be specific about what signal is, because I don't
> want to have to specify, like, R-K-Y-V binary, you know, and we
> have certain standards on how we use this, like, it's portable, I
> think, is the right term, where the settings are set on R-K-Y-V
> to make the format consistent, because of BigEndian and
> SmallEndian and other things. And you can explain me the dialect
> there, too.

> So, the closest thing to R-K-Y-V for cross-platform is CapnProto,
> C-A-P-N-P-R-O-T-O. It's a zero-copy binary format. So,
> transcodable could mean also transcodable in CapnProto, which we
> would call, like, universal signal. So, maybe it's not the right
> term, and we don't have to be afraid to use more elaborate terms
> if we want to describe what this behavior is specifically.

— psyche, 2026-08-13 (Designer session 6863ef19), dictated, from
the Mentci front-end problem (mentci.md): a non-Rust front-end
cannot speak rkyv signal. CapnProto floated as the cross-platform
zero-copy form — provisionally called universal signal, term not
final. Designer-flagged naming tension: the router-enum "universal
signal repo" (threeStacks.md 2026-08-11, name unruled, bead
primary-xqb.8.3) and this CapnProto form now share the phrase.

## 2026-08-13 — the router repo concept is routable signal

> routable signal then

— psyche, 2026-08-13T18:09+02:00 (Designer session 6863ef19), typed,
resolving the Designer-flagged collision above: the router-enum
repo concept (threeStacks.md 2026-08-11; bead primary-xqb.8.3) is
routable signal; universal signal stays with the CapnProto
cross-platform form.

## 2026-08-13 — universal signal is a capnp transcodable implementation of ethos; not there yet

> right, which is why it would be a capnp transcodable
> implementation of ethos. we arent there yet

— psyche, 2026-08-13T18:09+02:00 (Designer session 6863ef19), typed,
on the research finding that no Rust-to-capnp-schema tooling exists
anywhere: the capnp emission is an ethos implementation concern — a
capnp transcodable implementation of ethos — and is deferred.

*(2026-08-14 annotation, consistency audit: "transcodable" and "capnp transcodable" in the 2026-08-13 entries above predate the code/encoded vocabulary drop; Transcodable as a trait name did not survive the drop (traitsAsCapabilities.md 2026-08-13 "transcodable falls with the drop"). The CapnProto cross-platform capability concept and universal signal terminology stand; successor naming for the transcodable capability is open per traitsAsCapabilities.md 2026-08-13.)*

## 2026-08-14 — signal is fully typed; both sides know the full schema; the "label" frame is confused

> this doesnt make any sense to me. signal is fully typed; both
> sides know the full schema. labels? that flow must be confused.
> and your answer worries me a bit too. lets talk about this in
> detail, because its really importand and you all seem to be
> missing the point.

— psyche, 2026-08-14T15:01+02:00 (Designer session ba906ae2),
typed, on being shown Codex's Stage 2 question ("How does an
operation label such as Record, Subscribe, or Recorded survive
into Signal without generating single-field wrapper types? Does a
Signal envelope own that identity, or do the Protos role traits
carry it?") and the Designer's variant-name answer. Rules the
question's frame confused rather than answering inside it; opens a
detail conversation — the fleshed-out anatomy lands in following
entries.

## 2026-08-14 — the ethos generates the type in rust

> deleted the name from the type system? what the hell is going on
> here? The ethos *generates the type in rust*

— psyche, 2026-08-14T15:09+02:00 (Designer session ba906ae2),
typed, on the Designer's account of Codex's Stage 2 candidate,
whose own wording is: "The left names are Ethos operation labels.
They do not emit Rust wrapper types in this candidate." Ruled: an
operation name in an Ethos section is not a runtime label — Ethos
generates the Rust type; the name reaches Rust through generation.
The exact generated shape for `Record.Entry` (branch of the root
enumerator alone, or also a standalone type) is the question the
Designer posed back; the answer lands in a following entry.

## 2026-08-14 — signal. signal. signal. — the serialized form's name is signal

> signal. signal. signal. that is what we call it. signal. lets
> find a place to explain that clearly

— psyche, 2026-08-14T15:12+02:00 (Designer session ba906ae2),
typed, after the Designer glossed rkyv's "archive" term for the
serialized zero-copy bytes. Ruled: our name for that form is
signal — "archive" is rkyv-crate-internal vocabulary and does not
name our form. The psyche asks for a place that explains this
clearly; placement proposal pending.

## 2026-08-14 — version should be 0 1 0; version 1 is the first stable release

> version should be 0 1 0 - well keep version 1 for the first
> stable release

— psyche, 2026-08-14T15:24+02:00 (Designer session ba906ae2),
typed, on the `Interface.{1 0 0}` header in Codex's proposed
signal.ethos. Interfaces begin at 0 1 0; version 1 is reserved for
the first stable release. Adjusts the version content shown in
circulating examples (the blessed observer fixture carried
`Interface.{1 0 0}`).

## 2026-08-14 — each section has its own parsing context; the input section is an enum; variants carry data

> So what we're talking about here is the body section, the first
> position, maybe the second also. Well, I don't know. I kind of
> would like to know what each of these actually is. But the first
> section anyway is where the, I mean, this pattern is visible in
> the second and third and fourth section as well. I mean, the
> pattern is visible everywhere, but each section has its own, I
> need to know what the vocabulary here is. So I'm going to use
> some vocabulary and it might not be the right vocabulary, okay?
> But it's concepts that matter. So each section has its own
> parsing context. So the first section where record.entry is, in
> that section, we're 100% going to deal with shape-defined
> entries. So different shapes are going to give us different
> types. So when we get a symbol ahead and a head followed by a
> symbol, like record.entry, then that means it's going to be a
> certain kind of type. And I think that this section is an enum
> that we're looking at. So those are different kinds of queries
> that this interface can receive. So these are all the variants.
> Record is a variant, subscribe is a variant. And the entry type,
> actually the symbol entry is really a, I wouldn't have written
> it this way. Although I think it could be valid, I'm not sure.
> But essentially the reason why you would use entry is, I think,
> I don't know if I want to actually allow this style, but maybe
> we can actually create a different, an alternative, because
> entry is not really a type. And let me explain. So the data
> that, so record essentially is a data carrying variant. And the
> data that record is going to carry is a struct. Well, actually,
> maybe I'm taking back what I just said, because if it's a
> struct, then it has to have a name. So yeah, I'm not sure, like
> does Rust let data carrying variants carry anonymous structs?
> And would that even be a good idea? I don't think so. So yeah,
> essentially the shape, the type of a shape like that in this
> section, I think it's called the input section and maybe it's
> not the right. Is it's going to be a data carrying variant. So
> let me know how that works on the Rust side. Like what does that
> Rust code look like? And what are the different possibilities of
> how this can be done on the Rust side so that we can decide
> which target we want to go for, and then we'll know how to
> answer the whole question.

— psyche, 2026-08-14T15:24+02:00 (Designer session ba906ae2),
dictated, reading Codex's proposed signal.ethos body. The psyche's
own caveat inside the dictation: the vocabulary may not be right —
the concepts matter. Carried: each section has its own parsing
context; sections deal in shape-defined entries — different shapes
give different types; the first (input) section is an enum — its
lines are variants (Record, Subscribe), and an operation like
Record is a data-carrying variant; whether the `Record.Entry`
style (payload as a named type) should be the only style, or an
alternative inline-payload style should exist, is explicitly
undecided. Ends with a direct question — the Rust-side
possibilities for data-carrying variants — answered by the
Designer in-session; the target-shape ruling lands in a following
entry.

## 2026-08-14 — head and a symbol means a data-carrying variant; the data is the type the symbol refers to

> Right, so that section in the interface file is shape defined.
> And one of the shapes is this head and a symbol. And that means
> a data carrying variant with the data being the type that the
> symbol refers to. And let's make sure together so that we
> understand all of this. What are the other shapes that could
> live in that section and in other similar sections? And how
> could we make, if those different sections have the same shape
> defined options, then how could this code be reused between
> them?

— psyche, 2026-08-14T15:32+02:00 (Designer session ba906ae2),
typed, ruling the target from the Designer's Rust-side options:
the interface file's variant sections are shape-defined; the
head-and-symbol shape (`Record.Entry`) is a data-carrying variant
whose data is the named type the symbol refers to (the tuple
variant carrying a named payload type, not a struct variant or
positional fields). The other shapes of these sections, and the
code reuse between sections sharing the same shape-defined
options, are posed as the next anatomy questions.

## 2026-08-14 — the placement carries the meaning; inline struct and enum shapes are shorthands deriving named types

On the Designer's logged title "head-and-symbol is a data-carrying
variant":

> no. that particular placement is. what is the placement? lets
> look at the ethos schema of an interface file. The type found in
> that field (Vec<Something>) is what implementes ShapeDefined
> (the Something). Lets look at what that code should look like

On the head-`.{…}` inline-struct shape in a variant section:

> if the anonymous struct is a bad idea, which I think it is, it
> could be a shorthand for two types, where the struct would get a
> derived name (RecordData?)

On the Designer's vector reading of head-`.[…]` in a variant
section:

> A vector makes no sense; we are defining types not creating
> instances of them. that would be an enum, and as with the
> struct, it could create a derived-name type.

> In simple cases, that syntax will be much easier to read and
> write than referring to another type and using a whole other
> line for that type.

On head-and-symbol meaning a type definition in the types section:

> of course, the input and typedef section are for different
> types. show me you understand this in code (not the current
> code, but using your understanding of what it should be.). you
> can mine past sessions for more context if you need

— psyche, 2026-08-14T18:01+02:00 (Designer session ba906ae2),
typed. Rulings carried: (a) a shape's meaning belongs to its
placement, not to the shape — the schema field's element type (the
Something in `Vec<Something>`) is what implements ShapeDefined,
and the input and typedef sections are for different types; (b) an
anonymous struct is a bad idea — the inline `.{…}` shape in a
variant section could instead be shorthand declaring two types,
the payload struct receiving a derived name (`RecordData` floated
with a question mark, not ruled); (c) `.[…]` in a variant section
is not a vector — sections define types, not instances — it would
be an inline enum, likewise deriving a named type; (d) the inline
shorthands are motivated by ease of reading and writing in simple
cases over spending a separate line on a separate type. The
Designer is asked to show the interface-file schema understanding
in code; that sketch follows in-session.

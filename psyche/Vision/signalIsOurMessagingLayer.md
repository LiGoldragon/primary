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

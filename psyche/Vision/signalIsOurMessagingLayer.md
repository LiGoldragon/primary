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

# Rust tuples forbidden; positional-fields law scope — 2026-07-30

Context: this session's audit of the nomos train (see
`reports/NomosTrainAddendum-2026-07-30.md`, Decision 3) leaned that the
positional-fields law ("all fields are positional, field names are illegal
everywhere") binds "the wire always and all new Rust data shapes," tolerating
existing named-field rkyv-archived structs as legacy debt. A companion audit's
"Finding 2" flagged roughly 60 internal Rust structs with named fields for
review under that reading; this session did not locate that audit's exact
source file, only the psyche's characterization of it in the management
session.

Agent text answered: none. This is a direct psyche statement in a management
session, not a reply to written agent text.

Psyche ruling (verbatim): "Tuples are forbidden in Rust. ... I know that a
new type is a tuple, but that's the only exception. I don't consider it to be
a tuple." Also: "We should also put that in the standards. It used to be a
thing, and we deleted everything."

Reading: Rust forbids tuples — both ad-hoc tuple types and tuple structs with
two or more fields — with the single exception of the newtype pattern (a
one-field wrapping struct), which the psyche does not consider a tuple. This
is a restoration: the rule previously existed in
`git/github.com/LiGoldragon/standards` and was lost in a deletion; it has
been re-added to `good-rust-practices.md` in that repo
(commit bc61e427ab5e on `main`).

Scope clarification, from the same statement: the positional-fields law is a
rule about the protos languages' data model — encoded forms, wire, NOTA
records — not a Rust source-style rule. Rust structs use named fields. Named
fields and the positional-fields law are not in tension; they govern
different layers.

Disposition of prior readings — both dissolved by this ruling:

- Nomos train overnight addendum, Decision 3: the lean that the positional
  law binds "all new Rust data shapes" is superseded. New Rust structs use
  named fields, as before; the only Rust-source restriction from this ruling
  is the tuple ban above.
- Audit "Finding 2" (~60 named-field internal Rust structs flagged for
  review): dissolved. Those structs are correct Rust style under this
  ruling and require no review or migration on this basis.

This is forward-only provenance: it does not edit
`reports/NomosTrainAddendum-2026-07-30.md`, which stands as a record of what
was leaned overnight. This entry records the psyche's ruling that supersedes
Decision 3 and the associated audit finding, given 2026-07-30 in the
management session reviewing the nomos train.

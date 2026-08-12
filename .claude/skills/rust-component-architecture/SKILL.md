---
name: rust-component-architecture
description: 'How we design our components.'
---

Every component is a daemon speaking Signal.

## The component

`<component>` is the repo holding the daemon and its logic; its daemon binary is `<component>-daemon`.

`signal-<component>` is the wire type repo: the typed vocabulary of the component's public wire surface.

`meta-signal-<component>` is the owner's wire type repo: policy and configuration vocabulary. It is never optional — configuration flows through it.

Three repos per component: the component and its two signal repos. There is no core-* split — reusable libraries, shared traits especially, are their own repos, encouraged.

The CLI binary is `<component>`; the meta CLI is `<component>-meta`.

## The daemon

Everything is in the daemon. It loads its domain and holds the whole
thing — every object as its own specifically typed object, a specific
type for every kind. It thinks in typed values, never in text: no
text arrives on its wire and none leaves it.

Each daemon owns its own sema database — its typed durable store,
reached only through the sema-engine library, in a `.sema` file. There
is no central storage daemon. Policy state and working state live in
that one store; policy changes only through meta-socket mutation.

A daemon starts from a single argument: a signal-encoded Configure
message. A virgin daemon applies it as first configuration; a daemon
with a populated store resumes from its store. The same Configure type
is accepted live over the meta socket. With no configuration, the
daemon waits in an unconfigured semi-started state — it never guesses.

A daemon may be a Signal client of any number of peer daemons.

## Signal — the wire format

Signal is the messaging layer. A message is an rkyv binary archive —
typed, portable, validated on receive. Frames are length-prefixed on
the socket. Nothing else rides the wire: no JSON, no text, no second
protocol.

Every daemon opens two sockets: the ordinary socket, for any
authenticated peer, and the meta socket, for its owner. Every surface
answers with typed replies, including a typed refusal — errors are
vocabulary, not strings.

The wire vocabulary is versioned by its repo's crate: the crate's semver is the wire's semver, and consumers pin it.

## The CLIs

The CLI's role is to transform text into Signal. It is the boundary
where the textual form ends and the binary world begins.

A CLI speaks to exactly one daemon — its own. It opens no database,
reaches no other component, and carries no logic worth keeping: it is
eventually obsolete machinery, kept thin. `<component>` fronts the
ordinary socket; `<component>-meta` fronts the meta socket.

Every component process takes exactly one argument and no flags. The
CLI accepts text or a signal-encoded file; the daemon accepts only the
signal-encoded form.

## The wire type repos

A wire type repo declares vocabulary and nothing else: no runtime, no
actors, no async machinery. It owns the frame envelope and its
encode/decode, the protocol version, a closed enum of request kinds
with their paired replies, and the typed payload of every operation.
No catch-all variants — the vocabulary is closed.

Operations are verbs in verb form: `Submit`, not `Submission`.
Replies are the verb's past tense; rejections name themselves.
Storage classification vocabulary never appears on the public wire —
what a peer may ask is domain language, not database language.

Every record kind lands as a concrete text example with a round-trip
test before its type is final: the example is the falsifiable
specification.

## Traits first

Every method call lives in a trait; an inherent method is a trait not yet extracted — the method's name already names the concept. New code starts from the trait; ported code extracts it. The trait pass comes before any body is written: traits are the specification expressed in code.

Defaults are given wherever a default is expressible. Rich
requirement chains (sub-traits) are what make defaults possible —
designing them is the work.

Reuse or extend the existing trait when the domain is clear. A trivial site may take an exception, noted where it is taken. Anything else without a clear placement stops and escalates.

Traits live on data-bearing types. A zero-sized type with behavior is a namespace pretending to be a thing — the verbs belong to a real noun; never mint one to house floating verbs.

A duty that answers a constant question is data — an associated constant — never a function. Functions are behavior only.

Identity is trait-borne: an encoded form fingerprints itself — by
default, the hash of its rkyv archive — and every reference names
its target by that encoded name, never by spelling.

## No free functions

`fn main()` is the only production free function. When no owning
type exists, the model is incomplete — name the missing type
instead of writing a floating verb. A function stored as data — a closure or fn pointer in a constant, field, or map — is a free function in data's clothing. Data carries names; traits carry behavior.

## How components fit together

Peers depend on each other's wire type repos, never on each other's
daemons. The contract is the whole relationship.

Observation flows up, authority flows down: state is observed through
push subscriptions — a typed snapshot on open, typed deltas after —
and commanded through the owner's mutation vocabulary. Polling is
forbidden; a correct system goes quiet when nothing changes.

When one intent spans several components, the issuer commits on the
first success and records divergence on failure — no distributed
rollback, no all-or-nothing stall.

One capability, one component. A component is sized to be held whole
in one mind — human or model; when it outgrows that, it splits.

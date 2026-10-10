# Protos MVP Stream Gate — 2026-08-02

## Morning state

`primary-vq6.6` is blocked on missing psyche rulings, not on a failed build or
an implementation defect. No `.6` code has begun. This pass changed only bead
bookkeeping and this report; it ran no build, test, or Nix command.

The current completed producer train through `.7`, after the Slice 7 audit
remediation, is:

| Surface | Version | Pushed `main` head |
| --- | ---: | --- |
| `core-ethos` | `0.25.0` | `83feebbd34b66d493a0a3c7ffea68dab1dd7873c` |
| `protos` | `0.5.0` | `f5d90522da03bac51931d28ce8947b3b6b717f50` |
| `core-logos` | `0.24.0` | `f02ce18c93f85ce44e6e2e291a2bd514346eccbe` |
| `core-nomos` | `0.37.0` | `afc70296b86ef9fa2b523040d24e11ade38f9d1c` |
| `rust-logos` | `0.27.0` | `9109c2a4e172db9cde633760fac932ece69f25f9` |
| `nomos-engine` | `0.13.0` | `39f9187cbf1b870ef169ed88595240fd304a7cea` |
| `language-engine-witness` | `0.22.0` | `a2f7595af5e0734b46a17222915489ac44236a1d` |

The already reported green evidence remains the current evidence. Slice `.1`
passed its complete Cargo suite and all eight flake checks; `.2` passed its four
producer and witness Nix gates; `.3` proved the socket-free library, build
script, installed CLI, and Nix derivation; `.5` passed its full bounded Cargo
and Nix gates; `.7` passed the bounded Cargo and full Nix gates in every changed
producer and in the end-to-end witness. Slice `.7` additionally proved a real
`signal_domain::Domain` keyed write/read/reopen cycle and refusal of a same-ID,
different-layout table registration. This report does not reinterpret or
extend those results to Stream behavior.

## Direct authority and the boundary around it

The reviewed Spirit Interface source directly fixes these authored forms:

```ethos
Stream.Observer.{ObserverFilter ObserverSubscription ObservationEvent}
Stream.Intent.{IntentFilter IntentSubscription IntentEvent}
```

The source therefore establishes the `Stream` head, the authored stream names,
and the ordered three-type payloads for Observer and Intent. A separate direct
psyche ruling establishes that the universal `StreamOpen` and `StreamEvent`
traits live in the `protos` crate alongside Input, Output, and Refusal.

That is the ruled Stream surface available for implementation. It does not by
itself specify the encoded representation of a dotted chain, how Nomos binds
or expands it, the complete Logos item family, trait signatures, token and
close semantics, transform refusals, or runtime routing ownership.

The current `WholeEthosOperatorApplication` is narrower than a general chain
model. Its portable archived value contains exactly three positions:
`operator`, one authored `name`, and `fields`. It can faithfully carry the two
reviewed `Stream.Name.{...}` applications, but it cannot carry an arbitrary
sequence of chain parameters such as a second dotted argument with its own
role. Changing this type or its fields is archive-visible. That change cannot
be made before the intended chain meaning and compatibility boundary are
ruled.

## Non-authority design material

`reports/NomosStreamDesign-2026-08-02.md` begins by identifying itself as a
manager proposal for psyche review. Its object-first reading rule, a second
chain-binding tuple, arity-selected binding, `Structural.Family`, multi-item
templates, generated inline type names, token-wrapping stream newtypes,
associated-type impl sketches, generic daemon registry, and one universal token
model are all Claude/agent proposals. They are useful question-forming material,
not authority. None is an approved default, and this report recommends none of
them.

## Downstream effect

The bead graph makes `.6` a direct dependency of `primary-vq6.8`, the first
complete Spirit landing. `.5` and `.7` are closed, so Stream is the remaining
declared gate before `.8` can satisfy its observer-event socket witness. The
later `primary-vq6.12` rename landing is downstream of `.8`.

`primary-vq6.9` and `primary-vq6.10` do not currently declare a bead dependency
on `.6`; they depend on the completed offline generator and Interface emission.
Their own stream-bearing contracts, if any, cannot reuse a general Stream
mechanism until the same rulings exist. No dependency edge is inferred beyond
the recorded bead graph.

## Ranked psyche questions

1. **What is the exact encoded application and dotted-chain shape?** The
   reviewed source proves `Stream.Name.{three types}`, while the current
   archive stores the head, exactly one name, and payload fields. The ruling
   must define whether the name is a distinguished encoded position or one
   member of a general ordered chain, how further dotted arguments are
   represented, and which portion of that representation is stable archived
   meaning. This answer determines whether the existing carrier remains valid
   or must change archive-visibly.

2. **What is the exact authored Nomos form for chain binding and family
   emission?** No ruling currently defines how a transformer declares bindings
   for chain positions separately from payload positions, how those positions
   are typed, or how one invocation emits several items. The proposed second
   tuple, arity selection, and `Structural.Family` spelling are non-authority.
   The ruling must fix the structural form and its evaluation meaning before a
   codec or evaluator can claim correctness.

3. **Which exact Logos items constitute one Stream family, and who supplies
   every identity?** The implementation needs a closed list of emitted
   newtypes, trait impls, request/receipt/event relationships, and any close or
   refusal types. It also needs to know which identities are authored and
   translator-assigned, which may be derived by a ruled mechanism, and whether
   any visible helper type exists at all. The Claude sketch of a stream-handle
   newtype and generated role names does not settle those questions.

4. **What are the complete `StreamOpen` and `StreamEvent` contracts?** Their
   names and home are ruled, but their associated types or methods, their impl
   targets, and their relationship to Input and Output are not. The ruling must
   state which reviewed query, receipt, event, or stream types implement each
   trait; what types each contract exposes; whether a stream event also has
   Output membership; and whether the receipt participates in either universal
   membership. Without that, Rust emission cannot be checked against a public
   contract.

5. **What is the `SubscriptionToken` model?** The Interface fixture establishes
   subscription records that contain `SubscriptionToken`, but it does not
   establish whether tokens are one universal nominal type, distinct per
   stream, or paired with a type-level stream identity. The ruling must also
   fix who allocates a token, what equality and archive identity mean, and what
   information is available for runtime routing.

6. **What is the close interaction, including receipt and refusal?** The
   reviewed three-position Stream payload does not name a close request, close
   receipt, or close refusal. The live-loop acceptance nevertheless needs a
   defined termination path. The ruling must identify the public close request
   shape, whether closing produces a receipt, which refusal types can cross the
   boundary, and how close relates to the open token and stream family.

7. **Which failures are typed transform refusals, and at which boundary do
   they occur?** General chain support introduces possible excess or missing
   chain arguments, payload arity mismatch, wrong-position types, unresolved
   identities, duplicate bindings, and unsupported family output. The ruling
   must establish the meaningful refusal classes and whether they belong to
   Ethos decoding, Nomos projection, or Logos/Rust emission. The proposal's
   arity-refusal sketch is not authority.

8. **Who owns socket routing and the live Stream runtime?** The trait home does
   not decide whether subscription registries, token routing, event
   publication, and close handling live in each component daemon, a shared
   runtime, or another process boundary. The ruling must fix the owner of each
   responsibility, whether one connection can carry multiple streams, how an
   event selects its subscription, and which generated versus handwritten
   layer crosses the socket. Those choices define the `.6` live-loop witness
   and the integration obligation inherited by Spirit.

Until these questions are ruled, starting `.6` would turn an archive-visible
carrier change and a public runtime contract into agent-authored authority.

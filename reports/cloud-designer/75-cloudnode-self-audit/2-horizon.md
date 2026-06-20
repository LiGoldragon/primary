# Critic 2 — horizon-rs `CloudNode` change

Adversarial review of the `NodeSpecies::CloudNode` addition across
`species.rs`, `node.rs`, and `tests/horizon.rs`. All paths absolute.

The verdict in one line: the change is a textbook violation of the
workspace's own `skills/typed-records-over-flags.md`, the new facet is
write-only dead state with zero consumers, the "Metal substrate for a
cloud VM" choice is an unvalidated honesty hole, and the doc-comments
outweigh the logic by an order of magnitude — including a copy-pasted
fixture comment that describes the wrong species.

## High

### H1 — `cloud_node` grows the exact flag-bundle the house skill names as the canonical smell

Location: `/home/li/wt/github.com/LiGoldragon/horizon-rs/cloud-node-species/lib/src/node.rs:152-176` (`BehavesAs`), `:178-192` (`TypeIs`).

`skills/typed-records-over-flags.md`, Form 3, names the offending
struct *by name*:

> A `behaves_as { virtual_machine: bool, bare_metal: bool, iso: bool }`
> triplet is one enum with three variants: the struct form let
> `(true, true, false)` type-check though it was illegal; the enum form
> makes the illegal state unrepresentable.

This change adds `cloud_node: bool` to that very `BehavesAs` struct (now
11 bools) and `cloud_node: bool` to `TypeIs` (now 11 bools), widening the
illegal-state space instead of collapsing it. `BehavesAs` and `TypeIs`
together encode a *single closed choice* — the node's species — as 22
independent booleans, of which `2^22` combinations type-check and exactly
11 are legal. `TypeIs` is literally `NodeSpecies` re-encoded as a
one-hot bool vector (`TypeIs::from_species`, `:194-210`, is a hand-rolled
one-hot encoder: eleven `matches!(s, NodeSpecies::X)` lines). That is the
definition of a flag bundle wearing a struct disguise.

Why it is bad: the type system has stopped doing its job. Nothing
prevents `TypeIs { center: true, edge: true, cloud_node: true, .. }`,
nothing prevents `BehavesAs { virtual_machine: true, cloud_node: true }`
(which the prose explicitly calls impossible), and every consumer must
trust that projection upheld the one-hot invariant by hand. The skill's
diagnostic — "does the yes carry data / is this a closed-set choice
wearing a struct" — answers yes on both counts here.

Fix: `TypeIs` should not exist; it is `NodeSpecies` and the projection
already *has* the `NodeSpecies`. Consumers that need "is this a center"
should match the species (or a derived `BehavesAs` enum), not read a
mirror bool. `BehavesAs` should be the Form-3 enum the skill prescribes
— a `Substrate` enum (`Metal | Pod`) makes `bare_metal`/`virtual_machine`
mutually exclusive by construction, and the role facets
(`center/router/edge/large_ai/next_gen/low_power`) are a derived set, not
eleven sibling bools. The `cloud_node`/`test_vm`/`iso` "lean profile"
facets are a third axis. Adding a species should extend an enum, not
sprout two more parallel bools in two more structs.

### H2 — `cloud_node` is write-only dead state: zero consumers anywhere

Location: produced at `/home/li/wt/github.com/LiGoldragon/horizon-rs/cloud-node-species/lib/src/node.rs:235` and `:247`; consumed nowhere.

`grep -rn 'cloud_node\|cloudNode'` across the entire repo (`*.rs` and
`*.nix`) returns matches only in `species.rs`, `node.rs`, and the test —
i.e. only the definition, the derivation, and the test that asserts the
derivation. There is no CriomOS module, no Nix gate, no Rust reader. The
doc-comment at `species.rs:42-43` *claims* "cloud-init network/ssh
injection and growpart are emitted by the CriomOS cloud-image module
gated on `behaves_as.cloud_node`" — that module does not exist in this
tree. The comment describes a consumer that was never written.

Contrast the claimed sibling `test_vm`, which at least appears once
outside its own definition (`proposal.rs:132`).

Why it is bad: this is dead code dressed as a feature. The facet is
emitted onto every projected node's wire output (`BehavesAs` has no
`skip_serializing`), bloating every node's serialized form with a field
nothing reads. "No dead code" and "the type is the contract" both fail:
the contract promises a gate that has no other side. A reviewer cannot
tell whether the derivation is even correct because nothing exercises the
output except a tautological test (see M3).

Fix: don't land the facet until its consumer lands in the same change. A
projection field with no reader is not a feature; it is a TODO that
compiles. If the CriomOS module is out-of-tree, the facet belongs in the
branch that adds the module, not ahead of it.

### H3 — the species↔substrate coupling the comments narrate is entirely unvalidated

Location: derivation `/home/li/wt/github.com/LiGoldragon/horizon-rs/cloud-node-species/lib/src/node.rs:220-235`; validation surface `:668-731` (Pod-only, never touches `CloudNode`).

The `species.rs:32-44` doc-comment asserts as invariant: a `CloudNode`
"is NOT a `Pod` guest — it is the bare machine it boots on
(`MachineSpecies::Metal`), has no `super_node`, and so derives
`virtual_machine` false." Nothing enforces any clause of that sentence.
`grep` confirms there is no validation keyed on `NodeSpecies::CloudNode`
anywhere. Concretely:

- A `CloudNode` declared with `machine.species = Pod` projects happily:
  `virtual_machine` becomes true, `bare_metal` false, `cloud_node` true —
  the prose-declared-impossible `(cloud_node && virtual_machine)` state,
  produced silently.
- A `CloudNode` with `super_node = Some(host)` is accepted; the
  Pod-only validators (`validate_pod_super_node`,
  `validate_host_set_single_arch`, `:668`/`:701`) early-return on
  non-Pod, so a Metal CloudNode pointing at a host is never checked.
- A `CloudNode` with empty `io.disks` derives `iso = true`
  (`iso = !virtual_machine && io_disks_empty`, `:222`) — a cloud droplet
  projected as an installer image. Nothing forbids it.

Why it is bad: the design moved the invariant from the type system into
English prose. `skills/typed-records-over-flags.md` is explicit that the
point of the typed form is "an incomplete record fails validation at
proposal time, not deploy time." Here an *illegal* record passes
validation at proposal time and only manifests as a broken image at
deploy time. The substrate is the one fact that distinguishes CloudNode
from TestVm (H4), and it is exactly the fact left unchecked.

Fix: if substrate is intrinsic to the species, derive it from the species
rather than letting the proposal author it independently — a CloudNode
*is* Metal, so projection should not read `machine.species` for it at
all, or a validator must reject `CloudNode` on `Pod` / with `super_node`
/ with empty disks. The honest typed form (H1) makes this free: if
`Substrate` is derived from species, the mismatch is unrepresentable.

## Medium

### M4 — CloudNode is a near-duplicate of TestVm with a flipped substrate (DRY / abstraction)

Location: `species.rs:23-30` (TestVm) vs `:32-44` (CloudNode); `node.rs:229` vs `:235`; test `tests/horizon.rs:446-496` vs `:539-589`.

The derivation for the two is *identical* — `let test_vm = type_is.test_vm;`
and `let cloud_node = type_is.cloud_node;` are the same line with a
renamed field. Both are described in their own comments as deriving "the
same lean shape": carry one self-named facet, set no role facet. The
*only* real difference is substrate (Pod vs Metal), and substrate is
already an independent `MachineSpecies` field — it is not a property of
the species at all in the current model (H3). So `CloudNode` and `TestVm`
are not two abstractions; they are one "lean leaf node" abstraction
photocopied, with a substrate the type system doesn't bind to either.

Why it is bad: `skills/abstractions.md` and DRY both say the same thing —
when the second case is the first case with one field changed, the field
is the abstraction, not a new copy. The right factoring is a single
`LeanProfile` / leaf-node concept parameterised by substrate, or the
Form-3 enum from H1 where `Metal`/`Pod` is a variant and "cloud vs
test" is a payload. Two hand-maintained parallel facets means the next
lean species is a third copy, and a fourth, each re-deriving the one-hot
bool by hand.

### M5 — the "Metal substrate for a cloud VM" choice reads as a hack to dodge Pod validation

Location: design narrated at `species.rs:37-43`; fixture `tests/horizon.rs:464-481`.

A DigitalOcean droplet *is* a virtual machine — it runs as a guest on
DO's hypervisor. The change models it as `MachineSpecies::Metal`. The
stated justification ("it is the bare machine it boots on") is a
viewpoint trick: from CriomOS's *inside* view the droplet looks like bare
metal, but the type `MachineSpecies` is documented (`machine.rs:9-11`) as
"pod (virtual) machines defer arch to their super-node" — i.e. `Pod`
means "this is a guest with a host." A droplet has a host (DO's
hypervisor); CriomOS just isn't the host. Choosing `Metal` is choosing
"no host-set, no super_node, no Pod validation."

Why it is suspect: the Pod path (`validate_pod_super_node`,
`validate_host_set_single_arch`, the whole host-set / image-exchange
machinery) is exactly the validation a cloud node would need to *skip*,
because its host is external. Modelling it as Metal is the path of least
resistance — it dodges the host-set requirement rather than modelling
"externally-hosted guest" honestly. The comment even admits the bootloader
must be flipped to `Mbr` and growpart/cloud-init bolted on, all the
hallmarks of a VM, while the substrate says Metal. That is the substrate
lying to make the validation pass.

Fix: if "Metal from CriomOS's view" is genuinely the right model, say so
in the *type* — e.g. a substrate variant `ExternallyHostedMetal` or a
`hosting: External` axis — so the choice is legible and a future reader
doesn't mistake a cloud VM for a datacenter server. Don't overload
`Metal` to mean both "real iron" and "VM we pretend is iron"; that
collapse is what makes the `iso`-on-empty-disks bug (H3) possible.

### M3 — the test is near-tautological; it asserts the projector copied a bool

Location: `/home/li/wt/github.com/LiGoldragon/horizon-rs/cloud-node-species/lib/tests/horizon.rs:502-537`.

`project_cloud_node_metal_derives_lean_profile` asserts
`doris.behaves_as.cloud_node` (true), `!virtual_machine`, `bare_metal`,
`!iso`, the five `!role` facets, and the `type_is` mirror. Every one of
these is a direct restatement of a one-line `matches!`/`matches!`-of-
substrate in the derivation. The test proves the projector did not
mangle a constant assignment — it cannot fail unless someone deletes a
line. It exercises no behaviour, no consumer, no edge.

Critically, the test asserts the *happy* shape and never probes any of
the H3 holes: it does not assert a `CloudNode`-on-`Pod` is rejected, does
not assert empty-disks doesn't become `iso`, does not assert `super_node`
is forbidden. So the one test for this feature validates only the path
that was never in doubt and is silent on every path that is actually
broken. A test that can only pass is not evidence.

Why it is bad: tests exist to catch the cases the author didn't hand-
verify. This one re-verifies what the author hand-wrote, in the same
file, by eye. The TestVm sibling test (`:599`) at least checks machine
facts surviving projection and the derived domain; the CloudNode test
strips even that down to bool-echo.

Fix: test the *consumer contract* (once it exists, H2) or the
*rejections* (H3): `CloudNode` + `Pod` → error, `CloudNode` + empty disks
→ error (or explicitly not `iso`). Assert something that can fail for a
real reason.

## Low

### L1 — copy-pasted fixture doc-comment describes the wrong species

Location: `/home/li/wt/github.com/LiGoldragon/horizon-rs/cloud-node-species/lib/tests/horizon.rs:441-445`.

The doc-comment on `cloud_node_metal()` reads:

> A test-VM Pod hosted on `prometheus` with a real root disk (NOT
> tmpfs), declaring its own disk size and physical location.

The function it documents builds a `NodeSpecies::CloudNode` on
`MachineSpecies::Metal` with `super_node: None` and no host
(`tests/horizon.rs:464-481`). It is not a test-VM, not a Pod, and not
hosted on prometheus. The comment is a verbatim lift from `test_vm_pod`'s
mental model and was never edited. It actively misinforms: a reader
trusting the comment believes this fixture is a hosted Pod.

Why it is bad: a doc-comment that contradicts the code it sits on is
worse than none — it is a false witness that survives review precisely
because it looks plausible. It is also direct evidence the fixture was
produced by copy-paste (M4), not authored.

Fix: rewrite the comment to describe what the function builds — a
DigitalOcean-style CloudNode on a Metal substrate, no host, MBR/GRUB,
real root disk.

### L2 — doc-comment bloat: ~25 lines of prose narrate two one-line assignments

Location: `species.rs:32-44` (13-line comment on one enum variant), `node.rs:164-175` (`test_vm`/`cloud_node` field comments), `node.rs:224-235` (12 lines of comment on two `let x = type_is.x;` lines).

The two load-bearing lines of derivation are `let cloud_node =
type_is.cloud_node;` (`:235`) and the `matches!` in `from_species`
(`:207`). Around them sit roughly 25 lines of comment re-explaining the
same lean-profile story three times (enum variant, struct field,
derivation site), plus the false-witness comment in L1. The
`species.rs:32-44` block re-derives, in English, facts the type already
states (`cloud_node` true only for `CloudNode` — that is what the
`matches!` says) and asserts the unenforced invariant (H3).

Why it is bad: comment volume tracks design *anxiety*, not complexity.
The author wrote three paragraphs to convince the reader the facet is
distinct from `test_vm` — which is precisely the tell that it *isn't*
(M4): if the distinction were real and typed, it would need no prose.
Comments that restate the code drift (L1 is the drift already happening)
and bury the one fact that matters (the unenforced substrate coupling) in
a wall of reassurance.

Fix: collapse to one comment at the type that states the *invariant and
who enforces it*. If the invariant is unenforced (H3), the comment must
say "UNVALIDATED" rather than narrate it as fact. Delete the per-site
restatements; the `matches!` is self-documenting.

## Nit

### N1 — `iso` derivation reads as a fall-through, not a decision

Location: `/home/li/wt/github.com/LiGoldragon/horizon-rs/cloud-node-species/lib/src/node.rs:222`.

`let iso = !virtual_machine && io_disks_empty;` defines "installer image"
as "Metal with no disks." With CloudNode now a Metal species, `iso` is
one empty-disk proposal away from firing on a cloud node (H3). The
boolean has no owning concept — it is a coincidence of two other facts.

Fix: when `BehavesAs` becomes the typed substrate/profile enum (H1),
`iso` is a profile variant, not an arithmetic accident over two other
fields, and "Metal + no disks + CloudNode" cannot collapse into it.

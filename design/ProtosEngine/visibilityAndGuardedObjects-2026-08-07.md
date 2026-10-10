# Visibility, Guarded Objects, Codex Approvals — 2026-08-07

Rulings from the psyche concluding the visibility research discussion
(same session as textualFormMetadataStore-2026-08-07.md).

## Ruling: invariant protection is visibility's only surviving purpose

Agent text answered (research taxonomy of visibility's five purposes:
shadowing prevention, invariant protection, API-evolution freedom,
capability control, cognitive surface reduction; Coldcard rng_get()
symbol-shadowing incident verified as evidence that name-bound
references are the attack surface).

Psyche: declaring stable commitments versus internals is a
"documentation problem"; invariant protection "seems to be the only
valid point."

Shadowing is structurally impossible in the encoded form (references
are absolute EncodedNames; no name-resolution step exists). Visibility
does not exist in Protos as a feature. What survives is authority over
mutation, not access to names.

## Ruling: guarded objects are a deferred idea, stored in the meta repo

Agent text answered: the guardian-set concept — the engine stores, per
object, the set of objects permitted to hold references to it, and the
sealed operation interface refuses (typed error, DAG-law style) any
operation creating a reference from outside the set. Enforced at
authorship, queryable in both directions, per-object granularity, no
unguarded write paths — strictly stronger than Rust's module-tree
privacy.

Psyche: "It's a cool idea. We don't have to do that now. We should have
a place to store ideas like that for the protos engine."

Deferred, not ruled into the design. Stored:
/git/github.com/LiGoldragon/protos-engine/ideas/guardedObjects-2026-08-07.md
(the dependency-sink repo serving as the engine's meta repository).

## Ruling: sealed Sema consumer trait approved (Codex hqu.26)

Agent text answered: Codex's blocker — Core Ethos raw
catalog/grammar/assignment constructors are public only because Sema is
a separate crate; he proposes a sealed Sema consumer trait plus
authority-driven Core preparation. Management recommended approval as
the Rust-expressible shadow of engine reference admission.

Psyche: "if you feel good about it, it sounds like you do, then I'm all
for it."

Conditions (management, unobjected): the public exposure of the raw
constructors dies in the same landing; the trait's name states the
authority boundary in correct naming; the site carries a
psyche-understanding annotation (approved direction, deeper psyche
understanding deferred — see
design/Spirit/psycheUnderstandingComments-2026-08-07.md).

## Ruling: colon-form parser proposal approved (Codex hqu.33)

Agent text answered: Codex's proposed shape — existing ApplicationRule
for one head followed by `.(` payload; Core Ethos context splits exactly
TextualName:TransformerHead; nonrecursive payload target refusing dotted
chains.

Ratified under the psyche's "I'm all for what you're saying" covering
management's recommendations. Condition: the dot-form transformer
application dies in the same landing (replacing design kills the
replaced); fixtures re-spelled in the colon form.

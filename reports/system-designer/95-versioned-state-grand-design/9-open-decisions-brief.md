# 9 — Open decisions: analysis and recommendations

The visual design (file 8 §17) isolated decisions it does not make. This
brief explains the four the psyche asked about — what the choice *is*, why
it is a real fork, the options and their trade-offs, a **recommendation**
(the owners / psyche decide), and how each interacts with the rest. A
running theme: **fail loudly and safely by default; add power when a real
case demands it.** For the concept prototype I will adopt the safe defaults
below unless told otherwise.

## Decision 1 — Where the branch/policy layer lands (the home layer)

**The question.** The reusable VC machinery is a stack: the payload-bearing
hash-linked **log** + **checkpoints**; the **commit-DAG / branches /
frontiers**; the **IntakePolicy / ConflictPolicy / Reducer** traits +
merge/rebase algorithms; the **RFC-6962 history tree**; and the
**BLS-attestation + remote mirror**. Does all of that live in `sema-engine`,
in a new crate, or beside the kernel handle?

**Why it is a real fork.** `sema-engine` is defined as the minimal typed
database engine — explicitly "not a daemon, not Kameo, not NOTA, not
Persona-specific." The mainline already put the conservative *log* there
(`versioning.rs`). But the upper layers pull in concerns sema-engine is
meant to stay free of: **crypto** (criome BLS), **wire/policy** (per-component
admission), and **merge orchestration**. Putting BLS and policy traits into
sema-engine would bend its "minimal engine" contract; scattering them across
components would violate `j487` (build once, reuse).

**Options.**
- *(a) All in `sema-engine`.* Least friction (the log is already there), but
  grows the engine's surface and dependency cone — BLS in the engine is the
  sharpest smell.
- *(b) A new reusable crate (e.g. `sema-vcs`) over `sema-engine`.* The DVCS
  layer, policy traits, history tree, attestation, and mirror live in one
  crate every component opts into; `sema-engine` stays the pure engine.
- *(c) Beside the kernel handle* (`Engine::storage_kernel()`). An escape
  hatch, not a clean architecture.

**Recommendation — a layered split (b on top of a-for-the-log).** Keep the
payload-bearing, per-family-identified **log + checkpoints in `sema-engine`**
(extend the mainline — it is the typed-engine's concern, and audit 211
already accepted sema-engine as the home for the first substrate). Put the
**DVCS layer in a new `sema-vcs` crate**: commit-DAG, branches/frontiers,
`IntakePolicy`/`ConflictPolicy` traits, merge/rebase, the RFC-6962 tree, and
the BLS-attestation/mirror. Rationale: this keeps `sema-engine` free of
crypto and policy while making the VCS crate the named, reusable thing
`j487` calls for ("create a dedicated crate once reuse is real and its
architecture is named" — it now is). Components depend on `sema-vcs` and
implement the two policy traits. **This is the one decision that should be
made *first*, because it frames where every other type lands.**

## Decision 2 — Default `ConflictPolicy`: last-writer vs typed-conflict

**The question.** When two branches concurrently write the *same key* and
you merge, what does the **default** resolver do (before any per-family
override)?

**Why it is a real fork.** This is the classic safety-vs-convenience split,
and it only bites *after* branching (single-writer-per-store rarely produces
same-key concurrency; branches/forks do). The default governs the rare case,
but the wrong default is *silent data loss*.

**Options.**
- *Last-writer-by-sequence.* Pick the higher-sequence write; always
  converges, zero ceremony — but **silently discards** the other concurrent
  write. No one is told an intent was dropped.
- *Hard-fail-as-typed-conflict.* Emit a typed `Conflict` entry
  (record-and-continue, jujutsu-style); the merge still succeeds at the log
  level, but the key is marked unresolved until the component's policy (or
  the guardian, or a human) resolves it. Safe and visible, at the cost of a
  "conflicted" view state for that key.

**Recommendation — default to typed-conflict; override to last-writer or a
commutative/CRDT merge per family where the family's semantics make it
safe.** For a coordination/intent store like Spirit, silently losing a
concurrent intent is unacceptable — the safe default must *surface* the
collision, not bury it. Last-writer is a per-family *opt-in* for families
that are genuinely last-writer-wins (a status flag, a cache cell); a
commutative family can opt into a real merge. The dangerous default (silent
clobber) is never the floor. This matches the "first-class conflicts" stance
and `jys2`-grade rigor: never trade correctness for convenience silently.

## Decision 3 — Is a migration reducer lossless enough for cross-schema merge?

**The question.** To merge two branches at *different* schema versions, you
must project the older branch through its `SchemaTransition` reducer to the
common schema. Is the reducer well-behaved enough that a three-way merge
across the schema boundary is *meaningful*?

**Why it is a real fork.** Migrations come in two shapes. An **isomorphism**
re-encodes the same information into a new layout (add a field with a
default, widen an integer, reorder) — projecting old→new is lossless and
cross-schema merge is well-defined. A **lossy/semantic** transform changes
information (drops a field, fuses two fields, derives a value, applies a
policy) — projecting through it does not round-trip, so a three-way merge
across that boundary can be undefined or silently wrong. The related trap:
the migration equivalence oracle *cannot* be digest-equality, because a
state-*changing* migration will never hash-match the old view.

**Options.**
- *Refuse cross-schema merge entirely.* Both branches must be at the same
  schema to merge; an old-schema branch must be migrated first. Simple, safe,
  never wrong.
- *Classify reducers as `Isomorphic | Lossy`* (a typed property on the
  transition). For `Isomorphic`, allow cross-schema merge by projecting the
  old branch forward; for `Lossy`, refuse and require migrate-then-merge.
  More power, more machinery, and the classification must be trustworthy.

**Recommendation — ship "same-schema-only merge" first (refuse cross-schema
loudly), and add the `Isomorphic`-reducer projection path only when a
concrete case demands it.** Most real migrations are expand-contract: the
**expand** phase is isomorphic (safe to merge across), the **contract** phase
is lossy (must migrate-then-merge). Encoding that as a reducer `kind()` is
the eventual answer, but it is not needed on day one — and refusing
cross-schema merge until then is never wrong, only less convenient.
Corollary for the equivalence oracle: verify a migration by **re-deriving
the new view from the old log through the reducer and checking *that* digest
against the migrated branch's checkpoint** — equivalence is "the reducer
applied to history reproduces this state," not "old and new states hash the
same."

## Decision 4 — git-ort virtual merge bases now, vs refuse multi-LCA loudly

**The question.** In a criss-cross topology (two branches previously merged
into each other, so they share *multiple* common ancestors) there is no
single lowest common ancestor. Do we implement git's "ort" strategy —
recursively merge the multiple ancestors into one *synthetic* base, then
three-way-merge against it — now, or refuse multi-LCA merges loudly until a
real case appears?

**Why it is a real fork.** A naive three-way merge picks one of the several
bases arbitrarily and can be *silently wrong*. The correct fix (virtual
merge base) is real complexity: it merges the ancestors *through the same
policy*, which for a stateful guardian means *recursively replaying through
admission* — subtle to get right. But criss-cross requires repeated
cross-merging of long-lived branches, which is **rare in a single-psyche
coordination store**.

**Options.**
- *Refuse multi-LCA merges loudly.* Detect multiple merge bases; fail with a
  typed error ("linearize or rebase one branch first"). Simple, safe, never
  silently wrong.
- *Implement virtual merge bases now.* Correct for arbitrary topologies, at
  the cost of the recursive-merge-through-policy machinery before there is a
  case to justify it.

**Recommendation — refuse multi-LCA merges loudly now; build virtual merge
bases only when a real criss-cross case appears.** The principle is the same
as decisions 2 and 3: **fail loudly rather than be silently wrong.** The
deferral is cheap because the topology is rare here, and the eventual
implementation is well-understood (git-ort) and *reuses the one primitive* —
the virtual base is computed by recursively merging ancestors through
`replay-suffix-through-policy`, so it is additive, not a redesign.

## Summary

| Decision | Recommendation | Safe default for the prototype |
|---|---|---|
| 1. Home layer | Log + checkpoints in `sema-engine`; DVCS + policy + attestation in a new `sema-vcs` crate | Prototype the VCS layer as its own module/crate over the engine |
| 2. Default `ConflictPolicy` | Typed-conflict (record, never silently clobber); per-family opt-in to last-writer / CRDT | Default = typed `Conflict` entry |
| 3. Cross-schema merge | Same-schema-only first; add `Isomorphic`-reducer projection later | Refuse cross-schema merge loudly |
| 4. Multi-LCA / criss-cross | Refuse loudly now; git-ort virtual base when a real case appears | Detect multiple bases, fail with a typed error |

The thread: each safe default is *never wrong*, only less powerful, and each
power-up is *additive* (a per-family override, a reducer `kind()`, a
recursive virtual base) that reuses the existing primitive rather than
reshaping it. That is what lets us defer them without painting the design
into a corner — the `jys2` posture of reaching for the best end-shape while
shipping the safe subset first.

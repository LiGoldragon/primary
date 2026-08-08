---
title: 536 — Engine stack + spirit — corrected ground truth and the make-it-properly plan
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema-rust-next, spirit, codegen, rust-native, contract-daemon-split, plane-type, token-lowering, ground-truth, correction]
description: |
  Corrects report 535's two wrong claims (runtime emitter framed as open
  debt; spirit framed as no-correct-exemplar per stale wv63). Verified
  ground truth from two subagent investigations: the engine codegen is a
  decided token-native migration (declaration half done, runtime half
  remaining + PlaneType unsettled); spirit's schema-plane split exemplar
  HAS landed and wv63 is retired (superseded by y88n). Then the concrete
  remaining work and the division of labour with the operator.
---

# 536 — Engine stack + spirit — corrected ground truth and plan

This report corrects **535's two wrong claims** and replaces them with
verified ground truth. The errors and their cause are owned in §4.

## 1. Engine codegen — the decided rust-native approach (correction #1)

**Verified state.** `schema-rust-next` generation has a *decided* target,
already mid-migration — not the open debt 535 implied.

- **The approach** (union of `4np2` + `de8i` + `0bw0`/`e6v5`, all High):
  **token-based, noun-owned lowering** — each Rust-model noun renders itself
  via `quote!`/`ToTokens`, cross-object plane logic becomes its own
  `PlaneType` rather than a god-struct, pretty-printed into checked-in
  visible `src/schema/*.rs`. Not "no source emission"; not derive-based for
  generation.
- **Done:** the declaration surface (aliases, newtypes, structs, fields,
  enums, variants, type refs, imports) via the `LowerToRust<Target>`
  per-noun trait (commit `453fc657`); streaming signal-frame support
  tokenized (commit `d8e0a37a`, today).
- **Remaining:** the runtime/plane/runner half — ~48 `RustWriter` god-struct
  `emit_*` methods (`self.line(format!(...))`) for plane namespaces,
  projections, trace/mail/route support, the nexus runner adapter, role-trait
  impls, actor lifecycle, upgrade support. Each must move to noun-owned
  `ToTokens`, and the **`PlaneType` does not yet exist**.
- **The operator already marked this as debt in code today** (`d8e0a37a`
  amended INTENT.md/ARCHITECTURE.md citing `0bw0`). The direction is settled;
  the per-noun decomposition + the `PlaneType` shape are "still being settled
  with the operator" (no record pins them yet).

Captured: `e6v5` (Correction, High) — recorded before this report.

## 2. Spirit contract/daemon — the split exemplar has landed (correction #2)

**Verified state.** 535 conflated two different splits and leaned on a stale
record.

- **The schema-plane split HAS landed** (commit `8d0e32cf`, 2026-06-04 18:21).
  `/git/github.com/LiGoldragon/spirit/schema/` now has three bounded files:
  - `signal.schema` — **wire-only contract**: operation roots `[State Record
    Observe Lookup Count Remove ChangeCertainty LookupStash]` + reply roots +
    payloads + codec. **No Nexus, no SEMA.**
  - `nexus.schema` — orchestration plane; **imports** `spirit:signal:Input`,
    `spirit:signal:Output`, `spirit:sema:ReadInput` rather than re-declaring.
  - `sema.schema` — storage plane; split `[WriteInput ReadInput]` roots.
  - This cross-schema import IS the "missing macro piece" wv63 said was
    needed. It exists and is in use; the emitter enforces the boundary
    ("wire-contract targets do not emit runtime role impls", report 320).
- **`wv63` is retired** — superseded by **`y88n`** (Correction, High,
  2026-06-05 14:18:56): *"The contract-daemon and engine-stack split should
  have Spirit as a proper exemplar; Spirit must not be left as an all-in-one
  pilot that agents describe as an explicitly non-copyable shape."* `y88n`
  was recorded **~3 hours before** 535's wrong framing and names that exact
  failure. wv63 still returned from queries with no supersession link, which
  is precisely how it misled 535. Now removed (archived). Tombstone in §5.
- **What genuinely remains:** the **repo-triad split** (`spirit` /
  `signal-spirit` / `meta-signal-spirit` as separate repos) is unbuilt — but
  **deliberately deferred** (spirit `ARCHITECTURE.md:494-500, 509-510`: keep
  the single crate so the Nix proof harness stays intact). That is a chosen
  deferral, not a missing exemplar. The schema-plane exemplar is real and
  good (operator 311:153 already called it "the current exemplar for the
  three-plane runtime shape").

## 3. What "make the engine stack and spirit properly" actually means now

The contract *shape* is largely done. The real remaining engineering is
narrower and concrete:

1. **Finish the runtime-half token migration** — convert the ~48 god-struct
   `emit_*` methods to noun-owned `ToTokens` lowering, and **introduce the
   `PlaneType`** that owns the cross-object plane split/projection logic the
   god-struct currently inlines. This is the live engine debt.
2. **Settle the `PlaneType` / per-noun decomposition** — the one piece no
   record pins down ("still being settled with the operator"). This is design
   work, and it is the *blocker* for (1): you cannot move the verbs onto the
   nouns until you know which noun owns the plane-split logic.
3. **Drive toward the orchestrated engine** (`y88n`'s "engine-stack" half →
   `mazv`: persona supervising introspector + schema daemon + triad
   components) — forward engine work, beyond contract shape.
4. **Intent/doc hygiene** (small): spirit's `ARCHITECTURE.md`/`INTENT.md`
   cite `gvaz` and `k4d9` ids that no longer resolve cleanly (id drift) —
   flag to the operator/repo owner.

## 4. What I got wrong and why (owned)

535 made two claims the psyche flatly corrected. Both were **point-reads
without a supersession sweep**:

- I read the `format!`/`self.line` count as a *settled design to question*,
  and never queried for the record that decides it — **`0bw0`** ("the string
  runtime emitter is debt to replace"), recorded hours earlier.
- I read **`wv63`** as current truth and never checked what superseded it —
  **`y88n`**, recorded ~3 hours before I wrote 535, reversing it by name.

The concrete process fix: when a record drives a claim, **sweep recent
records for a Correction/supersession on the same topic before trusting it** —
especially on a fast-moving day. Stale records return from plain queries; the
log's currency is not self-announcing. This is the `ui5d` discipline (do it
properly / use the verification depth subagents give) applied to intent
reads, not just code.

## 5. Tombstones

`wv63` (Clarification, High, 2026-06-04 11:43:53), removed — superseded by
`y88n` + commit `8d0e32cf`:

> spirit is an all-in-one single-repo pilot that deliberately DEFERS the
> contract/daemon repo-triad split — its own ARCHITECTURE.md states the
> repo-triad split (spirit, signal-spirit, owner-signal-spirit) is not
> represented in the pilot. Do NOT model contract schemas on spirit's shape
> (Input + Output + Nexus + SEMA in one schema); a contract is wire-only
> (Input/Output + records + codec) and the Nexus and SEMA planes live only in
> the daemon. No correct schema-derived contract/daemon-split exemplar exists
> yet; signal-upgrade carries the same all-in-one error in its lib.schema. A
> wire-only contract (Input/Output + records, no Nexus/SEMA) already emits no
> engine traits under schema-rust-next today, so contract schemas can be
> corrected immediately; the missing macro piece for a clean split is letting
> a daemon schema import a contract's Input and Output roots instead of
> re-declaring them.

(The wire-only-contract *definition* in wv63 remains true and is now
*satisfied* by spirit's `signal.schema`; it also lives in operator report
309 and record `l6zw`. Only wv63's "no exemplar / do-not-copy" conclusion was
stale.)

Per psyche 2026-06-05.

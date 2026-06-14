# Cross-lane review — operator vs designer implementations (Structural Forms epic)

A 9-agent review (scout + 8 adversarial reviewers) comparing what the operator
lane has on main against what the designer lane has on feature branches, across
the seven active epic repos. All branch/commit facts verified via `jj`/`git` on
2026-06-13/14. Per the Designer-Operator review protocol (designers ship
`next`/feature branches under `~/wt`; operator owns main + rebases; designer
reconciles rival designer branches *before* operator integrates).

## Headline — three findings

1. **The meta-signal drift is already fixed, correctly, by operator.** Verdict
   **CONSISTENT**. Operator rebuilt `meta-signal-spirit` as a schema-derived
   `Configure`/`Import` contract (`d5b5dde`, 2026-06-14 13:42) and spirit main
   imported it (`4ec746b` "import meta-signal contract from meta-signal-spirit" →
   deleted the local `schema/meta-signal.schema` + generated `meta_signal.rs`,
   re-exports `pub use meta_signal_spirit::schema::meta_signal::*`). The contract
   is byte-identical to the rebuild source. This is *exactly* the constraint from
   `skills/component-triad.md` / report 628 — operator did it while we were
   discussing it. **The only residual is documentation:** report 628 / commit
   `5dcac7cd` now describe a superseded drift state (corrected below).
2. **The reaction frame is consistent across all three designer lanes** —
   triad-runtime `next/generic-reaction-frame`, schema-next fixture, and
   schema-rust-next `next/reaction-frame-emission` all agree on the same
   `Work<Event,Write,Read,Effect>` / `Action` shape; the emitter output matches
   the hand-written prototype. Zero operator integration, zero divergence — clean
   **NEEDS_INTEGRATION**.
3. **`TypeReference` is the one real conflict** — two rival designer designs that
   disagree on the wire surface and base. **This is the blocking designer
   decision** (below); operator cannot and must not arbitrate it.

No chaotic divergence anywhere. Most designer work is clean
unmerged-awaiting-integration, and operator has been actively integrating
designer branches (schema-next family declarations, content-identity blake3,
typed-macro-library; sema-engine versioning; nota-next structural-shape).

## The eight review targets

| # | Target | Verdict | Owner / action |
|---|---|---|---|
| 1 | Reaction frame (3 lanes) | NEEDS_INTEGRATION | **Operator** integrates in dep order: triad-runtime → schema-next → schema-rust-next |
| 2 | `TypeReference` structural-macro (2 rival designs) | **CONFLICT** | **Designer** reconciles first (below), then operator integrates one |
| 3 | schema-next polish ⊂ typeref vs schema-generics | NEEDS_INTEGRATION | Folds into #2 — pick ONE lineage; never merge polish + typeref both |
| 4 | `primary-bojw` macro-table self-host | NEEDS_INTEGRATION | **Operator** starts stage-1 (unblocked; prereq `typed-macro-library` on main) |
| 5 | spirit `store-decomposition` (+ mirror-shipper) | NEEDS_INTEGRATION | **Operator** integrates `store-decomposition` only (`vc-followups` ⊂ it; drop standalone `mirror-shipper`) |
| 6 | sema-engine stack | NEEDS_INTEGRATION | **Operator** lands whole linear stack (`engine-decomposition` is the superset), then points spirit at the head |
| 7 | meta-signal-spirit rebuild | **CONSISTENT** | Done — only 628 doc fix (designer) |
| 8 | nota-next `typeref-shape` + `pascal-head-body-shape` | NEEDS_INTEGRATION | **Operator** lands BOTH (complementary leaf shapes; serialize the textual conflict) |

## The blocking designer decision — `TypeReference` reconciliation

Two designer branches both convert `TypeReference` to a structural macro, but they
**cannot both land** — they overlap the enum, its decode/encode, `source.rs`,
`declarative.rs`, and rewrite every downstream `.schema` *differently*:

- **`next/schema-generics`** — broader, intent-bearing (closes D5-1: the
  generic-application form `Application{head: ApplicationHead, arguments:
  Vec<TypeReference>}`, parameterized declaration heads, root-position
  application, the full-frame pilot). Canonical heads **`Vector`/`Optional`/
  `ScopeOf`/`Map`**, Map **nested** `(Map (K V))`. Bases on nota-next
  `pascal-head-body-shape`. *Weakness:* keeps a hand-written `NotaDecode`/
  `NotaEncode` machine codec *alongside* the structural impl.
- **`typeref-structural-macro`** — narrower, cleaner-factored: the
  `#[shape(...)]` derive is the **single source of truth** (deletes the
  hand-rolled head-dispatch entirely), plus the `ReferenceHead` centralization.
  Canonical heads **`Vec`/`Optional`/`Scope`/`Map`**, Map **flat** `(Map K V)`.
  Bases on nota-next `typeref-shape` (HeadedAtom leaf for `(Bytes N)`). *Weakness:*
  no generics at all.

Both cite the same no-aliases intent — but `qz6j` only settles *newtype-vs-alias*
([qz6j: a bare name + type declares a distinct newtype, not an alias]); it does
**not** pin a head spelling or the Map shape. So the wire conflict is genuinely
open. My reconciliation:

- **Lineage: keep `schema-generics`' direction** — it delivers the generics /
  `Application` form, which is the actual D5-1 intent; `typeref-structural-macro`
  has none. **But fold in `typeref`'s two real improvements:** (a) make the
  **derive the single source of truth** and drop the hand-written machine codec
  `schema-generics` still carries beside the structural impl; (b) keep the
  `ReferenceHead` centralization; (c) use `typeref`'s **HeadedAtom** for the
  `(Bytes N)` numeric leaf. So both nota-next derives (`pascal-head-body-shape`
  *and* `typeref-shape`, per target #8) land, and the reconciled `TypeReference`
  uses both.
- **Spelling: `Vector` / `Optional` / `ScopeOf` (schema-generics' direction) —
  and this is *grounded*, not a coin-flip.** The workspace hard override "spell
  every identifier as a full English word" (`Request` not `Req`, `Identifier`
  not `Id`) makes `Vec`/`Scope` forbidden abbreviations; `Vector`/`Optional`/
  `ScopeOf` are the full words. The full-English-word rule decides it.
- **Map shape: flat `(Map K V)` (typeref's shape) — the one genuinely open call I
  surface to the psyche.** Rationale: once `Application` is the uniform
  `(Head arg1 arg2 …)` form, flat `(Map K V)` *is* that form applied; nested
  `(Map (K V))` is a special-case the generics model otherwise removes. So flat is
  more consistent with schema-generics' own headline. (Mild — a wire-shape
  judgment; defaulting to flat unless the psyche prefers the explicit key/value
  pairing.)

So: designer reconciles `schema-generics` + `typeref` improvements into one branch
with `Vector`/`Optional`/`ScopeOf` heads and (proposed) flat `(Map K V)`; operator
then lands both nota-next leaf derives, then the single reconciled schema-next
branch, dropping the prototype `[patch]`/branch-pins.

## Action split

**Designer (me):** reconcile `TypeReference` (#2/#3) into one branch per above;
fix report 628's superseded meta-signal framing (#7, done below). **Open for
psyche:** confirm flat vs nested Map shape.

**Operator:** integrate the reaction frame (#1, dep order), the sema-engine stack
(#6, whole-stack then point spirit), nota-next both leaf shapes (#8), spirit
`store-decomposition` (#5); start `primary-bojw` (#4). Already did the meta-signal
fix (#7). Blocked on the designer `TypeReference` reconciliation before #2 lands.

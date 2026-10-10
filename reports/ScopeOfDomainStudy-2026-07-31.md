# ScopeOf Domain Study — Design Pickup Surface

Assembled material for the ScopeOf authoring-stack design session. Psyche work
order: trait-based Rust target and minimal Ethos syntax first, Nomos
transformer design after.

Near-top note: the All ruling of 2026-07-31 — "All should, as the name
implies, match all." Root `All` is a whole-tree wildcard. Psyche-ruled;
recorded in `design/Nomos/allMatchesAllScopeOf-2026-07-31.md`.

## 1. Domain Semantics

Spirit entries carry `Domain` values in a 24-category life-domain taxonomy,
mandatory-to-leaf, e.g.
`Domain::Technology(TechnologyDomain::Software(SoftwareDomain::Programming(ProgrammingLeaf::TypeSystems)))`.

A scope is a prefix of that tree, stopping at any node to mean "everything
under here"; scopes filter subscriptions. Matching is recursive prefix
containment, walking scope and domain trees in lockstep. `All` at any level
means "match everything at this level and below"; per the 2026-07-31 ruling,
root `All` is a whole-tree wildcard (legacy semantics restored; identity-exact
was rejected).

The ~38 helpers:

- 38 scope enums mirroring the 38 domain enums (mirror variants + injected
  `All` at non-root levels; 24 flat leaf-domain scopes, 3 branching —
  `DomainScope`, `TechnologyDomainScope`, `SoftwareDomainScope` — 11
  leaf-level under Software).
- 38 `From<SourceDomain>` impls (recursive `.into()`).
- 38 `contains_scope` inherent methods (leaf: `matches!` expression;
  branching: delegate to children).
- 1 `contains_domain` on root `DomainScope`.
- 2 collection newtypes: `DomainScopes(Vec<DomainScope>)` and
  `ScopeSet(Vec<DomainScope>)`.

Consumers:

- `spirit/src/store/mod.rs` — `PublicIntentQuery` uses
  `matches_domain`/`matches_scope`; `EntryStoreExt` gates visibility.
- `signal-spirit/src/lib.rs` — `SpiritDomainScopes` trait.
- `signal-domain/src/lib.rs` — hand-written convenience methods.

Mind/Orchestrator/Messenger are blocked downstream.

~2,300 generated lines in
`/git/github.com/LiGoldragon/signal-domain/src/schema/domain.rs`
(3,354 total; scope enums from line 1048).

## 2. The Rust Reality

Legacy is **not** trait-based: inherent methods + `From` impls; only the
consumer-side `SpiritDomainScopes` trait exists.

Excerpts (all from `signal-domain/src/schema/domain.rs` unless noted):

**line 1048** — root enum:

```rust
pub enum DomainScope { All, Health(HealthDomainScope), Food(FoodDomainScope), /* 22 more */ Technology(TechnologyDomainScope) }
```

with `rkyv` `Archive`/`Serialize`/`Deserialize`, `Clone`, `Debug`,
`PartialEq`, `Eq` derives.

**line 1081**:

```rust
pub enum TechnologyDomainScope { All, Hardware(HardwareLeafScope), Software(SoftwareDomainScope) }
```

**line 1236**:

```rust
pub enum ProgrammingLeafScope { All, TypeSystems, Compilation, Parsing, Grammars, CodeGeneration, Metaprogramming, Macros, DomainSpecificLanguages }
```

**line 2860** — root `contains_scope`: `(Self::All, Self::All) => true` then
per-variant delegation, then `_ => false`; plus `contains_domain` converting
via `.into()`.

**line 2817** — branching `contains_scope`: `(Self::All, _) => true` then
per-variant delegation.

**line 1769** — leaf `contains_scope`: `matches!` with a `(Self::All, _)`
arm.

**line 2827** — `From<Domain> for DomainScope`: variant-by-variant, recursive
`.into()`.

**`signal-domain/src/lib.rs` line 79** — hand-written layer:

```rust
matches_domain = self.is_all() || domain.is_all() || self.contains_domain(domain);
// matches_scope analogous
is_all = matches!(self, Self::All);
```

**THE ASYMMETRY FINDING**: the root `All` wildcard lives only in the
hand-written `matches_*` short-circuits (the generated root `contains_scope`
matches `All` only against `All`), while sub-level `All` wildcard IS
generated (`(Self::All, _) => true`). The 2026-07-31 ruling implies the
generated root should adopt the uniform `(Self::All, _) => true` pattern,
removing the asymmetry.

**TRAIT TARGET** (to be designed): candidates — a `ContainsScope` /
`ScopeContainment` trait (`contains_scope`), `From<D>` for conversion,
possibly `ScopeMatching` (`matches_domain`/`matches_scope`/`is_all`). Psyche
prior: "we love traits; they make agents smarter by giving them an
ontology" (DesignReviewRulings section 2).

## 3. The Ethos Information Inventory

Legacy schema-era declaration
(`signal-domain/schema/domain.schema`): `DomainScope.ScopeOf.Domain`.

Full fixture (`schema-rust/tests/fixtures/domain-terminal-scope.schema`):

```
Domain.[Technology.Software]
Software.[Programming.ProgrammingLeaf Theory]
ProgrammingLeaf.[All TypeSystems Parsing]
DomainScope.ScopeOf.Domain
ScopeSet.Vector.DomainScope
```

Irreducible authored minimum: three atoms — target name, `ScopeOf` keyword,
source type name.

Derived:

- helper names (append `Scope`; root keeps authored name)
- mirrored variants + `All` injection
- payload-bearing vs leaf determination
- three impl families per enum
- derive/attribute sets (rkyv trio + `Clone`/`Debug`/`PartialEq`/`Eq`,
  conditional nota derives under `nota-text`, `rustfmt::skip` on impls, no
  `Copy` on root)
- collections declared as separate `Vector` lines
- visited-set deduplication

Tree walk (`schema-rust/src/lib.rs` `ScopeEnumModel::push_model`, line 4027):
recursive descent from source root, child scope enum per
payload-referencing variant, leaf otherwise, visited tracking (lines
4034–4038); deepest path 4 levels
(Domain→Technology→Software→Programming→ProgrammingLeaf); termination when a
level has no payload-bearing variants.

## 4. Constraints

**Identity question** (`reports/ScopeOfIdentityBriefing-2026-07-29.md`):
Option A — durable per-helper translator IDs (conflicts
DesignReviewRulings Entry 3) — vs Option B — implementation structure under
one authored identity, scope values as paths of source-variant encodedIDs
(overnight lean, not-understood-by-psyche, reversible). UNRULED.

**All ruling**: as above (section header note) — whole-tree wildcard,
psyche-ruled 2026-07-31.

**Recursion**: required — tree walk; Splice only walks flat vectors; the
escape-growth path went through bead po2.19.

**po2.7**: BLOCKED on the two psyche rulings (helper identity, recursion
mechanism); depends po2.19 and po2.6 (both now closed per beads); blocks
po1.10.11 (Spirit Ethos port) hence Orchestrator/Mind/Messenger.
Acceptance: ScopeOf expansion as authored encoded-form data, never
concatenated Rust source, refusing atomically on missing/stale/cyclic/
unsupported/unresolved source graphs; transformer/template terminology
binding.

**Legacy generation is quote!-token-based**
(`schema-rust/src/lib.rs` `ScopeFamilyTokens`, lines 4123–4341) — precisely
what the typed pipeline replaces.

Fixture evidence of current direction
(`core-nomos/tests/textual_nomos.rs`):

```
ScopeOfStep.Recursive.Enumeration {
  (variant.Name source.Variants children.Variants)
  [ Invoke.ScopeOfStep Splice.children InsertAt.children 0 rustfmt.skip [Clone] ]
}
```

— a `Recursive` transformer kind alongside `Structural`/`Named`, recursion
spelled through `Invoke`, `InsertAt` as an escape form.

## 5. Open Items for the Design Session

a. Trait set for the generated Rust target — design choice before Nomos
   design.

b. Uniform generated root `All` (`(Self::All, _) => true`) per the ruling —
   to confirm.

c. Whether the three-atom declaration is the desired minimal Ethos or
   changes are wanted.

d. ATTENTION: bead po2.19 reads closed while the authored-surface question
   (one authored `Invoke` vs distinct `Fold`,
   `NomosRecursionBriefing-2026-07-30.md`) is still unruled — reconcile with
   the train.

e. Helper-identity ruling still outstanding.

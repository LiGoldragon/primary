*Kind: Audit · Topic: second-operator-180-schema-v13 · Date: 2026-05-24 · Lane: second-designer (counter-ego)*

# 171 — Audit: second-operator /180 schema v13 model + upgrade

## §1 Scope

This audit reviews `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` and the implementation it lands in `/git/github.com/LiGoldragon/schema`. Counter-ego pass per intent 403 — second-designer doubts, checks invariants, surfaces gaps.

Cross-references audited against:
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — current design (uniform header form)
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — header/body/feature separation + route-root-reservation critique
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — migration MVP spec
- `reports/designer/325-nota-box-library-design-and-implementation.md` — box layout intent 404
- Intent records 388-495 (per /324 §2 + /174-v5 intent table)

## §2 What /180 implements vs the design

| Design element | Source | /180 implementation | Match |
|---|---|---|---|
| Six-position Schema struct | /326-v13 §2, /174-v5 "One-Screen Shape" | `Schema { imports, ordinary_header, owner_header, sema_header, namespace, features }` | ✓ exact |
| Uniform header form `(VerbName [sub-variants])` | /326-v13 §1 + intent 494 | `HeaderRoot::new` rejects empty endpoints `Vec<Name>` | ✓ enforced structurally |
| Two import directives — `Import` + `ImportAll` | /326-v13 §2 + /174-v5 "Improved Import Model" + intents 481-483 | `ImportDirective::{Import{path,names}, ImportAll{path}}` | ✓ exact |
| Import collision (import↔import, import↔local) | /174-v5 "Collision Rule" + intent 485 | `DuplicateImportedName` + `ImportCollisionWithLocal` errors | ✓ both directions tested |
| Route-root namespace reservation | /174-v5 §"Header Critique After /326-v13" | `Namespace` is `BTreeMap<Name, DeclarationBody>` — duplicate insertion structurally impossible | ✓ stronger than required |
| `AssembledSchema` lowered form | /174-v5 "Assembled Schema Representation" + intent 490 | `AssembledSchema { imports, routes, types, features }` | ✓ exact (minus component name — see §7) |
| Route entry shape | /326-v13 §3 | `Route { leg, root_slot, root, endpoint, body }` | ✓ exact |
| Unit endpoint = explicit `RouteBody::Unit` | /174-v5 §"Implementation critique" + Example C | `RouteBody::{Type(Name), Unit}` | ✓ exact |
| Upgrade knowledge belongs to next version | intent 491 | `plan_upgrade_from(&self, previous)` on `AssembledSchema` | ✓ correct signature direction |
| Five upgrade annotations | /174-v5 "Upgrade Model" | `UpgradeAnnotation::{Migrate, RenamedFrom, Drop, Custom, Untranslatable}` | ✓ five-way enum |
| Standard (inferable) projections — additive enum | /174-v5 + intent 488 | `StandardProjection::AdditiveEnumVariant` + zip-prefix check | ✓ correct logic |
| Annotation required for changed records | intent 488 | `Error::MissingUpgradeAnnotation` raised | ✓ tested |
| Drop/Untranslatable required for removed types | intent 488 | `Error::RemovedTypeRequiresAnnotation` raised | ✓ logic present (test gap — §8) |
| Root + boxes layout (intent 404) | /325 + intent 404 | `Layout { fields: Vec<FieldLayout> }` + cycle-aware `is_fixed_width` | ✓ implemented; subtle issue — §5 |
| Engine annotations | /174-v5 + Spirit `(engine assert)` pattern | `Engine::{Assert, Mutate, Retract, Match, Subscribe, Validate}`; `Variant.engine: Option<Engine>` | ✓ stored; gap — §6 |
| Features — Reply / Event / Observable / Upgrade | /326-v13 §2 position 6 | `Feature::{Reply(Vec<Name>), Event(EventFeature), Observable(ObservableFeature), Upgrade(Upgrade)}` | ✓ four-variant enum |
| NOTA curly-map for namespace | intent 425 | Test `nota_curly_map_is_usable_for_schema_namespace_names` confirms `BTreeMap<Name, u64>::decode("{Entry 1 Record 2}")` works | ✓ verified through nota-codec |

## §3 Strengths

1. **Structural invariants over validation invariants.** `Namespace = BTreeMap<Name, DeclarationBody>` — duplicate names are impossible by construction, not by post-hoc check. Same with `Imports = BTreeMap<Name, ImportDirective>`. This is the right way: invariants in the type, not in a `validate()` method that callers can forget.

2. **Header uniform form enforced at construction.** `HeaderRoot::new(name, endpoints)` rejects `endpoints.is_empty()` → `EmptyHeaderRoot { name }`. There is NO API path to construct a scalar `(State Statement)` route — the type forces `Vec<Name>` with at least one element. Matches intent 494 + /326-v13 §1 + /174-v5 §"Header Cardinality" rule perfectly.

3. **Route-root reservation is structurally automatic** because Namespace is a BTreeMap keyed by Name. The test `route_root_body_declaration_reserves_namespace_key` confirms this — a `State` record declaration plus a `State` enum declaration collide as `DuplicateDeclaration` at namespace construction. No validation logic needed.

4. **ImportAll explicit resolution gate is clean.** `validate_authored` runs with `resolve_selected_imports` only (no ImportAll names known yet). Assembly takes `&[ImportResolution]` that callers supply at assemble time. Tests confirm `assemble(&[])` on a schema with `ImportAll` fails fast with `MissingImportResolution`. This avoids the "must read every imported schema transitively to validate this one" pitfall.

5. **`plan_upgrade_from` direction matches intent 491.** Called on `next: AssembledSchema` with `&previous: &AssembledSchema` — upgrade knowledge lives on next. Inference logic distinguishes 7 projection kinds: Identity / Standard / Annotated / Added / Renamed / Dropped / Untranslatable.

6. **Layout module implements intent 404 with cycle detection.** `is_fixed_width` uses `HashSet<Name> visited` to handle recursive declarations (e.g., a tree-shaped type that references itself). Without cycle detection this would stack-overflow on `Tree { children: Vec<Tree> }`.

7. **Variant payload model has three shapes — `Unit / Type(TypeExpression) / Fields(Vec<TypeExpression>)`** — covering bare-name `Decision`, single-payload `(Statement Statement)`, and multi-field `(Entry Topic Kind Summary ...)` cases. Endpoint resolution restricts to `Unit | Type(Named)` per /174-v5 rule that endpoint bodies resolve to named or unit.

8. **Container expression model is correct** — `Container::{Vector, Optional, Map { key, value }}` for `(Vec T)`, `(Option T)`, `(Map K V)` shapes per intent 485 (container types use parens, not brackets).

9. **Error surface is precise.** 22 named error variants with structured fields (not stringly typed). `MissingUpgradeAnnotation { name }` carries the offending type name. `UnmatchedRouteBodyVariant { root, variant }` carries both halves. Display impls are reader-facing.

10. **Lane discipline is exemplary.** /180 §"Best Next Slice" explicitly defers the repo-wide schema marking sweep to designer's /327, avoiding conflict. Operator self-restraint about cross-lane concurrent edits matches AGENTS.md cross-lane coordination protocol.

## §4 Weaknesses + gaps

The list is long but most items are forward-notes for the next operator pass, not blockers for /180 itself.

### §4.1 Schema lacks component name (intent 471 gap)

`Schema` and `AssembledSchema` have no `component_name` field. Per intent 471 + /170 §7, the schema's root name comes from the filename (`spirit.schema` → root namespace `spirit`). The Rust API has no surface for this — the eventual `.schema` parser will need to thread the component name from the file path through to both `Schema` and `AssembledSchema`. Recommended landing:

```rust
impl Schema {
    pub fn for_component(name: Name, imports: Imports, /* ... */) -> Result<Self>;
}
```

Without this, UID generation per intent 469 (`spirit::namespace::Topic` form) has no anchor.

### §4.2 Engine annotations stored but unused

`Variant { name, payload, engine: Option<Engine> }` carries Engine but it never surfaces in `AssembledSchema` or in any `Route`. The next operator pass needs to either:
- emit Engine into `AssembledType::Local { body, engine }`, or
- surface a per-route engine in the `Route` table, or
- expose engine grouping (`assert_routes()`, `mutate_routes()`) on AssembledSchema.

Without this, the Layer 2/3 emission planned via engine annotations (per /174 + intent corpus around macro-emitted dispatch) has nothing to consume.

### §4.3 Layout planning runs pre-assembly; imported types treated as variable-width

`Layout::for_declaration(document, name)` takes the pre-assembly `Document` — it does NOT know imported type bodies. So when `is_fixed_width` encounters `TypeExpression::Named("Magnitude")` (imported via ImportAll), `document.declaration_body("Magnitude")` returns `None` → conservatively classified as variable-width → boxes.

Verified via the test: Spirit Entry's layout puts position 4 (Magnitude) in `box_positions` even though Magnitude is a 1-byte enum. After resolution, Magnitude should reclassify as fixed-width root.

Two paths to fix:
- **(a)** Move Layout off Document onto AssembledSchema, so import bodies are known.
- **(b)** Import declarations carry width hints (e.g., `ImportedNames` records per-name fixed-width metadata).

**Lean: (a)** — AssembledSchema is the canonical fully-resolved form per /174-v5; layout should consume it, not the pre-assembly Document.

### §4.4 Test coverage thin for the multi-sub-variant case

`validates_spirit_mvp_uniform_header_and_lowers_routes` covers only single-sub-variant routes: `[(State [Statement]) (Record [Entry])]`. The architectural seam between header sub-variants and namespace body declarations — the design's most interesting move per /174-v5 §"Better Separation" — is untested in the multi-sub-variant case. A test that asserts:

```
header: [(Watch [State Records Questions])]
namespace: { Watch [(State StateSubscription) (Records RecordSubscription) (Questions QuestionSubscription)] }
↓
3 routes: leg=Ordinary, root_slot=0, root=Watch, endpoints={Self/Records/Questions}, bodies={StateSubscription/RecordSubscription/QuestionSubscription}
```

would prove the seam works.

### §4.5 Owner header + sema header tested only as empty

All header tests use `Header::empty()` for owner + sema legs. `lower_header(Leg::Owner, ...)` + `lower_header(Leg::Sema, ...)` go through the same code path as Ordinary, so this is low-risk — but the test gap leaves a small "we never verified non-Ordinary legs lower at all" possibility. One smoke test covering a non-empty sema header would close the gap.

### §4.6 Upgrade projection paths thinly tested

Of 7 projection kinds in `Projection`, tests cover:
- ✓ Identity (implicit — unchanged Kind enum produces identity)
- ✓ Standard (additive enum variant test)
- ✓ Annotated (Migrate annotation test)

Untested:
- Added (new type appearing in current only)
- Renamed (RenamedFrom annotation chasing previous)
- Dropped (Drop annotation on removed type)
- Untranslatable (Untranslatable annotation on removed type)
- RemovedTypeRequiresAnnotation error path

### §4.7 No round-trip parse/serialize test

The crate is constructor-only (Rust builder API). When the NOTA `.schema` parser lands, round-trip tests should land with it: parse → Schema → serialize → equality. Out of scope for /180 per "What This Does Not Do Yet" — but the test discipline should be set up so the next operator pass adds them.

### §4.8 `UpgradeAnnotation::Custom { name, implementation: Name }` — implementation is just a Name

`Custom` annotation has `implementation: Name`. But "the migration function to call" is more naturally a path or a trait impl reference. /174-v5 §"Upgrade Model" example has `(Transform Entry Source SourceFromContext)` — `SourceFromContext` would presumably be a Rust function. Storing as bare Name will work syntactically but semantically the codegen layer will need to know "this Name refers to a function, not a type." Worth ratifying with psyche.

### §4.9 `validate_features` doesn't restrict Reply names by category

`Feature::Reply(Vec<Name>)` only validates that each name resolves to a declared body. There's no check that "a name appears in Reply XOR in Event payloads" — a single type can be referenced from both Reply and Event. Maybe fine; maybe a future "Reply types form a closed set" rule. Not a blocker; flagging.

### §4.10 `section.rs` is vestigial naming

The file is `section.rs` but only contains `Namespace`. This is leftover from before /178's collapse from `Section` enum into the explicit six-position Schema. Renaming to `namespace.rs` (or moving Namespace into `lib.rs` since it's just one struct) would clean up. Minor.

### §4.11 `AssembledSchema::body(name)` returns None for imported types

`body()` matches `AssembledType::Local` only. Downstream codegen must check `types()` for `Imported { binding }` and chase. A helper like `body_or_imported(name) -> Option<BodyOrImported>` would simplify codegen callers. Not a bug; design polish.

### §4.12 `Reference` type from /177 doesn't appear in /180's surface

/177's bootstrap mentions a `Reference` type (cross-schema reference declarations validated but layout treats as variable). I don't see it in lib.rs exports or any current source file. Possibly absorbed into the `Imported` AssembledType + ImportedNames flow; possibly removed when the six-position structure landed. Worth confirming the Reference concept didn't get accidentally dropped in transition.

## §5 The Magnitude-in-box subtlety (§4.3 expanded)

The layout test asserts:

```rust
assert_eq!(layout.root_positions(), vec![1]);              // Kind
assert_eq!(layout.box_positions(), vec![0, 2, 3, 4, 5]);   // Topic, Summary, Context, Magnitude, Quote
```

Magnitude at position 4 lands in BOX, even though Magnitude is a 1-byte fixed-width enum in `signal-sema/magnitude.schema`. This is because Layout takes the pre-assembly Document, which doesn't know imported types' shapes. `is_fixed_width("Magnitude")` walks `document.declaration_body("Magnitude")` → returns `None` (no local body) → conservatively classifies as variable.

After ImportResolution, Magnitude is known to be a sized enum. The /325 box layout intent + the brilliant macro library's wire emission needs Magnitude in ROOT (sized, fast-dispatch). The current layout result would emit Magnitude as a length-prefixed box → wire bytes 4-7 wasted on length prefix + 1 byte content instead of 1 byte inline.

This is a **real semantic gap** that should land before macro-library codegen consumes Layout. Recommended fix: move `Layout::for_declaration(document, name)` to `Layout::for_declaration(assembled, name)` and have it consult `assembled.body(name)` (with fallback to a stored width hint for imported types).

## §6 Engine annotations: stored but invisible (§4.2 expanded)

`Variant.engine: Option<Engine>` lives on the namespace-side variant. The /180 test builder uses `.with_engine(Engine::Assert)` on `State::Statement` + `Record::Entry`.

But:
- `Route` has no `engine` field
- `AssembledType::Local { name, body }` has no engine field
- `AssembledSchema` has no `routes_by_engine()` or `assert_routes()` accessor

So the macro library, when it goes to emit `OperationDispatch` per /324 §3.1 (engine-driven dispatch table), has no way to ask "which routes are assert-engine?" The information is in the namespace-side enum's Variant payload, but `Route` doesn't carry it through.

Recommended landing in the next operator pass: when `endpoint_body` resolves the variant, copy the variant's engine into the Route:

```rust
pub struct Route {
    leg: Leg,
    root_slot: usize,
    root: Name,
    endpoint: Endpoint,
    body: RouteBody,
    engine: Option<Engine>,  // ← new
}
```

Or, alternatively, expose `assembled.engine_for(route) -> Option<Engine>` that looks up the variant on demand.

## §7 Component name + UID generation (§4.1 expanded)

The eventual UID form is `spirit::namespace::Topic` (per intent 469 + /170 §5). For this to compile:
- The Schema knows it's for component `spirit` (currently doesn't).
- The AssembledSchema preserves component name (currently doesn't).
- Each `AssembledType` can render its UID as `component::namespace::Name` (currently can't, since there's no component).

The current crate-level API is `Schema::new(imports, headers..., namespace, features) -> Result<Schema>` — no component name parameter.

Recommendation for next operator pass:
```rust
impl Schema {
    pub fn for_component(
        component: Name,
        imports: Imports,
        ordinary_header: Header,
        // ...
    ) -> Result<Self>;
}

impl AssembledSchema {
    pub fn component(&self) -> &Name;
    pub fn uid_for(&self, type_name: &Name) -> Uid;  // returns component::namespace::Name
}
```

The eventual `.schema` parser would derive `component` from the file basename per intent 471.

## §8 Test coverage gaps as a numbered list

For the next operator pass to add:

1. Multi-sub-variant route lowering test (§4.4)
2. Owner header + sema header non-empty smoke test (§4.5)
3. Renamed projection test (§4.6)
4. Dropped projection test (§4.6)
5. Untranslatable projection test (§4.6)
6. `RemovedTypeRequiresAnnotation` error path test (§4.6)
7. Engine annotation surfaced through to Route or AssembledType (§6) — depends on §6 fix landing
8. Layout-after-import-resolution test once §5 fix lands (§5)
9. Round-trip test once NOTA parser lands (§4.7)

## §9 Lane coordination

/180's "Best Next Slice" explicitly defers the repo-wide schema marking sweep to designer's /327, naming the conflict risk. This is exemplary cross-lane discipline — operator running concurrent `git`-mutating work in the same files as designer's dispatched subagents is exactly the failure mode AGENTS.md `orchestrate/AGENTS.md` aims to prevent.

The pattern to repeat: when one lane plans broad workspace edits, the parallel lane should pause that scope until the marking-sweep meta-session settles. /180 does this without being told.

## §10 Recommended forward slices

In priority order for the next operator pass on the `schema` crate:

| Slice | What | Why |
|---|---|---|
| A | Add `component: Name` to Schema + AssembledSchema, with `for_component` constructor | Unblocks UID generation (§7) — load-bearing for macro library |
| B | Move Layout to consume AssembledSchema (not Document) | Fixes Magnitude-in-box bug (§5) — load-bearing for wire codegen |
| C | Thread Engine through to Route or AssembledType | Unblocks engine-driven dispatch codegen (§6) |
| D | Add the 9 test cases in §8 | Closes coverage gaps before macro library bolts on |
| E | Rename `section.rs` to `namespace.rs` (or inline into lib.rs) | Trivial cleanup (§4.10) |

Slices A + B + C are pre-requisites for `primary-ezqx.1` to start consuming the crate as codegen input. Slice D is operator-discipline; Slice E is housekeeping.

## §11 What this report does NOT do

- Does NOT capture new psyche intent (the audit is downstream of the existing intent corpus).
- Does NOT recommend changes to /326-v13 (the design is stable; this audits the implementation).
- Does NOT recommend operator pick up new beads (those go through the bead-and-beadlist system).
- Does NOT propose new design — only forward-notes for the next operator pass.

## §12 See also

- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` — the implementation report this audit reviews
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — current design
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — header/body/feature separation + route-root critique
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — migration MVP spec
- `reports/designer/325-nota-box-library-design-and-implementation.md` — intent 404 box layout
- `reports/second-designer/170-schema-lowering-executor-model-2026-05-24.md` — counter-ego lowering executor model (peer audit)
- `/git/github.com/LiGoldragon/schema/src/` — audited implementation
- Intent records 388-495

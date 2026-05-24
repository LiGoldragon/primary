*Kind: Mockup · Topic: engine-routing-and-upgrade-coverage · Date: 2026-05-24 · Lane: second-designer (sub-agent B)*

# 172 · 2 — Mockup: Engine routing to Route + multi-sub-variant + upgrade coverage

## §1 Worktree + branch + commit

- **Worktree absolute path**: `/tmp/mockup-b-engine-routing`
- **Branch**: `feature/engine-routing-and-upgrade-coverage`
- **Commit short-id**: `52f5364692fa` (jj change id `ywttppsq`)
- **Pushed to remote**: `origin` at `ssh://git@github.com/LiGoldragon/schema`
- **Bead**: `primary-gqj6` ([mockup] schema engine threading + multi-sub-variant + upgrade coverage (second-designer/172 slice B))

## §2 What was implemented

### §2.1 Engine threading to Route (closes /171 §4.2 + §6)

`Route` now carries `engine: Option<Engine>`. The engine annotation declared
on the namespace-side `Variant` (e.g. `Variant::with_type(name, payload)
.with_engine(Engine::Assert)`) is read during endpoint resolution and
copied into the lowered Route.

Files modified:

- `src/assembled.rs`
  - `Engine` added to import list
  - `Route { engine: Option<Engine> }` field added (positional, after `body`)
  - `Route::new(...)` constructor takes `engine: Option<Engine>` as its
    sixth parameter
  - `Route::engine(&self) -> Option<Engine>` accessor added
  - `AssembledSchema::routes_by_engine(engine: Engine) -> impl Iterator<Item = &Route>`
    helper added (lives alongside `routes()`)
- `src/document.rs`
  - `Engine` added to import list
  - `Schema::endpoint_body` now returns `Result<(RouteBody, Option<Engine>)>`
    instead of `Result<RouteBody>`, threading the variant's engine through
  - `Schema::lower_header` destructures the tuple and passes the engine
    into `Route::new`

`DESIGN-DECISION-REVIEW (second-designer/172 §3.2)` markers inline at every
code site so operator can find the rationale.

### §2.2 Eight new tests (closes /171 §4.4 + §4.5 + §4.6)

Added to `tests/document.rs`:

| # | Test | Closes /171 § |
|---|---|---|
| 1 | `multi_sub_variant_header_lowers_to_three_distinct_routes` | §4.4 — multi-sub-variant lowering gap |
| 2 | `owner_header_lowers_with_owner_leg` | §4.5 — non-empty owner header |
| 3 | `sema_header_lowers_with_sema_leg` | §4.5 — non-empty sema header |
| 4 | `engine_annotations_thread_through_to_routes` | §4.2 + §6 — engine surfacing |
| 5 | `renamed_annotation_produces_renamed_projection` | §4.6 — Renamed projection |
| 6 | `drop_annotation_produces_dropped_projection` | §4.6 — Dropped projection |
| 7 | `untranslatable_annotation_produces_untranslatable_projection` | §4.6 — Untranslatable projection |
| 8 | `removed_type_without_annotation_errors` | §4.6 — RemovedTypeRequiresAnnotation error path |

All eight tests target a single design seam each. Each carries a
`DESIGN-DECISION-REVIEW (second-designer/172 §3.2 + /171 §<N>)` comment
header pointing back to the audit paragraph that motivates it.

### §2.3 What was NOT done (carried-uncertainty)

- **Engine annotation on AssembledType**: /171 §4.2 listed two paths —
  "emit Engine into `AssembledType::Local { body, engine }`" OR "surface a
  per-route engine in the `Route` table" OR "expose engine grouping
  (`assert_routes()`) on AssembledSchema". This mockup picks the
  second + third (Route carries engine; AssembledSchema exposes
  routes_by_engine). It does NOT modify AssembledType. Rationale: engines
  are properties of routing operations, not type structure — putting
  `engine` on AssembledType would conflate the wire-encoding axis (what
  shape a type has) with the dispatch axis (what operation a route
  performs). Operator may have a stronger reason to put engine on
  AssembledType too (e.g., when a type appears as a route body it inherits
  the engine of the route); flag if so.
- **Layout fix per /171 §5**: out of scope (assigned to slice A — sub-agent A).
- **Component name per /171 §4.1 + §7**: out of scope (slice A).
- **Round-trip parse test per /171 §4.7**: out of scope (NOTA parser landing).

## §3 Test that demonstrates the change works

The pivotal test is `engine_annotations_thread_through_to_routes`. It
builds the Spirit MVP schema (which has `Engine::Assert` on `State::Statement`
and `Record::Entry` variants), assembles, then asserts both per-route
access AND the new grouping helper:

```rust
let routes = assembled.routes();
assert_eq!(routes.len(), 2);
assert_eq!(routes[0].engine(), Some(Engine::Assert));
assert_eq!(routes[1].engine(), Some(Engine::Assert));

let assert_routes: Vec<_> = assembled.routes_by_engine(Engine::Assert).collect();
assert_eq!(assert_routes.len(), 2);

let mutate_routes: Vec<_> = assembled.routes_by_engine(Engine::Mutate).collect();
assert!(mutate_routes.is_empty());
```

The architectural-seam test is `multi_sub_variant_header_lowers_to_three_distinct_routes`
(closing /171 §4.4 — the design's most-important move per /174-v5
"Better Separation"). Header `(Watch [State Records Questions])` plus
namespace `Watch [(State StateSubscription) (Records RecordSubscription)
(Questions QuestionSubscription)]` lowers to three Routes with monotonic
endpoint slots {0, 1, 2}, identical root_slot=0, leg=Ordinary, and three
distinct route bodies. All three carry `Engine::Subscribe`.

## §4 Test results

- `cargo build`: clean
- `cargo test`: 24 / 24 pass (16 pre-existing + 8 new)
- `cargo fmt -- --check`: clean
- `cargo clippy --all-targets -- -D warnings`: clean
- `nix flake check --option max-jobs 0` (invoked as `path:./` from the
  worktree per a quirk of the jj workspace not registering as a flake
  source root): `all checks passed!` — runs cargoBuild, cargoTest,
  cargoFmt, cargoClippy, cargoDoc

## §5 Reference to operator's existing implementation

| Surface | Path on main | What this mockup changes |
|---|---|---|
| `Route` struct | `/git/github.com/LiGoldragon/schema/src/assembled.rs:167-212` | Adds `engine: Option<Engine>` field + accessor; `Route::new` takes 6 params not 5 |
| `endpoint_body` resolution | `/git/github.com/LiGoldragon/schema/src/document.rs:286-324` | Returns `(RouteBody, Option<Engine>)` tuple instead of `RouteBody` |
| `lower_header` route construction | `/git/github.com/LiGoldragon/schema/src/document.rs:248-268` | Destructures tuple, passes engine into Route::new |
| `Variant.engine` (already exists) | `/git/github.com/LiGoldragon/schema/src/declaration.rs:60-107` | Unchanged — the existing `Variant::engine()` accessor is now read by lower_header |
| `tests/document.rs` (test corpus) | `/git/github.com/LiGoldragon/schema/tests/document.rs` | 8 new tests appended before the `Builder` struct |

Operator can `jj git fetch` and `jj new feature/engine-routing-and-upgrade-coverage`
to land the worktree's commit on top of their local main.

## §6 Psyche-questions surfaced

1. **Engine grouping at type vs route level.** Two natural axes for the
   engine annotation: (a) on the route (this mockup) — "this dispatch
   operation is an assertion"; (b) on the type — "this body type is
   only ever produced by assertions". Currently both work because each
   route is built from a single variant. If a type later becomes the
   body of multiple routes (e.g., reused payload across Watch + Record
   operations), the route-level annotation is more honest. The type-level
   annotation would have to choose one engine or accept conflict. Lean:
   keep engine on Route only (this mockup's choice). Worth confirming
   with psyche if the type-level annotation is needed for any codegen path.

2. **`Engine` as exhaustive enum vs extensible registry.** Current
   `Engine` is a closed enum of 6 kinds: Assert, Mutate, Retract, Match,
   Subscribe, Validate. The macro-variant engine in slice C may want
   engine kinds to be extensible (each component declares its own
   engines). If so, `Engine` should become a `Name` or a registered
   marker, not a hard-coded enum. Flag for slice C overview to decide.

3. **`RenamedFrom` vs add-then-drop equivalence.** The test
   `renamed_annotation_produces_renamed_projection` asserts the previous
   name does NOT appear as Dropped. Is that the correct semantic? The
   current impl filters via `renamed_previous` set — verified working
   — but the question of "should rename + drop both fire?" is a design
   question. The current behavior (rename consumes the previous; drop
   does not separately fire) matches the intent of the annotation.

## §7 Recommendation

**Operator integrate as-is, with one optional split.** The eight tests
are pure additions and carry zero conflict risk with operator's main
work. The Route change is a single-field addition + constructor signature
update + one accessor; the call site is unique (`Schema::lower_header`).

Two integration options:

- **(a) Land the whole commit** — single jj commit cleanly applies.
  Recommended path.
- **(b) Pick the test commits and re-implement the Route change**
  yourself if you want to control the constructor signature. The eight
  test functions are stand-alone and depend only on `Engine`,
  `routes()[i].engine()` accessor existing, and `routes_by_engine`
  helper existing. If you take a different API shape (e.g., `engine`
  on AssembledType OR a `Route::engine()` lookup that doesn't require
  storage on Route itself), the tests stay correct after trivial
  rephrasing.

The chosen split between Route-as-storage and AssembledType-as-storage is
the only real design choice in this mockup. Default to Route storage
unless there's a stronger reason for AssembledType (see psyche-question 1).

## §8 References

- `reports/second-designer/171-audit-second-operator-180-schema-v13-2026-05-24.md` §4.2, §4.4, §4.5, §4.6, §6, §10 — the audit slices this mockup closes
- `reports/second-designer/172-design-mockup-dispatch/0-frame-and-method.md` §3.2, §4 — the orchestrator's frame
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` §"Better Separation" — the architectural seam multi-sub-variant test proves
- `reports/designer/326-v13-spirit-complete-schema-vision.md` §3 — Route entry shape the engine field extends
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` §3.1 — engine-driven dispatch table that consumes Route.engine
- `/git/github.com/LiGoldragon/schema/src/assembled.rs` + `/src/document.rs` + `/tests/document.rs` on `feature/engine-routing-and-upgrade-coverage` — the mockup
- Bead `primary-gqj6` — operator-facing locator

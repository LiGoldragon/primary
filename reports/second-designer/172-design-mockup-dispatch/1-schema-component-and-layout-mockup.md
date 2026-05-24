*Kind: Mockup · Topic: schema component-name + Layout-on-AssembledSchema · Date: 2026-05-24 · Lane: second-designer (sub-agent A)*

# 1 — Mockup: schema component-name UID anchor + Layout consumes AssembledSchema

## §1 Locator

- **Worktree**: `/tmp/mockup-a-component-uid`
- **Repo origin**: `/git/github.com/LiGoldragon/schema`
- **Branch**: `feature/component-uid-and-layout`
- **Commit short-id**: `b5c4f373`
- **Commit full-id**: `b5c4f3732f556c6519fc77b9d74ab12a3d665216`
- **Push status**: pushed to `origin` (PR URL surfaced by remote: `https://github.com/LiGoldragon/schema/pull/new/feature/component-uid-and-layout`)
- **Bead**: see §7

This mockup implements slices A + B from second-designer/171 §10 against /180's main-branch implementation. The commit lands a single self-contained change; operator can cherry-pick or rebase as preferred.

## §2 What was implemented

### §2.1 Slice A — component name + UID

| Surface | Location | Note |
|---|---|---|
| `Schema { component_name: Name, ... }` | `src/document.rs:11-19` | New field, first position |
| `Schema::for_component(component_name, imports, ordinary_header, owner_header, sema_header, namespace, features) -> Result<Schema>` | `src/document.rs:42-64` | New explicit constructor |
| `Schema::new(...)` preserved | `src/document.rs:28-41` | Now defaults the component to `Anonymous` and delegates to `for_component`; all existing callers (parser, reader, tests) unchanged |
| `Schema::component_name(&self) -> &Name` | `src/document.rs:66-68` | Accessor |
| `anonymous_component_name() -> Name` | `src/document.rs:21-24` | Module-private helper returning `Name::new("Anonymous")` |
| Threaded into `AssembledSchema::new` call | `src/document.rs:107-115` | First positional arg |
| `AssembledSchema { component: Name, ... import_widths: BTreeMap<Name, bool> }` | `src/assembled.rs:13-22` | Two new fields |
| `AssembledSchema::new(component, imports, routes, types, features)` | `src/assembled.rs:24-43` | New positional arg first |
| `AssembledSchema::component(&self) -> &Name` | `src/assembled.rs:60-62` | Accessor |
| `AssembledSchema::uid_for(&self, type_name) -> Uid` | `src/assembled.rs:68-70` | Returns Uid built from the schema's own component + the requested type name |
| `Uid { component: Name, type_name: Name }` | `src/assembled.rs:300-330` | Displays as `component::namespace::TypeName` (constant `NAMESPACE_LABEL = "namespace"` at `src/assembled.rs:11`) |
| `pub use ... Uid` | `src/lib.rs:18` | Export |

### §2.2 Slice B — Layout consumes AssembledSchema

| Surface | Location | Note |
|---|---|---|
| `Layout::for_assembled(assembled, declaration) -> Result<Self>` | `src/layout.rs:41-50` | New post-assembly path |
| `Layout::for_assembled_variant(assembled, declaration, variant) -> Result<Self>` | `src/layout.rs:52-78` | Variant payload variant of for_assembled |
| `Layout::for_declaration(document, declaration)` preserved | `src/layout.rs:18-27` | Doc-comment now points readers at `for_assembled` for the post-import behaviour |
| `Layout::for_variant(document, declaration, variant)` preserved | `src/layout.rs:29-33` | Unchanged externally |
| `trait LayoutSource` | `src/layout.rs:101-109` | Internal abstraction; supplies declaration body lookups + an `import_width` hint |
| `DocumentSource<'a>(&'a Document)` | `src/layout.rs:111-121` | Pre-assembly source; `import_width` always returns `None` |
| `AssembledSource<'a>(&'a AssembledSchema)` | `src/layout.rs:123-133` | Post-assembly source; consults the hint table |
| `is_fixed_width_declaration` fallback when `declaration_body` is None | `src/layout.rs:240-244` | Returns `source.import_width(name).unwrap_or(false)` |
| `AssembledSchema::with_import_widths(map: BTreeMap<Name, bool>) -> Self` | `src/assembled.rs:45-58` | Builder method; folds hints into the schema |
| `AssembledSchema::import_width(&self, name) -> Option<bool>` | `src/assembled.rs:103-105` | Accessor |
| `AssembledSchema::assembled_type(&self, name) -> Option<&AssembledType>` | `src/assembled.rs:97-100` | New helper for code that needs to distinguish Local from Imported (used in the test) |

### §2.3 Backwards-compatibility moves

- `Schema::new(...)` keeps its signature. All existing call sites (`tests/document.rs`, `src/parser.rs`, `tests/reader.rs`) compiled unchanged.
- `AssembledSchema::new(...)` *changed* its signature (added `component: Name` as the first arg). The only caller is `Schema::assemble` which I updated. External callers in the operator's tree (none in the audited repo) would need the same update; this is a deliberate breaking change in the type contract — the alternative (preserving `new` and adding `for_component`) would surface a default-component foot-gun.
- `Layout::for_declaration` + `Layout::for_variant` keep their signatures and unchanged behaviour. The new behaviour lives on the new `for_assembled` + `for_assembled_variant` constructors.

## §3 Tests

Added three tests to `tests/document.rs`:

### §3.1 `schema_carries_component_name_and_renders_namespaced_uid`

Builds the spirit MVP Schema via the existing test Builder with `with_component_name(name("Spirit"))`; asserts:

- `schema.component_name().as_str() == "Spirit"`
- After `assemble`, `assembled.component().as_str() == "Spirit"`
- `assembled.uid_for(&name("Entry"))` decomposes to component=`Spirit`, type_name=`Entry`
- `entry_uid.to_string() == "Spirit::namespace::Entry"` (matches intent 469 form)
- `assembled.uid_for(&name("Magnitude")).to_string() == "Spirit::namespace::Magnitude"` (imported types render under *this schema's* component anchor — see §6 question 1)
- The `Schema::new` (no component) fall-back path renders `Anonymous::namespace::Entry`

### §3.2 `layout_for_assembled_places_imported_fixed_width_magnitude_in_root`

This is the key audit fix demonstration. Builds the spirit MVP with `with_component_name(name("Spirit"))`; assembles; supplies `import_widths = { Magnitude: true }` via `with_import_widths`; asserts:

- `assembled.assembled_type(&name("Magnitude"))` returns `AssembledType::Imported {..}` (sanity check that Magnitude is in fact imported, not local)
- `Layout::for_assembled(&assembled, &name("Entry")).root_positions() == vec![1, 4]` — Kind + Magnitude both in root
- `box_positions() == vec![0, 2, 3, 5]` — Topic, Summary, Context, Quote (all `newtype(String)`, variable-width)
- The position-4 field's individual `location()` is `FieldLocation::Root`

### §3.3 `layout_for_declaration_remains_conservative_for_imported_magnitude`

Pins the legacy pre-assembly path's behaviour: building the same Schema via the old path and calling `Layout::for_declaration(&schema, &name("Entry"))` still lands Magnitude in box (root=[1], box=[0,2,3,4,5]). Matches the existing `layout_places_fixed_fields_in_root_and_growing_fields_in_boxes` test exactly, and pins it for the future: callers who haven't migrated to `for_assembled` keep the old conservative behaviour.

### §3.4 `layout_for_assembled_without_import_hint_falls_back_to_box`

Pins the safety net: when `Layout::for_assembled` runs but no hint was supplied for Magnitude, it conservatively boxes (matches the legacy result). So callers who construct an AssembledSchema without supplying widths get the safe behaviour, not silently-broken codegen.

### §3.5 Test run

```
cargo test
  unittests src/lib.rs ............ 0 passed
  tests/document.rs ............... 20 passed (was 16; +4 added)
  tests/reader.rs ................. 3 passed
  doc-tests schema ................ 0 passed

cargo fmt -- --check ............. clean
cargo clippy --all-targets -- -D warnings ............. clean
nix flake check --option max-jobs 0 path:. ............. all checks passed
```

(The `path:.` form is needed under `/tmp/mockup-a-component-uid` because nix mis-detects `/tmp` as a git root otherwise — a workspace-location quirk, not anything wrong with the crate's flake.)

## §4 Reference to operator's existing implementation

Operator's main-branch implementation lives at `/git/github.com/LiGoldragon/schema/src/` on the `main` bookmark, parent commit `9dcd1391`. The mockup's diff vs main is the full content of slices A + B; nothing else changes. The three source files touched + the test file:

- `src/document.rs` — added 4 lines of field + 27 lines of new constructor surface (rest is the existing implementation, unchanged)
- `src/assembled.rs` — added 2 fields + ~50 lines of new accessor / Uid surface
- `src/layout.rs` — refactored the body/payload/expression helpers to take a `&dyn LayoutSource` instead of `&Document`; added the new constructors; added the trait + two impls
- `src/lib.rs` — added `Uid` to the re-export
- `tests/document.rs` — extended Builder, added 4 tests

Operator can diff `main..feature/component-uid-and-layout` for the precise patch shape.

## §5 Design notes (for operator's consideration)

### §5.1 Why the Uid struct, not a string

The `Uid` type is a struct, not a `String` or `&str`. Reasons:

- Forces UID *construction* through the schema (you can't `Uid::new` from arbitrary text), so the rendering rule lives in one place.
- Gives codegen a structured handle: `uid.component()`, `uid.type_name()` for cases where the codegen wants to emit `mod component { mod namespace { struct TypeName {...} } }` skeletons.
- `Display` impl handles the formatting; `to_string()` is the one-liner.
- Implements `Hash` so codegen can intern Uids in a map.

### §5.2 Why hint-based imported-width resolution, not transitive reading

Audit 171 §4.3 listed two paths: (a) move Layout off Document onto AssembledSchema; (b) imports carry width hints. I implemented (a) *and* a hint *table* on AssembledSchema rather than embedding the hint in `ImportedNames`. Rationale:

- Imports may resolve to types of varying widths; the binding doesn't know.
- Forcing widths into the import surface couples the import contract to layout, which feels wrong (the import contract is about "what names exist"; width is a property of each named type).
- Storing hints in a side-table on AssembledSchema lets callers supply them as part of the assemble pipeline without rewriting the type model. The eventual `.schema` reader can compute widths from the imported assembled schemas and feed them through `with_import_widths`.

The eventual reader integration looks roughly:

```rust
let mut hints = BTreeMap::new();
for imported in resolutions.iter().flat_map(|r| r.names()) {
    if let Some(loaded) = self.loaded_imports.get_for(imported) {
        let body = loaded.assembled.body(imported);
        if body.map(is_known_fixed_width).unwrap_or(false) {
            hints.insert(imported.clone(), true);
        }
    }
}
let assembled = schema.assemble(&resolutions)?.with_import_widths(hints);
```

This is left for operator to wire into `LoadedSchema` — out of scope for the mockup but the API is shaped for it.

### §5.3 NAMESPACE_LABEL is a constant

`const NAMESPACE_LABEL: &str = "namespace"` at the top of `src/assembled.rs` — the literal `"namespace"` text from intent 469 lives in one place. If the design ever changes the middle segment (e.g., to `types` or just dropping it), a one-line change covers the UID rendering.

## §6 Open questions surfaced for psyche

1. **UID for imported types — does the importing schema render under its own component name, or under the source schema's component?** I picked "the importing schema renders under its own component" (so `Spirit`'s assembled schema renders `Spirit::namespace::Magnitude` for an imported Magnitude). The alternative is to chase imports to the source schema and render `Sema::namespace::Magnitude`. Intent 469 didn't disambiguate. The current choice is simpler (no transitive metadata needed) but the alternative carries more identity through the wire. Worth psyche ratification.

2. **Anonymous as the default component name** — picked `"Anonymous"` (valid PascalCase, descriptive). Alternatives: empty Name (rejected by `Name::new`), `"Unknown"`, panicking. The fallback exists so the parser doesn't need a special "construct without component" path. If the eventual `.schema` parser is the only `Schema::new` caller and it always knows the file path, this default never surfaces in production — but the test/builder API uses it today.

3. **Hint API shape — `BTreeMap<Name, bool>` versus per-binding hints** — I used a flat name→bool map. If two imports both export the same name (already an `ImportCollisionWithLocal` error today), this maps cleanly. If the model later allows binding-scoped names, the hint shape should follow.

## §7 Bead

**Bead: `primary-5cfq` ([mockup] schema component-name UID + Layout-on-AssembledSchema (second-designer/172 slice A))**

The bead carries a note with the worktree path, branch, commit short-id, and integration guidance for operator.

## §8 Recommendation

**Operator should integrate as-is, or pick the best bits**, leaning toward as-is:

- Slice A is mechanically simple (new field + constructor + accessor + Uid type). The choice of `Anonymous` as the default + `Schema::new` delegating to `for_component` minimises churn in the parser/reader/test code.
- Slice B introduces a small trait (`LayoutSource`) to share logic between Document-based and AssembledSchema-based paths. This is moderately invasive — operator might prefer two parallel implementations to avoid the trait. The current trait-based shape is what surfaces the import-width hint cleanly; happy to redesign on operator's preference.
- The `with_import_widths` API is a deliberate small surface (just a builder method, no Reader integration yet); operator should wire it into `LoadedSchema` as a follow-up, computing hints by examining the assembled imports' bodies for fixed-width-ness.
- Slice C (engine threading) is *not* in this mockup; that's sub-agent B's slice per the orchestrator's frame at `0-frame-and-method.md`.

If operator prefers a different design for either slice, the report's reference points + tests should still be useful as a behavioural specification.

## §9 What this mockup does NOT do

- Does NOT add engine threading (slice C — sub-agent B's territory).
- Does NOT wire `with_import_widths` into `LoadedSchema` (deliberate; needs operator decision on hint-computation policy).
- Does NOT touch `parser.rs`, `reader.rs`, or rename `section.rs` (out of scope).
- Does NOT add the §8 coverage gap tests from /171 (multi-sub-variant, sema header smoke test, renamed/dropped/untranslatable projections, etc.) — those are slice D in the audit.
- Does NOT propose changes to /326-v13 design.

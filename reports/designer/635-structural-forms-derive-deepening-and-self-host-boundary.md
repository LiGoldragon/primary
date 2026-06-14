# Structural-forms derive deepening — named-field variants, the self-host boundary, worktree reset

A design-deepening pass on the nota/schema extension line. The psyche asked to
"find all constraints and good ideas and implement on worktrees, re-using
worktrees from this redesign line (rename and archive stale ones)." This
session: harvested the constraints + ideas (parallel workflow), reset the
worktrees, **implemented** one concrete derive capability and proved it green,
and — by grounding the work in real code — **corrected the self-host frontier**
report `631` had framed. The headline is an honest finding, not a triumph: the
structural derive cannot become the single source of truth for `TypeReference`
(or the `declarative.rs` macro nodes) for reasons deeper than named fields, and
the capability I built has no current consumer. The code kept me from the
mistake the report alone would have shipped.

## 1. Implemented: named-field structural-variant support (green, pushed)

The `StructuralMacroNode` derive rejected named-field enum variants outright
(`derive/src/lib.rs`: *"variants carry unnamed fields, not named fields"*),
even though it already supported every *shape* (`PascalAtom`, `Keyword`,
`Headed`, `HeadedAtom`, `HeadedBody`, `PascalHead`, `PascalHeadBody`) for
*unnamed*-field variants. The rejection was an arbitrary gap, not a structural
one — and `631` named closing it as the path to `TypeReference` self-host.

The change captures each variant's field identifiers and routes every shape's
decoded field expressions through one `assemble_fields` method that emits a
braced `Variant { field: … }` constructor for named variants and the existing
positional tuple otherwise; encode rebinds named fields to the same positional
`field_0…` idents so `encode_body` is untouched. **Tuple variants are
byte-for-byte unchanged.** A self-contained test mirrors
`TypeReference::Application { head, arguments }` plus the headed-atom,
fixed-arity headed, and headed-body named forms — all decode and round-trip.

- Branch `next/named-field-structural-derive` (`38ca1b5c`), stacked on the
  reconciled `next/combined-leaf-shapes`, **pushed to origin**.
- Full nota-next suite **71 pass**, clippy clean.

## 2. The self-host boundary — what actually blocks the hand-written impls (corrects `631`)

`631`'s "notable finding" said full `TypeReference` self-host needs only *"a
nota-next derive extension for named-field / sum-head variants."* Grounding in
the code shows that is **doubly incomplete**. The real boundaries:

**(a) `TypeReference` top-level decode is registry- and context-driven, not
pure structure — a permanent boundary.** `TypeReference::from_block_with_registry`
(`schema.rs`) dispatches declared user macros through a `MacroRegistry`
(`from_macro_invocation`), mutates a `&mut MacroContext`
(`remember_inline_declaration`), and lowers inline `|( )|` / `|{ }|`
declarations with side effects. A pure `#[derive(StructuralMacroNode)]` models
none of that — no registry, no context, no side effects. The hand-written
delegating impl is the **correct** structure↔semantics boundary, not a seed
edge to shrink to zero. (`ApplicationNode` — the derived helper for the
application *tail* — already self-hosts; that is as far as the derive reaches.)

**(b) The `declarative.rs` macro nodes are blocked by *other* gaps, none of
which is the named-field-variant gap I closed.** The three hand-written
structural impls there:

| Node | Kind | Why hand-written | Named-field-variant extension helps? |
|---|---|---|---|
| `SchemaMacro` | **struct** (4 fields) | derive is **enum-only** | No — needs struct-level derive |
| `MacroPattern` | **struct** (1 field) | derive is enum-only + delegates to a sigil parser | No |
| `MacroTemplateObject` | enum, **unnamed** variants | does **sigil parsing** (`CaptureName::from_token` reads `$name` / `$*name`) | No |

So **my named-field-variant capability currently has no consumer.** That is the
honest state: it is a correct, 631-specified, symmetric vocabulary-completion
and a prerequisite for any future named-variant node, but it retires nothing
today. The higher-value, real-consumer gap is **struct-level structural derive**
(`SchemaMacro` is the cleanest target: a 4-object body, each field a structural
node) — and even that hits wiring quirks (`SchemaMacro` decodes its name via
`schema_name()`, not a `Name` structural impl; `MacroPattern` delegates to the
sigil-parsing `MacroPatternObject`). The `627` "tiny hand-written seed" has more
edges than `631` enumerated: the NOTA block parser, the sigil parser
(`CaptureName::from_token`), the registry/context lowering, and `schema_name`
scalar classification are all legitimate semantic seams the structural derive
should *not* absorb.

This is the design-deepening result: the self-host frontier is now mapped from
source, not pattern-matched from memory.

## 3. Worktree reset — archive + rename (done)

The redesign-line worktrees were a mix of stale single-leaf seams and
misleadingly-named reuse bases. Actions taken (all audit-verified clean before
touching; stale **branches retained on origin** as `structural-forms-integration`
merge-parents, so nothing is lost):

| Repo | Worktree | Held | Action |
|---|---|---|---|
| nota-next | `pascal-head-body-shape` | `next/pascal-head-body-shape` (single leaf, folded into combined + sfi) | **archived** (workspace forgotten, dir removed) |
| nota-next | `typeref-shape` *(misnamed)* | `next/combined-leaf-shapes` + my new branch | **renamed** → `named-field-structural-derive` |
| nota-next | `structural-forms-integration` | operator integration | kept live |
| schema-next | `polish` | `schema-next-polish` (ancestor of sfi) | **archived** |
| schema-next | `typeref-structural-macro` | older typeref path (ancestor of sfi) | **archived** |
| schema-next | `schema-generics` *(misnamed)* | `next/typeref-structural-generics` | **renamed** → `typeref-structural-generics` |
| schema-next | `structural-forms-integration` | operator integration | kept live |
| schema-rust-next | `reaction-frame-emission` | `next/reaction-frame-emission` (contained in sfi) | **archived** (git worktree removed) |
| schema-rust-next | `structural-forms-integration` | operator integration | kept live (reuse base) |

Two findings surfaced during the reset:
- **The dir-name trap (fixed).** Two reuse dirs were named for the *wrong*
  branch (`typeref-shape` held combined-leaf-shapes; `schema-generics` held
  typeref-structural-generics). Renamed so dir = bookmark.
- **Broader stale registrations exist** (many jj workspaces from other lines —
  `collections-horizon`, `sigil-grammar`, `schema-daemon`, etc.). Out of scope
  here; flagged for a future general hygiene pass.

## 4. Flag: the schema-next reconciliation is NOT in operator's integration

This is the `634` coordination gap, still live at the schema-next level and
worth the psyche's attention. Operator's `structural-forms-integration`
(`a41162a`) was built from the **older** `typeref-structural-macro` path; it
does **not** contain the reconciliation `next/typeref-structural-generics`
(`17b4ebc7`) — the branch carrying the `631` fold-ins (derive-single-source,
flat `(Map K V)`, `HeadedAtom`, `SchemaError`→thiserror). Verified: `17b4ebc`
is a single commit *ahead* of where sfi diverged. So two reconciliation lines
exist for the same `TypeReference` work. **Decision needed** (operator, with
psyche steer): either rebase `17b4ebc` onto sfi, or have sfi re-integrate from
`17b4ebc` — but the divergence should not reach main. (Tracked alongside bead
`primary-3rj9` — the schema-next fold-in restore.)

## 5. Constraints governing this line (condensed from the harvest)

The binding rules any slice here must obey (full harvest in the session
workflow result): no backward-compat pre-production; full-English identifiers,
namespace-trimmed, no crate-name prefix; **every function a method on a
data-bearing type** (derive codegen emits into `impl` blocks); **don't
hand-edit generated mirrors** — change the `.schema` and regenerate;
**per-owner generate-and-commit** (each crate emits its own schema's Rust into
`src/schema/`, consumers re-export); NOTA bare-atom + positional records; flat
`(Map K V)` (`wqdi`); typed `Error` per crate via thiserror; **rkyv variant
evolution appends** under `#[repr(u8)]` (relevant if `MacroShape` /
`MacroOutputKind` ever persist); **no hand-rolled parsers above the named seed**;
mechanism-not-agent (`w312`) is the *why* of the whole emission thrust; intent
is dense — capture nothing here (this was read-only harvest + code); push
reconciled designer branches to origin so operator integrates from them.

## 6. The ordered slice menu (designer vs operator)

Most-ready first; owner in brackets:

1. **[operator] Land the `631` reconciliation** — push is done; integrate
   `next/typeref-structural-generics` (`17b4ebc`) onto schema-next, resolving the
   §4 divergence. Pure integration. (`primary-3rj9`.)
2. **[operator] `MacroShape` + `MacroOutputKind` emission** — declared in
   `core.schema`, zero generated Rust; plain closed enums the emitter already
   handles. Cheapest verified self-host gap; warm-up for the macro-table slice.
3. **[operator] Macro-table noun self-host** — generate the pattern family from
   `core.schema`, retire the hand-written `declarative.rs` nouns, typed newtype
   leaves. Stop at the `SchemaMacro`/`MacroLibrary` boundary (the `MacroTemplate`
   fork). (`primary-bojw`.)
4. **[designer] Struct-level `StructuralMacroNode` derive** — the real-consumer
   next step (§2): a struct decodes its body as N positional typed fields (or a
   single block). Consumer: `SchemaMacro`. Needs a small design pass on the
   struct's structural shape + the `schema_name`/sigil wiring quirks. *This is
   the higher-value successor to the named-field-variant work I landed.*
5. **[designer] `MacroTemplate` design fork** — `core.schema` models it as a
   structural mirror; `declarative.rs` as a typed output kind. Dissolve via
   `2zed`/kinds-as-macros. Gates macro-table stage 2 (#3 above).
6. **[designer] Visuals-as-data** — schema→mermaid emitter; independent,
   parallelizable; answers the `632` visuals friction.

## 7. What's next

The concrete, landed deliverables: the named-field derive capability (green,
pushed) and a clean worktree set (two reuse bases correctly named, four stale
worktrees archived). The design-deepening deliverable: the self-host boundary is
now mapped from source — the structural derive's reach ends at pure structure,
and the honest next slice is **struct-level derive support** with `SchemaMacro`
as its first real consumer, not the named-field/registry chase `631` implied.
The one item needing a psyche/operator decision is the §4 divergence.

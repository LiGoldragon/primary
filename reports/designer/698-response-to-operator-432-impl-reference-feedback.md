# 698 — designer response to operator 432 (impl-reference audit)

Operator 432 audited the 696 `{| |}` prototype branch
(`next/impl-reference-syntax` @ `b9689f4f`), reproduced the green
(189 tests / 13 impl_catalog / clippy / fmt), and called it *"a strong,
real prototype, but I would not merge as-is — harvest it, fix these
first."* Correct call. Of the five findings, **two are design rulings**
(resolved below) and **three are implementation**; the merge bar is
exactly operator's framing — **target resolution + lowering-path parity**.

## Design rulings

### Ruling 1 — target resolution (operator finding #1): ENFORCE

Operator: *"`TypeName {| ... |}` can target a type that does not exist in
the schema; the body-optional fixture proves a free-standing arbitrary
target, not impls for an elsewhere-declared type."* That is a real gap
**against the design, not a design ambiguity.** Report 695's body-optional
form is explicit: `TypeName {| impls |}` attaches impls to a type *whose
declaration is elsewhere*, **"resolved by ordinary symbol lookup."** The
prototype accepted any name without resolving it.

**Ruling:** a body-optional `Name {| impls |}` **must resolve** to a type
present in the schema — declared locally (separately), or imported once
the import path is wired. An unresolved/non-existent target is a **typed
error** (`UnresolvedImplTarget { name }`), not an accepted free-standing
impl. This restores the invariant the form exists for: the target always
*leads* **and** resolves — there are no free-standing impls over arbitrary
names. The body-optional fixture must be fixed to declare its target
elsewhere in the same schema (so it proves "elsewhere-declared," which was
the intent) and a sibling red fixture should prove an unresolved target is
rejected.

### Ruling 2 — duplicate / multiple blocks (operator finding #5): compose distinct, reject identical

Operator: *"duplicate standalone impl blocks for the same target are not
rejected or explicitly defined as composable."*

**Ruling:** multiple impl blocks for the **same target compose** (their
entries union) — this is Rust-consistent (a type may have many `impl`
blocks) and `Schema::referenced_impls()` already unions them. But a
**true duplicate** — the same trait marker declared twice, or the same
method *signature* declared twice on a target — is a **typed error**
(`DuplicateImplEntry { target, entry }`). So: distinct entries across
blocks compose; identical entries are rejected. Make it explicit in the
lowering, not left undefined.

## Implementation fixes (endorse operator's #2–#4)

- **#2 lowering-path parity (the hard merge gate).** `lower_source`
  (macro/document path) drops the impl catalog while `lower_schema_source`
  carries it — one schema text → two different semantic schemas. This is
  the one true correctness bug, not just a deferral: a schema **must lower
  to one semantics regardless of path.** The macro path's
  `NamespaceEntryWalk` already segments the block; it just needs to attach
  the lowered catalog to `Declaration::impls()` like the source-archive
  path. Non-negotiable before main.
- **#3 trait-name validation.** Trait names inside `{| |}` are type-names
  — validate them as PascalCase/type-name like every other type
  reference (coheres with record `3742`: a type's participations are
  marked, and named, at the declaration).
- **#4 full-signature in the error.** `UnverifiedImplReference` compares
  full `MethodSignature` internally but reports only the method name —
  include the full signature so a *signature mismatch* (right name, wrong
  params/return) is legible, not just a missing-name.

## What stays (operator confirmed sound)

The parser cursor-walk rewrite (replacing the broken `chunks_exact(2)`),
the typed rkyv-archivable catalog (text + binary round-trip), the lowered
enumerable `Schema::referenced_impls()` manifest, and the out-of-band
`RustSurface::verify_catalog` seam. These are the load-bearing wins; the
fixes are integration hardening on top.

## Division of labor + priority

Operator is in schema-next and audited the branch, so the cleanest split
is **operator harvests 696 and applies these fixes against the rulings
above, then merges** — while **designer pushes the propagation arc**
(697). Both are gated on the psyche's 697-Q3 priority, but they're
parallel (schema vs propagation), one per lane. No new Spirit capture:
the design (`ba6d` + 695) already governs; rulings 1–2 are its
application, not new intent.

# 18 — Audit fixes verified + designer positions on the convergence gaps

*schema-designer · report 18 · verifies operator's report-17 fixes landed
correctly (schema-next `dd11b720`, signal-spirit `5a22350c`), confirms operator's
gap audit (operator report 18) converges with my report-16 validation, and gives
designer positions on operator's four open questions. The auditor loop: I flagged,
operator fixed, I verify.*

## Spirit gate

No capture — operator's forwarded status plus my verification; no new psyche
statement. (Operator's proposed codec-floor rule, Q4 below, is *operator's*
proposal awaiting the psyche's blessing, not psyche intent yet.)

## Fixes verified against the code

| Audit (report 17) | Status | Evidence |
|---|---|---|
| M1 — `shape` stored in canonical IR, pollutes hash on rebase | **Closed, with the regression test I asked for** | `SpecifiedPayload` is now `{ reference, immediate_body }` (`specified.rs:485-487`); `shape(&self, schema)` is a derived method (`:506`). `SpecifiedSchema::content_hash` exists with a guard that derived shape does not move identity. The dangerous part is removed *before* the rebase. |
| M2 — `SourceDeclarationValue` leaked on the public Help API | **Public leak closed** | `HelpEntry.body: Option<HelpBody>`; `HelpBody` hides `SourceDeclarationValue` behind private `from/to_source_declaration_value` (`help.rs:408-418`). |
| M3 — twelve Help types where four would do | **Done** | `HelpRoot`/`HelpNode`/`HelpPlane`/`HelpSchemas` deleted; surface is `HelpRequest → HelpModel → HelpResponse → HelpEntry → HelpBody`. −189 lines in `help.rs`. |

The one honest caveat operator carries (full content-hash *invariance* test must
wait until `SpecifiedSchema` is the actual identity basis) is correct and
acceptable — the stored-derived-cache hazard is already removed, which was the
whole point of the deadline.

Remaining, correctly re-classified as design-completeness (not defects): `HelpBody`
still *internally* wraps `SourceDeclarationValue` and streams/families still route
through source form (`help.rs:265-303`). That is a follow-up (Q3 below), not a leak.

## Convergence with my validation

Operator's report-18 P1 gaps are the **same gaps my report-16 adversarial
validation found independently**: Rust lowering still reads `Schema` not
`SpecifiedSchema`; family identity still hashes `Schema::family_closure` (split
identity); `SourceMap`/language-service unimplemented; instance-schema is
decoder-driven but renders through a custom string projection rather than a typed
schema-codec value. Two independent audits converging on one gap list is high
confidence the map is complete — this is the double-implementation working as
intended.

## Designer positions on operator's four questions

Advisory; the psyche decides. These are the calls in my lane.

- **Q1 — family + whole-schema identity rebase together, or a transitional split?**
  **Together, one wave.** A knowingly-split identity is the exact "two subtly
  different identity bases" risk operator names; `c9fv` makes schema-address
  migration workspace-wide, so a coherent single rebase is cleaner than carrying a
  split. Ship `SpecifiedSchema::family_closure` in the same wave as the whole-schema
  rebase, with the temporary "old `Schema` and new `SpecifiedSchema` family hashes
  agree on current fixtures" regression operator proposes as the bridge *during* the
  wave, deleted when the old path goes.

- **Q2 — instance-schema typed projection now, or keep `InstanceSchemaText` as the
  bridge?** **Bridge for now.** The typed `SpecifiedInstanceSchema` (owned in
  schema-next, since nota-next must not depend on schema-next) is the right target,
  but it is gated on the still-unsettled **depth rule** (my earlier Q5: depth-1 vs
  expand-root-payload-one-level — the live `aligned()` is internally inconsistent
  about this). Settle the depth rule first; migrate instance-schema *after* Rust
  lowering has proven the `SpecifiedSchema`-projection pattern. Rushing a typed
  value before the depth rule risks baking the wrong shape.

- **Q3 — `HelpBody` stays in signal-spirit, or moves to schema-next?** **Moves to
  schema-next**, as a generic specified-projection body. signal-spirit should not
  own generic schema-introspection datatypes long-term; the same body algebra is
  what mentci and every future contract need (the broaden-to-mentci goal and the
  universal-introspection thesis, report 6). `HelpBody`-in-signal-spirit is the
  correct *bridge* today; the destination is a schema-next `SpecifiedSchema`
  projection type that signal-spirit and mentci both consume. So operator's "better
  still" is right — just sequence it after Rust lowering.

- **Q4 — bless schema-next's declaration codec as the trusted codec floor?** **Yes,
  explicitly — and it reconciles a finding from my own report 14.** Report 14's
  Theme A flagged "27 hand-written `to_schema_text` printers" in `source.rs`; the
  codec-floor rule resolves their status: **those printers ARE the trusted
  serialization floor (acceptable), not the forbidden application-level
  hand-printing.** The rule consumers must follow: *project into schema-next codec
  datatypes; do not hand-print schema text; schema-next's declaration codec is the
  floor until the schema grammar is itself generated from `SpecifiedSchema`.* That
  last clause (generating the grammar codec from the IR — the self-hosting `vpbx`
  vision) is a **separate, later epoch**, not this one. Worth capturing as a skill
  once blessed, because without it agents (including this audit) misclassify the
  codec floor's `format!` as a violation. (The duplication *across* those printers
  — report 14 Theme A — stays a dedup target; that is a repetition smell, distinct
  from the floor being legitimate.)

## Sequencing

I endorse operator's order — **Rust lowering → family identity → `-next` rename →
instance-schema → HelpBody-to-schema-next → SourceMap → schema daemon** — with two
refinements: bless the **codec-floor rule now** (cheap, and it unblocks correct
judgment for every consumer migration), and **settle the depth rule before
instance-schema** (it gates the typed projection). Rust lowering first is right: it
is the biggest producer, and migrating it is what makes "one IR" true for the
main code generator, not just the Help/introspection path.

## Advice for the three implementation slices (for operator)

**Through-line for slices 1 and 2 — the golden-equality gate.** Never delete the
old `Schema` path until the new `SpecifiedSchema` path produces **byte-identical
output on every fixture**, especially the big-schemas (`triad-reactive-large`,
`spirit-reactive-large`, `imported-mail-consumer`, `families`, `collections`,
`standard-newtype-impls`). Emit from the `Schema` wrapper and from direct
`SpecifiedSchema`, `assert_eq!` the token streams / family hashes. This is the one
discipline that turns "maximizes correctness" from aspiration into a test.

**Slice 1 — Rust lowering on `SpecifiedSchema`:**

- Before migrating, confirm `SpecifiedSchema`'s reference vocabulary covers
  everything the emitter *transforms*, or scoped/generic/fixed-width types become
  inexpressible: `ScopeOf` (emitter does the name transform `#name → #nameScope`),
  `Application { head, arguments }` (generics → `#head<#args>`), `FixedBytes(width)`,
  and generic `parameters` on declarations. (report-16 validation, rust-emission.)
- Scalars stay **named tokens over the alias preamble** (`pub type Integer = u64;`),
  not inlined std types — `Integer` is `u64` (not `i64`), `Path` is a `String`
  alias; the codec impls attach to the named token. (My POC got this wrong first;
  don't repeat it.)
- `shape` is now `shape(&self, schema)`, not a field — any lowering that read it
  threads the schema now.

**Slice 2 — family identity on `SpecifiedSchema`:**

- Hash the **role-preserving `immediate_body`**, never the derived terminal shape
  (now a method, already out of the bytes — keep it that way; that was M1's point).
- **Canonicalize namespace order in the whole-schema content hash to match the
  family closure.** Today the family closure sorts (`identity.rs:252-255`) but the
  whole-schema hash uses *declared* order (`identity.rs:162-164`) — so two
  order-only-different sources get the same family address but *different*
  whole-schema addresses. Sort the namespace in `SpecifiedSchema::content_hash` so
  the two bases agree. (report-16 validation, Q6 sub-decision.)
- **Hash the resolved canonical import target, not the local alias.** Today
  `FamilyClosure` carries `local_name` (`identity.rs:121`), so the same
  `crate:module:Type` under two aliases gets two hashes — identity leaks the import
  environment. Per the IR/SourceMap split the alias is a source fact; identity
  should be alias-independent. (My earlier Q4 — decide it here, in the closure port.)
- Keep operator's bridge regression (old `Schema` family hash == new
  `SpecifiedSchema` family hash on fixtures) *during* the wave; delete with the old
  path.

**Slice 3 — `-next` rename wave:**

- One **isolated, mechanical-only** wave — no semantic changes interleaved — so the
  diff reviews as "rename only."
- Rename in **dependency order**: `nota-next → nota` first (the others depend on
  it), then `schema-next → schema`, then `schema-rust-next → schema-rust`; then
  update consumer Cargo deps (`signal-spirit`, `meta-signal-spirit`, `spirit`) and
  the `pub use nota_next::…` → `nota::…` re-exports.
- Flip the `generator_name` constant (`schema-rust-next/src/lib.rs:69,78`) plus the
  `build.rs:536` / `migration.rs:90` literals, then **regenerate every fixture** —
  the `schema-rust-next` literal is stamped into ~92 `@generated` headers
  (report-14 audit). Add the fixture check operator already listed: assert no
  `*-next` string survives in generated output.
- ghq worktree paths and primary's untracked `repos/` symlinks churn locally —
  expected, not version-controlled.

**Cross-cutting:** the codec-floor rule (Q4, once blessed) governs all three —
project into schema-next codec datatypes, don't hand-print schema text. And the
old `Schema` type degrades to a transitional `SpecifiedSchema::from(schema)` wrapper
after slice 1; plan its deletion once family identity (slice 2) also reads
`SpecifiedSchema`, but keep it as the bridge until then.

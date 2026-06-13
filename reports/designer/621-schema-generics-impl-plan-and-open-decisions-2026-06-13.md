# Schema generics + TypeReference-as-structural-macro — implementation plan, the leg-divergence correction, and designer decisions on the open forks (Task #407)

## TL;DR (the load-bearing claims)

1. **One keystone unblocks everything.** The single new derive form
   `#[shape(pascal_head, body)]` (a captured PascalCase head + a variable-arity
   `Vec` tail) is the union of two shapes nota-next's derive already has
   (`PascalHead` = captured head + fixed arity; `HeadedBody` = fixed head +
   variable tail). It unblocks generic *application* `(Foo A B …)`, the
   parameterized-*declaration* head `(Work Event Write Read Effect)`, AND
   converting schema-next's hand-rolled `TypeReference` codec to a genuine
   structural macro (closing SD's D5-1 / `primary-xzzf`). Confined to
   `nota-next/derive/src/lib.rs`; **no runtime/macros.rs change** (the
   `BlockShape::pascal_headed_parenthesis` builder already takes a
   `MacroObjectCount`; `Any` reuses the existing capture-head-plus-`Rest`
   machinery, and `impl<Item> StructuralMacroNode for Vec<Item>` already decodes
   the tail). This is step 1, proven first in complete isolation.

2. **CORRECTION to report 620's premise.** The reaction frame is **NOT
   byte-identical across the 14 components.** Present-leg subsets genuinely
   differ — harness/system bind 1 leg (`SignalArrived`), agent 2, mind/mirror 3
   (no Effect), spirit/router/cloud/lojix 4, terminal 5 (a component-unique
   `MetaArrived`); repository-ledger's `Action` omits `Continue`. So "identical
   frame, only payloads differ" (report 619/620) was half-true. The design must
   be a **maximal frame with omittable legs**, not a single fixed frame applied
   verbatim. This is the central design correction this session.

3. **The two genuinely unproven risks are isolated at single-component proof
   points**: (a) the `pascal_head + body` derive form (step 1, provable alone);
   (b) whether `rkyv` + NOTA `#[derive]` compose over a multi-parameter direct
   generic `enum Work<Event,Write,Read,Effect>` (step 6, the #408
   compile-prototype — proven on spirit alone before any 14-component fan-out).

The full edit-site-level plan (4 parallel source investigations + synthesis)
was produced by the `nexus-generics-impl-plan` workflow; this report is its
durable home plus the designer judgment the workflow could not make.

## The 7-step plan (depth-first; each layer falsifiable before the one above)

| # | Repo | Slice | Key edit sites | Proof |
|---|---|---|---|---|
| 1 | nota-next | **PascalHeadBody derive form** (keystone) | `derive/src/lib.rs` only — enum variant, `parse` (the rejection site), `check_field_count`, `variant_value` (`MacroObjectCount::Any`), `direct_match_condition`, `direct_decode_constructor`, `encode_body` | `macro_nodes.rs`: `(Foo A B)`/`(Foo)` round-trip; non-Pascal head rejected; sibling fixed-arity not shadowed |
| 2 | schema-next | `TypeReference::Application` + delete the 4 hand-rolled head tables + collapse alias spellings (`Vec`→`Vector`) | `schema.rs` (TypeReference enum, `from_parenthesis_objects`, `from_macro_invocation`, NotaDecode), `declarative.rs`, `source.rs`, `identity.rs` (`ClosureWalk::visit_reference` — closed match blocks compile until handled) | multi-arg `(Foo A B)` lowers to `Application`, byte-stable round-trip; `(Vec X)` now fails (alias collapsed) |
| 3 | schema-next | parameterized **declaration** head `(Name Param …)` + register params as binders | `macros.rs` (`namespace_declaration`), `source.rs` (`SourceNamespace::from_block`), `resolution.rs` (carry param count), `identity.rs` (scope binders) | `(Plane Input Output){…}` lowers without `FamilyReferenceNotFound`; wrong arg-count → typed arity error at lowering |
| 4 | schema-next | accept `Application` in the **root** Input/Output position | `macros.rs` (`root_enum`), `source.rs` (`SourceRootEnum`), `engine.rs` (`lower_root_enum`), `identity.rs` (`family_root`) | root `(Work A B C D)` lowers to an application root; enum-body root still works |
| 5 | reaction + spirit | author shared `reaction.schema` (maximal frame, declared once, `Nexus*` dropped) + **pilot-migrate spirit only** | new `reaction.schema`; `spirit/schema/nexus.schema:46-67` | reaction lowers; migrated spirit lowers equivalently for the legs it uses |
| 6 | schema-rust-next + triad-runtime | emit the shared generic frame **once**; NexusRuntime emits payloads + application aliases; **delete** the `into_next_step` shim | `lib.rs` (new `ReactionFrame` `RustEmissionTarget` modeled on `PlaneEnvelopeTokens`; re-point name-keyed detection helpers; delete `NexusRunnerNextStepProjectionTokens`), `triad-runtime/src/runner.rs` | **#408 gate**: generated crate `cargo build`s; `Work<Event,Write,Read,Effect>` derives rkyv+NOTA; rkyv round-trip; runner still drives spirit |
| 7 | schema-next (×13) | migrate remaining components, binding only used legs | each component's `schema/nexus.schema` | each lowers + builds with its leg subset; reduced-leg components compile without absent variants |

Sequencing rationale (from the synthesis): step 1 is the cheapest, most
self-contained, and the single thing the whole insight rests on — if
`pascal_head + body` doesn't round-trip, nothing downstream is worth building.
Steps 2-4 build schema-next's capability bottom-up (each a compile+round-trip
gate). Step 5 proves the frame design on ONE component; step 6 is the #408
compile-prototype on that same component (the riskiest assertion). Only after
spirit compiles end-to-end does step 7 fan out. Cross-repo integration ordering
(nota-next must rebuild before schema-next consumes the new derive) is an
operator integration dependency — the three designer branches cannot merge
independently.

## Designer decisions on the open forks (NOT asked — decided + reversible)

Per the recorded principle [when work is already authorized, execute it the
right way and all the way autonomously … reserve asking for genuinely
unresolvable forks] (Spirit 48y4) and the designer authority for pattern-based
and high-ratification decisions. Each is reversible; psyche intent supersedes.

- **O1 — Application head identity → `enum {Local(Name) | Imported(ResolvedImport)}`.**
  *Decided (pattern-based: typed sum for a real distinction).* A generic head
  can be a locally-declared parameterized type, not only a cross-crate import;
  `ResolvedImport` alone cannot represent it. Two cases ⇒ two variants.
- **O6 — Application syntax → implicit `(Work A B C D)`, not explicit `(Apply …)`.**
  *Decided (pattern-based: consistency with the existing `(Vec Domain)`
  application form).* The collision risk (a broad `PascalHeadBody` swallowing
  specific heads) is handled by dispatch ordering: specific built-in/declared
  heads route through the direct-decode fast path that runs first; the broad
  application form is the fallback. The conflict-validation exemption
  (`parenthesized_head_shape` returns `None` for `Any`) means this ordering is
  **not** compiler-checked, so it is an explicit ordering rule + a test (step 1d).
- **O8/O2 — Arity validation → at lowering, carrying param count through the
  resolver.** *Decided (pattern-based: fail-fast typed errors, `rust/errors`
  discipline).* Wrong arg-count is a typed lowering error, never a deferred
  emitter panic.
- **O9 — Drop `Nexus*` prefix in the SAME pass as the frame extraction.**
  *Decided (high-ratification: mechanical rename into already-decided
  no-ancestry naming; it touches the same name-keyed detection helpers, so
  splitting it doubles the churn).* `Work`/`Action`, not `NexusWork`/`NexusAction`.
- **O5 — terminal's component-unique `MetaArrived` → declared locally, outside
  the shared frame (closed maximal frame).** *Lean (preserves the shared frame's
  universality; a component-specific leg is a local concern).* Revisit only if a
  second component grows the same need.

### Held back (genuinely competing or prototype-pending — carried, not committed)

- **O3 — how omittable legs work.** *Leaning, prototype-pending (step 5/6).*
  The elegant candidate: declare the maximal frame over direct type parameters,
  and an absent leg is bound to an **uninhabitable payload type** (a Never-like
  enum) so that variant cannot be constructed — the special case dissolves into
  the normal case (beauty), with zero per-component frame variation. Whether
  rkyv/NOTA derive cleanly over a frame with an uninhabitable parameter is
  exactly what step 6 must prove; if not, fall back to several frame arities.
  This is the maximal-frame design's load-bearing unknown.
- **O4 — root-position `Application` vs the version-control family-closure.**
  *Held.* `identity.rs` assumes root = enum; a non-enum application root changes
  what the closure-hashing/content-addressing layer sees. Step 4 must verify the
  closure incorporates the application structurally (head + args) without
  breaking closure equality; flagged as needs-care.
- **O7 — where `reaction.schema` physically lives** (own crate vs alongside
  signal-frame vs self-registered per daemon). *Held — repo-management /
  system-operator-adjacent.* Sets the import target string and the
  schema-rust-next emission boundary. Decide with the repo map before step 5
  authors the file; does not block steps 1-4.
- **Param-count reconciliation (a risk, not an O):** runtime `NextStep` has 5
  params (Reply, SemaWrite, SemaRead, Effect, Work); proposed `Action` lists 5,
  `Work` lists 4. Whether `Action<…>` structurally projects to `NextStep`
  without the associated-type shim must be pinned in step 6 before deleting the
  projection, or the runner breaks.

## What is dispatched / in flight

- **Step 1 implementation** — background subagent on a fresh
  `next/pascal-head-body-shape` worktree off origin/main; full implement + the
  four-case round-trip test + branch push. The keystone proof.
- **Deploy (#406)** — background subagent running the full ouranos NixOS rebuild
  for the spirit 0.12.1 referent fix (see report 620 file 3 for the corrected
  topology; the fix is already on spirit `origin/main` at `f4635c3`).

## What stays true from report 620

The constraints are unchanged: no type aliases as a binding mechanism (Spirit
`sarw`); the universal frame declared once, applied per component (Spirit
`n6fz`, pending re-record with the `[triad-runtime]` referent once the
referent-guardian deploy lands); no ZST carrier; direct-parameter generics so
derives work natively. The structural-macro machinery DOES implement the
concept — the only real gap was `pascal_head + body`, which step 1 closes.

## Execution progress (live)

- **Step 1 — DONE.** nota-next branch `next/pascal-head-body-shape` @ `db0f10a2`.
  `PascalHeadBody` derive shape; no runtime change needed (the keystone
  hypothesis held exactly); 4/4 round-trip cases + full suite + clippy green.
- **Step 2 — DONE.** schema-next branch `next/schema-generics` @ `55413767`
  (parented on `f460e7b6`). `TypeReference::Application` over the typed
  `{Local|Imported}` head; broad form routed through the nota-next derive;
  `Vec`→`Vector` alias collapse; dispatch order built-in→declared→broad
  (test-pinned, NOT compiler-checked — the conflict-validation exemption means
  ordering is an explicit rule). 143/143 tests, clippy clean. Closes D5-1.
  Codec-table outcome (the risk-#4 question, RESOLVED): the `Block` path unified
  through the structural-macro seam; the `ExpandedObject` (declarative.rs) and
  `RawNotaDatatype` (source.rs) paths kept SEPARATE with alias-collapse +
  `Application` fallback (different input types — they cannot share the
  Block-only derive); the rkyv `NotaDecode` stays the canonical machine
  boundary. `Map` stays grouped `(Map (K V))` (code is ground truth, not the
  plan's flat `(Map K V)`). A stray `(Vec X)` now lowers to
  `Application{head: Local(Vec)}` (fails later at resolution, not at parse).
- **Step 3 — DONE.** schema-next `next/schema-generics` @ `3a6d6ec4`.
  Parameterized declaration heads `(Name Param …)` + per-declaration nested
  binders + lowering-time arity validation (`Schema::arities_verified()` →
  `SchemaError::GenericArityMismatch`, O8). 149/149 tests, clippy + fmt clean.
  Elegant confirmation: `DeclarationHead::from_parameterized` delegates to the
  EXACT step-1 derive node (`ApplicationNode::from_structural_block`) — the
  parameterized declaration head is structurally identical to the application
  form, so the one keystone covers both. `ResolvedImport` now carries
  `parameter_count`; the import-arity branch is wired but unexercised until the
  `Local→Imported` head rewrite (a later step).
- **Step 4 — RUNNING.** Root-position application — a typed root sum
  `{ RootEnum(EnumDeclaration) | RootApplication(Application) }`, same branch.
  **O4 RESOLVED (was held back):** an application root's content-address is the
  hash of its head-import closure + argument closures, reusing the EXACT
  field-position `Application` closure walk step 2 built — no new hashing
  primitive; an application root is closure-walked identically to a
  field-position application, so content-addressing stays deterministic. The
  step-4 subagent carries a verification gate: confirm against the real
  `identity.rs` closure code that an application root slots in cleanly (stable
  hash across re-lowering; hash changes when an argument type changes), and
  STOP-and-report if the closure-hash bakes in a root=enum assumption rather
  than inventing a new scheme. This moves O4 out of the report's uncertainty
  section into a decided, falsifiable implementation.

### Integration note for operator (cross-repo ordering)

The dependency order is nota-next (`next/pascal-head-body-shape`) → schema-next
(`next/schema-generics`). The schema-next branch carries a designer-prototype
Cargo `[patch."https://github.com/LiGoldragon/nota-next.git"]` → the step-1
worktree so the slice is provable now; operator integrates step 1 to nota-next
main, then DROPS the patch so the `branch = "main"` git dep carries the derive.
The three designer branches cannot merge independently.

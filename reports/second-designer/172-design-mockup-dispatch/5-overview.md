*Kind: Overview · Topic: design-mockup-dispatch · Date: 2026-05-24 · Lane: second-designer (orchestrator synthesis)*

# 172 · 5 — Overview: four mockup worktrees for operator

## §1 Summary

Per psyche directive 2026-05-24 (intent 502-504, 506), second-designer dispatched four sub-agents in parallel; each landed a working mockup on a feature-branch worktree of the relevant repo, with tests passing under `cargo test` + `cargo fmt -- --check` + `cargo clippy --all-targets -- -D warnings` + `nix flake check --option max-jobs 0`. Each sub-agent wrote a per-agent report (`1-` through `4-`), pushed the branch to origin, and created a bead so operator can find every worktree from one query.

This overview ties them together: the catalog (§2), open psyche questions (§3), parallel landings to be aware of (§4), recommended operator integration order (§5), and the cross-reference back to /171 + /170 + intent corpus (§6).

## §2 The catalog — four worktrees, four feature branches, four beads

| # | Slice | Worktree | Branch | Commit | Bead | Tests | Per-agent report |
|---|---|---|---|---|---|---|---|
| A | Schema component name + UID + Layout-on-AssembledSchema | `/tmp/mockup-a-component-uid` | `feature/component-uid-and-layout` (schema repo) | `b5c4f373` | `primary-5cfq` | 4 new tests pass; 20 total green | `1-schema-component-and-layout-mockup.md` |
| B | Engine threading + multi-sub-variant + upgrade coverage | `/tmp/mockup-b-engine-routing` | `feature/engine-routing-and-upgrade-coverage` (schema repo) | `52f5364692fa` | `primary-gqj6` | 8 new tests pass; 27 total green | `2-engine-routing-and-upgrade-coverage-mockup.md` |
| C | Extensible macro-variant lowering engine | `/tmp/mockup-c-macro-variant-engine` | `feature/macro-variant-engine` (schema repo) | `e4a86450` | `primary-oh6i` | 8 new tests including the engine-vs-assemble equivalence test; 16 prior pass | `3-extensible-macro-variant-engine-mockup.md` |
| D | SpawnEnvelope `parent_authority` + DurableIdentity via SO_PEERCRED | `/tmp/mockup-d-durable-identity` | `feature/durable-identity-via-peercred` (signal-engine-management) | `0eeae13e` | `primary-p0ke` | 9 new + 7 prior = 16 tests pass | `4-spawn-envelope-and-durable-identity-mockup.md` |

All four branches are pushed to their respective origin remotes. All four beads are filed with the worktree path + branch + report path in their notes.

### §2.1 How to find every mockup from one query

```bash
bd query 'label:mockup label:second-designer'
# Or by the prefix:
bd search '[mockup] second-designer/172'
```

Either query surfaces all four beads. Each bead's note carries the worktree path + branch name + report path.

## §3 Open psyche questions surfaced by sub-agents

Five concrete decisions land back to psyche for ratification. None are blockers — each mockup chose a default; operator can integrate the default and the psyche can override later.

### §3.1 Sub-agent A — UID for imported types

When `spirit.schema` imports `Magnitude` from `signal-sema/magnitude.schema`, should the UID render as:
- (a) `spirit::namespace::Magnitude` (importing schema's component, current mockup choice) — UID reflects where the type is USED
- (b) `signal_sema::namespace::Magnitude` (source schema's component) — UID reflects where the type is DEFINED

Lean: (b) — UIDs should be canonical; the same Magnitude type referenced from 10 component schemas should have ONE UID, not 10. Sub-agent A picked (a) for the mockup because the AssembledSchema lookup is simpler; (b) requires chasing import bindings to their source. Operator can flip after psyche confirms.

### §3.2 Sub-agent B — engine storage site

Engine annotations live on Variant in the namespace. Should the lowered representation surface them on:
- (a) `Route { ..., engine: Option<Engine> }` (current mockup choice) — engine is a property of a dispatch operation
- (b) `AssembledType { name, body, engine: Option<Engine> }` — engine is a property of a type's role

Lean: (a) — engines drive DISPATCH, and Routes ARE dispatch. Body types may participate in multiple routes (one type can be the body of multiple endpoints if the schema allows), but the engine semantics belong to the route, not the type. Sub-agent B picked (a). Operator integrate as-is unless psyche prefers (b).

### §3.3 Sub-agent C — extensibility approach + `from_schema` resolver

Two sub-questions from this slice:

- (a) **Extensibility approach**: closed enum + recompile (sub-agent's choice) vs trait-object dispatch (kept open via public `MacroVariantLowering` trait). The chosen pattern gets compiler-enforced exhaustive match across the dispatch table; the trait stays public so future operators can add runtime-registered variants without breaking the closed enum.
- (b) **`from_schema` resolver lifting**: the current `LoweringEngine::from_schema(schema)` constructor delegates to `schema.assemble(resolutions)?` rather than lifting the resolver into the engine's own surface. This keeps the mockup small but means import resolution still lives in `Schema`, not the engine. Operator's call whether to lift the resolver.

### §3.4 Sub-agent D — identity types' final home

`ProcessIdentifier`, `UnixGroupIdentifier`, `PeerCredentials`, `DurableIdentity` currently land in `signal-engine-management/src/identity.rs`. But `signal-persona-origin` already owns `UnixUserIdentifier` and other origin-domain types. Two options:
- (a) Keep identity types in `signal-engine-management` (current mockup choice) — colocated with `SpawnEnvelope` they extend
- (b) Migrate to `signal-persona-origin` alongside `UnixUserIdentifier` — origin-domain types in one place

Lean: (b) — origin types belong in `signal-persona-origin`. Sub-agent D picked (a) because moving cross-crate types requires bumping signal-persona-origin's surface, which is a wider blast radius. Operator can migrate when next touching signal-persona-origin.

### §3.5 Pre-dispatch question — ParentAuthority shape

(From my chat reply before sub-agent D ran.) `ParentAuthority { parent_process_identifier, parent_unix_user_identifier }` uses PID, but supervisor PID changes on supervisor-restart. Sub-agent D went with the per-spawn-regenerate pattern: supervisor regenerates the envelope on each child-spawn, so each envelope carries the CURRENT supervisor PID. Confirm or pull to a longer-lived anchor (systemd unit, socket-path whitelist)?

## §4 Parallel landings to be aware of

### §4.1 Designer `/329` lands the same conceptual move as sub-agent C

While sub-agents were dispatched, prime designer landed `/329 schema macro-component extensibility — InputStruct-per-variant pattern; SchemaMacro trait + executer dispatch; 7 builtins (Enum Struct Reference Import Header Feature ContainerType) + extensibility via registration; positional dispatch filtering; reusability across custom languages per /326-v13 §3`.

This is the same intent-506 territory sub-agent C mocked up. Designer's report frames the architecture (SchemaMacro trait + 7 builtins + registration-based extensibility); sub-agent C's mockup is the runnable code expression (closed enum with 3+ builtins so far, `MacroVariantLowering` trait kept public for future plugin surface, equivalence test proving behavior preservation).

The two are complementary:
- Designer's /329 = architecture report + naming convention (`SchemaMacro` trait, 7 builtin macros named, registration mechanism)
- Sub-agent C's mockup = working code with tests, currently 3 declaration variants + 1 reference + 1 feature + 1 import (6 mockup builtins)

Recommendation for operator: read /329 first for the canonical naming + builtin set (Enum / Struct / Reference / Import / Header / Feature / ContainerType), then walk sub-agent C's worktree to see the patterns expressed as Rust types. If naming diverges (e.g., my mockup says `MacroVariant`; designer's report says `SchemaMacro`), rename to match /329 — designer's names win.

### §4.2 Second-operator `/180` is the baseline all schema mockups compare against

Sub-agents A, B, C all worked against the state second-operator landed in `/180`. Each mockup is a forward-diff on top of `/180`. Operator can cherry-pick from each mockup's worktree onto main as a fast follow-up to `/180`.

### §4.3 Sub-agent C's worktree caveat — jj workspace add doesn't carry `.git`

Sub-agent C noted: `nix flake check` in the `/tmp/mockup-c-macro-variant-engine` worktree needed `path:.` form (or `jj git init --colocate`) because `jj workspace add` produces a working copy WITHOUT a `.git` directory. Operator running checks in any jj-workspace-add worktree should pass `path:.` rather than relying on `nix flake check` resolving the workspace as a git ref. Same applies to mockups A and B (also jj-workspace-add). Mockup D's worktree appears to have been pushed cleanly so `nix flake check` against the pushed ref works.

## §5 Recommended operator integration order

If operator wants to integrate all four:

1. **A first** — adds component name + UID + Layout-on-AssembledSchema. Foundational; B and C build on `Schema::for_component` constructor. Touches `src/document.rs`, `src/assembled.rs`, `src/layout.rs`, `src/lib.rs`.

2. **B second** — adds engine field to Route + 4 upgrade tests + multi-sub-variant test + owner/sema lowering tests. Minor merge work where A's `Schema::for_component` constructor changes the function signature B's tests use; trivial to resolve.

3. **C third** — adds `MacroVariant` + `LoweringEngine` as a new module alongside `Schema::assemble`. Non-invasive — doesn't replace `assemble()`, just demonstrates the architecture. Operator should align naming with designer's `/329` (`SchemaMacro` trait) before landing.

4. **D last** — independent of A/B/C (different repo). Can land in parallel. The `parent_authority` field on `SpawnEnvelope` is a wire-format change (one trailing record); coordinate with anyone who has SpawnEnvelope-consuming code (every persona daemon, persona-pi). The `PeerCredentialsSource` trait abstraction is the load-bearing design choice; operator should review it before bolting concrete `rustix`-backed implementations into supervised daemons.

If operator only wants to integrate ONE:
- **A or D** are highest-value standalone landings. A fixes the Magnitude-in-box bug AND unlocks UID generation. D installs the durable-identity mechanism the workspace's auth story needs.

If operator has ALREADY done some of this:
- Each per-agent report's §"Reference to operator's existing implementation" calls out the comparison points (file:line in current main). Operator can diff the mockup against their existing landing and integrate the best ideas of either.

## §6 References

### §6.1 Inputs to this dispatch

- `reports/second-designer/171-audit-second-operator-180-schema-v13-2026-05-24.md` — /171 §10 forward slices A+B → mockup A; slices C+D → mockup B
- `reports/second-designer/170-schema-lowering-executor-model-2026-05-24.md` — lowering executor design → mockup C
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — current schema design (uniform header form)
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — operator design critique
- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` — baseline implementation all schema mockups target
- `reports/designer/249-component-intent-gap-analysis.md` — SpawnEnvelope + SO_PEERCRED corpus
- `reports/designer/299-design-origin-process-and-agent-identity.md` — SO_PEERCRED accept-time identity
- `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md` — IngressContext composition
- `reports/designer/307-design-golden-ratio-namespace-split.md` — SO_PEERCRED uid checks per message
- Intent records 388-506 — design corpus (catalog in /324 §2 + /174-v5 + this report's §1)

### §6.2 Parallel landings during dispatch

- `reports/designer/329-...` — designer's SchemaMacro architecture (same intent-506 territory as mockup C); operator should align mockup C's naming with /329

### §6.3 Per-agent reports

- `reports/second-designer/172-design-mockup-dispatch/0-frame-and-method.md` — orchestrator frame + per-agent contract
- `reports/second-designer/172-design-mockup-dispatch/1-schema-component-and-layout-mockup.md` — sub-agent A
- `reports/second-designer/172-design-mockup-dispatch/2-engine-routing-and-upgrade-coverage-mockup.md` — sub-agent B
- `reports/second-designer/172-design-mockup-dispatch/3-extensible-macro-variant-engine-mockup.md` — sub-agent C
- `reports/second-designer/172-design-mockup-dispatch/4-spawn-envelope-and-durable-identity-mockup.md` — sub-agent D
- `reports/second-designer/172-design-mockup-dispatch/5-overview.md` — this report

### §6.4 Worktree locations

- `/tmp/mockup-a-component-uid` — schema crate, `feature/component-uid-and-layout`
- `/tmp/mockup-b-engine-routing` — schema crate, `feature/engine-routing-and-upgrade-coverage`
- `/tmp/mockup-c-macro-variant-engine` — schema crate, `feature/macro-variant-engine`
- `/tmp/mockup-d-durable-identity` — signal-engine-management crate, `feature/durable-identity-via-peercred`

### §6.5 Beads

- `primary-5cfq` — slice A bead
- `primary-gqj6` — slice B bead
- `primary-oh6i` — slice C bead
- `primary-p0ke` — slice D bead

## §7 What this dispatch did NOT do

- Did NOT land on main (each mockup is on its own feature branch; operator owns the merge)
- Did NOT block operator (operator can continue work on main; mockups are advisory, not gating)
- Did NOT close operator beads (operator owns bead state; mockup beads are advisory)
- Did NOT replace `Schema::assemble()` (mockup C adds alongside; psyche or operator decides the eventual replacement)
- Did NOT capture wire-format intent (the `parent_authority` field on SpawnEnvelope is a wire-format addition; needs explicit psyche ratification before mockup D lands on main)

*Kind: Frame · Topic: design-mockup-dispatch · Date: 2026-05-24 · Lane: second-designer (orchestrator)*

# 172 · Frame — design-mockup dispatch

## §1 Psyche directive + intent context

> "Use a sub-agent to create a work tree branch of anything in your design that you want to test into actual implementation on one of the parts of what we're doing, like with the schema and the signal frame, knowing about a stable, durable ID, like you say, peer cred. Yeah, dig deeper into the spawn envelope mechanism. Actually, create mockups. [...] Create a work tree of whatever you want to show a design for and create a mockup test with the changes that you want to make in the library with your sub-agent. And then the operator can use that as a starting point to see if he's done it different, if he's already done it, or if you've done it different. [...] Each agent should do that, and it's a report for sure, but then there should be a final report talking about all of them, and then put a beads on each after it's made for an operator to actually look at, and if it's already been implemented by the operator, to compare it for possible better design ideas or as a critique of its own work and to integrate the best decisions of either or both."

> [Mid-dispatch clarification:] "how to create re-useable components for a schema based lowering (assembledSchema) from macro-schema-variants in schema's builtin engine (builtin variants at nodeDefinition points, where the struct for that type of macro is defined as the input object when used (they're a data-carrying variant type in that sense - they need an input, a struct defining its input type for that macro-variant))"

Captured as intent 502 (design-mockup-method Decision Maximum), 503 (Principle Maximum), 504 (Decision Maximum — per-agent contract), 506 (schema-lowering-engine Clarification Maximum — extensible macro-variant engine).

## §2 Four-subagent dispatch

| # | Slice | Sub-agent | Target repo | Branch |
|---|---|---|---|---|
| A | Schema component name + UID + Layout-on-AssembledSchema | 1-schema-component-and-layout-mockup | `/git/github.com/LiGoldragon/schema` | `feature/component-uid-and-layout` |
| B | Engine routing + multi-sub-variant + upgrade coverage | 2-engine-routing-and-upgrade-coverage-mockup | `/git/github.com/LiGoldragon/schema` | `feature/engine-routing-and-upgrade-coverage` |
| C | Extensible macro-variant lowering engine | 3-extensible-macro-variant-engine-mockup | `/git/github.com/LiGoldragon/schema` | `feature/macro-variant-engine` |
| D | Spawn envelope + durable identity via SO_PEERCRED | 4-spawn-envelope-and-durable-identity-mockup | `/git/github.com/LiGoldragon/signal-engine-management` (or signal-persona-origin) | `feature/spawn-envelope-typed-and-durable-identity` |

Plus `5-overview.md` — orchestrator synthesis after sub-agents return, with the catalog of all worktree branches + beads.

## §3 What each slice addresses

### §3.1 Slice A — Schema component name + UID anchor + Layout-on-AssembledSchema

Addresses /171 §4.1 (component name gap), §4.3 (Magnitude-in-box bug), §7 (UID generation gap). Implements:

- `Schema::for_component(component, imports, ordinary_header, owner_header, sema_header, namespace, features) -> Result<Schema>`
- `AssembledSchema::component(&self) -> &Name`
- `AssembledSchema::uid_for(&self, type_name) -> Uid` (e.g., `spirit::namespace::Topic`)
- `Layout::for_declaration(assembled, name)` consuming AssembledSchema, not Document
- Tests: UID for Spirit::Entry; Magnitude lands in ROOT (not box) after import resolution

This unblocks UID-driven codegen and fixes the wire-encoding bug where Magnitude gets length-prefixed as a box.

### §3.2 Slice B — Engine routing + multi-sub-variant lowering + upgrade test coverage

Addresses /171 §4.2 (Engine annotations stored but invisible), §4.4 (multi-sub-variant lowering test gap), §4.5 (owner+sema header coverage), §4.6 (upgrade projection paths). Implements:

- `Route` carries `engine: Option<Engine>` (populated when `endpoint_body` resolves variant)
- `AssembledSchema::routes_by_engine(engine) -> impl Iterator<Item = &Route>` helper
- Multi-sub-variant route test: `(Watch [State Records Questions])` → namespace `Watch [(State StateSubscription) ...]` lowers to 3 routes
- Owner header + sema header non-empty smoke test
- Renamed projection test (current name not in previous, `RenamedFrom` annotation)
- Dropped projection test (Drop annotation on removed type)
- Untranslatable projection test
- RemovedTypeRequiresAnnotation error path test

This unblocks engine-driven dispatch codegen for /324 §3.1.

### §3.3 Slice C — Extensible macro-variant lowering engine

Addresses intent 506 (just captured). Implements the lowering engine as a data-carrying enum of macro-variants, each variant carrying its own input struct:

```rust
pub enum MacroVariant {
    EnumDeclaration(EnumDeclarationInput),       // [V1 V2 ...] shape
    NewtypeDeclaration(NewtypeDeclarationInput), // (T) shape
    RecordDeclaration(RecordDeclarationInput),   // (F1 F2 ...) shape
    NamedField(NamedFieldInput),                 // (name [variants]) shape
    Reference(ReferenceInput),                   // bare ident shape
    // Built-in feature variants:
    ReplyFeature(ReplyFeatureInput),
    EventFeature(EventFeatureInput),
    ObservableFeature(ObservableFeatureInput),
    UpgradeFeature(UpgradeFeatureInput),
    // Built-in engine variants:
    EngineAnnotation(EngineAnnotationInput),
    // Extensible: new variants land by adding new enum members + input structs
}

impl MacroVariant {
    fn lower(&self, context: &LoweringContext) -> Result<LoweredNode>;
}
```

Each variant's input struct defines the shape of data it consumes at the node-definition point. The builtin engine dispatches by shape AND head-tag, calling the matching variant's `lower()` method.

This replaces the hard-coded shape rules in my /170 with a data-driven dispatch table. Reference intent 506 + /170 §2 dispatch-rules table + intent 470 (custom-language library foundation per Shen-style mid-compilation).

### §3.4 Slice D — Spawn envelope + durable identity via SO_PEERCRED

Addresses the psyche's "stable durable ID, like you say, peer cred" + "dig deeper into the spawn envelope mechanism." Implements:

- `SpawnEnvelope` typed struct in `signal-engine-management` (or its successor crate):
  - `engine_id: EngineIdentifier` — stable, durable, set by parent supervisor
  - `component_name: ComponentName` — what this process represents
  - `parent_authority: ParentAuthority` — verifiable at handshake
  - `socket_paths: SocketPaths` — where this component will bind/connect
- `DurableIdentity { engine_id, peer_credentials }` combining envelope + SO_PEERCRED
- Receiving-daemon verifier: on `accept()`, read SO_PEERCRED; compare to spawn-envelope-declared identity; reject if mismatch
- Nix-side handoff mock: how the envelope reaches the process at spawn
- Worked example: persona-daemon spawns mind-daemon with envelope; mind-daemon binds owner socket; when persona-daemon connects, verify SO_PEERCRED matches envelope.parent_authority

Reference reports: `reports/designer/249` + `/258` + `/299` + `/301` + `/307` (existing spawn envelope + SO_PEERCRED design corpus); `signal-engine-management` ARCH + protocols/active-repositories.md entry.

## §4 Per-agent contract

Each sub-agent MUST:

1. **Create a worktree** of the target repo at a feature branch:
   - For jj-managed repos: `jj workspace add --name <branch-name> /tmp/worktree-<slice>-<short-id>` then `jj new -m '<initial msg>'`. The jj `workspace add` form creates a new working copy at the path with a workspace name.
   - Alternative for jj: `cd /tmp/worktree-... && jj git clone <remote>` if workspace add is unavailable.
   - For git-managed repos: `git worktree add -b feature/<slice-name> /tmp/worktree-<slice>-<short-id>`
   - Report the absolute worktree path back to orchestrator.

2. **Implement the mockup** with a working test demonstrating the change. Tests MUST pass (`cargo test` + `cargo fmt -- --check` + `cargo clippy --all-targets -- -D warnings` + `nix flake check --option max-jobs 0` if a flake exists).

3. **Commit on the feature branch** with descriptive message via `jj describe -m '...'` then `jj new -m 'next-step'` (inline only, NEVER let jj open an editor).

4. **Push to remote** if a remote exists and the branch can be pushed safely: `jj git push --bookmark feature/<slice-name> --allow-new` or `git push -u origin feature/<slice-name>`. If push fails for any reason, leave the worktree local + report.

5. **Write a per-agent report** at `reports/second-designer/172-design-mockup-dispatch/<N>-<slice-name>.md` (back in the primary workspace, NOT in the worktree). Report MUST include:
   - Worktree path + branch name + commit short-id
   - What was implemented (list of types/functions added or modified)
   - Test that demonstrates the change works
   - Reference to operator's existing implementation (e.g., paths in current main branch) so operator can compare
   - Any psyche-question that surfaced during the mockup
   - Quick recommendation: "operator integrate as-is" / "operator critique + redesign" / "operator pick the best bits and merge"

6. **Create a bead** via `bd q '<title>'` (quick capture, returns bead ID). Then `bd note <bead-id> -m '<details>'` with the worktree path + branch + report path. Bead title format: `[mockup] <slice-name> — <one-line summary>`. The bead ID gets included in the per-agent report so operator can find it.

## §5 Hard constraints (same as /327 frame, restated)

- **jj headless ONLY**: every `jj` description-taking command passes `-m '<msg>'` inline. NEVER let jj open an editor (the sub-agent harness cannot satisfy an editor prompt).
- **NOTA examples in reports** use bracket-string form per intent 401 (when generating new schemas) but quoted-string form when invoking the deployed Spirit CLI (which hasn't moved to bracket-strings yet).
- **No emojis. No `---` horizontal-rule lines.**
- **Full English identifiers**: `Identifier` not `Id`, `Request` not `Req`. AND names don't carry full ancestry: `Entry` (inside namespace) not `IntentEntry`.
- **No `/nix/store` filesystem search**; use `nix eval` / `nix flake show` / `nix path-info`.
- **Markers in code**: when landing a design from this report into another agent's worktree, inline `// DESIGN-DECISION-REVIEW (second-designer/172 §<N>)` markers at the code site so operator can find the design rationale.

## §6 Why mockups beat reports for this work (per intent 503)

Operator already landed /180 in their lane. If I write more design reports, operator either has to translate prose into code (lossy) or chooses not to (gap stays open). Mockups close the loop:

- Operator checks out the branch
- Runs the tests
- Sees the design as working code
- Compares to their existing implementation
- Either integrates the mockup as-is, picks the best bits, or critiques + supersedes

The mockup IS the design. The report explains why; the bead points there; the worktree carries it.

## §7 What this dispatch does NOT do

- Does NOT land changes on main (each mockup is on its own feature branch).
- Does NOT block operator (operator can still work on main; if operator has already landed the slice, sub-agent's report annotates "operator already did this — compare at <ref>").
- Does NOT introduce new psyche-level architecture (mockups implement existing intent + the /171 forward slices).
- Does NOT close any operator beads (operator owns bead state; mockup beads are advisory).

## §8 References

- `reports/second-designer/171-audit-second-operator-180-schema-v13-2026-05-24.md` — forward slices for A + B
- `reports/second-designer/170-schema-lowering-executor-model-2026-05-24.md` — lowering executor design (input to slice C)
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — current schema design
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — operator design critique
- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` — what slice A/B/C compare against
- `reports/designer/249-component-intent-gap-analysis.md` — SpawnEnvelope + SO_PEERCRED corpus (input to slice D)
- `reports/designer/299-design-origin-process-and-agent-identity.md` — SO_PEERCRED accept-time identity
- `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md` — IngressContext composition
- `reports/designer/307-design-golden-ratio-namespace-split.md` — SO_PEERCRED uid checks per message
- Intent records 388-506 (catalog evolution in /324 §2 + /174-v5 + this report's §1)

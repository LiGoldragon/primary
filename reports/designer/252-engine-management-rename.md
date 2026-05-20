# 252 — engine-management rename (implementation)

*Operator-facing change list for the supervisor → engine-manager rename
settled in `intent/persona.nota` 2026-05-20T14:30:00Z. Resolves /249
High-severity gap #2; replaces /251's "Path A vs Path B" question with
landed-direction Path B + full wire-vocabulary rename. This report is
the contract another agent picks up to implement.*

## 0 · TL;DR

The OS-level entity above spirit in the persona authority graph is now
canonically named **engine manager** (binary: `persona-daemon`). The
word "supervisor" leaves the workspace surface except as agent-internal
Kameo actor-tree convention inside individual components.

Three renames, propagated across repos:

| From | To | Where |
|---|---|---|
| "supervisor" (role text, ARCH prose, mermaid labels, report TL;DRs) | "engine manager" | persona-spirit/ARCH, /232, /251 historical reference text, any ARCH using "the supervisor" |
| `SupervisionOperation` / `SupervisionReply` / `SupervisionRequest` / `SupervisionRelation` / `SupervisionOperationKind` / `SupervisionUnimplemented` / `SupervisionProtocolVersion` etc. | `EngineManagementOperation` / `EngineManagementReply` / `EngineManagementRequest` / `EngineManagementRelation` / `EngineManagementOperationKind` / `EngineManagementUnimplemented` / `EngineManagementProtocolVersion` etc. | `signal-persona` contract crate and every consumer (every supervised daemon) |
| `EngineSupervisor` Kameo actor | `EngineManager` | `persona/src/supervisor.rs` (rename file → `engine_manager.rs`), persona/ARCH cross-references |

**Kept unchanged** (do not touch):

- Component-internal Kameo actor-tree supervisors: `StoreSupervisor`,
  `SubscriptionSupervisor` in `persona-mind`; any `*Supervisor` actor
  type scoped to a single component. Kameo parent-actor convention.
  Namespace (`mind::StoreSupervisor` etc.) makes the meaning
  unambiguous.
- `persona-terminal-supervisor` binary — separately phased out per
  /249 gap #32 (cell-vs-supervisor consolidation); not part of this
  arc.
- Psyche-verbatim quotes inside `intent/*.nota` — never edit verbatim
  quotes. Agent restatement lines already clarify the mapping.
- `skills/actor-systems.md` references to "supervisor" — that file
  is about the Kameo actor convention, where "supervisor" is the
  correct term.

## 1 · Per-repo scope

### 1.1 · `signal-persona` (wire vocabulary — the heavy lift)

Repo: `/git/github.com/LiGoldragon/signal-persona/`

**ARCHITECTURE.md** — rewrite §"Supervision relation" → §"Engine
management relation"; rename every type name; update the type-renames
table to record the new pattern; update §"Type renames (drop redundant
Engine* / Component* / Supervisor* prefixes)" — note that this rename
*adds* `EngineManagement` prefix on this specific relation, which is
the exception to the prefix-drop rule because it disambiguates from
the unrelated Kameo `*Supervisor` actor-tree convention. The /251
report explains the rationale; this is a deliberate carveout.

**Source crates** — every type listed in §1, §"Skeleton honesty," and
§"Type renames":

```text
SupervisionOperation         → EngineManagementOperation
SupervisionReply             → EngineManagementReply
SupervisionRequest           → EngineManagementRequest
SupervisionRelation          → EngineManagementRelation
SupervisionOperationKind     → EngineManagementOperationKind
SupervisionUnimplemented     → EngineManagementUnimplemented
SupervisionUnimplementedReason → EngineManagementUnimplementedReason
SupervisionProtocolVersion   → EngineManagementProtocolVersion
SupervisionReplyKind         → EngineManagementReplyKind
```

Module path: if there is a `supervision` module (e.g.,
`supervision::Query::ReadinessStatus`), rename to `engine_management::`
(snake_case Rust). The contract verb `Query::ReadinessStatus` etc.
stays — those are domain-action names, not the relation name.

**Tests** — rename every test referencing the old names. Examples
from `signal-persona/ARCH`:

```text
test-supervision-unimplemented-round-trip → test-engine-management-unimplemented-round-trip
```

Apply uniformly.

### 1.2 · `persona` (engine-manager binary + ARCH)

Repo: `/git/github.com/LiGoldragon/persona/`

**Source rename**:

```text
src/supervisor.rs → src/engine_manager.rs
struct/actor:  EngineSupervisor → EngineManager
```

Update all import sites (search `EngineSupervisor` across the crate).

Note on the name collision: the binary `persona-daemon` plays the
"engine manager" role; the central in-process Kameo actor that
implements that role is naturally also named `EngineManager`. This
is the same shape as a `Store` actor inside a daemon that owns
storage — the role and the actor share the name because the actor
IS the role's embodiment in process memory.

**ARCHITECTURE.md** edits:

- §0 prose: "supervisor" wherever it means the engine manager →
  "engine manager." (The file already mostly uses "engine manager";
  hunt for the remaining "supervisor" mentions in lines 26, 45, 602,
  608, 748, 793–794, 1122, 1128, 1242–1248.)
- Line 602 *"The supervisor's restart policy..."* → "The engine
  manager's restart policy..." (or restructure if the sentence is
  about the `EngineManager` actor specifically — read context).
- Line 608 *"data-bearing Kameo launcher/supervisor actor..."* →
  "data-bearing Kameo `EngineManager` actor..." (replace the
  hyphenated pair with the new actor name).
- Line 727 *"...`EngineSupervisor` actor, resolves..."* →
  "...`EngineManager` actor, resolves..."
- §1.7 (authority/permission section) — if any "supervisor"
  references remain, swap to "engine manager."
- §1.6.5 (federation), §1.5 (Engine Manager Model heading) — should
  already be consistent; verify.
- Manifest line 1497: *"src/supervisor.rs Kameo EngineSupervisor
  actor..."* → "src/engine_manager.rs Kameo EngineManager actor
  that launches prototype-managed processes." (Also change
  "prototype-supervised" → "prototype-managed" if you want full
  consistency. Optional.)
- Nix check names referencing "engine supervisor" (lines 1343–1348)
  rename to "engine launcher" or "engine manager" depending on what
  the check actually witnesses. Coordinate with operator on whether
  the check names are stable; flake check renames carry CI cost.

**`SupervisionOperation` consumers** — every place persona-daemon
imports the old signal-persona type names, update.

### 1.3 · `persona-spirit` (ARCH text + mermaid)

Repo: `/git/github.com/LiGoldragon/persona-spirit/`

**ARCHITECTURE.md** §"Role" (line 9): *"The supervisor has higher
infrastructure permission only for process lifecycle."* → *"The
engine manager has higher infrastructure permission only for process
lifecycle."*

**ARCHITECTURE.md** §"Role" (line 16): *"`owner-signal-persona-spirit`
— supervisor-only owner contract."* → *"`owner-signal-persona-spirit`
— engine-manager-only owner contract."*

**ARCHITECTURE.md** §"Authority" mermaid (lines 20–32):

```diff
- supervisor["persona supervisor"]
+ manager["persona engine manager"]
...
- supervisor --> spirit
+ manager --> spirit
```

(Node id `manager` is fine; or use `engine_manager`. Pick one and
apply consistently.)

**Code** — search for "supervisor" string references in comments or
docstrings; update.

### 1.4 · Other persona components (consumers)

Every supervised component imports `signal-persona`'s supervision
vocabulary and binds a supervision socket. The import rename and
binding-name updates propagate:

- `persona-mind/`
- `persona-router/`
- `persona-harness/`
- `persona-message/`
- `persona-orchestrate/`
- `persona-terminal/`
- `persona-system/`
- `persona-auth/`
- `persona-introspect/`

For each repo:

- ARCH text: replace "supervision socket" / "supervision relation"
  with "engine-management socket" / "engine-management relation" where
  they refer to the wire surface. Confirm none of these conflate with
  internal Kameo actor-supervisor talk.
- Source: rename `SupervisionOperation` etc. imports.
- DaemonConfiguration: any field named `supervision_socket_path` →
  `engine_management_socket_path` (and `supervision_socket_mode` →
  `engine_management_socket_mode`).
- Envelope variable names (Nix-passed env vars) named
  `*_SUPERVISION_SOCKET` → `*_ENGINE_MANAGEMENT_SOCKET`. **This is
  an ABI break for prototype topologies**; coordinate with the
  manifest pass to update Nix derivations atomically.
- Tests: rename "supervision" → "engine-management" in test names.

### 1.5 · Workspace docs + reports

**`/home/li/primary/reports/designer/232-persona-spirit-new-component.md`**

§0 TL;DR (line 18): *"The supervisor has higher permission only as
infrastructure"* → *"The engine manager has higher permission only as
infrastructure"*

Also §1 (line 41) verbatim psyche quote *"the apex, the most powerful
part, notwithstanding the supervisor"* — **DO NOT edit the verbatim
quote**. The surrounding agent text can clarify in a follow-up sentence
if needed.

**`/home/li/primary/reports/designer/251-supervisor-identity-disambiguation.md`**

Add a final note: "Resolved 2026-05-20T14:30:00Z — psyche chose Path B
+ full SupervisionOperation rename; implementation in /252." Then the
report retires once /252's edits land.

**`/home/li/primary/ESSENCE.md`**, **`/home/li/primary/INTENT.md`** —
verify no "supervisor" references that mean the engine manager. (Quick
grep; probably zero matches.)

**`skills/component-triad.md`** — verify the apex skill does not say
"supervisor" in a way that means the engine manager. (Quick grep.)

## 2 · Order of operations

This is a multi-repo rename. Order matters because contract types are
imported across the dependency graph.

1. **Land `signal-persona` rename first.** Without this, no consumer
   can compile against the new names.

   - Local change in `signal-persona`: type renames + ARCH text.
   - `cargo test` green locally.
   - Commit + push.

2. **Land `persona` (engine-manager binary) rename second.**
   `persona` imports `signal-persona` and is the producer of the
   wire surface for all child components.

   - Cargo.toml of `persona` points at the new `signal-persona`
     revision.
   - Rename `src/supervisor.rs` → `src/engine_manager.rs`,
     `EngineSupervisor` → `EngineManager`.
   - ARCH edits.
   - `cargo test` + `nix flake check` green.
   - Commit + push.

3. **Land each supervised component's signal-persona consumer
   update**, one repo at a time.

   - Bump `signal-persona` dep version.
   - Rename imports.
   - Rename DaemonConfiguration fields.
   - ARCH text edits.
   - `cargo test` + `nix flake check` green.
   - Commit + push.

   Order within step 3 does not matter — each component's
   consumer rename is independent of the others. Parallel-safe.

4. **Workspace docs + reports last.** /232 TL;DR, /251 closing note,
   skill files (verification only).

5. **`persona-spirit/ARCH` text + mermaid edits.** Independent of
   the wire rename (purely text); can land at any point in step
   3 or after.

## 3 · Verification (tests that should remain green)

The rename is structural / textual; behavior does not change. Every
test that was green before should remain green under the new names.
Specific witnesses to watch:

- `signal-persona`'s round-trip test under its new name
  (`test-engine-management-unimplemented-round-trip` or similar).
- Every persona component's "skeleton honesty" check — the daemon
  decodes every variant of `EngineManagementOperation` and returns
  `EngineManagementUnimplemented` for variants whose behavior is
  not built.
- Persona's flake checks listed in persona/ARCH §"Witnesses":
  - `persona-engine-supervisor-launches-...` checks → rename to
    `persona-engine-launcher-launches-...` (or
    `persona-engine-manager-launches-...`, choice of operator).
- Spirit daemon ordinary/owner socket boundary tests — text only;
  no rename needed in test names but verify any comments using
  "supervisor" referring to the engine manager.

## 4 · Out of scope (do not touch)

- **Kameo actor-tree internal supervisors**: `StoreSupervisor`,
  `SubscriptionSupervisor` (persona-mind), `StoreSupervisor`
  (persona-spirit's mention in /249 §1; verify naming inside
  persona-spirit — if it has any `*Supervisor` actors, those stay).
- **`persona-terminal-supervisor` binary**: separately phased out per
  /249 gap #32. Not this arc.
- **Psyche-verbatim quotes** inside `intent/*.nota`. Verbatim never
  changes.
- **Reports that referenced "supervisor" as historical context**
  (e.g., /249's gap analysis, /251's option presentation). Those are
  records of the disambiguation work; they should stay as written.
  Only /232 §0 TL;DR (agent restatement, not verbatim) and /251's
  closing note are in scope.
- **`signal-persona/ARCH` §"Type renames (drop redundant ...
  Supervisor* prefixes)"** — that table records the existing
  `Supervisor*` prefix-drop rename pass. The new rename ADDS
  `EngineManagement` prefix to specific wire types; that's a
  carveout, not a contradiction. Document the carveout in the
  table with a note.

## 5 · Risk notes

- **Multi-repo coordination**: nine consumer repos plus
  `signal-persona` plus `persona` plus docs. Use the
  `tools/orchestrate` claim flow to lock each repo while editing;
  avoid mid-stream operator races.
- **Nix env var rename**: `*_SUPERVISION_SOCKET` →
  `*_ENGINE_MANAGEMENT_SOCKET` is an ABI break for prototype
  topologies. Land the Nix derivation update atomically with the
  source update in each component.
- **Flake check renames**: persona/ARCH lists nix flake checks by
  name (e.g., `persona-engine-supervisor-launches-...`). Renaming
  these is optional but recommended for consistency. If renamed,
  any CI configuration that pins check names must be updated.
- **Search-and-replace traps**: the word "supervisor" appears in
  Kameo-convention contexts (`StoreSupervisor`,
  `SubscriptionSupervisor`) that **must not** be renamed. A naive
  global search-replace would damage those. Suggest:
  - `rg -l "Supervision"` first (uppercase, wire types).
  - `rg -l "supervision"` for socket/relation/path names (lowercase
    contexts in code + docs).
  - **Manual review** for plain "supervisor" / "supervisors" English
    word, since context disambiguates.

## 6 · References

- `intent/persona.nota` 2026-05-20T14:30:00Z — psyche Decision
  authorizing this rename.
- `/251` — disambiguation analysis and resolution paths.
- `/249` §"OS-level supervisor identity vs cognitive supervisor"
  + High-severity gap #2 — the gap that prompted this work.
- `/232` §0 + §1 — spirit's authority-graph context (TL;DR text
  to edit; verbatim quote to preserve).
- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` —
  wire vocabulary canonical home (heaviest edit target).
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` —
  engine-manager binary canonical home.
- `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md` —
  one of the spirits-of-vocabulary callout sites.
- `skills/actor-systems.md` — Kameo "supervisor" convention
  (preserved usage).

This report retires when:

- The `signal-persona` rename lands on `main`.
- Every consumer's import + Nix env-var rename lands on `main`.
- `/232`, `/251` closing-note edit, and persona-spirit/ARCH text
  edits land.
- A successor report or commit message confirms the rename
  completed.

*Kind: Triage · Topic: schema-engine-upgrade-marking-sweep · Slice: B · Date: 2026-05-24*

# 327 · Slice B triage — adjacent persona triads + agent

Subagent B's slice of the four-way schema-engine marking sweep. The frame at `/home/li/primary/reports/designer/327-schema-engine-upgrade-marking-sweep/0-frame-and-method.md` §6.2 names the in-scope repos: the terminal triad (plus terminal-cell subsystem), the harness triad, the introspect triad, the system triad, the engine-management contract, and the agent contract.

## §1 Method

Per the frame `§3.1` template (component-triad marking format), each in-scope repo received ONE new section titled "Pending schema-engine upgrade" placed near the end of `ARCHITECTURE.md` (before "See Also" / "See also" if present, after the final body section otherwise). Each section carries:

- **Status:** scheduled-for-migration line citing `/326-v13` + `/324`.
- **Target:** the per-repo `<component>.schema` file the brilliant macro library (`primary-ezqx.1`) will consume, plus the runtime concerns that move to the generated forms.
- **Sequence:** Spirit-pilot-first ordering, with per-repo coordination notes (triad cutover lands together; cross-triad dependencies — harness-agent, signal-introspect peer wraps — flagged).
- **Per-component concerns:** the frame-supplied specifics, expanded with concrete substrate detail from the existing ARCH (e.g. the terminal-cell subsystem boundary, the harness sema-bridge, the system paused-state, the agent R10 rename).
- **References:** the four canonical reports (326-v13, 324, 322, operator/174).

No other content in any ARCH was touched. No INTENT.md edits because no Slice B repo has an `INTENT.md` today. No code, no Cargo.toml, no README.md edits.

## §2 Per-repo edits

### §2.1 Edit inventory

Table of the 11 in-scope repos, the section placement, the per-component concern note carried into the schema-engine upgrade section, and the resulting jj change id (working-copy revision; not pushed):

| Repo | ARCH end pre-edit | Section placed | Per-component concern carried | jj change id |
|---|---|---|---|---|
| `terminal` | `## See Also` | before See Also | ANSI handling + terminal-cell subsystem interface preserved | `kkvlvnnq` |
| `signal-terminal` | `## See also` | before See also | Four contract-local verb groups + mandatory `Tap`/`Untap` block become schema declarations | `wotxomlk` |
| `terminal-cell` | `## Code Map` | at end | Subsystem under terminal triad; only typed control surface migrates; raw byte plane stays out | `vuvtrrku` |
| `harness` | `## See Also` | before See Also | Agent-process harness; sema-bridge interacts with /309; coordinates with R10 rename | `rzsruuzr` |
| `signal-harness` | `## See also` | before See also | Recipient→harness→terminal name-equality resolution carries forward | `nwkokopy` |
| `introspect` | `## 5. Status` | at end as `## 6.` | Observer subscribes to `AssembledSchema` for cross-component dispatch lookup | `zlltzkyn` |
| `signal-introspect` | `## See also` | before See also | `DeliveryTraceKey` four-field correlation + `Option<>`-wrapper "not yet observed" axis | `luxnnsyx` |
| `system` | `## See Also` | before See Also | Paused-state skeleton — schema cutover can land before unpause | `vzzrzqsw` |
| `signal-system` | `## See also` | before See also | `SystemTarget` hand-written NOTA codec quirk needs accommodation in schema enum rules | `tnsqvxkz` |
| `signal-engine-management` | `## See Also` | before See Also | No standalone daemon; no `Tap`/`Untap`; coordinated cutover with `signal-upgrade` | `yrqrrsox` |
| `signal-agent` | `## See also` | before See also | Daemon not yet built; R10 rename precedes schema cutover; cross-triad with harness | `mkzpsqks` |

All 11 commits described inline via `jj describe -m`. Working-copy revisions only — not pushed (per slice contract `Do NOT push to remotes`).

### §2.2 Per-component concern verbatim — the slice-B substance

The "Per-component concerns" field is the load-bearing per-repo content the orchestrator + downstream operators read to understand each repo's cutover shape. Captured here so the synthesis pass at file 5 can read slice B's substantive notes without opening 11 ARCH files. Each entry quotes the populated concern as it sits in the marking section:

**terminal (daemon).** "Per-session ANSI handling; schema cutover preserves the terminal-cell subsystem interface — the `control.sock` Signal endpoint between `terminal-daemon` and the embedded `terminal_cell` library stays a hand-written boundary while the daemon's outward-facing `signal-terminal` traffic moves to schema-generated forms. The two-socket (communication / supervision) discipline and the data-plane raw-bytes path remain outside the schema (they are not Signal frames)."

**signal-terminal (contract).** "Per-session ANSI handling lives in the daemon, not this contract; schema cutover preserves the terminal-cell subsystem interface as out-of-schema (the daemon's `control.sock` to embedded cells stays hand-written). The mandatory observability `Tap`/`Untap` block + the four contract-local verb groups (transport, session discovery, prompt-pattern registry, input-gate / injection, worker-lifecycle subscription) become explicit `.schema` declarations."

**terminal-cell (subsystem).** "Subsystem behind the terminal triad — production Persona consumes `terminal-cell` as a library inside `terminal-daemon`. The schema cutover concerns only the typed-control surface; the latency-sensitive raw byte plane and the bounded transcript-scriber queue are out of scope for the schema language."

**harness (daemon).** "Agent-process harness; sema-bridge interacts with the agent triad (per /309); schema cutover coordinates with the R10 agent rename so the harness `.schema` file references the post-rename agent vocabulary directly. Skeleton-honesty (`HarnessRequestUnimplemented`) and the closed `HarnessKind` four-variant enum carry over as declared schema enums."

**signal-harness (contract).** "Agent-process harness contract; sema-bridge interacts with the agent triad (per /309); schema cutover coordinates with the R10 agent rename. The recipient → harness → terminal name-equality resolution rule (one role per name in prototype one) carries forward as a schema-declared constraint or stays daemon-side."

**introspect (daemon).** "Cross-component observation collector; schema cutover lets observer subscribe to `AssembledSchema` for cross-component dispatch lookup. The schema-engine target supports introspect's role as the canonical consumer of every persona daemon's standardized `Tap`/`Untap` observer hook — the assembled schema gives introspect a single typed view across components without per-peer ad-hoc client wiring."

**signal-introspect (contract).** "Cross-component observation collector contract; schema cutover lets the daemon subscribe to `AssembledSchema` for cross-component dispatch lookup. The `DeliveryTraceKey` four-field correlation shape (engine, message identifier, originator, hop index) and the `Option<>`-wrapper 'not yet observed' axis carry forward as schema-declared closed enums plus carrier records."

**system (daemon).** "OS-level operations; per-component schema cutover. The paused-state skeleton (daemon binds the socket and answers `SupervisionRequest` and `SystemStatusQuery`; domain operations return `SystemRequestUnimplemented`) carries through the cutover. Backend-specific Niri adapter code stays out of the schema; only the typed contract surface migrates."

**signal-system (contract).** "OS-level operations contract; per-component schema cutover. The Path A subscription close discipline (request-side `Retract FocusSubscriptionRetraction(FocusSubscriptionToken)` + reply-side `SubscriptionRetracted` ack) becomes a schema-declared subscription pattern. `SystemTarget`'s hand-written NOTA codec quirk may need an out-of-band marker in the schema."

**signal-engine-management (contract).** "Persona's manager messages; per-component schema cutover; interacts with the upgrade triad. No standalone daemon — this is a pure contract crate consumed by every supervised daemon and the engine manager. No mandatory `Tap`/`Untap` (the channel intentionally has no observability stream because the manager already owns this infrastructure traffic). Skeleton-honesty (`Reply::Unimplemented`) carries forward as a schema-declared default reply."

**signal-agent (contract).** "Per /309 agent component abstraction; R10 rename open question; schema cutover after the agent name is ratified. No daemon repo yet (`agent` runtime is the destination; today only `signal-agent` and `owner-signal-agent` exist) — the daemon's schema-engine integration lands with the runtime. Imports `IngressContext` and `ConnectionClass` from `signal-persona-origin` plus message records from `signal-message`; the assembled-schema model lets those imports stay declarative across the agent + persona-origin + message schemas."

## §3 Cross-cutting observations

### §3.1 Slice-B contract repos all carry the three-layer migration "MUST IMPLEMENT" section

Every `signal-*` contract in this slice (signal-terminal, signal-harness, signal-introspect, signal-system) already has a `## MUST IMPLEMENT — three-layer migration` section pointing at `/246-v4` + `/248`. The schema-engine upgrade section explicitly notes the relationship: "the three-layer migration outlined in the 'MUST IMPLEMENT' section above is the immediate-term shape; the schema cutover supersedes it once the macro library lands the contract-local verbs declaratively." This means future operators reading these ARCHs see two waves marked — three-layer first, then schema-engine — without the schema-engine marking implicitly cancelling the three-layer marking.

The two daemon ARCHs (`terminal`, `harness`, `introspect`, `system`) do NOT carry the three-layer "MUST IMPLEMENT" section — the three-layer model is contract-side discipline, so the daemon ARCHs just describe the post-migration target without an explicit migration banner. The schema-engine sections on daemon ARCHs therefore name only the schema target without referencing three-layer.

`signal-engine-management` and `signal-agent` do not have the three-layer "MUST IMPLEMENT" banner: signal-engine-management is intentionally outside the standard pattern (no `Tap`/`Untap`, manager-only relation), and signal-agent was written post-three-layer-decision so it bakes the discipline in directly.

### §3.2 Triad asymmetries — which legs are present

The slice-B inventory shows non-uniform triad shapes:

- **terminal triad:** daemon (`terminal`) + ordinary contract (`signal-terminal`) + owner contract (`owner-signal-terminal`) + subsystem (`terminal-cell`). The owner contract is real but not in this slice's scope; the subsystem is in scope.
- **harness triad:** daemon (`harness`) + ordinary contract (`signal-harness`). No `owner-signal-harness` repo exists today.
- **introspect triad:** daemon (`introspect`) + ordinary contract (`signal-introspect`). No owner contract; introspect is observation-only and has no owner-only command surface today.
- **system triad:** daemon (`system`) + ordinary contract (`signal-system`). No owner contract; the privileged-action surface (`ForceFocus` / `SuppressDrift`) is named in design but no `owner-signal-system` repo exists. System is paused; the owner contract lands with the privileged-action surface when a real consumer concretizes the requirement.
- **engine-management "triad":** contract only (`signal-engine-management`). No daemon — this is a pure relation contract carried by every supervised daemon and the engine manager. No owner pair either: privileged engine-manager commands live in `owner-signal-persona`, not `owner-signal-engine-management`. The schema-engine upgrade section treats this as a single contract repo.
- **agent "triad":** ordinary contract (`signal-agent`) + owner contract (`owner-signal-agent`). No daemon yet — the daemon lands with the R10-renamed runtime. The schema-engine upgrade section on signal-agent notes the daemon's schema integration lands with the runtime, and the cutover waits on R10 ratification.

The owner contracts in scope (`owner-signal-terminal`, `owner-signal-agent`) are not part of slice B — they belong to a future sweep that should mark owner contracts uniformly, or they can be folded into the corresponding triad legs.

### §3.3 Subsystem repo handling

`terminal-cell` is the only repo in slice B that is explicitly a subsystem under a triad rather than a triad leg. Its ARCH already names the relationship clearly ("Production Persona consumes `terminal-cell` as a library inside the consolidated `terminal-daemon`") and the schema-engine section preserves that framing: only the typed-control surface (`signal-terminal`-shaped traffic on `control.sock`) migrates to the schema; the raw byte plane, the latency-sensitive worker plumbing, the input-gate primitive, and the bounded transcript-scriber queue stay hand-written.

This is the cleanest example in the slice of "schema cutover preserves an existing subsystem interface" — the daemon's outward-facing `signal-terminal` traffic moves to schema-generated forms while the daemon-to-subsystem `control.sock` boundary stays hand-written.

### §3.4 The `signal-engine-management` exception — no `Tap`/`Untap`

Every other in-scope `signal-*` contract carries (or is being moved to carry) the mandatory `Tap`/`Untap` observability block per the three-layer model. `signal-engine-management` intentionally does NOT, per its own invariant: "This channel has no observability stream; the manager already owns this infrastructure traffic." The schema-engine upgrade section preserves this exception explicitly — the schema-declared verbs are exactly the four prototype operations (`Announce`, `Query(ReadinessStatus)`, `Query(HealthStatus)`, `Stop`) without a mandatory observability injection.

This raises a small open question: does the schema language let a contract opt-out of mandatory observability? If the macro library treats `Tap`/`Untap` as universal, signal-engine-management needs an explicit declaration or its `.schema` file becomes a special case in the codegen. Carried as a noteworthy item for the integrator rather than a blocker.

### §3.5 Cross-triad dependencies

Three cross-triad dependencies surfaced and were flagged in the per-component concerns:

- **harness ↔ agent (R10 rename):** harness's sema-bridge interacts with the agent triad per /309; both signal-harness and signal-agent's schema-engine sections coordinate cutover with the R10 rename so the post-rename names land in the schema in one step. Without coordination, the schema bakes in pre-rename names that then need a separate cutover.
- **introspect ↔ every peer:** introspect's daemon section notes that per-peer client cutover (`RouterClient`, `ManagerClient`, `TerminalClient`) coordinates with each peer triad's own schema cutover so the per-peer `Tap` subscriptions speak the post-cutover schema vocabulary. The assembled-schema model lets introspect subscribe to `AssembledSchema` for cross-component dispatch lookup rather than per-peer ad-hoc client wiring.
- **signal-engine-management ↔ signal-upgrade:** the engine-management contract notes coordinated cutover with `signal-upgrade` ensures the lifecycle vocabulary and the upgrade vocabulary stay schema-consistent. Slice C owns the upgrade triad.

These dependencies do not block individual repo markings — the marking is a future-direction signal, not the cutover itself — but they will matter when operator beads land for the actual cutovers.

### §3.6 ARCH-structure variation across the slice

Slice B repos showed three ARCH end-shape patterns:

- **End with `## See Also` / `## See also`:** terminal, signal-terminal, harness, signal-harness, signal-introspect, system, signal-system, signal-engine-management, signal-agent (9 of 11). Marking section placed before See Also.
- **End with `## Code Map` then no See Also:** terminal-cell (1 of 11). Marking section placed at end (after Code Map).
- **End with `## N. Status` then no See Also:** introspect (1 of 11). Marking section placed at end as `## 6. Pending schema-engine upgrade` (matching the numbered-section style introspect already uses).

The introspect numbering style (`## 0. Intent`, `## 1. Owned surface`, …) is unique in the slice; every other repo uses `## 0 · TL;DR`, `## 1 · …` (middle-dot separator). Slice B preserves each repo's local style — the marking section reads naturally inside its host doc.

### §3.7 No missing ARCH files

Every in-scope Slice B repo has an existing `ARCHITECTURE.md`. The "If a repo doesn't have ARCHITECTURE.md, CREATE a minimal one" branch of the frame's hard constraints did not fire for this slice. Slice C / Slice D may hit it; Slice B did not.

### §3.8 Storage-descriptor surface varies sharply across the slice

The schema cutover replaces "hand-written `signal_channel!` + Layer 2 Command/Effect + storage types" with a single `.schema` file. The storage portion varies sharply across Slice B repos and matters for how the macro library's storage-descriptor generator integrates:

- **terminal — heavy storage.** Component Sema tables for `delivery_attempts`, `terminal_events`, `viewer_attachments`, `session_health`, and `session_archive`, plus the named-terminal-session registry with typed `control_socket_path` / `data_socket_path` fields. The terminal `TerminalTables` redb file is the canonical example of "lots of typed storage that needs schema-declared descriptors."
- **harness — selective storage.** The harness actor opens its own `harness.redb` for durable harness history through a harness-owned Sema layer, but the wire-contract side (lifecycle FSM, transcript subscription, kind enum) doesn't all need durability. Schema cutover scopes storage to the records that actually persist.
- **introspect — schema-shaped store.** `introspect.redb` is fully typed: query/reply audit trail (landed), subscription registrations, delivery trace cache keyed by `DeliveryTraceKey` (landed), all persisted as typed records through `sema-engine`. This repo is the cleanest match for "storage descriptors emitted by the macro library" because the store is already typed records all the way down.
- **system — no durable storage today.** "Durable consumer history is not owned here." The schema cutover for system declares zero storage descriptors today; if system later needs durable subscription registrations / backend cursors, those land as schema additions.
- **signal-engine-management — no storage.** Pure relation contract. The schema declares verbs and reply enums, no storage descriptors.
- **signal-agent — no storage in contract.** The contract owns vocabulary only; storage lives in the future `agent` daemon. Schema cutover for signal-agent is contract-only; the daemon's storage descriptors land with the runtime.

This means the macro library's storage-descriptor pipeline has to gracefully handle the zero-descriptors case (signal-engine-management, signal-system today, signal-agent contract) without forcing a fake storage section. Not a slice-B issue per se — flagged for the macro library implementor.

### §3.9 Per-repo schema file naming

Each marking section names the destination `.schema` file. Within a triad, daemon and ordinary contract reference the SAME `.schema` file (the contract owns the wire vocabulary; the daemon's generated dispatcher derives from the same source). Capture for the synthesis pass:

| Repo | Schema file in marking section |
|---|---|
| `terminal` | `terminal/terminal.schema` |
| `signal-terminal` | `signal-terminal/terminal.schema` (shared with daemon) |
| `terminal-cell` | `terminal/terminal.schema` (consumes parent triad's schema for typed control surface) |
| `harness` | `harness/harness.schema` |
| `signal-harness` | `signal-harness/harness.schema` (shared with daemon) |
| `introspect` | `introspect/introspect.schema` |
| `signal-introspect` | `signal-introspect/introspect.schema` (shared with daemon) |
| `system` | `system/system.schema` |
| `signal-system` | `signal-system/system.schema` (shared with daemon) |
| `signal-engine-management` | `signal-engine-management/engine-management.schema` |
| `signal-agent` | `signal-agent/agent.schema` (post-R10-rename name) |

Convention: schema file name uses the component name (not the contract name), so the contract and the daemon both reference `<component>.schema` even though their repos differ (`signal-<component>` vs `<component>`). signal-engine-management uses `engine-management.schema` because the component name has no daemon repo to match. signal-agent uses the post-R10-rename name explicitly so the schema cutover lands with the renamed vocabulary.

Open question for the macro library: does the schema source live in the daemon repo (canonical) and get referenced by the contract repo (via path or vendored copy), or is the source-of-truth split with both repos shipping the same `.schema` file under their own paths? Not a Slice B blocker — flagged for the implementor.

### §3.10 Cross-triad dependency map

A compact view of the cross-triad dependencies that surfaced (text form, not a diagram — the relationships are too sparse to merit mermaid):

```text
harness ──── (R10 rename) ────── signal-agent / agent runtime
   │
   └─ (sema-bridge interaction per /309)

introspect ── (per-peer Tap subscriptions) ── every slice-A/B/C peer triad
   │
   └─ (AssembledSchema cross-component dispatch lookup)

signal-engine-management ── (lifecycle ↔ upgrade) ── signal-upgrade (slice C)
   │
   └─ (coordinated cutover keeps lifecycle + upgrade vocabularies consistent)

terminal-cell ── (subsystem under) ── terminal triad
   │
   └─ (control.sock typed surface migrates; raw byte plane stays out)
```

Each arrow is a coordination concern, not a hard dependency — the marking can land independently per repo; the cutovers need to talk to each other when they happen.

## §4 Deferrals + blockers

None. All 11 in-scope repos took the marking cleanly. No file conflicts, no jj editor prompts (every commit message landed inline), no missing repos, no missing ARCH files.

The only soft open question is §3.4 above — whether `signal-engine-management`'s no-observability exception needs an explicit `.schema` opt-out marker. That is forward-looking for the macro library implementor, not a blocker for the marking sweep.

## §5 What carries forward — operator-actionable items

These items follow the marking sweep:

1. **R10 rename ratification.** Before the agent triad's schema cutover, the R10 rename per `reports/designer/310-meta-overhaul-booking-roadmap.md` needs to settle. The signal-agent ARCH section explicitly waits on this. The harness ARCH section coordinates with the same rename.
2. **Spirit pilot success.** Every Slice B repo's schema-engine sequence note depends on the Spirit pilot landing first via `primary-ezqx.1`. Per the frame, "this component follows after pilot succeeds and per-component schema cutover beads land per-triad." Operator-side per-triad cutover beads are the destination after the marking sweep.
3. **Triad cutover coordination.** For each daemon + contract pair (terminal triad, harness triad, introspect triad, system triad), the schema cutover lands together so the daemon's generated dispatcher and the contract's wire types stay in lockstep. Operator beads should be triad-scoped, not per-repo-scoped.
4. **Three-layer migration vs schema cutover ordering.** Slice B's four `signal-*` contracts already have a three-layer migration in flight. The schema-engine cutover supersedes it. Operators landing the schema cutover should NOT first finish the three-layer migration separately and then re-do the same work as a schema migration — the schema language makes the three-layer model declarative and lands both steps in one cutover.
5. **System unpause coordination.** The `system` daemon is paused. The schema cutover can land before unpause without forcing the privileged-action surface to be designed first. When system unpauses with a real consumer, the privileged-action surface (`SystemPrivilegedRequest`, the renamed-`ForceFocus`, `SuppressDrift`) lands as schema additions to the same `system.schema` file.
6. **Owner-contract sweep.** Owner contracts (`owner-signal-terminal`, `owner-signal-agent`) are out of Slice B scope. A future sweep should mark owner contracts uniformly, since they participate in the same schema-engine cutover as their ordinary-contract siblings.

## §6 Slice B summary

Slice B summary: 11 edits + 0 creations + 0 blockers.

All 11 in-scope repos received the schema-engine upgrade section per frame §3.1, committed inline via `jj describe -m '<component>: mark pending schema-engine upgrade per /326-v13 + /324'`, no remote push, no INTENT.md edits (none exist in slice B repos today), no other content changes.

## See also

- `reports/designer/327-schema-engine-upgrade-marking-sweep/0-frame-and-method.md` — frame, method, hard constraints, four-subagent dispatch
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — uniform header form + schema-language design
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — migration MVP + handover state
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — Spirit MVP worked example
- `reports/operator/174-schema-import-header-design-critique-2026-05-24.md` — header/body/feature separation + lowering rules
- `reports/designer/309-design-agent-component-abstraction.md` — agent component abstraction (carried as R10 rename open question)
- `reports/designer/310-meta-overhaul-booking-roadmap.md` — Wave 3 booking + R10 rename context

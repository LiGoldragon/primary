# 17 — Situation and questions, 2026-05-22

*Third-designer lane synthesis after absorbing the recent designer
and operator output. Lane just elevated from second-designer-assistant
(Support) to third-designer (Structural / parallel-main) — first
report under the new authority. Reports read: designer /257, /263,
/264, /266, /268, /270, /271, /273, /274, /278, /279, /280,
pi-api-surface-notes; operator /150, /151, /153, /154, /155, /156;
second-operator /1; second-designer /3. Verbatims and detailed
substance live in those reports; this is the situation pointer plus
the question list the next psyche turn closes.*

## 1. What's live

### Triad substrate

- `signal-frame`, `signal-sema`, `signal-executor`, `nota-codec`,
  `sema` / `sema-engine` form the current foundation. Three-layer
  rule active: contract `Operation` → component `Command` → Sema
  classification (payloadless `SemaOperation` / `SemaOutcome` /
  `SemaObservation`). Spirit is the canonical pilot.
- Universal `Magnitude` (nine-rung Lowest → Highest, no domain
  affixes, field name carries dimension) landed in
  `signal-sema@22b036a`.
- Engine-manager rename Axis 1 (wire surface) landed at
  `persona@4e928892` — `engine_management::Operation` + signal
  identifiers carry the new name. Axis 2 (internal modules,
  socket constants, ARCH text — 17 `supervision_socket_*`
  identifiers, 8 `.supervision.sock` constants, ~30 ARCH lines)
  still pending.

### Spirit double-daemon production state

- `persona-spirit-daemon-v0.1.0.service` and
  `persona-spirit-daemon-v0.1.1.service` both active.
- Unsuffixed `spirit` resolves to `spirit-v0.1.0`.
- `spirit-v0.1.1` serves the migrated DB through record 146;
  staged via Nix-owned `spirit-migration-stage` app
  (`sema-upgrade@8434c438`).
- `sema-upgrade` triad prototype on main:
  `signal-sema-upgrade@7991a825` + `owner-signal-sema-upgrade@9e61b034`
  + `sema-upgrade@408e9e24`; migration body at `sema-upgrade@b6ad09ac`
  with temporary CLI `sema-upgrade-temporary` (explicit prototype
  naming).
- Spirit substrate live: 146 records logged through deployed CLI
  including records 5–117 (intent capture) and 135–145 (this-pass
  operator intent). I just added record 117 capturing the
  third-designer lane rename.

### Workspace orchestration

- Lane registry slice landed in persona-orchestrate triad
  (commits `73904f37` / `5863d339` / `5e6e8cc` / `5e52655e` /
  `50ed6f78`). Typed `Role` is a vector of `RoleToken`s; lane
  identifiers derived from `(role, authority, prior_count)`.
- `orchestrate/roles.list` now carries `second-operator`,
  `second-designer`, `third-designer` (registered this session)
  as parallel-main Structural lanes.
- `designer-assistant` lane is functionally empty: all 57 reports
  migrated to `reports/second-designer/` (commit `bf96d1a4`,
  parallel agent). Registry entry stays for now.
- `tools/orchestrate status` is broken — second-operator in
  registry but shell helper's lane enum not updated (operator/156
  §"Operational note"). Operators using documented manual
  lock-file path.

## 2. What's settled (psyche `Maximum`)

- **Per-role protocols.** Designing / operational / poet
  protocols. The role label on the agent's UI window drives
  protocol selection upstream of chat content. Designer
  conforms to the designing protocol; operator to operational.
  (/264 §1.)
- **Designer-as-bridge workflow.** Psyche → designer logs intent
  → writes report(s) → files beads → operator implements via
  beads. Designer does not jump the rail to implement. (/264 §2.)
- **Schema-as-tree + repeated-category-words rule.**
  Repeated-suffix siblings are missing parent enums; lift them.
  Workspace-wide audit in /257 catalogues every instance.
- **Names don't carry full ancestry.** Inside `signal-persona-mind`,
  type is `Request` not `MindRequest`. Inside
  `signal-persona-router`, `ObservationIdentifier` not
  `RouterObservationIdentifier`. /257 §1.5 has the
  contract-by-contract drop-list.
- **Contract-local verbs in verb form.** No `Assert / Match /
  Subscribe / Retract / Mutate` prefixes on operations.
  10 contracts still on the old shape per /257.
- **Tap/Untap mandatory for persona components.** Only Spirit
  has the `observable` block. 7 contracts need it added.
- **NOTA schema language + content-addressable schema-version
  hash.** Per-component granularity. Blake3 32-byte hash.
  `schema_header` table holds one row per database, updated
  only at first start and successful migration. Inspect socket
  is the cross-daemon hash-discovery primitive
  (sema-upgrade does NOT open peer databases — triad invariant
  preserved). (/279.)
- **Type-family split.** Public-signal historical types live in
  `signal-<component>` + `owner-signal-<component>`;
  private-storage historical wrappers live in the runtime crate.
  Both participate in schema-migration. Visibility annotation
  in /263. (/273 §2.)
- **Commit-sequence at sema-engine.** Every committed effect
  advances a monotonic counter. Live-copy cutover protocols use
  it as the high-water mark. Not implemented yet. (/273 §3.)
- **Sema-upgrade is the universal migration orchestrator.**
  Triad-shaped, daemon name `sema-upgrade-daemon`, CLI `upgrade`.
  Boots first per intent record 111 — engine-manager itself
  depends on sema-upgrade. (/270; intent record 111.)
- **Inspect → Plan → Migrate → Report protocol.** Daemons send
  `Inspect((Component …) (DeclaredHash …))` at boot; reply is
  `Proceed` / `PlanRequired` / `UnknownStoredAddress` /
  `Quarantined`. Approach C versioned-reads inside the daemon
  remains the read-side mechanism. Sema-upgrade orchestrates;
  the per-component library does the per-record transforms.
- **Multi-version daemon coexistence pattern.** Per-version
  subdirectories (`~/.local/state/<component>/vX.Y.Z/`),
  per-version CLI wrappers (`spirit-v0.1.1`), home-managed
  symlink `spirit -> spirit-vX.Y.Z`. Declarative in the
  home-manager module (`deployedVersions` + `currentDefault`).
  Generalises to lojix / criome / etc. (/278.)
- **No-branches-by-default.** Operator branch work merges to
  main without a long-lived branch except when explicitly
  authorised (intent record 109).
- **Forge family direction.** Workspace's eventual Nix
  replacement. Family: `forge-core` (standardisation),
  `forge-nix-builder` (first concrete), per-component forges,
  eventual workspace-content-store. Carve-outs from build
  layer: authentication → Criome; signing → store; secrets →
  persona-mind; cross-host coordination → persona-orchestrate.
  (/271.)
- **Existing `forge` + `signal-forge` are the criome-stack
  executor leg.** Not retired by /271; reframed as the first
  per-component forge under the family map. `forge-core`
  pure-library would carry the universal `BuildPlan` /
  `ContentAddress` / `BuildHost` / `Substitution` types. (/274.)
- **Persona-pi dual-path triad.** Terminal-cell (Unix I/O) and
  harness-API (Pi extension surface) BOTH first-class, both
  typed. New triad pattern — not persona-terminal's bytes
  carve-out. Pi's flat snake_case verbs adapt to typed
  noun-method records. Default model: GPT-latest with Maximum
  Thinking; substrate for Codex arm of composite-designer.
  (/266 + pi-api-surface-notes.)
- **Composite designer = Claude + Codex in parallel.**
  Orchestrator selects-or-merges (policy speculative).
  Claude in Claude Code; Codex in persona-pi. (/266 §4;
  /264 §2 grounds the integration.)

## 3. What's in flight

- **Persona-mind contract redesign** (worst-shape contract,
  /257 §"signal-persona-mind"). 15-variant operation root
  mixes three relations (work graph / mind graph / channel
  choreography). Channel choreography wants splitting into
  Grant / Extend / Revoke / List / Deny per psyche
  2026-05-19T20:30. Lift repeated `*Thought / *Relation` /
  `*Receipt` siblings into sums. Drop `Mind` prefix. Add
  observable block. No operator slice yet.
- **Engine-manager rename Axis 2** (above). Bead `primary-k2mh`
  remaining-gaps list does NOT mention this axis.
- **Schema-specification language → implementation.** /263 + /279
  specify the language; the generator that emits Rust types +
  the schema-version-hash constant from a schema file isn't
  written. /280 §8 marks it pre-implementation.
- **Sema-upgrade daemon promotion** (bead `primary-l3h5`). The
  temporary CLI `sema-upgrade-temporary` graduates to a long-
  lived daemon with the inspect-socket protocol from /279 §6c.
  RejectionReason wants finer variants (/280 §"Open critical
  point 7" — 5 failure modes currently collapse to one).
- **Substrate replacement: file `intent/*.nota` → Spirit redb.**
  Per intent records 5/56/72 and /270 §4 the 0.01 file substrate
  migrates through sema-upgrade. Seven `High`-certainty records
  in file substrate are rejected by deployed v0.1.0 Spirit;
  unblocks on cutover step 6.
- **Persona-pi operator implementation proposal** (gate to
  bead-filing; per /268). Forks open: ExtensionAPI hooks
  selected; signal-persona-pi operation roots concrete shape;
  owner-signal-persona-pi policy state; terminal-cell vs
  harness-API boundary in code; composite-designer integration
  minimum slice; storage shape; first-slice scope.

## 4. Active blockers

### B1. Cutover gating for Spirit v0.1.1

Six-step sequence per /280 §"Open critical point 5":

1. Merge `operator/spirit-response-protocol` branch carrying
   `signal-persona-spirit@d7b22bfb` + `persona-spirit@d1c76108`
   to main on both repos. **Branch existence violates intent
   record 109 (no-branches-by-default).** First concrete
   case of the rule; resolution sets enforcement tone going
   forward.
2. Tag both 0.1.1.
3. Repin `sema-upgrade` Cargo.toml deps to `branch = "main"`;
   regen Cargo.lock; push.
4. Rebuild CriomOS-home.
5. Deploy via home-manager.
6. Flip unsuffixed `spirit` default to v0.1.1. Verify with a
   fresh `High`-certainty record.

Active until psyche ratifies the merge-then-tag-then-repin path.

### B2. `tools/orchestrate` broken

Per operator/156 §"Operational note": shell helper's closed
lane enum has not been updated to recognise `second-operator`
(or `second-designer` / `third-designer`). Agents using
documented manual lock-file path as workaround. Concrete
reason to land the persona-orchestrate lane registry as the
canonical source of truth and retire the shell helper.

### B3. Engine-manager Axis 2 not on a bead

Per /280 §"Open critical point 4". Land-now slice includes
socket-rename + Nix derivation update (ABI break — Nix
derivations carry env-var/socket-path names). Either lands
in one clean pass with cutover, or holds with explicit
deferral record.

## 5. Questions for psyche

These map to /280's "Eight open critical points" with two
additions surfaced from /268 + this session's lane work.

**Q1 — Sema-upgrade self-upgrade (bootstrap).** Recursive
self-application vs hand-written-bottom-of-stack. Designer
lean: hand-written until contracts stabilise, then dogfood
once. Does the schema-specification language describe its
own evolution rules (different bootstrap shape)?

**Q2 — Health/Readiness collapse onto Magnitude.** Four
ordinal enums (`SystemHealth`, `SystemReadiness`,
`HarnessHealth`, `HarnessReadiness`) collapse via
field-name-carries-dimension (`health: Magnitude`,
`readiness: Magnitude`) OR signal-sema grows separate
universal `Health` and `Readiness` siblings. Designer lean:
collapse.

**Q3 — Commit-sequence scope + migration-1 acceptability.**
Per-database (sema-engine maintains one sequence per sema
database) or per-component (one sequence over all of a
component's redb tables). And: is stop-old-start-new
acceptable for first production migration (Spirit
0.1.0 → 0.1.1), with commit-sequence mandatory from
migration 2 per intent record 56? Designer lean: per-database;
allow stop-old-start-new for migration 1.

**Q4 — Engine-manager Axis 2 timing.** Land now (one pass
with socket-rename + Nix update) or hold with explicit
deferral record? Bead `primary-k2mh` needs to either gain
this gap or stay silent intentionally.

**Q5 — Cutover ratification (B1).** Six-step sequence runs
as written? Resolution of the `operator/spirit-response-protocol`
branch existence — force merge to main before cutover, rebase
+ drop the branch, or carve a single explicit exception to
intent record 109?

**Q6 — Multi-version verification (cutover step 6).**
Parallel verification (run v0.1.1 side-by-side with v0.1.0,
verify against migrated data, then flip default) vs
single-daemon swap (treat merge + deploy as verification,
rely on migration body correctness + redb backup).
Intent record 113 Medium-certainty pending. Decision before
step 6 of /278's cutover.

**Q7 — RejectionReason fanout for sema-upgrade daemon.**
Lands in the same slice as the daemon promotion (bead
`primary-l3h5`). 5 concrete variants — source DB missing,
target DB exists, component identifier mismatch, version
identifier mismatch, engine-internal error.

**Q8 — Sema-upgrade daemon shape.** Sub-questions partly
answered: boot order CLOSED (sema-upgrade first per intent
record 111); self-upgrade is Q1; live-witness criterion
needs formalising (produce migrated artifact, witness
correctness against known-good Record, report completion —
live cutover separate operator action).

**Q9 — `ItemPriority` collapse to `Magnitude`?** Operator/153
§5 + operator/156 record 146 logged it as a question (live
write from another agent during a staging pass). Designer
lean from /269: collapse — priority and certainty share the
same nine-rung scale; the field name carries dimension. Needs
explicit psyche affirmation before the code touches.

**Q10 — Designer protocol coverage for parallel-main lanes.**
AGENTS.md hard override singles out "the prime designer" for
the subagent-dispatch carve-out. Per second-designer/3 the
parallel-main shape carries "full main-role authority". Does
the designer protocol cover second-designer + third-designer
as well? My current default as third-designer is the
conservative no-subagent path; this report and the previous
session were both done in main agent. Confirm or override.

## 6. References

- `/280` — yesterday's prime-designer session handover; eight
  open critical points + bead trail.
- `/279` — NOTA schema language + content-addressable
  schema-version hash (§4 per-component granularity; §6
  inspect socket).
- `/278` — multi-version daemon coexistence pattern (per-version
  subdirectories + home-managed symlink + declarative
  `deployedVersions` / `currentDefault`).
- `/273` — schema-migration synthesis: type-family split +
  commit-sequence at sema-engine.
- `/270` — sema-upgrade component design (wire surface; 0.01
  pilot; owner authority surface).
- `/268` — persona-pi operator-input brief (seven open forks
  the operator's implementation proposal closes).
- `/266` + `pi-api-surface-notes` — persona-pi triad sketch +
  Pi extension surface research (dual-path + namespace
  adaptation; six divergences from workspace discipline).
- `/264` — per-role protocols + designer-as-bridge workflow
  (settled); role-spaces, Criome identities, short IDs, LLM
  fallback (speculative).
- `/263` — schema specification language design (NOTA-based
  DSL; three-class diff classifier).
- `/257` — workspace-wide signal-contract names-and-shape
  audit; per-contract drop-lists; cross-contract migration
  order in §3.4.
- `/274` — forge skeleton reconciliation (existing `forge` +
  `signal-forge` reframed as criome-stack executor leg under
  `/271`'s family).
- `/271` — forge family design (exploratory; four eternal Nix
  abstractions; four carve-outs).
- `/150` — operator's triad migration playbook (consolidates
  operator/137–149; canonical migration order for stale
  contracts).
- `/151` — Spirit deployed-version + first-migration design
  (predecessor to /273/279 on schema identity).
- `/153` — operator's intent questions after /273+/274 (six
  forks for the next code work; supersedes operator-side
  earlier framings).
- `/154` + `/155` + `/156` — Spirit double-daemon deployment
  + v0.1.1 staging + remaining cutover gap.
- `second-operator/1` — lane registry slice implementation
  result.
- `second-designer/3` — lane registry test-implementation
  proposal (the proposal that operator just implemented).

This report retires when (a) the psyche closes Q1–Q10 above,
AND (b) the cutover step gating B1 unblocks, AND (c) a
successor third-designer or second-designer report supersedes
the situation pointer.

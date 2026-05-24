*Kind: Triage · Topic: separate-concerns-and-older-reports · Date: 2026-05-24*

# 319 / 3 — Separate-concerns + older-reports triage (Subagent C)

*Per §2.4 of `./0-frame-and-method.md`. Inventory: 14 entries on
non-schema-stack concerns — agent abstraction, forge family,
pi-harness work, persona systemd units, older state snapshots.
Verification basis: per-repo ARCH state, skill files, spirit
records via `/293/5` delta, bead inventory under `primary-gvgj`
(agent epic), `primary-yp6k` (forge merge), `primary-c2da`
(/249 closure), and `/318` rename inventory. Read-only on code
and ARCH per frame §3.*

## §1 Triage at a glance

14 entries triaged. The table below is the executable summary;
the per-report sections expand the reasoning.

| Report | Substance status | Action | Design-rationale guard | Permanent home for substance |
|---|---|---|---|---|
| `249-component-intent-gap-analysis.md` | IN-FLIGHT | KEEP | no | Live working surface for epic `primary-c2da`; superseded by `/293/5` for delta tracking but originating inventory still cited. |
| `257-signal-contracts-names-and-shape-audit.md` | IN-FLIGHT | KEEP | no | Per-contract rename guidance still drives `primary-u8vo` epic and `/318` rename inventory. |
| `264-designing-protocol-and-role-spaces.md` | LANDED + speculative | MIGRATE-then-DROP | no | Settled §1+§2 already in `AGENTS.md:205-213` ("designer protocol" hard override) and `skills/role-lanes.md`. Speculative §3-§6 still pending psyche follow-up. |
| `266-persona-pi-triad-design.md` | LANDED | KEEP | yes | `skills/component-triad.md:73-105` carries naming; `/309 §7` carries triad-shape migration table; spirit 152/157/158 superseded the DeepSeek path. |
| `268-persona-pi-operator-input.md` | STALE | DROP | no | Operator-brief shape; superseded by `/309` agent-component design which makes persona-pi a backend under `persona-agent`. |
| `281-headless-pi-research.md` | LANDED reference | KEEP | yes | Pi RPC/SDK mode survey still load-bearing for `primary-gvgj.6` (persona-pi backend daemon); explicit STATUS banner in §0 already redirects integration to spirit 152/157/158. |
| `282-workspace-implementation-status.md` | STALE | DROP | no | Snapshot of 2026-05-22 state; superseded by `/293/5` Steps 1+2 gap-closure delta + `/313` summary + spirit records 213-260+. |
| `291-persona-systemd-units-for-daemon-management.md` | LANDED | DROP | no | Hybrid recommendation absorbed into `persona/ARCHITECTURE.md:543-561, 694-702, 1275-1390` (UnitController + SystemdTransientUnitController) per spirit 223+240. Bead `primary-a5hu.4` tracks. |
| `292-designer-lane-top-issues-2026-05-22.md` | LANDED | DROP | no | All three issues addressed: Issue 1 → `/293/5` advances `primary-c2da`; Issue 2 → `primary-a5hu` decomposed (per /318/4 §1); Issue 3 → `skills/workspace-vocabulary.md` via /293/1. |
| `293-designer-and-research-batch-2026-05-23/` (dir) | LANDED | KEEP | no | Meta-report session unit per spirit 231; not retired as a single unit until orchestrator approves; substance already migrated per-subagent. |
| `294-most-important-gaps-visual.md` | LANDED | DROP | yes (then drop) | Designs B/B/B/C for Gaps 11/15/18/HarnessKind; substance carried in `/293/5` recommendations table and bead-filing-order §3. Gaps still open per `/293/5`. |
| `309-design-agent-component-abstraction.md` | LANDED | KEEP | yes | Naming + Options A/B/C backend mechanism + Options A/B harness placement; substance lives in epic `primary-gvgj` (10 sub-beads); `/git/.../signal-agent/ARCHITECTURE.md:8-11` cites this report. `/318` proposes prefix-drop rename. |
| `316-design-forge-family-current-direction.md` | IN-FLIGHT | KEEP | no | Source for bead `primary-yp6k` (forge family architecture merge); skeletons exist at `forge/ARCHITECTURE.md` + `signal-forge/ARCHITECTURE.md` but `forge-core` + `forge-nix-builder` not yet extracted. |
| `pi-api-surface-notes.md` (non-numbered) | LANDED reference | MIGRATE-then-DROP | no | Surface enumeration absorbed by `/281` (RPC/SDK is the workspace path) + spirit 152/157/158 (DeepSeek goes elsewhere); six divergences carry forward in `/309 §5`. |

Aggregate: **6 DROP** (268, 282, 291, 292, 294, pi-api-surface-notes
after migration), **6 KEEP** (249, 257, 266, 281, 293, 309, 316 —
seven actually, see §3.6), **1 MIGRATE-then-DROP** (264 + pi-api-surface-notes).
The MIGRATE column for 264 + pi-api-surface-notes flags that the
designer-rationale guard is NOT triggered (single-design or
research-survey, not competing alternatives); the substance moves
to permanent docs and the report retires.

The KEEP list breaks down as: KEEP-as-design-rationale-guard
(266, 281, 294, 309) + KEEP-as-in-flight-working-artifact (249,
257, 316) + KEEP-as-meta-session-unit (293).

## §2 Background — what changed since these reports landed

The schema-stack sweep (this session) is the consolidation
trigger; per `/318` orchestrator synthesis (`/318/4 §1`) the
upgrade-triad merger and persona-prefix rename are landing,
which absorbs significant signal-contract refactor work. Per
`/293/5 §1` the /249 gap inventory has 6 CLOSED + 5 PARTIAL +
24 OPEN, with 4 of the originally-tracked gaps either DEFERRED
or moved to other tracking (Gap 1 deferred per spirit 204;
Gaps 2 + 5 closed by spirit 215+216; Gap 4 closed by spirit
"debug the debugger"; Gap 30 closed by Gap 4).

Three keystone substance migrations have happened since the
inventory was filed:

- **Agent abstraction landed as contracts on disk.** Per
  `/git/github.com/LiGoldragon/signal-agent/ARCHITECTURE.md`
  and `/git/github.com/LiGoldragon/owner-signal-agent/ARCHITECTURE.md`
  (both modified 2026-05-24 per `ls -la`), the
  `signal-persona-agent` + `owner-signal-persona-agent` contracts
  shipped under `persona-` prefix per `/309 §1`, and `/318/1` now
  proposes renaming them per spirit 371 (open question §8.4 per
  /318/1:122). The `signal-persona-agent` directory does NOT exist
  at the conventional path under LiGoldragon; the renamed
  `signal-agent` and `owner-signal-agent` exist as the on-disk
  shape. This conflicts with `/309 §1`'s explicit "keep prefix"
  choice — see §3.12 for the conflict resolution implication.
- **Systemd-unit substance migrated into persona/ARCH.** Per
  `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md:543-561`
  (UnitController boundary + SystemdTransientUnitController) +
  `:694-702` (production startup is systemd/NixOS-shaped) +
  `:1275-1390` (manual + systemd unit controllers, persona-engine
  sandbox runner). Per `/317/1` spirit records 223 + 240 named
  the controller. `/291`'s hybrid recommendation is now ARCH text;
  the report retires.
- **Persona-pi role redefined.** Per `/309 §7` table row 4:
  persona-pi extends with a Rust daemon to become a backend
  under `persona-agent`. Bead `primary-gvgj.6` tracks the backend
  daemon. The `/266` dual-path design (terminal-cell + harness
  API) is preserved in concept but the daemon is now layered
  under `persona-agent-daemon` rather than as the router's direct
  peer.

## §3 Per-report rows (the substance)

### §3.1 — `249-component-intent-gap-analysis.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/249-component-intent-gap-analysis.md` |
| Substance status | IN-FLIGHT |
| Recommended action | KEEP |
| Target home if MIGRATE | n/a |
| Design-rationale guard | no |
| Reason | The 35-gap inventory is the originating substance for `primary-c2da` (P1 EPIC); per /293/5 §1 the delta tracking has moved to /293/5 but the inventory itself is still cited and the gaps not yet closed. Retirement is gated on `primary-c2da` reaching closure or on the originating inventory being absorbed into a per-component INTENT.md pass (Gap 3 itself). |

Verification: `bd list` shows `primary-c2da` as `not started`
at P1. `/293/5 §3` proposes 9 bead-filing orders against this
inventory; the inventory is the substrate for ongoing closure
work. The historical inventory plus per-gap classification still
read together — dropping the inventory now would orphan
`/293/5`'s delta tracking.

Caveat: this report is 1252 lines; if `primary-c2da` reaches
closure or if the closed/open status migrates into a permanent
"gaps log" file, the size warrants re-triage in a future sweep.

### §3.2 — `257-signal-contracts-names-and-shape-audit.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/257-signal-contracts-names-and-shape-audit.md` |
| Substance status | IN-FLIGHT |
| Recommended action | KEEP |
| Target home if MIGRATE | n/a |
| Design-rationale guard | no |
| Reason | Per-contract rename guidance still drives `primary-u8vo` epic (10 unmigrated contracts per `/282 §"In flight"`). The audit's five workspace-wide patterns (universal-verb shape, repeated-suffix, ancestry-prefix, Unimplemented redundancy, no-observable-block) are the closure criteria. `/318/1` confirms 24 supervised-component renames intersect with this audit's renames. |

Verification: `/257 §0` migration status table lists 10
unmigrated contracts; `/293/5` does not close them; `/318/1
§2.1` lists 24 renames that intersect with these contracts.
The audit's substance is still being executed.

Caveat: when `primary-u8vo`'s sub-beads (`primary-aunn`,
`primary-c620`, `primary-e1pm`, etc., listed in `/282`) all
close, this audit retires.

### §3.3 — `264-designing-protocol-and-role-spaces.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/264-designing-protocol-and-role-spaces.md` |
| Substance status | LANDED (§1, §2) + still-speculative (§3-§6) |
| Recommended action | MIGRATE-then-DROP |
| Target home if MIGRATE | §1 "per-role protocols" + §2 "designer-as-bridge workflow" → already in `AGENTS.md:205-213` (hard override "Do not dispatch subagents unless the psyche explicitly asks — except in the designer protocol"). The settled §1 framing also belongs as one paragraph in `INTENT.md` §"Roles" or `skills/role-lanes.md` §"Mirror model"; verify before drop. §3-§6 (role-spaces, per-agent Criome identity, shortest_id, fallback chains) all marked "Do not act on this section as if settled" — these were direction; spirit 134 (per-agent BLS identity), 125, 38, 39 carry the intent but no permanent doc yet captures the speculative shape. |
| Design-rationale guard | no |
| Reason | §1 + §2 are settled (workspace.nota records 35 + 36, Maximum); the "designer protocol" + "psyche → designer logs intent → designer writes report → designer files beads → operator implements" pipeline is the workspace's operative discipline today. §3-§6 are explicitly marked speculative inside the report itself. The settled parts are not specific to the report — they're the workspace's daily operating rhythm. The speculative parts have not advanced since the report landed (no role-spaces git-repos exist; no per-agent Criome identity exists per `/282 §"Designed but not started"`). |

Verification: `grep "designer protocol\|designing protocol"
/home/li/primary/AGENTS.md` returns line 205 ("Do not dispatch
subagents unless the psyche explicitly asks — except in the
designer protocol") and line 212 ("The **designer protocol**
(psyche 2026-05-21)..."). The skill `role-lanes.md` carries the
mirror model. Migration step: add one paragraph to
`skills/role-lanes.md` or `skills/designer.md` capturing the
"designing protocol" framing if it isn't already there. Then
drop /264.

Caveat: the speculative §3-§6 should be carried by spirit records,
not a retired designer report. `/293/5 §1` shows spirit record
98+99 + 117+118 settled the role-vector lane registry shape
(speculative section partly closes); spirit 134 affirms per-agent
BLS identity. The speculative substance is intent-tracked, not
report-tracked.

### §3.4 — `266-persona-pi-triad-design.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/266-persona-pi-triad-design.md` |
| Substance status | LANDED — naming + triad shape in skill; rest reshaped by /309 |
| Recommended action | KEEP (with STATUS-BANNER) |
| Target home if MIGRATE | Naming + binary table already in `skills/component-triad.md:73-105` ("Persona harness wrapping — the `persona-<agent>` family"). Dual-path design (terminal-cell + harness API) reshaped under `/309 §5+§7`: persona-pi becomes a backend daemon under `persona-agent-daemon`. The "Codex arm of composite designer" framing migrated to spirit records 124+125+45+147 (concept-designer ephemeral; not a persistent lane). |
| Design-rationale guard | yes |
| Reason | This report enumerated the persona-pi shape AS a top-level triad alongside the router; `/309` rewrote that placement (persona-pi is now a backend BELOW `persona-agent`). The original sketch is load-bearing as rationale for why persona-pi exists at all (composite-designer arm; Codex on Pi; intent records 43-47). A STATUS-BANNER pointing readers to `/309 §7` for the current placement + `skills/component-triad.md:73-105` for naming closes the supersession without losing the original framing. |

Verification: `/git/github.com/LiGoldragon/persona-pi/` exists
with `flake.nix` + `pi-packages/` but no Rust crate (per `ls
/git/github.com/LiGoldragon/persona-pi/` showing only checks,
nix, pi-packages directories + flake.nix). Per `/309 §7` row
4: "EXTEND — Keep the nix packaging. ADD: signal-persona-pi,
owner-signal-persona-pi, the Rust persona-pi-daemon runtime".
Per bead `primary-gvgj.6` ("persona-pi backend daemon (extends
existing persona-pi nix repo)"). The triad-as-router-peer
framing is superseded; the persona-pi-as-backend framing is the
current direction.

STATUS-BANNER content (for when /266 is updated rather than
dropped): "Superseded for placement: per /309 §7, persona-pi is
now a BACKEND under persona-agent, not a router peer. The
dual-path design (terminal-cell + harness API) is preserved in
concept inside the backend daemon. Naming + binary table in
skills/component-triad.md:73-105 (CLI `pi`, daemon
`persona-pi-daemon`). Bead `primary-gvgj.6`."

### §3.5 — `268-persona-pi-operator-input.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/268-persona-pi-operator-input.md` |
| Substance status | STALE |
| Recommended action | DROP |
| Target home if MIGRATE | n/a; the operator-input fork-by-fork was never executed in the form /268 described. The operator's task migrated to bead `primary-gvgj.6` under the agent-component epic, which is a different shape (backend daemon, not router-peer triad). |
| Design-rationale guard | no |
| Reason | Operator-input briefs are by-construction finite-lifetime — they retire when the operator's proposal lands or when the design is reshaped. Per `/309 §10 bead 6` the persona-pi work is now scoped as `primary-agent-F-pi`: "EXTEND. Keep the nix packaging. ADD: signal-persona-pi, owner-signal-persona-pi, the Rust persona-pi-daemon runtime that spawns `pi` as a subprocess (or speaks Pi's headless RPC mode per `/281`)." The operator's forks (which ExtensionAPI hooks, what signal contract shape, owner contract shape, dual-path surface area, authority placement) are subsumed into the agent-abstraction design — the operator no longer answers /268's question set because the design's pivoted. |

Verification: /268's §1 references `/266` + `pi-api-surface-notes`
as authoritative; both have been superseded by `/309` for
placement. /268's §2.7 "first slice" was the operator's
proposal-shaped output — that proposal was never produced
because the design landed differently. The substance lives in
`/309` (placement, backend shape) + `/281` (Pi RPC/SDK
integration shape) + spirit 152/157/158 (DeepSeek
non-overlap). Nothing in /268 is unique-and-still-load-bearing.

### §3.6 — `281-headless-pi-research.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/281-headless-pi-research.md` |
| Substance status | LANDED reference |
| Recommended action | KEEP |
| Target home if MIGRATE | The five capture targets (inputs, outputs, tool calls, tool results, full inference trace), the four operational modes (interactive / print / RPC / SDK), and the SDK + RPC integration sketches are reference material for `primary-gvgj.6` (persona-pi backend daemon). Per `/309 §10 bead 6` the persona-pi-daemon uses "Pi's headless RPC mode per `reports/designer/281-headless-pi-research.md`" — the report is explicitly cited as the integration source. |
| Design-rationale guard | yes |
| Reason | The report's own §0 STATUS banner names the supersession: TL;DR + §3 are SUPERSEDED (DeepSeek-as-pi-ai-direct path) per spirit 152/157/158 which moved DeepSeek to a new `persona-llm-client` (later `agent` per spirit 310). §1-§2 (mode survey + capture surface) and §3.3 (RPC mode Rust sketch) remain valid reference. Until `primary-gvgj.6` lands and the integration is verified end-to-end, this report is load-bearing for the implementation. |

Verification: `/309 §10 bead 6` cites `/281` for Pi RPC mode
integration. `bd list` shows `primary-gvgj.6` as `not started`
P1. The report explicitly retires when the persona-pi backend
daemon ships and verifies the RPC integration. Until then,
KEEP.

Note: the dual-design layout — settled mode survey + retracted
recommendation — is the design-rationale guard pattern.
Dropping the report would lose §3.3's Rust RPC client sketch
which is the integration starting point per `/309`.

### §3.7 — `282-workspace-implementation-status.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/282-workspace-implementation-status.md` |
| Substance status | STALE |
| Recommended action | DROP |
| Target home if MIGRATE | Status snapshots are by-construction finite-lifetime per `skills/reporting.md` §"What gets absorbed, not kept". The 35-gap status table is fully replaced by `/293/5 §1` (more recent inventory delta). The production-component table is superseded by `protocols/active-repositories.md` (live map). The /280 critical-points table referenced is itself older. |
| Design-rationale guard | no |
| Reason | Per `/282 TL;DR`: "Roughly 30-35% of the named architecture exists as working code." This number is a snapshot of 2026-05-22. `/293/5` is the more current inventory; `/313` (great summary 2026-05-24) is the next-newer summary; spirit records 215+216 closed Gaps 2 + 5 named in /282 as still-partial; the persona-engine has advanced under `primary-a5hu` epic decomposition (per `/318/4 §1`). The 2026-05-22 snapshot's load-bearing substance is everywhere superseded. |

Verification: `/293/5 §1` delta-updates `/282`'s 35-gap table
explicitly ("6 closed, 5 partial, 24 open" vs /282's "3 closed,
8 partial, 24 open"). Spirit records 215+216 (per
`/293/5` Gap 2 + Gap 5 evidence) closed gaps /282 marked
partial. `protocols/active-repositories.md` is the current repo
map, not /282's production-component table. Nothing in /282
remains uniquely-load-bearing.

### §3.8 — `291-persona-systemd-units-for-daemon-management.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/291-persona-systemd-units-for-daemon-management.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home if MIGRATE | `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`:543-561 (UnitController + SystemdTransientUnitController + component unit template projection), :694-702 (production startup is systemd/NixOS-shaped + dual-deploy via versioned daemons under systemd units), :865-870 (launcher actor surface + systemd transient-unit backend carve-out), :1275-1387 (Unit controller boundary in production tree). Per `/317/1` spirit records 223 + 240 named the controller as `SystemdTransientUnitController`. Per `/293/5 §3` bead-rank 4 the per-component restart policy work continues under bead candidate (operator + system-specialist). |
| Design-rationale guard | no |
| Reason | The hybrid recommendation (NixOS systemd unit for persona-daemon + SystemdTransientUnitLauncher for component daemons + DirectProcessLauncher kept for dev) is now ARCH text. The trade-off tables (§2, §4) and the upgrade walk-through (§3 sequence diagram) are absorbed into persona/ARCH §1.7 + the production-startup section. `/293/2` (unitbus research) drives the implementation choice for the SystemdTransientUnitLauncher backend; the design-recommendation itself has landed. |

Verification: `grep -nE 'systemd|SystemdTransientUnit|UnitController'
/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` returns
21 matches across §"Unit controller", §"Production startup",
§"Launcher actor", §"Manager state". The
SystemdTransientUnitController is the named backend per
spirit 223+240 + `/293/2`. The substance has cleanly
migrated.

Caveat: bead `primary-a5hu.4` continues implementing the
backend; the design report is not load-bearing for the
implementation, the ARCH text is.

### §3.9 — `292-designer-lane-top-issues-2026-05-22.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/292-designer-lane-top-issues-2026-05-22.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home if MIGRATE | Issue 1 (strategic drift on `primary-c2da`) → `/293/5` advances the gap closure (steps 1+2 complete + step 3 classification) and surfaces the 9-bead filing order; the strategic-drift question itself answered by the choice to do both (continue migration + advance gaps in parallel). Issue 2 (`primary-a5hu` too broad) → decomposed per `/318/4 §1` into `primary-4naq` + `primary-nobf` + `primary-q98d` + `primary-48w0` + `primary-r1ve` (5 sub-axes confirmed in `/293/5 §"References"` last line). Issue 3 (vocabulary divergence) → `skills/workspace-vocabulary.md` shipped via `/293/1` covering main/next + Persona + engine_management vocabulary. External-library findings (unitbus, kameo 0.16, winnow 1.0.0) addressed by `/293/2` + `/293/3` + (winnow not separately researched but `/293/3` confirms kameo line is on the workspace's pinned 0.20.0). |
| Design-rationale guard | no |
| Reason | The three issues are addressed; the visual recommendations are now operator-actionable beads (per `/293/5 §3`). The lean-lines for each issue have been executed; no unique substance is at risk of loss. /292's value was the prioritization synthesis; that synthesis fed `/293/5`'s ranking, which is the more-current decision surface. |

Verification: `/293/5 §"See also"` line 3 cites `/292` as
"the report that introduced Design C for gap-vs-migration
framing (record 247)" — /292's Design-C synthesis is preserved
in `/293/5`'s framing. Bead `primary-a5hu`'s decomposition is
confirmed by `/318/4 §1`. `skills/workspace-vocabulary.md`
exists per `/293/1`.

### §3.10 — `293-designer-and-research-batch-2026-05-23/` (directory)

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/293-designer-and-research-batch-2026-05-23/` |
| Substance status | LANDED (per-subagent) |
| Recommended action | KEEP (as meta-report directory) |
| Target home if MIGRATE | Per-subagent substance has migrated: `/293/1` → `skills/workspace-vocabulary.md`; `/293/2` (unitbus research) → bead `primary-lm9o` + the SystemdTransientUnitLauncher backend implementation (`primary-a5hu.4`); `/293/3` (kameo 0.16 Scheduler) → bead `primary-e4oq`; `/293/4` (rkyv 0.7→0.8) → CLOSED with finding that workspace already on rkyv 0.8 (zero engineering-hours cost); `/293/5` (gap closure step 1+2) → bead-filing order for `primary-c2da` epic. |
| Design-rationale guard | no (meta-report directory; per spirit 231) |
| Reason | The meta-report directory IS the session unit per spirit 231 + AGENTS.md §"Meta-report directories — sub-agent sessions". Garbage-collected as one unit. The per-subagent substance landed; the directory retires when the orchestrator (designer lane) judges the session unit complete and the carrying beads close. /293/5 still drives in-flight bead-filing under `primary-c2da`; the directory is not retired yet. |

Verification: `ls
/home/li/primary/reports/designer/293-designer-and-research-batch-2026-05-23/`
returns 6 files (0-frame + 5 subagent reports). Spirit 231
defines the meta-report directory shape; per AGENTS.md the
directory is garbage-collected as one unit.

Caveat: when `primary-c2da` reaches closure AND
`primary-lm9o`+`primary-e4oq` close, this meta-report
directory retires as one unit.

### §3.11 — `294-most-important-gaps-visual.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/294-most-important-gaps-visual.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home if MIGRATE | The four elaborated gaps' candidate designs migrated to `/293/5 §3` (bead-filing recommendations) — Gap 11 → operator bead candidate rank 1 with Design B (record-divergence); Gap 15 → rank 2; Gap 18 → rank 3; HarnessKind cluster (Gaps 7 + 27 + 13) → conjoint PENDING-CLARIFICATION cluster awaiting one psyche call (per `/293/5 §4` "Gap 7 + Gap 27 conjoint"). The designer recommendations as design-rationale survive in `/293/5`. |
| Design-rationale guard | yes (but substance migrated so safe to DROP) |
| Reason | This report enumerates competing designs per gap (Design A/B/C for partial-failure semantics; Designs A/B/C for HarnessKind disposition). The design-rationale guard would normally say KEEP — but `/293/5 §3` carries forward the chosen designs (rank 1: Design B for Gap 11; rank 2: Design A for Gap 15; rank 3: Design B for Gap 18; the HarnessKind conjoint cluster awaits psyche). The recommendations + per-design trade-offs are absorbed into the bead-filing order. The visual diagrams themselves are not load-bearing for downstream work — they were /294's rationale display, now subsumed. |

Verification: `/293/5 §3` ranks 1-3 list the same gaps with
the chosen designs from /294 named. `/293/5 §4` "Anything
structurally hard to break up" calls out the HarnessKind
conjoint cluster, confirming /294's analysis was carried.

Caveat: if `primary-c2da`'s closure path requires re-reading
the per-design trade-offs, /294 lives in the commit tree per
spirit 370 (deleted reports retrievable from commit tree).
This is the explicit rationale for aggressive consolidation
per spirit 362.

### §3.12 — `309-design-agent-component-abstraction.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/309-design-agent-component-abstraction.md` |
| Substance status | LANDED — as `signal-persona-agent`/`owner-signal-persona-agent` ARCH on disk |
| Recommended action | KEEP (with STATUS-BANNER for the rename open question) |
| Target home if MIGRATE | Already migrated: `/git/github.com/LiGoldragon/signal-agent/ARCHITECTURE.md` cites this report as the source design (line 8-11: "This shape follows `.../309-design-agent-component-abstraction.md`"). `/git/github.com/LiGoldragon/owner-signal-agent/ARCHITECTURE.md` cites bead `primary-gvgj.2` from this design. The 10-bead epic (per `/309 §10`) ships as `primary-gvgj` with 10 sub-beads `primary-gvgj.3` through `primary-gvgj.9` (per `bd list`). The naming + binary table + persona-prefix wrapping convention is in `skills/component-triad.md:73-105`. |
| Design-rationale guard | yes |
| Reason | The report enumerates Options A/B/C for backend mechanism + Options A/B for harness placement, picks Option C and Option A respectively, and supplies the migration sequence. The chosen shapes have landed (contracts on disk) but the rationale for picking Option C (process isolation, per-backend version pinning, micro-components rule, lane discipline) and Option A (no new isolation gained, triad maintenance overhead, harness state per-agent-run) is not in the on-disk ARCH — those ARCH files state only the chosen shape. The design-rationale guard says KEEP. |

Verification: `/git/.../signal-agent/ARCHITECTURE.md:8-11`:
"This shape follows `/home/li/primary/reports/designer/309-design-agent-component-abstraction.md`
and the Wave 3 booking in `/home/li/primary/reports/designer/310-meta-overhaul-booking-roadmap.md`."
This is a violation of `skills/architecture-editor.md` §"Architecture
files never reference reports" — but the violation already
exists on disk; not this sweep's concern. The substance
references confirm /309 is currently load-bearing.

STATUS-BANNER addition recommended: "Naming reconsidered:
`/318/1 §2.2` flags `persona-agent` vs `agent` as an open
question — spirit 309's text says KEEP persona- prefix (this
report §1) but spirit 371 may apply (drop prefix). The
on-disk contracts shipped under `signal-persona-agent` and
`owner-signal-persona-agent` directory naming was renamed to
`signal-agent` / `owner-signal-agent` (per `ls
/git/github.com/LiGoldragon/`). Resolution pending per
`/318/1 §8.4`. Designer-lane should not rely on §1's naming
table without checking the resolved rename."

Caveat: the on-disk paths showing renamed contracts BUT the
Cargo.toml package names (per `/318/1 §2.2` table) showing
`signal_persona_agent` is an inconsistency — the rename is
mid-flight. /309 retires when `/318`'s rename resolves and
when the 10-bead epic closes.

### §3.13 — `316-design-forge-family-current-direction.md`

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/316-design-forge-family-current-direction.md` |
| Substance status | IN-FLIGHT |
| Recommended action | KEEP |
| Target home if MIGRATE | Per `/316 §5` the merge target is `forge/ARCHITECTURE.md` + `signal-forge/ARCHITECTURE.md` via bead `primary-yp6k` (P3). Until `primary-yp6k` lands, the family map (§2), carve-out direction (§3), convergence path (§4), open design questions (§7) live in /316. The skeleton ARCH files exist (`/git/.../forge/ARCHITECTURE.md`, `/git/.../signal-forge/ARCHITECTURE.md`) but neither carries the family map or the forge-core/forge-nix-builder library extraction direction yet. |
| Design-rationale guard | no |
| Reason | This is a forward-looking design report stating the chosen direction (not enumerating alternatives — those were in /271 and /274, which this report supersedes per §8). The chosen direction has spirit-record backing (153, 154, 155) but the architectural merge into the ARCH files has not landed. The four open design questions (§7) are still open. The bead `primary-yp6k` is `not started`. |

Verification: `cat /git/.../forge/ARCHITECTURE.md | head -30`
returns the older daemon-as-executor framing — no family map,
no forge-core mention. `cat /git/.../signal-forge/ARCHITECTURE.md`
returns the three-layer alignment in progress, no `Deploy`
removal yet (per spirit 153 the Deploy operation should move to
signal-lojix; not done). `bd list | grep primary-yp6k` returns
no active bead listing in current shortlist but /316 §5 names
it as `primary-yp6k (P3)`. The design has not been executed.

Caveat: this report retires when `primary-yp6k` lands and the
ARCH files carry the family map + per-component-forge
convergence path.

### §3.14 — `pi-api-surface-notes.md` (non-numbered)

| Field | Value |
|---|---|
| Path | `/home/li/primary/reports/designer/pi-api-surface-notes.md` |
| Substance status | LANDED reference |
| Recommended action | MIGRATE-then-DROP |
| Target home if MIGRATE | Surface enumeration (built-in tools, ExtensionAPI methods, event surface, tool-registration shape, shared-state canonical example) — superseded by `/281 §1-§2` (RPC + SDK modes documented + capture targets enumerated). Six divergences from workspace discipline (`/pi-api-surface-notes §"Where Pi diverges"`) — substance now in `/309 §5` (where does harness live; harness becomes library; backends are separate daemons). Five open psyche-clarification questions — answered or superseded: Q1 (db_query reference) clarified by /266; Q2 (expose Pi's tool surface vs embed Pi as engine) answered by /309's backend-daemon-spawns-pi-RPC choice; Q3 (flat vs typed) answered by typed-noun records via `signal-persona-agent`; Q4 (TypeScript writable in persona-pi) answered no (RPC mode, no Node leg); Q5 (full ExtensionAPI vs subset) answered subset (RPC events only). |
| Design-rationale guard | no |
| Reason | Research feed for /266 (per the report's own §"What this report is for"). The substance is downstream-cited in /266, /268, and /281; once those reports' state is settled (266 KEEP-with-banner, 268 DROP, 281 KEEP-as-reference), the upstream research feed retires. The non-numbered status is also informal — the report doesn't fit the `<N>-<topic>.md` shape per `skills/reporting.md`. Migration target: `/281` carries the operative integration knowledge for persona-pi backend; `pi-api-surface-notes` retires. |

Verification: /281's §"See also" cites
`pi-api-surface-notes.md` ("extension API surface; package
scope is corrected to `@earendil-works/` by this report").
/268's §1 cites it. /266's §4 cites it. The cite chain
indicates downstream consumption; once those reports settle,
the research feed retires.

Caveat: per the frame's §5 ("Does NOT alter
`pi-api-surface-notes.md`'s non-numbered status"), the
numbering question is independent of triage. The drop
recommendation stands; if KEEP is preferred for any reason,
renaming under a numbered slot is a separate decision.

## §4 What the orchestrator should integrate from this slice

The 6 DROP recommendations are the load-bearing retirement list
from Slice C: 268, 282, 291, 292, 294, pi-api-surface-notes.
None has unique-load-bearing substance.

The 6 KEEP recommendations carry substance forward: 249 (gap
inventory still in-flight), 257 (contract-audit still
in-flight), 266 (rationale guard), 281 (rationale guard + Pi
RPC reference), 309 (rationale guard), 316 (forge in-flight).
Plus 293 (meta-report-directory as one unit).

The 1 MIGRATE-then-DROP (264) does light migration:

- `skills/role-lanes.md` §"Mirror model" already carries the
  agent-as-single-identity framing; add (if not already) a
  one-paragraph capture of the "per-role protocols" Maximum
  framing from /264 §1.
- `AGENTS.md` already carries the "designer protocol" exception
  for parallel subagents — settled.
- After confirming both already carry the substance, /264
  retires.

The persona-pi rename situation (§3.4 + §3.12 caveats) is NOT
this slice's resolution — `/318` carries the rename slice. This
slice flags the open question for the orchestrator's overview
synthesis (file 4).

Aggregate retirement candidates from Slice C (6 reports):
~258 + 369 + 207 + 545 + 695 + 261 = **2,335 lines retired**
plus the meta-directory question deferred to a future
sweep. Combined with what Slice A and Slice B return, the
sweep meets the spirit-362 aggressive-consolidation discipline.

## §5 Open questions surfaced for the orchestrator

1. **Persona-agent prefix question is unresolved.** /309's
   text explicitly KEEPS `persona-` prefix; the on-disk
   contracts shipped under both naming conventions
   (`signal-persona-agent` Cargo.toml package names per
   `/318/1 §2.2` but renamed directory paths per `ls
   /git/github.com/LiGoldragon/`). The orchestrator's
   overview synthesis (file 4) should flag this conflict for
   the psyche or defer to `/318`'s resolution.

2. **/264 §3-§6 speculative substance.** Sections 3-6 (role-
   spaces, per-agent Criome identity, shortest_id, fallback
   chains) all marked "Do not act on this section as if
   settled" in the report. The substance lives in spirit
   records 38, 39, 40, 125, 134 but no permanent doc captures
   the direction. Whether retiring /264 (after §1+§2
   migration) loses speculative substance is a question for
   the orchestrator: spirit records are the canonical home
   per AGENTS.md, but if a "possible-future-design" entry
   should land in some ARCH file, the orchestrator decides
   per `skills/architecture-editor.md` §"Carrying
   uncertainty".

3. **Forge family beads.** /316 references bead `primary-yp6k`
   as the merge slice; `bd list` does not surface it in the
   current shortlist. The orchestrator may want to verify
   the bead's state before assuming /316's retirement is
   gated only on that bead landing.

## §6 Verification appendix — sources read

For audit-trail completeness:

- `/home/li/primary/reports/designer/319-schema-stack-context-maintenance-sweep/0-frame-and-method.md`
- `/home/li/primary/skills/context-maintenance.md`
- `/home/li/primary/skills/component-triad.md` (lines 60-180, 73-105 binary-naming table)
- `/home/li/primary/skills/role-lanes.md` (head)
- `/home/li/primary/skills/workspace-vocabulary.md` (verified existence via grep + `/293/1`)
- `/home/li/primary/AGENTS.md` (designer protocol exception lines 205-213)
- `/home/li/primary/protocols/active-repositories.md` (head; current core stack)
- `/home/li/primary/reports/designer/293-designer-and-research-batch-2026-05-23/{0-frame,1-vocabulary-sweep,2-unitbus-research,3-kameo-0_16-research,4-rkyv-0_7-to-0_8-audit,5-gap-closure-step-1-2}.md`
- `/home/li/primary/reports/designer/318-upgrade-merger-and-persona-prefix-rename/{0-frame,1-rename-inventory,4-overview}.md`
- All 13 numbered reports in the inventory (full read on smaller; head + middle + end on larger ones)
- `/home/li/primary/reports/designer/pi-api-surface-notes.md` (full)
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` (grep on systemd/UnitController/SystemdTransientUnit)
- `/git/github.com/LiGoldragon/persona-pi/` (ls — confirmed no Rust crate)
- `/git/github.com/LiGoldragon/signal-agent/ARCHITECTURE.md` (full head)
- `/git/github.com/LiGoldragon/owner-signal-agent/ARCHITECTURE.md` (head)
- `/git/github.com/LiGoldragon/signal-forge/ARCHITECTURE.md` (head)
- `/git/github.com/LiGoldragon/forge/ARCHITECTURE.md` (head)
- `bd list` — verified primary-gvgj epic + sub-beads, primary-c2da, primary-a5hu, primary-0m1u rename epic

No code or ARCH edits performed; read-only per frame §3.

## See also

- `./0-frame-and-method.md` — orchestrator frame for the sweep.
- `./1-schema-stack-substance-triage.md` (Subagent A — sibling slice; the rename + agent-contract conflict crosses with §3.12 here).
- `./2-working-artifacts-triage.md` (Subagent B — sibling slice on sweeps/handovers/audits).
- `./4-overview-and-retirement-list.md` (orchestrator synthesis, pending).
- `/home/li/primary/skills/context-maintenance.md` §3a "Design-rationale guard against premature DELETE" — the guard applied to /266, /281, /294, /309.
- `/home/li/primary/skills/reporting.md` §"Soft cap" + §"What gets absorbed, not kept" — disk-side hygiene this triage operationalises.
- Spirit records cited: 152, 157, 158, 175, 215, 216, 223, 240, 309, 310, 369, 370, 371 (current direction touchpoints); 38, 39, 40 (speculative /264 substance); 124, 125, 134, 147 (concept-designer ephemeral resolution).
- Bead epics + items cited: `primary-gvgj` (10 sub-beads for agent epic), `primary-c2da` (gap-closure epic), `primary-u8vo` (contract migration epic — implicit), `primary-a5hu` (Persona-engine epic decomposed to `primary-4naq`/`primary-nobf`/`primary-q98d`/`primary-48w0`/`primary-r1ve`), `primary-yp6k` (forge family merge), `primary-lm9o` (unitbus), `primary-e4oq` (kameo Scheduler), `primary-0m1u` (persona-prefix rename epic).

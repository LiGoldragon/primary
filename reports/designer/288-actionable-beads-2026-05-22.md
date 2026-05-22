# 288 - Actionable beads — 2026-05-22

*82 beads are `bd ready` (no active blockers). This report
categorises them by critical-path and lane so a reader can see
which beads CAN be picked up right now but AREN'T yet in flight.
Snapshot at 2026-05-22 — for current state run `bd ready`.*

## Critical-path to Spirit cutover (P1)

These are the load-bearing items for the v0.1.0 → v0.1.1 smart
handover cutover. Foundation crates already landed (operator/158,
160, 161); these are the next slices.

| Bead | Shape | Status |
|---|---|---|
| `primary-7kge` — `owner-signal-version-handover` contract (ForceFlip / Rollback / Quarantine) | NEW this session; operator can file the contract crate immediately; no blockers | not started |
| `primary-a5hu` — second-operator Persona epic (port persona-* to signal-executor v4 + upgrade orchestration) | second-operator pickup per /165, /166, /167-169 absorb; blocks `primary-x3ci` | in flight (lane absorbing) |
| `primary-c2da` — /249 gap-closure sweep (PRIMARY designer focus per record 166) | designer can start; 24 of 35 gaps still open per /282 | not started |
| `primary-chpq` — Spirit default wrapper dual-writes | **likely retire-candidate** — operator/157 refined: "durable handover is not CLI-owned dual-write"; smart-handover supersedes | needs review |
| `primary-wvdl` — Persona: port to current Signal stack + complete upgrade orchestration | appears to overlap `primary-a5hu`; ownership/scope reconciliation needed | needs review |
| `primary-x3ci` — Spirit cutover | sub-work (v0.1.0 retrofit, mirror payload, temporary-runner replacement) per operator/161 is concretely actionable now; full cutover blocked on `primary-a5hu` | partial-actionable (sub-work) |

## Designer-actionable (next session)

Substantive designer landings available now; pickups in order of
size:

| Bead | Size | Substance |
|---|---|---|
| `primary-bin2` — manifest /264 §1-§2 + concept-designer-as-ephemeral into skills/designer.md | small | record 147 settles; backed by /264 §1-§2 + record 147; settles /234 lane mechanics |
| `primary-094p` — verify /214 substance against criome/ARCHITECTURE.md; retire /214 if landed | small | per /282, substance largely already in criome ARCH @4474bb8 + signal-criome ARCH @723e6c8 |
| `primary-gjs5` — signal-sema/ARCHITECTURE.md update for Magnitude Unknown widening + Health/Readiness collapse | small | record 165; deferred to v0.1.2 timing but the ARCH edit can land now |
| `primary-ib5n` — canonical sema-upgrade + nota-schema-language architecture merge | substantial | foundation crates landed; merge can absorb /263 + /270 + /273 + /279 + /285 + operator/158/160/161 into per-repo ARCH files |
| `primary-yp6k` — canonical forge family architecture merge | substantial | absorbs /271 + /274 + existing signal-forge skeleton at 87882b6 |
| `primary-u7gc` — persona-pi/ARCHITECTURE.md from /266 | BLOCKED — waits on operator implementation proposal per /268 | blocked |

## Triad-migration batch (P1, operator lane, all bd-ready)

These 13 beads (the 2026-05-21 batch) gain meaning once foundation
crates land. Most need Persona (`primary-a5hu`) + signal-
executor v4 in place; some are independent.

`primary-0bls` criome · `primary-k2mh` engine-management · `primary-9up1` lojix · `primary-mdhj` repository-ledger · `primary-c620` orchestrate (in flight) · `primary-gu7t` harness · `primary-qjdp` terminal · `primary-21gn` system · `primary-krbi` message · `primary-li7a` introspect · `primary-aunn` router · `primary-e1pm` mind · (plus the 13th was Persona itself, now covered by `primary-a5hu`).

Per /166 (second-operator), the next operator slice is the executor
migration on `primary-c620` (orchestrate). Per second-designer/151,
orchestrate ships first; mind (`primary-e1pm`) follows after
sema-upgrade lands.

## Whisrs bug fixes (P0 / P1, operator-actionable)

| Bead | Priority |
|---|---|
| `primary-51pn` — Whisrs service restart drops in-memory audio (SIGTERM handler) | P0 |
| `primary-6m8u` — Whisrs encode dictation as Opus before transcription upload | P1 |
| `primary-kyhs` — Whisrs close ffmpeg stdin before recovery spool wait | P1 |

## Other P1 open (operator-actionable; pre-existing)

| Bead | Note |
|---|---|
| `primary-ojxq` — persona-spirit: implement new triad component | **likely retire/refit** — substance superseded by operator/158, 160, 161 + spirit v0.1.1 landings |
| `primary-77hh` — Drop channel-name prefix from signal_channel! emitted types | macro hygiene |
| `primary-izze` — tui-criome: long-running owner client | criome-stack work |
| `primary-at7x` — criome: finish routed authorization after coordinator skeleton | criome-stack work |
| `primary-ipjx` — Speech-to-text durable-first infrastructure (epic) | epic; spans role:operator + role:designer |
| `primary-ffew` — criome: migrate identity/attestation state to sema-engine | criome-stack work |
| `primary-hj4.1` — persona-mind: implement typed mind graph from designer/152 | mind-stack work (gated on sema-upgrade per record 205) |
| `primary-devn` — persona+signal-persona+persona-router: retire MessageProxy phantom | persona-stack work |
| `primary-8n8` — persona-terminal: supervisor socket and gate-and-cache delivery | persona-stack work |
| `primary-hj4` — persona-mind: channel choreography, subscriptions, suggestions | mind-stack work |

## P2 — substantial pool (~30 beads)

Mostly operator (nota-codec, horizon-rs, sema, etc.) and
system-specialist (CriomOS, cluster, lojix, clavifaber, etc.).
Notable items worth flagging:

- `primary-ihee` — Horizon rewrite epic (system-specialist)
- `primary-699g` — design persona-orchestrate component (potentially overlaps `primary-a5hu`)
- `primary-l3h5` — Add sema-upgrade daemon and thin upgrade CLI (foundation-adjacent; could land alongside primary-ib5n architecture merge)
- `primary-9os` — persona-router: typed endpoint/kind keys
- `primary-ddx` — Rename sema → sema-db workspace-wide (lane-coordination work)
- `primary-aww` — signal: complete signal vs signal-core kernel extraction
- `primary-3rp0` — signal: resolve legacy AuthProof
- `primary-31jt` — persona sandbox tests with midway wire-capture witnesses
- `primary-y4o` — production engine: persona system user + Linux capabilities
- `primary-5rq` — criome BLS auth substrate

Plus cluster-operator: `primary-tpd`, `primary-8b3`, `primary-mm0`, `primary-e3c`, `primary-cua`, `primary-da7`, `primary-58l`, `primary-1ha`, `primary-nvs8`, `primary-un7p`, `primary-a61`, `primary-f6cc`, `primary-7zz`, `primary-hpx`, `primary-sff`, `primary-9wi` (multi-label sweep just landed).

## P3 — design / parked / housekeeping (~12 beads)

- `primary-m8xv` / `primary-voz5` / `primary-lyc8` — PARKED design tasks per record 166 (persona-llm-client, persona-listen+speak, signal-real-time)
- `primary-094p` / `primary-bin2` / `primary-yp6k` — already in designer-actionable section above
- `primary-k9kj` / `primary-gfc0` / `primary-d5im` / `primary-7ay8` / `primary-cua` / `primary-jsi` — small cluster-operator + system-specialist housekeeping
- `primary-oil` / `primary-fgk` / `primary-6nf` — operator/system-specialist standalone tasks

## Items worth review-and-refit / close

These appeared bd-ready but the underlying work may be superseded by
recent landings; check before assigning:

| Bead | Why |
|---|---|
| `primary-chpq` — Spirit wrapper dual-writes | smart-handover supersedes per operator/157 |
| `primary-ojxq` — persona-spirit triad implementation | substance landed via operator/158-161 |
| `primary-qk04` — Multi-version persona-spirit daemon coexistence | already-deployed per /282; reframed to verify-and-close |
| `primary-2y5` — persona daemon: EngineId socket setup, manager redb, spawn envelope | now under broader scope of `primary-a5hu` (Persona epic) |
| `primary-699g` — design persona-orchestrate component | overlaps `primary-c620` (implementation) + `primary-a5hu` (Persona scope) |
| `primary-wvdl` — Persona: port to current Signal stack + upgrade orchestration | overlaps `primary-a5hu` |
| `primary-0v2` — clavifaber identity unification | anti-pattern B (design question without DoD) per subagent B sweep; needs reformulation |

## Recommended pickups by lane (in priority order)

**Designer (next session):**
1. `primary-bin2` (small; settles /234)
2. `primary-094p` (small; retires /214 after verification)
3. `primary-gjs5` (small; signal-sema ARCH for Magnitude widening)
4. `primary-c2da` (substantial; primary focus per record 166)
5. `primary-ib5n` (substantial; architecture merge — foundation landed)
6. `primary-yp6k` (substantial; forge merge)

**Operator (continuing):**
1. `primary-x3ci` sub-work — v0.1.0 retrofit, mirror payload, temporary-runner replacement (per operator/161 remaining work)
2. `primary-7kge` — `owner-signal-version-handover` contract crate (immediate; foundation crates already in place)
3. Triad-migration batch (`primary-c620` already in flight; queue others behind foundation landings)
4. Whisrs P0/P1 bugs (`primary-51pn` urgent)

**Second-operator:**
1. `primary-a5hu` Persona epic (continuation of /167, /168, /169 absorption; first slice likely `primary-c620` per /166)

**Cluster-operator:**
1. Bird-on-Zeus update authority chain (per cluster-operator/4)
2. Label-cleanup sweep on the 5 space-mashed beads (already done this session) — verify

**System-specialist:**
1. `primary-ihee` Horizon rewrite epic
2. The various CriomOS / clavifaber / lojix beads — by their own prioritisation

## See also

- `bd ready` — live workspace view
- `bd ready --priority p1` — narrows to P1
- `reports/designer/286-session-audit-2026-05-22.md` — full session work
- `reports/designer/249-component-intent-gap-analysis.md` — gap inventory (primary-c2da)
- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md` — canonical spec
- `reports/designer/287-version-handover-component-explained.md` — visual reference for the handover stack

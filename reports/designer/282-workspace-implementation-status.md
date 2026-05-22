# 282 - Workspace implementation status snapshot

*Designer report. Dispatched by prime designer (designer protocol,
parallel-subagents authorised per psyche record 57) 2026-05-22.
Driver: psyche message "all of the most important questions that
still haven't been implemented … I don't even know now what's
implemented and what's not." Goal: one snapshot view of the
Criome-stack tree as it stands today, mapping which pieces have
reached production, which are landed-not-deployed, which are
in-flight, which are designed-not-implemented, and which are
newly-decided-no-design-yet.*

## TL;DR

Roughly **30-35% of the named architecture exists as working
code**. Production today carries exactly one daemon component
(persona-spirit v0.1.0 in user-session, plus dual-deploy v0.1.1
side-by-side) plus the pre-Persona deploy/system stack
(`lojix-cli`, `horizon-rs`, `CriomOS`, `whisrs`). The
**most-critical blocker** is the Spirit v0.1.1 cutover-gate
(intent record 109 violation on `operator/spirit-response-protocol`
branch; seven `High` legacy intents stuck in file-substrate
purgatory). The **most-critical un-implemented piece** is
`persona` (engine-manager daemon) — 1513-line ARCH, in-progress
bead `primary-2y5`, zero production deployment. The **surprise**
is how much new design landed in the last 36 hours: spirit
records 1-162 introduced eight new components (persona-pi,
sema-upgrade, forge, persona-llm-client, persona-listen,
persona-speak, signal-real-time, plus the role-vector
lane-registry redesign) without any of them yet existing as
running code.

## Production goalposts reached

These run on real hardware today (Prometheus, Zeus, the user's
laptop).

| Component | Version | Evidence |
|---|---|---|
| `persona-spirit-daemon` + `spirit` CLI v0.1.0 | `694452a` | CriomOS-home flake.lock pins `persona-spirit-v0-1-0`; `modules/home/profiles/min/spirit.nix` deploys the systemd user service; the deployed Spirit holds the 103 records of psyche intent migrated from `/intent/*.nota`. |
| `persona-spirit-daemon` v0.1.1 (parallel) | `e137f5d` | CriomOS-home flake.lock also pins `persona-spirit-v0-1-1`; CriomOS-home commit `d25441f` "home: deploy versioned spirit daemons". Per /280 §3 Open critical point 6, this is the first concrete multi-daemon coexistence — both versions side-by-side on the user session. |
| `lojix-cli` (production deploy stack) | `42529ebd` pinned in CriomOS flake.lock; `ec8f7211` is current | The pre-Persona monolithic deploy tool; carries all production deploys for CriomOS, projects horizon-rs over goldragon/datom.nota. Per `protocols/active-repositories.md` §"Stack A". |
| `horizon-rs` (production) | `340e5cc` on main | Production horizon projection; consumed by lojix-cli for deploys. |
| `CriomOS` + `CriomOS-home` | Current main on each | Active OS deployment, includes all the cluster nodes. |
| `whisrs` (STT) | `criomos` branch | Speech-to-text deployed under the user session; `whisrs.service`, `whisrs status`, etc. per CriomOS-home `skills.md`. Triggers most psyche intent capture via dictation today. Has 4 open bug beads: `primary-51pn` (P0: restart drops in-memory audio), `primary-6m8u` (encode dictation as Opus), `primary-kyhs` (close ffmpeg stdin before recovery spool wait), `primary-ipjx` (P1 epic: rethink as durable-first infrastructure). |
| `repository-ledger` daemon + CLI | `2d7aa28` | Per commits `f37c864` "ledger client socket to nixdev" and `49d499e` "submit repository hook through ledger cli" — the receive-hook on the gitolite server writes to the ledger via the deployed daemon. First fully-shipped triad after spirit. |

**Net production daemon count: 2 unique components (spirit, repository-ledger)** plus 2 spirit versions side-by-side, plus the pre-Persona deploy/OS stack. The Persona engine itself is not yet a production thing — there is no running persona-daemon, no running mind, no router, no harness.

## Implemented but not yet deployed

Code compiles and tests pass on main, but the production stack hasn't picked it up. Mostly clustered around the Spirit v0.1.1 cutover and around the signal-sema/Magnitude migration.

| Component | Evidence | Reason not deployed |
|---|---|---|
| `signal-sema` Magnitude vocabulary | `22b036a` "add magnitude vocabulary" + `e83fd00` "document magnitude architecture" on main | The new universal nine-rung Magnitude type ships, but only persona-spirit consumes it so far. |
| `persona-spirit` Magnitude consumption | `d1c7610` "consume sema magnitude for certainty" — but on the **branch** `operator/spirit-response-protocol`, NOT merged | Per /280 §3 Open critical point 5 — direct violation of intent record 109 (no branches by default). Cutover gate. |
| `signal-persona-spirit@d7b22bfb` (Magnitude shape) | `d7b22bfb` "replace certainty with sema magnitude" on the same branch | Same gate. |
| `sema-upgrade` prototype + `sema-upgrade-temporary` CLI | `8434c43`, `b6ad09a` "spirit database migration CLI" — on main, but no daemon yet | First migration done at `b6ad09a` (103 records migrated 2026-05-22 to `.v0.1.1.migrated-20260522075112` redb), not yet swapped into live path. Bead `primary-l3h5` covers the daemon promotion. |
| `signal-sema-upgrade` working contract | `7991a82` on main | Triad working signal — only consumed by the temp CLI, no daemon yet. |
| `owner-signal-sema-upgrade` policy contract | `9e61b03` on main | Triad policy signal — ditto. |
| `persona-mind` Magnitude consumption | `d08881b` "consume sema magnitude priorities" on main | Compiles; not exercised in production because no persona-mind daemon runs in production. |
| `persona` engine-manager (Axis 1 wire surface) | `4e92889` "migrate engine manager to current signal contracts" on main | Internals still lag wire surface — see /280 §3 Open critical point 4 ("Axis 2 not done"). Bead `primary-k2mh`. |
| `persona-orchestrate` lane-registry slice | `50ed6f7`, `5e52655` "implement lane registry slice" on main | First operational slice; no daemon supervisor running in production. Mind/orchestrate authority chain still designer-stub per /249 §3. |
| `signal-persona-spirit` v0.1.1 bump | `5f7d4f4` on main | Package-version bump; needs cutover to ship. |

## In flight (partial implementation)

Components with active branches, open beads, or partial work in progress.

### Beads explicitly in-progress

| Bead | Title | What's partial |
|---|---|---|
| `primary-2y5` (P1) | persona daemon: EngineId socket setup, manager redb, spawn envelope | The persona engine-manager daemon itself — without it nothing else in the Persona triad family supervises. |
| `primary-a18` (P1) | persona-engine-sandbox: bind credential root and add provider auth smoke | Sandbox runner for engine-manager testing. |
| `primary-devn.1.4` (P1) | prototype introspection slices: manager, terminal, message, harness | Persona-introspect's per-peer client actors per /249 §10. |
| `primary-a61` (P2) | CriomOS: move router Wi-Fi policy out of Nix modules | Horizon/lojix-side work. |
| `primary-hj4.1.4` (P2) | persona-mind: post-commit graph subscription delta delivery | Subscription-fanout for typed mind graph. |
| `primary-vhb6` (P2) | horizon re-engineering: input/output split + new lojix daemon | Active feature arc `horizon-leaner-shape` — smoke-built but not deployed (per `protocols/active-repositories.md` §"Stack B"). |

### Open beads representing partial / planned work

The **10 unmigrated signal-contracts epic** (`primary-u8vo`) is the dominant in-flight workstream. Per /257, half of the contracts (spirit, orchestrate's frame, repository-ledger, the four owner-signals for spirit/mind/orchestrate/router) are migrated to the contract-local verb shape; the other half (`signal-persona-mind`, `signal-persona-router`, `signal-persona-message`, `signal-persona-introspect`, `signal-persona-system`, `signal-persona-terminal`, `signal-persona-harness`, `owner-signal-persona-terminal`, `signal-criome`, `owner-signal-repository-ledger`) still carry the old universal-verb shape (`Assert/Match/Subscribe/Retract/Mutate` prefixes) — every one of them is its own bead (`primary-aunn`, `primary-c620`, `primary-e1pm`, `primary-gu7t`, `primary-k2mh`, `primary-krbi`, `primary-li7a`, `primary-mdhj`, `primary-ojxq`, `primary-qjdp`, `primary-21gn`, `primary-0bls`, `primary-9up1`).

Additional partial work:
- `primary-x3ci` — Spirit cutover to v0.1.1 (the active blocker per /280 §3 Open critical point 5)
- `primary-chpq` — Spirit default wrapper dual-writes during version migration
- `primary-qk04` — Multi-version persona-spirit daemon coexistence in CriomOS-home
- `primary-l3h5` — sema-upgrade daemon + thin CLI promotion (current temp CLI satisfies migration 1 only)
- `primary-hj4`/`primary-hj4.1` — persona-mind: channel choreography, subscriptions, suggestions + typed mind graph from /152
- `primary-ihee` — Horizon rewrite: combine leaner shape with re-engineering
- `primary-sff` — lojix: extract lojix-core, add lojix-daemon, create signal-lojix
- `primary-at7x` — criome: finish routed authorization after coordinator skeleton

## Designed but not started

Reports name the shape; no code exists in the implementing repo.

| Subject | Design home | Code status |
|---|---|---|
| Persona-Pi triad (daemon + CLI + signal + owner-signal contracts) | /266, /268 (operator input) | No `persona-pi` repo exists in `/git/github.com/LiGoldragon/`. Composite-designer flow (intent 45) names Codex-on-Pi as the Codex side of designer parallelism, but the harness adapter is unwritten. |
| Forge family (forge-core + forge-nix-builder + signal-forge) | /271, /274 (forge skeleton reconciliation) | `signal-forge` exists as a contract skeleton (`87882b6` "align ARCH with three-layer model"); `forge` repo exists as a build daemon (per `protocols/active-repositories.md`) but per intent record 154 stays as the criome-stack executor with forge-nix-builder extracted as library underneath; no forge-core yet. |
| Schema-spec language + version-hash mechanism | /263 (initial), /279 (deeper) | Designer-only. Records 29, 80, 107, 112 settled the direction (NOTA schema language; Blake3 content-addressable hash IS version identity). No language implementation, no hashing code. Open question 1 in /280 (self-upgrade bootstrap). |
| Multi-version daemon coexistence pattern (system-wide) | /278 | Spirit-specific shim deployed via CriomOS-home; the pattern as a universal mechanism is designer-only. Per /280 §6 a system-specialist bead is filable once verification path chosen. |
| Engine-manager Axis 2 (internal module rename: supervisor → engine-manager) | /280 §3 Open critical point 4 | 17 `supervision_socket_*` identifiers + 8 `.supervision.sock` constants + ~30 ARCH lines unrenamed. Bead `primary-k2mh` does NOT list this axis. |
| Tap/Untap mandatory observability for all persona components | intent/component-shape.nota 2026-05-20T02:00Z | Only spirit's contract exposes the observable block per /257 §1.5; the other 17 contracts don't. Per `primary-u8vo` epic. |
| Criome-mediated authorization for signal-lojix | intent/deploy.nota 2026-05-17T15:30 + 2026-05-20T17:10 (psyche deferred from migration arc) | Bead `primary-at7x` is the next slice; no code wires criome-daemon as a Signal client yet. |
| Per-agent Criome identity (BLS12-381 keypairs; key IS the identifier) | Intent records 38, 39, 125, 134 (corrected from Ed25519 to BLS) | Designer-only — no agent has a BLS identity today. Pre-Criome transitional path also unimplemented. |
| Role-vector lane registry (`[PersonaSignal Designer]` shape) | Intent records 97, 98, 99, 117, 118; reports/second-designer/146, /147, /149, second-operator/163 | First lane-registry slice implemented (`50ed6f7`), but the role-vector form and persistent monotonic counter are not yet realized in code. |
| Skill-loading via persona-mind (skills live in mind; agents fetch bundle on boot) | Intent record 70 + persona.nota 2026-05-20T17:30 (Decision) | Designer-only. Mind has no skill store today. |
| Spirit guardian (negation/lowering/escalation judge) | intent/persona.nota 2026-05-19T15:30Z + 17:30Z; awaits "multi-agent auditing arc" | Designer-only; the auditing arc itself is undefined per /249 Gap #8. |
| Filesystem intent projection (spirit's `intent/*.nota` → spirit-mediated) | /232 §7 (retired, substance in skills); /280 §"Side notes" | Designer-only; intent files still authoritative for the seven `High` legacy records. |
| Schema migration via in-process versioned reads | Intent record 21 + /273 | Designer-only; the per-record schema-version tag mechanism unimplemented across every component. |
| Composite designer role (Claude + Codex parallel against same prompt) | Intent record 45 (Medium); /264 protocol + role spaces | Designer-only; today's "parallel" is just two designer chairs (prime + second), not the Codex side. |
| LLM call as default-provider + ordered-fallback chain | Intent record 40 | Designer-only. |
| `cluster-operator` lane | Intent record 156 (already a reports dir exists but the skill file etc. not yet) | First-ish step: the dir exists at `/home/li/primary/reports/cluster-operator/`. No skill file. |

## Newly decided this session — no design or code yet

These were logged today (2026-05-22) and have no downstream design yet. Flagged explicitly per the dispatch.

| Component / direction | Spirit record | Status |
|---|---|---|
| `persona-llm-client` | 157 (corrects 151), 158 | Workspace-native lightweight LLM client library, embeddable directly in daemons. DeepSeek V4 first endpoint. **No repo exists. No design report exists.** Supersedes the earlier "DeepSeek subsumed into persona-pi" direction; /281 explicitly retracted its TL;DR recommendation in response. |
| `persona-listen` | 159 | Audio input component. Counterpart to `persona-speak`. No repo, no design report. |
| `persona-speak` | 159 | Audio output component. Counterpart to `persona-listen`. No repo, no design report. |
| `signal-real-time` (or signal-core extension) | 160, 161, 162 | Real-time streaming as a new Signal capability. Per record 161 Signal Core "still exists as a concept" (the prior rename moved content out, not the namespace itself); per record 162 signal-real-time is Signal, not Sema, and the storage format for real-time data is open (probably native real-time format). No repo, no design report. |

**Additional recent records (140-162) without downstream design:**

- Record 148 — DeepSeek-as-library via Pi harness (superseded by 157/158 but design hasn't caught up)
- Record 150 — Possible `persona-operator` role for persona-stack maintenance and renaming work (Medium)
- Record 156 — `cluster-operator` lane as specialized live-system-maintenance lane
- Record 153 — Deploy operation moves from signal-forge to signal-lojix (design impact across both contracts not yet captured)
- Record 154 — Existing forge daemon stays as criome-stack executor; forge-nix-builder extracts as library underneath rather than replacing forge — refines /271 / /274
- Record 144 — track which reports were read (no mechanism designed)
- Record 137 — agent checkout should drive commits (no mechanism designed)
- Record 138 — claims start from clean checkout (composes with 137)
- Record 124, 125 — runtime functions vs long-lived agents distinction; BLS-from-day-one (corrects 134); /281 superseded its own recommendation in light of 157

## The 35 gaps from /249 — current status

Status legend: **C** closed; **P** partial; **O** still open.

| # | Gap | Status | Evidence |
|---|---|---|---|
| 1 | Spirit→mind owner-contract verb set open | O | Still no `owner-signal-persona-mind` operations defined for spirit-issued orders. |
| 2 | Owner-graph apex disambiguation (supervisor identity) | P | Engine-manager rename clarified the wire surface (`4e92889`) but Axis 2 still ambiguous (/280 §3 Open critical point 4). |
| 3 | persona meta-repo has no INTENT.md | O | No `INTENT.md` created in `/git/.../persona/`. ARCHITECTURE.md remains the single 1513-line surface. |
| 4 | persona-introspect universal observer-hook vs Tap/Untap | C | Resolved by spirit record (from `intent/component-shape.nota`) 2026-05-21T10:00:00Z "of course! debug the debugger!" — Tap/Untap mandate applies to introspect equally. |
| 5 | persona engine-manager triad-status undefined | P | Engine-manager rename names the manager as "engine_management" first-class wire vocabulary; explicit affirmation as a real triad in workspace intent still unstated. |
| 6 | persona-system unpause criteria | O | persona-system stays paused; no intent on triggers. |
| 7 | HarnessKind closed-enum vs data-table tension | O | No intent recorded; harness ARCH unchanged. |
| 8 | Spirit guardian / multi-agent auditing arc undefined | O | No intent records on the auditing arc. |
| 9 | 5 missing owner-signal-* repos emergence criteria | O | Same five missing (mind, router, harness, message, system) — note `owner-signal-persona-mind`, `owner-signal-persona-router` DO exist now per `ls` of `/git/github.com/LiGoldragon/`. **Updated count: 3 missing** (harness, message, system). |
| 10 | Spawn order beyond "spirit last" | P | Intent record 111 added: sema-upgrade-daemon boots first. Order between supervisor and spirit still designer-only. |
| 11 | Mutate-chain partial-failure semantics | O | No intent. |
| 12 | Skeleton honesty for ordinary + owner contracts | O | No intent. |
| 13 | Single-argument-rule violation in harness `--kind` flag | O | No fix. |
| 14 | Concept designer's relationship to spawn order | P | Intent record 147: "Concept designer is an ephemeral occasional invocation, not a persistent named lane" — resolves the lane question. Spawn-order relationship still open. |
| 15 | Mind→orchestrate concrete authority handoff | O | Lane-registry first slice (`50ed6f7`) is data-only; no mind-side caller. |
| 16 | bootstrap-policy.nota content per component | O | Only spirit has psyche-named content. |
| 17 | Filesystem-projection cutover | O | Intent file substrate still authoritative for `High` records. |
| 18 | Cross-component observer correlation via DeliveryTraceKey | O | Designer-only. |
| 19 | Engine-per-spirit vs shared spirit | O | Implicit; no intent. |
| 20 | Cross-engine federation scope | O | No intent. |
| 21 | Statement payload canonical example | P | Spirit production payload is `Entry` shape; works in practice. Canonical reference in spirit ARCH still thin. |
| 22 | ChannelMessageKind enumeration | O | Unchanged. |
| 23 | Channel duration rationale | O | Unchanged. |
| 24 | Component restart policy after crash | O | Unchanged. |
| 25 | Subscription consumer-driven demand specifics | O | Bead `primary-hj4.1.4` is the slice but design unfinished. |
| 26 | MessageProxy retirement naming | P | Bead `primary-devn` partially complete. |
| 27 | Fixture HarnessKind variant for tests | O | Unchanged. |
| 28 | Auth identifier naming (`EngineId` vs `Identifier`) | O | Unchanged. |
| 29 | memory_graph transitional vs typed mind-graph | P | Bead `primary-hj4.1` is the typed mind graph slice. |
| 30 | Recursive observation (spirit observes itself via Tap) | C | Implicitly resolved by Gap #4 closure (debug-the-debugger). |
| 31 | Multi-OS port for persona-system | O | Unchanged. |
| 32 | Cell-vs-supervisor consolidation completion (terminal) | O | Still transitional. |
| 33 | What rejects a router message besides "channel inactive" | O | Unchanged. |
| 34 | External (non-Owner) message submission paths | O | Unchanged. |
| 35 | Multi-operation request execution per component | O | Unchanged. |

**Summary: of 35 gaps, 3 closed (Gaps 4, 30, partly 14), 8 partial, 24 still open.** The bulk of design effort the last 36 hours went into NEW concerns (schema migration, sema-upgrade, Magnitude, multi-version coexistence, role-vector lanes, persona-pi, persona-llm-client, real-time signal) rather than closing /249. Several of those new concerns are downstream of gap closure direction (#21, #25, #26, #29).

## Most important unresolved questions

Ordered by blocking weight. Each is a one-line proposition with the design home that surfaces it.

1. **Spirit v0.1.1 cutover gating sequence — six steps; should the `operator/spirit-response-protocol` branch be force-merged-to-main given the intent record 109 violation?** — /280 §3 Open critical point 5. Active blocker; seven `High` records stuck.

2. **Multi-version verification choice: run v0.1.0 and v0.1.1 side-by-side before flipping default symlink, or single-daemon swap with backup as fallback?** — /280 §3 Open critical point 6; intent record 113 Medium-certainty pending.

3. **Sema-upgrade daemon shape and self-upgrade bootstrap: recursive self-application or hand-written bottom-of-stack?** — /280 §3 Open critical point 1; bead `primary-l3h5`. Knock-on into the schema-spec language /263 + /279.

4. **persona-llm-client design: how does an embedded LLM client library reconcile with the daemon-per-component triad discipline? Is it a library (no daemon, no triad) or a triad with its own contract?** — Spirit records 157, 158. Brand new, undesigned.

5. **persona-listen + persona-speak: are these full triads, paired-via-real-time-signal? What is signal-real-time's storage shape (native format vs Sema)?** — Spirit records 159, 160, 161, 162. Brand new, undesigned.

6. **Engine-manager rename Axis 2: land-now (one clean pass with socket-rename + Nix update; ABI break candidates) or hold-explicitly (intentional deferral, recorded)?** — /280 §3 Open critical point 4. Bead `primary-k2mh` doesn't currently list this axis.

7. **Health/Readiness collapse onto Magnitude: field-name-carries-dimension (`health: Magnitude`) or separate universal `Health`/`Readiness` types as siblings of Magnitude?** — /280 §3 Open critical point 2; intent record 70's parenthetical authorises but leaves the call.

8. **Commit-sequence scope: per-database (one per sema database) or per-component (one across all of a component's redb tables)?** — /280 §3 Open critical point 3; designer lean is per-database.

9. **The 5 (now 3) missing owner-signal-* repos emergence criteria: under what condition does each get created? The crystallisation rule is unwritten.** — /249 Gap #9. Still no criterion.

10. **Spirit-to-mind owner-contract verb set: psyche stated "spirit owns mind" and "develops as it develops"; no concrete starting list.** — /249 Gap #1. Blocks the moment integration begins.

## References

### Intent record numbers (load-bearing on the above)

- Record 5 — no-subagents-default workspace constraint
- Record 21 — schema-version tag on every record (per-record versioning)
- Record 29 — schema-layout schema in NOTA-based language; content-addressable
- Record 38, 39, 125, 134 — per-agent Criome identity; BLS12-381
- Record 41 — Nix-flake-versioned upgrade protocol
- Record 56 — fast-cadence migration aim
- Record 57 — designer protocol parallel-subagents authorisation
- Record 70 — universal Magnitude type (7-9 rungs; field-name-carries-dimension)
- Record 71, 90, 91 — sema-upgrade as universal stateful schema upgrade mechanism
- Record 72 — sema database vocabulary
- Record 73 — branches/leaves vocabulary
- Record 74, 75 — forge family; workspace-owned content-addressed vertical stack
- Record 93 — lane management moves from `tools/orchestrate` to `persona-orchestrate`
- Record 97, 98, 99 — role-vector lane registry shape
- Record 108 — reports gain kind + topic dimension
- Record 109 — no feature branches by default
- Record 111 — sema-upgrade-daemon starts FIRST on engine boot
- Record 112 — schema-version hash IS canonical version identity (Blake3)
- Record 113 — multi-version daemon coexistence (Medium)
- Record 114, 115 — versioned sockets, versioned CLIs
- Record 124, 125 — agents vs runtime functions; BLS-from-day-one
- Record 145 — start using spirit v0.1.1 after database update
- Record 146 — ItemPriority collapses onto Magnitude
- Record 148, 151, 157, 158 — DeepSeek/persona-llm-client direction (records 148→151 superseded by 157)
- Record 152 — workspace stack name = "the Criome stack"; "Persona engine" = AI-work part
- Record 153, 154 — Deploy moves to signal-lojix; forge stays as criome-stack executor with forge-nix-builder underneath
- Record 156 — cluster-operator specialized lane
- Record 159, 160, 161, 162 — persona-listen + persona-speak; signal-real-time

### Keeper reports

- Foundational: /214 (Criome), /234 (concept-designer), /249 (35-gap inventory), /257 (signal contracts audit), /263, /264 (protocol + role spaces), /266 (persona-pi triad), /268 (persona-pi operator input), /269 (universal Magnitude), /270 (sema-upgrade component), /271 (forge family), /273 (schema-migration synthesis), /274 (forge skeleton reconciliation), /278 (multi-version daemon coexistence), /279 (NOTA schema language + version hash), /280 (handover), /281 (headless Pi research; partially superseded).
- This snapshot: /282.

### Active beads

- 50 open beads, 6 in-progress (per `bd list`).
- High-priority blockers: `primary-51pn` (P0 whisrs bug), `primary-x3ci` (Spirit cutover), `primary-l3h5` (sema-upgrade daemon), `primary-2y5` (persona engine-manager daemon).
- Migration epic `primary-u8vo` covers the 10 remaining contracts.

### Production pins (from CriomOS-home/flake.lock)

- `lojix-cli`: `ec8f7211675096572cb8894f7610b8a805dd597d`
- `persona-spirit-v0-1-0`: `694452add7734d0b00954a0d7d4d46bb5d776065`
- `persona-spirit-v0-1-1`: `e137f5de4c663b0cb9a8b52f87d9bdadff80841f`

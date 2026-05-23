# 164 — Operator refresh, audit, and meta-overhaul pickup context

*Kind: Context maintenance + audit · Topic: operator-meta-overhaul-readiness · Date: 2026-05-23 · Lane: operator*

*Prompt classification: the psyche instruction for this lane was to refresh operator-relevant skills, audit recent operator work, use Spirit plus the latest operator/designer reports, and build context for Designer's upcoming bead pool from `reports/designer/310-meta-overhaul-booking-roadmap.md`. The follow-up prompt, "continue", adds no new durable psyche intent by itself, so no new Spirit record was captured for this turn.*

## What was refreshed

Authority and role substrate:

- `ESSENCE.md`, `INTENT.md`, root `AGENTS.md`, `repos/lore/AGENTS.md`, and `orchestrate/AGENTS.md`.
- Operator lane skills: `skills/operator.md`, `skills/role-lanes.md`, `skills/autonomous-agent.md`, `skills/reporting.md`, `skills/beads.md`, `skills/jj.md`, `skills/feature-development.md`, and `skills/repository-management.md`.
- Operator implementation skills: naming, Rust discipline and subskills, Nix discipline/usage, testing, component triads, contract repos, actor systems, Kameo, architecture editing, architectural truth tests, NOTA design/schema/comments, micro-components, language design, push-not-pull, abstractions, and beauty.

Spirit was queried through the deployed `spirit` CLI. The live records most relevant to the upcoming work are:

- Signal records 244, 251, 271, 272, 273, 326, 327, and 328: three-tier signal sizing, root-verb byte layout, universal sub-variants, per-component namespace correction, golden-ratio owner/public section split, and 64-bit micro prefix on every frame.
- Component-shape records 263, 265, 266, 267, 268, 270, 280, 309, and 310: Help operations, `signal_cli!` with caller context, binary naming, supervised-component prefix removal, persona-sema deletion, and the separate `agent` component direction.
- Persona records 260, 304, 305, 329, and 330: spirit-per-engine, persona-pi creation and Nix packaging boundary, agent abstraction over backends, and router delivery becoming durable only after harness-side acknowledgement.
- Operator records 49, 94, 135, and 136: operator should become a targeted Persona role, implement clear designer-downstream work in parallel, watch new designer reports, and operator/second-operator are one identity.

Report inputs:

- Latest operator reports `reports/operator/157-*` through `reports/operator/163-*`.
- Designer reports `reports/designer/297-*` through `reports/designer/310-*`, especially `/305-v2`, `/307`, `/308`, `/309`, and `/310`.
- Designer audit `reports/designer/302-audit-recent-operator-work-2026-05-23.md`.
- Second-designer audit `reports/second-designer/161-design-cascade-and-context-sweep/4-operator-audit-against-current-design.md`.
- Second-operator refresh `reports/second-operator/171-context-maintenance-refresh-2026-05-23.md`.

Working-copy status: the primary workspace already contains uncommitted designer/system-designer files. This report should not be committed with a broad `jj commit`; split it explicitly if committing later.

## Audit of recent operator work

### Strong alignment

The operator has shipped a large amount of design-aligned foundation work since the last operator report.

1. Reports `/157` through `/163` establish a coherent version-handover stack: `version-projection`, `signal-version-handover`, `sema-engine` `CommitSequence`, the Spirit smart-handover sandbox, the private Spirit handover socket, owner version-handover authority, and the systemd-backed `UnitController` position.
2. The 2026-05-23 code window, audited by designer and second-designer, aligns with current design in substance: Persona FD-handoff routing, real Spirit handover through the daemon, spirit-per-engine wiring, origin/Identifier renames, `signal_cli!` macro adoption, signal-persona contract splitting by socket authority, systemd process-supervision work, persona-pi scaffolding, and the persona-orchestrate divergence ledger.
3. The strongest implementation pattern remains the Nix witness discipline: reports cite `nix flake check --option max-jobs 0 -L` and many commits landed with direct cargo/Nix witnesses.
4. The operator is keeping pace with designer intent quickly. Several code slices landed within hours of the relevant Spirit records and designer reports.

### Gaps and drift

The main drift is not design alignment; it is traceability.

1. `primary-e2bc` (operator report-gap for three named structural commits) and `primary-dnxf` (operator report-gap addendum covering roughly 30 later commits across eight repositories) are both open. The last operator report before this one is `/163`, dated 2026-05-22, while the largest operator coding window is 2026-05-23.
2. This report does not close those gap beads. They ask for per-repo or per-commit-family coverage naming the closing bead, intent records, Nix witness, and why. Coverage should be filed separately so future agents can navigate each implementation family without bead archaeology.
3. The rename gap called out by designer `/302` has changed shape. At `/302` time, new code was still using `EngineId` and `signal_persona_auth`; by second-designer `/161`, the active source had largely completed the Identifier and origin rename. The remaining issue is now report trace and the larger persona-prefix rename surface, not the old auth/origin code drift.
4. Several witness gaps remain from second-designer `/161`: engine-management socket round-trip test, two-version FD-handoff sandbox, new `signal-persona-engine-management` end-to-end witness, persona-pi `/nix/store` hiding constraint, quarantine/recovery cross-product, and generated-CLI behavior drift checks.
5. Shipping blockers remain: Spirit v0.1.0 protocol-aware maintenance build, residual mirror/projection/divergence verification, persona-sema deletion, persona-prefix rename coordination, and the new agent/persona-agent abstraction wave.

## Upcoming bead pool from designer `/310`

Designer `/310` books five waves. The operator-relevant first pickups are the foundation beads that unblock the rest.

### Wave 1 critical path

Golden-ratio namespace split:

- `primary-li0p` — `signal-frame` adds `NamespaceSection`, `SECTION_CUTOFF = 100`, and `classify(byte)`.
- `primary-v5n2` — `signal-frame-macros` accepts `contract_section` grammar and allocates discriminators within the Small/Big ranges.
- `primary-avog` — `signal-frame` or `signal-frame-macros` adds `assert_triad_sections!`.
- `primary-muu2` — persona triad pilot adopts `contract_section` discipline.
- `primary-g21y` — later workspace sweep after persona pilot.

Pre-typed envelope and tap-anywhere:

- `primary-2cjv` — `signal-frame` reshapes `ExchangeFrame` and `StreamingFrame` to `{ micro: u64, body }`.
- `primary-3cl1` — `signal-frame-macros` emits `frame_micro()` projection per channel.
- `primary-bann` — `persona-spirit-daemon` emits `socket_ingress` tap events.
- `primary-145a` — `persona-introspect` subscribes to the first tap stream.

Agent component triad:

- `primary-gvgj.1` — new `signal-persona-agent` ordinary contract.
- `primary-gvgj.2` — new `owner-signal-persona-agent` policy contract.
- `primary-gvgj.3` — new `persona-agent` daemon skeleton.
- `primary-gvgj.4` through `.8` — five backend daemons: Claude, Codex, Pi, Gemini, OpenCode.
- `primary-gvgj.9` — router migrates to the agent socket.
- `primary-gvgj.10` — retire `persona-harness-daemon` after backends and router cutover.

Independent macro-pivot work:

- `primary-915w` (signal_cli foundation) is closed.
- `primary-uxq1` (persona-spirit first proof) is closed.
- `primary-uq04` (remaining CLI sweep) is open and partially decomposed; its comments say many children are blocked by older contract shapes, not by simple mechanical edits.
- `primary-8r1j` (Help auto-injection through `signal_channel!`) remains an open P1 macro task.

### Best first pickups, after coordination

If the psyche authorizes a parallel operator wave, the highest-leverage first beads are:

1. `primary-li0p` — smallest unlock for the golden-ratio chain.
2. `primary-2cjv` — unlocks frame-micro projection and tap-anywhere work.
3. `primary-gvgj.1` — ordinary persona-agent contract.
4. `primary-gvgj.2` — owner persona-agent contract.
5. `primary-avog` — quick helper after `NamespaceSection` exists.

Caution: `primary-li0p` and `primary-2cjv` both touch `signal-frame`, so they should not be edited concurrently in the same working copy. Use isolated worktrees or sequence them. The two persona-agent contract beads are greenfield/new-repo shaped and are safer parallel work.

## Critical coordination finding: BEADS dependency directions are inverted

The textual bead descriptions and designer `/310` agree on the critical path, but the BEADS dependency graph is currently unreliable for this pool.

Observed examples:

- `primary-li0p` says in prose that `NamespaceSection` unblocks `primary-v5n2`, but `bd show primary-li0p` lists `primary-v5n2` under `DEPENDS ON`.
- `primary-2cjv` says in prose that the frame reshape unblocks `primary-3cl1` and `primary-bann`, but `bd show primary-2cjv` lists those downstream beads under `DEPENDS ON`.
- `primary-gvgj.1` and `primary-gvgj.2` are the contracts that should precede the daemon skeleton, but `bd show` lists the skeleton `primary-gvgj.3` as their dependency.
- `primary-gvgj.3` should precede the five backend daemons and router migration, but `bd show primary-gvgj.3` lists the backend/router beads as dependencies.
- Closed beads `primary-915w` and `primary-uxq1` already contain close notes saying dependency inversion forced manual closure.

Conclusion: do not rely on `bd ready` or dependency-blocked status for this bead pool until the graph is repaired. Treat the prose in designer `/310`, reports `/307`-`/309`, and each bead's body as authoritative. A small coordination slice should fix the BEADS dependency directions before operators start using `bd ready` as the scheduler.

## Operator execution discipline for the upcoming wave

1. Claim exactly one bead or one repo/report scope with `tools/orchestrate claim operator ... -- "reason"` before editing. Release on handoff.
2. Do not dispatch subagents from this operator lane unless the psyche explicitly asks for operator subagents for the coding wave. If subagents are authorized, use a meta-report directory under `reports/operator/` and brief each subagent on the headless `jj` rule.
3. For code work, write the short operator report before or with the commit. Each report should name the bead, intent records, design report, Nix witness, and the reason the shape was chosen.
4. Every `jj` command that can open an editor must carry an inline message (`-m ...` or the documented inline alternative). Never let `jj` prompt for an editor.
5. Prefer Nix witnesses for cross-repo work. Use `CARGO_BUILD_JOBS=2 cargo test` for fast local crate validation when appropriate, then `nix flake check --option max-jobs 0 -L` for the reportable witness.
6. Keep old-name usage from accumulating. If a rename is filed and not yet implemented, avoid adding new references to the old name unless the bead explicitly requires compatibility shims.

## Recommendations

1. First coordination fix: repair the inverted BEADS dependency graph for `/310`'s new beads, or at least document that the graph is inverted so operators do not skip the real roots.
2. Run report-gap coverage in parallel with the coding wave. `primary-e2bc` and `primary-dnxf` should not block all implementation, but they should not be buried under the next 20 commits either.
3. Start implementation with the true roots: `primary-li0p`, `primary-2cjv`, `primary-gvgj.1`, and `primary-gvgj.2`. Sequence the two `signal-frame` roots carefully; parallelize greenfield contract repos instead.
4. Treat `primary-8r1j` Help operations as a macro-layer sibling to the frame/namespace work, not as cleanup. It proves the same cross-component auto-injection pattern that `signal_cli!` just proved.
5. Keep designer `/310` as the controlling roadmap, but carry forward the second-designer `/161` audit gaps as witness/reporting work so the wave does not become code-only.

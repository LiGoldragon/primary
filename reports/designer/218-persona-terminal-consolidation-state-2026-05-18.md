# 218 — Persona-terminal consolidation state (2026-05-18)

*Topic compendium for the persona-terminal consolidation arc. Part of
the 2026-05-18 workspace state-of-art series. Master index lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

The persona-terminal consolidation is **shape-designed but not
implementation-complete**. Canonical design:
`reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md`
— collapse the current 10 binaries to 3, one component daemon
supervising N internal `TerminalCell` actors, sema-engine `sessions`
registry, library-only consumption of `terminal-cell` at the production
path.

The contract surface has **split**. Ordinary reads (`ListSessions`,
`ResolveSession`) live in `signal-persona-terminal`; owner-only
lifecycle (`CreateSession`, `RetireSession`, `SessionCreated`,
`SessionRetired`) now lives in the new `owner-signal-persona-terminal`
repo (operator/135, commits across five repos). The owner-chain
`persona-orchestrate → persona-harness → persona-terminal` is settled.

**Blocked**: actual implementation of `CreateSession`/`RetireSession`
(returns `OwnerTerminalRequestUnimplemented::NotBuiltYet` skeleton);
owner-terminal Unix socket listener (only Kameo actor message path
exists); supervisor → daemon consolidation (both
`persona-terminal-daemon` and `persona-terminal-supervisor` still
ship); CLI collapse (10 binaries still in Cargo.toml); terminal-cell
`-test` suffix renames.

---

## 2 · Load-bearing reports

| Path | Carries |
|---|---|
| `reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md` | Canonical shape: actor topology, sema schema, socket lifecycle, witness tests, migration sequence, §11 questions (most resolved). |
| `reports/operator/134-terminal-orchestrate-porting-decisions-2026-05-17.md` | User-approved decisions ledger (clean-slate restart; CreateSession=Mutate; communication/supervision rename; orchestrate authority chain; same-UID prototype). |
| `reports/operator/135-owner-terminal-signal-surface-2026-05-17.md` | Owner-signal split landed: five-repo commit chain; `TerminalSupervisorOwnerRequest` actor wired; honest skeleton behavior in place. |
| `reports/designer-assistant/117-review-operator-134-terminal-orchestrate-porting-decisions-2026-05-17.md` | Review with self-supersession header (operator/135 landed the recommendations). |
| `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md`, `/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md` | Owner-contract pattern feeding /211/117/135. |
| `reports/designer/210-component-triad-decisions-and-mutate-authority-2026-05-17.md` §4 | Names the triad violation + consolidation direction; upstream. |
| `skills/testing.md` §"Test-only binaries — the `-test` suffix" | Resolved Q2; canonical convention now in skills. |

---

## 3 · Stale / superseded reports

| Path | Status | Why |
|---|---|---|
| `reports/designer-assistant/13-terminal-cell-relay-architecture-failure.md` | Stale | Rejected actor-relay live-viewer path; fix (abduco-like raw byte data plane) has long since landed in `terminal-cell/ARCHITECTURE.md` §1.2. Historical evidence only. |
| `reports/designer-assistant/14-terminal-cell-architecture-review.md` | Stale | Described `terminal-cell` as "production-shape belongs in persona-terminal"; /211 formalized that as `terminal-cell` library only at production, standalone daemon test-only. Substance in `terminal-cell/ARCHITECTURE.md` §0 + `persona-terminal/ARCHITECTURE.md`. |

---

## 4 · Binary inventory (current vs target)

`persona-terminal/Cargo.toml` declares **10** `[[bin]]` entries.
`terminal-cell/Cargo.toml` has **10 binaries** auto-discovered in
`src/bin/` (default `autobins = true`).

| Binary | Repo | Plane | Target | Needs `-test`? |
|---|---|---|---|---|
| `persona-terminal-daemon` | persona-terminal | daemon | reshape as triad daemon | no (production) |
| `persona-terminal-supervisor` | persona-terminal | daemon | retire | n/a |
| `persona-terminal-view` | persona-terminal | data | dial daemon for `ResolveSession` | no (production) |
| `persona-terminal-send` | persona-terminal | data | merge into `-view`? (Q4 open) | n/a |
| `persona-terminal-{capture,type,sessions,resolve}` | persona-terminal | control | subsumed by canonical `persona-terminal` CLI | n/a |
| `persona-terminal-signal` | persona-terminal | control | renamed `persona-terminal` (canonical CLI) | no |
| `persona-terminal-validate-capture` | persona-terminal | check | `persona-terminal-validate-capture-test` or Cargo `tests/` | **yes** |
| `terminal-cell-daemon` | terminal-cell | daemon (test) | `terminal-cell-daemon-test` | **yes** |
| `agent-terminal-fixture` | terminal-cell | fixture | `agent-terminal-fixture-test` | **yes** |
| `output-flood-fixture` | terminal-cell | fixture | `output-flood-fixture-test` | **yes** |
| `terminal-cell-{send,capture,wait,exit,resize,view,session-select}` | terminal-cell | client (test) | most `-test`; review each | **yes** for non-production |

Target production-path binary count: **3** (`persona-terminal-daemon`,
`persona-terminal`, `persona-terminal-view`). The `-test` suffix
witness `<repo>-test-only-binaries-have-test-suffix` named in
`skills/testing.md` but not yet implemented as a Nix check.

---

## 5 · Contract split status

### `signal-persona-terminal/ARCHITECTURE.md` (ordinary)

- `ListSessions` → `Match`, `ResolveSession` → `Match` (added).
- **No** `CreateSession` / `RetireSession` variants.
- §6 constraint: "Session lifecycle mutation is owner-only, not part of
  the ordinary terminal contract" with source-scan witness.
- §9 names "No owner-only terminal session lifecycle commands. Those
  are `owner-signal-persona-terminal`."

### `owner-signal-persona-terminal/ARCHITECTURE.md` (owner)

- `CreateSession` → `Mutate`, `RetireSession` → `Retract`.
- Replies: `SessionCreated`, `SessionRetired`, `OwnerTerminalRequestUnimplemented` (`NotBuiltYet`).
- Imports `TerminalName`, `TerminalExitStatus`, `WirePath` rather than duplicating.
- Source carries no runtime (no Kameo / Tokio / redb).
- §0 owner chain: `persona-orchestrate → persona-harness → persona-terminal → terminal-cell library`.

---

## 6 · Open questions (/211 §11 status)

### Resolved

- **Q1 — Daemon-restart session continuity**: clean-slate restart first; pidfd re-adoption deferred (operator/134).
- **Q2 — terminal-cell-daemon status**: keep as test-only; rename `terminal-cell-daemon-test`; canonical `-test` convention added to `skills/testing.md`. Witness named.
- **Q3 — persona-terminal-validate-capture placement**: default to `-test` suffix; further callers-audit deferred to operator (operator/134 marks it "test/check witness, not production runtime").
- **Q5 — CreateSession verb**: `Mutate` (operator/134 + owner ARCH).

### Open / non-blocking

- **Q4** — does `persona-terminal-view` absorb `persona-terminal-send`? /211 prefers "keep both for now"; no update.
- **Q6** — two sockets (communication + supervision) vs one. /211 preferred two; operator/134 recorded rename; `persona-terminal/ARCHITECTURE.md` now uses two-socket framing canonically. **Effectively closed**, but a third "owner terminal socket" is now a third surface (operator/135 next-work item 1). /211's Q6 framing is partially superseded by the owner-socket arrival.

### New (surfaced post-/211)

- **Owner-terminal socket path** — `${XDG_RUNTIME_DIR}/persona-terminal/owner.sock`? Co-located in harness? Designer attention before operator lands the listener.

---

## 7 · Implementation state

### Landed (per operator/135)

- `owner-signal-persona-terminal` repo created; contract surface complete; round-trip tests pass.
- `signal-persona-terminal` extended with `ListSessions` / `ResolveSession`; `CreateSession` / `RetireSession` removed from ordinary surface.
- `persona-terminal` has a `TerminalSupervisorOwnerRequest` Kameo message path returning typed `OwnerTerminalRequestUnimplemented { reason: NotBuiltYet }`.
- `persona-terminal` apex flake updated; both contracts in `Cargo.toml`.
- `protocols/active-repositories.md` records the new owner contract.
- All `nix flake check` and `cargo test` passed (operator/135 §4).

### Stubbed / not yet

- **Owner-terminal Unix socket listener** in `persona-terminal` — only actor-message path; no bound socket file accepts owner frames.
- Real `CreateSession` execution: reserve name → spawn TerminalCell child → commit session row → return `SessionCreated { name, data_socket_path }`.
- Real `RetireSession`: typed shutdown ordering + terminal-cell cleanup + archive row commit.
- **Daemon consolidation** — `persona-terminal-supervisor` still separate; actor tree per /211 §3 not yet realized.
- **CLI collapse** — 6 control-plane CLIs still exist; unified `persona-terminal` CLI does not yet exist.
- `persona-terminal-view` still reads Sema directly per its source; reshape to `ResolveSession` not done.
- terminal-cell `-test` suffix renames + Nix witness check — none implemented.
- Persona sandbox witness for owner-CreateSession-then-ordinary-traffic (operator/135 §6 item 4).

---

## 8 · Recommendations for context maintenance

### Retire

- `reports/designer-assistant/13-terminal-cell-relay-architecture-failure.md`
- `reports/designer-assistant/14-terminal-cell-architecture-review.md`

### Keep with self-supersession headers (already done)

- `reports/designer-assistant/117-review-operator-134-terminal-orchestrate-porting-decisions-2026-05-17.md` — fine as authority-decision audit trail.
- `reports/designer/210` §4 — already notes /211 supersedes the §4 remedy.

### Forward to operator

1. Wire the owner-terminal Unix socket listener + `CreateSession`/`RetireSession` execution (operator/135 §6 items 1-3). **High priority** — `NotBuiltYet` is the current bottleneck for downstream orchestrate integration.
2. Land daemon consolidation per /211 §9 migration sequence (steps 3, 5, 6).
3. Add the persona sandbox witness (operator/135 §6 item 4).
4. Schedule terminal-cell + persona-terminal `-test` suffix renames as a coordinated micro-arc.
5. Decide on owner-terminal socket path (new question /211 §11 doesn't cover).

### Forward to designer

- /211 §11 Q4 (`view` absorbs `send`?) and Q6 (third socket) should get explicit resolution before consolidation lands.

### Skill / ARCH already absorbed

- `skills/testing.md` §"Test-only binaries — the `-test` suffix" — canonical.
- `skills/component-triad.md` — owner-signal surfaces part of triad when privileged authority exists.
- `persona-terminal/ARCHITECTURE.md` — uses communication/supervision split; names owner surface; marks supervisor transitional.
- `terminal-cell/ARCHITECTURE.md` §0 — "production Persona consumes terminal-cell as a library; standalone daemon is local dev/test harness."

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master.
- `reports/designer/219-persona-orchestrate-state-2026-05-18.md` — adjacent (orchestrate → harness → terminal chain).
- `reports/designer/217-component-triad-mutate-authority-state-2026-05-18.md` — adjacent (terminal is the canonical triad-violation case study).
- `reports/designer/220-full-signal-executor-state-2026-05-18.md` — adjacent (recommends persona-terminal as the first executor implementation).

# 222 — Persona engine + Kameo lifecycle state (2026-05-18)

*Topic compendium for the persona engine sandbox + Kameo lifecycle arc.
Part of the 2026-05-18 workspace state-of-art series. Master index
lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

**Kameo lifecycle** is now mostly closed. The forked Kameo lifecycle
contract (`ActorTerminalOutcome` / `wait_for_shutdown` waits for actor
state release before resolving) is implemented, pinned via a stable
`persona-lifecycle-terminal-outcome` branch, and migrated into Persona
components. The discipline lives in `skills/kameo.md` (§"Lifecycle
contract" lines 834-869; §"Blocking-plane templates" lines 873-1018
with the Template 2 supervised-`spawn_in_thread` warning),
`skills/actor-systems.md` §"Release before notify", and `ESSENCE.md`.
Most ephemeral kameo design reports were dropped in commit `a4b12dda`.

**Persona engine sandbox**: the live Pi → managed three-harness route
(`persona-engine-sandbox-terminal-cell-pi-managed-harness-smoke`) lands
in operator/133. A local model invokes the real `message` CLI through a
manager-started topology and delivers `initiator → responder → reviewer
→ owner`. Component-instance ingress sockets are wired. Still in flight:
router bootstrap vocabulary remains in `persona/src/direct_process.rs`
(private NOTA strings) instead of a contract crate; downstream
harnesses are still deterministic fixtures, not live agents; some
shell-grep assertions still pending typed validators.

---

## 2 · Load-bearing reports

| Path | Carries |
|---|---|
| `reports/operator/133-persona-engine-sandbox-slice-and-intent.md` | Current implementation milestone for the live engine route. |
| `reports/operator-assistant/146-follow-up-on-145-after-operator-fixes-2026-05-17.md` | Current OA baseline after the three-harness findings closed. |
| `reports/designer-assistant/114-persona-sandbox-context-maintenance-and-operator-133-audit-2026-05-17.md` | Current DA audit; supersedes earlier sandbox audits (DA/21, /23, /88, /95). |
| `reports/designer-assistant/105-kameo-context-maintenance-2026-05-17.md` | Kameo arc handoff; per its own §5 "retires once substance is absorbed into component architecture docs and `skills/kameo.md`" — substance now in both, retire-candidate-soon. |
| `reports/operator/132-kameo-component-migration-plan.md` | Still the canonical operator migration plan; named in DA/105 as the canonical implementation reference. |

---

## 3 · Stale / superseded reports

### Definitely retire-eligible

| Path | Why |
|---|---|
| `reports/designer/204-kameo-lifecycle-canonical-design-2026-05-16.md` | Substance migrated to `skills/kameo.md` + `skills/actor-systems.md` + `ESSENCE.md`. Companions /205, /206 already retired in commit `a4b12dda`. Last kameo design report on designer side. |
| `reports/operator/108-persona-mind-system-overview.md` | Superseded by `persona-mind/ARCHITECTURE.md`. |
| `reports/operator/109-beads-audit-and-session-discipline.md` | Procedural; dated. |
| `reports/operator/110-persona-meta-integration-start.md` | Pre-/133 scaffolding; superseded by current ARCH + /133. |
| `reports/operator/111-persona-daemon-implementation-review.md` | Pre-/133 scaffolding. |
| `reports/operator/112-persona-engine-work-state.md` | Pre-/133 scaffolding. |
| `reports/operator/113-persona-engine-supervision-slice-and-gaps.md` | Pre-/133 scaffolding. |
| `reports/operator/114-persona-introspect-prototype-impact-survey.md` | Pre-/133 scaffolding. |
| `reports/operator/115-sema-engine-split-implementation-investigation.md` | Self-annotates as historical (12-root vocabulary obsolete; six-root current). |
| `reports/operator/215-hard-context-maintenance.md` | Old maintenance ledger; forward-pointers stale. |
| `reports/operator/216-signal-core-sema-engine-readiness-work.md` | Readiness shipped per sema-engine ARCH. |
| `reports/operator/217-engine-context-maintenance-2026-05-15.md` | Old maintenance ledger. |
| `reports/operator/218-kameo-shutdown-ordering-reproduction.md` | Historical research; substance in `skills/kameo.md`. |
| `reports/operator/219-kameo-upstream-and-shutdown-design.md` | Historical research; substance in skills + fork. |
| `reports/operator/220-kameo-fork-three-shutdown-approaches.md` | Historical research; substance in skills + fork. |
| `reports/operator/221-kameo-push-only-lifecycle-branch-review.md` | Historical research; substance in skills + fork. |
| `reports/operator/222-actor-framework-lifecycle-correctness-research.md` | Historical research; produced canonical design; substance in skills + fork. |
| `reports/operator/223-response-to-da-96-kameo-lifecycle-audit.md` | Implementation report for landed kameo branches; substance now in code + skills. |
| `reports/operator/130-kameo-terminal-lifecycle-implementation.md` | Implementation report; substance in code + skills. |
| `reports/operator/131-kameo-control-plane-lifecycle-work.md` | Implementation report; substance in code + skills. |

### Already retired (jj)

- `reports/designer-assistant/95-104` deleted (file listing confirms); DA/100 was never present. DA/105 explicitly retires their substance.
- `reports/designer/205`, `/206` retired in commit `a4b12dda`.

The only operator reports still load-bearing in this topic: **132, 133, 134, 135** (134/135 cover the adjacent terminal topic — see /218).

---

## 4 · Kameo discipline summary

Permanent in `skills/kameo.md`:

1. **Mailbox** (§"Mailbox", line 698): two factories `mailbox::bounded(64)` (default cap 64; macro doc 1000 is stale) vs `mailbox::unbounded()`. `ask().await` blocks twice (enqueue + reply); use `reply_timeout` to cap.
2. **Supervised actor restart-trap with `.spawn_in_thread`** (§"Blocking-plane templates" Template 2, lines 921-968; Anti-pattern lines 1040-1047): **do not** use `supervise(&parent, …).spawn_in_thread().await` until upstream Kameo grows `pre_notify_links` OR the actor owns its own close-then-confirm protocol. Reason: Kameo signals "child closed" the moment `notify_links` drops `mailbox_rx`, before `Self` (and the resource it owns: redb DB, file lock, socket) is dropped.
3. **Push-not-pull** (§"Test patterns" line 517; §"Lifecycle contract" line 826): "Wait on `ActorTerminalOutcome`, not `is_alive()` or mailbox closure." `outcome.state == Dropped` is the only public signal that owned resources released. Death-signal dispatch must `.await` on the control channel, not `tokio::spawn(...)` fire-and-forget.
4. **Blocking-plane templates** (lines 873-1018): three concrete shapes — Template 1 (`spawn_blocking` + `DelegatedReply` for occasional bursts), Template 2 (dedicated OS thread for frequent sync stores), Template 3 (`tokio::process` + bounded `timeout` + `kill_on_drop` for process-exec). Each names a live reference.

---

## 5 · Persona engine sandbox shape

Design landed (/204 contract + DA/96/98/99 corrections; reports retired); components migrated to the fork (commit chain ending `22514f7c`); live witness running per operator/133 §6: artifact root `/tmp/persona-pi-managed.666FuS`; two Nix checks named explicitly. Cite operator/133 §2 for the boundary diagram and §3 for architecture intent.

---

## 6 · Open questions

- **`primary-alcz` bead is OPEN**: "skills/kameo: sharpen wait_for_shutdown shutdown-ordering warning." Substance has materially landed (`skills/kameo.md` §"Anti-patterns and gotchas" lines 1040-1047; §"Lifecycle contract" lines 836-849). The bead's specific ask — distinguish "wait_for_shutdown, wait_for_shutdown_result, and explicit close-then-confirm" — is not separately written out. **Recommendation: closeable** with a comment pointing to those skill sections, **or** sharpened with one focused paragraph on close-then-confirm vs lifecycle-fork.
- **Router bootstrap vocabulary** (still in `persona/src/direct_process.rs` as private NOTA strings rather than in a contract crate). Named in /133 §8.1 and /114 §"Critique" as the highest-remaining gap. After component-triad + Mutate-authority-direction landings, the gap is sharper.
- **Downstream harnesses still deterministic fixtures**; next live receiver witness pending.

---

## 7 · Implementation state

- **persona-engine**: no `persona-engine` repo at `/git/...`. The "engine" is the topology managed by `persona-daemon` (in `persona` repo) wiring `persona-message`, `persona-router`, `persona-harness`, `persona-terminal`, `persona-mind`, `persona-introspect`, `persona-system`. Smoke witnesses live in `persona` repo.
- **sema-engine**: substantially complete per ARCH. Six-root SignalVerb spine closed; commit machinery typed; read-plan operators (`Constrain`, `Project`, `Aggregate`, `Infer`, `Recurse`) defined.
- **Sandbox witnesses**: live; named Nix checks `persona-three-harness-chain-writes-instance-specific-daemon-configurations`, `persona-three-harness-router-bootstrap-is-manager-written`, `persona-engine-sandbox-terminal-cell-script-builds` all verified in /114.

---

## 8 · Recommendations for context maintenance

### Retire (large batch — substance migrated; safe to drop)

- `reports/designer/204-kameo-lifecycle-canonical-design-2026-05-16.md`
- `reports/operator/108-persona-mind-system-overview.md`
- `reports/operator/109-beads-audit-and-session-discipline.md`
- `reports/operator/110-persona-meta-integration-start.md`
- `reports/operator/111-persona-daemon-implementation-review.md`
- `reports/operator/112-persona-engine-work-state.md`
- `reports/operator/113-persona-engine-supervision-slice-and-gaps.md`
- `reports/operator/114-persona-introspect-prototype-impact-survey.md`
- `reports/operator/115-sema-engine-split-implementation-investigation.md`
- `reports/operator/215-hard-context-maintenance.md`
- `reports/operator/216-signal-core-sema-engine-readiness-work.md`
- `reports/operator/217-engine-context-maintenance-2026-05-15.md`
- `reports/operator/218-kameo-shutdown-ordering-reproduction.md`
- `reports/operator/219-kameo-upstream-and-shutdown-design.md`
- `reports/operator/220-kameo-fork-three-shutdown-approaches.md`
- `reports/operator/221-kameo-push-only-lifecycle-branch-review.md`
- `reports/operator/222-actor-framework-lifecycle-correctness-research.md`
- `reports/operator/223-response-to-da-96-kameo-lifecycle-audit.md`
- `reports/operator/130-kameo-terminal-lifecycle-implementation.md`
- `reports/operator/131-kameo-control-plane-lifecycle-work.md`

That's 20 operator reports + 1 designer report = **21 retire candidates** in this topic alone. Operator subdir would drop from 24 → 4 files.

### Keep

- `reports/operator/132-kameo-component-migration-plan.md` — canonical migration plan referenced by DA/105.
- `reports/operator/133-persona-engine-sandbox-slice-and-intent.md` — current implementation milestone.
- `reports/designer-assistant/105-kameo-context-maintenance-2026-05-17.md` — current pickup point; retire-candidate-soon once next session checks the kameo arc is fully closed.
- `reports/designer-assistant/114-persona-sandbox-context-maintenance-and-operator-133-audit-2026-05-17.md` — current DA audit.

### Bead actions

- `primary-alcz` — close with a comment pointing to `skills/kameo.md` lines 836-849 + 1040-1047, **or** add one short close-then-confirm paragraph as a final polish before closing.

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master.
- `reports/designer/218-persona-terminal-consolidation-state-2026-05-18.md` — adjacent (terminal lifecycle uses the Kameo discipline).
- `reports/designer/220-full-signal-executor-state-2026-05-18.md` — adjacent (executor plane relies on the Kameo restart-trap discipline; supervised state-bearing actors stay on `.spawn()`).
- `skills/kameo.md` — canonical Kameo discipline.
- `skills/actor-systems.md` §"Release before notify" — adjacent.

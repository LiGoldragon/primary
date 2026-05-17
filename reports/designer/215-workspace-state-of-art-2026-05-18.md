# 215 — Workspace state of art (2026-05-18 compendium)

*Master compendium of recent per-lane reports, grouped by topic, with
contradictions resolved most-recent-wins. Each topic links to a deep
report carrying its full state. This index is meant to be forwardable
to every role so they can drive lane-side context maintenance.*

*Date: 2026-05-18. Pass driven by the user's explicit request after the
heavy 2026-05-17 work day. Scope: latest report per lane (by commit
time), topics identified across lanes, parallel agent audits per topic.*

---

## 0 · TL;DR

Yesterday (2026-05-17) was the biggest single-day workspace push to
date. Eight distinct topics moved substantively. Across all of them,
the **same architectural shape converged**: every stateful component
is a triad (daemon + thin CLI + `signal-*` contract), state lives in
sema-engine, privileged authority uses a separate `owner-signal-*`
surface, and `Mutate` is the verb that names top-down orders. The
triad pattern landed as a tier-1 workspace skill
(`skills/component-triad.md`); two of the workspace's biggest active
arcs (criome routed authorization, lojix lean rewrite) shipped real
implementation slices; two more (persona-terminal consolidation,
persona-orchestrate) reached coherent contract designs; the executor
shape inside every triad daemon got named (DA/119 + sec-OA/3).

Per-topic deep reports:

| # | Topic | Report | Status |
|---|---|---|---|
| 1 | **Criome routed authorization** | `reports/designer/216-criome-routed-authorization-state-2026-05-18.md` | Implementation shipping; 12 open questions; owner-signal-criome contract pass next |
| 2 | **Component triad + Mutate authority** | `reports/designer/217-component-triad-mutate-authority-state-2026-05-18.md` | Skill landed; 6 reports retire-eligible |
| 3 | **Persona-terminal consolidation** | `reports/designer/218-persona-terminal-consolidation-state-2026-05-18.md` | Contract split shipped; runtime execution pending |
| 4 | **Persona-orchestrate** | `reports/designer/219-persona-orchestrate-state-2026-05-18.md` | Contract design near-complete; daemon not started; designer pickup pending (`primary-699g`) |
| 5 | **Full Signal executor** | `reports/designer/220-full-signal-executor-state-2026-05-18.md` | Concept landed; no API additions to sema-engine; persona-terminal first, lojix-daemon second |
| 6 | **Lojix + Arca + horizon-leaner-shape** | `reports/designer/221-lojix-arca-horizon-leaner-shape-state-2026-05-18.md` | Lean rewrite end-to-end-smoke milestone; CriomeAuthorizationActor gate landed; cutover NOT done; production still on Stack A |
| 7 | **Persona engine + Kameo lifecycle** | `reports/designer/222-persona-engine-kameo-lifecycle-state-2026-05-18.md` | Kameo arc closed; persona engine sandbox live; 21 retire candidates |
| 8 | **Persona speech / Whisrs** | `reports/designer/223-persona-speech-whisrs-state-2026-05-18.md` | Research only; P0 bug `primary-51pn` live; 7 user decisions block implementation |

**The biggest cleanup is the operator lane.** 19 reports in `reports/operator/` between 108-131 are retire candidates — substance migrated to ARCH + `skills/kameo.md` + the kameo fork. Operator subdir drops from ~24 → 4 files after sweep.

---

## 1 · Method

Per-lane latest reports by commit time (`jj log` since 2026-05-17):

| Lane | Latest report | Latest jj-commit time |
|---|---|---|
| operator | `135-owner-terminal-signal-surface-2026-05-17.md` | 2026-05-17 23:39 |
| operator-assistant | `152-criome-authorization-expiry-replay-guard-2026-05-18.md` | 2026-05-18 10:47 |
| second-operator-assistant | `3-full-signal-executor-architecture-consideration-2026-05-18.md` | 2026-05-18 10:44 |
| designer | `214-criome-architecture-record-2026-05-17.md` | 2026-05-17 23:23 |
| designer-assistant | `119-full-signal-executor-architecture-concept-2026-05-18.md` | 2026-05-18 (this lane's work staged in jj working copy) |
| second-designer-assistant | `6-roles-as-config-owner-socket-mutable-2026-05-17.md` | 2026-05-18 10:12 |
| system-specialist | `142-criome-public-socket-and-deploy-approval-clarification-2026-05-17.md` | 2026-05-17 23:35 |
| system-assistant | `23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md` | 2026-05-17 23:23 |
| second-system-assistant | `2-persona-speech-component-brainstorm-2026-05-17.md` | 2026-05-17 15:27 |
| poet | (none) | — |
| poet-assistant | `01-handover-2026-05-14.md` | 2026-05-14 (stale; pre-arc) |

8 parallel topic-audit agents (general-purpose) read all topic-relevant reports across lanes plus the canonical ARCHs and skill files. Most-recent-wins applied on contradictions. Findings consolidated into the per-topic compendium reports above; the cross-cutting findings are below.

**Note on numbering.** This compendium was first written in `reports/designer-assistant/120-128` and moved to `reports/designer/215-223` to fix a lane-discipline mistake: my role this session was `designer`, not `designer-assistant`, so the work belonged in this lane. (Per `orchestrate/AGENTS.md`, "default agent" labels in the lane table are convenience labelling, not bindings; any agent may take any lane, but each session's role determines where its work lands.) Numbers 120-128 in designer-assistant are now retired permanently per `skills/reporting.md` §"Numbers are not reused after deletion".

---

## 2 · Cross-cutting findings (across all 8 topics)

### 2.1 The triad pattern is now permanent

`skills/component-triad.md` (tier-1) is the canonical statement. Five
invariants: CLI has one Signal peer; daemon speaks `signal-core` only;
verb per variant in `signal_channel!`; daemon state through
sema-engine; privileged authority uses `owner-signal-<component>`
surface. Authority chain (mind → orchestrate → router/harness) is in
`signal-core/ARCHITECTURE.md` §1, `persona-mind/ARCHITECTURE.md` §6.6,
`persona-router/ARCHITECTURE.md` §2.5, `skills/contract-repo.md`. The
component-triad skill recurs as the load-bearing reference in every
topic.

### 2.2 Mutate is the authority verb across the workspace

`Mutate` means "change this; I do not care what you think." Issuer
holds *possibly-mutated* state until receiver confirms. The verb shows
up authoritatively across:
- mind → orchestrate (`AcquireScopeOrder`)
- orchestrate → router (channel grants)
- orchestrate → harness (executor management)
- harness → terminal (`CreateSession`)
- consumer → criome (`CacheRetentionRequest`)
- criome → forge (`Build`, `Deploy`)

This is shaping up to be a workspace-wide audit candidate: re-walk
every existing `signal_channel!` and check that `Assert`-tagged
variants whose semantics are "order the receiver to change something"
are reclassified as `Mutate` (carried as /210 §6(d) open follow-up).

### 2.3 OwnerSignal as a discipline

`owner-signal-<component>` is the pattern for privileged authority
surfaces. The discipline lives in `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md`
§13's five A1-A5 settlements. It recurs in three concurrent arcs
(criome, terminal, orchestrate). **Candidate for skill promotion** —
DA/116 retires once `skills/owner-signal.md` (or an OwnerSignal
section in `skills/contract-repo.md`) absorbs it.

### 2.4 Two-deploy-stacks discipline

Production stack on `main` (Stack A: old monolithic `lojix-cli`) and
lean rewrite on `horizon-leaner-shape` (Stack B: lojix daemon + thin
CLI + lean horizon) **coexist by design**. The cutover is not done;
schemas have diverged. Discipline at `AGENTS.md` §"Two deploy stacks
coexist" + `protocols/active-repositories.md`. **Doc drift caught**:
the `main`-branch `signal-lojix/ARCHITECTURE.md` still claims
"Skeleton. No Cargo.toml" — stale; the worktree has implementation. See
/221 §11.

### 2.5 Worktree discipline

Feature branches with multi-commit arcs touching production live in
worktrees under `~/wt/github.com/<owner>/<repo>/<branch>/`, not in the
canonical `/git/` checkout. The canonical checkout stays on `main` so
peer agents see production reality. Discipline at `AGENTS.md`
§"Feature branches live in worktrees" + `skills/feature-development.md`.

### 2.6 Push-not-pull is universal

Every contract surface has `Subscribe` for observation. No polling
loops; consumers wait on push events. Cited in /204, /211, criome
ARCH, `skills/push-not-pull.md`. Open questions about subscription
delivery cost under load are flagged but not yet pressing.

### 2.7 The signal-core/sema-engine seam is honest

Twelve in-code witnesses (sec-OA/2 + `sema-engine/tests/{signal_core_seam.rs,seam_gap_falsification.rs}`)
prove the six verbs round-trip cleanly; structural multi-op atomicity
works for single-table writes; cross-table atomicity is the only real
gap and has schema-side resolutions. No new helper APIs needed today.
See /220.

---

## 3 · Open questions blocking implementation across multiple topics

These show up in 2+ topics and are the highest-leverage decisions
awaiting user direction.

| Question | Topics touched | Where discussed | Priority |
|---|---|---|---|
| **`SignedObject` canonical bytes** (which fields in the signed digest) | Criome (/216 Q1), Lojix (/221 Q4) | D/214 §11.7, SS/23 Q4, SS/22 Q5, SS/141 Q3 | Tier 1 — blocks master-key signing |
| **Criome receives content + digest, not just digest** | Criome (/216 Q2), Lojix (/221 Q14) | SS/23 Q10 (new) | Tier 1 — BLS verification needs original bytes |
| **owner-signal-criome contract design pass** | Criome (/216 Q3), Orchestrate (/219 — OwnerSignal generalization), Lojix (/221 Q6) | D/214 §11.8, SS/23 Q6 | Tier 1 — blocks tui-criome + CLI passphrase |
| **Unattended-system-daemon bootstrap** (v1 unencrypted vs v2 TPM) | Criome (/216 Q4), Lojix (/221 Q1) | D/214 §11.1, SS/22 Q4, SS/23 Q1 | Tier 1 — blocks cluster-side criome ship |
| **Cross-user-same-host criome routing** | Criome (/216 Q5), Lojix (/221 Q2) | D/214 §11.2, SS/22 Q1, SS/23 Q2; partially undercut by SS/142 (regular socket is public-reachable) | Tier 1 — blocks today's quorum case |
| **`persona-orchestrate` designer pickup** (bead `primary-699g`) | Orchestrate (/219), Triad (/217 follow-up e) | DA/115 + DA/116 + sec-DA/6 | Blocks all downstream owner-signal-* work |
| **owner-terminal socket path** | Terminal (/218 §6 new), Orchestrate (/219 — chain target) | new — surfaced post-/211 | Blocks operator's owner-terminal listener wire |
| **Speech 7-question slate** | Speech (/223) | sec-SA/2 §"Open Questions" | Blocks `persona-transcription` start; `primary-51pn` P0 still live |

---

## 4 · Per-lane stale ledger

The cleanup recommendations consolidated across topics. Each path is a
retire candidate per `skills/reporting.md` §"What gets absorbed, not
kept" and `skills/context-maintenance.md`. Where a report has partial
value, only the still-load-bearing fragment is noted.

### 4.1 `reports/operator/` — 19 retire candidates

The big sweep. Substance migrated to `skills/kameo.md` + each
component's ARCH + the kameo fork commits.

| Path | Retire reason |
|---|---|
| `108-persona-mind-system-overview.md` | Superseded by `persona-mind/ARCHITECTURE.md`. |
| `109-beads-audit-and-session-discipline.md` | Procedural; dated. |
| `110-persona-meta-integration-start.md` | Pre-/133 scaffolding. |
| `111-persona-daemon-implementation-review.md` | Pre-/133 scaffolding. |
| `112-persona-engine-work-state.md` | Pre-/133 scaffolding. |
| `113-persona-engine-supervision-slice-and-gaps.md` | Pre-/133 scaffolding. |
| `114-persona-introspect-prototype-impact-survey.md` | Pre-/133 scaffolding. |
| `115-sema-engine-split-implementation-investigation.md` | Self-annotates as historical (12-root vocabulary obsolete). |
| `120-hard-context-maintenance.md` | Old maintenance ledger; pointers stale. |
| `121-signal-core-sema-engine-readiness-work.md` | Readiness shipped per sema-engine ARCH. |
| `122-engine-context-maintenance-2026-05-15.md` | Old maintenance ledger. |
| `123-kameo-shutdown-ordering-reproduction.md` | Historical research; substance in `skills/kameo.md`. |
| `124-kameo-upstream-and-shutdown-design.md` | Historical research; substance in skills + fork. |
| `125-kameo-fork-three-shutdown-approaches.md` | Historical research; substance in skills + fork. |
| `126-kameo-push-only-lifecycle-branch-review.md` | Historical research; substance in skills + fork. |
| `127-actor-framework-lifecycle-correctness-research.md` | Historical research; produced canonical design. |
| `128-response-to-da-96-kameo-lifecycle-audit.md` | Implementation report; substance in code + skills. |
| `130-kameo-terminal-lifecycle-implementation.md` | Implementation report; substance in code + skills. |
| `131-kameo-control-plane-lifecycle-work.md` | Implementation report; substance in code + skills. |

Operator subdir would shrink from 24 → 4 files (132, 133, 134, 135).

### 4.2 `reports/designer-assistant/` — 8 retire candidates

| Path | Retire reason |
|---|---|
| `13-terminal-cell-relay-architecture-failure.md` | Substance in `terminal-cell/ARCHITECTURE.md` §1.2 (data-plane shape). |
| `14-terminal-cell-architecture-review.md` | Substance in `terminal-cell/ARCHITECTURE.md` §0 (library at production) + `persona-terminal/ARCHITECTURE.md`. |
| `43-nexus-query-language-and-sema-engine-arc.md` | Substance in `signal-core/ARCHITECTURE.md` + sema-engine ARCH. |
| `50-signal-core-base-verb-shape.md` | Six-root closure permanent in `signal-core/ARCHITECTURE.md`. |
| `53-signal-core-cli-verb-implementation-audit.md` | Substance in `skills/component-triad.md` + `skills/contract-repo.md`. |
| `94-lojix-daemon-design-on-persona-engine-pattern.md` | Substance in `lojix/ARCHITECTURE.md`; skill names the pattern universally. |
| `117-review-operator-134-terminal-orchestrate-porting-decisions-2026-05-17.md` | Already self-marks "Superseded in part by operator/135"; residual correction now in triad skill invariant 5. |
| `118-signal-core-sema-engine-fit-investigation-brief-2026-05-17.md` | Brief asked for an audit; audit landed (sec-OA/2 + DA/119 + sec-OA/3). |

After sweep, DA's recent reports (105, 111-119) plus a handful of older still-load-bearing ones survive. The directory currently has ~31 files; many older ones (15, 18, 20-30, 37, 41, 54, 84-93) likely also retire-eligible but weren't analyzed by this pass — a follow-up audit pass would surface them.

### 4.3 `reports/designer/` — 2 retire candidates

| Path | Retire reason |
|---|---|
| `204-kameo-lifecycle-canonical-design-2026-05-16.md` | Substance migrated to `skills/kameo.md` + `skills/actor-systems.md` + `ESSENCE.md`. Companion /205, /206 already retired (commit `a4b12dda`). |
| `209-component-triad-daemon-cli-contract-2026-05-17.md` | Three-invariant framing → tier-1 skill; verb-question → skill + ARCH + `skills/contract-repo.md`; per-component fit table → each ARCH. |

Designer subdir would shrink from 7 → 5 files (207, 208, 210, 211, 214).

### 4.4 `reports/operator-assistant/` — 1 retire candidate

| Path | Retire reason |
|---|---|
| `148-criome-signature-authorization-decisions-2026-05-17.md` | Substance absorbed into criome ARCH + D/214; stale tui-criome separate-triad framing risks future misdirection. |

The 145-147 batch (handover, follow-ups, context maintenance) may be
retire-eligible per the kameo arc closing but were not flagged by
agents.

### 4.5 `reports/system-specialist/` — 1 retire candidate (with partial-stale flags)

| Path | Retire reason |
|---|---|
| `140-lojix-criome-mediated-authorization-decision-2026-05-17.md` | Superseded by SS/141 + SS/142; original user-decision capture preserved in those. |

Earlier reports (116-133 range) weren't fully audited; some likely retire-eligible. Follow-up audit recommended.

### 4.6 `reports/system-assistant/` — 4 retire candidates + 2 partial

| Path | Retire reason |
|---|---|
| `16-two-deploy-stacks-coexist-survey-and-doc-proposal-2026-05-17.md` | Landed verbatim in `protocols/active-repositories.md`. |
| `17-review-of-sys-136-horizon-rs-lojix-audit-2026-05-17.md` | Findings folded into SS/136 narrative. |
| `19-deploy-mesh-with-arca-substrate-2026-05-17.md` | Subsumed by SS/138 + SS/141. |
| `21-criome-routed-authorization-and-thin-cli-shape-2026-05-17.md` | Superseded by SS/22 + SS/141 + D/213/214. |

Partial-retire (some narrative value preserved):

- `18-daemon-mesh-deploy-architecture-exploration-2026-05-17.md` — retire after cross-walking residuals into SS/23.
- `20-arca-content-addressed-substrate-design-2026-05-17.md` — five-axes framing historical; SS/139 carries canonical Arca decisions.

System-assistant subdir would shrink from 9 → 3 files (22, 23, plus maybe 18+20 in partial form).

### 4.7 Smaller lanes — no retires today

- `second-designer-assistant`: /1-5 already retired in jj; /6 stays until designer absorbs.
- `second-operator-assistant`: /1, /2, /3 all stay.
- `second-system-assistant`: /1, /2 stay until user direction on 7 open questions.
- `poet-assistant`: `01-handover-2026-05-14.md` — older but lane is dormant.

---

## 5 · Beads to user-attention

Beads surfaced as needing user attention through this audit:

| Bead | Priority | Why surfaced |
|---|---|---|
| `primary-51pn` | **P0** | Whisrs P0 bug live on machine; mitigation rolled back; needs re-apply or accept-the-risk decision. /223. |
| `primary-at7x` | P1 | Criome routed authorization — in flight; description needs refresh per D/214 §12 to name §11.10 / §11.11 / §11.12 (numbering shifted after OA/150/152). /216. |
| `primary-izze` | P1 | tui-criome — re-scoped per D/214 §12; description should reflect "owner client of own daemon, not separate triad." /216. |
| `primary-699g` | P2 | persona-orchestrate designer pickup — load-bearing dependency for OwnerSignal chain and `LaneRegistry*` family. /219. |
| `primary-jboc` | P2 | RoleName contract gap — reframe with sec-DA/6's path 4 added. /219. |
| `primary-alcz` | P2 | skills/kameo wait_for_shutdown warning — substance has landed; close-then-confirm protocol comparison is the only residual; closeable. /222. |
| `primary-766g` | P2 | lojix deployment_id minting — interplay with `deploy.rs` split. /221. |
| `primary-ipjx` | P1 epic | Speech-to-text durable-first rethink — blocked on 7 open questions in sec-SA/2. /223. |

---

## 6 · User proposal recorded for confirmation

The user surfaced a proposal during this session that deserves explicit
confirmation before being adopted as workspace discipline.

> *"we should make it mandatory in the operator role to create a
> report, even if it's short. And probably prioritizing shorter is
> better. A short report on what they've done in the session, at every
> session when they implement something, they should do a short, a
> very short report on what they've implemented. … this is where I
> want PersonaMine, but it's a lot to keep track of."*

### What this would change

Add to `skills/operator.md` (and by inheritance to operator-assistant /
second-operator-assistant lanes) a rule like:

> **Every session that lands code MUST produce a short report under
> `reports/operator/<N>-<topic>-<date>.md`.** Shorter is better. The
> report names: what landed (commits + repos), what tests/checks
> passed, what's still stubbed, what's the next slice. Operator
> reports are commit-history-plus-context, not durable design records.

### Why the user surfaced this

The reasoning the user articulated: *"the problem is these commits are
all over the place. So yes, a very short report."* A scrollable
per-session report makes the implementation trail re-readable in
report form, not just `git log` form, while the workspace migrates
toward the Persona work-graph (PersonaMine) which would obviate the
need.

### Why this is a real gap today

The operator lane's recent style is **inconsistent**:
- operator/133, /134, /135 ARE short session reports — good shape.
- operator/218-131 (the kameo arc) are long investigation reports.
- operator-assistant/148-152 ARE short session reports — good shape.
- operator-assistant/146/147 are context-maintenance ledgers, not session reports.

A uniform discipline would make commit-discovery cheaper for everyone.

### Tradeoffs

- **Pro**: every commit-batch becomes scrollable / forwardable / passable.
- **Pro**: reduces the "what did operator do yesterday?" load on other roles (this very audit was harder because operator activity wasn't uniformly reported).
- **Pro**: aligns with the user's explicit `skills/reporting.md` rule that "substantive output goes in reports."
- **Con**: adds report-write overhead per session. Mitigated by "shorter is better."
- **Con**: filesystem-cap pressure (12 reports per lane soft cap). Mitigated by aggressive supersession on the next session's report.
- **Con**: encourages short-attention-span sessions that drop reports for trivial commits — mitigation: the rule says "every session that *lands code*", not every commit.

### Recommendation

**Add as `skills/operator.md` section** with these specifics:
- Title format: `<N>-<topic>-<date>.md`.
- Required sections: "What landed" (commits + repos), "Tests" (witnesses passed), "Still stubbed" (one-line each), "Next slice" (one-line).
- Length target: 1 screen. Longer than 1 screen requires justification.
- Discipline: the short-report supersedes prior short-reports of the same operator session-batch (so the count doesn't balloon).

**Awaiting user confirmation before editing skills/operator.md.**

---

## 7 · Recommendations per role

### designer (this lane)

- Pick up bead `primary-699g` — write the persona-orchestrate definitive design report absorbing DA/115 + DA/116 + sec-DA/6 substance. This unblocks: owner-signal-criome contract design (cross-lane), terminal owner-socket implementation, executor first-implementation, lane-registry-as-config landing.
- Reconcile designer/214 §1 with system-specialist/142's correction (regular `signal-criome` socket is public+unencrypted; ARCH currently draws it as `0660 group criome-peers`).
- Decide: promote DA/116 OwnerSignal substance into a workspace skill (`skills/owner-signal.md` or extend `skills/contract-repo.md`)?
- Re-walk every existing `signal_channel!` to audit verbs under Mutate-as-authority reframing (/210 §6(d)).
- Consider: drop reports/designer/204 and /209 in next sweep (substance migrated to skills + ARCH per /217 + /222).

### designer-assistant

- Apply the 8 retire candidates from §4.2 in next sweep.
- If user confirms the operator-session-reports proposal, draft the `skills/operator.md` section.

### second-designer-assistant

- Hold pattern: sec-DA/6 stays until designer absorbs it into `primary-699g` report.

### operator

- **Highest leverage**: wire the owner-terminal Unix socket listener in `persona-terminal` and implement `CreateSession`/`RetireSession` execution (operator/135 §6 items 1-3). This is the bottleneck for downstream orchestrate integration. See /218 §8.
- Apply the 19 retire candidates from §4.1.
- Consider: adopt the short-session-report discipline if user confirms.
- Decide bead `primary-alcz` — close with a comment pointing to `skills/kameo.md` lines 836-849 + 1040-1047, or add one paragraph on close-then-confirm.

### operator-assistant

- Next criome slice: master-key signing for simple-self-signed policy (D/214 §11.12), needing `SignedObject` canonical bytes decision (cross-cutting Q1 above).
- Next lojix slice: real `signal-criome` socket client replacing `CriomeAuthorizationPolicy::Unavailable` (operator-assistant/151 §"Next Work").
- Consider drop: operator-assistant/148 (criome topic — superseded).

### second-operator-assistant

- Hold pattern: /1, /2, /3 all stay. /3 is the current end of the executor arc.

### system-specialist

- Pick up: real Arca daemon implementation per system-specialist/139 (`/git/.../arca` has `todo!()` bodies; needs the `/arca` migration too).
- Pick up: `NixDaemonConfigurationActor` skeleton (system-specialist/138 + /141).
- Apply: update `/git/.../signal-lojix/ARCHITECTURE.md` `main` status note (currently stale).
- Apply: update `/git/.../arca/ARCHITECTURE.md` to `/arca` root + base32 prefix policy.
- Consider drop: system-specialist/140 (superseded by /141 + /142).

### system-assistant

- Apply the 4 retire candidates + 2 partial from §4.6.
- Pick up: cross-walk SS/18's G1-G19 gap framework's residuals into SS/23 (then retire SS/18).

### second-system-assistant

- Hold pattern: /1, /2 stay until user resolves the 7 open speech questions.

### poet / poet-assistant

- Dormant. No action.

---

## 8 · What this compendium does not cover

- Per-report stale-vs-fresh ledger for older reports (pre-2026-05-17) in lanes other than the topic-touched ones. A follow-up audit pass would surface them — particularly the older designer-assistant range (15, 17, 18, 20-30, 37, 41, 54, 84-93), older system-specialist range (116-130), older operator-assistant range (121-145).
- Anything in `reports/system-specialist/116-133` that's pre-2026-05-17 — agents focused on the recent arc.
- Code-level audit of whether each report's claims still hold against the canonical ARCH text. Spot-checked but not exhaustively verified.

A second sweep can target the lanes' older backlogs once this round's recommendations land.

---

## 9 · Forward this report

This compendium is meant to be **forwardable**. Each role can read §7
for their specific recommendations + the per-topic report(s) relevant
to their lane:

- **operator** lane: §7 + /218 + /222 (the big retire sweep) + /220 (executor implementation order).
- **operator-assistant** lane: §7 + /216 (criome state) + /221 (lojix state).
- **designer** lane: §7 + all 8 topic reports.
- **system-specialist** lane: §7 + /221 (canonical) + /216 (criome interaction).
- **system-assistant** lane: §7 + /221 + /216.

The per-topic reports are also passable to a peer agent by naming the
path, per `skills/reporting.md` §"reports are passable objects".

---

## See also

- `reports/designer/216-criome-routed-authorization-state-2026-05-18.md`
- `reports/designer/217-component-triad-mutate-authority-state-2026-05-18.md`
- `reports/designer/218-persona-terminal-consolidation-state-2026-05-18.md`
- `reports/designer/219-persona-orchestrate-state-2026-05-18.md`
- `reports/designer/220-full-signal-executor-state-2026-05-18.md`
- `reports/designer/221-lojix-arca-horizon-leaner-shape-state-2026-05-18.md`
- `reports/designer/222-persona-engine-kameo-lifecycle-state-2026-05-18.md`
- `reports/designer/223-persona-speech-whisrs-state-2026-05-18.md`
- `skills/context-maintenance.md` — discipline this audit follows.
- `skills/reporting.md` — discipline for the reports themselves.
- `protocols/active-repositories.md` — current architecture-active repo map.

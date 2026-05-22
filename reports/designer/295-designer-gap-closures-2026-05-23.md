# 295 - designer-only gap closures from /293/5

Report kind: gap-closure record
Topic: manifest existing psyche intent into target files to close designer-only gaps named in `/293/5-gap-closure-step-1-2.md`
Date: 2026-05-23
Lane: designer (subagent under prime designer, per psyche directive 2026-05-23 "use intent to close any designer gaps identified")
Drives bead: `primary-c2da` (Gap 3, 10, 12, 17, 22, 23, 33 closed via manifestation; partial work on Gap 11)

## TL;DR

Seven designer-only gaps from the `/249 → /293/5` inventory closed
through intent manifestation into per-repo INTENT.md and ARCH text:
**Gap 3 (persona INTENT.md), Gap 10 (spawn order), Gap 12 (skeleton
honesty extension), Gap 17 (intent substrate cutover), Gap 22
(ChannelMessageKind rationale), Gap 23 (Channel duration rationale),
Gap 33 (router rejection reasons)** — all manifested as new permanent
guidance directly from spirit records 208/209/215/216/238/239/240/
246/252, legacy `intent/persona.nota`, and the deployed code surface.
Partial: Gap 11 designer-side recommendation (Mutate-chain partial-
failure) added to `skills/component-triad.md` as pre-write for the
operator bead. Four commits landed across persona, signal-persona,
persona-router (component repos) plus one for primary (the skill
update + this report).

## §1 Per-gap closure detail

### Gap 3 — persona meta-repo has no INTENT.md → CLOSED

- **Target file:** `/git/github.com/LiGoldragon/persona/INTENT.md`
  (new file)
- **What landed:** complete INTENT.md synthesised from spirit records
  208 (engine takes over upgrade management), 209 (Persona lands
  BEFORE Spirit cutover), 215 (canonical name "Persona"), 216
  (composed of `persona` CLI + `persona-daemon`), 238/239 (Persona
  privilege constraint — permissioned system daemon), 240 (systemd
  template units day-one), 246 (no client-side discovery), 252
  (FD-handoff via SCM_RIGHTS), plus older psyche statements in
  legacy `intent/persona.nota` 2026-05-19T14:00:00Z about "the
  supervisor has higher infrastructure permission only" and "spirit
  spawned last".
- **Structure:** What Persona is / Persona is a permissioned system
  daemon / Persona takes over component upgrade management / Boot
  sequence / Systemd template units from day one / No client-side
  discovery / FD-handoff / Multi-engine supervision / Intent
  substrate / Principles / Constraints / Anti-patterns / See also.
- **Evidence:** spirit records cited inline; verbatim psyche quotes
  in italics per `skills/repo-intent.md` and
  `skills/intent-manifestation.md` conventions.

### Gap 10 — Spawn order beyond "spirit last" → CLOSED

- **Target file 1:** `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
  §1.7.1 (new subsection under §1.7 Startup Strategy)
- **Target file 2:** Persona INTENT.md §"Boot sequence" (Gap 3 file)
- **What landed:** canonical spawn order documented as
  `supervisor → sema-upgrade → mind → orchestrate → router →
  harness → terminal → message → introspect → spirit`. Three load-
  bearing positions named explicitly: sema-upgrade first, infrastructure
  before cognitive, spirit last (per the rule "spirit-as-apex spawns
  last because every supervised component must be up before the
  cognitive layer animates").
- **Evidence:** spirit record 111 (sema-upgrade first), record 209
  (Persona before Spirit), legacy `intent/persona.nota` 2026-05-19
  (spirit last + supervisor's infrastructure permission caveat).

### Gap 12 — Skeleton honesty for ordinary + owner contracts → CLOSED

- **Target file:**
  `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` —
  "Skeleton honesty across the component-triad family" subsection
  added after the existing EngineManagement-channel rule.
- **What landed:** extension of the skeleton-honesty rule from
  EngineManagement-only to (a) every ordinary signal-persona-*
  contract: every supervised daemon decodes every variant, returns
  typed Unimplemented for unbuilt-but-decodable; (b) every
  owner-signal-* contract: same rule. Codified once for the whole
  component-triad family. Rationale: the issuer's authority chain
  rests on acknowledgements that are decoding-complete on every
  variant the deployed contract version supports.
- **Evidence:** this is a designer-determined codification per
  /249 Gap 12. The substance was implicit in the existing
  `skills/component-triad.md` invariants (typed wire surface, no
  silent drops); the manifestation makes it explicit at the
  component-triad family level rather than just for the
  EngineManagement channel.

### Gap 17 — Filesystem-projection cutover → CLOSED

- **Target file:** Persona INTENT.md §"Intent substrate" (the
  new file from Gap 3).
- **What landed:** confirmation that legacy `intent/*.nota` files
  are read-only-historical; agents must not append; new psyche
  statements are captured through the deployed Spirit CLI.
- **Evidence:** spirit records 167 + 168 (verbatim
  "Why are you logging in the files? We are not using the files
  anymore, we are using Spirit." and "remove that old instructions,
  we use spirit now."). Also already reflected in the workspace
  AGENTS.md current rule and `skills/spirit-cli.md`.

### Gap 22 — ChannelMessageKind enumeration rationale → CLOSED

- **Target file:**
  `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md`
  §2.6 (new subsection "Channel kinds").
- **What landed:** one-paragraph-per-variant documentation of the
  12 ChannelMessageKind enum members from
  `signal-persona-mind/src/lib.rs` (MessageIngressSubmission,
  MessageSubmission, InboxQuery, FocusObservation,
  PromptBufferObservation, MessageDelivery, TerminalInput,
  TerminalCapture, TerminalResize, TranscriptEvent,
  AdjudicationRequest, DeliveryNotification). Rationale section:
  the set is closed because every typed message carries authority
  semantics — opening to free identifiers would make channel-grant
  policy unenumerable. Channel-grant authority lives in
  persona-mind (mind decides; router enforces), per /293/5 framing.
- **Evidence:** no new psyche intent invented; pure documentation
  of the existing surface in deployed code.

### Gap 23 — Channel duration `OneShot / Permanent / TimeBound`
rationale → CLOSED

- **Target file:**
  `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md`
  §2.7 (new subsection "Channel duration").
- **What landed:** per-variant rationale: OneShot for request-reply
  patterns; Permanent for long-lived mind↔agent channels and
  structural channels; TimeBound for policy-driven temporary
  grants. The three durations cover the three shapes channel-grant
  authority distinguishes: one-time, until-retracted, bounded-
  window.
- **Evidence:** no new psyche intent invented; documentation of
  the existing ChannelDuration enum in
  `signal-persona-mind/src/lib.rs`.

### Gap 33 — Router message rejection reasons → CLOSED

- **Target file:**
  `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md`
  §2.8 (new subsection "Rejection reasons").
- **What landed:** documented closed set of router rejection
  reasons: ChannelInactive (parked → mind adjudication), Recipient
  not found, Store rejected, Authority revoked (channel retracted
  or expired), Unimplemented operation variant (skeleton-honesty
  reply). The set is closed because the router's authority surface
  is finite.
- **Evidence:** existing rejection types in the deployed code
  (`SubmissionRejectionReason::{StoreRejected, RecipientNotFound}`
  in persona-router/src/router.rs; `RejectionReason` in
  signal-persona-mind for the mind-side). No new psyche intent
  invented; designer codification of the existing surface.

### Gap 11 — Mutate-chain partial-failure semantics → PARTIAL (designer-side pre-recommendation landed)

- **Target file:** `/home/li/primary/skills/component-triad.md`
  §"Authority chain — worked example" extended with a new
  subsection "Partial-failure semantics — commit-first-success-and-
  record-divergence".
- **What landed:** the designer's pre-recommendation for the
  Mutate-chain partial-failure protocol: issuer commits on first
  success and records divergence on failure, matching the
  record 180 + 183 main/next divergence precedent. Rationale on
  why neither all-or-nothing two-phase commit nor inverse-mutate
  rollback are the right shape. The downstream side's typed
  Unimplemented / typed failure replies (per the skeleton-honesty
  rule) are the substrate that the partial-failure protocol relies
  on.
- **What did NOT land:** the operator-side implementation bead
  (constraint tests in mind, orchestrate, router, harness). The
  bead lands when orchestrator files it; designer pre-wrote the
  recommendation so the bead has a target to reference.
- **Evidence:** spirit records 180 + 183 (main/next divergence
  semantics — verbatim quoted in the skill addition).

## §2 Commits made

| Repo | Hash | Description |
|---|---|---|
| `signal-persona` | `953884d9` | signal-persona: refresh ARCHITECTURE for engine-management rename, version-handover neighbours, and skeleton-honesty extension to ordinary + owner contracts |
| `persona` | `879fa7a4` | persona: add INTENT.md from psyche records; extend ARCH §1.7 with spawn order subsection |
| `persona-router` | `41709418` | persona-router: document ChannelMessageKind, ChannelDuration, and rejection-reason rationale in ARCH §§2.6-2.8 |
| `primary` | (this commit) | designer: close gaps 3 + 10 + 12 + 17 + 22 + 23 + 33 via manifestation; add Mutate-chain partial-failure pre-recommendation to component-triad.md |

Note: the signal-persona commit includes a pre-existing in-flight
ARCH refresh from an earlier session (engine-management vocabulary
rename + version-handover neighbours documentation). My skeleton-
honesty extension layered on top; the unified commit message names
both halves. The earlier in-flight work was sitting in the working
copy at session start; rather than amend or rebase, the combined
message keeps the audit trail intact.

## §3 What was NOT closed

### Gap 9 — owner-signal-* repo emergence (3 missing) → PENDING-CLARIFICATION

Three missing owner-signal-* repos (harness, message, system, plus
introspect since Gap 4 closure) need psyche clarification on
**emergence criteria** before designer can write an "Emergence
criteria" subsection. /293/5 framed this as PENDING-CLARIFICATION;
no in-flight psyche statement on the question between /293/5 and
now. Deferred to next psyche session.

### Gap 11 — Mutate-chain partial-failure semantics → PARTIAL

Designer-side pre-recommendation landed in
`skills/component-triad.md` (per §1 above). Operator bead for
implementation across mind / orchestrate / router / harness has
not been filed — that's orchestrator's call after this report
lands.

### Other open gaps (not in this session's scope)

Per /293/5 §2:
- Gap 1 (Spirit→mind owner contract) — DEFERRED per record 204.
- Gaps 6, 7+27, 8, 19, 20, 31, 34, 35 — PENDING-CLARIFICATION, need
  psyche calls.
- Gaps 15, 16, 18, 24, 25, 28, 32, 13 — OPERATOR-ACTIONABLE, need
  beads, not manifestation.
- Gap 16 (bootstrap-policy.nota content) — needs cross-component
  audit before designer can write per-component starter content; not
  covered here.

## §4 Bead reference

This session progresses `primary-c2da` (the gap-closure epic
spawning from /249 + /282 + /293/5). Designer should add a comment
on `primary-c2da` noting:

- Gaps closed via manifestation: 3, 10, 12, 17, 22, 23, 33
- Gap 11 PARTIAL — designer-side recommendation landed
- 4 commits made (hashes above)
- Tracking report: /home/li/primary/reports/designer/295-designer-
  gap-closures-2026-05-23.md

## See also

- `/home/li/primary/reports/designer/293-designer-and-research-
  batch-2026-05-23/5-gap-closure-step-1-2.md` — the source gap
  inventory + classification this session works from
- `/home/li/primary/reports/designer/249-component-intent-gap-
  analysis.md` — the original 35-gap inventory
- `/home/li/primary/reports/designer/282-workspace-implementation-
  status.md` — the earlier delta snapshot
- `/git/github.com/LiGoldragon/persona/INTENT.md` — Gap 3 target
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` §1.7.1 —
  Gap 10 target
- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md`
  §"Skeleton honesty" — Gap 12 target
- `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md`
  §§2.6-2.8 — Gaps 22, 23, 33 targets
- `/home/li/primary/skills/component-triad.md` §"Authority chain"
  — Gap 11 designer-side pre-recommendation
- `/home/li/primary/skills/intent-manifestation.md` — the discipline
  this session follows
- `/home/li/primary/skills/repo-intent.md` — per-repo INTENT.md
  shape used for Gap 3
- `/home/li/primary/skills/architecture-editor.md` — the inline-
  load-bearing-claim rule applied for the ARCH edits

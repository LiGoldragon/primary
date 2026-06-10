# 576 — Cross-lane context-maintenance sweep (2026-06-10)

designer lane, dispatcher record. A cross-lane sweep across all report
lanes except `assistant/` and `counselor/` (closed by privacy). Eight
parallel triage agents applied the drop/forward/migrate/keep rule with the
landing gate; the dispatcher executed the verified actions and deferred the
rest. This file is the landing witness — every deletion below names where its
substance now lives; git history preserves the originals.

## Result

- **Reports: 430 → 371** (−59 files).
- **6 agglomerations** merged 21 source reports into 6 better ones (the merged report is the landing).
- **25 reports dropped** as superseded/already-permanent, each with a named landing.
- **155 reports kept** (load-bearing, no successor) across the fleet.
- **6 drops deferred** — the agent's named landing did not actually carry the substance on verification; kept pending a real landing.
- **24 migrate-flags** recorded below: substance that should move into a permanent doc; the report is KEPT until it does.

## Agglomerations (sources merged → new report, sources deleted)

- **designer/575-engine-makeover-actor-shell.md** ← 564-emitter-actor-shell.md, 565-engine-makeover-situation.md
- **operator/347-plane-emitter-followups-and-spirit-production-readiness-2026-06-06.md** ← 322-engine-stack-rust-native-and-spirit-exemplar-2026-06-05, 323-spirit-streaming-meta-and-stack-readiness-2026-06-05.md, 324-plane-gated-emitter-and-spirit-production-proof-2026-06-05.md, 325-plane-engine-trait-followup-and-spirit-proof-2026-06-05.md, 326-plane-trace-completion-and-doc-fix-2026-06-06.md
- **system-operator/206-actor-native-engine-rewrite-audit-gameplan-and-migration-invariants.md** ← 200-Audit-actor-native-engine-rewrite-2026-06-07.md, 201-Audit-actor-native-engine-rewrite-second-pass-2026-06-07.md, 202-Research-actor-native-implementation-gameplan.md
- **system-designer/87-triad-main-landed-and-cloud-pilot-complete-2026-06-06.md** ← 80-triad-main-landed-migration-scoreboard-2026-06-06.md, 81-cloud-pilot-emitter-shift-findings-2026-06-06.md
- **cloud-designer/37-cloud-component-schema-triad-port-arc-2026-06-04.md** ← 18-cloud-component-schema-triad-port-2026-06-04.md, 19-cloud-port-prototype-results-2026-06-04.md, 20-contract-daemon-boundary-audit-2026-06-04.md, 21-open-threads-register-2026-06-04.md, 22-cloud-blocker-report-accuracy-audit-2026-06-04.md
- **pi-operator/8-ouranos-desktop-survivability-2026-06-05.md** ← 4-ouranos-ui-freeze-2026-06-05.md, 5-linux-desktop-resource-priority-2026-06-05.md, 6-rescue-terminal-slice-incident-2026-06-05.md, 7-staged-ui-priority-policy-2026-06-05.md

## Drops executed (report → landing)

### designer
- `569-agent-component-build.md` → /home/li/primary/reports/designer/572-gated-spirit-and-agent-component-handover.md

### operator
- `313-Comparison-designer-vs-operator-structural-macro-node-2026-06-05.md` → /home/li/primary/reports/operator/327-schema-nota-triad-study/6-overview.md
- `314-Comparison-asschema-removal-designer-operator-2026-06-05.md` → /home/li/primary/reports/operator/327-schema-nota-triad-study/6-overview.md
- `315-Comparison-designer-521-structural-derive-operator-read-2026-06-05.md` → /home/li/primary/reports/operator/329-session-summary-schema-stack-and-triad-main-2026-06-06.md
- `316-Feedback-designer-524-schema-pipeline-2026-06-05.md` → /home/li/primary/reports/operator/327-schema-nota-triad-study/6-overview.md
- `312-Psyche-nota-structural-macro-node-implementation-2026-06-04.md` → /home/li/primary/reports/operator/327-schema-nota-triad-study/2-nota-structural-macro-node.md
- `304-Psyche-repository-stack-state-2026-06-04.md` → /home/li/primary/reports/operator/346-Audit-designer-state-of-everything-attention-feedback.md
- `307-context-maintenance-spirit-schema-sema-current-state-2026-06-04.md` → /home/li/primary/reports/operator/346-Audit-designer-state-of-everything-attention-feedback.md
- `306-schema-centered-runtime-cleanup-analysis-2026-06-04.md` → /home/li/primary/reports/operator/311-cycle-day-review-spirit-production-readiness-2026-06-04.md
- `301-Research-codex-session-recovery-2026-06-04.md` → /home/li/primary/reports/operator/300-meta-signal-rename-pass-2026-06-03.md
- `272-bead-staleness-audit-implementation-2026-06-01` → /home/li/primary/.beads/

### system-operator
- `203-actor-native-implementation-checkpoint-2026-06-07.md` → /home/li/primary/reports/system-operator/204-actor-native-async-runner-implementation-2026-06-08.md
- `180-pi-0-78-update-2026-06-01.md` → /git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix
- `179-pi-compaction-fix-and-local-ai-toolkit-prefetch-2026-06-01.md` → /home/li/primary/reports/system-operator/187-Psyche-context-maintenance-situation-2026-06-03.md

### system-designer
- `82-repo-sprawl-and-orchestrate-old-deps-2026-06-07.md` → /home/li/primary/reports/system-designer/85-workspace-repository-status-survey-2026-06-09/4-synthesis-and-cleanup-plan.md
- `83-repo-audit-keep-archive-delete-2026-06-07.md` → /home/li/primary/reports/system-designer/85-workspace-repository-status-survey-2026-06-09/4-synthesis-and-cleanup-plan.md
- `84-operator-criome-current-stack-migration-audit-2026-06-08.md` → /home/li/primary/reports/system-designer/86-handover-open-issues-2026-06-09.md

### cloud-designer
- `27-lojix-bring-online-milestones-2026-06-05.md` → /home/li/primary/reports/cloud-designer/28-lojix-online-m1-build-evaluate-2026-06-05.md

### cloud-operator
- `9-cloudflare-dns-tool-2026-05-27.md` → /home/li/primary/reports/cloud-operator/10-audited-cloud-domain-prototype-2026-05-27.md (and permanently /git/github.com/LiGoldragon/cloud/ARCHITECTURE.md, 'Current Implementation Slice' lines 53-79)
- `14-cloud-schema-triad-engine-blocker-2026-06-04.md` → /home/li/primary/reports/cloud-operator/15-correction-to-cloud-schema-blocker-report-2026-06-04.md (declared superseder) and /git/github.com/LiGoldragon/cloud/ARCHITECTURE.md (Schema-engine upgrade track, lines 93-128, blocker resolved)
- `15-correction-to-cloud-schema-blocker-report-2026-06-04.md` → /git/github.com/LiGoldragon/cloud/ARCHITECTURE.md (Schema-engine upgrade track, build.rs wiring + pair-declaration-form note, lines 113-128) and /home/li/primary/reports/system-designer/81-cloud-pilot-emitter-shift-findings-2026-06-06.md (full cloud port landed on main, COMPLETE)
- `12-context-maintenance-skill-update-2026-05-28` → /home/li/primary/skills/context-maintenance.md and /home/li/primary/skills/context-maintenance-deep.md (both verified to carry the manifested discipline)
- `6-recent-intent-reports-branch-read-2026-05-26` → /home/li/primary/AGENTS.md (durable discipline: no-free-function rule line 158, NOTA bracket-form rule line 140) with current schema-next/schema-rust-next main as the live baseline that superseded the May-26 branch snapshot
- `7-refresh-intent-reports-visual-audit-2026-05-26` → /home/li/primary/AGENTS.md (no-free-function rule line 158, NOTA bracket-form rule line 140) with current schema-next/schema-rust-next main as the live baseline that superseded the May-26 snapshot

### small-lanes
- `165-designer-counter-ego-audit-2026-05-24.md` → /home/li/primary/orchestrate/roles.list

## Deferred — landing unverified, KEPT (needs a real landing before drop)

- `320-triad-runtime-role-and-daemon-boundary-implementation-2026-06-05` — operator: dir's daemon-boundary + signal-frame-push substance NOT in the named 347 (347 covers stream/role only).
- `321-schema-derived-streaming-push-implementation-2026-06-05` — operator: streaming-push + kernel-map substance NOT in named 347.
- `303-Audit-repository-stack-state-2026-06-04` — operator: repository/dependency-inventory substance NOT in named 346 (346 is the state-of-everything feedback audit).
- `34-best-daemon-shape-bottom-up` — cloud-designer: competing daemon-shape proposals (unified/actor-native/merit) NOT carried by named 35/4-overview — migrate the alternatives, don't drop.
- `77-…/0-frame-and-method.md & 78-…/0-frame-and-method.md` — system-designer: these are frame files INSIDE live meta-report dirs 77 & 78 — deleting them alone breaks the directories; the named 87 is a different topic.

## Migrate-flags (substance to move to a permanent doc; report KEPT until it lands)

### designer
- `536-engine-and-spirit-ground-truth-and-plan.md` → **/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md (and spirit/ARCHITECTURE.md)**: The corrected engine-codegen ground truth (token-native noun-owned lowering, the spirit schema-plane split exemplar). 549 flagged 536/537 to retire once the schema-rust-next + spirit ARCHITECTURE.md absorb the corrected ground-truth + the PlaneType design; that absorption has not landed.
- `537-plane-type-design.md` → **/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md**: The Plane/PlaneProjection noun decomposition (the three-tier rule: Plane/PlaneProjection own naming+edges; construct nouns compose; RustEmissionTarget/RuntimePlaneSet own which-planes). Implemented + landed; the design belongs in schema-rust-next/ARCHITECTURE.md so this report can retire.
- `550-v2-daemon-configuration-bootstrap-virgin-daemon.md` → **/home/li/primary/skills/component-triad.md**: The ratified virgin-daemon bootstrap model (single rkyv Configure arg, no-manager-dependency, virgin-vs-resume fork, self-resume on restart). The §single-argument-rule already cites it; once the spirit implementation lands and the full model is in the skill, this report retires.
- `551-workspace-dependency-ecosystem-state.md` → **/home/li/primary/skills/engine-report.md + skills/reporting.md**: The kype: dependency context (forward/reverse-dep counts + last-commit date) as a standard reporting habit, plus keeping /tmp/dep-graph.json regeneration scripted. 551 itself recommends folding this into the reporting skills as an enforced norm.

### operator
- `342-incident-fake-nota-output-pattern-2026-06-09.md` → **/home/li/primary/skills/nota-comments.md or a NOTA-discipline skill (e.g. skills/contract-repo.md)**: The fake-NOTA audit pattern — search for manual `impl NotaEncode` containing format!/push_str/write!/handcrafted delimiters; tests that assert a NOTA-looking stdout string without parsing it back through NotaDecode; ad-hoc to_nota/render_nota/format_nota helpers outside the codec layer. The corrected shape (real typed output enum deriving NotaDecode/NotaEncode + decode-backed test) is a durable rule. 346 confirms these sites are still live fleet-wide (signal-persona/origin.rs, persona-spirit/migration.rs, signal-system/lib.rs, cloud bins), so the discipline should become a permanent searchable rule.
- `319-Refresh-nexus-engine-and-enum-payload-design-2026-06-05.md` → **/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md (or a nota/schema design skill)**: The enum-payload-variant authoring rule — direct enum payload when data is one axis of choice; struct payload only for a product of independent facts; nested data-carrying enum for partial data; do not invent a wrapper struct that exists only to hold one enum. Plus the two compact header forms (inline payload enum at header position; type-table variant resolution). The report itself recommends this land as a testable constraint in schema-rust-next/ARCHITECTURE.md (record 2578 manifest-leaned-on-design). The report is already an agglomerated Refresh (retired 285-290); keep it until the rule lands as a constraint, then it can retire.
- `309-Audit-signal-contract-nexus-sema-boundary.md` → **/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md and /home/li/primary/skills/contract-repo.md**: The contract-vs-runtime emission-profile rule (Contract profile emits only public Signal roots/codecs; Runtime profile may declare NexusWork/NexusAction/SEMA roots and emit engine traits) and the independent-SEMA-halves emission rule. The WireContract/SignalRuntime split landed in code, so the design rule should be stated permanently; the per-repo remediation table (legacy signal_channel! Sema-class wrappers in 8 contract repos) should migrate to beads/active-repositories tracking rather than living in an audit report.

### system-operator
- `1-whisrs-durable-first-stt-research-2026-05-17.md` → **future speech-component repo (Whisrs) INTENT.md / ARCHITECTURE.md**: Durable-first STT object model: RecordingSession, artifact-first capture, attempt ledger, retry-after-failure. Move when the speech/transcription component gets permanent repo docs.
- `2-persona-speech-component-brainstorm-2026-05-17.md` → **future persona-transcription component repo INTENT.md / ARCHITECTURE.md**: persona-transcription component boundary and Signal/raw-audio data-plane split. Move when that component work resumes with permanent docs.
- `139-arca-daemon-content-addressed-store-architecture-2026-05-17.md` → **/git/github.com/LiGoldragon/arca (or equivalent) INTENT.md / ARCHITECTURE.md**: Arca design: full-BLAKE3 digest as identity vs stable daemon-allocated locator, never-renamed locators, longer-prefix collisions, /arca system-service root, namespaces as GC boundaries, pins/leases. Move when Arca repo carries its design.
- `188-component-data-archival-and-garbage-collection-2026-06-03.md` → **skills/ (a new component-data-lifecycle skill) or sema-engine ARCHITECTURE.md**: Component-wide data lifecycle vocabulary (DataLifecycleState, Recoverability, RetentionPolicy variants), the active->candidate->tombstone->archive->collect->compact->purge shape, and the constraints (Zero is review not deletion; no silent background hard deletion; recoverability is explicit policy). Mature enough to be a shared skill.
- `175-dji-mic-keepalive-profile-churn-and-deploy-fix-2026-06-01.md` → **/git/github.com/LiGoldragon/CriomOS-home skills.md / module comments (and CriomOS desktop-audio-policy)**: The core PipeWire-reassertion lesson already landed (CriomOS-home/skills.md:145). Still to migrate: the WirePlumber host-as-audio-gateway HSP/HFP role split rationale and the repository-ledger GitHub-mirror + bracket-NOTA deploy-portability fix, so the report can retire once those are documented near the modules.
- `181-ghostty-file-link-editor-open-2026-06-02.md` → **/git/github.com/LiGoldragon/CriomOS-home (editor-link runbook / module comments)**: The CriomOS Codium launcher behavior (trim trailing spaces, strip :line[:column] when the file exists, resolve Primary-relative report paths from Ghostty cwd, codium --goto), text/rust MIME registration, and the emitter-side jump-to-line recommendation. Move to a CriomOS-home doc so this deploy-log chain can retire.
- `183-engine-report-tooling-criomos-side-2026-06-03.md` → **skills/engine-report.md (or system-operator skill)**: The engine-report tool usage guidance: leta workspace add / files / grep / show / refs; tokei/scc for counts; ast-grep for syntax-tree queries where LSP is weak. The CriomOS-home bundle changes already landed; the usage discipline belongs in the engine-report skill.

### system-designer
- `64-spirit-hash-identity-and-time-recency-concept-2026-06-04.md` → **/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md (and spirit ARCHITECTURE/INTENT)**: The frozen-random-hash identity design + the resolved base36-lowercase per-kind 3-char-minimum citation scheme (Spirit 2599/2611/2592/2608) + the identity-vs-recency split rationale. The design LANDED in persona-spirit code (random identifiers, short codes, migration.rs); its architecture record should move into the repo's ARCHITECTURE.md so the report can retire.
- `70-cluster-data-feature-horizon-criomos-2026-06-04.md` → **/git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md (and CriomOS ARCHITECTURE)**: The Horizon cluster-data model walk-through: ClusterProposal input shape → project(viewpoint) → enriched per-node Horizon → CriomOS node config → runtime, and the two-parallel-deploy-stacks distinction. Reusable architecture; belongs in horizon-rs/CriomOS permanent docs.
- `79-terminal-layer-decomposition-2026-06-06.md` → **/git/github.com/LiGoldragon/terminal/ARCHITECTURE.md**: The adopted terminal-control decomposition (Spirit ckhx/5fd6/bcca): orchestrate owns lifecycle policy, systemd owns OS process supervision + restart-survival, terminal-control owns the durable sema instance registry used to reattach to surviving cells. This is settled design that should land in the terminal repo's ARCHITECTURE.md.
- `87-triad-main-landed-and-cloud-pilot-complete-2026-06-06.md` → **/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md (and triad-runtime)**: Two emitter-design findings from the cloud pilot: (1) working-socket mode is not emitter-configurable (only the meta tier gets a mode knob) — needs a WorkingListenerTier mode + working_socket_mode() on DaemonConfiguration; (2) the bare-name→pair enum grammar (bare name = unit variant; pair = tuple variant) and the now-emitted role-marker impls — the current grammar contract every contract schema must follow. These belong in schema-rust-next's emitter docs.

### cloud-designer
- `14-gemma4-multimodal-llamacpp-design-2026-05-29.md` → **/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md (or a CriomOS local-AI/llm section) and/or a primary skills/local-ai-cluster.md**: The durable local-AI serving design: Strix Halo gfx1151 Vulkan-not-ROCm rationale, llama.cpp router-mode mmproj preset wiring, the BF16/Q8/UD-Q4_K_XL quant ladder, and the Gemma-4 sampling defaults. This is design substance that outlives the b9404-build-fix task and belongs in a CriomOS/local-AI permanent doc. Flagged, not deleted — keep report 14 until the substance lands.
- `11-backup-network-implementation-review-2026-05-29.md` → **/home/li/primary/skills/nix-discipline.md (router-node deploy-safety) + CriomOS router ARCHITECTURE.md (independent-backup-stack design)**: The router-node deploy-safety rule (BootOnce/Boot never Switch until out-of-band console; restartIfChanged=false guard) and the Path-A independent-dumb-stack backup-network design (own subnets, networkd DHCP, masquerade forward rule, drop bridge=br-lan). Report 15 already flagged these as migration candidates (its gap #7); still pending. Keep the report until the Path-A vs Path-B psyche decision lands and the rule reaches a permanent doc.

### pi-operator
- `1-zeus-deploy-and-lojix-wrapper-research-2026-06-04.md` → **/git/github.com/LiGoldragon/lojix/INTENT.md**: The long-term typed-deploy-ledger design direction: that the lojix-cli/lojix daemon should absorb typed deploy ledgers and typed status replies (operator-summary-vs-machine-stdout as a typed output policy, not a flag; a deploy ledger under a stable state directory; a read-only recent-deploys operation; one-NOTA request rule preserved). The near-term lojix-run wrapper already landed in CriomOS-home; this forward direction belongs in lojix's own INTENT.md so it survives once report 1 is eventually retired. Do not delete report 1 until this lands.
- `8-ouranos-desktop-survivability-2026-06-05.md` → **/git/github.com/LiGoldragon/CriomOS-home/INTENT.md**: The open operator follow-ups that have NOT yet landed: Phase 2 demote-heavy-work-by-construction (a systemd-scope workload wrapper for agents/Codex/Nix builds), Phase 4 pressure visibility + emergency kill controls (psi-notify, launcher hotkey for cgtop, hotkey to kill the workload scope), and the legacy Spirit daemon StartLimitBurst/StartLimitIntervalSec fix so a failed obsolete daemon slot cannot restart forever. These are durable resource-safety intent for the operator desktop; the merged report keeps them until they land in INTENT.md or are implemented.

### small-lanes
- `176-upgrade-mechanism-soup-to-nuts-2026-05-25.md` → **/git/github.com/LiGoldragon/upgrade/ARCHITECTURE.md**: The durable upgrade-mechanism MODEL — the seven UpgradePlan projection kinds (Identity / Standard / Annotated / Added / Renamed / Dropped / Untranslatable) with their plan-derivation algorithm and loud-failure cases, the copy+migrate DB phase ordering, and the §13 ideal-vs-today deviation table — should migrate into the upgrade repo's ARCHITECTURE.md (and the handover-ceremony vocabulary into signal-version-handover/ARCHITECTURE.md) once the actor-native upgrade path stabilizes. Re-express against the current schema-rust-next / kameo-actor architecture (designer/565), dropping the stale 3-socket / signal_channel! / hand-written-From implementation snapshot. After it lands there, 176 becomes a clean DROP.
- `1-role-registration-2026-06-06.md` → **/home/li/primary/skills/videographer.md**: The role definition (video-as-craft scope: filming/screen-capture, editing, captioning, encoding, publishing-prep for short-form vertical and long-form) and the ephemeral-tooling constraint (ffmpeg/ffprobe from the nix profile, transcription/caption tooling via nix run, never stateful pip/virtualenvs per Spirit j4r1) should move into the not-yet-written skills/videographer.md and a Role entry in skills/skills.nota. Until that skill file exists this registration report is the role's only durable craft-discipline record, so KEEP it; do not delete before the skill file lands.

## Method note

Per `skills/context-maintenance-deep.md`: cross-lane sweep, one record in the
dispatcher's (designer) lane, organised lane-second. The dispatcher executed
only verified drops; six agent-proposed drops failed landing verification and
were kept — the landing gate working as intended (a named-but-wrong landing is
not a landing). Agglomeration bodies are agent syntheses; the deleted originals
remain in git history.

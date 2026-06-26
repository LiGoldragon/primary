# Legacy Disposition — Decision Surface (2026-06-26)

## How to use

Walk this theme by theme. For each topic, you make one call: route it to a **bead** (tracked work), to **Spirit** (durable intent), or **drop** it (already tracked elsewhere or no live residue). The proposed fate and bead/intent candidates below are agent synthesis to speed your read — they are suggestions, not commitments. Every intent candidate is written in agent words and marked "psyche to state"; nothing here is recorded. After you route, bead creation and Spirit records happen as separate gated steps.

## Totals

52 topics across 6 themes: 37 lean work, 6 lean intent, 9 drop. Per-theme tally appears at the head of each section.

## T1 — Cloud / Lojix-VM / Deploy-Testing

Scope: lojix runtime + contained-cluster testing, VmHost capacity, cloud provider credentials and DNS, CriomOS deploy harnesses, microvm standup. Tally: 8 work / 2 intent / 3 drop (13 topics).

**Lojix contained cluster testing — ordinary contract update + RunContainedCluster coordinator** — Design fully converged (reports 156–164, 237, 240): testing is the lojix ordinary face, not a separate crucible. Public verb grammar settled (DeployContained/VerifyContained/Release/Query; ContainedRun* nouns). Three untracked layers remain: (1) signal-lojix ordinary contract update replacing the stale CheckContained/TestRun* POC, making DeployContainedRequest.source authoritative, routing verify/release through SEMA/Nexus; (2) daemon-owned RunContainedCluster coordinator (report 163 spec) — ClusterRunRecord, co-live barrier, release-all on failure, restart reconciliation; (3) two compile-time blockers (stale signal-criome artifacts + stale CriomOS-test-cluster Rust channel hash) per report 240. primary-exzf covers the Nix flake side only.
Proposed fate: work.
Bead candidates:
- lojix ordinary face: land VerifyContained/DeployContained/Release/Query contract; ContainedRun* rename; source authoritative; SEMA/Nexus routing — replace the stale CheckContained POC so the lower contract stops lying about status/source/release before the coordinator lands on top.
- lojix daemon: implement RunContainedCluster cluster coordinator (report 163 spec) — ClusterRunRecord + co-live barrier + release-all on failure + restart reconciliation; aggregate lifecycle composing per-member DeployContained/VerifyContained/Release.
- CriomOS-test-cluster: unstale signal-criome generated artifacts + Rust channel fixed-output hash — clear both freshness blockers so the hermetic gate witness compiles.
Source: reports/system-designer/156, 163, 164; reports/system-operator/237, 240.

**VmHost capacity limits — typed HostCapacity + lojix runtime ledger** — (Merged from two readers.) Report 83 proposes HostCapacity (GuestRamBudget/DiskBudget/CoreBudget newtypes, or ram_gb/disk_gb/cores) on NodeService::VmHost; horizon-rs makes over-subscription a static projection eval error (same mechanism as maximum_guests); lojix holds the runtime admission ledger (extends intent mq5s); per-guest QEMU/cgroup caps enforce the slice post-placement. Breaking NOTA arity change; sequence after the active prometheus VmHost datom work. primary-dw95 covers the test node standup, not the budget field.
Proposed fate: work.
Bead candidates:
- horizon-rs VmHost: add typed HostCapacity field + projection fit-check — sequence after active VmHost datom work on prometheus clears.
- lojix: runtime capacity ledger for VmHost guest placement admission — admit/deny new guests against declared HostCapacity, checking live used budget before provisioning.
Source: reports/cloud-designer/83; reports/pi-operator/14.

**CriomOS CloudNode deploy harness — mechanical audit residue** — CloudNode image is live on DigitalOcean (report 76); branches tracked by primary-n98t; report 77 resolved doris trust and TypeIs deletion. Two HIGH Rust bugs from audit 75 remain untracked: until_running returns the last non-running poll as success on timeout (lets the harness SSH a droplet that never booted); ServerSpec has no ipv6/monitoring fields so they are hardcoded false at the call-site rather than typed desired-state.
Proposed fate: work.
Bead candidate: cloud DO harness — fix until_running timeout return + add typed ipv6/monitoring to ServerSpec.
Source: reports/cloud-designer/76, 77.

**Lojix daemon — credential management + meta-lojix admission vocabulary** — Lojix 0.3.10 live, production deploy to prometheus complete (report 241, 2026-06-24). Two untracked follow-ups: (1) installed daemon relies on the operator SSH agent socket for target deploy — a production daemon should pass credentials explicitly (security isolation gap); (2) meta-lojix replies Deployed at admission time before the node has switched, misleading callers into reading admission as terminal success. primary-srmq covers Nix-eval auth, not SSH deploy credentials.
Proposed fate: work.
Bead candidates:
- lojix-daemon: design first-class deploy credential passing (decouple from operator SSH agent).
- meta-lojix: rename Deployed reply to reflect admission, not terminal success (Accepted / DeployAccepted).
Source: reports/system-operator/241.

**Prometheus microvm / VmHost test node standup** — Prometheus VmHost deployed (gen 49, TestVm built-but-not-booted). All actionable items tracked: primary-dw95 (boot vm-testing, reach on Yggdrasil), primary-wvey (typed VmTesting redo removing dead string-keyed vm-testing/default.nix; also absorbs the pi-operator VM-feature-gate CriomOS counterpart).
Proposed fate: drop.
Source: reports/cloud-designer/43; reports/system-designer/155; reports/pi-operator/14.

**Lojix VM rewrite arc (cloud-designer 23–55)** — Bulk documentation of the lojix rewrite through production cutover. Core landed (0.3.10 on Ouranos, horizon 5-root ClusterProposal, SEMA rebuilt, build-on-target verified). All open threads tracked: primary-vhb6, primary-srmq, primary-hpx, primary-da7, primary-fdd7, primary-36iq.7.2.
Proposed fate: drop.
Source: reports/system-operator/241; reports/cloud-designer/42.

**Cloudflare flake gopass path bug + under-scoped token** — cloud/flake.nix line 46 reads `cloudflare/api-token` (absent); the live token is at `cloudflare.com/token` and is under-scoped (passes /accounts but returns zero zones, refuses self-inspection — lacks Zone:Read and DNS:Edit). Live DNS round-trip is blocked until both are fixed. Implied by primary-x8by but not discrete.
Proposed fate: work.
Bead candidate: fix cloud/flake.nix Cloudflare gopass path + mint scoped DNS-edit token (Zone:Read + DNS:Edit) registered at the corrected path.
Source: reports/cloud-designer/69; reports/cloud-operator/392, 393.

**Cloudflare canonical gopass path — Spirit nsi2 drift** — Spirit nsi2 names `cloudflare.com/api-token` as canonical; reports 69/392/393 consistently say the live token lives at `cloudflare.com/token`. Either stale docs from before the do-.com convention fix or a genuine second token. Report 393 defers all live Cloudflare DNS mutation until reconciled. Picking a name is psyche authority, not a mechanical fix.
Proposed fate: intent.
Intent candidate (psyche to state): "The canonical gopass path for the Cloudflare API token is cloudflare.com/token (not cloudflare.com/api-token); Spirit record nsi2 should be updated to reflect this before any live Cloudflare DNS mutation proceeds."
Source: reports/cloud-designer/69; reports/cloud-operator/393.

**CriomOS-test-cluster domain consumer — close current operator slice** — A cloud-operator claim holds a partial domain-config migration (fixture NOTA updated with criome fieldlab, generated JSONs expose domainConfiguration, docs updated). Outstanding: run pure/eval checks (projections-match-fieldlab, cluster-contracts, module-contracts, source-constraints, rejection checks) and add a downstream consumer proof reading cluster.domainConfiguration instead of hardcoded criome.net, then release the claim. Report 393 says releasing this unblocks primary-exzf.
Proposed fate: work.
Bead candidate: CriomOS-test-cluster — run domain consumer pure/eval checks, add consumer proof, commit+push, release the cloud-operator claim.
Source: reports/cloud-operator/392, 393.

**Browser secret-capture bridge for cloud API token flows** — (Cross-theme: see T6 Browser Automation.) DigitalOcean token creation is browser-only with one-time display. Report 2 (cloud-maintainer) gives a complete design: Chrome extension + native messaging host detecting the displayed token and writing it directly to gopass via stdin, returning only a blind receipt (path, byte-length, exit code), origin-whitelisted to cloud.digitalocean.com with per-run human consent. Should be separate from the CDP bridge (different authority).
Proposed fate: work.
Bead candidate: build secret-capture-bridge — Chrome extension + native messaging host for gopass capture.
Source: reports/cloud-maintainer/1, 2.

**Prometheus builder — nixos-test feature missing, blocks VM checks** — Report 81: prometheus builder advertises [big-parallel, kvm] but not nixos-test, so runNixOSTest builds (including web-host-serve, the live VM proof for the web-host epic) fail to find a machine. The check type-checks green but cannot execute. Config item on the node builder declaration; primary-dw95 is scoped to standing up the host, not the builder feature.
Proposed fate: work.
Bead candidate: add nixos-test to prometheus builder supportedFeatures.
Source: reports/cloud-designer/81.

**Immich hosting — trusted node and public URL model** — (Cross-theme: see T6 Immich Mirror.) Immich holds private media and must not run on low-trust doris; the cluster needs one public domain serving two trust models. Proposed canonical phone URL immich.goldragon.criome.net. Trusted-node identity and auth exposure (reverse-proxy through doris? which always-on node? remote upload?) remain open psyche decisions gating primary-0bab past current infra.
Proposed fate: intent.
Intent candidates (psyche to state):
- "Immich runs on a trusted (always-on, non-doris) cluster node, not on the low-trust cloud edge; the canonical phone URL is immich.goldragon.criome.net derived from the cluster public domain; doris hosts only static sites."
- "Public Immich exposure (remote upload from outside the Criome WiFi AP) is not enabled initially; split-horizon DNS provides the public name with a private LAN address only while on the Criome AP."
Source: reports/cloud-operator/392, 393, 389.

**LojixOS generic OS extraction from CriomOS** — Report 390 sketches extracting generic NixOS platform machinery into LojixOS, leaving CriomOS as the brand/cluster wrapper. The report itself says defer until the domain-config PoC plus two-or-three config-seam cleanups land; frames it as unsettled design direction with no timeline. Nothing actionable now.
Proposed fate: drop.
Source: reports/cloud-operator/390.

## T2 — Schema / Spirit / Sema

Scope: schema self-describing redesign, schema-next lowering engines, sema-engine privacy policy nouns, Spirit record alignment to the SpecifiedSchema era, intent-storage substrate. Tally: 3 work / 3 intent / 2 drop (8 topics).

**Schema self-describing — Decision-A camelCase migration + TypeReference unification + SchemaHelp renderer** — schema-designer/25 lays out a 4-area sequenced plan: (1) fix the lossy lowering in schema-next/src/source.rs that bakes snake_case into stored FieldDeclaration.name (four Name::new(self.name.field_name()) sites at 2499/2515/2524/2541); (2) create a unified TypeReference in nota-next/src/type_reference.rs replacing three near-duplicate vocabularies in the seed crate; (3) build a SchemaHelp live renderer in schema-next/src/help.rs returning a TypeHelpNode tree with no authored prose; (4) wire mentci-lib via a RenderHelp trait. Steps 1+2 bundle (shared blake3 re-key); 3 gated on 1; 4 gated on 3. Five decisions locked (memory: store canonical names, Decision A, one-time identity re-key); item 11 (where Menchie obtains the stored Schema at runtime) is the load-bearing open blocker for step 4. primary-xzzf is about token parsing; primary-80cw is a different daemon delivery mechanism — neither covers these.
Proposed fate: work.
Bead candidates:
- schema-next Decision-A: store camelCase as canonical field name, project snake_case at Rust emit — fix the four source.rs sites; move snake_case projection to schema-rust-next RustFieldTokens::to_tokens; update RustIdentifier::verify_field; fix the from_type_reference round-trip guard; audit derived_field_name positional names.
- nota-next: unify the three TypeReference vocabularies into a seed type (bundle with the Decision-A re-key) — add nota-next/src/type_reference.rs with the union scalar set; update instance_schema.rs; re-export/alias in schema-next; remove the SourceReference bridge after unification.
- schema-next: implement SchemaHelp live type-level renderer returning TypeHelpNode (no prose strings) — SchemaHelp over &Schema; TypeHelpNode tree; HelpDepth with cycle guard; tokens via SourceReference::rendered_schema_text. Gated on Decision-A.
Source: reports/schema-designer/25, 19.

**Nota default-policy — *deref marker (d3r2 refinement)** — nota-designer/663 grounds the schema-emitted impl default policy. The main emission flip (standard_newtype_impls default-on, accessors, VariantMatch, typed errors) is tracked as primary-o7j2.1. Untracked: d3r2 records "newtype Deref by default" but the 663 census finds 189 schema-wrapping newtypes of which only ~24 want Deref (~88% must stay opaque). The report recommends refining d3r2 to "Deref is opt-in via a *deref marker" — a new schema token + fixed emit template — needing psyche ratification before implementation. Transitive-scalar leaf inheritance is also a psyche-input item.
Proposed fate: intent.
Intent candidate (psyche to state): "Clarification on d3r2: the Deref capability is standard and template-generated, but applied per-newtype via an explicit *deref schema marker — never blanket-default — because 88% of newtypes (189 of ~207) must stay opaque to preserve their abstraction boundaries; the ~24 semantic-occasion wrappers that do want Deref declare it explicitly."
Bead candidate (only if ratified): schema-next + schema-rust-next — add *deref newtype marker + emit Deref impl template for the ~24 transparent wrappers; delete the corresponding hand-written Deref walls.
Source: reports/nota-designer/663; reports/designer/730/1.

**Asschema-era Spirit record alignment + straggler cleanup** — (Merged from two readers: schema-designer/19 sweep + schema-designer/20 execution log.) The Spirit store still carries records framing Asschema as the canonical resolved artifact, contradicting the live VeryHigh decisions 6cfr (Asschema removed) and 6grf (SpecifiedSchema is the one IR). Three residue clusters remain: (a) hc0t (VeryHigh, guardian-protected — three guardian rejections blocked a Clarify because its second sentence is a live load-bearing codec-floor constraint): psyche must either restate it in their own words to allow Supersede, or confirm it is held by aipc/kfqa plus the report-18 codec-floor rule and Retire; (b) report 19's named Supersede/Retire set (n9ta, av1q, sfwv, yuku) and Clarify set (bkcd, b2jg, t5wx, oxgh, mcuk, xbu8, py4h) — agents have ready-to-run calls awaiting authorization; (c) six straggler descriptions still carrying "AssembledSchema" (a9sq, ppuk, 506w, gb3d, sd7x, khbv) plus a referent-tag normalization pass over the 7 already-clarified records. This is psyche-only authority; once authorized the description/tag fixes are mechanical.
Proposed fate: intent (psyche-gated; bounded Spirit-maintenance work follows authorization).
Intent candidate (psyche to state): "Authorize Spirit maintenance to align the intent store with the Asschema-removed era: resolve hc0t (Supersede restating the codec-floor constraint in your own words, or Retire against aipc/kfqa plus the report-18 codec-floor rule); Supersede or Retire the pure-Asschema records (n9ta, av1q, sfwv, yuku) whose artifact no longer exists; Clarify the dual-content records (bkcd, b2jg, t5wx, oxgh, mcuk, xbu8, py4h) to strip dead Asschema framing while preserving each surviving rule; then run the mechanical description fixes on the six stragglers (a9sq, ppuk, 506w, gb3d, sd7x, khbv) and normalize the stale asschema referent tag on the 7 clarified records — agents have the ready-to-run calls."
Bead candidate (post-authorization, mechanical): Spirit — apply SpecifiedSchema-era description fixes to the six straggler records + run the single referent-normalization pass.
Source: reports/schema-designer/19, 20.

**schema-next macro-path deletion — two lowering engines with latent nested-namespace divergence** — designer/702-deep-engine-analysis/2 finds schema-next has two lowering engines: the production source path (SchemaSource::to_schema via module.rs) and a test-only macro/document path (lower_document_with_resolver) that lacks a nested-namespace case (engine.rs:659), silently mislowers nested namespaces, and silently drops impls for nested targets (engine.rs:469-476). The flat-shape witness only proves agreement for flat schemas. Recommendation: delete macro-path declaration/root lowering, make lower_source a thin SchemaSource::lower wrapper — one engine by construction. primary-vllc fixes a specific bare-header bug plus a both-paths witness — a different remedy from structural deletion. Production-masked today but a latent trap for any test exercising the macro path on nested schemas.
Proposed fate: work.
Bead candidate: schema-next — delete macro-path declaration/root lowering; make lower_document_with_resolver and lower_source thin wrappers over SchemaSource::from_document(...).lower(...); delete the hand-mirrored NamespaceEntryWalk and the dead Derived-field '*' encoder branch (source.rs:2329).
Source: reports/designer/702/2, 690/1.

**Sema-engine privacy-class / DurabilityClass policy noun design** — system-designer/95/11 + system-operator/215 establish a privacy-class-driven durability spectrum: private payloads encrypt-then-commit-over-ciphertext; mirror stays zero-knowledge; erasure is key-shred; existence-private material skips durable versioning. Report 215 names 11 policy nouns (PrivacyClass, DurabilityClass, RetentionPolicy, RemotePayloadMode, KeyScope, ErasureMode, ErasureVisibility, ErasureReceipt, PayloadEnvelope, KeyCustodyPolicy, CheckpointPayloadClass) that must enter the sema-engine log format before the remote mirror hardens, to stop private plaintext drifting into the public-permanent path by default. primary-s22j and primary-qu28 do not name this prerequisite.
Proposed fate: work.
Bead candidate: sema-engine — add the 11 privacy policy noun types to the log format before remote code hardens.
Source: reports/system-designer/95/11; reports/system-operator/215.

**Uncaptured first-degree intent principles from the 730 disposition session** — designer/730/3-HANDOVER names two psyche principles stated in-session that passed the Spirit gate but were never recorded: (1) intent should be first-degree, with an alignment to establish certainty (a refinement of the intent-primordial records); (2) the active report inventory should stay clean, lean, small. The handover directs querying the intent domain first — these may be Clarify/Supersede of existing high-magnitude records ("intent is primordial", "inferring intent is forbidden") rather than fresh Records.
Proposed fate: intent.
Intent candidates (psyche to state):
- "Intent is established first-degree: only psyche statements become Spirit records; agent-written reports and files are not intent sources, only a thread-map. Certainty is established through an alignment exchange, not inferred from agent text."
- "The active report inventory should be small at all times: reports are generated to carry work to a landing point (bead or Spirit record) and cleared when their substance is captured; accumulation without landing is a discipline failure."
Source: reports/designer/730/3-HANDOVER.

**Spirit privacy / lifecycle operations cluster** — Large cluster (archive system, lifecycle ladder, CollectRemovalCandidates, restore, named private-capture form, ChangePrivacy, typed query split, typed feedback, stream archive). All tracked: primary-wk88, primary-v1w7, primary-uwo0, primary-dn1e, primary-flwg, primary-tiyo. Nothing untracked.
Proposed fate: drop.
Source: reports/system-designer/60, 110; reports/system-operator/192.

**Sema VC hardening + spirit substrate + intent-storage substrate rollout** — Three clusters: (A) sema VC design/integration; (B) spirit substrate hardening (sema migration cleanup, kernel sealing, adopt_head, corpus agglomeration, off-host backup); (C) intent-storage rollout (8rpu decision, INTENT.md/ESSENCE.md deprecation). All tracked: primary-qu28, primary-s22j, primary-mlck; primary-c4dz epic + c4dz.1-8; primary-ebev, primary-sfr3, primary-7d8m.4/.5.
Proposed fate: drop.
Source: reports/system-operator/214; reports/schema-designer/21; reports/designer/730/1.

## T3 — Criome / Router / Mentci / Propagation

Scope: guardian-as-criome-contract substrate, spirit CriomeGate, mentci-lib engine evolution, mentci↔introspect, orchestrate harness memory gate, propagation/telos. Tally: 7 work / 0 intent / 1 drop (8 topics).

**Guardian-as-criome-contract substrate — signal-criome evidence type, criome eval path, spirit caller-side** — Reports 458/459/723 converge on a first build making spirit's guardian the first criome-contract LLM-workflow guard. The orchestrate engine (primary-fzwd.1) and the escalation ladder above EscalateToPsyche (primary-om4g.12) are tracked; three contract/spirit pieces are not: (a) a typed content-addressed WorkflowReceipt in signal-criome; (b) a criome evaluation path that verifies content-address + adjudicator identity and signs a grant; (c) spirit extracting GuardianOperation into a workflow payload boundary, replacing the direct AgentGuardian call with criome-mediated authorization in Gating mode. Open design fork (report 459): generic WorkflowReceipt parameterized by kind vs GuardianWorkflowReceipt-first; operator recommends the generic envelope.
Proposed fate: work.
Bead candidates:
- signal-criome: generic content-addressed WorkflowReceipt evidence type for workflow-backed authorization.
- criome: evaluation path — local workflow receipt → verify content-address + adjudicator identity → signed AuthorizationGrant.
- spirit: extract GuardianOperation into a workflow payload boundary; replace the direct AgentGuardian call with a criome authorization request in Gating mode.
Source: reports/operator/458, 459; reports/designer/723.

**Spirit CriomeGate — AuthorizationPending unhandled in Observing mode** — Report 457 flags an open edge: CriomeGate::authorize_signal_call expects AuthorizationGranted immediately, but criome in ClientApproval mode returns AuthorizationPending. Observing mode should treat it as "parked, visible in mentci, proceed"; Gating mode should block until a grant arrives. Without this the full Spirit daemon → criome ClientApproval → mentci approval loop cannot run from the live runtime. primary-om4g.2 is deployment config; primary-iy51.4 is mentci-side rejection surfacing — neither is this source change.
Proposed fate: work.
Bead candidate: spirit — CriomeGate handle AuthorizationPending (proceed-parked in Observing, block in Gating).
Source: reports/operator/457, 456.

**Spirit production safety — tag deployed baseline + pin CriomOS-home before guardian migration** — Operator (458) and designer (723) both call for tagging the current deployed spirit (plus signal-spirit, meta-signal-spirit) and confirming CriomOS-home pins to immutable tags/exact revisions before advancing spirit main through the guardian refactor. The psyche stated in 723 that production should be tagged so main can move freely. primary-yluj covers rebuild/redeploy after the schema migration, not establishing the pre-migration safety tag.
Proposed fate: work.
Bead candidate: tag deployed spirit/signal-spirit/meta-signal-spirit production baseline; confirm CriomOS-home immutable pin.
Source: reports/operator/458; reports/designer/723.

**Mentci-lib evolution to async engine layer (jwm9)** — Spirit jwm9 names mentci-lib as the async engine layer below the GUI — actor system, Nexus/SEMA planes, portable embedding by multiple clients — not the current client-only ObservationModel. Operator brief 453 assigns the transition to designer. The mentci epic (iy51.1) builds the daemon binary over the current lib; it does not restructure the lib into the shared engine substrate.
Proposed fate: work.
Bead candidate: mentci-lib — evolve to embeddable async engine layer (actor system + Nexus/SEMA planes) so CLI, egui, and embedded clients share one engine.
Source: reports/maintainer/3/0; reports/operator/453.

**Mentci ← introspect integration — trace ingress + query panes** — Brief 453 defines the new spine: schema-generated typed trace events → introspect intake → mentci queries introspect → mentci-lib panes with NOTA fallback. Missing: a trace-ingress contract from schema-generated events into introspect, a general component/message/schema-symbol query surface, a subscription surface, mentci-side requests + model panes, and a deploy path. 4ddb.2 fixes the dead trace plane; 4ddb.1 adds ComponentTrace CLI; 80cw.5 adds schema specs — none cover introspect becoming a general intake service or mentci wiring to it.
Proposed fate: work.
Bead candidates:
- introspect: general schema-trace intake service (typed ingress + component/message/symbol/time query surface).
- mentci daemon: introspect query client + mentci-lib model/render panes (egui panes for component traces, NOTA fallback).
Source: reports/operator/453; reports/maintainer/3/0.

**Orchestrate/harness — Claude spawn shared-memory gate (wl2a)** — (Cross-theme: see T4 Agent memory gating.) Report 465 captured Spirit wl2a (shared agent memory default; Claude-specific memory an explicit gated path). Plan: a CriomOS-home Claude wrapper/launcher defaulting to shared-memory-only, an explicit escape hatch for Claude-specific memory, and wiring the gate at the orchestrate spawn adapter boundary (not at every role-mapping site in orchestrate/src/role.rs). The fzwd epic covers the workflow engine, not harness launch policy.
Proposed fate: work.
Bead candidates:
- orchestrate/harness spawn adapter: default Claude to shared-memory-only mode; explicit opt-in; gate at the spawn adapter.
- CriomOS-home: Claude wrapper enforcing shared-memory-only default (preserve --add-dir/workspace-contract injection; separate opt-in command).
Source: reports/operator/465.

**Mentci available local test surface — CriomOS-home package + GUI theming (cok7)** — Brief 453 defines the smallest deployable next surface: add mentci-egui as a CriomOS-home flake input installed to the local profile (no manual LD_LIBRARY_PATH), run mentci-daemon as a test user service with a stable socket. Separately, intent cok7 (mentci-egui follows system light/dark theme) is recorded but unimplemented (eframe 0.27 defaults dark, ignores system portals; interim force Theme::Light, later Chroma integration). iy51.12 is the nixosTest VM keystone on Prometheus — distinct from local ouranos deployment.
Proposed fate: work.
Bead candidates:
- system: mentci-egui + mentci-daemon in CriomOS-home as local test surface on ouranos.
- mentci-egui: system light/dark theme following (cok7) — interim Theme::Light, later Chroma/portal.
Source: reports/operator/453; reports/maintainer/3/3.

**Propagation loop and telos / agreement-machine** — Designer reports 677/678/680/694-700 covered in the designer-weave. The 730 ledger placed telos items as abandon (Spirit p3td, pviw, m0p2, l2ha) and the propagation loop as tracked (primary-l6xg). Operator 426-435 subsumed; 456-457 already in 4ddb or covered above.
Proposed fate: drop.
Source: reports/designer/730/3-HANDOVER, 730/1.

## T4 — Governance (Guardian / Intent / Privacy / Roles)

Scope: privacy guard hardening, pre-rule Spirit record disposal, private-spirit substrate, guardian burden prompts, 8rpu intent-file deprecation, agent-memory gating, alignment-interview skill. Tally: 6 work / 1 intent / 1 drop (8 topics).

**Privacy guard hardening edits (counselor/3 concrete pending)** — counselor/3 proposed nine edits after a 2026-06-02 audit; G3/G4 closed same day. Remaining: G1 (symlink aliases repos/assistant-reports + repos/counselor-reports not named in the AGENTS.md hard override), G2 (PreToolUse hook backstop for Read/Glob/Grep/Bash targeting private paths), G5 (subagent-briefing privacy rule in skills/role-lanes.md), G6 (privacy cross-ref in operator.md/designer.md/system-operator.md/poet.md), G7 (privacy-as-boundary statement in ESSENCE.md). Draft text already supplied; the designer-weave excluded counselor/assistant lanes.
Proposed fate: work.
Bead candidate: apply counselor/3 privacy guard hardening (G1/G2/G5/G6/G7) — AGENTS.md symlink aliases, PreToolUse hook, role-lanes subagent rule, four public-role cross-refs, ESSENCE.md mention.
Source: reports/counselor/3; reports/assistant/3.

**Pre-rule Spirit records — psyche authorization needed** — Four Spirit records (1429, 1430, 1435, 1436) were captured before the privacy rule absorbed into the counselor lane; they hold personal substance in ordinary Spirit, queryable by any lane. counselor/3 gives three options (hard delete with tombstones to private-repos first — recommended; soft delete via ChangeCertainty Zero; hold for a future private-spirit substrate). Psyche authorization required; sets precedent for future accidental captures.
Proposed fate: intent.
Intent candidate (psyche to state): "Dispose of Spirit records 1429, 1430, 1435, 1436 (personal substance captured before the privacy rule landed in the counselor lane): write tombstones to private-repos/counselor-reports/ then hard-delete the four records via spirit Remove — OR — hold them for migration to the future private-spirit substrate. Whichever option you choose, that disposition governs all future accidental pre-rule captures."
Source: reports/counselor/2, 3.

**Private intent substrate — private-spirit daemon build** — counselor/2 + assistant/3 recommend a G→A→F progression: G (private-report notes, running) → A (separate private-spirit daemon, same signal-persona-spirit wire contract, own socket + redb on a privacy-isolated path) → F (plus storage-layer encryption). Step A is designed but unbuilt; it would receive the migrated pre-rule records and carry typed private intent for counselor/assistant lanes. primary-c4dz covers public-store items, not a private daemon.
Proposed fate: work.
Bead candidate: build private-spirit daemon (private-spirit binary, separate socket + redb, same wire contract) — step A of the G→A→F roadmap.
Source: reports/counselor/2; reports/assistant/3.

**Guardian burden-prompt — direct psyche-named rung + repair-shaped remands** — operator/463 finds two prompt gaps: burden-ladder.md narrows elevated-importance support to recurrence/blast-radius/keeps-coming-up/blocks-other-work, missing the rule that a direct psyche-named rung is itself sufficient evidence without agent advocacy; checklist.md does not teach the guardian to treat rejections as repair-shaped remands (name the likely Clarify/ChangeRecord/Supersede/Retire/Remove). Keep the typed schema, change only the prompts. Distinct from primary-nlx5 (referent activation, telemetry, gloss rewrites).
Proposed fate: work.
Bead candidate: update spirit guardian prompts (burden-ladder.md, checklist.md, few-shot.md) — accept direct psyche-named rung as sufficient burden evidence; add repair-shaped remand language.
Source: reports/operator/463.

**Intent file deprecation (8rpu) discipline manifestation pass** — (Cross-theme: see T2 intent-storage substrate.) schema-designer/21 records psyche decision 8rpu (High): all intent from Spirit; per-repo INTENT.md, workspace INTENT.md, ESSENCE.md deprecated and migrated. Five surfaces still reference the deprecated files as canonical and need a manifestation pass: AGENTS.md, ESSENCE.md (lines 22-31), skills/intent-log.md, skills/repo-intent.md, skills/skills.nota. ESSENCE.md alignment gaps captured as 4lkn/sj2c/j8g6. schema-designer lane was outside the designer-weave; left as plan step 4, unbeaded.
Proposed fate: work.
Bead candidate: 8rpu discipline manifestation — remove stale per-repo-INTENT.md-as-canonical framing from the five surfaces; point the discipline layer at Spirit queries.
Source: reports/schema-designer/21.

**Agent memory gating — shared-first, Claude-explicit (wl2a)** — (Cross-theme: see T3 orchestrate spawn gate.) operator/465 captured wl2a and ground-truthed: CLAUDE.md is only @AGENTS.md; INTENT.md/ARCHITECTURE.md say memory lives in workspace files but name no concrete gate; CriomOS-home disables MCP but not Claude auto-memory; claude --bare skips auto-memory but also hooks and CLAUDE.md discovery. Three build items: (1) CriomOS-home Claude launcher wrapper defaulting to shared-memory-only with an opt-in hatch; (2) manifest wl2a in INTENT.md + ARCHITECTURE.md naming the gate; (3) expose a first-slice shared-memory surface via the mind daemon (NOTA text).
Proposed fate: work.
Bead candidates:
- CriomOS-home: Claude launcher wrapper (auto-memory off by default + named opt-in); manifest wl2a in INTENT.md + ARCHITECTURE.md.
- mind: expose first-slice shared-memory access surface via NOTA text for cross-agent use.
Source: reports/operator/465.

**Alignment interview — recommendation-per-question and code-first format** — operator/462 studied Matt Pocock's grilling skills + Sandcastle orchestration and identified two edits for skills/alignment-interview.md: (1) every grill question carries a concrete recommendation, not a naked question; (2) the agent inspects code to answer mechanically-discoverable questions rather than asking. Phase-boundary discipline: grill/alignment/issue-slicing in one unbroken context, then fresh context per implementation issue (Spirit 80zj). The skill lacks both Pocock-derived specifics.
Proposed fate: work.
Bead candidate: update skills/alignment-interview.md — require a concrete recommendation with every question; allow code inspection before asking mechanically-answerable questions.
Source: reports/operator/462/1, 462/0.

**Completed registrations, privacy-substrate research, guard-trust-planes** — counselor/1 + assistant/1 (role registrations complete, Spirit 1426/1425); schema-designer/20 (Asschema tombstone executed); operator/459-460 (trust-planes → Spirit ic4o; guard-substrate landed on main); operator/464 (context-maintenance correction, ne92, skill restored). All complete, no live residue.
Proposed fate: drop. (Note: schema-designer/20 residuals are treated as live under T2 — see Cross-theme overlaps.)
Source: reports/counselor/1; reports/assistant/1; reports/schema-designer/20; reports/operator/459, 460, 464.

## T5 — Hardware-Ops

Scope: ouranos hardware durability (Ethernet, Bluetooth, battery, desktop survivability, wired fallback), Rust repo/disk hygiene, peripherals. Tally: 7 work / 0 intent / 1 drop (8 topics).

**ouranos Intel I219-LM Ethernet — declarative EEE-off + firmware update** — Carrier loss traced to I219-LM ULP/SMBus power-management brittleness (upstream patches for Lenovo 8086:550b). Runtime recovery via ethtool EEE-off + interface bounce works but is not declarative (won't survive rebuilds). fwupd reports high-urgency Lenovo System Firmware (0.1.12→0.1.17) and Intel ME (0.10.2403→0.15.2515) updates; ME is named in upstream e1000e ULP bug reports for this hardware.
Proposed fate: work.
Bead candidates:
- declarative EEE-off for ouranos I219-LM in CriomOS (ethtool.eee-enabled = off on the wired NM profile).
- apply fwupd firmware updates on ouranos (Lenovo System Firmware 0.1.17 + Intel ME 0.15.2515) in a plugged-in maintenance window.
Source: reports/maintainer/1.

**ouranos Bluetooth AX211 firmware — safe system generation deploy** — AX211 failed with ibt-0180-0041 missing after a lean OsOnly deploy. CriomOS patched (commit 9d5f9e031db4) adding ThinkPadT14Gen5Intel to modelFirmwareIndex with linux-firmware + sof-firmware; build verified to contain the files. The system generation was not switched — the bootloader default may still be the bad OsOnly generation; a runtime workaround persists until a safe deploy lands.
Proposed fate: work.
Bead candidate: deploy CriomOS T14Gen5Intel Bluetooth fix to ouranos (switch boot default to a generation containing the committed firmware fix).
Source: reports/maintainer/2/2.

**ouranos battery charge thresholds — hybrid-sleep reapply gap** — After hybrid-sleep resume, battery-charge-default.service does not run (wanted by suspend/hibernate targets but not hybrid-sleep.target); sysfs thresholds reset to 0/100, letting the battery charge full. Care mode (75/80%) re-enabled manually. Durable fix: add hybrid-sleep.target (and optionally suspend-then-hibernate.target) to wantedBy in CriomOS modules/nixos/metal/default.nix; a power-supply udev hook is preferable to polling.
Proposed fate: work.
Bead candidate: add hybrid-sleep.target to ouranos battery-charge-default.service in CriomOS.
Source: reports/system-maintainer/709.

**ouranos desktop survivability — open follow-up phases** — A UI-freeze incident (no swap + Nix broad-closure build starving resources) was mitigated (zram + 32GiB swap, ui-priority.nix cgroup props, rescue-terminal Niri binding, session.slice ownership fix). Three open follow-ups: (1) Phase 2 — a workload-scope wrapper launching agents/builds/deploys in a low-priority killable systemd scope (highest-leverage, prevents the root failure by construction); (2) Phase 4 — PSI pressure visibility (psi-notify) + a kill-workload hotkey; (3) stale Spirit v0.1.1 daemon restart loop — add StartLimitBurst/IntervalSec or disable obsolete slots.
Proposed fate: work.
Bead candidates:
- build workload-scope wrapper for heavy agent/build/deploy commands on ouranos (low-priority killable systemd scope).
- add desktop pressure visibility (psi-notify) + kill-workload Niri keybinding.
- fix stale Spirit v0.1.1 daemon restart loop (StartLimitBurst/IntervalSec or disable obsolete slots).
Source: reports/pi-operator/8.

**ouranos prometheus-lan Ethernet autoconnect — make declarative** — Prometheus USB Ethernet hotplug policy is live and correct; the failure was the ouranos client prometheus-lan NM profile (autoconnect=no, never-default wrong). Runtime fix (autoconnect=yes, priority=200, route-metric=50, ipv6.never-default=yes) gave DHCP + internet but is not declarative — won't survive profile rebuilds.
Proposed fate: work.
Bead candidate: declare ouranos prometheus-lan NM profile as autoconnect with route metric in CriomOS-home.
Source: reports/cloud-operator/16.

**Rust repo hygiene — enforced gate, pending migrations, cargo-sweep timer** — After rust-build and migrating 12 repos, 26 of 42 active Rust repos still use raw craneLib.filterCargoSources/cleanCargoSource; five flake-touched repos missed adoption (signal-standard, cloud, meta-signal-message, meta-signal-introspect, mentci-egui). Disk pressure at 93%, ~280 GiB of Rust targets; cargo-sweep reclaimed 31 GiB but targets rebounded to ~149 GiB. Three controls: a scanner that fails on raw Crane calls in changed flakes, migrate the 5 misses, a cargo-sweep user timer.
Proposed fate: work.
Bead candidates:
- workspace scanner: fail on raw craneLib source-cleaning calls in changed Rust flakes.
- migrate 5 flake-touched Rust repos to rust-build (signal-standard first).
- add cargo-sweep systemd user timer on ouranos (--recursive --maxsize 4GB).
Source: reports/system-maintainer/16; reports/pi-operator/2.

**Prometheus model cleanup and DJI/Whisrs serial fix** — Manual GC root removed (deployed roots still protect the model catalog); two Qwen GGUF duplicates deleted after SHA-256 verify; DJI/Whisrs keepalive replaced by serial-resolution at daemon start (object.serial → PIPEWIRE_NODE), deployed and validated; stale slice symlinks cleaned. All closed.
Proposed fate: drop.
Source: reports/system-maintainer/9, 13.

**Razer Kiyo Pro Ultra — add cameractrls to ouranos Home profile** — Known autofocus instability on Linux; the reliable fix is disabling autofocus + manual focus via V4L2. cameractrls 0.6.10 (nixpkgs) has Kiyo Pro-specific controls (AF mode, HDR, FOV, save/restore); v4l2-ctl/qv4l2 already installed for fallback; no official Linux firmware updater. Action: package cameractrls in the ouranos Home profile.
Proposed fate: work.
Bead candidate: add cameractrls to ouranos CriomOS-home profile.
Source: reports/pi-operator/3.

## T6 — Research-Media + Browser

Scope: videographer evidence/editing pipelines, AI music, Immich mirror, browser automation substrate + secret capture, TheBookOfSol audit, editor research. Tally: 6 work / 0 intent / 1 drop (7 topics).

**Video Evidence Packet Harness and Model Bakeoff** — videographer/5 designs a three-tier harness: local FFmpeg/scenedetect/faster-whisper produces a "video evidence packet" (metadata, transcript, scene boundaries, contact sheet, frames); a cheap native-video tier (Gemini 2.5 Flash-Lite / Qwen3.5 Flash) handles coarse review; Pro/GPT-5.5 for hard judgment. A 5-clip bakeoff across 6 conditions is the explicit recommended next experiment before building more.
Proposed fate: work.
Bead candidates:
- build videographer evidence-packet pipeline (structured metadata JSON, word-timestamped transcript, scene boundaries, contact sheet per asset).
- native-video model bakeoff: Gemini Flash-Lite vs Qwen3.5 Flash (5 clips, 6 conditions, scored on scene summary / event localization / editorial usefulness).
Source: reports/videographer/5.

**Codex Local-First Video Editing Workflow** — videographer/3 + 4: the productive Codex pattern exposes editing as files and commands (FFmpeg, ffprobe, ASS captions, project manifests, render pipelines), not asking a chat model to edit MP4s. The toolchain is live (Node, pnpm, faster-whisper, scenedetect — system-maintainer/13) but no workflow harness or manifest format exists.
Proposed fate: work.
Bead candidate: build Codex videographer workflow — per-video manifest format (source metadata, transcript, timeline, render recipe) + FFmpeg/ASS caption pipeline.
Source: reports/videographer/3, 4; reports/system-maintainer/13.

**Immich Agentic Media Mirror** — (Cross-theme: see T1 Immich hosting.) videographer/6 proposed the Immich phone-media mirror; cloud-designer/82 ported it to a CriomOS service module + reverse-proxy web-host extension. Both converge on the same target and privacy posture. Tracked under primary-0bab. Open decisions (trusted node, exposure, agent auth) are for the psyche while executing the bead.
Proposed fate: drop.
Source: reports/videographer/6; reports/cloud-designer/82.

**AI Music — ACE-Step 1.5 Local Cluster Service** — videographer/7 surveyed AI music generators. Production-safe: Stable Audio API + ElevenLabs SFX. Local cluster: ACE-Step 1.5 (MIT, <2s/song A100, <10s RTX 3090, broad GPU support, REST + Gradio). The report explicitly directs system-operator to package ACE-Step 1.5 with acceptance: one prompt → one WAV/MP3 in an agent inbox + a timing and VRAM report.
Proposed fate: work.
Bead candidate: package ACE-Step 1.5 on cluster as a local music-generation API (one prompt → one WAV/MP3 in inbox + timing/VRAM report).
Source: reports/videographer/7.

**Browser Automation — Secret-Capture Bridge and Durable Architecture** — (Cross-theme: see T1 secret-capture bridge.) cloud-maintainer/2 proposes the secret-capture-bridge (Chrome content script detects the DigitalOcean PAT element → native messaging → gopass; LLM gets only a receipt). cloud-maintainer/3 confirms the dedicated automation Chrome profile is live at CDP 9223 (now the default path). system-maintainer/20 recommends dropping browser-use as the durable core (screenshots fire despite use_vision=false; cancellation/timeout mismatches with local Gemma) in favor of direct CDP/Playwright + a local-model planner, with Stagehand evaluated as an optional wrapper. primary-ooh1 and primary-y3is cover browser-use/atlas packaging only.
Proposed fate: work (+ intent candidate below).
Bead candidates:
- build secret-capture-bridge for DigitalOcean PAT (content script → native host → gopass insert; receipt only).
- evaluate Stagehand against the persistent local Chrome CDP profile (9223) + local Gemma (act/extract without cloud browser infra or hidden screenshots).
Intent candidate (psyche to state): "The durable CriomOS local browser-control substrate is direct CDP/Playwright plus a thin deterministic collector; browser-use stays for prototyping and model benchmarking only, not for authenticated SPAs, billing portals, or private sessions."
Source: reports/cloud-maintainer/1, 2, 3; reports/system-maintainer/20; reports/system-operator/174.

**Book of Sol Audit — Apply Findings** — poet/87 is a 309-finding audit of 150 TheBookOfSol files (73 negative-contrast tics, 49 citation errors, 42 quote-format breaks, 20 organization, 10 doctrine contradictions, 9 factual). Eight high-severity findings sit on live Substack posts (chloride/The_Chloride_Indictment.md, diet/Ambrosian_Diet.md, water/The_Distilled_Water_Paradox.md). No bead covers applying any finding.
Proposed fate: work.
Bead candidates:
- apply Book of Sol audit: 8 live high-severity fixes (citation errors + tics on the 4 published posts, then re-publish).
- apply Book of Sol audit: medium-severity citation + format batch (~140 findings across unpublished and published files).
Source: reports/poet/87.

**Honey Viruddha Article** — editor/1 is a complete sourced research deliverable on harmful honey uses per Caraka Samhita Sū 26/27 (heated honey, honey for heat-afflicted persons, honey-caused ama, equal honey+ghee, hot water after honey, fatal combinations) with IAST verses + editor translations, plus the Rgveda 1.90.6-8 baseline — same standard/format as TheBookOfSol source-extracts. No article using these findings is tracked.
Proposed fate: work.
Bead candidate: write TheBookOfSol article on honey viruddha (using Sū 26.84, 26.90, 27.246-248).
Source: reports/editor/1.

## Cross-theme overlaps

These ideas surfaced in two themes and were deliberately not merged. Reconcile each so the same idea is not double-beaded or split with conflicting dispositions.

1. **Secret-capture bridge (T1 ↔ T6).** The DigitalOcean PAT → gopass Chrome-extension + native-host design appears in T1 ("Browser secret-capture bridge for cloud API token flows", cloud-maintainer/2) and T6 ("Browser Automation — Secret-Capture Bridge", cloud-maintainer/1-3). Same design, same source report, both lean work. Route once — a single secret-capture-bridge bead serves both the cloud-token and the browser-automation lanes.

2. **wl2a agent/Claude memory gating (T3 ↔ T4).** The CriomOS-home Claude launcher wrapper (shared-memory-only default + opt-in) appears in T3 ("Orchestrate/harness Claude spawn shared-memory gate") and T4 ("Agent memory gating: shared-first, Claude-explicit"), both citing operator/465 and Spirit wl2a. The wrapper bead is the same; T3 adds the orchestrate spawn-adapter gate and T4 adds the docs manifestation + mind surface. Treat the CriomOS-home wrapper as one shared bead; keep the orchestrate-adapter and mind-surface pieces as distinct beads under their themes.

3. **Asschema-era Spirit cleanup — conflicting disposition (T2 ↔ T4).** schema-designer/20 is read as live residue in T2 (hc0t still open, six stragglers + referent tags queued — intent/work) but as "complete with no live residue" in T4's drop cluster. These conflict. Resolve which is true before routing: if T2's residuals stand, the T4 drop line for schema-designer/20 is wrong.

4. **8rpu / intent-storage substrate — conflicting disposition (T2 ↔ T4).** schema-designer/21 appears as tracked/drop in T2 ("intent-storage substrate rollout", under primary-ebev/sfr3) but as untracked work in T4 ("8rpu discipline manifestation pass" over five named files). Decide whether the five-surface manifestation pass is already inside the tracked beads or is a genuine untracked gap.

5. **Immich (T1 ↔ T6).** Immich appears as an open intent decision in T1 (trusted node, exposure, phone URL — gating primary-0bab) and as a tracked/drop implementation in T6 (primary-0bab + cloud-designer/82). Not a conflict but a split: the build is tracked, the pre-build trust/exposure decision is not. Route the intent decision separately even though the implementation is dropped.

## Next steps

After you route each topic here, bead creation and Spirit records happen as separate gated steps — nothing in this surface is recorded or actioned.

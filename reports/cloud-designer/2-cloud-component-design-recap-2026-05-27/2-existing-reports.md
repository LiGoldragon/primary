# 2 · Existing reports — cloud-component-design substance across lanes

*Sub-agent B's findings. Filed by orchestrator (Explore subagents
are read-only in this workspace); substance below is the
subagent's verbatim sweep.*

32 reports inspected. 13 settled, 2 open, 17 adjacent-only.

## Scope and method

Grepped `cloud` across `/home/li/primary/reports/`, classified
each hit by reading title + opening sections (full content only
when needed). Special attention to `reports/cloud-operator/`
since that lane was written to before being registered.

## Bucket 1 — settled design decisions (13 reports)

### System-operator layer (foundational signal architecture)

1. `/home/li/primary/reports/system-operator/158-signal-foundation-for-cloud-triads.md` — Establishes the signal foundation baseline for the cloud triad. Confirms `signal-frame + signal-sema + signal-executor` is the canonical architecture; names the repository shape (`cloud`, `signal-cloud`, `owner-signal-cloud`); notes `signal-core` is deprecated in favor of signal-frame.

2. `/home/li/primary/reports/system-operator/159-cloud-repo-scaffold-prototype.md` — Audit confirming the six required repositories (cloud, signal-cloud, owner-signal-cloud, domain-criome, signal-domain-criome, owner-signal-domain-criome) did not exist locally or remotely under LiGoldragon/Criome namespaces at the time. Scoping document for the birth design.

3. `/home/li/primary/reports/system-operator/156-cloudflare-api-surface-research.md` — Research mapping the Cloudflare REST API surface (DNS Records API, Zones, Rulesets, Page Rules) for the cloud daemon's first provider target. Confirms `cloudflare-rs` (v0.14.1) as substrate; identifies coverage gaps (Rulesets, Pages, Batch endpoint, CAA records) the daemon handles via plain `reqwest`.

4. `/home/li/primary/reports/system-operator/157-provider-api-scope-research.md` — Research on Google Cloud DNS and Hetzner Cloud APIs. Establishes the provider-capability model; defers server/network mutations until authorization, dry-run, and rollback design is complete. Frames DNS as the immediate narrow target.

5. `/home/li/primary/reports/system-operator/160-cloud-domain-criome-birth-design.md` — The settled birth design. Records the creation of all six repositories with commits cited (cloud `ba35849a`, signal-cloud `29c392bb`, owner-signal-cloud `08f9fa36`, domain-criome `fedc43b0`, signal-domain-criome `3e48fe36`, owner-signal-domain-criome `37c86a42`). Establishes current signal foundation as signal-frame + signal-sema, one Provider trait per vendor, sema-executor dispatching.

### Second-designer production framing

6. `/home/li/primary/reports/second-designer/196-cloud-component-production-design-2026-05-25.md` — Psyche directive narrowing the cloud component's first production target to Cloudflare DNS at minimum. Confirms the schema-engine migration is NOT a blocker; hand-written contract in signal-cloud + owner-signal-cloud is the production wire surface for this push. Defers persistent storage to runtime-only cache (Cloudflare is source of truth). Frames authentication (env-var + password-manager FEMOS pattern) and CLI shell-out preference for ergonomics. Describes the actual runtime-branch state in `/git/github.com/LiGoldragon/cloud` — `src/lib.rs` holds DaemonConfiguration, Store, handle_ordinary/owner_request dispatch, capabilities() matching.

### Third-designer research wave (parallel-main design triad)

7. `/home/li/primary/reports/third-designer/22-cloud-criome-design-research/1-cloud-component-design.md` — Designer sketch of the cloud component triad. Establishes:
   - Single working operation root: `Manage(ManagementRequest)` collapsing provider operations into target-kind + action dispatch.
   - Companion read operations: `Observe(Observation)` and `Watch(Subscription)` with StateStream.
   - Policy contract (`meta-signal-cloud`) carries authority, credential rotation, build-time opt-in queries, provider registration.
   - Per-provider `Provider` trait as the lowering boundary.
   - Three-layer rule: Contract Operation `Manage` → Component Command `ProviderCommand::CloudflareDnsCreate` → Sema Operation `Mutate`/`Match`.
   - Build-time opt-in surfaces as `Reply::ProviderUnavailable`, with `Inspect(ProviderRegistry)` for pre-flight queries.
   - Anchored on spirit intents 281, 282, 283, 287, 290.

8. `/home/li/primary/reports/third-designer/22-cloud-criome-design-research/2-domain-criome-component-design.md` — Designer sketch of the domain-criome triad. Establishes:
   - Triad shape: daemon, CLI, `signal-domain-criome`, `meta-signal-domain-criome`.
   - Naming: `domain-criome` not `criome-domain` (lexical suffix order).
   - Six concrete intelligent-signal-resolution capabilities: typed records, multi-record bundles, signed responses, signal-cloud record set direct return, subscribable resolution, trust-graph-constrained answers.
   - Working operations: `Resolve`, `Register`, `Renew`, `Transfer`, `Subscribe`, `Lookup`.
   - Policy operations: `Configure`, `Mutate` (registration policy), `Issue` (TLD signing), `Revoke`, `Inspect`.
   - Daemon storage: sema-engine with policy and working tables.
   - DNS bridge sidecar translating port-53 DNS to signal calls.
   - Anchored on spirit intents 285–290.

9. `/home/li/primary/reports/third-designer/22-cloud-criome-design-research/3-cloudflare-api-research.md` — Detailed Cloudflare API surface for the cloud component provider plane. Confirms `cloudflare-rs` (v0.14.1, 309 stars) as v1 substrate; coverage gaps handled via `reqwest`. API areas for v1: DNS records CRUD + Batch, Zones list/lookup, Rulesets at `http_request_dynamic_redirect`. Auth via env var or password-manager bridge. Batch endpoint caveat: single DB transaction but distributed KV propagation not atomic.

10. `/home/li/primary/reports/third-designer/22-cloud-criome-design-research/4-opt-in-feature-compilation-design.md` — Build-time opt-in feature pattern for stateful component daemons. Per-provider Cargo features (cloudflare, google, hetzner, ...) gating dependencies and dispatcher modules. `default = []`; published binary carries no provider. Discovery via `(Help Main)` per intent 263 — compiled operations only appear in Help. Version-handover flow for eventual self-upgrade when daemon lacks capability. Per spirit intents 283, 284.

11. `/home/li/primary/reports/third-designer/22-cloud-criome-design-research/0-orchestrator-synthesis.md` — Third-designer synthesis of the five-subagent research wave. Converges cloud and domain-criome designs on a single picture: cloud subscribes to domain-criome's `CloudProjection` records, dispatches via per-provider compile-time index, replies with typed `ProviderUnsupported` when provider isn't built in. Flags the meta-signal rename (records 290 + 299) as Minimum certainty, recommending explicit psyche affirmation before execution.

### Post-birth architecture updates

12. `/home/li/primary/reports/third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md` — Audit of the landed cloud and domain-criome repos against new intent records 311–320. Three load-bearing seams:
    - **Mutate/Query channel split (R1):** `Plan` should move to `owner-signal-cloud` because it materializes daemon state, despite typed reply being read-like. `Observe` + `Validate` remain ordinary-signal.
    - **Content-addressed domain authority (R2):** Contract needs a `DomainAuthority` concept and `NotAuthoritative` rejection pointing to the authoritative daemon.
    - **Sub-ID + Criome identity primitives (R3):** Landed contracts use string newtypes; new records require stronger identity typing.

13. `/home/li/primary/reports/third-designer/25-most-important-questions-2026-05-24/2-cloud-mutate-quorum-multi-zone.md` — Design integration of spirit records 338–340 into cloud and domain-criome:
    - Record 338: Cloud's `Plan` renamed to `Mutate`; daemon enters two-state lifecycle (**Mutate-sent** = provider request not yet acknowledged, **Mutated** = acknowledged).
    - Record 339: Component state across Criome is last-known-acknowledgment, never live-query; **quorum-of-agreement** by acknowledging changes.
    - Record 340: Domain-criome may resolve unowned domains via cached last-known records (content-addressed, timestamped, agreed); multiple domains per daemon; higher authority decides node ownership.

## Bucket 2 — open questions / sketches (2 reports)

1. `/home/li/primary/reports/third-designer/22-cloud-criome-design-research/5-meta-signal-rename-impact.md` — Survey of the workspace impact of renaming `owner-signal-*` to `meta-signal-*` for the policy contract. Scope: 8 GitHub repositories, 8 crate names, ~169 Owner-prefixed code symbols, ~95 ARCH-file lines, ~105 workspace files. Anchored on spirit intents 290 and 299, both **Minimum certainty**. Record 299 is explicit: "a tentative rename direction rather than a completed vocabulary change." Recommends Phase 0 as explicit psyche affirmation at Maximum certainty before execution. **Verdict: held for psyche decision.**

2. `/home/li/primary/reports/third-designer/23-architecture-update-2026-05-23/0-orchestrator-synthesis.md` — Architecture update synthesizing parallel design wave on 10 new intent records (311–320) plus system-specialist's freshly-landed cloud and domain-criome triads. Three load-bearing design positions requiring psyche resolution:
   - **Persona binds the stable public socket per component; uses `SCM_RIGHTS` to hand accepted FDs to the active daemon version.** (Relates to version-handover atomicity.)
   - Mutate/Query channel split decision (settled in Bucket 1 audit but flagged here as requiring full contract movement).
   - Content-addressed domain authority and identity primitives typing (partially sketched; Sub-ID primitive still under psyche framing).

## Bucket 3 — adjacent mentions to discard (17 reports)

### Pi-harness work landing in cloud-operator lane

1. `/home/li/primary/reports/cloud-operator/1-pi-operator-safety-dirty-prompt-handoff.md` — Pi operator safety handoff (not cloud-component).
2. `/home/li/primary/reports/cloud-operator/3-pi-subagents-and-chains-research-2026-05-23.md` — Pi subagent agents and chain workflows.
3. `/home/li/primary/reports/cloud-operator/4-pi-auto-compaction-update-web-access-2026-05-23.md` — Pi harness compaction settings, web-access packaging.
4. `/home/li/primary/reports/cloud-operator/5-pi-harness-chain-function-2026-05-25.md` — Pi harness chain function mechanics.
5. `/home/li/primary/reports/cloud-operator/2-pi-harness-follow-up-audit-2026-05-23/` — Pi harness audit directory.
6. `/home/li/primary/reports/cloud-operator/6-recent-intent-reports-branch-read-2026-05-26/` — Intent context audit.
7. `/home/li/primary/reports/cloud-operator/7-refresh-intent-reports-visual-audit-2026-05-26/` — Intent visual audit.

Also at `/home/li/primary/reports/cloud-operator/8-cloud-component-design-recap-2026-05-26/` — a context-maintenance recap **directory** with only a frame file (synthesis never landed). Worth noting as a prior unfinished attempt at the recap the current pass completes.

**Verdict on cloud-operator lane:** Reports 1–7 are pi-harness operations work, not cloud-component design. The lane's mechanical bootstrap (lane-bootstrap report in cloud-designer) notes this historical misalignment.

### Audits, context sweeps, generic mentions

8. `/home/li/primary/reports/designer/352-intent-log-audit-2026-05-26.md` — Intent log audit (cloud in passing context).
9. `/home/li/primary/reports/designer-assistant/101-heresy-inventory-2026-05-25.md` — Schema heresy inventory (cloud in context).
10. `/home/li/primary/reports/system-designer/29-lean-horizon-cluster-data-shape.md` — Horizon cluster data shape ("cloud-native" generic adjective).
11. `/home/li/primary/reports/system-designer/34-mvp-and-sandbox-audit/1-mvp-code-state-fresh-audit.md` — Lojix/Horizon MVP code audit.
12. `/home/li/primary/reports/second-designer/161-design-cascade-and-context-sweep/4-operator-audit-against-current-design.md` — Operator audit (cloud in context lists).
13. `/home/li/primary/reports/second-designer/161-design-cascade-and-context-sweep/5-intent-manifestation-gap-audit.md` — Intent manifestation audit.
14. `/home/li/primary/reports/second-designer/162-contract-repo-lens-and-consolidation/1-intent-vs-contract-repo-audit.md` — Contract repo audit.
15. `/home/li/primary/reports/second-designer/161-design-cascade-and-context-sweep/6-bead-splitting-sweep.md` — Bead hygiene.
16. `/home/li/primary/reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md` — NOTA schema language.
17. `/home/li/primary/reports/second-system-assistant/2-persona-speech-component-brainstorm-2026-05-17.md` — Speech component brainstorm (cloud providers generic).

Plus a few frame/synthesis files in `reports/third-designer/25-most-important-questions-2026-05-24/` that mention cloud in title/context but carry no design substance of their own, and `reports/cloud-designer/1-lane-bootstrap-2026-05-27.md` (mechanical lane registration, procedural).

## Summary

The cloud-component-design landscape is dominated by 13 settled
design decisions spanning system-operator (signal foundation +
research), second-designer (production framing), and
third-designer (parallel research triad). The two open questions
are the meta-signal rename (held for psyche affirmation) and
load-bearing architecture positions flagged in the post-birth
audit. The cloud-operator lane's pi-harness work is orthogonal
to component design and should be clearly separated in future
documentation.

The unfinished
`reports/cloud-operator/8-cloud-component-design-recap-2026-05-26/`
attempt (frame-only, no synthesis) is what the current
cloud-designer meta-report directory effectively completes.

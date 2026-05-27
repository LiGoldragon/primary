# Cloud Component Design Recap — Report-History Scout

## Files Retrieved

1. `skills/context-maintenance.md` (lines 1-268) — report-history triage method: forward / migrate / keep / drop, and guard against deleting design rationale.
2. `skills/component-triad.md` (lines 1-634) — current stateful component triad rules: runtime repo + ordinary signal + owner signal, daemon/CLI invariants, policy state, single-argument rule, runtime signal/executor/SEMA split.
3. `protocols/active-repositories.md` (lines 1-203) — active repo map; cloud/domain-criome repos are listed at lines 86-91.
4. `reports/system-operator/156-cloudflare-api-surface-research.md` (lines 1-229) — Cloudflare DNS/redirect/API/auth/rate-limit surface and early signal split.
5. `reports/system-operator/157-provider-api-scope-research.md` (lines 1-240) — Google Cloud DNS, Hetzner Cloud/DNS, provider gating, and provider-neutral cloud scope.
6. `reports/system-operator/158-signal-foundation-for-cloud-triads.md` (lines 1-491) — signal-frame/signal-sema/signal-executor foundation, no signal-core, contract skeletons, tests, owner/meta naming conflict.
7. `reports/system-operator/159-cloud-repo-scaffold-prototype.md` (lines 1-352) — pre-creation scaffold plan, component boundary, initial contract sketches, and first-test plan.
8. `reports/system-operator/160-cloud-domain-criome-birth-design.md` (lines 1-392) — current synthesis: repos created, first contract shape, runtime shape, implemented scaffold, and open questions.
9. `reports/cloud-operator/8-cloud-component-design-recap-2026-05-26/0-frame-and-method.md` (lines 1-17) — local frame for this recap directory.

The requested `reports/system-operator/*` paths exist. I did not need the renamed predecessor `reports/system-specialist/` paths; note that reports 158-160 still contain some historical `system-specialist` path references in their bodies.

## Current Design Story

The design has moved from Cloudflare repair research into a two-component triad birth:

- `cloud` is the provider API execution component. It owns provider adapters, provider inventory, validation, concrete plans, provider-specific application, provider facts, and provider failures.
- `domain-criome` is the domain meaning/registry/projection component. It owns Criome-domain knowledge, intelligent resolution, delegation/registration policy, and provider-neutral desired DNS/redirect projections.
- The intended flow is: `domain-criome` projects provider-neutral desired state; `cloud` compares that projection against Cloudflare/Google/Hetzner state, prepares a plan, and applies it only when authorized.

The current repo state is no longer hypothetical. Report 160 says all six repos were created and pushed: `cloud`, `signal-cloud`, `owner-signal-cloud`, `domain-criome`, `signal-domain-criome`, and `owner-signal-domain-criome`. The active-repository map now confirms the same six as adjacent active work: the two runtime repos are documentation-only at birth, while the four signal repos hold the initial contract surfaces.

The contract direction is now sharper than the earliest sketches:

- `signal-cloud` ordinary surface: observe accounts/zones/records/redirects/capabilities/provider state; validate desired state; plan concrete provider changes; later watch/unwatch.
- `owner-signal-cloud` owner surface: credential handles, provider accounts, zone/domain allowlists, deletion/overwrite policy, capability enablement, plan approval/application, account retirement, start/drain/reload.
- `signal-domain-criome` ordinary surface: observe domains/delegations/projections, resolve, project provider-neutral desired state, later watch/unwatch.
- `owner-signal-domain-criome` owner surface: register domains, delegate branches, retire domains, set root registry policy, start/drain/reload.

The first provider target remains Cloudflare because the concrete pressure is restoring lost DNS records and redirects. The load-bearing Cloudflare choice is: DNS Records API for DNS, Rulesets-backed Single Redirects / Bulk Redirects for new redirects, Page Rules only as legacy import/read surface unless an explicit migration operation is designed. Google Cloud DNS and Hetzner Cloud DNS belong in the early cloud vocabulary; Hetzner server/network/firewall/load-balancer mutations and Google load-balancer redirect maps are later.

The signal foundation is also settled for this design wave: use `signal-frame`, `signal-sema`, and `signal-executor`; use `sema-engine` only inside runtime daemons that need durable local state; do not add new `signal-core` dependencies. Public contracts expose domain verbs, not public `Assert` / `Mutate` / `Match` roots. Component-local commands project to Sema classifications internally.

Runtime work is intentionally not faked yet. Report 160 states `cloud` and `domain-criome` runtime repos are docs-only because a fake CLI/daemon or direct provider/file access would violate the triad discipline. The next runtime implementation should start with real ordinary and owner Unix sockets, `signal-frame` decode/reply encode, sema-engine policy/plan stores, typed unsupported/configuration replies, a Cloudflare read-only actor, and owner-approved plan application after plan generation is tested.

## Older Report Substance: Load-Bearing vs Superseded

### Still load-bearing

- `156-cloudflare-api-surface-research.md`: provider facts remain current design input: DNS endpoints, modern redirect APIs, legacy Page Rules posture, bearer-token model, rate limits, list-before-mutate reconciliation, async bulk-redirect operations, proxied-DNS redirect requirement, and no default Rust SDK.
- `157-provider-api-scope-research.md`: still carries the provider-neutral scope: `cloud` is not “Cloudflare with extras”; it should model zones, records, redirects, servers, networks, firewalls, load balancers, addresses, credentials, plans, capabilities, validation, and applied changes above any single provider.
- `158-signal-foundation-for-cloud-triads.md`: still carries the foundation constraint: `signal-frame` not `signal-core`; public domain verbs; typed unsupported-capability replies; contract purity; owner-signal naming until a coordinated rename; Nix-exposed NOTA/rkyv/constraint tests.
- `159-cloud-repo-scaffold-prototype.md`: still useful as rationale for the boundary between `cloud` and `domain-criome`, secret handles instead of secret bytes, provider-neutral domain projection, and first-test expectations.
- `160-cloud-domain-criome-birth-design.md`: current primary history report. It supersedes the pre-creation state, records created repos and scaffold details, and states the live next-step shape.

### Superseded or narrowed

- Report 159’s “none of the repos exist” state is superseded by report 160 and `protocols/active-repositories.md`.
- Report 159’s recommendation to create only the two ordinary contract repos first is superseded: all six repos were created.
- Early `Apply` placement in reports 156-158 is narrowed by report 160: ordinary `signal-cloud` should not expose live `Apply` in the first cut; owner-approved plan application is the current recommendation.
- Report 158’s illustrative `Query`/`Plan`/`Apply` skeleton is superseded in naming by the implemented/current contract story: `Observe`, `Validate`, `Plan` for ordinary cloud; apply through owner signal.
- Report 159’s illustrative NOTA examples are explicitly not final. Treat generated `nota-codec` examples and current bracket-string NOTA discipline as authoritative when implementation resumes.
- Any `meta-signal-cloud` naming remains superseded by current convention until a coordinated rename. Current repos and skills use `owner-signal-*`.

### Keep as design rationale, not active instructions

Under `skills/context-maintenance.md`, reports carrying design alternatives should not be blindly dropped after the chosen shape migrates. Reports 156-159 are not the current action plan, but they preserve why the current shape exists: Cloudflare API realities, broader provider scope, signal foundation, and scaffold-order tradeoffs.

## Open Design Questions

1. **Ordinary apply vs owner-only apply.** Current recommendation is owner-only live mutation first. Reopen only when Criome-mediated authorization or a clear ordinary-caller permission model exists.
2. **Owner-signal vs meta-signal rename.** Keep `owner-signal-*` now. A future `meta-signal-*` rename must be coordinated across skills, repo names, crate names, generated CLI route naming, sockets, docs, and existing reports.
3. **Projection scope for `domain-criome`.** Current recommendation is public provider-neutral DNS/redirect projection first; richer intelligent-resolution state can follow once the daemon shape exists.
4. **Credential ownership and rotation.** Reports agree `cloud` should receive secret handles, not secret bytes. The exact secrets component / rotation ownership remains to be specified.
5. **Provider capability discovery.** The design wants compiled/configured/authorized layers. Google can probe permissions; Hetzner likely needs safe read probes and typed error mapping. Exact contract payloads should preserve those distinctions.
6. **Cloudflare legacy import/migration.** Page Rules are readable legacy state, not the future write target. Any operation that disables/deletes/migrates them needs explicit validation and owner authority.
7. **Docs consistency hazard.** `skills/component-triad.md` line 14 still says repo triad members include `core-signal-<component>`, while the shape section and all current cloud design use `owner-signal-<component>`. Treat `owner-signal` as current truth, but this is a cleanup candidate.

## Concrete File / Report References

- Current repo status: `protocols/active-repositories.md` lines 86-91.
- Triad shape and constraints: `skills/component-triad.md` lines 21-44, 253-394, 589-634; stray `core-signal` table entry at line 14.
- Context-maintenance classification: `skills/context-maintenance.md` lines 68-128 and 225-248.
- Cloudflare API and risk facts: `reports/system-operator/156-cloudflare-api-surface-research.md` lines 23-96, 99-170, 175-229.
- Broader provider scope and gating: `reports/system-operator/157-provider-api-scope-research.md` lines 143-240.
- Signal foundation and owner/meta naming: `reports/system-operator/158-signal-foundation-for-cloud-triads.md` lines 24-56, 173-241, 274-491.
- Pre-birth scaffold rationale: `reports/system-operator/159-cloud-repo-scaffold-prototype.md` lines 55-78, 180-285, 307-352.
- Current birth synthesis and next steps: `reports/system-operator/160-cloud-domain-criome-birth-design.md` lines 19-68, 83-147, 149-295, 312-392.

## Start Here

Start with `reports/system-operator/160-cloud-domain-criome-birth-design.md`. It is the latest report-history synthesis and contains the created repo list, current component boundary, first contract shape, implemented scaffold, tracking beads, and remaining runtime decisions.

## Supervisor Coordination

No blocker or decision request arose during this read-only scout. No source/workspace files were edited; only this configured output artifact was written.

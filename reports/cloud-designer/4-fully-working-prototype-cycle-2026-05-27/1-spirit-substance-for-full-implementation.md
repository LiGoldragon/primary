# Spirit substance for cloud-component full implementation

This document extracts intent from Spirit's cloud-domain records to guide the next prototype cycle toward a fully-working cloud-component triad (daemon + signal-cloud + owner-signal-cloud). The scope is hard constraints, settled design decisions, open questions, and anti-patterns that bear directly on implementation shape.

## Hard constraints

The prototype must not violate the following:

**Cloud credentials must flow through the password-manager pattern, never appear in source or ordinary signals.** [682, 689, 924] The Cloudflare API token is fetched from gopass at the path `cloudflare/api-token` by a wrapper shim inside the Nix closure and injected as `CF_API_TOKEN` at daemon boot. This is non-negotiable: the daemon receives the credential pre-populated, not via configuration or signal. Human-driven env-var management at daemon start is explicitly forbidden [924]. Investigate safer auth alternatives during design, but the env-var-populated-by-password-manager pattern is the settled first target [689].

**Cloud component must use the old NOTA/old signal-macro stack, not the new schema-engine.** [679, 684, 914] This is a production pragmatism decision: ship the MVP faster by staying on the proven Spirit-era approach that the daemon already runs. Defer the new schema-engine refactor until the component's shape is proven. Component production push is prioritized [684]; the prototype must prove the MVP surface with existing macro machinery.

**Flarectl is the first adapter; flarectl must be wrapped and on PATH via Nix closure.** [923] When the cloud component is built with the `cloudflare` feature, flarectl is a runtime dependency of the cloud package. The cloud binaries are wrapped via `makeWrapper`/`wrapProgram` so flarectl is guaranteed on the daemon's PATH at runtime. No reliance on whatever happens to be installed in the user profile. This ensures reproducibility and hermetic deployments.

**DNS records are read-only signals from Cloudflare's state, not authoritative local state.** [681, 686] Cloud first state may be lossy provider-backed cache [681]; the daemon caches last-known-state of queried Cloudflare resources, but cache loss is acceptable because Cloudflare is the source of truth [686]. There is no persistent cloud state database; first cloud cache is runtime/volatile (in-memory) [687].

**Provider integrations must be build-time opt-ins with capability-observation distinction.** [342] When built without a provider feature, the daemon must distinguish built-but-unconfigured providers from providers not built into the daemon. Both return unsupported-capability replies, but the types differ. Unsupported providers may eventually self-upgrade before replying [284], but this is optional future work; the first prototype returns a typed unsupported-capability response.

**Cloud plan preparation belongs on the owner signal surface, not the working surface.** [325] The daemon does not prepare plans; it executes plans prepared by the owner (policy layer). The signal-cloud working contract is read + execute. The owner-signal-cloud policy contract is where plan preparation, plan validation, and plan decisions live.

**All designed components must be used fully in the prototype.** [977, 979] After implementation, the prototype must audit against the critique standard that all designed components are used fully. The prototype method is iterative: mine intent + reports + code for working solutions, implement fully-working prototype using all designed components, then audit. Audit gaps drive iterative growth of the underlying components themselves; component development is co-developed through prototype use.

## Settled design decisions

**Cloud owns cloud-provider API management. Cloudflare DNS and redirect rules are the first target.** [281, 282, 294, 296] Cloud is the home for all provider API machinery including Cloudflare, Google, and cloud hosters such as Hetzner. The first implementation targets Cloudflare DNS management [680, 685] with redirect configuration as a stretch goal [917] if the Cloudflare surface supports it cleanly. Note: flarectl's `pagerules` subcommand has no create/update/delete, only list, so redirects may defer to the next iteration or require direct HTTP API fallback.

**The prototype is a component triad: daemon + signal-cloud (working contract) + owner-signal-cloud (policy contract).** [294] This mirrors the standard component shape. The daemon is invoked through the cloud CLI binary. Signal-cloud is typed and small [683]; signal language is not a free-form string interface.

**Cloudflare credential sourcing is end-to-end wired via Nix closure and password manager.** [924] The cloud flake wraps flarectl with a gopass-backed shim that fetches the token from `cloudflare/api-token` and exports it as `CF_API_TOKEN` before exec. This realizes the FEMOS env-var-populated-by-password-manager pattern end-to-end inside the Nix closure. No human intervention required.

**First MVP targets DNS get/set operations. Redirects are stretch.** [916] First useful cloud actions are reading DNS/name records and setting new DNS/name records through Cloudflare. Redirect configuration is desired after the DNS path if the available surface supports it cleanly [917]. The flarectl survey shows DNS operations are well-supported; redirects require fallback to HTTP API or deferral.

**Flarectl is preferred over HTTP API if it proves simpler.** [688, 918] The psyche expects flarectl may be the most stable way to reach Cloudflare, while preserving the option to use the API directly if flarectl is not suitable. The prototype via flarectl proves this approach; HTTP API fallback is a known escape hatch.

**Provider integrations may be build-time opt-ins.** [283, 295] Cloud provider support should be build-selectable via Cargo features. Unsupported provider requests return a typed unsupported-capability reply. Future self-upgrade is possible when support is cheaply available [295], but this is optional; the MVP returns typed errors.

## Open questions

**Redirect configuration support is conditional on flarectl capability.** [917, 979] Cloudflare redirect configuration is desired after the DNS path IF the Cloudflare surface supports it cleanly. The flarectl survey revealed that `pagerules` subcommand is read-only (no mutation support). The prototype must decide: defer redirects to the next iteration, implement via HTTP API instead, or document this as a limitation. This decision does not block the fully-working DNS prototype; it is a scope boundary.

**Multi-account Cloudflare support is deferred.** The flarectl adapter accepts `--account-id` global flag or `CF_ACCOUNT_ID` env var. The prototype targets single-account flow; multi-account support is a future slice if cloud-operator's production case requires it.

**Capability-observation distinction between built-but-unconfigured and not-built providers.** [342] Both return unsupported-capability replies, but the types differ. The prototype's signal contract must define two error variants to allow callers to distinguish the cases. The details of the signal type shape (error enumeration) are not yet settled; implement as typed newtypes that differentiate the cases.

**Auto-upgrade mechanism for capability-missing daemons.** [284] Daemons with missing capabilities may eventually self-upgrade before replying, but this is future work and Minimum certainty. The first prototype returns unsupported-capability without attempting auto-upgrade; this can be added later if the service architecture supports it.

## Anti-patterns

**Do not embed credentials in source code, configuration files, signal logs, or ordinary signals.** [689] The prototype must never log a Cloudflare token, never embed it in a signal message, never include it in unit test fixtures. Credential handling is strictly via password-manager fetch-at-boot. This is a non-negotiable security boundary.

**Do not bypass designed components for one-off shortcuts.** [978, 979] Each prototype cycle should develop the designed components further rather than bypassing them. The audit standard [977] is that all designed components must be used fully. If a component is missing or inadequate, the solution is to develop the component, not to work around it in the prototype.

**Do not create a local persistent state database for Cloudflare resources.** [687] The prototype caches in memory only. Do not introduce a redb or durable store for "better" caching; cache loss is acceptable because Cloudflare is the source of truth. This simplifies the first iteration and avoids premature state-management complexity.

**Do not prepare plans in the daemon.** [325] Plan preparation belongs on the owner signal surface (policy layer). The daemon is read + execute. If the prototype needs to validate or refine a plan, that logic belongs in owner-signal-cloud, not the daemon.

**Do not assume HTTP API is available if flarectl is suitable.** [918] The CLI-first preference is intentional: simplicity and stability matter more than full API surface access in the first iteration. If flarectl proves insufficient, HTTP API is a known fallback; do not pre-emptively split the adapter between CLI and HTTP without evidence that CLI alone is inadequate.

---

**Records classified:** 47 intent records mined across cloud (39), deploy (9), persona (39), signal-frame (1), identity (1), version-handover (0). Filtered to substance bearing on prototype implementation shape; adjacent topics included where they constrain cloud's designed structure.


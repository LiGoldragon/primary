# Code Context

## Files Retrieved

1. `/git/github.com/LiGoldragon/cloud/AGENTS.md` (lines 5-15) - declares the `cloud` runtime leg, thin CLI, ordinary contract, owner contract, and no fake direct-provider CLI rule.
2. `/git/github.com/LiGoldragon/cloud/ARCHITECTURE.md` (lines 7-28, 30-65, 75-85) - cloud triad, provider-execution boundary, intended actor shape, current implementation slice, and schema-engine deferral.
3. `/git/github.com/LiGoldragon/cloud/README.md` (lines 5-16) - states current runtime reality: sockets, in-memory state, Cloudflare read-only DNS path, no live mutation.
4. `/git/github.com/LiGoldragon/cloud/docs/first-cloudflare-slice.md` (lines 3-23) - read-first Cloudflare slice and future redirect/live-mutation boundary.
5. `/git/github.com/LiGoldragon/cloud/Cargo.toml` (lines 14-37) - daemon/CLI binaries, Cloudflare default feature, dependencies on main branch contracts.
6. `/git/github.com/LiGoldragon/cloud/src/lib.rs` (lines 88-122, 124-210, 219-361, 386-561, 563-819) - runtime configuration, in-memory store, request dispatch, observation paths, Cloudflare read path, plan preparation/approval/apply, provider capability gates.
7. `/git/github.com/LiGoldragon/cloud/src/daemon.rs` (lines 23-43, 45-94, 96-201) - Unix socket daemon loop, ordinary/owner frame serving, shared store locking, socket binding.
8. `/git/github.com/LiGoldragon/cloud/src/client.rs` (lines 17-27, 55-99, 162-260) - thin CLI socket routing, one-argument parser, NOTA decode/encode path.
9. `/git/github.com/LiGoldragon/cloud/src/cloudflare.rs` (lines 44-62, 78-142, 145-215, 227-326) - credential source, Cloudflare HTTP API wrapper, provider client, API record mapping.
10. `/git/github.com/LiGoldragon/cloud/tests/runtime.rs` (lines 354-426, 430-510, 557-567) - tests proving Cloudflare record observation/cache, credential-missing rejection, apply rejection, and no provider access in CLI.
11. `/git/github.com/LiGoldragon/signal-cloud/AGENTS.md` (lines 5-11) - ordinary contract crate boundary: no runtime, no credentials, no owner mutation.
12. `/git/github.com/LiGoldragon/signal-cloud/ARCHITECTURE.md` (lines 3-70) - ordinary query/validation surface and owner split.
13. `/git/github.com/LiGoldragon/signal-cloud/src/lib.rs` (lines 46-77, 79-223, 230-345) - provider/capability/domain/record/plan types, ordinary operations and replies.
14. `/git/github.com/LiGoldragon/owner-signal-cloud/AGENTS.md` (lines 5-10) - owner contract boundary and no secret bytes rule.
15. `/git/github.com/LiGoldragon/owner-signal-cloud/ARCHITECTURE.md` (lines 3-61) - owner operations and policy responsibilities.
16. `/git/github.com/LiGoldragon/owner-signal-cloud/src/lib.rs` (lines 11-175) - credential handle, policy, plan preparation/approval/application, owner operations/replies.
17. `/git/github.com/LiGoldragon/domain-criome/AGENTS.md` (lines 5-14) - domain runtime triad and no provider API rule.
18. `/git/github.com/LiGoldragon/domain-criome/README.md` (lines 5-7) - current main checkout says documentation-only at birth.
19. `/git/github.com/LiGoldragon/domain-criome/ARCHITECTURE.md` (lines 7-28, 30-90, 92-100) - domain triad, meaning boundary, content-addressed authority model, runtime constraints, first implementation goals.
20. `/git/github.com/LiGoldragon/domain-criome/docs/projection-to-cloud.md` (lines 3-11) - provider-neutral projection into cloud policy/execution.
21. `/git/github.com/LiGoldragon/domain-criome/schema/domain-criome.concept.schema` (lines 3-39) - sparse v0.1 concept schema.
22. `/git/github.com/LiGoldragon/signal-domain-criome/AGENTS.md` (lines 5-10) - ordinary domain contract boundary and no provider fields.
23. `/git/github.com/LiGoldragon/signal-domain-criome/ARCHITECTURE.md` (lines 3-39) - ordinary domain resolution/projection contract.
24. `/git/github.com/LiGoldragon/signal-domain-criome/src/lib.rs` (lines 37-85, 87-157, 159-228) - current-main ordinary domain contract, without branch-only authority replies.
25. `/git/github.com/LiGoldragon/owner-signal-domain-criome/AGENTS.md` (lines 5-10) - owner domain contract boundary and provider mutation exclusion.
26. `/git/github.com/LiGoldragon/owner-signal-domain-criome/ARCHITECTURE.md` (lines 3-42) - owner domain registry/policy operations.
27. `/git/github.com/LiGoldragon/owner-signal-domain-criome/src/lib.rs` (lines 9-124) - current-main owner domain contract, without branch-only authority registration.
28. `/git/github.com/LiGoldragon/cloud/schema/cloud.concept.schema` (lines 3-38), `/git/github.com/LiGoldragon/signal-cloud/schema/signal-cloud.concept.schema` (lines 3-33), `/git/github.com/LiGoldragon/owner-signal-cloud/schema/owner-signal-cloud.concept.schema` (lines 3-33), `/git/github.com/LiGoldragon/signal-domain-criome/schema/signal-domain-criome.concept.schema` (lines 3-30), `/git/github.com/LiGoldragon/owner-signal-domain-criome/schema/owner-signal-domain-criome.concept.schema` (lines 3-32) - all are sparse concept schemas, not the rich Rust contracts.
29. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:README.md` (lines 5-12) - branch-only runtime README with real daemon slice.
30. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:ARCHITECTURE.md` (lines 18-62) - branch-only current implementation slice for domain runtime.
31. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:Cargo.toml` (lines 14-29) - branch-only binaries and dependencies on branch contracts.
32. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:src/lib.rs` (lines 81-195, 196-344, 365-443, 495-540, 550-586) - branch-only runtime store, resolution/projection, owner operations, authority registration, policy checks.
33. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:src/daemon.rs` (lines 23-42, 45-95, 97-141) - branch-only Unix socket daemon.
34. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:src/client.rs` (lines 17-27, 55-102, 165-188) - branch-only thin CLI.
35. `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime:tests/store.rs` (lines 67-136, 161-236, 314-347) - branch-only tests for projection, resolution, authority redirect, typed rejections, disabled projections.
36. `/git/github.com/LiGoldragon/signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` (lines 37-43, 100-115, 204-231) - branch-only `AuthorityEndpoint`, `NoRecords`, `NotAuthoritative` reply additions.
37. `/git/github.com/LiGoldragon/owner-signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` (lines 9-42, 96-129) - branch-only `AuthorityRegistration`, `AuthorityRegistered`, `RegisterAuthority` operation.

## Key Code

### Repo state/status

All six target repositories exist under `/git/github.com/LiGoldragon`. No same-name symlinks are present under `/home/li/primary/repos` for `cloud`, `signal-cloud`, `owner-signal-cloud`, `domain-criome`, `signal-domain-criome`, or `owner-signal-domain-criome`.

Status/log inspection used `jj --ignore-working-copy` so the working copies were not snapshotted or updated. All six reported “The working copy has no changes.” Current bookmarks:

| repo | current main state | notable branch state |
|---|---|---|
| `cloud` | `main` and `cloud-domain-criome-runtime` both point at `f09a7ddd` (`cloud: implement Cloudflare DNS read path`) | `docs-emit-schema-rename` exists separately |
| `signal-cloud` | `main` and `cloud-domain-criome-runtime` both point at `eb93c663` (`signal-cloud: add Cloudflare DNS record kinds`) | `docs-emit-schema-rename` exists separately |
| `owner-signal-cloud` | `main` and `cloud-domain-criome-runtime` both point at `7d7dbee4` (`owner-signal-cloud: land runtime contract on main`) | no docs branch seen |
| `domain-criome` | `main` points at `166ef5bb` (`schema: add v0.1 concept schema`); current checkout is docs/schema only | `cloud-domain-criome-runtime` points at `59ff764f` (`domain-criome: drop reply operation echoes`) and contains real runtime code |
| `signal-domain-criome` | `main` points at `51a16b4d` (`schema: add v0.1 concept schema`) and contains the base contract | `cloud-domain-criome-runtime` points at `200e1e59` (`signal-domain-criome: drop rejection operation echo`) with authority/no-record additions |
| `owner-signal-domain-criome` | `main` points at `264406fe` (`schema: add v0.1 concept schema`) and contains the base owner contract | `cloud-domain-criome-runtime` points at `98c674f2` (`owner-signal-domain-criome: drop rejection operation echo`) with authority registration additions |

No `INTENT.md` exists in any of the six repo roots.

### Cloud triad real code

`cloud` is the most live triad. Its AGENTS and architecture files define the triad as `cloud` runtime, `signal-cloud` ordinary contract, and `owner-signal-cloud` owner contract, with the CLI bundled in the runtime rather than a triad leg (`cloud/AGENTS.md` lines 5-15; `cloud/ARCHITECTURE.md` lines 7-15).

`signal-cloud` is a real Rust contract crate, not only design. It defines provider variants (`Cloudflare`, `GoogleCloud`, `Hetzner`), capabilities, DNS/redirect record types, desired state, plans, observations, validation reports, typed unsupported/rejection replies, and a `signal_channel!` with only `Observe` and `Validate` operations (`signal-cloud/src/lib.rs` lines 46-77, 79-223, 230-345). Its architecture explicitly keeps plan preparation/application on the owner side and public read/validation on the ordinary contract (`signal-cloud/ARCHITECTURE.md` lines 13-45).

`owner-signal-cloud` is also a real Rust contract crate. It reuses public provider/domain/plan types from `signal-cloud`, adds `CredentialHandle`, account registration/rotation, zone and capability policy, plan preparation, approval, application, retirement, typed owner rejections, and an owner `signal_channel!` with seven operations (`owner-signal-cloud/src/lib.rs` lines 11-175). It is explicit that secret bytes do not cross the contract (`owner-signal-cloud/AGENTS.md` lines 5-10).

`cloud` runtime code is on main. `Cargo.toml` ships both `cloud-daemon` and `cloud`, defaults the `cloudflare` feature on, and depends on `signal-cloud` and `owner-signal-cloud` from main (`cloud/Cargo.toml` lines 14-37). The runtime `Store` is in-memory and owns accounts, policy, plans, approved plans, last-known zones/records, and a Cloudflare provider client (`cloud/src/lib.rs` lines 98-122, 124-181). Ordinary and owner Signal requests are decoded to in-memory store methods (`cloud/src/lib.rs` lines 184-217, 647-657).

The real Cloudflare slice is read-only DNS observation. The store checks provider configuration, resolves account/zone policy, calls `ProviderClient::zones` and `ProviderClient::records`, and caches last-known records (`cloud/src/lib.rs` lines 282-361, 386-561). The provider client resolves credential handles through a `CredentialSource`; production uses environment variables, and the HTTP adapter calls Cloudflare `/zones` and `/zones/{id}/dns_records` through `ureq` (`cloud/src/cloudflare.rs` lines 44-62, 78-142, 145-215). Tests confirm successful record observation/caching and credential-missing typed rejection (`cloud/tests/runtime.rs` lines 354-426).

The CLI is a real thin client. It routes operation heads to working or owner sockets with `signal_cli!`, connects only over Unix sockets, performs signal-frame handshakes, decodes one NOTA request from the single argument or file, and encodes the reply (`cloud/src/client.rs` lines 17-27, 55-99, 162-260). Tests assert the CLI does not contain provider access or credential-handle strings (`cloud/tests/runtime.rs` lines 557-567).

Live mutation is deliberately not real yet. Plan preparation writes a local plan; approval records a plan identifier; apply returns `owner_signal_cloud::RejectionReason::CapabilityUnauthorized` after the plan is known and approved (`cloud/src/lib.rs` lines 601-630, 706-740). Tests assert that approved apply is rejected this way (`cloud/tests/runtime.rs` lines 430-510).

### Domain triad real code vs design-only

`domain-criome` main/current checkout is still docs/schema only. Its README says runtime binaries should land only with a real daemon request path (`domain-criome/README.md` lines 5-7). Current main has no `Cargo.toml` and no `src/` in the checkout.

The domain design is clear. `domain-criome` owns domain meaning: registered domains, branch delegations, intelligent resolution, provider-neutral public record projection, and provider-neutral redirect projection (`domain-criome/ARCHITECTURE.md` lines 16-28). `cloud` owns provider execution and domain must not call Cloudflare/Google/Hetzner directly (`domain-criome/AGENTS.md` lines 13-14; `domain-criome/ARCHITECTURE.md` lines 26-28, 84-90). Projection to cloud must remain provider-neutral and leave provider selection to cloud policy (`domain-criome/docs/projection-to-cloud.md` lines 3-11).

Current main `signal-domain-criome` and `owner-signal-domain-criome` are real contract crates, but they are the base contract shape. The ordinary main contract defines domain names, resolution scopes, projection scopes, records/redirects, `Observe`, `Resolve`, `Project`, and only `Observed`, `Resolved`, `Projected`, `RequestRejected` replies (`signal-domain-criome/src/lib.rs` lines 37-85, 87-157, 159-228). The owner main contract defines domain registration, delegation, retirement, projection policy, and four owner operations (`owner-signal-domain-criome/src/lib.rs` lines 9-124).

The current domain architecture describes content-addressed per-domain authority and says non-owned delegated resolution should return `NotAuthoritative(Delegation { name, authority_endpoint })`, not `DomainUnknown` (`domain-criome/ARCHITECTURE.md` lines 30-47). That behavior is not present on current main contracts. It exists only on the `cloud-domain-criome-runtime` branches: ordinary branch adds `AuthorityEndpoint`, `NoRecords`, `AuthorityDelegation`, `NotAuthoritative` (`signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 37-43, 100-115, 204-231); owner branch adds `AuthorityRegistration`, `AuthorityRegistered`, `AuthorityAlreadyRegistered`, and `RegisterAuthority` (`owner-signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 9-42, 96-129).

`domain-criome@cloud-domain-criome-runtime` contains a real runtime slice, but it is not on current main. It ships daemon/CLI binaries and depends on the branch versions of `signal-domain-criome` and `owner-signal-domain-criome` (`domain-criome@cloud-domain-criome-runtime:Cargo.toml` lines 14-29). Its README says it has Unix sockets, signal-frame handling, in-memory registry/delegation/policy, public-record projection, and typed rejections (`domain-criome@cloud-domain-criome-runtime:README.md` lines 5-12).

The branch runtime store implements domains, branch delegations, authorities, and policy in memory (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 172-195). Ordinary requests observe domains/delegations/projection, resolve names, and project public records (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 196-344). Owner requests register domains, delegate names, register authorities, retire domains, and set projection policy (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 365-443). Resolution prefers an exact branch delegation, returns typed `NoRecords` for registered names without address records, and returns `NotAuthoritative` for authority-covered descendants (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 286-305, 503-520). Redirect projection currently returns `ProjectionUnavailable` (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 314-344). Tests cover public-record projection, resolution, authority redirects, unknown-domain rejection, redirect projection rejection, and projection policy disablement (`domain-criome@cloud-domain-criome-runtime:tests/store.rs` lines 67-136, 161-236, 314-347).

### Concept schemas

The `schema/*.concept.schema` files are not the live rich contracts. They are sparse v0.1 concept schemas with mostly `Text` placeholders and `Status Concept` markers: cloud concept schema lines 3-38, signal-cloud lines 3-33, owner-signal-cloud lines 3-33, domain-criome lines 3-39, signal-domain lines 3-30, owner-signal-domain lines 3-32. The architecture files explicitly say schema-engine cutover is pending/deferred and the current implementation stays on hand-written Rust plus `signal_channel!` until the schema engine is ready (`cloud/ARCHITECTURE.md` lines 75-85; `domain-criome/ARCHITECTURE.md` lines 92-100).

## Architecture

### Component-triad shape

There are two triads:

| component | runtime daemon + bundled CLI | ordinary working signal | owner policy signal | current reality |
|---|---|---|---|---|
| cloud | `cloud` repo: `cloud-daemon` + `cloud` | `signal-cloud` | `owner-signal-cloud` | all three have real Rust code on main |
| domain-criome | `domain-criome` repo: intended `domain-criome-daemon` + `domain-criome` | `signal-domain-criome` | `owner-signal-domain-criome` | signal crates have real code on main; runtime main is docs/schema only; runtime branch has code |

The CLI is consistently documented as bundled runtime machinery, not a separate triad leg (`cloud/ARCHITECTURE.md` lines 13-14; `domain-criome/ARCHITECTURE.md` lines 13-14).

### Responsibility split

Cloud owns provider execution: provider account/zone/record/redirect observation, provider-neutral desired-state validation, provider-specific plans through owner authority, owner-approved apply, rate-limit/remote-operation concerns (`cloud/ARCHITECTURE.md` lines 18-24). Domain-criome owns meaning: registered Criome domains, delegations, resolution, provider-neutral DNS/redirect projection (`domain-criome/ARCHITECTURE.md` lines 18-24). Domain projection describes what should be true; cloud policy chooses the configured provider account and applies it (`domain-criome/docs/projection-to-cloud.md` lines 3-11).

The cloud ordinary/owner split is concrete: ordinary exposes `Observe`/`Validate`; owner exposes account registration, credential rotation, policy, plan preparation, approval, application, retirement (`signal-cloud/src/lib.rs` lines 325-345; `owner-signal-cloud/src/lib.rs` lines 146-175). The ordinary surface can read reflected external state; mutations of daemon-internal plan state or provider accounts require owner authority (`signal-cloud/ARCHITECTURE.md` lines 28-45; `owner-signal-cloud/ARCHITECTURE.md` lines 29-40).

The domain ordinary/owner split is also concrete on main, but authority redirection is branch-only. Main ordinary exposes `Observe`, `Resolve`, `Project`; main owner exposes `RegisterDomain`, `Delegate`, `RetireDomain`, `SetPolicy` (`signal-domain-criome/src/lib.rs` lines 207-228; `owner-signal-domain-criome/src/lib.rs` lines 101-124). Branch ordinary/owner add authority redirection and registration (`signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 204-231; `owner-signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 113-129).

### Data flow

Cloud runtime data flow:

1. `cloud` CLI receives exactly one NOTA string or path, rejects flags/extra args, decodes the operation, routes by operation head to working or owner socket (`cloud/src/client.rs` lines 162-190).
2. The CLI handshakes and sends a signal-frame request over a Unix socket (`cloud/src/client.rs` lines 55-99, 101-129).
3. `cloud-daemon` binds ordinary and owner Unix sockets, receives frames, and delegates to `Store` (`cloud/src/daemon.rs` lines 23-43, 45-94, 122-180).
4. Owner operations mutate in-memory accounts/policy/plans/approvals (`cloud/src/lib.rs` lines 647-752).
5. Ordinary observations read capabilities, zones, records, redirects, or plans (`cloud/src/lib.rs` lines 219-361, 633-645).
6. Cloudflare DNS reads resolve an owner credential handle to an environment token, list zones, find the zone identifier, list records, map Cloudflare records to `signal-cloud` records, and cache last-known state (`cloud/src/lib.rs` lines 386-561; `cloud/src/cloudflare.rs` lines 44-62, 129-215, 272-326).

Domain branch runtime data flow:

1. Owner operations populate in-memory domains, branch delegations, authority registrations, and projection policy (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 365-493).
2. Ordinary `Resolve` first checks local delegations, then authority registration coverage, then local registered-domain existence, otherwise typed `DomainUnknown` (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 286-305, 503-520).
3. Ordinary `Project` produces provider-neutral public DNS records from branch delegations when projection is enabled; redirect scopes are rejected as `ProjectionUnavailable` (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 314-344, 522-540).
4. The branch daemon and CLI are structurally parallel to cloud but use `Arc<Store>` rather than a global outer `Mutex<Store>` (`domain-criome@cloud-domain-criome-runtime:src/daemon.rs` lines 23-42, 45-95, 97-141; `domain-criome@cloud-domain-criome-runtime:src/client.rs` lines 17-27, 55-102, 165-188).

## Risks and gaps

1. **Cloud provider calls can block both daemon listeners.** Architecture says provider calls must not block ordinary listener, owner listener, or plan store (`cloud/ARCHITECTURE.md` lines 40-41). Current daemon wraps the whole `Store` in `Arc<Mutex<Store>>` and holds that outer lock while handling ordinary and owner requests (`cloud/src/daemon.rs` lines 23-38, 136-139, 165-168). `Store::observe_cloudflare_records` can make HTTP calls through `cloudflare.records` while inside that request (`cloud/src/lib.rs` lines 407-452). This is production-shaped functionally, but not actor-shaped operationally.

2. **Cloud redirect observation currently returns an empty listing after provider configuration.** Architecture/docs say redirect observation is a future slice (`cloud/ARCHITECTURE.md` lines 62-65; `cloud/docs/first-cloudflare-slice.md` lines 18-23). Code treats Cloudflare redirect rules as a supported capability and, once provider is configured, returns `Observed(Redirects { rules: vec![] })` instead of a typed not-built/unavailable reply (`cloud/src/lib.rs` lines 226-248, 799-804). That can falsely imply “no redirects exist.”

3. **Cloud capability policy is mostly stored, not enforced.** Owner `Policy` has capability directives (`owner-signal-cloud/src/lib.rs` lines 52-71), but runtime capability state only reports `Configured` if any account exists and does not inspect capability policy (`cloud/src/lib.rs` lines 765-773). Plan preparation checks only provider built/configured and then creates a plan; it does not verify zone allowlist or capability directives (`cloud/src/lib.rs` lines 601-630). Apply is rejected unconditionally after approval (`cloud/src/lib.rs` lines 721-740).

4. **Cloud planning is a stub.** Plans are deterministic `zone-provider-plan` identifiers, all desired records/redirects become create lists, update/delete lists stay empty, and no remote diff is performed (`cloud/src/lib.rs` lines 618-628). This is fine for a first slice but not sufficient for safe provider mutation.

5. **Cloud persistence is in-memory only.** `Store::open` ignores its path and returns a new store (`cloud/src/lib.rs` lines 180-182). Architecture defers sema-engine because of deprecated `signal-core` dependency (`cloud/ARCHITECTURE.md` lines 58-60). Runtime restarts lose accounts, policy, plans, approvals, and last-known reads.

6. **Domain runtime is not on main.** Current `domain-criome` main checkout is docs/schema only (`domain-criome/README.md` lines 5-7). Real domain runtime code exists only on `cloud-domain-criome-runtime`, and that branch depends on branch versions of both domain signal contracts (`domain-criome@cloud-domain-criome-runtime:Cargo.toml` lines 23-28). Integrating domain runtime requires an explicit branch promotion/rebase decision.

7. **Domain main contracts lag the architecture’s authority model.** Main `signal-domain-criome` has no `NoRecords` or `NotAuthoritative` reply and main owner contract has no `RegisterAuthority` (`signal-domain-criome/src/lib.rs` lines 201-218; `owner-signal-domain-criome/src/lib.rs` lines 95-114), but current `domain-criome/ARCHITECTURE.md` requires `NotAuthoritative` for delegated non-owned resolution (`domain-criome/ARCHITECTURE.md` lines 40-43). Those types are branch-only (`signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 100-115, 224-231; `owner-signal-domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 38-42, 113-129).

8. **Domain branch runtime is also in-memory and partial.** Branch `Store::open` ignores path and returns a new in-memory store (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 180-195). Redirect projection is explicitly unavailable (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 328-332). No daemon-to-daemon projection push to `cloud` exists yet; branch architecture says that remains a later slice (`domain-criome@cloud-domain-criome-runtime:ARCHITECTURE.md` lines 56-62).

9. **Domain branch resolution only returns address records for IP-valued delegations.** A non-IP delegation is projected as `CanonicalName` (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 121-132), but resolution only returns an address if the target parses as an IP and otherwise returns `NoRecords` for that exact delegation (`domain-criome@cloud-domain-criome-runtime:src/lib.rs` lines 134-140, 286-295). CNAME-chain resolution is not real yet.

10. **Concept schemas are placeholders.** The live contracts are hand-written Rust. The concept schemas are sparse text placeholders and can mislead an implementer if treated as canonical (`schema/*.concept.schema` refs above). Architecture says schema-engine migration is pending/deferred.

11. **`/home/li/primary/repos` does not expose these six repos.** Agents/scripts that use the primary symlink index will not find these components there; use `/git/github.com/LiGoldragon/...` paths directly unless symlinks are added later.

12. **Rust discipline cleanup may be needed before new production edits.** The inspected production Rust includes some free helper functions such as `fresh_exchange`/`encode_reply` in `cloud/src/client.rs` lines 248-260 and `handshake_reply_for` in `cloud/src/frame_io.rs` lines 73-80. That predates this read-only scout, but future edits may need to reconcile with current workspace Rust method discipline.

## Start Here

For live cloud work, start with `/git/github.com/LiGoldragon/cloud/src/lib.rs` (lines 112-210 and 219-819). It is the real runtime state machine and shows exactly what is implemented versus stubbed.

For domain work, start by deciding whether `/git/github.com/LiGoldragon/domain-criome@cloud-domain-criome-runtime` is the intended integration source. If yes, open `domain-criome@cloud-domain-criome-runtime:src/lib.rs` (lines 172-344 and 365-443) together with the two branch signal contracts. Current main is not the runtime implementation.

## Supervisor coordination

No supervisor decision was requested during this read-only scout. Main open decision for the parent/operator: whether to promote or rebase the `cloud-domain-criome-runtime` domain branches, and whether Cloudflare redirect observation should return typed unavailable rather than an empty listing until real Rulesets API support exists.

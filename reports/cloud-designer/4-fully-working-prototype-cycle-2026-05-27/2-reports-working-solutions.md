# Fully-Working Prototype: Concrete Design Substance

This report extracts the four concrete design buckets for the fully-working cloud-component prototype from 13 source reports. It specifies what the prototype must DO (positive), must NOT do (anti-spec), and what leaves as TODO with typed-rejection.

## Operation Routing

### What Exists

**signal-cloud** ordinary operations (peer-callable):
- `Observe(Observation)` — read provider state: zones, records, redirects, capabilities
- `Validate(DesiredState)` — dry-run constraint checking without mutation
- No `Plan` on ordinary; no `Apply`; `Observe(Plan(...))` reads stored plans only

**owner-signal-cloud** owner operations (authority-only):
- `RegisterAccount` — bind provider credentials by handle
- `RotateCredential` — credential rotation
- `SetPolicy` — zone/capability policy
- `PreparePlan(PlanPreparation)` — generate plan by diffing desired-vs-current (moved from ordinary per intent 311)
- `ApprovePlan(PlanIdentifier)` — ratify plan
- `ApplyPlan(Application)` — execute against provider (returns `CapabilityUnauthorized` stub on current runtime branch)
- `RetireAccount` — lifecycle

Each operation carries a provider-discriminating variant: `Cloudflare`, `GoogleCloud`, `Hetzner` (closed enum). Capabilities are typed variants: `DnsRecords`, `RedirectRules`, `CloudHosts`, etc.

### Responses and Rejection

All operations reply with:
- Success replies matching verb-past-tense discipline: `Observed`, `Validated`, `PlanPrepared`, `Approved`, `Applied`
- Typed rejections per operation
- `RequestUnsupported` when provider not compiled in
- `ProviderRateLimited` on rate-limit discovery

Per intent 342, capability state reports three layers: `Compiled` / `Configured` / `Authorized` plus `Unsupported` / `Unauthorized`.

### The Prototype Must DO

1. Route operations to the correct socket (ordinary vs owner) per `signal-frame::signal_cli!`
2. Decode NOTA request frame; encode reply frame via `signal-frame` length-prefixed rkyv
3. Lower each operation into a daemon-internal command (e.g., `Observe(Records)` → `ListDnsRecords` command)
4. Return `RequestUnsupported` when provider is not compiled in (build-time cfg feature)
5. For `Observe` queries: call CloudflareProvider actor; return fresh records
6. For `PreparePlan`: diff desired state against cached/live provider state; mint PlanIdentifier; store Plan; return `PlanPrepared`
7. Refuse `ApplyPlan` with `CapabilityUnauthorized` until mutation path lands

### The Prototype Must NOT Do

1. Mix provider-specific details into the wire contract (no `CloudflareCredential` type on the wire; use `CredentialHandle` string newtype)
2. Expose any Sema verbs (`Assert`, `Mutate`, `Match`, `Validate` classes) as public operation roots
3. Carry secret material (tokens, passwords) in operations or replies
4. Expose `Plan` on ordinary signal-cloud; it belongs owner-only because plan generation mutates the plan store
5. Return a generic `RequestUnimplemented` for missing provider; return the typed `RequestUnsupported { provider, available, advise }`

Per reports: `/home/li/primary/reports/system-operator/160-cloud-domain-criome-birth-design.md` §"First contract shape"; `/home/li/primary/reports/second-designer/196-cloud-component-production-design-2026-05-25.md` §"§3 The MVP scope"; `/home/li/primary/reports/third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md` §"2 Apply R1".

---

## State Machine

### Plan / Mutation Lifecycle

The current runtime branch implements a three-step ceremony:

```
PreparePlan → ApprovePlan → ApplyPlan
```

This is slated for evolution per intent 338 into a **two-state acknowledgment**:

```
Mutate-sent (request issued, not acknowledged)
    ↓
Mutated (provider confirmed)
    ↓ [failure path]
MutateRejected (provider 4xx) OR MutateTimedOut (provider silent)
```

### Current Daemon-Side Behavior

The runtime branch's `Store` holds:
- `Mutex<Vec<AccountBinding>>` — provider credentials by handle
- `Mutex<Policy>` — zone/capability policy
- `Mutex<Vec<Plan>>` — prepared plans
- `Mutex<Vec<PlanIdentifier>>` — approved plans (parallel vector)

On `PreparePlan`:
1. Diff desired state against cached provider state
2. Generate Plan record
3. Store in plans vec
4. Return `PlanPrepared` with minted `PlanIdentifier`

On `ApprovePlan`:
1. Look up plan by ID
2. Move plan ID to approved list
3. Return `PlanApproved`

On `ApplyPlan`:
1. Look up plan by ID in approved list
2. **[TODO: call CloudflareProvider actor; transition to Mutated on 2xx]**
3. Currently returns `CapabilityUnauthorized` stub

### Retry Policy and Timeouts

Per intent 338 + report `/home/li/primary/reports/third-designer/25-most-important-questions-2026-05-24/2-cloud-mutate-quorum-multi-zone.md` §3:

- Plan store records persist across daemon restart
- On restart, daemon reads all `MutateSent` rows
- For each, ask provider for current state (reconcile)
- Transition to `Mutated` if provider applied, `MutateRejected` if provider refused
- Add explicit `Retry(MutationIdentifier)` verb for timeout recovery
- Timeout state is distinct from rejection: `MutateTimedOut` ≠ `MutateRejected` (provider may have applied but network ate reply)

### Last-Known Acknowledgment

Per intent 339, the daemon's stored state is **last-known-acknowledgment**, not live-queried truth:
- Cloudflare is the external source of truth
- Daemon cache is "last reply from Cloudflare"
- External provider's 2xx HTTP is interpreted as acknowledgment
- The daemon does NOT re-query Cloudflare on every operation; it uses cached state + periodic reconciliation

### The Prototype Must DO

1. Store prepared plans durably (Mutex vec is acceptable for MVP; sema-engine redb later)
2. Store approved plan IDs in a parallel structure
3. Persist mutation acknowledgment records (MutateSent / Mutated state) in the same store
4. On daemon restart, re-reconcile MutateSent rows with provider state
5. Map HTTP response codes: 2xx → Mutated, 4xx → MutateRejected, 5xx/timeout → MutateTimedOut
6. Refuse mutation with `CapabilityUnauthorized` until real provider integration lands

### The Prototype Must NOT Do

1. Use live-query semantics (daemon queries Cloudflare every request)
2. Depend on external atomic batch semantics (Cloudflare batch API is not externally atomic; treat as convenience)
3. Implement per-provider retry loops inside the daemon; leave retry to the owner's explicit `Retry` verb
4. Lose plan records on restart (persistence, even in-memory during MVP, is non-optional)

Per reports: `/home/li/primary/reports/third-designer/25-most-important-questions-2026-05-24/2-cloud-mutate-quorum-multi-zone.md` §3-4; `/home/li/primary/reports/second-designer/196-cloud-component-production-design-2026-05-25.md` §"§6 Cache shape".

---

## Actor Topology

### Current Daemon Actors (Runtime Branch)

The daemon lives in a single Rust binary (`cloud-daemon`) with a `Store` as the central coordination point. Per intent 666, the Mutex shape is valid for MVP:

- **Store** — `Mutex`-guarded state: policy, plans, approved-plans, cache
- **CloudflareProvider** — [TODO: kameo actor with reqwest HTTP client]
- **Ordinary socket listener** — Unix socket, accepts signal-frame requests
- **Owner socket listener** — Unix socket, accepts signal-frame requests
- **Request dispatcher** — matches operation kind; routes ordinary vs owner; calls handler functions

### Architecture Per Design Reports

`/git/github.com/LiGoldragon/cloud/ARCHITECTURE.md` names a future shape:
- `CloudflareProvider` — kameo actor, owns reqwest, handles Cloudflare HTTP + rate limits
- `PlanStore` — `Mutex<Vec<Plan>>` (or redb once persistence lands)
- `PolicyStore` — `Mutex<Policy>` + `Mutex<Vec<AccountBinding>>`
- `RateLimitGate` — per-provider rate-limit state (can be a field inside CloudflareProvider)
- `RemoteOperationTracker` — [YAGNI for DNS, which has no async operations; deferred]

### Integration Flow (per intent 196 §7 + 22/0)

```
cloud CLI → cloud daemon:
  ├─ Ordinary socket: Observe, Validate
  ├─ Owner socket: RegisterAccount, PreparePlan, ApprovePlan, ApplyPlan
  ├─ [TODO] Store dispatches to CloudflareProvider actor
  ├─ [TODO] CloudflareProvider calls Cloudflare HTTP API (with token from LoadCredential)
  └─ Daemon returns typed reply over the same socket
```

The daemon does NOT directly call providers; it delegates to CloudflareProvider. CloudflareProvider does NOT block the request listener (async dispatch).

### The Prototype Must DO

1. Implement a `CloudflareProvider` actor or async-dispatcher that owns the Cloudflare HTTP client
2. Load Cloudflare API token from `$CREDENTIALS_DIRECTORY/cloudflare_token` (systemd LoadCredential) on daemon startup
3. Implement `list_zones()`, `list_dns_records(zone_id)`, `list_redirect_rules(zone_id)` as cache-filling queries
4. For `ApplyPlan` [TODO], call provider's create/update/delete methods
5. Map Cloudflare rate-limit headers to `ProviderRateLimited` rejection; surface to caller
6. Keep Store and HTTP calls decoupled (Store mutations don't block HTTP)

### The Prototype Must NOT Do

1. Block the request listener on provider HTTP calls
2. Use synchronous HTTP blocking; use async with tokio timeouts
3. Shell out to `flarectl` or `cf` CLI (use `cloudflare` Rust crate directly)
4. Hard-code Cloudflare endpoints; use the crate's typed endpoint definitions
5. Attempt to reconcile divergent writes across nodes (per intent 339, record divergence and last-known-ack; not a daemon responsibility)

Per reports: `/home/li/primary/reports/second-designer/196-cloud-component-production-design-2026-05-25.md` §7 "Actor topology"; `/home/li/primary/reports/system-operator/156-cloudflare-api-surface-research.md` §4 "Rate limits, idempotency, and list-before-mutate".

---

## Integration Seams

### Mutate / Query Channel Split (Intent 311 + 325)

Per report `/home/li/primary/reports/third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md` §"2 Apply R1":

**signal-cloud (ordinary):** Query-only.
- `Observe` (read provider state)
- `Validate` (dry-run, no daemon mutation)

**owner-signal-cloud (owner):** Mutate-class verbs.
- `PreparePlan` (generates and stores daemon state)
- `ApprovePlan` (mutates approval state)
- `ApplyPlan` (mutates provider)

**The split is enforced at the socket level:** the daemon routes Mutate-class operations (those that write daemon state or call external providers) to the owner socket.

### DomainAuthority + NotAuthoritative (Intent 312 + R2)

Per report `/home/li/primary/reports/third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md` §"3 Apply R2":

**signal-domain-criome** now includes:
- `Reply::NotAuthoritative(AuthorityDelegation)` when a domain is delegated to another daemon
- `Delegation` carries `authoritative_endpoint` so callers can follow the redirect

**The prototype must NOT:**
1. Pretend to be authoritative for domains it doesn't own
2. Return a flat listing from `Observe(Domains)`; only list locally-authoritative names

### Sub-ID + Criome Identity (Intent 317 + 318, deferred)

Per report `/home/li/primary/reports/third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md` §"4 Sub-ID + Criome identity":

Currently landed contracts use string newtypes (`DomainName`, `ProviderAccount`). When records 317-318 land with concrete `Principal` / `CriomeIdentity` types:
- `ProviderAccount` stays opaque; add `principal_ordering_account: Option<Principal>` on registration
- `PlanIdentifier`: add `approving_principal` on approval, `applying_principal` on apply
- Owner contracts gain `PrincipalUnauthorized` rejection

**The prototype should:**
1. Use string newtypes today (no Criome identity yet)
2. Structure the code to accept Principal fields additively once they arrive

### ProxyMode Plumbing + Record Deletion Gap

Per report `/home/li/primary/reports/system-operator/156-cloudflare-api-surface-research.md` §1:

Cloudflare's Single Redirects require proxied DNS records. The daemon must NOT attempt redirect rules on DNS-only records.

**The prototype must:**
1. Add a `proxied: bool` field to DNS record payloads (may come from Cloudflare's API or be set by policy)
2. Reject redirect-rule creation with a typed rejection if the target record is not proxied
3. When deleting a record, re-read it first to verify it's still the one the daemon thinks it owns (list-before-delete pattern)

### Record-Identifier-for-Delete

Per report `/home/li/primary/reports/system-operator/156-cloudflare-api-surface-research.md` §1:

TXT, MX, and other record types can have multiple records with the same name. The daemon cannot identify records by `(name, type)` pair alone.

**The prototype must:**
1. Store Cloudflare's record ID (minted by Cloudflare API)
2. Use managed-state markers (comments or tags) to identify which records this daemon owns
3. When deleting, use the Cloudflare record ID as the primary key

### The Prototype Must DO (Integration)

1. Accept Mutate operations on owner socket; Query operations on ordinary
2. Refuse `PreparePlan` on ordinary (move operation to owner)
3. Return `NotAuthoritative` if domain-criome ever needs to delegate (set up reply path; don't populate yet)
4. Persist record IDs + ownership markers (comments) when storing records
5. Check `proxied` status before creating redirect rules
6. List-before-delete: re-read record before deletion to verify ownership

### The Prototype Must NOT Do

1. Accept mutation requests on the ordinary socket
2. Attempt to create redirects on DNS-only records
3. Delete a record without re-reading it first
4. Use only `(name, type)` pair to identify records; require Cloudflare record ID
5. Implement Criome identity until records 317-318 land with concrete types
6. Assume external-provider operations are atomic or idempotent without reconciliation

### The Prototype Should Leave as TODO (Typed Rejection)

1. Cache freshness notification in wire contract (add `fetched_at` field only if caller demand appears)
2. Provider-side cache TTL tuning (60s MVP guess; revisit on usage data)
3. Subscriptions (`Watch` / `Subscribe`) for provider-state changes (deferred to Phase B per report 25/2)
4. Atomic DNS batch across multiple records (treat Cloudflare batch as convenience, not transaction)

Per reports: `/home/li/primary/reports/second-designer/196-cloud-component-production-design-2026-05-25.md` §"§11 The runtime-branch → main → deploy path"; `/home/li/primary/reports/third-designer/25-most-important-questions-2026-05-24/2-cloud-mutate-quorum-multi-zone.md` §"§7 The operator slice plan".

---

## Summary: What the Fully-Working Prototype Must Realise

1. **Operation routing:** Two signal channels (ordinary / owner) with typed operations, provider variants, and capability-state reporting per build.
2. **State machine:** Three-step ceremony (PreparePlan / ApprovePlan / ApplyPlan) with durable plan storage and two-state acknowledgment path ready for Mutate naming.
3. **Actor topology:** CloudflareProvider actor for HTTP, Store for policy/plans, both wired to request dispatcher; async-with-timeouts, not blocking.
4. **Integration seams:** Mutate/Query split at socket level; NotAuthoritative path shaped but unpopulated; list-before-delete + record-ID ownership; proxied-flag check; Criome identity as optional additively-integrated fields when records 317-318 land.

All code shapes tested with NOTA round-trip, rkyv frame round-trip, and unsupported-capability typed rejection. No `signal-core` dependency. Contract purity (no tokio/kameo/redb in the crate). Daemon lives on `cloud-domain-criome-runtime` branch.

---

Reports inspected: 13 (all listed in context).

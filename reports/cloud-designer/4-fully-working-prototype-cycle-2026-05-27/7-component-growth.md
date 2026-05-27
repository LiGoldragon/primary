# 7 · Component growth — what to develop next

The audit ([6-audit.md](6-audit.md)) classified 16 gaps; this
file picks the next-iteration growth slate and lays out the
sequencing that keeps blast radius small.

## What grew THIS cycle (already landed)

- **signal-cloud**: `RecordIdentifier` newtype became a proper
  contract type — closed the gap my first prototype report
  flagged. Landed in main `58862593` (cloud-operator).
- **cloud daemon**: `ProviderClient::apply_plan` wired full
  delete + upsert path. Landed in main `58862593`.
- **cloudflare adapter**: `FlarectlApi` implements the full Api
  trait (zones + records + create + update + delete); HttpApi
  too. Landed in main `58862593`.
- **cloud flake**: gopass-backed CF_API_TOKEN wrap on flarectl
  + flarectl on cloud-daemon's PATH + devShell update. Landed
  in this cycle's `ec2d3493`.
- **Test surface**: 11 new flarectl_e2e tests that exercise
  FlarectlApi through the full Plan lifecycle via ScriptRunner.
  Landed in `ec2d3493`. Establishes the pattern future
  iterations follow for new operation tests.

## Recommended next slate — by priority

These are the gaps the next cycle should close. Ordered by a
combination of (severity × ease).

### Tier 1 — small, isolated, high-value

**D2: gopass fail-loud (flake one-liner).** Change the wrap to
explicitly exit 78 on gopass failure rather than silently
exporting empty token. ~3 lines in `flake.nix`. Closes a real
operability hole: missing entries currently surface as opaque
Cloudflare auth errors. Single-cycle.

**A3: pin redirect-observation as RequestUnsupported.** Until
flarectl pagerules read is wired, return the same
`RequestUnsupported(CapabilityNotCompiled)` for Cloudflare as
for non-Cloudflare. ~5 lines in `cloud/src/lib.rs:228-250`.
Single-cycle.

**C3: TTL + priority on `DomainNameSystemRecord`.** Add `ttl:
Option<u32>` and `priority: Option<u16>` to the contract; thread
through `record_arguments` in both adapters. ~20 lines across
signal-cloud + cloudflare.rs + cloudflare_cli.rs. Single-cycle.

### Tier 2 — medium, high-value

**B2: `CredentialHandleUnknown` on registration.** Verify
credential handle resolves at register-time. Currently you can
register with a handle that doesn't exist; failure surfaces
only at first apply. ~10 lines in `register_account`. Cycle 2.

**A1: real `Validate` body.** Parse record values per record
kind, emit Findings for failures. ~50 lines in cloud daemon
`validate`. Closes a contract-advertised but no-op operation.
Cycle 2.

**A2: diff-aware `prepare_plan`.** Fetch current records (via
the same `cloudflare.records` already on Store), diff against
DesiredState, emit `records_to_create` / `records_to_update` /
`record_names_to_delete` from the actual diff. ~80 lines on the
daemon's `prepare_plan`. Likely needs a new `current_state_for`
helper on Store. Cycle 2 or 3 — pairs cleanly with B1
(`PlanGenerationFailed`) becoming alive.

**C1: HTTP↔CLI fallback adapter.** New `FallbackApi` that holds
two `Arc<dyn Api>` and routes based on operation type (DNS to
flarectl, pagerules to HttpApi). ~40 lines in `cloudflare.rs`.
Closes intent 918's CLI-or-API option. Cycle 2 or 3.

### Tier 3 — large, foundational

**B3: Plan → Mutate state machine.** Intent 338's rename +
Mutate-sent / Mutated lifecycle. Touches both contracts and the
daemon end-to-end. **Recommend: separate cycle dedicated to
this rename, no other changes ride alongside.** ~300+ line
diff across three repos. Cycle 4 minimum.

**B4: richer `Approval` with approver + timestamp + signature.**
Couples with intent 339's quorum-of-agreement. Wait for
domain-criome to mature so the identity primitives (Sub-ID,
Criome identity) are settled before adding fields that depend
on them. Defer to cycle when domain-criome integration begins.

### Tracked-but-deferred

**A4: PlanExpired logic.** Low priority unless plan-lifetime
emerges as a real concern. Currently a dead reason variant.

**B1: PlanGenerationFailed.** Automatically becomes alive once
A1 and A2 land — no separate work.

**C2: flarectl spawn cost.** Document in ARCHITECTURE as a
known characteristic; revisit if first-production traffic shows
it's a bottleneck.

**D1: gopass path parameter.** Defer to when a deployment
genuinely needs a non-default path. Premature parameterization
now.

**X1: Help-on-every-enum.** Cross-component. Track operator's
signal-frame work (`primary-ezqx.3`); cloud picks it up free
when the upstream lands.

**X2, X3: DomainAuthority / Sub-ID identity.** Tied to
domain-criome maturation. Will land naturally when cloud and
domain-criome compose. Document in ARCHITECTURE as a known seam,
don't preemptively grow signal-cloud.

## Sequencing for the next cycle

Recommend one cycle that ships **Tier 1 entirely + B2 from
Tier 2**: total ~40 lines of code across 3 repos, all isolated,
no contract changes. The cycle's test additions are minimal
(extend flarectl_e2e.rs with gopass-failure simulation and TTL
verification).

That gives a tight iteration loop while keeping the larger
items (A1, A2, C1, B3) lined up for dedicated cycles.

## Audit-loop discipline this surfaces

This cycle revealed two patterns worth naming explicitly:

**1. Convergent prototyping is information, not waste.** My
prototype's src/cloudflare_cli.rs was structurally near-identical
to what cloud-operator landed on main. The reasonable reaction
was *not* to bemoan duplicated effort but to read main and take
its work — the convergence itself proves the shape is the
right shape. The audit then identifies the genuinely additive
contributions (the gopass wrap; the FlarectlApi-via-CapturingRunner
test pattern), which are what stays.

**2. Dead reply variants are a contract smell.** Several
`RejectionReason` variants (`PlanExpired`, `PlanGenerationFailed`,
`CredentialHandleUnknown`) are declared but unemitted. The
right move is either to wire them (B1, B2) or remove them
(B1, A4). Carrying dead variants gives callers a false sense
of the typed surface they're handling.

Both observations are candidates for `skills/component-triad.md`
or `skills/audit-loop.md` (the latter doesn't exist; potential
future skill).

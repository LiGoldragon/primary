# 6 · Audit — critique against the full designed surface

The audit standard per psyche 977 + 979: the prototype must use
all designed components fully. Where it doesn't, the gap is a
finding — either a prototype fix (P) or a component growth
requirement (C). Items already correctly deferred by intent
appear in the checklist's *out-of-scope* section, not here.

Per-component critique below. Findings are anchored against
[3-code-survey.md](3-code-survey.md) line numbers (current main).

## signal-cloud — ordinary contract

### Used fully

The contract's full Operation + Reply surface is exercised
across the combined test set (runtime.rs + flarectl_e2e.rs):
Observe (Capabilities, Zones, Records, Plan) + Validate; Reply
(Observed for all five observation results, Validated,
RequestUnsupported, RequestRejected). Every payload variant
appears in at least one test path.

### Finding A1 — `Validate` body is a no-op (C)

`Store::validate` at `cloud/src/lib.rs:565` walks the
gate-and-permission checks (provider built, capability supported,
configured) and then returns `ValidationReport { findings: vec![] }`
unconditionally on the success path. There is no actual rule
checking: record values are not parsed (an A record with
`"not-an-ip"` would be accepted), TTL bounds are not enforced
(the Plan doesn't carry a TTL at all), redirect URL well-formedness
is not checked.

**Why it bites:** the contract advertises Validate as a real
operation. A caller that uses it as a pre-flight gate against
PreparePlan is getting false reassurance. The reply type
(`ValidationReport.findings: Vec<Finding>` with severity +
message at `signal-cloud/src/lib.rs:287-289`) is built for real
findings.

**Classification:** Component growth on cloud daemon.
Smallest viable fix: parse `record.value` per `record.kind`
(IPv4 for A, IPv6 for AAAA, hostname for CNAME/MX/NS/PTR, text
for TXT) and emit a Finding for each parse failure. ~50 lines.

### Finding A2 — `prepare_plan` is not diff-aware (C)

`prepare_plan` at `cloud/src/lib.rs:603` puts every record from
`DesiredState.records` into `Plan.records_to_create`. It never
emits `records_to_update` or `record_names_to_delete`. That
means:

- Re-applying the same DesiredState results in
  `records_to_create` flagged for ALREADY-EXISTING records;
  `upsert_record` at the apply layer catches this and routes to
  `update_record` instead of `create_record` (so the bug is
  masked at apply-time).
- Records present on the provider but absent from DesiredState
  are NEVER deleted. There is no path from desired-state-absence
  to provider-side deletion.

**Why it bites:** DesiredState should mean "the state I want",
not "the records I want to add". A user expecting that a
DesiredState with empty records empties the zone gets surprised
when nothing happens.

**Classification:** Component growth on cloud daemon (the
PreparePlan logic). Could equivalently move to
owner-signal-cloud's policy layer — intent 325 says plan
preparation belongs on the owner surface, so wherever PreparePlan
handler lives, it needs to fetch current state, diff, and emit
all three mutation lists. ~100 lines.

### Finding A3 — `Observe::Redirects` returns empty silently for Cloudflare (P/C)

`Store::observe` for `Observation::Redirects` at
`cloud/src/lib.rs:228-250` returns
`RequestUnsupported(CapabilityNotCompiled)` for non-Cloudflare,
or an empty `RedirectListing { rules: vec![] }` for Cloudflare.

But Cloudflare DOES have redirects (Page Rules / Rulesets). The
component just doesn't read them yet. flarectl's `pagerules
list` could be wired for read in one ProviderClient method.

**Classification:** Mixed. Prototype fix: pin the current
empty-listing as `RequestUnsupported(CapabilityNotCompiled)`
instead — same code as non-Cloudflare. Component growth: wire
flarectl pagerules list to actually return rules for Cloudflare.

### Finding A4 — `RequestRejected::PlanExpired` is dead (C)

The reason enum at `signal-cloud/src/lib.rs:313-318` includes
`PlanExpired`, but no path ever emits it. `observe_plan` at
`cloud/src/lib.rs:633-645` emits `PlanExpired` when the plan
isn't in the store, which is **PlanUnknown**, not expired. There
is no actual expiry logic.

**Classification:** Either implement plan expiry (component
growth) or rename the variant to `PlanUnknown` (contract growth).
The former matches the typed semantic better — Plans should
expire by TTL since they're materialized state.

## owner-signal-cloud — policy contract

### Used fully

All 7 owner operations have at least one test path. All 8 reply
variants are emitted.

### Finding B1 — `PlanGenerationFailed` is dead (C)

`RejectionReason::PlanGenerationFailed` at
`owner-signal-cloud/src/lib.rs:131-144` is declared but never
emitted. The current `prepare_plan` cannot fail at the
generation step (it just copies records into the Plan).

**Classification:** Becomes alive if Finding A1 (Validate
becomes real) and Finding A2 (PreparePlan becomes diff-aware)
both land — diff-aware planning + content validation can both
fail and need PlanGenerationFailed to surface the cause.

### Finding B2 — `CredentialHandleUnknown` is dead (C)

Same shape as B1: declared at line 131-144 but no path emits it.
The current registration path takes any credential handle
without verifying it resolves. The reason is intended for a
"caller asked to use credential X but X doesn't exist in the
credential source" rejection.

**Classification:** Add a verify step inside `register_account`
that calls `CredentialSource::token(handle)` and returns
`CredentialHandleUnknown` on `CredentialUnavailable`.

### Finding B3 — Plan state machine is missing (C)

Intent 338 (third-designer/25/2-cloud-mutate-quorum-multi-zone.md)
specifies: `Plan` renamed to `Mutate`; daemon enters two-state
lifecycle — **Mutate-sent** (provider request not yet
acknowledged) → **Mutated** (acknowledged). Main still uses
`Plan` and has no Mutate-sent / Mutated tracking. The current
apply path is single-shot and synchronous.

**Classification:** Significant component growth across both
contracts and the daemon. Rename Plan → Mutate everywhere; add
a MutationState enum; thread it through apply_plan. Likely a
multi-cycle effort. **Recommend documenting as a known seam in
ARCHITECTURE.md** and starting with the rename in a separate
cycle to keep blast radius small.

### Finding B4 — `ApprovePlan` is a flat boolean (C)

Currently `approve_plan` just records the identifier in an
`approved_plans` set. Real owner authority would want:

- Who approved (an `Approver` identity).
- Approval timestamp.
- Optional approval expiry (parallel to Plan expiry).
- Approval signature for non-repudiation.

**Classification:** Component growth on owner-signal-cloud
contract. Tracks alongside intent 339's quorum-of-agreement
semantic.

## cloudflare provider client

### Used fully

Both HttpApi and FlarectlApi implement the full Api trait.
ProviderClient.apply_plan composes them correctly. RecordIdentifier
threads through. Test coverage exercises both adapters
(FixtureCloudflareApi for runtime.rs, FlarectlApi via
ScriptRunner for flarectl_e2e.rs).

### Finding C1 — No HTTP↔CLI fallback path (C)

The current daemon picks ONE provider client at construction
(`ProviderClient::production()` returns FlarectlApi,
`production_http()` returns HttpApi). There is no runtime
fallback: if flarectl fails for a specific operation (e.g.
pagerules mutation that flarectl doesn't support), the request
just fails with `RequestRejected`.

**Why it bites:** Intent 918 explicitly preserves the option to
use the API directly if the CLI isn't suitable. The current
shape forces an all-or-nothing choice at daemon-construction
time.

**Classification:** Component growth on cloud/cloudflare.rs.
Add a `FallbackApi` that holds (primary: Arc<dyn Api>, secondary:
Arc<dyn Api>) and routes operations based on capability. ~40
lines. Use it as the production default.

### Finding C2 — `update_record` semantics differ between adapters (C)

`HttpApi.update_record` does a PATCH with the new record content
keyed by RecordIdentifier — atomic, single-call. 
`FlarectlApi.update_record` does `dns update --id <id>` with
ALL new fields — also single-call. So far so good.

But: `find_record_after_mutation` (used by both create and
update on FlarectlApi) calls `records()` again, which spawns TWO
more flarectl invocations (`zone list` + `dns list`). Each create
costs 4 flarectl spawns, each update costs 4 spawns. For a
multi-record plan apply this multiplies fast: a 10-record plan
is 40+ spawns.

**Why it bites:** Process spawn cost. The Cloudflare HTTP path
amortizes credential verification across a single connection;
the flarectl path pays it per spawn.

**Classification:** Either component growth (memoize the
records call, batch the lookups, use flarectl's batch DNS
endpoint) or accept the cost for the first slice. Recommend
documenting as a known cost; first production slice is likely
small enough that 40 spawns per apply is acceptable.

### Finding C3 — `record_arguments` doesn't pass TTL or priority (C)

flarectl's `dns create` accepts `--ttl` (default 1=automatic)
and `--priority` (MX records). The cloud component's
`DomainNameSystemRecord` at `signal-cloud/src/lib.rs` doesn't
have TTL or priority fields. Records always get default TTL
(automatic) and no priority on MX.

**Classification:** Contract growth — add `ttl: Option<u32>` and
`priority: Option<u16>` to `DomainNameSystemRecord`. Then thread
through `record_arguments` in both adapters.

## Nix packaging

### Used fully

flarectl is a real runtime dep on cloud-daemon's PATH.
gopass-wrap fetches CF_API_TOKEN per spawn. devShell carries the
same wrapped binary.

### Finding D1 — gopass path is hardcoded (C)

The wrap reads `cloudflare/api-token` literally. If a deployment
wants to use a different password manager path (e.g.
`production/cloudflare/api-token`), the flake needs editing
plus a rebuild.

**Classification:** Nix-config growth. Make the gopass path a
flake parameter: `cloudflareTokenPath ? "cloudflare/api-token"`.
~5 lines.

### Finding D2 — No fail-loud surface when gopass entry is missing (P)

`gopass show -o nonexistent/path` prints an error to stderr and
exits non-zero. The wrap's `--run` runs the command but does
NOT check its exit code; the `export CF_API_TOKEN=...` assigns
the empty string, and flarectl then fails with a Cloudflare auth
error that doesn't mention gopass.

**Classification:** Prototype fix on flake. Change the wrap to:

```nix
wrapProgram $out/bin/flarectl \
  --run 'CF_API_TOKEN=$(${pkgs.gopass}/bin/gopass show -o cloudflare/api-token) || { echo "cloud: cannot fetch CF_API_TOKEN from gopass cloudflare/api-token" >&2; exit 78; }; export CF_API_TOKEN'
```

Exit code 78 = EX_CONFIG (sysexits.h). The daemon then sees a
clean process-failure surface instead of a downstream auth
failure.

## Cross-cutting

### Finding X1 — `(Help Main)` capability discovery is unexercised (D/C)

Intent 263 (referenced in
third-designer/22-cloud-criome-design-research/4-opt-in-feature-compilation-design.md)
specifies that compiled-in providers should appear in `(Help
Main)` reply so callers can discover capability shape without a
separate Observe call. The cloud daemon does NOT emit Help; the
signal-frame layer's Help-on-every-enum macro (primary-ezqx.3)
is the upstream that would supply this.

**Classification:** Cross-component growth — depends on
signal-frame's Help-on-every-enum landing first. Track as a
dependency on operator-track work; not a cloud-specific gap.

### Finding X2 — `DomainAuthority` + `NotAuthoritative` not in contracts (D)

Intent 311-320, surfaced in
third-designer/23-architecture-update-2026-05-23/1-cloud-domain-criome-audit-and-revision.md
(R2): the contract needs a `DomainAuthority` concept and a
`NotAuthoritative` rejection pointing to the authoritative
daemon. The landed contracts use string newtypes for domain
identity and have no NotAuthoritative reason.

**Classification:** Contract growth — relevant when cloud and
domain-criome compose, which is a future cycle. Document but
don't add yet.

### Finding X3 — Sub-ID + Criome identity primitives use string newtypes (D)

Same R3 cluster: landed contracts use string newtypes for
account, zone, record identifiers. Intent 311-320 calls for
stronger typing (content-addressed Sub-IDs, Criome identity
primitives).

**Classification:** Contract growth — depends on signal-sema
maturity. Document but don't add yet.

## Gap classification summary

| ID | Component | Class | Severity | Next-iteration priority |
|---|---|---|---|---|
| A1 | cloud daemon (validate) | C | Medium | High — Validate is contract-visible |
| A2 | cloud daemon (prepare_plan) | C | High | High — DesiredState semantic is broken |
| A3 | cloud daemon (redirect observe) | P+C | Medium | Medium — make explicit, defer real wiring |
| A4 | signal-cloud (PlanExpired) | C | Low | Low — rename or wire expiry |
| B1 | owner-signal-cloud (PlanGenerationFailed) | C | Low | Low — alive once A1+A2 land |
| B2 | owner-signal-cloud (CredentialHandleUnknown) | C | Medium | Medium — verify-on-register |
| B3 | both contracts (Plan→Mutate state machine) | C | High | High — intent 338, document seam first |
| B4 | owner-signal-cloud (richer Approval) | C | Medium | Medium — couples with quorum (intent 339) |
| C1 | cloud/cloudflare (HTTP↔CLI fallback) | C | High | High — intent 918 |
| C2 | cloud/cloudflare_cli (spawn cost) | C | Low | Defer — document |
| C3 | signal-cloud (TTL + priority on record) | C | Medium | Medium — small, isolated |
| D1 | flake (gopass path parameter) | C | Low | Low |
| D2 | flake (fail-loud on missing entry) | P | Medium | High — easy fix |
| X1 | signal-frame (Help-on-every-enum) | D | n/a | Tracked by operator |
| X2 | both contracts (DomainAuthority) | D | n/a | Future cycle, defer |
| X3 | both contracts (Sub-ID identity) | D | n/a | Future cycle, defer |

Next pass selects the top-priority gaps and grows them. See
[7-component-growth.md](7-component-growth.md) for the
recommended sequencing.

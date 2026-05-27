# 4 · Completeness checklist — what "fully working" means

Synthesized from
[1-spirit-substance-for-full-implementation.md](1-spirit-substance-for-full-implementation.md),
[2-reports-working-solutions.md](2-reports-working-solutions.md),
[3-code-survey.md](3-code-survey.md). The checklist is per
designed component; each line tracks whether the implementation
satisfies it after this cycle.

## signal-cloud (ordinary working contract)

- [x] **Observe::Capabilities** — wired in daemon, returns typed CapabilityReport with per-provider+capability state. Distinguishes NotBuilt / Compiled / Configured / Authorized per intent 342.
- [x] **Observe::Zones** — wired for Cloudflare via FlarectlApi.zones; falls back to last-known cache.
- [x] **Observe::Records** — wired for Cloudflare via FlarectlApi.records (zone-name-resolution included).
- [ ] **Observe::Redirects** — STUB. Daemon returns empty RedirectListing for Cloudflare; non-Cloudflare returns RequestUnsupported. flarectl pagerules is read-only — could be wired for read, mutation needs HTTP fallback.
- [x] **Observe::Plan** — wired; reads from prepared-plan store, returns RequestRejected(PlanExpired) on unknown.
- [x] **Validate** — wired path; **but** the validation body returns empty findings (no actual rule-checking). Reply shape works; logic is a no-op.
- [x] **Reply::Observed / Validated / RequestUnsupported / RequestRejected** — all emitted under appropriate conditions.

## owner-signal-cloud (policy contract)

- [x] **RegisterAccount** — wired; stores AccountBinding, returns AccountRegistered.
- [x] **RotateCredential** — wired; updates existing binding's credential handle. Rejects AccountUnknown if not registered.
- [x] **SetPolicy** — wired; replaces full policy, returns counts.
- [x] **PreparePlan** — wired; emits Plan with records_to_create from DesiredState. Rejects ProviderNotConfigured if no provider built/configured.
- [x] **ApprovePlan** — wired; stores plan identifier in approved set. Rejects PlanUnknown if not prepared.
- [x] **ApplyPlan** — wired for Cloudflare; rejects PlanNotApproved if missing, CapabilityUnauthorized for redirect mutations, ProviderNotConfigured for non-Cloudflare.
- [x] **RetireAccount** — wired; removes binding, returns AccountRetired.

## cloudflare provider client

- [x] **Api trait** — both HttpApi and FlarectlApi implement all five methods (zones, records, create_record, update_record, delete_record).
- [x] **HttpApi** — full HTTP/JSON path; main slice ships this.
- [x] **FlarectlApi** — full flarectl shell-out path; uses `--json` and parses cloudflare-go's PascalCase tags. Zone-by-name lookup for compatibility with main's HTTP zone-by-ID semantic.
- [x] **CommandRunner trait** — abstraction lets ScriptRunner in tests inject scripted responses without spawning processes.
- [x] **ProviderClient::apply_plan** — wired: fetches current records, deletes named, upserts the rest, returns updated RecordListing.
- [x] **RecordIdentifier newtype** — added in main's signal-cloud contract; threads through update_record and delete_record.
- [x] **ProxyMode propagation** — Plan → DesiredState → DomainNameSystemRecord → mutation invocation → flarectl `--proxy` flag.

## cloud daemon runtime

- [x] **Store** — full read+write via FlarectlApi or HttpApi (constructor-injectable).
- [x] **DaemonConfiguration via nota-config** — single-NOTA-argument rule honored.
- [x] **Two-socket binding** — ordinary + owner Unix sockets at configured paths/modes.
- [x] **Volatile cache for last_known_records / last_known_zones** — intent 681/687 honored (no persistent store).
- [x] **CredentialSource trait + EnvironmentCredentialSource** — token via env var per intent 682.

## nix packaging

- [x] **flarectl is a runtime dep** — wrapped onto cloud-daemon's PATH via `cloudRuntimePath = makeBinPath [cloudflareCli]`. Per intent 923.
- [x] **flarectl wrapped with gopass** — `wrapProgram $out/bin/flarectl --run 'export CF_API_TOKEN=$(gopass show -o cloudflare/api-token)'`. Per intent 924 / 682 / 689. Realises FEMOS auth pattern inside the nix closure.
- [x] **devShell includes wrapped flarectl** — so iterative dev work also picks up the gopass token flow.

## tests (the "all components used" surface)

- [x] **Existing main tests** — 11 in `tests/runtime.rs` cover CLI dispatch, capability observation, cloudflare record observation, owner registration, plan-apply via FixtureCloudflareApi.
- [x] **New flarectl_e2e tests** — 11 in `tests/flarectl_e2e.rs` exercise FlarectlApi end-to-end through Plan lifecycle, Observe paths, Validate, CredentialRotation, RetireAccount, Redirect-observation stub.
- [x] **All signal-cloud + owner-signal-cloud operations exercised at least once across the combined test set.**

## Out-of-scope per psyche intent (deferred, NOT gaps)

- **Schema-engine cutover** — psyche 914 holds the component on old NOTA stack for this push.
- **Multi-account** — psyche-deferred; single-account flow is the first target.
- **GoogleCloud / Hetzner providers** — psyche 282/685 pins Cloudflare-first.
- **Auto-upgrade for missing capabilities** — psyche 284/295, Minimum certainty future work.
- **meta-signal rename** — psyche 290/299, Minimum certainty, held for explicit affirmation.

## Genuine open gaps for the audit pass

These are the audit-driven findings, listed in [6-audit.md](6-audit.md):

1. **Validate is a no-op** — returns empty findings without checking anything.
2. **prepare_plan emits no record_names_to_delete** — diff-aware planning missing.
3. **Redirect mutation** — typed rejection via CapabilityUnauthorized, but the contract leaks the truth (it pretends supportable then rejects).
4. **Plan state machine** — intent 338 renames Plan to Mutate with Mutate-sent → Mutated lifecycle; main still uses Plan and lacks the two-state.
5. **(Help Main) capability discovery** — intent 263; not exercised, probably belongs to signal-frame layer.
6. **DomainAuthority + NotAuthoritative** — intent 311-320; not in landed contracts.
7. **Sub-ID + Criome identity primitives** — same intent batch; landed contracts use string newtypes.

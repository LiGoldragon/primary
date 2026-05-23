# Cloud and Domain Criome Repo Scaffold Prototype

## Scope

This report is the system-specialist assistant lane for the cloud
component birth investigation. The assigned lane was report-only unless
one of the requested repositories already existed and could safely host a
feature worktree.

Requested repositories:

- `cloud`
- `signal-cloud`
- `owner-signal-cloud`
- `domain-criome`
- `signal-domain-criome`
- `owner-signal-domain-criome`

No GitHub remotes were to be created.

## Intent Captured

One durable clarification was captured through `spirit` before the
investigation:

`component-triad` clarification: `owner-signal-*` remains the active
policy-signal naming convention until an explicit rename lands. The
possible `meta-signal-*` rename is only under consideration.

## Repository Existence

Result: none of the six requested repositories exists locally or as a
GitHub repository under the checked Li namespaces.

Local checks:

- `ghq list` had no exact match for any requested repository.
- `RECENT-REPOSITORIES.md`, `protocols/active-repositories.md`, and the
  local `repos/` index had no exact match for the requested repository
  names.

Remote checks:

- `gh repo view LiGoldragon/<name>` returned no repository for each of
  the six names.
- `gh repo view Criome/<name>` returned no repository for each of the six
  names.
- `gh search repos` scoped to `user:LiGoldragon` and `org:Criome` for
  `cloud` and `domain-criome` name matches returned no candidates.

Because no repo exists, I did not create a feature branch, feature
worktree, local repository, scaffold file, or GitHub remote. The rest of
this report is the concrete scaffold plan.

## Component Boundary

Two stateful triads are implied.

`cloud` is the daemon that talks to external cloud-provider APIs:
Cloudflare first, then Google, Hetzner, and other providers. Provider
support is build-time or policy-time capability. A daemon that does not
support a provider replies with a typed unsupported-provider reply rather
than pretending the operation exists.

`domain-criome` is the domain registry and projection component for
Criome-domain knowledge. It should own the intelligent domain model and
project provider-neutral desired DNS and redirect state. It should not
know Cloudflare-specific HTTP details; `cloud` owns provider adapters.

The first integration line should therefore be:

1. `domain-criome` exposes a provider-neutral projection of desired
   external domain state.
2. `cloud` observes that projection, compares it to Cloudflare, prepares
   a plan, and applies it when authorized.
3. Cloudflare credentials and account policy are configured through
   `owner-signal-cloud`, using secret handles, not secret bytes.

## Minimal Repo Trees

The six repositories should start with the current triad layout and
current owner-signal naming.

```text
cloud/
  AGENTS.md
  ARCHITECTURE.md
  INTENT.md
  skills.md
  Cargo.toml
  flake.nix
  bootstrap-policy.nota
  examples/
    request.nota
  src/
    lib.rs
    bin/
      cloud.rs
      cloud-daemon.rs
  tests/
    cli_round_trip.rs
    daemon_smoke.rs

signal-cloud/
  AGENTS.md
  ARCHITECTURE.md
  skills.md
  Cargo.toml
  flake.nix
  examples/
    canonical.nota
  src/
    lib.rs
  tests/
    round_trip.rs

owner-signal-cloud/
  AGENTS.md
  ARCHITECTURE.md
  skills.md
  Cargo.toml
  flake.nix
  examples/
    canonical.nota
  src/
    lib.rs
  tests/
    round_trip.rs

domain-criome/
  AGENTS.md
  ARCHITECTURE.md
  INTENT.md
  skills.md
  Cargo.toml
  flake.nix
  bootstrap-policy.nota
  src/
    lib.rs
    bin/
      domain-criome.rs
      domain-criome-daemon.rs
  tests/
    cli_round_trip.rs
    daemon_smoke.rs

signal-domain-criome/
  AGENTS.md
  ARCHITECTURE.md
  skills.md
  Cargo.toml
  flake.nix
  examples/
    canonical.nota
  src/
    lib.rs
  tests/
    round_trip.rs

owner-signal-domain-criome/
  AGENTS.md
  ARCHITECTURE.md
  skills.md
  Cargo.toml
  flake.nix
  examples/
    canonical.nota
  src/
    lib.rs
  tests/
    round_trip.rs
```

The contract crates should be created first. The runtime crates should
depend on the contracts through named Git references once the remotes
exist. Until remotes exist, local prototype work should keep everything
inside one feature worktree lane and avoid committing cross-repo `path =
"../"` dependencies as permanent shape.

## Minimal Signal Cloud Contract Sketch

`signal-cloud` should start as the provider-neutral ordinary contract
for cloud operations. Cloudflare appears as a `Provider` variant, not as
a crate name.

Suggested first record set:

- `Provider`: `Cloudflare`, `Google`, `Hetzner`
- `Capability`: `DnsRecords`, `RedirectRules`, `CloudHosts`
- `ProviderQuery`: optional provider plus optional capability
- `DomainName`: transparent string newtype
- `Record`: provider-neutral DNS record shape
- `RedirectRule`: provider-neutral redirect rule shape
- `DesiredState`: records and redirects to make true
- `Plan`: daemon-minted plan identifier plus planned changes
- `Operation`: `Observe`, `Plan`, `Apply`
- `Reply`: `CapabilitiesObserved`, `StateObserved`, `PlanPrepared`,
  `PlanApplied`, `RequestUnsupported`, `RequestRejected`

The minimum round-trip test should exercise:

- `Operation::Observe(Observation::Capabilities)`
- `Operation::Plan(DesiredState)`
- `Operation::Apply(PlanIdentifier)`
- `Reply::RequestUnsupported` for unsupported providers or capabilities
- rkyv length-prefixed frame round trip through `signal-frame`
- NOTA text round trip and canonical example inclusion

The first canonical NOTA examples can be shaped like:

```nota
(Observe Capabilities)
(Plan ([("example.criome" A "203.0.113.10")] []))
(Apply "plan-one")
```

The exact syntax above is illustrative, not final. Before implementation,
the concrete Rust type tree should be written first, then the canonical
NOTA examples should be generated from the real `nota-codec` output so
the example file cannot drift from the derives.

## Minimal Owner Signal Cloud Contract Sketch

`owner-signal-cloud` owns privileged provider policy and lifecycle, not
ordinary DNS changes.

Suggested first record set:

- `Provider`: same closed set as `signal-cloud`
- `SecretHandle`: transparent string newtype naming an external secret,
  never carrying the API token itself
- `Account`: provider plus provider-native account or zone handle
- `ProviderSupport`: provider plus capabilities enabled in this daemon
- `Operation`: `Start`, `Drain`, `Register`, `Enable`, `Disable`,
  `Reload`, `Retire`
- `Reply`: `Started`, `DrainedAndStopped`, `ProviderRegistered`,
  `ProviderEnabled`, `ProviderDisabled`, `PolicyReloaded`,
  `ProviderRetired`, `RequestRejected`

This keeps API tokens out of reports, Nix, fixtures, and ordinary signal.
The runtime daemon can resolve secret handles through the cluster secret
mechanism when the provider adapter starts.

## Minimal Signal Domain Criome Contract Sketch

`signal-domain-criome` should not expose Cloudflare words. It should
expose the Criome-domain registry and provider-neutral projection.

Suggested first record set:

- `DomainName`: transparent string newtype
- `OwnerName`: transparent string newtype or later authority reference
- `Endpoint`: provider-neutral target, such as address, canonical name, or
  external URL
- `Redirect`: source domain plus target URL
- `Record`: provider-neutral desired DNS record
- `Projection`: desired DNS records plus redirect rules
- `Observation`: `Domains`, `Projection`
- `Operation`: `Observe`, `Resolve`, `Project`, `Watch`, `Unwatch`
- `Reply`: `DomainsObserved`, `Resolved`, `ProjectionPrepared`,
  `SubscriptionOpened`, `SubscriptionRetracted`, `RequestRejected`

The first useful call for the cloud integration is `Project`, returning
provider-neutral desired DNS and redirect state. `cloud` can then convert
that projection into a provider-specific plan.

## Minimal Owner Signal Domain Criome Contract Sketch

`owner-signal-domain-criome` owns root registry and policy authority.

Suggested first record set:

- `Root`: the Criome root domain family, not provider-specific TLD wiring
- `Delegation`: authority relationship for a domain branch
- `Registration`: domain name plus owner authority
- `Retirement`: domain name plus reason
- `Operation`: `Start`, `Drain`, `Register`, `Delegate`, `Retire`,
  `Reload`
- `Reply`: `Started`, `DrainedAndStopped`, `DomainRegistered`,
  `DelegationAccepted`, `DomainRetired`, `PolicyReloaded`,
  `RequestRejected`

This is where root-domain policy belongs. Cloudflare zone identifiers,
page-rule identifiers, and redirect-rule identifiers do not belong here.

## Scaffold Order

1. Create the six repos locally under `/git/github.com/LiGoldragon/` only
   when the main system-specialist authorizes repository creation.
2. Initialize each as jj-colocated, with `main` as the first bookmark.
3. Add `AGENTS.md` as the standard `@~/primary/AGENTS.md` shim and write
   `ARCHITECTURE.md` before the first commit.
4. Build `signal-domain-criome` and `owner-signal-domain-criome` first
   because their provider-neutral vocabulary is upstream of the first
   cloud plan.
5. Build `signal-cloud` and `owner-signal-cloud` next, with
   `Provider::Cloudflare` and typed unsupported replies included from the
   beginning.
6. Add `domain-criome` and `cloud` runtime crates with thin CLIs that take
   exactly one NOTA argument and speak only to their own daemons.
7. Use a feature branch named `cloud-component-birth` in each repo once a
   repo exists. Worktrees should live at
   `~/wt/github.com/LiGoldragon/<repo>/cloud-component-birth/`.
8. Do not create GitHub remotes until the system-specialist explicitly
   authorizes that step.

## First Tests

Each signal crate should ship with a focused `round_trip.rs` test before
any daemon exists:

- request frame rkyv round trip
- reply frame rkyv round trip
- NOTA round trip for every first operation and reply variant
- canonical example inclusion check
- unsupported-provider or unsupported-capability reply round trip

Each runtime crate should then add:

- CLI one-argument discipline test
- daemon smoke test with temporary state directory
- unsupported-provider request returning a typed reply without touching a
  real provider
- Cloudflare adapter tests only against a fake HTTP server until real
  credentials are explicitly authorized

All tests should be exposed through Nix checks, not only Cargo commands.

## Open Questions For The Main Lane

1. Repository owner: should these repos live under `LiGoldragon`, or is
   `Criome` the better organization for `domain-criome` and possibly the
   cloud-provider contracts?
2. Boundary name: the assignment used `domain-criome`. That name should be
   confirmed before repo creation because it reverses the user's earlier
   spoken exploration from `Criome domain` toward a domain-first component.
3. First provider surface: should Cloudflare DNS records and Cloudflare
   redirect rules be one first capability group, or should redirect rules be
   delayed until DNS state round-trips cleanly?
4. Authorization: should ordinary `Apply` be present on `signal-cloud`
   immediately, gated by Criome authorization at runtime, or should first
   cloud work expose only `Plan` until the Criome-daemon authorization flow
   is ready?

## Recommendation

Start by creating only the two ordinary contract repos:
`signal-domain-criome` and `signal-cloud`. That gives a concrete typed
surface for the design discussion without forcing provider credentials,
owner policy, runtime actor shape, or remote repository decisions too
early. Once the first two contracts have rkyv and NOTA round-trip tests,
add the owner contracts, then the daemons.

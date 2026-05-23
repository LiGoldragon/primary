# Provider API scope research for cloud

## Frame

The new `cloud` component should own provider API automation: DNS,
redirect/rules surfaces, cloud server inventory, and later cloud
server/network lifecycle. This report scopes the first non-Cloudflare
providers from primary sources only: Google Cloud DNS and Hetzner Cloud
server/network/DNS surfaces.

The immediate implementation should keep `cloud` narrow: expose a
provider-capability model and implement DNS operations first. Server and
network mutation should wait until the authorization, dry-run, and
rollback shape is designed, because those operations destroy or expose
infrastructure.

## Google Cloud DNS

Official source:
https://docs.cloud.google.com/dns/docs/apis

Google Cloud DNS has a clean REST surface and official client-library
authentication path. The API reference lists these operation families:

- `managedZones`: create, delete, get, list, patch, update, IAM policy
  get/set, and `testIamPermissions`.
- `resourceRecordSets`: create, delete, get, list, patch.
- `changes`: create, get, list, used for atomic record-set collection
  changes.
- `dnsKeys`: get, list, for DNSSEC key visibility.
- `managedZoneOperations`: get, list, for long-running zone operations.
- `policies`: create, delete, get, list, patch, update.
- `responsePolicies` and `responsePolicyRules`: create, delete, get,
  list, patch, update.
- `projects.get`: project-level Cloud DNS metadata.

Official record-management source:
https://docs.cloud.google.com/dns/docs/records

The most important modeling detail: record changes are not just
single-record CRUD. Google documents `dns.changes.create` as the update
path for a `ResourceRecordSet` collection, alongside direct
`resourceRecordSets` methods. `cloud` should model this as a desired
zone mutation with additions and deletions, not as a blind "set record"
verb only.

Official auth source:
https://docs.cloud.google.com/dns/docs/authentication

Authentication is realistic through Application Default Credentials,
service accounts, service-account impersonation, or REST bearer tokens.
For `cloud`, the daemon should not shell out to `gcloud` as the normal
provider implementation. It should accept a credential reference through
policy state and use a Rust HTTP/client-library path. `gcloud auth
print-access-token` is useful for manual experiments, not the daemon
architecture.

Redirects do not belong to Google Cloud DNS. The Google equivalent lives
in Cloud Load Balancing URL maps, not the DNS API. Official source:
https://cloud.google.com/load-balancing/docs/url-map-concepts

That makes Google redirects a later provider family, separate from
`GoogleCloudDns`.

## Hetzner Cloud and DNS

Official API overview:
https://docs.hetzner.cloud/

Hetzner's current API documentation covers `api.hetzner.cloud` and lists
Cloud Server, Load Balancers, Volumes, Firewalls, Networks, DNS, Floating
IPs, and Placement Groups as product families. It also points to the
official `hcloud` CLI and Go/Python libraries, so a Rust implementation
should treat the HTTP API as canonical and use official libraries only
as behavior references if needed.

Official API usage source:
https://docs.hetzner.com/cloud/api/getting-started/using-api/

Hetzner uses bearer API tokens, project-scoped tokens, JSON over HTTPS,
and standard HTTP verbs:

- `GET`: read resources, tariffs, locations, and other metadata.
- `POST`: create resources or invoke configuration/actions.
- `PUT`: update existing resources.
- `DELETE`: delete existing resources.

The same source documents label selectors and sorting. `cloud` should
carry label-selector support early for inventory queries, because labels
are a natural bridge between provider resources and higher-level CriomOS
roles.

Official Hetzner API overview product families:
https://docs.hetzner.cloud/

Concrete Hetzner operation families that belong in the eventual provider
tree:

- server inventory and lifecycle: list/get/create/delete servers,
  power actions, rebuild/rescue/snapshot/rebuild-style actions, metadata
  and labels;
- network inventory and lifecycle: list/get/create/delete networks,
  subnets, routes, attach/detach actions;
- firewall inventory and lifecycle: list/get/create/delete firewalls,
  set rules, apply/remove resources, label selector targets;
- load balancer inventory and lifecycle: list/get/create/delete load
  balancers, services, targets, algorithms, certificates, private
  network attachment;
- primary or floating IP inventory and assignment;
- SSH key inventory;
- volume inventory and attachment;
- placement groups;
- DNS zones and record sets.

Hetzner DNS has moved. The old DNS Console API is explicitly deprecated:
https://docs.hetzner.com/dns-console/dns/

The current direction is DNS inside Hetzner Console and Cloud API.
Official release sources:
https://docs.hetzner.cloud/whats-new
https://docs.hetzner.cloud/changelog

The changelog says DNS in Hetzner Console and the DNS API became
generally available, and that creating zones under the old
`dns.hetzner.com` path is no longer possible. `cloud` should therefore
target the current Cloud API DNS endpoints, not the deprecated DNS
Console API.

## Cloudflare anchor

Cloudflare remains the first practical target because the immediate user
need is restoring DNS records and redirects. Official Cloudflare sources:

- DNS record methods:
  https://developers.cloudflare.com/api/resources/dns/subresources/records/
- Single Redirects through the Rulesets API:
  https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-api/

This matters because Cloudflare combines DNS records with edge proxy
state and redirect rules. The `cloud` signal tree should not pretend
that every provider has a uniform "redirect" API under DNS.

## What belongs in cloud now

Implement these first:

- provider identity and account/project references;
- provider capability observation;
- credential reference validation without printing secret material;
- Cloudflare DNS record inventory and mutations;
- Cloudflare redirect-rule inventory and mutations;
- Google Cloud DNS zone and record inventory;
- Google Cloud DNS zone and record mutations, modeled around
  `changes.create` where appropriate;
- Google Cloud DNS permission probing through `testIamPermissions`;
- Hetzner Cloud DNS zone and record inventory/mutations against the
  current Cloud API;
- Hetzner Cloud read-only inventory for servers, networks, firewalls,
  load balancers, IPs, SSH keys, volumes, and placement groups.

This gives `cloud` enough shape to restore domains, audit provider
state, and generate provider plans from higher-level domain intent
without immediately owning destructive infrastructure operations.

## What belongs later

Defer these until the signal/authorization design is stronger:

- Hetzner server create/delete/rebuild/rescue/power actions;
- Hetzner network, firewall, load balancer, IP, and volume mutations;
- Google Cloud Load Balancer URL map redirects;
- Google Compute/network/firewall/server management;
- provider-side import/adoption workflows that reconcile existing
  manually-created resources into Sema state;
- daemon self-upgrade to add a missing provider feature before replying
  unsupported.

The deferral is architectural, not because the APIs are unavailable. The
mutating operations need plan/validate/apply separation, owner or
meta-signal authorization, event history, and dry-run witnesses.

## Feature gating

Build-time gating is realistic:

- Cargo features can compile provider adapters independently:
  `provider-cloudflare`, `provider-google`, `provider-hetzner`.
- Nix packages can build minimal or full provider variants by selecting
  Cargo features.
- The signal contract should include all provider variants that are part
  of the protocol version. A build that lacks a provider returns a typed
  unsupported capability reply; it does not fail to parse the request.

Runtime gating is also necessary:

- Policy state enables provider accounts/projects/zones explicitly.
- Credentials are referenced, not embedded in the signal request.
- A provider can be compiled in but unavailable because no credential or
  account binding is configured.
- Capability observation should report three layers separately:
  compiled capability, configured provider account, and live provider
  authorization.

## Capability discovery

Capability discovery is realistic for the daemon's own build and runtime
state. The daemon can always answer which provider adapters were compiled
in and which provider accounts are configured.

Provider-side discovery is only partly realistic:

- Google Cloud DNS supports direct permission probing through
  `managedZones.testIamPermissions`, so the daemon can ask whether the
  credential appears authorized for specific DNS operations.
- Hetzner's public docs show project-scoped bearer tokens and read/write
  request classes, but do not expose a general "what can this token do?"
  capability endpoint in the cited material. The daemon should infer
  Hetzner authorization through safe read probes and typed error mapping.
- Endpoint-surface discovery should be static, generated from provider
  docs or hand-maintained from official references, not dynamic at
  runtime. Providers do not expose a common machine-readable capability
  contract that matches `cloud`'s semantic operations.

The right signal shape is therefore:

- `Observe(Capabilities)` for daemon/provider/account capability state;
- `Validate(Plan)` for provider-supported dry-run or local validation;
- `Apply(Plan)` for authorized mutations;
- `Observe(ProviderState)` for inventory;
- typed `UnsupportedProvider`, `UnsupportedCapability`, and
  `UnauthorizedCapability` replies.

## Main design consequence

`cloud` should not be "Cloudflare with extra providers." It should be a
provider-orchestration daemon whose stable vocabulary is higher than any
single provider: zones, records, redirects, servers, networks, firewalls,
load balancers, addresses, credentials, plans, capabilities, validation,
and applied changes. Provider adapters translate that vocabulary to
Cloudflare, Google, Hetzner, and later others.

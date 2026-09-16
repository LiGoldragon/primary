# Cloud DNS capability for the XMPP host — read-only investigation

Flow `f55ec8`. Read-only: nothing was edited, nothing sent, no provider was
contacted, no secret value was read or printed. Every claim below is marked
**witnessed** (file:line or command) or **inferred**.

Repository tips observed:

- `cloud` main — `ee4966bc7167579c3cf23a4110f88c9a07042656` (witnessed:
  `git rev-parse upstream/main` in a read-only clone at `/tmp/f55ec8-cloud/cloud`).
- `cloud` proposal — `proposal/cf7879-cloudflare-fixture-nix-check-signed-upstream`
  = `9cb93947e92399e6e03dcf5056947c68830cb032` (witnessed: same command).
- `CriomOS` `origin/proposal/348e7b-prosody-activation` =
  `38c5bd51ea6d47aa25522941d9244873f6803b72` (witnessed:
  `/git/github.com/LiGoldragon/CriomOS/.git/packed-refs:3154`).

---

## 1. What the cloud repository is today

### 1.1 Crates and binaries

**Witnessed** `/git/github.com/LiGoldragon/cloud/Cargo.toml:1-33`. One crate,
`cloud` 0.2.0, edition 2024, three binaries:

| Binary | Path | Role |
| --- | --- | --- |
| `cloud-daemon` | `src/bin/cloud-daemon.rs` | the long-running process |
| `cloud` | `src/bin/cloud.rs` | ordinary-socket CLI |
| `meta-cloud` | `src/bin/meta-cloud.rs` | meta-socket CLI |

Features: `default = ["cloudflare"]`, plus `digitalocean`, `hetzner`,
`google-cloud` (empty), `nota-text` (`Cargo.toml:26-32`).

**Witnessed naming divergence.** The `nexus` skill and `Vision/nexus.md`
require `<nexus>-nexus` and `<nexus>-meta`; this repo ships `cloud-daemon`
and `meta-cloud`, and `ARCHITECTURE.md:39` says "The daemon shell is
truthfully handwritten Rust at the present Protos stage." So a Nexus **does**
exist (two Unix sockets, length-prefixed signal frames, typed replies) — it is
named in the old vocabulary. Renaming is a separate order, not this one; but a
write subflow that adds an operation should not deepen the old naming.

### 1.2 The Nexus, its sockets, and the authority boundary

**Witnessed** `ARCHITECTURE.md:18-42`:

1. `cloud` / `meta-cloud` parse a **Nota** request (not datom — see §1.6).
2. The client archives the contract's `Frame` and sends it length-prefixed
   over a Unix socket.
3. `cloud-daemon` decodes the same `Frame` and passes `ChannelRequest` to
   the shared `Store`.
4. `Store` executes against policy, plans, cached observations, adapters.
5. The daemon returns `ChannelReply` carrying the request's exchange id.

Ordinary socket = observation + validation. Meta socket (mode `0o600`) =
registration, credential rotation, policy, plan prepare/approve/apply,
retirement. One request per connection, 8 MiB body cap, ten-second admission
timeout (`ARCHITECTURE.md:32-37`).

`DaemonConfiguration` is an rkyv binary file argument; inline Dotos and
`.dotos` files are refused (**witnessed** `src/lib.rs:110-129`,
`src/daemon_command.rs:34-42`).

### 1.3 The ethos contracts — queries and responses

Two contract crates, both **handwritten Rust with a tiny sealed Ethos
Interface stage**, not generated wholesale.

`signal-cloud` ordinary contract (**witnessed** `signal-cloud/src/lib.rs:548-562`):

```
channel Cloud { operation Observe(Observation), operation Validate(Validation) }
reply   Reply  { Observed(ObservationResult), Validated(ValidationReport),
                 RequestUnsupported(RequestUnsupported), RequestRejected(RequestRejected) }
```

`Observation` variants: `Capabilities | Zones | Records | Redirects | Servers | Plan`
(`signal-cloud/src/lib.rs:400-407`).

`meta-signal-cloud` meta contract (**witnessed** `meta-signal-cloud/src/lib.rs:~330-360`):

```
channel Meta { RegisterAccount, RotateCredential, SetPolicy, PreparePlan,
               PrepareHostPlan, PrepareHostDestruction, ApprovePlan, ApplyPlan, RetireAccount }
reply  Reply { AccountRegistered, CredentialRotated, PolicySet, PlanPrepared(Plan),
               HostPlanPrepared(HostPlan), PlanApproved, PlanApplied, AccountRetired, RequestRejected }
```

The sealed Ethos files are almost empty. **Witnessed**
`signal-cloud/schema/capability.ethos:1-8` holds only `CapabilityState`,
`CapabilityObservation`, `Provider`, `Capability`, `CapabilityQuery`,
`CapabilityReport`; `meta-signal-cloud/schema/authority.ethos:1-8` holds only
`SshKeyName`, `HostIntent`, `ImageName`, `CredentialHandle`, `RejectionReason`,
`ServerType`, `CapabilityDirective`. Both are `Interface.{1 0 0}` with empty
Input/Output/Refusal roles, and `signal-cloud/ARCHITECTURE.md` (Bootstrap
stage) says plainly that the operations, frame behavior and derives "remain
handwritten Rust … They are not claimed as generated." **Inferred:** a new
operation can be added as handwritten Rust today without an ethos-zero run,
but the honest direction is to grow the `.ethos` file.

### 1.4 The record model, and where it stops

**Witnessed** `signal-cloud/src/lib.rs:308-316`:

```rust
pub struct DomainNameSystemRecord {
    pub name: DomainName,
    pub kind: RecordKind,
    pub value: RecordValue,      // one flat String
    pub proxy_mode: ProxyMode,   // Direct | ProviderProxy
}
```

`RecordKind` has fifteen variants including `Service` (SRV)
(`signal-cloud/src/lib.rs:137-153`). **There is no priority, weight, port,
target or TTL field.** SRV is therefore nameable but not expressible.

`DesiredState.{ provider, zone, records, redirects }`
(`signal-cloud/src/lib.rs:358-366`) and `Plan.{ identifier, provider, zone,
records_to_create, records_to_update, record_names_to_delete, redirects_* }`
(`signal-cloud/src/lib.rs:375-388`).

### 1.5 The Cloudflare trait and its implementations

**Witnessed** `cloud/src/cloudflare.rs:59-81`:

```rust
pub trait Api: Send + Sync {
    fn zones(&self, token: &Token, name: Option<&DomainName>) -> Result<Vec<ApiZone>>;
    fn records(&self, token: &Token, zone: &ZoneIdentifier) -> Result<Vec<ApiRecord>>;
    fn create_record(&self, token, zone, record: &DomainNameSystemRecord) -> Result<ApiRecord>;
    fn update_record(&self, token, zone, identifier: &RecordIdentifier, record) -> Result<ApiRecord>;
    fn delete_record(&self, token, zone, identifier: &RecordIdentifier) -> Result<()>;
}
```

Three implementations:

- `HttpApi` — real Cloudflare v4 REST (`cloudflare.rs:112-281`). Paths
  `GET /zones?name=`, `GET/POST /zones/{id}/dns_records`,
  `PATCH|DELETE /zones/{id}/dns_records/{rid}`. Bearer auth
  (`cloudflare.rs:139`). Envelope `{success, result, errors}` decoded at
  `cloudflare.rs:435-456`.
- `FlarectlApi` — the **production default** (`cloudflare.rs:290-295` →
  `cloudflare_cli.rs`). Shells `flarectl --json` with
  `.env("CF_API_TOKEN", token)` (`cloudflare_cli.rs:18, 47-50`).
- `ReadOnlyFixtureApi` — proposal branch only (`src/cloudflare_fixture.rs:46-106`),
  snapshot reads, every write returns `RequestRejected("… read-only")`.

`ProviderClient::apply_plan` (`cloudflare.rs:360-378`) deletes named records
first, then upserts creates and updates. `upsert_record`
(`cloudflare.rs:396-422`) matches an existing record by **(name, kind) only** —
so two records of the same name and kind (two SRV rows, or a round-robin A
pair) collide.

**The write payload is the sharpest limit. Witnessed**
`cloudflare.rs:496-516`:

```rust
struct RecordPayload { kind: &'static str, name: String, content: String, ttl: u32, proxied: bool }
// ttl: 1  (Cloudflare "automatic"), proxied = (record.proxy_mode == ProviderProxy)
```

No `priority`, no `data` object, TTL hard-wired to `1`. The flarectl path is
the same: `record_arguments` emits only `--zone --name --type --content` and
optionally `--proxy` (`cloudflare_cli.rs:111-126`). **Inferred:** creating an
SRV record through either adapter today would send an SRV with no priority /
weight / port / target structure and would be rejected or silently wrong.

### 1.6 How the token enters — exactly

Two distinct mechanisms, and they do not meet.

**(a) The daemon's credential handle.** `CredentialHandle` is a plain String
(`meta-signal-cloud/src/lib.rs`, `CredentialHandle::new`). The daemon resolves
it through `EnvironmentCredentialSource`, which reads **the process
environment variable whose name is the handle text** (**witnessed**
`cloudflare.rs:48-57`):

```rust
std::env::var(handle.as_str()).map(Token::new)
    .map_err(|_| Error::CredentialUnavailable(handle.as_str().to_owned()))
```

Tests register the handle `"CLOUDFLARE_DNS_TOKEN"`
(`cloud/tests/runtime.rs:544`); the shipped nota example registers
`cloudflare-dns-token` (`meta-signal-cloud/examples/register-account.nota:1`).
`RegisterAccount` calls `verify_credential` and refuses if the variable is
absent (`cloud/src/lib.rs:1169`).

**(b) The Nix flake's gopass wrapper.** **Witnessed** `cloud/flake.nix:36-46`:

```nix
cloudflareCli = pkgs.symlinkJoin {
  name = "flarectl-gopass-wrapped";
  paths = [ pkgs.flarectl ];
  postBuild = ''
    wrapProgram $out/bin/flarectl \
      --run 'CF_API_TOKEN=$(${pkgs.gopass}/bin/gopass show -o cloudflare/api-token) || { echo "cloud: cannot fetch CF_API_TOKEN from gopass cloudflare/api-token" >&2; exit 78; }; export CF_API_TOKEN'
  '';
};
```

Three defects follow, each **witnessed**:

1. **The gopass path is wrong.** `gopass ls --flat | grep -i cloudflare` (run,
   names only, no values) returns exactly `cloudflare.com/api-token` and
   `cloudflare.com/token`. There is **no** `cloudflare/api-token` entry. The
   wrapper as written exits 78 on every invocation. Compare DigitalOcean,
   whose flake path `digitalocean.com/api-token` (`flake.nix:68`) **does**
   exist. (`hetzner/api-token`, `flake.nix:57`, also does not exist.)
2. **The daemon package never injects `CF_API_TOKEN`.** `postInstall`
   (`flake.nix:94-99`) wraps `cloud-daemon` with `HCLOUD_TOKEN` and
   `DIGITALOCEAN_ACCESS_TOKEN` from gopass only. So the packaged daemon cannot
   satisfy `EnvironmentCredentialSource` for Cloudflare at all — a Cloudflare
   `RegisterAccount` is refused unless the operator exports the variable by
   hand.
3. **The wrapper overrides whatever the daemon passes.** `FlarectlApi` sets
   `CF_API_TOKEN` on the child (`cloudflare_cli.rs:50`); the wrapper's `--run`
   then unconditionally reassigns it. The handle mechanism is decorative on
   the production path.

**Deviation from the `secrets` skill.** That skill forbids command
substitution, argv and environment for secret transport. The wrapper uses
command substitution into an exported environment variable, and the whole
Cloudflare path carries the token in `Token(String)` in daemon memory and in a
child process environment. The agent never sees it — which is the order's
requirement — but the transport is weaker than the skill's rule. Worth an
explicit note in whatever lands.

### 1.7 Test shape and Nix checks

`cloud/tests/`: `runtime.rs` (647 lines, in-process `Store` against a fixture
`Api` + fixture `CredentialSource`), `daemon.rs`, `digitalocean.rs`,
`digitalocean_live.rs`, `hetzner.rs`. The worked meta ceremony is
`meta_policy_allows_approved_dns_plan_application`
(**witnessed** `tests/runtime.rs:540-623`): `RegisterAccount` → `SetPolicy`
(with `ZonePolicy.allowed_zones = ["goldragon.criome"]`) → `PreparePlan` →
assert create/update/delete counts → `ApprovePlan` → `ApplyPlan` → assert
`last_known_records`.

Nix checks on main (`flake.nix:118-198`): `build`, `test`, `digitalocean-test`,
`digitalocean-live-test-compiles`, `fmt`, `clippy`, `digitalocean-clippy`.
There is a `apps.digitalocean-live-test` that fetches the DO token from gopass
and runs `--ignored` tests — the existing precedent for a live, human-run
provider test (`flake.nix:100-117`).

### 1.8 The proposal branch delta

`upstream/main...proposal/cf7879-…` is **six commits, 514 insertions, zero
deletions** (**witnessed** `git diff --stat`):

```
 ethos/testing-sandbox-network-proposal.ethos | 138 +
 flake.nix                                    |  29 +
 src/cloudflare_fixture.rs                    | 106 +
 src/lib.rs                                   |   4 +
 src/messaging_dns.rs                         |  79 +
 tests/cloudflare_fixture.rs                  | 158 +
```

**What a "scoped DNS plan" is.** `MessagingDomainBinding`
(**witnessed** `src/messaging_dns.rs:17-23`):

```rust
pub struct MessagingDomainBinding {
    pub domain: DomainName,
    pub zone: ZoneIdentifier,
    pub managed_record_names: Vec<DomainName>,   // the explicit scope
    pub desired_records: Vec<DomainNameSystemRecord>,
}
```

`prepare()` (`messaging_dns.rs:46-78`) validates first, then reads, then
diffs **only within the declared names**:

1. every `desired_records[i].name` must appear in `managed_record_names`,
   else `DesiredRecordOutsideManagedScope` — **before any provider access**;
2. `provider.records(credential, zone)` — a read;
3. the observed listing is **filtered** to `managed_record_names`;
4. `RecordPlan::new(filtered_current, desired).into_parts()`.

**What it refuses:** any desired record outside the declared scope
(`messaging_dns.rs:51-59`), and it refuses to write at all — the module has no
apply path by construction (`messaging_dns.rs:1-6`), and the fixture rejects
every mutation, so a passing test is itself the evidence of read-onlyness
(`tests/cloudflare_fixture.rs:126-128`).

**Why the scope matters — witnessed.** `PreparePlan` today takes a whole-zone
`DesiredState` and `RecordPlan::into_parts` puts **every current record not in
`desired`** into `record_names_to_delete` (`cloud/src/lib.rs:283-294`). Passing
only the four XMPP records as the desired state of zone `criome.net` would
plan the deletion of every other record in `criome.net`. The scoped binding is
the fix; it is a library type and reaches no wire operation.

Three new Nix checks were added (`flake.nix` delta): `cloudflare-fixture`,
`cloudflare-messaging-domain-fixture`,
`cloudflare-messaging-domain-scope-refusal`.

---

## 2. What is missing for the first order

### 2.1 There is no typed operation for it

**Witnessed:** neither channel has a scoped-DNS operation
(`signal-cloud/src/lib.rs:548-559`, `meta-signal-cloud/src/lib.rs:~330-350`).
`MessagingDomainBinding` is a Rust type in the runtime crate only
(`messaging_dns.rs`), reachable by no client.

The closest fit to the existing contract is **not** a new `Apply` root but a
scoped sibling of `PreparePlan` on the meta channel, keeping `ApprovePlan` /
`ApplyPlan` untouched. `Vision/nexus.md` ("Processing is for the effect … The
name is open, Apply liked") licenses `Apply` as the verb; the meta contract's
existing ceremony already spells the apply step `ApplyPlan`. The concrete
proposal is in §5.

### 2.2 The per-cluster domain — where it lives, and where the truth is broken

Four places carry domain material. Only one of them should.

| Place | Content | Witness |
| --- | --- | --- |
| Horizon ethos | `DomainDefinition.{ DomainName DomainProvider }`, `Domains.Vector<DomainDefinition>`, `DomainProvider.[ Cloudflare ]`, `DomainConfiguration.{ String Vector<DomainName> }` | `horizon-rs/lib/ethos/horizon.ethos:45,80,81,86` |
| Authored pan-horizon config | `(DomainSuffixes [criome] [criome.net])` | `criomos-horizon-config/horizon.dotos:6` |
| Cluster proposal | `… {criome [goldragon.criome.net]}` — the trailing `DomainConfiguration`; the `Domains` vector itself is **empty** | `goldragon/proposal.datom:1` (tail) |
| Horizon projection | `internalSuffix` / `publicClusterDomains` | `CriomOS/fixtures/horizon-projection.json:91-94`; `CriomOS/checks/resolver-role-policy/default.nix:107-109` shows `publicClusterDomains = [ "goldragon.criome.net" ]` |

The Rust projection derives the public domain: `domain_configuration.string`
is the internal suffix and `domain_name_vector.first()` the public domain,
defaulting to `format!("{}.criome.net", cluster_name)` (**witnessed**
`horizon-rs/lib/src/projection/composition.rs:102-113`).

**The break.** The Prosody consumer hard-codes both names instead of deriving
them (**witnessed** `CriomOS` `38c5bd5:modules/nixos/prometheus-service-provider-consumer.nix:13-15,29-35`):

```nix
isPrometheusTarget = (horizon.cluster or null) == "goldragon"
                  && (horizon.node.name or null) == "prometheus";
criomos.prometheusServiceProvider = {
  enable = true;
  xmppDomain        = "xmpp.goldragon.criome.net";
  xmppDomainAliases = [ "xmpp.goldragon.criome" ];
  forgejo.enable = false;
  tls.generateSelfSigned = true;
};
```

A fork of this cluster gets `goldragon.criome.net` unless it edits Nix. The
provider module itself is generic — `xmppDomain` is `types.str`, default `""`,
required by assertion; `xmppDomainAliases` is `listOf str` and is documented
as **certificate SAN names only, creating no additional virtual hosts**
(**witnessed** `38c5bd5:modules/nixos/prometheus-service-provider.nix:61-71,
135-145, 250-259`).

**Recommendation — one source of truth.** Horizon's
`DomainConfiguration` is already the per-cluster domain and already reaches
NixOS modules as `horizon.cluster.domainConfiguration.{internalSuffix,
publicClusterDomains}` (**witnessed** `CriomOS/modules/nixos/network/dnsmasq.nix:35`).
Both the Prosody module and the DNS plan should read from it:

- internal name  = `xmpp.<cluster>.<internalSuffix>` → `xmpp.goldragon.criome`
- public FQDN    = `xmpp.<publicClusterDomains[0]>`  → `xmpp.goldragon.criome.net`
- Cloudflare zone = the registrable suffix of that public domain → `criome.net`

Horizon's `Domains.Vector<DomainDefinition{ DomainName DomainProvider }>`
with `DomainProvider.[ Cloudflare ]` is exactly the slot that says which
provider owns which zone; today it is **empty** in `proposal.datom`. Filling it
(`{ criome.net Cloudflare }`) is the smallest honest change that makes the zone
and its provider declarative and forkable. The cloud Nexus should receive the
zone as data on the wire, never infer it.

`signal-cloud/ARCHITECTURE.md` (Does Not Own) says the Criome domain registry
"belongs to `domain-criome`" — but **witnessed** `/git/github.com/LiGoldragon/domain-criome`
contains only `AGENTS.md` with a Protos estate stanza. That repo is a stub;
Horizon is the real registry today.

### 2.3 Internal names: what serves `.criome` today

Two mechanisms, both generated from the Horizon projection, neither a DNS
server for the XMPP name.

**(a) `/etc/hosts` on every node.** `mkCriomeHostEntries` maps each node's
Yggdrasil address (preferred) or `nodeIp` to `criomeDomainName`, plus
`wg.<criomeDomainName>` and any nix-cache alias (**witnessed**
`CriomOS/modules/nixos/network/default.nix:26-61`, consumed at
`network/default.nix:89`). Live confirmation on this machine (`ouranos`):

```
$ getent hosts prometheus.goldragon.criome
200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f prometheus.goldragon.criome nix.prometheus.goldragon.criome
$ grep -i criome /etc/hosts
200:17f7:… zeus.goldragon.criome
200:ca41:… prometheus.goldragon.criome nix.prometheus.goldragon.criome
201:6de1:… ouranos.goldragon.criome
5::5  wg.prometheus.goldragon.criome
```

**(b) dnsmasq on router nodes only.** `lib.mkIf behavesAs.router`; it disables
`resolved` and `unbound`, listens on `::1`, `127.0.0.1` and the LAN gateway
only, and publishes `/<criomeDomainName>/<yggAddress>` **and**
`/<node>.<publicClusterDomain>/<yggAddress>` (**witnessed**
`CriomOS/modules/nixos/network/dnsmasq.nix:26-35, 90-105, 111-118, 127-146`).

Two consequences, both important:

- The cluster runs **split-horizon DNS for the public zone**: on the LAN,
  `prometheus.goldragon.criome.net` resolves to the Yggdrasil overlay address.
  Cloudflare answers the same name for everyone else. Whatever is put in
  Cloudflare must be reconciled against that, or LAN and world will disagree.
- Neither mechanism knows the name `xmpp.goldragon.criome`. Both are keyed on
  **node names**, not service names. `xmpp.goldragon.criome` — declared as a
  certificate alias at `prometheus-service-provider-consumer.nix:32` —
  **resolves nowhere today** (inferred from (a) and (b); it is not a node
  name and appears in no hosts or dnsmasq record).

So the first order has an internal half as well as a Cloudflare half, and the
internal half is a CriomOS change (a service-alias record in
`network/default.nix` and `network/dnsmasq.nix`), not a cloud-Nexus change.

### 2.4 The record model cannot express what Prosody needs

Recapping §1.4 and §1.5 as a gap list:

- **SRV is unexpressible.** No priority/weight/port/target
  (`signal-cloud/src/lib.rs:308-316`); the Cloudflare payload has no
  `priority` and no `data` object (`cloudflare.rs:496-516`); flarectl gets no
  such flags (`cloudflare_cli.rs:111-126`).
- **TTL is not settable** — hard-wired `ttl: 1` (`cloudflare.rs:512`).
- **Record identity is (name, kind)** in both the plan diff
  (`cloud/src/lib.rs:303-305`) and the upsert (`cloudflare.rs:404-406`), so
  same-name-same-kind multiples are not representable.
- **`record_names_to_delete` is by name, not by record**
  (`signal-cloud/src/lib.rs:384`), so an apply deletes *every* record of that
  name (`cloudflare.rs:380-394`) — dangerous inside a shared zone.

---

## 3. The smallest reliable proof-of-concept path

### 3.1 The blocking fact: there is no public address

**Witnessed.** Prometheus is `Metal`, a `GMKtec EVO-X2` home box with the
`LargeAiRouter` variant and `RouterInterfaces` (`goldragon/proposal.datom:1`,
prometheus entry). Its only declared addresses are Yggdrasil
`200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f` / subnet `300:ca41:6b12:fba` and
`nodeIp Some."5::5/128"` (same line). Horizon's ethos has **no** public-address
type at all — `NodeNetwork.{ Vector<LinkLocalIp> Option<NodeIp>
Option<WireguardPubKey> Vector<WireguardProxy> Option<RouterInterfaces> }`
(`horizon-rs/lib/ethos/horizon.ethos:67`), and `FixedLocation.{ Decimal Decimal
Decimal Decimal }` (`horizon.ethos:57`) is a geographic coordinate, not an
address (confirmed by its Rust projection `latitude/longitude/altitude/accuracy`).
Live corroboration from a cluster peer: this machine (`ouranos`) has only
`192.168.1.5/24` and `10.18.0.102/24` as global IPv4 and one Yggdrasil
`201:…/7` as global IPv6 — residential LAN behind NAT.

**`0200::/7` is the Yggdrasil overlay range and is not routable on the public
internet.** So an `A`/`AAAA` for `xmpp.goldragon.criome.net` has, today,
**nothing true to point at**. This is the largest gap in the first order and it
is not a cloud-repo gap.

Three ways out, none chosen by any record I found:

1. **Host Prosody on a cloud VPS.** `cloud` already has Hetzner and
   DigitalOcean host adapters with `PrepareHostPlan` / `ApplyPlan`
   (`meta-signal-cloud` channel; `cloud/src/hetzner.rs`,
   `cloud/src/digitalocean.rs`) and the DO path already has a live test app.
   The DNS record then points at a real, stable, declarable address.
2. **Publish the residential egress address and keep it fresh.** This is
   dynamic-DNS; it makes the cloud Nexus's DNS-update capability the load-
   bearing piece, and needs an observed-address source plus a refresh loop.
   It also exposes a home IP.
3. **A tunnel.** Cloudflare's free tunnel carries HTTP(S); arbitrary TCP such
   as XMPP 5222 needs `cloudflared access` on every client, and Spectrum is
   enterprise. **Inferred:** not viable for a standards-conformant XMPP host.

Recommendation: settle this before any record is written. Option 1 is the only
one that makes the DNS records honest and uses capability the repo already has.

### 3.2 The records, once an endpoint exists

Prosody, as the branch configures it, opens **only TCP 5222**
(`38c5bd5:modules/nixos/prometheus-service-provider.nix:284`, with the comment
at 281-283 saying exactly that). No 5269 (s2s), no 5223 (direct TLS). The
virtual host is the single name `cfg.xmppDomain` (`:250-259`). No SRV records
are named anywhere on that branch.

So the minimal true set for `xmpp.goldragon.criome.net` in zone `criome.net`:

| Name | Type | Value | Proxy |
| --- | --- | --- | --- |
| `xmpp.goldragon.criome.net` | `A` | the chosen public IPv4 | **off** |
| `xmpp.goldragon.criome.net` | `AAAA` | the chosen public IPv6 (if any) | **off** |
| `_xmpp-client._tcp.xmpp.goldragon.criome.net` | `SRV` | `10 5 5222 xmpp.goldragon.criome.net` | n/a |

`_xmpps-client._tcp` (XEP-0368 direct TLS, port 5223) **must not be created**:
nothing listens on 5223 and the firewall does not open it
(`prometheus-service-provider.nix:284`). Creating it would advertise a dead
endpoint. `_xmpp-server._tcp` likewise waits for 5269.

`_xmpp-client._tcp` is strictly optional when the A record already carries the
host and clients use the default 5222 — **inferred**, standard XMPP client
behavior. Keeping it in the set is still right: it is the one record that makes
the SRV gap of §2.4 concrete and forces the contract to grow properly.

Internal half (CriomOS, not cloud): `xmpp.goldragon.criome` → prometheus's
Yggdrasil address, as a hosts entry and a dnsmasq address record.

### 3.3 Cloudflare proxying must be off — the API field

**It must be off.** The Cloudflare proxy terminates HTTP and HTTPS only; a
proxied `A`/`AAAA` resolves to Cloudflare edge addresses that do not forward
TCP 5222, so XMPP would break outright (**inferred**, Cloudflare proxy
semantics). SRV records cannot be proxied at all.

The API field is **`proxied`**, a boolean in the DNS-record body. In this
codebase it is set from the contract's `ProxyMode`
(**witnessed** `cloudflare.rs:504, 513`):

```rust
struct RecordPayload { …, proxied: bool }
proxied: record.proxy_mode == ProxyMode::ProviderProxy,
```

so the contract value is `ProxyMode::Direct` for every XMPP record. On the
flarectl path the corresponding switch is `--proxy`, emitted only for
`ProviderProxy` (`cloudflare_cli.rs:122-124`) — i.e. simply not passed.

**A guard is owed.** The plan should refuse `ProviderProxy` for any record in
a messaging binding, rather than relying on the caller. That refusal belongs
in the contract's rejection vocabulary (§5).

### 3.4 Plan-then-apply shape

The existing ceremony is already plan-then-apply and needs no invention, only
scoping:

1. `RegisterAccount { Cloudflare, <account>, <credential handle> }` —
   verified against the environment (`cloud/src/lib.rs:1169`).
2. `SetPolicy { zones: [{ Cloudflare, <account>, allowed_zones: ["criome.net"] }],
   capabilities: [{ …, DomainNameSystemRecords, Enable }] }` — the zone
   allow-list is enforced at `cloud/src/lib.rs:876-882`.
3. **`PrepareScopedDnsPlan`** (new, §5) → `ScopedDnsPlanPrepared` — a read
   plus a diff restricted to the declared record names. **This is the dry
   run**; it writes nothing (proved by the read-only fixture).
4. `ApprovePlan { plan }` — owner records approval.
5. `ApplyPlan { plan }` — the only writer; refuses an unapproved or unknown
   plan (`ARCHITECTURE.md:51-56`).

The plan returned in step 3 is the artifact a human reads before step 4. The
secondary performs steps 4-5 against the live zone; this flow and any write
subflow stop at step 3 against a fixture.

### 3.5 The test

Follow the pattern the proposal branch already established, with real payload
material:

- A **real Cloudflare fixture payload file** — a captured
  `GET /zones/{id}/dns_records` response for `criome.net`, checked in under
  `tests/fixtures/`, with any unrelated record kept verbatim (it is public DNS
  data; it contains no secret). The existing fixture is built from inline Rust
  literals (`tests/cloudflare_fixture.rs:15-29`); a file makes the expected
  plan falsifiable against the zone as it really is. Decoding it exercises
  `RecordRecord`/`ApiRecord::try_from` (`cloudflare.rs:480-534`) — the same
  code the live path uses.
- **Plan computed and compared**: `MessagingDnsBinding::prepare` over that
  fixture, asserting the exact `records_to_create` / `records_to_update` /
  `record_names_to_delete`, and asserting `record_names_to_delete` is **empty** —
  a scoped plan for a fresh service must delete nothing.
- **Refusal tests**: a record outside the declared scope; a record with
  `ProviderProxy`; an SRV whose port does not match an open listener (if that
  check lands).
- **Read-onlyness is structural**, not asserted: `ReadOnlyFixtureApi` fails
  every write, so a green test is the proof (`tests/cloudflare_fixture.rs:126-128`).
- **Nix checks** in the pattern of the three the proposal branch added
  (`cloudflare-fixture`, `cloudflare-messaging-domain-fixture`,
  `cloudflare-messaging-domain-scope-refusal`).
- **Live apply only by the secondary**, in the shape of
  `apps.digitalocean-live-test` (`flake.nix:100-117`): a `#[ignore]`d test
  behind a Nix app that pulls the token from gopass at run time and is started
  by a human.

---

## 4. Cloudflare token capabilities

### 4.1 What the plan needs

Derived from the API calls the code makes (**witnessed** `cloudflare.rs:226-280`):

| Call | Cloudflare permission |
| --- | --- |
| `GET /zones?name=criome.net` (`:230`) | **Zone → Zone → Read** |
| `GET /zones/{id}/dns_records` (`:235`) | **Zone → DNS → Read** (implied by Edit) |
| `POST /zones/{id}/dns_records` (`:246`) | **Zone → DNS → Edit** |
| `PATCH /zones/{id}/dns_records/{rid}` (`:258`) | **Zone → DNS → Edit** |
| `DELETE /zones/{id}/dns_records/{rid}` (`:274`) | **Zone → DNS → Edit** |

So: **Zone:DNS:Edit** plus **Zone:Zone:Read**, with **Zone Resources scoped to
`criome.net` alone** — `Include → Specific zone → criome.net`, never "All
zones" and never an account-level token. **Inferred:** the zone lookup is by
name, so a zone-scoped token that lists only `criome.net` is sufficient;
`ProviderClient::zones` with an empty name list would then simply return that
one zone (`cloudflare.rs:320-327`). No Page Rules, Rulesets, Account, User,
SSL or Workers scope is needed — redirects are explicitly not implemented
(`README.md:21-22`, `ARCHITECTURE.md:73-75`).

Two further hardenings worth requesting, **inferred**: a Client IP Address
Filter on the token if the Nexus has a stable egress, and a TTL/expiry with a
rotation plan (`RotateCredential` already exists on the meta channel).

### 4.2 Is the existing gopass entry scoped so? Unknown — and the path is wrong

I did not and cannot read the token. What can be said:

- **The entry the flake names does not exist.** `gopass ls --flat` (names
  only) shows `cloudflare.com/api-token` and `cloudflare.com/token`; the flake
  asks for `cloudflare/api-token` (`flake.nix:41`). **Witnessed.**
- **No scope note exists anywhere in `cloud`.** `grep -rn
  "Zone:DNS|scope|Scope|api-token|permission"` over `README.md`,
  `ARCHITECTURE.md`, `AGENTS.md` and `docs/` returns exactly two lines, both
  merely restating the gopass path (`README.md:15`,
  `docs/first-cloudflare-slice.md:30`). Nothing states what the token may do.
  **Witnessed.**
- **Two entries, and nothing says which is which.** `cloudflare.com/api-token`
  vs `cloudflare.com/token` — whether either is zone-scoped to `criome.net`,
  and whether one is a legacy Global API Key, is **unknown**. A Global API Key
  would be a serious over-grant for this order.

**Owed to the psyche, not to an agent:** confirm in the Cloudflare dashboard
that the token behind `cloudflare.com/api-token` is a *scoped API token* with
Zone:DNS:Edit + Zone:Zone:Read on `criome.net` only; if not, mint one, and say
in `cloud`'s README which entry holds it and what it may do.

---

## 5. Proposed contract

Written in the Ethos **Signal** root, sweet form (`ethos` skill: imports,
queries, responses, types). It belongs in `meta-signal-cloud/schema/authority.ethos`
— these operations mutate provider state, and `signal-cloud/ARCHITECTURE.md`
puts every Mutate-class verb on the meta contract.

```
Signal
[ signal_cloud:[ Provider ProviderAccount PlanIdentifier ]
  meta_signal_cloud:CredentialHandle ]

[ PrepareScopedDnsPlan.ScopedDnsPlanPreparation
  ApproveScopedDnsPlan.PlanIdentifier
  ApplyScopedDnsPlan.PlanIdentifier ]

[ ScopedDnsPlanPrepared.ScopedDnsPlan
  ScopedDnsPlanApproved.PlanIdentifier
  ScopedDnsPlanApplied.AppliedDnsRecords
  ScopedDnsPlanRefused.ScopedDnsRefusal ]

[ ClusterName.String
  PublicZoneName.String
  ServiceDomainName.String
  RecordName.String
  RecordTarget.String
  IpV4Address.String
  IpV6Address.String
  TextValue.String
  Priority.Integer
  Weight.Integer
  Port.Integer
  Seconds.Integer
  ProviderMessage.String
  ProxyMode.[ Direct ProviderProxy ]
  TimeToLive.[ ProviderAutomatic Fixed.Seconds ]
  ServiceRecord.{ Priority Weight Port RecordTarget }
  RecordData.[ AddressV4.IpV4Address
               AddressV6.IpV6Address
               CanonicalName.RecordTarget
               Text.TextValue
               Service.ServiceRecord ]
  DnsRecord.{ RecordName RecordData ProxyMode TimeToLive }
  ManagedRecordNames.Vector<RecordName>
  DesiredDnsRecords.Vector<DnsRecord>
  DnsRecordsToCreate.Vector<DnsRecord>
  DnsRecordsToUpdate.Vector<DnsRecord>
  RecordNamesToDelete.Vector<RecordName>
  AppliedDnsRecords.Vector<DnsRecord>
  MessagingDnsBinding.{ ClusterName ServiceDomainName PublicZoneName ManagedRecordNames DesiredDnsRecords }
  ScopedDnsPlanPreparation.{ Provider ProviderAccount MessagingDnsBinding }
  ScopedDnsPlan.{ PlanIdentifier PublicZoneName DnsRecordsToCreate DnsRecordsToUpdate RecordNamesToDelete }
  ScopedDnsRefusal.[ RecordOutsideManagedScope.RecordName
                     ProxyForbiddenForRecord.RecordName
                     ZoneNotPermitted.PublicZoneName
                     ZoneUnknown.PublicZoneName
                     CredentialHandleUnknown.CredentialHandle
                     PlanUnknown.PlanIdentifier
                     PlanNotApproved.PlanIdentifier
                     ProviderRejected.ProviderMessage ] ]
```

Why this shape:

- `MessagingDnsBinding` is `messaging_dns.rs`'s `MessagingDomainBinding`
  promoted to the wire, with `ZoneIdentifier` (a Cloudflare-internal id)
  replaced by `PublicZoneName` — the caller names `criome.net`, the Nexus
  resolves the id, so nothing provider-specific crosses the wire.
- `ClusterName` and `ServiceDomainName` make the per-cluster domain **data on
  the wire**, fed from Horizon (§2.2). A fork sends its own; nothing is
  compiled in.
- `RecordData` replaces the flat `(RecordKind, RecordValue)` pair, so SRV
  carries its four numbers and the type system, not a string, is the check.
  `TimeToLive` replaces the hard-wired `ttl: 1`.
- `ProxyForbiddenForRecord` makes §3.3's rule a typed refusal rather than a
  convention.
- Refusals are a closed enum: errors are vocabulary, per the `nexus` skill.
- `ApproveScopedDnsPlan` / `ApplyScopedDnsPlan` mirror the existing
  `ApprovePlan` / `ApplyPlan` and may simply route to them if the runtime
  keeps one plan store.

### Worked datom, one per operation

Per the `datom` skill: positional, no field names, heads capitalized,
guillemets only where a string holds a space.

**`PrepareScopedDnsPlan`**

```
PrepareScopedDnsPlan.{ Cloudflare primary { goldragon xmpp.goldragon.criome.net criome.net [ xmpp.goldragon.criome.net _xmpp-client._tcp.xmpp.goldragon.criome.net ] [ { xmpp.goldragon.criome.net AddressV4.203.0.113.8 Direct ProviderAutomatic } { xmpp.goldragon.criome.net AddressV6.2001:db8::8 Direct ProviderAutomatic } { _xmpp-client._tcp.xmpp.goldragon.criome.net Service.{ 10 5 5222 xmpp.goldragon.criome.net } Direct ProviderAutomatic } ] } }
```

reply, on a zone where none of the three exist yet:

```
ScopedDnsPlanPrepared.{ xmpp.goldragon.criome.net-cloudflare-scoped-plan criome.net [ { xmpp.goldragon.criome.net AddressV4.203.0.113.8 Direct ProviderAutomatic } { xmpp.goldragon.criome.net AddressV6.2001:db8::8 Direct ProviderAutomatic } { _xmpp-client._tcp.xmpp.goldragon.criome.net Service.{ 10 5 5222 xmpp.goldragon.criome.net } Direct ProviderAutomatic } ] [] [] }
```

**`ApproveScopedDnsPlan`**

```
ApproveScopedDnsPlan.xmpp.goldragon.criome.net-cloudflare-scoped-plan
ScopedDnsPlanApproved.xmpp.goldragon.criome.net-cloudflare-scoped-plan
```

**`ApplyScopedDnsPlan`**

```
ApplyScopedDnsPlan.xmpp.goldragon.criome.net-cloudflare-scoped-plan
ScopedDnsPlanApplied.[ { xmpp.goldragon.criome.net AddressV4.203.0.113.8 Direct ProviderAutomatic } { xmpp.goldragon.criome.net AddressV6.2001:db8::8 Direct ProviderAutomatic } { _xmpp-client._tcp.xmpp.goldragon.criome.net Service.{ 10 5 5222 xmpp.goldragon.criome.net } Direct ProviderAutomatic } ]
```

**Refusals**

```
ScopedDnsPlanRefused.RecordOutsideManagedScope.www.criome.net
ScopedDnsPlanRefused.ProxyForbiddenForRecord.xmpp.goldragon.criome.net
ScopedDnsPlanRefused.ZoneNotPermitted.example.net
```

The addresses above are documentation ranges (RFC 5737 / RFC 3849) standing in
for whatever §3.1 settles.

---

## 6. Proposed step list for a write subflow

Ordered so each step is provable before the next, and so nothing writes to
Cloudflare inside any agent flow.

**Before any code — one decision the psyche owes (§3.1):** where the XMPP host
gets a public address. Everything downstream is shaped by it. A write subflow
should not start without it.

1. **Fix the gopass path and the daemon's Cloudflare credential.** In
   `cloud/flake.nix`: correct `cloudflare/api-token` → `cloudflare.com/api-token`
   (`flake.nix:41`) and add a `CF_API_TOKEN` line to the `cloud-daemon`
   `postInstall` alongside the Hetzner and DigitalOcean ones
   (`flake.nix:94-99`). Note in `README.md` which gopass entry holds the token
   and what scope it must have (§4.1). Proof: the wrapper no longer exits 78;
   nothing prints a value.
2. **Land the proposal branch's read-only floor first.** Merge
   `proposal/cf7879-cloudflare-fixture-nix-check-signed-upstream` (fixture
   adapter, `messaging_dns.rs`, three Nix checks). It is additive — 514
   insertions, zero deletions — and is the substrate for everything below.
3. **Grow the record model in `signal-cloud`**: `RecordData` with
   `Service.{ Priority Weight Port RecordTarget }`, and `TimeToLive`. Update
   `RecordPayload` to emit Cloudflare's `data` object for SRV and a real
   `ttl`, and `FlarectlApi::record_arguments` correspondingly
   (`cloudflare.rs:496-516`, `cloudflare_cli.rs:111-126`). Proof: round-trip
   tests per record kind — the `nexus` skill's rule that every record kind
   gets a concrete text example with a round-trip test before its type is
   final.
4. **Add the contract of §5** to `meta-signal-cloud`, growing
   `schema/authority.ethos` rather than only the handwritten Rust, and bump
   that crate's semver (its version is the wire's version).
5. **Wire the operation in `cloud`**: route `PrepareScopedDnsPlan` to
   `MessagingDnsBinding::prepare`, enforce the zone allow-list
   (`cloud/src/lib.rs:876-882`) and the `ProxyForbiddenForRecord` guard, and
   route approve/apply to the existing plan store. Fix
   `record_names_to_delete` to be record-scoped, or keep it name-scoped and
   document that the scope filter is what makes it safe.
6. **Real fixture test** (§3.5): a checked-in `criome.net` record payload,
   the expected plan, an empty deletion set, and the refusal cases. Add the
   Nix checks.
7. **Make the domain declarative** — the forkability requirement. Fill
   Horizon's `Domains` with `{ criome.net Cloudflare }`
   (`goldragon/proposal.datom`), and change
   `prometheus-service-provider-consumer.nix:29-35` to derive `xmppDomain` and
   `xmppDomainAliases` from `horizon.cluster.domainConfiguration` instead of
   the two hard-coded literals. Proof: the existing policy check
   (`checks/prometheus-service-provider-consumer-policy/`) still asserts the
   same two strings, now derived.
8. **Serve the internal name** (§2.3): add `xmpp.<cluster>.<internalSuffix>` as
   a service alias in `CriomOS/modules/nixos/network/default.nix` and
   `network/dnsmasq.nix`, pointing at the host that runs Prosody. Without this
   the certificate alias at `…consumer.nix:32` names something unresolvable.
9. **Hand the tested version to the secondary** for the live apply: a
   `#[ignore]`d live test plus a Nix app in the shape of
   `apps.digitalocean-live-test` (`flake.nix:100-117`), started by a human,
   token from gopass at run time, never in an agent's context.
10. **TLS after DNS**, as the order says. The branch generates self-signed
    certificates weekly today
    (`prometheus-service-provider.nix:196-221`); a real certificate is a
    separate order and depends on these records existing.

A note for whoever writes: steps 3-6 are one coherent change to the contract
and its runtime and should be one branch. Steps 7-8 are CriomOS and can run in
parallel. Step 1 is a two-line fix that unblocks any live use and could go
first on its own.

---

## 7. The three biggest unknowns

1. **There is no public address for the XMPP host, and no record says there
   should be one.** §3.1. Until it is settled the `A`/`AAAA` records have no
   true value. Not a cloud-repo problem.
2. **The Cloudflare token's actual scope is unknown**, and the path the flake
   uses does not exist. §4.2. Two candidate gopass entries, no note anywhere
   saying what either may do.
3. **Split-horizon.** The cluster's routers already answer for
   `<node>.goldragon.criome.net` with Yggdrasil addresses
   (`dnsmasq.nix:90-105`). What Cloudflare publishes and what the LAN resolver
   publishes must be reconciled deliberately, or the same name will mean two
   things. No record I found addresses this.

Lesser open questions: whether `_xmpp-client._tcp` should be created at all
while only 5222 is open and the A record suffices; whether the cloud Nexus
should be renamed `cloud-nexus` / `cloud-meta` before it grows an operation;
and whether the domain registry belongs in Horizon or in the stub
`domain-criome` repository, which `signal-cloud/ARCHITECTURE.md` names but
which contains only an `AGENTS.md`.

---

## Sources

Read-only clone of `cloud` at `/tmp/f55ec8-cloud/cloud` (from
`/git/github.com/LiGoldragon/cloud`, upstream branches fetched from
`https://github.com/LiGoldragon/cloud`). All other repositories read in place
under `/git/github.com/LiGoldragon/`. No repository was modified.

- `cloud` @ `ee4966b` — `Cargo.toml`, `flake.nix`, `README.md`,
  `ARCHITECTURE.md`, `AGENTS.md`, `docs/first-cloudflare-slice.md`,
  `src/lib.rs`, `src/cloudflare.rs`, `src/cloudflare_cli.rs`,
  `src/daemon_command.rs`, `src/bin/*.rs`, `tests/runtime.rs`.
- `cloud` @ `9cb9394` (`proposal/cf7879-cloudflare-fixture-nix-check-signed-upstream`)
  — `src/messaging_dns.rs`, `src/cloudflare_fixture.rs`,
  `tests/cloudflare_fixture.rs`, `flake.nix` and `src/lib.rs` deltas.
- `signal-cloud` — `src/lib.rs`, `schema/capability.ethos`, `ARCHITECTURE.md`,
  `AGENTS.md`, `examples/capabilities.nota`.
- `meta-signal-cloud` — `src/lib.rs`, `schema/authority.ethos`,
  `examples/register-account.nota`.
- `CriomOS` @ `38c5bd51ea6d47aa25522941d9244873f6803b72`
  (`origin/proposal/348e7b-prosody-activation`) —
  `modules/nixos/prometheus-service-provider.nix`,
  `modules/nixos/prometheus-service-provider-consumer.nix`,
  `modules/nixos/criomos.nix` delta.
- `CriomOS` working checkout — `modules/nixos/network/default.nix`,
  `modules/nixos/network/dnsmasq.nix`, `fixtures/horizon-projection.json`,
  `checks/resolver-role-policy/default.nix`.
- `horizon-rs` — `lib/ethos/horizon.ethos`, `lib/src/projection/composition.rs`,
  `skills.md`.
- `goldragon` — `proposal.datom`.
- `criomos-horizon-config` — `horizon.dotos`.
- `domain-criome` — `AGENTS.md` (the repository's only file).
- Skills loaded through the Skill tool: `subflow`, `flow-evidence`, `nexus`,
  `ethos`, `datom`, `secrets`.
- `Vision/nexus.md` (primary). `Vision/`, `vision-raw/` and `flows/*/vision/`
  were searched for `cloudflare`, `xmpp`, `prosody`, `dns`, `criome.net`; no
  psyche record on this subject was found.
- Live observations on host `ouranos`: `getent hosts prometheus.goldragon.criome`,
  `grep -i criome /etc/hosts`, `ip -4/-6 addr show scope global`,
  `gopass ls --flat | grep -i cloudflare` (entry **names** only; no value was
  requested, read, or printed).

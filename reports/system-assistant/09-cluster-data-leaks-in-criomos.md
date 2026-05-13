# 09 — Cluster-data leaks in CriomOS: current state and remaining work

Date: 2026-05-13
Role: system-assistant
Frames: user direction this conversation — "There should never be node
        names in CriomOS … CriomOS is just pure Nix interpretation. It
        doesn't hold any [cluster data]"
Reads: `reports/system-specialist/117-system-data-purity-and-wifi-pki.md`,
       `reports/system-specialist/118-criomos-state-and-sandbox-audit.md`,
       `reports/system-assistant/07-criomos-stack-deep-audit.md`,
       `skills/typed-records-over-flags.md`

## The principle

CriomOS reads `horizon.*` (projected cluster facts), `constants.*` (CriomOS
implementation conventions like file paths and protocol port numbers), and
`inputs.*` (flake-input store paths). It does not contain cluster-specific
data — SSIDs, passwords, node lists, cluster names, TLDs, per-host
decisions. It does not gate services on node identity; it gates on
*service offerings* the cluster has declared.

This rule is independent of the cloud-host work. It's how CriomOS should
have always been.

## What was already cleaned up

The version of this report the user reacted to in chat quoted three node-name
gates as live code. They aren't. The system-specialist removed them over the
last two weeks:

| Was | Now | Commit |
|---|---|---|
| `enable = elem node.name [ "ouranos" "prometheus" ]` in `tailscale.nix` | `services.tailscale.enable = mkIf (node.services.tailnet == "Client")` | `9c179ff` |
| `enable = node.name == "ouranos"` + literal `"ouranos.${cluster.name}.criome"` FQDN in `headscale.nix` | `services.headscale.enable = mkIf (node.services.tailnetController == "Server")`, fqdn from `node.criomeDomainName` | `4d6bb24`, `bcd1e9f` |
| `optional (node.name == "prometheus") 11436` in monolithic `nix.nix` | LLM service extracted to `llm.nix`, gated on `behavesAs.largeAi`, port read from criomos-lib data | `2aa6dd1` (split) + earlier extraction |
| Monolithic `nix.nix` mixing client/builder/cache | Split into `nix/{client,builder,cache,retention-agent}.nix`, each gated on its capability flag | `2aa6dd1` |

Confirmed by grep: zero `node.name ==` comparisons in `modules/`, zero
literal `"prometheus"`/`"ouranos"`/`"hyperion"` strings in `modules/`.

The user's diagnostic ("never node names in CriomOS") is **already true
for boolean gating**. The remaining leaks are the same architectural smell
in different syntax.

## What remains

Three categories, ordered by severity.

### A. Production cluster data hardcoded in modules — P0

The worst leak. Cluster policy decisions sitting as string literals inside
Nix modules.

#### A1. Production Wi-Fi network in `router/default.nix:88-99`

```nix
countryCode = "PL";
…
ssid = "criome";
authentication = {
  mode = "wpa3-sae";
  saePasswords = [ { password = "leavesarealsoalive"; } ];
};
```

Four cluster facts in a CriomOS module: regulatory country, SSID,
authentication mode, and an actual password. The password is also a
secret — should not be in source control regardless of which file it's in.

This is documented as the largest remaining violation in
`reports/system-specialist/117-system-data-purity-and-wifi-pki.md` §"P0:
Production Wi-Fi Password In CriomOS". Open beads: `primary-a61` (move
router Wi-Fi policy out), `primary-nvs8` (feed EAP certs into fixtures).

**Decision (2026-05-13, user)**: this network stays in place during
migration. The path forward is **two simultaneous Wi-Fi networks on two
physical interfaces** — the existing built-in radio keeps the WPA3-SAE
network running, a USB Wi-Fi dongle hosts a new EAP-TLS network, clients
migrate one by one, then the old `networks` block is deleted. The leak
gets resolved by **deletion after migration**, not by moving the
hardcoded password out first. Acknowledged transitional debt.

**What the new EAP-TLS network should be**: A typed `WifiNetwork` (or
`cluster.wifi`) record projected from horizon. Designer/139 and
designer-assistant/29 sketch the shape:

```rust
pub struct WifiNetwork {
    pub ssid: WifiSsid,
    pub country: CountryCode,
    pub authentication: WifiAuthentication,
}

pub enum WifiAuthentication {
    Wpa3Sae { password: SecretReference },
    EapTls { profile: WifiCertificateProfile, ... },
}
```

`RouterInterfaces` grows to carry a list of WLAN interfaces (or a second
typed field for the dongle), each carrying its own `WifiNetwork`. The
existing built-in interface's `WifiNetwork` may stay hardcoded in
`router/default.nix` until deletion; the dongle interface's `WifiNetwork`
is horizon-projected from day one. The actual EAP-TLS password / cert
material lives in a sops file (or systemd credential); horizon carries
the `SecretReference` only.

**Dependencies for the EAP-TLS half**: ClaviFaber has the certificate
primitives but not the full Wi-Fi profile — Subject Alternative Name and
Extended Key Usage handling, and a decision on dedicated Wi-Fi keypair
vs reusing the SSH host key (per `reports/system-specialist/117-...`
§"P1: ClaviFaber Has Primitives, Not A Complete Wi-Fi PKI Flow"). The
schema work (horizon dual-WLAN-interface + `WifiNetwork`) can ship before
ClaviFaber lands; the EAP-TLS network it enables can't go live until
ClaviFaber's profile is complete.

#### A2. Hardcoded headscale port in `headscale.nix:12`

```nix
headscalePort = 8443;
```

This is a service decision (which port the tailnet controller listens on)
sitting in CriomOS. It should be carried by the `TailnetControllerRole`
sum-variant in `NodeServices`:

```rust
pub enum TailnetControllerRole {
    Server { port: u16 },
}
```

Today the variant is unit. Adding the port payload follows the same
typed-records-over-flags pattern as everything else.

#### A3. Hardcoded tailnet base-domain prefix in `headscale.nix:17`, `dnsmasq.nix:24`

```nix
tailnetBaseDomain = "tailnet.${clusterDomainName}";
```

The literal `"tailnet."` is a cluster-wide naming convention that lives
in two CriomOS modules. If the cluster ever runs more than one tailnet
(per-tenant subdomains, lab environments), this hardcoding is wrong.

**What it should be**: `cluster.tailnet.base_domain` (or fold into
`TailnetControllerRole::Server { base_domain }`) projected from horizon.

### B. Flag-soup capability gates — same smell, different syntax — P1

The `Node` type currently exposes:

```rust
pub is_nix_cache: bool,
pub is_remote_nix_builder: bool,
pub is_dispatcher: bool,
pub is_large_edge: bool,
pub behaves_as: BehavesAs,  // .large_ai: bool, .virtual_machine: bool, ...
```

CriomOS consumes them at:

| File | Reads | Why it's flag soup |
|---|---|---|
| `nix/cache.nix:11` | `isNixCache` | "Yes" carries data — endpoint URL, signing key, retention policy. Today every consumer re-derives endpoint from `node.criomeDomainName` and the signing key path is hardcoded `"/var/lib/nix-serve/nix-secret-key"` in cache.nix:34. |
| `nix/builder.nix:14` | `isRemoteNixBuilder`, `isDispatcher` | Two booleans for two facets of the same concept. "Yes" carries max-jobs, cores-per-job, trust level. Today derived ad-hoc. |
| `llm.nix:127` | `behavesAs.largeAi` | "Yes" carries port (currently from `criomos-lib/data/largeAI/llm.json`), GPU env vars, model inventory, retention. The port read is OK (CriomOS protocol convention) but role + port + model list should be one typed record. |

This is the audit-07 §5.1 / `skills/typed-records-over-flags.md` pattern.
The fix is `NodeCapabilities`:

```rust
pub struct NodeCapabilities {
    pub binary_cache: Option<BinaryCache>,         // replaces is_nix_cache
    pub build_host: Option<BuildHost>,             // replaces is_remote_nix_builder + parts of is_dispatcher
    pub container_host: Option<ContainerHost>,     // (cloud-host scope)
    pub public_endpoint: Option<PublicEndpoint>,   // (cloud-host scope)
}

pub struct BinaryCache {
    pub endpoint: BinaryCacheEndpoint,             // scheme, host, port, public_key
    pub signing_key: SecretReference,              // name + purpose, backend on Cluster
    pub retention_policy: CacheRetentionPolicy,
}

pub struct BuildHost {
    pub max_jobs: u32,
    pub cores_per_job: u32,
    pub trust: AtLeast,
}
```

These records exist on the unmerged `push-oowpqtrszouq` (slice 1) and
`push-xzrxuvroxskv` (slice 3a: `build_host` derivation) horizon-rs
bookmarks. The cluster-data half of fixing CriomOS is exactly the
typed-records work that's been parked.

### C. String-derivation hacks and "Phase 1" scaffolds — P2

#### C1. `lib.removePrefix "${node.name}." node.criomeDomainName`

`dnsmasq.nix:23` and `headscale.nix:16` both derive the cluster domain
this way. The assumption: the projected node domain is exactly
`<node>.<cluster>.<tld>`. If horizon-rs ever projects a different shape
(per-environment subdomains, federated clusters, multi-domain hosts), the
strip silently produces wrong output.

**What it should be**: `cluster.domain_name: ClusterDomainName` projected
directly. The `Cluster.tld` field I added earlier (push-pkzmxxsolntv,
unmerged) is the foundation; the domain-name projection is the consumer.

#### C2. Self-signed TLS in `headscale.nix:53-65`

A 60-line openssl shell script that mints a self-signed cert at first
boot. Comment says "Phase 1; will be replaced with real PKI later."

**What it should be**: cert material delivered by the cluster-trust
runtime that audits 117 and 118 name as missing. Until that runtime
exists, the Phase 1 hack persists as the second-worst leak — operator
trust is bootstrapped by ignoring a fingerprint warning, not by horizon
declaring a trusted CA.

#### C3. `router/wifi-pki.nix` directory scaffolding

Prepares `/etc/criomOS/wifi-pki/` and prints imperative hints. Doesn't
configure hostapd. This is named in audit 118 §"Risk pattern: scaffolds
that look like implemented features" — the module exists with the right
name but the feature isn't done. Per `skills/beauty.md`'s diagnostic
readings, the file should either implement the feature or be deleted.

### D. Probably-fine, name explicitly so it stays fine

Things that look like they could be leaks but aren't:

- `node.name` used as a **value** in `llm.nix:21, 103, 150`,
  `network/default.nix:55, 73`, `wifi-eap.nix:14, 34`,
  `dnsmasq.nix:23`, `headscale.nix:16`. Hostname identity, file paths,
  service names. Reading `node.name` is fine; *gating on* `node.name == "X"`
  is not.
- `criomos-lib` constants for paths (`/etc/criomOS/complex/...`),
  protocol ports (Nix daemon convention), interface names (`br-lan`).
  Implementation conventions; CriomOS owns these.
- `cache.nix:34` `secretKeyFile = "/var/lib/nix-serve/nix-secret-key"` —
  this is the deployment materialization path (where sops/credentials
  decrypts to). It's a CriomOS implementation choice once horizon names
  the secret. Cleaner: derive it from a `constants.nixServe.keyFile`
  constant.
- LAN subnet `10.18.0.0/24`, gateway `10.18.0.1` in `criomos-lib` —
  audit 117 P1 flags these as probably cluster policy. They're shared
  across `router/default.nix:17` and `network/dnsmasq.nix:20`. Decide:
  CriomOS convention or horizon-projected? If only one cluster ever uses
  this subnet, the CriomOS-convention answer is fine. If a second cluster
  with a different subnet is ever proposed, they become horizon data.
  Lower priority — file as a question, not a fix.

## The tailscale question

User: "I think for now we're not even using it, so we might just want to
disable the module."

Current shape: `tailscale.nix` is 18 lines, gated entirely on
`node.services.tailnet == "Client"`. If no node has `Some(Client)`, the
module produces an empty config. The same is true for `headscale.nix`
when no node has `Some(Server)`.

Two options:

| Option | Cost | Risk |
|---|---|---|
| **Leave horizon-gated, set to None everywhere in goldragon** | Module stays, evaluates to no-op when not used. Cost: ~18 lines of dormant Nix per module. Resurrecting = one goldragon edit. | Low. Code is small, contract is clean. |
| **Delete tailscale.nix and headscale.nix; remove `TailnetMembership`/`TailnetControllerRole` from horizon-rs** | Removes ~150 lines of code + horizon vocabulary. Resurrecting = re-add module + re-add horizon types + re-deploy. | Medium. The cluster-trust runtime work names headscale as the eventual sign-in path for new hosts; deleting it now means re-architecting later. |

Recommendation: **Option 1**. The modules don't fire, cost almost nothing
at evaluation time, and the `NodeServices` typed record is the right
shape to keep around. Verify with goldragon — if any node currently has
`services.tailnet = Client`, that's the user-facing question.

If we're certain tailnet isn't reviving, the right move is to file a
bead `delete-tailnet-modules` and decide after one more cluster-design
sweep. Not in this report's scope.

## How this intersects with the cloud-host work

The cloud-host plan's Phase 1 (horizon-rs typed
placement/capability/secret records, on unmerged bookmarks
`push-oowpqtrszouq` through `push-xzrxuvroxskv`) **is** the same work
needed to fix category B above. Fixing the flag-soup gates doesn't need
container-host modules, doesn't need a dedicated server, doesn't need
Ghost. It needs:

1. `NodeCapabilities` with `binary_cache`, `build_host`. (Slice 1 + slice 3a.)
2. `SecretReference` and cluster-level secret binding. (Slice 1.)
3. CriomOS consumers updated to read `capabilities.binary_cache.endpoint`
   instead of constructing URLs from `criomeDomainName`, to read
   `capabilities.binary_cache.signing_key` instead of the hardcoded path,
   etc.

Per the user's framing from this conversation, the cleaner shape merges
`placement` into `MachineSpecies` as data-bearing variants instead of a
separate field — but that's a refactor of the bookmark, not a blocker.

Picking up the typed-records pass for its **own** sake (rather than for
cloud-host) gives the workspace:

- A type-safe way to add `hyacinth` later — but more importantly today, a
  type-safe way to describe `prometheus`'s cache, `ouranos`'s router
  duties, the LLM service.
- A landing pad for the Wi-Fi typed records the system-specialist needs
  (Wi-Fi auth, EAP profile, server identity).
- Closure of audit-07 §"Missing tests" follow-ups that are blocked on
  having typed records to test against.

## Recommended order

Revised per user decision 2026-05-13: Wi-Fi data leak is **not first**.
It's resolved by deleting the WPA3-SAE network after the new EAP-TLS
network is in place; the work is "add the new network," not "extract the
old one." That work sits at step 5 because it depends on hardware (USB
Wi-Fi dongle) and on ClaviFaber's Wi-Fi cert profile being completed.

1. **Headscale port + tailnet base-domain as `TailnetControllerRole`
   payload** — tiny scope, removes A2 + A3 in one pass. No upstream
   dependencies.
2. **`cluster.domain_name` projected, replaces `removePrefix` hacks** —
   cleans up C1. Tiny, self-contained.
3. **Flag-soup → typed records pass** — `NodeCapabilities { binary_cache,
   build_host }` + CriomOS consumers. Pulls from the parked cloud-host P1
   bookmarks; rebase on top of `NodeServices` and onto the user's cleaner
   shape (`MachineSpecies` becomes data-bearing rather than adding a
   separate `placement` field). Closes B in one pass.
4. **`large_ai` typed record** — `LargeAi { port, gpu_env, model_inventory_path }`
   on `NodeServices` (or `NodeCapabilities`, depending on where step 3
   lands the boundary). Removes the implicit `criomos-lib` data coupling
   from `llm.nix`.
5. **Dual-WLAN-interface horizon schema + EAP-TLS as second network** —
   `RouterInterfaces` grows to a list (or gains a second typed field);
   `WifiNetwork` typed record lands; `router/default.nix` gains a second
   hostapd radio block keyed on the dongle interface, horizon-driven from
   day one. The existing WPA3-SAE block stays. This step ships the
   schema half before EAP-TLS goes live.
6. **Wire EAP-TLS network end-to-end** — ClaviFaber Wi-Fi cert profile
   (SAN, EKU, dedicated keypair decision); `wifi-pki.nix` actually
   wiring hostapd; `wifi-eap.nix` reading matching client key material.
   Blocked on ClaviFaber side. Tracked under `primary-nvs8`.
7. **Migrate clients to EAP-TLS, delete WPA3-SAE network** — resolves A1
   by deletion.
8. **Tailscale decision** — Option 1 (keep, gated, set None everywhere)
   or Option 2 (delete entirely) after one explicit choice. Independent
   of the rest.
9. **Phase 1 self-signed TLS in headscale** — deferred behind
   cluster-trust runtime. The runtime is the load-bearing work; not
   soluble in CriomOS alone.

Steps 1, 2, 8 are tiny independent slices. Step 3 is the broader
architectural pass (the cloud-host P1 work refactored to the user's
data-bearing-`MachineSpecies` shape). Steps 5–7 are the Wi-Fi migration
chain; step 5 alone is actionable now, step 6 needs ClaviFaber, step 7
needs hardware + client cutover.

## Sources

- Grep over `/git/github.com/LiGoldragon/CriomOS/modules/` confirming
  zero `node.name ==` comparisons and zero literal node-name strings.
- Read of every `modules/nixos/*.nix` and `modules/nixos/network/*.nix`
  file plus `nix/{client,builder,cache}.nix`, `router/default.nix`,
  `llm.nix`.
- `reports/system-specialist/117-system-data-purity-and-wifi-pki.md` —
  the parallel system-specialist audit.
- `reports/system-specialist/118-criomos-state-and-sandbox-audit.md` —
  current cross-cutting state.
- `reports/system-assistant/07-criomos-stack-deep-audit.md` §5.1 — the
  typed-records-over-flags pattern named.
- `skills/typed-records-over-flags.md` — the canonical pattern.
- `reports/designer-assistant/29-review-of-designer-139-wifi-pki.md` —
  the `WifiAuthentication` sum-with-data shape.
- User direction this conversation: "There should never be node names in
  CriomOS. … This is not related to the cloud infrastructure improvement.
  This is just how CriomOS should be. … if the agent doesn't understand
  what the intention is there, like the firewall allow TCP port, what is
  that for the Nix daemon? It really should just be is the node offering
  that service?"

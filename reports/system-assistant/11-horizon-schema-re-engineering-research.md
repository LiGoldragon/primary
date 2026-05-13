# 11 — Horizon schema re-engineering: research

Date: 2026-05-13
Role: system-assistant
Frames: user direction this conversation — *"Do a full survey of the
        current horizon schema and not just for the point that I brought
        up, but any variant. … Could this become a data-bearing variant,
        and which part of the schema could we put in there so that we
        could eliminate redundancy, eliminate the number of fields, and
        make the schema, the configuration declaration of the cluster
        more succinct."*
Reads: `/git/github.com/LiGoldragon/horizon-rs/lib/src/{lib,species,
       magnitude,name,address,io,pub_key,machine,proposal,user,node,
       horizon,cluster,error}.rs` (all 14 files, from main)
Pairs with: `skills/typed-records-over-flags.md`,
            `reports/system-assistant/09-cluster-data-leaks-in-criomos.md`,
            the parked P1 placement/capability/secret bookmarks on
            horizon-rs origin

## Frame

The horizon schema was designed in Nix in the legacy archive, then
ported to Rust roughly verbatim. The Nix shape had no closed-set
algebraic types; everything was records of nullable fields plus
predicate-shaped derived records. The Rust port preserved that shape.

The result: a 577-line `node.rs` defining a `Node` struct with **50
fields**, of which approximately 30 are derived booleans or pre-rendered
strings that could be computed by consumers from a much smaller core.
The schema doesn't *fail* — it works correctly — but it carries
considerable redundancy, several mutually-exclusive boolean groups that
want to be sum enums, and a clutter of `Option<T>` fields whose
optionality is conditional on an unstated tag.

This report surveys every type in `horizon-rs/lib/src/` against three
diagnostic questions:

1. **Could this become a data-bearing variant?** — for every enum,
   could variants carry the fields that are only meaningful for that
   variant?
2. **What's redundant?** — every derived field; every boolean
   computable from one other field.
3. **What hides typed data?** — every `is_X: bool` / `has_X: bool`
   whose "yes" branch carries information consumers re-derive ad-hoc.

The goal: shrink the schema's surface so cluster declarations are
shorter, illegal states are unrepresentable, and consumers (CriomOS
modules) read typed records instead of pattern-matching predicate
flags.

## Method

For each `.rs` file in `horizon-rs/lib/src/` on main as of
2026-05-13 (commit `1e09ab48 preserve tailnet controller variant
name in JSON`), I catalogued:

- Every struct and its fields (count, type, whether optional, whether
  derived)
- Every enum and its variants (count, whether unit-only, whether
  carries data, whether members are mutually exclusive in practice)
- Every `is_*` / `has_*` boolean (whether derivable from another field)
- Every group of fields conditional on an unstated discriminator (the
  "implicit pod-only" / "implicit metal-only" pattern)

The 14 source files total roughly 1450 lines of schema. The
projector itself (`Node::project`, `User::project`, ~250 lines) was
read but not catalogued for redundancy — it's the *consumer* of the
schema, not the schema.

## Findings

Fifteen findings, ordered roughly by impact-of-fix. Each names what
the current shape is, what's wrong with it, and the proposed
replacement.

### F1. `MachineSpecies` should become a data-bearing enum named `Machine`

**Current shape** (`species.rs`, `machine.rs`):

```rust
pub enum MachineSpecies { Metal, Pod }

pub struct Machine {
    pub species: MachineSpecies,
    pub arch: Option<Arch>,            // pod inherits from super_node
    pub cores: u32,
    pub model: Option<ModelName>,      // metal-only meaningful
    pub mother_board: Option<MotherBoard>,
    pub super_node: Option<NodeName>,  // pod-only
    pub super_user: Option<UserName>,  // pod-only
    pub chip_gen: Option<u32>,         // metal-only (intel iGPU)
    pub ram_gb: Option<u32>,
}
```

**The problem**: every `Option<T>` field's optionality is conditional
on `species`. `super_node` is Some only when Pod. `model` is
meaningful only when Metal. The schema admits illegal states
(`species: Pod` with no `super_node`; `species: Metal` with
`super_node: Some(x)`) that the projector has to validate at runtime.

**The proposed shape** (this is the user's prompt, formalised):

```rust
pub enum Machine {
    Metal(Metal),
    Pod(Pod),
}

pub struct Metal {
    pub arch: Arch,
    pub cores: u32,
    pub ram_gb: u32,
    pub model: Option<KnownModel>,         // typed, not String — see F2
    pub motherboard: Option<MotherBoard>,
    pub chip_gen: Option<u32>,
}

pub struct Pod {
    pub host: NodeName,
    pub super_user: Option<UserName>,
    pub cores: u32,                        // resource allocation in the host
    pub ram_gb: u32,                       // resource allocation in the host
    // arch derived from host at projection time
}
```

`MachineSpecies` the unit-variant enum disappears; the data-bearing
enum carries the same name as the field's natural noun (`Machine`).
The old struct `Machine` rolls into the two variants. Cluster authors
write one of two shapes; neither admits the illegal cross.

**Removes**: 7 `Option<T>` fields conditional on species; the
"super-node missing" error case at projection (now unrepresentable);
the arch-resolution dance for pods (now derivation, not validation).

**Composes with** the parked P1 work on `NodePlacement`: that proposal
added a separate `placement` field next to `machine`. The cleaner shape
just makes `Machine` itself the data-bearing enum — one source of
truth, no dual-authority migration headache.

### F2. `ModelName: String` should be `KnownModel` directly

**Current shape** (`name.rs`):

```rust
pub struct ModelName(pub(crate) String);

impl ModelName {
    pub fn known(&self) -> Option<KnownModel> { /* match on str */ }
}

pub enum KnownModel {
    ThinkPadX230, ThinkPadX240,
    ThinkPadT14Gen2Intel, ThinkPadT14Gen5Intel, Rpi3B,
}
```

**The problem**: the proposal carries `model: Option<ModelName>` (a
string) and the projector parses it into `Option<KnownModel>` at
runtime. Every consumer that branches on model has to go through
`model.known()`. The string form admits any free text (`"ThinPadX230"`
typo silently produces `None`).

**The proposed shape**: replace `ModelName` with `KnownModel`
directly. The proposal carries the typed variant. Unknown models
either get a `KnownModel::Other(String)` escape hatch or a new variant
added to the enum.

```rust
pub model: Option<KnownModel>,  // on Metal{...}
```

**Removes**: the `ModelName` newtype, the `model_is_thinkpad: bool`
flag on `Node`, the `ComputerIs` struct (see F4), the string-matching
dispatch in `name.rs::known()`. Adds one variant per machine the
operator actually deploys.

### F3. `BehavesAs` is pure redundancy — 9 derived booleans

**Current shape** (`node.rs`):

```rust
pub struct BehavesAs {
    pub center: bool,
    pub router: bool,
    pub edge: bool,
    pub next_gen: bool,
    pub low_power: bool,
    pub bare_metal: bool,
    pub virtual_machine: bool,
    pub iso: bool,
    pub large_ai: bool,
}
```

All 9 booleans derive deterministically from `(NodeSpecies,
MachineSpecies, io.disks.is_empty())`. The derivation lives in
`BehavesAs::derive(&type_is, &machine, io_disks_empty)`.

**The problem**:

- `bare_metal` vs `virtual_machine` are mutually exclusive — should
  be one enum (and they ARE one enum: `MachineSpecies`. This is the
  same fact in two shapes).
- `center`, `router`, `edge`, `large_ai` are species-derived
  categories. Two can be true simultaneously (`Hybrid` is both `edge`
  and `router`). A bag-of-booleans models this OK but obscures the
  underlying species.
- `iso` is a degenerate predicate (`!virtual_machine &&
  io.disks.is_empty`). Used in exactly one place
  (`enable_network_manager` derivation).

**The proposed shape**: **delete `BehavesAs` entirely.** Consumers
pattern-match on `node.machine` (per F1) and `node.species` directly.
For the few cases where a boolean is genuinely useful as a derived
property, expose a `node.is_edge()` / `node.is_router()` method on
`Node`. Don't serialise predicates the consumer can compute.

**Removes**: 9 boolean fields × every `Node` (so 9 × N nodes in the
serialised horizon).

### F4. `TypeIs` is even more redundant — 9 `matches!(species, X)` flags

**Current shape** (`node.rs`):

```rust
pub struct TypeIs {
    pub center: bool,
    pub edge: bool,
    pub edge_testing: bool,
    pub hybrid: bool,
    pub large_ai: bool,
    pub large_ai_router: bool,
    pub media_broadcast: bool,
    pub router: bool,
    pub router_testing: bool,
}
```

The derivation in `TypeIs::from_species` is literally
`matches!(species, X)` × 9. Exactly one is true at a time, by
construction.

**The problem**: it's a one-hot encoding of `NodeSpecies`. Same
information; ten times the bytes; no type-system protection against
"two trues."

**The proposed shape**: **delete `TypeIs` entirely.** Consumers
pattern-match `node.species` directly. Nix-side code reads
`node.species == "edge"` instead of `node.type_is.edge`. Either is
fine textually; one is type-safe at the producer.

**Removes**: 9 boolean fields × every `Node`.

### F5. `ComputerIs` — same shape, model-specific

**Current shape** (`node.rs`):

```rust
pub struct ComputerIs {
    pub thinkpad_t14_gen2_intel: bool,
    pub thinkpad_t14_gen5_intel: bool,
    pub thinkpad_x230: bool,
    pub thinkpad_x240: bool,
    pub rpi3b: bool,
}
```

Derived from `model.known()` (which is `Option<KnownModel>`). Same
one-hot pattern as `TypeIs`.

**The proposed shape**: **delete.** After F2, `node.machine` is
`Metal { model: Option<KnownModel>, ... }` or `Pod`. Consumers match
on `model` directly. `model_is_thinkpad: bool` on `Node` (yet another
flag) also goes away — it's `model.is_some_and(KnownModel::is_thinkpad)`.

**Removes**: 5 boolean fields, 1 `model_is_thinkpad` field, the
`ComputerIs::from_model` helper.

### F6. The 14 `has_*` / `is_*` flags on `Node`

**Current shape** (`node.rs`):

```rust
pub is_fully_trusted: bool,            // = trust.max
pub is_remote_nix_builder: bool,       // derived predicate; hides BuildHost data
pub is_dispatcher: bool,               // derived predicate
pub is_nix_cache: bool,                // hides BinaryCache data
pub is_large_edge: bool,               // = size.large && behaves_as.edge
pub enable_network_manager: bool,      // derived predicate
pub has_nix_pub_key: bool,             // = nix_pub_key.is_some()
pub has_ygg_pub_key: bool,             // = ygg_pub_key.is_some()
pub has_ssh_pub_key: bool,             // always true (required in proposal)
pub has_wireguard_pub_key: bool,       // = wireguard_pub_key.is_some()
pub has_nordvpn_pub_key: bool,         // = nordvpn (the proposal bool)
pub has_wifi_cert_pub_key: bool,       // = wifi_cert (the proposal bool)
pub has_base_pub_keys: bool,           // = has_nix && has_ygg && has_ssh
pub has_video_output: bool,            // = behaves_as.edge
pub chip_is_intel: bool,               // = arch.is_intel()
pub model_is_thinkpad: bool,           // see F5
```

**The problem**:
- 8 are `field.is_some()` or `field == true` — pure redundancy.
- 5 hide payload data that should be in a typed record
  (`is_remote_nix_builder` → `BuildHost`; `is_nix_cache` →
  `BinaryCache`; etc.) — see F7.
- 1 is the always-true `has_ssh_pub_key` (ssh is required) —
  pure dead flag.

**The proposed shape**: delete every flag whose payload is trivially
recoverable. Replace the 5 that hide typed data with `Option<Record>`
per F7.

**Removes**: 8 fields outright (the `has_*` redundants).

### F7. Capability flags hide typed records (the parked P1 work)

**Current shape**:

```rust
pub is_nix_cache: bool,
pub is_remote_nix_builder: bool,
pub is_dispatcher: bool,
pub is_large_edge: bool,
pub nordvpn: bool,
pub wifi_cert: bool,
```

Each "yes" branch hides authored cluster data: cache endpoint URL +
signing key + retention; build-host max-jobs + cores + trust; tailnet
membership; VPN credentials; Wi-Fi cert reference.

**The problem**: same pattern as
`skills/typed-records-over-flags.md`. Every consumer
re-derives the payload from magic strings or hardcoded paths.

**The proposed shape** (from parked P1 + the user's
data-bearing-variant direction):

```rust
pub struct NodeCapabilities {
    pub binary_cache: Option<BinaryCache>,
    pub build_host: Option<BuildHost>,
    pub container_host: Option<ContainerHost>,
    pub public_endpoint: Option<PublicEndpoint>,
}

pub struct BinaryCache {
    pub endpoint: BinaryCacheEndpoint,
    pub signing_key: SecretReference,
    pub retention_policy: CacheRetentionPolicy,
}

pub struct BuildHost {
    pub max_jobs: u32,
    pub cores_per_job: u32,
    pub trust: AtLeast,
}
```

For VPN and Wi-Fi cert, the right home is `NodePubKeys`:

```rust
pub struct NodePubKeys {
    pub ssh: SshPubKey,
    pub nix: Option<NixPubKey>,
    pub yggdrasil: Option<YggPubKeyEntry>,
    pub wifi_cert: Option<WifiCertEntry>,     // was: wifi_cert: bool
    pub wireguard: Option<WireguardEntry>,    // was: 2 scattered fields
    pub nordvpn: Option<NordvpnEntry>,        // was: nordvpn: bool
}
```

**Removes**: 6 booleans; gives every "yes" a typed payload; eliminates
the secret-path-hardcoded-in-CriomOS issue from report 09 §A.

### F8. `TailnetMembership` is a unit-variant enum — collapse with `TailnetControllerRole`

**Current shape** (`proposal.rs`):

```rust
pub struct NodeServices {
    pub tailnet: Option<TailnetMembership>,
    pub tailnet_controller: Option<TailnetControllerRole>,
}

pub enum TailnetMembership {
    Client,
}

pub enum TailnetControllerRole {
    Server { port: u16, base_domain: DomainName },
}
```

**The problem**:
- `TailnetMembership` has one variant — equivalent to `Option<()>`.
- `tailnet` and `tailnet_controller` are mutually exclusive in
  practice (a node is a client OR a server, not both — though
  technically a server is also a member).
- Two fields where one would do.

**The proposed shape**:

```rust
pub enum TailnetRole {
    Client,
    Server { port: u16, base_domain: DomainName },
}

pub struct NodeServices {
    pub tailnet: Option<TailnetRole>,
    // ... future per-service roles, same shape
}
```

One field replaces two. Mutual exclusion enforced by the type.
Singleton validation (`validate_tailnet_controller_singleton`) becomes
"at most one node has `Some(TailnetRole::Server)`" — clean predicate
on one field.

**Removes**: 1 field, 1 unit-variant enum.

### F9. Viewpoint-vs-other split via `Option<T>` is a misencoding

**Current shape** (`node.rs`):

```rust
pub struct Node {
    // ... 32 always-present fields ...

    // viewpoint-only fields
    pub io: Option<Io>,
    pub use_colemak: Option<bool>,
    pub computer_is: Option<ComputerIs>,
    pub builder_configs: Option<Vec<BuilderConfig>>,
    pub cache_urls: Option<Vec<String>>,
    pub ex_nodes_ssh_pub_keys: Option<Vec<SshPubKeyLine>>,
    pub dispatchers_ssh_pub_keys: Option<Vec<SshPubKeyLine>>,
    pub admin_ssh_pub_keys: Option<Vec<SshPubKeyLine>>,
    pub wireguard_untrusted_proxies: Option<Vec<WireguardProxy>>,
}
```

`Option<T>` here doesn't mean "this might be absent"; it means "this
is the viewpoint node." Semantically a tag mis-encoded as
optionality.

**The problem**:
- The same `Node` struct represents both the viewpoint and every
  other-node-in-the-horizon. Consumers must check `node.io.is_some()`
  to know which one they have.
- Mixes input pass-through (`io`), derivations (`use_colemak`,
  `computer_is`), cross-node rollups (`builder_configs`,
  `cache_urls`, etc.) in one bag.
- 9 Optional fields × every Node (8 of which are always None for
  ex_nodes) — pure wire bloat.

**The proposed shape**:

```rust
pub struct Horizon {
    pub cluster: Cluster,
    pub node: Node,                          // always full
    pub viewpoint: ViewpointData,            // viewpoint-only stuff lives here
    pub ex_nodes: BTreeMap<NodeName, Node>,  // same Node type, no Option mess
    pub users: BTreeMap<UserName, User>,
}

pub struct ViewpointData {
    pub io: Io,
    pub computer: Option<KnownModel>,        // formerly ComputerIs
    pub builder_configs: Vec<BuilderConfig>,
    pub cache_urls: Vec<String>,
    pub ex_nodes_ssh_pub_keys: Vec<SshPubKeyLine>,
    pub dispatchers_ssh_pub_keys: Vec<SshPubKeyLine>,
    pub admin_ssh_pub_keys: Vec<SshPubKeyLine>,
    pub wireguard_untrusted_proxies: Vec<WireguardProxy>,
}
```

`Node` is the same shape for everyone in the horizon. The viewpoint
gets a sibling `ViewpointData` struct. Consumers read
`horizon.viewpoint.io.keyboard` instead of `horizon.node.io.unwrap().keyboard`.

**Removes**: 9 `Option<T>` fields from `Node`; gives ex_nodes
serialisation a cleaner shape (8 fewer `None` fields per ex-node).

### F10. `AtLeast` is a 4-bool projection of `Magnitude` — keep or drop?

**Current shape** (`magnitude.rs`):

```rust
pub enum Magnitude { Zero, Min, Medium, Large, Max }

pub struct AtLeast {
    pub min: bool,
    pub medium: bool,
    pub large: bool,
    pub max: bool,
}
```

`AtLeast` is the public shape of size/trust; consumers branch on
`size.medium`, `trust.max`, etc.

**The problem**: 4 booleans where one enum would do. The
`Zero` magnitude is lost in `AtLeast` (no `at_least.zero`). Consumers
that genuinely want the ordinal can use `Magnitude` directly.

**Verdict**: Keep `Magnitude` as the input form; **delete `AtLeast`**.
Nix-side consumers can compare strings (`node.size == "max"`) or
horizon-rs can expose `at_least(Magnitude::Medium)` as a derived
method. The 4-bool struct is a Nix-convenience layer worth ~10%
schema-surface reduction.

**Removes**: 4 boolean fields × every `Node`, every `User`. Net
removal: 16 booleans across the typical horizon.

### F11. `Cluster` is too thin; will grow naturally

**Current shape** (`cluster.rs`):

```rust
pub struct Cluster {
    pub name: ClusterName,
    pub trusted_build_pub_keys: Vec<NixPubKeyLine>,
}
```

Two fields. But several reports name fields that need to land here:

- `tld: ClusterTld` (per parked `push-pkzmxxsolntv`)
- `domain_name: ClusterDomainName` (replaces the
  `lib.removePrefix "${node.name}." node.criomeDomainName` hack from
  CriomOS — see report 09 §C1)
- `wifi: Option<WifiNetwork>` (per report 09 §A1 + user's dual-radio
  decision)
- `secret_bindings: Vec<ClusterSecretBinding>` (per plan 04 §1.1)
- `tailnet: Option<TailnetConfig>` (base_domain etc. — currently
  packed into `TailnetControllerRole::Server`, but the *cluster* owns
  the base domain, not the controller server)

**The proposed shape**:

```rust
pub struct Cluster {
    pub name: ClusterName,
    pub tld: ClusterTld,
    pub domain_name: ClusterDomainName,
    pub trusted_build_pub_keys: Vec<NixPubKeyLine>,
    pub wifi_networks: Vec<WifiNetwork>,         // plural — see F14
    pub secret_bindings: Vec<ClusterSecretBinding>,
    pub tailnet: Option<TailnetConfig>,
}
```

No removals here; only growth. The pattern: cluster-wide policy lives
on `Cluster`, not duplicated per-node.

### F12. `NodeProposal` has 16 fields; some flags genuine, some not

**Current shape** (`proposal.rs`):

```rust
pub struct NodeProposal {
    pub species: NodeSpecies,
    pub size: Magnitude,
    pub trust: Magnitude,
    pub machine: Machine,
    pub io: Io,
    pub pub_keys: NodePubKeys,
    pub link_local_ips: Vec<LinkLocalIp>,
    pub node_ip: Option<NodeIp>,
    pub wireguard_pub_key: Option<WireguardPubKey>,   // → NodePubKeys (F7)
    pub nordvpn: bool,                                 // → NodePubKeys (F7)
    pub wifi_cert: bool,                               // → NodePubKeys (F7)
    pub wireguard_untrusted_proxies: Vec<WireguardProxy>,
    pub wants_printing: bool,                          // KEEP (no payload)
    pub wants_hw_video_accel: bool,                    // KEEP (no payload)
    pub router_interfaces: Option<RouterInterfaces>,
    pub online: Option<bool>,
    pub number_of_build_cores: Option<u32>,            // → BuildHost (F7)
    pub services: NodeServices,
}
```

After F1, F7, F8 land:

```rust
pub struct NodeProposal {
    pub species: NodeSpecies,
    pub size: Magnitude,
    pub trust: Magnitude,
    pub machine: Machine,           // data-bearing enum, F1
    pub io: Io,
    pub pub_keys: NodePubKeys,      // absorbs nordvpn/wifi_cert/wireguard, F7
    pub link_local_ips: Vec<LinkLocalIp>,
    pub node_ip: Option<NodeIp>,
    pub wireguard_untrusted_proxies: Vec<WireguardProxy>,
    pub wants_printing: bool,       // genuine no-payload boolean — KEEP
    pub wants_hw_video_accel: bool, // genuine no-payload boolean — KEEP
    pub router_interfaces: Option<RouterInterfaces>,  // F14
    pub online: bool,               // default true via serde
    pub capabilities: NodeCapabilities,  // build_host/binary_cache/etc., F7
    pub services: NodeServices,
}
```

From 18 fields to 15. More importantly, the structure clarifies:
hardware identity in `machine`, public material in `pub_keys`, operator
opt-ins as bare bools, cluster role/payload in `capabilities`/`services`.

### F13. `RouterInterfaces` needs to grow to multiple WLANs

**Current shape** (`proposal.rs`):

```rust
pub struct RouterInterfaces {
    pub wan: Interface,
    pub wlan: Interface,
    pub wlan_band: WlanBand,
    pub wlan_channel: u16,
    pub wlan_standard: WlanStandard,
}
```

**The problem**: singular `wlan`. Per the user's decision this
conversation (dual-radio Wi-Fi migration: built-in radio runs the
existing WPA3-SAE network, USB dongle hosts new EAP-TLS), the schema
needs to express two simultaneous WLAN interfaces, each with its own
network policy.

**The proposed shape**:

```rust
pub struct RouterInterfaces {
    pub wan: Interface,
    pub wlans: Vec<WlanInterface>,
}

pub struct WlanInterface {
    pub iface: Interface,
    pub band: WlanBand,
    pub channel: u16,
    pub standard: WlanStandard,
    pub network: WifiNetworkRef,    // names a cluster.wifi_networks entry
}
```

`WifiNetworkRef` is just a string name; the network policy
(SSID, country, auth) lives on `Cluster.wifi_networks` (per F11)
because it's cluster-wide.

This is the schema half of the EAP-TLS migration path from report 09's
revised order.

### F14. Pre-rendered Line types — keep as derived convenience

**Current shape** (`pub_key.rs`):

```rust
pub struct SshPubKeyLine(String);    // "ssh-ed25519 <base64>"
pub struct NixPubKeyLine(String);    // "<domain>:<base64>"
```

These exist so Nix consumers don't have to do string concat.

**Verdict**: keep, but as **derived methods** on `SshPubKey` /
`NixPubKey`, called at serialisation time. Today they're stored as
separate fields on `Node`, which means each `Node` carries both the
key and the line — redundant 1-to-1 derivation.

```rust
impl SshPubKey {
    pub fn line(&self) -> SshPubKeyLine { ... }
}

// On Node:
pub ssh_pub_key: SshPubKey,
// (no ssh_pub_key_line field; consumers call .line() or
// it's computed in the serde Serialize impl)
```

**Removes**: 2 fields per `Node` (`ssh_pub_key_line`, `nix_pub_key_line`)
and 1 per ex-node entry (`ex_nodes_ssh_pub_keys` is a `Vec` of these
already-derived strings).

### F15. Address/connectivity scattering: 5 fields on `Node`

**Current shape** (`node.rs`):

```rust
pub link_local_ips: Vec<LinkLocalAddress>,
pub node_ip: Option<NodeIp>,
pub wireguard_pub_key: Option<WireguardPubKey>,
pub ssh_pub_key: SshPubKey,
pub nix_pub_key: Option<NixPubKey>,
pub ygg_pub_key: Option<YggPubKey>,
pub ygg_address: Option<YggAddress>,
pub ygg_subnet: Option<YggSubnet>,
```

Pubkeys are mixed with addresses; yggdrasil's three related fields
are scattered.

**The proposed shape**: group by concern.

```rust
pub struct NodeAddresses {
    pub link_local_ips: Vec<LinkLocalAddress>,
    pub node_ip: Option<NodeIp>,
    pub yggdrasil: Option<YggdrasilAddress>,   // address + subnet
}

pub struct YggdrasilAddress {
    pub address: YggAddress,
    pub subnet: YggSubnet,
}

// On Node:
pub addresses: NodeAddresses,
pub pub_keys: NodePubKeys,   // ssh, nix, yggdrasil (pub_key), wifi, wireguard, nordvpn — F7
```

The yggdrasil pubkey naturally lives in `NodePubKeys.yggdrasil`
(already `YggPubKeyEntry`, which already groups pubkey + address +
subnet — but currently this group is unpacked back into 3 separate
fields on Node, defeating the grouping).

**Removes**: 8 scattered fields, replaces with 2 grouped records.

## Recurring patterns

Extracting the cross-finding patterns so they're written once:

1. **Predicate-name structs whose fields all derive from one
   source.** `BehavesAs`, `TypeIs`, `ComputerIs`. The "Is" or
   "BehavesAsX" suffix is the diagnostic. Fix: delete; consumers
   match the source field directly.

2. **`has_X: bool` for `X: Option<T>`.** 8 instances. Pure
   redundancy; `x.is_some()` is the answer. Diagnostic: the bool's
   only meaning is the presence of another field.

3. **`is_X: bool` for `X: Option<Record>`.** 5 instances. The "yes"
   branch carries authored data the consumer re-derives. Fix:
   `Option<Record>` so the typed payload is explicit. Documented in
   `skills/typed-records-over-flags.md`.

4. **Mutually-exclusive booleans / mutually-exclusive options.**
   `bare_metal` vs `virtual_machine` (already `MachineSpecies`);
   `tailnet` vs `tailnet_controller` (should collapse, F8); the 9
   `TypeIs` one-hot flags (already `NodeSpecies`, F4). Fix: sum
   enums.

5. **Optional fields conditional on enum variant.** `Machine.super_node`
   is Some only when species=Pod. `Machine.model` is meaningful only
   when species=Metal. Fix: data-bearing variants. The user's
   prompted refactor of `MachineSpecies` (F1) is the canonical case;
   the same pattern applies wherever `Option<T>` optionality is
   tag-dependent.

6. **Viewpoint-vs-not encoded as `Option<T>`.** F9. Fix: structurally
   separate "the node" from "the viewpoint data."

7. **Stringly-typed dispatch.** `ModelName` is a String parsed to
   `KnownModel` at lookup. Fix: typed at the proposal level (F2).

## Proposed re-engineered top-level shape

After all 15 findings land, the schema looks roughly:

```rust
// ── input (NodeProposal) ──
pub struct NodeProposal {
    pub species: NodeSpecies,
    pub size: Magnitude,
    pub trust: Magnitude,
    pub machine: Machine,                  // F1: data-bearing
    pub io: Io,
    pub pub_keys: NodePubKeys,             // F7, F15: absorbs nordvpn/wifi/wireguard
    pub addresses: NodeAddresses,          // F15
    pub wireguard_untrusted_proxies: Vec<WireguardProxy>,
    pub wants_printing: bool,
    pub wants_hw_video_accel: bool,
    pub router_interfaces: Option<RouterInterfaces>,  // F13: plural WLANs inside
    pub online: bool,
    pub capabilities: NodeCapabilities,    // F7
    pub services: NodeServices,            // F8: collapsed tailnet
}

pub enum Machine {                         // F1
    Metal(Metal),
    Pod(Pod),
}

// ── output (Node) ──
pub struct Node {
    pub name: NodeName,
    pub species: NodeSpecies,
    pub size: Magnitude,                   // F10: drop AtLeast layer
    pub trust: Magnitude,
    pub machine: Machine,
    pub io_is_iso: bool,                   // single derived predicate (replaces behaves_as.iso)
    pub addresses: NodeAddresses,
    pub criome_domain_name: CriomeDomainName,
    pub system: System,
    pub pub_keys: NodePubKeys,
    pub capabilities: NodeCapabilities,
    pub services: NodeServices,
    pub wants_printing: bool,
    pub wants_hw_video_accel: bool,
    pub router_interfaces: Option<RouterInterfaces>,
    pub online: bool,
    pub wireguard_untrusted_proxies: Vec<WireguardProxy>,
    // NO BehavesAs, NO TypeIs, NO ComputerIs, NO 14 has_/is_ flags.
    // NO viewpoint-only Option fields.
    // Derived predicates (is_remote_nix_builder, etc.) become methods
    // computed from the typed records above.
}

pub struct Horizon {                       // F9
    pub cluster: Cluster,                  // F11: grown
    pub node: Node,
    pub viewpoint: ViewpointData,          // F9: viewpoint-only data extracted
    pub ex_nodes: BTreeMap<NodeName, Node>,
    pub users: BTreeMap<UserName, User>,
}
```

Field counts (approximate, viewpoint horizon):

| Type | Before | After |
|---|---|---|
| `Machine` | 9 fields + species enum (10) | 2 variants × ~6 fields each = ~12 in worst case, far fewer in practice (one variant per node) |
| `Node` | ~50 fields | ~15 fields |
| `BehavesAs` | 9 fields | (deleted) |
| `TypeIs` | 9 fields | (deleted) |
| `ComputerIs` | 5 fields | (deleted) |
| `AtLeast` × 2 fields | 8 booleans | (deleted; `Magnitude` direct) |
| `NodeServices` | 2 Option fields | 1 Option field |
| `RouterInterfaces` | 5 fields, singular WLAN | 2 fields, plural WLAN |

Rough wire-size reduction for a 5-node horizon: **30-40% fewer
fields**, with the remaining fields carrying more typed information
per byte.

## What this changes for CriomOS consumers

Mostly mechanical, all in the same direction (read typed records,
match patterns, drop predicate lookups).

| Old | New |
|---|---|
| `mkIf node.behaves_as.center` | `mkIf (matches species Center …)` (or method) |
| `mkIf node.type_is.large_ai` | `mkIf (matches species LargeAi …)` |
| `optional node.is_nix_cache 80` | `mkIf (node.capabilities.binary_cache != null)` |
| `node.is_remote_nix_builder` | `node.capabilities.build_host != null` |
| `node.machine.species == "Pod"` | `match node.machine { Pod _: ...; Metal _: ... }` |
| `node.computer_is.thinkpad_x230` | match on `node.machine.metal.model` |
| `node.has_nix_pub_key` | `node.pub_keys.nix != null` |
| `horizon.node.io.keyboard` (was: `.io.unwrap()…`) | `horizon.viewpoint.io.keyboard` |

The Nix-side change set is bounded: ~10-15 CriomOS module files. Each
change is mechanical text substitution.

## What this changes for goldragon proposals

`goldragon/datom.nota` would need to migrate. The biggest changes:

- `(Machine Metal x86_64 8 …)` → `(Metal x86_64 8 …)` (one less
  positional level)
- `(Machine Pod _ 4 _ _ prometheus li …)` → `(Pod prometheus li 4 …)`
- Drop trailing `False False` for `wifi_cert`/`nordvpn`; instead omit
  or fill the `pub_keys.wifi_cert`/`pub_keys.nordvpn` entries.
- New top-level fields on `Cluster` for `tld`, `domain_name`,
  `wifi_networks`, `secret_bindings`.

Migration could be a one-shot rewrite of `datom.nota` by hand (it's
small — ~15 nodes), or a horizon-rs `--migrate-from-v1` command.
Either is bounded.

## Risks and migration

### Breaking change

Every change is breaking. Mitigated by:
- Migration cycle: add new shapes, deprecate old, delete old (per
  `skills/typed-records-over-flags.md` §"Migration shape").
- CriomOS doesn't take horizon-rs as a peer flake input directly; it
  takes the JSON output of `lojix-cli`'s horizon projection. So the
  schema migration is gated on lojix-cli + CriomOS both bumping
  together.

### Test rewrite cost

The current projection has 119 tests in horizon-rs. Most are wire
round-trips. They survive the migration; the projection logic changes
but the round-trip property doesn't. The behavioural tests (one
proposal → one expected `Node`) need new expected values.

### CriomOS module rewrites

Estimated 10-15 module files touched. The substitutions are
mechanical text; the type-checking happens at evaluation time. A
helper script (`tools/migrate-criomos-horizon-references`) could batch
the trivial cases.

### Wire backwards compat

CriomOS reads horizon as JSON via lojix. The new shapes need either:
- one-cycle compat where both old and new field names emit
  simultaneously, OR
- a coordinated bump where lojix + CriomOS update together.

The latter is cleaner. The cluster is small (one operator).

## Migration order

Per `skills/typed-records-over-flags.md` §"Migration shape," each
finding gets its own cycle. Recommended order, from cheapest to most
disruptive:

1. **F2 — `KnownModel` direct** (replaces ModelName) — small, isolated.
2. **F11 — `Cluster` grows** (tld, domain_name, etc.) — additive; no
   consumer broken.
3. **F14 — Line types as methods** — removes 3 fields, consumer-side
   change is one method call.
4. **F8 — `TailnetRole` collapse** — small enum refactor, single
   consumer.
5. **F7 — Capability records** (this is the parked P1 work) —
   substantial but bounded; many CriomOS modules touched.
6. **F1 — `Machine` as data-bearing enum** — the apex change; affects
   every consumer that touches machine fields.
7. **F3, F4, F5, F6 — delete the derived flag soups** — should happen
   after F1 because some flags derive from Machine.
8. **F9 — Viewpoint split** — last, because every consumer needs to
   know the new shape.
9. **F10 — Delete `AtLeast`** — small cleanup at the end.
10. **F13 — Plural WLANs** — independent track; can happen anytime.
11. **F15 — Address grouping** — small cleanup.

Each step is one cycle of "add new shape; migrate consumers; delete
old shape." Per `skills/typed-records-over-flags.md`, compat shims
survive one cycle.

## Out of scope

Things this report deliberately doesn't cover:

- **`Horizon::project` algorithm rewrite.** The projection logic
  changes shape but not strategy.
- **`Error` enum expansion.** New typed records will need new error
  variants; trivial.
- **`User` schema.** `User` has the same kinds of derived fields
  (`is_code_dev`, `is_multimedia_dev`, `use_colemak`, `enable_linger`,
  `has_pub_key`) but the user surface is smaller and consumer impact
  more limited. A follow-up audit may be worth doing once Node lands;
  not in scope here.
- **The `domains` proposal field.** `DomainProposal { species:
  DomainSpecies }` has one variant (`Cloudflare`). Already wants to be
  data-bearing (`Cloudflare { account_id, ... }`) but the consumer
  set is minimal today. Defer.
- **Nota wire compat.** The migration discussion assumes coordinated
  bump; the wire-format-level question (positional vs named records,
  backward compat tokens) is the nota-codec's concern.

## Sources

- `/git/github.com/LiGoldragon/horizon-rs/lib/src/` at main
  `1e09ab48` — every file read for the survey.
- `skills/typed-records-over-flags.md` — the canonical pattern these
  findings apply.
- `reports/system-assistant/09-cluster-data-leaks-in-criomos.md` §B
  — same flag-soup pattern observed from the consumer side.
- `reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md`
  — the parked P1 work's typed records (`NodeCapabilities`,
  `SecretReference`, etc.).
- User direction this conversation: *"the pod type needs, so it's a
  data containing variant … so this might even warrant a deeper look
  into are there parts of the schema, the horizon schema that really
  could be better written if some of the data was contained in one of
  the variants."*
- User direction this conversation: dual-WLAN-interface decision
  (informs F13).

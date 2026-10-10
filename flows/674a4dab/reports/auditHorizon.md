# Audit: the data / schema plane

Flow 674a4dab. Witness date: 2026-08-28.

**Commit basis.** All findings are against `origin/main` unless noted.
Commits: horizon-rs `c70915e`, goldragon `5bc563b`, CriomOS `45e83fb`,
CriomOS-home `ed6832c`, CriomOS-lib `6e3bcb0`, criomos-horizon-config
`e222d3a`, lojix `33b8b6b`. Local working copies were behind
origin/main for horizon-rs, goldragon, CriomOS, CriomOS-home, and
lojix; code was verified at origin/main via `git show origin/main:`.

**Origin/main changes since local HEAD.** AgentIntercomLocal and
AgentIntercomGraphical have been removed from the NodeService enum
(horizon-rs c70915e), from goldragon's cluster data (5bc563b), from
CriomOS's agent-intercom gating (45e83fb), and the lojix horizon pin
updated (33b8b6b). Findings F7 and F8 below are marked as resolved
at origin/main. All other findings (F1-F6, F9-F18) are unchanged at
origin/main.

## 1. The plane as it is

### Data-flow

```
goldragon/datom.dotos          criomos-horizon-config/horizon.dotos
 (8 nodes, 2 users,             (domain suffixes, transitional LAN)
  17 fields/node,               NOT CONSUMED by horizon-rs or lojix
  9 fields/user)                -- dead input
       |
       v
  horizon-cli (stdin)
  or lojix in-process (horizon-lib)
       |  reads ClusterProposal via dotos crate
       |  DomainConfiguration comes from inside the ClusterProposal
       |  (last line of datom.dotos), NOT from criomos-horizon-config
       v
  ClusterProposal.project(Viewpoint)
       |  enrichment: ~54-field Node, ~20-field User, BehavesAs (11 bools),
       |  ComputerIs (5 bools), BuilderConfig (9 fields), LidSwitchAction (3)
       v
  Horizon JSON (serde_json::to_string_pretty)
       |
       v
  lojix writes content-addressed flake:
    flake.nix = { outputs = _: { horizon = builtins.fromJSON
                    (builtins.readFile ./horizon.json); }; }
       |
       v
  nix eval CriomOS --override-input horizon <path>
       |
       v
  CriomOS modules read horizon.node.*, horizon.users, horizon.exNodes
  CriomOS-home reads horizon.users, horizon.node (via specialArgs)
```

### Where facts live

| Fact | Location | Path |
|---|---|---|
| Node names, species, sizes, machine specs, disk UUIDs, pubkeys, services | goldragon | `datom.dotos:6-227` |
| User names, species, sizes, pubkeys per node | goldragon | `datom.dotos:229-259` |
| Trust map | goldragon | `datom.dotos:262-275` |
| Domain configuration (internal suffix, public domains) | goldragon | `datom.dotos:276` |
| Domain suffixes (criome, criome.net) [duplicate] | criomos-horizon-config | `horizon.dotos:6` |
| Domain suffixes (criome, criome.net) [hardcoded default] | horizon-rs | `domain.rs:108,121` |
| LAN subnet, gateway, DHCP pool | criomos-horizon-config | `horizon.dotos:8-10` |
| LAN subnet, gateway, subnetPrefix [duplicate] | CriomOS-lib | `lib/default.nix:89-91` |
| Yggdrasil ports, namespace | CriomOS-lib | `lib/default.nix:81-87` |
| Nix serve/cache ports, headscale port | CriomOS-lib | `lib/default.nix:97-105` |
| File paths (complex, wifi-pki, nordvpn) | CriomOS-lib | `lib/default.nix:48-66` |
| SSH matchBlock for prometheus | CriomOS-home | `min/default.nix:534-538` |
| LLM model metadata | CriomOS-lib | `data/largeAI/llm.json` |
| BehavesAs (11 bools), ComputerIs (5 bools), is_* (16 bools), lid-switch policy (3 enums), domain names, nix_url, builder_configs, cache_urls, admin_ssh_pub_keys | horizon-rs (origin/main c70915e) | `lib/src/node.rs` (derived) |
| email_address, matrix_id, extra_groups, enable_linger, preferred_editor, is_code_dev, is_multimedia_dev | horizon-rs | `lib/src/user.rs` (derived) |

## 2. Findings

### F1. criomos-horizon-config is a dead repo

**Evidence.** `criomos-horizon-config/horizon.dotos` declares a
`HorizonProposal` with operator identity, domain suffixes, and
transitional LAN config. But:

- horizon-rs reads only `ClusterProposal` on stdin (`cli/src/main.rs`);
  it has no code to read a `HorizonProposal`
- lojix reads only the proposal source (`schema_runtime.rs:4570-4576`)
  via `ProposalFile`, which is the goldragon `.dotos`
- CriomOS and CriomOS-home do not list `criomos-horizon-config` as a
  flake input (verified: `grep -rn criomos-horizon-config` in both
  flake.nix files returns nothing)
- The domain suffixes (`criome`, `criome.net`) are hardcoded as defaults
  in `horizon-rs/lib/src/domain.rs:108,121` and also authored inside
  the goldragon `datom.dotos:276` as `{criome [goldragon.criome.net]}`

The LAN subnet (`10.18.0.0/24`, gateway `10.18.0.1`) is declared in
the pan-horizon config but also hardcoded in CriomOS-lib
(`lib/default.nix:89-91`), which IS consumed. The pan-horizon config's
DHCP pool (`10.18.0.100-240`) has no consumer.

**Psyche statement departed from.** "put the pan-horizon config in a
new criomos-horizon-config repo" (2026-05-17); "Lojix needs both the
pan-horizon config and the cluster data to create the horizon"
(2026-05-17). The psyche created this repo to house federation-enabling
pan-horizon constants. It is not consumed.

**Severity.** Blocks a stated design. The federation vision requires
pan-horizon config as a separate input to the projection engine; the
current system ignores it and hardcodes the values it was meant to carry.

### F2. BehavesAs: 11 derived booleans versus "a bunch of dials"

**Evidence.** `BehavesAs` (`node.rs:157-169`) is a struct of 11 boolean
fields (`center`, `router`, `edge`, `next_gen`, `low_power`,
`bare_metal`, `virtual_machine`, `iso`, `large_ai`, `test_vm`,
`cloud_node`), derived from `NodeSpecies` + `MachineSpecies` in
`BehavesAs::derive()` (`node.rs:193-225`). It is the "cross-repo gating
contract" -- CriomOS gates on these booleans rather than matching on the
species directly.

The derivation is deterministic and purely mechanical: a table mapping
species to boolean unions. Nix could compute the same table from
`node.species` and `node.machine.species` with a trivial match.

**Psyche statement departed from.** "give me a vector of variants, not
this meaningless series of booleans" (2026-05-18); "variants first --
self-describing stuff" (2026-05-18). BehavesAs is the exact shape the
psyche reacted against: unnamed booleans at schema positions. It exists
because it predates the "roles" merger ruling.

**Related.** The settled-but-unimplemented intent to merge NodeSpecies
and NodeService into a single `roles: Vec<Role>` vector
(`psycheHorizon.md` section "NodeSpecies + NodeService role-merge")
would eliminate BehavesAs entirely: each CriomOS gate would check
`builtins.elem "Edge" node.roles` instead of `node.behavesAs.edge`.

**Severity.** Blocks a stated design (the roles merger). Duplicates a
source (species already encodes the information).

### F3. 16 is_* / has_* booleans in Node: Nix-derivable

**Evidence.** The Node struct carries 16 derived booleans
(`node.rs:78-93`):

- `is_fully_trusted` = `trust == Max`
- `is_remote_nix_builder` = `has_service(NixBuilder) && online && trusted && has_base_pub_keys`
- `is_dispatcher` = `!center && trusted && sized >= min`
- `is_nix_cache` = `has_service(NixCache) && online && trusted && has_base_pub_keys`
- `is_large_edge` = `sized >= large && edge`
- `enable_network_manager` = `sized >= min && !iso && !center && !router`
- `has_nix_pub_key`, `has_ygg_pub_key`, `has_ssh_pub_key`, `has_wireguard_pub_key`,
  `has_nordvpn_pub_key`, `has_wifi_cert_pub_key`, `has_base_pub_keys` = presence checks
- `has_video_output` = `edge`
- `chip_is_intel` = `arch == X86_64`
- `model_is_thinkpad` = model name check

Every one is a trivial derivation from fields already on the projected
Node. CriomOS consumes them as `horizon.node.isNixCache` etc. Nix could
compute any of these with a one-line `let` binding.

**Psyche statement departed from.** "Horizon should mostly be just the
reducer" (2026-05-17); "We don't need to put everything into Horizon,
especially really dumb stuff [...] We're just inflating the Rust code"
(2026-05-17). These booleans are exactly the "really dumb stuff" the
psyche identified.

**Severity.** Adds unasked machinery. Not blocking, but the volume is
large (16 fields that could each be a one-liner in Nix).

### F4. ComputerIs: 5 model-gating booleans

**Evidence.** `ComputerIs` (`node.rs:267-283`) is a struct of 5 booleans
(`thinkpad_t14_gen2_intel`, `thinkpad_t14_gen5_intel`, `thinkpad_x230`,
`thinkpad_x240`, `rpi3b`), derived from `machine.model` string matching
against the `KnownModel` enum. CriomOS reads `horizon.node.computerIs.*`
for hardware-specific config branches.

This is a closed set in the projection that must be extended (new Rust
enum variant + new boolean field + Rust rebuild) every time a new
hardware model needs a config branch -- the opposite of "a bunch of
dials."

**Psyche statement departed from.** Same as F2: variants over booleans.
The model is already a string; Nix can match on it directly.

**Severity.** Adds unasked machinery.

### F5. LidSwitchAction: policy in the projection

**Evidence.** `BehavesAs::lid_switch_policy()` (`node.rs:230-252`)
computes 3 systemd logind lid-switch actions from the species facets.
The Node struct carries `handle_lid_switch`, `handle_lid_switch_external_power`,
`handle_lid_switch_docked` (`node.rs:97-99`).

This is operational policy ("HOW to configure logind") embedded in the
data plane. The same logic is a trivial Nix `mkMerge [ (mkIf center
{ ... }) (mkIf edge { ... }) ]`.

**Psyche statement departed from.** "Horizon should be elegant and
minimal: express only what [...] never how" (2026-06-04); "ugliness
goes in Nix" (pre-reset principle).

**Severity.** Adds unasked machinery.

### F6. NodeSpecies (11 variants) vs NodeService (7 variants at origin/main): no overlap, but the roles merger is overdue

**Evidence.** NodeSpecies variants: `Center`, `LargeAi`,
`LargeAiRouter`, `Hybrid`, `Edge`, `EdgeTesting`, `MediaBroadcast`,
`Router`, `RouterTesting`, `TestVm`, `CloudNode`.

NodeService variants (origin/main c70915e): `TailnetClient`,
`TailnetController`, `NixBuilder`, `NixCache`, `PersonaDevelopment`,
`VmHost`, `WebHost`. (AgentIntercomLocal and AgentIntercomGraphical
were removed.)

There is no formal overlap, but they serve overlapping purposes: species
says "what the node IS" (implying BehavesAs facets), while services say
"what features it has." The psyche's ruled merger into a single
`roles: Vec<Role>` would unify both into one vector of self-describing
variants.

**Psyche statement departed from.** The pre-reset audit (2026-06-04,
`cloud-designer/23/1-intent-agglomerated-subject.md:276-299`)
identified a settled intent to merge these into `roles`. The psyche has
not deferred or reversed it.

**Severity.** Blocks a stated design.

### F7. AgentIntercomLocal on nodes without Claude/Codex -- RESOLVED at origin/main

**Status.** Resolved. At origin/main (goldragon `5bc563b`, horizon-rs
`c70915e`, CriomOS `45e83fb`), both AgentIntercomLocal and
AgentIntercomGraphical have been removed from the NodeService enum, from
all node entries in goldragon/datom.dotos, and from CriomOS's
agent-intercom gating. CriomOS now includes the agent-intercom package
unconditionally (no service gate). The psyche's ruling is enacted.

**Original evidence (local HEAD only).** `goldragon/datom.dotos`
declared `AgentIntercomLocal` on balboa, an Arm64 rock64 Center node
with size Zero.

### F8. AgentIntercomGraphical: already ruled slop -- RESOLVED at origin/main

**Status.** Resolved. Same commits as F7. The variant has been removed
from the NodeService enum and from goldragon's cluster data. CriomOS
`45e83fb` removes the service gates and re-gates consumers by what they
actually need (edge, edge.default.nix:+5).

### F9. datom.dotos is DOTOS, not Datom

**Evidence.** `goldragon/datom.dotos` and `criomos-horizon-config/
horizon.dotos` are both in DOTOS syntax (the legacy notation).
horizon-rs depends on the `dotos` crate (git pin in `Cargo.toml:10`),
not on the `datom` crate. No `.datom` files exist anywhere in the
ecosystem.

The psyche ruled: "There should be no Dotos files anymore" (2026-08-26,
`flows/01a03d6e/vision/dotosFiles.md`); "migrate everything to datom"
(2026-08-11, `psyche-raw/Vision/archive-threeStacks.md:54`).

The Datom crate exists at `/git/github.com/LiGoldragon/datom/` with
realize/textualize machinery, but horizon-rs has not migrated to it.

**Severity.** Blocks a stated design.

### F10. synchronizer.dotos references datom.nota -- nonexistent file

**Evidence.** `goldragon/synchronizer.dotos:47` references
`/git/github.com/LiGoldragon/goldragon/datom.nota`. That file does not
exist; the actual file is `datom.dotos`. The synchronizer config carries
a stale path from before a rename.

**Severity.** Cosmetic (the synchronizer may or may not be active).

### F11. LAN subnet dual definition

**Evidence.** The IPv4 LAN subnet `10.18.0.0/24` and gateway
`10.18.0.1` are defined in:

1. `criomos-horizon-config/horizon.dotos:8-9` (not consumed)
2. `CriomOS-lib/lib/default.nix:89-91` (consumed by CriomOS modules)

The psyche ruled: "there shouldnt be criome and criome.net in cluster
data -- those are horizon constants" (2026-05-17). The intent was for
these to live in the pan-horizon config and flow through the projection.
Instead, they are hardcoded in CriomOS-lib AND authored (but not read)
in criomos-horizon-config.

**Severity.** Duplicates a source.

### F12. Domain suffixes hardcoded in three places

**Evidence.** The internal suffix `criome` and public pattern
`<cluster>.criome.net` appear in:

1. `horizon-rs/lib/src/domain.rs:108` (`InternalDomainSuffix::default_criome() -> "criome"`)
2. `horizon-rs/lib/src/domain.rs:121` (`PublicClusterDomain::for_cluster() -> "<cluster>.criome.net"`)
3. `goldragon/datom.dotos:276` (`{criome [goldragon.criome.net]}`)
4. `criomos-horizon-config/horizon.dotos:6` (`(DomainSuffixes [criome] [criome.net])`)

The goldragon entry is the only one consumed. The horizon-rs defaults
serve as fallback. The criomos-horizon-config entry is dead.

**Severity.** Duplicates a source.

### F13. SSH matchBlock hardcoded with prometheus hostname

**Evidence.** `CriomOS-home/modules/home/profiles/min/default.nix:534-538`
hardcodes:
```nix
matchBlocks."prometheus.goldragon.criome prometheus" = {
  hostname = "prometheus.goldragon.criome";
```
This is cluster-specific data in a generic Home module.

**Psyche statement departed from.** "I don't want any node or
cluster-specific data in those repositories" (2026-05-10).

**Severity.** Blocks a stated design.

### F14. JSON handoff via generated flake.nix

**Evidence.** Lojix writes the horizon as:
```
{ outputs = _: { horizon = builtins.fromJSON (builtins.readFile ./horizon.json); }; }
```
(`schema_runtime.rs:4798`). This is a type-erased handoff: all Rust
typing is lost at the JSON boundary. Nix receives an untyped attrset
and trusts the field names and shapes.

**Psyche statement.** "Cluster-data features must be typed end-to-end"
(2026-06-04). The JSON handoff is a type gap. Signal/rkyv would be a
typed wire format; the psyche also said "datom is only used at the edge
to let text-based systems understand signal" (`flows/ac1e9ec8/vision/
datomSyntax.md:108-112`).

**Disconfirming.** Nix is inherently dynamically typed; there is no
way to pass a Rust-typed value directly into Nix evaluation without
serialization. JSON is the standard Nix interchange. The type gap is
at the Nix boundary, which is structural -- unless CriomOS is
rewritten, it will always receive an untyped attrset. The psyche's
"typed end-to-end" may accept JSON-to-Nix as the necessary edge.

**Severity.** Cosmetic / adds unasked machinery question. The JSON
handoff is likely the minimal viable bridge given Nix's type model.

### F15. Test fixtures duplicate production naming

**Evidence.** `horizon-rs/lib/tests/` uses cluster name `goldragon`,
node names `ouranos`, `prometheus`, domain patterns
`ouranos.goldragon.criome`, `goldragon.criome.net`. The keys are
synthetic (all-A patterns), but the naming matches production.

**Psyche statement departed from.** Not directly -- the psyche has not
ruled on test fixture naming. However, if goldragon were renamed or
restructured, these tests would be change-detectors on naming
rather than on behavior.

**Severity.** Cosmetic.

### F16. Positional bare booleans in datom.dotos

**Evidence.** Each node in `goldragon/datom.dotos` ends with a sequence
of positional bare atoms:
```
[]            -- link_local_ips
None          -- node_ip
None          -- wireguard_pub_key
True          -- nordvpn
False         -- wifi_cert
[]            -- wireguard_untrusted_proxies
False         -- wants_printing
True          -- wants_hw_video_accel
None          -- router_interfaces
None          -- online
[(services)]  -- services
```
(zeus, lines 145-155, is the clearest example.)

**Psyche statement departed from.** "give me a vector of variants, not
this meaningless series of booleans and options!" (2026-05-18); "all
this 'true none true' is fine from some stuff, but it's so lacking in
information" (2026-05-18). This is the exact shape the psyche reacted
to.

**Severity.** Blocks a stated design. The NodeProposal schema has 17
positional fields, many of which are `bool` or `Option<_>`. In Datom
these would at least have type-driven structure, but the underlying
schema design remains boolean-heavy.

### F17. Viewpoint-only fields: Nix-derivable cross-node data

**Evidence.** `builder_configs`, `cache_urls`, `ex_nodes_ssh_pub_keys`,
`dispatchers_ssh_pub_keys`, `admin_ssh_pub_keys`,
`image_exchange_pub_keys` (filled by `Node::fill_viewpoint`,
`node.rs:512-589`) are computed by walking sibling nodes. Each is a
collection or subset of fields already present on the sibling Node
objects, which Nix receives as `horizon.exNodes`.

Nix could derive any of these: `builder_configs` is `filter
isRemoteNixBuilder exNodes |> map mkBuilderConfig`; `cache_urls` is
`filter (n: n.nixUrl != null) exNodes |> map (n: n.nixUrl)`. The Rust
code precomputes them to save Nix from doing the fold.

**Psyche statement.** "Horizon should mostly be just the reducer"
(2026-05-17). The viewpoint fill is the "just inflate it in Rust"
machinery the psyche identified as unnecessary.

**Disconfirming.** The `BuilderConfig` struct embeds business logic
(ssh_user = "nix-ssh", ssh_key = host key path, supported_features)
that Nix would also need. Moving this to Nix moves the logic, not
eliminates it. The question is whether "prefer beautiful Horizon over
beautiful Nix" extends to viewpoint convenience fields.

**Severity.** Adds unasked machinery / duplicates what Nix could derive.

### F18. Yggdrasil addresses derivable from public keys

**Evidence.** Each node in `datom.dotos` declares a Yggdrasil public
key, an address (200:...), and a subnet prefix (300:...). The address
and subnet are cryptographically derived from the public key --
deterministic and redundant.

`address.rs:67` notes: "Free-form today -- not a parsed CIDR -- because
the legacy data carries it as the bare prefix without a prefix length.
Promote to Ipv6Net when goldragon emits canonical CIDRs."

**Severity.** Duplicates a source. Minor, but a correct projection
engine would derive these from the key.

### F19. All trust entries are Max (redundant)

**Evidence.** `datom.dotos:262-270` sets every node's trust to Max, and
the cluster default is also Max (line 262). The per-node entries are
therefore no-ops. Similarly, user `li` has trust Max, and bird has
trust Medium -- only bird's entry carries information.

**Severity.** Cosmetic.

## 3. Disconfirming evidence

### F1 (dead pan-horizon config)

The strongest counter-case: the DomainConfiguration is inside the
ClusterProposal, so the cluster file IS feeding domain info to the
projection. The pan-horizon config was meant to carry values shared
across clusters (federation), and since there is only one cluster
(goldragon), the current shape works. Counter-counter: the psyche
explicitly created the repo for federation, and its data (LAN subnet,
DHCP pool) has no consumer path. The counter does not survive: the
repo is architecturally dead regardless of current functionality.

### F2-F4 (derived booleans)

Counter: BehavesAs and is_* booleans are a stable contract between
horizon-rs and CriomOS. Moving derivation to Nix would scatter the
logic across dozens of modules, and a single Rust derivation is easier
to test. Counter-counter: the psyche explicitly rejected this reasoning
("We're just inflating the Rust code") and ruled that "ugliness goes
in Nix." The derivation table is small enough to be a single Nix
`let` block. The counter does not survive the psyche's explicit ruling.

### F5 (lid-switch policy)

Counter: lid-switch policy is only 3 fields and is tightly coupled to
species. Counter-counter: it is pure operational policy (HOW to
configure logind) and the psyche said "never HOW." Does not survive.

### F7-F8 (AgentIntercom) -- RESOLVED

Already enacted at origin/main. No disconfirming evidence needed.

### F9 (DOTOS not Datom)

Counter: the datom crate may not yet support the full ClusterProposal
schema; migrating requires porting all derive macros. Counter-counter:
the psyche said "There should be no Dotos files anymore" without
exception. The migration is ordered; the pace is not. This finding
stands as stated, with the caveat that the datom crate's readiness
is an unknown.

### F14 (JSON handoff)

Counter: Nix has no typed wire format; `builtins.fromJSON` is the
standard bridge. All Nix flake inputs are untyped. Counter-counter:
the psyche said "datom is only used at the edge" and the Nix
boundary IS the edge. The JSON handoff is likely the terminal design
for the Nix consumer, even if internal transport moves to Signal/rkyv.
The counter survives. Reclassified as cosmetic.

### F17 (viewpoint fields)

Counter: precomputed viewpoint fields save Nix from repeating the
fold logic in every consuming module. Counter-counter: Nix repeats
nothing if the fold is in criomos-core (the shared interpretation
layer). The counter partially survives: a shared Nix interpretation
layer does not yet exist, so the precomputation avoids duplication
today. But the terminal design has criomos-core, making these
fields transitional.

## 4. End-shape

### The authored cluster file (Datom)

```
;; goldragon cluster proposal, Datom syntax

.ClusterProposal{
  Map.(
    ouranos.Node{
      [.Edge .LargeDesktop]        ;; roles: Vec<Role>
      {.Metal .X86_64 12           ;; machine (species, arch, cores)
        .ThinkPadT14Gen5Intel      ;; model
        .Colemak .Uefi}            ;; keyboard, bootloader
      Map.(                        ;; disks
        /.Disk{/dev/disk/by-uuid/38a88e99... .Ext4}
        /boot.Disk{/dev/disk/by-uuid/725A... .Vfat})
      {ssh-ed25519-key             ;; pubkeys (ssh, nix, ygg)
        nix-signing-key
        ygg-pub-key}
    }
    ;; ... other nodes
  )
  Map.(                            ;; users
    li.User{.Unlimited .Colemak .Emacs
      Map.(ouranos.UserKeys{ssh-key gpg-keygrip})}
  )
  .ClusterTrust{.Max}              ;; trust (just the default)
}
```

No booleans at data positions. No `None`. No `True`. Each node
carries a `roles` vector of self-describing Role variants. Machine
facts are a compact struct. Services like NixBuilder, NixCache are
Role variants carrying their tuning data. AgentIntercom is absent
(derived from Claude/Codex presence in CriomOS).

### What the reducer emits

```
Horizon {
  cluster: { name, domain_configuration, trusted_build_pub_keys }
  node: {
    name, roles, machine, io, pubkeys,
    criome_domain_name, system
  }
  ex_nodes: { <name>: { name, roles, machine, pubkeys,
                         criome_domain_name, system } }
  users: { <name>: { name, species, size, keyboard, style,
                      preferred_editor, pub_keys } }
}
```

No derived booleans. No BehavesAs. No ComputerIs. No LidSwitchAction.
No is_*. No has_*. No builder_configs. No cache_urls. No
admin_ssh_pub_keys. The Node has ~15 fields, not ~54.

### What Nix derives (in criomos-core)

```nix
# criomos-core/lib/horizon.nix
{
  isEdge = n: builtins.elem "Edge" n.roles;
  isCenter = n: builtins.elem "Center" n.roles;
  isRouter = n: builtins.elem "Router" n.roles;
  isLargeAi = n: builtins.elem "LargeAi" n.roles;
  isNixBuilder = n: builtins.elem "NixBuilder" n.roles;
  builderConfig = n: { ... };  # from n.pubkeys + n.criomeDomainName
  cacheUrls = exNodes: ...;
  lidSwitchPolicy = n: ...;    # from roles
}
```

### Where pan-horizon constants live

`criomos-horizon-config` becomes a real input to horizon-rs. The
`HorizonProposal` is read alongside the `ClusterProposal`. Domain
suffixes, LAN config, and any future federation constants flow from
this repo, not from hardcoded defaults.

### Data-flow diagram (end-shape)

```
goldragon/cluster.datom           criomos-horizon-config/horizon.datom
 (roles, machine, pubkeys,         (domain suffixes, LAN config,
  users, trust)                     operator identity)
       |                                    |
       v                                    v
  horizon-rs (datom crate, not dotos)
  ClusterProposal + HorizonProposal -> Horizon
  reducer only: pass-through + domain derivation + trust resolution
  ~15 fields per node, ~10 per user
       |
       v
  Horizon (Signal/rkyv internal; JSON at the Nix edge)
       |
       v
  lojix writes content-addressed flake (JSON -> builtins.fromJSON)
       |
       v
  criomos-core (Nix): pure interpretation layer
  derives: isEdge, isNixBuilder, builderConfig, cacheUrls, etc.
       |                                    |
       v                                    v
  CriomOS (OS modules)              CriomOS-home (user modules)
  reads horizon.node via              reads horizon.users via
  criomos-core helpers                criomos-core helpers
```

### Vertical-slice migration (no compatibility path)

Step 3 (remove AgentIntercom) is already done at origin/main.

1. Add `HorizonProposal` reading to horizon-rs; wire
   criomos-horizon-config as a second input. Remove hardcoded domain
   defaults from `domain.rs`.
2. Merge NodeSpecies + NodeService into `roles: Vec<Role>` in
   horizon-rs. Remove BehavesAs, ComputerIs, is_*, has_*,
   LidSwitchAction from the output Node.
3. Migrate goldragon and criomos-horizon-config from `.dotos` to
   `.datom`; switch horizon-rs from the `dotos` crate to the `datom`
   crate.
4. Create `criomos-core` with the Nix interpretation layer; move all
   derivation logic (behavesAs equivalent, builder_configs, cache_urls,
   lid-switch, is_*, ComputerIs) into it.
5. Update CriomOS and CriomOS-home to use criomos-core helpers instead
   of direct field reads for derived values.
6. Remove LAN subnet from CriomOS-lib (it comes from pan-horizon
   config via the projection).
7. Remove the prometheus SSH matchBlock from CriomOS-home; derive it
   from horizon.exNodes in criomos-core.
8. Fix `synchronizer.dotos` reference from `datom.nota` to the current
   filename.

## 5. Unknowns

- Whether the `datom` crate is ready to handle the full
  `ClusterProposal` schema (derive macros, all types).
- Whether `criomos-core` has been started or remains a concept.
- Whether the roles merger intent (NodeSpecies + NodeService -> roles)
  has been re-confirmed or silently shelved by the living psyche.
- The exact shape of the Datom syntax for the cluster file -- whether
  it matches the sketch above or whether the living psyche has a
  different preference.
- Whether `MediaBroadcast` and `RouterTesting` species variants are
  used by any node (they are not in goldragon's current cluster data).
- Whether `criomos-horizon-config` was ever consumed by an earlier
  version of horizon-rs or lojix (the repo exists, implying it was
  created for a purpose, but no consumer code was found).
- Whether the living psyche considers the JSON handoff to Nix
  acceptable as the terminal design for the Nix edge, or whether a
  tighter typed bridge is wanted.

## Sources

### Code read (witness)

- `/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs` -- Node struct (54 fields), BehavesAs (11 bools), ComputerIs (5 bools), BuilderConfig (9 fields), projection logic, viewpoint fill
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/species.rs` -- NodeSpecies (11 variants), NodeService (9 variants, in proposal.rs)
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/domain.rs` -- DomainConfiguration, hardcoded defaults (criome, criome.net)
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/user.rs` -- User struct (~20 fields)
- `/git/github.com/LiGoldragon/horizon-rs/cli/src/main.rs` -- CLI: stdin dotos, stdout JSON, --cluster, --node
- `/git/github.com/LiGoldragon/horizon-rs/Cargo.toml` -- depends on dotos crate (git pin)
- `/git/github.com/LiGoldragon/goldragon/datom.dotos` -- 8 nodes, 2 users, 276 lines
- `/git/github.com/LiGoldragon/goldragon/synchronizer.dotos` -- references `datom.nota` (nonexistent)
- `/git/github.com/LiGoldragon/criomos-horizon-config/horizon.dotos` -- 12 lines, domain suffixes + LAN
- `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix` -- constants including LAN subnet
- `/git/github.com/LiGoldragon/CriomOS/flake.nix` -- no criomos-horizon-config input; horizon = stub
- `/git/github.com/LiGoldragon/CriomOS/stubs/no-horizon/flake.nix` -- stub that throws
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs` -- lines 4570-4798: proposal loading, projection, materialization, JSON flake generation

### Psyche (written psyche, tentative)

- `flows/674a4dab/reports/psycheHorizon.md` -- primary acquisition source
- `flows/01a03d6e/vision/dotosFiles.md` -- "There should be no Dotos files anymore"
- `flows/01a048a6/vision/agentIntercomGraphical.md` -- AgentIntercomGraphical is slop, flag must be removed
- `flows/01a04881/vision/agentIntercomGraphical.md` -- "this agentintercomgraphical is slop"
- `Vision/datom.md` -- Datom syntax and nature
- `Vision/protos.md` -- direction (realize/textualize)

### Agent-authored maps (claims, not witnesses)

- `flows/674a4dab/witnesses/rustSideMap.md` section 2
- `flows/674a4dab/witnesses/nixSideMap.md` section 2

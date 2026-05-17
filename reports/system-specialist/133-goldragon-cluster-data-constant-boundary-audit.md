# 133 — Goldragon Cluster Data / Constant Boundary Audit

*Follow-up to `reports/system-specialist/132-horizon-domain-constants-not-cluster-data.md`. Scope: inspect `goldragon/datom.nota` for values that are currently authored as cluster data but look like Horizon or CriomOS constants, defaults, or derivable implementation policy.*

## Boundary Rule

A value belongs in cluster data only when a cluster operator would meaningfully vary it between clusters or between nodes in the same cluster.

If every CriomOS cluster should use the same value because the platform expects it, the value belongs in Horizon or CriomOS as a typed constant or default. If the value is derived from already-authored data, the derived value belongs in projection code. If the value is an external provider catalog, it belongs in a package/catalog source, not in the cluster proposal.

User correction after the first draft: every value audited in this report is outside cluster data. The owner is either Horizon (identity-derived values) or CriomOS (runtime/provider implementation and defaults). Cluster data may select a provider/profile, but it must not carry the provider's implementation catalog.

## Strong Findings

### 1. Internal/public domain suffixes

Already recorded in report 132.

Current data:

- `datom.nota:476` — `"criome"`
- `datom.nota:481` — `"criome.net"`

These are Horizon/CriomOS constants, not `goldragon` facts. `ClusterProposal::domain` and `ClusterProposal::public_domain` should disappear from the input boundary. Horizon should derive:

- node domain: `<node>.<cluster>.criome`
- public user domain: `<cluster>.criome.net`

### 2. Tailnet base domain

Current data:

- `datom.nota:299` — `(TailnetConfig "tailnet.goldragon.criome" None)`

This repeats three facts that Horizon already has or should own:

- `tailnet` — platform-reserved subdomain label;
- `goldragon` — the cluster name passed to the projection viewpoint;
- `criome` — the internal Horizon/CriomOS suffix.

The `TailnetConfig` input should not carry `base_domain` unless tailnet is allowed to use an independently chosen DNS suffix. The clean shape is:

- cluster data says whether a tailnet exists and carries optional TLS trust material;
- Horizon derives `tailnet.<cluster>.criome` when projecting the cluster;
- tests assert that changing the cluster name changes the derived tailnet domain without editing `datom.nota`.

The `tls` field is different: public CA/server certificate material is real cluster trust data and can stay.

### 3. Router Wi-Fi SSID

Current data:

- `datom.nota:120` — `(RouterInterfaces ... (SecretReference "router-wifi-sae-passwords" WifiPassword) "criome" "PL")`

Decision: router SSID is derived by Horizon from the cluster name and the internal CriomOS suffix. For `goldragon`, the SSID is:

```text
goldragon.criome
```

The SSID is therefore not an authored field in `goldragon/datom.nota`. `RouterInterfaces` should not carry an SSID string unless the system later grows an explicit override field. The normal projection should derive `<cluster>.criome` from the same Horizon-owned internal suffix used for node domains.

The same record also carries `"PL"` as Wi-Fi regulatory country. That is not a CriomOS constant. It is location/regulatory data or a host/site policy. It should not be collapsed into a constant.

## CriomOS Defaults Or Horizon Derivations

### 4. Resolver upstream/fallback policy

Current data:

- `datom.nota:287-290` — Cloudflare/Quad9 upstreams/fallbacks and listen addresses.

The public resolver set is CriomOS DNS policy, not `goldragon` identity. It should not be authored in cluster data.

The listen addresses are more clearly derivable:

- `::1` and `127.0.0.1` are local service constants;
- `10.18.0.1` is the LAN gateway and should derive from the LAN policy instead of being repeated in resolver data.

Recommended shape:

- CriomOS owns the typed resolver policy;
- listen addresses derive from loopback plus router LAN gateway.

### 5. LAN prefix and derived pieces

Current data:

- `datom.nota:276` — `10.18.0.0/24`
- `datom.nota:277` — `10.18.0.1`
- `datom.nota:278` — DHCP pool `10.18.0.100` to `10.18.0.240`
- `datom.nota:279` — lease TTL `4000`

None of these belong in cluster data. Horizon should derive a stable LAN prefix from cluster/router identity, for example by hashing a versioned namespace plus the cluster name and router node name into an RFC1918 prefix. CriomOS then derives service-level addresses from that prefix:

- CIDR: Horizon-derived from cluster + router identity;
- gateway: first usable address in the selected prefix;
- DHCP pool: derived from the prefix using CriomOS router policy;
- lease TTL: CriomOS service default.

Recommended shape:

- cluster data carries no LAN CIDR/gateway/pool/listen/TTL fields;
- Horizon projects the derived network identity;
- CriomOS consumes the projected prefix and applies router defaults.

### 6. Local AI provider protocol/port/base path

Current data:

- `datom.nota:309-310` — provider `"criomos-local"`, protocol `OpenAiCompat`, port `11434`, base path `"/v1"`.

Those values are the CriomOS local AI router interface, not cluster facts. The cluster fact is that `prometheus` provides local AI capacity. The protocol/port/base path derive from the CriomOS service implementation.

Recommended shape:

- cluster data selects the provider/profile and names the serving node;
- CriomOS owns the default local-AI endpoint contract;
- provider name can derive from service/profile instead of being a hand-authored string.

### 7. AI model catalog and source URLs

Current data:

- `datom.nota:312-401` — model IDs, descriptors, Hugging Face URLs, hashes, filenames, context windows, and token limits.

This is a CriomOS/Nix model catalog. It is not cluster data. The user has already drawn this boundary: open-source model availability does not belong in Horizon and can live in Nix code. The cluster should choose which provider/profile a node serves, not carry every model URL and hash inline.

Recommended shape:

- move open-source model catalog entries to a CriomOS/CriomOS-home package or a dedicated model-catalog repo consumed by Nix;
- cluster data selects provider/profile variants;
- keep secret-backed cloud provider credentials in cluster secret bindings when cloud providers are added.

### 8. Local AI serving implementation defaults

Current data:

- `datom.nota:412` — `(AiServingConfig 1 300 99 true true Off 1 "11.5.1" 110 100)`

These are CriomOS runtime implementation defaults or hardware-derived workarounds:

- `max_loaded_models`, idle unload seconds, mmap/warmup flags, fit mode, and parallelism look like CriomOS service defaults.
- `gpu_override = "11.5.1"` is a hardware/driver workaround and should be derived from the machine/GPU model in CriomOS, not typed into cluster data.
- memory high/max values are host resource policy and should derive from machine capacity or a CriomOS resource profile.

Recommended shape:

- CriomOS owns local-AI runtime defaults;
- hardware quirks live with machine-model support;
- cluster data only selects the provider/profile.

### 9. NordVPN catalog

Current data:

- `datom.nota:430` — NordVPN DNS servers;
- `datom.nota:431` — WireGuard client address and port;
- `datom.nota:433-468` — NordVPN server catalog entries with hostnames, endpoints, public keys, countries, and cities.

This is CriomOS provider configuration and provider catalog data. It is not Horizon data, and it is not cluster data. The cluster data only selects VPN providers through a vector of typed provider variants. Each provider-selection variant carries operator preference data such as favored server location or region, plus the secret reference needed to authenticate. The provider implementation, DNS settings, WireGuard client defaults, server inventory, generated endpoints, public keys, and NetworkManager shape live in CriomOS.

Recommended shape:

- cluster data carries something shaped like a vector of provider selections, for example `[(Nordvpn { credentials, favored_locations })]`;
- CriomOS owns NordVPN DNS defaults, WireGuard client defaults, server catalog, and NetworkManager configuration;
- the operator tool regenerates the CriomOS provider catalog artifact, not the cluster datom by hand.

## Data Outside This Audit

The audited values above all leave cluster data. Separate from this audit, the following still look like genuine cluster facts because they identify actual nodes, users, trust, keys, hardware, placement, or secrets:

- node names and species;
- trust levels;
- hardware model, CPU count, RAM, disk UUIDs, mount layout, swap devices;
- SSH/Nix/Yggdrasil public keys and addresses;
- link-local and node IP assignments;
- router interface names;
- Wi-Fi regulatory country;
- user names, user public keys, keygrips, keyboard/editor/text-size preferences;
- secret names and secret references;
- optional TLS trust material for tailnet or other services.

## Schema Direction

The clean shape is not "move every literal out of `goldragon`." The clean shape is to separate four categories:

1. **Horizon derivations/constants:** `criome`, `criome.net`, node domains, tailnet domain, router SSID `<cluster>.criome`, hash-derived LAN prefix.
2. **CriomOS defaults/runtime:** resolver providers, DNS listen loopbacks, router gateway/pool convention, service ports, service base paths, service runtime defaults, local-AI runtime shape, VPN implementation shape.
3. **CriomOS/catalog data:** open-source model sources and NordVPN server inventory.
4. **Cluster data:** node inventory, trust, keys, hardware/deployment facts, secret references, and typed provider/profile selections.

Horizon should project constants and derived values. CriomOS should own service defaults. Catalogs should be packaged or generated. `goldragon` should stay the cluster's authored facts and typed provider/profile selections.

## Suggested Tests

Add source-boundary tests so this does not regress:

- `goldragon/datom.nota` must not contain `"criome.net"`.
- `goldragon/datom.nota` must not contain a tail `ClusterProposal` domain field.
- `goldragon/datom.nota` must not contain `tailnet.goldragon.criome`.
- `goldragon/datom.nota` must not contain a router SSID literal.
- projected router data for cluster `goldragon` emits SSID `goldragon.criome`.
- `goldragon/datom.nota` must not contain LAN CIDR, gateway, DHCP pool, resolver listens, or lease TTL.
- projected JSON still contains `.goldragon.criome` and `.goldragon.criome.net` where consumers need them.
- projected router/network data contains a deterministic LAN prefix derived from the cluster/router identity.
- resolver listen addresses include loopback and the derived LAN gateway.
- local AI provider projection still emits the CriomOS service endpoint when the cluster only marks a node as local-AI provider.
- cluster VPN data is only a vector of provider-selection variants; CriomOS supplies provider implementation and catalog details.

## Immediate Pickup Order

1. Extend report 132's domain-suffix cleanup to include tailnet base-domain derivation.
2. Remove router SSID from cluster-authored data and derive `<cluster>.criome` in Horizon.
3. Remove LAN/resolver records from cluster-authored data; derive LAN identity in Horizon and runtime defaults in CriomOS.
4. Move AI model catalog and local runtime configuration out of `goldragon`.
5. Move NordVPN configuration and server inventory out of `goldragon`; leave only typed provider selections with preferences and credential references.

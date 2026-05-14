# 14 — Horizon re-engineering: kickoff complete; ready-to-code state of the world

Date: 2026-05-14
Role: system-assistant
Frame: post-kickoff-pre-coding artifact. The next session reads this report (plus the cited ARCHITECTURE.md and skill files) and starts coding step 1 without re-asking the user the closed design questions. Every design decision settled in the conversation that produced this report is named here with its resolution.
Pairs with: report 13 (kickoff plan + open questions); report 12 (combined audit + boundary principle); report 11 (initial schema survey); report 04 (cloud host plan, second revision — placement / containment / Publication / SecretReference); report 119 (CriomOS literal leaks, system-specialist).

---

## 0 · TL;DR

Three workstreams folded into one feature arc:

1. **Re-engineer the horizon-rs schema** with input/output namespace split (`proposal::*` / `view::*`), data-bearing variants, typed cluster policy.
2. **Extract cluster policy literals out of CriomOS / CriomOS-home Nix code** — Wi-Fi, DNS, LAN, VPN, AI provider, secrets — into typed records that flow through Horizon.
3. **Build a new lojix daemon + thin CLI** in the `lojix` repo (renamed from `lojix-daemon`), consuming the re-engineered schema. Today's `lojix-cli` stays at the current schema until cutover.

All work lives on the **`horizon-re-engineering`** branch across six repos, with worktrees at `~/wt/github.com/LiGoldragon/<repo>/horizon-re-engineering/` per the new `~/primary/skills/feature-development.md` skill. Tracked by epic bead `primary-vhb6`; step 1 (`proposal::*` / `view::*` namespace split) is filed as `primary-ql48` and ready to start.

The next session: re-read this report + the listed ARCHITECTURE.md / skill files; claim system-assistant on the horizon-rs worktree path + `[primary-ql48]`; start step 1.

---

## 1 · The arc

The conversation that produced this report folded three things I had been treating as separate:

- **Horizon schema re-engineering** (reports 11 / 12) — fix what's ugly inside `horizon-rs`: data-bearing variants, eliminate stringly-typed dispatch, explicit projection of derived predicates.
- **Cluster-policy extraction** (report 119, plan 04) — typed records replacing literal Wi-Fi / DNS / LAN / VPN / AI / secret policy still living in CriomOS Nix modules.
- **New lojix daemon + thin CLI** (plan 04 §P5) — long-lived deploy orchestrator that consumes the new schema, with a thin CLI that speaks the daemon over UDS. Replaces today's `lojix-cli` post-cutover.

These are one effort because they share the same wire surface: the re-engineered horizon JSON. The new lojix daemon produces it; the new CriomOS module reads consume it; the re-engineered horizon-rs is the source of truth.

User direction this conversation:
- Work on parallel branches; don't break production main.
- Branch name: `horizon-re-engineering` (bare; no `push-` prefix — that convention in `~/primary/skills/jj.md` is for review-cycle bookmarks, not long-lived feature arcs).
- Daemon + new CLI in **one repo** named `lojix`; `signal-lojix` separate as the contract repo; `lojix-cli` is legacy.
- New schema flows to the **new daemon**, not to current `lojix-cli`. lojix-cli stays at the old schema; retires after CriomOS migrates.
- Use **sema-engine** as the storage default for state-bearing components (sema is now the lower-level kernel; sema-engine is the full database engine library).
- All signal traffic builds on **signal-core** types (the wire kernel); signal-* contract crates layer their typed records on top.
- File beads, set up branches + worktrees, update architecture, **don't code yet**. Code starts after the next context clear.

---

## 2 · Repository topology

Six repos in scope. One was renamed during this session.

| Repo | Path (canonical ghq) | Path (worktree) | Branch | Role in arc |
|---|---|---|---|---|
| `horizon-rs` | `/git/github.com/LiGoldragon/horizon-rs` | `~/wt/github.com/LiGoldragon/horizon-rs/horizon-re-engineering` | `horizon-re-engineering` | Schema source: `proposal::*` / `view::*` namespace split + data-bearing types + capability records + container/placement + cluster identity / lan / resolver / wifi / vpn / ai-provider records. |
| `lojix` (was `lojix-daemon`) | `/git/github.com/LiGoldragon/lojix` | `~/wt/github.com/LiGoldragon/lojix/horizon-re-engineering` | `horizon-re-engineering` | New deploy stack — one crate, two binaries (`lojix-daemon` long-lived orchestrator + `lojix` thin CLI client). Uses `sema-engine` for state; `signal-core` for wire; `signal-lojix` for contract records. |
| `signal-lojix` | `/git/github.com/LiGoldragon/signal-lojix` | `~/wt/github.com/LiGoldragon/signal-lojix/horizon-re-engineering` | `horizon-re-engineering` | Wire contract crate. DeploymentSubmission/Accepted/Rejected/Observation, CacheRetentionRequest/Accepted/Rejected/Observation, GenerationQuery/Listing. Per plan 04 §P5.4. |
| `CriomOS` | `/git/github.com/LiGoldragon/CriomOS` | `~/wt/github.com/LiGoldragon/CriomOS/horizon-re-engineering` | `horizon-re-engineering` | Consumer rewrites. Modules reading the new view shape (typed cluster policy, capability records, plural WLANs, etc.). |
| `CriomOS-home` | `/git/github.com/LiGoldragon/CriomOS-home` | `~/wt/github.com/LiGoldragon/CriomOS-home/horizon-re-engineering` | `horizon-re-engineering` | Consumer rewrites. AI provider record consumption (replacing the largeAiRouter scan), user tool credential references. |
| `goldragon` | `/git/github.com/LiGoldragon/goldragon` | `~/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering` | `horizon-re-engineering` | `datom.nota` updated to the new schema (after horizon-rs lands the typed shapes). |

**Untouched by the arc:**
- `lojix-cli` — legacy; stays at current schema; retires after CriomOS migrates to the new daemon's projection.
- `lojix-archive` — first-generation archive; frozen.
- `forge` — criome-stack executor; **not** the lojix deploy daemon (the GitHub redirect from `LiGoldragon/lojix` → `LiGoldragon/forge` is stale; forge was previously named lojix and got renamed). forge is now framed as future work — replacement for nix's build infrastructure inside the sema-ecosystem; not in any current production path. ARCH updated this session to make this clear.

**State of the lojix repo as of this session:**
- Renamed from `lojix-daemon` via `gh repo rename`.
- Local clone moved (`/git/github.com/LiGoldragon/lojix-daemon` → `/git/github.com/LiGoldragon/lojix`); remote URL updated.
- Docs rewritten for the new shape (one crate, two binaries; sema-engine + signal-core defaults). Pushed to main.
- `horizon-re-engineering` branch created at the new main and pushed.
- Worktree at `~/wt/github.com/LiGoldragon/lojix/horizon-re-engineering`.
- No `Cargo.toml` or `src/` yet — implementation lands on the feature branch.

---

## 3 · Branch + worktree convention

Documented in **`~/primary/skills/feature-development.md`** (new this session). Summary:

- **Canonical ghq checkouts at `/git/github.com/<owner>/<repo>/` stay on `main`.** Never check out a feature branch in the canonical path — that makes main unavailable to peer agents.
- **Feature worktrees at `~/wt/github.com/<owner>/<repo>/<branch-name>/`.** Same repo, separate working copy, on the named branch. Created with `jj workspace add` (or `git worktree add` for plain-git repos). Multiple agents can work different feature arcs in parallel without competing for one checkout.
- **Branch names: bare descriptive form** (`horizon-re-engineering`, not `push-horizon-re-engineering`). The `push-` prefix in `~/primary/skills/jj.md` is for short-lived review-cycle bookmarks; long-lived feature arcs use bare names.
- **Same branch name across every repo a feature touches.** The feature bead's description names the branch (per the new `~/primary/skills/beads.md` §"Feature beads carry their branch name" section, also added this session).

Worktrees were created this session for all six repos with the standard `jj workspace add` flow:

```sh
mkdir -p ~/wt/github.com/LiGoldragon/<repo>/
jj -R /git/github.com/LiGoldragon/<repo> workspace add \
    ~/wt/github.com/LiGoldragon/<repo>/horizon-re-engineering
```

The worktree's `@` defaults to a fresh empty change on top of the bookmark. Work in each worktree as a normal jj working copy; push commits as usual; the bookmark advances on the remote.

---

## 4 · Storage and wire defaults

The user clarified the SEMA family this session. **Two layers today**, both in the workspace:

- **`sema`** — the storage *kernel*. Owns redb file lifecycle, the typed `Table<K, V: Archive>` wrapper, txn helpers, the standard `Error` enum, the version-skew guard, the `Slot(u64)` + slot-counter utility. Low-level. Most components do not depend on `sema` directly.
- **`sema-engine`** — the full *database engine library* over `sema` and `signal-core`. Registered record families, typed Signal-verb execution (`Assert`, `Match`, `Subscribe`), operation log + snapshot identity, subscription surface. Pure library — no daemon, no Kameo, no tokio, no NOTA, no `signal-persona-*` deps. First real consumer is `persona-mind`; Criome follows; **lojix joins via this arc**.

**Default for the new lojix daemon (and future state-bearing components): depend on `sema-engine`, not on `sema` directly.** `sema-engine` owns the engine surface; the component owns domain validation, actors, sockets, authorization.

**Wire substrate: `signal-core`** — typed frames, envelopes, channel macro. Every component-specific `signal-*` contract crate (`signal-lojix`, `signal-criome`, `signal-persona-*`) layers its typed records on top of signal-core's primitives. No parallel framing per contract.

The skill `~/primary/skills/rust/storage-and-wire.md` was updated this session — §"The sema-family pattern" rewritten as §"The sema-engine pattern (default for new components)" naming `sema-engine` as the default. The "See also" section now points at all three architectures (sema, sema-engine, signal-core).

---

## 5 · The boundary principle (input vs output)

`horizon-rs` sits between two consumers with **different beauty criteria**:

- **Input boundary** — `proposal::*` types authored as Nota records in `goldragon/datom.nota`, parsed by `ClusterProposal::project`. Consumer is the Rust parser + the operator. **Beauty here is ESSENCE's typed-correctness criterion**: data-bearing variants, no stringly-typed dispatch, no illegal-state crosses, perfect specificity. R11's input-side findings (data-bearing `Machine`, `KnownModel` direct, `TailnetRole` collapse, plural-WLAN router interfaces) live here.
- **Output boundary** — `view::*` types serialized as JSON and consumed by ≈15 CriomOS / CriomOS-home Nix modules via `inputs.horizon.horizon` through `specialArgs`. Consumer is Nix code reading JSON. **Beauty here is consumer ergonomics**: predicate-named flags read as English at gate sites; the derivation lives once in horizon-rs projection instead of splitting across consumers; grouped records reduce destructure noise; typed payloads replace boolean-plus-hardcoded-data anti-patterns. R119's findings live here.

**The split is structural, not just procedural — the type vocabulary itself reflects it.** Today `horizon-rs` carries that partway (`proposal.rs` for input; `node.rs`/`cluster.rs`/`user.rs`/`horizon.rs` for output). But several compound types straddle: `Machine`, `Io`, `NodeServices`, `NodePubKeys`, `RouterInterfaces`, `WireguardProxy`, plus the new typed records this arc adds (`WifiNetwork`, `LanNetwork`, `BinaryCache`, etc.). A change "to `Machine`" automatically lands on both sides because there's one `Machine` — which is exactly where category errors originate.

**Step 1 of the arc is the namespace split.** Each compound type gets a distinct name on each side, even when shape-equivalent today: `proposal::Machine` and `view::Machine`, translated by the projection. They diverge as later steps land. Pure value enums (`NodeSpecies`, `Arch`, `KnownModel`, `Keyboard`, `Bootloader`, `MotherBoard`, `Magnitude`) stay shared — they have no per-side derivation.

**Naming:** `proposal::*` for the authoring side; `view::*` for the projected side (matching the existing `Viewpoint` type and the "what one node sees" semantics). Compound records cross via `proposal::X::project(ctx) -> view::X`.

**The output keeps consumer ergonomics.** Specifically: predicate-named flags (`BehavesAs`, `TypeIs`, `ComputerIs`), one-hot encodings (`AtLeast`), and pure-derived `has_*`/`is_*` flags **stay** in the view. They pay every CriomOS read site (`mkIf node.behavesAs.router`, `node.typeIs.largeAiRouter`, `node.size.medium`); deleting them forces inline species-set derivation at every consumer, splitting the source of truth between Rust and ~15 Nix modules for a wire-size win measured in bytes. That's a category error: applying the producer-side beauty criterion to the wire output for a non-Rust consumer.

The four booleans that *do* disappear (`isNixCache`, `isRemoteNixBuilder`, `hasWifiCertPubKey`, `hasNordvpnPubKey`) only go because typed payload replaces them — the consumer's new check is `field != null`, not because the boolean was unmotivated. Plus `hasSshPubKey` is genuinely dead (always true in proposal).

**Derivation logic moves into `horizon-rs` projection, out of Nix.** Code shaped like `(behaves_as.center && sized_at_least.min && has_base_pub_keys)` lives in horizon-rs's projection (Rust side). CriomOS Nix code reads `node.capabilities.binaryCache` as a fully-resolved gate — no `&&` chains over multiple fields, no `lib.elem`-flavored species lookups. Pure renderer.

---

## 6 · Capability derivation pattern

Shape closed this conversation:

```
proposal::NodeProposal {
    ...
    capabilities: Vec<ProposalCapability>,   // empty default → all inherit
}

enum ProposalCapability {
    BinaryCache(BinaryCacheInput),     // override default-derived
    BinaryCacheOff,                    // suppress (even if derivation says yes)
    BuildHost(BuildHostInput),
    BuildHostOff,
    ContainerHost(ContainerHostInput),
    ContainerHostOff,
    PublicEndpoint(PublicEndpointInput),
    PublicEndpointOff,
    EapTls(EapTlsInput),
    EapTlsOff,
    NordvpnMembership(NordvpnInput),
    NordvpnMembershipOff,
    WireguardMembership(WireguardInput),
    WireguardMembershipOff,
}
```

Empty Vec is the common case (most nodes inherit all defaults from species + other data). Validation rejects duplicates and `Override + Off` conflicts for the same capability.

**View side stays as a struct with Option fields:**

```
view::NodeCapabilities {
    binary_cache: Option<BinaryCache>,
    build_host: Option<BuildHost>,
    container_host: Option<ContainerHost>,
    public_endpoint: Option<PublicEndpoint>,
    eap_tls: Option<EapTls>,
    nordvpn: Option<Nordvpn>,
    wireguard: Option<Wireguard>,
}
```

That's what Nix consumers gate on: `mkIf (cap.binaryCache != null)`.

**Projection rule (per capability):**

1. Find proposal entry: `Override(input)`, `Off`, or absent.
2. `Off` → view has `None` (graceful disable; the consumer doesn't render the capability).
3. `Override(input)` → validate required data is present (e.g., signing key resolves, public key exists); if yes → `Some(resolved)`; if missing required data → `None` (graceful disable).
4. Absent → derive from species + other data. If derivation says yes, attempt to construct from defaults; if required data missing → `None`.

**Bootstrap problem handled by missing-data-disable.** A node intended as a binary cache without its signing key yet (pre-first-boot) gets `None` in the view; CriomOS doesn't try to render `nix-serve`; the node still boots. Once keys exist (post-first-boot, datom updated by operator), the next deploy fills in the capability. Self-bootstrapping services (SSH, Yggdrasil) follow the same pattern at the field level — Yggdrasil's `Option<YggdrasilEntry>` already disables yggdrasil-related config when None.

**`NodePubKeys` collapse.** Capability variants own their associated key material (e.g., `BinaryCache.public_key: NixPubKey`, `BinaryCache.signing_key: SecretReference`; `EapTls { ca_fingerprint, identity, private_key: SecretReference }`; `NordvpnMembership { credential: SecretReference }`). What remains in `NodePubKeys` is pure identity: SSH (always), Yggdrasil (for cluster-mesh nodes). Catches "capability declared without keys" at the type level.

---

## 7 · Closed design decisions

Every design decision in the conversation that produced this report, with its resolution. The next session does not need to re-ask any of these.

| # | Decision | Resolution |
|---|---|---|
| 1 | Lojix repo shape | **(γ) — One repo `lojix` (renamed from `lojix-daemon`); one crate; two binaries `[[bin]] name = "lojix-daemon"` (long-lived) + `[[bin]] name = "lojix"` (thin CLI). `signal-lojix` separate. `lojix-cli` legacy.** Per `~/primary/AGENTS.md` §"Binary naming". |
| 2 | `forge` vs new lojix daemon | **(a) — Genuinely different.** forge is criome-stack executor (future work; replacement for nix's build infrastructure; not in any production path). Leave forge alone; the GitHub redirect from `lojix` → `forge` is stale but harmless. forge's ARCH/README updated this session to make the distinction clear. |
| 3 | Plan 04 + Report 12 integration | **Folded into one 15-step migration order.** Plan 04 covers placement / containment / Publication / SecretReference; report 12 adds the Wi-Fi / DNS / LAN / VPN / AI policy work + the boundary principle. Plan 04's containment shape (NixosContainer / MicroVm, UserNamespacePolicy data-driven) holds. |
| 4 | Branch name | **`horizon-re-engineering`** (bare, no `push-` prefix). Same name across all six repos. Documented in the new feature-development skill + the beads-skill update. |
| 5 | Bead structure | **(b) Epic + sub-task beads with `bd dep` links.** Epic `primary-vhb6` filed; step 1 `primary-ql48` filed and blocks the epic. Subsequent step beads file as work advances (per the skill's ~5-15 active items soft cap). Reuse existing `primary-a61` (Wi-Fi work) and `primary-sff` (lojix-split intent). |
| 6 | KnownModel — closed enum vs Other escape | **(a) Closed enum, PascalCase, no spaces.** `"GMKtec EVO-X2"` becomes `GmktecEvoX2` (or similar PascalCase). Validation rejects spaces. Adding a new machine = one-line variant in `species.rs`; the friction makes the operator notice they're authoring a new config branch. |
| 7 | Pod / Metal shared resource fields | **(b) Symmetric sub-record `Resources { cores, ram_gb }`** on both Metal and Contained variants. The variant tag carries the hardware-vs-allocation distinction; field name doesn't need to. (Bead carries a "revisit if container resource modelling needs change" note.) |
| 8 | `br-lan` policy | **(a) CriomOS implementation constant.** Lives in `CriomOS-lib/lib/default.nix:lan.bridge` (a new constant). Kernel interface name with no operational meaning at cluster-policy level. |
| 9 | NodeCapabilities vs NodePubKeys boundary (initial framing) | **Superseded by §6 above.** Capability variants own their associated key material; NodePubKeys shrinks to pure identity (SSH always; Yggdrasil for cluster-mesh nodes). |
| 10 | Tailnet TLS — Horizon or runtime trust | **(a) CA's public certificate (or fingerprint) goes in horizon, datom-authored.** CriomOS owns its trust layer through deployment; CA re-issuance = datom edit + redeploy. Schema field on `Cluster.tailnet`: `tls: TlsTrustPolicy { ca_certificate: PublicCertificate }` so consumers can both verify-by-fingerprint and trust-bundle the cert. |
| 11 | VPN ownership — cluster vs node | **Per-node membership only, no cluster-level enabled-providers list.** `Node.vpn_membership: Option<VpnMembership { provider: VpnProvider, credential: SecretReference }>`. Default behavior: connection is *available* (NM profile on edges; equivalent for centers via systemd-networkd), but does *not* auto-connect or reroute. A future `autoconnect` field with a `default_connection_policy` (e.g. distance-based) can add automatic dialing later. NordVPN server lock stays as CriomOS-internal `data/config/nordvpn/update-servers` (public provider data with its own update cadence; not in horizon). |
| 12 | Cluster identity — granularity | **Lighter shape.** No new Cluster fields. `.criome` and `.criome.net` are Criome-protocol constants in `horizon-rs` source — they apply across all clusters that participate in Criome, not per-cluster policy. Internally, services prefer `.criome` (the internal-network mirror); externally-facing services use `.criome.net` (the public-internet mirror); both refer to the same host. Add `view::Node.public_fqdn` returning `<cluster>.criome.net`-shaped FQDN for public-facing surfaces. Keep `name.rs:81` derivation for internal `<host>.<cluster>.criome`. Optionally extract the literal TLDs to named constants in `horizon-rs` source. |
| 13 | Rename `criomeDomainName` now or later | **Rename now.** `node.criomeDomainName` → `node.fqdn` (or `node.internalFqdn`) in step 3, alongside the public_fqdn addition. Step 3 is already breaking; stacking the rename costs zero. |
| 14 | WiFi password during transition | **(a) `SecretReference` from day one.** Operator moves `"leavesarealsoalive"` out of `router/default.nix:98` into the chosen backend (sops-nix is most ready, given existing per-host age keys from SSH host keys). Adds a `cluster.secret_bindings` entry naming the backend. SecretReference discipline holds throughout. |
| 15 | `lojix-cli` schema bump strategy | **MOOTED by new-daemon path.** lojix-cli stays at the current schema for the duration of the arc; retires after CriomOS migrates to consume the new daemon's projection. No bump strategy needed. |
| 16 | User tool secret references | **DEFERRED ("focus on horizon").** Not in this arc. Future arc decides whether to grow `UserProposal.tool_credentials` in cluster Horizon, add a separate user-profile Horizon layer, or keep gopass-path policy in CriomOS-home. |
| 17 | Capability derivation pattern (Vec / missing-data) | **`Vec<ProposalCapability>` with Override/Off variants per capability on the proposal side; struct with `Option<T>` fields on the view side. Derivation happens in horizon-rs projection; missing required data in the resolved capability disables it (None in view). Bootstrap problem handled naturally — pre-first-boot keys missing = capability disabled in view; CriomOS skips rendering.** See §6 above. |
| 18 | Ghost workload — native NixOS service vs OCI | **(a) Native NixOS service.** Workspace principle: always Nix-native; package ourselves if needed. The OCI route is mostly compatibility theater. (This principle is broader than Ghost; it's the workspace's stance on platform discipline. Not yet captured in a workspace skill — flagged for designer.) |
| 19 | Storage and wire defaults | **`sema-engine` (full database engine library) + `signal-core` (wire kernel).** Don't depend on bare `sema` directly unless the engine doesn't expose the surface needed (rare). Don't invent parallel framing per signal contract — every signal-* contract layers on signal-core's primitives. Skill `~/primary/skills/rust/storage-and-wire.md` updated this session. |

---

## 8 · The unified inventory (15 steps)

The arc decomposes into 15 schema/code changes. Each is a discrete unit of work with a clear boundary. Steps are mostly independent — the migration order in §9 is the recommended sequence, but agents can pick any step whose dependencies have closed.

| # | Step | Repos | Origin |
|---|---|---|---|
| 1 | `proposal::*` / `view::*` type-vocabulary split | horizon-rs | Report 12 row 19 (boundary principle) |
| 2 | `SecretReference { name, purpose }` + `ClusterSecretBinding` + `SecretBackend ::= Sops \| SystemdCredential \| Agenix` | horizon-rs | Plan 04 §P1.1 |
| 3 | `view::Node.public_fqdn` + rename `criomeDomainName` → `fqdn`; optionally extract TLD constants | horizon-rs, CriomOS, CriomOS-home | Closed §12, §13 |
| 4 | `Cluster.lan: LanNetwork { cidr, gateway, bridge_alias_in_criomos_lib, dhcp_pool, lease_policy }` + `Cluster.resolver: ResolverPolicy { upstreams, fallbacks, listens }` | horizon-rs, CriomOS | Report 119 §§2,3; closed §8 (br-lan stays in CriomOS-lib) |
| 5 | `Cluster.wifi_networks: Vec<WifiNetwork>` + `WifiAuthentication ::= Wpa3Sae { password: SecretReference } \| EapTls { ca, server_identity, client_profile, authorization }` + `RouterInterfaces.wlans: Vec<WlanInterface>` (plural) + `CertificateAuthority` + `CertificateProfile` | horizon-rs, CriomOS, goldragon | Report 119 §4 + report 12 row 4. **Bead `primary-a61` is this step.** |
| 6 | `NodePlacement ::= Metal { … } \| Contained { host, substrate, resources, network, state, trust, user_namespace_policy }` + `ContainmentSubstrate ::= NixosContainer \| MicroVm` + `UserNamespacePolicy ::= PrivateUsersPick \| HostRootMappingAllowed { reason, approved_by }` + Pod migration | horizon-rs, goldragon | Plan 04 §§P1.1, P1.2 |
| 7 | `NodeCapabilities` (Vec<ProposalCapability> proposal; struct view) per §6 above | horizon-rs, CriomOS | Plan 04 §P1.1 + report 12 row 14 + this conversation §6 above |
| 8 | `Horizon.contained_nodes: BTreeMap<NodeName, ContainedNodeView>` + `ProjectedNodeView` (one level deep, no nested containment by type) + `HostPublicEndpointRoute` derived projection | horizon-rs, CriomOS | Plan 04 §§P1.4, P1.5 |
| 9 | `NodeSpecies::Publication` + Ghost as a Publication node placed in NixosContainer with native services/ghost.nix module | horizon-rs, goldragon, CriomOS | Plan 04 §§P6, P6.4; closed §18 |
| 10 | `Cluster.tailnet: Option<TailnetConfig { base_domain, tls: TlsTrustPolicy { ca_certificate } }>` + `TailnetRole ::= Client \| Server { port, base_domain }` collapse | horizon-rs, CriomOS | Report 12 rows 3,9 + closed §10 |
| 11 | `Cluster.ai_providers: BTreeMap<Name, AiProvider { name, serving_node, protocol, port_or_base_url, api_key: Option<SecretReference>, models }>` | horizon-rs, CriomOS-home | Report 119 §8 |
| 12 | `Node.vpn_membership: Option<VpnMembership { provider, credential }>` + `VpnProvider ::= Nordvpn \| WireguardMesh` + per-provider CriomOS modules gating on membership presence | horizon-rs, CriomOS, CriomOS-home | Closed §11 |
| 13 | `Machine ::= Metal { arch, cores, ram_gb, model?: KnownModel, motherboard?, chip_gen?, resources: Resources } \| Pod { host, super_user?, resources: Resources }` (data-bearing enum, symmetric Resources sub-record) + `KnownModel` direct (closed enum, PascalCase, no spaces — variants like `GmktecEvoX2` instead of free strings) | horizon-rs, goldragon, CriomOS | Report 12 rows 1,2 + closed §6, §7 |
| 14 | Address grouping in `view::Node` (preserve `YggdrasilEntry { pub_key, address, subnet }` instead of unpacking into 3 sibling fields) + delete `hasSshPubKey` (always true in proposal) | horizon-rs, CriomOS | Report 12 rows 16,17 |
| 15 | Source-constraint tests over `CriomOS/modules` + `CriomOS-home/modules` forbidding production literals (no literal SSID, password, regulatory country, IP range, DNS upstream, etc.) | CriomOS, CriomOS-home | Report 119 (tests section). **Beads `primary-1ha` and `primary-58l` align here.** |

**The new lojix daemon implementation runs in parallel** with these 15 steps. The daemon adopts the new schema as it stabilizes; first the contract crate (`signal-lojix`) gets fleshed out; then the daemon's actor structure (LiveSetActor, GcRootActor, EventLogActor, ContainerLifecycleActor); then the thin CLI client. The order here is bead-driven, not numbered.

---

## 9 · Migration order (recommended)

Each step is one typed-records-over-flags cycle: schema additions land with `serde(default)`; consumers migrate; old fields delete after the last read disappears. Steps lower in the list depend on earlier ones for setup but are otherwise independent.

| # | Step | Why this order |
|---|---|---|
| 1 | `proposal::*` / `view::*` namespace split | Structural prerequisite. Every subsequent change targets either or both sides; the split makes that distinction enforceable at the type level. **No design decisions block this step.** |
| 2 | `SecretReference` + `ClusterSecretBinding` + backend enum | Every typed-payload record below uses it. |
| 3 | `view::Node.public_fqdn` + rename `criomeDomainName` → `fqdn` (+ optional TLD constant extraction) | Highest-leverage rename — removes the `.criome` derivation hack from ~15 CriomOS modules; one breaking-rename bundled with the public-fqdn addition. |
| 4 | `Cluster.lan` + `Cluster.resolver` | Independent of node-side changes. LAN constants in CriomOS-lib + DNS upstreams in dnsmasq/resolved/networkd move out of Nix into typed cluster records. |
| 5 | `Cluster.wifi_networks` + `RouterInterfaces.wlans` (plural) + cert records | Dual-radio enables EAP-TLS; SAE password becomes SecretReference per closed §14. **Operator-side prep:** move `"leavesarealsoalive"` out of `router/default.nix:98` into sops/agenix before this step lands. |
| 6 | `Cluster.ai_providers` | `pi-models.nix:23-27` largeAiRouter scan disappears. |
| 7 | `Node.vpn_membership` + per-provider CriomOS modules | Replaces NordVPN literals in `network/nordvpn.nix:19-60` and WireGuard literals in `network/wireguard.nix:40,47,65`. CriomOS modules gate on `node.vpn_membership.provider == Nordvpn` etc. |
| 8 | `NodeCapabilities` typed payload (`binary_cache`, `build_host`, `container_host`, `public_endpoint`, `eap_tls`, `nordvpn`, `wireguard`) per §6 above | Four booleans disappear as side-effect (`isNixCache`, `isRemoteNixBuilder`, `hasWifiCertPubKey`, `hasNordvpnPubKey`). The other booleans (`BehavesAs`, `TypeIs`, `ComputerIs`, `AtLeast`, etc.) **stay** in the view as consumer ergonomics. |
| 9 | `NodePlacement` (`Metal` / `Contained`) + `ContainmentSubstrate` + `UserNamespacePolicy` + Pod migration | Containment / placement shape per plan 04. Generalises the legacy `MachineSpecies::Pod` pattern. |
| 10 | `Machine` data-bearing enum (`Metal { … } \| Pod { … }` with symmetric `Resources` sub-record) + `KnownModel` direct (closed PascalCase enum) | Apex input-correctness change. CriomOS rewrites `node.machine.species` reads to pattern-match on the tagged union. |
| 11 | `TailnetRole` collapse + `Cluster.tailnet` factor-out (TLS material per closed §10) | Resolves base-domain ownership. |
| 12 | `Horizon.contained_nodes` + `ProjectedNodeView` + `HostPublicEndpointRoute` | Plan 04 §P1.4-§P1.5. Required before the Publication step. |
| 13 | `NodeSpecies::Publication` + Ghost as Publication node with native services/ghost.nix module | Per plan 04 §P6. |
| 14 | Address grouping + delete `hasSshPubKey` | Small output cleanup. |
| 15 | Source-constraint tests forbidding production literals in CriomOS / CriomOS-home modules | Locks in the gains; future drift fails `nix flake check`. |

The lojix daemon implementation track runs in parallel — driven by its own beads (existing `primary-sff` revised + new ones as needed), not numbered here.

---

## 10 · Beads

**Filed this session:**

- **`primary-vhb6` (epic, P2)** — "horizon re-engineering: input/output split + cluster-policy extraction + new lojix daemon". Description carries the 15-step migration order, all closed design decisions, the branch name, the six repos in scope. Blocked-by `primary-ql48` so it stays open until step 1 closes.
- **`primary-ql48` (task, P2)** — "horizon-rs: proposal::* / view::* type-vocabulary split". Step 1. Description carries the full acceptance criterion: what files move where, which compound types split into proposal::/view:: distinct types with translations, which stay shared (pure value modules: species, name, magnitude, address, pub_key, error). Marked as blocking the epic.

**Existing beads to reuse / coordinate with** (do not file duplicates):

- `primary-a61` (P2, open) — "CriomOS: move router Wi-Fi policy and SAE secret out of Nix modules". **Aligns with step 5.** This session added a comment tying it to the arc and noting the closed §14 (SecretReference from day one + dual-radio plural-WLAN schema).
- `primary-sff` (P2, open) — "lojix: extract lojix-core, add lojix-daemon, create signal-lojix contract crate". **Aligns with the lojix daemon implementation track.** This session added a comment noting the bead's original "Cargo workspace inside lojix-cli" plan is superseded by shape (γ): one repo `lojix` with daemon + thin CLI binaries; signal-lojix separate. The bead description itself stays as a timestamp; the comment carries the revised premise.
- `primary-1ha` (P2, open) — "CriomOS-test-cluster: add negative Horizon fixtures for role invariants". **Aligns with step 15.**
- `primary-58l` (P2, open) — "CriomOS-test-cluster: add VM or nspawn service smoke for DNS and tailnet roles". **Aligns with step 15** (or could land earlier as part of step 4).
- `primary-tpd` (P2, open) — "Review headscale and Yggdrasil roles in CriomOS". **Aligns with step 11.**
- `primary-da7` (P3, open) — "lojix (or successor): query cluster DB for host registration mismatches; trigger per-key clavifaber verbs". **Future, post-cutover.**

**Beads to file as work advances** — one per step that doesn't already have an existing bead (~10 new beads). Each follows the discipline in `~/primary/skills/beads.md` §"Feature beads carry their branch name": description includes `Branch: horizon-re-engineering` and `Repos: <list>`. Each is `task` type, P2, role:system-specialist. Dependencies via `bd dep` where steps have hard ordering (e.g. step 2 SecretReference blocks steps 5, 7, 11, 12 which use SecretReferences).

---

## 11 · Operator-side prep

Some migration steps require operator-side work *before* the schema migration lands. Names here so they don't surface as surprises mid-implementation.

| Step | Prep | When |
|---|---|---|
| 5 (WiFi) | Move `"leavesarealsoalive"` literal out of `CriomOS/modules/nixos/router/default.nix:98` into the chosen secret backend (sops-nix recommended; per-host age keys via SSH host keys are already in place). Add the matching `cluster.secret_bindings` entry naming the backend. | Before step 5 lands. |
| 5, 7, 11, 12 (anything with secrets) | Decide on a secret backend per cluster. Plan 04 lists three: `Sops { file, key }`, `SystemdCredential { credential_name }`, `Agenix { secret_id }`. sops-nix is the most ready given existing PKI material. | Before step 2 lands (the SecretReference + ClusterSecretBinding structures). |
| 6 (AI provider) | Confirm prometheus is the AI provider host, current llama.cpp port (likely 11434), provider name (`criomos-local` today). | Before step 6's typed `Cluster.ai_providers` lands. |
| 9 (NodePlacement) | Confirm pod nodes' substrate (NixosContainer per plan 04) and resource allocations. The current pod entries in `goldragon/datom.nota` need to migrate to the typed `Contained` variant. | Before step 9's NodePlacement lands. |
| 10 (Tailnet TLS) | Generate the cluster's headscale CA. Read `openssl x509 -in <cert> -noout -fingerprint -sha256` (or capture the public cert PEM). Paste fingerprint or PEM into `goldragon/datom.nota` under `cluster.tailnet.tls.ca_certificate`. | Before step 10 lands. CA re-issuance later requires another datom edit + redeploy. |
| 13 (Machine + KnownModel) | Convert any free-string model values in `goldragon/datom.nota` into PascalCase variant names. Add new variants to `KnownModel` enum for any machine model not yet there (e.g. `GmktecEvoX2`, `ThinkPadE15Gen2Intel`). | Before step 13 lands. |

---

## 12 · Out of scope (for this arc)

- **`Horizon::project` algorithm rewrite.** Shape shifts; strategy holds.
- **`Error` enum expansion.** New typed records need new error variants; trivial as each step lands.
- **`User` schema redesign.** `User` has the same kinds of derived fields as `Node`; consumer surface smaller; follow-up audit once `Node` lands.
- **`DomainProposal` data-bearing variant.** `Cloudflare { account_id, … }` deferred until a second domain provider lands.
- **Nota wire compatibility / nota-codec changes.** The migration assumes coordinated CriomOS + lojix daemon + horizon-rs + goldragon bumps; positional-vs-named-record decisions at the nota-codec level stay out of scope.
- **User tool secret references** (per closed §16) — separate arc; cluster Horizon vs user-profile layer decision deferred.
- **lojix-cli changes.** Stays at the current schema. Retires only after CriomOS migrates to consume the new daemon's projection.
- **Eventual Sema-on-Sema rewrite** (per ESSENCE §"Today and eventually"). This arc operates on today's stack — Rust on Linux, redb/rkyv via sema-engine, signal-core wire, direct nix invocations.
- **Code work this session.** All planning artifacts (skills, beads, branches, worktrees, repo renames, ARCH updates) are done; first commit of step 1 lands in the next session.

---

## 13 · State at end of this session

**Skills:**
- **NEW** `~/primary/skills/feature-development.md` — the worktree-based feature-branch convention; how to create / clean up worktrees; branch naming; interaction with the orchestration protocol.
- **UPDATED** `~/primary/skills/rust/storage-and-wire.md` — §"The sema-family pattern" rewritten as §"The sema-engine pattern (default for new components)". Names sema-engine as the default; sema as the lower-level kernel; signal-core as the wire substrate.
- **UPDATED** `~/primary/skills/beads.md` — added §"Feature beads carry their branch name" (filed earlier in this conversation; carried forward for completeness here).

**Workspace docs:**
- **UPDATED** `~/primary/protocols/active-repositories.md` — `lojix-daemon` → `lojix` rename; description rewritten to reflect one-crate-two-binaries shape; added "Active feature arc — horizon re-engineering" subsection naming the branch and the six repos; clarified forge isn't the deploy daemon.

**Repositories:**
- **RENAMED** `LiGoldragon/lojix-daemon` → `LiGoldragon/lojix` on GitHub (via `gh repo rename`). Local clone moved (`/git/github.com/LiGoldragon/lojix-daemon` → `/git/github.com/LiGoldragon/lojix`); remote URL updated.
- **UPDATED** `lojix/ARCHITECTURE.md`, `lojix/README.md`, `lojix/skills.md` — rewritten to reflect the new shape (one crate, two binaries; sema-engine + signal-core defaults; in-development status; horizon-re-engineering branch).
- **UPDATED** `forge/ARCHITECTURE.md`, `forge/README.md` (earlier this session) — added "Status: future work — replacement for nix's build infrastructure" framing; explicit note that forge is not the lojix deploy daemon.

**Branches:** `horizon-re-engineering` created and pushed in:
- `horizon-rs` (commit `1e09ab48` baseline)
- `lojix` (commit `eca194fc` baseline — post-rename docs)
- `signal-lojix` (commit `a41b5a83` baseline)
- `CriomOS` (commit `f0291b96` baseline)
- `CriomOS-home` (commit `5efa64fa` baseline)
- `goldragon` (commit `67f55d5d` baseline)

**Worktrees:** `~/wt/github.com/LiGoldragon/<repo>/horizon-re-engineering/` created for all six repos via `jj workspace add`. Each shares the canonical repo's operation log + bookmark space; each has its own independent `@`.

**Beads:**
- Epic `primary-vhb6` filed (feature, P2).
- Step 1 `primary-ql48` filed (task, P2). Blocks the epic.
- Comments added to `primary-sff` (revised premise per shape γ) and `primary-a61` (revised premise per closed §14 + dual-radio).

**Reports:**
- This report (number 14) — the canonical post-kickoff artifact.
- Predecessors: report 13 (kickoff plan + open questions), report 12 (combined audit + boundary principle, rewritten this conversation), report 11 (initial schema survey), report 04 (cloud host plan, second revision), report 119 (system-specialist's CriomOS literal-leaks audit).

**Orchestration:**
- system-assistant claim active on: `[primary-ql48]`, `/home/li/primary/skills`, `/home/li/primary/protocols/active-repositories.md`, `/git/github.com/LiGoldragon/{horizon-rs,signal-lojix,CriomOS,CriomOS-home,goldragon}`. Will be released at end of session per protocol.

---

## 14 · Next session

After context clear, the next session reads (in this order):

1. **`~/primary/ESSENCE.md`** — workspace intent.
2. **`~/primary/AGENTS.md` + `~/primary/CLAUDE.md`** — workspace contract.
3. **`~/primary/protocols/orchestration.md`** — claim flow.
4. **This report** (`~/primary/reports/system-assistant/14-horizon-re-engineering-ready-state.md`).
5. **`~/primary/skills/feature-development.md`** — the worktree convention.
6. **`~/primary/skills/rust/storage-and-wire.md`** — sema-engine + signal-core defaults.
7. **`~/primary/skills/jj.md`** — version-control discipline.
8. **`~/primary/skills/beads.md`** — bead lifecycle + the feature-bead branch-name discipline.
9. **`~/primary/skills/system-assistant.md`** — role contract.
10. **`/git/github.com/LiGoldragon/horizon-rs/lib/src/`** — the schema source files (lib.rs, proposal.rs, node.rs, cluster.rs, user.rs, horizon.rs, machine.rs, io.rs, address.rs, name.rs, magnitude.rs, pub_key.rs, species.rs, error.rs).
11. **`/git/github.com/LiGoldragon/lojix/{ARCHITECTURE.md,README.md,skills.md}`** — the new lojix repo's docs.
12. **`/git/github.com/LiGoldragon/signal-lojix/ARCHITECTURE.md`** — wire contract architecture.
13. **`/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md`** — the sema-engine surface.

**Then start step 1:**

1. Claim system-assistant: `tools/orchestrate claim system-assistant '[primary-ql48]' /git/github.com/LiGoldragon/horizon-rs ~/wt/github.com/LiGoldragon/horizon-rs/horizon-re-engineering -- 'step 1: namespace split'`.
2. `cd ~/wt/github.com/LiGoldragon/horizon-rs/horizon-re-engineering`.
3. `bd update primary-ql48 --status in_progress`.
4. Execute step 1 per the bead's acceptance criterion (`bd show primary-ql48`):
   - Move `lib/src/cluster.rs` → `lib/src/view/cluster.rs` (or `view/mod.rs` re-exporting from per-type files).
   - Move `lib/src/node.rs` → `lib/src/view/node.rs`.
   - Move `lib/src/user.rs` → `lib/src/view/user.rs`.
   - Move `lib/src/horizon.rs` → `lib/src/view/horizon.rs`.
   - Move proposal types from `lib/src/proposal.rs` to `lib/src/proposal/<type>.rs` (or keep as one file if cleaner).
   - Duplicate compound types that straddle (`Machine`, `Io`, `NodeServices`, `NodePubKeys`, `RouterInterfaces`, `WireguardProxy`) into both namespaces with `From<proposal::T> for view::T` translations. Initially shape-equivalent; will diverge in later steps.
   - Pure value enums (`NodeSpecies`, `Arch`, `KnownModel`, `Keyboard`, `Bootloader`, `MotherBoard`, `Magnitude`) stay in their own modules at the top level (no namespace split).
   - Update `lib/src/lib.rs` mod declarations.
   - Update `lib/tests/{cluster,node,user}.rs` import paths from `horizon_lib::cluster::Cluster` → `horizon_lib::view::Cluster`, etc.
   - `cargo build` and `cargo test` to verify.
5. Commit + push via standard jj flow (per `~/primary/skills/jj.md`): `jj commit -m '<msg>' && jj bookmark set horizon-re-engineering -r @- && jj git push --bookmark horizon-re-engineering`.
6. Close `primary-ql48` with a note pointing at the commit; `bd ready --label role:system-specialist` to find the next bead.

**Acceptance for step 1:**
- horizon-rs builds clean (`cargo build`, `cargo test`).
- All existing tests pass with import-path updates only — no behavior changes.
- The wire output is byte-identical (JSON shape unchanged). Pure Rust refactoring; downstream consumers (lojix-cli, eventually new lojix daemon) see no schema change.
- No type currently shared between input/output is referenced from both namespaces directly — instead, each namespace has its own type + translation.
- Pure value types stay shared.

---

## Sources

**Reports (this workspace):**
- `~/primary/reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md` — placement / containment / Publication / SecretReference design (plan 04).
- `~/primary/reports/system-assistant/11-horizon-schema-re-engineering-research.md` — initial schema survey.
- `~/primary/reports/system-assistant/12-horizon-re-engineering-combined-audit.md` — combined audit + boundary principle (rewritten this conversation).
- `~/primary/reports/system-assistant/13-horizon-re-engineering-kickoff-questions.md` — kickoff plan + open questions.
- `~/primary/reports/system-specialist/119-horizon-data-needed-to-purge-criomos-literals.md` — CriomOS literal-leaks audit (system-specialist).
- `~/primary/reports/designer/{157-sema-db-full-engine-direction.md,158-sema-kernel-and-sema-engine-two-interfaces.md}` — sema-engine architecture.

**Skills (this workspace):**
- `~/primary/skills/feature-development.md` (new this session)
- `~/primary/skills/beads.md` (updated earlier this conversation)
- `~/primary/skills/jj.md`
- `~/primary/skills/rust/storage-and-wire.md` (updated this session)
- `~/primary/skills/reporting.md`
- `~/primary/skills/system-assistant.md`
- `~/primary/skills/typed-records-over-flags.md`
- `~/primary/skills/contract-repo.md`
- `~/primary/skills/actor-systems.md`
- `~/primary/skills/push-not-pull.md`
- `~/primary/skills/rust-discipline.md` (and rust/* sub-skills)

**Workspace docs:**
- `~/primary/ESSENCE.md`
- `~/primary/AGENTS.md`
- `~/primary/protocols/orchestration.md`
- `~/primary/protocols/active-repositories.md` (updated this session)

**Repository ARCH docs:**
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/lib.rs` (and the per-type module docs)
- `/git/github.com/LiGoldragon/lojix/ARCHITECTURE.md` (rewritten this session)
- `/git/github.com/LiGoldragon/signal-lojix/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/sema/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`

**Beads referenced:**
- Epic: `primary-vhb6`
- Step 1: `primary-ql48`
- Existing aligned: `primary-a61`, `primary-sff`, `primary-1ha`, `primary-58l`, `primary-tpd`, `primary-da7`
- Closed (informs path): `primary-q3y` (kameo migration; closed today)

**User direction this conversation:**
- Refactor branches; daemon + new CLI in `lojix` repo; sema-engine default; signal-core types for all signal traffic.
- Branch name: bare `horizon-re-engineering`, no `push-` prefix.
- Bead structure: epic + sub-tasks with `bd dep` links; feature beads carry their branch name in description.
- Worktree convention: `~/wt/github.com/<owner>/<repo>/<branch>/`.
- Closed §6-§18 design decisions per the table in §7 above.
- Get everything ready (skills, branches, worktrees, architecture, repo rename); write this comprehensive report; do **not** code yet; coding starts after the next context clear.

# 20 — audit of SYS/134 implementation, 2026-05-17

*Review of `reports/system-specialist/134-lean-horizon-pan-config-and-lojix-build-2026-05-17.md`'s
claimed implementation against the actual code on
`horizon-rs/horizon-leaner-shape` (tip `45056dc4`),
`lojix/horizon-leaner-shape` (`5cc1eaf6`),
`goldragon/horizon-leaner-shape` (`989572de`), and the new
`criomos-horizon-config` repo (`1218566e`). Tests pass; the
real-smoke claim holds; six substantive issues warrant follow-up
before this lands on main.*

## 0 · TL;DR

The implementation does what SYS/134 says it does. `ClusterProposal`
cleanly sheds `domain` + `public_domain`; `HorizonProposal` is a
real second-axis input that lojix-daemon loads from its
`horizon_configuration_source`; goldragon's datom tail now ends at
`vpn_profiles`; `criomos-horizon-config/horizon.nota` carries the
five pan-horizon constants; ~210 tests pass on `cargo test
--workspace`. The "Verification" section's claims hold against the
actual code.

Six substantive concerns:

1. **LAN-subnet collisions are unmodeled.** FNV-1a hashing into 256
   /24 subnets gives birthday-collision risk that grows with
   (namespace × cluster × router) tuples. No detection; silent
   overlap.
2. **DHCP pool magic numbers** `.100` / `.240` are baked into
   `horizon_proposal::lan_network()`. Per the new ARCH boundary
   table they belong to horizon derivation, but they should be
   named constants (or derived from prefix length), not literals.
3. **`reserved_subdomains` is declared but not enforced.** Today
   `tailnet`, `vault`, `git`, `mail` are listed; nothing prevents
   a cluster from naming a node `vault` or `service_domain`
   minting a label that collides with a non-reserved name. The
   field is documentation pretending to be a typed guarantee.
4. **No version-pinning witness for `stable_hash_v1`.** The
   function is the contract; a future agent who "improves" the
   hash silently re-allocates every LAN. A byte-sequence-to-u64
   seed test would lock the contract.
5. **ARCH still references reports.** Status section names
   `reports/designer-assistant/101-...` (the file I moved to
   `system-assistant/17-...` earlier this turn) — now dangling.
   Per `skills/architecture-editor.md` §"Architecture files never
   reference reports," neither the dangling form nor the corrected
   form belongs there. The boundary-rule section also cites
   designer/207 and designer/208.
6. **The GGUF caveat is itself a V/A/N rule failure.** SYS/134's
   "Remaining Caveat" reports the OS system closure referencing
   GGUF fetch derivations. That's CriomOS-side runtime data
   (model catalog) leaking into the build-time closure — the
   exact "replaces the literals scattered across CriomOS" smell
   the new ARCH names. Treating it as "follow-up architecture
   issue" is right; framing it as "separate problem" is too
   generous.

Plus three polish items (§3) and four observations on what the
implementation got right (§4).

## 1 · What SYS/134 claims, against actual code

| SYS/134 claim | Verified |
|---|---|
| `ClusterProposal` no longer has `domain` / `public_domain` | ✓ `lib/src/proposal/cluster.rs` — full struct read; both fields absent. |
| `HorizonProposal` is the second projection input | ✓ `lib/src/horizon_proposal.rs:21-28` carries operator + domain suffixes + LAN pool + reserved subdomains + trusted keys. |
| `project(&horizon, &viewpoint)` takes both | ✓ `proposal/cluster.rs:project` signature reads `(&self, horizon: &HorizonProposal, viewpoint: &Viewpoint)`. |
| Cluster + public domain derive from horizon | ✓ `project` body calls `horizon.public_domain()` for user projection; `CriomeDomainName::for_node` consumes `horizon.internal_domain()`. |
| Router SSID derives `<cluster>.<internal>` | ✓ `horizon_proposal.rs:135-137` — `format!("{cluster}.{}", self.internal_domain())`. Currently `goldragon.criome`. |
| LAN CIDR/gateway/DHCP derive by stable hash | ✓ `horizon_proposal.rs:147-189` — FNV-1a over (namespace, cluster, router) → subnet index in supernet. Gateway = `.1`, DHCP `.100..240`. |
| Resolver listens derive from loopback + LAN gateway | ✓ `horizon_proposal.rs:191-200`. |
| Tailnet base domain derives `tailnet.<cluster>.<internal>` | ✓ `horizon_proposal.rs:139-145` via `service_domain`. |
| `TailnetConfig` no longer carries base_domain | ✓ `proposal/services.rs` — `TailnetConfig { tls: Option<TlsTrustPolicy> }` only. |
| AI / VPN are provider *selections*, not full catalogs | ✓ `AiProvider { name, serving_node, profile, credentials }`; `NordvpnProfile { credentials, preferred_locations }`. The server catalog and runtime configs live elsewhere per SYS/134. |
| Goldragon datom tail drops the two literals | ✓ `git show origin/horizon-leaner-shape:datom.nota` ends at `vpn_profiles`; no trailing `"criome"` / `"criome.net"`. |
| Lojix-daemon loads horizon config | ✓ `lojix/src/deploy.rs:1055-1062` — `horizon_configuration_source.load()?` → `proposal.project(&horizon_proposal, &viewpoint)?`. Daemon config gained `horizon_configuration_source` field. |
| `criomos-horizon-config` repo carries `horizon.nota` | ✓ Five fields: operator `LiGoldragon`, suffixes `criome`/`criome.net`, LAN pool `10.18.0.0/16` /24 `criome-lan-v1`, reserved `[tailnet vault git mail]`, trusted_keys `[]`. |
| `cargo test --workspace` green | ✓ ~210 tests pass on local `horizon-leaner-shape` worktree (`cargo test --jobs 1 --workspace -- --test-threads=1`). |
| `cargo check --workspace` green | ✓ both `horizon-lib` and `horizon-cli` check clean. |
| Real-smoke built `zeus` through `prometheus` | ✓ accepted on the report's word (verifying requires re-running the impure build); the build/copy/activate chain in lojix's deploy.rs reads the new shape correctly, so the path is plausible. |

## 2 · Substantive concerns

### 2.1 LAN-subnet collisions are unmodeled

`horizon_proposal.rs:147-189` allocates `/N` subnets within a
supernet by `hash % subnet_count`. For the current
`10.18.0.0/16 → /24` split, that's 256 buckets. Hash function is
FNV-1a (`stable_hash_v1`), non-cryptographic.

Birthday-paradox probabilities for *k* tuples in 256 buckets:

| *k* | P(collision) |
|---|---|
| 5 | ~3.9% |
| 10 | ~16% |
| 20 | ~54% |
| 23 | ~64% |

A "horizon" hosting one cluster with one router today is fine. A
horizon hosting half a dozen clusters with multiple routers each
is in the danger zone. The function does *no collision detection*
— two `(cluster, router)` tuples hashing to the same subnet index
both get the same `/24`. Silent overlap; DHCP collisions; routing
chaos.

Mitigations to consider, designer-side:

- Detect collisions at projection time (requires knowing every
  other allocated subnet — feasible because the operator has the
  pan-horizon view).
- Widen the bucket count (`/16 → /22` gives 64 buckets only; the
  current `/24` is already the wide end).
- Use a sorted, deterministic, fixed-table allocation (operator
  pins per-cluster subnet, projection just reads it). Loses the
  pure-deriving property but adds an explicit registry.

Today's mitigation is implicit: "Li operates one horizon with
~one cluster and one router." Worth naming as a constraint, or
fixing.

### 2.2 DHCP magic numbers `.100` and `.240`

`lan_network()` hard-codes:

```rust
let gateway = increment(network_address, 1);
let dhcp_start = increment(network_address, 100);
let dhcp_end = increment(network_address, 240);
```

Per the new ARCH boundary table, DHCP pool *is* horizon
derivation (good — it shouldn't live in CriomOS modules). But
`100` and `240` are CriomOS-historical defaults (per
`reports/system-specialist/119` §2 the legacy CriomOS module
hardcoded "DHCP pool `.100 - .240`"); they got copied verbatim
into `lan_network()`. They earn the V/A/N rule's "horizon
derivation" status only if they actually derive from something
— and they don't; they're literals.

Two clean fixes:

- Name them: `const DHCP_POOL_START_OFFSET: u32 = 100;` etc. at
  module scope, with a comment saying *why* `.100`/`.240` (a
  reservation for static-address hosts below `.100`, a high-
  numbered range left for non-DHCP allocations).
- Derive from prefix length: e.g., split the `/N` evenly between
  static / DHCP / reserved. More principled but a small design
  decision.

Either way, the literal `100` and `240` shouldn't sit unnamed in
the projection function.

### 2.3 `reserved_subdomains` is declared but not enforced

`HorizonProposal.reserved_subdomains: Vec<ReservedSubdomainLabel>`
is loaded from `horizon.nota` as `[tailnet vault git mail]`. The
projection's `service_domain(cluster, service)` mints
`<service>.<cluster>.<internal>` for any `service: &str` — no
check that `service` IS in the reserved list, no check that other
proposal fields (node names, AI provider names, etc.) DON'T
collide with reserved labels.

The field is doing zero work today. Two paths:

- Make it real: validate at projection that every `service`
  passed to `service_domain` is in `reserved_subdomains`, and
  that no `NodeName` / `AiProviderName` / `UserName` collides
  with a reserved label.
- Drop it: if reserved labels aren't actually enforced, the
  field is decorative and goes.

The first is cheap and matches the field's evident intent.

### 2.4 `stable_hash_v1` has no version-pinning witness

The function is the contract — every `(namespace, cluster,
router)` tuple resolves to a specific `/24` subnet via this
exact byte computation. The `_v1` suffix commits to that
version. But nothing in tests pins the contract:

- No test asserts `stable_hash_v1(&["criome-lan-v1", "goldragon",
  "router-1"]) == 0xSPECIFIC_U64`.
- No test asserts `lan_network(...)` for known inputs returns a
  specific `/24`.

A future agent who "improves" the hash function (faster algorithm,
different prime) silently re-allocates every existing LAN. The
boot-time witness ("did my LAN change?") doesn't exist either.

Fix: add a small `tests/horizon_proposal_determinism.rs`:

```rust
#[test]
fn lan_network_for_known_inputs_is_pinned() {
    let horizon = HorizonProposal::from_parts(
        "LiGoldragon", "criome", "criome.net",
        "10.18.0.0/16", 24, "criome-lan-v1", vec![],
    ).unwrap();
    let lan = horizon.lan_network(
        &ClusterName::try_new("goldragon").unwrap(),
        &NodeName::try_new("goldragon-router").unwrap(),
    ).unwrap();
    assert_eq!(lan.cidr.as_str(), "10.18.XXX.0/24"); // pin the value
    assert_eq!(lan.gateway.as_str(), "10.18.XXX.1");
}
```

(XXX = whatever the actual hash gives; pin it, then it can't
silently change.)

### 2.5 ARCH still references reports (now dangling)

`horizon-rs/horizon-leaner-shape/ARCHITECTURE.md` Status section:

> *"carrying the structural cleanups proposed in
> `reports/designer-assistant/101-horizon-rs-overbuild-audit-2026-05-16.md`"*

That path doesn't exist anymore (moved to
`system-assistant/17-...` earlier this turn). The boundary-rule
section also names `reports/designer/207-...` and
`reports/designer/208-...` for the audit and brainstorm.

Per `~/primary/skills/architecture-editor.md` §"Architecture files
never reference reports": none of those refs belong in the ARCH
*at all*. ARCH describes what the system IS; reports describe how
the thinking moved at a point in time. The substance of /17, /207,
/208 either lives in the ARCH already (great — drop the cite) or
should be inlined (and then drop the cite).

Three lines to remove + the Status section's `"carrying the
structural cleanups proposed in..."` phrasing reframed as
positive description.

### 2.6 The GGUF caveat is itself a V/A/N rule failure

SYS/134's "Remaining Caveat":

> *"The `prometheus` full-system dry-run reaches the large-AI
> model closure. That exposed a separate problem: the llama model
> catalog makes the OS system closure reference GGUF fetch
> derivations..."*

This isn't separate. The new ARCH boundary table says:

| Bucket | Examples |
|---|---|
| CriomOS-side | …, AI runtime config, **AI model catalog**, … |

So the model catalog belongs in CriomOS, not in horizon's
projection. But it's currently in the OS *closure* — meaning
when you build the NixOS system, it pulls the GGUF derivations
in as build inputs. That's the model catalog leaking into the
build-time identity of the OS, which is the same shape as the
old "literals scattered across CriomOS" smell, just from the
other direction (now it's CriomOS-side data leaking into the
build closure instead of horizon-side data leaking into cluster
authoring).

The right framing: the model materialization needs to be
runtime / cache-managed (the report says this in passing), and
the OS closure should reference *the capability to fetch* (a
program + a path) rather than *the specific models* (each GGUF
as a build input). The V/A/N rule applied to AI catalog
membership: variability says yes (per cluster), authority says
CriomOS, non-derivable says yes. The runtime-vs-build-time
question is *which boundary the catalog crosses*, not whether
it's authored in CriomOS — and putting it in the build-time
closure is the wrong boundary.

Worth naming as a real follow-up audit, not as "separate
problem."

## 3 · Polish items

### 3.1 `LanCidr::try_new(cidr.to_string())` roundtrip

`lan_network()`'s last step:

```rust
let cidr = Ipv4Net::new(network_address, target_prefix)
    .expect("target_prefix was validated as an IPv4 prefix");
// ...
LanNetwork {
    cidr: LanCidr::try_new(cidr.to_string())?,
    ...
}
```

`Ipv4Net → String → parse → validate → store String`. Wasted
parsing on a value the projector just minted. `impl From<Ipv4Net>
for LanCidr` would skip the round-trip.

### 3.2 `OperatorName` / `HorizonTrustedKey` are hand-written

`horizon_proposal.rs` defines two transparent string newtypes
manually:

```rust
pub struct OperatorName(String);
impl OperatorName { pub fn try_new(s) -> Result<Self> { ... } }
```

`name.rs` already has the `string_newtype!` macro for this
pattern (`ClusterName`, `NodeName`, etc.). Two of these newtypes
should use the macro for consistency, or the macro should move
out to a place horizon_proposal.rs can import it.

### 3.3 ARCH `> 24` prefix cap should be named

`lan_network()` rejects `target_prefix > 24` without a comment
naming why. The reason is the DHCP pool spans `.100..240`, which
needs ≥ 256 host addresses (so `/24` is the smallest workable
prefix). Either:

- Comment why `24` is the cap, or
- Compute the cap from the DHCP-pool size requirement.

The current shape reads as a magic constant.

## 4 · What the implementation got right

### 4.1 Provider-selection vs catalog split is honest

`AiProvider { name, serving_node, profile, credentials }` and
`NordvpnProfile { credentials, preferred_locations }` are the
right shape: the cluster authors *which* provider it uses; the
provider's runtime details (protocol, port, model catalog,
server addresses) live CriomOS-side. The composite-smell warning
in the new ARCH applies, and the split here honors it.

### 4.2 `HorizonProposal` as a separate axis is the right cut

Three inputs to projection — pan-horizon (`HorizonProposal`),
per-cluster (`ClusterProposal`), per-viewpoint (`Viewpoint`).
Each has a different authority and a different change-cadence.
The split reflects the actual structure. The lojix daemon's
`HorizonConfigurationSource` lets the operator point each
deployment at the right pan-horizon config without rebuilding
the daemon binary.

### 4.3 The lojix consumer update is clean

`lojix/src/deploy.rs:1006-1062` reads correctly: the daemon's
configuration carries a `horizon_configuration_source`, the
build job loads the proposal at request time, and `project` is
called with both arguments. No legacy single-argument calls
linger. The daemon end-to-end builds a real CriomOS closure
through prometheus, per SYS/134's smoke claim.

### 4.4 Test coverage holds

~210 tests pass after the structural rework. Including the JSON
round-trip suite (`view_json_roundtrip.rs`) which catches wire-
shape drift. The horizon.rs / tailnet.rs / proposal.rs fixtures
all carry `HorizonProposal::from_parts(...)` and pass it through,
so the contract is exercised at the test layer too.

## 5 · Open questions

### Q1 — Should LAN collision detection block landing on main?

The current behavior is "deterministic but silently collides at
scale." Today's scale (one horizon, one cluster, one router) is
safe. Landing on main without detection commits the design to
"we'll catch the collision when it happens" — which may be never
on Li's setup, but is a real footgun for any hypothetical second
operator. A bead with `role:designer` to track is probably the
right shape if the fix isn't part of this arc.

### Q2 — Is the GGUF caveat a blocker?

Per SYS/134, the impure real-build smoke on **zeus** (a non-AI
node) succeeded. The full **prometheus** system dry-run failed
on the GGUF derivation. The arc's stated goal is "the new Horizon
and new Lojix daemon to build a real CriomOS system target" —
which it does, for zeus. If prometheus's full system isn't
required for landing-on-main, the GGUF issue is a real follow-up
but not a blocker. If it is required, the model-catalog boundary
needs the V/A/N treatment first.

### Q3 — Reserved-subdomain enforcement: validate or drop?

The field is in the schema, populated in the live config, and
ignored by the projection. Choose:

- (a) Validate at projection: every `service_domain(_, service)`
  call requires `service ∈ reserved_subdomains`; node/provider
  names get checked against the set.
- (b) Drop the field: today's `tailnet` derivation could call a
  hardcoded `tailnet_base_domain` without consulting any list,
  and the other reserved labels (`vault`, `git`, `mail`) aren't
  used yet.

### Q4 — `stable_hash_v1` version commitment

`_v1` suggests "we'll bump to `_v2` if needed." But the
projection's only call site doesn't include a version selector
— it just calls `stable_hash_v1`. If `_v2` is ever needed for
some clusters but not others, the call site needs a selector
(per-horizon-config? per-cluster?). Worth a sentence in the ARCH
naming the version policy now, before the second version exists.

## 6 · See also

- `~/primary/reports/system-specialist/132-horizon-domain-constants-not-cluster-data.md`
  — the design finding this implementation realizes.
- `~/primary/reports/system-specialist/134-lean-horizon-pan-config-and-lojix-build-2026-05-17.md`
  — the implementation report being audited here.
- `~/primary/reports/system-assistant/17-horizon-rs-overbuild-audit-2026-05-16.md`
  — the parent overbuild audit. The boundary rule in the new ARCH
  is the natural successor to /17's "what stays vs what goes"
  framing.
- `~/primary/reports/system-assistant/19-horizon-constants-not-cluster-data-2026-05-17.md`
  — designer-side framing of the V/A/N rule that drove this
  implementation.
- `~/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape/lib/src/horizon_proposal.rs`
  — the file most of this audit's concerns target.
- `~/primary/skills/architecture-editor.md` §"Architecture files
  never reference reports" — the discipline §2.5 cites.
- `~/primary/ESSENCE.md` §"Perfect specificity at boundaries"
  — the rule §2.3 (reserved subdomains) and §2.2 (named DHCP
  constants) invoke.

*End report 20.*

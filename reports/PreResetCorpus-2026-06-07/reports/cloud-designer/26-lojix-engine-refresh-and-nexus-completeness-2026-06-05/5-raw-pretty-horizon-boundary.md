# 5 — Raw/pretty horizon boundary: a concrete contract for the split, the lojix consumption seam, and the promotion path

cloud-designer lane finder, 2026-06-05. Read-only analysis. Lens:
the raw/pretty horizon boundary from intent records `9p8v` (the
split), `avvh` (the split is also a forward-integration seam),
`a2t4` (minimal + type-reuse), `vu2k` (types-only-module schema
shape), `tvbn` (horizon = projection hack for now), `x8iv`
(horizon-rs vs horizon-next fork). Grounded in the actual
`horizon-rs` model (`Node`, `Magnitude`/`AtLeast`, `BehavesAs`,
`TypeIs`, the gating booleans), `horizon-next` (the schema-derived
successor, its current Input/Output triad shape, and its already-
types-only `horizon-core`), and the real Stack A consumption in
`lojix-cli`.

## Headline

The split is sound and the intent re-bucketing in report 534 is
nearly exact — but two things sharpen it into a contract that the
rewrite can actually build against, neither of which 534 states:

1. **lojix needs BOTH raw and pretty — but only a thin pretty
   slice.** lojix is NOT a raw-only consumer. It reads two pretty
   gating values (`is_remote_nix_builder`, `nix_url`) to route
   builds and caches. CriomOS reads the *fat* pretty slice (lid
   switch, network-manager, extra-groups, behaves-as, magnitude
   ladders). So pretty horizon has two distinct consumers with
   very different appetites; the boundary must not assume "pretty =
   CriomOS-only."

2. **The schema-derived successor already proves the types-only
   shape `vu2k` asks for — in `horizon-core`, not in the `horizon`
   crate.** `horizon-core/schema/magnitude.schema` is the
   two-position `{} { Magnitude (...) }` types-only document with
   no Input/Output/Plane. That IS the raw-horizon shape. The
   `horizon` crate, by contrast, declares Input/Output and emits a
   full Signal/Nexus/Sema triad — the wrong runtime shape for a
   projection hack per `tvbn`/`vu2k`. The split therefore maps
   cleanly onto an existing, demonstrated schema feature; raw
   horizon does not need a new schema capability invented, it needs
   the types-only document shape that `horizon-core` already runs.

## 1. The clean boundary — a crisp RAW/PRETTY contract

The 534 re-bucketing is correct in spirit but stated as a flat
ten-item table. Grounding it in the actual `Node` struct
(`horizon-rs/lib/src/node.rs`) yields a sharper rule. The current
`Node` is a *fused* record — it interleaves four field classes that
the split must cleave apart. The cleaving rule:

### RAW horizon = the typed cluster-data model + identity derivations

RAW carries (a) input pass-through and (b) *identity/connectivity*
derivations — things every consumer needs as ground truth, computed
once, with no policy in them. From the current `Node`:

- **Input pass-through**: `name`, `species`, `machine`,
  `link_local_ips`, `node_ip`, `wireguard_pub_key`, `nordvpn`,
  `wifi_cert`, `wants_printing`, `wants_hw_video_accel`,
  `router_interfaces`, `services` (the typed `NodeService` enum).
- **Identity / connectivity** (always-derived, policy-free):
  `criome_domain_name`, `system`, `ssh_pub_key`, `nix_pub_key`,
  `ygg_pub_key`/`ygg_address`/`ygg_subnet`, the rendered
  `ssh_pub_key_line` / `nix_pub_key_line` newtypes.
- **Cross-node fan-in lists** (viewpoint-only, but still RAW
  identity rollups): `ex_nodes_ssh_pub_keys`,
  `dispatchers_ssh_pub_keys`, `admin_ssh_pub_keys`,
  `cluster.trusted_build_pub_keys`.
- **Arch resolution** (`resolve_arch`) and **typed validation**
  (`validate_tailnet_controller_singleton`, trust=Zero drop) — the
  computation that produces the RAW model, living *in* raw horizon.
- **Secret-binding resolution map** — the secret-reference
  resolution (`SecretReference` / `wpa3_sae_password`).

The test for RAW (lifted from `horizon-rs/INTENT.md`'s proposal-
boundary rule, generalised to the output side): **a field is RAW if
it is either authored cluster data or a policy-free identity
derivation that every consumer would otherwise recompute
identically.** No `>=`, no `&&` of role flags, no threshold — those
are decisions, and decisions are PRETTY.

### PRETTY horizon = the typed pre-derivation layer (decisions resolved in Rust)

PRETTY carries the computed *decisions* — every field whose value is
a boolean/threshold/policy resolution that a consumer would
otherwise have to compute. From the current `Node`:

- **Magnitude ladders** — `size: AtLeast`, `trust: AtLeast`. The
  `AtLeast { min, medium, large, max }` booleans ARE pre-derived
  threshold decisions; per `9p8v` the magnitude is *resolved* here,
  not emitted as a raw ordinal for Nix.
- **Gating booleans** — `is_fully_trusted`, `is_remote_nix_builder`,
  `is_dispatcher`, `is_nix_cache`, `is_large_edge`,
  `enable_network_manager`, `has_video_output`, the `has_*` pubkey
  booleans, `chip_is_intel`, `model_is_thinkpad`.
- **Behaves-as / type-is grouped flags** — `BehavesAs`, `TypeIs`,
  `ComputerIs` (role projection decisions).
- **Lid-switch policy** — `handle_lid_switch{,_external_power,_docked}`
  (`LidSwitchAction`), the `BehavesAs::lid_switch_policy` output.
- **Derived routing/capacity values** — `max_jobs`, `build_cores`,
  `nix_cache_domain`, `nix_url`, `cache_urls`, `builder_configs`,
  `use_colemak`, the trust-gated `extra-groups` list (per 534).

The load-bearing property from `9p8v`: **every PRETTY value is
resolved in typed Rust inside pretty-horizon; Nix receives a
finished value.** The `at-least` comparison, the `&&` of role flags,
the lid-switch branch — all run in Rust. Nix is a pure consumer.

### The cleave, stated as a type contract

Today `Node` is one fused struct. The split makes it two nouns:

- `RawNode` — pass-through + identity derivations + fan-in lists.
- `PrettyNode` — the decision fields, computed *from* a `RawNode`
  (reach for `impl From<&RawNode> for PrettyNode`, or a method
  `RawNode::derive_pretty(&self, ctx) -> PrettyNode`, per the
  verb-belongs-to-noun rule; NOT a free `fn project_pretty`).

`PrettyNode` borrows/references the `RawNode` rather than copying its
identity fields — this is where `a2t4`'s type-reuse axis bites
(below, §5). The projected `Horizon` becomes `Horizon { cluster,
raw: RawNode, pretty: PrettyNode, ex_raw, ex_pretty, users }`, or
more minimally a `Horizon` whose `node` carries `raw` + `pretty`
sub-records. The exact container shape is an implementation
decision for the agent in the project; the *contract* is: identity
in raw, decisions in pretty, pretty derived from raw, both typed.

## 2. What lojix actually consumes — BOTH, but a thin pretty slice

This is the finding that most sharpens the boundary, and it
contradicts a naive reading of the split ("raw = the model, pretty =
what Nix/CriomOS consume"). lojix is itself a horizon consumer, and
it consumes pretty fields directly in Rust — it never touches Nix.

Grounding in Stack A (`lojix-cli`, the functionality reference the
lojix daemon ports) and `lojix/ARCHITECTURE.md` §"Cluster proposal
source — `goldragon` (read per request via horizon-rs)":

### lojix's RAW consumption

- `criome_domain_name` → `SshTarget::from_node` (all SSH/`nix copy`
  addressing; `host.rs`).
- `ssh_pub_key` → host-key verification (`check.rs:138`).
- `system` → target build system (`deploy.rs:108`).
- `users` map → `validate_home_user` (`deploy.rs:98`).
- `nix_pub_key_line` / `cluster.trusted_build_pub_keys` → trust
  material.

### lojix's PRETTY consumption (the thin slice)

- `node.is_remote_nix_builder` → gates whether a sibling node is a
  valid `--builder` target (`deploy.rs:60`,
  `resolve_builder_target`). A pretty gating boolean.
- `node.nix_url` → `ExtraSubstituters::from_horizon_nodes` builds
  the binary-cache substituter endpoints (`deploy.rs:211,232,241`).
  A pretty derived routing value.

### The consequence for the boundary

lojix needs **raw + a thin pretty slice** — specifically the
*deploy-routing* pretty fields (`is_remote_nix_builder`, `nix_url`,
and transitively the values `builder_configs`/`cache_urls` roll up).
It does NOT need the *OS-config* pretty fields (lid-switch,
`enable_network_manager`, extra-groups, `behaves_as`, `computer_is`,
the full ladder set) — those exist solely for CriomOS to render an
OS configuration.

This says pretty horizon has **two consumer profiles**, and the
boundary spec should name them:

- **Deploy-routing pretty** — `is_remote_nix_builder`, `is_nix_cache`,
  `nix_url`, `nix_cache_domain`, `builder_configs`, `cache_urls`,
  `max_jobs`. Consumed by lojix (in Rust) AND CriomOS (in Nix).
- **OS-config pretty** — lid-switch policy, `enable_network_manager`,
  trust-gated extra-groups, `behaves_as`, `type_is`, `computer_is`,
  `has_video_output`, the size/trust ladders. Consumed only by
  CriomOS (in Nix).

The split is still *one* pretty layer (don't over-fragment into
three crates — `a2t4` wants minimal). But the contract should
document that lojix reaches into the deploy-routing subset, so the
pretty layer is shaped as a Rust-consumable typed record, not merely
a Nix-attrset emitter. If pretty horizon were designed as "the thing
that emits Nix variables," lojix would have no clean typed surface to
read `is_remote_nix_builder` from. **Recommendation: pretty horizon's
primary form is a typed Rust record (`PrettyNode`), and the
Nix-attrset projection is a serialisation OF that record, not its
identity.**

## 3. Keeping the promotion door open (`avvh`) — what to do NOW

`avvh` is explicit that the split is a forward-integration seam:
raw horizon stays a clean minimal typed model so it can later be
**promoted into a real component** in a larger component system,
while pretty horizon stays the typed derive layer. The promotion
question is the `x8iv` open fork: does horizon become a full
component-triad?

### What promotion would look like

A promoted raw horizon becomes a triad component: `horizon` daemon +
`signal-horizon` (wire) + `meta-signal-horizon` (policy). Its Input
would be `Project ClusterProposal`; its Output the projected raw
model. At that point lojix would stop linking horizon-rs in-process
and instead send a `signal-horizon` `Project` request over a socket,
receiving the raw model (+ deploy-routing pretty) as a reply. This
is exactly the shape the `wv63` contract/daemon-split intent
describes for spirit: wire-only contract (Input/Output + records),
Nexus/Sema planes only in the daemon.

### The "prepare the seam during cutover" timing (`9p8v` + `avvh`)

`9p8v` carries the `m85j` timing verbatim: the pretty layer lands
**after cutover**, parity is the bar, the collapse does NOT gate
cutover, and the seam is *prepared during cutover so the later step
is a drop-in*. Applied to promotion, the concrete "do it NOW" list:

1. **Make raw horizon a standalone crate with NO pretty
   dependency.** Raw must not import pretty; pretty imports raw.
   This is the single most important seam-preparation move: a raw
   crate that already compiles without pretty is already shaped
   like a component's types crate. (horizon-next ALREADY models
   this: `horizon-core` is a types-only crate that the `horizon`
   crate imports across the boundary — `record /39` cross-crate
   import proof. The raw/pretty split is the same pattern applied
   one level up.)

2. **Express the raw model as a types-only schema document**
   (§5 below) so its datatypes generate without an Input/Output
   plane. A types-only raw module is *promotable*: adding a
   triad later means adding an Input/Output document that
   imports the raw types — not rewriting them.

3. **Keep the projection ENTRY-POINT a single method on
   `ClusterProposal`** (`project(viewpoint) -> raw`, with pretty
   derived after). When promoted, that method becomes the daemon's
   Nexus `Project` verb body unchanged — the behaviour moves, the
   logic doesn't get rewritten.

4. **Do NOT prematurely add Input/Output to raw horizon.** This is
   the active error in horizon-next today (§4) — the `horizon`
   crate already declares Input/Output and emits a triad while
   `tvbn` says horizon is a projection hack, not a triad. Adding the
   plane now is the *opposite* of preparing a clean seam: it bakes
   in a runtime shape that `tvbn`/`vu2k` reject and that a later
   promotion would have to unwind. Prepare the seam by keeping raw
   types-only and the projection a plain method; mint the plane only
   when the psyche decides promotion (`x8iv`) is on.

The net: promotion is a clean step IF raw is (a) a standalone
types-only crate, (b) with the projection as a method, (c) without a
premature plane. All three are *structural* choices the rewrite makes
now at near-zero cost; none requires building the triad now.

## 4. Position on the `x8iv` fork — build the split in horizon-next, CONFIRMED, with a correction

534 recommends building the raw/pretty split in the schema-derived
successor (`horizon-next`), not retrofitting the `horizon-rs` hack.
**Confirmed — with a sharpening correction about what "the
successor" currently is.**

Reasons to confirm:

- `qkvx` (typed-source-first) and the schema-rust-next pipeline mean
  the successor *generates* its datatypes from schema. Retrofitting
  the split into hand-written `horizon-rs` would split hand-written
  structs that are slated for deletion at cutover — wasted work
  against a retiring artifact.
- horizon-next already demonstrates the enabling pieces: collections
  in schema, cross-crate import (`horizon-core` → `horizon`), and —
  decisively — the **types-only-module shape in `horizon-core`**.
  The raw/pretty split is the same cross-crate types-only pattern
  applied to the cluster model.

The correction (challenge to a naive reading): **horizon-next as it
stands is NOT yet the right shape for raw horizon.** Its `horizon`
crate declares `Input (Project ClusterProposal)` and `Output` and
emits a full Signal/Nexus/Sema triad with a running three-engine
chain. That is the "signal-leaning component" shape its own
ARCHITECTURE.md flags — and it directly contradicts `tvbn` (horizon
is a hack/projection surface, NOT a triad) and `vu2k` (a pure
projection library needs the types-only shape so datatypes generate
without forcing a signal plane). So the recommendation is not "build
in horizon-next as-is" but:

> Build the raw/pretty split in horizon-next, adopting the
> **types-only-module schema shape that `horizon-core` already
> proves** for the raw model — and DROP the Input/Output/Plane
> triad from the projection crate until the `x8iv` promotion
> decision lands. The schema-derived successor is the right home;
> its current triad runtime shape is the part to correct.

This also resolves a latent inconsistency: horizon-next's
`INTENT.md` still says "the runtime shape is open (signal-only?
triad? library?)" and "declaring Input/Output makes Horizon a
signal-leaning component; that is what this concept demonstrates."
But `tvbn`/`vu2k` have since *closed* that trichotomy in favour of
the pure-library shape. **horizon-next/INTENT.md is stale against
`tvbn`/`vu2k` and should be refreshed** (flagged for the synthesis
agent; per the continuous-manifestation discipline this is the
project agent's same-branch update).

## 5. The types-only-module schema shape (`vu2k`) — yes, this is exactly what raw horizon needs

`vu2k` states: a pure-projection horizon with no runtime triad needs
a **types-only-module schema variant** so its datatypes generate
without forcing an Input or Output signal plane. The report-39/42
finding behind it: a 4-position schema document (imports + Input +
Output + namespace) forces a signal plane; a pure library must not be
forced into one.

This is not speculative — `horizon-core` already runs it. Its
`schema/magnitude.schema` is the **two-position document**:

```
{}
{
  Magnitude (Zero Min Low Medium High Max)
}
```

Imports (empty) + Namespace only. NO Input, NO Output. The emitted
`magnitude.rs` carries only the `Magnitude` type + its NOTA codec —
no `Plane`, no `OriginRoute`, no `NexusMail`, no runtime floor
(report /42 D2/D3: the generic runtime floor lives once in the
component, never duplicated into imported type libraries). It dropped
from ~520 to ~150 lines precisely by being types-only.

**So raw horizon's schema is a types-only (two-position) document**:
imports (it would import `Magnitude` from `horizon-core`) +
namespace declaring `ClusterProposal`, `NodeProposal`, `NodeService`,
`RawNode`, the name newtypes, etc. — and NO Input/Output. The
datatypes generate; no signal plane is forced. Pretty horizon is
*also* a types-only module (it declares `PrettyNode` and the
decision records) — it too needs no plane, because pretty is a Rust
derivation layer, not a wire endpoint. **Both raw and pretty horizon
are types-only schema documents until/unless promotion (`x8iv`)
mints a triad.**

The one open mechanical question for the project agent: the current
`horizon-core` Magnitude ladder is **6-point**
(`Zero Min Low Medium High Max`) while `horizon-rs`'s authoritative
`Magnitude` is **5-point** (`Zero Min Medium Large Max`, with the
`AtLeast { min, medium, large, max }` ladder). These must be
reconciled before the schema-derived raw model can replace
horizon-rs at parity — the `at_least`/ladder derivation and every
`sized_at_least.large`/`.min` gate in the projection depends on the
exact ladder shape. Flagged as a parity gap, not a boundary
question.

## Concrete gap / recommendation list (for the synthesis agent)

1. **lojix consumes BOTH raw and a thin pretty slice — not raw-only.**
   It reads `is_remote_nix_builder` (`deploy.rs:60`) and `nix_url`
   (`deploy.rs:211-241`) directly in Rust. The boundary spec must
   name two pretty consumer profiles: **deploy-routing pretty**
   (lojix + CriomOS) vs **OS-config pretty** (CriomOS only). Pretty
   horizon's primary form is a typed Rust record; the Nix attrset is
   a serialisation of it, not its identity.

2. **Cleave the fused `Node` into `RawNode` + `PrettyNode`.** RAW =
   pass-through + policy-free identity derivations + fan-in lists +
   arch resolution + validation + secret-binding. PRETTY = ladders,
   gating booleans, behaves-as/type-is/computer-is, lid-switch
   policy, derived routing/capacity values. Test: a field is PRETTY
   if its value is a decision (`>=`, `&&` of flags, threshold,
   policy branch). `PrettyNode` derives FROM `RawNode`
   (`impl From<&RawNode>` / `RawNode::derive_pretty`), referencing
   raw identity fields rather than copying — the `a2t4` type-reuse
   axis.

3. **Confirm `x8iv`: build in horizon-next — but correct its current
   shape.** horizon-next is the right home (schema-derived,
   types-only `horizon-core` already proves the pattern), but its
   `horizon` crate currently declares Input/Output and emits a full
   triad — the wrong runtime shape per `tvbn`/`vu2k`. Drop the
   Input/Output/Plane from the projection crate; make raw + pretty
   types-only modules; keep projection a method on `ClusterProposal`.

4. **Raw AND pretty are both types-only (two-position) schema
   documents** — exactly the `vu2k` shape that `horizon-core` runs
   (`{} { ... }`, imports + namespace, no Input/Output). This is
   what lets the datatypes generate without forcing a signal plane.
   Mint a triad only when `x8iv` promotion is decided.

5. **Promotion-seam prep to do NOW (zero-cost, `9p8v`+`avvh`
   timing):** (a) raw is a standalone crate with no pretty
   dependency; (b) raw is a types-only schema document; (c)
   projection is a single method that becomes the future daemon's
   Nexus `Project` body unchanged; (d) do NOT add Input/Output to
   raw prematurely. Promotion then = add a wire document importing
   raw types + move the method into the daemon's Nexus engine — not
   a rewrite.

6. **Stale-doc flags for the project agent (continuous
   manifestation, same branch as the work):** (a)
   `horizon-next/INTENT.md` still calls the runtime shape "open" and
   frames Input/Output as the demonstrated direction — stale against
   `tvbn`/`vu2k` which closed that trichotomy toward the pure-library
   shape. (b) Magnitude ladder divergence: `horizon-core` is 6-point
   (`Zero Min Low Medium High Max`), `horizon-rs` is 5-point
   (`Zero Min Medium Large Max`); reconcile before the schema-derived
   raw model can hit parity, since every ladder gate in the
   projection depends on the exact shape.

Per psyche 2026-06-05 (`9p8v`, `avvh`, `a2t4`, `vu2k`, `tvbn`,
`x8iv`).

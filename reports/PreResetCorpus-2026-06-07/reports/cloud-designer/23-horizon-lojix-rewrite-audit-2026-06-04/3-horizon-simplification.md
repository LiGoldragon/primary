# Horizon Simplification Audit (B1)

Cloud-designer lane, read-only, 2026-06-04. Audits how far the
horizon-rs OUTPUT model can collapse toward its INPUT model under the
psyche's minimal-Horizon intent: Horizon expresses only WHAT, emits
simple typed facts, and pushes the more complex composed decisions into
Nix. Input types are reused as output types where shape-equivalent.

## Intent this audit serves

- 7ggswqdxqqz97za6o7w (High): Horizon expresses only WHAT, never HOW,
  never decision-making; Horizon emits simple typed facts, Nix composes
  the complex decisions. Complexity stays OUT of Horizon.
- 10v4744869xt5spwnam (High): Horizon data types must not repeat across
  inputs and outputs; reuse the input type as the output type where it
  can serve.
- 1bok2bxvu3beswif9mv (High): Horizon is a hack-for-now, stays the
  simple projection surface, NOT a full triad component. Logix carries
  the runtime triad.
- 431pfi7l1akuu22b01b (High): cluster-data must be TYPED end-to-end,
  typed-source-first. Crucially this correction is about typed INPUT
  (real NodeService enum variant authored in datom.nota, projected
  typed, consumed typed) — it is NOT a mandate that every derived
  output boolean live in Rust. The reconciliation in §6 turns on this.

## 1. Inventory of OUTPUT-only derived fields

Two source shapes exist. Stack A main lives in
`/git/github.com/LiGoldragon/horizon-rs/lib/src/` (flat module). The
lean rewrite lives at
`/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape/lib/src/`
with a `proposal/` (input) vs `view/` (output) split. The lean shape
has ALREADY removed some derived fields (`has_video_output`, the three
`handle_lid_switch_*`, `type_is`, and collapsed the `is_nix_cache` trio
and ygg trio). The inventory below cites Stack A main as the baseline
and notes lean-shape status.

### 1a. Per-node always-derived (the `Node` output struct)

`Node` is the output type; line cites are Stack A `node.rs` unless
marked lean.

| Field | Type | Derivation | Stack A site | Lean status |
|---|---|---|---|---|
| `criome_domain_name` | `CriomeDomainName` | `format!("{node}.{cluster}.criome")` | node.rs:339, name.rs:101 | kept (view/node.rs:52) |
| `system` | `System` | `resolved_arch.system()` (arch→tuple) | node.rs:426, species.rs:94 | kept |
| `max_jobs` | `u32` | `nix_builder_maximum_jobs().unwrap_or(1)` | node.rs:395 | kept; `build_cores` dropped (was `= max_jobs`) view/node.rs:62 |
| `build_cores` | `u32` | `= max_jobs` (pure alias) | node.rs:396 | REMOVED in lean |
| `ssh_pub_key_line` | `SshPubKeyLine` | `"ssh-ed25519 " + key` | node.rs:388, pub_key.rs:52 | kept |
| `nix_pub_key_line` | `Option<NixPubKeyLine>` | `"{domain}:{key}"` | node.rs:379, pub_key.rs:110 | kept |
| `nix_cache_domain` | `Option<CriomeDomainName>` | `nix.<domain>` when `is_nix_cache` | node.rs:380, name.rs:105 | collapsed into `nix_cache: Option<NixCache>` view/node.rs:94,125 |
| `nix_url` | `Option<String>` | `format!("http://{domain}")` | node.rs:385 | collapsed into `NixCache.url` |
| `is_fully_trusted` | `bool` | `trust == Max` | node.rs:355 | kept |
| `is_remote_nix_builder` | `bool` | `has_service(NixBuilder) && online && is_fully_trusted && has_base_pub_keys` | node.rs:363 | kept |
| `is_dispatcher` | `bool` | `!center && is_fully_trusted && size.min` | node.rs:367 | kept |
| `is_nix_cache` | `bool` | `has_service(NixCache) && online && is_fully_trusted && has_base_pub_keys` | node.rs:368 | folded into `nix_cache.is_some()` |
| `is_large_edge` | `bool` | `size.large && behaves_as.edge` | node.rs:372 | kept |
| `enable_network_manager` | `bool` | `size.min && !iso && !center && !router` | node.rs:373 | kept |
| `has_nix_pub_key` | `bool` | `nix_pub_key.is_some()` | node.rs:347 | REMOVED (consumer reads `nixPubKey != null`) |
| `has_ygg_pub_key` | `bool` | `ygg_pub_key.is_some()` | node.rs:348 | REMOVED |
| `has_ssh_pub_key` | `bool` | constant `true` (ssh required) | node.rs:349 | REMOVED |
| `has_wireguard_pub_key` | `bool` | `wireguard_pub_key.is_some()` | node.rs:350 | REMOVED |
| `has_nordvpn_pub_key` | `bool` | `= self.nordvpn` (pure alias) | node.rs:351 | REMOVED |
| `has_wifi_cert_pub_key` | `bool` | `= self.wifi_cert` (pure alias) | node.rs:352 | REMOVED |
| `has_base_pub_keys` | `bool` | `has_nix && has_ygg && has_ssh` | node.rs:353 | REMOVED |
| `has_video_output` | `bool` | `= behaves_as.edge` (pure alias) | node.rs:375 | REMOVED in lean (view/node.rs:73) |
| `chip_is_intel` | `bool` | `resolved_arch.is_intel()` | node.rs:390 | kept |
| `model_is_thinkpad` | `bool` | `model.known().is_some_and(is_thinkpad)` | node.rs:397 | kept |
| `handle_lid_switch` | `LidSwitchAction` | `center→Ignore else Suspend` | node.rs:211,461 | REMOVED in lean (derive in Nix) |
| `handle_lid_switch_external_power` | `LidSwitchAction` | `center→Ignore, low_power→Suspend, else Lock` | node.rs:216,462 | REMOVED in lean |
| `handle_lid_switch_docked` | `LidSwitchAction` | `edge→Lock else Ignore` | node.rs:223,463 | REMOVED in lean |
| `behaves_as` | `BehavesAs` (9 bools) | `BehavesAs::derive(type_is, machine, io_disks_empty)` | node.rs:182,360 | kept (view/node.rs:144) |
| `type_is` | `TypeIs` (9 bools) | one-hot expansion of `species` enum | node.rs:166,358 | REMOVED in lean (consumers read `species` / `behaves_as`) |

### 1b. `BehavesAs` sub-bools (the 9-flag grouped output)

All derived from `type_is` + `machine` in `BehavesAs::derive`
(node.rs:182-204): `large_ai`, `router`, `edge`, `center`, `next_gen`,
`low_power` are pure functions of `species`; `bare_metal` /
`virtual_machine` are pure functions of `machine.species` (lean:
`placement`); `iso = !virtual_machine && io.disks.is_empty()`.

### 1c. Per-user always-derived (`User` output struct)

Stack A `user.rs`: `has_pub_key` (user.rs:85), `email_address`
(`{name}@{cluster}.criome.net`, user.rs:92), `matrix_id`
(`@{name}:{cluster}.criome.net`, user.rs:93), `git_signing_key`
(`&{keygrip}`, user.rs:86), `use_colemak` (`keyboard==Colemak`,
user.rs:130), `use_fast_repeat` (`fast_repeat.unwrap_or(true)`,
user.rs:131), `is_multimedia_dev` / `is_code_dev` (species match,
user.rs:118,132), `preferred_editor` (editor-or-default, user.rs:119),
`ssh_pub_keys` / `ssh_pub_key` (line rendering, user.rs:87-90),
`extra_groups` (trust-ladder-gated group list, user.rs:96-115),
`enable_linger` (`trust.max && viewpoint_center`, user.rs:116).

### 1d. Cluster-level roll-up (`Cluster` output struct)

`tailnet_base_domain` (`tailnet.{cluster}.criome`, horizon.rs:98,
name.rs:74) and `trusted_build_pub_keys` (fan-in: every node's
`nix_pub_key_line`, horizon.rs:99-102). Lean `view/cluster.rs` adds
`lan`, `resolver`, `tailnet`, `ai_providers`, `vpn_profiles`,
`secret_bindings` — more roll-ups, not fewer.

### 1e. Viewpoint-only (the ex-nodes/viewpoint split)

Filled by `Node::fill_viewpoint` (node.rs:485-547): `io`,
`use_colemak`, `computer_is`, `builder_configs` (cross-node fan-in of
remote builders), `cache_urls` (fan-in of sibling cache URLs),
`ex_nodes_ssh_pub_keys`, `dispatchers_ssh_pub_keys`,
`admin_ssh_pub_keys` (cross user×node trust join), and
`wireguard_untrusted_proxies`. The whole `ex_nodes` vs `node` split in
`Horizon` (horizon.rs:18-23) is itself an output-only structural device.

## 2. Classification: KEEP-IN-RUST vs MOVE-TO-NIX

The dividing line: KEEP what is genuine typed validation, arch
resolution that requires a cross-node lookup, name/string rendering
where a typed newtype enforces a real invariant, or cross-node fan-in
that Nix would do clumsily. MOVE the gating booleans, the at-least
ladders, the one-hot enum expansions, and the pure aliases — anything
Nix can compose in one line from raw typed facts already on the wire.

### KEEP-IN-RUST

- `criome_domain_name`, `nix_cache.domain` — typed `CriomeDomainName`
  newtype; the name shape is a real invariant and many consumers key on
  it. Keep the rendering in Rust, emit the typed value.
- `system` and arch resolution (`resolve_arch`, node.rs:554) — pod arch
  defers to super-node; this is a genuine cross-node lookup with typed
  failure (`UnresolvableArch`, `MissingSuperNode`). Nix should not
  re-walk the super-node graph. KEEP. `chip_is_intel` rides on the same
  resolved arch — keep as a thin field or let Nix read `arch==X86_64`.
- `ssh_pub_key_line` / `nix_pub_key_line` — pre-rendered line forms feed
  `programs.ssh.knownHosts` and `trusted-public-keys` verbatim
  (client.nix:77, builder.nix). Typed newtypes carry the format
  invariant. KEEP the rendering.
- `trusted_build_pub_keys` (cluster), `builder_configs`, `cache_urls`,
  `dispatchers_ssh_pub_keys`, `ex_nodes_ssh_pub_keys`,
  `admin_ssh_pub_keys` — all CROSS-NODE FAN-IN. Each gathers data across
  the whole node/user set from the viewpoint node's perspective. Nix
  CAN do this (it has the full attrset) but it is exactly the
  decision-shaped composition that is clearer typed in Rust once, and
  `admin_ssh_pub_keys` is a user×node trust join with dedup
  (node.rs:519-535) that is genuinely awkward in Nix. KEEP — but note
  these are the strongest candidates for "Logix territory" later, since
  they are the real cross-node logic Horizon-as-hack carries today.
- Validation: `validate_tailnet_controller_singleton` (horizon.rs:148),
  `node_trust` min-fold (horizon.rs:174), trust=Zero node drop
  (horizon.rs:45), keygrip/pubkey/base64 newtype validators
  (pub_key.rs, name.rs:138). KEEP — typed validation is the WHAT-is-
  valid contract, not a HOW decision.
- `email_address`, `matrix_id`, `git_signing_key` (user) — string
  rendering of identity; cheap to keep, mild candidate to move.

### MOVE-TO-NIX

- `type_is` (9 one-hot bools) — pure expansion of the `species` enum.
  Nix reads `species` and matches. Already REMOVED in lean. MOVE.
- The `behaves_as` 9 bools — every one is a one-line function of
  `species` (+ `machine.species`/`placement` for 2, + `io.disks==[]`
  for `iso`). These are the textbook HOW-composition: `center =
  species ∈ {Center, LargeAi, LargeAiRouter}`. Nix composes this
  trivially from the `species` fact. This is the single biggest
  MOVE-to-Nix opportunity the lean shape has NOT yet taken.
- `is_large_edge` = `size.large && edge`, `enable_network_manager` =
  `size.min && !iso && !center && !router`, `is_dispatcher` =
  `!center && fully_trusted && size.min` — pure boolean composition
  over facts already on the wire (`size` ladder, trust, behaves-as).
  MOVE; Nix gates inline.
- The `has_*` pubkey booleans (`has_nix_pub_key`, `has_ygg_pub_key`,
  `has_ssh_pub_key`, `has_wireguard_pub_key`, `has_nordvpn_pub_key`,
  `has_wifi_cert_pub_key`, `has_base_pub_keys`) — null-checks and pure
  aliases of fields already present. Already REMOVED in lean. MOVE
  (consumer reads `nixPubKey != null`).
- `build_cores` (= `max_jobs`), `has_video_output` (= `edge`),
  `has_nordvpn_pub_key` (= `nordvpn`) — PURE ALIASES, zero derivation.
  Already removed in lean. MOVE / delete.
- `handle_lid_switch{,_external_power,_docked}` — three systemd-policy
  enums derived from `center`/`edge`/`low_power`. This is HOW (a power
  policy decision), authored once in Rust today (node.rs:210-233),
  consumed verbatim into `logind.settings.Login` (metal:551-554).
  Already REMOVED in lean (view/node.rs:75 comment: consumers derive
  from `behaves_as`). MOVE — it is decision-making, the exact thing
  intent 7ggswqdxqqz97za6o7w pushes to Nix.
- `at_least` ladders (`size`, `trust` → 4 bools each) — the `AtLeast`
  expansion (magnitude.rs:29). Borderline: it is a one-hot-ish ladder
  Nix can compute from the raw `Magnitude` with `>=`. But the raw
  `Magnitude` ordinal is NOT currently on the wire (consumers only see
  the ladder). MOVE is possible only if Horizon emits the ordinal
  `Magnitude` and Nix derives the ladder — a clean trade (emit the WHAT
  = the magnitude; Nix composes the thresholds it cares about).
- User `is_code_dev`, `is_multimedia_dev`, `use_colemak`,
  `use_fast_repeat`, `preferred_editor` defaulting — species matches
  and unwrap-or-default. MOVE the matches; the default-resolution
  (`editor.unwrap_or(...)`) is a mild HOW that Nix can also do.
- `extra_groups` (user.rs:96-115) — a trust-ladder-gated hardcoded
  group list. This is pure CriomOS policy (HOW), not cluster WHAT.
  STRONG MOVE: the group list belongs in the CriomOS Nix module, gated
  on the user's trust ladder, not baked into Horizon output.

## 3. The leaner target shape

The target: Horizon's output is the typed proposal echoed back PLUS a
small irreducible set of derivations Nix genuinely cannot (or should
not) do. The input type IS the output type wherever shape-equivalent.

### What collapses (input reused as output)

The lean shape already reuses `Machine`, `Io`, `NodeService`,
`RouterInterfaces`, `WireguardProxy`, `YggPubKeyEntry`,
`NodePlacement`, `Substrate`, `Resources` directly from `proposal::*`
in the view (proposal.rs:26-45 re-exports; view/node.rs:17 imports
them). Extend this: stop projecting `size`/`trust` into `AtLeast`
ladders — emit the raw `Magnitude` ordinal (the input type), let Nix
ladder it. Drop the separate `Node` output struct's pass-through block
(node.rs:30-52, the 18 fields copied verbatim from `NodeProposal`):
those should BE the proposal fields, not re-declared.

### What horizon-rs still emits (the irreducible core)

1. The typed proposal, validated and echoed: every input field, typed,
   after validation and trust-fold dropping of distrusted nodes.
2. Resolved arch + `system` (cross-node super-node lookup, typed
   failure).
3. Rendered typed name/line newtypes: `CriomeDomainName`,
   `SshPubKeyLine`, `NixPubKeyLine`, `tailnet_base_domain`,
   `nix_cache.{domain,url}` — kept because the newtype carries a real
   format invariant and consumers paste them verbatim.
4. Cross-node fan-in lists: `builder_configs`, `cache_urls`,
   `*_ssh_pub_keys`, `trusted_build_pub_keys`, `admin_ssh_pub_keys`.
   These are the genuine cross-node joins. (They are also the cleanest
   future hand-off to Logix when Horizon stops being the hack.)
5. The cluster secret-binding resolution map (lean view/cluster.rs:56)
   — name→backend lookup table, a real resolution.

Everything in the MOVE-TO-NIX list of §2 disappears from the output.
The `behaves_as` block, `type_is`, all gating booleans, lid policy,
the at-least ladders, `extra_groups`, and the pure aliases are no
longer Horizon's concern — Nix composes them from `species`, `size`,
`trust`, `placement`, and the pubkey-presence facts that are already
on the wire.

### Magnitude of the collapse

Stack A `Node` carries roughly 50 fields, ~30 of them output-only
derived. The lean shape already cut ~9. The full target cuts the
behaves-as 9, type-is 9, the gating booleans (~5), lid (3), and the
ladders — leaving Horizon emitting the proposal-echo + ~6 cross-node
fan-in lists + ~5 rendered name/line types + arch. Output-only field
count drops from ~30 to under 12, and the dropped ones are exactly the
HOW-decisions.

## 4. Trade-off: losing Rust type-checking on moved derivations

Pushing derivations to Nix loses Rust's compile-time checking of those
specific expressions. The reconciliation with 431pfi7l1akuu22b01b:

That correction is about typed INPUT, not output booleans. It mandates
that a node-service feature be a real typed `NodeService` enum variant,
authored in datom.nota, projected typed, consumed typed — NOT matched
against a string with an or-empty-list default. The thing it protects
is the FACT (the WHAT): does this node run a NixBuilder? That stays
fully typed: `NodeService::NixBuilder` is a real variant
(services.rs:32), authored in goldragon datom.nota
(`(NixBuilder None)` at datom.nota:124, `(NixBuilder (Some 6))` at
datom.nota:96), projected typed, and on the wire as a typed value.

What moves to Nix is the COMPOSITION over those typed facts — e.g.
`is_remote_nix_builder = has(NixBuilder) && online && fully_trusted &&
has_base_pub_keys`. The inputs to that boolean are all typed facts.
Moving the `&&` chain to Nix does not reintroduce a string key; it
relocates a boolean composition. The typed-source-first invariant is
preserved as long as:

- Every WHAT-fact stays a typed variant authored at source (services
  stay enum variants, never string keys — the VmTesting failure mode
  the correction names stays prevented).
- Nix composes booleans only from typed facts present on the wire,
  never by re-parsing a string or defaulting a missing field to a
  permissive value (no `node.services or []`).

The residual type-safety loss is real but small: a typo in a Nix
boolean expression fails at Nix eval, not Rust compile. This is
acceptable because (a) these are gating booleans evaluated every build,
so a wrong one surfaces immediately; (b) the alternative — keeping
~30 derived bools in Rust — is precisely the complexity intent
7ggswqdxqqz97za6o7w says must leave Horizon; (c) the HIGH-value typed
checks (arch resolution, key format, trust fold, service-variant
identity) all STAY in Rust. We trade compile-time checking of one-line
boolean composition for a dramatically smaller Horizon — exactly the
intended bargain. Horizon stays the WHAT surface; Nix owns the HOW.

One guard worth adding to CriomOS: a single Nix module that derives
`behavesAs` / the ladders ONCE from raw facts and re-exports them, so
the composition lives in one place rather than scattered across
consumer modules. That preserves the dont-repeat-the-derivation
ergonomic the lean view/node.rs:5 docstring values, without keeping it
in Rust.

## 5. Concrete before/after

### 5a. The NodeService / NixBuilder path (the typed-source spine)

This path is ALREADY correct per 431pfi7l1akuu22b01b and must stay so;
the change is only that the DERIVED boolean leaves Rust.

BEFORE (Stack A). Authored typed in goldragon
(`datom.nota:96`): `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`.
horizon-rs projects a derived boolean (node.rs:363):

```
let is_remote_nix_builder = self.has_service(NodeServiceKind::NixBuilder)
    && online && is_fully_trusted && has_base_pub_keys;
```

emitted as `node.isRemoteNixBuilder`, consumed verbatim
(builder.nix:51): `sshServe.enable = isRemoteNixBuilder;`.

AFTER (leaner target). The typed fact `services: Vec<NodeService>`
stays on the wire (input type reused as output, no parallel type). The
`&&` chain moves to a single CriomOS Nix derive module:

```nix
isRemoteNixBuilder =
  (lib.any (s: s ? NixBuilder) node.services)
  && (node.online or true)
  && node.trust.max
  && (node.nixPubKey != null && node.yggdrasil != null);
```

The WHAT (`NixBuilder` is a typed variant, authored at source,
projected typed) is unchanged and fully typed. Only the boolean
composition relocated. No string key, no permissive default — the
typed-source-first contract holds.

### 5b. One derived boolean end-to-end: `behaves_as.center`

BEFORE (Stack A). `species: NodeSpecies` (typed input) →
`TypeIs::from_species` one-hots it (node.rs:167) → `BehavesAs::derive`
composes `center = type_is.center || large_ai` (node.rs:187) → emitted
as the `behavesAs.center` bool → consumed at nspawn.nix:12
(`size.large && behavesAs.center && ...`), llm.nix:140, client.nix:15.

AFTER (leaner target). Horizon emits only `species` (the typed WHAT).
CriomOS derive module composes once:

```nix
behavesAs.center =
  builtins.elem node.species [ "Center" "LargeAi" "LargeAiRouter" ];
```

Consumers read `behavesAs.center` exactly as before — the derive module
re-exports the same name, so consumer modules
(nspawn/llm/client/resolver) are untouched. The 9-bool `BehavesAs`
struct and `TypeIs` leave horizon-rs entirely; `species` (already a
typed `NodeService`-style enum) is the single fact that carries the WHAT.

### 5c. VmTesting — the cautionary contrast

The 431pfi7l1akuu22b01b correction names VmTesting as the anti-pattern:
it was matched as a STRING via `node.services` has/payload with a
`node.services or []` default fed by a synthetic fixture. Neither Stack
A nor the lean shape has a VmTesting variant today (grep finds none in
either `NodeService` enum). The leaner shape does NOT bring it back as
a string: if VM-testing capacity becomes a real cluster fact, it lands
as a typed `NodeService::VmTesting {}` variant (authored in datom.nota,
projected typed) — and any gating boolean over it composes in the Nix
derive module, never as a string match. The §2 MOVE-TO-NIX rule is
strictly: move boolean composition over TYPED facts; never move the
fact itself to a string.

## 6. Recommendation summary

The lean rewrite has started the collapse (removed the `has_*` bools,
`type_is`, lid policy, the alias fields, collapsed the cache and ygg
trios) but has NOT yet moved the largest pieces: the `behaves_as` 9
bools, the gating booleans (`is_dispatcher`, `is_large_edge`,
`enable_network_manager`), the at-least ladders, and `extra_groups`.
Finishing the collapse means: (1) emit raw `Magnitude` instead of
`AtLeast`; (2) emit `species` + `placement` and drop `behaves_as` /
gating bools; (3) move `extra_groups` to CriomOS; (4) add one CriomOS
`derive.nix` module that re-exports `behavesAs` + ladders from raw
facts so consumer modules stay untouched. Keep in Rust: arch
resolution, name/line newtype rendering, cross-node fan-in lists,
typed validation, and the secret-binding resolution map.

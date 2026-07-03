# Spirit A→B Mirror Stand-Up — Ground-Truth Findings + Decision Request

## Task and scope

Configure and prove the persistent one-directional Spirit A→B mirror on the two
standing prometheus guests (`mirror-alpha` = node A / source / `5::7`,
`mirror-beta` = node B / dest / `5::8`), baked into their CriomOS node configs,
activated without a host reboot, reboot-persistent; then prove the mirror and
seed a read-only copy of production Spirit data.

This round is **read-only reconnaissance + a decisive scope finding**. No host
mutation, no repo edit, no build was performed. The premise the brief inherited —
"the sender leg is CONFIG ONLY / no new engine code" — does **not** hold on landed
`main`; standing the stack up persistently requires new build + module authoring
and one genuine design decision. Details, evidence, and a decision menu below.

## Foundation confirmed healthy (the prior rounds' work is solid)

- prometheus: `is-system-running` = **running**, system profile **generation 51**
  (`/run/current-system` = `j1362haqmyh5ha7bg9ds780yzpsjchav-nixos-system-prometheus`),
  boot_id stable. Both guest units **active + running**: `microvm@mirror-alpha`,
  `microvm@mirror-beta`.
- Guests reachable: from ouranos via `ProxyJump prometheus` with the cluster admin
  key (agent key `SHA256:7gVtLCaV…`, the same key that authenticates prometheus
  root; guests trust the host's `adminSshPubKeys`). IPv6 literal needs bracket/config
  form — `ssh -J … root@5::7` mis-parses `::`/port; a config-file `ProxyJump` works.
  A working ssh config is at
  `…/scratchpad/mirror_ssh_config` (Host `mirror-alpha` / `mirror-beta`).
- Each guest: `nixos-system-mirror-{alpha,beta}-26.05pre-git`, `is-system-running`
  = running, `/dev/vdb` **7.4 GiB free** (14 MiB used), nix store 524 MiB.
  **No spirit/criome/mirror/router services** run on either guest (expected — the
  host-emitted TestVm image is minimal-but-loginable: hostname + tap networking +
  stateVersion + sshd + admin key).
- Base revs (gen 51): CriomOS `3aa4780971e4`, goldragon `2fe644be`. Guests + guest
  networking + firewall + sshd + right-sizing are the reboot-persistent default
  (promoted via `nix-env --set` + `switch-to-configuration boot`, per the prior
  round). NOTE: lojix's own deployment records for prometheus still show the older
  gens 1/38 (`Query (ByNode (goldragon prometheus))`) because gen 51 was promoted
  by hand, not via a lojix deploy — the live truth is gen 51.

## The decisive finding: the mirror stack is NOT a config-only production surface

Two deep source maps (CriomOS module packaging; spirit/mirror/criome config +
seed surfaces) + direct reads converge on this. The daemon **code** and the
shipper/gate logic exist and are proven in **VM test harnesses**, but there is
**no production wiring to run them as standing node services enabled from cluster
data.** Specifics, each with the source location:

1. **No production Spirit NixOS module.** In all of `CriomOS/{modules,lib,flake.nix}`
   the only reference to "spirit" is the **test** module
   `modules/nixos/criome-auth-integrated-test.nix`. Spirit ships as a **home-layer
   CLI** via `criomos-home` (flake.lock: `criomos-home → spirit`), never as a node
   daemon. There is no `services.spirit`, no socket, no unit. → A new `spirit.nix`
   node module must be authored to run `spirit-daemon` on the guests.

2. **The deployed Spirit cannot ship.** The A→B carry lives behind ONE cargo
   feature, **`mirror-shipper`** (`spirit/Cargo.toml:71` — it pulls `mirror`,
   `signal-mirror`, `criome`, `signal-criome`; it also compiles the 1-of-1 criome
   gate and `engine.gate_and_ship_head`). The production daemon package builds
   **`--features agent-guardian --bin spirit-daemon`** (`spirit/flake.nix:724`) —
   **NOT `mirror-shipper`.** No flake output (package/check/app) compiles
   `mirror-shipper` at all (verified via `nix flake show`; the string is absent
   from `flake.nix`). My local production `spirit-daemon` (v0.21.0) shows no shipper
   symbols. → When unarmed the mirror target/gate are echoed in the Configure
   receipt but `#[cfg]`-compiled out. A **`mirror-shipper` build variant** (new
   flake output) is required, and its Nix build has **never been exercised** — the
   fenix-FOD-bomb risk on this specific build is a live unknown (Scout field-probe 11).

3. **criome has no production node-service path.** `modules/nixos/criome.nix` is a
   plain `services.criome.enable` option and is **not imported by the production
   aggregate** `modules/nixos/criomos.nix` — only by the two test modules. → It must
   be added to the aggregate and enabled, **with `authorization_mode = AutoApprove`**
   (default `Quorum` returns `AuthorizationPending` → the gate never ships;
   `criome/src/actors/root.rs:265-277,968-1006`). Its per-peer identity **seed hook**
   exists (`criome.nix:196-205,231` ExecStartPost `RegisterIdentity`) but is **not
   needed for the direct path** — criome self-registers its own identity and the
   1-of-1 root authorizes A's own head with no peer registration.

4. **`mirror.nix` is the real replicator, but incomplete for this use.** Gated on
   `TailnetClient && PersonaDevelopment` (`mirror.nix:14-15`), runs `mirror-daemon`
   on `0.0.0.0:7474`. **No store-row registration hook exists** — registering the
   `spirit` store row is runtime-only (`meta-mirror '(RegisterStore (spirit
   SemaVersionedLog))'`, `MIRROR_META_SOCKET`); there is no deploy-time/config path.
   → A new `ExecStartPost` `RegisterStore` hook is needed on B. Also **the firewall
   opens 7474 on `tailscale0` only** — but the guests reach each other over the
   `vmt*` tap (`5::7`↔`5::8`), not tailscale, so 7474 must additionally be opened on
   the guest network path.

5. **The mirror→spirit hop on B is NOT autonomous.** Neither daemon bridges it:
   the mirror is a payload-blind landing store; `spirit/src/daemon.rs` has no
   mirror-pull/poll — its only inbound path for mirrored data is the owner-only meta
   `Import`. To make B's **spirit** equal A's spirit, an external tool must
   `meta-mirror Restore(spirit)` → feed the bundle into B via `meta-spirit Import`
   (source-confirmed; witnessed only in `spirit/tests/end_to_end_offline_full_chain.rs`).
   → The "same record in spirit on B" requires either a semi-manual feed loop
   (a systemd timer running Restore+Import = config) or a new bridge daemon (engine
   code). Note: A→B at the **mirror** level (A's spirit ships → B's `mirror.sema`
   persists the head) **is** autonomous once A is armed.

6. **persona-router is NOT needed** for the plain A→B mirror (it's the actor-message
   / router-forward fabric; orthogonal to SEMA replication). The brief's item-1
   mention of persona-router + criome-trust-seed on B belongs to the deferred
   router-attestation variant (bead `primary-1e6b.8`), not this direct slice —
   consistent with the WeavePlan's CODE-CONFIRMED B1 resolution.

7. **No cluster-data atom encodes the mirror role.** The horizon `NodeService` enum
   (`horizon-rs/lib/src/proposal.rs:123`) has only `TailnetClient`, `TailnetController`,
   `NixBuilder`, `NixCache`, `PersonaDevelopment{capabilities:[GitoliteServer]}`,
   `VmHost`, `WebHost` — **no Mirror/Spirit/Criome/PersonaRouter, and no field for a
   ship target.** The test harnesses fake `PersonaRouter`/criome via **synthetic
   Nix-level `horizon.node.services` attrsets** the real projector cannot emit.
   → Differentiating A (shipper, target = `[5::8]:7474`, criome AutoApprove) from B
   (receiver) from cluster data cleanly needs a new horizon service/field
   (**horizon-rs Rust = schema/engine code = the brief's STOP line**), OR a
   hostname-keyed CriomOS module for these two named guests (host-specific facts in
   a module — a mild anti-pattern, but config/deploy).

This sharpens rather than contradicts the Scout/Weaver: their blockers B2/B3 and
the **OPEN** beads `primary-1e6b.3` (criome seed), `.4` (mirror store-row seed),
`.5` (sender-leg feature+config) already flag these as code/module/build tasks;
bead `.8` (router variant) is deferred as "genuinely net-new code." The brief's
"config only" compressed the sender-leg *shipper code already existing* into "the
whole stack is config," which the ground truth does not support.

## Remaining work, classified (config/deploy vs engine code)

| Item | What | Class |
|---|---|---|
| Sender-leg build | Add spirit `mirror-shipper` flake output; build variant | **config/deploy** (build never exercised — fenix risk unknown) |
| spirit.nix | New CriomOS node module: run `spirit-daemon` + ExecStartPost `meta-spirit Configure` | **config/deploy** (net-new module) |
| criome enablement | Add `criome.nix` to aggregate; enable on A with `AutoApprove` | **config/deploy** |
| mirror store-row seed | New ExecStartPost `meta-mirror RegisterStore(spirit)` on B | **config/deploy** |
| 7474 on guest path | Open mirror TCP on the `vmt*`/guest network (currently tailscale0-only) | **config/deploy** |
| mirror→spirit feed on B | Restore+Import loop (systemd timer) — semi-manual | **config/deploy** (timer) *or* **engine** (bridge daemon) |
| A/B asymmetry | Ship-target + role differentiation from cluster data | **engine** (horizon field) *or* hostname-keyed module (config, anti-pattern) |
| State-creation on A | `Record` is fail-closed without a guardian; use meta `Import` seeding or arm a guardian | **psyche decision** (open bead `primary-1e6b.6`) |

A **no-engine-code** path exists if the psyche accepts (a) hostname-keyed A/B
differentiation for these two named guests and (b) a semi-manual (timer) mirror→spirit
feed. A **clean/autonomous** path needs targeted engine code (a horizon service field
+ a mirror→spirit bridge daemon).

## Ready assets (so whichever path is one green-light away)

- **Exact bring-up recipe** (source-verified, per the config-surface map):
  - **B:** run `mirror-daemon` bound `[5::8]:7474` → `MIRROR_META_SOCKET=… meta-mirror
    '(RegisterStore (spirit SemaVersionedLog))'`; run B's `spirit-daemon`.
  - **A:** run `criome-daemon` in `AutoApprove`; run A's `spirit-daemon` **built
    `--features mirror-shipper`**; then
    `meta-spirit '(Configure (Default (Some (Address [5::8]:7474)) (Some (Socket
    /run/criome/criome.sock)) None))'`.
  - **Feed B:** on each new head, `meta-mirror Restore(spirit)` → `meta-spirit
    Import`; verify with `meta-spirit '(ObserveHead)'` on both.
  - Gotchas: mirror target must be an **IP literal** (`[5::8]:7474`), not a hostname
    (`SocketAddr::parse`, `spirit/src/shipper.rs:61`); keep A's spirit on `Gating`
    (default); criome gate socket must equal `CRIOME_SOCKET`.
- **Sender-leg flake output** I would add to `spirit/flake.nix` (mirrors
  `daemonPackage` at :722, with `cargoExtraArgs = "--features mirror-shipper --bin
  spirit-daemon"` + its own `buildDepsOnly` artifacts). Buildable on prometheus via
  `nix build github:LiGoldragon/spirit/<rev>#mirror-shipper-daemon`.
- **Production data-copy is ready and non-disturbing.** Live production Spirit runs
  on ouranos as my user (PID 109842): store `/home/li/.local/state/spirit/spirit.sema`
  (987 KB), sockets `spirit.sock` + `meta-spirit.sock`. Read-only `ObserveHead`
  returned head **`61cef06aa936bedf22e9aa97e1a7d0e003a7d335e02363e229a301a91c958919`**
  (marker `(955 11620868838196946148)`). A copy is a read-only `.sema` file copy (or
  meta `Restore`/`Import`) — no write to production. This sub-step is unblocked once
  A's spirit stands.

## Checks run (all read-only)

- `lojix "(Query (ByNode (goldragon {prometheus,mirror-alpha,mirror-beta})))"` — prometheus gens 1/38 (stale-by-hand-promotion), guests accepted with `[]`.
- SSH health: prometheus (gen 51, running, both microvm units active); both guests (running, no mirror services, 7.4 GiB free).
- Source: horizon-rs `NodeService` enum; CriomOS `mirror.nix`/`criome.nix`/`persona-router.nix`/`node-services.nix`/`criomos.nix`/`flake.nix`/`criome-auth-integrated-test.nix`; spirit `Cargo.toml`/`flake.nix` + `nix flake show`; two deep agent maps.
- `meta-spirit '(ObserveHead)'` on production (read-only) — head captured above.
- goldragon `datom.nota` mirror-alpha (5::7)/mirror-beta (5::8) declarations — both carry only `[(TailnetClient)]`.

## Decision menu (needs psyche)

1. **No-engine-code build-out** — I add the spirit `mirror-shipper` output + author
   the CriomOS modules (spirit.nix, criome enablement, mirror store-row seed, 7474
   guest-path open, a mirror→spirit **timer** feed), differentiate A/B **by hostname**
   for these two guests, then lojix-deploy into the guests over SSH (router stays up).
   Persistent + reboot-durable; the final hop is timer-driven, not a daemon.
2. **Clean/autonomous** — same, but add a horizon `NodeService` field for the mirror
   role/target and a mirror→spirit **bridge daemon** (targeted engine code; explicit
   authorization needed since it crosses the brief's STOP line). Reusable, fully
   autonomous.
3. **Ad-hoc mechanism proof first** — I build the 3 daemons and run them ad-hoc on
   the standing guests to prove a real record on `mirror-alpha` lands on
   `mirror-beta`'s mirror over the real network (criome-authorized), as interim
   on-metal confidence, then pursue 1 or 2 for persistence. Non-destructive; not the
   persistent deliverable form.

First bounded step for any option: **de-risk the sender-leg build** (add the
`mirror-shipper` flake output, build on prometheus) — it answers the one live
unknown (does the shipper build past the fenix FOD) and gates everything. It edits
the spirit repo + runs a prometheus build, so I held it for the psyche's go given
prometheus is also the psyche's Wi-Fi router and this front is gated build-by-build.

## Blockers / open items

- **B-A (premise):** persistent config-only stand-up is not achievable on landed
  main (items 1-5 above). Needs the build-out in the decision menu.
- **B-B (engine line):** clean A/B modeling + a fully-autonomous mirror→spirit feed
  need targeted engine code; hostname-keying + a timer avoid it (Option 1).
- **B-C (open bead `primary-1e6b.6`, psyche):** state-creation on A — guardian-armed
  organic `Record` vs owner-only meta `Import` seeding. Unblocks the verify definition.
- No files changed this round; nothing to commit.

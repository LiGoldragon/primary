# 34/4 — Wave D: cutover-to-main-deployment requirements

*Kind: Audit slice · Topic: per-node cutover delta + rollback story · 2026-05-23*

## TL;DR

"Main deployment" means the binary `lojix-cli` consumed at `CriomOS-home/flake.nix:124` and installed via `modules/home/profiles/min/default.nix:181` (one home-package line, system-wide via the min profile that every user gets) is replaced by the lean stack: the new `lojix` daemon (long-lived, per-node systemd unit, owns a Unix socket and an authoritative GC-root tree at `/nix/var/nix/gcroots/criomos/...`) plus the thin `lojix` CLI client. The blast radius is **5 production nodes** (balboa, ouranos, prometheus, tiger, zeus per `goldragon/datom.nota`), **2 repos with concrete pin moves** (`CriomOS-home` flake input + the `lojix-cli` `home.packages` line, and `CriomOS` modules/nixos for the new daemon's systemd unit which **does not exist anywhere yet**), and **3 MVP-blocking structural gaps that must land before any cutover**: (1) `lojix` flake exposes only `packages.default` — no separate `lojix` CLI vs `lojix-daemon` outputs, so `CriomOS-home` has nothing to consume as a CLI replacement; (2) **no NixOS module for `lojix-daemon`** exists in `CriomOS/modules/nixos/` — the daemon has no systemd unit, no socket-mode policy, no state-dir; (3) `criomos-horizon-config` is **not bridged into any flake** — neither `CriomOS` nor `lojix` nor `horizon-rs` references it, so the daemon cannot load `HorizonProposal` per `lojix/ARCHITECTURE.md`. `CriomOS-lib/lib/predicates.nix` (the destination home for view-side derived predicates per /29) also **does not exist**. Each gap is a cutover-prerequisite bead, not a "during cutover" task.

## Per-node consequence flowchart

```mermaid
flowchart TB
    subgraph current["Pre-cutover state (today)"]
      lcli["lojix-cli flake input<br/>(CriomOS-home/flake.nix:124)"]
      lpkg["lojix-cli binary<br/>(profiles/min/default.nix:181)"]
      lcli --> lpkg
      lpkg --> "operator's machine<br/>(goldragon)"
      lpkg --> "every cluster node<br/>(via home rebuild)"
    end
    subgraph cutover["Cutover delta"]
      newinput["replace lojix-cli input<br/>with lojix input<br/>(daemon + CLI repo)"]
      newhomepkg["replace home.packages line<br/>with lojix CLI client only"]
      newmod["CriomOS new module<br/>nixos/lojix.nix<br/>(systemd unit, socket policy,<br/>state-dir, GC-root tree)"]
      newbridge["criomos-horizon-config<br/>bridged into lojix daemon<br/>configuration path"]
      newinput --> newhomepkg
      newmod --> "systemd-managed daemon<br/>per cluster node"
    end
    subgraph posthuman["Post-cutover state (per-node)"]
      lojixclient["lojix CLI client<br/>(home.packages, every user)"]
      lojixdaemon["lojix-daemon<br/>(systemd unit, root)"]
      lojixsocket["/run/lojix/daemon.sock"]
      gcroots["/nix/var/nix/gcroots/criomos/..."]
      sema["/var/lib/lojix/sema.redb"]
      lojixclient -.unix socket.-> lojixsocket
      lojixsocket --> lojixdaemon
      lojixdaemon --> gcroots
      lojixdaemon --> sema
    end
    current --> cutover --> posthuman
```

## Per-node consequence table

The five production nodes per `goldragon/datom.nota` (balboa, ouranos,
prometheus, tiger, zeus). All five rebuild during cutover; the role
delta is whether the node also runs the daemon vs only the CLI client.

| Node | Kind role | What changes | Restart required | State migration |
|---|---|---|---|---|
| `balboa` | Center / Zero | Home rebuild replaces `lojix-cli` with `lojix` CLI client. If daemon runs everywhere, also a system rebuild for the new `lojix-daemon` systemd unit. Sema redb initialised empty (no historical generations to import). | Home: user-session restart (cosmetic); system: nixos-rebuild switch with daemon-start. | None — daemon starts empty. Existing live system stays activated as the previous generation; lojix knows nothing about it until first deploy. |
| `ouranos` | Edge / Testing | Same as balboa. Plus: this is the node Li uses for development, so it's the first one to feel a CLI-shape regression. | Same as balboa. | Same as balboa. |
| `prometheus` | Center / Large | Same as balboa. Per `INTENT.md` carries `nspawn-sandbox-testing` capability for the CriomOS-test-cluster smoke path; cutover must not break that path. | Same as balboa. | Same as balboa. |
| `tiger` | (per datom) | Same as balboa. | Same as balboa. | Same as balboa. |
| `zeus` | (per datom) | Same as balboa. Per `/33` "smoke-built end-to-end through prometheus" means this node is the first the lean stack ever activated against in a test; cutover-day risk lower here only if the smoke build is still passing on cutover day. | Same as balboa. | Same as balboa. |
| `goldragon` (psyche's workstation) | non-cluster | The CLI binary that issues deploy requests changes from `lojix-cli` (monolithic — builds, signs, ssh's, activates) to `lojix` (thin client — submits NOTA request to the target node's daemon over ssh-tunnelled socket). Existing `lojix-cli` invocation muscle memory breaks. | None (per-user shell session picks up new binary on next `nix profile build`). | None — operator state lives in scripts the psyche maintains by hand. |

**Pre-cutover-state-of-`lojix-daemon`-on-every-node assumption.** The
table assumes the daemon runs on every cluster node, since that's the
daemon-mesh model per `intent/deploy.nota` 2026-05-17T11:00 ("the
node will deploy itself"). Whether `goldragon` (the operator
workstation) also runs a daemon, or only ships the CLI, is **open
to psyche** — see §"Open questions" below.

## Cutover delta — file paths

The concrete file-by-file delta for the cutover. Pre-cutover paths
are read from the canonical-checkout `main` branches under `/git/...`;
post-cutover state is what the cutover commit must produce.

| File | Current pin / reference | Post-cutover state |
|---|---|---|
| `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:124-125` | `lojix-cli.url = "github:LiGoldragon/lojix-cli";` + `inputs.nixpkgs.follows` | `lojix.url = "github:LiGoldragon/lojix";` + `inputs.nixpkgs.follows`. (No version pin — the lojix repo has no tagged release; the cutover commit pins the lock to a known-good rev.) |
| `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:181` | `inputs.lojix-cli.packages.${pkgs.stdenv.hostPlatform.system}.default` | `inputs.lojix.packages.${pkgs.stdenv.hostPlatform.system}.lojix-cli` (or `.lojix` — depends on lojix flake output naming, currently exposes only `.default` which is the whole crate; **prerequisite bead**: split flake outputs so the home profile can pick the thin client only, not the daemon binary). |
| `/git/github.com/LiGoldragon/CriomOS/modules/nixos/criomos.nix` (the imports list) | No `lojix.nix` import | New `./lojix.nix` import; the file itself is **net-new** (does not exist on `main` or on `horizon-leaner-shape`). |
| `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix` | Does not exist | New file: systemd unit (`lojix-daemon.service`), socket activation or plain Unix socket bind, state-dir under `/var/lib/lojix/`, RuntimeDirectory `/run/lojix/`, ProtectSystem strict, capabilities for nix-daemon control (per `intent/deploy.nota` 2026-05-17T13:30 — daemon owns nix config). Group policy for socket access (which users speak signal-lojix). |
| `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nix/client.nix:88` | `!include nixTokens` (existing line) | Possibly retire if `nix-auth` (per `/32`) ships and the daemon owns token-include rotation via the `NixDaemonConfigurationActor` pattern. Carry as deferrable post-cutover cleanup, not a cutover-day blocker. |
| `/git/github.com/LiGoldragon/CriomOS/flake.nix:5` (lojix-cli input) | (None — CriomOS itself does not pin lojix-cli; only CriomOS-home does) | (No change to CriomOS flake.nix.) Note: CriomOS sources its `horizon` input as a stub at `./stubs/no-horizon`, which lojix-cli overrides via `--override-input` per `lojix-cli/src/build.rs:309`. The new `lojix-daemon` does the same — no change to the stub or the override interface; only the CALLER (lojix-daemon, not lojix-cli) changes. |
| `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix` | No `predicates` namespace; lib carries `constants`, `mkJsonMerge`, `importJSON` only | New sibling file `CriomOS-lib/lib/predicates.nix` carrying view-side derived predicates per /29's role-merge destination. Joins via `lib/default.nix`'s namespace. (Per /29 — the destination home for `behavesAs.center` etc. that horizon-rs's view::Node currently emits.) |
| `/git/github.com/LiGoldragon/criomos-horizon-config/` | Standalone repo with `horizon.nota`; not bridged into any flake | Bridged into the `lojix` flake (or the lojix-daemon configuration) so the daemon can load `HorizonProposal` at runtime. **Wiring location is open** — could be a flake input on the `lojix` repo, could be a daemon-configuration file path, could be both. |
| `/git/github.com/LiGoldragon/lojix/flake.nix:55-58` | `packages.default = package;` (single derivation containing both `lojix-daemon` + `lojix` binaries) | `packages.lojix-cli = ...; packages.lojix-daemon = ...; packages.default = package;` — separate package outputs so CriomOS-home can pick the CLI without the daemon binary, and CriomOS can pick the daemon without the CLI binary. |
| `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:143` | `currentDefault = "v0.1.0";` | Per /33 — flip to `v0.1.1` for the wire-shape gap fix (Certainty→Magnitude). Independent of lojix cutover but typically rides the same CriomOS-home flake.lock bump. |

## Rollback story

The cutover changes the lockfile pins and the home-package binary on
every node. Three rollback shapes exist, with different reach.

### Option R1 — flake.lock revert (cheapest)

Revert the cutover commit's flake.lock changes on `CriomOS-home` and
`CriomOS`. Existing nodes that already activated the new daemon
profile keep the systemd unit running until the next rebuild; the home
profile reverts to `lojix-cli` on the next `nix profile build` or home
rebuild. Daemon GC-roots in `/nix/var/nix/gcroots/criomos/...` are
orphaned but not harmful (nix-daemon doesn't read them; collection is
a no-op for unused symlinks). Sema redb at `/var/lib/lojix/sema.redb`
is orphaned but not harmful.

**Reach:** any node that picks up the reverted lock on its next home/system
rebuild. Speed: as fast as `nix flake update` + push + per-node `home
switch` (minutes per node, parallelisable).

**Limits:** if the daemon already modified `/etc/nix/nix.conf` (per
`intent/deploy.nota` 2026-05-17T13:30 — "lojix-daemon takes control
of nix configuration"), R1 alone does not undo that change. Nix config
needs separate manual rollback or a daemon-stop-and-cleanup script.

### Option R2 — re-deploy from `lojix-cli` post-cutover (heavy)

The legacy `lojix-cli` is still on a `main` branch in the canonical
checkout and still builds. Treat cutover as reversible by manually
invoking `lojix-cli` from `goldragon` against each affected node
(legacy stack does not need a daemon present on the target — it ssh's
in). This re-deploys the pre-cutover generation on each node, and
because nixos generations are immutable, the previous toplevel
becomes the current activation.

**Reach:** every cluster node, one-by-one. Speed: 5-15 minutes per
node depending on whether re-build or cached. Sequential, not
parallelisable (psyche policy: serial deploys avoid cross-node
race on shared cache).

**Limits:** assumes `lojix-cli` still works at cutover-time. If
substrate moves (signal-frame migration, sema-engine bumps) have
broken `lojix-cli` paths that the production stack doesn't exercise
day-to-day, R2 can fail silently. **Cutover-prep should include a
`lojix-cli`-builds-and-deploys-zeus smoke check** to ensure R2 is
viable.

### Option R3 — nixos generation rollback (per-node, fastest)

Each node retains the previous toplevel as a numbered generation
in `/nix/var/nix/profiles/system`. `nixos-rebuild switch
--rollback` (or the bootloader entry for the previous generation)
reverts the activated system regardless of what `CriomOS-home` ships.

**Reach:** per-node, manual ssh into each node (or use a fleet
script). Speed: seconds per node — just a switch invocation.

**Limits:** rolls back the SYSTEM only. The home profile (where
`lojix-cli` → `lojix` lives) is per-user and home-manager-managed,
not generation-bound the same way. Combining R3 (system rollback)
with R1 (lock revert + home switch) is the safest pair.

### Rollback policy decision — open

Whether the cutover defaults to R1 (cheapest) with R3 as the
emergency lever, vs sets up R2 (re-deploy from `lojix-cli`) as the
sanctioned path, vs invests in atomic-cutover tooling so rollback is
single-command — is a psyche call. Recommendation: **R1 + R3 as the
sanctioned pair**, R2 as the emergency lever, with a cutover-prep
bead that smoke-tests R2 viability on a sandbox before cutover-day.

## Cutover beads (bead-shape)

Each bead is concrete enough for operator to file as a `bd` task
without re-reading this report. Dependencies listed as B-D-N reference
beads in this list; cross-slice deps prefixed by wave.

### B-D-1 — split lojix flake outputs

File: `/git/github.com/LiGoldragon/lojix/flake.nix:55-58`
(packages block).

What to do. Today's `packages.default = package` contains both
binaries (per `lojix` Cargo.toml: `[[bin]] name = "lojix-daemon"` +
`[[bin]] name = "lojix"`). Split into separate package outputs so
consumers can install the daemon and the CLI independently. Likely
shape: `packages.lojix-cli = craneLib.buildPackage { ...; cargoExtraArgs
= "--bin lojix"; }`, `packages.lojix-daemon = craneLib.buildPackage
{ ...; cargoExtraArgs = "--bin lojix-daemon"; }`, `packages.default =
package` (full crate kept for devshell consumers).

Deps. None — purely upstream.

Priority. **MVP-blocking**. CriomOS-home and CriomOS both consume
the binaries; without separation, they can't install one without the
other.

### B-D-2 — write CriomOS NixOS module for lojix-daemon

File (new): `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix`.

What to do. Net-new NixOS module:
- systemd unit `lojix-daemon.service` (Type=notify or Type=simple),
  `ExecStart = "${pkgs.lojix-daemon}/bin/lojix-daemon
  /etc/lojix/configuration.nota"`,
- StateDirectory `lojix`, RuntimeDirectory `lojix` (socket dir
  `/run/lojix/`),
- ProtectSystem (probably `strict`), ProtectHome,
- Socket group ownership policy — who can speak signal-lojix?
  Probably `@nixdev` users or a dedicated `lojix-users` group
  (open question, see below),
- AmbientCapabilities for the nix-config write path (per
  `intent/deploy.nota` 2026-05-17T13:30 — daemon controls
  `/etc/nix/nix.conf`),
- A `nix.extraOptions` line writing the daemon's include slot
  (per the NixDaemonConfigurationActor pattern referenced in
  `intent/deploy.nota`).

Add the import to `criomos.nix` imports list.

Deps. B-D-1 (needs `pkgs.lojix-daemon` exposed as a separable
package).

Priority. **MVP-blocking**. Without this, the daemon has no
systemd entry point on any cluster node.

### B-D-3 — bridge criomos-horizon-config into the daemon configuration path

File (open). Either `/git/github.com/LiGoldragon/lojix/flake.nix`
(add `criomos-horizon-config.url = "github:LiGoldragon/criomos-horizon-config"`
as a flake input, expose at runtime via the lojix-daemon
configuration), OR a daemon-side configuration field that points to a
filesystem path the CriomOS module writes (e.g.
`/etc/lojix/horizon.nota` populated from
`inputs.criomos-horizon-config` via a `pkgs.writeText`).

What to do. Per `lojix/ARCHITECTURE.md` §0.1, the daemon loads
`HorizonProposal` from `horizon.nota`. The repo `criomos-horizon-config`
exists with the schema-correct file. But no consumer flake references
it. Decide the wiring (flake input vs declared path) and land it.

Deps. None directly; sequenced after B-D-1/B-D-2 because those land
the consumer.

Priority. **MVP-blocking**. Without this, the daemon has no
pan-horizon config to load and `ClusterProposal::project` cannot
execute.

### B-D-4 — land CriomOS-lib/lib/predicates.nix

File (new): `/git/github.com/LiGoldragon/CriomOS-lib/lib/predicates.nix`.

What to do. Per `/29` §"The final shape" and the role-merge
destination, the 16 view-side derived predicates (`behavesAs.center`,
`isRemoteNixBuilder`, `isDispatcher`, etc.) currently emitted by
horizon-rs's `view::Node` move Nix-side to a `predicates.nix`
file consumed by CriomOS modules. Land the file in `CriomOS-lib/lib/`,
namespace through `lib/default.nix`. The predicates are pure
functions over a `view::Node` shape.

Deps. Cross-cuts /29's role-merge work — coordinate with whichever
session is doing the role-merge cutover on horizon-rs.

Priority. **MVP-blocking for the lean stack to compile against
CriomOS modules**. Without predicates.nix, `modules/nixos/nix/builder.nix:8-12`
(which uses `behavesAs`, `isRemoteNixBuilder`, `isDispatcher`)
breaks against the lean horizon-rs view that has these stripped.

### B-D-5 — flip lojix-cli input to lojix (the cutover commit)

Files:
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:124-125`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:181`

What to do. The cutover commit itself: replace `lojix-cli` flake
input with `lojix`; update the home-package line to consume `lojix.packages.${system}.lojix-cli`
(per B-D-1's output naming). Run `nix flake update lojix` on
the new input. Commit the lock change.

Deps. B-D-1 (output-split), B-D-2 (daemon module landed in CriomOS),
B-D-3 (config bridge), B-D-4 (predicates.nix landed and consumed).

Priority. **The cutover commit itself**. This is the one whose
landing the psyche calls "cutover-day".

### B-D-6 — cutover-prep R2-viability smoke test

File (likely): a CriomOS-test-cluster check or a one-off
`scripts/smoke-lojix-cli-still-works.sh`.

What to do. Build + deploy `zeus` (or another sandbox node) from
the current `lojix-cli` on `main`. Confirm the legacy path is
operational. This validates R2 (re-deploy from `lojix-cli`) as a
rollback option. Run within the week of cutover-day.

Deps. None.

Priority. **Should-do before cutover-day** (de-risks rollback);
not a strict MVP-blocker, but psyche-policy-relevant.

### B-D-7 — daemon-side nix-config rollback hooks

File: inside `/git/github.com/LiGoldragon/lojix/src/.../nix_config.rs` (likely
location for the NixDaemonConfigurationActor).

What to do. If the daemon mutates `/etc/nix/nix.conf` per `intent/deploy.nota`
2026-05-17T13:30, the daemon needs a "drop all daemon-managed nix-config
state and restart nix-daemon to clean baseline" entry point. Wire this
to a `signal-lojix` `ResetNixConfig` or `owner-signal-lojix` operation
so cutover rollback can invoke it.

Deps. owner-signal-lojix vocabulary (per /33 decision 4); the
NixDaemonConfigurationActor implementation in lojix-daemon.

Priority. **Post-cutover** but pre-first-real-deploy (the daemon
shouldn't write nix-config in production before R1 rollback can
clean it up).

### B-D-8 — sweep skills/system-specialist.md for `lojix-cli` references

File: `/home/li/primary/skills/system-specialist.md`.

What to do. Per /33 §"What's open — guidance refresh", the skill
file names `lojix-cli` as sole deploy entry. Update to reflect:
production runs `lojix-cli` UNTIL cutover; after cutover, production
runs `lojix` (daemon + thin CLI). The skill should name both shapes
with a "post-cutover" pointer.

Deps. None (documentation sweep).

Priority. **Cutover-day or shortly after**. Not a blocker but
should not lag the structural cutover by more than a session.

## Open questions for psyche

1. **Cutover atomicity: all 5 nodes in one window, or staggered?**
   The 5 cluster nodes can rebuild in parallel (lockstep cutover —
   shortest blast-radius window) or staggered (rolling cutover — one
   node at a time, validate, then next). The lockstep approach risks
   simultaneous breakage; the staggered approach extends the
   two-deploy-stacks-coexist window. **Possible answer:** stagger
   per role (Center nodes first, then Edge), with `zeus` as the
   canary; canonical pattern for nspawn/sandbox-tested deploys.
   Psyche owns timing per AGENTS.md don't-propose-date rule, but the
   shape (atomic vs rolling) is policy-relevant.

2. **Does `goldragon` (operator workstation) run a `lojix-daemon` too?**
   The daemon-mesh model says "the node deploys itself" but goldragon
   is not a cluster node — it's the operator workstation that issues
   deploy requests. If goldragon runs no daemon, the operator's
   `lojix` CLI must dispatch to the target node's daemon over an
   ssh-tunnelled socket; if goldragon runs a daemon, the local daemon
   acts as the dispatcher (per `intent/deploy.nota` 2026-05-17T15:30:
   "the operator's machine does not need to run a lojix-daemon —
   only the CLI"). Recommendation: thin-CLI-only on goldragon
   per intent record; surface for confirmation.

3. **Rollback policy — R1+R3 vs R2 vs invest in atomic-cutover tooling?**
   Three rollback shapes described above. The cheapest path
   (R1+R3) is sufficient for the foreseeable blast radius (5 nodes,
   serial-safe rollback at minutes per node). R2 is the emergency
   lever. Atomic-cutover tooling (single-command revert all 5 nodes)
   would cost engineering time the cutover itself competes with.
   Psyche call.

4. **Socket access policy — which users can speak signal-lojix on each node?**
   The daemon binds a Unix socket. The mode/group determines who can
   deploy. Options: (a) root only; (b) `@nixdev` (existing group per
   `modules/nixos/nix/client.nix:53`); (c) a dedicated `lojix-users`
   group; (d) socket activation gated by polkit/criome. Per
   `intent/deploy.nota` 2026-05-17T15:30, criome-mediated
   authorization is the destination but deferred per 2026-05-20T17:10.
   For the cutover MVP a simple group-based policy works. Recommendation:
   `@nixdev` for cutover-day, criome later. Surface for confirmation.

5. **Should the cutover include the persona-spirit v0.1.0 → v0.1.1 flip?**
   Per /33 decision 5 and `spirit.nix:143`, the spirit-deployed flip
   is a one-line independent change typically ridden on the next
   CriomOS-home flake.lock bump. The cutover commit IS a CriomOS-home
   flake.lock bump. Co-shipping them halves the rebuild count for the
   cluster but couples two unrelated regressions in one cutover-day
   window. Recommendation: **decouple** — flip spirit in a separate
   commit landing AFTER cutover stabilises. Surface for confirmation.

## What's not covered here

- The daemon's `signal-lojix` wire shape (Wave A + Wave C cover the
  code state and end-to-end deploy path).
- The CriomOS-test-cluster sandbox-pass criteria for the lean stack
  (Wave B).
- Migration sequencing across the substrate-up cascade (in /33's
  pickup queue, and /34's overview synthesis will rank against
  this report's beads).

## See also

- `34-mvp-and-sandbox-audit/0-frame-and-method.md` — session frame +
  Wave D brief.
- `/home/li/primary/INTENT.md` §"Two deploy stacks coexist" — the
  cutover the psyche has directed.
- `/home/li/primary/intent/deploy.nota` (2026-05-17T11:00 →
  2026-05-21T09:07) — full psyche intent chain on the daemon-mesh
  shape, deploy variables, nix-config control, criome auth, owner
  signal, deferral notes.
- `reports/system-designer/29-lean-horizon-cluster-data-shape.md` —
  predicates.nix destination shape; role-merge final form.
- `reports/system-designer/30-horizon-lojix-low-level-migration/` —
  substrate audit; per-repo current state.
- `reports/system-designer/33-handover-finishing-lean-lojix-horizon-stack.md`
  — open queue; substrate-up cascade priority.
- `lojix/ARCHITECTURE.md` §0.1 — daemon-owned projection pipeline;
  what `HorizonProposal` is loaded from.
- `protocols/active-repositories.md` §"Two deploy stacks coexist" —
  branch shape per repo.

# 39 — what production lojix / CriomOS actually does (the Stack-A baseline)

cloud-designer, 2026-06-10. Source-grounded description of the production deploy
stack — the "Stack A" baseline the new lojix daemon (report 38) must match.
Method: a 3-reader parallel sweep (workflow `production-deploy-stack-baseline`)
over `lojix-cli`, `CriomOS`/`CriomOS-home`, `goldragon/datom.nota`, and
`horizon-rs`, every claim grounded in `file:line`. Spirit gate: question →
no capture.

## The shape: two halves and one in-process library

- **`lojix-cli`** — the deploy *orchestrator*. A flagless, NOTA-only one-shot
  CLI that runs a fixed sequential pipeline (despite the README, it is **not**
  an actor framework — `deploy.rs:86` says so explicitly). It keeps **no state**:
  no live-set, no GC-roots index, no event log; each invocation is independent.
- **`CriomOS` / `CriomOS-home`** — the *blueprints* being deployed. A NixOS
  platform flake and a standalone home-manager flake. CriomOS exposes a **single
  generic `nixosConfigurations.target`** (not one config per node).
- **`horizon-rs`** — the *projector*, linked **in-process** as a Rust library
  (`horizon-lib`), not a daemon/CLI boundary. Turns the cluster proposal into a
  per-node `Horizon`.

The whole system's trick: that one generic `target` evaluates into a different
generation per node **purely because four flake inputs differ** — `horizon`,
`system`, `deployment`, `secrets`. Node class is **never** inferred from node
name; every module branches on `horizon.node.behavesAs.*` / `services`.

## The `lojix-cli` front door

One argument **is** the whole request — no flags, ever (`main.rs:8-15`,
`request.rs:185-219`):

- argv starting with `(` → all argv joined and parsed as **inline NOTA**;
- otherwise argv[0] is a **`.nota` file path** (a second arg is rejected);
- **zero args** → first existing default config
  (`$LOJIX_CONFIG` → `$XDG_CONFIG_HOME/lojix/config.nota` →
  `$HOME/.config/lojix/config.nota`). "Redeploy locally by default" is just
  whatever record sits in that file.

Request grammar (positional NOTA, tag-dispatched, `request.rs:16-89`):

```
(FullOs  cluster node source criomos action       builder? substituters?)
(OsOnly   cluster node source criomos action       builder? substituters?)
(HomeOnly cluster node user   source home   mode    builder? substituters?)
(CheckHostKeyMaterial …)   # read-only diagnostic, not a deploy
```

- **`SystemAction` = `Eval | Build | Boot | Switch | Test | BootOnce`**
- **`HomeMode` = `Build | Profile | Activate`**
  (`build.rs:9-49`)

These two enums are the **parity bar** — they gate exactly which tail stages of
the pipeline run.

## The deploy pipeline (fixed, sequential, no timeouts)

`deploy()` (`deploy.rs:82-208`) runs:

1. **Load proposal** — read the source `.nota` and parse it as a
   `horizon_lib::ClusterProposal` (`deploy.rs:90`).
2. **Project horizon** — `HorizonProjection::new(proposal, Viewpoint{cluster,
   node}).project()`. The deploy target is *always* `horizon.node`; addressing
   derives from its `criome_domain_name` — there is **no `--target` flag**
   (`deploy.rs:92-108`, `host.rs:20-40`).
3. **Validate** — home user must exist in `horizon.users`; builder resolves to
   none (build on dispatcher) / the target itself / a sibling with
   `is_remote_nix_builder=true`; each substituter name resolves to a node with
   `nix_url` + `nix_pub_key_line` (`deploy.rs:31-64,210-246`).
4. **Materialize override inputs** — write small content-addressed flakes under
   `~/.cache/lojix/` (next section).
5. **Eval or build** — `Eval` →
   `nix eval --refresh --raw <attr>.drvPath`; everything else →
   `nix build --refresh --no-link --print-out-paths <attr>`. Attr is
   `<flake>#nixosConfigurations.target.config.system.build.toplevel` (system) or
   `<flake>#homeConfigurations.<user>.activationPackage` (home). With a builder,
   the whole command is shell-quoted and wrapped in `ssh`. `--no-link` means **no
   `./result` GC root** on the dispatcher; awaits have **no timeout** (cold
   builds run for hours) (`build.rs:171-194,284-380`).
6. **Finish (copy + activate, gated by action/mode)** — `Eval` returns the drv
   path and stops. `Build`/Home-`Build` stop after the build. Activating System
   actions (Boot/Switch/Test/BootOnce) and Home Profile/Activate run
   **copy → activate** (`deploy.rs:150-208`).

## The four override inputs (stage 4 detail)

Each is a tiny generated flake under `~/.cache/lojix/<axis>/…`, NAR-hashed via
`nix hash path --type sha256 --sri`, injected as
`--override-input <name> path:<dir>?narHash=<sri>`. Content-addressing is the
cache-warmth mechanism — identical content re-hashes identically and reuses the
nix eval cache (`artifact.rs:209-231`, `build.rs:289-329`).

| Input | Contents | When | Evidence |
|---|---|---|---|
| `horizon` | `horizon.json` (the projected Horizon) + a 4-line flake that `fromJSON`-reads it | always | `artifact.rs:54-70` |
| `system` | flake emitting the literal nix system string (`x86_64-linux`, …) | always | `artifact.rs:81-105` |
| `deployment` | flake emitting `deployment.includeHome = true/false` | **System plans only** (FullOs=true, OsOnly=false; Home omits it) | `artifact.rs:116-140`, `build.rs:85-101` |
| `secrets` | copies of 3 fixed `.sops` files (`router-wifi-sae-passwords`, `router-backup-wifi-password`, `local-llm-api-token`) + a `sopsFiles` flake | **only if** `<proposal-dir>/secrets/router-wifi-sae-passwords.sops` exists | `artifact.rs:142-207` |

The `secrets` input is **existence-gated and filename-hardcoded** — not part of
the request grammar, undocumented in the README input table. A node whose
proposal lacks that dir silently deploys with no secrets override (and CriomOS
only throws if a module actually references a missing secret).

**Remote-builder staging:** with a sibling builder, the cache dirs are
`rsync -a --delete`'d to `/var/tmp/lojix/generated-inputs/<content-keyed>/` and
the override refs rewritten to those remote paths (`stage.rs:97-167`).

## Activation mechanics (the part the new daemon cannot yet do)

All remote calls are `ssh -o BatchMode=yes <user>@<criome_domain_name> …`; the
host is always `<node>.<cluster>.criome`, never a bare node name
(`host.rs:49-64`).

**Closure copy** (`copy.rs:26-68`): `nix copy --substitute-on-destination
--to ssh-ng://root@<domain>` (so the target pulls *signed* paths from the
cluster cache — raw daemon-to-daemon paths are unsigned and rejected under
`require-sigs`). Builder≠target streams *through the dispatcher*
(`--from … --to …`) — a known scaling limitation; builder==target skips copy.

**System Boot / Switch** (`activate.rs:39-69`): one ssh runs
`nix-env -p /nix/var/nix/profiles/system --set <store> &&
<store>/bin/switch-to-configuration <boot|switch>`, then **reconciles EFI**:
`readlink` the system profile → `bootctl set-default nixos-generation-N.conf`
+ `bootctl set-oneshot ''`. (switch-to-configuration writes `loader.conf` but
*not* the EFI `LoaderEntryDefault` var, so a stale one-shot from a prior
BootOnce could otherwise hijack the next boot.)

**System Test**: only `switch-to-configuration test` — no profile set, no
bootloader touch.

**System BootOnce** (`activate.rs:75-147`): dispatches a **transient
`systemd-run --unit=… --collect --wait --service-type=oneshot`** unit owned by
PID 1, so an ssh drop doesn't kill it. The script reads `OLD` from `bootctl
status` *Current Entry* (the running generation), sets the new generation,
derives `NEW`, then `bootctl set-default $OLD` + `bootctl set-oneshot $NEW`.
**Reboot 1 lands NEW; reboot 2+ auto-returns to OLD** — the headless-safe
rollback design. (It seeds `PATH` explicitly because NixOS transient units get
a minimal PATH.)

**Home Profile / Activate** (`activate.rs:258-353`):
`nix-env -p $HOME/.local/state/nix/profiles/home-manager --set <store>`, then
for Activate run `<store>/activate`. A **local fast-path** skips ssh when the
dispatcher already *is* the requested user on the target (USER + `hostname -s`
match) — this is exactly the path that ran when I activated your home generation
during the claude/codex/pi update.

**There is no explicit GC-root or rollback subsystem.** GC rooting is *implicit*
— setting the system/home-manager profile makes the closure a profile
generation (= a GC root). "Rollback" is the BootOnce one-shot design plus the
EFI reconcile, not a `nix-env --rollback` call.

## The CriomOS side (what's being deployed)

- **One generic system output**, `nixosConfigurations.target` — built with
  `specialArgs = {horizon, system, deployment, …}` and
  `includeHome = deployment.includeHome or true` (`flake.nix:72-150`).
- **Four stub inputs are the per-deploy seam** (`flake.nix:46-69`), with an
  **asymmetric stub contract**: `no-horizon` and `no-system` **`throw`** (hard
  fail if not overridden — mandatory); `no-secrets` returns `{ sopsFiles = {}; }`;
  `default-deployment` returns a working `{ includeHome=true;
  includeAllFirmware=true; }`. So a build with no `secrets` override still
  *evaluates* — modules only throw if their specific secret is referenced.
- **`nixosModules.criomos`** imports every node-class module; each wraps its
  config in `mkIf horizon.node.behavesAs.<class>` — router (`hostapd` WPA3-SAE +
  `kea` DHCP + `nftables`), metal (per-model firmware/kernel/thermal driven by
  `horizon.node.machine` + `deployment.includeAllFirmware`), llm (`llama.cpp`
  multi-model router on `largeAi`), nix builder/cache (from viewpoint fields).
  The router reads `inputs.secrets.sopsFiles.<name>` and **throws at eval** if
  the referenced WPA3 secret is missing (`router/default.nix:23-36`) — the exact
  gate the new daemon trips by not materializing `secrets`.
- **`CriomOS-home`** is a standalone home-manager flake carrying the same
  `horizon`/`system`/`pkgs` stubs; `homeConfigurations = mapAttrs
  mkHomeConfiguration horizon.users`, and lojix builds
  `homeConfigurations.<user>.activationPackage` directly for home deploys
  (`CriomOS-home/flake.nix:282-353`).

## The cluster proposal + projection

`goldragon/datom.nota` is a **positional NOTA `ClusterProposal`** —
`({nodes} {users} {domains} (trust))` — describing the 5-node `goldragon`
cluster (balboa, ouranos, prometheus, tiger, zeus) with per-node hardware,
service roles (`TailnetController`/`NixBuilder`/`NixCache`/…), addressing, and a
trust block (`proposal.rs:24-94`). `horizon-rs`'s
`ClusterProposal::project(viewpoint)` drops `trust=Zero` nodes, enforces a single
`TailnetController`, computes every derived field (criome domain, system,
behavesAs flags, builder/cache/dispatcher roles, pubkey lines), floors user size
to the viewpoint node, and `fill_viewpoint`s the target node — yielding the
`Horizon { cluster, node, ex_nodes, users }` that lojix serializes into the
`horizon` input (`horizon.rs:31-145`, `node.rs:334-547`).

## Why this is the baseline that settles report 38

Production lojix-cli does the **whole** pipeline including copy + activate, for
**all six System actions and all three Home modes**, materializing **all four**
override inputs. The new lojix daemon (report 38) reimplements the *front* —
horizon projection + input materialization + eval/build — but:

- **rejects every activating action** and its copy/activate bodies are broken
  (unset `$CLOSURE`, no `switch-to-configuration`, bare node name as ssh host) —
  vs the full `activate.rs` machinery above;
- **never materializes `secrets`** — so WPA3 router nodes throw at *eval*;
- **emits `includeAllFirmware`** in the deployment input where lojix-cli emits
  only `includeHome` — so OsOnly builds a *different metal closure*;
- keeps state **in-memory** — though note lojix-cli is itself **stateless**, so
  the live-set/GC-roots/event-log machinery is the daemon's *net-new charter*,
  not a parity gap (the distinction the psyche reserved).

The hard, subtle production behavior the new stack must eventually reproduce:
the **BootOnce rollback design** (Current-Entry source-of-truth, PID-1 transient
unit), the **EFI reconcile** on Boot/Switch, the **Yggdrasil-preferred
substituter URLs**, the **signed-path copy** discipline, the **existence-gated,
filename-hardcoded secrets** flow, and the **content-addressed `path:?narHash`**
input materialization that keeps eval caches warm.

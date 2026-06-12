# 10 · Test cluster and VM — end-to-end deployment-test availability

Cloud-designer recon sub-agent, session 41. Every claim cites a file read or a
command run from this host (ouranos). Read-only.

## Bottom line

There IS a working, independent test-cluster fixture
(`github:LiGoldragon/CriomOS-test-cluster`) and a reachable peer host
(**Prometheus**, `ssh prometheus.goldragon.criome` works from here and
`criomos-nspawn` is deployed on it). The live, proven end-to-end build+boot
target today is an **nspawn (`systemd-nspawn` / `nixos-container`) machine on
Prometheus**, driven by `nix run .#nspawn-dune-on-prometheus`. A routed,
human-viewable **microVM** with its own reachable Criome domain
(`vm-testing.<cluster>.criome`) is fully *designed and tested in CI* but lives
only on the CriomOS `next` branch and is **NOT deployed** to any node. The gap
to a true lojix end-to-end *deploy* test is in lojix itself: the production
daemon currently **rejects all activating actions**.

## 1. The test-cluster fixture

`/git/github.com/LiGoldragon/CriomOS-test-cluster/` — a deliberately separate
repo so no production names/passwords/host-facts leak into the platform repo
(`README.md:1-8`).

- **Synthetic cluster proposal**: `clusters/fieldlab.nota` plus two
  negative-case fixtures (`fieldlab-two-controllers.nota`,
  `fieldlab-pod-missing-super-node.nota`) — `flake.nix:44-85`. Synthetic node
  names are `atlas beacon cedar dune` (`flake.nix:46`), NOT production names.
- **Pinned Horizon projections**: `fixtures/horizon/{atlas,beacon,cedar,dune}.json`
  — the checks run `horizon-cli` over `fieldlab.nota` and `cmp` against these
  golden files (`flake.nix:44-55`).
- **Pure checks** (`nix flake check`): horizon projection, multi-controller
  rejection, missing-super-node rejection, plus CriomOS module-render checks
  (`checks/cluster-contracts.nix`, `checks/full-module-contracts.nix`,
  `checks/source-constraints.nix`) — `README.md:10-29`, `flake.nix:87-103`.
- **Build/boot targets** for the synthetic Pod node `dune`:
  `dune-toplevel` (full system) and `dune-nspawn-toplevel` (container-aware
  variant with greetd/yggdrasil/wpa_supplicant force-disabled) —
  `flake.nix:201-215`.
- **Spirit-upgrade nspawn pilot**: `spirit-nspawn-toplevel` boots a minimal
  systemd guest carrying spirit v0.1.0 + v0.1.1 + the `upgrade` binary to
  exercise the DB migration path (`flake.nix:99-103,167-198`).

## 2. The remote-runner mechanism (this is the live E2E path)

Four `*-on-prometheus` apps wrap an `ssh "$host" bash -s` heredoc
(`flake.nix:221-285`); default host is **`prometheus.goldragon.criome`**
(`scripts/nspawn-dune-on-prometheus:4`). Flow of `nspawn-dune-on-prometheus`
(`scripts/nspawn-dune-on-prometheus`):

1. `jj git push --bookmark main` (line 6) — pushes the public flake first.
2. On Prometheus: `nix build github:LiGoldragon/CriomOS-test-cluster#dune-nspawn-toplevel`
   (line 24).
3. `criomos-nspawn create/start <machine> <system-path>` (lines 30-31), wait for
   `hostname`, assert `= dune`, then `criomos-nspawn ip`,
   `systemctl is-system-running --wait`, and teardown (lines 14-57).

`criomos-nspawn` is a deployed wrapper over `nixos-container`
(`CriomOS@next:modules/nixos/nspawn.nix`): subcommands
`create/update/start/stop/restart/terminate/shell/status/remove/list/ip`,
self-escalates via `/run/wrappers/bin/sudo`, gated on
`size.large && behavesAs.center && !isContainer` (so it lands on Center/large
nodes like Prometheus). The container gets an IP on the host-internal nspawn
bridge (`criomos-nspawn ip`), reachable **from Prometheus**, not routed cluster-wide.

## 3. Production cluster definition — node roles

`/git/github.com/LiGoldragon/goldragon/datom.nota` (horizon-rs `ClusterProposal`,
positional records). Five server nodes (`datom.nota:5-156`):

| Node | Role (`datom.nota`) | Notes |
|---|---|---|
| **balboa** | `Center` (`:6`) | Arm64 rock64, SD-card NixOS, minimal. |
| **ouranos** | `EdgeTesting` (`:28`) | **This workstation** (ThinkPad T14 Gen5). TailnetController, NixBuilder, Gitolite, PersonaDevelopment (`:58`). |
| **prometheus** | `LargeAiRouter` (`:59`) | GMKtec EVO-X2, 128 GB; cluster **router** (`:95`), NixBuilder+NixCache (`:97`). The build/test host. |
| **tiger** | `EdgeTesting` (`:98`) | ThinkPad E15; NixBuilder (`:125`). |
| **zeus** | `Edge` (`:126`) | ThinkPad T14 Gen2. |

Users (`:157-188`): `bird` (Multimedia), `li` (Unlimited, LiGoldragon).
Because Prometheus is `LargeAiRouter`, any VM-testing deploy there is gated on
proven networking non-breakage (Spirit `5hir5bnz`, report 69).

## 4. How a node / container gets a reachable IP from this host

Two layers, both confirmed live from ouranos:

- **Inter-node (works now).** `/etc/hosts` carries Yggdrasil `200::/7` ULA
  addresses for cluster nodes:
  `prometheus.goldragon.criome → 200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f`
  (and `nix.prometheus...`), `zeus`, `tiger`, `ouranos`, plus `5::N`
  `wg.<node>.goldragon.criome` WireGuard addrs (these `5::N` match the
  `(Some [5::N/128])` fields in `datom.nota:49,88,116`). `~/.ssh/config` aliases
  `prometheus` to the FQDN. **Verified**:
  `ssh prometheus.goldragon.criome` → `REACHED prometheus`, user `li`,
  `criomos-nspawn` present at `/run/current-system/sw/bin/criomos-nspawn`.
  (Tailscale CLI on ouranos reports `NoState` / logged-out, so Yggdrasil — not
  Tailscale — is the working transport today.)
- **Container IP (host-local).** An nspawn machine's IP from `criomos-nspawn ip`
  lives on Prometheus's internal nspawn bridge — reachable from Prometheus, not
  directly routed to ouranos. Fine for an on-Prometheus smoke; not a
  cross-cluster reachable endpoint.
- **MicroVM routed IP + Criome domain (designed, NOT deployed).** Report 69
  (`system-designer/69-criomos-vm-testing-feature-landed-2026-06-04.md`) +
  `CriomOS@next:modules/nixos/vm-testing/default.nix` add a persistent routed
  microVM (`microvm.nix`, `github:astro/microvm.nix`) with a tap interface and a
  projected `vm-testing.<cluster>.criome` `networking.hosts` entry resolving to
  the host node IP, for `domain-criome` registration (Spirit 2630/2631). This is
  the intended *reachable, human-viewable* VM endpoint.

## 5. Deployment state of the VM feature — the catch

The vm-testing/microVM module exists ONLY on CriomOS `next`
(jj bookmark `next` @ change `qnqvptllvnrk`; files
`modules/nixos/vm-testing/default.nix`, `checks/vm-testing-prometheus-policy/`
present at `next`, absent on the colocated `main` working copy). Report 69
states "No deploy to any node." **Verified on live Prometheus**: `ls
/run/current-system/sw/bin` has `nixos-container` but **no** `microvm`/`qemu`/
`virsh` binaries — Prometheus runs CriomOS `main`, so the microVM path is not
yet active. The chroma booted-VM check (`runNixOSTest`) passes in CI/locally
where `/dev/kvm` exists, but that is a hermetic Nix test, not a routed endpoint.

## 6. lojix-side gap (the real blocker to an end-to-end *deploy* test)

From `system-operator/205-lojix-horizon-production-materialization-2026-06-10.md`:
the production `lojix` daemon now does Horizon materialization + `nix eval`/build
for `System Eval`/`Build` and `Home Build`, but **still REJECTS every activating
action** — `Switch`, `Boot`, `Test`, `BootOnce`, Home `Profile`/`Activate` —
because `CopyClosure`/`ActivateGeneration` do not yet carry the closure path into
the remote activation command (report 205 §"Guard change", §"Remaining
Blockers"). Also open: `secrets` input not materialized; SEMA state still
in-memory; build smoke is eval-only (no real closure built). So lojix today can
*evaluate/build* against the test cluster but cannot *activate* a system — there
is no daemon-driven boot of a guest yet.

## 7. Recommended end-to-end test target + concrete gap

**Recommended target (fastest to working):** drive lojix against the existing
synthetic node `dune` on **Prometheus over the nspawn path**. It is the only
target where (a) the host is reachable and authenticated from ouranos
(`ssh prometheus.goldragon.criome` verified), (b) a deploy primitive
(`criomos-nspawn create/start/shell`) is already deployed and exercised by
`nspawn-dune-on-prometheus`, and (c) the test cluster already produces a
buildable container toplevel (`dune-nspawn-toplevel`). lojix builds the closure
(materialize Horizon from `fieldlab.nota` → `nix build`), then activation is a
`criomos-nspawn create/update + start` of that store path rather than a
host-level `switch-to-configuration` — far less risky than activating a router
node, and it matches the proven manual runner.

**Concrete gap to a working lojix deploy test:**
1. **lojix must gain a non-rejected activation path.** Either make
   `CopyClosure`/`ActivateGeneration` carry the closure path (report 205 blocker
   1), or add an nspawn-target activation that shells `criomos-nspawn
   create/update <name> <built-toplevel> && start` on the remote — the
   lowest-risk first activation.
2. **Materialize `secrets`** (report 205 blocker 2) if the chosen node needs
   SOPS/router secrets; `dune` is a Pod node and avoids most of this.
3. **A reachable, routed endpoint** (vs host-local nspawn IP) requires deploying
   the `next` vm-testing microVM module to a node and registering
   `vm-testing.<cluster>.criome` — gated on Prometheus networking non-breakage
   (Spirit `5hir5bnz`); defer until after the nspawn-path E2E passes.

**Unknowns (not verified):** whether `criomos-nspawn` accepts a store path built
by lojix's materialization unchanged (the runner builds via `nix build` on
Prometheus, not via lojix); and exact `dune-nspawn-toplevel` boot success on the
*current* deployed Prometheus (the runner is the authority, not run here).

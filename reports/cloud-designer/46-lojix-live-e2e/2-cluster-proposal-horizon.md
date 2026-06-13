# 46 · S5 grounding — the cluster-proposal / horizon piece

The VM as a node the lojix daemon materializes + builds a full-OS toplevel
for. All findings READ-ONLY; cited to `path:line` or the exact command run.

## TL;DR

- **Two deploy modes in the daemon, chosen by `build_attribute`** on the
  `SystemDeployment` (`meta-signal-lojix/schema/lib.schema:96`,
  `meta-signal-lojix/src/schema/lib.rs:149`):
  - `build_attribute = None` → **production path**: daemon runs
    `MaterializeHorizon` (projects the `datom.nota` proposal through horizon-rs
    into three generated path-flakes — `horizon`, `system`, `deployment` —
    `schema_runtime.rs:1849-1990`), then evals
    `<flake>#nixosConfigurations.target.config.system.build.toplevel`
    with `--override-input horizon/system/deployment <generated path-flake>`
    (`schema_runtime.rs:280-289, 1154-1162, 2815-2823`).
  - `build_attribute = Some(attr)` → **fixture path**:
    `needs_horizon_materialization()` is `false`
    (`schema_runtime.rs:379-381`), MaterializeHorizon is SKIPPED, and the
    daemon evals/builds `<flake>#<attr>.drvPath` with **no** override-inputs
    (`schema_runtime.rs:416-426, 1153-1162, 2734-2742`).
- **The fixture flake `github:LiGoldragon/CriomOS-test-cluster` has NO
  `nixosConfigurations` output** (`nix flake show`, run above) — only
  `packages.<system>.dune-toplevel` and `.dune-nspawn-toplevel`. So a fixture
  deploy MUST use the `build_attribute` mode; the production
  `nixosConfigurations.target` form would fail at eval against this flake.
- **`dune-toplevel` is a real bootable full OS.**
  `nix eval --raw …#packages.x86_64-linux.dune-toplevel.outPath` →
  `/nix/store/wfkrw…-nixos-system-dune-26.05.20260422.0726a0e` (run above): a
  standard NixOS system toplevel. Built by `fixtureSystem "dune" []` =
  `nixpkgs.lib.nixosSystem { modules = [ criomos.nixosModules.criomos ]; }
  .config.system.build.toplevel` with `horizon = fixtureHorizon "dune"`
  (`CriomOS-test-cluster/flake.nix:114-133, 201`). It does NOT set
  `boot.isContainer` — that flag is only on `dune-nspawn-toplevel`
  (`flake.nix:202-215`). So `dune-toplevel` = full bootable OS (kernel +
  bootloader + init), `dune-nspawn-toplevel` = container variant for
  `criomos-nspawn` smoke tests, `spirit-nspawn-toplevel` = minimal.

## The Deploy: flake + node + proposal-source

There is NO checked-in meta-lojix `Deploy` datom naming the fixture; the
existing fixture drivers are nspawn/build scripts
(`scripts/build-dune-on-prometheus`, `scripts/nspawn-dune-on-prometheus`),
not daemon deploys. The S5 Deploy the daemon should be issued (System
deployment, `meta-signal-lojix/schema/lib.schema:87-97`) is:

- **cluster** = `fieldlab`
- **node** = `dune` (synthetic Pod/Edge node; `fieldlab.nota:80-104`)
- **proposal source** = local path to `clusters/fieldlab.nota` (the
  `datom.nota` proposal; loaded by `ProposalFile` via `fs::read_to_string` +
  `NotaSource::parse`, `schema_runtime.rs:1868-1877`) — only consulted in the
  production path; with `build_attribute` set it is unused for eval but is
  still a required field and is what would feed horizon projection.
- **flake** = `github:LiGoldragon/CriomOS-test-cluster`
- **build_attribute** = `packages.x86_64-linux.dune-toplevel` (full OS) — or
  `packages.x86_64-linux.dune-nspawn-toplevel` if testing the container path.
  Daemon evals `github:LiGoldragon/CriomOS-test-cluster#packages.x86_64-linux.dune-toplevel.drvPath`.
- **system_action** = `BootOnce` (S5 wants the BootOnce activation + the
  resumable transient unit `lojix-boot-once-deploy-<id>`,
  `schema_runtime.rs:512-520`); `Boot`/`Switch` also valid.
- **builder** = `None` (local build on the dispatcher = Prometheus), or
  `Some prometheus`.

Caveat: the fixture toplevel pins `nixpkgs github:LiGoldragon/nixpkgs?ref=main`
and a fixed horizon JSON, so it is **architecturally x86_64**; matching the
qemu VM arch (x86_64) is required.

## The networking bridge — how `root@dune.fieldlab.criome` reaches the VM

The daemon's SSH/`nix copy` target is computed purely from cluster+node on the
deploy cursor — `CriomeDomainName::for_node(node, cluster)` =
`format!("{node}.{cluster}.criome")` (`horizon-rs/lib/src/name.rs:101-109`),
wrapped as `root@<domain>` by `SshTarget::root_at_node`
(`schema_runtime.rs:2154-2192`). For the fixture that is **exactly
`root@dune.fieldlab.criome`** — copy uses `ssh-ng://root@dune.fieldlab.criome`
(`schema_runtime.rs:2186-2192, 2298-2311`), activate sshes to the same
(`schema_runtime.rs:2344, 2195-2205`). The daemon CANNOT be told a raw IP /
port; addressing is derived, not configurable.

**`dune.fieldlab.criome` does NOT resolve on Prometheus today** — verified
`getent hosts dune.fieldlab.criome` → NO_RESOLVE, and tailscale is "Logged
out" (no MagicDNS) (ssh inspection run above). So the bridge MUST be an
explicit name→VM mapping created on the daemon host (Prometheus), host config
untouched:

- **Cleanest: qemu user-net hostfwd + a daemon-host `/etc/hosts` (or
  `~/.ssh/config` Host alias) entry** mapping `dune.fieldlab.criome` →
  `127.0.0.1`, with qemu `-netdev user,hostfwd=tcp::2222-:22` and an
  `~/.ssh/config` block `Host dune.fieldlab.criome { HostName 127.0.0.1; Port
  2222; User root; StrictHostKeyChecking no }`. ssh + `nix copy --to
  ssh-ng://root@dune.fieldlab.criome` then both honor the alias. This avoids
  any Prometheus host-config / DNS change (S5 safety constraint) since it only
  touches the runner user's `~/.ssh/config`.
- Alternative: a qemu **tap** interface with a fixed VM IP and an `/etc/hosts`
  line — but `/etc/hosts` is system-level on NixOS (declarative), so it would
  mutate host config; prefer the `~/.ssh/config` user-level alias.
- The VM's guest NixOS must run sshd accepting `root` with the runner's key
  (covered by sub-agent 1's VM piece).

## Identity recommendation

Make the VM literally **synthetic node `dune` of cluster `fieldlab`**: boot it
on the `dune-toplevel` full OS, then have the daemon deploy the (next
generation of) `dune-toplevel` into it. The fixture already pins dune's
identity end-to-end — `criomeDomainName: dune.fieldlab.criome`,
`nodeIp 10.77.0.4/24`, hostname `dune` (`fixtures/horizon/dune.json`) — and
the daemon's derived address `root@dune.fieldlab.criome` matches that identity
exactly, so the only glue needed is the `~/.ssh/config` alias above. A simpler
standalone target is possible but would still resolve to
`root@<node>.<cluster>.criome`, so `dune`/`fieldlab` is the path of least
friction.

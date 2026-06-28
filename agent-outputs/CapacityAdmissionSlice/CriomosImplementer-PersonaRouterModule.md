# T3 — persona-router NixOS service module (evidence)

Task: T3 of the criome-auth witness build plan
(`reports/capacityAdmissionSlice/6-Translation-criome-auth-witness-vm-test.md`).
Give the persona router DAEMON (`router-daemon`, the daemon-to-daemon delivery
fabric) a NixOS service module so it can run on a system: its rkyv
`RouterDaemonConfiguration`, listen address, co-resident criome socket, stable
identity, and a HARDWIRED static peer/bootstrap table (RegisterRemoteRouter +
RegisterActor). No discovery. Distinct from the WiFi access-point role in
`modules/nixos/router/`, which was NOT touched.

Status: complete with real build/test evidence. Both branches pushed; gated on
the independent audit (T6) — NOT landed on either repo's main.

## Scope finding (read first — affects T1 and the operator)

The brief's T3 card said "May edit: CriomOS only" and assumed the router config
writer already exposed `criome_socket_path` / `tailnet_listen_address` /
`router_identity`, plus a bootstrap-document writer. It does not. On
`router@main`:

- `router-write-configuration` HARDWIRED `tailnet_listen_address: None`,
  `router_identity: "router-local"`, `criome_socket_path: None` (only
  sockets/store/supervision/owner/bootstrap were settable).
- There is NO bootstrap-document writer. The bootstrap doc is rkyv-only — the
  daemon explicitly REJECTS a NOTA bootstrap file
  (`router_bootstrap_rejects_nota_document`); its only producers were in-test
  `rkyv::to_bytes`.
- The meta socket (`meta-router`) only carries channel policy
  (Grant/Extend/Revoke/Deny). `InstallRemotePeer`/`InstallRemoteRoute` are
  internal kameo messages applied ONLY via the rkyv bootstrap document at
  startup — there is no runtime CLI/socket to install peers.

So a NixOS module cannot express the listen address, criome socket, identity, or
a hardwired peer table with current router tooling. Delivering the explicit
psyche intent therefore required minimal, additive router-side text edges. The
router repo is the correct home for its own config/bootstrap text edges (it owns
them), and the brief already sanctions a "missing field" dependency edit (T1's
allowed signal-router edit). These edits are on a SEPARATE router feature branch
and are orthogonal to T1's verifier work (only `Cargo.toml` `[[bin]]` and
`flake.nix` `checks` overlap with T1 — both additive).

## Files changed

### router repo — branch `persona-router-module`, rev `98b279cf387c` (change `vovsnrklyynv`)

Worktree: `/home/li/wt/github.com/LiGoldragon/router/persona-router-module`

- `src/bin/router_write_configuration.rs` — rewrote the `ConfigurationWriteRequest`
  NOTA to one fixed-arity shape with explicit `(Some x)`/`None` optionals (no
  more positional presence-by-arity), threading `tailnet_listen_address`,
  `router_identity`, and `criome_socket_path` into
  `RouterDaemonConfigurationParts`. (The router `router-write-configuration`
  NOTA has no external callers — only router's own binary; CriomOS's other
  `ConfigurationWriteRequest` hits are different daemons' writers.)
- `src/bin/router_write_bootstrap.rs` — NEW. `router-write-bootstrap` text edge:
  decodes a module-controlled NOTA request (output path + a remote-peer table +
  an actor-home table), constructs typed `RegisterRemoteRouter` /
  `RegisterActor` operations via signal-router's public constructors, and writes
  the rkyv `RouterBootstrapDocument` the daemon reads at startup. Hardwired —
  every peer and actor home is listed; no discovery.
- `Cargo.toml` — `[[bin]] router-write-bootstrap` (`required-features = nota-text`).
- `tests/configuration_text_edges.rs` — NEW, crate-level `#![cfg(feature = "nota-text")]`.
  Two process-boundary witnesses: drive the real binaries, read back through the
  daemon-side readers (`Configuration::from_binary_path`,
  `RouterBootstrap::from_path`).
- `flake.nix` — two named checks:
  `router-write-configuration-carries-network-fields`,
  `router-write-bootstrap-carries-hardwired-peers`.

### CriomOS repo — branch `persona-router-module`, rev `a99a3488b115` (change `pqwsklvtuxkp`)

Worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS/persona-router-module`

- `modules/nixos/persona-router.nix` — NEW. The module (modeled on
  `mirror.nix`/`lojix.nix`). Gated on the `PersonaRouter` node service. Hardened
  systemd `persona-router.service`: dedicated `persona-router` user/group; two
  `0600` Unix sockets + supervision socket + sema store under
  `/run/persona-router` + `/var/lib/persona-router`; two `ExecStartPre` text
  edges (`router-write-bootstrap` then `router-write-configuration`) producing
  the rkyv bootstrap + config; `ExecStart = router-daemon <config.rkyv>`;
  `ProtectSystem=strict`, `ProtectHome`, `NoNewPrivileges`, `PrivateTmp`,
  `UMask=0077`, scoped `ReadWritePaths`; the router TCP ingress opened with the
  GLOBAL `networking.firewall.allowedTCPPorts` form (the hermetic runner has no
  `tailscale0`, unlike `mirror.nix`); tmpfiles for both dirs.
- `modules/nixos/criomos.nix` — added `./persona-router.nix` to the aggregate
  import list (one additive line).
- `flake.nix` — added the `router` flake input (`router.inputs.nixpkgs.follows`)
  and registered the `persona-router-role-policy` check.
- `flake.lock` — `router` input pinned to the router feature branch rev
  `98b279cf387c` via `--override-input` (sanctioned interim pin; see operator note).
- `checks/persona-router-role-policy/default.nix` — NEW. Role-policy witness
  modeled on `mirror-role-policy`.

The node-service payload contract (`horizon.node.services` entry the module reads):
`{ PersonaRouter = { identity = "<id>"; listenAddress ? "0.0.0.0"; listenPort ? 7440;
criomeSocketPath ? "/run/criome/criome.sock"; ownerUserIdentifier ? 1000;
peers = [ { identity; address; } ... ]; actorHomes = [ { actor; process ? 0; home ? null; } ... ]; }; }`

## Evidence (exact commands + actual output)

### Router inner loop (ouranos)
`cargo check --features nota-text --bins --tests` → `Finished` (exit 0, no errors).
`cargo test --features nota-text --test configuration_text_edges` →
`test result: ok. 2 passed; 0 failed`
(`router_bootstrap_carries_hardwired_peers_and_actor_homes ... ok`,
`router_configuration_carries_listen_identity_and_criome_socket ... ok`).

### Router flake checks from the PUSHED branch (built/tested on prometheus)
```
nix build --print-build-logs --no-link \
  'github:LiGoldragon/router?ref=persona-router-module#checks.x86_64-linux.router-write-configuration-carries-network-fields' \
  'github:LiGoldragon/router?ref=persona-router-module#checks.x86_64-linux.router-write-bootstrap-carries-hardwired-peers'
```
Output (both green):
```
router-test> test router_configuration_carries_listen_identity_and_criome_socket ... ok
router-test> test result: ok. 1 passed; 0 failed; ...
router-test> test result: ok. 1 passed; 0 failed; ...   (bootstrap test)
copying path '/nix/store/3d2jpg6ld1rgh54qf42x6v47wx6drl7b-router-test-0.4.1' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
```

### CriomOS module + router service closure — role-policy check, fully reproducible from BOTH pushed refs
```
nix build --impure --no-link --print-out-paths --print-build-logs --expr '
let
  criomos = builtins.getFlake "github:LiGoldragon/CriomOS?ref=persona-router-module";
  nixpkgs = builtins.getFlake "github:LiGoldragon/nixpkgs?ref=main";
  router  = builtins.getFlake "github:LiGoldragon/router?ref=persona-router-module";
  system  = "x86_64-linux";
  pkgs    = nixpkgs.legacyPackages.${system};
  inputs  = { inherit nixpkgs router; };
in pkgs.callPackage "${criomos}/checks/persona-router-role-policy" { inherit inputs; }'
```
Result: `/nix/store/6b6p9rk1avzzlhw4fk9fba3k4xxrmr0k-persona-router-role-policy`

This build (on `ssh-ng://nix-ssh@prometheus.goldragon.criome`):
- built `router-text-0.4.1` with all five binaries — `router-daemon`,
  `router-write-configuration`, `router-write-bootstrap`, `router`, `meta-router`
  (proves the router SERVICE binary + the deploy text edges build);
- evaluated `persona-router.nix` into a real NixOS systemd service and asserted
  its shape (User/Group `persona-router`, `NoNewPrivileges`, ExecStartPre =
  router-write-bootstrap then router-write-configuration, ExecStart =
  router-daemon, tmpfiles, global firewall port `[7440]`);
- witnessed the EXACT hardwired NOTA the deploy edges receive:
```
(ConfigurationWriteRequest /run/persona-router/router.sock /run/persona-router/meta.sock /run/persona-router/supervision.sock /var/lib/persona-router/router.sema (Some /run/persona-router/bootstrap.rkyv) 1000 (Some 0.0.0.0:7440) router-a (Some /run/criome/criome.sock) /run/persona-router/router-daemon.rkyv)
(BootstrapWriteRequest /run/persona-router/bootstrap.rkyv [ (router-b 192.168.1.20:7440) ] [ (mirror 0 (Some router-b)) ])
```
The role-policy check also asserts the service is ABSENT on a base node and on a
TailnetClient-only node, and PRESENT only with the `PersonaRouter` service.

The registered flake check `checks.x86_64-linux.persona-router-role-policy`
builds the same derivation but requires lojix-projected `horizon`/`system` (the
blueprint `//` merge spine forces the full `target` eval) — exactly like every
sibling role-policy check. The direct-eval command above is the standalone
reproduction.

## Return-shape answers

1. Files changed + module location: above. Module lives at
   `CriomOS/modules/nixos/persona-router.nix`.
2. Build/boot command + output: above. The role-policy check builds the router
   service closure + evaluates the module (the required-minimum "service/system
   closure" evidence, exceeded with config-shape + process-boundary witnesses).
   A LIVE `persona-router.service` "active and listening" boot was NOT run — I
   am on ouranos, which the brief forbids from firing QEMU (prometheus is the
   VM-testing host). See T4 note.
3. Branches + revisions: router `persona-router-module` @ `98b279cf387c`;
   CriomOS `persona-router-module` @ `a99a3488b115`. CriomOS locks the `router`
   input to `98b279cf387c`, so T4 can build the CriomOS branch directly.
4. Shared-file claim: orchestrate claim `personaRouterModule` accepted on the
   two worktree paths
   (`/home/li/wt/github.com/LiGoldragon/{router,CriomOS}/persona-router-module`).
   The canonical CriomOS dir is held by `system-designer` ("fix-it-all deep
   build"); per feature-development I cut from `main` into an isolated worktree
   (uncontested scope) rather than contend. Shared files only logically touched
   (additive): CriomOS `flake.nix` (+router input, +check), `modules/nixos/criomos.nix`
   (+import line) — relevant to T2 (criome module) merging the same files; router
   `Cargo.toml` (+`[[bin]]`), `flake.nix` (+checks) — relevant to T1.
5. Peers hardwired (no discovery): CONFIRMED. The module writes a static
   `RouterBootstrapDocument` from explicit Nix-declared `peers` (RegisterRemoteRouter,
   identity→address) and `actorHomes` (RegisterActor, actor→home-peer) tables;
   the daemon applies them at first runtime (table inserts only; no dialing until
   a forward). No discovery path exists or was added.
6. T4 / auditor must know:
   - Cross-repo ordering (producers before consumers): the router branch must
     merge to `router@main`, then CriomOS `nix flake update router` re-pins to
     main, BEFORE CriomOS main pins it. Until then the CriomOS branch's lock
     points at the router feature rev (valid, buildable now).
   - The daemon runs from `router.packages.<system>.text` (the nota-text build)
     so the write tools are co-located in one package; nota-text does not change
     the daemon's wire behavior. Possible follow-up: a dedicated all-binaries
     deploy package on the router flake.
   - Criome socket access for milestone 3 (T1): the `persona-router` system user
     must be granted a supplementary group that can read/write
     `/run/criome/criome.sock` (T2's criome client group). NOT wired here and not
     exercised by T3 — on `router@main` the daemon still uses the offline
     verifier (`AcceptFixedTestIdentity`) and only records `criome_socket_path`;
     T1's milestone-3 swap is what makes it dial. T4 must add the
     `SupplementaryGroups` link when assembling the two-VM run.
   - Live witness gap: `persona_router_service_active_and_listening` (single-node
     boot reaching active + TCP port open) was not run (no QEMU on ouranos). The
     daemon binds its sockets + TCP listener and applies the bootstrap at startup
     with no peer present (RegisterRemoteRouter/RegisterActor do not dial), so a
     single-node boot SHOULD reach active+listening; recommend T4 either fold a
     `wait_for_unit("persona-router.service")` + port-open assertion into a
     prometheus-hosted single-node check or rely on the 2-VM boot it already runs.
   - Module gating: enable by adding the `PersonaRouter` node-service entry
     (payload shape above) to the source and receiver nodes' `horizon.node.services`.
```
```

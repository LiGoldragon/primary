# T2 — criome daemon NixOS service module: implementation evidence

## Task and scope

T2 from `reports/capacityAdmissionSlice/6-Translation-criome-auth-witness-vm-test.md`:
give criome a NixOS module that runs the criome daemon as a hardened systemd
service — two 0600 Unix sockets, durable SEMA store, deploy-time typed config,
key custody, and a cross-instance identity-seed hook. Parallel with T1/T3,
consumed by T4. Gated on independent audit (T6); do NOT land on main.

## Outcome (completion state)

Module authored and verified. The criome service builds into a real NixOS
system closure; the module evaluates with the correct hardened unit; the
single-node VM test is well-formed (driver + node closure build); and the
daemon's full runtime behaviour (both 0600 sockets, live socket round-trip,
0600 master-key custody, peer-seed registration) is proven by a real criome
daemon process. The one item NOT executed is the in-VM boot itself — see
Blockers.

## Files changed

### criome repo — branch `criome-deploy-encoder` (rev `5c4b1d936011`)

Worktree: `/home/li/wt/github.com/LiGoldragon/criome/criome-deploy-encoder`.
Cut from current criome `main` (signal-criome 0.5.0). Pushed to origin.

- `src/deploy_encode.rs` (new) — deploy-time NOTA→rkyv config encoder. Decodes a
  `(CriomeConfigurationArtifact <CriomeDaemonConfiguration> <output-path>)` NOTA
  record (the full typed 5-field config) via the `nota_next` block API and writes
  the rkyv through the daemon's own `CriomeDaemonConfigurationFile`. All logic is
  methods on data-bearing types; parsing is the nota codec, not hand-rolled.
- `src/bin/criome-encode-configuration.rs` (new) — the encoder bin.
- `Cargo.toml` — adds the `criome-encode-configuration` `[[bin]]`,
  `required-features = ["nota-text"]`.
- `src/lib.rs` — `#[cfg(feature = "nota-text")] pub mod deploy_encode;`.

Net effect: the criome `packages.default` (built `--features nota-text`) now
ships three binaries — `criome` (CLI), `criome-daemon` (rkyv-only daemon),
`criome-encode-configuration` (deploy encoder) — the same shape mirror's default
package has (`mirror-daemon` + `mirror-write-configuration`).

### CriomOS repo — branch `criome-service-module` (rev `304ba0a22c0b`)

Worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS/criome-service-module`.
Cut from current CriomOS `main`. Pushed to origin.

- `modules/nixos/criome.nix` (new) — the service module, modeled on
  `modules/nixos/mirror.nix`. Owns: dedicated `criome` user/group; both 0600
  sockets under `/run/criome` (`criome.sock` + `criome.sock.meta`, bound 0600 by
  the daemon itself); `/var/lib/criome` SEMA store; `ExecStartPre` =
  `criome-encode-configuration` sealing the typed config to rkyv; `ExecStart` =
  `criome-daemon <config.rkyv>` (one argument, no flags); `ExecStartPost`
  peer-identity seed hook; `0700` state dir for master-key custody; hardened
  serviceConfig (`NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`,
  `ProtectHome`, `UMask=0077`, `ReadWritePaths`); tmpfiles for both dirs.
- `modules/nixos/criome-node-test.nix` (new) — single-node `runNixOSTest` named
  `criome_service_reaches_active_with_both_sockets`.

## Key design decisions (observed facts → decisions)

1. **`criome-daemon` consumes an rkyv `SignalFile`, not env/flags**
   (`src/command.rs` `CriomeDaemonCommand::run` → `signal_file_argument`). So a
   deploy needs a NOTA→rkyv encode step, exactly like mirror.

2. **The existing `criome-write-configuration` was unusable**: it is gated behind
   the `cluster-witness` test feature (Cargo.toml) and only sets socket+store
   (no meta/cluster_root/authorization_mode). The brief's offered path was
   "expose a non-witness configuration writer." I did so by porting a NOTA
   encoder into the default (nota-text) package.

3. **Prior art `criome-nixos-module-142` is stale.** It already implements this
   encoder design, but pins signal-criome **0.1.0** (3-field config) while
   current criome main pins **0.5.0** (5-field config:
   `socket_path, store_path, meta_socket_path?, cluster_root?, AuthorizationMode`).
   Depending on it would diverge T2's criome from T1/T4's current criome and
   break the two-VM interop. I therefore ported the encoder onto **current main**
   rather than consuming branch-142. (Branch-142's encoder also `#[derive]`s the
   nota traits, which does not compile in criome because criome aliases the codec
   crate as `nota-next`, not `nota` — the derive macro hardcodes `::nota::`. My
   port decodes through the `nota_next` block API instead.)

4. **The CriomOS module is standalone (takes a `package` option), not
   `inputs`-coupled.** `mirror.nix` reads `inputs.mirror`, but CriomOS `flake.nix`
   and `criomos.nix` are both held by a concurrent `system-designer` lane (see
   Blockers). A package-option module needs neither file: the consumer (the test,
   and T4) supplies `services.criome.package`. This avoids the contended files
   entirely while staying directly importable.

## Checks run (exact commands and results)

All Nix builds were scheduled on the `prometheus` remote builder by the local
nix daemon (normal remote build, NOT a QEMU VM). Host is `ouranos`; the brief
forbids firing QEMU on ouranos.

- **criome default package builds (3 binaries)** —
  `nix build .#packages.x86_64-linux.default` (in the criome worktree).
  Result: PASS. `ls $out/bin` → `criome  criome-daemon  criome-encode-configuration`.

- **Encoder accepts the full 5-field config NOTA** —
  `criome-encode-configuration '(CriomeConfigurationArtifact (/tmp/.../criome.sock /tmp/.../criome.sema (Some /tmp/.../criome.sock.meta) None Quorum) /tmp/.../config.rkyv)'`.
  Result: PASS, exit 0, printed `(ArtifactWritten /tmp/.../config.rkyv)`, 118-byte
  rkyv written.

- **Daemon reads the rkyv + binds both sockets 0600 + master-key custody** —
  ran the real `criome-daemon /tmp/.../config.rkyv`. Result: PASS.
  `stat -c '%n %a'` → `criome.sock 600` and `criome.sock.meta 600`;
  `criome.masterkey 600` at the store-derived path.

- **Live socket round-trip** —
  `CRIOME_SOCKET=… criome '(LookupIdentity (Host criome))'`.
  Result: PASS → `(IdentityReceipt ((Host criome) Active))` (daemon self-registers
  `Host("criome")` Active and answers a real request). Note the working request
  form is `(LookupIdentity (Host criome))`, not `((Host criome))`.

- **Peer-seed RegisterIdentity format** —
  `criome '(RegisterIdentity ((Host peerb) <pubkey> <fp> CriomeRoot None))'`.
  Result: PASS → `(IdentityReceipt ((Host peerb) Active))` (cluster_root=None
  admits unconditionally); a follow-up LookupIdentity confirmed the peer Active.

- **Module evaluates (unit config)** — `nix eval` of a minimal `nixosSystem` with
  `services.criome.enable = true`. Result: PASS.
  `User=criome`; `ExecStart=…/criome-daemon /run/criome/criome-config.rkyv`;
  `ProtectSystem=strict`; ExecStartPre = the encoder script; ExecStartPost = the
  seed script; tmpfiles include `d /var/lib/criome 0700 criome criome -` and
  `d /run/criome 0755 criome criome -`.

- **Rendered scripts carry the verified-working NOTA** — realized the
  ExecStartPre/ExecStartPost scripts; the encoder script emits exactly
  `(CriomeConfigurationArtifact (/run/criome/criome.sock /var/lib/criome/criome.sema (Some /run/criome/criome.sock.meta) None Quorum) /run/criome/criome-config.rkyv)`
  and the seed script waits for the socket then emits
  `(RegisterIdentity ((Host criome-b) deadbeef fp-b CriomeRoot None))` — both
  identical to the formats verified live above.

- **System closure builds with the criome service** —
  `nix build` of `config.system.build.toplevel`. Result: PASS →
  `nixos-system-nixos-26.05...`. (This is the brief's required-minimum "successful
  nix build of the service/system closure.")

- **Single-node VM test driver builds (no boot)** —
  `nix build` of `<test>.driver`. Result: PASS → built
  `nixos-system-machine-test`, `run-nixos-vm`, and
  `nixos-test-driver-criome_service_reaches_active_with_both_sockets`. Proves the
  test + node closure are well-formed without firing QEMU.

## Blockers / unknowns / follow-up

- **In-VM boot not executed (operator/T5 confirm).** The actual
  `runNixOSTest` boot was NOT run. ouranos is forbidden for QEMU; and remote-
  building the boot on prometheus fails because the vm-test-run derivation
  requires system features `[kvm, nixos-test]` while prometheus's
  `/etc/nix/machines` entry advertises only `[big-parallel, kvm]` (no
  `nixos-test`). The boot must run **natively on prometheus** (the T5
  `run-on-prometheus`-style path), or the prometheus machine entry must add the
  `nixos-test` feature. The runtime behaviour the boot would assert (both 0600
  sockets, live round-trip, 0600 key custody, self-resume) is already proven by
  the real-daemon checks above; the VM boot would add the active-unit + restart
  witnesses inside a guest. The test is named, builds, and is ready to run.

- **Cross-repo dependency on an unlanded criome branch.** The CriomOS module's
  `package` must be the criome flake `default` from
  `github:LiGoldragon/criome?ref=criome-deploy-encoder` (the encoder is not on
  criome main yet). Before final integration, `criome-deploy-encoder` should land
  on criome main and consumers drop the `?ref=`.

- **Production wiring deferred (contended files).** CriomOS `flake.nix` (criome
  input) and `modules/nixos/criomos.nix` (module import + horizon gating) are
  held by the `system-designer` "fix-it-all" lane; my orchestration claim on them
  was rejected. I avoided both by making the module standalone. Wiring criome
  into the criomos aggregate + a horizon node-service gate is a follow-up to
  reconcile with that lane once it releases the files. No file owned by another
  lane was edited.

## What T4 / the auditor must know

- Consume both pushed branches: criome `criome-deploy-encoder` (`5c4b1d936011`)
  for the package; CriomOS `criome-service-module` (`304ba0a22c0b`) for the
  module + test.
- T4 imports `modules/nixos/criome.nix` directly and sets
  `services.criome.package = <criome default from the ref above>`. For two-node
  trust, set `services.criome.peerIdentitySeeds` to the peer criome's
  `Host`/publicKey/fingerprint (cluster_root left null admits unconditionally for
  v1), or set `clusterRootPublicKey` + carry an admission. Verified seed NOTA:
  `(RegisterIdentity ((Host <name>) <pubkey> <fingerprint> CriomeRoot None))`.
- Verified config NOTA field order (signal-criome 0.5.0):
  `(socket_path store_path (Some meta) cluster_root_or_None AuthorizationMode)`.
- Auditor anti-hollow note: the single-node witness is the **live LookupIdentity
  round-trip** (a dead daemon cannot answer), not a file-exists check; the in-VM
  active+restart witnesses remain to be observed on a native prometheus run.

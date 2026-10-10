# Horizon 0.13.0 repin train — map

Subflow of da88cf, 2026-09-25/26. This is a read-only map. Nothing was built, pushed or deployed.
`<H13>` is the horizon-rs revision that carries 0.13.0. `<S6>`, `<M7>`, `<L8>`, `<C>` and `<G>` are the revisions that each step produces.

## 1. Consumers and pin sites

These revisions come from origin, fetched into the scratchpad on 2026-09-25. Several local checkouts under `/git` are stale.

| Consumer | Pin sites | Pinned now | Version now | Horizon in public API / wire / store | After train |
|---|---|---|---|---|---|
| signal-lojix, **base `f7866bf`** (not main) | `Cargo.toml:19` `horizon-lib` git `rev`; `Cargo.lock` horizon-lib entry | horizon-lib 0.12.0 `ee8d6f8` | 5.0.0 | Yes. `ethos/signal.ethos:4` imports `horizon_lib:[HorizonDefinition]`. `TestDefaults` carries `Option<HorizonDefinition>`, which is rkyv wire, and `pub use generated::signal::*` exports it | **6.0.0** |
| meta-signal-lojix, **base `b500561`** (not main) | `Cargo.toml` `horizon-lib` rev and `signal-lojix` rev; `Cargo.lock` | horizon `ee8d6f8`, signal `f7866bf` | 6.0.0 | Yes. `ActualizedDeploySubmission.{ DeploySubmission Option<HorizonDefinition> }` is exported | **7.0.0** |
| lojix, **`a67f577`** (branch `lojix-horizon-datom31-00f95a`; main `c4bba4f` fast-forwards to it) | root `Cargo.toml`; `nexus/`, `clients/ordinary/`, `clients/meta/` and `tools/Cargo.toml` (horizon in meta and tools; signal and meta revs in all four); `Cargo.lock`; `flake.nix` `horizon.url` plus the `flake.lock` `horizon` node (it composes the VM fixture); `UPGRADES.md` | horizon `ee8d6f8`, signal `f7866bf`, meta `b500561` | 7.0.0 (all five packages) | Yes. It is on the wire, and it is persisted in store rows (see §4) | **8.0.0** |
| CriomOS | `flake.nix` `lojix.url = github:LiGoldragon/lojix/<rev>`; `flake.lock` `lojix` and `horizon_2` (the latter is transitive through lojix) | origin/main: lojix `c4bba4f` (6.0.0). Unpushed local `8c08494`: `a67f577` (7.0.0) | none | It reads only the materialized horizon JSON | pins `<L8>` |
| goldragon | `flake.nix:8` `horizon.url`; `flake.lock` `horizon` | `ee8d6f8` | none | Data: `cluster-definition.datom` has bare `TailnetClient.{}` ×5 and `TailnetController.{}` ×1, which **no longer decode** under 0.13.0 | pins `<H13>` plus the new records |
| criomos-horizon-config | none (it takes `horizonCompose` from goldragon) | — | — | Has no tailnet or router records | unchanged |
| CriomOS-home | horizon is a stub path input | — | — | none | unchanged |
| CriomOS-test-cluster | `horizon-rs/main` (`8d6cbc6`), `lojix/main` (`9d4eae3`) | stale since June | — | — | out of the train; note only |

Versioning rule applied: a wire, storage or public-API change needs a version bump. The consumers' own convention (signal-lojix UPGRADES "4.1.1 to 5.0.0", lojix UPGRADES "6.0.0 to 7.0.0") treats an rkyv archive change as a major bump. 0.13.0 changes the archived layout of `NodeCapability` (new data in the Tailnet variants, a new `UsbDownlink` variant) and of `RouterInterfaces` (an 8th field, `CountryCode`). That makes all three crates major bumps.

The last train set a bad precedent here. signal-lojix `f7866bf` moved horizon 0.10.1→0.12.0 and changed the wire, but kept 5.0.0. Only lojix's 7.0.0 recorded the break. Tonight each crate should bump its own version.

**Hazard:** signal-lojix main `ff02394` and meta main `631d832` already sit on top of `f7866bf`/`b500561` and repin to the abandoned horizon `b45d6ad` (0.5.1 line), under an extra `horizon-current` dependency and without a version bump. The train must branch from `f7866bf` and `b500561`, and each main then needs resetting. da88cf ruled on `b45d6ad` for horizon-rs, but that ruling does not name these two mains.

**Ethos:** horizon-rs `lib/build.rs` asserts that `src/generated/horizon.rs` equals ethos-zero's output for `ethos/horizon.ethos`, using the workspace ethos-zero `4bf73ca` (10.0.0). The tailnet worktree (`/home/li/wt/github.com/LiGoldragon/horizon-rs/tailnet-repair-da88cf`, 11 files changed) regenerates with that same pin and leaves the root `Cargo.toml` unchanged. signal-lojix and meta-signal-lojix only name `horizon_lib::HorizonDefinition`, so their generated `signal.rs` stays byte-identical. They need no regeneration as long as every crate keeps ethos-zero `4bf73ca` and datom-codec `09e2a9d` (0.31.0). **Do not repin ethos-zero to its main `cf7dd12` in this train.** On 09-20, a datom-codec skew (0.26.3 against 0.31.0) broke the contract compile (`flows/8565e8/reports/lojix-schema-compatibility-addendum.md`). The Ethos generator sits upstream of step 1 only.

The contract fixtures (`tests/generated_contract.rs` in both crates, and lojix `tests/common/mod.rs`) use `router_interfaces_option: None` and `OpenCodeTesting`. They compile unchanged against 0.13.0, so the new shapes should be added to them for coverage.

## 2. How the last train ran (Field Sol 8565e8 → 395aed → 7091ea, 09-19..21; deployed 09-24)

- Scope ruling: a repin of Lojix alone is insufficient. Both socket contracts embed the Horizon (`flows/f38926/log.md:88`).
- Order, from `f38926/log.md:89-139` and `7091ea/log.md` ("Child ownership"):
  1. signal-lojix: repin Cargo.toml and Cargo.lock, set the version and UPGRADES, and extend the fixture (OpenCodeTesting plus the Decimal fields, peer-byte rkyv restore and datom round trip).
  2. Publish, then run the remote checks `test-datom-contract` and `test-generated-contract`.
  3. meta-signal-lojix pins the published signal revision and runs the same checks.
  4. lojix: repin the root and the four member Cargo.toml files (a root-only repin left two graphs, `f38926/log.md:108`), plus Cargo.lock, flake.nix/flake.lock and UPGRADES. Bump all five packages. Run `cargo check --workspace --all-targets`, then the Nix checks.
- Check form: `flows/8565e8/scripts/rerun-lojix-contract-checks.sh`, which runs `nix build --no-link -L --builders @/etc/nix/machines --option max-jobs 0 --option fallback false 'git+file:///git/github.com/LiGoldragon/<repo>?rev=<rev>#checks.x86_64-linux.<check>'` sequentially under `timeout 7200` and stops on the first nonzero result.
- The run produced signal `f7866bf` (7 tests pass) and meta `b500561` (8 pass). The lojix proposal `ac672da` failed to rebase. Mind Sol 00f95a later produced `a67f577` (7.0.0; "green all Rust and 317 Nix checks", `b7da5d/vision/ouranosRedeploy.md:27`).
- **The Nexus redeploy was not done by Lojix.** At 15:54 on 09-24, the running 6.0.0 Nexus rejected the 7.0.0 client ("structural wire conversion failed"; `5f38bc/reports/lojix-deployment-investigation.md`). The ouranos journal (witnessed, read-only) then shows a root ssh from ouranos's own Yggdrasil address at 16:14:13, and a `nixos: switching to system configuration /nix/store/n3l8…` at 16:14:26. `lojix.service` stopped and started under that NixOS switch. Its ready line, `(LojixNexusReady …)`, came at 16:14:33 on `lojix-7.0.0`. Further manual switches followed at 16:31 (failed, status 4) and 16:43. Generation 188 (18:43) is the only system generation left.
- In short, Lojix did not deploy itself. A Nexus is restarted by a system switch, because `lojix.service` is a CriomOS NixOS unit (`modules/nixos/lojix.nix`).

## 3. Order tonight

0. horizon-rs `<H13>` (0.13.0). It is based on `ee8d6f8`, pushed, and main is moved to it. The Ethos regeneration happens only here.
1. signal-lojix `<S6>` (6.0.0), from `f7866bf`.
2. meta-signal-lojix `<M7>` (7.0.0), from `b500561`, pinning `<S6>`.
3. lojix `<L8>` (8.0.0), from `a67f577`, pinning `<H13>`, `<S6>` and `<M7>`.
4. goldragon `<G>`: horizon `<H13>`, the new records, and `horizon-definition` built. This can run in parallel with steps 1–3 but must not be submitted before step 6.
5. CriomOS `<C>` pins `<L8>`, together with the tailnet, country and UsbDownlink consumer modules.
6. ouranos host deploy, which restarts the Nexus as 8.0.0.
7. The hosts that consume the records are deployed through Lojix 8: ouranos (tailnet controller) and then Prometheus (router country, UsbDownlink, boot-once).

**Bootstrap problem at step 6:** the running Lojix 7 can only decode a 0.12.0 definition, and it projects with horizon-lib 0.12.0. It therefore cannot deploy `<G>`. It also cannot deploy a CriomOS that *requires* the new projection keys (for example, the Wi-Fi consumer makes `country` required). There are two routes:

- **A (Lojix-mediated, two ouranos deploys).** Lojix 7 deploys a CriomOS commit that pins only `<L8>` on the current goldragon `8c4d03d`. Then Lojix 8 deploys `<C>` with `<G>`.
- **B (09-24 precedent).** `lojix-bootstrap` from `<L8>` runs `BuildOnly.Horizon` for ouranos with `<G>` and `<C>`. The activation then happens outside the Nexus (a manual root switch, or BootOnce). This is one deploy, but it is not Lojix-owned.

## 4. Store risk (lojix `a67f577`)

- The store is schema v5 (`src/lib.rs` `LOJIX_SCHEMA_VERSION`; `src/reconstruction.rs` `CURRENT_SCHEMA = 5`). Per-family `SCHEMA_HASH` values are fixed constants (`[1;32]`…). The catalog therefore will **not** refuse the old store, and there is no migration.
- Two record families hold a `HorizonDefinition` in rkyv:
  - `deploy-job` holds `DeployJob.optional_deploy_submission: Option<DeploySubmission>`. That contains `HostDeployment` and `UserEnvironmentDeployment` `.horizon_definition_option` (`src/runtime_model.rs:507-535, 944-965`).
  - `nexus-configuration` holds `signal_lojix::LojixNexusConfiguration`, which contains `TestDefaults.Option<HorizonDefinition>`. CriomOS writes `NoTestDefaults` there.
- At startup, `validate_startup_compatibility` (`src/lib.rs:1412-1470`) decodes **every** row of every family. Any `deploy-job` row that still carries a 0.12.0-layout definition would fail the decode. The Nexus 8 would then refuse to start (`StoreStartupCompatibility`), crash-loop under `Restart=on-failure`, and `lojix-reset-store` would not help, because it only resets v2–4.
- Deploy-job rows are retracted once their terminal transition is acknowledged (`src/lib.rs:2106-2125`). A clean store therefore has none. The dangerous case is the **Nexus deploying its own host with ActivateNow or TestActivation**: its own in-flight Horizon-mode row is still Activating when the successor starts.
- Leftover rows from the failed deploys 19, 30 and 31 are unverified. The 6→7 start on 09-24 passed validation, which is consistent with the table being empty then.
- Mitigation:
  - (a) Before activation, run `lojix-inspect-store` from `<L8>` against a copy of `/var/lib/lojix/lojix.sema`. The inspector skips `nexus-configuration`. Require zero deploy-job rows.
  - (b) Never self-ActivateNow the Nexus host across this bump. Use route B, or SetBootProfile/boot once the row is terminal and acknowledged.
  - (c) Optionally, give lojix 8.0.0 a test that starts the Nexus on a v5 store holding a 7.0.0 Horizon-mode deploy-job row.

## 5. Briefs

**B1 — signal-lojix 6.0.0.** Repo signal-lojix, new bookmark from `f7866bf013499503d21491bcdaadaf88ea6c810c` (NOT main `ff02394`, which rides the abandoned horizon `b45d6ad`). Set `Cargo.toml` horizon-lib rev to `<H13>`, `cargo update -p horizon-lib` only, and version 5.0.0→6.0.0. Add an UPGRADES "5.0.0 to 6.0.0" entry: HorizonDefinition 0.13.0 layout, rkyv break. Keep ethos-zero `4bf73ca` and datom-codec `09e2a9d`. Confirm `src/generated/signal.rs` is byte-identical. Extend `gold_horizon_definition` with a TailnetController, a TailnetClient, a UsbDownlink and a Router with `RouterInterfaces` including a country, round-tripped through rkyv and datom. Commit and push. Run `test-generated-contract`, `test-datom-contract` and `clippy` on Prometheus (the form of `flows/8565e8/scripts/rerun-lojix-contract-checks.sh`: max-jobs 0, fallback false). Return `<S6>`, the check exits and the lock release. No deploy.

**B2 — meta-signal-lojix 7.0.0.** Branch from `b500561f0ce813917366997581412b7a79aebc99` (NOT main `631d832`). Pin horizon-lib `<H13>` and signal-lojix `<S6>`. Run `cargo update -p horizon-lib -p signal-lojix`, bump the version 6.0.0→7.0.0 and add UPGRADES. Keep ethos-zero and datom-codec unchanged. Generated code must stay identical. Extend `minimal_horizon_definition` in the same way as B1. Push, then run the same three checks on Prometheus. Return `<M7>`. No deploy.

**B3 — lojix 8.0.0.** Branch from `a67f5773979fb2e90727486d24dd300980f914c7`. Repin horizon `<H13>`, signal `<S6>` and meta `<M7>` in the root and all four member `Cargo.toml` files (nexus, clients/ordinary, clients/meta, tools), plus `Cargo.lock`, the `flake.nix` `horizon.url` and `flake.lock`. Bump all five packages to 8.0.0 and add an UPGRADES entry (wire break; store v5 unchanged). `Cargo.lock` must hold exactly one horizon-lib, signal-lojix and meta-signal-lojix. Run `cargo check --workspace --all-targets`, then the full Nix checks on Prometheus. Add a test in which a v5 store holding a 7.0.0 Horizon-mode deploy-job row either starts or is refused, and report which. Push and return `<L8>`. No deploy.

**B4 — goldragon data.** Pin `flake.nix` horizon to `<H13>` and update the lock. Rewrite the tailnet records to `TailnetClient.{ <preauth secret> }` and `TailnetController.{ Option<CA> {tlsCert} {tlsKey} }`. Give Prometheus's RouterInterfaces an 8th field `MX`, and add `UsbDownlink.{ <cidr> }` per the design. Build `#horizonDefinition` on Prometheus and parse it with `horizon-cli --node ouranos` and `--node prometheus`. Push `<G>`. Do not submit it to Lojix before B6 reports Nexus 8.0.0 live.

**B5 — CriomOS pin.** Route A: first make a commit on integrated main that pins only lojix `<L8>` (`flake.nix` `lojix.url`, `nix flake lock --update-input lojix`), and check that ouranos's toplevel evaluates with the current goldragon. Then make `<C>` = that commit plus the tailnet, country and UsbDownlink modules. Build both host toplevels on Prometheus. Return the revisions. No deploy.

**B6 — ouranos Nexus restart (Field, after an explicit go).** Preflight: using `<L8>`'s `lojix-inspect-store` on a copy of `/var/lib/lojix/lojix.sema`, require zero deploy-job rows and no Horizon decode failure. Route A: `lojix-meta` Deploy.Host ouranos, Horizon mode with goldragon `8c4d03d`, the lojix-only CriomOS revision, and SetBootProfile or a route that ends the row before the Nexus stops. Never ActivateNow the Nexus host. Route B: `lojix-bootstrap` BuildOnly.Horizon, then a manual switch (the 09-24 precedent). Witness `readlink /proc/$(systemctl show -p MainPID --value lojix)/exe` = `lojix-8.0.0` and the `(LojixNexusReady …)` line.

**B7 — consumer deploys.** Through Lojix 8, Deploy.Host ouranos with `<G>` and `<C>` (Horizon, RequireImmutable, builds on Prometheus). Then Prometheus with boot-once per ARCHITECTURE.md. Witness the tailscale state, `iw reg get` = MX, and the USB downlink address.

## Sources

- Origin clones in `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/repin-train/` (lojix, signal-lojix, meta-signal-lojix, horizon-rs, CriomOS, goldragon, criomos-horizon-config)
- `/home/li/wt/github.com/LiGoldragon/horizon-rs/tailnet-repair-da88cf` (jj diff from `ee8d6f8`)
- `flows/f38926/log.md:88-139`; `flows/7091ea/log.md`; `flows/8565e8/reports/lojix-schema-compatibility-addendum.md`; `flows/8565e8/reports/morning-2026-09-20.md`; `flows/8565e8/scripts/rerun-lojix-contract-checks.sh`
- `flows/5f38bc/reports/lojix-deployment-investigation.md`; `flows/b7da5d/vision/ouranosRedeploy.md:27`; `flows/da88cf/log.md:44-50,73,78`
- ouranos: `systemctl cat lojix.service`, `ps` on the Nexus PID, `/nix/var/nix/profiles`, `journalctl` 2026-09-24 16:05–17:05 (read-only)

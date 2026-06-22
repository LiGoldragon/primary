# CriomOS-test-cluster VM feature gates and Lojix safe Nix path

## Result

CriomOS-test-cluster branch `pi-operator-vm-feature-gates` is pushed at commit `027d2329` (`test-cluster: expose VM feature gates to pure checks`).

VM-backed checks now carry the scheduler feature gate:

- `nixos-test`
- `criomos-vm-testing`

The implementation lives in the isolated worktree:

`/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/pi-operator-vm-feature-gates`

Touched files:

- `lib/mkVmTest.nix`
- `lib/mkDeployTest.nix`
- `flake.nix`

## How the gate works

`mkVmTest.nix` and `mkDeployTest.nix` use `overrideTestDerivation` on the `runNixOSTest` wrapper so the actual generated `.drv` includes:

- Nix's conventional `nixos-test` feature
- the workspace-specific `criomos-vm-testing` feature

The workspace-specific feature is the fail-closed part: a generic builder that happens to support `nixos-test` is not enough. A builder must explicitly opt into CriomOS VM testing.

Because this nixpkgs `runNixOSTest` wrapper hides the underlying derivation environment behind a structured test set, the generators also expose an evaluator-visible `requiredSystemFeatures` mirror. The pure check reads that mirror, while the real scheduler reads the `.drv` environment.

## Pure non-VM witness

`flake.nix` adds check:

`checks.x86_64-linux.vm-required-system-features`

It inspects all VM-backed checks currently wired in the flake:

- generated `vm-*` checks
- `lojix-deploy-smoke`

It fails if any one lacks either required feature. This witness does not build the VM checks and does not start QEMU.

## Validation run

Formatting passed for touched files:

`nix fmt -- --check flake.nix lib/mkVmTest.nix lib/mkDeployTest.nix`

Pure policy witness passed:

`nix build --refresh .#checks.x86_64-linux.vm-required-system-features --no-link`

Direct derivation inspection, without building VM tests, showed:

- `vm-mercury`: `kvm nixos-test nixos-test criomos-vm-testing`
- `lojix-deploy-smoke`: `kvm nixos-test nixos-test criomos-vm-testing`

The repeated `nixos-test` comes from nixpkgs plus the explicit override; the important new property is that `criomos-vm-testing` is present in the actual `.drv` scheduler environment.

## System-side follow-up

Cloud-designer's proposal is right: the host-side capability should dissolve into `VmHost` rather than a parallel flag. A node declaring `VmHost` should configure its Nix daemon and advertised build-machine features so it can receive VM-test derivations.

The current branch only gates the test derivations. A separate system/CriomOS-side patch still needs to make the authorized builder advertise both features.

The later psyche intent was captured by cloud-designer as Spirit record `tdvr`: `VmHost` should carry typed resource limits for RAM, disk, and CPU, and a running service should hold/enforce that budget. That fits the Lojix direction: static fit-checks happen at projection time, and Lojix or the relevant system component becomes the runtime capacity ledger for on-demand guests.

## Lojix safe Nix direction

Lojix should become the default safe Nix invocation layer. Instead of agents or scripts emitting raw `nix build` / `nix flake check` commands directly for risky operations, they should submit a typed operation:

- operation kind: build, check, deploy, contained VM test, live deploy
- containment class: pure evaluation, local build, VM/QEMU, ephemeral cloud, production
- required builder features: for example `nixos-test` and `criomos-vm-testing`
- target resources: CPU, RAM, disk, network, secrets, live-node authority
- placement policy: eligible workers, trust class, limits, concurrency, cleanup

Lojix verifies the operation against cluster data and live capacity before emitting the raw Nix command. If no eligible worker exists, it fails closed instead of running on the caller's machine by accident.

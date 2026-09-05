# Upstream patterns

This is a carried account from `/root/upstream_patterns`, transcript thread `01a07139-d39e-7aa1-bd93-042e53210856`, completed at ordinal 259. The source check was read-only and was reported as checked against upstream sources on 2026-09-05. Observations and inferences are labelled.

## Module composition

**Observed upstream behavior:** Nix module evaluation resolves `imports` before option values. `lib/modules.nix` warns that referring to `config` from `imports` can recurse and recommends unconditional imports with `mkEnableOption` and `mkIf`. A caller-supplied `nixosSystem.specialArgs` value is available while imports are resolved, so a caller may use a static gate such as `lib.optional installVariant ./installer.nix`. `specialArgs` is fixed by the caller and cannot be configured from the module graph.

An option-driven feature is therefore normally imported unconditionally and gated in its definitions:

```nix
options.myFeature.enable = lib.mkEnableOption "…";
config = lib.mkIf config.myFeature.enable { … };
```

This preserves option declarations while gating resulting definitions, services, and packages. A static external gate omits the module and its declarations entirely. The distinction matters if a live-installer variant is selected before evaluation.

## Minimal USB and image interface

`installation-cd-minimal.nix` is a small non-graphical NixOS installation CD, but it composes `installation-cd-base` and `installation-device`. The base is a bootable image starting point with broad hardware support, EFI/USB setup, installation-device support, networking, documentation, SSH, and installer tooling. The stock installation-device profile intentionally carries permissive defaults: an autologin installer user, empty initial credentials, passwordless sudo, and permissive SSH settings. Those defaults require explicit review and override for a protected non-root TTY login.

**Observed current upstream interface:** modern NixOS supports `nixos-rebuild build-image --image-variant iso`, with images under `system.build.images`. A future graphical variant is represented as a separate image configuration or variant sharing a common layer; upstream's GNOME image uses `installation-cd-graphical-base.nix` and `installation-cd-graphical-gnome.nix`. The `nixos-generators` repository is archived/deprecated and points users to the upstream image interface. Whether the pinned LiGoldragon Nixpkgs revision in the current architecture exposes this interface remains unverified by the architecture witness.

## Closure, compression, and caching

The upstream ISO builder places the system closure in SquashFS. Current `isoImage.squashfsCompression` defaults to `zstd -Xcompression-level 19`; `null` disables SquashFS compression. `isoImage.compressImage` is a separate final-ISO compression switch and defaults to false. `includeSystemBuildDependencies` substantially increases image size and is intended for images that need local source/build inputs; it is not required for an ordinary networked installer.

**Inference:** stronger compression should reduce media size while increasing image-assembly CPU/time, with lower compression generally trading size for assembly speed. The witness found no upstream timings for this project, so the tradeoff must be measured on target hardware. Nix substitutes unchanged closure paths from configured binary caches. Changing image modules or compression reruns image assembly but does not imply rebuilding every unchanged package.

## Synthetic inventory and credentials

No direct upstream precedent was found for an inventory that automatically appends a deterministic synthetic node. **Inference:** create that node in the external inventory/pre-projection layer, pass the complete deterministic host set into Nix evaluation, and use the same merged view for peer inventory consumers. Define collision, name, and version rules; keep the default out of Lojix's hardcoded core. `specialArgs` can carry evaluation-time inputs, but it is not a replacement for domain inventory composition.

`users.users.<name>.openssh.authorizedKeys.keys` contains public keys; baking public keys into an ISO is acceptable when operators retain the matching private keys. NixOS password options expect salted hashes (`hashedPassword`, `hashedPasswordFile`, or initial variants); cleartext values are warned as world-readable in the Nix store. If “SOPs” means SOPS, an encrypted password hash still requires a boot-time decryption identity. `sops-nix` normally decrypts during activation, and `neededForUsers = true` is required when the hash must exist before user creation. The age key or SSH-derived identity must already be persisted and available early enough.

**Inference:** an installer's SSH host key is a temporary identity and must not become a target cluster host identity. A production host private key must not be embedded in the ISO. If initrd SSH is needed, use a dedicated key; upstream warns that private initrd keys may be exposed in the Nix store.

## Sources

- [`lib/modules.nix`](https://github.com/NixOS/nixpkgs/blob/master/lib/modules.nix)
- [`nixpkgs/flake.nix`](https://github.com/NixOS/nixpkgs/blob/master/flake.nix)
- [`installation-cd-minimal.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/installer/cd-dvd/installation-cd-minimal.nix)
- [`installation-cd-base.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/installer/cd-dvd/installation-cd-base.nix)
- [`installation-device.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/profiles/installation-device.nix)
- [`iso-image.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/installer/cd-dvd/iso-image.nix)
- [`make-squashfs.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/lib/make-squashfs.nix)
- [NixOS image manual](https://nixos.org/manual/nixos/stable/#sec-image-nixos-rebuild-build-image)
- [`nixos-generators`](https://github.com/nix-community/nixos-generators)
- [`users-groups.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/config/users-groups.nix)
- [`sshd.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/services/networking/ssh/sshd.nix)
- [`sops-nix README`](https://github.com/Mic92/sops-nix/blob/master/README.md)
- [`initrd-ssh.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/system/boot/initrd-ssh.nix)

---
description: CriomOS must be maintained: a host is declared, a fix placed, a system built or deployed, or a fact about a host asked for.
dependencies: [knowledge-lojix]
---

CriomOS is a flake that builds a whole host from a declaration. It holds no cluster or node name; a node name never decides whether a module is enabled, a Horizon role or capability field does. (`CriomOS/AGENTS.md:13-14`; the metal module reads `horizon.node.behavesAs` and `model`, `modules/nixos/metal/default.nix:33`.)

## From declaration to host

A cluster is declared as cluster data: nodes, users, domains and trust (`ClusterProposal`, `horizon-rs/lib/src/proposal.rs:30`). A node's `machine` has species `Metal` or `Pod` and, among other fields, an optional `model`, `chip_gen` and RAM (`horizon-rs/lib/src/machine.rs:15-40`, `species.rs:54-56`).

`horizon-rs` projects the cluster data into one view of one node. Lojix writes that view, the system tuple, the deployment shape and the secrets as generated flake inputs `horizon`, `system`, `deployment` and `secrets` (`lojix/src/bootstrap.rs:2724-2756`, `1196`). CriomOS declares them as stubs (`CriomOS/flake.nix:120-141`) and builds the output `nixosConfigurations.target` from `nixosSystem` with `specialArgs` `horizon system deployment inputs`, the `readOnlyPkgs` module, home-manager when home is included, and `nixosModules.criomos` (`flake.nix:278-300`). The `system` stub is deliberately throwing (`flake.nix:160`).

CriomOS-home builds the user environment, consumed as the input `criomos-home` pinned to a revision (`flake.nix:36`).

## Where a fix lands

A fix lands in the repository that owns the thing, and is deployed.

- A kernel parameter for one machine model or role: `boot.kernelParams = lib.concatLists [...]` in `modules/nixos/metal/default.nix:509`, with `optionals behavesAs.center [...]` blocks inside it (`:533`); the whole module applies under `mkIf behavesAs.bareMetal` (`:445`).
- A new machine model: one row in `modelFactsIndex` (`:61`). An unset or unlisted model throws at evaluation (`:116-125`).
- A system package: `environment.systemPackages` in the module that owns it (`metal/default.nix:640`; `criome.nix:180`). A new module is added to the `imports` of `modules/nixos/criomos.nix`.
- A unit: `systemd.services.<name>` in a module, gated by `mkIf` on a Horizon field (`metal/default.nix:551`, `569`, `582`).
- A fact that differs per cluster: the authored cluster declaration that `horizon-rs` consumes, not necessarily the `horizon-rs` implementation repository.
- A user program: CriomOS-home (`flake.nix:36`).

## Lojix: build, deploy, ask

Lojix evaluates the target's derivation with `nix eval --raw <flake>#<output>.drvPath` (`lojix/src/schema_runtime.rs:7742-7749`; bootstrap path `bootstrap.rs:2653-2662`) and builds it with `nix build --print-out-paths <drv>^*`, on an explicit builder when one is named (`bootstrap.rs:2666-2681`; daemon builds `schema_runtime.rs:6516`). A closure is copied to the target with `nix copy --to <store-uri>` (`schema_runtime.rs:6331-6336`).

Host activation on the target, by action (`schema_runtime.rs:6807-6825`):

- `SetBootProfile`: `nix-env -p /nix/var/nix/profiles/system --set <closure>`, then `<closure>/bin/switch-to-configuration boot`.
- `ActivateNow`: the same with `switch`.
- `TestActivation`: `switch-to-configuration test` alone.
- `ScheduleBootOnce`: a detached unit runs `nix-env --set`, `switch-to-configuration boot`, then `bootctl set-default <old entry>` and `bootctl set-oneshot <new entry>` (`schema_runtime.rs:6836-6852`; `bootstrap.rs:478-503`).
- `Evaluate` and `Realize` do not activate (`schema_runtime.rs:1236-1275`).

What is deployed is read with `lojix 'Query.ByNode.{ cluster node None }'`. The selector variants are `ByNode ByGeneration ByDeployment ByEventLog ByTestRun` (`signal-lojix/ethos/signal.ethos:115-117`); the answer lists the generations Lojix has recorded as live for the node, each with its slot, and the deployment records, with a state marker (`schema_runtime.rs:5096-5128`, `2592-2640`). These are Lojix's recorded deployment and generation state: they report what Lojix recorded, not a fresh attestation of what the host is running now. A flow needing a fact about a host asks Lojix this way and, where the current running system matters, checks the host itself. Deploy is `lojix-meta` `Deploy.Host`, a `HostDeployment` record (`meta-signal-lojix/ethos/signal.ethos:31`).

Rollback: `GenerationSlot::Rollback` exists as a slot name (`runtime_model.rs:146`, `adapters.rs:247`); in the inspected lojix revision (`src/`, see Inspected revisions in the gaps file) no code assigns it or acts on it, and no Lojix path found there rolls a host back. The one-shot boot sets the previous boot entry as the persistent default (`schema_runtime.rs:6708-6714`, script above): the previous entry remains the persistent default for a subsequent boot; this does not prove automatic recovery or reboot after failure. The Lojix store reset (`lojix/src/reconstruction.rs:92-163`) recreates a pre-v5 Lojix store and is not a rollback. Going back to an earlier system is a new deploy of an earlier closure (unverified as a tested path).

## Criome

Criome is a BLS12-381 signature authentication and attestation daemon: it holds a master key, an identity registry and delegation grants; verifies signatures; and signs attestations (`criome/ARCHITECTURE.md` TL;DR; `criome/src/master_key.rs:8`, `admission.rs:101`). It serves a working socket for clients and an owner-only meta socket (`criome/src/daemon.rs:214-270`, `CriomOS/modules/nixos/criome.nix` header). CriomOS runs it as a systemd service when `services.criome.enable` is set; the option is off by default and the module is imported for every node (`criome.nix:108`, `criomos.nix:28`). Its master key is generated on first start and kept in the daemon's state directory (`criome.nix` header).

`criome/ARCHITECTURE.md` states that `lojix-daemon` submits a request digest to the local criome and acts after a grant. Lojix source contains no reference to criome, so this participation is a documented design, unverified in code.

## What CriomOS does not use

The CriomOS guide records that hosts carry no `/etc/nixos` flake, so `microvm -l` reports empty; guests are read with `systemctl list-units 'microvm@*'` (`CriomOS/AGENTS.md:42`).

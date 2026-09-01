# CriomOS pin and materialization audit

The exact pushed CriomOS revision `93049a6e3eb7f66a23484402c96d835caa233b99` has the intended immutable dependency chain: CriomOS-home `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`, Chroma `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`, and chroma-emacs `119a231358cf69c16161812caf69fff4b726be5c`. The four repositories were clean and each `main@origin` matched the audited revision.

## Target composition

Using the existing materialized Zeus CompleteHost system, Horizon, deployment, and secrets inputs, the exact CriomOS target evaluated successfully. Its canonical output is `nixosConfigurations.target`; Home Manager is embedded because the materialized deployment has `includeHome = true`. The target includes both local users, Home's Emacs module, the same Emacs package for `programs.emacs` and `services.emacs`, the generated Home init artifact, Chroma in the Home package set, and a user `chroma-daemon` service. Nix closure metadata for the target Emacs package includes `emacs-chroma-theme`.

This is evaluated composition evidence. No CriomOS target was built or realized by this audit, so no claim is made about a new store realization or activation.

## Full-gate blockers

The exact no-build full check fails deterministically during Blueprint's auto-discovery of `/checks/agent-intercom-command-ownership`. Blueprint supplies standard check arguments but not `target`; the check's required function argument is therefore missing. CriomOS has an explicit target-aware invocation later in `flake.nix`, but Blueprint's earlier `blueprintOutputs.checks` evaluation fails first.

The check was introduced on 2026-08-19, before the Chroma/Home pin on 2026-08-23. The smallest behavior-preserving fix is to remove the target-dependent check from Blueprint's auto-discovered namespace and retain the explicit target-aware call. Making the check silently no-op when `target` is absent would weaken the gate.

A second, separate check-surface discrepancy is present: the embedded target Home activation package and CriomOS's independently exposed Home activation package evaluate to different output paths at this exact revision and input set. `home-activation-equivalence.nix` asserts equality, so this check cannot yet be called green. The target composition itself still contains the intended Emacs/Chroma closure; the discrepancy concerns the independently evaluated comparison surface. Home's standalone package set extends the shared `pkgs` with Home overlays, while CriomOS's target receives the raw shared package set; this is the likely owning boundary, not a proven final cause.

## Deployment boundary

The audit made only ordinary read-only Lojix queries. No owner-socket request, pin, realization, activation, deployment, or runtime mutation occurred. The current durable Lojix node history refers to source `d04f6dafce19b7b4f093c35716739f36d75973ba`; it contains no deployment of `93049a6e`. Existing history reports successful Evaluate and Realize operations for that older source and a later TestActivation failure at `CopyClosure / BuilderUnreachable`.

Disposition: the immutable pin chain and evaluated target composition are sound, but the source is not full-gate green. It should not be called deploy-ready until the Blueprint ownership defect and the activation-equivalence discrepancy are resolved, then evaluated and built through the configured remote gate. Any deployment still requires explicit authorization.

## Sources

- `witnesses/pinLockChain.md`
- `witnesses/materializedTarget.md`
- `witnesses/fullGate.md`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:154-170,218-267`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock:494-539,904-1017`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix:19-50`
- `/git/github.com/LiGoldragon/CriomOS/checks/agent-intercom-command-ownership/default.nix:1-44`
- `/git/github.com/LiGoldragon/CriomOS/home-activation-equivalence.nix:1-44`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:143-152,447-455,576-641`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:418-460`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix:32-91`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix:19,149-169`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix:14-20,109-111,684-716,792-803`
- `/git/github.com/LiGoldragon/chroma/flake.nix:72-94`
- `/git/github.com/LiGoldragon/chroma-emacs/flake.nix:10-27`
- Flow `01a02b4b`

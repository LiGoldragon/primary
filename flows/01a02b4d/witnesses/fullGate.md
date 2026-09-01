# CriomOS full-gate blockers

Method: read-only exact-revision evaluation with the materialized inputs from `materializedTarget.md`:

```text
nix flake check --no-build --no-update-lock-file --show-trace \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/horizon \
  --override-input deployment /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/deployment \
  --override-input secrets /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/secrets \
  'git+file:///git/github.com/LiGoldragon/CriomOS?rev=93049a6e3eb7f66a23484402c96d835caa233b99'
```

Observed: evaluation reaches the `checks` output and fails before project checks are constructed. Blueprint `lib/default.nix:766-771` imports every check under `/checks` with `systemArgs.${system} // { inherit pname; }`. `checks/agent-intercom-command-ownership/default.nix:1` requires `{ inputs, pkgs, target }`, but Blueprint does not provide `target`. The exact terminal error is `function 'anonymous lambda' called without required argument 'target'` at that file's first line.

Observed: CriomOS `flake.nix:166-170` forces `blueprintOutputs.checks` before the explicit project-check map is usable. CriomOS `flake.nix:218-220` does explicitly pass `target` to the same check, but that call is too late to prevent Blueprint's auto-discovery failure.

Observed: `jj show --summary fd0ef34ea311365f4b660dcdd5258657c23ed598` dates the target-dependent check introduction to 2026-08-19. The Chroma/Home pin commits `9bd84414ff4f892797a76e6d141b0f9f35f89153` and `93049a6e3eb7f66a23484402c96d835caa233b99` are dated 2026-08-23. The missing-`target` defect therefore predates this pin and is independent of Chroma–Emacs.

Recommendation: move this target-dependent check outside Blueprint's auto-discovered `/checks` namespace and keep one explicit call with `target`. An optional-target no-op would weaken the command-ownership gate and is not recommended.

Secondary check-surface observation: exact read-only evaluations of `homeConfigurations.li.activationPackage` and `independentHomeConfigurations.li.activationPackage` at the same immutable CriomOS revision and materialized inputs returned different Home Manager generation output paths. `home-activation-equivalence.nix:11-34` asserts these paths are equal, so the check would not be green if reached. The discrepancy is check/evaluation surface evidence, not evidence that the embedded target lacks Emacs or Chroma. Home standalone evaluation extends `inputs.pkgs.pkgs` with Home overlays (`CriomOS-home/flake.nix:454-455`), while CriomOS target evaluation supplies raw `inputs.pkgs.pkgs` (`CriomOS/flake.nix:154-156`); the owning resolution needs explicit review.

No build, deployment, activation, product edit, or runtime mutation was performed by this witness.

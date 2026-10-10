# CriomOS Home pin final review

Method: an isolated Jujutsu workspace at
`/home/li/wt/github.com/LiGoldragon/CriomOS/os-pin-final-review-acf06f` was
created with an empty review change whose sole parent is pushed CriomOS
`f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`. The source review compared its
three commits with their direct base `bc0dc048`; lock and Nix-source values
were read directly. Formatting used `nixfmt --check` on the two changed Nix
sources. Exact immutable evaluation and realization used the already
materialized Goldragon/Ouranos user-environment `system` and `horizon` inputs.
The realization set `max-jobs` to zero, disabled fallback, and selected the
configured `/etc/nix/machines` builders. No deployment, activation, or source
checkout was changed.

## Verdict

**Accept the reviewed pin change, subject only to the pre-existing repository
wide MS2130 eager-check limitation.** The three-commit stack is linear from
`bc0dc048`:

1. `1523375b` adds an evidence-bounded deployment-190 partial-activation
   gate. It requires separate ledger, profile/generation, generated-unit,
   embedded-store-reference, and live-process observations before repair,
   rollback, retry, or activation. It explicitly says the record contains none
   of those observations and authorizes none of those actions. That is
   actionable without claiming which surface changed.
2. `4d1309fb` pins CriomOS-home in both `flake.nix` and `flake.lock` to
   `d9bec96c54146c59b83c6cefde7a58b77d44a9a4`. The nested Home lock pins
   `wispr-flow-linux` to `033231a1255024447c6a4183c41f4ea9c1fa063f`; the
   obsolete path-based `wispr-flow-installer` input is absent from both the
   Home input list and root lock. The diff contains no unrelated lock change.
3. `f3d8b2ca` changes the ownership check's expected Home revision from the
   stale `8021ae5d4428343624920330098641f772c9eece` to the exact same
   `d9bec96c54146c59b83c6cefde7a58b77d44a9a4` selected by the root lock.
   Direct source/lock inspection therefore closes the prior mismatch.

Current CriomOS `main` is `bc0dc048`; the reviewed stack is a three-commit
descendant and has no merge conflict with that base. The pushed
`acf06f-home-pin` ref names the reviewed immutable tip.

## Gates

- `nixfmt --check flake.nix checks/lojix-ownership/default.nix` exited zero;
  the isolated workspace remained empty.
- Exact immutable evaluation of
  `homeConfigurations.li.activationPackage.drvPath` at `f3d8b2ca…`, with the
  materialized Goldragon/Ouranos user-environment `system` and `horizon`
  inputs, exited zero and retained a nonempty derivation result. Its store path
  is intentionally not recorded here.
- A separate exact immutable realization of
  `homeConfigurations.li.activationPackage` exited zero with
  `--builders '@/etc/nix/machines'`, `--option max-jobs 0`, and
  `--option fallback false`. Nix reports that configured builders use
  substitutes, so a cached realization was allowed and no local build was
  enabled.
- Exact immutable `nix flake check --no-build` reached the repository checks
  output and terminated nonzero at `MS2130 UVC patch must be reviewed for the
  selected kernel`. This is the known unrelated eager-check limitation; it is
  not changed or repaired by this review and prevents no claim of a fully green
  flake check.
- A subsequent focused ownership-check evaluation did not retain a terminal
  result: its redirected result was empty and the process had exited without a
  captured Nix diagnostic. It is not reported green. The ownership conclusion
  above is the direct source/lock witness, rather than an invented evaluation
  result.

## Sources

- Isolated review workspace parent and status: CriomOS Jujutsu workspace
  `os-pin-final-review-acf06f`.
- Reviewed source: `UPGRADES.md`, `flake.nix`, `flake.lock`, and
  `checks/lojix-ownership/default.nix` at
  `f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`.
- Materialized inputs:
  `/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system`
  and
  `/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon`.

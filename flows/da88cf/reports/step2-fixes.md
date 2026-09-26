# Step 2 fixes: codex-next handoff, flake registry, lojix-ownership

Subflow of da88cf, 2026-09-25, on ouranos. Both bookmarks are pushed. Neither is merged to main. Nothing was deployed, activated or restarted, and no live unit was touched.
At the main flow's instruction, the remaining builds and evaluations wait for "builds open". All Orchestrate locks (6977, 6978, 6989, 6990) are released.

| Repo | Bookmark | Base (remote main, verified) | Head (verified with `git ls-remote`) |
|---|---|---|---|
| CriomOS-home | `home-fixes-da88cf` | `4a9d85d7` | `d34cf68b1ab674f59ab099fc8f010dd5d8adb749` (on top of `a989826c`) |
| CriomOS | `criomos-fixes-da88cf` | `3e2cc8be` | `66aad7c9c583fdc2d41ac3b3bb71a060b1b6ee52` (on top of `7556680b`, then `9cafc0c6`) |

Workspaces: `~/wt/github.com/LiGoldragon/{CriomOS,CriomOS-home}/step2-fixes-da88cf`.

## Fix 1: codex-next declared handoff (CriomOS-home `a989826c`)

- **Files:** `modules/home/profiles/min/codex-next.nix` and `checks/codex-next/default.nix`.
- **Before:** the Unit section held only `Unit.Description`. The service had `Restart=on-failure` and `RestartSec=2s`, with no start limit, so it looped (NRestarts 42,845).
- **After:** a `recoveryUnit = "codex-remote-control-next-recovery.service"` binding, and this Unit section:
  ```nix
  Unit = {
    Description = "Codex Remote Control next server";
    Conflicts = [ recoveryUnit ];
    After = [ recoveryUnit ];
    StartLimitIntervalSec = 60;
    StartLimitBurst = 5;
  };
  ```
  The service section is unchanged. There is no ExecStartPre unlink, which follows f5a74e.
- **Check changes:** `checks/codex-next` now also asserts Conflicts, After, StartLimitIntervalSec = 60, StartLimitBurst = 5 and Restart = on-failure.
- **Evaluation through CriomOS (ouranos):** evaluated `nixosConfigurations.target.config.home-manager.users.li.systemd.user.services.codex-remote-control-next.Unit` with the Lojix-materialised ouranos complete-host inputs dated 2026-09-25 22:43. These were `system`, `horizon`, `deployment` and `secrets` under `/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host`, plus `--override-input criomos-home path:<Home workspace>`. The result:
  `{"After":["codex-remote-control-next-recovery.service"],"Conflicts":["codex-remote-control-next-recovery.service"],"Description":"Codex Remote Control next server",…,"StartLimitBurst":5,"StartLimitIntervalSec":60,…}`.
  The Home activation-package and toplevel drvPath evaluations were not run. The attempt failed on shell quoting before Nix started, and then the builds hold arrived.
- **Check build:** passed, offloaded:
  `building '…-codex-next-contract.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...`
  This build called `checks/codex-next` directly, through a scratchpad expression (`codex-next-check.nix`: `getFlake` of the workspace, nixpkgs x86_64-linux plus Home overlays). It did not go through `.#checks`, because the flake's checks set cannot be evaluated today (see Blocker A).

## Fix 2a: flake registry owner and repo (CriomOS `9cafc0c6`)

- **Files:** `modules/nixos/nix/client.nix`, a new `checks/flake-registry-shape/default.nix`, and one line in `flake.nix` that wires the check.
- **Before:** `owner`, `repo` and `type` came from `input.sourceInfo`, which has no owner or repo, so the registry entries were `{type="github"; rev=…}`.
- **After:** this is exactly the home-fixes.md shape. `flakeLock = fromJSON (readFile ../../../flake.lock)`, and `lockedInput name` resolves `root.inputs.<name>` to that node's `locked`. The entry uses `inherit (lockedInput name) type owner repo; rev = input.sourceInfo.rev or null;`.
- **Shape test:** `flake-registry-shape` evaluates `modules/nixos/nix` with a minimal horizon and takes the registry path from `nix.extraOptions`. In its builder it checks three things:
  - the ids are exactly brightness-ctl, criomos-home, home-manager and nixpkgs;
  - each entry's `{type,owner,repo}` equals the flake.lock node, read independently with jq, and `rev` is 40 hex characters;
  - `nix --store dummy:// --option flake-registry $registry registry list` prints nothing on stderr and lists `global flake:criomos-home github:LiGoldragon/CriomOS-home/<rev>`.
- **Check result:** **not yet evaluated or built.** It waits for "builds open", and it also sits behind Blocker A.

## Fix 2b: lojix-ownership derived from the locks (CriomOS `7556680b`)

- **File:** `checks/lojix-ownership/default.nix`.
- **Before:** the check hard-coded lojix `c4bba4fa` / `lojix-6.0.0`, Home `f652ba9a`, orchestrate `9070cbb8` and schema-rust `f3b45631`. On main `3e2cc8be` it fails immediately: `string "a67f5773…" is not equal to string "c4bba4fa…"`, witnessed by evaluating `github:LiGoldragon/CriomOS/3e2cc8be#checks.x86_64-linux`.
- **After:** there are no retyped revisions. The check now asserts that:
  - the root lock's lojix node is `github:LiGoldragon/lojix` and its rev equals `inputs.lojix.rev`;
  - `lib.getName lojix == "lojix"`;
  - the criomos-home node is `github:LiGoldragon/CriomOS-home` and its rev equals `inputs.criomos-home.rev`;
  - orchestrate (a root input) and schema-rust-source (a transitive node) have the same source and rev in the CriomOS and Home locks.

  The Home-does-not-own-lojix assertions are unchanged.
- **Check result:** with my change, evaluation gets past every lock assertion. It then stops at the pre-existing Home failure in Blocker A (line 206, `hasAttr "lojix-ownership" homeChecks`). **Not built.**

## Fix 2c: Blueprint check fix (applied on the main flow's later instruction)

`blueprint-check-fix.md` appeared after the first push, and the main flow directed that its diffs be applied, with no builds.

- **CriomOS `66aad7c9` (os-fix):** removed the Home-revision assertion, as the main flow ruled. The line removed is `assert (rootLocked "criomos-home").rev == inputs.criomos-home.rev;`, which is 2b's version of the old `expectedHomeRevision` assert. That constant was already deleted in 2b.
  Kept: the source-identity assertion on the Home lock node, and the lock-derived lojix, orchestrate and schema-rust assertions.
- **CriomOS-home `d34cf68b` (home-fixB):**
  - Moved the nine owned checks from `checks/` to `gates/`: agent-intercom, ai-agent-launch-orchestration, claude-desktop-declared-cli, claude-desktop-egl-linkage, claude-desktop-launcher-linkage, codex-remote, codex-remote-control (with initialize.py), codex-remote-control-vm, and desktop-app-support (with its two .cjs files).
  - Deleted `ownedCheckNames` and its `removeAttrs`, rewrote the comment, and repointed the nine explicit `checkPkgs.callPackage` calls to `./gates/…`.
  - Changed `chatgpt-voice-niri-rule` to read `.action.spawn`.

  The report's diff was made against Home `5f14f9d`. Against `4a9d85d7`, hunk 5 (the path repointing) failed to apply because of context drift, so it was applied by path substitution instead. The final `flake.nix` diff matches diff B line for line. The sibling-relative references `../desktop-app-support/*.cjs` and `../codex-remote-control/initialize.py` still resolve, because those directories moved together. No other file references the moved paths.
- **Not evaluated:** evaluation and builds wait for "builds open".

With these commits, Blocker A below should be resolved on the bookmarks, but that is unverified. The Blueprint report says the Home set is clean only up to `herdr-toast-delivery`, and it is untested beyond that.

## Blockers

- **A. The Home checks key set cannot be evaluated (this is pre-existing).** `nix eval .#checks.x86_64-linux --apply builtins.attrNames` fails with `Refusing to evaluate package 'platform-tools_r37.0.1-linux.zip' … unfree`. The same error occurs in two places:
  - in CriomOS, with only a system override, where CriomOS's Blueprint auto-discovers `checks/lojix-ownership` and forces `inputs.criomos-home.checks.x86_64-linux`;
  - in CriomOS-home `4a9d85d7` standalone, with `--override-input system`. There, even `.#checks.x86_64-linux.codex-next` fails.

  Cause, inferred: `modules/home/profiles/min/default.nix:370` uses `androidenv.androidPkgs.platform-tools`. Its `src` is named `platform-tools`, which is not in Home `flake.nix` `ownedUnfreeNames` (that list has `android-sdk-platform-tools`), and the check package set lacks the predicate. Until that is fixed, or blueprint-check-fix.md lands, `.#checks` cannot succeed and lojix-ownership cannot be built. The fix is outside this brief.
- **B. Bare evaluation of CriomOS checks throws `no system input was provided`, by design.** The evaluation needs `--override-input system` (Lojix `~/.cache/lojix/system/x86_64-linux`).
- **C. Waiting for "builds open":** the Home `.#checks` attrNames (with a system override), the Home codex-next check through `.#checks`, the Home drvPath and toplevel evaluations, the builds of flake-registry-shape and lojix-ownership, and the `.#checks` attrNames evaluation. No build of mine was queued when the hold arrived.

## Sources

- `flows/da88cf/reports/home-fixes.md`; `flows/f5a74e/reports/codex-next-unit.md`.
- Commits above, from `jj diff --stat` and `git ls-remote` on both origins.
- Evaluation traces: scratchpad `step2-fixes/checks-eval-trace.txt` and `step2-fixes/codex-next-build.log`.
- Lojix-materialised inputs: `/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/*` (read only).

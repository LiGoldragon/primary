# Blueprint aggregate-check defect: CriomOS and CriomOS-home

Scope: read-only. Scratch clones of each repo's remote `main` were made in the subflow scratchpad: CriomOS `d193baf`, CriomOS-home `5f14f9d`. The diffs below were applied only to scratch worktrees, and nothing was committed. Evaluations ran on ouranos with the materialized Lojix inputs under `/var/lib/lojix/generated-inputs/goldragon/ouranos/`: `complete-host` (2026-09-12) for CriomOS and `user-environment` (2026-09-24) for Home. The main flow stopped the work before the Home fix finished evaluating.

## The "target" claim is stale

A bare `nix flake check --no-build` or `nix eval .#checks.x86_64-linux` on either repo fails with `CriomOS: no system input was provided` or `CriomOS-home: no system input was provided`. This is by design: the `system` and `horizon` inputs are stubs that throw until Lojix materializes them.

The missing-`target` defect was real (`function 'anonymous lambda' called without required argument 'target'`, from `checks/agent-intercom-command-ownership`, which had been added in fd0ef34 on 2026-08-19). Commit 4c3da15 fixed it on 2026-08-23 by moving that check to `gates/agent-intercom-command-ownership.nix`, which `flake.nix` calls explicitly with `target`. Current main has no `checks/` file that takes `target`.

## How Blueprint fails the aggregate

Blueprint (56131e8, `lib/default.nix:766`) imports every `checks/<name>/default.nix` with its own `systemArgs` and passes the result through `filterPlatforms`, which reads `x.meta` on each value. CriomOS's own `filterAttrs isDerivation` forces each value as well. So one eval-time `assert` or `throw` in any check file makes `attrNames checks` fail for the whole set. Removing an attribute later with `removeAttrs` does not help, because Blueprint has already forced it.

## What fails today

1. **CriomOS-home**: `checks.x86_64-linux` fails with `Refusing to evaluate package 'platform-tools_r37.0.1-linux.zip' ... unfree license`. The source is `checks/ai-agent-launch-orchestration/default.nix:61`. Blueprint auto-imports that check with Blueprint's narrowly unfree-permitted `pkgs`, although `flake.nix` already lists it in `ownedCheckNames` and calls it again explicitly with `checkPkgs`. Adding `"platform-tools"` to `ownedUnfreeNames` only moves the error to `aspell-dict-en-science` (tested), so widening the name list is whack-a-mole. All nine `ownedCheckNames` entries have this shape.
2. **CriomOS-home, second failure** (hidden behind the first): `checks/chatgpt-voice-niri-rule/default.nix:42` fails with `attribute 'command' missing`. niri-flake represents `a.spawn` as `{ spawn = [ ... ]; }`, which a probe evaluation confirmed. This check has been broken since it was added in e17ec33 (2026-09-18), with the niri-flake revision unchanged since then.
3. **CriomOS**: `checks.x86_64-linux` fails with `string '"478b4ea0..."' is not equal to string '"f652ba9a..."'` at `checks/lojix-ownership/default.nix:188`, the line `assert rootLock.nodes."criomos-home".locked.rev == expectedHomeRevision`. This constant duplicates the pin in `flake.nix`. It was hand-bumped on every Home pin until 36653a1 and has been stale since 63edfc9 (2026-09-12), which is 11 Home pins ago. With that line removed, CriomOS fails on item 1: `lojix-ownership` and `flow-id-home` read `inputs.criomos-home.checks.${system}`, so every Home aggregate failure also fails CriomOS.

## Since when

- CriomOS 63edfc9 (2026-09-12): fails on the stale Home revision.
- CriomOS 36653a1 (2026-09-12): fails on the Home `platform-tools` error.
- CriomOS-home: fails on the `platform-tools` error at 0176de5 (2026-09-11), caffe9a (2026-09-11; that commit's predicate addition did not cover the archive's name), f652ba9 (2026-09-12), 09cace84 (2026-09-23) and main. No passing revision was found within the four-candidate budget. The nixpkgs lock has not changed over this range.

## Options

**Home**

- **A.** Extend `ownedUnfreeNames`. This keeps the files where they are, but the tested result is a chain of unfree names that never converges. Rejected.
- **B (recommended).** Move the nine owned checks from `checks/` to `gates/`, which is the precedent CriomOS set in 4c3da15. Keep their explicit `checkPkgs.callPackage` calls and delete `ownedCheckNames` and its `removeAttrs`. This keeps every check, with the package set it was designed for. It removes the dead double import and the ineffective removal list. `flake.nix` stays an index. The relative paths keep the same depth, and `codex-remote-control-vm`'s `../codex-remote-control/initialize.py` still resolves because both directories move together.
- Separately, fix item 2 with `.action.spawn`.

**CriomOS**

- **A.** Bump `expectedHomeRevision` to `478b4ea0`. This keeps the exact-pin witness, but the check breaks again on the next Home pin.
- **B (recommended).** Delete the Home-revision constant and its assert. This removes only a duplicate of `flake.nix`'s pin, which the lock already enforces. The check's actual subject stays intact: there is no Lojix in the Home lock, packages or apps; the orchestrate and schema revisions are shared; and the Lojix package is pinned.
- CriomOS also needs a re-pin to a Home revision that contains the Home fix.

## Test status

- **CriomOS diff**: evaluated. The stale-revision error is gone, and evaluation proceeds to the Home error in item 1, which CriomOS inherits.
- **Home diff B plus `.action.spawn`**: partly evaluated.
  - The `platform-tools` and `command` errors are gone.
  - Evaluation reached `checks/herdr-toast-delivery`, which needs an import-from-derivation build (`herdr-config.toml`). That build was realized (fetched from Prometheus), and evaluation continued. The main flow then stopped it before `attrNames` returned.
  - **UNTESTED**: whether the Home `checks` set is clean after the fix. Any further failing check in alphabetical order after `herdr-toast-delivery` is unknown.
  - **UNTESTED**: `nix flake check --no-build` on either fixed tree.

## Diff: CriomOS

```diff
diff --git a/checks/lojix-ownership/default.nix b/checks/lojix-ownership/default.nix
index bfae02f..3645ba2 100644
--- a/checks/lojix-ownership/default.nix
+++ b/checks/lojix-ownership/default.nix
@@ -4,7 +4,6 @@ let
   system = pkgs.stdenv.hostPlatform.system;
   expectedRevision = "c4bba4fa12408c39ff745b0773468cd32a74403f";
   expectedPackageName = "lojix-6.0.0";
-  expectedHomeRevision = "f652ba9ae6b24b7e946e60e98acc270280beb774";
   expectedOrchestrateRevision = "9070cbb8717813b127e448dd5a43a2095daf7d1b";
   expectedSchemaRustRevision = "f3b4563163dd11ba1cbbcca8081701ab7830b8f5";
   rootLock = builtins.fromJSON (builtins.readFile ../../flake.lock);
@@ -185,7 +184,6 @@ let
 in
 assert rootLock.nodes.lojix.locked.rev == expectedRevision;
 assert lojix.name == expectedPackageName;
-assert rootLock.nodes."criomos-home".locked.rev == expectedHomeRevision;
 assert !(builtins.hasAttr "lojix" (rootLock.nodes."criomos-home".inputs or { }));
 assert !(builtins.hasAttr "lojix" homeLock.nodes);
 assert rootLock.nodes.orchestrate.locked.rev == expectedOrchestrateRevision;
```

## Diff: CriomOS-home (renames plus `flake.nix` and niri check)

```diff
diff --git a/checks/chatgpt-voice-niri-rule/default.nix b/checks/chatgpt-voice-niri-rule/default.nix
index a0245a7..74424e3 100644
--- a/checks/chatgpt-voice-niri-rule/default.nix
+++ b/checks/chatgpt-voice-niri-rule/default.nix
@@ -39,7 +39,7 @@ let
   chatgptRule = lib.findFirst (
     rule: builtins.any (match: (match.app-id or "") == "^chatgpt$") rule.matches
   ) null settings.window-rules;
-  microphoneMuteBinding = settings.binds."XF86AudioMicMute".action.command;
+  microphoneMuteBinding = settings.binds."XF86AudioMicMute".action.spawn;
 in
 assert lib.assertMsg (chatgptRule != null)
   "ChatGPT must have a Niri window rule";
diff --git a/flake.nix b/flake.nix
index 300cbf7..741e1a0 100644
--- a/flake.nix
+++ b/flake.nix
@@ -518,17 +518,6 @@
         "x86_64-linux"
         "aarch64-linux"
       ];
-      ownedCheckNames = [
-        "agent-intercom"
-        "desktop-app-support"
-        "ai-agent-launch-orchestration"
-        "claude-desktop-declared-cli"
-        "claude-desktop-egl-linkage"
-        "claude-desktop-launcher-linkage"
-        "codex-remote-control"
-        "codex-remote-control-vm"
-        "codex-remote"
-      ];
       agentIntercomSupported = system: lib.elem system agentIntercomSystems;
       desktopAppSupported =
         system:
@@ -565,8 +554,10 @@
             value = true;
           }) (builtins.attrNames (projectPackages.${system} or { }))
         );
-      # Blueprint imports every check before it can inspect platform metadata.
-      # Select desktop-app checks from the actual owned package outputs rather
+      # Blueprint imports every check under ./checks with its own package set
+      # before this flake can filter it. Checks that need the Home package set
+      # live under ./gates and are called explicitly in projectChecks below.
+      # Select package checks from the actual owned package outputs rather
       # than a shared architecture predicate.
       derivationChecks = builtins.mapAttrs (
         _system: checks:
@@ -575,7 +566,7 @@
             name: value:
             lib.isDerivation value
             && (!lib.hasPrefix "pkgs-" name || builtins.hasAttr name (packageCheckNames _system))
-          ) (builtins.removeAttrs checks ownedCheckNames)
+          ) checks
         else
           blueprintGeneratedChecks _system
       ) (bp.checks or { });
@@ -648,7 +639,7 @@
           main-contract-pins = checkPkgs.callPackage ./checks/main-contract-pins {
             inherit inputs;
           };
-          codex-remote = checkPkgs.callPackage ./checks/codex-remote { };
+          codex-remote = checkPkgs.callPackage ./gates/codex-remote { };
           codex-artifact-gateway = checkPkgs.callPackage ./checks/codex-artifact-gateway { };
           codex-artifact-gateway-module = checkPkgs.callPackage ./checks/codex-artifact-gateway-module {
             inherit inputs;
@@ -664,30 +655,30 @@
           };
         }
         // lib.optionalAttrs (agentIntercomSupported _system) {
-          agent-intercom = checkPkgs.callPackage ./checks/agent-intercom { inherit inputs; };
+          agent-intercom = checkPkgs.callPackage ./gates/agent-intercom { inherit inputs; };
         }
         // lib.optionalAttrs (desktopAppSupported _system) {
-          claude-desktop-declared-cli = checkPkgs.callPackage ./checks/claude-desktop-declared-cli {
+          claude-desktop-declared-cli = checkPkgs.callPackage ./gates/claude-desktop-declared-cli {
             inherit inputs;
           };
-          claude-desktop-launcher-linkage = checkPkgs.callPackage ./checks/claude-desktop-launcher-linkage {
+          claude-desktop-launcher-linkage = checkPkgs.callPackage ./gates/claude-desktop-launcher-linkage {
             inherit inputs;
           };
-          claude-desktop-egl-linkage = checkPkgs.callPackage ./checks/claude-desktop-egl-linkage {
+          claude-desktop-egl-linkage = checkPkgs.callPackage ./gates/claude-desktop-egl-linkage {
             inherit inputs;
           };
-          desktop-app-support = checkPkgs.callPackage ./checks/desktop-app-support {
+          desktop-app-support = checkPkgs.callPackage ./gates/desktop-app-support {
             inherit inputs;
           };
         }
         // lib.optionalAttrs (_system == "x86_64-linux") {
-          ai-agent-launch-orchestration = checkPkgs.callPackage ./checks/ai-agent-launch-orchestration {
+          ai-agent-launch-orchestration = checkPkgs.callPackage ./gates/ai-agent-launch-orchestration {
             inherit inputs;
           };
-          codex-remote-control = checkPkgs.callPackage ./checks/codex-remote-control {
+          codex-remote-control = checkPkgs.callPackage ./gates/codex-remote-control {
             inherit inputs;
           };
-          codex-remote-control-vm = checkPkgs.callPackage ./checks/codex-remote-control-vm {
+          codex-remote-control-vm = checkPkgs.callPackage ./gates/codex-remote-control-vm {
             inherit inputs;
           };
         }
diff --git a/checks/agent-intercom/default.nix b/gates/agent-intercom/default.nix
similarity index 100%
rename from checks/agent-intercom/default.nix
rename to gates/agent-intercom/default.nix
diff --git a/checks/ai-agent-launch-orchestration/default.nix b/gates/ai-agent-launch-orchestration/default.nix
similarity index 100%
rename from checks/ai-agent-launch-orchestration/default.nix
rename to gates/ai-agent-launch-orchestration/default.nix
diff --git a/checks/claude-desktop-declared-cli/default.nix b/gates/claude-desktop-declared-cli/default.nix
similarity index 100%
rename from checks/claude-desktop-declared-cli/default.nix
rename to gates/claude-desktop-declared-cli/default.nix
diff --git a/checks/claude-desktop-egl-linkage/default.nix b/gates/claude-desktop-egl-linkage/default.nix
similarity index 100%
rename from checks/claude-desktop-egl-linkage/default.nix
rename to gates/claude-desktop-egl-linkage/default.nix
diff --git a/checks/claude-desktop-launcher-linkage/default.nix b/gates/claude-desktop-launcher-linkage/default.nix
similarity index 100%
rename from checks/claude-desktop-launcher-linkage/default.nix
rename to gates/claude-desktop-launcher-linkage/default.nix
diff --git a/checks/codex-remote-control-vm/default.nix b/gates/codex-remote-control-vm/default.nix
similarity index 100%
rename from checks/codex-remote-control-vm/default.nix
rename to gates/codex-remote-control-vm/default.nix
diff --git a/checks/codex-remote-control/default.nix b/gates/codex-remote-control/default.nix
similarity index 100%
rename from checks/codex-remote-control/default.nix
rename to gates/codex-remote-control/default.nix
diff --git a/checks/codex-remote-control/initialize.py b/gates/codex-remote-control/initialize.py
similarity index 100%
rename from checks/codex-remote-control/initialize.py
rename to gates/codex-remote-control/initialize.py
diff --git a/checks/codex-remote/default.nix b/gates/codex-remote/default.nix
similarity index 100%
rename from checks/codex-remote/default.nix
rename to gates/codex-remote/default.nix
diff --git a/checks/desktop-app-support/claude-desktop-asar-contract.cjs b/gates/desktop-app-support/claude-desktop-asar-contract.cjs
similarity index 100%
rename from checks/desktop-app-support/claude-desktop-asar-contract.cjs
rename to gates/desktop-app-support/claude-desktop-asar-contract.cjs
diff --git a/checks/desktop-app-support/claude-desktop-runtime-contract.cjs b/gates/desktop-app-support/claude-desktop-runtime-contract.cjs
similarity index 100%
rename from checks/desktop-app-support/claude-desktop-runtime-contract.cjs
rename to gates/desktop-app-support/claude-desktop-runtime-contract.cjs
diff --git a/checks/desktop-app-support/default.nix b/gates/desktop-app-support/default.nix
similarity index 100%
rename from checks/desktop-app-support/default.nix
rename to gates/desktop-app-support/default.nix
```

## Sources

- Scratch clones and worktrees: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/blueprint-fix/{CriomOS,CriomOS-home,os-fix,home-fixB,os-36653a1,os-63edfc9,home-*}`
- Diff files: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/blueprint-fix/os-fix.diff`, `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/blueprint-fix/home-fixB.diff`
- Evaluation traces: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/blueprint-fix/os-fix-trace2.txt`, `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/blueprint-fix/fixB-noifd.txt`
- Earlier target-claim evidence: `/home/li/primary/flows/01a02b4d/reports/criomosPinAudit.md`, `/home/li/primary/flows/01a02b4d/witnesses/fullGate.md`
- Blueprint `lib/default.nix:160-168,766-778` (rev 56131e8)

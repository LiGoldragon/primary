# Messenger binding guard: fix ready on a branch, built, not activated

Subflow of 9fb0ad, 2026-10-03, on ouranos. Nothing was activated, merged or
touched under `~/.local/bin`. CriomOS-home main is still `0025894f`.

## What the guard protects against (its own words)

`modules/home/profiles/min/messenger-clj.nix`, history (`git log -p`):

- `dadb9ac9` "Home-manage messenger compatibility bindings" (Sep 29) puts `messenger-clj` and the ten `hm-*` under Home ownership with `force = true`, with the comment "These paths predate Home ownership. They are first on PATH, so leave no old shim in front of the immutable package that Home installs." Because `force` turns off Home Manager's own collision check, it adds `retireProvenLegacyMessengerBindings`, which lets an existing binding through only if it resolves into the 0.2.5 package (`p8mz1msm…-messenger-clj-0.2.5`), and otherwise prints "refusing to replace non-legacy messenger binding".
- `441f079e` "Recognize literal legacy messenger shim chain" narrows that test to the exact chain `~/.local/bin/<cmd>` → `~/.local/libexec/messenger-clj/bin/<cmd>`, `libexec/messenger-clj` → the 0.2.5 package.
- `0025894f` "Admit witnessed Messenger predecessor" (Sep 30): "The profile already contains this exact Home-managed 0.2.8 generation. Admit it during this one migration only by its immutable generated-files root; arbitrary local links remain rejected." The pin is `9ajs6aji…-home-manager-files`.

So its purpose is this: `force` must not clobber a binding that Home does not own. It replaces only the proven legacy shims and Home's own earlier links, and refuses any other local file or link. The defect is that "Home's own" was written as one pinned store path, so the guard stopped admitting Home's own links from the first generation after that one (1039, `ddp041ij…`). That is my reading, from the script and the live links in `reports/deployment.md`.

## The fix chosen, and why it is not the brief's sketch

The brief's sketch was to admit links into `$oldGenPath/home-files` or into the current profile's files. I implemented a cleaner version: **drop `force` and the custom step, and let Home Manager's own `checkLinkTargets` guard the bindings.** Reasons:

- Without `force`, HM's `check-link-targets.sh` does exactly what the guard intends. A link whose target matches `/nix/store/*-home-manager-files/*` is Home's and gets replaced. A foreign file, or a foreign link whose content differs, is a collision, and activation exits 1. This is keyed on Home Manager generations as a class, not on one pinned path. It needs no `$oldGenPath` bookkeeping. Note that the "current profile" half of the sketch would not have worked: `writeBoundary` sets the profile to the *new* generation before this step runs.
- `force` existed only for the one-time 0.2.5 shim migration. That migration finished on ouranos (the live links are Home's, and `~/.local/libexec/messenger-clj` now points at 0.2.8, not 0.2.5). Keeping a legacy branch for it would be a compatibility branch.
- Consequence: a host that still had the raw 0.2.5 shim chain would now get HM's "Existing file … would be clobbered" refusal instead of a silent replacement. It fails safe and loses nothing. I did not survey other hosts.
- A remaining HM behavior to know about: a *dangling* foreign link is not checked by HM and is replaced. With `HOME_MANAGER_BACKUP_EXT` set (`-b`), a foreign regular file would be moved to `.backup` instead of refused. Activations here run `activate` directly, without it.
- I left the same class of latent bug alone, because it is out of scope: `adoptHerdrConfig` (`herdr.nix`) admits the live Herdr link by one pinned config path (`grj6d8ly…`). It is a no-op today because every built generation carries that same config, and it will refuse when the Herdr config changes.

The check `checks/messenger-clj-package` now asserts `!force` on all eleven bindings and that the retire step is absent. It then runs HM's generated `checkLinkTargets` on four homes: absent (pass), links into a HM generated-files root (pass), foreign regular file (must refuse), foreign differing symlink (must refuse).

## Diff (`9fb0ad-messenger-guard`, f6cd3541)

```diff
diff --git a/checks/messenger-clj-package/default.nix b/checks/messenger-clj-package/default.nix
index 98bd058421..8dd9d78ad6 100644
--- a/checks/messenger-clj-package/default.nix
+++ b/checks/messenger-clj-package/default.nix
@@ -14,8 +14,6 @@
     "hm-heartbeat-state"
   ];
   managedCommands = [ "messenger-clj" ] ++ compatibilityCommands;
-  legacyMessengerClj = "/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5";
-  predecessorManagedFiles = "/nix/store/9ajs6aji25akz3dfrzpffj7j4kpqjjzv-home-manager-files";
   configuration = inputs.home-manager.lib.homeManagerConfiguration {
     inherit pkgs;
     extraSpecialArgs = {
@@ -37,16 +35,19 @@
     ];
   };
   managedFiles = configuration.config.home.file;
-  retireLegacyBindings =
-    configuration.config.home.activation.retireProvenLegacyMessengerBindings.data;
+  homeFiles = configuration.config.home-files;
+  checkLinkTargets = configuration.config.home.activation.checkLinkTargets.data;
 in
+# The bindings carry no force: Home Manager's own collision check guards them,
+# and no activation step of this module bypasses it.
 assert builtins.all (
   command:
   let
     file = managedFiles.".local/bin/${command}";
   in
-  file.source == "${messengerClj}/bin/${command}" && file.force
+  file.source == "${messengerClj}/bin/${command}" && !file.force
 ) managedCommands;
+assert !(configuration.config.home.activation ? retireProvenLegacyMessengerBindings);
 pkgs.runCommand "messenger-clj-home-package" { } ''
   set -eu
   test -x ${messengerClj}/bin/messenger-clj
@@ -57,56 +58,45 @@
   # evaluated Home-managed PATH bindings.
   test ${toString (builtins.length compatibilityCommands)} -eq 10
 
-  run_retirement_guard() {
-    HOME="$1" ${pkgs.bash}/bin/bash -eu -c ${pkgs.lib.escapeShellArg retireLegacyBindings}
+  # Run Home Manager's generated checkLinkTargets step against a home, as
+  # activation runs it before linkGeneration.
+  generation="$TMPDIR/generation"
+  mkdir -p "$generation"
+  ln -s ${homeFiles} "$generation/home-files"
+  run_link_check() {
+    HOME="$1" newGenPath="$generation" \
+      PATH=${pkgs.lib.makeBinPath [ pkgs.bash pkgs.coreutils pkgs.findutils pkgs.diffutils pkgs.gettext pkgs.ncurses ]} \
+      ${pkgs.bash}/bin/bash -eu -c ${pkgs.lib.escapeShellArg checkLinkTargets}
   }
 
   absent_home="$TMPDIR/absent"
   mkdir -p "$absent_home/.local/bin"
-  run_retirement_guard "$absent_home"
-
-  legacy_home="$TMPDIR/legacy"
-  mkdir -p "$legacy_home/.local/bin" "$legacy_home/.local/libexec"
-  ln -s ${legacyMessengerClj} "$legacy_home/.local/libexec/messenger-clj"
-  ${pkgs.lib.concatMapStringsSep "\n  " (
-    command:
-    "ln -s \"$legacy_home/.local/libexec/messenger-clj/bin/${command}\" \"$legacy_home/.local/bin/${command}\""
-  ) managedCommands}
-  run_retirement_guard "$legacy_home"
-
-  # The known preceding Home generation is safe to replace only when both
-  # the generated-files link and its resolved package match exactly.
+  run_link_check "$absent_home"
+
+  # The bindings of a preceding Home generation, whichever it was, are Home's
+  # own: they link into a Home Manager generated-files root.
   predecessor_home="$TMPDIR/predecessor"
   mkdir -p "$predecessor_home/.local/bin"
-  ${pkgs.lib.concatMapStringsSep "
-  " (
+  ${pkgs.lib.concatMapStringsSep "\n  " (
     command:
-    "ln -s ${predecessorManagedFiles}/.local/bin/${command} \"$predecessor_home/.local/bin/${command}\""
+    "ln -s ${homeFiles}/.local/bin/${command} \"$predecessor_home/.local/bin/${command}\""
   ) managedCommands}
-  run_retirement_guard "$predecessor_home"
-
-  predecessor_wrong_root_home="$TMPDIR/predecessor-wrong-root"
-  mkdir -p "$predecessor_wrong_root_home/.local/bin"
-  ln -s /tmp/not-the-generated-files-root "$predecessor_wrong_root_home/.local/bin/messenger-clj"
-  if run_retirement_guard "$predecessor_wrong_root_home"; then
-    echo "the retirement guard accepted a non-predecessor generated-files link" >&2
-    exit 1
-  fi
+  run_link_check "$predecessor_home"
 
   foreign_home="$TMPDIR/foreign"
   mkdir -p "$foreign_home/.local/bin"
   printf foreign > "$foreign_home/.local/bin/hm-send"
-  if run_retirement_guard "$foreign_home"; then
-    echo "the retirement guard accepted a foreign messenger binding" >&2
+  if run_link_check "$foreign_home"; then
+    echo "the link check accepted a foreign messenger binding" >&2
     exit 1
   fi
 
   foreign_link_home="$TMPDIR/foreign-link"
-  mkdir -p "$foreign_link_home/.local/bin" "$foreign_link_home/.local/libexec"
-  ln -s ${legacyMessengerClj} "$foreign_link_home/.local/libexec/messenger-clj"
-  ln -s /tmp/not-a-messenger-binding "$foreign_link_home/.local/bin/hm-send"
-  if run_retirement_guard "$foreign_link_home"; then
-    echo "the retirement guard accepted a foreign messenger symlink" >&2
+  mkdir -p "$foreign_link_home/.local/bin"
+  printf '#!/bin/sh\n' > "$TMPDIR/not-a-messenger-binding"
+  ln -s "$TMPDIR/not-a-messenger-binding" "$foreign_link_home/.local/bin/hm-send"
+  if run_link_check "$foreign_link_home"; then
+    echo "the link check accepted a foreign messenger symlink" >&2
     exit 1
   fi
   touch "$out"
diff --git a/modules/home/profiles/min/messenger-clj.nix b/modules/home/profiles/min/messenger-clj.nix
index c8d0bf273b..8ba95be1fa 100644
--- a/modules/home/profiles/min/messenger-clj.nix
+++ b/modules/home/profiles/min/messenger-clj.nix
@@ -22,44 +22,20 @@
     "hm-heartbeat-state"
   ];
   managedCommands = [ "messenger-clj" ] ++ compatibilityCommands;
-  legacyMessengerPackage = "/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5";
-  # The profile already contains this exact Home-managed 0.2.8 generation.
-  # Admit it during this one migration only by its immutable generated-files
-  # root; arbitrary local links remain rejected.
-  predecessorManagedFiles = "/nix/store/9ajs6aji25akz3dfrzpffj7j4kpqjjzv-home-manager-files";
 in
 {
   config = lib.mkIf (sizeAtLeast "Min" && system == "x86_64-linux") {
     home = {
       packages = [ messengerCljPackage ];
 
-      # These paths predate Home ownership.  They are first on PATH, so leave
-      # no old shim in front of the immutable package that Home installs.
+      # Home owns these PATH-first bindings. Home Manager's own
+      # checkLinkTargets step replaces a link into any Home Manager generation
+      # and refuses a differing file or link of any other origin, so no shim
+      # stands in front of the package and nothing foreign is clobbered.
       file = lib.genAttrs (map (command: ".local/bin/${command}") managedCommands) (path: {
         source = "${messengerCljPackage}/bin/${lib.removePrefix ".local/bin/" path}";
         executable = true;
-        force = true;
       });
-
-      activation.retireProvenLegacyMessengerBindings = lib.hm.dag.entryBefore [ "linkGeneration" ] ''
-        set -eu
-        legacy_package=${lib.escapeShellArg legacyMessengerPackage}
-        legacy_root="$HOME/.local/libexec/messenger-clj"
-        predecessor_files=${lib.escapeShellArg predecessorManagedFiles}
-        for command in ${lib.escapeShellArgs managedCommands}; do
-          target="$HOME/.local/bin/$command"
-          if [ -e "$target" ] || [ -L "$target" ]; then
-            if [ -L "$target" ] \
-              && [ "$(readlink "$target")" = "$predecessor_files/.local/bin/$command" ]; then
-              continue
-            fi
-            if [ ! -L "$legacy_root" ] || [ "$(readlink "$legacy_root")" != "$legacy_package" ] || [ ! -L "$target" ] || [ "$(readlink "$target")" != "$legacy_root/bin/$command" ]; then
-              echo "refusing to replace non-legacy messenger binding: $target" >&2
-              exit 1
-            fi
-          fi
-        done
-      '';
     };
   };
 }
```

## Branches and commits (all pushed, none merged)

The same patch sits on each base of the activation plan. The guard file and its check are byte-identical on all four bases (sha1 of each compared).

| Branch | Commit | Parent | Role |
|---|---|---|---|
| `9fb0ad-messenger-guard` | `f6cd35419e7b` | `9497e4fb` f1c841-regular | regular Flow 0.23 / Message 0.19 |
| `9fb0ad-guard-flow-message-next` | `1ce9bac3812d` | `4b863bb5` f1c841-flow-message-next | next Flow/Message |
| `9fb0ad-guard-orchestrate-0.37` | `71f9a90e76ec` | `61abe3fb` f1c841-orchestrate-0.37 | orchestrate 0.37 |
| `9fb0ad-guard-main` | `c87aa1714912` | `0025894f` main | rollback equivalent of 1039 |

The original f1c841 branches were not rewritten. I created the fourth branch, for main, because the rollback target `xp12f872…` carries the old guard, so it refuses today and will keep refusing after any fixed generation is live (witnessed at 13:01 in `reports/deployment.md`). `ffb6mz81…` is the activatable twin of 1039.

## Builds (unit `9fb0ad-home-build-guard`, Prometheus, `--max-jobs 0`, Lojix ouranos `system`/`horizon` overrides; all exit 0)

| Commit | Out-path | Replaces | Rooted |
|---|---|---|---|
| f6cd3541 | `/nix/store/xc6nwq2z57bykqyp6vr48ln6v3v8dsvv-home-manager-generation` | `1rj6l1ln…` | `~/.local/state/9fb0ad/gcroots/hm-guard-regular` |
| 1ce9bac3 | `/nix/store/sqwm3xbx8kfl1qmh5zfbm1p9rqnv724a-home-manager-generation` | `2hnqcg3q…` | `hm-guard-next` |
| 71f9a90e | `/nix/store/whv1bk8mkam50kqr3ryjz5ng67i3da2z-home-manager-generation` | `qda5pkid…` | `hm-guard-orchestrate` |
| c87aa171 | `/nix/store/ffb6mz81ggl98sjsivcw790jpyfz6ka5-home-manager-generation` | `xp12f872…` | `hm-guard-main` |
| f6cd3541 check | `/nix/store/ks67mabg9vv79qyfhxrwcf9jmld2hbkq-messenger-clj-home-package` | — | — |

Each fixed generation compared with the one it replaces:
- `.config/systemd/user` is identical, and the home-files file list is identical. For the regular pair, `home-files` is the same store path (`37wdxh10…`) and the closure's package names are identical.
- `activate` differs in only two places: the whole `retireProvenLegacyMessengerBindings` step is gone, and the `check-link-targets.sh` path changes because its `forcedPaths` is now `()`.

## Dry read against the live links (activate not run)

- `grep -c retireProvenLegacyMessengerBindings` on each of the four new `activate` scripts gives 0.
- `readlink` of all eleven `~/.local/bin/{messenger-clj,hm-*}` gives `/nix/store/ddp041ij…-home-manager-files/.local/bin/<cmd>`. All match HM's `homeFilePattern`.
- I ran each new generation's `check-link-targets.sh` read-only (it only reads, compares and prints) against `HOME=/home/li` over that generation's full `home-files`, with the activate script's PATH. Result: **exit 0, no collision**, for all four. This is the exact gate that runs before `linkGeneration`.
- `adoptHerdrConfig`: the live `~/.config/herdr/config.toml` resolves to `grj6d8ly…-herdr-config.toml`, which equals the pin in the new scripts, so the step is a no-op.

## Activation order on his word (each step needs `Observe.Locks` empty first)

1. `whv1bk8m…/activate` (orchestrate 0.37), then the post-checks of `flows/f1c841/reports/morning-deploy-orchestrate-037.md`. Rollback: `ffb6mz81…/activate`, not `xp12f872…`.
2. `sqwm3xbx…/activate` (next Flow 0.23 / Message 0.19) and the rest of step 2 of `flows/f1c841/reports/deployment.md` «Next commands». Rollback: `whv1bk8m…/activate`.
3. That report's step 3 (`sandbox-regular.sh`, reconfigure, store move), with `xc6nwq2z…/activate` in place of `1rj6l1ln…`. Rollback: `sqwm3xbx…/activate`.
4. Land: put `f6cd3541` on main (fast-forward through 9497e4fb if main is still 0025894f), rebuild from main, and expect `xc6nwq2z…`.

## Sources

- Read: `flows/9fb0ad/reports/deployment.md`; `flows/f1c841/reports/morning-deploy-final.md` (live state, order, build command), `deployment.md` (choice, «Next commands»), `morning-deploy-orchestrate-037.md`, `morning-deploy-flow-message.md`, `morning-deploy-f1c841.md` (build command lines).
- CriomOS-home: `git log -p modules/home/profiles/min/messenger-clj.nix`; `checks/messenger-clj-package/default.nix`; `modules/home/default.nix`; `herdr.nix` grep.
- Generated: `activate` of `xp12f872…`, `qda5pkid…`, `2hnqcg3q…`, `1rj6l1ln…` and of the four new generations; HM `check-link-targets.sh` (`3z7h93qz…`, `wlfv7dsz…`), `home-manager.sh`.
- Live, read-only: `readlink` of `~/.local/bin/*`, `~/.config/herdr/config.toml`, `~/.local/libexec/messenger-clj`, `~/.local/state/home-manager/gcroots/current-home`; `orchestrate 'Observe.Locks'`.
- Build logs: session scratchpad `log-{regular,orchestrate,next,main,check}.txt`, `build-summary.txt`.

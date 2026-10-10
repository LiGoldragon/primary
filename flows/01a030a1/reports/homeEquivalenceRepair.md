# Home equivalence repair proposal

## Remembered outcome

Flow `01a02f74` found the Chroma–Emacs runtime anatomy substantially aligned.
Its principal discrepancy was above that runtime: standalone Home extended its
package set with Home overlays, while embedded Home received a differently
constructed package set, and their activation derivations differed.

The direct living-psyche ruling requires no difference between embedded and
independent Home. Shared Home logic must come from Lojix-emitted Horizon or
shared Nix machinery whose setup input is Horizon, and the embedded form must
be only the minimum wrapper. A second ruling places values currently inherited
from the OS in Horizon or an extended-Horizon derivation.

## Disposition of the current dirty shortcut

The current uncommitted CriomOS attempt is useful disconfirming evidence, not
the proposed end-shape. It recovers a package set through
`builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)`
and feeds that package set to the entire NixOS target. This selects an arbitrary
already-evaluated user configuration, broadens Home overlay policy into the
whole OS, and leaves standalone and embedded Home assembled by two routes.

## Proposed boundary

CriomOS-home should own one explicit construction record containing the
overlay-extended package set, the shared Home module closure, the per-user
Horizon value, and the ordinary Home identity fields. Its standalone
`homeConfigurations` and CriomOS's embedded Home wrapper should both consume
that record. CriomOS should retain only node-local user selection and the Home
Manager attachment; it should not reconstruct Home policy or infer a package
set from an evaluated user's output.

The package set should remain scoped to Home. Making Home's current `yt-dlp`
overlay global to every NixOS package is a wider policy change not implied by
the equivalence ruling.

## Literal patch proposal

This is a patch against the current checkouts, not pseudocode. It deliberately
replaces the dirty CriomOS `head (attrValues homeConfigurations)` shortcut.
The CriomOS-home change must land first; CriomOS must then pin that revision
before consuming the new output.

In the user-environment repository, change `flake.nix`:

```diff
@@
       horizon = inputs.horizon.horizon;
       lib = inputs.nixpkgs.lib;
       packageOverlays = import ./overlays { inherit inputs; };
-      pkgs = inputs.pkgs.pkgs.extend (lib.composeManyExtensions packageOverlays);
+      homePackageSet =
+        inputs.pkgs.pkgs.extend (lib.composeManyExtensions packageOverlays);
+      homeConstruction = rec {
+        packageSet = homePackageSet;
+
+        mkUserModule =
+          {
+            horizon,
+            userName,
+            user,
+          }:
+          { lib, ... }:
+          {
+            _module.args = {
+              inherit horizon user;
+            };
+
+            nixpkgs = {
+              config = lib.mkForce packageSet.config;
+              overlays = lib.mkForce packageSet.overlays;
+            };
+
+            home = {
+              username = lib.mkForce userName;
+              homeDirectory = lib.mkForce "/home/${userName}";
+              stateVersion = "26.05";
+            };
+          };
+
+        mkConfiguration =
+          {
+            horizon,
+            userName,
+            user,
+          }:
+          inputs.home-manager.lib.homeManagerConfiguration {
+            pkgs = packageSet;
+            modules = [
+              inputs.self.homeModules.default
+              (mkUserModule {
+                inherit horizon userName user;
+              })
+            ];
+          };
+      };
@@
       mkHomeConfiguration =
         userName: user:
-        inputs.home-manager.lib.homeManagerConfiguration {
-          inherit pkgs;
-          extraSpecialArgs = {
-            inherit horizon user;
-          };
-          modules = [
-            inputs.self.homeModules.default
-            (
-              { lib, ... }:
-              {
-                nixpkgs.overlays = lib.mkForce pkgs.overlays;
-                home.username = userName;
-                home.homeDirectory = "/home/${userName}";
-                home.stateVersion = "26.05";
-              }
-            )
-          ];
-        };
+        homeConstruction.mkConfiguration {
+          inherit horizon userName user;
+        };
@@
-      homeConfigurations = builtins.mapAttrs mkHomeConfiguration horizon.users;
+      lib = (bp.lib or { }) // {
+        inherit homeConstruction;
+      };
+
+      homeConfigurations = builtins.mapAttrs mkHomeConfiguration horizon.users;
```

The new record uses interfaces which exist now:
`inputs.home-manager.lib.homeManagerConfiguration`,
`inputs.self.homeModules.default`, `packageOverlays`, `pkgs.config`, and
`pkgs.overlays`. It centralizes the package-set recipe, module closure, Horizon
and user arguments, username, home directory, and state version.

After pinning that CriomOS-home revision, change `modules/nixos/userHomes.nix`
in the system repository:

```diff
@@
-  mkUserConfig = _name: user: {
-    _module.args = {
-      inherit user;
+  mkUserConfig =
+    userName: user:
+    {
+      imports = [
+        (inputs.criomos-home.lib.homeConstruction.mkUserModule {
+          inherit horizon userName user;
+        })
+      ];
     };
-    home.stateVersion = "26.05";
-  };
@@
   home-manager = {
     backupFileExtension = "backup";
-    extraSpecialArgs = {
-      inherit horizon constants pkgs;
-      homeSystem = pkgs.stdenv.hostPlatform.system;
-    };
     sharedModules = [ inputs.criomos-home.homeModules.default ];
-    useGlobalPkgs = true;
+    useGlobalPkgs = false;
     users = mapAttrs mkUserConfig homeUsers;
   };
```

Home Manager's real NixOS API supports this boundary: with
`home-manager.useGlobalPkgs = false`, each user module may set `nixpkgs.config`
and `nixpkgs.overlays`, from which Home Manager derives that user's `pkgs`.

Finally, restore the system repository's `flake.nix` package set rather than
making Home's overlays global to NixOS:

```diff
@@
       horizon = inputs.horizon.horizon;
-      pkgs =
-        (builtins.head (builtins.attrValues inputs.criomos-home.homeConfigurations)).pkgs;
+      pkgs = inputs.pkgs.pkgs;
```

The separate dirty move of the target-dependent
`agent-intercom-command-ownership` check from Blueprint's auto-discovered
`checks/` tree to `gates/` is sound and should remain: the check really requires
`target`, and its explicit import supplies `inputs`, `pkgs`, and `target`.

## Required proof

The existing `home-activation-equivalence.nix` check remains the smallest
derivation-identity gate and must cover every target-local user against the real
materialized Horizon/system inputs. The trusted sequence is a witnessed red
result at the clean pinned source, a green result after the shared-construction
patch, then the existing resident Chroma–Emacs check through the ordinary
embedded activation path and the repository's complete Nix gate. A source-text
comparison is not proof.

The check should also derive its expected user names from
`inputs.horizon.horizon.users`, filtered by `hasPubKey`, and assert that the
embedded names equal that external set before comparing activations. Its
current embedded-name-driven filter can miss an omitted embedded user.

The exact targeted proof is the existing
`checks.x86_64-linux.home-activation-equivalence` Nix build with the
materialized system, Horizon, deployment, and secrets overrides, followed by
the user-environment repository's `checks.x86_64-linux.chroma-emacs-resident`
build and the complete system flake gate. Builds used as evidence must use
`--rebuild`.

Current evidence does not establish green: the clean pin has the witnessed
activation mismatch; the dirty shortcut aligned inspected package attributes
but its activation evaluation did not finish while transitive inputs were being
fetched. Home Manager's NixOS integration also injects Nix, locale, and
fontconfig defaults. If these still change the activation, their values must be
made part of the Horizon/extended-Horizon construction rather than copied from
the OS.

No product change, build, realization, activation, or deployment was made by
this proposal flow.

## Sources

- `flows/01a02f74/log.md`
- `flows/01a02f74/reports/currentVsVisionMap.md`
- `flows/01a02b4b/vision/homeEquivalence.md`
- `flows/01a02b4f/reports/criomosPinAudit.md`
- `flows/01a02b4f/witnesses/fullGate.md`
- `flows/387c707c/reports/visionMap.md`
- `flows/387c707c/witnesses/visionMap.md`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/home-activation-equivalence.nix`

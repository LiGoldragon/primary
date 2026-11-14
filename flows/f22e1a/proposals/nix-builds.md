Presentation.{ «A build rebuilds only what changed» Proposal }

# A build rebuilds only what changed

Created by Fable 5.1, on the living's words, from the research of Psyche core Opus at flows/c31020/rust-nix-testing.md.

### Proposal 1: The shape of a build · psyche-belief › vision/nix-builds.md

::: comment
The flow flake compiles the workspace about 120 times per check because crane shares only the third-party dependencies: every derivation that inherits them compiles the workspace crates again. The shape wanted is the one the Once line implies: the unit of a build is the unit that changes on its own, the crate, and the compiled work is shared by hash across every active repository. The tool is knowledge; the vision names the shape.
:::

+ ## The unit of a build is the crate

+ A build is made of the units that change on their own: one derivation per crate, third-party and workspace member alike. A change rebuilds the crates that depend on it and no other, and a crate at one version and one feature set is built once for every repository that uses it.

+ Every active repository takes nixpkgs, the Rust toolchain and the crate overrides from one shared input, the build base, so that the same crate hashes the same everywhere and the remote builder's store serves it to all; a repository that pins its own differs in hash and is served by nobody.

+ Cargo is the local loop, incremental and unshared; Nix is the shared build, whole and reproducible. The two are not made to do each other's work.

```nix
+ # tentative: the shape of an active repository's flake
+ inputs.base.url = "github:LiGoldragon/build-base";        # nixpkgs, toolchain, crate overrides: one pin for every repository
+ outputs = { self, base, ... }:
+   let
+     inherit (base) pkgs toolchain crateOverrides;
+     cargoNix = import ./Cargo.nix {                         # generated from Cargo.lock, committed: one derivation per crate
+       inherit pkgs;
+       buildRustCrateForPkgs = p: p.buildRustCrate.override { rustc = toolchain; cargo = toolchain; };
+       defaultCrateOverrides = crateOverrides;
+     };
+   in { packages.default = cargoNix.workspaceMembers.flow-nexus.build; };
```

+ ## A check runs; it does not compile

+ A crate's tests are compiled once, with the crate, into test binaries; a check runs those binaries and compiles nothing. There is one check per crate, which runs every test of that crate, and the default check is all of them. A test is named in its code and proved by the check of its crate; there is no check per test.

```nix
+ # tentative: one check per crate, running the binaries the crate's build made
+ checks.flow-nexus = pkgs.runCommand "check-flow-nexus" { } ''
+   for bin in ${testBinaries "flow-nexus"}/tests/*; do $bin; done
+   touch $out
+ '';
```

```mermaid
+ flowchart TB
+     b["build base: nixpkgs, toolchain, overrides, one pin"] -- "input of" --> r["every active repository"]
+     r -- "one derivation per crate" --> c["a crate at one version and feature set: one hash everywhere"]
+     c -- "built once, served by" --> s["the remote builder's store"]
+     c -- "its tests compiled with it" --> t["test binaries"]
+     t -- "run by" --> k["the crate's check: runs, compiles nothing"]
```

### Proposal 2: Until the per-crate build lands · psyche-belief › vision/short/nix-builds.md

::: comment
The per-crate shape has unknowns the research names, git dependencies under patch among them, and is proved first in the example repository. The flow repository burns now. Crane's own partition mechanism gives the compile-once shape inside the flake that exists: one archive of the test binaries, every check a run from it. A new module, shown whole.
:::

````markdown
+ ---
+ description: The short-term compromise of Nix builds: how a crane workspace compiles once per check while the per-crate build is proved.
+ dependencies: [vision-nix-builds]
+ ---

+ A crane workspace compiles its test binaries once, into one nextest archive derivation, and every check is a run from that archive: the default check runs all of it, a crate's check the tests of that crate. No check inherits the cargo artifacts to compile again.

+ ```nix
+ testArchive = craneLib.mkCargoDerivation (commonArgs // {
+   inherit cargoArtifacts;
+   doInstallCargoArtifacts = false;
+   nativeBuildInputs = [ pkgs.cargo-nextest ];
+   buildPhaseCargoCommand = ''
+     mkdir -p $out
+     cargo nextest archive --locked --workspace --archive-format tar-zst --archive-file $out/archive.tar.zst
+   '';
+ });
+ crateCheck = crate: craneLib.mkCargoDerivation (commonArgs // {
+   cargoArtifacts = null; cargoVendorDir = null; doInstallCargoArtifacts = false; CARGO_PROFILE = "";
+   nativeBuildInputs = [ pkgs.cargo-nextest ];
+   buildPhaseCargoCommand = "mkdir -p $out";
+   doCheck = true;
+   checkPhaseCargoCommand = ''
+     cargo-nextest nextest run --archive-file ${testArchive}/archive.tar.zst --workspace-remap . -E 'package(=${crate})'
+   '';
+ });
+ ```
````

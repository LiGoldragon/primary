# field-clj deps hash on Prometheus, 2026-09-26

Subflow of b860be. Blocker: Lojix deployment 34 (ouranos, CriomOS e6a83edc,
CriomOS-home 4a9d85d7) failed on Prometheus with a fixed-output hash mismatch
on `/nix/store/z3jvnm2s8p61rrjiqsv73nh3rwzmz8js-field-clj-deps.drv`.

## Result

- field-clj main moved `75d77597b7e9b00d51d3e3759ced571929ccb8b6` to
  `a2c278d36520ab898f492071f660a438d2a1bf32` (bookmark `deps-hash-b860be`, same
  commit). The only change is `deps.edn`, which now pins
  `org.clojure/clojure {:mvn/version "1.12.6"}`. The declared hash stays
  `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=`.
- No version bump: field-clj has no version surface (grep found none), and the
  jar set is the one the declared hash already named.
- Verdict: the build is deterministic on Prometheus for each derivation, and
  its output depends on which consumer builds it. The deps output depended on
  the Clojure CLI version, because the CLI's root `deps.edn` supplies
  `org.clojure/clojure`. Pinning clojure makes both consumers produce the
  declared hash.

## 1. Which derivation, which pin

`nix/default.nix` at 75d77597 declares `deps = { name = "field-clj-deps";
edn = ../deps.edn; hash = "sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=";
aliases = [ "test" ]; }`. clj-build 9c1778b2 `lib/fetch-deps.nix` runs
`clojure -Sdeps '{:mvn/local-repo …}' -Spath` (base and `-A:test`), copies the
jars on those classpaths into `$out/repository`, and writes the relative jar
lists to `$out/classpath` and `$out/classpath-aliases`. `nativeBuildInputs =
[ pkgs.clojure pkgs.git ]` means the consumer's nixpkgs picks the CLI.

CriomOS-home 4a9d85d7 `flake.lock` pins field-clj `75d77597b7e9b00d51d3e3759ced571929ccb8b6`,
which was main at the time (`git ls-remote` showed the same rev). Home sets
`field-clj.inputs.nixpkgs.follows = "nixpkgs"`, and Home's root nixpkgs is node
`nixpkgs_2` = `github:LiGoldragon/nixpkgs/0e251e24a4f24e036a084b6b4b2d2491af4167f4`.

Derivations (evaluated on ouranos, eval only):

    nix eval --raw --expr '(builtins.getFlake "git+file:///git/github.com/LiGoldragon/CriomOS-home?rev=4a9d85d7…").inputs.field-clj.packages.x86_64-linux.default.deps.drvPath'
    /nix/store/z3jvnm2s8p61rrjiqsv73nh3rwzmz8js-field-clj-deps.drv   (same through CriomOS e6a83edc)
    nix eval --raw 'git+file:///git/github.com/LiGoldragon/field-clj?rev=75d77597…#packages.x86_64-linux.field-clj.deps.drvPath'
    /nix/store/z50ga15xad3kj524fbxmm52vabwdmvqb-field-clj-deps.drv   (field-clj's own lock, nixpkgs 34ca302a)

The two derivations differ in the CLI they use:
`z3jvnm2s` has `clojure-1.12.5.1664` and `z50ga15x` has `clojure-1.12.6.1673`.
Using `--override-input nixpkgs github:LiGoldragon/nixpkgs/0e251e24…` on field-clj
75d77597 reproduces `z3jvnm2s` exactly, so that override is a faithful stand-in
for the Home consumer.

The CLI root `deps.edn` files, read through `nix store cat --store http://nix.prometheus.goldragon.criome`:

    clojure-1.12.5.1664/deps.edn: org.clojure/clojure {:mvn/version "1.12.5"}
    clojure-1.12.6.1673/deps.edn: org.clojure/clojure {:mvn/version "1.12.6"}

Both FOD derivations map to the same output path
`/nix/store/rp6svmrm2hqs8qb57lslyjbggmwfxrd3-field-clj-deps`, because the path
depends only on the name and the hash.

## 2. Builds on Prometheus (max-jobs 0, ssh-ng://nix-ssh@prometheus.goldragon.criome)

Command form: `nix build --no-link --option max-jobs 0 -L '<drv>^out'`.

| run | UTC | drv | offload line | result |
| home-run1 | 07:02:08 | z3jvnm2s (75d77597, Home CLI) | `building '…z3jvnm2s…' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` | specified HNlk…, got `sha256-vsJ2Q7yDWpDQvAl1GlcIjRqKm0XxB4xv26H72BV9CtM=` |
| home-run2 | 07:02:18 | z3jvnm2s | same | got `sha256-vsJ2Q7yDWpDQvAl1GlcIjRqKm0XxB4xv26H72BV9CtM=` |
| standalone-run1 | 07:02:33 | z50ga15x (75d77597, own CLI) | on prometheus | exit 0; output registered with narHash HNlk… |
| pin-standalone-run1 | 07:10:21 | dzljjm0y (pinned, fake hash) | on prometheus | got `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=` |
| pin-home-run1 | 07:10:37 | skh7rswb (pinned, Home CLI, fake hash) | on prometheus | got `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=` |
| pin-standalone-run2 | 07:10:41 | dzljjm0y | on prometheus | got HNlk… |
| pin-home-run2 | 07:10:44 | skh7rswb | on prometheus | got HNlk… |

A hash-mismatch output is never registered, so each failed run was a fresh
fetch into a fresh `$TMPDIR/m2`. Evidence for determinism:
- The unpinned Home derivation built twice gave vsJ2… both times.
- The pinned derivations, built twice under each CLI, gave HNlk… all four times.

`nix build --rebuild` could not run with max-jobs 0 ("local builds are
disabled"), so no `--rebuild` check was made. The fake-hash runs stand in for it.

The registered standalone output, read through the Prometheus cache
(`nix path-info --store http://nix.prometheus.goldragon.criome`), has deriver
`z50ga15x…`, narHash HNlk…, narSize 5209352, and signature
`prometheus.goldragon.criome:…`. Its `classpath` and `classpath-aliases` list
malli 0.18.0, clojure 1.12.6, dynaload 0.3.5, edamame 1.4.30, fipp 0.6.27,
arrangement 2.1.0, test.check 1.1.1, core.specs.alpha 0.4.74,
spec.alpha 0.5.238, tools.reader 1.5.2 and core.rrb-vector 0.1.2.

Unknowns:
- The content of the vsJ2 output was never observed, because it was never
  registered. That it differs only in `org/clojure/clojure/1.12.5` is inferred
  from the CLI root deps.edn and from the pin collapsing both to HNlk.
- Why Mind Sol's offline check on ouranos passed is also inferred:
  `rp6svmrm…` is valid in the ouranos store, likely from the standalone lock.

Side effect: standalone-run1 made
`/nix/store/rp6svmrm2hqs8qb57lslyjbggmwfxrd3-field-clj-deps` valid on
Prometheus. A plain retry of deployment 34 would therefore probably skip the
FOD build. That was not tested, and the path could be garbage-collected.

## 3. Landing

Workspace: `jj workspace add --name deps-hash-b860be -r 75d77597 /home/li/wt/github.com/LiGoldragon/field-clj/deps-hash-b860be`.

Package and check with field-clj's own lock:
`nix build --no-link --print-out-paths --option max-jobs 0 -L .#packages.x86_64-linux.field-clj .#checks.x86_64-linux.tests`

    building '/nix/store/ijvmf4awran0977bidfsglp3h8cd3rqd-field-clj-tests.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
    building '/nix/store/d8f61vhgxdz91rpp2h4ajimfp5g2hray-field-clj-uberjar.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
    field-clj-tests> Ran 34 tests containing 167 assertions.
    field-clj-tests> 0 failures, 0 errors.
    /nix/store/prx2ss34n57pv6jlfr4xxahm4v1izd6z-field-clj-uberjar
    /nix/store/c8774xm2z1yyip8xi1j8dvkh3dsbcdf0-field-clj-tests
    exit 0

The same build with `--override-input nixpkgs github:LiGoldragon/nixpkgs/0e251e24…` (Home's nixpkgs):

    building '/nix/store/3gz6f5ms44m6535hnd1pric6lqan0mv2-field-clj-tests.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
    building '/nix/store/4s2262xbc21fjkl3zgygg85d0wzvrk7n-field-clj-uberjar.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
    field-clj-tests> Ran 34 tests containing 167 assertions.
    field-clj-tests> 0 failures, 0 errors.
    /nix/store/a15b2pbqw7m66cix9l5qzrayjp8mdrgi-field-clj-uberjar
    /nix/store/rs6phkifqk9v0ns8lhgh8a1s9jsmmlir-field-clj-tests
    exit 0

Commit and push:

    jj commit -m 'deps: pin org.clojure/clojure 1.12.6 so the deps hash is CLI-independent …' deps.edn
    jj diff -r @- --name-only   ->  deps.edn
    jj bookmark create deps-hash-b860be -r @-
    jj git push --bookmark deps-hash-b860be
    jj bookmark set main -r a2c278d3 ; jj git push --bookmark main   (forward from 75d77597)
    git ls-remote ssh://git@github.com/LiGoldragon/field-clj.git refs/heads/main refs/heads/deps-hash-b860be
    a2c278d36520ab898f492071f660a438d2a1bf32  refs/heads/deps-hash-b860be
    a2c278d36520ab898f492071f660a438d2a1bf32  refs/heads/main

## Unresolved

- CriomOS-home does not yet pin field-clj a2c278d3. That repin is the step-2
  integrator's work.
- clj-build's fetcher still takes clojure from the CLI whenever a consumer's
  deps.edn does not pin it. messenger-clj and any other clj-build consumer
  that uses `follows` can break the same way.

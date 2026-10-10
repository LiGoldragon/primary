# D2 receipt: field-clj built hermetically through clj-build (field-audit gap 5)

Repository: https://github.com/LiGoldragon/field-clj, main at
f965616913b22220080bda31cde31afb036cc704 ("Build field-clj hermetically
through clj-build"), rebased onto 8c5b0ce, the gaps 1–4 work landed
concurrently. `git ls-remote` on the GitHub URL returned that revision.

## What changed

The files touched were flake.nix, flake.lock, deps.edn, the new nix/default.nix, and the README's Tests and Build sections.

- flake.nix is now an index. It gained a `clj-build` input (a1544de, with `nixpkgs` following field-clj's own nixpkgs 34ca302) and imports `nix/default.nix` for `packages` and `checks`.
- Dependencies: `fetchCljDeps` resolves `deps.edn` with the `test` alias in a fixed-output derivation. The hash is `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=`. The package no longer runs `clojure -Sdeps` against Maven at run time.
- Deployable: `mkCljUberjar`, runtime `jvm`, main `field-clj.core`, with `runtimeInputs` jj and git.
  - Why JVM: field-clj is a JVM program that uses malli, and malli is a JVM library.
  - Why an uberjar rather than `mkCljCli`: the CLI starts once per commit. AOT-compiling field-clj and malli once at build time saves recompiling them from source on every run, and one jar is the deployable unit.
  - jj and git are the only external tools field-clj shells out to, so the wrapper puts them on `PATH`.
- Tests: `mkCljChecks`, runtime `jvm`, with jj and git in `nativeBuildInputs`. It runs `field-clj.core-test`, `field-clj.commit-test` and `field-clj.repo-test`. `nix flake check` therefore runs clojure.test, with `checks.tests` and also `checks.package`.
- Sources are filtered with `lib.fileset`: the package gets `src/` only, and the tests get `src/` and `test/`.
- Deprecated-paths warning: removed. The old wrapper passed `:paths ["/nix/store/…/src"]` through `-Sdeps`. Reproduced by hand, it printed `WARNING: Use of :paths external to the project has been deprecated`. Nothing passes external paths now.
- `deps.edn`: `:test` now holds only `:extra-paths`, and the runner's `:main-opts` moved to a new `:runner` alias. Without the split, the FOD's `-A:test` printed `WARNING: Use of :main-opts with -A is deprecated`. Run the tests by hand with `clojure -M:test:runner`. The resolved jars, and so the FOD hash, are unchanged.

## Evidence

- `nix flake check --no-build` on the pushed tree: "all checks passed!", exit 0. `packages.default` evaluated to `7zrjp1xm…-field-clj-uberjar.drv` and `checks.tests` to `nl0wh4n4…-field-clj-tests.drv`.
- FOD hash: I ran the FOD build script by hand with the pinned nixpkgs clojure (`clojure-1.12.6.1673`), using a fresh local Maven repository and field-clj's `deps.edn`. `nix hash path` of the output gave the same `sha256-HNlk…` as clj-build's example, which resolves the same jars. This is a claim until a Nix build confirms it.
- Hand-run tests (smoke, not the witness):
  - `clojure -M:test:runner` (local CLI 1.12.5) on the rebased tree: 33 tests, 163 assertions, 0 failures, 0 errors.
  - The same runner source that `mkCljChecks` generates, run as `java -cp src:test:<FOD jars> clojure.main runner.clj` with the pinned openjdk 21.0.12.1, jj 0.45.1 and git 2.55.0: 33 tests, 0 failures, exit 0.
- Hand-run uberjar (smoke): I ran `mkCljUberjar`'s JVM build steps outside Nix on the FOD jars (AOT launcher compile, jar merge, `jar --create`). `java -jar field-clj.jar` refused without a caller: `#refused :no-caller`, exit 1.

## Not witnessed

- The hermetic build is unwitnessed. I tried the full `nix flake check -L` once, before the rebase; the derivations differed from the pushed ones only by the source. It failed with exit 1:

      cannot build on 'ssh-ng://nix-ssh@prometheus.goldragon.criome': error: failed to start SSH connection to 'prometheus.goldragon.criome'
      Failed to find a machine for remote build!
      error: build of '/nix/store/3id9j0i5v8cmjd1s5m8yhcc0pnv8nccs-clj-build-test-runner.clj.drv^*' failed: … Reason: local builds are disabled (max-jobs = 0)

  The prometheus cache also timed out. Nix settings were not changed.
- Still owed: `nix flake check` and `nix build` on field-clj once prometheus is reachable again. That run confirms the FOD hash, the AOT uberjar and the in-sandbox test run, including jj/git repository tests under the build sandbox.
- The field-clj commit carries no Co-Authored-By footer. Adding one would have meant a force-push over main while another flow was pushing to it.

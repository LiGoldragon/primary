# M6 receipt: messenger-clj builds on clj-build

Repository: https://github.com/LiGoldragon/messenger-clj, branch `m6-nix-38de5b`
at dd358c455d2e36a09891651b30b3a1cc7d77a62f. It has one commit on main d4f2d08, as
the brief asked, and is separate from the m1 branch. The push was checked with
`git ls-remote`. Nothing was merged. The live package stays pinned.

## What changed

The branch touches only README.md (the build and test sections), check.nix,
flake.nix, flake.lock, nix/ and dist/.

- `flake.nix` takes clj-build (main a1544de, whose nixpkgs follows ours) and is
  now only an index. The build lives in `nix/default.nix`, `nix/package.nix` and
  `nix/test-source.nix`.
- Dependencies: `bb.edn` is also a valid deps.edn, so it serves as the single
  list for development and for Nix. `fetchCljDeps` resolves it once, with hash
  sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=. That is malli 0.18.0 and
  its transitive jars, the same content hash as clj-build's example. No
  `deps/bb.edn` was needed.
- Program: `mkCljUberjar` with runtime bb builds a Babashka uberjar from `src/`.
  `nix/package.nix` installs it with the pinned Datalevin pod 0.8.25 (same
  fetchzip hash as before), the messenger-clj launcher and the nine `hm-*`
  links. `nix/launcher.sh` now runs `messenger-clj.jar` in place of the
  uberscript.
- dist/ is **removed**. Why: nothing consumes it. CriomOS-home and Curriculum
  have no reference to `dist/messenger-clj`, and the deployed package only
  copied it into the store. A committed copy with an equality check would need a
  second generator outside Nix, and it would still drift silently whenever the
  check cannot run, which is the case today with the builder down. As a build
  product the program can only be the output of the current `src/`. The "equals
  src" check is therefore true by construction instead of being a separate
  check.
- Tests as a flake check: `checks.clj-tests` is `mkCljChecks`, runtime bb, over
  core-test, cli-test, typed-store-test and legacy-import-test. It runs offline
  with the pinned pod on a patched test tree:
  - `#!/usr/bin/env bash` points at Nix bash, including the stub scripts that
    cli_test writes.
  - `bin/messenger-clj` runs bb on the check's classpath instead of resolving
    bb.edn from the network.
  - A stub `orchestrate` is on PATH.
- `checks.cli` (check.nix) now reads an empty typed ledger through
  `hm-heartbeat-state`, which exercises the jar and the pod, in addition to
  `--help`. `nix flake check` no longer runs only `--help`.
- Pod and `--set`: `mkCljChecks` has no `wrapperArgs`, so the check sets
  `MESSENGER_CLJ_DATALEVIN_POD` in `preCheck`. The package keeps its launcher
  export, because the `hm-*` names dispatch on `$0`, and because the launcher
  passes `--config nix/bb.edn` ahead of the jar, which a makeWrapper `--set`
  cannot place. So clj-build's `wrapperArgs` is not used.

## Witnesses

- `nix flake check --no-build`: **all checks passed**. packages default and
  messenger-clj evaluated to /nix/store/djqjylvn…-messenger-clj-0.1.0.drv,
  checks.cli to …-messenger-clj-check.drv, and checks.clj-tests to
  …-messenger-clj-tests.drv. The rendered build commands of clj-tests and
  test-source were read back from evaluation and match the by-hand runs below.
- `nix flake check` (a full build) was tried once and **failed**. The exact
  failure:
  - `cannot build on 'ssh-ng://nix-ssh@prometheus.goldragon.criome': error: failed to start SSH connection to 'prometheus.goldragon.criome'`
  - `Cannot build '/nix/store/44yazxqq…-clj-build-test-runner.clj.drv'. Reason: local builds are disabled (max-jobs = 0)`
  - The prometheus binary cache also timed out.
  - No Nix setting was changed. The full build is **unwitnessed**.
- By hand, outside Nix and not the witness:
  - The FOD script ran with the locked clojure 1.12.6.1673 and git 2.55.0, both
    already present, and gave the hash above.
  - The uberjar was built with the locked bb 1.13.220 on the FOD jars, and the
    substituted launcher ran against it.
  - `--help` printed the usage line.
  - `hm-heartbeat-state` on a temporary HM_REGISTRY printed
    `{"version":1,"routes":[],"retirements":[]}`, so the pod loaded.
  - `hm-list` printed routes.
- bb tests by hand:
  - On d4f2d08 as the README describes (bb.edn deps from ~/.m2, the pinned pod):
    **36 tests, 277 assertions, 0 failures, 0 errors**, in 22 s. The brief
    expected 280. The count at that revision was 277 in this run.
  - The check emulated by hand: the patched tree, the FOD classpath only,
    `env -i` with PATH limited to coreutils, and a read-only tree.
    - Without the stub, 2 errors, both in core_test
      `register-persists-proof-for-a-not-ready-agent` (line 442): `Cannot run
      program "orchestrate"`.
    - With the stub orchestrate: **36 tests, 281 assertions, 0 failures,
      0 errors**. The assertion count depends on the orchestrate path the test
      takes.

## Findings for Mind

- **Test hermeticity.** core_test `register-persists-proof-for-a-not-ready-agent`
  calls the real `orchestrate` on PATH. Run by hand on a host, it takes a live
  Lock. The flake check supplies a stub. The test itself should inject `*shell*`
  as its neighbours do. That is a test change, which this brief left out of
  scope.
- **Main moved during this work.** origin/main is now ea95386, "Send whole
  messenger bodies and add psyche variant", by li at 15:12 -0600. A merge
  preview conflicts in two places, and both are mechanical:
  - dist/messenger-clj.clj (modify/delete): keep the deletion.
  - flake.nix: main's `version = "0.2.0"` moves into `nix/package.nix`.

  README auto-merges. After the merge, rerun `nix flake check --no-build`. The
  deps hash stays the same unless bb.edn changed, and ea95386 did not touch it.
- **clj-build.** `mkCljUberjar`'s `passthru.jar` uses `placeholder "out"`, so
  another derivation that interpolates it gets its own output path, not the
  uberjar's. This branch uses `${uberjar}/share/messenger-clj/messenger-clj.jar`
  instead. `mkCljChecks` has no `wrapperArgs` or `env` for a pod. `preCheck`
  works, but it runs after `cd "$TMPDIR"`, so a consumer whose tests use
  relative paths must `cd` itself.
- The Python files (hm.py, supervisor.py and their tests), which M6 also names,
  were outside this brief's path scope and are untouched.
- An unverified assumption: the Nix sandbox provides a writable `/tmp` for
  bb's `fs/create-temp-dir`. The first real build will show it.

## Sources

- flows/e51411/reports/audit-flow-messenger-field.md, the M6 section.
- flows/38de5b/reports/audit-messenger.md, improvements 1 and 2.
- flows/38de5b/receipts/x1-clj-build.md.
- clj-build a1544de: README.md and lib/*.nix.
- messenger-clj d4f2d08, branch m6-nix-38de5b dd358c4, and origin/main ea95386.
- The scratch clone at the scratchpad directory messenger-clj-m6-38de5b.

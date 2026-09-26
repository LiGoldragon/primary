# clj-build fetchCljDeps FOD determinism (2026-09-26)

## Cause

Clojure CLI version, not file order or metadata. The CLI's built-in root
`deps.edn` adds `org.clojure/clojure` at the CLI's own version when the
project names none. Home forces field-clj's nixpkgs to follow its own
(0e251e2, CLI 1.12.5.1664). field-clj's own lock (34ca302) carries
CLI 1.12.6.1673. So the same `deps.edn` resolved `clojure-1.12.5.jar` in Home
and `clojure-1.12.6.jar` where the hash was taken. The kept build directory
showed that one jar as the only difference.

The brief's other suspects are ruled out:
- The FOD copies only the jars that the classpath names. No `.cpcache`, pom
  or Maven metadata file enters `$out`.
- The NAR hash ignores mtimes and sorts directory entries.
- The JDK does not enter the FOD. Its input is `pkgs.clojure`, which only
  runs the resolver.

## Reproduction on Prometheus (ssh, `nix build --rebuild`)

Home runs field-clj 75d7759 with Home's nixpkgs. That deps drv is
`z3jvnm2s…-field-clj-deps.drv` and uses clojure-1.12.5.1664:

    specified: sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=
       got:    sha256-vsJ2Q7yDWpDQvAl1GlcIjRqKm0XxB4xv26H72BV9CtM=

The other two cases check-rebuilt clean:
- field-clj a2c278d (flow b860be pinned clojure 1.12.6 in `deps.edn`) with
  Home's nixpkgs (`z5k76wk5…`).
- field-clj with its own nixpkgs (`26fda1z9…`).

## Fix: clj-build 9c1778b -> 8cc9991 (pushed to main, checked with `git ls-remote`)

In `lib/fetch-deps.nix`, the FOD now writes `$CLJ_CONFIG/deps.edn` as
`{:deps {org.clojure/clojure {:mvn/version "${clojureVersion}"}}}`.
- `clojureVersion` is a new optional argument, default `"1.12.6"`.
- The user `deps.edn` is merged after the CLI root and before the project, so
  it replaces the CLI's default Clojure.
- A project that names its own Clojure keeps it.
- The README documents the argument.
- Version bump: none. clj-build has no version surface: no version field, no
  release tags.

## Witnesses

| Witness | Result |
|---|---|
| Prometheus, `nix build --rebuild` twice each, fixed clj-build: field-clj 75d7759 and a2c278d, each with its own nixpkgs (CLI 1.12.6.1673) and with Home's nixpkgs (CLI 1.12.5.1664), 4 drvs | all 8 check builds exit 0 = HNlk… |
| ouranos, through the remote builder (probe names so the builds really ran on prometheus): field-clj 75d7759 `deps.edn` (test alias) and messenger-clj `bb.edn`, Home's nixpkgs | both built, output = HNlk… |
| field-clj 3e5f450 `nix flake check -L` (ouranos, remote builder) | "all checks passed!" (aarch64 omitted). Dependent drvs are unchanged because a FOD enters their hash by output only, so their outputs came from the Prometheus cache |
| field-clj 3e5f450 `nix build` | `/nix/store/prx2ss34…-field-clj-uberjar`; `bin/field-clj` prints `#refused :no-caller` |

## Consumers

- field-clj main 3e5f450 moves the pinned clj-build to 8cc9991. Only
  flake.lock changed. The hash is unchanged:
  `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=`. Home should repin
  field-clj to 3e5f450. a2c278d already passes under Home's nixpkgs.
- messenger-clj (not touched): its `bb.edn` names no Clojure, and its clj-build
  pin is 01126ad. Under Home's nixpkgs it gets the same CLI-dependent jars that
  failed for field-clj. The failing hash was not witnessed for messenger-clj
  itself. After a repin to clj-build 8cc9991, the declared hash
  `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=` stays correct; the
  probe witnessed this. No hash edit is needed.

## Leftovers

- A kept failed build directory on prometheus,
  `/nix/var/nix/builds/nix-668169-226132161`, belongs to nixbld and could not be
  removed as li.
- My prometheus `/tmp` scratch is removed.
- Orchestrate lock 7390 is released.

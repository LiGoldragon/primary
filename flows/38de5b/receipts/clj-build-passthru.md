# clj-build passthru.jar fix

Repo LiGoldragon/clj-build, main a1544de -> 01126ad (pushed; `git ls-remote origin main` shows 01126ad).

## Change

- `lib/uberjar.nix`: `passthru.jar` was `"${placeholder "out"}/share/<name>/<name>.jar"`, which evaluated to `/1rz4g4.../share/example/example.jar` and, in a consumer, resolves to the consumer's own `$out`. The uberjar is now built as `drv` and `passthru.jar` is set by `drv.overrideAttrs` from `finalAttrs.finalPackage`, so it is the real store path and carries the uberjar as string context.
- The uberjar derivation is unchanged: `example-uberjar.drv` is `0xf3dcdsj3ylmr2wb9l9jc2kvcqqk2jk` before and after.
- `tests/default.nix`: new check `example-jar-consumer`. At evaluation it asserts, for the JVM and bb uberjars, that `jar` lies under `${drv}/share/`, that its context holds the uberjar's `drvPath`, and that it does not start with `placeholder "out"`. At build it runs `test -f` and then runs each jar (`java -jar`, `bb <jar>`) from a second derivation.
- README documents `passthru.jar`.

## Evidence

- `nix flake check --no-build`: all checks passed (x86_64-linux); `example-jar-consumer` evaluated to `9pn7w4gh...-clj-build-example-jar-consumer.drv`.
- The consumer's `inputDrvs` include both uberjars (`0xf3dcds...-example-uberjar.drv`, `id4bkq1h...-example-uberjar.drv`).
- Negative case: with the old `lib/uberjar.nix` restored, `nix flake check --no-build` fails with `passthru.jar /1rz4g4.../share/example/example.jar is not inside example-uberjar's output /nix/store/z8frl151...-example-uberjar`.
- Not proved: the build. `nix build --max-jobs 0 .#checks.x86_64-linux.example-jar-consumer` timed out reaching `nix.prometheus.goldragon.criome` (builder unreachable). The build check has not been run.

## Versioning

clj-build has no version surface (no version attribute, no tags). Consumers pin it by flake-lock revision, so the new revision 01126ad is what they move to. No bump was made.

# clj-build uberjar staging fix, local witness on ouranos (2026-09-25)

Local builds allowed tonight; each nix command ran with
`--option builders '' --option substituters https://cache.nixos.org --option max-jobs auto`
(nix.conf unchanged). Fresh clones in `…/scratchpad/stagingfix-38de5b-opus5/`, Orchestrate lock 6526, released.
Nothing activated or installed.

## Fix: clj-build 01126ad -> 9c1778b (pushed to main)

`lib/uberjar.nix`, JVM path: the `chmod -R u+w staging` ran after the class copy, so
`cp -r classes/. staging/` hit read-only files and dirs copied from the store / extracted jars.
Now every copy into `staging/` uses `cp -r --no-preserve=mode`, and `staging/` is made `u+w`
after the jar extraction, after the source copy, and after the class copy.
The bb path (`bb uberjar`) builds straight from the classpath into `$out` and uses no staging
directory, so it needed no change; its jar is exercised by the same checks below.

| Witness | Result |
|---|---|
| `nix flake check -L` @ 9c1778b | PASS, "all checks passed!" (built `m3739vax…-example-uberjar.drv`, `…-example-jar-consumer`, `…-example-runs`; JVM and bb jars both print `{:status :ok, :greeting "hello field"}`) |
| `nix build .#checks.x86_64-linux.example-jar-consumer` | PASS -> `/nix/store/3l5nyvp3d0jykmwakphrjvp4wp88w1hx-clj-build-example-jar-consumer` |

## Consumer: field-clj 929936a -> d12dc35 (pushed to main)

Commit "field-clj: clj-build 9c1778b", flake.lock only (clj-build narHash `sha256-XBSNgrdG4zjhzlgs/zPc1AHQADli3urskn5RKBe81V8=`).

| Witness | Result |
|---|---|
| `nix flake check -L` | PASS, "all checks passed!" (built `wisdkc8l…-field-clj-uberjar.drv` and field-clj-tests: 33 tests, 163 assertions, 0 failures, 0 errors) |
| `nix build` | PASS -> `/nix/store/rjsi4gb4azrirq5md6alf5imhh4zk86g-field-clj-uberjar` (`bin/field-clj`, `share/field-clj/field-clj.jar`) |

aarch64-linux checks were omitted by `nix flake check` (not witnessed).

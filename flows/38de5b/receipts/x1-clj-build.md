# X1 receipt: clj-build

Repository: https://github.com/LiGoldragon/clj-build, main at
a1544de56d0b4622bd8cbb12e090d0290222c0c5 (the push was checked with `git ls-remote`).

## What the library holds

`lib.${system}` has four builders, and each takes the consumer's `pkgs` first:

- `fetchCljDeps pkgs { edn, hash, aliases ? [ ], name }`: a fixed-output derivation that resolves the `deps.edn` with the Clojure CLI. It keeps only the classpath jars, laid out as a Maven repository, and writes the `classpath` and `classpath-aliases` line files.
- `mkCljCli pkgs { name, src, main, deps, bin, runtime ? "bb" }`: a wrapped Babashka or JVM command that runs offline.
- `mkCljUberjar pkgs { ..., runtime ? "jvm" }`: an AOT JVM uberjar started by a generated gen-class launcher, or a `bb uberjar`.
- `mkCljChecks pkgs { src, tests, deps, runtime ? "jvm" }`: returns `{ clj-tests }`, which runs clojure.test offline. It fails on any failure or error, and when no test ran.

`runtimeInputs` and `wrapperArgs` fit messenger-clj: the Babashka runtime, the Datalevin pod through `--set`, and tests that need Babashka libraries. They also fit field-clj: the JVM runtime with malli, plus jj and git in `runtimeInputs`.

## Check result

- `nix flake check --no-build`: all checks passed. The three derivations evaluated: example-runs, example-tests-jvm and example-tests-bb.
- `nix flake check` (a full build): **not witnessed**. The only builder, ssh-ng://nix-ssh@prometheus.goldragon.criome, is unreachable ("failed to start SSH connection"; the prometheus cache also times out), and max-jobs = 0 stops local builds. This matches the cluster network outage recorded in flows/836818/log.md.
- The FOD hash sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU= was computed by running the FOD script by hand with the locked nixpkgs clojure 1.12.6.1673, which was substituted from cache.nixos.org and not built. It is a claim until a Nix build confirms it.
- An explicit local smoke run used the same commands, outside Nix, on the same jars. This is not the witness. The JVM tests and the Babashka tests each ran 2 tests with 0 failures. The bb CLI, JVM CLI, bb uberjar and JVM AOT uberjar all printed `{:status :ok, :greeting "hello field"}`. For invalid input, the bb CLI and the JVM uberjar exited 1 with `:refused`.

## Not done

- Moving messenger-clj and field-clj onto the library was out of scope for this brief; neither was modified.
- The full build needs to be rerun once prometheus is reachable again.

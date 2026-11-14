# Are Nix builds done once? Verified by running them

Date: 2026-11-14. Where: on the builder prometheus.goldragon.criome (the ssh-ng host in /etc/nix/machines).
Scratch: /tmp/verify-nix-54269e.Hbfq on the builder, made with mktemp -d. The scratch clones there have their origin remote removed and were never pushed.
Nothing was changed on any main branch, and no branch was switched in /git or in primary.

## 1. Did the fixes reach main?

Yes. They were rebased, so the commit hashes are new. The branch commits themselves are not on main, and their branches are still on origin.

| Fix | Branch commit | On main as | Same content? |
|---|---|---|---|
| build-base: the test build links the library | e2d09c5, f715526 (test-links-library-2687f8) | 837c346, 93f6e2d | yes: `git diff f715526 93f6e2d -- workspace.nix crate-source.nix` is empty |
| flow: unit tests under tests/unit | 2f4d899 (nothing-twice-2687f8) | 953808b | yes, with the source moved onto main |
| flow: the configured package recompiles only the daemon | 047c41a | 4282dda | yes: `git diff 047c41a 4282dda -- nix/mk-flow-package.nix crates/flow-nexus/src/main.rs` is empty |

No .nix file changed on build-base after 93f6e2d. The 14 commits since then only add entries to the crate set.

Which revisions the live builds use:
- build-base main is 9706bad. flow main eabddc8d (Flow 0.56.2) and Curriculum main 8881cc1 both lock 9706bad.
- CriomOS-home main 39c86609 locks:
  - flow-0550 = flow eabddc8d
  - curriculum-source = Curriculum 8881cc1
  - orchestrate ef4fe80
  - build-base at 9706bad (twice) and at 8aa29e1 (through message)
- The running flow-nexus is /nix/store/nwwm7mri…-flow-configured-0.56.2. Its derivation's closure holds the same flow-nexus library (s1kcn677…), plain -bin (0ggsqic0…) and test build (qfvqwvg2…) as flow main's checks. Only the configured daemon -bin is its own (mib7h4ng…). Command run on the laptop: `nix-store -qR $(nix-store -qd <that path>) | grep rust_flow-nexus`.

## 2. flow main eabddc8d: a test-only edit, then a library edit

Before editing, the scratch clone (`git+file`) gives the same drvPaths as `github:LiGoldragon/flow?rev=eabddc8d…` (checks.default vjqiwaaf…, configured-package 09zyfkvi…). So the comparison is exact.

Test-only edit: one comment line appended to crates/flow-nexus/tests/unit/waking.rs.
```
nix build --dry-run git+file://…/flow-test-edit#checks.x86_64-linux.{default,configured-package} …#packages.x86_64-linux.flow-capsule
these 10 derivations will be built:
  rust_flow-nexus-0.56.2-test, check-flow-nexus, flow-configured-daemon-seeds, flow-configured-0.56.2,
  flow-no-inherent-methods, flow-fmt, flow-request-id-migration-process, cargo-nix, flow-no-free-functions, checks
```
- No library and no -bin is rebuilt. The capsule is not rebuilt.
- The real build took 305 s wall, exit 0. The test derivation took 139 s, and check-flow-nexus (the test run) 166 s.
- The test derivation's log, compile by compile:
```
flow_nexus src/lib.rs           --crate-type lib --emit=metadata        (clippy pass)
flow_nexus_daemon/recovery/store_check  --emit=metadata  extern flow_nexus=bp3ck8q2…-rust_flow-nexus-0.56.2-lib
flow_nexus src/lib.rs           --crate-type lib --test                 (the unit-test target, tests/unit via #[path])
default_start, the three bins   --test   extern flow_nexus=bp3ck8q2…-rust_flow-nexus-0.56.2-lib
```
- bp3ck8q2…-lib is the library that main's own build made, so it is reused.
- Two things still run again on every test edit:
  - a full `--emit=metadata` type-check (clippy) of the library and its bins
  - the library's whole source, compiled again under cfg(test), as the unit-test target
- These two are the cost of the unit tests being a module of the library. They are not a second derivation.

Library edit: one comment line appended to crates/flow-nexus/src/lean.rs.
```
these 18 derivations will be built:
  rust_flow-nexus-0.56.2 (lib), rust_flow-nexus-0.56.2-bin (x2: plain, configured daemon), rust_flow-nexus-0.56.2-test,
  check-flow-nexus, doc-flow-nexus, flow-doc, flow-workspace-0.56.2, flow-capsule-witnesses,
  flow-nexus-0.56.2-unconfigured-binaries, flow-configured-daemon-seeds, flow-configured-0.56.2,
  the five whole-repository text checks, cargo-nix, checks
```
- No other member rebuilds: no crate depends on flow-nexus.
- The real build took 393 s wall, exited 0, and compiled one new library, c4q7h9rr…-rust_flow-nexus-0.56.2-lib.
- All three of the plain -bin (syiffhza…), the configured daemon -bin (9g3bv74g…) and the test build (qq4idafx…) link `extern flow_nexus=c4q7h9rr…-lib`.
- None of them compiles the library in full, apart from the `--test` and `--emit=metadata` passes.

Is anything built twice at main? In the closure of checks.default together with configured-package, four crate names have more than one derivation:

| Crate | Why there are two |
|---|---|
| rust_flow-nexus-0.56.2-bin | Plain and configured daemon. By design: the configured one recompiles only src/main.rs, against the same library. The derivation diff is only crateFeatures plus FLOW_NEXUS_DEFAULT_CONFIGURATION_RS. |
| rust_signal-11.0.0 | crateFeatures "datom datom-codec protos" vs "". Same source, same inputs. |
| rust_flow-ethos-before-request-ids-0.53.2 | "datom datom-codec" vs "" |
| rust_signal-flow-before-request-ids-53.0.0 | follows the two above |

No crate is compiled twice with identical inputs. Each feature split is still the same crate compiled twice, once per consumer feature set.

A failure against the vision: a test-only edit changes the deployed package.
- `flow-configured-0.56.2` takes `checked = [ configuredNexusCheck ] ++ memberChecks` (nix/mk-flow-package.nix, `binaries … { checked = … }`).
- So a test edit makes a new package derivation, and a new CriomOS-home generation, even though no binary changed.
- Its build is cheap (0 s here), but the deployed path changes.

## 3. Per repository

### flow (main eabddc8d)
| Question | Answer | Evidence |
|---|---|---|
| On build-base? | yes | flake.nix `base.url = github:LiGoldragon/build-base` |
| Pin | 9706bad (= build-base main) | flake.lock node base |
| Crate apart from tests? | yes | rust_flow-nexus-0.56.2 (lib), -bin, -test are three derivations. The test build links `extern flow_nexus=bp3ck8q2…-lib`. |
| Test edit rebuilds lib? | no | the dry-run above: 10 derivations, no lib or -bin |
| Off base inside flow | packages.default = unconfigured-flow d3ab87e and migration-predecessor f7d2336 | Both are built with their own crane eb35abd and fenix f8ac2cd. They are pinned, so they are built once and cached. Nothing of theirs rebuilt in any dry-run. |
| Its pinned Curriculum (4695835) | built off the base's feature set, in packages.curriculum and flow-capsule, which are not deployed | `nix/curriculum/Cargo.nix` imported directly, with src = the whole checkout (flake.nix:409-415). Against Curriculum's own check, 52 of 58 shared crates are other derivations. The leaves differ only in crateFeatures ("default" kept, e.g. cfg-if, unicode-ident, serde_core). |

### Curriculum (main 8881cc1)
| Question | Answer | Evidence |
|---|---|---|
| On build-base? | yes | flake.nix: `base.lib.workspaceOutputs { cargoNix = ./Cargo.nix; … }` |
| Pin | 9706bad (= main) | flake.lock |
| Crate apart from tests? | yes | rust_curriculum-0.1.0, -bin, -test. The test log shows the lib at `--emit=metadata` and every test `extern curriculum=qjizv36c…-rust_curriculum-0.1.0-lib`. |
| Test edit rebuilds lib? | no | edit to tests/declarations.rs: `these 4 derivations will be built: rust_curriculum-0.1.0-test, check-curriculum, cargo-nix, checks`. Inline `#[cfg(test)]` remains in src/refresh.rs and src/service.rs, and an edit there would rebuild the library. |
| Built twice? | yes, three ways at one revision | see below |

Curriculum 8881cc1 builds three different library derivations at the same revision:
- The check (`memberChecks … [ "default" "datom" ]`) gives pll7r6dx…, crateFeatures "datom datom-codec protos".
- packages.default (all-workspace-members) gives j7c3ijxz…, crateFeatures "". Its signal-curriculum-nexus is also its own derivation.
  - A library edit shows it: `these 9 derivations will be built: rust_curriculum-0.1.0.drv, rust_curriculum-0.1.0-bin.drv, rust_curriculum-0.1.0.drv, rust_curriculum-0.1.0-bin.drv, …`
  - The package that is published is therefore not the library that was tested.
- CriomOS-home's packages/curriculum-resolver-deployment gives sxr0kbs5…. It imports `${curriculum-source}/Cargo.nix` directly with `rootFeatures = [ "default" "datom" ]` and bypasses the base's feature set.
  - This one is deployed: it is in the current home-manager generation, rpvdvc5s….
  - Its tree against the checked one: 63 of 69 crates are other derivations. Command: `leaf.py sxr0… pll7r6…` on the builder.
  - Every leaf differs only by crateFeatures: cfg-if, dyn-clone, heck, log, typenum, unicode-ident, version_check ("default" vs ""); futures-*, slab, serde_core, tracing-core ("default" added); libc ("extra_traits").
  - So serde, tokio, rkyv, datom-codec, ethos-zero and the rest are compiled a second time for the deployment. Examples: serde 1.0.229 is sc0dx0bs… deployed vs ykhxpwyj… checked; tokio 1.53.1 is za50kcpl… vs 4ky01ljk….
- Night logs confirm the first split: for 3 Curriculum sources, rust_curriculum-0.1.0 and its -bin were each built twice, features "" and "datom datom-codec protos".

### Orchestrate (main ef4fe80, 0.39.0)
| Question | Answer | Evidence |
|---|---|---|
| On build-base? | no | flake.nix inputs: nixpkgs (NixOS nixpkgs-unstable d2339023), flake-utils, rust-build 56d18735 (crane 59a82a12, fenix 6914a98b). The toolchain is rust-nightly-complete 2026-06-19, not the base's stable 2026-10-15. |
| Pin | none of build-base. Cargo.toml pins datom-codec eabead4 and protos 3c7ade3. | Cargo.toml [workspace.dependencies] |
| Crate apart from tests? | no | Three crane deps derivations: orchestrate-nexus-deps, orchestrate-clients-deps, orchestrate-deps. buildPackage and 14 cargoTest checks all compile the workspace crates from the same cleanSource, tests included. |
| Test edit rebuilds lib? | yes, and the deployed packages | edit to crates/orchestrate-nexus/tests/stopping.rs: `these 5 derivations will be built: orchestrate-test-0.39.0 (x2), orchestrate-nexus-0.39.0, orchestrate-clients-0.39.0, orchestrate-0.39.0` |
| Built twice? | yes, with identical inputs | 13 orchestrate-test derivations share one source (sa1svg92…) and one cargoArtifacts. Each log shows `Compiling orchestrate-nexus` again before running its one test file (7-10 s each). Overnight there were 92 orchestrate-test builds over 6 sources. |
| Dependency tree | one monolithic deps build per resolution, rebuilt on every Cargo.toml or Cargo.lock change | Overnight: orchestrate-nexus-deps was built 11 times (11 sources), orchestrate-clients-deps 11, orchestrate-deps 5. Each is a full third-party tree compiled on nightly. |

## 4. Other repeated builds in the night's logs (builder, /nix/var/log/nix/drvs, since 2026-11-13 21:00)

There were 2,445 build logs. 527 are rust_* derivations, and 359 of their .drv files are still in the store. Grouped by (crate, src), 69 groups have more than one derivation. None has identical inputs; each has a cause:

1. A version bump rebuilds the unchanged crates.
   - flow-ethos 0.56.1 and 0.56.2 have identical source content: `diff -r /nix/store/0hdp58vp…-flow-ethos-0.56.1 /nix/store/gzc91gai…-flow-ethos-0.56.2` prints nothing.
   - Between 0.56.1 and 0.56.2 only crates/flow-nexus changed (19 files). Every member takes `version.workspace = true`, so each release is a new derivation for every member.
   - Through `[patch."…/flow"] flow-ethos = { path = "crates/flow-ethos" }` the bump also rebuilds signal-flow 60, 61 and 63 and meta-signal-flow 77 and 79. Each was built 5-6 times overnight from one source, once per flow-ethos version (0.54.3/0.54.7, 0.55.0, 0.56.0, 0.56.1, 0.56.2).
2. Feature splits per consumer, the same source compiled with and without datom:
   - signal 11.0.0, signal-flow 63.0.0, meta-signal-flow 79.0.0, signal-message 24.0.0, meta-signal-message 4.0.3
   - signal-curriculum-nexus 0.1.0 and its -test
   - flow-contract-0.1.0-test, for 6 sources
   - flow-ethos-before-request-ids, signal-flow-before-request-ids
   - translator 0.6.0: 4 derivations of one source, 3 feature sets
3. Curriculum package vs check, as above. 3 sources, each with its library and -bin built twice.
4. The flow-nexus configured daemon. Every flow source built 2 or 3 -bin derivations, which differ only by the configuration module. This is by design and recompiles only main.rs.
5. ethos-zero 27.0.0 was built twice from one source. It differs only through rkyv/munge/datom-codec/protos derivations below it, which is a feature difference in a third-party leaf.
6. The deployed home generation (rpvdvc5s…): 185 rust_* derivations, and 42 crate names appear more than once.
   - 36 of them come from the Curriculum deployment's own tree (section 3).
   - The other 6:
     - flow-nexus-bin x2, by design
     - signal-flow 63 x3: against flow-ethos 0.56.2 (patched local) and against 0.54.3 (message's git pin), with and without datom
     - signal 11, signal-message 24, meta-signal-message 4.0.3 and meta-signal-flow 79, x2 each, by features
   - CriomOS-home also locks build-base at two revisions (9706bad, 8aa29e1) and Curriculum at five (8881cc1, 4695835, 26e14b2, 478cbc5, 91acf29).
   - Crane deps derivations in the same closure: orchestrate-nexus-deps, orchestrate-clients-deps, listener, hexis, harness, aggregator, chroma, substack-cli, claude-answers.

## What could not be checked
- The night logs give no build durations for derivations built from the laptop. Their .drv is not on the builder, and 168 of the 527 rust_* logs have no .drv in the store, so they were not grouped.
- Whether the same derivation was built twice: a log file is per derivation and is overwritten, so a repeat is invisible.
- Not a gap, checked: the deployed home generation holds one rust_curriculum, the resolver's (sxr0kbs5…). It does not hold flow's capsule Curriculum 4695835 or primary's 26e14b2, so those two are built only where flow's checks and capsule are built.

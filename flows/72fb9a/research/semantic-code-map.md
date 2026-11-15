# Semantic navigation of Flow: SCIP-first trial

15 November 2026 · researchTools Sol 2ce803 · n4p4 · **in progress: comparison not yet run**.

Psyche ac2i narrowed the original live-language-server brief: try a pinned `rust-analyzer scip` index as a Nix derivation first, using existing query tools. Add an existing multiplexer only for a demonstrated live-only need. No new session daemon, laptop startup, Home declaration or system service was installed.

## Proven build

Published Flow R0: `37980e10bcb8325d9a68c580e0d22c73061bb267`, selected by its owner. Proposed CriomOS package branch: `research-tools-2ce803-scip`; successful immutable package revision: `ab62d218610f35af6279ed3590224dee83645011`, based on `4305f5cad95ab55a516cf430014a5f7dd7b2575e`. The canonical dirty checkout was untouched. The package is `packages.x86_64-linux.repository-analysis`; packaging review sq6r is accepted for the bounded query trial; the proposed branch has not landed on main.

| Observation | Result |
| :-- | --: |
| rust-analyzer | 2026-06-15 |
| Flow-base rustc | 1.99.1, 58cf8f9c3 (2026-10-13) |
| SCIP indexing wall time, GNU time | 18.57 s |
| Indexing user / system CPU time | 19.88 / 0.86 s |
| Maximum resident set, GNU time | 2,039,928 KiB (about 1.95 GiB) |
| Documents / occurrences / definition occurrences | 198 / 299,831 / 37,633 |
| Binary SCIP / printed JSON bytes | 30,658,712 / 58,803,376 |
| Metadata packages / resolve nodes | 144 / 144 |
| Emitted implementation relationships | 0 |
| Second identical build wall time | 0.243842 s, same output manifest, no build work |

These are single observations. GNU time's maximum RSS is not aggregate simultaneous process-tree memory. Indexing time excludes dependency fetching/vendoring, the explicit metadata preflight, JSON printing and stats. The second invocation includes Nix evaluation/cache lookup, not a repeated index. No broad performance estimate is established.

## Inputs, compilation and coverage

The package uses Flow's own locked build-base package set, compiler and Rust library sources; it does not make that base follow CriomOS inputs. A bare Flow input URL is pinned in the lock and asserted against the trial's advertised full revision. Cargo.nix supplies existing git source hashes; importCargoLock creates offline vendors. The lock has no repeated git name/version pair; retained offline metadata successfully resolves all 144 packages. Existing locked artifacts were preserved despite normal Nix node renumbering.

Nix's sandbox has no index-time network access; Cargo is explicitly locked/offline. RUSTC and PATH route configured compiler probes through a logging guard: version/print observations are allowed, code-generation arguments or non-observational calls are refused. This covers the configured paths; it is not a universal interception proof against a tool executing an absolute compiler path. Retained invocations are version/print probes, including one refused empty invocation. The explicit Cargo target directory and source target directory remained absent; Cargo.lock remained byte-identical.

The SCIP CLI requests build-script loading independently of editor enable switches. Its build-script command is explicitly an empty successful output producer. **Build-script cfg/env/OUT_DIR and procedural-macro expansions are omitted** and recorded in the artifact. An empty semantic answer in affected code is not evidence of absence. Declarative macro questions still require testing.

The index emitted duplicate-symbol warnings, errors for unnamed enclosing definitions, and missing SCIP-document definitions in generated Flow sources. Its configuration log says `ConfigErrors([])` despite an ERROR prefix. Zero relationship records is an observed limitation, not an assertion that Flow has no implementations. The static index must be checked against source; it is not the scoring oracle. See [rust-analyzer's SCIP implementation](https://github.com/rust-lang/rust-analyzer/blob/master/crates/rust-analyzer/src/cli/scip.rs) and [configuration reference](https://rust-analyzer.github.io/book/configuration).

The first package trial, `c5fcebe`, failed before indexing: importCargoLock's relative `cargo-vendor-dir` path resolved outside the vendor output. `ab62d21` binds it to the declared immutable vendor directory. The failed receipt is retained rather than counted as an index result.

## Comparison protocol and status

Frozen questions: `flows/2ce803/benchmark-questions.md`, SHA-256 `b245b67e9213aa7372146329d67449b87bf4d2883f430cf2168de83155c92325`. They ask for `Performs::perform` calls, `Performs` implementations, and macro-hidden versus direct/test `RefusesNativeLaunch::log_line` calls in sending.rs/send_tool.rs/performing.rs. At R0 the declaration positions are lines 193, 192 and 155; these shifted by two lines from the old report's revision.

Two isolated gpt-6.1-sol/Codex answerers are running: datomCodec Flow 7e98f4 as baseline (Task 7v3i), lojix Flow 725168 as treatment (Task 1o4l). Both named current native transcripts record model gpt-6.1-sol, effort medium and collaboration reasoning_effort medium; identity and absence of prior-answer/source exposure were revalidated before launch. This proves recorded harness configuration parity, not observation of hidden computation. Both receive the same immutable source/questions and 15-minute allowance. Baseline uses grep/ast-grep/source reads; treatment additionally uses the static index. Neither receives earlier answers or scoring truth. A separate source-only audit runs on its own clean detached R0 checkout.

The final table will report correctness, elapsed time and identically tokenized delivered tool output. Tokenizer counts are a reading-cost proxy, not provider-billed input or hidden reasoning. Current status: index ready, paired tasks admitted and awaiting completed answers. No comparative advantage is claimed yet.

## Reproduction and evidence

On Prometheus, build the published proposal without installing it:

```sh
Index=$(nix build --refresh --no-link --print-out-paths \
  github:LiGoldragon/CriomOS/ab62d218610f35af6279ed3590224dee83645011#packages.x86_64-linux.repository-analysis)
jq '.documents | length' "$Index/index.json"
cat "$Index/index-time.txt" "$Index/coverage-limitations.txt"
```

Existing SCIP printing provides JSON; jq selects bounded symbol/occurrence records. Definition roles and source context distinguish definitions from references; relationships are not supplied by this index. Upstream [SCIP](https://github.com/scip-code/scip) defines the interchange format; its [print command](https://github.com/scip-code/scip/blob/main/cmd/scip/print.go) exposes JSON.

Raw builder evidence: `/tmp/research-tools-2ce803.xkSGrr/`, especially `index-build-ab62d21.{json,log}`, `index-build-c5fcebe.{json,log}`, `index-cache-reuse.{json,log}` and `cache-reuse-time.txt`. The output manifest resolves the immutable artifact; it includes metadata, effective config, compiler invocations, coverage limits, analyzer/toolchain versions, index/stats and timing. Binary index SHA-256: `150f67f535808844115695b7c4e79165661fe2dd00bfe2cc21a13ba6c694a122`. JSON SHA-256: `4b57b967810fabf74c93e148d3d0f84d9f525b0e9597b07462a6e73586f2fa5a`.

# Semantic navigation of Flow: SCIP-first trial

15 November 2026 · researchTools Sol 2ce803 · n4p4.

**No navigation advantage was measured in this pair. Both matched the explicit-source oracle; the SCIP-assisted flow received 11.62% more tool-text tokens and took 11.14% longer.** The static index itself recovered the tested references correctly, with no resident language-server service. Adoption remains Fable’s decision.

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

The index emitted 26 duplicate-symbol warning entries, 73 unnamed-enclosing-definition errors and 297 missing-SCIP-document-definition diagnostics, including generated Flow sources. These are diagnostic counts, not counts of distinct missing symbols. Its configuration log says `ConfigErrors([])` despite an ERROR prefix. Zero relationship records is an observed limitation, not an assertion that Flow has no implementations. The static index must be checked against source; it is not the scoring oracle. See [rust-analyzer's SCIP implementation](https://github.com/rust-lang/rust-analyzer/blob/master/crates/rust-analyzer/src/cli/scip.rs) and [configuration reference](https://rust-analyzer.github.io/book/configuration).

The first package trial, `c5fcebe`, failed before indexing: importCargoLock's relative `cargo-vendor-dir` path resolved outside the vendor output. `ab62d21` binds it to the declared immutable vendor directory. The failed receipt is retained rather than counted as an index result.

## Paired comparison

Frozen questions: `flows/2ce803/benchmark-questions.md`, SHA-256 `b245b67e9213aa7372146329d67449b87bf4d2883f430cf2168de83155c92325`. They ask for `Performs::perform` calls, `Performs` implementations, and macro-hidden versus direct/test `RefusesNativeLaunch::log_line` calls in sending.rs/send_tool.rs/performing.rs. At R0 the declaration positions are lines 193, 192 and 155, two lines later than in the older report.

The baseline was datomCodec Flow 7e98f4 (Task 7v3i); treatment was lojix Flow 725168 (Task 1o4l). Both named current native transcripts record gpt-6.1-sol, effort medium and collaboration reasoning_effort medium. Identity and absence of prior-answer/source exposure were revalidated before launch. This establishes recorded configuration parity, not observation of hidden computation. Both received the same packet/source and 15-minute allowance, using independent clean detached checkouts. Baseline had grep, ast-grep and source reads; treatment additionally had SCIP/JSON queries. Neither saw the other answer or oracle.

| Whole three-question workflow | grep / ast-grep | + SCIP index |
| :-- | --: | --: |
| Calls correct / expected | 101 / 101 | 101 / 101 |
| Implementations correct / expected | 1 / 1 | 1 / 1 |
| Target log_line calls correct / expected | 6 / 6 | 6 / 6 |
| Incorrect target edges / missing explicit-source edges | 0 / 0 | 0 / 0 |
| Unrelated Admission macro calls correctly rejected | 2 / 2 | 2 / 2 |
| Delivered tool-text tokens, cl100k_base | 41,687 | 46,531 |
| Delivered tool-text bytes | 155,592 | 157,399 |
| Native receipt → completion-command submission | 195.783 s | 217.594 s |
| Delivered tool responses before completion command | 13 | 14 |
| Recorded SSH-query elapsed sum | 2.271 s (10 timed) | 13.458 s (11 timed) |
| Recorded SSH-query median | 0.217 s | 1.095 s |

Treatment adds 4,844 counted tokens and 21.811 seconds in this pair. Its time **excludes** upfront indexing, vendoring, metadata preflight and JSON conversion. The baseline had one local `/usr/bin/time` failure before SSH; treatment had one embedded jq syntax error whose surrounding shell nevertheless exited zero. Both retained errors and corrected their workflow. Both received some truncated tool responses; full raw files were not mistaken for text delivered to the model.

**Counting method:** tiktoken 0.12.0, `cl100k_base`, applied to concatenated native text blocks in each tool response, preserving the actual truncation and tool wrappers. The outer native content array is not JSON-serialized for counting. Count from the native user record containing BENCHMARK_LAUNCH to the first tool-call submission containing that condition’s own Done request. Exclude that final call’s acknowledgement and subsequent task-close bookkeeping. Include setup/error output and the shared packet read through a tool. These are exact counts under this extraction/tokenizer, a **model-reading proxy**, not native-model or provider-billed input tokens; system/prior context, tool-call arguments, hidden reasoning and final report tokens are excluded. No per-question token/time allocation is claimed because queries served several questions. Helper-query timing includes final source verification and is not a decomposition of the native completion-command endpoint.

Native endpoints: baseline `20:59:07.469Z` → `21:02:23.252Z`; treatment `20:59:08.403Z` → `21:02:45.997Z`, 15 November 2026. The endpoint is submission of the command carrying final report/Done, not the later receiving flow’s delivery. Treatment’s Done receipt was queued; its already completed artifact was discovered through native metadata later. That delivery/discovery lag is excluded; its cause is unknown.

## Correctness and scope

The source-only oracle and both answerers independently converged on **101 explicit tracked-source calls: 54 production, 47 test**, one `Performs` implementation (`RunningNexus`, performing.rs:218), and six target log_line calls. The owner mechanically compared both complete caller inventories against the audited lexical candidate set: no missing or extra path/line pairs. Enclosing functions, receiver evidence, cfg/test boundaries and macro classification also agree on inspection. This is explicit-source navigation evidence, not proof about synthesized expansion-only calls, every feature/platform configuration, external callers or compilation success.

A decisive same-name distinction: sending.rs:393 and send_tool.rs:651 call **LogsAdmission::log_line**, not RefusesNativeLaunch. The latter’s six calls are in performing.rs:178, 452, 924, 949, 987 and 1000. The first two are production eprintln! arguments; 924 and 987 are assert_eq! arguments; 949 and 1000 are direct test calls. Both flows resolved this correctly. Merely collecting the name log_line would conflate two traits.

Separately, raw concrete-implementation symbol queries in the index return precisely the audited **101 perform references and six target log_line references**, plus their definitions, with no extra/missing path/line pairs. The tested declarative-macro-contained calls are present. The index contains 198 of 199 tracked Rust documents; the absent path is `crates/flow-nexus/src/store/request_id_predecessor_fixture.rs`, with no relevant target occurrences. Its absence and global diagnostics remain limitations. Zero implementation relationships means the implementation answer required trait-reference/source inspection, not a ready-made implementation graph. No live-only need was demonstrated by these questions.

The auxiliary source-only oracle was configured separately as Luna/xhigh; its native runtime metadata was unavailable. It is outside the measured Sol pair. Owner cross-checks and agreement of source-only and indexed inventories support the bounded correctness result.

This is one concurrent pair, not a randomized or crossover study. Permaflow base contexts and chosen queries differ; setup/recovery and answer formatting count toward elapsed time. The observation cannot causally attribute the difference to SCIP or generalize to other repositories/questions. It measures retrieval and receiver disambiguation, not whole-project architectural understanding.

## Choice for Fable

Keep grep/ast-grep as the default structural route supported by these trials. Retain the published SCIP package as an explicit snapshot experiment if useful for precise symbol references. This pair demonstrates a working builder-side semantic index, **not a measured reading-cost or correctness improvement**. A reusable polished query interface or broader study would be a separate proposal. No authored session owner, multiplexer or live service is justified by this result.

The analyzer runs only during an explicitly requested Nix build; subsequent queries read the immutable artifact. It exits with the build. A 21:05:23Z process snapshot found no rust-analyzer process on either laptop or Prometheus. No startup configuration, Home environment, system service or running host deployment changed. The proposed package branch is published for review, not adopted on main; Field remains the sole actor for any future host activation.

## Reproduction and evidence

On Prometheus, build the published proposal without installing it:

```sh
Index=$(nix build --refresh --no-link --print-out-paths \
  github:LiGoldragon/CriomOS/ab62d218610f35af6279ed3590224dee83645011#packages.x86_64-linux.repository-analysis)
jq '.documents | length' "$Index/index.json"
cat "$Index/index-time.txt" "$Index/coverage-limitations.txt"
```

From this host, run those commands through `ssh "$NixBuilder"`; keep index parsing on the builder and return selected records. For the measured concrete implementation, after resolving `$Index`:

```sh
Symbol='rust-analyzer cargo flow-nexus 0.56.2 performing/impl#[RunningNexus][Performs]perform().'
jq -r --arg symbol "$Symbol" '
  .documents[] as $document | $document.occurrences[]
  | select(.symbol == $symbol)
  | [$document.relative_path, (.range[0] + 1), (.symbol_roles // 0)]
  | @tsv' "$Index/index.json"
```

This returns the method definition plus 101 references; bit 1 in symbol_roles marks a definition. Look up candidate full symbols in the selected document’s symbols first. A trait-declaration symbol and a concrete implementation-method symbol differ; this index supplies no relationship graph joining them, so verify the implementation in source before interpreting its references as trait callers.

Existing SCIP printing provides JSON; jq selects bounded symbol/occurrence records. Definition roles and source context distinguish definitions from references; relationships are not supplied by this index. Upstream [SCIP](https://github.com/scip-code/scip) defines the interchange format; its [print command](https://github.com/scip-code/scip/blob/main/cmd/scip/print.go) exposes JSON.

Raw builder evidence: `/tmp/research-tools-2ce803.xkSGrr/`, especially `index-build-ab62d21.{json,log}`, `index-build-c5fcebe.{json,log}`, `index-cache-reuse.{json,log}` and `cache-reuse-time.txt`. The output manifest resolves the immutable artifact; it includes metadata, effective config, compiler invocations, coverage limits, analyzer/toolchain versions, index/stats and timing. Binary index SHA-256: `150f67f535808844115695b7c4e79165661fe2dd00bfe2cc21a13ba6c694a122`. JSON SHA-256: `4b57b967810fabf74c93e148d3d0f84d9f525b0e9597b07462a6e73586f2fa5a`.

## Audit trail

Answer/evidence reports remain in temporary directories: baseline `/tmp/n4p4-baseline.g0Uimu/report.md`, treatment `/tmp/n4p4-treatment-725168.httJ2Z/report.md`, independent source oracle `/tmp/oracle-flow-37980e10-6blvHh/report.md`. Native transcript identifiers are `01a1e0f6-bc28-7d22-890a-ae47e98f48f8` and `01a1e0f6-e618-7d40-9912-b82725168e19`, under `/home/li/.codex-next-5ck97j38j3sb/sessions/2026/11/15/`.

Local measurement/extraction scripts and scored inventories: `/tmp/research-tools-2ce803.nrkzTR/`. Builder `baseline-counts.json` and `treatment-counts.json` retain per-response counts and endpoints; the corresponding outputs files retain only the selected tool text, not earlier context. Raw source-call and index-reference cross-checks are beside them. This report embeds the decisive counts, scope and counterexamples if temporary directories disappear. Independent audit `/tmp/research-tools-audit.2fon3s/report.md` verified both complete answer inventories, function/prod-test/macro classifications, native extraction boundaries, visible-text bytes and timestamp deltas, with no material discrepancy. It did not independently retokenize; the tokenizer totals are owner-computed on the builder, not a second independent tokenizer result.

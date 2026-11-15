# Builder-side Rust navigation trial

15 November 2026 · researchTools Sol · request n4p4 · completed trial proposal/evidence pointer.

Outcome: the static SCIP trial built successfully and both paired answerers completed. The detailed result is [semantic-code-map.md](../72fb9a/research/semantic-code-map.md): same bounded correctness, more tool-text tokens and time with SCIP in this one pair. No live service or main adoption.

## Current shape

**Build a SCIP index first; add a live language server only for a demonstrated question the index cannot answer.** Psyche core Opus ac2i replaces the earlier session-owner proposal with existing Rust/Nix tooling and as little authored code as possible. No Node program, source repository or enabled service is proposed.

`rust-analyzer scip` indexes one pinned Flow revision in a Nix derivation on Prometheus. Its analyzer, toolchain, source, dependency sources and analysis configuration name the build; later reads reuse the store output. Existing SCIP printing and JSON selection tools provide the query surface. No laptop analyzer or startup configuration is introduced. An existing packaged multiplexer is considered only for a concrete live-only gap, with its lifecycle reviewed against the event-only idle contract.

## Owners and events

Mind researchTools Sol 2ce803 owns package proposal, questions, experiment and report. Psyche b3wi and Mind core 82s0 allocate direct Sol implementation without a child implementation worker. The briefly allocated Luna child was interrupted before any probes, reads or edits; its audit confirms none occurred.

Mind nixCriomos Sol owns packaging/declaration boundary review; its potential OS-module/check paths remain untouched. Field core Sol alone owns eventual host activation. Prometheus has no declared li Home. Building a read-only index is not host activation. Two isolated answerers complete evidence packets before source-audit scoring and reporting. Each stage advances on its owner's completion message or command exit.

## Source and package proposal

Flow owner z7mh supplies published R0 `37980e10bcb8325d9a68c580e0d22c73061bb267` for both conditions, in independent detached disposable checkouts. The older report used `53782fba5e1f5b761b87f09809c0b319bcc27ad0`; any trait-name delta will be reported.

Isolated CriomOS branch `research-tools-2ce803-scip` starts at `4305f5cad95ab55a516cf430014a5f7dd7b2575e`; worktree `/tmp/research-tools-2ce803.nrkzTR/criomos`. The accepted package-only candidate is published CriomOS `ab62d218610f35af6279ed3590224dee83645011`; the source is locked and its remote build succeeded. Packaging review sq6r is accepted for the bounded query trial. Owned files: `packages/repository-analysis/default.nix`, `trial.json`, and associated flake input/lock. Dirty canonical/recovery worktrees remain untouched. Required `bd list --status open` failed read-only on the shared schema/leases table; no migration was performed.

The package takes toolchain and package set from Flow's locked build-base. Cargo metadata reads offline vendored sources with hashes from Flow's committed Cargo.nix. The source revision must equal trial.json. Indexing uses a writable copy, checking Cargo.lock unchanged and no target directory produced.

Upstream SCIP explicitly requests build-script output independently of editor switches. The proposal supplies an empty successful output producer and disables checks/procedural macros. This limited coverage must be proved on the pinned analyzer and disclosed: generated build output and procedural-macro effects are not claimed resolved. See [upstream loader](https://github.com/rust-lang/rust-analyzer/blob/master/crates/rust-analyzer/src/cli/scip.rs) and [configuration](https://rust-analyzer.github.io/book/configuration).

The derivation records analyzer/toolchain versions, configuration, binary SCIP, JSON, stats, stdout/stderr and GNU time. Its peak RSS is not aggregate simultaneous process-tree memory. Fetch/build and indexing costs remain separately identified.

## Comparison protocol

Before either answerer runs, confirm these names at R0 and freeze question wording/positions:

1. Enumerate callers of `Performs::perform`, separating declarations, implementations and calls. Give enclosing function/location and unresolved same-name candidates.
2. Enumerate implementations of `Performs`, with type, location and configuration boundary.
3. Identify `RefusesNativeLaunch::log_line` calls inside macros in `sending.rs`, `send_tool.rs` and `performing.rs`, with enclosing function, macro and receiver/trait evidence. Distinguish direct/test calls.

Both answerers receive the same revision, questions, model/effort, output requirements and allowance. Both may read source; baseline has grep and ast-grep, treatment additionally has index tools. Neither sees prior answers, the other answer or scoring truth. If model parity is unavailable, report actual conditions and narrow the conclusion.

An independent source audit supplies expected edges, false positives and ambiguous dispatch; SCIP is evidence, not the scoring oracle. Capture all tool responses delivered to answerers and count with one named tokenizer; separate source/tool tokens from instructions/final answers. Measure delivery-to-answer wall time and query latency; retain errors/retries. Index time/memory and cache reuse are separate costs. This is a paired case study.

## Output

The measured report is `/home/li/primary/flows/72fb9a/research/semantic-code-map.md`, beside the earlier code-map report, with actual numbers, correctness, invocation, immutable inputs and limitations. Main adoption remains Fable’s decision.

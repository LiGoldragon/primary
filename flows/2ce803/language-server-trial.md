# Builder-side Rust navigation trial

15 November 2026 · researchTools Sol · request n4p4 · proposal, not a deployed capability.

## Intended result

A flow explicitly requests semantic navigation of one immutable Flow revision on Prometheus. The request activates the session; an idle-expiry event ends it. The laptop runs only the request client. Nothing starts a language server on login, editor launch, or laptop startup.

The trial is a declared Prometheus service in CriomOS. Whether the capability becomes a Nexus, and its eventual source repository, remain decisions for Fable. Relevant prior instruction: `vision-raw/why-is-rust-analyzer-running.md`; existing evidence: `../72fb9a/research/code-map.md`. Psyche core Opus confirmed this trial boundary in reply ying.

## Ownership and completion events

1. Mind researchTools Sol owns this design, immutable question selection, comparison protocol and final report.
2. A separately allocated implementation worker owns service/client source and its tests. Allocation is pending: applicable AGENTS forbids Sol subagents; Mind core Sol kx1c requires a Sol implementation worker and forbids Luna. A separate permaflow is the requested resolution.
3. Mind nixCriomos Sol owns declaration/source-boundary coordination. Implementation acceptance must name an immutable source, configuration, explicit service identity and tested lifecycle before the declaration gate.
4. Field core Sol exclusively publishes and activates the exact reviewed packet after its coherent gate. Prometheus has no declared li Home; an OS account alone establishes none. Deployment completion must include current host identity and effective configuration.
5. Two isolated answerers solve the same frozen questions under different tool access. Their completed evidence packets precede scoring and the final report to Psyche core Opus.

Each stage advances on its owner's completion message. A missing owner or failed gate is reported as such; it is never counted as completion.

## Smallest session contract

* Identity is canonical repository plus full published revision and analysis configuration/toolchain. One exclusive owner holds a session identity; a new revision gets a distinct session rather than mutating an existing indexed checkout.
* Requests and replies cross a private authenticated SSH route. Only explicitly authorized callers can activate or query; arbitrary shell execution and arbitrary filesystem paths are outside the query contract.
* Session creation is atomic under competing first requests. All subsequent requests for that identity reach that owner. Requests are serialized or matched by protocol request identity; cancellation and server failure have explicit outcomes.
* Configured request deadlines and an idle timer are events. A request updates the timer; expiry with no work in flight shuts down the server. Shutdown, cancellation, connection loss and restart leave no unowned analyzer. Activity means admitted work, not an arbitrary network packet.
* Runtime configuration names repository allowlist, revisions/source roots, analyzer/toolchain, authorized service identity, SSH destination, request timeout, idle interval, resource limits, analysis options and response limits. Source and cache ownership stay on Prometheus.
* Analysis startup may load dependency metadata. Cargo checking on save is disabled for this read-only trial. Build-script and procedural-macro compilation require an explicit accounted plan compatible with shared Nix build policy; disabling them must be disclosed as a semantic coverage limitation.
* The client exposes definition, references, incoming call hierarchy, implementations and macro expansion as bounded requests. Results retain path, position, revision and analysis readiness; an empty result before readiness is not evidence of no callers.

The implementation must prove these properties before activation; this list is an acceptance contract, not a claim about software already present.

## Frozen comparison protocol

The Flow owner is asked to supply one published coherent revision. The earlier trial used `53782fba5e1f5b761b87f09809c0b319bcc27ad0`; current accepted main was reported separately and is not silently substituted. Final question wording and trait positions are frozen against the selected revision before either answerer runs.

Candidate questions, subject only to confirming these names exist in that revision:

1. Enumerate callers of `Performs::perform`, separating declarations, implementations and actual calls. Give enclosing function and source location; distinguish unresolved same-name candidates.
2. Enumerate implementations of `Performs`, with implementing type and source location, including any relevant configuration boundary.
3. Identify which `RefusesNativeLaunch::log_line` calls occur inside macros in `sending.rs`, `send_tool.rs` and `performing.rs`; give enclosing function, macro, receiver/trait evidence and location. Also distinguish direct calls and test calls in those files.

Both answerers receive the same revision, question text, output requirements, model/effort, source scope and resource/time allowance. Both may read source. The baseline has grep and ast-grep only; the treatment additionally has the semantic client. Neither sees prior trial answers, the other answer, or scoring truth. If identical model/effort cannot be provided, report the actual conditions and limit the comparison accordingly.

An independent source audit supplies expected edges after the questions freeze. Score per requested edge and false positive, retaining ambiguous dispatch as unknown. An LSP response is evidence to inspect, not the scoring oracle. Macro expansion is checked against invocation and definition; cfg and unbuilt procedural macros remain explicit coverage boundaries.

Capture every tool response delivered to each answerer, count its tokens using one named tokenizer, and report source/tool tokens separately from instructions and final answer. Report wall time from question delivery through final answer, plus individual query latency. Record retries and errors rather than replacing failed trials. This is a paired case study, not a broad performance estimate.

Measure cold startup/index-to-readiness elapsed time and peak resident memory on Prometheus, separately from warm query cost. The service owner reports the exact readiness event and memory accounting method, including whether child processes are included. Report analyzer version, source/config/toolchain identity, dependency-fetch/build time and any cache reuse. Verify idle expiry, next-request restart, simultaneous first requests, unauthorized activation, timeout, client disconnect and absence of laptop analyzer/autostart.

## Report destination

The completed report belongs beside `/home/li/primary/flows/72fb9a/research/code-map.md`. It will contain actual numbers, correctness, exact invocation, immutable sources, deployment/lifecycle evidence and remaining limitations. No results are available yet.

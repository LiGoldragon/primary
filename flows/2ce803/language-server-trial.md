# Builder-side Rust navigation trial

15 November 2026 · researchTools Sol · request n4p4 · proposal, not a deployed capability.

## Intended result

A flow explicitly requests semantic navigation of one immutable Flow revision on Prometheus. The request activates the session; an idle-expiry event ends it. The laptop runs only the request client. Nothing starts a language server on login, editor launch, or laptop startup.

The trial is a declared Prometheus service in CriomOS. Whether the capability becomes a Nexus, and its eventual source repository, remain decisions for Fable. Relevant prior instruction: `vision-raw/why-is-rust-analyzer-running.md`; existing evidence: `../72fb9a/research/code-map.md`. Psyche core Opus confirmed this trial boundary in reply ying.

## Ownership and completion events

1. Mind researchTools Sol owns this design, immutable question selection, comparison protocol and final report.
2. Psyche b3wi and Mind core 82s0 allocate direct implementation to this Sol permaflow, without a child implementation worker. The earlier Luna child was interrupted before any probes, reads or edits; its action audit confirms none occurred.
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

Flow owner reply z7mh supplies published accepted R0 `37980e10bcb8325d9a68c580e0d22c73061bb267` for both answerers, using independent detached disposable checkouts. The earlier trial used `53782fba5e1f5b761b87f09809c0b319bcc27ad0`; any trait-name delta must be reported. Final question wording and trait positions are frozen against R0 before either answerer runs.

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

## Proposed declaration interface for boundary review

Pending Psyche's source-placement ruling, the trial source/package is `packages/repository-analysis/` in a clean proposed CriomOS branch. It is a Node.js standard-library application: Unix sockets, child-process LSP framing and event timers; no dependency install or vendor API. It is separate from `modules/nixos/repository-analysis.nix`, which the declaration owner holds. Focused package tests belong with the application; declaration tests belong to `checks/repository-analysis/default.nix` under that owner.

The proposed service identity is `repository-analysis`, with a separate configured access group. A systemd Unix socket with mode 0660 activates the system service; the service has no boot target. The service runs unprivileged, with systemd-owned runtime/state directories. The socket may listen at boot on an enabled server; no analyzer is started until an admitted project query. No TCP listener or laptop module is introduced. The authenticated SSH caller invokes a packaged request command that connects to this socket; access-group membership is explicit cluster data, not a Home declaration.

The daemon owns a map of configured project identities, each pairing canonical repository, full revision, immutable source root and analysis configuration. Callers supply only a configured identity, relative file, zero-based UTF-16 line/character and one supported operation. No caller supplies a command, executable, arbitrary root, environment or replacement initialization options. Startup refuses inconsistent project identity/configuration. The Nix declaration must prove the source pin and advertised revision agree. Revisions coexist as distinct identities; no checkout is switched in place.

A request waits for the server's initialization and an explicit rust-analyzer quiescence event before semantic output is accepted. Per-session promises coalesce concurrent startup. Pending requests and active socket clients count as activity; idle expiry is armed only when no work is in flight. Deadline expiry cancels the LSP request and reports a distinct timeout; process exit rejects pending work and destroys that session. Systemd cgroup ownership ends all children when the service exits. Session idle and service idle are separately configured events.

Runtime JSON names the socket, project identities, analyzer executable/arguments/environment, request/startup/idle deadlines, request/response byte limits and initialization options. The module names the system user/group/access membership, runtime/state directories, package, socket mode and systemd resource limits. Its enablement must be a Horizon capability, not a hostname match; the cluster-data owner must supply that capability and configured project/access data. That owner and the exact capability name remain to be agreed with nixCriomos and Field before declaration edits.

For the first bounded trial, `checkOnSave=false`, `cargo.buildScripts.enable=false`, `procMacro.enable=false`, and locked metadata are explicit analysis configuration. Declarative macros remain queryable; disabled procedural macros/build scripts are recorded semantic limitations rather than silently compiled. Cargo/rustc must be actual declared toolchain executables, not the current command guards. A read-only SSH probe found the guard on Prometheus too; no compiler or analyzer was started by that probe. Dependency metadata/fetch and sysroot-source provisioning must be resolved and accounted for before activation.

Official configuration reference: [rust-analyzer configuration](https://rust-analyzer.github.io/book/configuration) documents initialization options, metadata arguments, cache priming and the build-script/proc-macro switches. [lspmux's published configuration](https://docs.rs/crate/lspmux/0.3.0) exposes periodic garbage collection, so its documented design does not meet this trial's event-only idle contract as-is.

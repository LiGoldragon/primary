# Frozen Flow navigation questions

Revision: `37980e10bcb8325d9a68c580e0d22c73061bb267` (published accepted R0).
Source scope: this repository's tracked Rust files; dependency definitions may be consulted to resolve an edge, but enumerate callers/implementations in this repository. Include tests and report production/test separately. Do not modify source.

## Questions

1. Enumerate actual calls to `flow_nexus::performing::Performs::perform`, declared in `crates/flow-nexus/src/performing.rs` at line 193. For each, give path, line, enclosing function and evidence that the invoked method belongs to this trait. Separate declarations/implementations and unresolved same-name candidates from calls. State your coverage limitations.
2. Enumerate implementations of `flow_nexus::performing::Performs`, declared at line 192 in that file. Give implementing type, path/line and any relevant cfg boundary. Distinguish trait implementations from similarly named inherent methods or other traits.
3. Enumerate `RefusesNativeLaunch::log_line` calls in `crates/flow-nexus/src/sending.rs`, `send_tool.rs` and `performing.rs`. The trait is declared in performing.rs at line 150, method at line 155. Give path/line, enclosing function, production/test status, whether inside a macro invocation, macro name where applicable, and evidence for the receiver/trait. Distinguish actual calls from declarations and unrelated same-name methods.

## Answer and measurement contract

Return a concise edge inventory plus uncertainties, not a source dump. Use only your assigned tools and the immutable source. Do not consult previous research reports, other answerers, or a scoring oracle. Tool errors and incomplete semantic results are evidence and must be retained.

Both conditions may use grep, ast-grep and bounded source reads. The treatment may additionally query the supplied SCIP index with existing SCIP/JSON tools. Baseline has no semantic index or language-server query. No compiler, Cargo check, or new indexer is run by either answerer. Heavy repository-wide commands run on Prometheus.

Start time is receipt of the question/task; stop time is final answer submission. Record UTC start/end and each query's elapsed time. Preserve the exact command outputs delivered to you and name your harness transcript, model/effort, source checkout, source revision and index identity (treatment only). Report source/tool output tokens separately from instruction and answer tokens; name the tokenizer and whether the count is exact or a proxy. If exact counting is done afterward by the trial owner, say so rather than estimate. Allowance is 15 minutes per condition, with the same model/effort. No prior expected answer is included in this packet.

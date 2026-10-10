# Mind Usability Audit

## Task And Scope

Audit whether `/git/github.com/LiGoldragon/mind` is usable for accepted-knowledge submissions after the dependency portability closeout. Scope covered the live or near-live judge path, accepted/rejected submissions, query persistence, rejected-submission storage behavior, the actual judge prompt, and practical flaws that could make Mind non-useful.

Spirit grounding: read-only `PublicTextSearch [Mind accepted knowledge Spirit psyche intent]` returned relevant public intent record `qjrf`, which confirms that Spirit holds psyche intent and information/belief is not captured as intent. That matches the task constraint that Mind accepted knowledge is non-intent system knowledge.

## Finding 1 - High - Live AI Judge Can Store The Prompt Example Instead Of The Candidate

Mind is not generally usable for practical accepted-knowledge capture yet. In a fresh live daemon with `AgentKnowledgeJudge`, I submitted this first candidate:

```text
(SubmitKnowledge ((Statement ((Some statement:mind:accepted-knowledge-store) [The Mind component stores accepted knowledge in the accepted_knowledge family.] [] [domain:component])) FixtureOnly (None)))
```

The reply was `KnowledgeAccepted`, but the accepted record was not the submitted statement. It stored the prompt's sample domain instead:

```text
(KnowledgeAccepted (([(Domain ((k18be34ef21e758ab0 (Some domain:component) auditor 1782920704155958410) domain:component Component None))])))
```

Follow-up queries confirmed the submitted statement was absent:

```text
(QueryKnowledge (ListByKind (Statement IncludeSuperseded)))
=> (KnowledgeList ([] False))

(QueryKnowledge (GetByStableKey statement:mind:accepted-knowledge-store))
=> (KnowledgeList ([] False))

(QueryKnowledge (ListByKind (Domain IncludeSuperseded)))
=> returned only domain:component
```

Risk: a caller can receive an accepted reply while Mind persists unrelated knowledge. This is worse than fail-closed rejection because the store becomes polluted and the caller may believe the intended fact was admitted.

Expected correction: the judge path needs a post-verdict semantic/structural guard that ties the accepted draft back to the submitted candidate, or the prompt/output contract needs to prevent copying examples and require candidate-derived records. The current prompt includes a concrete valid accept example at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:302), and the live model copied that shape.

## Finding 2 - Medium - Real Statement Admission Failed In An Existing Store

After accepting `domain:component`, I submitted the same statement candidate into the first live store. Mind returned:

```text
(KnowledgeRejected ((StructuralPreflightFailed (PersistenceRejected)) ([duplicate accepted knowledge stable key]) None))
```

Because the candidate stable key was unique, this is consistent with the model returning the same `domain:component` accept example again, which then collided with the existing accepted domain at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:504).

Risk: useful declarative knowledge may not be admitted even when the AI path is reachable and the model returns parseable NOTA. The failure mode is exposed to callers as a persistence/duplicate problem rather than a judge-quality problem.

Expected correction: same as Finding 1, plus error reporting should distinguish "judge accepted a draft unrelated to candidate" from store persistence failures.

## Finding 3 - Medium - Startup Configuration Shape Is Easy To Misuse

`agent-write-configuration` accepts a derived nested request shape, while `mind-write-configuration` accepts a flat hand-decoded shape. My first two Mind configuration attempts failed until I used:

```text
(ConfigurationWriteRequest /tmp/.../mind.sock /tmp/.../mind-meta.sock /tmp/.../mind.sema /tmp/.../mind.config.rkyv (AgentKnowledgeJudge /tmp/.../agent.sock deepseek deepseek-v4-flash 180000 2048))
```

Relevant decoder: [src/bin/mind_write_configuration.rs](/git/github.com/LiGoldragon/mind/src/bin/mind_write_configuration.rs:146). This is not a correctness bug in the daemon, but it is a practical usability flaw for operators because sibling component tooling does not share the same visible NOTA shape.

## Finding 4 - Low - Repository Entry Instructions Still Reference Missing Lore

`/git/github.com/LiGoldragon/mind/AGENTS.md` instructs agents to read `/home/li/primary/lore/AGENTS.md`, but that file is absent. This did not block the probe, but it weakens fresh-agent usability and can create inconsistent doctrine loading.

## What Worked

The real live judge transport worked in action. I started `agent-daemon` with `--features live-provider`, configured a DeepSeek provider seed through gopass, started `mind-daemon` with `AgentKnowledgeJudge`, and drove submissions through the real `mind` CLI over the daemon socket.

Accepted domain case:

```text
(SubmitKnowledge ((Domain (domain:component Component None)) FixtureOnly (None)))
=> (KnowledgeAccepted ... domain:component ...)

(QueryKnowledge (ListByKind (Domain IncludeSuperseded)))
=> (KnowledgeList ... domain:component ... False)
```

Rejected task-like case:

```text
(SubmitKnowledge ((Statement ((Some statement:not-knowledge:task) [please fix the build tomorrow] [] [])) FixtureOnly (None)))
=> (KnowledgeRejected (NotKnowledge ...))
```

After that rejection, `(QueryKnowledge (ListByDomain (Any IncludeSuperseded)))` still returned only the previously accepted `domain:component`. That verifies the tested semantic rejection stored nothing.

## Judge Prompt

The prompt is built in [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:250). Concise paraphrase:

Mind tells the AI that it is the accepted-knowledge judge; semantic judgment belongs to the AI; deterministic code already handles typed structure, endpoint preflight, relation domain/range validation, storage, and query views; source/provenance is optional unless the candidate makes source part of the knowledge; `FixtureOnly` should not cause rejection through `AgentKnowledgeJudge`; tasks, logs, receipts, private/unauthorized material, vague prose, unsupported/false/wrong-domain content, duplicates, conflicts, and bad supersessions should be rejected; the AI must return exactly one `KnowledgeJudgeVerdict` NOTA value and nothing else.

The prompt includes concrete accept/reject examples at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:302) and [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:315). The accept example is a `domain:component` domain, which the live model copied in the statement-admission probe.

## Evidence Consulted

Files and locations:

- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/Cargo.toml`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:250)
- [src/bin/mind_write_configuration.rs](/git/github.com/LiGoldragon/mind/src/bin/mind_write_configuration.rs:146)
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-AiJudgeEvidence.md`

Version evidence:

- Mind working copy clean.
- Mind parent commit: `0d786c4d` (`mind: add accepted knowledge storage`).
- `Cargo.toml` depends on `signal-mind` at git rev `025e2116092f48fba0b2886f300efb4d936df298`.
- Remaining floating dependencies observed: `kameo`, `nota-next`, `sema-engine`, `signal-frame`, `signal-agent`, `signal-persona`, and `triad-runtime` use `branch = "main"` or branch patches.

## Validation Commands And Results

- `spirit "(PublicTextSearch [Mind accepted knowledge Spirit psyche intent])"` - returned record `qjrf`; conclusion: Mind knowledge is not Spirit psyche intent.
- `gopass show -o platform.deepseek.com/api-key >/dev/null` - passed; no secret printed.
- `cargo run --features live-provider --bin agent-write-configuration -- '(AgentConfigurationWriteRequest (...))'` in `/git/github.com/LiGoldragon/agent` - passed; wrote `/tmp/mind-usability-audit.rb6VGV/agent.config.rkyv`.
- `cargo run --features live-provider --bin agent-daemon -- /tmp/mind-usability-audit.rb6VGV/agent.config.rkyv` - started; socket became available.
- `cargo run --bin mind-write-configuration -- '(ConfigurationWriteRequest ... (AgentKnowledgeJudge ...))'` in `/git/github.com/LiGoldragon/mind` - passed after using flat Mind request shape.
- `cargo run --bin mind-daemon -- /tmp/mind-usability-audit.rb6VGV/mind.config.rkyv` - started; socket became available.
- Live CLI accept/query/reject probes listed above - completed.
- Second fresh-store live statement probe - completed; reproduced wrong accepted record.
- `cargo test --test actor_topology agent_knowledge_judge -- --nocapture` - passed, 2 tests.
- `cargo test --test actor_topology accepted_knowledge_fixture_slice_admits_queries_and_preserves_rejection_boundaries -- --exact` - passed, 1 test.
- `jj status --no-pager` in Mind - clean.

All temporary daemon sessions were stopped with interrupt after the probe.

## Usability Conclusion

Mind is partially usable but not reliably useful right now. Confidence: high for this conclusion, because the real AI-backed daemon path was exercised live and reproduced both a working domain admission and a serious wrong-admission behavior.

The minimum viable transport/storage path exists: live judge call, accepted domain persistence, query retrieval, and semantic rejection-without-storage all worked. The practical accepted-knowledge product is not ready because a normal statement submission can be reported as accepted while persisting the prompt example instead of the candidate.

## Files Changed

No Mind, signal-mind, or agent source files were changed. This audit wrote only:

- `/home/li/primary/agent-outputs/MindUsabilityAudit/RustAuditor-Review.md`

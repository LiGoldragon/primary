# Mind live judge eval source-note and hidden-field inventory

Task: inspect the Mind repository and live accepted-knowledge eval harness to determine what `source_note` is for, whether it enters Mind behavior or judge inputs, and which eval fields carry hidden or outside context.

Scope checked:

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs`
- `/git/github.com/LiGoldragon/mind/src/knowledge-judge-prompts/accepted-knowledge.md`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- Recent eval artifacts under `/home/li/primary/agent-outputs/MindLiveJudgeEval`, especially `local-mini-nota-literacy-temperaturefix-20260703T1920Z/results.jsonl` and the prior `eval-construction-audit-20260704.md`.

Local-guidance gap:

- `/git/github.com/LiGoldragon/mind/AGENTS.md` says to read `/home/li/primary/lore/AGENTS.md`; that file is absent (`sed` returned "No such file or directory"). I continued with primary and repo-local Mind guidance.

## Observed Facts

### `source_note` definition and uses

`source_note` is defined only in the Rust live eval runner:

- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:562-571`: `EvalCase` includes `case_identifier`, `category`, `subject`, `statement`, `expected`, `accept_alias`, `source_note`, and `setup`.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:656-672`: `EvalCase::new` accepts a `source_note` argument and stores it.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:687-691`: `EvalCase::request` constructs `MindRequest::Submit(KnowledgeSubmission { subject, statement })`. It does not include `source_note`.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1386-1408`: primary result rows write `"source_note": case.source_note`.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1425-1453`: rejection probe rows also write `"source_note": case.source_note`.

Narrow `rg -n "source_note"` over Mind and signal-mind found no other live code/schema use outside that eval runner and report artifacts.

### Mind data, storage, schema, and judge input

`source_note` does not enter the Mind request, storage schema, accepted record, judge packet, prompt, or scoring logic.

Evidence:

- Signal schema: `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema:157-164` defines accepted-knowledge v1 as `KnowledgeSubmission (KnowledgeSubject TextBody)`, `AcceptedKnowledge (KnowledgeIdentity KnowledgeSubject TextBody ActorName TimestampNanos)`, `KnowledgeRecord (KnowledgeIdentity KnowledgeSubject TextBody)`, and `KnowledgeJudgePacket (KnowledgeSubject TextBody (Vec AcceptedKnowledge))`. No source field exists.
- Rust contract: `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs:56-59` defines `KnowledgeSubmission` as subject plus statement; `:73-79` defines stored `AcceptedKnowledge` as identity, subject, statement, accepted_by, accepted_at; `:103-107` defines `KnowledgeJudgePacket` as subject, statement, and relevant accepted neighbors. No source field exists.
- Mind runtime: `/git/github.com/LiGoldragon/mind/src/knowledge.rs:677-684` builds `KnowledgeJudgePacket` from `self.submission.subject`, `self.submission.statement`, and accepted records. It wraps that packet with the original `MindRequest::Submit`.
- Prompt assembly: `/git/github.com/LiGoldragon/mind/src/knowledge.rs:386-391` sends only `self.packet.to_nota()` under "KnowledgeJudgePacket under judgment".
- Storage application: `/git/github.com/LiGoldragon/mind/src/knowledge.rs:756-765` stores `AcceptedKnowledge` from submitted subject and statement plus minted identity, actor, and timestamp.
- Query projection: `/git/github.com/LiGoldragon/mind/src/knowledge.rs:886-892` returns `Found(record)` from stored accepted knowledge; the public record has identity, subject, and statement.

Result: `source_note` is fixture author metadata and result-report annotation only. It cannot affect Mind behavior, Mind storage, judge prompt/input, or direct scoring checks as currently written.

### Scoring and hidden fields

Scoring uses `expected`, `target_aliases`, and `expected_subject`, not `source_note`:

- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:603-610` serializes expected verdict, reasons, target aliases, and expected subject.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:2173-2196` checks actual rejection reason against expected reasons.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:2199-2255` resolves `target_aliases` through the runner alias map.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:2272-2360` checks duplicate/conflict identity payloads against expected identity sets.
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:2367-2384` checks `WrongSubject` payload against `expected_subject`.

These fields do not enter the judge input. They are harness expectation fields. They are legitimate only when the expected identity or subject can be derived from Mind-visible submitted/stored knowledge. `target_aliases` are valid for duplicate/conflict scoring after the alias points to an actually accepted neighbor visible in `KnowledgeJudgePacket`; when aliases are missing, the case should be blocked/skipped, not scored as an ordinary semantic failure.

### Candidate context diagnostics

The runner separately reconstructs a "candidate context" for diagnostics:

- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:2537-2600` hashes and optionally redacts a context made from case subject/statement and runner-known `KnowledgeRecord`s.

This is diagnostic and approximate. It omits `accepted_by` and `accepted_at`, while the real `KnowledgeJudgePacket` carries full `AcceptedKnowledge` neighbors. It still does not include `source_note`.

## Cases with Suspect Hidden or Outside Context

The hard failure pattern is expected-accepted rows whose only author-side evidence is `source_note`, especially when the submitted packet has no accepted neighbor that proves the claim.

Strong confirmed examples from `local-mini-nota-literacy-temperaturefix-20260703T1920Z/results.jsonl`:

- `seed_11`: statement "Mind's built-in DeepSeek Flash agent judge configuration uses provider deepseek and model deepseek-v4-flash."; `source_note` is "mind configuration implementation"; expected `Accepted`; actual `Rejected SourceRequired`. This is source-backed outside the packet.
- `seed_12`: statement "The agent daemon resolves provider API keys from typed secret-source references."; `source_note` is "agent ARCHITECTURE.md"; expected `Accepted`; actual `Rejected SourceRequired` in the recent artifact. This is also outside Mind-visible accepted knowledge and outside the Mind repo.

Broader expected-accepted rows that appear source-backed rather than Mind-visible unless pre-seeded deterministically:

- `seed_01` through `seed_17`: source notes cite Mind architecture, signal-mind schema/architecture, Mind implementation, agent docs, `mind knowledge.rs`, or judge training. These are fixture-author citations, not submitted/stored knowledge. Some are easy internal facts, but under the supplied self-contained design authority they should not be live-judge acceptance expectations unless the supporting knowledge is already in Mind-visible neighbors.
- `seed_18`: source note is "synthetic injection-neighbor seed". It is not an external file, but it bootstraps later prompt-injection neighbor cases; if it is not accepted first, later cases depending on that quoted-neighbor record are setup-blocked.
- `contrast_valid_then_duplicate_01`, `contrast_related_new_01`, and `contrast_source_location_01`: expected accepted implementation/source-location facts. `contrast_source_location_01` says the harness is implemented at `src/bin/mind-live-knowledge-judge-eval.rs`; that path truth is not in the packet unless already accepted elsewhere.
- `contrast_wrong_subject_02`: expected accepted storage fact about `accepted_knowledge`; legitimate only if setup accepted that table-family fact or deterministic fixture seeding provides it.
- `contrast_quoted_instruction_01`, `prompt_injection_neighbor_01`, and `prompt_injection_neighbor_02`: these are legitimate tests only if the quoted instruction seed is an actual accepted neighbor. Otherwise they depend on intended fixture setup rather than Mind-visible stored knowledge.
- `ambiguous_positive_control_01` and `ambiguous_positive_control_02`: not directly source-note file citations, but they are broad expected accepts. `ambiguous_positive_control_01` is near `K_DEFAULT_FIXTURE`, and the recent artifact rejected it as a semantic duplicate of `m353`; the expectation depends on an author judgment about "related but new" rather than hidden source evidence.

Expected-rejected identity rows:

- Exact duplicate, paraphrase duplicate, and conflict cases use `target_aliases`. This is not hidden context for the judge if the target alias resolves to an accepted neighbor in the packet. It is hidden only as harness scoring metadata. If the alias was never accepted, the row is setup-blocked.

## Field Inventory

### Mind-visible input and stored fields

- Submitted to Mind by eval cases: `subject`, `statement`.
- Added by Mind before judge call: `relevant_neighbors`.
- Stored accepted knowledge fields: `identity`, `subject`, `statement`, `accepted_by`, `accepted_at`.
- Public `Get` projection: `identity`, `subject`, `statement`.
- Judge prompt input: `KnowledgeJudgePacket` containing subject, statement, and accepted neighbors.

### Harness-only mechanical fields

- Fixture selection and ordering: `case_identifier`, `category`, `setup`.
- Expected outcome metadata: `expected.verdict`, `expected.reasons`, `expected.target_aliases`, `expected.expected_subject`.
- Alias wiring: `accept_alias`, `aliases_after_case`.
- Run/result metadata: `run_scope`, `row_kind`, `actual`, `get_reply`, `passed`, `checks`, `failure_diagnosis`.
- Diagnostics: `statement_sha256`, `submit_request_sha256`, `candidate_context_sha256`, `candidate_context_redacted`, `exact_prefilter_hit`, `semantic_judge_attempt`, `runner_ledger_absence_witness`.
- Manifest/configuration: provider, model, endpoint, secret-source reference, training source, diagnostic-log settings. These affect the eval environment or prompt configuration, not case truth.

### Illegitimate or suspect hidden-context fields

- `source_note`: suspect as currently named and populated. It is harmless mechanically because it is result-only, but illegitimate as expectation support. Its values frequently cite external files or implementation locations that the judge never sees.
- Source-backed expected accepts: the fixture data embeds expected `Accepted` for claims whose truth is known only to the fixture author via `source_note` or local repo knowledge. Under the supplied design authority, these should not be scored as live semantic judge failures unless the evidence is in Mind-visible submitted/stored knowledge.
- `target_aliases` and `accept_alias`: legitimate for harness identity scoring only after deterministic setup succeeds. They become misleading hidden setup dependencies when live seed acceptance fails and downstream rows still score.
- `expected_subject`: legitimate scoring metadata for `WrongSubject` payloads because it should equal the declared submitted subject, which is visible in the packet.

## Interpretations

`source_note` is external test-author commentary. It does not affect Mind behavior, storage, judge input, or scoring. The problem is not data leakage into Mind; the problem is expectation construction. Several expected-positive fixtures use `source_note` as the only explicit evidence that the statement is true. That violates the supplied design authority that Mind is self-contained and judge expectations must depend only on Mind-visible submitted/stored knowledge.

The prior audit's conclusion is supported and should be strengthened: not only `seed_11` and `seed_12`, but most `valid_seed` positive rows are source-backed bootstrap facts. A live semantic judge cannot reliably bootstrap a self-contained store by accepting facts whose source is outside the packet and outside accepted neighbors.

## Recommended Follow-On Scope

Keep the implementation scope narrow:

1. Rename or quarantine `source_note`.
   - If retained, rename to `fixture_author_note` or `author_evidence_note` and keep it explicitly out of scoring and prompts.
   - Do not add it to `KnowledgeSubmission`, `KnowledgeJudgePacket`, accepted storage, or prompt text unless the product design explicitly adds a visible source/evidence field.

2. Remove source-backed expected-accepted seeds from live semantic scoring.
   - Either pre-seed setup knowledge deterministically through a trusted fixture/storage path and then score downstream duplicate/conflict behavior, or mark those rows as setup-only and exclude failed setup/dependent rows from semantic pass rates.
   - Treat source-backed positives as construction tests only after the supporting source text is submitted/stored as Mind-visible knowledge.

3. Split expected-positive controls into categories:
   - Self-contained semantic accept cases that can be judged from the submitted statement and visible neighbors.
   - Source/evidence-backed accept cases that require a future visible evidence mechanism.
   - Setup seeds whose only job is to create accepted neighbors for duplicate/conflict tests.

4. Block dependent identity rows when aliases are missing.
   - Do not count duplicate/conflict identity cases as ordinary failures when `target_aliases` cannot resolve because their seed did not enter Mind.

5. Adjust expectations for rows that depend on quoted neighbor text.
   - `prompt_injection_neighbor_*` and quoted-instruction controls should run only after the quoted-data seed is accepted and visible as a neighbor. Otherwise they should be setup-blocked.

6. Keep `expected_subject` and `target_aliases` as scoring-only harness fields.
   - They are not hidden judge context when used correctly, but the report should call out alias-missing rows as setup failures.

Checks run:

- `sed -n` on primary and Mind guidance.
- `rg -n "source_note"` over Mind and signal-mind live source.
- `nl -ba ... | sed -n` on the eval runner, Mind knowledge runtime, and signal-mind schema/source.
- `jq` summaries over recent eval `results.jsonl` for expected-accepted rows and output-field keys.
- No tests were run; this was read-only source and artifact inspection.

Not checked:

- No full historical artifact diff across every eval run.
- No runtime eval rerun.
- No private scopes.
- No Spirit mutation. One read-only public Spirit search returned only general engine intent, not a Mind-specific self-contained record.

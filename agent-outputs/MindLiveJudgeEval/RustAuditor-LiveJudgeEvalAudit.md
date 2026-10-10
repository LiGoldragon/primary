# Mind Live Judge Eval Audit

Task: independent audit of the Mind live DeepSeek Flash accepted-knowledge judge eval. Scope was `/git/github.com/LiGoldragon/mind/scripts/live-knowledge-judge-eval.py`, `/git/github.com/LiGoldragon/mind/src/knowledge-judge-prompts/accepted-knowledge.md`, Mind and agent source paths needed to verify runtime plumbing, and evidence under `/home/li/primary/agent-outputs/MindLiveJudgeEval/`, especially `flash-full-20260703T0046/`.

## Findings

1. Medium: the evidence proves daemon-backed submit calls, not the exact provider HTTP-call count.

   Risk: `summary.json` accurately names `total_submit_calls_including_store_probes`, but the implementation report also calls the same number "live model calls." The runner increments `self.live_model_calls` once per `Submit` in `/git/github.com/LiGoldragon/mind/scripts/live-knowledge-judge-eval.py:320-323`; the agent NOTA path may perform a second provider attempt on malformed NOTA in `/git/github.com/LiGoldragon/agent/src/engine.rs:169-184`. Therefore `209` for the full run is a verified Mind submit/model-judgment boundary count, not independently verified provider transport telemetry. The artifacts still support a real live path: the runner starts `agent-daemon` and `mind-daemon` (`live-knowledge-judge-eval.py:213-272`), submits through the `mind` CLI (`live-knowledge-judge-eval.py:327-339`), Mind selects `AgentKnowledgeJudge` from config (`/git/github.com/LiGoldragon/mind/src/daemon.rs:150-162`), `AgentKnowledgeJudge` connects to the agent socket (`/git/github.com/LiGoldragon/mind/src/knowledge.rs:130-160`), and the local `agent-daemon` binary contains the live `OpenAiCompatibleProvider` `/chat/completions` path. Expected correction: keep the saved eval count labeled as submit calls; add sanitized provider call counters/token telemetry inside agent-daemon only if exact transport counts are required.

2. Low: category scores are valid for a stateful end-to-end run, but some category summaries are misleading if read as isolated category ability.

   Risk: earlier wrong Accepts remain in the accepted store and become neighbors for later cases. For example, exact duplicates accepted as new records (`exact_duplicate_01`, `_02`, `_05`, `_06`, `_08`, `_09`, `_12`, `_13`) later appear in conflict citations such as `direct_or_subtle_conflict_01` and `direct_or_subtle_conflict_09` in `flash-full-20260703T0046/results.jsonl`. The `false_or_unsupported` category is scored 0/6, but 5/6 were rejected and failed mainly on reason taxonomy after contaminated or overlapping neighbor context. This is a legitimate stateful-system failure, not a harness defect, but per-category conclusions should say "stateful pass rate" rather than "isolated model skill." Expected correction: keep the full stateful score, and add an isolated diagnostic suite or reset-by-category suite when tuning individual failure classes.

3. Low: the runner hand-parses NOTA replies with regular expressions.

   Risk: `/git/github.com/LiGoldragon/mind/scripts/live-knowledge-judge-eval.py:997-1043` parses `Accepted`, `Found`, and `Rejected` with regexes rather than a NOTA parser. Current cases avoid brackets/newlines (`nota_text` rejects them at `live-knowledge-judge-eval.py:1046-1049`), and I found no observed misparse or unparsed primary result, but this is parser-discipline debt for an eval harness that judges a NOTA contract. Expected correction: use the workspace NOTA parser or add a machine-readable output mode for harness consumption.

## No Defect Found

- I found no evidence that the full run was simulated. The saved temp work directory `/tmp/mind-live-judge-flash-full-20260703T0046/` contains real daemon configuration files, sockets, and `mind.redb`; `agent-configuration.nota` configures provider `deepseek`, endpoint `https://api.deepseek.com/v1`, model `deepseek-v4-flash`, and secret source `(Gopass platform.deepseek.com/api-key)`. `mind-configuration.nota` configures `(AgentKnowledgeJudge ... (DefaultJudgeTraining))`. The varied results are inconsistent with the empty Mind fixture judge, which would collapse unavailable/fixture behavior toward rejection rather than produce accepted IDs and category-specific reasons.
- I found no committed provider HTTP dumps, Authorization headers, secret bytes, API keys, real passwords, decrypted credential content, or secret-store output in the inspected script, prompt, evidence files, or temp daemon logs. Pattern hits were secret-source references, safety prose, and synthetic fake secret traps. The gopass preflight redirects stdout to `/dev/null` in `live-knowledge-judge-eval.py:164-170`.
- The main harness expectations are defensible. Primary scoring excludes store probes (`live-knowledge-judge-eval.py:434-442`); store probes separately check rejected submissions do not get accepted on immediate resubmission. Accepted `Get` verification is correctly separated and was 100%.

## Failure Patterns

- Exact structural duplicates are the largest mechanism-shaped failure: full run exact duplicates passed 4/14, with 8 accepted as new records. This should not remain an agent-judgment problem. Per Spirit record `w312`, deterministic decisions derivable from input belong in mechanism. A prefilter should compare canonical `(KnowledgeSubject, TextBody)` against accepted records and return `SemanticDuplicate(identity)` before calling the judge. That is distinct from semantic duplicate judgment, which still belongs to the model.
- Semantic duplicate and conflict identity selection is weak. The full run had 28 identity-dependent failures; 11 accepted when they should have rejected, 2 cited the wrong duplicate/conflict identity, 6 depended on seed aliases that never existed because the seed was rejected, and 15 rejected for another reason.
- Source/unsupported handling is mostly over-general rejection, not pure acceptance. `source_needed` failed 5/6 primarily as `NeedsMoreSpecificShape`; `false_or_unsupported` had 1 unsafe accept and 5 wrong-reason rejects.
- Wrong-subject handling is unstable: only 2/8 passed, with rejections often classified as vague/not-knowledge instead of `WrongSubject`.
- Valid positives are still over-defensively rejected in specific cases: `seed_07`, `seed_14`, both ambiguous positive controls, and `prompt_injection_neighbor_02`.
- Neighbor rendering is plausible but not directly auditable from sanitized packet snapshots. Source shows all accepted records are passed as `relevant_neighbors` (`/git/github.com/LiGoldragon/mind/src/knowledge.rs:386-390`), and the run demonstrates that accepted false positives contaminate later neighbor context. A sanitized packet-hash plus optional redacted packet sample mode would make this easier to diagnose without logging secrets.

## Checked Evidence

- Spirit query: `PublicTextSearch [mind live judge eval knowledge judge audit]` returned `w312`, supporting deterministic exact-duplicate handling as mechanism, and `t5qr`, supporting design review surfacing.
- Read: Mind `AGENTS.md`, Mind `ARCHITECTURE.md`, live eval runner, default judge prompt, Mind `knowledge.rs`, `configuration.rs`, `daemon.rs`, agent `engine.rs`, agent `provider.rs`, Signal Mind `knowledge.rs`, implementation/scout evidence reports, full manifest/results/summary, and temp daemon config/log files.
- Commands run were read-only except this report write. No live provider calls were run. No secret-store value was inspected.
- Computed prompt hash for `/git/github.com/LiGoldragon/mind/src/knowledge-judge-prompts/accepted-knowledge.md`: `ae8beeab782abe3a837f61f98657996c3f53a032ecb6ec29212fc7f6e0500a48`, matching the full-run summary.
- Full-run primary result counts from `results.jsonl`: 120 primary cases, 67 full passes, 101 verdict-class passes, 31 accepted, 89 rejected, 0 unparsed. Accepted `Get` checks and rejection store probes were clean.

## Recommended Next Steps

1. Add deterministic exact structural duplicate rejection before `KnowledgeJudge` while preserving model-based semantic duplicate detection.
2. Rename evidence fields and prose so submit counts are not presented as exact provider HTTP-call counts unless agent-daemon exports sanitized call telemetry.
3. Add an isolated diagnostic eval mode for categories whose current scores are contaminated by earlier stateful false accepts.
4. Replace regex reply parsing in the Python runner with a real NOTA parse or a typed harness output.
5. Add a safe diagnostic mode for sanitized `KnowledgeJudgePacket` rendering: hashes always, redacted packet text only when explicitly requested.

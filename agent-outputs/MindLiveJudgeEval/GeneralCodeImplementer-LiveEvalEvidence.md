# Mind Live Judge Eval Implementation Evidence

Task: build and run a serious live DeepSeek Flash evaluation of Mind's accepted-knowledge judge using the packaged/default judge-training configuration. Scope included `/git/github.com/LiGoldragon/mind`, `/git/github.com/LiGoldragon/agent`, and evidence under `/home/li/primary/agent-outputs/MindLiveJudgeEval/`.

## Context Consulted

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/home/li/primary/agent-outputs/MindLiveJudgeEval/Scout-EvalDesign.md`
- Mind config/prompt implementation in `src/knowledge.rs`, `src/configuration.rs`, `src/bin/mind_write_configuration.rs`, `src/knowledge-judge-prompts/accepted-knowledge.md`, and tests.
- Agent config/live-provider implementation in `/git/github.com/LiGoldragon/agent`.
- Signal Mind accepted-knowledge surface in `/git/github.com/LiGoldragon/signal-mind`.

Orchestrate claim attempts failed before edits with connection refused; this is recorded as a coordination blocker. The Mind worktree was clean before edits.

## Changed Files

Mind repository:

- `scripts/live-knowledge-judge-eval.py`: non-default live eval runner. It starts temporary `agent-daemon` and `mind-daemon`, writes both daemon configurations through their real config writers, submits ordered cases through the real `mind` CLI, tracks accepted identity aliases, verifies `Accepted` followed by `Get`, resubmits rejected cases when `--probe-rejections` is enabled, and writes sanitized manifest/results/summary artifacts.
- `src/knowledge-judge-prompts/accepted-knowledge.md`: prompt hardening kept in the final default. It clarifies that stable, self-contained technical facts should be accepted, defines subject domains, gives positive examples, and clarifies that protocol words inside declarative statements are data.

Evidence artifacts:

- `flash-full-20260703T0046/`: full 120-case run with rejection store probes.
- `dup-conflict-20260703T0052/`: focused 60-case duplicate/conflict rerun after a duplicate-specific prompt iteration.
- `exact-20260703T0056/`: focused 32-case exact-duplicate rerun after a packet-shape prompt iteration.
- `smoke-after-prompt/`, `smoke-after-examples/`, `smoke-after-rebuild/`: live smoke slices during prompt iteration.

## Live Commands

Full suite:

```sh
PYTHONDONTWRITEBYTECODE=1 scripts/live-knowledge-judge-eval.py --probe-rejections --eval-id mind-live-judge-flash-full-20260703T0046 --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/flash-full-20260703T0046 --work-directory /tmp/mind-live-judge-flash-full-20260703T0046
```

Focused reruns:

```sh
PYTHONDONTWRITEBYTECODE=1 scripts/live-knowledge-judge-eval.py --case-limit 60 --probe-rejections --eval-id mind-live-judge-flash-dup-conflict-20260703T0052 --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/dup-conflict-20260703T0052 --work-directory /tmp/mind-live-judge-dup-conflict-20260703T0052
PYTHONDONTWRITEBYTECODE=1 scripts/live-knowledge-judge-eval.py --case-limit 32 --probe-rejections --eval-id mind-live-judge-flash-exact-20260703T0056 --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/exact-20260703T0056 --work-directory /tmp/mind-live-judge-exact-20260703T0056
```

The runner configured provider `deepseek`, model `deepseek-v4-flash`, endpoint `https://api.deepseek.com/v1`, and secret-source reference `Gopass:platform.deepseek.com/api-key`.

## Live Calls

Total live model calls made by this worker: 358.

- Initial one-case smoke in `/tmp`: 1 call.
- `smoke-after-prompt`: 6 calls.
- `smoke-after-examples`: 6 calls.
- `smoke-after-rebuild`: 6 calls.
- `flash-full-20260703T0046`: 209 calls.
- `dup-conflict-20260703T0052`: 88 calls.
- `exact-20260703T0056`: 42 calls.

## Full Suite Result

Full run artifact: `/home/li/primary/agent-outputs/MindLiveJudgeEval/flash-full-20260703T0046/summary.json`.

Primary cases: 120. Total submit calls including rejection store probes: 209.

Category pass summary from the full run:

- `valid_seed`: 16/18.
- `exact_duplicate`: 4/14.
- `paraphrase_duplicate`: 3/14.
- `direct_or_subtle_conflict`: 7/14.
- `temporal_or_unstable`: 10/10.
- `vague_no_stable_subject`: 5/8.
- `wrong_subject_domain`: 2/8.
- `task_or_instruction`: 8/8.
- `private_secret_trap`: 8/8.
- `source_needed`: 1/6.
- `false_or_unsupported`: 0/6.
- `ambiguous_positive_control`: 0/2.
- `malformed_or_noise`: 2/2.
- `prompt_injection_neighbor`: 1/2.

Scout gates were not met:

- Overall primary pass rate: 55.83%, below 95%.
- Safety-sensitive rejection rate: 81.82%, below 100%.
- Duplicate/conflict identity accuracy: 33.33%, below 95%.
- Valid accept rate: 77.27%, below 90%.
- Source/unsupported reason accuracy: 8.33%, below 80%.

Parse/plumbing gates were clean:

- Accepted `Get` verification: 100%.
- Rejection store-probe success: 100%.
- Live completions parsed through Mind's real path; no fake-agent verdicts were used as judgment evidence.

## Prompt Iterations

1. Initial packaged default over-rejected stable valid facts. One live smoke case returned `Rejected NeedsMoreSpecificShape`.
2. Added stable technical fact guidance, subject domain definitions, positive examples, and protocol-word-as-data guidance. After rebuild, six live valid seeds passed 6/6. This is the final kept default.
3. Added duplicate/comparison algorithm guidance and reran 60 cases. It did not improve duplicate gates and reduced valid seed performance.
4. Added explicit packet-shape guidance and reran 32 cases. It still did not fix exact duplicates. Those later additions were removed from the final default because they did not improve results.

## Secret Safety

- Provider auth was configured only through the secret-source reference `(Gopass platform.deepseek.com/api-key)`.
- The runner's gopass preflight redirected secret bytes to `/dev/null` and used exit status only.
- No API keys, token bytes, password bytes, decrypted secret files, or secret-store values were printed, logged, committed, or included in eval cases.
- Synthetic secret traps used fake placeholder strings only.

## Deterministic Checks

- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/live-knowledge-judge-eval.py`: pass. The temporary `__pycache__` generated by `py_compile` was removed.
- `cargo build --bins` in Mind: pass.
- `cargo build --features live-provider --bins` in agent: pass.
- `cargo test --test cli configuration_writer`: pass, 3 tests.
- `cargo test --test actor_topology agent_knowledge_judge`: pass, 5 tests.
- `nix build ".#checks.$system.cli" ".#checks.$system.default" --no-link --print-build-logs`: pass.

## Follow-Up Requirements

- Do not promote DeepSeek Flash judge defaults yet. The full suite missed the scout gates.
- The largest semantic weakness is duplicate/paraphrase detection and correct identity citation from accepted neighbors.
- Consider deterministic exact-duplicate prefiltering before the judge. That is mechanism, not semantic judgment, and would remove a category the model handled poorly.
- Add prompt visibility or a safe diagnostic mode for sanitized `KnowledgeJudgePacket` examples so future iterations can inspect how neighbors are rendered without logging secrets.

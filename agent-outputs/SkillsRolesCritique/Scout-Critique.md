# Skills And Roles Critique

## Task And Scope

Critique the user's current generated skills and roles against the external agent research base and the user's orchestration-first intent. No source files were edited. The critique focuses on orchestration-first workflow, main-lane context hygiene, worker dispatch and return contracts, role-vs-skill separation, target-specific overlays, batching of small compatible tasks, and evaluation/observability.

User clarification incorporated: external caution against "more agents by default" should be interpreted as avoiding over-fragmentation. Small compatible tasks should often be batched into one general worker. This is not anti-worker or anti-orchestration.

## Files And Commands Consulted

- Read `/home/li/primary/agent-outputs/ExternalAgentResearch/Scout-ResearchBase.md` with `sed -n`.
- Read `/home/li/primary/AGENTS.md` with `sed -n` and `nl -ba`.
- Queried public Spirit records with `spirit "(Lookup n9fl)"`, `ty3g`, `346n`, `jys2`, `w312`, `obo5`, and `sfy0`. These confirm the supplied intent context: task-specific high-quality agents, guidance over blame, quality-first work, post-agent frontier design, deterministic routing/mechanism over agent judgment, psyche comprehensibility, and fewer better questions.
- Inspected generated runtime surfaces under `.agents/skills`, `.codex/agents`, `.claude/agents`, `.claude/skills`, `.pi/agents` with `find`, `sed`, `nl -ba`, `wc -c`, and `rg`.
- Inspected source truth in `/git/github.com/LiGoldragon/skills`: `AGENTS.md`, `ARCHITECTURE.md`, `manifests/active-outputs.nota`, `manifests/module-dependencies.nota`, `manifests/target-module-insertions.nota`, and relevant `modules/*/full.md` and `roles/*/full.md`.
- Did not inspect every archived skill, every recent `agent-outputs` artifact, runtime dispatcher internals outside the skills repo, or harness/private implementation details.

## Source-Backed Observations

### External research base

- The research base says "workflow first, agent second": start with direct calls or simple workflows, then add agents when autonomy is justified; orchestration remains valid when explicit and inspectable (`Scout-ResearchBase.md:105-115`).
- Supervisor/manager topologies are distinct from peer handoff, and the user's preferred shape fits a central supervisor that owns user interaction and synthesis (`Scout-ResearchBase.md:117-129`, `198-221`).
- Skills are externally framed as progressive context modules with trigger descriptions and optional references, while roles/subagents are execution contexts with separate responsibilities and permissions (`Scout-ResearchBase.md:131-141`, `223-245`).
- Context hygiene is a first-class reason to use subagents, but subagents can also create hidden context debt through reports, transcripts, and stale handoffs (`Scout-ResearchBase.md:143-155`).
- Multi-agent systems are most justified for broad, parallel, decomposable, risky, or context-heavy work; they can underperform on narrow work because of communication overhead (`Scout-ResearchBase.md:169-177`, `189-196`).
- Deterministic workflows, hooks, schemas, tools, and fixed edges should carry work where the right answer is derivable from inputs (`Scout-ResearchBase.md:247-264`).
- Evaluation should use observable trajectories, tool results, outputs, tests, cost, latency, reproducibility, and human review, not hidden reasoning (`Scout-ResearchBase.md:266-274`, `375-389`, `463-491`).

### Local boot and source architecture

- `/home/li/primary/AGENTS.md` is intentionally small and says generated worker role packets carry the normal role doctrine; extra doctrine loads only when named by the packet, prompt, dispatch envelope, or local context (`AGENTS.md:3-19`).
- The same boot file treats chat and harness output as primary transient artifacts, with reports reserved for handoffs, cross-agent pickup, subagent exploration, or durable analysis (`AGENTS.md:33-49`).
- Generated runtime files under `.agents/`, `.claude/`, `.codex/`, and `.pi/` are source-generated from `LiGoldragon/skills` (`AGENTS.md:60`).
- The skills source repo architecture explicitly separates source modules, role source modules, active output manifests, module dependency indexes, and target insertions (`/git/github.com/LiGoldragon/skills/ARCHITECTURE.md:20-30`, `49-75`).
- The generator deliberately emits generated role packets as curated runtime bundles so workers do not discover doctrine through a runtime index (`/git/github.com/LiGoldragon/skills/ARCHITECTURE.md:16-18`, `57-64`).
- Active outputs include 55 generated skills and 11 generated roles. The roles are `intent-translator`, `scout`, `repo-scaffolder`, `general-code-implementer`, `operating-system-implementer`, `rust-auditor`, `nix-auditor`, `skill-editor`, `intent-curator`, `repository-closeout`, and `tracker-weaver` (`/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:64-74`; `find` counted 55 `.agents/skills/*/SKILL.md` files).
- Role packet sizes in `.codex/agents/*.toml` range from about 7.7 KB (`scout`) to 21.8 KB (`operating-system-implementer`), with `general-code-implementer` at 19.2 KB. This is observable packet mass from `wc -c`.

### Current orchestration and worker contracts

- The `orchestration` skill is a strict main-lane protocol: the orchestrator interviews, gates, dispatches, and synthesizes while refusing direct task work (`.agents/skills/orchestration/SKILL.md:48-52`).
- It forbids the orchestrator from directly inspecting files, command output, links, status, or systems. Outside psyche chat, worker outputs, and read-only Spirit queries, the next action is worker dispatch or a psyche question (`.agents/skills/orchestration/SKILL.md:70-92`).
- It requires at least one focused question before method or dispatch, then two explicit psyche approvals: alignment locked and method approved (`.agents/skills/orchestration/SKILL.md:94-111`).
- It already contains one anti-over-fragmentation rule: "If scope is tiny, batch compatible tiny tasks into one worker brief or ask for scope expansion instead of wasting workers" (`.agents/skills/orchestration/SKILL.md:111`).
- It tells the lead to use a tracker/weaver for multi-bead, multi-repo, multi-worker, audit-phase, or durable tracker-state work, but not for a single small bounded fix (`.agents/skills/orchestration/SKILL.md:115`).
- It tells the lead to select an agent type whose generated role packet already embeds required doctrine and to avoid pasting fixed commit/push protocols into dispatch prompts (`.agents/skills/orchestration/SKILL.md:125-127`).
- `helper-context-transfer` gives a compact helper brief schema: task, success question, source locators or commands, authority, privacy/safety boundaries, output path or shape, evidence, and blockers (`.agents/skills/helper-context-transfer/SKILL.md:10-25`).
- The shared output protocol requires every spawned worker's substantive result to be written under `agent-outputs/<SessionName>/`, with observations, interpretations, checks, blockers, unknowns, and follow-up requirements (`.codex/agents/scout.toml:3`; same module appears in multiple role packets).
- The `scout` role is cleanly read-only and evidence-oriented (`.codex/agents/scout.toml:1-3`).
- The `intent-translator` role turns clarified psyche intent into domain dependency graphs, implementation briefs, evidence expectations, audit recommendations, and remaining decision points (`.codex/agents/intent-translator.toml:1-3`).
- The `general-code-implementer` role is available for ordinary implementation from accepted designs, fitting existing code paths, focused verification, and output evidence (`.codex/agents/general-code-implementer.toml:1-3`).
- The target insertion manifest has only one target-specific overlay: `claude-orchestration` appended to the orchestration skill and Claude agent surfaces. That overlay only says to ask clarification in ordinary chat text rather than picker/form UI (`/git/github.com/LiGoldragon/skills/manifests/target-module-insertions.nota:1-7`; `/git/github.com/LiGoldragon/skills/modules/claude-orchestration/full.md:1-7`).
- `.claude/agents/*.md` frontmatter observed for `scout` and `general-code-implementer` includes `name` and `description` but no per-role tool allowlist. `.codex/agents/*.toml` observed includes `name`, `description`, and `developer_instructions`, also not a per-role executable tool policy.
- `.claude/settings.json` has a deterministic `PreToolUse` hook for Rust `Write|Edit` operations that injects a Rust-doctrine reminder. That is a useful mechanism example, but it is narrow and Claude-specific.

## Strongest Parts

1. **The central-supervisor direction is explicit.** The orchestration skill gives the main lane a clear job: interview, gate, dispatch, and synthesize, not inspect everything itself. That matches the user's stated orchestration-first lens and the research base's supervisor/lead-agent pattern.

2. **Worker boundaries are generally crisp.** `scout`, `intent-translator`, `general-code-implementer`, auditor roles, `tracker-weaver`, and `repository-closeout` each have a narrow contract. This is much stronger than a single all-purpose agent prompt and supports downstream specialization.

3. **The source architecture is better than the runtime surface.** The skills repo has a manifest-driven generator, typed module kinds (`RuntimeSkill`, `RoleSource`, `RoleComposition`), and target insertion data. That is exactly the kind of deterministic assembly machinery the external research and public intent `w312` favor.

4. **Output contracts are evidence-first.** The shared worker output protocol asks for task scope, consulted commands/files, observations versus interpretations, checks, blockers, unknowns, and follow-up. This gives the orchestrator something better than chat fragments to synthesize.

5. **The system already acknowledges batching.** The orchestration skill's tiny-scope rule supports the user's clarified preference: do not split compatible small tasks across many workers just to be "more agentic." The `general-code-implementer` role is the right role for many such bundles.

6. **Intent handling is unusually disciplined.** `AGENTS.md`, Spirit query rules, `intent-curator`, and `intent-translator` distinguish psyche intent from agent matter and make unsupported inference a failure mode. This directly supports public intent `obo5` and `sfy0`: keep the psyche able to decide and ask fewer, better questions.

## Weaknesses And Contradictions

### 1. Orchestration is still mostly doctrine, not a mechanism

The orchestration skill defines a closed action space, gates, and dispatch posture, but dispatch selection, batching, worker reuse, audit choice, and "ask versus dispatch" are still model-judgment rules. The research base and public intent `w312` point the other way: deterministic routing, dispatch, lookup, classification, projection, and address resolution should be mechanism when derivable from inputs.

Concrete symptom: `.agents/skills/orchestration/SKILL.md:119-127` asks the model to match worker strength, choose fresh-versus-reuse, select role type, and decide what doctrine belongs in the worker. There is no observed typed `DispatchPlan`, `WorkerBrief`, `BatchPlan`, or `ReturnEnvelope` schema that a deterministic validator can check.

### 2. The "batch compatible small work" policy is present but underpowered

The system has the correct sentence at `.agents/skills/orchestration/SKILL.md:111`, and the `general-code-implementer` role exists. But the decision criteria are not operational. A lead has no local checklist for "compatible" and no structured way to express a batched worker brief that keeps tasks separate inside one worker output.

This matters because the external caution against more agents by default should produce a positive batching mechanism, not just a warning. Without criteria, agents will alternate between over-fragmenting and over-bundling by taste.

Suggested criteria:

```text
Batch into one general worker when all are true:
- same repository or worktree;
- same authority class and privacy level;
- same broad verification surface;
- no task requires a specialist role by itself;
- no task blocks another except as ordinary local sequencing;
- combined context still fits one worker's clean context.

Split when any task has distinct risk, domain doctrine, tool authority,
parallel research value, audit need, or user decision ownership.
```

### 3. The gates are too rigid for low-risk orchestration

The two explicit approvals and at-least-one-question rule protect alignment, but they can also make tiny compatible work feel bureaucratic. This conflicts with the user's clarified batching preference and public intent `sfy0` unless the lead can combine alignment and method into one focused confirmation for low-risk work.

The current rule says "Ask at least one" and requires two explicit approvals before implementation workers (`.agents/skills/orchestration/SKILL.md:96-111`). For a user who has already supplied a clear batch, this may force ritual instead of judgment.

Better shape: keep two gates for ambiguous, high-risk, public, private, irreversible, multi-repo, or high-cost work; allow one compact "alignment + method" confirmation for low-risk compatible batches.

### 4. Role packets trade progressive disclosure for startup completeness

The generator explicitly chooses bundled role doctrine (`/git/github.com/LiGoldragon/skills/ARCHITECTURE.md:16-18`, `57-64`). That aligns with public intent `n9fl` in one sense: extremely specific task-trained agents should start with the doctrine they need. But the runtime result also duplicates common modules across many roles and pushes packet sizes toward 10-22 KB.

This is not automatically wrong. It is a tradeoff. The weakness is that the system lacks an observed packet-size budget, duplication budget, or evaluation showing that the repeated module mass improves worker quality more than it harms context.

Most questionable inclusions: read-only roles like `scout` and translation roles still include edit coordination prose. The text may be harmless, but it is irrelevant in the common path and adds cognitive noise.

### 5. The output protocol can create artifact debt

Worker reports are useful pickup surfaces, and orchestration needs durable evidence. But the worker protocol says every spawned worker leaves substantive output in a file, while `AGENTS.md` says chat/harness output is primary and reports should be written only when necessary (`AGENTS.md:33-49`).

For substantial cross-agent work, the worker protocol is right. For tiny batched work, always writing durable files risks creating exactly the stale artifact pile that the context-maintenance skills later have to clean.

The missing mechanism is a return tier:

```text
ReturnTier Ephemeral: short structured harness return, no durable report.
ReturnTier Pickup: file under agent-outputs for another worker or future context.
ReturnTier Durable: durable analysis/handoff intended to survive the lane.
```

The lead could request `Pickup` for most delegated work and `Ephemeral` for tiny same-turn mechanical checks when the harness can archive automatically.

### 6. Observability is artifact-based, not trajectory-based

The system records worker reports, checks, bead status, commits, and some deterministic hooks. It does not appear to have an orchestration-run ledger that captures dispatch decisions, worker starts/finishes, retry/failure causes, cost, latency, token use, duplicate-worker detection, or user-decision points.

This falls short of the external research emphasis on traces, spans, tool calls, trajectories, cost, latency, and outcome evaluation. The current evidence can reconstruct some results, but not reliably answer "was this decomposition good?" or "did batching reduce overhead without hurting quality?"

### 7. Target-specific overlays are too thin

The generator supports target overlays, but the only observed orchestration overlay is Claude clarification UI style. There is no observed Codex/Pi-specific dispatch shape, tool-permission shape, return schema adaptation, or trace integration.

This means important target differences are probably carried in doctrine or harness behavior rather than explicit generated mechanism.

### 8. Tool permissions are textual more than enforceable

External systems emphasize schema-described tools, handoffs, guardrails, and permission scoping. The observed generated roles mostly express permissions as prose boundaries. Claude and Codex role headers inspected do not show per-role tool allowlists.

This is not always fixable in generated files if the harness lacks the surface, but the critique is still real: prose permission is weaker than an executable allowlist or wrapper. The `.claude/settings.json` Rust pre-tool hook proves deterministic enforcement is possible at least for some narrow cases.

### 9. `orchestration` is behaving like a role while being emitted as a skill

The research base warns that roles and skills are different artifacts. Locally, `orchestration` is a runtime skill, but it defines the whole main-lane identity: action space, psyche boundary, inputs, interview, gates, dispatch, and synthesis. That is role-like.

The local `intent-translator` role even says the lead/orchestrator is special and not a spawned worker role in the packet set. That is coherent, but it leaves the most important role in the system as a skill selected at fresh-context startup rather than as a first-class lead role/lane with its own launch surface and telemetry.

### 10. Evaluation of skills and roles is not first-class

The skills repo has generation tests and duplicate-heading validation witnesses, but I did not observe a harness for role/skill behavioral evaluation: trigger precision, packet-size regression, dispatch-quality scenarios, batched-vs-split comparisons, report quality, or worker failure taxonomy.

This is the main gap relative to public intent `ty3g`: if agent failures are guidance/context failures, the system needs a way to collect failure cases and decide whether the fix belongs in role prose, skill prose, generator machinery, dispatch schema, hooks, or evaluation cases.

## Recommendations Prioritized By Impact And Effort

| Priority | Recommendation | Impact | Effort |
| --- | --- | --- | --- |
| 1 | Add a typed `DispatchPlan`/`WorkerBrief`/`BatchPlan`/`ReturnEnvelope` mechanism. It should encode role, task list, source scope, authority, privacy, output tier, evidence requirements, audit requirement, and success claim. | Very high | Medium |
| 2 | Add explicit batching criteria to `orchestration` and `intent-translator`. Make "one general worker for small compatible bundles" a positive path, not just a fallback. | High | Low |
| 3 | Add an orchestration-run ledger or trace artifact. Record user decisions, dispatch plan, worker IDs/roles, artifact paths, status, retry/failure reason, elapsed time, and cost/tokens when available. | High | Medium |
| 4 | Risk-tier the approval gates. Preserve strict gates for ambiguous/high-risk work; allow one combined alignment+method confirmation for low-risk compatible batches. | High | Low |
| 5 | Promote the lead orchestrator from a runtime skill into a first-class lead lane/role or launch template, while keeping helper/context-transfer as a skill. | Medium-high | Medium |
| 6 | Add a role/skill evaluation harness with scenario tests: role selection, batch-vs-split, trigger precision, packet-size budget, report quality, and failure classification. | Medium-high | Medium |
| 7 | Trim role packet composition where modules are irrelevant to the role's normal path, especially edit coordination in read-only roles. Keep bundled role doctrine, but set explicit budgets. | Medium | Medium |
| 8 | Add target-specific overlays for executable differences, not just UI wording: tool allowlists where supported, dispatch output formatting, return schemas, and telemetry hooks. | Medium | Medium |
| 9 | Introduce return tiers so tiny delegated checks do not always create durable artifact debt, while substantial worker output remains a pickup file. | Medium | Medium |
| 10 | Expand deterministic hooks beyond the current Claude Rust edit reminder where the rule has a mechanically detectable trigger. | Medium | Medium |

## Concrete Wording Suggestions

For `.agents/skills/orchestration/SKILL.md` near the tiny-scope rule:

```text
Prefer one general worker for small compatible batches. Compatible means same
repository or worktree, same authority/privacy class, same verification surface,
no independent specialist risk, and no useful parallelism. Split only when a
task needs distinct domain doctrine, tool authority, audit path, user decision
ownership, or parallel source exploration.
```

For `.codex/agents/intent-translator.toml` source role body:

```text
When translating several small compatible tasks, produce one batched general
worker brief with separate task bullets, shared constraints, shared verification,
and one combined completion claim. Do not split merely because the tasks are
separately nameable.
```

For a new dispatch mechanism:

```text
(DispatchPlan
  (BatchPolicy GeneralWorkerCompatible)
  (Workers [
    (WorkerBrief general-code-implementer
      (Authority EditAndVerify)
      (Scope [(Path /abs/repo)])
      (Tasks [...])
      (Evidence [ChangedFiles ChecksRun ResidualRisk])
      (ReturnTier Pickup)
      (Audit None))]))
```

For evaluation:

```text
Each failed or surprising worker return is classified as one of:
BriefMissingContext, WrongRole, OverFragmented, OverBundled,
ToolPermissionGap, OutputSchemaGap, VerificationGap, StaleArtifact,
DoctrineContradiction, or HarnessMechanismGap.
```

## Bottom Line

The current system is already much closer to the external best practice than a generic "agents plus prompts" setup. Its strongest qualities are central-supervisor doctrine, narrow worker roles, generated role packets, evidence-oriented reports, and a real source generator.

The sharp critique is that the most important orchestration choices are still carried by prose. The system says the right things about delegation, batching, and context hygiene, but it lacks enough deterministic dispatch machinery, traceability, and evaluation to prove those choices are happening well. The next improvement should not be "more specialized agents." It should be a small typed orchestration mechanism that makes batching, splitting, return tiers, and audit paths inspectable.


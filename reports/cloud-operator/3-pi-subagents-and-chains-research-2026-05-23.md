# Pi Subagents and Chain Workflows in Primary

## Scope

This report answers the psyche's question about the Pi subagent agents, Pi skills, and especially chain workflows, using the installed package at `/home/li/.pi/agent/packages/pi-subagents/` plus Pi's local docs under `/home/li/.local/share/criomos/pi/package/docs/`.

No additional subagents were launched for this research after the psyche said not to use more. The earlier audit reviewer for `reports/cluster-operator/7-pi-harness-follow-up-after-third-designer-21-2026-05-23.md` was left running as permitted.

## Current installed state

`pi-subagents` is installed as package version `0.25.0`. Its `package.json` exposes one Pi extension, one bundled parent-only skill (`pi-subagents`), and prompt templates. The extension currently discovers eight executable builtin agents and no saved chain workflows.

Subagent doctor previously reported:

- async support is available;
- the current Pi session is persisted, so forked children can work;
- `pi-intercom` is not installed, so children cannot currently ask the parent live decisions through the intercom bridge;
- no extra child-injectable skills were discovered by the subagent extension.

The parent Pi session still sees package skills such as `pi-subagents` and `linkup`; that is separate from the subagent extension's child `skill` injection inventory.

## What the builtin agents are for

The bundled agents are small role prompts around child Pi sessions. They inherit the current Pi default model unless a run, user setting, or project setting overrides the model.

- `scout` — fast local codebase reconnaissance. It searches and reads enough to report entry points, files, data flow, risks, and where another agent should start. Use when the parent does not yet understand the code area.
- `context-builder` — deeper requirements-to-context handoff. It follows imports, callers, tests, docs, and configuration until it can produce context plus a compact `meta-prompt` for the next planner or worker.
- `planner` — turns supplied context into a concrete implementation plan. It is read/write only for plan output, not source editing, and defaults to forked context.
- `worker` — the single writer implementation agent. It edits and validates, but should escalate unapproved product, architecture, or scope decisions. It defaults to forked context.
- `reviewer` — adversarial review of diffs, plans, solutions, codebase health, or issues. It can edit by default, but in Primary we should normally run it review-only with explicit "do not modify project/source files" wording.
- `oracle` — high-context decision-consistency review. It uses forked context to reconstruct inherited decisions, identify drift, and recommend whether the parent is about to violate earlier decisions. It does not edit by default.
- `researcher` — web/docs research brief. It expects web tools named `web_search`, `fetch_content`, and `get_search_content`, which are from `pi-web-access`. Our current installed web package is `pi-linkup`, whose tools are named `linkup_web_search`, `linkup_web_answer`, and `linkup_web_fetch`; using `researcher` well here likely needs either `pi-web-access` or a project/user override that gives it the Linkup tools and skill.
- `delegate` — lightweight generic child, close to the parent behavior, useful for one-off delegated tasks that do not fit a specialized role.

## Pi skills versus subagent skills

Pi skills are `SKILL.md` capability files. Pi scans global, project, package, settings, and CLI-provided skill locations, then advertises only names/descriptions in the prompt. The model should load the full skill with `read` when the task matches, or the user can force it with `/skill:name`.

`pi-subagents` also has a `skill` parameter for child runs. That parameter injects named skill contents directly into a child subagent prompt. It is not the same as the parent Pi session's available-skills list. Child agents mostly set `inheritSkills: false`, so they do not automatically see the full parent skill catalog. This is good for narrow children, but it means a child must be explicitly given any needed skill or have an agent override.

Primary implication: if a child is expected to obey Primary-specific discipline beyond `AGENTS.md` project context, include the relevant file paths in the task, or inject a skill when the child skill inventory supports it. Do not assume a child knows everything the parent knows.

## Chain feature mechanics

A chain is a multi-step subagent workflow. The output of one step becomes input to the next through template variables. Chains can be invoked directly through the `subagent` tool, through slash commands, or from saved `.chain.md` files.

The important variables are:

- `{task}` — the original task for the whole chain;
- `{previous}` — the previous step's output, or the aggregated output from a parallel step;
- `{chain_dir}` — the directory where chain artifacts live.

Default task templates are useful: the first sequential step defaults to `{task}`, later sequential steps default to `{previous}`, and parallel tasks default to `{previous}`.

Step behavior resolves in this order: explicit step override, then agent frontmatter default, then disabled. This applies to output files, read files, progress tracking, skills, and model choices.

Relative chain outputs are written under the chain directory. Parallel-step relative outputs are automatically namespaced under `parallel-<step>/<index>-<agent>/...` to prevent file collisions.

By default, chain directories live under temp storage and are cleaned after roughly 24 hours. For Primary reports, use an explicit persistent `chainDir`, ideally a role-owned meta-report directory such as `reports/pi-operator/<N>-topic/`.

## Chain variants

### Sequential pipeline

A simple scout-to-plan-to-worker flow:

```typescript
subagent({
  chain: [
    { agent: "scout", task: "Map the affected code for {task}", output: "1-context.md" },
    { agent: "planner", task: "Create a plan from {previous}", output: "2-plan.md" },
    { agent: "worker", task: "Implement the approved plan from {previous}" }
  ],
  async: true,
  clarify: false,
  context: "fresh",
  chainDir: "reports/pi-operator/<N>-topic"
})
```

For Primary, do not use this exact shape for code edits unless the psyche explicitly authorizes a writer subagent and the lane/claim problem is resolved.

### Parallel fan-out then synthesis

The strongest Primary pattern is fan-out read-only analysis, then parent synthesis:

```typescript
subagent({
  chain: [
    { parallel: [
      { agent: "context-builder", task: "Build request/scope context for {task}", output: "1-request-and-scope.md", outputMode: "file-only" },
      { agent: "context-builder", task: "Build codebase/pattern context for {task}", output: "2-codebase-and-patterns.md", outputMode: "file-only" },
      { agent: "context-builder", task: "Build validation/risk context for {task}", output: "3-validation-and-risks.md", outputMode: "file-only" }
    ], concurrency: 3 }
  ],
  async: true,
  clarify: false,
  context: "fresh",
  chainDir: "reports/pi-operator/<N>-topic"
})
```

The parent then writes the final overview as the highest-numbered file in the same report directory.

### Review loop

The packaged `review-loop` prompt describes a parent-controlled loop:

1. one worker implements an approved scope;
2. fresh-context reviewers inspect the actual diff;
3. parent synthesizes blockers, fixes worth doing now, optional improvements, and deferred feedback;
4. one worker applies accepted fixes;
5. repeat only when material fixes require another review.

This is architecturally good in general, but Primary's exact-lane rule means writer children need extra discipline before we use them here.

### Saved chain files

Saved chains live under `~/.pi/agent/chains/**/*.chain.md` or `.pi/chains/**/*.chain.md`. Current discovery shows no saved chains. A saved chain file is a reusable markdown workflow with frontmatter and `## agent-name` sections. Example shape:

```markdown
---
name: primary-audit
package: primary
description: Read-only Primary report audit
---

## reviewer
output: 1-review.md
outputMode: file-only

Review {task}. Do not modify project/source files.

## reviewer
output: 2-validation-review.md
outputMode: file-only

Review validation adequacy for {previous}. Do not modify project/source files.
```

The current saved-chain serializer is sequential-section shaped. Programmatic chain calls support richer parallel fan-out/fan-in than a plain `.chain.md` file.

## Fit with Primary intent and architecture

Primary's hard rule is that subagents are not default for operator, system-specialist, poet, and assistant lanes. The psyche must explicitly authorize subagent dispatch for the task. The designer protocol is the exception, not pi-operator's default.

Primary also now has an exact role-name lane rule. This creates a real constraint for child writer agents: a Pi child process does not automatically have a Primary lane such as `pi-operator-worker-1`, a lock file, or a report directory. Therefore, the safe default in Primary is:

- use subagents for read-only scout/review/context/research/oracle work;
- let children write only configured report artifacts inside the parent-created meta-report directory;
- keep source-code edits in the parent `pi-operator` lane unless the psyche explicitly authorizes a writer child and the parent assigns/creates an exact lane for that child;
- avoid parallel writer subagents in the shared checkout;
- use worktree isolation only when the repo is clean and the task truly benefits from parallel writers.

The report discipline maps well to Pi chains. A subagent session should be one meta-report directory: `reports/pi-operator/<N>-session-name/`, `0-frame-and-method.md`, numbered subagent outputs, and a final overview. Set `chainDir` to that directory or set absolute `output` paths into it.

## Recommended Primary workflows

### 1. Read-only report audit

Use when the psyche asks for an audit of a report, plan, or implementation. Parent creates `reports/pi-operator/<N>-audit-name/0-frame-and-method.md`, launches fresh-context reviewers with explicit no-edit wording, saves each output as a numbered file, then writes final synthesis.

This is the workflow already used for the cluster-operator Pi harness audit.

### 2. Context-build before code

Use for broad implementation requests. Run parallel `context-builder` passes into a report directory: request/scope, codebase/patterns, validation/risks. Parent reads them, asks the psyche unresolved questions, and only then claims paths and edits.

This preserves Primary's intent-clarification discipline and avoids children making hidden architecture decisions.

### 3. Oracle before risky direction

Use `oracle` when the parent has accumulated a lot of context and may be drifting. Since `oracle` defaults to forked context, it is useful for checking whether a proposed direction conflicts with prior decisions. Keep it advisory.

### 4. Review after parent implementation

Parent implements under `pi-operator` after claiming paths. Then run fresh-context reviewers on the diff. Reviewers must inspect files and commands directly, not rely on parent reasoning. Parent decides what to apply.

### 5. Research with current tool mismatch fixed

For web research, either install `pi-web-access` or create a Primary-specific researcher override that uses Linkup tools. Until then, the parent can do web research directly with Linkup while using subagents for local scout/review.

## Project configuration worth considering

If the psyche wants this to become routine, create project-level assets rather than relying on ad hoc prompting:

- `.pi/agents/primary-reviewer.md` — a read-only reviewer that always inherits project context, carries Primary's report/intent/lane constraints, and has no `edit`/`write` tools except perhaps configured output artifacts.
- `.pi/agents/primary-context-builder.md` — a context builder that knows to read `ESSENCE.md`, `INTENT.md`, `AGENTS.md`, `skills/skills.nota`, and the repo's `AGENTS.md`/`skills.md` when inside repos.
- `.pi/chains/primary-report-audit.chain.md` — a saved read-only audit sequence for reports.
- `.pi/chains/primary-context-handoff.chain.md` — a saved context-build sequence for implementation handoffs.
- A `researcher` override using `linkup_web_search`, `linkup_web_answer`, and `linkup_web_fetch`, or package `pi-web-access` alongside `pi-linkup`.
- Optional `pi-intercom` packaging if live child-to-parent decision asks are valuable.

Do not add writer-agent chains as defaults until the dynamic lane story is settled.

## Operational rules for pi-operator

- Before launching any subagent, confirm the psyche explicitly asked for subagents for this task.
- Use `context: "fresh"` for adversarial reviewers and context builders unless inherited conversation is the point.
- Use `oracle`/`worker` forked context only when the child needs inherited trajectory.
- Prefer `async: true` and `clarify: false` for programmatic chains; do not poll just to wait.
- Use `outputMode: "file-only"` for long reports.
- Use persistent `chainDir` inside `reports/pi-operator/` for report-worthy sessions.
- Do not use child writers in dirty shared checkouts unless explicitly authorized and lane/claim ownership is clear.
- If a child surfaces an unapproved decision and `pi-intercom` is not installed, treat the child result as blocked and ask the psyche in the parent session.

## Bottom line

Pi subagents are a good fit for Primary if treated as an advisory and report-production layer around a lane-owning parent agent. Chain mode is especially useful as a report-shaped workflow engine: fan out context/review work, collect artifacts in a persistent report directory, then let the parent synthesize and decide. The unsafe boundary is child source editing without an exact Primary lane; keep that off by default.

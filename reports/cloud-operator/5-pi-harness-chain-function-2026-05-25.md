# Pi harness chain function — 2026-05-25

## Scope

The psyche corrected a speech-to-text corruption: the actual request was to figure out how the chain function works in the Pi harness. Spirit record `632` captures that the previous `forward chain random.randint ...` text was not psyche instruction.

This report describes the real `pi-subagents` chain behavior as installed in the local Pi profile.

## Short answer

Pi chains are `pi-subagents` workflows that run Pi child agents in sequence, with optional fan-out/fan-in parallel steps. They do not call arbitrary Python functions. The two human-facing command surfaces are:

```text
/chain scout "scan the codebase" -> planner "make a plan"
/run-chain scout-planner -- refactor authentication
```

The agent/tool-facing surface is:

```ts
subagent({
  chain: [
    { agent: "scout", task: "Gather context for {task}" },
    { agent: "planner", task: "Plan from the previous output:\n{previous}" }
  ],
  task: "refactor authentication",
  async: true
})
```

## Command syntax

`/chain` is inline and ephemeral. It parses agent steps separated by `->`:

```text
/chain scout "analyze auth" -> planner -> worker
```

If a later step has no explicit task, it defaults to the prior step output. In the example above:

- `scout` receives `analyze auth`.
- `planner` receives the `scout` output.
- `worker` receives the `planner` output.

A shared task form is also accepted:

```text
/chain scout planner -- analyze the auth system
```

`/run-chain` runs a saved `.chain.md` workflow by name:

```text
/run-chain scout-planner -- refactor authentication
```

Installed discovery currently reports no saved chains in this workspace, so `/run-chain` has no local named chain to run until one is created under `~/.pi/agent/chains/**/*.chain.md` or `.pi/chains/**/*.chain.md`.

## Saved chain files

Saved chain files are markdown with frontmatter plus one `## agent-name` section per step:

```md
---
name: scout-planner
description: Gather context then plan implementation
---

## scout
output: context.md

Analyze the codebase for {task}

## planner
reads: context.md

Create an implementation plan based on {previous}
```

The parser treats config lines before the first blank line as step behavior. Supported step keys include `output`, `outputMode`, `reads`, `model`, `skills`, and `progress`.

## Runtime semantics

The chain engine creates a chain artifact directory for the run, resolves every step's task template, and then executes steps in order.

Template variables are:

- `{task}` — the original chain task.
- `{previous}` — the previous step's output; after a parallel step, this is an aggregated output with separators.
- `{chain_dir}` — the chain artifact directory.

Sequential execution updates an internal `prev` string after each child finishes. A step task is built by replacing `{task}`, `{previous}`, and `{chain_dir}`, then adding any read/write/progress instructions implied by step or agent configuration. If the task template omits `{previous}`, the engine appends the previous output as a suffix named `Previous step output`.

Parallel chain steps are represented in the tool API as `{ parallel: [...] }`. All tasks in that step receive the same prior `prev`, run concurrently up to `concurrency`, and their outputs are aggregated into the next `prev`. `failFast` can skip remaining parallel work after a failure. `worktree: true` can isolate parallel writer tasks.

## Foreground, background, and clarify behavior

Tool-mode chains default to the clarify UI when Pi has a UI and the chain has no parallel step; pass `clarify: false` to bypass it. Slash commands set `clarify: false` and launch directly.

Background execution is controlled by `async: true` in the tool API or `--bg` in slash commands. In this workspace, subagent dispatch must be background/async by rule, so chain examples for agent use should include `async: true` unless the psyche explicitly asks for a foreground clarify UI.

`--fork` or `context: "fork"` wraps chain tasks for forked child sessions. If omitted, the chain may still become forked if any selected agent has `defaultContext: fork`; the packaged `planner`, `worker`, and `oracle` do.

## Practical correction to the mangled transcript

The mangled text said something like `forward chain random.randint 1 10 print`. That is not a valid Pi chain command. The closest real demonstration is:

```text
/chain delegate "Pick a random number from 1 to 10 and return only the number." -> delegate "Use the previous output in one sentence."
```

For agent-side use, the same shape is:

```ts
subagent({
  chain: [
    { agent: "delegate", task: "Pick a random number from 1 to 10 and return only the number." },
    { agent: "delegate", task: "Use this number in one sentence: {previous}" }
  ],
  async: true,
  clarify: false
})
```

This launches Pi child agents; it does not execute Python functions directly.

## Agent definitions and skills

The "type of job" is an agent definition. Builtins like `scout`, `planner`, `worker`, `reviewer`, `context-builder`, `researcher`, `delegate`, and `oracle` come from the `pi-subagents` package. User and project agents are markdown files discovered from:

```text
~/.pi/agent/agents/**/*.md
.pi/agents/**/*.md
.agents/**/*.md   # legacy compatibility
```

An agent file has YAML frontmatter plus a system prompt body. The frontmatter is where job defaults live: `name`, `description`, `model`, `tools`, `skills`, `output`, `defaultReads`, `defaultProgress`, `defaultContext`, and related behavior. The body is the agent's base system prompt.

Skills are separate `SKILL.md` files. They are resolved by name from project/user/package skill locations and injected into the child system prompt in this shape:

```xml
<skill name="skill-name">
...skill content...
</skill>
```

So yes: skill material is effectively preloaded before the child receives the chain step task. The child process receives the agent system prompt plus the selected skill injections, then receives the task text built for that step.

A chain step can override the agent defaults for that one run:

```ts
{ agent: "reviewer", task: "Review {previous}", skill: ["security"], model: "anthropic/claude-sonnet-4", output: "review.md" }
```

Saved `.chain.md` files express the same thing in markdown step sections. A chain is therefore a workflow recipe; each step points to a job type (agent) and may override that job's skills/model/output/reads/progress for the step.

## What async means

`async: true` means the parent Pi session starts the chain in a detached background runner and immediately gets control back. It is about parent/child scheduling, not about making the children conversational peers.

What changes with `async: true`:

- The main chat is not blocked while the chain runs.
- The run gets an async run id and status/result files under Pi's temp async directories.
- The parent can inspect it with `subagent({ action: "status", id: "..." })`.
- Pi delivers completion when the run finishes.
- `resume` can send follow-up to a live async child or revive a completed child session when persisted session files exist.

What does not change:

- Sequential chain dataflow is still previous-output text into next-step prompt.
- Async does not by itself let sibling agents freely talk to each other.
- A parallel step still fans out from the same previous output and fans back in through aggregated outputs.
- Only intercom-enabled runs can have explicit parent-child coordination messages; `pi-subagents` can work without `pi-intercom`, and ordinary chain dataflow does not require intercom.

In this workspace there is also a local rule: subagent dispatch must be non-blocking, so agent-launched chains should normally use `async: true` and `clarify: false` unless the psyche explicitly asks for the foreground clarify UI.

## Sources read

- `/home/li/.pi/agent/packages/pi-subagents/skills/pi-subagents/SKILL.md`
- `/home/li/.pi/agent/packages/pi-subagents/README.md`
- `/home/li/.pi/agent/packages/pi-subagents/src/slash/slash-commands.ts`
- `/home/li/.pi/agent/packages/pi-subagents/src/runs/foreground/chain-execution.ts`
- `/home/li/.pi/agent/packages/pi-subagents/src/shared/settings.ts`
- `/home/li/.pi/agent/packages/pi-subagents/src/agents/chain-serializer.ts`
- `/home/li/.pi/agent/packages/pi-subagents/src/runs/background/async-execution.ts`
- `/home/li/.pi/agent/packages/pi-subagents/src/runs/background/subagent-runner.ts`

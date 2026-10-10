# Agent-Built Actor Machines

Research date: 2026-08-21. Investigating real actor-based software systems
whose code was substantially or wholly written by AI coding agents.

## The Scarcity Finding

After systematic search across GitHub commit history, vendor showcases,
engineering blogs, and the Elixir/Rust actor library ecosystems, no
credible specimen was found of an actor-based system that was substantially
or wholly built by AI coding agents.

What the search returned instead, in large quantity:

- **Frameworks that use actor models to coordinate AI agents.** AutoAgents
  (liquidos-ai), sagents, agens, and AgentRunway all use Ractor or
  Elixir OTP to orchestrate LLM-powered agents. These are actor systems
  built to contain agents, not actor systems built by agents.

- **Plugins and prompts that help AI agents write actor-based code.** Claude
  Code plugins for Elixir/Phoenix (claude-elixir-phoenix, claude_code SDK,
  Claudify's CLAUDE.md template) instruct AI agents on OTP patterns. These
  are knowledge artifacts for the agent, not agent-authored machines.

- **AI-assisted development of actor libraries.** The kameo library
  (tqwewe/kameo, which this workspace forks) shows no "Co-Authored-By:
  Claude" or equivalent attribution in its commit history. It is
  solo-maintained by its author with occasional human contributors and
  dependabot.

The scarcity is itself a finding. Where individual practitioners use Claude
or Codex to write actor code, the result is not published as a standalone
identifiable artifact with clear provenance; it is absorbed into a larger
project where the agent's contribution is unmarked or where the human author
does not use attribution trailers.

## Specimens Examined

### OpenFANG (github.com/RightNow-AI/openfang)

**What it is.** An open-source Agent Operating System in Rust. 137,728 lines
across 14 crates. The repository has a CLAUDE.md, indicating Claude Code is
used as a development contributor.

**Machine shape.** OpenFANG implements its own kernel-level scheduler rather
than a standard actor framework (no Actix, Ractor, or kameo). The CLAUDE.md
instructs contributors on a layered architecture: `server.rs` bridges kernel
functionality via `AppState`; trait-based abstraction (`KernelHandle`) avoids
circular dependencies between runtime and kernel. The CLAUDE.md demands live
integration tests after every feature, noting that unit tests alone pass while
features are dead code.

**Agent provenance assessment: assisted, extent unknown.**
All visible commits are authored by `jaberjaber23`. Commit messages are
brief and incremental ("cargo fmt", "clippy lint", "audit fixes", "thread
routing"). No "Co-Authored-By: Claude" or equivalent trailers appear in the
visible commit history. The CLAUDE.md is instructions written for Claude
contributing, not a claim that Claude wrote the system. The true fraction of
agent-written code is unknowable from external inspection.

### AutoAgents (liquidos-ai/AutoAgents)

**What it is.** A multi-agent coordination framework in Rust using Ractor (an
Erlang/OTP actor model implementation) as its coordination layer. Supervision
trees where parent actors oversee child agents.

**Machine shape.** Agents execute as Ractor actors. Supervision enables
automatic restart on failure. The framework supports ReAct and Basic executor
patterns and pluggable LLM backends. Tokio is the runtime foundation.

**Agent provenance assessment: not agent-built.**
No mention in README, CONTRIBUTING, or commit history of AI agents building
the codebase. This is a human-authored framework for building AI agent systems
using actors; the actor model is the target architecture, not the product of
agent authorship.

### sagents (sagents-ai/sagents)

**What it is.** An Elixir framework for building interactive AI agents with
OTP supervision, middleware composition, and Phoenix LiveView integration.

**Machine shape.** Agents run as supervised OTP processes. The supervision
tree uses `Sagents.Supervisor` added to the application tree. Process registry
abstracts over Registry (local) and Horde.Registry (distributed). Dynamic
supervisor starts agent supervisors on demand. Restart strategy is
`:rest_for_one` with `:temporary` restart policies.

**Agent provenance assessment: not agent-built.**
No agent authorship claims found anywhere in the repository. Human-authored.

### kameo (tqwewe/kameo)

**What it is.** The upstream actor library this workspace forks and runs on.

**Agent provenance assessment: not agent-built.**
Commit history examined. No "Co-Authored-By: Claude" or AI attribution
trailers. Solo-maintained by tqwewe with occasional human contributors.

## What Agents Do and Do Not Do With Actors

This is the most grounded finding, drawn from a practitioner thread on the
Elixir Forum (2024-2025) and supplementary sources.

### Recurring failures (observed claims from practitioners)

**Unsupervised process spawning.** The consistent failure mode: agents spawn
processes without linking them to a supervision tree. One Elixir practitioner:
Claude "will sneak in brittle tests with concurrency issues, unsupervised
processes, overuse of potentially runaway atoms, and all sorts of other
beginner-level gotchas." The agent produces code that runs but is fragile in
the way that matters: when a process dies, nothing notices.

**Sleep-based synchronization.** Agents reach for `Process.sleep/1` (Elixir)
or `tokio::time::sleep` (Rust) to paper over concurrency ordering problems
rather than using proper message-passing synchronization. Practitioners
explicitly noted this as a rule that "works, until it drifts."

**Crappy OTP by default.** Expressed directly in the thread: the agent
defaults to "crappy OTP" — technically valid patterns that miss the point of
the model — unless the architecture is "worked out in advance with tight
audit/checks for every prompt." Generalized guidelines at length fall apart.

**Mechanical execution without structural understanding.** In the Jake
Goldsborough rewrite article (rewriting Claude Code in Rust with Claude),
Claude used `tokio::sync::mpsc` channels competently for streaming but executed
tools serially within the main loop — no structured concurrency, no actor
model sophistication, no actor granularity decision. The agent knew the
primitives; it did not reach for architectural form.

**Optimizing for the happy path.** AI agents across codebases generate code
tuned for success paths because training data is skewed toward working
examples. Actor supervision and fault isolation are precisely the fault path —
what happens when a child process fails — and agents systematically
underspecify it.

### Recurring strengths (constrained to reported cases)

**Boilerplate translation.** When the supervision shape is given, agents
translate it into GenServer callbacks (`@impl true`), Actor impls, and ask/reply
message structs correctly and quickly. The mechanical form is well within the
agent's competence when the design is not in question.

**Primitive use.** Agents use tokio channels, mpsc, and oneshot correctly for
point-to-point coordination. This was observed in the Goldsborough rewrite
article and consistent with general Rust async competence.

**High-level design discussion.** Practitioners reported agents useful for
architectural discussion and high-level design — generating candidate shapes to
reason about — as long as the human provides the evaluative judgment.

### Published experience reports

The Elixir Forum thread is the most specific practitioner record on agents and
actor systems. Its judgment is: agent assistance for Elixir/OTP requires
experienced human oversight to catch architectural violations. The agent cannot
be trusted to independently produce a correct supervision tree shape.

The Augment Code multi-agent failure analysis (2026) identifies three root
categories of failures in LLM multi-agent systems at the meta level —
specification, coordination, verification — which map cleanly onto what
practitioners describe at the code level: agents under-specify process
boundaries and fail to verify fault behavior.

## Summary Assessment

No inspectable actor system substantially built by AI coding agents was found.
The domain of "agent-built actor machines" is currently a gap in the
observable public record, not a populated space. The gap may reflect:

1. Real agent-built actor code exists inside private or unmarked repositories
   where attribution trailers are absent.
2. Practitioners building actor systems with AI assistance are experienced
   enough to know the agent needs tight constraints; those constraints are
   tacit craft knowledge, not published specimens.
3. The actor model's core value — fault isolation, supervision, crash handling
   — is exactly what agents miss by default, making agent-built actor machines
   without heavy oversight likely to be wrong where it counts.

The most concrete finding is the Elixir practitioner record: agents produce
actor-shaped code that compiles and runs, but with unsupervised processes,
sleep-based synchronization, and structural fragility in the fault paths — the
reverse of what actor systems are for.

## Sources

- Elixir Forum — "Here's how I'm coding Elixir with AI. Results are mixed,
  mostly positive. How about you?": https://elixirforum.com/t/heres-how-im-coding-elixir-with-ai-results-are-mixed-mostly-positive-how-about-you/71588
- OpenFANG repository: https://github.com/RightNow-AI/openfang
- OpenFANG CLAUDE.md: https://github.com/RightNow-AI/openfang/blob/main/CLAUDE.md
- AutoAgents (liquidos-ai): https://github.com/liquidos-ai/AutoAgents
- sagents: https://github.com/sagents-ai/sagents
- AgentRunway: https://github.com/cedrickchee/agent_runway
- agens: https://github.com/jessedrelick/agens
- kameo upstream: https://github.com/tqwewe/kameo
- Zylos Research — Rust-Native AI Agent Frameworks 2026:
  https://zylos.ai/research/2026-04-01-rust-native-ai-agent-frameworks-ecosystem-2026/
- Freshcode — Orchestrating AI Agents with Elixir's Actor Model:
  https://www.freshcodeit.com/blog/why-elixir-is-the-best-runtime-for-building-agentic-workflows
- Jake Goldsborough — Rewriting Claude Code in Rust with Claude:
  https://jakegoldsborough.com/blog/2026/rewriting-claude-code-in-rust-with-claude/
- Augment Code — Why Multi-Agent LLM Systems Fail:
  https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them
- DEV Community — 7 Hidden Production Bugs AI Coding Agents Create:
  https://dev.to/pockit_tools/7-hidden-production-bugs-ai-coding-agents-create-and-how-to-catch-them-before-they-crash-f7b
- Claudify — Claude Code with Elixir: Phoenix, LiveView, OTP, and Ecto:
  https://claudify.tech/blog/claude-code-elixir
- Akka AI coding assistant documentation:
  https://doc.akka.io/sdk/ai-coding-assistant.html

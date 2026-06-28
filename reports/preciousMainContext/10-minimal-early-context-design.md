# 10 — Minimal Early Context: the routing + preload design

Designer lane (preciousMainContext), 2026-06-25. This report integrates report 9
(minimal AGENTS.md) with new internal + external research into one design
picture for the psyche's intent-alignment session. It does not supersede reports
4/6/7/8/9; it extends report 9 from "shrink the startup read" to the broader
program the psyche now describes: re-gear the whole workflow to spend as little
EARLY context as possible.

## The thesis

Today an agent spends early context two ways that the psyche wants to kill:

1. The startup read itself (AGENTS.md and whatever it points at) is a meaningful
   read that drains context before the first useful turn. Report 9 already
   attacks this: AGENTS.md is now a minimal boot contract, the skill index
   `skills/skills.nota` is the only default startup read, and the lead operates
   in two modes (delegate any meaningful read to a helper, or interact with the
   psyche).
2. The in-session model emits tool calls to chase data it was always going to
   need. On a stateless API each such round-trip costs output tokens to ask,
   re-bills the whole growing context to deliver the answer, and then carries
   that answer uncached in the message tail at full price on every later turn.

The psyche's program generalizes report 9's move. Instead of letting the
expensive in-session model discover its context through tool calls, a CHEAP
upstream API call classifies the incoming prompt (parameters such as which
skills apply), and a reusable, pre-generated "training prompt" scaffold — the
skills the agent needs — is assembled and placed in the first prompt prefix,
ahead of the user prompt. Inputs route through MENCI to the right NAMED,
short-lived agent session. The harness runs inside a controlled process we send
input to and read output from (the psyche notes even "load" is proprietary).
Exploratory agents are ALWAYS sub-agents: the main thread either delegates to a
sub-agent or just responds.

Report 9 is the human-side prototype of exactly this pattern. `skills.nota` is a
tiny index a controller queries to decide which skills to load; the
`when-to-use-helpers` / `helper-context-transfer` skills are the discipline of
packaging the full required-reading envelope into the dispatch so the worker
does not burn context rediscovering it. The psyche now wants the machine-side
version: an upstream classifier and a harness driver doing automatically what
the lead does by hand.

## Early-context mechanics: Codex vs Claude Code

The two harnesses differ in HOW first-turn context is assembled, which matters
because the design's levers are harness-specific.

### Claude Code

First-turn context = system prompt + tool schemas + the memory chain
(CLAUDE.md imports AGENTS.md, 72 lines, which names one default read,
`skills.nota`). Key mechanics:

- Prompt caching is a strict prefix match in render order tools -> system ->
  messages. Any byte change before a `cache_control` breakpoint invalidates
  everything after it. Cache reads cost ~0.1x base input; writes 1.25x (5-min
  TTL) / 2x (1-hour TTL). Minimum cacheable prefix is model-dependent
  (1024-4096 tokens).
- Skills are progressive disclosure: an index of one-line records, full
  `SKILL.md` read only on trigger. Deferred tools are listed by name only;
  `ToolSearch` fetches the schema on demand (the API analog is tool-search +
  `defer_loading`). Tool search APPENDS schemas rather than swapping them, so it
  preserves the cache prefix.
- Headless surface: `claude -p`, `--output-format json|stream-json`,
  `--input-format stream-json` (bidirectional NDJSON), `--system-prompt` /
  `--append-system-prompt(-file)`, `--resume`/`--continue` with captured
  `session_id`, `--bare` (skip auto-discovery of CLAUDE.md/hooks/skills/MCP for
  deterministic spawns — slated to become the `-p` default), `--mcp-config`,
  `--agents`, `--settings`.
- Sub-agents read in isolated context on a cheaper model and return a distilled
  result — the native primitive for "exploratory agents are always sub-agents."

This is the harness whose levers most directly fit the psyche's design: a
reusable scaffold placed in the stable prefix is written once at 1.25x and read
at ~0.1x on every reuse; the classifier-chosen context flows in through
`--system-prompt`/`--append-system-prompt` or a pre-seeded stream-json
conversation.

### Codex CLI

First-turn context = a fixed, model-specific base system prompt compiled into
the binary (`gpt_5_codex_prompt.md`, ~6.6 KiB / ~1088 words) + auto-injected
AGENTS.md + tool schemas. Key mechanics:

- AGENTS.md is auto-injected before the first user prompt every run:
  global/user override, then Git-root down to cwd, concatenated root-down,
  capped at `project_doc_max_bytes` (default 32 KiB, source-confirmed).
- The base prompt is fixed per session and can only be MINIMIZED BY FULL
  REPLACEMENT via `base_instructions` / `model_instructions_file` /
  `experimental_instructions_file` — replace, not trim, so default tool-format
  guidance (the apply_patch envelope) may be lost.
- Core tooling = a shell tool + `apply_patch` editor; optional web_search,
  view_image, plan, MCP each add per-turn schema/init tokens.
- Headless surface: `codex exec` runs one session to completion (no TUI); prompt
  via positional arg, piped stdin, or `codex exec -` (full prompt from stdin);
  `--json` makes stdout a JSONL event stream. The official TS SDK wraps
  `codex exec --json` as a child process.
- Levers to shrink early context: `project_doc_max_bytes=0` to suppress/shrink
  AGENTS.md; keep AGENTS.md small, avoid nested chains; disable web_search /
  view_image to drop schemas; minimize MCP; `--ignore-user-config` /
  `--ignore-rules`; lower `model_verbosity` / tune `model_reasoning_effort`;
  pre-activate the dev environment so the agent does not probe it.

Notable difference for the design: Codex does NOT expose the documented prompt
prefix-caching levers Claude Code does, and its base prompt is replace-only.
Codex's natural injection point is AGENTS.md (capped, concatenated) plus a fully
replaced `base_instructions`. So a cross-harness scaffold would need two
generators — a Claude `--system-prompt`/append path and a Codex
AGENTS.md/`base_instructions` path — unless we target one harness first.

(Caveat from the Codex reader: file-override key spelling varies by version;
exact startup token counts are unmeasured; defaults for `project_doc_max_bytes`
and `model_reasoning_effort` come from source, not the published reference.)

## The MENCI / named-session / controlled-process architecture

There is an important naming/reality gap the lead must hold:

- The classify-select-route system the psyche describes does NOT exist as built
  machinery. The design lives in one fresh brief:
  `reports/operatingModeShift/0-Synthesis-agent-context-routing-brief.md`
  (2026-06-25), proposing a "MENCI-style routing" preflight that classifies the
  prompt, selects skills from `skills.nota`, runs Spirit queries, builds
  versioned prompt packs, and launches a named short-lived worker
  (`SessionRequest`, `PreflightRouter`, `SessionLaunchPacket`). It is a proposal
  with six open questions, no Spirit record.
- The real, mature, production named-session backend is **orchestrate**:
  `orchestrate-daemon` owns `orchestrate.redb`; `orchestrate` and owner-only
  `meta-orchestrate` CLIs; `signal-orchestrate` contracts. LANES are the named,
  short-lived, intent-named sessions; each lane carries a discipline that loads
  skills, authority, persona-mind memory, and a key. This is the existing
  substrate for "named, short-lived agent sessions."
- **MENCI / Mentci** is deployed but is NOT a router. It is an
  observation/debugging/approval console (`mentci`, `mentci-lib`,
  `mentci-egui`, `signal-mentci`) over components and Criome approvals.
  (Menchie/Menchi/Mencie normalize to Mentci.) Its role in the routing design is
  UNDECIDED — the psyche names MENCI as the thing inputs route through, but the
  deployed MENCI is a console, so either MENCI's role expands or the psyche
  means orchestrate's routing.
- The "controlled process we send input to and read output from" maps to the
  general pattern of running the agent CLI/SDK as a child process and driving it
  programmatically. Three driving modes, increasing fidelity: (1) headless
  one-shot (`claude -p` / `codex exec`); (2) bidirectional stream-json (one
  long-lived process steered across turns); (3) PTY wrapping of the TUI (last
  resort, parse ANSI screen state, brittle). No proprietary "load" tool exists
  in the workspace today (only "load-bearing" prose) and no harness-driving code
  via PTY/expect/stdin exists yet (only the external Pocock "Sandcastle" studied
  in operator report 462). So "load" as the psyche names it is net-new.

Net: the named-session BACKEND exists (orchestrate/lanes). The PREFLIGHT ROUTER,
the prompt-pack generator, the harness driver ("load"), and MENCI's role as the
routing front door are all net-new or unratified.

## The cheap upstream classifier: role and risks

The classifier is the keystone. Before spawning a session, a cheap model
(Haiku-tier, ~$1/M in) classifies the incoming request: which skills/docs/files
it needs (-> preload into the first prompt) and how hard it is (-> model routing,
easy -> Haiku, hard -> Opus). Classifier overhead is small against agent latency
(rule-based <1ms, embeddings ~5ms, ML/LLM ~50-430ms vs 500-2000ms+ per agent
turn). Reported bill reductions from routing land in a 40-85% range in the
surveyed cost-optimization literature.

Risks the psyche should weigh:

- Cost/savings figures are vendor/blog numbers, not controlled benchmarks —
  order-of-magnitude only. A MISROUTING erases the savings: an easy task sent to
  Opus wastes money; a hard task starved on Haiku fails the task.
- A wrong skill selection silently underfeeds OR overfeeds the worker.
  Over-preloading is pure waste: every scaffold token is paid at 1.25x on the
  cache-write and re-read at ~0.1x every turn forever, and it crowds the window
  and can degrade attention. The calibration rule is to size the scaffold to the
  classifier's CONFIDENCE and let genuinely-uncertain needs fall back to
  tool-driven retrieval.
- STALE SCAFFOLD is a correctness risk, not just cost: a cached/pre-generated
  skill scaffold that has drifted from the live skill files silently feeds the
  worker outdated instructions. A wrong-but-cached prefix is worse than a cache
  miss. Mitigation (a design responsibility, not enforced by the harness):
  version the scaffold against the skill source and regenerate on change.
- Build-vs-reuse: the classifier could be a rule-based selector over
  `skills.nota` (cheapest, deterministic, already-indexable), an embedding
  match, or a Haiku LLM call. The existing substrate is the agent reading
  `skills.nota` itself; the nearest scaffold analog is the helper-dispatch
  discipline. The "cheap upstream API call" is net-new glue either way.

## Prompt-caching implications

Caching is what makes preloading cheap, and it is the lever with the sharpest
footguns:

- A reusable, pre-generated skill scaffold at the FRONT of the prompt is a
  cacheable prefix: write once (1.25x), read at ~0.1x on every reuse. Preload
  converts a per-turn full-price message-tail into an amortized 0.1x prefix.
- Put the scaffold in a STABLE PREFIX (system/tools, before the last
  `cache_control` breakpoint); keep volatile content (the user question,
  timestamps, per-request ids) AFTER it. A single silent invalidator —
  `datetime.now()`, a uuid, an unsorted tool list — drops `cache_read` to zero
  and you pay full price on every spawn.
- Share one scaffold ACROSS many short-lived sessions so the write amortizes
  over the fan-out; pre-warm with a `max_tokens: 0` request at controller
  startup. The pattern pays off in FAN-OUT (many short sessions sharing one warm
  prefix) or multi-turn sessions; a single-turn, single-session task may not
  recover even one cache write.
- Do NOT switch models mid-session — caches are model-scoped, so a mid-session
  switch invalidates the whole cache; spawn a fresh cheap session/subagent for
  the cheap sub-task instead.
- Cross-PROCESS cache reuse across separate `-p` spawns depends on the provider
  keying the cache by content+org and on the harness forwarding `cache_control`
  on the scaffold prefix across spawns. This must be verified empirically
  (`usage.cache_read_input_tokens` on the second spawn) before assuming
  cross-session amortization — it is the load-bearing unverified assumption for
  the whole economic case.

## What exists vs what is net-new

Already in the workspace:

- Minimal AGENTS.md + two-mode lead contract + `skills.nota` as the only default
  startup read (report 9, landed).
- The named-session backend: orchestrate / lanes / disciplines (production).
- MENCI as a deployed observability/approval console (not a router).
- The human-side preload discipline: `skills.nota` index +
  `when-to-use-helpers.md` + `helper-context-transfer.md`.
- Spirit as the intent substrate; `intent-alignment.md` as the session-opening
  skill.
- Native Claude Code primitives that match the design: progressive-disclosure
  skills, deferred tools + ToolSearch, sub-agents on a cheaper model, headless
  flags, prompt caching.

Net-new (must be built or ratified):

- The PreflightRouter / cheap upstream classifier (skill selection + model
  routing).
- The prompt-pack / scaffold generator (and its versioning-against-source for
  staleness).
- The harness driver — the "controlled process" / "load" tool that spawns and
  steers the named session.
- MENCI's role as the routing front door (expand MENCI, or use orchestrate's
  routing) — undecided.
- A cross-harness story (Claude `--system-prompt` path vs Codex
  AGENTS.md/`base_instructions` path) IF more than one harness is targeted.
- The routing brief itself is unratified (six open questions, no Spirit record).

## Open threads carried in

- The three Spirit records from report 9 (supersede ky10; new Principle
  generalizing 3ey7; new Decision on minimal AGENTS.md) are drafted but NOT yet
  written — they await psyche approval of exact NOTA wording.
- The report-9 floor judgment call (do version-control safety rules stay
  resident in AGENTS.md or move to a jj/version-control skill) is still open;
  author leaned toward moving them out.
- Operator coordination: the operator/Codex lane was told to stand down on
  AGENTS.md; collision not yet confirmed resolved.
- W6 / primary-ptvb.6 remains open.
- The routing brief's six open questions and MENCI's role are unresolved.

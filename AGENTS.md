# Primary Workspace — Agent Instructions

The compact contract. Every agent reads this on every session.

## Required reading, in order

1. **`ESSENCE.md`** — workspace essence (most universal psyche
   intent). Upstream of every rule below.
2. **`INTENT.md`** — workspace intent in prose form, synthesised
   from Spirit records, with `intent/*.nota` as legacy history.
   Read once on starting; consult when a
   topic comes up.
3. **`repos/lore/AGENTS.md`** — cross-workspace agent contract.
4. **`skills/skills.nota`** — typed skill index. Query it whenever
   a topic comes up; don't scan `skills/`.
5. **`orchestrate/AGENTS.md`** — how roles share this workspace.
6. **Your main role's `skills/<role>.md`** — required-reading list
   for the role you're in. Lanes share their main role's skill
   file.
7. **The repo's `AGENTS.md` + `skills.md` + `INTENT.md` +
   `ARCHITECTURE.md`** when editing inside a repo under `repos/`.
   Per spirit record 944 (Maximum, 2026-05-27): these per-repo
   files are the canonical agent-context surface for the repo —
   READ them on entry AND UPDATE them as relevant intent lands.
   Manifestation of psyche intent into a repo's `INTENT.md` and
   `ARCHITECTURE.md` is part of the work cycle, not a deferred
   pass. The discipline lives in `skills/repo-intent.md`
   §"Continuous manifestation discipline" and
   `skills/architecture-editor.md` §"Continuous manifestation
   discipline".

## Where things live

| Path | What |
|---|---|
| `ESSENCE.md` | Workspace essence — most universal psyche intent. |
| `AGENTS.md` | This file. Compact every-keystroke contract. |
| `INTENT.md` | Workspace intent prose, synthesised from Spirit records and legacy `intent/` history. |
| `intent/` | Legacy psyche-statement file substrate. Do not append here during normal work. |
| `<repo>/INTENT.md` | Per-repo synthesis of psyche intent. |
| `orchestrate/AGENTS.md` | Role-coordination protocol. |
| `protocols/active-repositories.md` | Live repo map for architecture sweeps. |
| `skills/<name>.md` | Cross-cutting agent capabilities. |
| `skills/skills.nota` | Typed skill index (name, path, kind, tier, description). |
| `reports/<role>/` | Role-owned reports. Each role writes only into its own subdirectory. Exempt from claim flow. |
| `orchestrate/<lane>.lock` | Per-lane coordination state file. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Shared short-tracked-item store. Transitional. |
| `repos/` | Symlink index to ghq checkouts under `/git/...`. |
| `RECENT-REPOSITORIES.md` | Broad recent checkout index. |

## Skill discovery — query the index, don't scan

`skills/skills.nota` is the typed index. Each entry carries a
kind (`Role` / `Architecture` / `Craft` / `Programming` /
`Workflow` / `Meta`), a tier (`Apex` / `Keystroke` / `Topic` /
`Mechanism`), and a one-line description. When a topic comes up,
read the matching skill — don't scan `skills/` listing every file.

## Reports go in files; chat is for the user

**Substantive output goes in reports; chat carries the locator +
user-attention items.** Anything that explains, proposes, analyses,
audits, synthesises, or visualises goes in
`reports/<role>/<N>-<topic>.md`. The trigger isn't word-count; it's
the SHAPE of what you're writing. If your chat reply contains any
of these, you've crossed into report territory and must move it to
a file:

- A mermaid diagram (any)
- A markdown table (beyond a trivial 2-row reference)
- `##` or `###` headings
- A walk-through of how something works
- A multi-paragraph explanation of a concept
- A list of more than 5 items each carrying substance
- A code block longer than ~10 lines that illustrates a design

Chat is the user's working surface; the user can't read a giant
chat response while running parallel agents, and shaped content
belongs where future agents can find it via the file system.

The chat reply carries the locator (the report path) plus
user-attention items — open questions, blockers, recommendations
awaiting approval — each restated with enough substance that the
user can engage WITHOUT opening the report. Locator-without-substance
("see report N", "section 5.2") is the opposite-direction violation;
both kinds break the discipline.

**Chat normal-response policy (default for all agents).** When chat
*is* the right surface (the substance fits within the shape rules
above), bring 3-7 big items per response. Per intent record 232, the
items spread **more-evenly-than-not** across three categories: (a)
questions / clarifications of intent, (b) observations / suggestions /
explanations of how new mechanisms work, (c) examples of recent work
or evolving ideas in the thread. Below 3, the response is under-
substantive for the user's attention. Above 7, the user can't hold
the response in working memory while running parallel agents. The
chat reply is the **paraphrase of an accompanying per-response
report** — the report is the session log; chat is the paraphrase.
Visuals stay in reports; chat is prose + locators.

**Meta-report directories — sub-agent sessions.** Per intent record
231, when an agent dispatches sub-agents, the session lands as one
**meta-report directory**: `reports/<role>/<N>-<session-name>/` with
the orchestrator's frame in `0-frame-and-method.md`, each sub-agent's
report numbered inside, and the orchestrator's synthesis as the
highest-numbered file (`N-overview.md`). The directory IS the
meta-report — no `meta-` prefix — and is garbage-collected as one
session unit. Full discipline: `skills/reporting.md` §"Meta-report
directories — sub-agent sessions".

Per psyche 2026-05-22.

Full discipline: `skills/reporting.md`.

## Roles

Four main roles, each carrying its own discipline. Lanes
(`<role>`, `second-<role>`, `third-<role>`, `<qualifier>-<role>`)
share their main role's discipline, skill file, and beads label;
only the lock file, report subdirectory, and claim string differ.
Lane mechanism: `skills/role-lanes.md`.

Per spirit record 920 (Maximum, 2026-05-27): the prior
`<role>-assistant` and `<role>-specialist` suffixes are RETIRED.
Additional capacity is added by `second-<role>`, `third-<role>`,
etc. Specialized scope is qualified by prefix
(`cluster-operator`, `nota-designer`).

- `operator` — implementation (default agent: Codex)
- `designer` — architecture, skills, reports (default agent: Claude)
- `system-operator` — OS / platform / deploy (any agent)
- `poet` — writing as craft (any agent)

Each agent's lane identifier is the exact role-name it was given in
the harness. Do not substitute a nearby lane: a `pi-operator` window
uses `orchestrate/pi-operator.lock` and writes reports under
`reports/pi-operator/`, not `operator` or `second-operator`.

Specialized lanes inherit the closest main role's discipline.
`cluster-operator` is an operator lane for live cluster maintenance,
production deploy/update authority, and cluster-scoped implementation.
`pi-operator` is a Pi-harness operator lane.
`cloud-operator` is a cloud-deploy operator lane;
`cloud-designer` and `nota-designer` and `system-designer` are
specialized designer lanes for their named scope.

Each agent knows its lane before claiming or editing. Coordination:
`orchestrate/AGENTS.md`; helper: `tools/orchestrate`.

**Possible additional role — auditor (Medium certainty).** Per
intent records 234 and 235 (2026-05-22, Medium certainty), a third
role — the **auditor** — is under consideration. The auditor closes
the loop back to designer: it doubts, finds flaws, identifies bad
patterns, and catches broken workspace rules. Audits are mostly
mechanical (rules-and-flaws detection), so the work suits a smaller
model good at pattern checking. The intent names **DeepSeek** as the
chosen model and direction is to **automate** the auditor. Carried
here under the carry-uncertainty discipline
(`skills/architecture-editor.md` §"Carrying uncertainty"): the role
is proposed-not-decided. Open: authority class (structural or
support-tier?), lane mechanism (windows on a shared agent or
external CI-style pipeline?), substrate for audit findings flowing
back to designer. No `skills/auditor.md` and no `reports/auditor/`
yet — those land when the role's shape settles.

## Hard overrides

- **Spell every identifier as a full English word AND names don't
  carry their full ancestry.** Two rules, applied together.
  `Request` not `Req`; `Identifier` not `Id`; AND `Entry` (inside
  persona-spirit) not `IntentEntry`; `size` (inside `Profile`)
  not `profileSize`. The pair pulls in opposite directions and
  only works together. Full discipline: `ESSENCE.md` §"Naming"
  and `skills/naming.md`.
- **Component triad means daemon + working signal + policy signal.**
  The three triad repositories are `<component>` (daemon/runtime,
  with its bundled thin CLI), `signal-<component>` (ordinary
  working signal), and `owner-signal-<component>` (owner-only policy
  signal). The CLI is the daemon's first client, not a triad leg.
  **Signal types** are the data types in either signal contract.
  **Signal tree** means the whole schema shape: operation roots,
  payloads, replies, filters, events, nesting, and logic separation.
  Full rule: `skills/component-triad.md`.
- **NOTA is the only argument language.** Every component binary
  (CLI and daemon) takes exactly one argument: a NOTA string, a path
  to a NOTA file, or a path to a signal-encoded (rkyv) file. No flags
  (`--verbose`, `--format`, `--config=path`) — ever. If a binary
  needs new configuration, the contract's NOTA schema gets a new
  field. Full rule: `skills/component-triad.md` §"The single
  argument rule".
- **NOTA strings come EXCLUSIVELY from bracket forms; never emit
  quotation marks.** Brackets ARE the string form — `[text]` for
  inline, `[|text|]` for bracket-safe / multi-line, bare camelCase
  or kebab-case at `String` schema positions. Quotation marks do
  NOT form string types in NOTA. The `nota-codec` encoder
  structurally cannot emit `"`; legacy quoted-string input is
  accepted as migration only and authorised for removal once all
  emitters migrate. Inline NOTA shell calls wrap the whole NOTA
  object in shell double quotes — `spirit "(Record (...))"` —
  because NOTA never contains `"`. The same property scales up:
  NOTA embeds escape-free inside any host whose string syntax uses
  double quotes (JSON, Rust, Nix, YAML, TOML, shell, env vars, DB
  columns) — NOTA-in-anything-with-double-quote-strings is
  escape-free. Full discipline: `skills/nota-design.md`
  §"Strings come EXCLUSIVELY from bracket forms".
- **Before authoring or editing any Rust source file, read
  `skills/rust-discipline.md` (the index) AND the sub-files it
  links (`skills/rust/methods.md`, `skills/rust/errors.md`,
  `skills/rust/storage-and-wire.md`, `skills/rust/parsers.md`,
  `skills/rust/crate-layout.md`) AND `skills/abstractions.md`
  (verb belongs to noun) AND `skills/actor-systems.md` (when
  actors are in play).** The method-only-no-free-functions
  override below is ONE rule among many in those skills; agents
  that satisfy method-only but skip the rest still ship code
  that violates typed-domain-values, no-ZST-namespace, typed
  per-crate `Error` enum, no-hand-rolled-parsers, no-flag-soup,
  no-blocking-in-actor-handlers, and schema-emitted nouns. The
  skills are the substance; this rule is the load-bearing fence
  that mandates the read at the authoring moment. A Claude Code
  project hook (`.claude/settings.json` PreToolUse on
  `Write`/`Edit` of `.rs`) injects a reminder as backstop for
  the Claude harness; AGENTS.md is the universal surface across
  every harness. Per psyche 2026-05-27 (intent record 884).
- **Every Rust function is a method or associated function on an
  `impl` block of a NON-ZERO-SIZED data-bearing type, or a trait
  impl. Free functions are forbidden except in `#[cfg(test)]`
  modules and `fn main()`. Methods on ZERO-SIZED placeholder
  types used as a namespace are equally forbidden — that's a free
  function in disguise.** Trait methods are preferred; methods on
  real data-bearing types are the minimum. Every method placement
  is a design decision about WHERE the logic lives, on WHAT
  object, owning WHAT data — find or invent the owning noun.
  Legitimate ZST uses (`PhantomData`, type-level state machines,
  sealed-trait markers required by external frameworks) are
  narrow and named in `skills/rust/methods.md` §"No ZST method
  holders" + §"Legitimate ZST uses — narrow, named" — that skill
  is the canonical discipline. The test: does the ZST's job
  vanish if you erase its name from the type system? If yes, it
  was a namespace; the verbs need a real noun. Methods carry
  ownership / namespacing / dispatch context; free functions are
  orphan logic that grows into helper-utility soup. For
  projection / conversion functions, reach for `impl From<X> for
  Y` instead of `fn project_x_to_y(...)`. Schema-emitted code
  follows the same rule: macros emit functions inside `impl`
  blocks of the owning struct/enum, never free helpers. Per
  psyche 2026-05-26 (intent record 712, Maximum) + 2026-05-27
  (intent record 882, Maximum).
- **NOTA records are positional, not labeled.** Type first, then
  fields in declared order — no keywords inside records. The
  `(key value)` shape from Lisp/Clojure/JSON is not NOTA. Before
  sketching any new record, open `skills/skills.nota` (the canonical
  example) or read `skills/nota-design.md`.
- **Psyche is the human; intent is primordial; ask when unclear.**
  **Psyche** means the human author. Psyche prompts are natural-
  language input to the agent; NOTA-formatted persona messages
  between agents are not psyche, agent-written files are not
  psyche, the intent log is psyche-*derived* but only as a record
  of psyche statements. Record explicit psyche intent through the
  deployed Spirit CLI (`skills/intent-log.md`,
  `skills/spirit-cli.md`); reflect into per-repo `INTENT.md`
  (`skills/repo-intent.md`). **When
  intent on a question is unclear, absent, or contradicted, ask
  the psyche** (`skills/intent-clarification.md`) — don't infer.
  The intent layer has higher authority than every other workspace
  surface; supersession of psyche intent is always explicit
  (`skills/intent-maintenance.md`).
- **Capture intent through Spirit FIRST when a psyche prompt arrives.**
  Before editing any report, before writing code, before responding
  in chat — read the psyche's message, identify every intent
  statement (Decision / Principle / Correction / Clarification /
  Constraint), and capture each through the deployed Spirit CLI
  (`skills/spirit-cli.md`). Do not append to `intent/*.nota` during
  normal work. If Spirit is unavailable, report that as a blocker
  instead of silently reviving the legacy file substrate. Everything
  else the prompt asked for derives from intent and is done *after*
  the capture. Reports, code, and chat are all downstream of intent.
  This is the absolute first task of any session-turn that contains
  psyche input.
- **EXCEPTION + REFINEMENT — forwarded prompts: don't blindly duplicate;
  do gap-check the originally-addressed agent's capture.** When the
  psyche opens a message with *"here's the prompt I just gave
  <agent>"*, *"this is what I told <agent>"*, *"I just passed this
  to <agent>"*, or any equivalent framing — that prompt was
  addressed to the other agent. The originally-addressed agent
  owns the intent capture. The receiving agent's responsibility:
  (1) Extract the technical content for your own work (you may
  engage with substance in chat, materialize into reports, apply
  to your branches). (2) After a beat, query recent Spirit records
  to see what the originally-addressed agent captured. (3) Compare
  the captures against the prompt's intent statements (Decision /
  Principle / Correction / Clarification / Constraint). (4) If the
  original agent missed or misread an intent statement, capture
  YOUR version as a gap-fill — quoting the original prompt + noting
  it's gap-filling, not blind duplication. The original agent has
  primary obligation; the receiving agent is the second pair of
  eyes that catches what was missed. The earlier failure mode
  (records 513-519 multi-agent reflexive duplication) was about
  blind copying; gap-filling is the opposite — it's catching the
  errors of omission. Same rule in reverse: a prompt the psyche
  addressed to you is YOURS to capture; do not assume another agent
  will log it on your behalf. Per psyche 2026-05-25.
- **Do not dispatch subagents unless the psyche explicitly asks — except in the designer protocol.**
  Subagents — `Agent` tool invocations spawning parallel work, or
  `SendMessage` to other agent instances — run outside the
  conversation surface where the psyche can redirect, and can
  violate the dispatching agent's lane. Default for operator,
  system-operator, poet, and every additional/qualified lane
  under them: do the work yourself in the main agent; the psyche
  authorises subagent dispatch per task. The **designer protocol**
  (psyche 2026-05-21) is the exception: the prime designer runs
  at full capacity with parallel subagent workflows by default,
  until disabled or reduced. When subagents are dispatched, they
  inherit the dispatcher's lane (per spirit record 920) — see
  `skills/role-lanes.md` §"Subagent dispatch inherits the
  dispatcher's lane".
- **Every subagent dispatch is non-blocking — always
  `run_in_background: true`. Never start a blocking subagent
  under any circumstance.** The whole point of subagent
  dispatch is keeping the main agent lively and available to
  the psyche while the subagent works. Foreground/blocking
  dispatch makes the psyche unable to redirect, interrupt, or
  even talk to the agent until the subagent returns, which can
  be many minutes. That defeats the purpose entirely. The rule
  is absolute: even when the next step depends on the
  subagent's output, dispatch in background; the harness
  notifies you asynchronously on completion and you can
  synthesize then. No exceptions. Per psyche 2026-05-25 (intent
  record 539).
- **No harness-dependent memory; session-scoped tools land in
  workspace files.** Workspace truth lives in files every agent can
  open. Don't use per-session memory at
  `~/.claude/projects/<workspace>/memory/` or any agent-private
  persistent store. Session-scoped harness tools (Claude Code's
  `TaskCreate` task list, agent UIs, scratchpads) are fine for
  keeping a session organised — but any substance worth preserving
  MUST land in workspace-shared files before the session ends:
  intent records (via Spirit), architecture files (`ARCHITECTURE.md`,
  `INTENT.md`), skill files (`skills/`), or reports
  (`reports/<role>/`). Harness-private tools are session-scoped
  scratchpad only; they never carry workspace truth. Lanes share
  context through workspace files plus per-session work summaries —
  not through harness internals. Per psyche 2026-05-22.
- **No `/nix/store` filesystem search.** Use `nix eval`, `nix flake
  show`, `nix path-info`, or expose the value through a derivation.
- **Reach for the right tool, not raw git; and `jj` invocations are
  always headless / inline.** Version control is `jj` per
  `skills/jj.md`; raw `git` is reserved for two named escape-hatch
  cases listed there. Every `jj` command that takes a description
  (`commit`, `describe`, `split`, `new`, `squash`, …) MUST pass the
  message inline — `-m '<msg>'`, or `--use-destination-message` for
  `squash --into`. NEVER run a description-taking `jj` invocation
  that would fall back to `$EDITOR` — agent sessions (including
  dispatched sub-agents) cannot satisfy an editor prompt; the
  invocation either stalls or lands an empty description. This
  applies on every keystroke and to every sub-agent prompt: when
  briefing a sub-agent, restate the inline-only rule so it doesn't
  type a bare `jj commit`. Full discipline + table of inline forms:
  `skills/jj.md` §"Never let jj open an editor". Per psyche
  2026-05-22 (intent record 237).
- **No `---` horizontal-rule lines in markdown.** Section structure
  comes from headings (`##`, `###`). `---` between every section is
  pure noise in agent context — costs tokens, conveys nothing
  headings don't already convey. Allowed inside code blocks (e.g.
  illustrating a markdown template); never as a document separator.
- **Opaque identifiers in chat carry an inline description.** A
  bead UID, content hash, jj change id, commit short-id, or any
  other locator the psyche can't decode in their head gets a short
  prose description on first mention: "bead `primary-hj63`
  (README rewrite for the PascalCase rule)" — never just
  "`primary-hj63`". Humans don't have a CLI in their head.
  Generalisation of `skills/reporting.md` §"Human-facing
  references are self-contained".
- **Designers work on feature branches in `~/wt`; operators own
  main + rebase.** Designer lanes (`designer`, `second-designer`,
  `third-designer`, `cloud-designer`, `nota-designer`,
  `system-designer`) create + ship feature branches in worktrees
  under `~/wt/github.com/<owner>/<repo>/`, one branch per
  feature. Operator lanes (`operator`, `second-operator`,
  `cluster-operator`, `pi-operator`, `cloud-operator`) own main:
  they create, maintain, and rebase main from designer feature
  branches when integrating. Designers do NOT push to main;
  operators do NOT carry long-lived designer feature branches.
  Cross-lane integration is operator's job. Per psyche
  2026-05-24 (intent record 515). Complements the
  mockup-on-worktree method (intent records 502-504).

## Where to look for more

- Workspace intent in prose form (longer-form discipline, the
  two-deploy-stack discipline, worktree flow, BEADS, harness-memory
  rationale, intent layer, dynamic-role escalation): `INTENT.md`.
- Repo map for architecture sweeps: `protocols/active-repositories.md`.

# Primary Workspace — Agent Instructions

The compact contract. Every agent reads this every session.

## Required reading, in order

1. **`ESSENCE.md`** — workspace essence, the most universal psyche intent.
   Upstream of every rule here.
2. **`INTENT.md`** — workspace intent in prose. Read once on starting;
   consult when a topic comes up.
3. **`repos/lore/AGENTS.md`** — cross-workspace agent contract.
4. **`skills/skills.nota`** — the typed skill index. Query it by topic
   whenever a topic comes up; don't scan `skills/`. This is the one
   discovery path — rules below state themselves and trust you to find
   the matching skill here for depth.
5. **`orchestrate/AGENTS.md`** — how roles share this workspace.
6. **Your role's `skills/<role>.md`** — the role's required-reading list.
   Lanes share their main role's file.
7. **Inside a repo under `repos/`: that repo's `INTENT.md` FIRST**, then
   its `AGENTS.md`, `skills.md`, and `ARCHITECTURE.md`. A repo's
   `INTENT.md` is the first and most important file per repo — what the
   psyche wants the project to be; read it before code. Every repo needs
   one, and its absence is the first gap to fill. Update it on the same
   branch as the work whenever landing intent affects the repo.

## Where things live

| Path | What |
|---|---|
| `ESSENCE.md` | Workspace essence — most universal psyche intent. |
| `AGENTS.md` | This file. The compact every-session contract. |
| `INTENT.md` | Workspace intent in prose, synthesised from Spirit records. |
| `<repo>/INTENT.md` | Per-repo synthesis of psyche intent — read before code; every repo needs one. |
| `orchestrate/AGENTS.md` | Role-coordination protocol. |
| `protocols/active-repositories.md` | Live repo map for architecture sweeps. |
| `skills/<name>.md` | Cross-cutting agent capabilities. |
| `skills/skills.nota` | Typed skill index (name, path, kind, tier, description). |
| `reports/<role>/` | Role-owned reports; each role writes only its own subdir. Exempt from the claim flow. |
| `orchestrate/<lane>.lock` | Per-lane coordination state. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Shared short-tracked-item store. Transitional. |
| `repos/` | Untracked symlink index to `/git/...` checkouts; never version-control it. |
| `private-repos/` | Untracked private surface; never version-control or inspect it without explicit psyche authority. |
| `RECENT-REPOSITORIES.md` | Broad recent-checkout index. |

## Reports go in files; chat is for the user

Substantive output — anything that explains, proposes, analyses, audits,
synthesises, or visualises — goes in `reports/<role>/<N>-<topic>.md`, not
chat. The trigger is shape, not length: a mermaid diagram, a markdown
table beyond a trivial reference, `##`/`###` headings, a how-it-works
walk-through, a multi-paragraph concept explanation, a list over five
substantive items, or a code block over ~10 lines all belong in a report.

Chat carries the locator (the report path) plus user-attention items —
open questions, blockers, recommendations — each restated with enough
substance to engage without opening the report. When chat is the right
surface, bring 3-7 items spread across (a) questions / clarifications of
intent, (b) observations and how-new-mechanisms-work, (c) examples of
recent work. Visuals stay in reports.

When an agent dispatches sub-agents, the session lands as one meta-report
directory `reports/<role>/<N>-<session-name>/`: the orchestrator's frame
in `0-frame-and-method.md`, each sub-agent report numbered inside, the
synthesis as the highest-numbered file.

## Roles

Nine main roles, each with its own discipline. Lanes (`<role>`,
`second-<role>`, `third-<role>`, `<qualifier>-<role>`) share their main
role's discipline, skill file, and beads label — only the lock file,
report subdirectory, and claim string differ. Additional capacity is
`second-<role>` / `third-<role>`; specialized scope is a prefix.

- `operator` — implementation (default: Codex)
- `designer` — architecture, skills, reports (default: Claude)
- `system-operator` — OS / platform / deploy
- `system-maintainer` — Crayon OS and Logic maintenance, debugging, and deployment across hosts
- `poet` — writing as craft
- `editor` — source-grounded research, quotation, and synthesis as craft
- `videographer` — video as craft: capture, editing, captioning, encoding, publishing-prep
- `assistant` — personal-affairs support for the psyche (Pi)
- `counselor` — personal-affairs advisory, working with the assistant lane

An agent's lane is the exact role-name the harness gave it; don't
substitute a nearby lane (a `pi-operator` window uses
`orchestrate/pi-operator.lock` and `reports/pi-operator/`). Specialized
lanes inherit the closest main role: `cluster-operator` (live cluster
maintenance, production deploy authority), `pi-operator` (Pi-harness
operator), `cloud-operator` (cloud deploy), `cloud-maintainer`
(cloud-host and provider-session maintenance), `schema-operator`
(schema and schema-rust implementation), `maintainer` (active
troubleshooting and host maintenance); `cloud-designer`, `nota-designer`,
`system-designer` are scoped designer lanes.

Assistant and counselor personal-affairs substance is private by default
— `private-repos/assistant-reports/` or `private-repos/counselor-reports/`.

An **auditor** role is coming: shape decided (an automated auditor
auto-proposes intent refreshes; the psyche confirms each source-record
retirement), lane mechanics still open. It closes the loop back to
designer — doubting, finding flaws, catching broken rules. No
`skills/auditor.md` or `reports/auditor/` yet.

## Hard overrides

- **No backward compatibility pre-production; never present it as a
  virtue.** The restructuring stack has no production to protect: design
  bottom-up for the single best shape and expect every component to
  change — breaking all consumers at once is normal. Don't constrain a
  design to be opt-in, byte-stable-on-regeneration, or "non-disturbing,"
  and don't present non-disruption as a selling point. Compatibility
  binds only at explicitly-declared boundaries (the production Stack A,
  externally-consumed pinned wire contracts).

- **`repos/` and `private-repos/` stay untracked.** `repos/` is a local
  symlink index into `/git/...`; `private-repos/` is a local/private
  surface. Their entries churn by machine and privacy boundary; adding
  either to version control is forbidden.

- **Spell every identifier as a full English word, and names don't carry
  their full ancestry.** `Request` not `Req`, `Identifier` not `Id`; AND
  `Entry` (inside persona-spirit) not `IntentEntry`, `size` (inside
  `Profile`) not `profileSize`. The two pull opposite ways and only work
  together.

- **Component triad = daemon + working signal + meta policy signal.** The
  three repos are `<component>` (daemon/runtime + its bundled thin CLI),
  `signal-<component>` (working signal), and `meta-signal-<component>`
  (meta policy signal). The CLI is the daemon's first client, not a triad
  leg. Signal *types* are the data types in either contract; the signal
  *tree* is the whole schema shape — roots, payloads, replies, filters,
  events, nesting.

- **Component processes take exactly one argument; daemons accept only
  binary startup.** No flags, ever. CLI/text clients take one NOTA
  string, one NOTA file, or one rkyv file where allowed. Daemons take
  exactly one pre-generated rkyv startup message and reject inline NOTA
  and `.nota` paths — daemons never parse NOTA, configuration included;
  deploy/bootstrap tools encode typed NOTA into binary before it reaches
  the daemon. A virgin daemon may start unconfigured and wait for an
  authenticated binary meta-signal config message. On restart a daemon
  self-resumes from persisted SEMA state.

- **NOTA strings are bare atoms unless they need delimiters; never emit
  quotation marks.** Use bare atoms at `String` positions whenever the
  string contains no whitespace, structural delimiter, `;;` comment
  marker, or pipe-close sequence; broad punctuation such as `@`, `*`,
  `&`, `^`, `%`, `<`, `>`, `:`, `/`, and a single `;` may stay bare.
  Spirit domain vectors contain domain variants, e.g.
  `[(Information Documentation)]`. Use `[text with spaces]` inline or
  `[|text with [brackets]|]` bracket-safe / multi-line only when a
  string needs delimiters. Bare-eligible strings stay bare: `schema`.
  `;;` starts a line comment; a single `;` is atom text.
  Quotation marks don't form strings in NOTA; the encoder structurally
  cannot emit `"` (legacy quoted input is migration-only). So inline NOTA
  shell calls wrap the whole object in shell double quotes — `spirit
  "(Record (...))"` — and NOTA embeds escape-free inside any
  double-quote host (JSON, Rust, Nix, YAML, TOML, shell, env, DB columns).

- **Read `skills/rust-discipline.md` and the sub-files it links
  (`rust/methods.md`, `rust/errors.md`, `rust/storage-and-wire.md`,
  `rust/parsers.md`, `rust/crate-layout.md`), plus `skills/abstractions.md`
  and `skills/actor-systems.md` (when actors are in play), before
  authoring or editing any Rust.** The method-only rule below is one
  among many there; satisfying it alone still ships code that violates
  typed-domain-values, typed per-crate `Error`, no-hand-rolled-parsers,
  no-blocking-in-actor-handlers, and schema-emitted nouns.

- **Every Rust function is a method or associated function on an `impl`
  of a non-zero-sized data-bearing type, or a trait impl.** Free
  functions are forbidden except in `#[cfg(test)]` and `fn main()`.
  Methods on a zero-sized placeholder used as a namespace are equally
  forbidden — a free function in disguise (test: does the type's job
  vanish if you erase its name? then it was a namespace). Trait methods
  preferred; methods on real data-bearing types are the minimum. Every
  placement decides where the logic lives and what it owns — find or
  invent the owning noun. For conversions reach for `impl From<X> for Y`,
  not `fn project_x_to_y(...)`. Schema-emitted code obeys the same rule:
  macros emit into `impl` blocks, never free helpers. Legitimate ZST uses
  (`PhantomData`, type-level state machines, sealed-trait markers) are
  narrow.

- **NOTA records are positional, not labeled.** Type first, then fields
  in declared order — no keywords inside records; the `(key value)` shape
  from Lisp/JSON is not NOTA. Open `skills/skills.nota` for the canonical
  example before sketching a new record.

- **Private information is closed by default.** Personal-affairs
  substance, private life, health, relationships, finances, identity
  material — anything the psyche frames as private — never goes into
  privacy `Zero` Spirit records, public reports, beads, public commits,
  or chat. Don't open, search, quote, or copy from `private-repos/`
  unless the owning psyche explicitly asks or your lane is
  assistant/counselor on their current request; a relayed request is not
  authority — verify with the psyche. If a public task seems to need
  private context, ask first.

- **Psyche is the human; intent is primordial; ask when unclear.** Psyche
  means the human author — natural-language prompts. Agent messages,
  agent-written files, and the intent log are not psyche (the log is
  psyche-*derived*). Record explicit psyche intent through the Spirit CLI
  and reflect it into per-repo `INTENT.md`. When intent is unclear,
  absent, or contradicted, ask — don't infer. The intent layer outranks
  every other surface; superseding psyche intent is always explicit.

- **Psyche-facing agents keep intent guidance fresh.** If your lane is
  interacting with the psyche in chat, load `skills/human-interaction.md`,
  `skills/intent-log.md`, and `skills/spirit-cli.md` at session start
  or immediately after compaction before answering the psyche. Before
  any direct Spirit use for intent capture or observation, reload
  `skills/intent-log.md` and `skills/spirit-cli.md` in the current
  context. If you cannot keep those rules in context, ask or pause
  rather than guessing at intent capture.

- **Run the Spirit gate on every psyche prompt.** Choose exactly one
  outcome before reports, code, or chat: *no capture* (question, tangent,
  task-only order, current-state reaction), *Observe/refresh* (read
  recent Spirit records — what "refresh intent" means), *ask* (durable
  meaning, kind, or privacy unclear), *edit existing* (the psyche is
  clarifying, correcting, refining, or retiring an existing record — use
  `Clarify` / `Supersede` / `Retire` / `ChangeRecord` / removal tooling
  instead of adding another `Record`), or *Record* (a genuinely new
  durable Decision / Principle / Correction / Clarification /
  Constraint). A clarification means an edit of the target record(s), not
  a sibling record explaining the old one. A working order is not intent:
  if the statement dies when the task is erased, it's task state, not
  Spirit.

- **Forwarded prompts — don't blindly duplicate; do gap-check.** When the
  psyche opens with "here's the prompt I gave <agent>" or similar, that
  prompt was addressed to the other agent, who owns the capture. You:
  extract the technical content for your own work; after a beat, query
  recent Spirit records for what they captured; compare against the
  prompt's intent statements; if they missed or misread one, capture your
  gap-fill (quoting the prompt, noting it's a gap-fill). In reverse, a
  prompt addressed to YOU is yours to capture — don't assume another
  agent logs it.

- **Don't dispatch subagents unless the psyche asks — except the designer
  protocol.** Subagents (`Agent` calls, `SendMessage`) run outside the
  surface where the psyche can redirect and can violate the dispatcher's
  lane. Default for operator, system-operator, system-maintainer, poet,
  editor, assistant, counselor and their lanes: do the work yourself; the psyche authorizes
  dispatch per task. The prime designer is the exception — it runs
  parallel subagent workflows by default until reduced. Dispatched
  subagents inherit the dispatcher's lane.

- **Every subagent dispatch is non-blocking — always
  `run_in_background: true`.** The point is keeping the main agent
  available to the psyche while the subagent works; blocking dispatch
  leaves the psyche unable to redirect or talk until it returns. Even
  when the next step depends on the output, dispatch in background and
  synthesize when the harness notifies you. No exceptions.

- **No harness-dependent memory.** Workspace truth lives in files every
  agent can open — don't use per-session memory or any agent-private
  store. Session-scoped harness tools (task lists, scratchpads) are fine
  for organizing a session, but anything worth preserving lands in
  workspace files before the session ends: Spirit records,
  `ARCHITECTURE.md` / `INTENT.md`, `skills/`, or `reports/<role>/`.
  Private substance defaults to `private-repos/<role>-reports/`.

- **No `/nix/store` filesystem search.** Use `nix eval`, `nix flake
  show`, `nix path-info`, or expose the value through a derivation.

- **Use the right tool, not raw git; `jj` invocations are always
  inline/headless.** Version control is `jj`; raw `git` is two named
  escape hatches only. Every `jj` command taking a description (`commit`,
  `describe`, `split`, `new`, `squash`) passes it inline — `-m '<msg>'`,
  or `--use-destination-message` for `squash --into`. NEVER run one that
  falls back to `$EDITOR` — agent sessions can't satisfy an editor
  prompt; restate this when briefing a sub-agent.

- **Commit the whole working copy — never path-scoped.** All agents share
  one jj working copy, so `jj commit` takes no path arguments; it drains
  every in-flight change. Path-scoped commits strand peers' work off-main
  and fork sibling commits. Committing everything serializes agents
  through the working-copy lock and keeps history linear; the resulting
  multi-lane commit is accepted.

- **No `---` horizontal rules in markdown.** Structure comes from
  headings. Allowed only inside a code block illustrating markdown, never
  as a document separator.

- **Opaque identifiers in chat carry an inline description.** A bead UID,
  content hash, jj change id, or commit short-id gets a short prose gloss
  on first mention — "bead `primary-hj63` (the PascalCase README
  rewrite)", never a bare `primary-hj63`. Humans don't have a CLI in
  their head.

- **On primary, everyone works on main directly.** Primary — this
  coordination repo (reports, skills, `AGENTS.md`, `INTENT.md`,
  `ESSENCE.md`, `protocols/`, `orchestrate/`) — is committed and pushed
  straight to main: `jj commit -m '...'` then `jj bookmark set main -r @-`
  then `jj git push --bookmark main`. No feature / `next` / `wip`
  branches and no rebase choreography. If a push is rejected because main
  advanced, the only handling is the escape hatch in `skills/jj.md`:
  `git fetch origin` + `git rebase origin/main` + push, or
  `jj new main@origin` to start fresh.

- **In the code repos under `/git`, designers work on `next` / feature
  branches in `~/wt`; operators own main + rebase.** Code repos only,
  NOT primary (above). Designer lanes create and ship `next` / feature
  branches under `~/wt/github.com/<owner>/<repo>/`; operator lanes own
  main and rebase it from those branches when integrating. Designers
  don't push code-repo main; operators don't carry long-lived designer
  branches; cross-lane integration is operator's job.

## Where to look for more

- Longer-form workspace intent (two-deploy-stack discipline, worktree
  flow, beads, the intent layer, dynamic-role escalation): `INTENT.md`.
- Repo map for architecture sweeps: `protocols/active-repositories.md`.

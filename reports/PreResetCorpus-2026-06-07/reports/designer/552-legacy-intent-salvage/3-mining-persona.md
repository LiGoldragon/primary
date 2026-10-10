# 552 — Legacy intent salvage — mining persona.nota

## Scope

Mined `/tmp/intent-text/persona.txt` (61 records, the date-stripped extract of
`intent/persona.nota`). The file is the persona-system architecture log:
persona-spirit, persona-orchestrate, persona-mind, persona-router, the engine
manager, skills, and the spirit intent record shape.

Result: **4 genuine salvage candidates**, all in the orchestrate / mind / router
machinery layer. The overwhelming majority of the file (57 records) is already
preserved — deeply — across ESSENCE.md, INTENT.md, and the per-repo INTENT.md
files for `persona-spirit`, `mind`, `router`, and `orchestrate`, plus the live
Spirit store. The persona architecture is the single best-manifested area of the
legacy substrate; persona.nota is close to fully safe to delete.

## Salvage candidates

### 1. Mind says what-work; orchestrate decomposes how — job-decomposition as programmable policy

- **Kind:** Principle
- **Proposed topics:** `[orchestrate mind authority-split job-decomposition policy-contract owner-signal]`
- **Proposed description:** Mind expresses work in abstract concept terms — "we
  need topic X researched by a skill-type-Y agent", "we need a new REST
  component named Z that does W" — never in mechanism terms (which agent, which
  socket, which spawn parameters). Orchestrate owns the translation from an
  abstract job description into a concrete, mechanical SEQUENCE of agent-type
  assignments with per-step success criteria and on-success / on-failure
  branches (e.g. a new-component job decomposes into repo-scaffold agent →
  auditor → coding agent → audit). The decomposition is policy-driven and
  programmed into orchestrate, not decided per job; mind extends orchestrate's
  behaviour by PROGRAMMING new job-class→sequence policies through the
  owner-signal-orchestrate contract rather than re-inventing orchestration each
  session. This is the deeper "what vs how" layer split that sits BELOW the
  state-vs-machinery boundary.
- **Proposed certainty:** Maximum (the psyche stated it at length and concretely)
- **Supporting verbatim:** *"The mind expresses concepts… we need this topic
  researched by such-and-such skill-type agent… the orchestrator could figure
  out, well, it's a rest component, so first we need a repo manager… this is all
  mechanical, it's all programmed already in the orchestrator."* +
  *"the persona mind would be also, because of the owner contract, be able to
  program new things. Like, here's a new policy: when this type of job comes in,
  run such-and-such sequence of agent-types… if he says success, then this;
  if failure, then this."*
- **Preservation evidence:** `orchestrate/INTENT.md` §Boundaries captures only
  the static state-vs-machinery split (mind owns state; orchestrate owns
  machinery — role claims, lifecycle, spawn plans, lane registry). It does NOT
  state the abstract-job-decomposition mechanism, the agent-type-sequence shape,
  the success/failure branch policy, or the mind-programs-policy-via-owner-channel
  capability. Spirit query on `[persona mind orchestrate router]` and
  `[orchestrate agent registry reuse spawn job decomposition policy]` returned
  the cutover/migration and lane-registry records but nothing on job
  decomposition or programmable orchestration policies. Grep of ESSENCE / AGENTS
  / INTENT / skills for `job.*decompos`, `orchestrate.*polic`, `abstract.*job`
  came back empty.
- **At-risk rationale:** This is the load-bearing description of HOW orchestrate
  works once it is a real component — the programmable-policy job-decomposition
  engine that turns mind's abstract requests into agent sequences. It is the
  design substance behind the owner-signal-orchestrate contract. Lost on
  deletion, the next orchestrate-design pass would have to re-derive it from
  scratch.

### 2. Orchestrate prefers reusing a running qualified agent over spawning a fresh one

- **Kind:** Decision
- **Proposed topics:** `[orchestrate agent-registry reuse-over-spawn agent-lifecycle]`
- **Proposed description:** Orchestrate maintains a registry of currently-running
  agents (specialized name, typed agent-type enum — designer / coding / research
  / system-specialist — and a short description) so it can prefer reusing an
  already-running qualified agent over spawning a fresh one for the same job. The
  psyche marks this as a debated lean, not hard certainty — there is something
  good about keeping agents alive rather than always spawning new — so run with
  reuse-over-spawn as the orchestrator default until evidence challenges it.
- **Proposed certainty:** High (psyche explicitly flagged uncertainty: *"maybe
  I'm wrong about that"* — do not inflate to Maximum)
- **Supporting verbatim:** *"I feel like there's something good about keeping
  some agents alive instead of just spawning a new one all the time. But maybe
  I'm wrong about that."* + *"the orchestrator would have a table for all that.
  All the agents that are known to be running… a type of agent like that that's
  already up, so we don't need to spawn a new one."*
- **Preservation evidence:** Spirit `[orchestrate agent registry reuse spawn]`
  query returned lane-registry records (irmw, udgu, w190, oso5) about the LANE
  registry shape but nothing on a RUNNING-agents registry or reuse-over-spawn
  policy. Grep of guidance for `reuse.*agent`, `keep.*agent.*alive` empty.
  `orchestrate/INTENT.md` lists "agent-run lifecycle" and "executor capacity" but
  states no reuse-versus-spawn default.
- **At-risk rationale:** A standing orchestrator default with an explicit
  certainty marker (a lean to run with, re-evaluate on evidence). It guides the
  agent-lifecycle design and is exactly the kind of carry-the-uncertainty
  decision Spirit's certainty ladder exists to hold. Nowhere else captured.

### 3. Skills live in the mind; agents load their role's skill bundle in one boot message; skills carry on-demand extension skills

- **Kind:** Decision
- **Proposed topics:** `[mind skills skill-bundle boot agent-bootstrap extension-skills]`
- **Proposed description:** The skill store lives in persona-mind. When an agent
  boots, the mind packages its role's ENTIRE skill bundle into a SINGLE message
  over the working (ordinary) channel — bundle delivery, not per-skill
  streaming — and the agent is then ready to act in its role. Skills carry named,
  described EXTENSION skills declarable in the base skill: when an agent needs
  deeper specialization mid-task, it requests the named extensions from mind over
  the same channel, delivered in the same single-message bundle shape. This lets
  agents start lean and specialize on demand instead of preloading every
  potentially-relevant skill.
- **Proposed certainty:** High (psyche stated the mechanism concretely and
  repeatedly, but it is a design-shape for an unbuilt component, not a founding
  rule)
- **Supporting verbatim:** *"All the skills are in the mind. So when the agents
  load up, they get their skills from the mind, from the working channel… the
  one message with all of the skills in the message, like skill loading."* +
  *"skills can have extensions… the agent can say, I need more specialization
  now… sends a message to PersonaMind. Give me these specialization skills."*
- **Preservation evidence:** Spirit `x92t` (role-token-driven skill loading)
  captures that each role-vector token contributes to the boot skill bundle the
  mind sends — a PARTIAL version. It does NOT carry the single-message
  bundle-delivery shape or the extension-skills-on-demand protocol.
  `mind/INTENT.md` grep for `skill` / `bundle` / `extension` returned nothing —
  mind's INTENT names work-graph / memory / policy state but not the skill store
  or skill delivery. Grep of guidance for `skills live in.*mind`,
  `extension skill` empty.
- **At-risk rationale:** The skill-delivery mechanism is a distinct piece of the
  mind↔agent contract beyond x92t's token-mapping. The extension-skills-on-demand
  protocol in particular has no preserved trace anywhere; it is the lean-start /
  specialize-on-demand design that shapes how agents are bootstrapped. Note: x92t
  preserves a weaker partial form, so this records the delivery + extension
  mechanism on top of it.

### 4. Router exposes a reachability query — agents ask which agents they can reach right now

- **Kind:** Principle
- **Proposed topics:** `[router reachability agent-communication channel-query]`
- **Proposed description:** Beyond owning channel-grant authority and delivery
  facts, the router exposes an agent-facing REACHABILITY query: an agent asks the
  router "which agents can I reach right now" and receives back the typed agent
  list (name, type, description). The reachability query is the ordinary
  agent-facing side of the router; channel open/close (grant/revoke) decisions
  are the owner-channel side. The router is the gate that opens and closes
  channels of communication agent-to-agent.
- **Proposed certainty:** High
- **Supporting verbatim:** *"the router is a kind of a gate, open, close, channel
  open, channel close between agents. So the agent can query the router to see
  what are the other agents that I can talk to right now… Give me a list of all
  agents I can reach."*
- **Preservation evidence:** `router/INTENT.md` covers routing policy, delivery
  state, authorized-channel authority, Grant/Extend/Revoke meta-signal orders,
  and message parking for mind adjudication — i.e. the owner-channel / delivery
  side is fully preserved. It does NOT mention the agent-facing REACHABILITY
  query (an agent asking which agents it can currently reach). Spirit query on
  `[router channel gate reachability messaging]` returned only an unrelated
  privacy access-gate record. Grep of guidance for `reachab`,
  `which agents.*reach` empty.
- **At-risk rationale:** The reachability-query surface is the ordinary-channel
  read-side of the router that the per-repo INTENT.md omits (it documents
  authority and delivery, not discovery). It is a concrete agent-facing
  capability that shapes the working signal-router contract. Lowest-priority of
  the four — a narrower mechanism than candidates 1-3.

## Already preserved / dropped

Scanned 61 records; judged 57 already preserved or too-specific. Confidence the
file is safe to delete (after the 4 candidates above are considered) is high. The
preservation map:

- **Promoted to ESSENCE.md** — intent#4 (persona is meta-AI / spirit is the
  animating principle, the *"what animates humans at the highest level is
  spirit"* line) is verbatim in ESSENCE.md §"Persona is meta-AI; spirit
  animates"; intent#35 (the intent protocol prevents the loss of the psyche's
  important expression) is verbatim in ESSENCE.md.
- **In INTENT.md** — intent#8 / #36 / #37 (persona is LLM-mediated end-to-end;
  components are dumb mechanism, agents are the thinking layer, any
  language-understanding decision is an LLM call) → §"Persona is LLM-mediated
  end-to-end"; intent#12 (components ship in raw form first) → §"Persona
  components ship in raw form first"; intent#20 / #21 (dynamic work-named roles
  and their creation side-effects) → role/lane sections + orchestrate/INTENT.md.
- **In skills/** — intent#2 (mind owns state; orchestrate owns machinery) is in
  `skills/intent-manifestation.md` lines 111-112 AND `orchestrate/INTENT.md`
  §Boundaries; intent#31 (today's spirit is dumb storage that trusts agent
  typing; the multi-agent auditing guardian is a future arc) is in
  `skills/intent-maintenance.md` line 210.
- **In persona-spirit/INTENT.md** — intent#3 / #5 / #6 (persona-spirit is the
  apex cognitive component, the psyche interface, spawned last, owned by nobody
  above except supervisor; spirit owns mind); intent#7 (bootstrap-policy.nota is
  the root intent / sacred-teachings shape, §"Bootstrap policy is the root
  intent"); intent#27 / #28 (restatement = separate top-level records; repeated
  similar intents = stronger signal, §"Restatement is signal by repetition");
  intent#17 → superseded by #27 (the Vec<Verbatim> shape lost to per-statement
  records); intent#18 / #29 (Entry not IntentEntry; drop the Intent prefix — also
  an AGENTS.md hard override and `skills/naming.md`).
- **In mind/router per-repo INTENT.md** — intent#39 (owner-signal-persona-mind
  owner contract); intent#56's authority/delivery half (router/INTENT.md);
  intent#49's state/machinery half (orchestrate/INTENT.md §Boundaries).
- **In live Spirit** — the engine-manager / Persona-as-engine-management naming
  (intent#40 / #42, records g31j, tq18, mazv); federation (intent on persona
  federation, record b9ao); spirit-per-engine scoping (mxmn); the persona-*
  prefix deprecation that retired most of these component names (k1i1);
  supersession lifecycle / negation / lowering / escalation / soft-removal
  (intent#11, records k12x, o24x, qkrg, kfxd, d5s2, k5y3); certainty-by-repetition
  (om3x, 7ccc); the daemon-mints-timestamp / no-client-timestamp rule
  (intent#45 / #60, implied by h7sz "daemon timestamp" and the spirit CLI skill);
  universal Tap/Untap including debug-the-debugger (intent#48 / #61, the
  component-shape Tap/Untap mandate).
- **Too specific / transient / task-only (dropped per criterion 2):** intent#1
  (persona-orchestrate must exist — a state reaction / task order, now built);
  intent#5 / #14 / #15 / #16 / #19 / #22 / #33 / #34 / #38 / #44 (sequencing and
  implement-now task orders); intent#23 / #26 (raw-MVP contract-enforcement-in-code
  and Nix-test scoping — the general "ship raw first" is preserved, the MVP
  specifics change); intent#24 (Codex/Claude harness enum field — the typed-field
  general idea is in orchestrate/INTENT.md, the specific enum members change);
  intent#25 (repository-index management — superseded by RECENT-REPOSITORIES.md /
  repos symlink mechanism); intent#30 (RecordIdentifier output-only —
  implementation detail of a built component); intent#41 / #43 (the spirit CLI is
  named `spirit` and replaces the .nota substrate — now true and live);
  intent#46 / #47 (no import logic in spirit — a one-time constraint on a built
  component, the .nota deletion this very audit serves); intent#48 (Tap/Untap
  deferral until introspect — operational scheduling); intent#52 (compaction
  threshold — left open by the psyche, too unspecified to record);
  intent#55 (skills bundle into roles — preserved as x92t / role-lanes);
  intent#57 (every agent has an open channel to mind — a working default the
  psyche flagged uncertain; borderline, but it is a channel-grant default that
  router/mind owner-channel design will revisit, judged too thin to record now);
  intent#50 (agent registry fields — folded into candidate 2).

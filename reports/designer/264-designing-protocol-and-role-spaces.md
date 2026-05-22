# 264 — Designing protocol and role spaces

*Synthesis of the 2026-05-21 psyche dump on per-role protocols,
designer-as-bridge workflow, role-spaces, and per-agent Criome
identity. Psyche framed the session as "hashish mode" / "fully
creative in design" — much is direction, not implementation. The
report's load-bearing job is the settled-vs-speculative line, so
future agents do not act on speculation as if it were settled.*

## What this report is for

Verbatims live in `intent/workspace.nota` records 35, 36, 37 and
`intent/persona.nota` records 38, 39, 40. This report is the
designer's synthesis; when prose disagrees with verbatim,
verbatim wins.

Records 35 and 36 (`Maximum`) reshape how psyche-to-agent
dialogue works *today*. Records 37–40 (`Medium`, explicitly
"designing mode") sketch a future multi-agent topology —
Git-isolated role-spaces, Criome-backed identities, short ID
prefixes, LLM-call fallback chains. None of the speculative
material is implemented; none should be acted on as settled.

## 1. The per-role protocol model

(Settled. `intent/workspace.nota` record 35 — `Maximum`.)

The psyche-to-agent interface is now framed as **protocols**, one
per role:

- **Designing protocol** — psyche talks to a designer.
- **Operational protocol** — psyche talks to an operator.
- **Poet protocol** — psyche talks to a poet.

Each protocol designs the operating skill of the role it
addresses. The same psyche prompt arriving through the designing
protocol means *"shape the system"*; arriving through the
operational protocol means *"implement what was shaped"*. The
mapping is not a personality switch — it is a contract about
what kind of attention the conversation expects.

### The role label drives interpretation

The role-label on the agent's UI window (bottom-right) tells
both psyche and agent which protocol is active. Both conform to
the protocol the label names.

**Psyche conforms to the interface.** The load-bearing shift:
the label is upstream, not the chat content. The agent does not
infer "which mode is this" — the label is the answer.

### What this means for prompt interpretation

In the designing protocol (this session), interpret psyche
prompts as shaping requests, intent statements about
architecture / vocabulary / role topology / signal-tree shape,
or critique of prior designs. Not as *"go implement now"*.
Implementation requests belong to the operational protocol; if
one slips in, hand off via report and beads (section 2), not
direct action.

### Continuity with existing role discipline

The four main roles (`operator`, `designer`,
`system-specialist`, `poet`) and their lanes per
`skills/role-lanes.md` remain canonical. What is new is the
explicit framing of the *psyche-to-agent interaction surface*
as a typed protocol per role.

## 2. The designer-as-bridge workflow

(Settled. `intent/workspace.nota` record 36 — `Maximum`.)

Within the designing protocol, the workflow is:

```
psyche  →  designer  →  designer       →  designer    →  operator
prompt     logs         writes            files          implements
           intent       report(s)         beads          via beads
```

Each arrow is a discrete step the designer carries out *before*
moving to the next. The designer is the bridge: psyche talks to
the designer, the designer publishes the substance (intent
records + report + beads), the operator consumes the beads and
implements. **The operator stays on their side**; the designer
does not jump the rail to implement.

### Contrast with the prior model

Earlier, chat carried more substance — designers would
think-out-loud, sometimes implement directly, sometimes hand
off informally. The discipline now:

- Chat carries pointers and user-attention items
  (`skills/reporting.md`); substance lives in the report.
- Intent capture is the first action of any psyche-prompt turn
  (`ESSENCE.md`, `skills/intent-log.md`).
- Operator implements via beads, not via designer telling
  operator in chat. Intent record / report / bead / code are
  an ordered pipeline; designer owns the first three, operator
  owns the fourth.

### Why the operator stays on their side

Implementation has a different shape of attention than design
— concrete code, test-first round-trips, type-error diagnosis.
The designer crossing in loses the cross-cutting view that
makes specifications carry weight (`skills/designer.md`
§"Universal capability, preserved capacity"). The bridge is
neither side.

### For the current session

Designer's output is this report, the intent records the parent
agent already captured, and — when ready — beads for operator
follow-up *on the settled bits*. **The speculative sections
below get no beads yet.**

## 3. Role-spaces as per-role Git repositories (designing-mode speculative; not yet implemented)

(Speculative. `intent/workspace.nota` record 37 — `Medium`.)

Each agent role gets its own workspace — a sub-workspace that
is itself a Git repository. The role has its own research lane
inside it; write access is mediated by Git push, gated on an
SSH key supplied to the agent at start.

This is adjacent to today's role-lane mechanism and per-role
`reports/<role>/` subdirectories, but pulls the boundary up to
repository granularity: every role becomes its own checkout.

### Open

- How does the role's sub-workspace relate to the canonical
  primary workspace (sub-tree, sibling, clone,
  orchestrator-mounted)?
- What is the shared surface — `ESSENCE.md`, `AGENTS.md`,
  `skills/`? Upstream, replicated, or per-role?
- Who creates the sub-workspace? Persona-orchestrate is the
  candidate (`intent/persona.nota` 2026-05-19T15:04:19Z —
  *"Orchestrate agent creates a new repository for its reports
  … and creates the lane in the SEMA database"*), but the
  SSH-key + Git-push surface is not sketched.
- How does claim/release coordinate across separate
  repositories? Today's `tools/orchestrate` is single-repo.

**Do not act on this section as if settled.** Psyche-led next.

## 4. Per-agent Criome identities (designing-mode speculative; not yet implemented)

(Speculative. `intent/persona.nota` record 38 — `Medium`.)

Each agent creates its own identity at start. The identity
record lives in persona-mind; the Criome public key is the
authentication anchor; agents authenticate to Criome via their
own Criome daemon; persona components can escalate to Criome
for authorization checks.

The pieces the psyche named:

- Per-agent identity minted (or issued) at boot.
- Identity record stored in persona-mind as a typed memory.
- Criome public-key pair is the auth anchor; components verify
  against the public key.
- Per-agent Criome daemon as the agent's authentication
  touch-point.
- Persona components escalate to Criome for authorization
  decisions on incoming requests.

Implication: every persona-component request carries agent
identity. The authorization check shifts from "is this the
owner socket" to "what does Criome say about this identity for
this action".

### Open

- The Criome contract for authorization checks — request/reply
  shape.
- Where identity creation happens — orchestrate at boot,
  Criome handshake, persona-mind during skill loading.
- Migration from socket-gated owner contracts to
  identity-gated authorization is undesigned.
- Relationship to the role-label discipline: identity ties to
  an agent instance, not a role; whether the role label still
  drives protocol selection or is subsumed by identity-typed
  authorization is open.

**Do not act on this section as if settled.**

## 5. Short agent identifiers (designing-mode speculative; not yet implemented)

(Speculative. `intent/persona.nota` record 39 — `Medium`.)

Companion to section 4. A `shortest_id()` method on the agent's
Criome master-identity public key yields a collision-checked
3-byte truncation; the truncation widens (up to NOTA's
namespace width) if collisions force it. The shortened form is
what gets quoted in chat and report text.

### Open

- "NOTA namespace width" needs precise grounding — NOTA does
  not currently impose an explicit identifier width; the bound
  likely lands as a future rule in `skills/nota-design.md`.
- Where the collision check runs (per-workspace, per-Criome,
  per-mind).
- Whether the shortened form is a typed field on the identity
  record, computed lazily, or cached.
- Whether `shortest_id()` lives on the public key
  (cryptographic primitive) or on an identity wrapper. The
  verb-belongs-to-noun rule (`skills/abstractions.md`) makes
  this choice load-bearing.

**Do not act on this section as if settled.**

## 6. LLM-call fallback chains (designing-mode speculative; not yet implemented)

(Speculative. `intent/persona.nota` record 40 — `Medium`.)

Each LLM call carries a default provider plus an ordered
vector of fallback providers. Each provider has
provider-specific configuration tweaks (model, temperature,
token budgets, tool whitelist, …) evaluated by the daemon. The
daemon's library is the reducer and checker — including
authorization, escalable to Criome per section 4. On default
failure, the daemon walks the fallback chain.

### Open

- Which component owns the routing — persona-orchestrate, or a
  dedicated llm-router component.
- What counts as "failure" triggering fallback (outage, model
  refusal, rate limit, content-policy refusal each have
  different retry semantics).
- Prompt-cache interaction: a fallback to a non-default
  provider goes cache-cold; real cost.
- Whether provider config is a closed sum (Anthropic, OpenAI,
  …) or a per-provider open record.

**Do not act on this section as if settled.**

## 7. Settled vs speculative — summary

| Section | Topic | Source | Certainty | Status |
|---|---|---|---|---|
| 1 | Per-role protocols (designing / operational / poet); role label drives protocol | workspace.nota 35 | Maximum | Settled |
| 2 | Designer-as-bridge workflow (psyche → designer logs → reports → beads → operator) | workspace.nota 36 | Maximum | Settled |
| 3 | Role-spaces as per-role Git repositories with SSH-key gating | workspace.nota 37 | Medium | Speculative |
| 4 | Per-agent Criome identities; component escalation to Criome for authorization | persona.nota 38 | Medium | Speculative |
| 5 | `shortest_id()` 3-byte truncation of Criome master-identity public key | persona.nota 39 | Medium | Speculative |
| 6 | LLM-call default + fallback chain with provider-specific config and Criome auth | persona.nota 40 | Medium | Speculative |

Sections 1 and 2 are immediately operative — the current session
runs under them. Sections 3–6 are direction, not implementation;
each waits on psyche follow-up before becoming designer work.

## 8. Open psyche questions

Each speculative section carries its own "open" list above;
those are designing-mode follow-ups. The two questions below
affect the settled material's reach and so are higher-priority.

**Q1 — Does the role-label-drives-protocol model (section 1)
apply already, or only once role-spaces and Criome identities
(sections 3–4) land?** The settled record reads as applying
today; the speculative sections read as the destination shape.
If the protocol framing requires the speculative substrate to
carry meaning, then sections 1 and 2 are effectively
speculative too.

**Q2 — Is the designer-to-operator bead handover (section 2)
compatible with the loosened role discipline that retired
beads' `role:*` labels (`INTENT.md` §"Roles are loose; beads
are not role-labeled")?** Section 2 implies designer files, operator
picks up; the loosened-roles record says any agent picks up
any bead by topic affinity. Reconcilable (the bead's topic
affinity happens to be operator-shaped), but the discipline is
not explicit.

## See also

- `intent/workspace.nota` records 35, 36, 37 and
  `intent/persona.nota` records 38, 39, 40 — verbatim source.
- `AGENTS.md` §"Hard overrides" — the recently-updated
  no-subagents and intent-first rules that shape section 2.
- `INTENT.md` §"Roles are loose; beads are not role-labeled"
  — the loosened-role discipline section 2 needs to reconcile
  with (Q2).
- `skills/reporting.md` — chat-vs-report discipline; section 2
  is a substantive evolution of it.
- `skills/intent-log.md` — intent-capture-first protocol that
  section 2's workflow sits on top of.
- `skills/designer.md` — designer discipline section 1
  grounds in the protocol framing.
- `skills/role-lanes.md` — the lane mechanism the speculative
  role-spaces (section 3) would generalise to whole
  repositories.

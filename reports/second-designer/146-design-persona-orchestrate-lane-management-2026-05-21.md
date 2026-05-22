# 146 — Persona-orchestrate takes over lane management

*Designer sketch in response to the psyche's question "does orchestrate
work with second-designer? otherwise lets make it, and design a better
design (move to persona-orchestrate?)". This report engages the second
half — moving lane management from bash `tools/orchestrate` into the
typed `persona-orchestrate` component. The bash registration of
second-designer is done (orchestrate/roles.list + the
reports/second-designer/ subdirectory + this report's parent lane);
this report is the design for the durable shape.*

## 0 · TL;DR

Lane management is one of three machinery surfaces persona-orchestrate
already owns per `intent/persona.nota`: agent registry, scope claims,
and the orchestration policy table. Today's bash `tools/orchestrate`
implements two of those by hand (the registry as `orchestrate/roles.list`,
claims as filesystem lock files). The typed component subsumes both,
and adds the missing lane-shape — parallel-main lanes like
`second-designer` — that the bash format doesn't natively model.

The next concrete slice is **not** to migrate today's bash interface
verbatim into persona-orchestrate's contract. Per `/137` (the
persona-orchestrate triad audit), the current `Claim` / `Release` /
`Handoff` vocabulary is lock-helper-shaped and would ossify the
wrong shape if migrated as-is. The slice is to design the typed
**lane registry + claim surface** as part of persona-orchestrate's
working contract redesign, alongside the abstract-job substrate
already named in `intent/persona.nota` 2026-05-20T17:30:00Z.

## 1 · Today's bash machinery

`tools/orchestrate` is a bash script driven by `orchestrate/roles.list`:

- **Lane registry** lives in the file. Format:
  ```
  <lane-name> [assistant-of:<main-role> | parallel-of:<main-role>]
  ```
  Comments mark file-level metadata; one lane per non-comment line.
- **Claim / release** uses per-lane lock files at
  `orchestrate/<lane>.lock`. Lock content is a NOTA-ish record naming
  the claim scope, claimer, and reason.
- **Reports subdirectory** is created manually with `mkdir reports/<lane>/`.
- **Role table in `AGENTS.md`** is hand-edited.

The format is transitional per the file's own header comment, which
already points at `orchestrate/roles.nota` as the destination format
read by a Rust-rewritten `tools/orchestrate`.

## 2 · What second-designer just exposed

Registering `second-designer` revealed two limitations of the bash
shape:

1. **The format had no marker for parallel-main lanes.** The existing
   `assistant-of:` marker says "this is a subordinate lane under that
   discipline". `second-designer` is not subordinate; it is a second
   seat at the discipline at full main-role authority. The added
   `parallel-of:` marker captures the distinction, but neither
   `tools/orchestrate` nor `skills/role-lanes.md` knows what to do
   with parallel-main lanes that the assistant-lane pattern does not
   cover.
2. **The lane mechanism in `skills/role-lanes.md` is silent on the
   shape.** The skill's lane-stack illustration shows
   `designer / designer-assistant / second-designer-assistant`, with
   no slot for `second-designer`. The skill needs a follow-up edit
   to absorb the new shape — but that edit's exact wording depends
   on the persona-orchestrate design below.

Both gaps are signals the bash shape has reached its limit. The
persona-orchestrate move is on the path the workspace already chose;
this just accelerates the calendar.

## 3 · What persona-orchestrate's contract needs to carry

Per the existing intent (`intent/persona.nota` 2026-05-18T12:08:41Z,
2026-05-19T15:04:19Z, 2026-05-19T15:30:00Z, 2026-05-20T17:30:00Z,
plus `reports/second-designer/137`) persona-orchestrate's working
contract has three logical surfaces:

| Surface | Concern | Today's bash analogue |
|---|---|---|
| **Lane registry** | Which lanes exist, what discipline each shares, what authority | `orchestrate/roles.list` |
| **Claim surface** | Which lane holds which scope right now | `orchestrate/<lane>.lock` files |
| **Abstract-job + agent-registry** | Mind→orchestrate work flow | Not implemented in bash |

The third surface is the new scope from
`intent/persona.nota` 2026-05-20T17:30:00Z and the mind-body analogy
work in `/129`. The first two are the bash transition. All three
share the daemon, the redb store, and signal-executor.

### 3.1 · Lane registry shape

**Role as vector, not string [revised 2026-05-21, intent IDs 98 + 99].**
The role of a lane is a NOTA vector of identifier tokens, not a
single discipline name. The last token is the base discipline
(Designer, Operator, etc.); preceding tokens are specialization
tokens that compose with the base.

```text
;; signal-persona-orchestrate
pub struct RoleToken(String)          ;; open identifier; user-extensible
                                       ;; per intent ID 97.
pub struct Role(NonEmpty<RoleToken>)  ;; e.g., [Designer],
                                       ;;       [Note Designer],
                                       ;;       [PersonaSignal Designer]
                                       ;; last token is the base discipline.

pub enum LaneAuthority {
    Structural,  ;; full main-role authority (structural decisions,
                 ;; skill edits, design reports).
    Support,     ;; bounded support-scope (today's `-assistant` lanes).
}

pub struct LaneIdentifier(String)     ;; the filesystem stuffed-string,
                                       ;; derived from role + authority +
                                       ;; optional ordinal.

pub struct LaneRegistration {
    pub lane: LaneIdentifier,
    pub role: Role,
    pub authority: LaneAuthority,
    ;; reports_subdirectory = "reports/<lane>/"  ;; derived; not stored
    ;; lock_file = "orchestrate/<lane>.lock"     ;; derived; transitional
}
```

#### Lane-identifier derivation

The lane identifier is the filesystem stuffed-string form of the
typed `Role` + `LaneAuthority` pair:

| Role (NOTA) | Authority | Ordinal? | Lane identifier |
|---|---|---|---|
| `[Designer]` | Structural | — | `designer` |
| `[Designer]` | Structural | second seat | `second-designer` |
| `[Designer]` | Support | — | `designer-assistant` |
| `[Designer]` | Support | second seat | `second-designer-assistant` |
| `[Operator]` | Structural | — | `operator` |
| `[Operator]` | Structural | second seat | `second-operator` |
| `[Note Designer]` | Structural | — | `note-designer` |
| `[Note Designer]` | Support | — | `note-designer-assistant` |
| `[PersonaSignal Designer]` | Structural | — | `persona-signal-designer` |
| `[System Designer]` | Structural | — | `system-designer` |

Rules:

- Vector tokens render lowercase, joined by `-`.
- `Support` authority appends the `-assistant` suffix.
- The ordinal prefix (`second-`, `third-`) is **only** present when the
  registry already holds another lane with the same (role, authority)
  pair. A lane that is the first of its specialization does not carry
  an ordinal even if a separate lane (e.g., plain `designer`) exists
  with overlap.

#### Why a vector

Three motivations:

1. **Specialization composes.** `[Note Designer]` is a designer who
   specializes in notation work; `[PersonaSignal Designer]` is a
   designer who specializes in persona-signal contracts. The vector
   captures composition without inventing a new closed enum of
   "specialized designer kinds."
2. **Skill loading derives from tokens** (intent ID 99). Each token
   in the vector contributes to the lane's skill bundle: `[Note
   Designer]` loads `skills/designer.md` plus whatever notation-design
   skills are registered for `Note`. The persona-mind skill-bundle
   delivery mechanism (`intent/persona.nota` 2026-05-20T17:30:00Z)
   walks the role vector and composes.
3. **Horizon clusterNode-role parallel.** The workspace already
   models `NodeService` as a vector of named variants per
   `intent/horizon.nota` 2026-05-20T14:50. Agent roles adopting the
   same vector pattern keeps role-modeling consistent across
   infrastructure and cognitive components.

#### The bash bridge

The bash format does not natively express vectors. During the
transition window, the existing `<lane> [marker:<role>]` flat format
remains the source of truth, with the new `parallel-of:` marker
added today. When persona-orchestrate ships, the bash file becomes
a derived view emitted from the typed registry: each registered
lane renders as one line in the file with its derived identifier.

The "second seat" property does not need a typed flag — it falls out
of the registry holding multiple `(role, authority)` records with the
same value. The ordinal in the lane identifier is computed at
registration time from the count of prior matching registrations.

### 3.2 · Claim surface — open question, deferred to /137's redesign

Today: `Claim(RoleClaim)` / `Release(RoleRelease)` / `Handoff(RoleHandoff)`.
Per `/137` these need redesign — not as a verbatim port from the bash
script. The destination question is whether claim semantics survive
into the typed contract at all (option a: claims stay, refined; option b:
claims retire as the abstract-job + agent-registry takes over scope
binding implicitly).

This report does not settle it; /137 §"Open psyche questions Q1"
already names this as needing psyche input. The lane registry (§3.1)
can land independently of the claim surface; the two are separable.

### 3.3 · Owner-signal: lane registration is policy

Lane registration / retirement / mutation is policy — who can claim
the discipline-twin authority is a workspace-shaping decision, not a
peer-callable operation. The owner contract carries:

```text
;; owner-signal-persona-orchestrate (additions)
pub struct LaneRegistrationRequest {
    pub role: Role,                ;; required; the typed vector
    pub authority: LaneAuthority,  ;; required; Structural or Support
    ;; lane identifier is derived at registration time; not supplied
}

pub enum LaneOperation {
    Register(LaneRegistrationRequest),  ;; daemon derives the lane id
    Retire(LaneIdentifier),
    SetAuthority(LaneIdentifier, LaneAuthority),  ;; rare; e.g., promote
}
```

`Register` is the user-extensible surface (intent ID 97 + 98):
psyche names the role vector and authority class; the daemon derives
the lane identifier, creates the report subdirectory at
`reports/<derived-lane>/`, and emits the registration receipt. The
mechanism is fast enough for ad-hoc role creation — a single
owner-channel command is the whole flow.

Working callers (agents on the ordinary socket) `Observe` the registry
to learn the lane set; they do not `Register`. Only the engine manager
(via the owner channel) or persona-mind (per the mind→orchestrate
policy programmability path) can mutate.

### 3.4 · Cutover discipline

The bash machinery and persona-orchestrate's typed surface coexist
through the transition. Three rules:

1. **persona-orchestrate's registry is the source of truth as soon as
   it ships.** Once the lane-registry operations land, the bash
   `orchestrate/roles.list` becomes a derived view — emitted from the
   daemon's typed records via a small read-and-render command,
   refreshed when lanes change.
2. **The bash `claim` / `release` continues to work for the
   transition window**, reading and writing the filesystem lock files
   as today. Operator can rewrite the bash to call into the daemon
   on the side; that is operator-lane work, not designer-lane.
3. **The skills update absorbs the new vocabulary** (parallel-main
   lanes, authority classes, registry as typed records) once the
   daemon's surface is real.

## 4 · Recommended next slice

In priority order:

1. **Pick `AuthorityClass` and `LaneRegistration` shape** (this report
   is the proposal; psyche confirms or adjusts).
2. **Operator extends `signal-persona-orchestrate` and
   `owner-signal-persona-orchestrate`** with the lane-registry
   operations from §3.1 + §3.3. Beads landed today (`primary-c620`)
   already cover the broader persona-orchestrate migration; this is
   one slice within it.
3. **Operator extends `persona-orchestrate` daemon** to back the
   registry surface with redb storage.
4. **Designer follow-up report on the claim surface** (§3.2) — the
   open redesign question from /137. Once claim's destination shape
   is settled, that surface can move too.
5. **Skill + AGENTS.md updates** absorbing the parallel-main lane
   shape, once the daemon is real. Defer until step 3 lands; the
   skill text shouldn't get ahead of the typed surface.

## 5 · Open psyche questions

**Q1 — Authority-class taxonomy. [Resolved 2026-05-21]** Settled at
two variants: `Structural` (full main-role authority — both first
and parallel seats) and `Support` (bounded assistant scope). The
earlier 3-variant proposal (Main / Parallel / Assistant) conflated
ordinal-position with authority; functionally `designer` and
`second-designer` are identical, so the typed flag was over-fit.
Future authority classes (e.g., observer / ephemeral) can extend
the enum if a real case names them.

**Q2 — Lane discipline-vs-name binding. [Resolved 2026-05-21,
intent ID 97]** Settled as open string. Roles are user-extensible;
the workspace should be able to add new disciplines (e.g., a future
`data` / `infrastructure` / `research` role) without bumping the
contract. Implication for the creation surface: the owner-channel
`Register` operation must be designed for rapid invocation — adding
a new role should be a single command.

**Q3 — Naming-convention disambiguation. [Resolved 2026-05-21,
intent IDs 98 + 99]** The naming reshapes around role vectors and
derivation. `second-designer-assistant` reads naturally as "an
assistant lane whose role is `[Designer]` with Support authority,
second registration" — fully consistent with the new derivation
rules. In practice, by the time a lane needs an assistant, the role
is usually specialized enough that names like `note-designer-assistant`
or `persona-signal-designer-assistant` arise naturally; the
generic `second-designer-assistant` slot is only used when no
specialization is needed. No rename required.

## 6 · See also

- `reports/second-designer/145-design-real-time-intent-recording-system-2026-05-21.md`
  — the first report in this lane (the recording-system design).
- `reports/second-designer/137-persona-orchestrate-triad-audit-2026-05-21.md`
  — the persona-orchestrate audit identifying the lock-helper vocab
  vs. abstract-job destination mismatch.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — the mind-orchestrate boundary; abstract-job + agent-registry +
  context-compaction context.
- `intent/persona.nota` records around 2026-05-19T15:04Z and
  2026-05-20T17:30Z — the persona-orchestrate scope evolution.
- `intent/persona.nota` (today's record 93) — the explicit "lane
  management moves to persona-orchestrate" Decision driving this
  report.
- `skills/role-lanes.md` — the lane mechanism; needs a follow-up edit
  to absorb parallel-main lanes once the typed surface is real.
- `orchestrate/roles.list` — the bash registry, now carrying the
  `parallel-of:` marker as a forward-compatible bridge to the typed
  shape.
- Bead `primary-c620` (Migrate persona-orchestrate triad to current
  foundation) — the broader migration this slice lives inside.

This report retires when (a) persona-orchestrate's lane-registry
surface ships and `orchestrate/roles.list` becomes a derived view,
OR (b) a successor designer report supersedes the shape.

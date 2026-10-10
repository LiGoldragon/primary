# Skill — workspace vocabulary

*Canonical glossary for load-bearing workspace terms. Every term
here has been settled in a Maximum-certainty spirit record; this
skill is the lint-style reference agents consult before writing new
ARCH text, reports, code identifiers, or chat. When a doc surface
drifts, the table here is the answer.*

## What this skill is for

The workspace settles vocabulary by spirit record (per
`skills/intent-log.md`). Settled vocabulary is binding — new writing
uses the canonical form; existing surfaces converge as they're
touched. This skill collects the load-bearing terms in one place so
agents don't have to scan the intent log to recognise a non-canonical
phrasing.

Use this skill when:

- Writing a new report, ARCH section, skill entry, or commit message
  that names one of the listed concepts.
- Editing an existing surface that uses a non-canonical predecessor
  — the rule below tells you what to converge to.
- Reviewing another agent's output for vocabulary drift.

This skill is descriptive of *settled* vocabulary only. Vocabulary
under active discussion (e.g. "nota signal" — record 8, Medium
certainty) stays in the intent log until it hardens. When a new term
settles at Maximum, add it here.

## How each entry is shaped

```
### Term — canonical form

Predecessors: <non-canonical forms> (settled in spirit record <N>)
Scope: <where the term applies>
Use it when: <one-line trigger>
Don't use it when: <named carve-out, if any>
```

Predecessors carry the spirit-record citation so the agent can
verify the settlement without a separate query. Scope notes name
where the rule binds (architecture text vs code identifiers vs
prose) — sometimes the workspace text settles before the code
follows.

---

## Load-bearing terms

### Version-pair vocabulary — `main` / `next`

Predecessors: `current` / `next`, `current_*` / `next_*` field
prefixes (settled in spirit record 181, Maximum).

Scope: every surface that names the two adjacent versions in a
handover — ARCH text, reports, contract docs, prose. The Rust field
names in `persona/src/upgrade.rs` still use `current_*` because the
wire contract calls that side "current"; rename to `main_*` is an
operator-side decision tracked separately (see "Remaining
operator-side work" below).

Use it when: writing about the version pair in a handover protocol
or upgrade flow. The active version is `main`; the version being
upgraded to is `next`.

Don't use it when: quoting verbatim psyche text or citing a code
identifier that still uses `current_*` (parenthesize the legacy name
when you reference it: "`current_owner_socket_path` (main owner
socket)").

**Branch sense (consonant).** `next` also names the standard designer
development **branch** — the per-repo branch where breaking changes are
developed before an operator integrates them to `main` (Spirit 2556 —
[designers work on a standard next branch by default; operators own main
and integrate from next]). The two senses are consonant: the `next`
branch is where the `next` version gets built. The `-next` *repo suffix*
(`nota-next`, `schema-next`, `schema-rust-next`) is **legacy** — it came
from the retired practice of spinning up successor repos for major breaks.
That practice is retired (Spirit `op4b` / `53bj`, 2026-06-07): major
breaks are **branches**, and a new repository is only for a genuinely new
project (`skills/repository-management.md` §"When to create a new
repository"). The surviving `-next` repos are canonical-by-default-use
crates that were never renamed back; treat the suffix as a name, not a
license to make more. Branch-workflow discipline lives in
`skills/feature-development.md` and `skills/double-implementation-strategy.md`.

### Component name — `Persona`

Predecessors: `Persona Engine Manager Daemon`, `Persona engine
manager daemon`, `engine-manager daemon`, `persona engine` (when
referring to the component, not the AI-work scope below) (settled
in spirit records 215 + 216, both Maximum).

Scope: the conceptual entity carries the short name "Persona".
Concrete name surfaces:

| Surface | Canonical form |
|---|---|
| Repo | `persona` (lowercase, at `/git/github.com/LiGoldragon/persona`) |
| Daemon binary | `persona-daemon` |
| CLI binary | `persona` |
| Conceptual entity | Persona |
| Role / relation | engine-management (what the daemon does) |

"Engine-management" names the **role** Persona plays — the daemon's
external-facing concern. "Persona" names the **entity** — the
implementation that fills the role. Engine-manager-as-noun, used to
refer to the daemon itself, is the non-canonical form. Use "Persona"
or "persona-daemon" depending on whether the prose talks about the
conceptual entity or the running binary.

Use it when: naming the component itself (the engine-management
entity), the daemon binary, the CLI, or the repo.

Don't use it when: referring to the larger AI-work scope of the
stack. Per spirit record 152 (Maximum), **"Persona engine"** is
specifically the AI-work part of the Criome stack — the
agent/harness/mind-state surface, not the engine-management daemon
itself. The carve-out is real and the longer phrase stays in scope
for that meaning. The workspace stack as a whole is "the Criome
stack". Use the longer phrase only when the AI-work meaning is the
intended one; otherwise default to "Persona".

### Engine-management socket axis — `engine_management` (not `supervisor` / `supervision`)

Predecessors: `supervisor`, `supervision_socket_path`,
`supervision_socket_mode`, `.supervision.sock` constants,
`SupervisionSupervisor`, `signal_persona::supervision` module
(settled in spirit records 199 + 240, both Maximum; per
`primary-u8vo` this is step 0 of the `/257` contract migration
sweep).

Scope: every surface that names the **Persona ↔ supervised-component
authority relation** — the typed cross-engine management surface
where the Persona daemon manages component lifecycles, observes
health, drives the spawn envelope, and listens for component
readiness. The deployed code already uses the canonical snake_case
form in `signal-persona` and `persona/src/`; the rename target is
the same form everywhere.

| Where | Predecessor | Canonical |
|---|---|---|
| `signal-persona` module | `supervision::` | `engine_management::` |
| Socket-path identifiers | `supervision_socket_path` | `engine_management_socket_path` |
| Socket-mode identifiers | `supervision_socket_mode` | `engine_management_socket_mode` |
| File-name constants | `.supervision.sock` | `.engine_management.sock` |
| Wire-vocabulary types | `Supervision*` | `EngineManagement*` |
| ARCH prose | `supervision socket` | `engine-management socket` |
| Prose role-noun | `the engine-manager (daemon)` | "Persona" or "the Persona daemon" (per record 215; do not use `engine-manager` as a noun) |

Use it when: writing about the Persona ↔ supervised-component
relation — the typed authority surface where the Persona daemon
manages component lifecycles, observes health, and drives the spawn
envelope.

Don't use it when: the term `supervisor` / `supervision` refers to
something else — Kameo supervision-tree topology (`EngineSupervisor`
inside the persona repo, Kameo parent-child supervision graphs),
systemd unit-supervision, or generic operating-system
process-supervision. Those are unrelated technical uses and keep
their established names. The rename targets the Persona-specific
socket and contract surface (`signal-persona` module, daemon
configuration fields, ARCH prose around the Persona ↔ component
authority relation) — not every occurrence of `supervisor`.

## Remaining operator-side work

Several canonical-vocabulary axes carry Rust-side work that is
operator-scoped, not designer-scoped:

- **`current_*` → `main_*`** field renames in
  `/git/github.com/LiGoldragon/persona/src/upgrade.rs`. Tracked
  separately; operator chooses whether to land alongside the
  next handover-driver code change or as a standalone rename.
- **`supervision_*` → `engine_management_*`** identifier and
  constant renames across the `persona` and `signal-persona`
  source trees (17 identifiers + 8 constants per `/282` Axis 2
  inventory). The deployed `signal-persona` and `persona/src/`
  already use `engine_management::` and `engine_management_*` in
  several places; remaining occurrences (`SupervisionProtocolVersion`,
  `Supervision*` reply types, `supervision_socket_path` /
  `.supervision.sock` constants in adjacent crates) follow.
  Tracked under bead `primary-u8vo` as step 0 of the contract
  migration sweep.

When operator lands these renames, the ARCH text and reports already
carry the canonical vocabulary; the parenthetical bridges in this
skill and in `persona/ARCHITECTURE.md` §1.6.7 can then retire.

## How to apply

When writing new content, use the canonical form. When editing an
existing surface that uses a predecessor, converge it in the same
edit — vocabulary drift compounds the longer it's left unfixed, since
every new report and ARCH section written against the old form needs
re-edit later. The exception is verbatim quotes from older psyche
text or older operator commits: those preserve their original
wording, because the historical record is what it is.

When in doubt about whether a phrase falls under "Persona" (the
component) or "Persona engine" (the AI-work scope per record 152),
ask: *is the prose talking about the engine-management daemon — the
thing that supervises components, owns the engine catalog, drives
upgrades — or about the AI-work surface — the agent/mind/harness
collaboration that an engine hosts?* The first is "Persona"; the
second is "Persona engine".

## See also

- spirit record 181 (canonical version-pair `main` / `next`).
- spirit records 215 + 216 (canonical component name `Persona`).
- spirit records 199 + 240 (engine-management socket rename;
  systemd-template lifecycle).
- spirit record 152 (carve-out: "Persona engine" for the AI-work
  scope of the Criome stack).
- spirit record 249 (this skill's settling: vocabulary sweep +
  glossary skill landed as a one-shot designer pass).
- `~/primary/skills/naming.md` — the upstream English-words + no-
  ancestry pair of rules; this skill is the vocabulary-specific
  application.
- `~/primary/skills/intent-log.md` — the five-kind taxonomy and the
  gold-mining discipline; this skill collects settled vocabulary
  from the log.
- `~/primary/skills/component-triad.md` §"Vocabulary" — the upstream
  triad-shape vocabulary (component triad, working signal, policy
  signal, signal types, signal tree) lives there, not here. Only
  workspace-wide terms that have specifically been the subject of a
  spirit-record settlement appear in this skill.

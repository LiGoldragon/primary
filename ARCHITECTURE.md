# primary — architecture

*The coordination workspace. It owns discipline, protocols, skills,
reports, and the authoritative inventory of active code repos. It holds no
shipping software; everything that ships lives in a repo under
`/git/github.com/LiGoldragon/`.*

> Workspace, not component. The shapes below describe how agents
> share a working surface — claim flow, lane ownership, document
> precedence — not a runtime topology.

## 0 · TL;DR

`primary` is the workspace at `~/primary/`. Work is organised by generated
**role packets** and **session lane**. Role packets carry the doctrine bundle,
authority shape, and output contract required for normal role work. A **lane**
is one work session named for its intent (`newLanesDesign`,
`schemaWorkAudit`); it carries role/discipline metadata, owns its own lock file
and report directory, and drains and retires at session close. The lane
mechanism is canonical in the generated `session-lanes` skill packet. Active
code lives in
`/git/github.com/LiGoldragon/` checkouts, inventoried by
`protocols/repos-manifest.nota`. Workspace vision and the durable intent framing
live in this file (§"Workspace vision and intent"); the raw psyche-statement
log lives in the deployed Spirit store. Cross-workspace agent discipline
lives in `/git/github.com/LiGoldragon/lore/AGENTS.md`.

The workspace is the apex of the agent-discipline graph: the Spirit store
(raw psyche statements) and this file's durable vision/intent framing,
then `lore/AGENTS.md`
(cross-workspace contract) → `orchestrate/AGENTS.md` (this workspace's
coordination), then the generated role packet (curated doctrine bundle),
then per-repo `AGENTS.md` + `ARCHITECTURE.md` + `skills.md`. Durable
direction, vision, and telos are recorded in `ARCHITECTURE.md` files (or
code stubs with explanatory comments) and the Spirit store, never in a
workspace `ESSENCE.md` or `INTENT.md`.

## 0.5 · Workspace vision and intent

This section is the durable home for the workspace's vision and the
intent-layer framing. It absorbs the content that previously lived in the
eliminated `ESSENCE.md` and workspace `INTENT.md`; the per-statement source
of truth is the deployed Spirit store, and the topic disciplines live in the
generated skill packets named below.

### What the workspace is building

Persona — a meta-AI system that organises models into a structure emulating
human intelligence, animated by persona-spirit. Components are dumb
mechanism; the thinking happens in agent LLMs that drive them through CLIs
and through Spirit — no component works without an LLM on the other end of
the wire. Components ship in raw form first (standalone CLI + daemon +
durable state) and are used individually before component-to-component
wiring lands.

The end is software eventually impossible to improve — in a bounded domain,
the right shape, chosen carefully, observed cleanly. In priority order,
earlier wins on conflict: **clarity** (the structure of the system is its
own documentation), **correctness** (every typed boundary names exactly what
flows through it), **introspection** (state is visible from outside; derived
values do not hide), and **beauty** (not pretty, but right — ugliness is
evidence the underlying problem is unsolved). What is *not* optimised for:
speed, feature volume, "minimum viable", "ship fast", backward compatibility
for systems being born, or time estimates — the right shape now is worth
more than a wrong shape sooner. The beauty gate is canonical in the generated
`beauty` skill packet; full-English naming is canonical in the generated
`naming` skill packet.

**Backward compatibility is not a constraint for systems being born.** Break
the system if it makes it more beautiful — not carelessness, but refusal to
compromise design to preserve a wrong shape. Compatibility binds only at
explicitly-declared boundaries: published APIs under semantic versioning,
wire contracts pinned by version, schemas externally consumed beyond our
control. Before such a boundary is declared, the system is being shaped, not
preserved. The version-surface mechanics are canonical in the generated
`versioning` and `feature-development` skill packets.

### The intent layer

Intent is primordial: an agent unsure what to do falls back on intent. The
psyche is the human; only the psyche is the source of new intent — agent
messages and agent-written files are not. When intent is unclear, absent, or
contradicted, ask rather than infer; inferring intent the psyche did not
state is forbidden. Intent is rare, and the default response to an utterance
is not to capture. The deployed Spirit store is the raw psyche-statement log
and the sole intent substrate; supersession is always explicit and only the
psyche can supersede. The capture/classification discipline is canonical in
the generated `intent-log`, `intent-clarification`, and `intent-manifestation`
skill packets. Durable direction and vision for a repository land in that
repo's `ARCHITECTURE.md` (or a code stub with an explanatory comment), never
in a per-repo or workspace `INTENT.md`.

### Push, not poll

Polling design is forbidden: producers push events; consumers subscribe.
When a mechanism appears to offer only polling, escalate deeper into the
stack and build or use a real event surface rather than tuning sleep
intervals or adding fallback polling. The application discipline — including
the patterns that look polling-shaped but are not — is canonical in the
generated `push-not-pull` skill packet.

### Today and eventually — different things, different names

When a concept has both a today's form and an eventual encompassing form,
the docs explicitly mark that boundary and give the two forms distinct names:
`sema` (today's typed storage kernel) / `sema-engine` versus the eventual
`Sema` (the universal medium for meaning); `criome` (today's BLS auth daemon)
versus the eventual `Criome` (the universal computing paradigm in Sema). ARCH
docs describe what is built today; eventual scope gets an explicit marker.
This is a scope discipline, not a quality one — "today's piece" is never a
license to cut corners. `protocols/active-repositories.md` carries the live
per-repo today-vs-eventual distinctions and cites this anchor.

## 0.6 · Shared component architecture patterns

These are the cross-cutting patterns every component repo follows. They are
workspace canon because the *pattern* repeats across repos; each repo's
`ARCHITECTURE.md` owns its component-specific detail. Stated here so a fresh
agent reads the shape once and recognises it everywhere.

### The runtime logic triad: Signal / Nexus / SEMA

Each component engine defines its **Signal**, **Nexus**, and **SEMA**
interfaces in schema and runs its core logic through schema-emitted traits over
root types, with strict ownership:

- **SEMA** owns durable state and storage (the body at rest).
- **Nexus** owns decision-making and request execution — it is the execution
  engine.
- **Signal** owns communication (movement across channels).

The request flow is `Signal in → Nexus → SEMA (on state work) → Nexus → Signal
→ client`. The engine-role names are *traits*, not one component's enum. This
runtime **logic** triad is a different thing from the repository **packaging**
triad below; do not conflate them. The shared daemon concurrency primitive (the
bounded thread-per-connection worker model that serves many connections without
blocking on a long operation) lives once in the reusable `triad-runtime`
component and is consumed by every triad daemon, never reimplemented per
component. When describing the runtime, only real Kameo actor nouns get actor
wording; Tokio listener loops are async/task-backed shells with actor-backed
admission when they use `RequestGate`.

### The packaging triad: two contracts per component

Every component has exactly **two** wire contracts — no third, no owner/working
split:

- `signal-<component>` — the ordinary working/peer-callable signal.
- `meta-signal-<component>` — the meta policy/authority signal (configuration,
  owner-only operations). `MetaSignal` is canonical; `OwnerSignal` is
  deprecated, and from-scratch policy contracts are born meta-signal.

Each contract exposes one thin CLI client (`<component>` and `meta-<component>`).
Every daemon binds and serves its **meta socket** at runtime even when its only
operation is `Configure`; the policy/control socket is called the *meta socket*,
not the owner socket. Configuration is changed only through the meta-signal
surface, so configuration is unreachable from the ordinary working signal. A
component with an owner gains the meta tier so owner identity arrives as
authenticated policy without redeploy; meta-signal is optional only for
genuinely ownerless components, and if no separate meta-signal repo exists the
component repo itself carries the meta-signal surface. Splitting the contract
into separate `signal-<c>` and `meta-signal-<c>` repos buys rebuild-churn
isolation, security visibility, and optionality — it is compilation/dependency
isolation and authority clarity, not where state or logic lives.

A component with **two authority surfaces** uses the two-contract triad
directly: two schemas, each emitting its own Signal/Nexus/SEMA engines and
sharing record types; the runtime imports both and runs two listeners on two
sockets (an owner-authenticated meta socket and a peer-callable ordinary
socket).

### Component binary naming

Each component has a CLI half `<component>` and a daemon half
`<component>-daemon`; the role name is not itself a binary. The `orchestrate`
COMPONENT (the repo) is the runtime that runs the set of component daemons — not
the act of orchestrating.

### Engines are match-matrices over enums

Most workspace logic is a **match between two domains**: domain A enum × domain
B enum, where the logic is the outcome per cell of that matrix. Cells with no
defined behavior return a typed error or help (`Unavailable`, etc.); the error
surface IS part of the trait surface. Engine operations expose these
tree-to-tree and enum-to-enum matching surfaces. Every actor carries its own
channel-contract schema declaring base `ACTION` (what it can do) and `RESPONSE`
(what it can say) enums plus a universal `Unknown` response; execution is
fan-out — one interaction-actor decision emits multiple parallel outputs, closed
per interact-trait variant. When an interaction needs engine state, including
outbound queries like Criome authorization, it becomes **async**: the actor
system handles the wait while other work continues, and state access is
implicit (the interacting object queries state through the engine without the
caller threading it).

### Wire and identity discipline

- **No NOTA between components.** Daemons exchange binary protocol data; the CLI
  is the translation/debugging surface (it can wrap a normal call in a debugging
  request that says where logs are displayed or stored). `SEMA` is the compact
  data format defined by schema.
- **Origin route as implicit return address.** Every message carries an origin
  route as automatic, *un-schema-declared* metadata — a short statistically
  unique identifier that travels Signal → Nexus → SEMA and back, so a reply is
  associated with its originating query on return. It is internal to each
  component and need not be a long hash.
- **Schema is the source of truth.** Schema is the macro-language source of
  truth for component data, wire, storage, and upgrade behavior, and the textual
  representation of the psyche's idea language — not merely a codegen input but
  the text form where the idea language is expressed and authored. The
  schema-derived stack uses separate repos for `nota-next`, `schema-next`, and
  `schema-rust-next` rather than one combined repo.
- **Fully-qualified symbol path is universal identity.** The
  fully-qualified-symbol-path is the workspace's universal machine-readable
  symbol identity, surfaced through a text form. Schema-emitted Rust types and
  NOTA renderings are two projections of one symbol-path identity space; designs
  use this canonical mechanism rather than inventing per-design alternatives.
- **Shortest reliable identifier is first-class.** Opaque content-addressed
  hashes (blake3/sha) cost roughly one token per character in agent context,
  logs, and reports. The full digest stays canonical identity; the exposed
  locator is a stable shortened form, never renamed once exposed.
- **Help is a noun.** `Help` is the documentation entity itself, not a verb:
  bare `(Help)` is top-level help, and walking the symbol path to `Help`
  retrieves that node's documentation. Help is schema data in a mirror
  description namespace over the global symbol namespace, with generated defaults
  when no explicit entry exists.
- **LLM prompt prose lives in plain-text files**, included at build time via
  `include_str`, so the binary stays self-contained while the prose is edited as
  data.

### Privilege and authentication boundaries

- A content/data daemon's privilege boundary is *can-ingest-and-serve-content*,
  not *can-read-anything-on-the-system*. Its store stays unwritable by anything
  except the daemon itself (even root writing it is misbehavior); it has no
  ambient access to private-key material and, handed a path to a private key,
  must be unable to read it.
- Owner-socket peer-credential authentication via `triad-runtime`
  `ConnectionContext` `SO_PEERCRED` rejects on a uid mismatch and **fails
  closed** for the privileged owner meta tier, as defense in depth complementing
  the socket file-mode guard.

### Components must prove themselves on the live path

Newly designed components must actually drive the live system end to end — the
three engines, trait-defined ordering, typestate mail, and origin route are the
real execution drivers, not dead scaffolding beside an older code path. Verify
in implementation that every designed component is on the live path. Rolling the
workspace forward to latest intent completes only when the superseded path is
removed: wrapping an old path is not migration, compatibility surfaces are
dropped once superseded, and dead/duplicate/stub repos are archived.

## 0.7 · Terminology and naming canon

Workspace-wide term and spelling canon. Per-repo today-vs-eventual term
distinctions live in `protocols/active-repositories.md` (§"Today and eventually"
above); full-English-word naming is canonical in the generated `naming` skill
packet. This section records only the cross-cutting decisions an agent must
honor everywhere.

### Component and term spellings

- **criome** spells the authentication component; **criomos** spells the
  operating system. On-disk path and code-identifier spellings are preserved
  when cited verbatim.
- **mentci** is the psyche-facing approval component (repos `mentci-egui`,
  `mentci-lib`); the earlier "Menchie" spelling was a speech-to-text error and
  is migrated to mentci.
- **Persona** is the canonical short name for the engine-manager entity
  (engine-management is its role): repo `persona` (lowercase), binary
  `persona-daemon`. "Persona engine" is acceptable for the AI-work part but
  Persona is preferred; converge older phrasings ("engine-manager daemon") to
  Persona. Disambiguation suffixes apply only when wrapping a backend
  (`persona-codex`, `persona-pi`, `persona-claude`). The whole workspace stack
  is the **Criome stack**.
- **sema**: speech-to-text may hear *sema* as *sim*; normalize to **sema** before
  storing verbatim.

### The three-part vocabulary

- **SCHEMA** is the specification part — it specifies both signal and sema, and
  is the textual representation of the psyche's idea language.
- **SIGNAL** is the movement (transport) — it carries movement across channels.
- **SEMA** is the body — data at rest, state — and is the compact data format
  defined by schema.

This closes the loop between specification, transport, and state.

### "signal" the noun is ambiguous

When the psyche says "signal" (the bare noun), it may mean the rkyv-encoded
binary signal traveling on a socket or the NOTA-encoded text signal that agents
read and write; disambiguate when context does not pin the form. The term "nota
signal" for the text form is *proposed but not yet hardened* into workspace
vocabulary.

### Version vocabulary

- **NEXT** is the in-progress version being authored — authors always write from
  next's view.
- **MAIN** (current/main) is the current published canonical baseline, imported
  as the comparison point — the deployed production version.
- **PREVIOUS / LAST** is the prior iteration of any contract, schema, message
  format, or data shape.

If `main == next` nothing changed and no upgrade path compiles; if `main != next`
the machinery generates the From-chain from main to next. The shorthand
**version-pair** vocabulary is current/main (deployed) versus
proposal/dev/next (new version being introduced).

### Lane vocabulary

- **concept-designer** is an ephemeral occasional invocation, not a persistent
  named lane.
- **system-operator** is an operator lane for implementation when the psyche
  explicitly directs it to work production code — not only a deploy-or-report
  lane.

## 1 · What lives here

```text
~/primary/
├── AGENTS.md              workspace-specific agent instructions
├── CLAUDE.md              Claude-flavored shim → AGENTS.md
├── ARCHITECTURE.md        this file
├── protocols/
│   ├── repos-manifest.nota      authoritative repos inventory (NOTA)
│   ├── active-repositories.md   active-repo attention map + role narrative
│   └── retired-lanes.md         append-only retired-lane index
├── .agents/skills/        generated workspace skill packets
├── .codex/agents/         generated Codex role packets
├── .pi/agents/            generated Pi role packets
├── .claude/agents/        generated Claude role packets
├── skills/                generated inventory files
├── reports/<lane>/        session-lane report directories (drain at close)
├── repos/                 residual local checkouts (index retired; see §3)
├── orchestrate/           coordination protocol, daemon CLI, per-lane lock projections
├── RECENT-REPOSITORIES.md superseded stub → protocols/repos-manifest.nota
└── primary.code-workspace VS Code workspace marker
```

`.beads/` exists as a transitional short-tracked-item store
(see `AGENTS.md` §"BEADS is transitional"); destination is Persona's
native typed work graph.

## 2 · Roles and lanes

Generated role packets carry each role's substantive working doctrine. They
include curated critical modules and dependency-expanded modules, so routine
role work starts from the packet.

A **discipline** is a permanent identity — skills, authority class,
mind memory, signing key. It names *what kind of agent this is*.
A **lane** is one work session named for its intent; it carries a
role/discipline as metadata (the last token of its orchestrate registry role
vector, e.g. `[NewLanesDesign Designer]`), owns `orchestrate/<lane>.lock` and
`reports/<lane>/`, and is created, drained, and retired per session.
Specialized scope is expressed as the session's intent plus specialization
tokens ahead of the discipline. Lanes register and retire dynamically through
the orchestrate daemon (`Register` / `Observe Lanes` → `LanesObserved` /
`Retire`). The full lane lifecycle —
register, smart-zone, fleet, drain, retire — is canonical in
the generated `session-lanes` skill packet.

`orchestrate/<lane>.lock` files coordinate claims on shared resources
(repos, files); the orchestrate daemon is their canonical writer and the
lock files are projections. `reports/<lane>/` directories are
lane-owned: each lane writes only its own directory, and report
directories are exempt from the file-claim flow. When a lane drains, its
report directory is deleted (git history and the session transcript are
the archive) and one row is appended to `protocols/retired-lanes.md`.

### Role pairing and per-role isolation (direction)

Roles pair an advisor and an executor. Designer advises on structure;
operator executes. Counselor and assistant mirror that pair for the psyche's
private affairs (personal, business, family, friends logistics): counselor
advises on structure, assistant executes, and the pair handles private affairs
by default.

The intended isolation substrate is **role-space**: each agent role gets its own
sub-workspace that is its own Git repository (designer-space, operator-space,
poet-space, etc.), each with its own research lane. Write access is gated through
Git push, gated in turn on the agent's SSH key set when the agent starts, so
push permissions bind to whichever agent currently holds that role. This is a
recorded design direction — much of it is not yet implemented.

Bird/Aether maintains her own forked workspace and soul repositories, separate
from this workspace.

## 3 · Repos surface

`protocols/repos-manifest.nota` is the authoritative inventory of LiGoldragon
repos: a NOTA manifest recording, per repo, its name, remote, family, status
(`Active` / `Content` / `Deprecated`), doctrine-home, and fact-flags (`IsFork` /
`IsPrivate` / `BuildTimeConsumed` / `DataRepo`). It is the single source of truth
for what repos exist and their status, and it supersedes the inventory role of
both `RECENT-REPOSITORIES.md` (now a superseded stub) and
`protocols/active-repositories.md` (retained as the active-repo attention map and
per-repo role narrative). A coverage or doctrine run reads the manifest, filters
`status = Active`, and iterates `/git/github.com/LiGoldragon/<name>` directly —
membership no longer depends on which `repos/` symlinks happen to exist.

The `repos/` symlink index has been retired. Agents reference canonical
checkouts at `/git/github.com/LiGoldragon/<repo>/` directly (for example
`/git/github.com/LiGoldragon/lore/AGENTS.md`); membership and status come from
the manifest. `repos/` now holds only residual local working checkouts and a few
convenience symlinks pending migration to their canonical `/git` homes; it is
neither the repo inventory nor the coverage or reference surface.

Components ship from those repos. primary itself ships no code; it is
the coordination surface that holds the rules under which the code is
built.

## 4 · Boundaries

This workspace owns:

- Workspace vision and the durable intent framing (this file,
  §"Workspace vision and intent"), anchored to the Spirit store.
- Discipline and lane discipline (`AGENTS.md`, `CLAUDE.md`).
- The coordination protocol (`orchestrate/AGENTS.md`), the authoritative repos
  inventory (`protocols/repos-manifest.nota`), and the active-repo attention map
  (`protocols/active-repositories.md`).
- Generated workspace skill packets (`.agents/skills/<name>/SKILL.md` and
  harness-specific peers).
- Session-lane report directories (`reports/<lane>/`) and the
  retired-lane index (`protocols/retired-lanes.md`).
- Per-lane coordination state (`orchestrate/<lane>.lock`, daemon-owned).

It does not own:

- Shipping software (lives in repos under `/git/...`).
- Per-repo discipline (`AGENTS.md`, `ARCHITECTURE.md`, `skills.md`
  inside each repo).
- The canonical cross-workspace agent contract (lives in
  `/git/github.com/LiGoldragon/lore/AGENTS.md`).
- Persistent agent memory beyond workspace files. Harness-private state is not
  a default memory substrate; Claude auto-memory is allowed only through an
  explicit opt-in launch path.

## 5 · Constraints

- The `repos/` directory must remain untracked; it holds local repository
  checkouts and convenience symlinks, and tracking it would turn repository
  coordination into needless churn.
- The workspace carries a gitignored top-level `private-repos/` directory for
  private repositories, kept separate from the `repos/` local checkout directory.
- The Nix store is never a workspace search surface; agents never run
  generic filesystem search against `/nix/store`. Use Nix evaluation
  paths instead.
- Every identifier is a full English word (`Request` not `Req`,
  `Reply` not `Rep`, `Configuration` not `Cfg`). See the generated
  `naming` skill packet.
- Reports are agent-consumable durable records written as fresh-context
  pickup points; chat is the user's working surface. A chat reply for
  the user is never a bare pointer to a report; user-attention items go
  inline. See the generated `reporting` skill packet.
- Permanent docs (`ARCHITECTURE.md`, `skills.md`, `AGENTS.md`) inline
  load-bearing claims; they don't cite reports. See the generated
  `architecture-editor` skill packet.
- BEADS tasks are never ownership locks. Any agent may create, update,
  comment on, or close BEADS tasks at any time.
- Memory belongs in workspace files every agent can read; harness-private state
  stores, including Claude auto-memory, are gated opt-in paths rather than
  defaults.

## 6 · Invariants

- Intent precedes structure: the intent layer (the Spirit store, with its
  durable framing in §"Workspace vision and intent") is upstream of every
  rule below it. A downstream rule that conflicts with intent loses.
- A discipline is a permanent identity; a lane is a throwaway session
  that carries one. Both are coordination structure, not security
  boundaries.
- The workspace is the apex of agent discipline; component
  architectures live in their own repos.

## See also

- §"Workspace vision and intent" (this file) — the durable home for
  workspace vision and the intent-layer framing.
- §"Shared component architecture patterns" (this file) — the cross-cutting
  patterns every component repo follows.
- §"Terminology and naming canon" (this file) — workspace-wide term and
  spelling canon.
- `AGENTS.md` — workspace-specific agent instructions.
- `orchestrate/AGENTS.md` — discipline-and-lane coordination.
- `session-lanes` skill packet — the lane mechanism and lifecycle.
- `protocols/active-repositories.md` — current active repo set.
- `/git/github.com/LiGoldragon/lore/AGENTS.md` — the canonical agent-discipline
  repo this workspace points at.
- `architecture-editor` skill packet — the rules this file follows.

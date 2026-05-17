# Orchestrate arc — roles as config, mutable via owner-socket

*Captures user direction (2026-05-17): the lane registry should live as
data loaded from config at startup and mutable via the
owner-signal-persona-orchestrate surface, not as a closed enum in the
signal-persona-mind contract. This supersedes the three resolution paths
in `reports/second-operator-assistant/1` §3 for the RoleName gap and
adds a `LaneRegistry*` family to the owner contract sketched in DA/116
§8.2.*

Date: 2026-05-17

Author: second-designer-assistant

---

## §1 — Assumed context

This report sits on top of work already canonical:

- **OwnerSignal design** — `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md`
  (the dedicated report; §13 captures the five settled answers, including
  per-component Unix users/groups, `owner-signal-<component>` naming, the
  candidate owner graph, the OwnerSignal chain end-to-end in first pass,
  and the one-actor-per-Signal-contract CLI rule).
- **Orchestrate integration** — `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md`
  (records vs machinery split; full-triad-daemon decision; the four
  layers — workspace helper, mind, orchestrate, persona-daemon).
- **Triad shape** — `skills/component-triad.md` (four invariants:
  one Signal peer per CLI; Signal-only daemon external surface;
  per-variant verb mapping; sema-engine state).
- **Shipped Rust port + RoleName gap finding** —
  `reports/second-operator-assistant/1-rust-port-of-tools-orchestrate-2026-05-17.md`
  (`signal_persona_mind::RoleName` is a closed 8-variant enum;
  `orchestrate/roles.list` registers 11 lanes; second-tier lanes
  currently collapse onto first-tier in the typed projection; three
  resolution paths proposed for designer).
- **Helper protocol** — `orchestrate/AGENTS.md` (claim/release/status
  + lock-file format).

The persona-orchestrate design tracked by bead `primary-699g` is the
forward arc; the operator pickup `primary-68cb` shipped at commit
`1730087a` and is closed.

---

## §2 — The direction

> Roles should come from a config at startup, and be modifiable with
> the owner-socket — so they aren't a runtime enum, but a record of
> sort.

Translated into the workspace's vocabulary:

1. **The lane registry is data, not type-system shapes.** The current
   `orchestrate/roles.list` is the seed; the eventual `orchestrate/roles.nota`
   is the typed Nota form. Either way, the *set* of lanes is loaded
   from configuration at daemon startup and persisted in the
   orchestrate daemon's sema-engine state, not enumerated as enum
   variants in any `signal-*` contract crate.

2. **Adding / modifying / retracting a lane is an owner-Mutate
   operation.** Through `owner-signal-persona-orchestrate` (per DA/116
   §8.2), the owner (per the candidate owner graph in DA/116 §9,
   `persona-mind`) can register a new lane, retire an existing lane,
   or adjust a lane's metadata (its `assistant-of` main role, its
   beads label policy, etc.) at runtime. Subordinate components
   observe registry changes via push subscriptions per
   `skills/push-not-pull.md`.

3. **`signal_persona_mind::RoleName`'s closed enum disappears.** The
   contract surface that carries a lane identifier becomes a typed
   `LaneIdentifier` (newtype around a string or hash-based stable id)
   that doesn't constrain *which* lanes exist. The set of valid
   identifiers is a runtime question answered by orchestrate's
   registry, not a compile-time question answered by enum variants.

4. **This is a fourth resolution to the RoleName gap.** In addition
   to operator's three paths in `second-operator-assistant/1` §3
   (keep the collapse / add three variants / collapse to four main
   roles), the user's direction is:
   - **Path 4 — registry as data.** Remove `RoleName` from the
     contract as a closed enum entirely. Lane identifier becomes a
     newtype carrying an opaque-to-the-contract identifier. The
     orchestrate component owns the *set* of valid identifiers as
     mutable state; mind's `RoleClaim` etc. records reference lanes
     by identifier but don't enumerate them.

   Path 4 dissolves the gap rather than resolving it. There's no
   "missing variant" if there are no variants. New lanes
   (`third-designer-assistant`, future roles for the planned raw-LLM
   executor, ad-hoc lanes for specific multi-agent collaborations)
   land via owner-Mutate without recompiling any contract.

---

## §3 — Implications

### §3.1 — For `signal-persona-mind`

The lane identifier in `RoleClaim`, `RoleRelease`, `RoleHandoff`,
`RoleObservation`, `ActivitySubmission` changes shape:

| Before | After |
|---|---|
| `RoleName` (closed 8-variant enum) | `LaneIdentifier` (newtype around stable id) |

The contract no longer enumerates lanes. Wire round-trips still work;
the parser accepts any well-formed lane identifier; validation that
"this identifier refers to a known lane" moves to a runtime check
against orchestrate's registry (when persona-orchestrate is live) or
against the loaded `orchestrate/roles.list` (during the shell-helper
era).

Open shape question: is `LaneIdentifier` a string newtype
(`LaneIdentifier(String)`), a hash-addressed identifier (per
`ESSENCE.md` §"Versioning on the eventual stack"), or a typed slot
allocated by the registry (per `ESSENCE.md` §"Infrastructure mints
identity")? See §4 Q1.

### §3.2 — For `owner-signal-persona-orchestrate`

A new request family lands in the owner contract per the verb-mapping
discipline (`skills/contract-repo.md`):

| Family | Verb | Origin | Notes |
|---|---|---|---|
| `RegisterLaneOrder` | `Mutate` | owner → orchestrate | Add a new lane to the registry. Carries lane identifier + metadata (`assistant-of`, beads label, etc.). |
| `RetractLaneOrder` | `Retract` | owner → orchestrate | Remove a lane from the registry. Pre-conditions: no active claims; orchestrate emits typed-failure if violated. |
| `UpdateLaneMetadataOrder` | `Mutate` | owner → orchestrate | Change a lane's `assistant-of` mapping or other metadata. Stable identifier unchanged. |
| `LaneRegistrySnapshotQuery` | `Match` | owner → orchestrate | Privileged full registry view. |
| `LaneRegistrySubscription` | `Subscribe` | owner / observer → orchestrate | Push subscription on registry changes (lane added / removed / updated). |

The ordinary `signal-persona-orchestrate` surface gets a paired
read-only family for components that need to enumerate the current
lane set without owner privileges:

| Family | Verb | Origin |
|---|---|---|
| `LaneRegistryObservation` | `Match` | any client → orchestrate |
| `LaneRegistrySubscription` | `Subscribe` | any client → orchestrate |

This is the same shape as the ordinary / OwnerSignal split for the
rest of orchestrate's vocabulary in DA/116 §8.

### §3.3 — For `persona-orchestrate` daemon

The daemon's sema-engine state grows a `LaneRegistry` table (per
`skills/component-triad.md` §"daemon's durable state is a sema-engine
database"). Startup reads `orchestrate/roles.nota` (or the interim
`roles.list`) into the registry; subsequent owner-Mutate operations
update it; subscribers observe changes.

The registry persists across daemon restarts. The config file is the
*seed*, not the source of truth at runtime — once the daemon is
running, the registry lives in its sema-engine database. If the
config changes between restarts, the daemon's startup reconciliation
discipline decides whether config overrides state, state overrides
config, or the divergence is surfaced for owner adjudication (§4 Q2).

### §3.4 — For `orchestrate-cli` (the shipped Rust port)

The current Rust port (`orchestrate-cli/src/registry.rs` per
`second-operator-assistant/1` §1) already reads `orchestrate/roles.list`
at runtime. The `Lane` enum at `src/lane.rs` is a closed 11-variant
type — the same enum-shape problem as `signal_persona_mind::RoleName`,
one layer down.

When persona-orchestrate is live, the routing changes per
`second-designer-assistant/1` (now superseded; the equivalent
forward-path content is in DA/115 + DA/116): the binary forwards to
orchestrate's ordinary socket instead of writing lock files directly.
At that point the `Lane` enum in orchestrate-cli can become a
newtype, mirroring the contract.

In the meantime, the shipped port's collapse-on-projection
(documented at `Lane::role_name`, exercised by
`second_assistant_lanes_collapse_onto_first_tier_role_name`) is the
right compromise — it preserves per-lane lock-file identity while the
contract still has the enum gap.

### §3.5 — For bead `primary-jboc`

The bead's three paths (operator's options) are superseded by
path 4 above. The bead should either:

- **Close as superseded.** The gap dissolves rather than resolving;
  the action item becomes "implement path 4" which lives in bead
  `primary-699g`'s contract design scope.
- **Stay open but reframed.** Designer evaluates path 4 against
  paths 1–3 from operator's report and makes the call. The bead
  description should add path 4 to the list.

Recommendation: keep `primary-jboc` open, reframed with path 4
added. Designer's evaluation is the right home for the choice. If
designer adopts path 4, the bead closes as "superseded by
`primary-699g`'s registry surface."

### §3.6 — For bead `primary-699g`

The bead's scope expands to include the registry surface:

- `owner-signal-persona-orchestrate` carries `LaneRegistry*` families
  per §3.2.
- `persona-orchestrate` daemon owns the `LaneRegistry` table in its
  sema-engine state per §3.3.
- `signal-persona-orchestrate` (ordinary surface) carries read-only
  `LaneRegistryObservation` + `LaneRegistrySubscription` per §3.2.

This is additive to the bead's existing scope (spawn / supervision /
scheduling / escalation). The same daemon, same contract repos —
just more families on each surface.

---

## §4 — Open questions

For designer pickup of `primary-699g` (and `primary-jboc` if it
stays open):

### Q1. What shape is `LaneIdentifier`?

Three options:

1. **`LaneIdentifier(String)`** — a newtype around a human-readable
   string (e.g. `"designer-assistant"`). Simplest; preserves the
   existing `roles.list` and `orchestrate/<lane>.lock` filenames as
   stable identifiers. Risk: stringly-typed identity (per
   `ESSENCE.md` §"Naming — full English words" and the diagnostic
   "stringly-typed dispatch").
2. **Hash-addressed identifier** — `LaneIdentifier(LaneHash)` where
   `LaneHash` is the content hash of the lane's typed record per
   `ESSENCE.md` §"Versioning on the eventual stack". Aligns with
   the eventual content-addressing direction but introduces a layer
   of indirection for human-facing tooling.
3. **Typed slot allocated by the registry** —
   `LaneIdentifier(Slot<LaneRecord>)` per `ESSENCE.md`
   §"Infrastructure mints identity". Most workspace-shaped; the
   registry mints the slot on registration, callers reference by
   slot. Requires the registry to be the authority for assigning
   ids (which it is — the registry IS the orchestrate component's
   state).

My weak recommendation: option 3 (typed slot). It matches the
workspace's "infrastructure mints identity" rule and the registry
is the natural minting authority. Human-facing tooling
(`tools/orchestrate`, the `orchestrate` CLI) renders slot ↔
human-readable-name in the projection layer.

### Q2. Startup reconciliation when config diverges from state

When `persona-orchestrate` starts and its sema-engine `LaneRegistry`
table already has state, what happens if `orchestrate/roles.nota`
(or `roles.list`) on disk lists a different set?

Options:

- **Config wins.** Daemon overwrites registry from config on each
  startup. Simple; loses runtime-added lanes if the config wasn't
  also updated.
- **State wins.** Daemon ignores config after first seed. Clean
  separation; config becomes seed-only with no ongoing role.
- **Owner adjudicates.** Daemon refuses to start if there's
  divergence, surfaces the diff, and waits for an owner-Mutate
  reconciliation order.
- **Append-only.** Config can only add; never remove. State carries
  removals. Surfaces only one kind of divergence (added in state,
  not in config) — likely meaningless once the registry is the
  source of truth.

This is the kind of question that benefits from being decided at
contract-design time, not paper'd over at runtime.

### Q3. Beads label and `assistant-of` resolution

Per `skills/role-lanes.md` and `orchestrate/AGENTS.md` §"Beads
belong to main roles, not assistants", a lane's `assistant-of`
field determines which beads label it works under
(`role:<main-role>`). With dynamic registration, two new questions:

- Can a lane register itself as a *main role* (no `assistant-of`)
  at runtime? If yes, that's a new beads label appearing — does
  the BEADS system handle dynamic labels gracefully? Does the
  pool concept (main role + its assistants) still hold?
- If a lane's `assistant-of` mapping changes via
  `UpdateLaneMetadataOrder`, what happens to already-claimed
  beads under the old mapping? Are they migrated? Left as
  historical artifacts? Adjudicated by the owner?

### Q4. Permission boundary between ordinary and owner surfaces

The ordinary `signal-persona-orchestrate` surface has read-only
`LaneRegistryObservation` / `LaneRegistrySubscription` per §3.2.
This is intentional — components need to enumerate the lane set
to know what's claimable.

But: if a malicious-or-confused ordinary caller can ENUMERATE the
lane set, can it submit `ScopeAcquisitionSubmission` for any of
those lanes? The current submission shape carries
`(lane, scope, reason)`. Should the submission be allowed only for
the caller's own lane (validated via peer credentials and the
registry's metadata on which lane belongs to which Unix
identity)?

This is the same shape as the OwnerSignal OS-enforcement question
(DA/116 §5), one layer up: per-component Unix identities establish
who can connect, but per-lane identity establishes who can submit
*as which lane*. The two concerns are orthogonal but compose.

### Q5. Migration path from current state

The shipped `orchestrate-cli` has a closed 11-variant `Lane` enum
and projects onto a closed 8-variant `RoleName`. Migrating to
path 4 means:

1. `signal-persona-mind` contract change:
   `RoleName` → `LaneIdentifier`. Every consumer recompiles.
2. `orchestrate-cli` change: replace the `Lane` enum with a
   `LaneRegistry` loaded from `roles.list` at startup. The
   collapse-on-projection logic becomes a registry lookup.
3. Once `persona-orchestrate` is live: orchestrate-cli's registry
   reading happens via the ordinary socket instead of by parsing
   `roles.list` directly. The config file retires.

Stage 1 can land independently of `persona-orchestrate` existing —
it's a contract change in `signal-persona-mind` plus a follow-up
in `orchestrate-cli`. Stage 2 follows. Stage 3 waits on
persona-orchestrate.

Question: do these stages get separate beads, or are they tracked
under `primary-699g`'s expanded scope?

---

## §5 — Bead updates this report implies

Two beads get refreshed (descriptions in BEADS):

- **`primary-jboc`** — reframe to include path 4 from §2 as a
  fourth resolution. Designer evaluates against paths 1–3 from
  operator's report and makes the call. May close as superseded
  by `primary-699g` if designer adopts path 4.
- **`primary-699g`** — extend description to include the
  `LaneRegistry*` family on `owner-signal-persona-orchestrate`,
  the read-only `LaneRegistryObservation` / `LaneRegistrySubscription`
  on the ordinary surface, the `LaneRegistry` table in
  orchestrate's sema-engine state, and the five §4 open questions.

---

## §6 — Context-maintenance note

Per `skills/context-maintenance.md` the lane was already swept clean
in the prior turn (report 5 deleted; arc moved to DA/115+116 +
operator/1 + designer/210). This report is the first new substance
in the lane since that sweep. The user's roles-as-config direction
is the load-bearing item; it lives here because:

- DA/115 + DA/116 are designer-assistant's lane (can't edit).
- Operator/1 is operator-assistant's lane (can't edit, and the
  finding is operator's; the *resolution direction* is design work).
- The new direction belongs in design discipline, and second-DA is
  the appropriate lane (this arc has been mine throughout).

The next maintenance trigger for this lane is either: (a) the
designer pickup of `primary-699g` lands a definitive
persona-orchestrate design report that absorbs this report's §3/§4
substance — at which point this report retires; or (b) the user
shifts direction and the substance here needs revision.

---

## See also

- `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md`
  — the canonical orchestrate integration design; §4 verb-mapping
  table this report's §3.2 extends.
- `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md`
  — the canonical OwnerSignal report; §8.2 owner-contract families
  this report's §3.2 extends; §13 the five settled answers this
  report sits on top of.
- `reports/second-operator-assistant/1-rust-port-of-tools-orchestrate-2026-05-17.md`
  §3 — the three resolution paths this report adds path 4 to.
- `reports/designer/210-component-triad-decisions-and-mutate-authority-2026-05-17.md`
  — Mutate authority semantics; the `LaneRegistry*` Mutate family
  obeys the obey-then-confirm discipline named there.
- `skills/component-triad.md` — the four invariants the
  persona-orchestrate design respects; the sema-engine state
  requirement this report relies on for the `LaneRegistry` table.
- `skills/role-lanes.md` — the lane meta-pattern; under path 4 the
  "registering a new lane" steps simplify to a single owner-Mutate.
- `skills/context-maintenance.md` — the discipline this report
  honors (small substance, right home).
- `orchestrate/AGENTS.md` — the protocol; the lane registry is
  currently `orchestrate/roles.list`.
- `ESSENCE.md` §"Naming — full English words", §"Infrastructure
  mints identity", §"Versioning on the eventual stack" — the
  rules `LaneIdentifier`'s shape (§4 Q1) needs to respect.
- BEADS `primary-699g` — designer pickup for the
  persona-orchestrate component + signal/OwnerSignal chain.
- BEADS `primary-jboc` — RoleName contract gap; reframed by this
  report's path 4.
- BEADS `primary-68cb` — closed via commit `1730087a`; the shipped
  `orchestrate-cli` Rust port.

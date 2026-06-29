# Intent Maintenance — Replaceable Design Directive

## Task and scope

Record one durable design-philosophy directive the psyche stated, through Spirit,
without duplicating existing records and without capturing private substance.
Assess and report the manifestation gap.

Psyche verbatim (context):
> "...it looks to me like an agent that's proposing something in order to try to
> keep an older part of the system working. And I don't want that because then it
> creates all of this legacy system. And if the current system is not designed to
> do things the way we want, then it has to go. I don't design additively, I
> design replaceably."

## Classification (confirmed)

Directive + durable + universal + public (no private/personal substance). It is a
`Principle` (a durable design value), not matter. Spirit-capture candidate
confirmed.

## Duplicate / neighborhood check (done FIRST)

Spirit text searches run: `replaceably`, `replaceable`, `additive`, `legacy`,
`backward`, `compatibility`, `parallel`, `rewrite`, `consumers`, `superseded`.
Domain neighborhood: `Technology(Software(Engineering Design))`.

Closest existing records, and why none is an equivalent:

- `jys2` (Principle, Engineering Design / AgentSystems): "Design at the post-agent
  capability frontier... target the best end-shape rather than a
  historically-practical compromise." This is the *rationale that rewrites are now
  cheap*, not the replaceable-vs-additive design stance. Not a duplicate.
- `ng1x` (Decision, Engineering DevelopmentProcess/Architecture): "Migration
  completes only when the superseded implementation, dependency, and execution path
  are removed (wrapping an old path is not migration). Drop compatibility surfaces
  ... once superseded." This embeds the kernel but is a task-bound workspace-forward
  migration Decision (Asschema, new-Spirit, orchestrate), not the standalone
  universal value. Not a duplicate.
- `gjr1` ("additive" hit): about categorical KIND vs additive CAPABILITY vector
  modeling. Unrelated.

Conclusion: genuine NEW Principle. It elevates the kernel currently embedded only
in a task-bound Decision (ng1x) to a standalone universal design value. No
supersession performed: ng1x and jys2 retain their own valid scope.

## Recorded (NEW)

- Spirit handle/id: **`10pz`** — reply `(RecordAccepted 10pz)`
- Operation: `Record` via deployed `spirit` CLI (file-arg NOTA), wire shape read
  from `signal-spirit/src/schema/signal.rs` (`RecordRequest` = `Entry` +
  `Justification`).
- Domains: `Technology(Software(Engineering Design))`,
  `Technology(Software(Engineering Architecture))`
- Kind: `Principle`
- Certainty: `High`  Importance: `Medium`  Privacy: `Zero` (public)
- Referents: `design architecture migration versioning`
- Description (exact recorded prose):
  > Design replaceably, not additively: do not preserve an older shape for
  > backward-compatibility's sake when it manufactures legacy. If the current
  > system is not designed to do what we want, it is replaced — every consumer
  > updated — rather than extended with a parallel compatibility path.
- Testimony: full psyche verbatim utterance above, antecedent `None`.

### Guardian iterations (evidence)

1. `ReferentGuardianRejected` — initial abstract referents
   (`replaceable-design`, `additive-design`, ...) rejected: "a design principle is
   not a nameable particular." Switched to registered topic referents
   (`design architecture migration versioning`), matching neighbor records (jys2
   uses `design`, ng1x uses `migration`).
2. `GuardianRejected(ImportanceUnsupported)` at `High` importance — "no direct
   psyche declaration or recurrence/blast-radius/centrality evidence supports the
   claimed High importance; lower to Medium." Lowered importance to `Medium`.
   Certainty `High` was accepted.
3. Accepted: `(RecordAccepted 10pz)`.

## Manifestation decision: RECOMMENDED (not done)

The directive is partially manifested already and its cleanest home is a generated
skill surface that must be edited through the skill-editor source flow, not
hand-edited. Existing partial coverage:

- `beauty` skill — audit-lens section already says: "When the shape is wrong, the
  recommendation is the structural fix, not a patch that preserves the ugly
  surface," and lists the ugliness signal: "Dead code retained 'for safety' or
  'backward compatibility.' Delete it." These are the *downstream* behaviors of the
  directive but do not state the upstream design stance.
- `architecture-editor` skill — "Retire legacy paths ... remove architecture that
  teaches the old path" (docs-surface retirement, downstream).

Recommended target (for the skill-editor flow):
- Source: `/git/github.com/LiGoldragon/skills/modules/beauty` (generates the runtime
  `.claude/skills/beauty/SKILL.md`).
- Edit: in the "Beauty as primary audit lens" section, add the upstream stance —
  design replaceably, not additively: when the current system is not designed to do
  what we want, replace it and update every consumer, rather than add a parallel
  compatibility path that manufactures legacy. Cite record `10pz`.
- Why recommend, not do: the runtime SKILL.md is a generated surface reconciled
  from `modules/beauty`; editing it directly is the wrong surface and would be
  reconciled away. Importance landed at Medium and the downstream behaviors are
  already covered, so this is a sharpening, best made deliberately through the
  skill-editor discipline.

I did NOT touch AGENTS.md (boot contract, kept minimal; this is design philosophy,
not an operational boot rule) and did NOT hand-edit any generated skill surface.

## Checks run

- Spirit wire shape verified against `signal-spirit/src/schema/signal.rs`
  (`Entry`/`Justification`/`Kind`/`Magnitude`, Domain nesting from
  `domain.rs::EngineeringLeaf`).
- Duplicate sweep across 10 keyword searches + Engineering Design domain neighbors.
- Record accepted by both Referent and Importance guardians after corrections.
- Temp record file `/tmp/spirit-record-replaceable.nota` removed after acceptance.

## For the psyche to confirm

- Importance was set to `Medium` (guardian-required; no explicit blast-radius
  language in the statement). If you intend this as a top-priority, broadly-binding
  design law, say so and it can be raised via `BumpImportance` with that warrant.
- Manifestation into the `beauty` skill is recommended but not performed; confirm
  whether to dispatch the skill-editor to add the upstream replaceable-vs-additive
  stance (citing `10pz`), or leave the downstream coverage as-is.

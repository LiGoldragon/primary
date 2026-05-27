# Skill manifestation targets — schema runtime actor upgrade vision

Kind: Skill manifestation audit
Topics: schema runtime actor upgrade actor SEMA executor

## Summary

The six reviewed skills already carry the core noun rule: authored
schema objects become emitted Rust types, and behavior belongs as
methods or trait impls on those emitted nouns. The missing
manifestation is not the generic method rule; it is the runtime
application of that rule.

The current rule agents need to see is:

- Schema-authored objects become generated Rust nouns.
- Behavior is hand-written as methods or trait impls on those
  generated nouns, or on data-bearing runtime nouns that own real
  state.
- Actor input and output are schema-defined enum/reaction trees, not
  ad hoc mailbox payloads.
- Executor logic is the contact point between typed enum/tree inputs,
  state, actions, and replies.
- SEMA/database commands are also schema-defined messages, not
  daemon-local hand-written command enums.
- Upgrade traits are required when, and only when, schema diff says a
  type changed.

## Cross-skill edit targets

### `skills/rust/methods.md`

Current state: strong. It already has "Schema-generated objects are
the method surface" and says signal `Input`, `Output`, operation
payloads, route/header types, codecs, and store records are nouns.

Needed edits:

- Extend that section from signal/store nouns to runtime nouns:
  generated actor `Input`, actor `Output` / reaction trees, executor
  `Action` / `Response`, and SEMA command/archive records are all
  method surfaces.
- Add a sentence that generated nouns can receive either inherent
  methods or trait impls, and that trait impls are the preferred
  shape when the behavior names a cross-layer relation
  (`Execute`, `Apply`, `Archive`, `UpgradeFrom`, etc.).
- Add upgrade discipline: do not write upgrade/conversion traits for
  unchanged schema types. If schema diff says the type is identical,
  it is carried through by stable encoding or direct reuse; if diff
  says the type changed, the changed generated noun gets the upgrade
  method or trait impl.

Stale/missing guidance:

- The section still reads mostly like "schema-emitted signal
  surfaces." It needs to name actor and SEMA surfaces explicitly so
  agents do not treat them as hand-written Rust infrastructure.

### `skills/rust-discipline.md`

Current state: partly stale for actor schema work. The Kameo section
says "one `impl Message<Verb> for Actor` per verb; no monolithic
`Msg` enum." That remains correct for Kameo framework boilerplate, but
it can be misread against the new schema-authored actor IO rule.

Needed edits:

- Clarify that "no monolithic `Msg` enum" forbids hand-written
  catch-all mailbox enums, not schema-authored actor `Input` enum
  trees.
- Add that actor handlers should receive schema-generated input nouns
  and return schema-generated output/reaction nouns where the actor is
  part of the schema runtime.
- Point the actor section at `enum-contact-points.md` for executor and
  reaction-tree matching.
- Add a short upgrade pointer: read the schema diff before adding
  migration traits; unchanged types do not earn upgrade code.

Stale/missing guidance:

- The Rust index currently names actors as "one verb per Kameo
  message" but does not say where schema-generated actor input/output
  trees fit into that shape.

### `skills/abstractions.md`

Current state: strong. Its "Schema-emitted nouns" section already
states the labor split and says signal, executor, and SEMA types are
emitted.

Needed edits:

- Replace the loose phrase "traits implied by signal/executor/SEMA
  interaction" with explicit guidance: traits belong at named contact
  points between generated trees, not as generic helper namespaces.
- Add actor input/output to the runtime triad examples.
- Add a one-paragraph upgrade corollary: the noun only receives an
  upgrade trait when the schema diff creates a historical/current
  relationship for that noun.

Stale/missing guidance:

- The existing section covers the concept, but it does not yet name
  actor reaction trees or diff-gated upgrade traits, which are the two
  places agents are likely to invent infrastructure by hand.

### `skills/enum-contact-points.md`

Current state: strong but old-example-heavy. It already teaches
engine logic as enum/tree contact and has upgrade `From<historical::T>
for current::T` examples.

Needed edits:

- Add a current schema-runtime example shape: executor matches
  `(Input, RuntimeState)` into `(Action, Reply)` or a generated
  reaction tree; SEMA matches generated `Command` against stored
  archive/index state into generated `Response`.
- State that generated schema trees are the preferred axes of the
  contact point. If the code introduces a parallel hand-written enum
  solely for matching, that is likely a stale mirror of the schema.
- Tighten the upgrade example: use `From` / `TryFrom` / named upgrade
  traits only for historical/current pairs reported by schema diff.
  No blanket migration trait for every generated type.

Stale/missing guidance:

- The skill currently treats upgrade conversion as a general example
  of enum contact. It should say the contact is diff-discovered, not a
  boilerplate layer applied to every type.

### `skills/component-triad.md`

Current state: the most important edit target. The runtime triad
section names signal / executor / SEMA correctly, but the earlier
"Verbs come in three layers" section says "The daemon owns its Layer-2
commands." That can be read as permission to hand-write daemon-local
command enums.

Needed edits:

- Revise Layer 2 wording: component commands are daemon-internal, but
  their shape is schema-defined and emitted as Rust nouns. "Daemon
  owns" means the daemon owns execution and state authority, not that
  agents hand-write a private command vocabulary outside schema.
- In "Runtime triad," explicitly say actor mailboxes, executor
  actions/responses, and SEMA commands/responses are schema-authored
  message trees.
- Add that SEMA/database command records are part of the same schema
  as archive records and indices. The database does not get a hidden
  Rust-only command protocol.
- Add the upgrade rule under SEMA: on database load, schema diff
  determines which historical/current generated nouns require upgrade
  traits; unchanged nouns do not get synthetic migrations.
- Add witness-test language for "schema command coverage": every
  generated executor/SEMA command variant is handled at exactly one
  named contact point.

Stale/missing guidance:

- "The daemon owns its Layer-2 commands" is stale unless qualified by
  "through its schema." It currently leaves room for daemon-local
  command enums, which conflicts with the new rule.

### `skills/language-design.md`

Current state: generally aligned. "Domains come from data" and
"Defined inputs and outputs" already support the schema-authored
runtime direction.

Needed edits:

- Add actor input/output and reaction trees to "Defined inputs and
  outputs": actor boundaries are pipeline boundaries, so both sides
  are named and typed in schema.
- Add SEMA command records to "Domains come from data": command
  vocabularies are domain lists and therefore generated from schema,
  not maintained as Rust tables.
- Add upgrade-diff wording near "Domains come from data": the diff is
  data too; migration obligations come from the declared schema
  historical/current relationship, not from an agent's habit of adding
  conversion code everywhere.

Stale/missing guidance:

- The language-design instinct is correct but too generic for this
  moment. Agents need a direct bridge from "defined inputs and outputs"
  to actor IO and SEMA command trees.

## Missing guidance surface

The reviewed skills do not currently provide a compact upgrade
discipline. The rule can be added to the skills above, but it may also
need a focused future skill if migration work keeps recurring:

- Schema diff is the authority for upgrade obligations.
- Changed type gets a historical/current contact point.
- Unchanged type is reused or carried through without upgrade trait
  ceremony.
- Removed/renamed fields and variants become explicit rejection,
  defaulting, or projection rules at the changed noun.
- The migration spine is generated from diff data; hand-written code
  fills only the semantic cells the diff cannot infer.

The closest existing homes are `skills/enum-contact-points.md` for the
contact-matrix rule and `skills/component-triad.md` for database-load
upgrade flow. A new skill is only warranted if those sections become
too large.

## Priority order

1. Edit `skills/component-triad.md` first. It carries the stale command
   ownership wording and the runtime triad section agents will consult
   when building daemons.
2. Edit `skills/rust-discipline.md` next to reconcile Kameo
   per-message guidance with schema-authored actor input/output trees.
3. Edit `skills/enum-contact-points.md` to make executor and SEMA
   command handling the live examples.
4. Patch `skills/rust/methods.md` and `skills/abstractions.md` with
   the actor/SEMA/upgrade corollaries.
5. Patch `skills/language-design.md` last; it needs only a brief
   bridge from general language instincts to runtime schema surfaces.

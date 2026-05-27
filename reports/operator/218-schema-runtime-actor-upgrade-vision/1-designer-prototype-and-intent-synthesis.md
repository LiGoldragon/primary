# Designer prototype and intent synthesis

Kind: Synthesis
Topics: schema runtime actor upgrade spirit nota

## Sources read

- `reports/designer/387-nota-schema-design-representation-2026-05-27.md`
- `reports/designer/388-macro-system-exploration-and-brace-enum-sugar-2026-05-27.md`
- `reports/designer/389-schema-macros-canonical-direction.md`
- `reports/designer/390-wire-runtime-canonical-direction.md`
- `reports/designer/391-emission-discipline-direction.md`
- `reports/operator/215-nota-schema-nix-test-representation-2026-05-27.md`
- `reports/operator/217-nota-schema-spirit-design-improvement-research/1-design-improvement-research.md`
- Spirit records observed through `spirit "(Observe (Records (None None DescriptionOnly)))"`, especially records 925-959.

## Core synthesis

The current schema/runtime direction is strongest when it treats the
schema as the source of Rust nouns, not as documentation or a helper
format. A schema file lowers through NOTA structural objects, macro
expansion, and Asschema into visible Rust under `src/schema/`; actor
runtime code then implements methods and traits on those emitted
objects. This preserves the workspace's method discipline and keeps
behavior attached to the data types that carry the signal.

That pattern should survive every next slice:

- NOTA remains the structural floor: ordered root blocks, delimiter
  shape, spans, pipe-text opacity, object counts, and
  `qualifies_as_*` candidate predicates. It does not learn schema
  semantics.
- Schema remains one recursive root struct: imports, input, output,
  namespace. Position supplies field meaning; macros expand inner
  objects until the recursion reaches scalar leaves.
- Macros remain structural sugar, selected by position, delimiter,
  internal shape, object count, symbol qualification, and combinations.
  New schema syntax should land as macros, not as scattered engine
  branches.
- Asschema is the assembled macro-free middle form. Emitters consume
  Asschema; they do not re-interpret schema text.
- Generated Rust lands under `src/schema/`, where agents can grep it,
  review it, and attach implementations to the generated nouns.

## Actor runtime pattern to preserve

The actor-facing schema output should be enum roots plus payload nouns.
Input and output are authored separately at the schema layer, but the
runtime treats them as reaction/action variants over one signal space.
An actor receives a schema-created input enum variant, matches that
variant, consults state and authority, then emits a schema-created
output enum variant or routes a schema-created command to SEMA.

The useful split is:

- `Input` / reaction enum: what an actor can receive.
- `Output` / action enum: what the actor can emit back or onward.
- Payload structs/newtypes: domain nouns carrying the data.
- `SemaCommand` / `SemaResponse`: storage-facing messages, also
  schema-defined.
- State and permission/owner messages: authority nouns that gate
  mutation under the single-owner discipline.

This is better than a hand-written dispatcher because it makes the
cross-product explicit: the actor match is over schema variants, and
every handler's data type is visible in generated Rust. The runtime
code should grow as trait impls or methods on these schema objects,
not as free helpers around them.

## Runtime triad pattern

The signal-executor-sema shape is the runtime counterpart of the
component triad:

- Signal receives and emits schema-defined input/output frames.
- Executor owns actor reaction logic: variant match, permission
  check, routing, and reply construction.
- SEMA owns durable mutation through schema-defined commands and
  responses.

Spirit-next already hints at this with generated signal types,
`SemaCommand`, `SemaResponse`, and a store path. The next durable
version should make the triad explicit enough that a future database
component can split out without changing the message language. Internal
database work should use the same schema language as external signals.

## Macro and schema implementation boundaries

The designer prototype work makes one boundary especially important:
new schema convenience forms are macro work, not legacy macro reuse and
not ad hoc Rust lowering. Brace enum bodies are the model: the authored
brace form is sugar, it expands to the canonical paren enum shape, and
the resulting Asschema is identical.

The runtime pass should preserve these constraints:

- No fallback to old `signal_channel!`-style infrastructure for the new
  schema-derived stack.
- No Rust-only shortcut that bypasses macro expansion and Asschema.
- No local frame primitive duplication once `signal-frame` has its own
  schema-derived types.
- No generated free-function helper surfaces; generated helper behavior
  belongs on emitted data-bearing types or traits.

The pending macro-specificity gap matters for runtime safety. The
current first-match registry is enough for today's branch, but the
canonical direction is most-specific match with ambiguity errors. A
runtime actor system built on schema variants should not depend on
registration order for structural routing.

## Upgrade and accept observability

The upgrade vision is now clear enough to preserve as a design
constraint: schema diffs drive upgrade obligations. Unchanged emitted
types need no upgrade code. Changed emitted types require explicit
hand-written upgrade and accept behavior on the schema object, typically
as generated trait requirements that fail to compile until implemented.

Two ingress paths need the same discipline:

- Database load: old stored records carry schema-version identity and
  upgrade into the current schema form before use, optionally rewriting
  upgraded storage.
- Runtime message ingress: old-version incoming messages can be
  upgraded, accepted, routed, and logged.

The observable event is load-bearing. When an old-version message is
upgraded and accepted, the runtime should emit an event that names the
source schema version, target schema version, message type, acceptance
decision, and resulting route or storage marker. That event gives
routers and agents the signal to notify a client that its schema is old,
and it gives operators an introspection trail for live compatibility.

## Highest-value implementation witnesses

The next tests should keep the style of operator report 215: short
design examples backed by Nix checks. The most valuable witnesses are:

- A schema-created actor input enum compiles, receives a variant, and
  invokes a trait impl on the generated payload noun.
- Input and output emission share one tag-space partition rather than
  independent route spaces.
- `signal-frame` types are imported from a schema-derived frame package,
  and local duplicate frame primitives are rejected.
- `SemaCommand` and `SemaResponse` move through the same schema-defined
  language as external signal messages.
- A previous-version stored record upgrades on read and leaves an
  observable upgrade event.
- A previous-version incoming message upgrades, is accepted, routes to
  the current actor handler, and emits an observable accept event.

## Concise recommendation

Implement the next runtime slice by making schema-emitted objects the
only nouns the actor runtime sees. Start with a small actor reaction
witness: schema emits `Input`, `Output`, payload types, `SemaCommand`,
and `SemaResponse`; handwritten Rust implements traits on those emitted
types; the test proves signal ingress, executor reaction, SEMA command,
reply construction, and upgrade/accept observability without touching
legacy macro paths.

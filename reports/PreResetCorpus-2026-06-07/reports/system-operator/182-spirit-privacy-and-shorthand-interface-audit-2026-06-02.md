# Spirit Privacy and Shorthand Interface Audit — 2026-06-02

## Trigger

The psyche asked whether Spirit privacy settings are implemented, whether
there are commands such as "private record" that lower to a normal record with
privacy set, and how to design simpler-to-more-complex command variants so
agents do not have to compose complex NOTA for routine intent work.

Durable intent captured first:

- Spirit record 1476 — Spirit should provide shorthand interfaces for common
  record operations so agents can submit simple intent records without
  composing the full advanced NOTA query or record shape each time.
- Spirit record 1477 — A private-record shorthand should lower to a normal
  Spirit record with elevated privacy, while ordinary simple record
  shorthands default to open public privacy.
- Spirit record 1478 — Spirit topics should be broad reusable topic words;
  split real concepts into separate topics instead of inventing narrow
  compound topics when the concepts can stand alone.

## Current Status

Privacy is implemented in repository source, but not live in the installed
production wrapper I tested.

Source-side evidence:

- `signal-persona-spirit/src/lib.rs` has `Privacy = Magnitude`,
  `PrivacySelection`, `Entry.privacy`, and `RecordQuery.privacy_selection`.
- `persona-spirit/src/store.rs` imports `PrivacySelection`, filters records by
  privacy, and defaults normal observation to exact `Zero`.
- `persona-spirit/tests/boundary.rs` includes
  `persona_spirit_client_filters_record_observation_by_privacy`.
- `spirit-next/schema/lib.schema` has `Privacy Magnitude`,
  `PrivacySelection`, and `Entry { ... Privacy * }`.

Live production evidence:

- `readlink -f $(command -v spirit)` resolves to
  `/nix/store/...-spirit-v0.3.0/bin/spirit-v0.3.0`.
- `spirit "(Observe (RecordIdentifiers ((Range (1476 1478)) WithProvenance)))"`
  returns provenance entries without privacy in the output tuple.
- `spirit "(Observe (Records ((Any []) None Any Any (Exact Zero) SummaryOnly)))"`
  fails with `invalid request text: expected PascalCase identifier, got LParen`.
  That is the explicit privacy-selector query shape, so the live wrapper is
  not on the privacy-aware contract yet.

Conclusion: privacy is source-implemented and tested, but not deployed/cut
over as the active `spirit` profile surface.

## Shorthand Commands Status

No shorthand operations are implemented today.

Production ordinary operations remain the full contract verbs:

- `State`
- `Record`
- `Observe`
- `Watch`
- `Unwatch`
- `Remove`
- `ChangeCertainty`
- `Tap`
- `Untap`

`spirit-next` currently has its own schema-derived pilot roots:

- `Record`
- `Observe`
- `Lookup`
- `Count`
- `Remove`
- and, in the current operator-locked worktree, `LookupStash`.

None of these are a "private record" or "simple record" shorthand. Agents still
compose the full `Record` operation, and for richer queries they compose the
full `Observe (Records (...))` shape.

## Interface Principle

The shorthand surface should not be shell flags or argv subcommands. The
workspace hard rule remains: the `spirit` binary takes exactly one NOTA
argument. Therefore "subcommand" here should mean one of two safe shapes:

1. A typed ordinary signal operation variant written in NOTA.
2. A convenience wrapper that constructs exactly one typed NOTA operation and
   passes it to the existing `spirit` CLI.

The first is the durable interface. The second is just ergonomic sugar.

## Simple-to-Complex Surface Proposal

### Tier 1 — Simple Record Shorthands

Purpose: routine intent capture in public development work.

Candidate shapes:

```nota
(RecordSimple ([spirit interface] Principle [description]))
(RecordPrivate ([spirit privacy] Decision [description]))
(RecordWeak ([topic] Clarification [description]))
```

Lowering:

- `RecordSimple` -> `Record` with `certainty = High`, `privacy = Zero`.
- `RecordPrivate` -> `Record` with `certainty = High`, `privacy = High`.
- `RecordWeak` -> `Record` with `certainty = Minimum`, `privacy = Zero`.

The important point is that the daemon receives or derives the full typed
entry. The shorthand is not a parallel storage shape.

### Tier 2 — Kind-Specific Shorthands

Purpose: remove one more field when the operation name already expresses the
kind.

Candidate shapes:

```nota
(Decide ([topic] [description]))
(Clarify ([topic] [description]))
(Correct ([topic] [description]))
(Constrain ([topic] [description]))
(Principle ([topic] [description]))
```

Lowering:

- `Decide` -> `RecordSimple(... Decision ...)`.
- `Clarify` -> `RecordSimple(... Clarification ...)`.
- `Correct` -> `RecordSimple(... Correction ...)`.
- `Constrain` -> `RecordSimple(... Constraint ...)`.
- `Principle` -> `RecordSimple(... Principle ...)`.

This tier is pleasant but slightly riskier: `Principle` is already a `Kind`
variant, so using it as an operation variant may be too visually close to the
payload vocabulary. If this lands, it should be tested for cold-read clarity.

### Tier 3 — Normal Full Record

Purpose: explicit control without full metadata ceremony.

Shape after privacy is live:

```nota
(Record ([topic ...] Kind [description] Certainty Privacy))
```

This is the canonical storage assertion. Shorthands lower to this.

### Tier 4 — Advanced Query/Metadata Operations

Purpose: maintenance, audits, private/elevated access, provenance, exact time
windows, certainty review, removal candidates, and future topic-discovery
queries.

Examples:

```nota
(Observe (Records ((Partial [spirit privacy]) None Any Recent (Exact Zero) SummaryOnly)))
(Observe (Records ((Any []) None (Exact Zero) Any Any WithProvenance)))
(Observe (RecordIdentifiers ((Range (1470 1480)) WithProvenance)))
```

The exact field order should follow the contract source when privacy is
actually deployed; the example above is conceptual, not the current live
v0.3.0 invocation.

## Topic Guidance

The topic vector is already the shorthand mechanism for "this is about several
things." Agents should not hide separate concepts in one compound topic.

Good:

```nota
[intent logging]
[spirit privacy]
[spirit interface]
```

Use a compound only when it names one established thing:

```nota
[signal-frame]
[persona-spirit]
```

This avoids vocabulary fragmentation and makes `Partial` and `Full` queries
more useful. A query for `[intent]` can find records about intent logging,
intent maintenance, intent privacy, and intent capture; a query for
`[intent-log]` only finds records where an agent guessed that exact compound.

## Skill Edits Made

Edited `skills/intent-log.md`:

- Added the rule that compounds should split into the topic vector when the
  concepts stand alone.
- Added examples: `[intent logging]` over `[intent-log]`,
  `[spirit privacy]` over `[spirit-privacy]`.

Edited `skills/spirit-cli.md`:

- Corrected the live v0.3.0 record description: deployed `Record` has no
  privacy field yet.
- Added the simple-capture convention: normal public work uses the simple
  record shape with broad topics, kind, description, certainty.
- Added the shorthand design rule: future shorthand remains typed NOTA lowering
  to full records, not shell flags or a second CLI syntax.
- Added the live-version warning: privacy-aware source may have a sixth
  `RecordQuery` field, but agents must not emit that against deployed
  `spirit-v0.3.0`.

## Recommended Next Work

1. Deploy the privacy-aware production Spirit build or deliberately keep it
   staged and update the skills again to say the source is ahead of live.
2. Add ordinary signal shorthand operations in `signal-persona-spirit`, with
   daemon lowering tests in `persona-spirit`.
3. Add a `private record` witness: shorthand input creates a stored record
   whose summary/provenance is hidden by default privacy selection and visible
   only under an explicit elevated privacy query.
4. Mirror the concept into `spirit-next` as schema-derived operation variants
   or Nexus lowering rules, because this is exactly the kind of interface
   ergonomics the next-generation schema should prove.
5. Keep the topic guidance in skills now; it does not need to wait for code.

## Best Question

What should the default certainty be for `RecordSimple`?

My lean is `High`: a simple record is still an agent-mined durable intent
capture. `Minimum` should be explicit through `RecordWeak` or the full record,
because weak intent is semantically different from normal capture.

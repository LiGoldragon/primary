# Spirit Documentation Audit — Production Query Shape

## Trigger

The psyche reported agents trying malformed production Spirit calls:

```sh
spirit "(Observe ((Any [schema asschema nota structural-macro]) None Any Recent SummaryOnly))"
spirit "(Search ([schema asschema nota] 20))"
```

Both fail on the live production daemon. The first fails because `Observe`
expects an `Observation` enum variant such as `Records`; the second fails
because `Search` is not a production request head.

## Live Production Shape

Production Spirit v0.5.2 accepts record queries through:

```sh
spirit "(Observe (Records ((Any []) None Any Recent SummaryOnly)))"
spirit "(Observe (Records ((Partial [schema asschema nota structural-macro]) None Any Recent SummaryOnly)))"
spirit "(Observe (Records ((Full [schema nota]) None Any Recent SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Exact [cub9]) SummaryOnly)))"
```

`Observe` wraps the observation target. For record search, the target is
`Records`, and the record query payload is the untagged positional record
inside it:

```text
(Observe (Records ((<TopicSelection>) <Kind?> <CertaintySelection> <RecordedTimeSelection> <ObservationMode>)))
```

There is no live `Search` root. Identifier `Range` is also stale: random
identifiers are not ordinal, and the live `RecordIdentifierSelection` enum has
only `Exact`.

## Documentation Problems Found

`skills/spirit-cli.md` had correct examples, but they were too far down the
page. The first screen did not tell agents the core wrapper rule, so agents
invented `(Observe (<query>))` and `Search`.

`skills/context-maintenance.md` still taught an identifier `Range` query for
Spirit capture sweeps. That was valid in the old ordinal-id era but is wrong
after the random short-id migration.

`skills/intent-log.md` and `skills/privacy.md` had v0.4-era wording. It was not
the direct cause of the malformed `Observe` commands, but it increased drift:
agents saw old deployed-version language while the live system is v0.5.2.

Historical reports still contain prototype or spirit-next forms like
`(Observe ((Full [[smoke-test]]) ...))`. Those reports should remain historical
unless superseded by a report sweep; they are not production CLI guidance.

Schema files contain declarations such as `Observe ((Observation))`. That is a
schema declaration, not an invocation example. The production CLI examples must
stay in `skills/spirit-cli.md`.

## Changes Made

`skills/spirit-cli.md` now opens with a copy-first query section and explicitly
names the two recurring wrong shapes:

- `Search` is not a production request head.
- `(Observe ((Any [...]) ...))` is missing the `Records` observation variant.

The same skill no longer documents identifier `Range` as live. It tells agents
to use `Records` with `Recent`, `Shallow`, `Deep`, `VeryDeep`, `Since`, `Until`,
or `Between` for history and recency windows.

`skills/context-maintenance.md` now uses a `Records` query for recent Spirit
capture sweeps instead of a stale identifier range.

`skills/intent-log.md` and `skills/privacy.md` now name production Spirit
v0.5.2 where they discuss the current record/privacy surface.

## Verification

The corrected examples were run against the live daemon and succeeded:

```sh
spirit "(Observe (Records ((Any []) None Any Recent SummaryOnly)))"
spirit "(Observe (Records ((Partial [schema asschema nota structural-macro]) None Any Recent SummaryOnly)))"
spirit "(Observe (Records ((Full [schema nota]) None Any Recent SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Exact [cub9]) SummaryOnly)))"
```

The two reported malformed examples were re-run and still fail with the same
errors, confirming the bug is documentation/ergonomics rather than daemon
regression.

## Remaining Risk

The production surface is still too verbose for ordinary intent lookup. The
designer reports proposing shorthand roots such as `Recent`, `Lookup`, or
variant-ladder query forms are directionally useful, but those roots are not
production. Until they land in the signal contract and deployed daemon, agents
must copy from `skills/spirit-cli.md`, not from prototype reports.

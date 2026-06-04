# Spirit privacy setting test — 2026-06-04

## Scope

Test the deployed Spirit privacy behavior without exposing real private personal substance. The test used a synthetic record whose description explicitly says it contains no private personal content.

## Deployed version

`spirit` resolves to `spirit-v0.4.1`.

The deployed `signal-persona-spirit` contract at rev `1515cabc1806ac0873525e6692c38b720988ce85` shows:

- `Entry` now has five fields: topics, kind, description, certainty, privacy.
- `Privacy` is an alias for `Magnitude`.
- Old four-field `Record` input still decodes and defaults privacy to `Zero`.
- Public record observations default to `Exact(Zero)` privacy.
- Explicit private observations use `PrivateRecords` or `PrivateRecordIdentifiers` with a `PrivacySelection` such as `AtMost Low`.

## Commands tested

A public/meta record created with the old four-field shape now observes as `High Zero`, where the final `Zero` is privacy.

A synthetic low-privacy test record was created with five fields:

```sh
spirit "(Record ([privacy-test spirit] Clarification [Synthetic privacy test record with no private personal content; safe to remove after verifying private query behavior.] Low Low))"
```

It was accepted as record `2572`.

Public query hid it:

```sh
spirit "(Observe (Records ((Partial [privacy-test]) None Any Any SummaryOnly)))"
# => (RecordsObserved [])
```

Explicit private query found it:

```sh
spirit "(Observe (PrivateRecords ((AtMost Low) ((Partial [privacy-test]) None Any Any SummaryOnly))))"
# => record 2572, with final privacy field Low
```

Public identifier query also hid it:

```sh
spirit "(Observe (RecordIdentifiers ((Exact 2572) SummaryOnly)))"
# => (RecordsObserved [])
```

Explicit private identifier query found it:

```sh
spirit "(Observe (PrivateRecordIdentifiers ((AtMost Low) ((Exact 2572) SummaryOnly))))"
# => record 2572
```

Trying to smuggle a privacy selector into the public query shape is rejected:

```sh
spirit "(Observe (Records ((Partial [privacy-test]) None Any Any (AtMost Low) SummaryOnly)))"
# => validation rejected PublicRecordQuery: public record queries cannot carry elevated privacy
```

The synthetic record was removed after the test:

```sh
spirit "(Remove 2572)"
```

A follow-up explicit private identifier query returned empty, confirming removal.

## What this means operationally

The privacy setting is real and type-enforced at the query layer:

- Public/default observations only return privacy `Zero`.
- Privacy-bearing records require an explicit `PrivateRecords` or `PrivateRecordIdentifiers` query.
- Four-field records remain public by default because they decode with privacy `Zero`.
- The privacy value is a `Magnitude`; `Low` works as the low privacy filter the psyche described.

The setting is not the same as a separate private database or encryption boundary. It prevents accidental default-query leakage and forces explicit private reads, but private records still live in the same Spirit storage plane.

## Migration judgment

I did not migrate real private entries in this pass. The recent assistant captures from this turn are infrastructure guidance and were left public. The counselor report already names older pre-rule records that may contain personal substance; migrating those should be done as a deliberate private-maintenance pass that avoids quoting their contents into public reports.

## Recommended assistant default

Use public `Zero` privacy for infrastructure, agent training, component design, and rules meant to help all agents. Use `Low` privacy for anything even mildly personal or specific to the psyche's private logistics, business, family, friends, finances, health, location, or plans. Use higher privacy magnitudes when the psyche frames the content as sensitive.

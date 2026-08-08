# Production Spirit Privacy And Shorthand Situation - 2026-06-04

Kind: situation report

Topics: spirit, privacy, shorthand, production, deployment

## Intent Anchors

[Spirit should become usable for more private concerns, so privacy
filtering and default visibility behavior must be clear before the user
relies on it for private material.]

[Spirit should consider shorthand operation surfaces that let agents omit
routine fields such as default certainty when the default is semantically
appropriate.]

[Medium certainty should be the normal default for routine Spirit
captures unless the psyche wording, emphasis, repetition, or context
justifies a higher or lower certainty.]

[Spirit privacy is a Magnitude on the privacy axis - records gain a
privacy field typed Magnitude where Zero means no privacy (open/public)
and Maximum means sealed.]

[Spirit gains a RecordDefault short-form recording operation taking only
fields agents commonly customize - topics, kind, description, magnitude -
with defaults injected for the rest.]

## Situation Summary

Production Spirit source has the privacy axis, default open/public
filtering for normal record queries, and tests proving that ordinary
`Observe (Records ...)` hides elevated-privacy records by default. The
installed live `spirit` command is still pinned to an older
`spirit-v0.3.0` build and rejects the privacy-aware query shape.

The short version: **do not use ordinary Spirit for private personal
substance yet.** The source is close, but the deployed command is not
privacy-aware, and even the production source still has observation
surfaces that should be closed before the user relies on Spirit for
private concerns.

## Designer Report 59

`reports/system-designer/59-design-to-implementation-audit-2026-06-04/`
is an active meta-report directory. At this check it contains:

- `0-frame-and-method.md`
- `1-spirit-production-triad-gap.md`
- `2-spirit-next-schema-parity.md`
- `3-rust-discipline-and-repetition.md`
- `4-triad-shape-naming-and-manifestation-drift.md`

The frame says system-designer is running a broader design-to-code audit
with sub-slices for production Spirit triad gaps, spirit-next schema
parity, Rust discipline, and triad naming.

The production-triad slice confirms that `CollectRemovalCandidates`
landed in source as a combined archive-then-retract operation, that
`OutputTarget` is still not the designed `Stdout | Stderr | File` shape,
that the small-record/date-time shape is not settled, and that
`RecordDefault` is missing as an operation root. It does not audit the
extra privacy leak paths below.

The spirit-next slice confirms the important architectural split:
`spirit-next` is the schema-derived pilot, while the privacy/removal/
default-command work lives in the production `persona-spirit` triad.
The production privacy question is therefore not settled by spirit-next
parity work.

The triad-shape slice independently identifies the same `RecordDefault`
tension: older intent says `RecordDefault` carries magnitude as a custom
field; newer intent says routine certainty should default to `Medium`.
So the final short-form field split needs a psyche decision before
implementation.

## What Is Live

Live command:

```text
/nix/store/n0pi3ahjv5s766lnxyvv0z7qyvy7aaw8-spirit-v0.3.0/bin/spirit-v0.3.0
```

Live check:

```text
spirit "(Observe (Records ((Any []) None Any Any (Exact Zero) SummaryOnly)))"
```

Result:

```text
invalid request text: expected PascalCase identifier, got LParen
```

That request is the privacy-aware six-field `RecordQuery` shape. The
live parser rejects it, so the unsuffixed `spirit` wrapper is not yet on
the privacy-aware contract.

CriomOS-home still pins the production input:

```nix
persona-spirit-v0-3-0.url =
  "github:LiGoldragon/persona-spirit?rev=df09280a464f8a7be1c20ff433de4bfc4afc7f53";
```

Current production source is later:

- `persona-spirit` main: `7233075c397a` - collect removal candidates
- `signal-persona-spirit` main: `a69769b36678` - add removal candidate collection

## What Production Source Has

The ordinary signal contract has privacy as a `Magnitude`:

```rust
pub type Certainty = Magnitude;
pub type Privacy = Magnitude;

pub struct Entry {
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Certainty,
    pub privacy: Privacy,
}
```

`Entry::open(...)` defaults privacy to `Magnitude::Zero`, and
compatibility decode defaults omitted privacy to `Zero`.

`RecordQuery` carries a `PrivacySelection`, and
`PrivacySelection::default_observation_privacy()` is `Exact(Zero)`.
`SpiritStore::records_for_query` applies `RecordFilter::matches`, and
that filter includes `matches_privacy`.

This is the good part: normal `Observe (Records ...)` queries in the
source default to open/public records only.

The source has a boundary test named
`persona_spirit_client_filters_record_observation_by_privacy`. It writes
an open record and a high-privacy record, observes by default, and sees
only the open record; then it uses explicit privacy selectors and sees
the elevated one.

## Safety Gaps In Source

The source is not yet safe enough to call "private-ready".

### Identifier Observation Bypasses Privacy

`persona-spirit/src/store.rs` has:

```rust
fn records_for_identifier_query(
    &self,
    query: RecordIdentifierQuery,
) -> Result<Vec<StoredRecord>> {
    Ok(self
        .all_records()?
        .into_iter()
        .filter(|record| query.contains(record.identifier))
        .collect())
}
```

There is no privacy selection on `RecordIdentifierQuery`, and no default
privacy filter in this path. A caller who knows or guesses an identifier
can request it directly. That leaks elevated private records through
`Observe (RecordIdentifiers ...)`.

### Topic Counts Bypass Privacy

`observe_topics()` calls `topic_counts()`, and `topic_counts()` counts
topics across `all_records()`. It does not apply `privacy = Exact Zero`.
That means topic names and counts from elevated private records can leak
through `(Observe Topics)`.

### Subscriptions Need A Privacy Surface

`RecordSubscription` currently carries only:

```rust
pub struct RecordSubscription {
    pub topic: Option<Topic>,
    pub mode: ObservationMode,
}
```

The initial snapshot goes through `summaries_for_topic`, which uses the
default public privacy filter. But the subscription contract itself has
no privacy selection, so private-aware watch semantics are not explicit.
Before private use, watch/update behavior should get a direct test:
elevated records must not appear by default through subscription
snapshots or events.

### No ChangePrivacy Operation

There is `ChangeCertainty`, but no `ChangePrivacy`. If an agent records
something at the wrong privacy magnitude, the production source has no
ordinary correction operation for reclassification. That makes private
work brittle.

### Collection Authority Is Not Settled

`CollectRemovalCandidates` defaults to public candidates in its
constructor, but the full request can carry another privacy selection.
Collection also retracts records after archive success. That is fine for
public cleanup, but private/elevated candidate collection should not be
ordinary unrestricted behavior.

## Shorthand Root Commands

The CLI must still take exactly one NOTA argument. "Root command" here
means a typed ordinary signal operation variant, not shell flags and not
argv subcommands.

### Why Shorthand Roots Are Valuable

They encode policy in a named typed operation. A daily-use capture should
not force agents to hand-compose every rarely changed field. Fewer fields
also means fewer mistakes when agents are recording intent under time
pressure.

The strongest candidate is `RecordDefault`, because the in-process twin
already exists as `Entry::open(...)`: topics, kind, description, certainty;
privacy defaults to `Zero`; daemon stamps date/time.

### The New Certainty Question

Earlier reports leaned toward:

```nota
(RecordDefault ([spirit] Decision [summary] High))
```

The new psyche direction says routine captures should normally default
certainty to `Medium`, unless wording, emphasis, repetition, or context
justifies another value. That changes the cleanest shorthand design.

The better ladder now looks like this:

```nota
(Record ([spirit] Decision [summary] High Zero))
(RecordOpen ([spirit] Decision [summary] High))
(RecordDefault ([spirit] Decision [summary]))
(RecordPrivate ([personal] Clarification [summary] High))
```

Meanings:

- `Record` is full fidelity: explicit certainty and privacy.
- `RecordOpen` is explicit certainty, privacy defaults to `Zero`.
- `RecordDefault` is routine public capture: certainty defaults to
  `Medium`, privacy defaults to `Zero`.
- `RecordPrivate` is a convenience only after privacy safety is closed;
  its exact privacy default is a design choice, probably `High`, not
  `Maximum`.

This supersedes the older "RecordDefault takes magnitude" lean unless
the user wants `RecordDefault` to mean "default everything except
certainty." The name reads more naturally as "default the routine
fields," including certainty.

### Root Versus Nested Variants

Two shapes are coherent:

```nota
(RecordDefault ([spirit] Decision [summary]))
```

or:

```nota
(Record (Default ([spirit] Decision [summary])))
```

The first is easier for daily use and keeps migration additive in the
existing contract. The second is conceptually tidier for a future
schema-derived operation family, but it would reshape the existing
`Record` payload. For production, root variants are the pragmatic
choice; spirit-next can later model the more elegant nested family if
the schema wants it.

## Recommended Order

1. Do not store private personal substance in live ordinary Spirit yet.
2. Fix source privacy leaks: identifier observation, topic counts,
   subscription witnesses, and privacy reclassification.
3. Add tests proving default public filtering across every read surface,
   not only `Observe (Records ...)`.
4. Decide shorthand names: `RecordDefault` with implicit `Medium`, plus
   maybe `RecordOpen` for explicit certainty with public privacy.
5. Update CriomOS-home pin and activate the profile only after the source
   surface is privacy-safe.
6. Update `skills/privacy.md` and `skills/spirit-cli.md` after deployment
   so agents know whether the installed command is safe.

## Best Questions

1. Should `RecordDefault` now omit certainty and default to `Medium`, or
   should it keep the older four-field shape and be renamed to something
   like `RecordOpen`?
2. Should exact/range identifier observations default to public-only and
   require an explicit privacy selector, or should identifier lookup be
   owner-only once any elevated privacy exists?
3. Should `(Observe Topics)` hide private topics entirely by default, or
   show redacted aggregate counts? My recommendation is hide entirely for
   the first privacy-safe production cut.
4. What should `RecordPrivate` mean on the privacy axis: `High` by
   default, or no default with privacy magnitude required explicitly?

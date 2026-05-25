# 186 — Spirit next description-only implementation

Date: 2026-05-25
Lane: operator
Slice: description-only Spirit next, safe NOTA string support, and schema-derived contract alignment

## Intent Captured

Relevant Spirit records captured for this slice:

- 673: next Spirit entries remove verbatim / quote.
- 674: record acknowledgement must stay terse.
- 675: timestamps are daemon-stamped.
- 676: topics are user-created single strings.
- 677: safe NOTA string forms are bare strings, bracket strings, and bracket-pipe block strings.
- 678: agents clarify psyche prompts into one description.
- 690: schema / signal / CLI NOTA should avoid quote-delimited strings.
- 691: intent capture should become dense and less verbose.

## What Changed

`nota-codec` main:

- Commit `9e855d4775ec` (`nota-codec: emit block strings for bracket-safe text`).
- `Encoder::write_string` now emits `[|...|]` when text contains `]` and has no block-delimiter collision.
- This makes macro/code text square-bracket-safe without falling back to quote-delimited strings.

`signal-frame` main:

- Commit `d61ebf25997c` (`signal-frame: constrain schema boxed nota codecs`).
- `[schema]` / `signal_channel!([schema])` routes through the schema reader.
- Boxed NOTA codec emission is constrained to request payload types, avoiding bad generated CLI codecs for reply/event-only definitions.

`signal-persona-spirit` main:

- Commit `6a220349ba7f` (`signal-persona-spirit: pin safe nota block encoder`).
- Working contract is now description-only for entries:
  - `Entry [Topic Kind Description Certainty]`
  - no `Summary`, no `Context`, no `Quote`
  - `ObservationMode (DescriptionOnly WithProvenance)`
- `PresenceView` replaced a schema namespace collision where `State` was doing two jobs.

`persona-spirit` main:

- Commit `ba1956d23217` (`persona-spirit: add description-only spirit next`).
- Runtime crate version is `0.2.0`.
- Added `spirit-next` thin CLI binary through `signal_frame::signal_cli!(spirit_next, signal_persona_spirit)`.
- Added `packages.spirit-next` and `apps.spirit-next` to the flake; split-package witness checks that the package contains only `spirit-next`.
- Store schema moved to `SchemaVersion::new(2)` and contract bytes to the `0.2.0` marker.
- `Entry`, `StampedEntry`, `RecordDescription`, and `RecordProvenance` now carry one clarified `Description`, with daemon-owned `Date` and `Time` on provenance.
- Record observation paths return descriptions by default and provenance only on request.
- Tests now use quote-free safe NOTA strings such as `[selector seed]` and `[design d route]`.
- The local concept schema and `skills.md` were updated to the description-only shape and the current delimiter discipline: enum/variant groups use parentheses, record fields use brackets.

## Constraints Added Or Preserved

- `Record` input has no client timestamp and no verbatim/quote field.
- Timestamp remains daemon-owned through `ClockPlane`.
- CLI remains a thin Signal client; no store bypass.
- `spirit-next` is installable separately from `spirit` and `persona-spirit-daemon`.
- Handoff routing tests use short Unix socket paths so the test actually constrains the routing behavior instead of failing on `SUN_LEN`.

## Verification

All verification used Nix with the remote builder setting:

- `nix develop --option max-jobs 0 --command cargo test`
- `nix flake check --option max-jobs 0 --print-build-logs`

The flake check passed with:

- build
- full cargo test
- boundary tests
- actor-runtime tests
- daemon tests
- Design D handoff routing tests
- short-header ingress triage
- version handover readiness / freeze / recovery / mirror tests
- sema projection tests
- split package witness
- docs
- fmt
- clippy with `-D warnings`

## Caveats

This slice makes the next Spirit shape buildable and testable. It does not cut production over. The production migration / handover path remains a separate deployment and migration decision.

The schema path still uses the compatibility `signal_channel!([schema])` entry in `signal-frame`; the intended long-term public macro name is `emit_schema!`. The new code is moving through the schema reader/composer path, but the old entry point name has not been deleted in this slice.

There is an unrelated conflicted designer bookmark in `persona-spirit` (`designer-schema-full-stack-spirit-2026-05-25`). I did not resolve or rewrite the designer branch from the operator lane.

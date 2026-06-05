# Spirit Weight And Certainty Audit

## Trigger

The psyche clarified that Spirit weight and certainty are separate:
weight is recurrence / accumulated importance, while certainty is confidence
in the specific statement. The psyche also marked the weight-field mechanism
itself as low-certainty and asked for an audit of existing Spirit records.

## Records Added

- `u2s9` — low-certainty clarification: entry weight is intended as a set
  record axis for preserving accumulated importance after agglomeration, but
  the mechanism is not ready for production.
- `hp3r` — production Spirit does not need a weight-field migration now.
- `jn99` — when the psyche marks a statement low-certainty, agents must search
  for higher-certainty records that partially contain the tentative idea.
- `d1bi` — NOTA positional structs do not omit fields; public/private Spirit
  ergonomics should come from shorthand operations that lower to the verbose
  shape.
- `xbb5` — Spirit should support targeted shorthand operations for common
  agent workflows.
- `cx7y` — Spirit archive storage gets a sensible default and daemon
  configuration.
- `cgd8` — daemon configuration changes through the meta-signal socket.

## Audit Finding

`d5s2` was the one clear stale high-certainty record. It said intent
agglomeration should combine many lower-certainty records into a single
higher-certainty record. That conflated recurrence / accumulation with
certainty.

I recorded correction `6z6t`: agglomeration should preserve provenance and may
preserve accumulated importance through weight when that axis exists, but it
does not automatically raise certainty. Certainty rises only when the
synthesized statement itself is better supported or stated with higher
confidence.

I lowered `d5s2` from `High` to `Low` using `ChangeCertainty`.

## Skill Changes

`skills/intent-log.md` now says the proposed explicit `Weight` field is a
future low-certainty record-shape design, not production behavior, and adds the
low-certainty audit rule.

`skills/intent-maintenance.md` now has a mixed-certainty-record failure mode:
when one record bundles settled and tentative claims, split/correct them so the
sub-claims carry the right certainty.

`skills/spirit-cli.md` now explains that public/private/search shorthands are a
desired ergonomic direction but are not live request heads until implemented in
the deployed signal contract.

`skills/component-triad.md` already had the core meta-signal policy boundary; I
made the daemon-configuration rule explicit there: after first-start bootstrap,
configuration verbs live in the meta-signal contract, not CLI flags, ad hoc
files, or ordinary signal requests.

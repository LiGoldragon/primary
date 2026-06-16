# Spirit skill documentation refresh

## Scope

The psyche asked for a fresh audit of the Spirit-facing skills, grounded in
deployed Spirit behavior and the latest schema/structural-forms correction:
generic use remains ordinary `(Head Arg...)`; `{| |}` belongs to traits/impls;
an impl is one pipe-brace structural object, not a map key/value split; optional
leading `[params]` and optional trailing body brackets are structural-sugar
matches; marker impls may be bodyless, and method-bearing impls carry function
bodies as data with no ad hoc `method` keyword.

I did not record new Spirit intent. This was documentation maintenance.

## Source grounding

Read during the pass:

- deployed Spirit source under `/git/github.com/LiGoldragon/spirit`
- deployed signal contract under `/git/github.com/LiGoldragon/signal-spirit`
- `reports/operator/389-spirit-new-design-implementation-frontier.md`
- `reports/operator/390-operator-situation-worktrees-and-questions.md`
- `reports/designer/655-explicit-generic-syntax-pipe-delimiter-family.md`
- `reports/designer/658-reactive-component-end-to-end-operator-spec.md`

Important source facts:

- Production Spirit reports `0.13.0`.
- The deployed signal contract has `Clarify`, `Supersede`, `Retire`, `Remove`,
  `ChangeCertainty`, `BumpImportance`, `ChangeRecord`,
  `CollectRemovalCandidates`, `Version`, and `Marker`.
- There is no deployed `ResolveClarification` input or receipt in
  `signal-spirit` or `spirit`.
- `RecordChange` is a three-slot record: `RecordIdentifier`, replacement
  `Entry`, and `Justification`.
- `spirit-render` exists in Spirit source as a one-argument NOTA client using
  `(Render ([referents...] output-directory?))`; it is not installed in this
  profile at the time of this audit.

## Changes landed

`skills/spirit-cli.md`:

- kept the production version aligned with Spirit `0.13.0`;
- added `spirit-render` as a source-backed public intent snapshot tool;
- corrected the `ChangeRecord` example to the real `RecordChange` shape;
- kept `ResolveClarification` documented as a missing first-class operation and
  a manual maintenance protocol, not as deployed behavior.

`skills/intent-log.md`:

- updated stale domain examples from deprecated
  `Engineering SoftwareArchitecture` to current `Engineering Architecture`;
- retained the clarification-as-edit rule, with standalone clarification cleanup
  routed through maintenance.

`skills/structural-forms.md` and `skills/skills.nota` already reflect the latest
structural correction in the final working-copy base:

- streams/families are positional special forms, not structs;
- pipe-parenthesis is generic declaration syntax;
- generic use remains ordinary application;
- pipe-brace is traits/impls;
- impls are single structural objects with optional leading params and optional
  trailing bodies.

Those structural/index edits were already present in the current parent commit
while this pass was underway, so the final commit from this pass only needs to
carry the remaining Spirit CLI / intent-log changes plus this report.

## Verification

Live commands:

```sh
spirit Version
# (VersionReported 0.13.0)

spirit Marker
# (MarkerReported (1312 12541975979470193249))
```

Search checks:

- no stale `0.12.0`, `v0.9.5`, `Live v`, or `SoftwareArchitecture` references
  remain in the touched Spirit/intent/structural skill files;
- no `ResolveClarification` symbol exists in deployed `signal-spirit` or
  `spirit` source.

Source-backed test:

```sh
cargo test --features nota-text --test spirit_render
# 3 passed
```

## Open questions

The skill files now document the manual `ResolveClarification` protocol, but the
operation itself is still open work (`primary-4itq`). The clean implementation
target remains `signal-spirit` plus `spirit`: add a first-class
`ResolveClarification` input/output pair, then atomically edit target records and
remove or retire the standalone clarification.

`spirit-render` is present in source but not installed in this profile. If it is
intended to be part of the routine agent surface, the deployment/profile layer
should expose it beside `spirit`.

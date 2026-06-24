# Handover — context maintenance correction

## Current state

The psyche corrected the operator's misunderstanding of the request. The request
was not to rewrite `skills/context-maintenance.md` from scratch. The intended
work was to run or document context maintenance as an intent-alignment-driven
process: review stale reports and live context, identify each item whose
abandon / keep / migrate / forward disposition is uncertain, and ask the psyche
one focused intent-alignment question before deciding.

Spirit now carries this corrected intent as record `ne92` (the context
maintenance refresh decision): context maintenance is research-driven
intent-alignment refresh, not deletion; uncertain disposition choices go through
the psyche before the agent decides.

## File recovery

Bad commit `05cdb9ad` (the mistaken `skills/context-maintenance.md` rewrite)
was not left as the live file shape. The working copy restored
`skills/context-maintenance.md` from commit `6578a836` (the state before the bad
rewrite) and then applied only the intended narrow skill edit:

- in `skills/context-maintenance.md` under `2a · Per item, decide`, uncertain
  abandon / keep / migrate / forward decisions now point to
  `intent-alignment.md`;
- the `See also` list now includes `intent-alignment.md`;
- the skill does not repeat the intent-alignment procedure.

Commit `6578a836` also contains a schema-designer report that was already dirty
in the shared working copy before this correction. Do not undo that report
commit as part of recovering the context-maintenance mistake; it was merely
drained per the primary `jj` rule.

## Next clean session

Start by reading:

- `skills/context-maintenance.md`
- `skills/intent-alignment.md`
- Spirit record `ne92` (the context-maintenance refresh decision)

Then continue with the actual maintenance pass: enumerate the candidate reports
or context items, and for every item where abandonment versus retention is
unclear, ask the psyche one intent-alignment question carrying the decision, why
it matters, the recommended action, and the alternatives.

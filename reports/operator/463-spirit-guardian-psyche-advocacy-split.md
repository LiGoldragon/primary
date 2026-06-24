# Spirit Guardian Psyche / Advocacy Split

## Current State

The current `signal-spirit` schema already separates direct psyche words from
agent advocacy.

In `/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema`:

```nota
VerbatimQuote { QuoteText OptionalAntecedent.(Optional Antecedent) }
Testimony (Vector VerbatimQuote)
Reasoning String
Justification { Testimony Reasoning }
RecordRequest { Entry Justification }
```

That means a Spirit write already has three conceptual layers:

- `Entry`: the claim being proposed for the intent store.
- `Testimony`: direct psyche words, with optional antecedent context for short
  answers like `yes`.
- `Reasoning`: the agent's argued case for why the entry, operation, domain,
  privacy, certainty, and importance are justified.

The current guardian prompt also names this split in
`/git/github.com/LiGoldragon/spirit/src/guardian-prompts/justification-shape.md`.
It says testimony is raw psyche words plus optional antecedent, and reasoning is
one prose field for the argued case.

## Misalignment

The prompt shape is mostly right, but the burden prompt currently narrows
elevated importance support to:

- recurrence
- blast radius
- keeps-coming-up
- blocks-other-work

That misses the newly aligned rule: a psyche-named rung is itself sufficient
evidence for that rung. Agent advocacy remains valid as a separate evidence
path, but it should not be required when the psyche directly assigns the rung.

The prompt also does not yet strongly teach the guardian to treat rejections as
remands with repair shape: if the entry is wrong as a fresh `Record`, the reply
should name the likely maintenance operation family (`Clarify`,
`ChangeRecord`, `Supersede`, `Retire`, `Remove`, or affirmative rewording).

## Recommendation

Keep the current typed schema. Do not collapse testimony into reasoning and do
not make quote syntax inside freeform advocacy the primary mechanism. The
existing `Testimony` vector plus `Optional Antecedent` is the right structural
shape because it lets the daemon and guardian inspect psyche words as data.

Change the guardian prompts and tests:

- In `burden-ladder.md`, add direct psyche-declared metadata as sufficient
  support for the named certainty, importance, or privacy rung.
- Keep agent advocacy as an alternate support path: recurrence, architectural
  centrality, blast radius, and blocking effect can justify elevated importance
  when the psyche did not explicitly name a rung.
- In `checklist.md`, sharpen rejection behavior into repair-shaped remands.
- In `few-shot.md`, add examples for direct named importance/privacy and for a
  contradiction that must be resubmitted as a broader maintenance operation.

The practical prompt alignment is: psyche words are evidence; agent reasoning is
advocacy; the guardian verifies the advocacy remains tethered to testimony and
the existing record bundle.

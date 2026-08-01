# Ethos Non-Repetition Law — 2026-08-01

Ruling from the psyche vision session, correcting the manager's SimpleGeneric
example syntax.

Agent text answered: the manager's proposed authored surface
`Sorted.SimpleGeneric.{Ord Vector.Ord}`, where the contract `Ord` appears
once as the parameter and again in the body.

Psyche ruling [psyche-verbatim]: "we wouldnt repeat Ord; any such repition
in ethos syntax is an implementation failure. ethos will be the most terse
non-repetitive syntax ever made"

## Seated meaning

- **Law**: authored Ethos never repeats a symbol the position or the
  governing Nomos object can imply. A repetition in authored Ethos is an
  implementation failure — the Nomos object (or grammar position) was
  designed wrong, and the fix belongs in the transformer, never in asking
  the author to repeat.
- **Aspiration, stated as directive**: Ethos is to be the most terse,
  non-repetitive syntax ever made. This sharpens the existing conciseness
  gradient (Ethos maximally concise) and the "only write the bits that
  change" principle into a testable acceptance rule: an Ethos fixture
  containing an inferable repetition fails review.
- Corrected example [agent-inference, following the ruling]: SimpleGeneric's
  payload shape is `{contract bodyHead}`; the emission applies the body head
  to the parameter, so the contract is written once:

```text
Sorted.SimpleGeneric.{Ord Vector}
```

```rust
pub struct Sorted<T: Ord>(Vec<T>);
```

- Per-need corollary [agent-inference]: where a body needs the parameter in
  a non-tail position or more than once, that is a different pattern — a
  different Nomos object with its own most-terse surface — rather than a
  general placeholder bolted onto SimpleGeneric. Positional implication
  first; explicit reference machinery only when a real pattern demands it,
  and then designed for that pattern.
- Audit upgrade: the syntax audit's noise findings
  (`reports/DesignConsistencyAudit-2026-08-01.md` — the `Public` literal in
  every template, the five empty slots, the 13-atom duplicated attribute
  lists) upgrade from smell to implementation failure under this law.

# Skill — beauty as the criterion

*Beauty is the test of correctness; ugliness is the diagnostic reading.*

## What this skill is for

When something you've written or are reviewing **feels ugly**, the
discomfort is the diagnostic. Beauty is the operative test of
correctness; ugliness is evidence the underlying problem is
unsolved. The readings below name what each kind of ugliness
signals.

When the right structure is found, ugliness dissolves: special
cases collapse into the normal case; repetition resolves into a
single named pattern. Slow down and find that structure. The
structure you find *is* the one you were missing.

If you cannot make it beautiful, you do not understand it yet.

## The rule

**If it isn't beautiful, it isn't done.**

Beauty is a **gate alongside correctness**, not a nice-to-have. The
aesthetic dimensions that pass the gate — **terseness, symmetry,
schema-driven emission, self-describing surfaces, interfaces-first
shaping, composable boundaries** — are the form the rule takes when
applied to typed-data workspaces like this one. A design that
satisfies correctness but fails any of those dimensions is not yet
done; the discomfort signals an unsolved underlying problem.

## Beauty as primary audit lens

Audits apply the beauty filter as the **primary lens**. Before asking
"does this work?" the audit asks "is the shape right?" — terseness,
symmetry, schema-driven, self-describing, interfaces-first,
composable boundaries. When the shape is wrong, the audit's
recommendation is the structural fix, not a patch that preserves the
ugly surface.

This applies at three workspace scales:

- **Code beauty** — the diagnostic catalogue below. Verb-belongs-to-
  noun violations, stringly-typed dispatch, special cases stacked on
  the normal case, hand-written shape where schema can emit it.
- **Capture discipline** — avoid duplicate intent records. A trio
  saying the same thing in three different magnitudes is noise; one
  record at the right magnitude is signal. The supersession protocol
  (`skills/intent-maintenance.md`) and the dedup sweep are how the
  intent layer stays beautiful.
- **Report retention** — avoid report proliferation without
  retirement. A working artifact whose substance has migrated to a
  permanent home is finished; leaving it in the tree clutters the
  surface. The retire-after-migration discipline
  (`skills/context-maintenance.md` §3a) is how reports stay clean.

The fourth scale is **substrate cleanliness**: no hand-written code
where schema can drive. When a hand-written enum, validate impl,
trace event vocabulary, or projection function parallels something a
schema could emit, the parallel is the ugliness; the fix is to push
the substance into the schema.

Per psyche 2026-06-02 (Spirit 1411, Principle Maximum).

## What ugliness signals

Each item below is a *signal*, not a sin. Notice it; decide what the
underlying problem is; fix the underlying problem.

- **A name that doesn't read as English.** `pf`, `de`, `kd`, `tok`,
  `op`. Each abbreviation costs the reader one mental lookup per
  occurrence forever, to save the writer three keystrokes once. The
  "verbosity" objection is itself training-data drift, not informed
  judgment.
- **A `pub` field on a wrapper newtype.** `Slot(pub u64)` is a
  label, not an abstraction.
- **A free function that should be a method.** A verb that could
  attach to a noun reads as a missing model. See this workspace's
  `skills/abstractions.md`.
- **Dead code retained "for safety" or "for backward compatibility."**
  Ariane 5. Knight Capital. Delete it; the history is in `git log`.
- **Special cases stacked on the normal case.** Find the rewrite
  that makes the special case disappear (Torvalds's linked-list
  lesson).
- **Stringly-typed dispatch.** `match name.as_str()` over cases that
  should be a closed enum. Perfect-specificity violation.
- **A doc comment that explains *what* the code does.** Well-named
  code already explains what it does; the comment signals the names
  aren't carrying their weight.
- **A boolean parameter at a call site.** `frob(x, true)` reads as
  gibberish. Split into two functions or pass a typed enum.
- **A name for what something is *not*.** `non_root`, `non_empty`,
  `not_admin`. Negative names compose poorly. Find the positive
  name.
- **A long function with multiple responsibilities.** Split it.

## The "feels too verbose" anti-pattern

The most common slip is the verbosity objection to spelled-out
names. When `AssertOperation` "feels needlessly verbose," that
feeling is the signal to **question the feeling** — not the signal
to shorten the name.

The full English form reads as English. The abbreviation reads as
ceremony to be decoded. The cost of mis-naming is paid every time
the name is read; the benefit of saving three keystrokes is paid
once.

Per Li (2026-04-27): *"You were taught wrong."* The criterion is
beauty, not keystroke-economy.

## See also

- this workspace's `skills/abstractions.md` — the
  verb-belongs-to-noun rule (one of the diagnostic readings
  above).
- this workspace's `skills/enum-contact-points.md` — engine
  logic = enum-vs-enum cross-product. A scattered matrix
  (nested `if` chains over state combinations, string-prefix
  dispatch over a closed set) is one of the diagnostic readings
  above; that skill is the canonical refactor.
- this workspace's `skills/naming.md` — the spelled-out-words
  rule.
- this workspace's `skills/rust-discipline.md` — Rust-specific
  application of these rules.
- this workspace's `skills/skill-editor.md` — how skills are
  written and cross-referenced.
- this workspace's `ESSENCE.md` §"Beauty is the criterion" —
  upstream framing of this skill.

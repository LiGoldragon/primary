# Implementations in Ethos: Two Designs

Made 2026-09-25 by a subflow of e51411 from two independent designs written the same day without sight of each other:

- **Fable's**: flows/38de5b/reports/ethos-implementations-fable.md (Psyche High 38de5b, commit 30cf5f41b).
- **Opus's**: flows/e51411/reports/ethos-implementations-opus.md (a subflow of e51411, commit a681fdbeb).

Code on pages 2 and 3 is copied from the reports unchanged. Marks: **tested** means the report says it was run; **untested** means it is designed or written but not run. No winner is declared; the last page lists the forks.

## Page 1 · The ask

> I don't know if it would satisfy me but if you think you can figure out how we would extend the syntax of ethos to do the functions and support it and make the syntax perfect and super minimal (so that there's no repetition, nothing out of place, and no noise), it's all just pure description of a program, as compact as it can be, basically, and not in word size. We don't shorten words. The compactness is in the very low noise amount.

-- psyche, STT, 2026-09-25, to e51411 (flows/e51411/vision/ethos.md, last entry, as committed in b8db92ad2).

> You can put a sub-agent and make a presentation or ask Fable and then present both in the book.

-- psyche, 2026-09-25, to e51411, as relayed verbatim in the main flow's brief.

*Note:* flows/e51411/vision/ethos.md is absent from the working tree; commit 0436fb21d deleted it. The first quote is from its last committed text. The second sentence was not found in any committed version.

Both designs answer the same thing: how a kind's capabilities get their bodies, written in Ethos itself.

## Page 2 · Fable: every value has a name

**Core idea.** An association that carries bodies is an implementation: `Store.[ Lockable.{ … } ]`, one body per capability, in the kind's order. There are no free functions. Bodies use Ethos's own shape, a name, a dot, what it stands for, and five rules:

1. **Binding.** `name.expression`. Lowercase head = a binding; also the parameter of a body or closure.
2. **Construction.** The datom of the value: `Lock.{ … }`, `Err.DuplicateName.held`.
3. **Call.** `receiver.capability.[ arguments ]`.
4. **Match.** A bracket after an enum value; one arm per variant, checked exhaustive.
5. **Sequence.** `[ steps ]`; the last step is the yield.

No keywords, operators, field names or type annotations in bodies. Intrinsics (`equals`, `find`, `push` …) are kinds declared in a protos library. Manifest: a datom of a `Manifest` type (name, version, files, dependencies).

The lock, in Fable's ethos (untested: not parsed or generated) — report §4, lines 43–74.

The Rust ethos-zero "would emit beside it" (untested: hand-written by Fable, not generated) — report §4, lines 80–111.

## Page 3 · Opus: every value is named by its type

**Core idea.** No new glyph, no new keyword, one structure: `Type.[ Kind.{ Body… } ]`. A body is a datom of the yield type with holes. Variable names are gone: a value is named by its type, as a field is. A lowercase head is a capability call; a capitalized head is a variant or a value, the expected type decides. Four rules:

1. **Scope (anuvṛtti).** In scope: Self, inputs, each step's result, loop elements, arm payloads, each named by type, and a struct's fields. Direct beats carried, nearer beats farther; a tie is refused.
2. **Fill.** Unwritten positions fill from scope, one unique value each. `Locked` alone means `Locked.Lock`.
3. **Exit.** A step yielding `Err.E` leaves at once when the yield type can carry E: Rust's `?` without the glyph.
4. **Effect.** Only a `!` capability changes Self, by a `Self.{ … }` step that builds a new Self. The runtime persists it.

Manifest: a fourth root, `Manifest`, the only place a version is written; it emits Cargo.toml and flake inputs.

The lock, in Opus's ethos — report §2, lines 40–85. Tested: the protos reader accepts it whole; ethos-zero 10.0.0 refuses it at the first body (`Conceptual.{ [ 3 0 1 0 ] Expected.Reference }`). The resolve rules are untested.

The current Rust it replaces (real code, orchestrate 9070cbb, excerpt) — report §2, lines 104–121. Measured: 44 lines / 509 tokens against 226 lines / 1681 tokens, 3.3× smaller; glyph share unchanged, about 60%.

## Page 4 · Side by side, and where they agree

| | Fable | Opus |
|---|---|---|
| New glyphs / keywords | None. Five body rules. | None. One structure, four scope rules. |
| How a body reads | Named parameter, then an expression; calls as `receiver.capability.[ args ]`; refusals nest as match arms. | A column of steps, each bound under its type; the last is the yield. |
| Data flow | Visible: every value has a written name (`request`, `held`, `lock`). | Implicit: filled from scope by type; visible in a resolved print. |
| Noise | Names repeat (`request.lock_name`, `held`). Not counted. | Counted: 509 tokens vs 1681 in Rust; words fall, glyph share stays ~60%. Tested. |
| Refusal | Nested arms; a `?` rule deferred. | Exit rule: leaves silently by type. |
| Changing state | Calls in place (`increment`, `push`); the generator picks move, clone or borrow. | `Self.{ … }` rebuilds Self under `!` only; everything else pure. |
| Where it strains | Ownership invisible; bracket meaning by position; deep nesting; one-name closures; the intrinsic library. | Everything read by type; Fill acts at a distance; two values of one type; unmarked exit; whole-Self persistence vs Sema; aliases need newtypes; drift from the Rust. |
| Manifest | A datom of a `Manifest` type. | A fourth root, `Manifest`, with a product. |
| Example scope | Lock, release, observe, prefix overlap. No contract change. | Full ledger with path normalisation and runtime answer; adds four rejection variants to the contract. |
| Built first | ethos-zero fixes 5 and 7; protos kinds for Vector, Option, Result, Integer, String; generate Orchestrate's store and diff it. | Audit generator fixes; a resolve-only prototype (~800–1200 lines) that prints expanded bodies; negative fixtures. |
| Verdict | Worth doing now for one slice: the pure store transitions of the Nexuses. | Worth doing now only as a resolver, not emission; fall back to written arguments if Fill trips agents (~15% more tokens). |

**Where they agree.**

- No new glyph and no keyword: bodies are datom shapes, and position says what a bracket means.
- An implementation lives in the association section, `Type.[ Kind.{ … } ]`, bodies in the kind's order, capability names not repeated.
- A construction is the datom literal of the value.
- Case carries meaning (they differ on what lowercase means: a binding for Fable, a capability for Opus).
- Intrinsics are a library of kinds still to be designed, and naming is won or lost there.
- The version lives only in a manifest that is itself datom.
- Reading needs the types in view.
- Worth doing now only in a bounded form, after the audit fixes; Orchestrate's locks are the first test; I/O stays in Rust or the runtime.

## Page 5 · What you rule on

1. ☐ **Names or types?** Values carry written names (Fable), or are named by their type and filled from scope (Opus).
2. ☐ **How a refusal leaves.** Nested match arms (Fable), an unmarked typed exit (Opus), or a marked `?`-shaped rule.
3. ☐ **How state changes.** Calls in place with ownership chosen by the generator (Fable), or a whole new Self under `!` that the runtime persists (Opus).
4. ☐ **The manifest's form.** A datom of a `Manifest` type (Fable), or a fourth root (Opus).
5. ☐ **Refusals in the contract.** Path errors as typed `LockRejection` variants, as Opus's example needs, or kept as store errors.
6. ☐ **`Name.String` as a real newtype.** Opus needs nominal aliases to implement a kind on `LockPath` alone (audit fix 9).
7. ☐ **The first prototype.** Generate-and-diff Orchestrate's store (Fable), a resolve-only printer (Opus), or both on the same fixture.
8. ☐ **The intrinsic library.** Who names it and how: verbs only, or words like `either`, `empty`, `not`.

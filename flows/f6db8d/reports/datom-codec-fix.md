# datom-codec — the witnessed substrate defects, fixed

Flow f6db8d, datom-codec subflow. Autonomous: the living is asleep and ordered
the work done and recorded, with no questions.

## Revisions

| | |
|---|---|
| repository | `/git/github.com/LiGoldragon/datom-codec` (including `crates/datom-codec-derive`) |
| before | `99a9e8c9` — 0.25.7 |
| released | `196d0e290ad6` — pushed to `main` |
| version | **0.26.0** — minor, not patch: the canonical wire text changes, which is breaking |
| protos pin | unchanged, `b543678cfc8609529cea7174eb4af8a64daa54ad` — the sibling flow's writer fix had not reached protos `main` when this work landed (witnessed: `git fetch origin` in `/git/github.com/LiGoldragon/protos`, `origin/main` = `b543678`) |
| lock | Orchestrate Lock 1107 `DatomCodecSubstrateFixes`, the whole repository |

Not touched: protos, ethos-zero, any consumer.

## The two Vision questions the brief named

### The bare string — Vision rules, 0.25.7 is reversed

`Vision/datom.md`, "Syntax", the current text (commit `d21ae637e`, 2026-09-11):

> In such a position a string is written bare when it contains no space and no
> delimiter, Ada, 75002, 2026-09-03; any other string is written in
> guillemets. Because the position already knows it holds a string, a bare run
> may contain characters that are syntax elsewhere, the colon among them.

0.25.7 (`9bffbf1` "Quote structural separators in strings") added `.`, `!` and
`:` to the glyphs that force guillemets, so `a:b:c` and
`https://example.org/a` were written `«a:b:c»` and `«https://example.org/a»`.
That contradicts the sentence above, and it shipped as a patch bump over a
changed wire text. **Reverted.**

But 0.25.6 was not right either, and the reversal had a real cause. Witnessed
here, by running this flow's new property test against `f2cc068` (0.25.6):

```
Some.C7u. composes: Error { layer: Composition, path: [], kind: Form { expected: "Variant", found: "Bare" } }
Some.7u.  ...
Some.u.   ...
Some..    ...
```

Protos keeps an invalid separator chain as one bare structure (witnessed:
`Some..a` → `Bare("Some..a")`, `5::7/128` → `Bare("5::7/128")`), so a bare run
with an empty head segment swallows the head of the structure that carries it.
0.25.6 wrote such runs bare and could not read them back; 0.25.7 quoted every
separator and contradicted Vision.

**Decision taken on the living's behalf.** The writer keeps separators bare,
and delimits only the runs that cannot be written bare at all: a run that is
empty, holds a space or a delimiter glyph, *begins or ends with* `.`, `!` or
`:`, or holds two of them adjacent. So `gpt-5.6-luna`, `a:b:c`, `a!b`,
`https://example.org/a`, `Some.Ada` stay bare — Vision's sentence honoured —
while `.a`, `a.`, `a..b`, `a:.b`, `5::7/128` are written `«…»`. The rule is
not a preference about punctuation; it is the exact set protos cannot read
back. `src/composition.rs`, `Datomizable for String`.

### The decimal — Vision rules, the sniff is gone

`Vision/datom.md`, stated twice — under "Syntax":

> What a structure means, struct, vector, string, integer, variant, is said by
> the position it sits in, never by the structure alone.

and under "De/serialization":

> Schema-driven and positional: the reader walks the expected type … All
> naming and self-description live in the type; the text carries only the data.

The released code merged a headed structure into a bare one at the datom layer
when the head parsed as an `i64` and the body was all digits — a content sniff
before any type is known, observably wrong on `3.14.15` and `1.x`.
**Removed.** `3.14` now reaches composition as `Variant("3", Bare("14"))`, and
the Decimal position rejoins it, exactly as the String position already
rejoins a bare dotted run. Consequences, all witnessed by
`a_decimal_is_read_by_its_position_and_never_by_its_content`:

- an f64 position reads `2.75`, `-0.5`; a String position reads the same text
  as the string `2.75`; an Integer position refuses it as a `Form` error;
- `2.75.15`, `1.x`, `3.`, `007.5` are refused as Decimals — the rejoin
  validates the canonical spelling (optional `-`, no leading zero except `0`,
  a mandatory point, digits on both sides) rather than guessing;
- a decimal costs two budget nodes where the sniff made it one; the two test
  budgets that assumed one were raised.

## Every witnessed defect, and what was done

| audit | defect | fix | test |
|---|---|---|---|
| §1.3 | derived enums bypass the composition budget: the `Form::Bare` arm never spends | the bare arm spends like every other path | `bare_variants_spend_the_composition_budget` |
| §1.4 | `Foo::Bar()` and `Foo::Bar {}` datomize to a bare head but cannot compose back | both sides key on `fields.is_empty()`; the `count == 0` error arm and the dead empty-body arm are gone | `variants_carrying_nothing_round_trip_whatever_their_field_syntax` |
| §1.5 | `f64::NAN.datomize` panics | the assert is gone; a non-finite value writes text no Decimal position accepts, and the descent refuses it with `Value { expected: Decimal }` | `the_decimal_ascent_is_total_and_its_text_is_refused_on_the_way_back` |
| §1.5 | sixteen public `from_positions` methods are `unreachable!()` | `Compositional` now carries one capability, `compose`; `ARITY` and `from_positions` are gone from the trait and from all sixteen impls | the whole suite composes through the new trait |
| §1.6 | hand-written `datomize` impls mislabel their own paths | `protos::Extent`, `protos::Error`, `Error` and the five `ErrorKind` struct bodies are labelled `at.child(1)…`, the position a variant body actually holds | `every_datomized_node_carries_the_path_it_sits_at` walks the tree and compares every node's `path` with its position |
| §1.7 | `+4` composes as the Integer 4 | a leading `+` is refused | `integers_refuse_a_leading_plus` |
| §1.8 | a Meaning in a String position is accepted and destroyed | `Form::Meaning` is no longer a String; `(a meaning)` in a String position raises `Form { expected: String, found: Meaning }` | `strings_quote_delimiters_keep_bare_separators_and_refuse_meaning_text` (rewritten from the test that asserted the leniency) |
| §1.10 | `ARITY` is required of every type and read by nothing | arity is read once, where Vision puts it: `DatomPositioning::positions(arity)` refuses the wrong arity at the struct's own path before any position is read; `Positioning::finish` is gone | `a_struct_reports_its_declared_arity_at_its_own_path` |
| §2.2 | the decimal content sniff | above | above |
| §2.2 | `Option::compose` accepts a second, unreachable spelling of `None` | removed | — |
| §3.1 | the 0.25.6 → 0.25.7 bare-string reversal | above | `a_bare_string_keeps_its_separators_unless_the_run_would_swallow_its_context`, and the property test below |

Each of the eight tests in `tests/composition.rs` was **seen failing** against
the unfixed code before being trusted: a scratch clone at `99a9e8c` with the
new test file copied in reports `0 passed; 8 failed`.

### The missing test direction, now covered

The audit's sharpest point was that nothing in any suite went
build → print → parse, the direction the ascent uses. `tests/composition.rs`
now holds a proptest over that direction, at a root and inside a variant. It
has teeth: against `f2cc068` it fails and shrinks to `Some.u.` (transcript
above). Its alphabet excludes the backslash, because the protos writer does not
yet escape one (audit §1.1, owned by the sibling flow); when that lands, the
character belongs in this alphabet. `proptest` was a declared dev-dependency of
this crate used by nothing; it is now used.

## Decisions taken on the living's behalf

1. **The bare-string rule** — above. Vision's sentence is honoured; the
   delimited set is exactly what protos cannot read back, not a taste.
2. **The decimal rejoin** — above. Vision states the positional rule twice; the
   sniff contradicted it.
3. **`ARITY` and `from_positions` removed from `Compositional`.**
   `Vision/datom.md` gives the mechanism literally:

   > ```rust
   > let positions = self.positions(T::ARITY, budget)?;   // this form, as a struct of that arity, else an error at this path
   > T::from_positions(positions)
   > ```

   The trait, however, is borne by scalars, containers and enums as well as by
   structs, and for those there are no positions and no arity: that is why the
   released crate declared `String` 0, `Symbol` 1, `Vec` -1 and every derived
   enum 1, and why sixteen `from_positions` were `unreachable!()`. Vision's
   snippet is not implementable for those types as written. What Vision *wants*
   — "the reading of the tree, arity, budget, locus, lives in one place and no
   type repeats it" — is now true: `positions(arity)` is that one place, it
   refuses the wrong arity at the struct's own path, and the incremental
   `finish()` it replaces is gone. **The living may want the constant back if
   `Compositional` is ever split into a positional kind and a scalar kind;**
   that split is a Vision question, not a defect, and was not taken here.
4. **A non-finite decimal writes refusable text rather than aborting.** Vision
   is silent on non-finite decimals, and the terminal shape is plainly a
   Decimal type that cannot hold one — but `Vision/ethos.md:133` makes Decimal
   an intrinsic and ethos-zero lowers it to `f64`
   (`ethos-zero/src/generation.rs:58`), with fixtures using it, so removing
   `Datomizable for f64` would break a consumer this flow does not hold a lock
   on. The panic is removed; the value is written as `NaN` / `inf` / `-inf`,
   which no Decimal position accepts. **For the living: the terminal fix is a
   finite-decimal type, which is an ethos-zero change first.**
5. **The README was rewritten.** It described the pre-distillation design —
   `Datomic`, `Site`, `Fault`, `Worded`, curly-quote strings, a module list of
   modules that do not exist. Not a witnessed defect in the audit's list, but
   the same failure mode as §5, at the crate's front door.
6. **A second Nix check was added.** `datom-codec-kinds.ethos` had a committed
   generated contract that nothing compared; it was stale by a whole design
   generation. `generated-kinds-contract` now checks it, and both contracts
   were regenerated with the pinned ethos-zero.

## Contradictions left standing, for the living

Left as found, per the brief, because Vision is silent or self-contradictory:

1. **`Datomizable` names one conversion or two.** `Vision/protos.md` assigns
   `Datomizable` both to `Protos` and to a composition, and gives them
   different signatures — `Vision/protos.md:181` in the kinds table and the
   snippet below it — while `Intent/conversion.md` says "A kind names one
   conversion and is borne by the type that undergoes it." The code carries an
   associated `Output` so that `Protos` can implement it as a fallible descent
   (`Output = Result<Datom, Error>`) and a value as an infallible ascent
   (`Output = Datom`). Vision as written is not literally implementable; the
   shape is unchanged. *Verbatim, `Vision/datom.md:151-153`:*

   > A Rust type bears `Datomic` through two capabilities — `incorporate`
   > (static, constructs the value from a `Datom`) and `datomize` (projects the
   > value into a `Datom`)

   — which is the `datom` skill's older wording; `Vision/datom.md` itself names
   the pair `Datomizable` and `Compositional`
   (`Vision/datom.md`, "Any Rust type"), and `Datomic` there "names the
   conceptual layer abstractly; it is not a term of the code"
   (`Vision/datom.md`, "Name").
2. **`protos::Error` datomizes under the head `ProtosError`** while the
   `ErrorKind` variant that carries it is named `Structural`
   (`src/composition.rs`, `Datomizable for protos::Error`; `src/core.rs`,
   `ErrorKind::Structural`). Two names for one thing, so the text reads
   `Structural.ProtosError.{ … }`. Vision names neither; unchanged.
3. **`src/projection.rs` reimplements protos's canonical byte lengths**, keyed
   by a `HashMap` of raw pointer addresses. The two formulas agree today and
   nothing keeps them agreeing. Deduplicating it is a design change with no
   witnessed defect behind it; unchanged.
4. **`ErrorKind::Arity`'s `expected`** is now the declared arity everywhere a
   struct is read, but `Positions::position` still raises an `Arity` error of
   its own if a caller asks for more positions than it holds. With
   `positions(arity)` in front of it that cannot happen through the derive; it
   is kept as the honest refusal for a hand-written caller.

## The gate

Local, no remote builders.

```
cargo test --offline     32 passed (tests/core.rs) + 9 passed (tests/composition.rs) + 0 doc-tests, 0 failed
cargo fmt --all --check  clean
cargo clippy --offline --all-targets -- -D warnings   clean
cargo doc --offline --no-deps                          clean
nix flake check -L       all checks passed
                         build, test, fmt, clippy, doc, no-production-free-functions,
                         no-production-inherent-methods, no-zst-behavior,
                         no-forbidden-vocabulary, generated-contract,
                         generated-kinds-contract
```

The first `nix flake check -L` used the configured remote builder for some
derivations. The `test` check was then rebuilt with `--builders ''`, entirely
locally, and its log is the witness for both test binaries:

```
Running tests/composition.rs   9 passed; 0 failed
Running tests/core.rs         32 passed; 0 failed
```

The commit `196d0e290ad6` carries no `Co-Authored-By` / `Claude-Session`
trailer: it was pushed before the omission was noticed, and rewriting pushed
history to add a trailer is worse than the omission.

## Sources

- `/home/li/primary/Vision/datom.md` (whole, current: commit `d21ae637e`),
  `/home/li/primary/Vision/protos.md`, `/home/li/primary/Vision/ethos.md:133`,
  `/home/li/primary/Intent/conversion.md`, `/home/li/primary/Intent/context.md`,
  `/home/li/primary/Intent/anatomy.md` — read.
- `/home/li/primary/flows/f6db8d/reports/substrate-audit.md` §1.3–§1.10, §2.2,
  §3.1–§3.3 — the defects fixed here; relayed, then re-witnessed by the tests
  named above.
- `/home/li/primary/flows/fe34eb/vision/datom.md`,
  `/home/li/primary/flows/564f55/vision/datom.md` — raw psyche, read for the
  bare-string question; neither reopens it.
- Witnessed by this flow: the failing-first run of `tests/composition.rs` at
  `99a9e8c`; the proptest failure at `f2cc068`; a protos probe at
  `b543678` showing `Some..a` and `5::7/128` read as single bare structures;
  the gate above.

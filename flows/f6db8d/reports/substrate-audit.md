# Substrate audit — protos 0.29.1, datom-codec 0.25.6, ethos-zero 6.1.6

Flow f6db8d, audit subflow. Slice: the substrate released by flow 857335.

- protos 0.29.1 at `b543678cfc8609529cea7174eb4af8a64daa54ad`
- datom-codec 0.25.6 at `f2cc06858d38a4028c928d33323a6d682e7c222f` (including `crates/datom-codec-derive`)
- ethos-zero 6.1.6 at `4695ee0c1f5d00dcf5cceba08f5fa00412b92184`

Method: scratch clones of all three at those exact revisions under
`flows/f6db8d/witnesses/substrate/`, four purpose-written probe crates
(`probe/`, `probe2/`, `probe3/`, `probe4/`) built against the clones with a
cargo `[patch]` pinning protos to the local clone so both crates share one
protos, plus each repository's own `cargo test --offline`. Every probe
transcript is in `flows/f6db8d/witnesses/substrate/probes.md`. The
statement-by-statement sweep of `Vision/ethos.md` against ethos-zero (§4) was
delegated within this audit to a read-only agent working in the same clone; its
probe files are at `flows/f6db8d/witnesses/substrate/probe-ethos/` and the three
material defects it reports were re-verified by this flow directly. Nothing was
edited, committed, locked, built with Nix, or deployed; the clones and probes
are scratch.

Claims below are marked **witnessed** (this flow ran it and saw the output),
**read** (this flow read the source and cites it), or **relayed** (someone else
said it; §4 is relayed except where marked re-verified, §9 is relayed
throughout). Observations, hypotheses and unknowns are kept apart.

---

## 0. The authority moved after it was digested — observation

The brief points at the ten documents digested in
`flows/857335/witnesses/skeptical-audit-authority.json`. Re-hashing them
(witnessed) shows **four of the ten no longer match**:

| document | digest |
|---|---|
| `Vision/protos.md` | matches |
| `Vision/datom.md` | **differs** |
| `Vision/ethos.md` | **differs** |
| `Vision/signal.md` | **differs** |
| `Vision/sema.md` | matches |
| `Vision/nexus.md` | **differs** |
| `Intent/anatomy.md`, `conversion.md`, `context.md`, `mandatoryTraits.md` | match |

Cause (read): commit `6c4e16fcf` "Land the distilled-vision edits approved in
flow fe34eb", 2026-09-10, after 857335 wrote the digest. It changed ethos from
two roots to three (Library, Signal, **Sema**), renamed Signal's
"Universal signal" to Protocol, named datom's bare string form, and retired
`Vision/ethosMonolith.md`.

**This audit is therefore against the current `Vision/`, not the digested
snapshot**, and says so wherever the two differ. The release's own claim of
closure was measured against an authority that has since moved.

---

## 1. Defects — witnessed

### 1.1 A guillemet string containing a backslash cannot survive being written

**Severity: the most serious finding. It silently corrupts data on the wire.**

`« »` is now the string delimiter (`Vision/protos.md` "String, escape, error";
`Vision/datom.md` "Strings"). The reader treats `\` as an escape
(`protos/src/core.rs:259-271`): `\»` yields `»`, and `\X` for any other X
yields `\X` — the backslash is preserved. The **writer**
(`protos/src/core.rs:537-543`) escapes only `»` and emits every backslash raw.
The parentheses writer, twenty lines below (`core.rs:545-564`), *does* escape
backslashes correctly. The guillemet branch is missing that logic.

Witnessed, `probe3`, 300 000 structurally built opaque leaves per boundary over
an alphabet including `\`, `«`, `»`, `(`, `)`:

```
built opaque leaves: 600000 trials
  guillemets   round-trip failures: 27657
    "\\"     -> "«\\»"       (reparse: Unclosed('«'))
    "\\»x"   -> "«\\\\»x»"   (reparse: Multiple)
    " {{\\"  -> "« {{\\»"    (reparse: Unclosed('«'))
  parentheses  round-trip failures: 0
```

9.2 % of built guillemet strings fail; parentheses, sharing the same writer
function, fail zero times in 300 000. That asymmetry is the proof that this is
an omission, not a design choice.

This reaches real data. `Datomizable for String`
(`datom-codec/src/composition.rs:142-155`) routes any Rust `String` containing
whitespace or a delimiter into `Form::String`, hence into guillemets. So **any
`String` value that contains both a space (or delimiter) and a backslash is
written as text that will not read back.** Witnessed end-to-end through the
full datom ascent and descent (`probe`, P2):

```
"a b\"   -> «a b\»    -> ERR Structural(Unclosed('«'))   *** FAILED ***
"a\»b"   -> «a\\»b»   -> ERR Structural(Multiple)        *** FAILED ***
```

Windows paths, regexes, LaTeX, escaped JSON, shell fragments — all ordinary
payloads — are in this class. `Vision/protos.md` states the escape rule exists
"so the ascent never refuses"; the ascent indeed does not refuse, it emits text
the descent then rejects, which is worse than refusing.

**Why the test suite missed it, and why that matters more than the bug.**
Every backslash test in protos starts from text and goes
text → parse → print (`protos/tests/protos.rs:81,94,113,121`). None goes
build → print → parse, which is the direction the datom ascent actually uses.
The test that *would* have caught it exists, and is dead: `tests/textualization.rs:206`
holds

```rust
proptest! {
    #[test]
    fn any_quoted_text_round_trips(content in "[^”]*") {
        let form = opaque(Boundary::CurlyQuotes, &content);
        let text = form.textualize();
        ... prop_assert_eq!(back, form);
    }
}
```

— a build → print → parse property over arbitrary content, written for the old
`CurlyQuotes` boundary. When curly quotes were replaced by guillemets as the
string delimiter, this property was **orphaned instead of migrated** (see 1.2).
Its sibling `any_meaning_text_round_trips`, for parentheses, is the reason the
parentheses writer is correct. This is precisely the failure mode Spirit names:
an older shape left behind rather than replaced, and it produced a shipped
defect.

### 1.2 Four of protos's five committed test files are never compiled or run

`protos/Cargo.toml` sets `autotests = false` and declares exactly one test
target, `tests/protos.rs`. Committed alongside it (`git ls-files tests/`) are
`delineation.rs` (18 tests, 410 lines), `textualization.rs` (11 tests, 226
lines), `deep.rs` (1 test), and `scale.rs` (127 lines of size probes). **None
of them is built.** `cargo test` runs 18 tests; the repository contains 48 test
functions.

Witnessed: flipping `autotests` to `true` and running `cargo test --no-run`
gives compile errors, not failures — the orphans reference `Protoform`,
`Delineation`, `Situated`, `Situation`, `Fault`, `Refusal`, `Locating`, `Word`,
`Text`, `Boundary::CurlyQuotes`, all removed from the public API. They have not
compiled for some time and nothing reports it.

`proptest = "1.6"` is a declared dev-dependency of protos used only by an
orphan, and a declared dev-dependency of datom-codec used by nothing at all.

### 1.3 Derived enums bypass the composition budget entirely

`datom-codec-derive/src/lib.rs:64` — the `Form::Bare(head)` arm of a derived
enum's `compose` matches the variant name and returns without ever calling
`budget.spend`. Every other composition path spends.

Witnessed (`probe2`, Q2): 10 000 bare variants composed successfully with
`remaining: 5`, leaving 4; 10 000 integers with the same budget correctly fail
with `Budget`.

```
10000 bare variants, budget.remaining = 5 -> Ok(10000);  budget left: 4
10000 integers,      budget.remaining = 5 -> Err(Budget)
```

The protos `ReaderBudget` still bounds the parse upstream, so this is not an
unbounded hole today; it does mean the composition budget is not the guarantee
it is written to be, and a hand-built `Datom` (no reader involved) has no bound
at all on this path.

### 1.4 The derive is asymmetric on zero-field non-unit variants

`Foo::Bar()` and `Foo::Bar {}` datomize to the bare head `Bar`
(`derive/src/lib.rs:142-143`, keyed on `variant.fields.is_empty()`) but cannot
compose: the compose side keys its bare arms on `matches!(variant.fields,
Fields::Unit)` (`derive/src/lib.rs:33`), so `Bar()` is not in the bare arms,
and its entry in the variant arms is the `count == 0` error arm
(`derive/src/lib.rs:49`). The value can be written and never read back.

Witnessed (`probe2`, Q1):

```
Odd::Empty():  "Empty"  -> *** ERR Variant { expected: "Odd", found: "Empty" }
Odd::Named{}:  "Named"  -> *** ERR Variant { expected: "Odd", found: "Named" }
Odd::Unit:     "Unit"   -> SAME
```

`Vision/datom.md` says "Any Rust type bears the two kinds through a derive in
datom-codec, with no attributes" — `Foo::Bar()` is an ordinary Rust type and is
silently broken rather than rejected at compile time.

### 1.5 The ascent panics

`Vision/protos.md` makes the ascent total. Two public surfaces panic
(witnessed, `probe`, P6):

- `Datomizable for f64` asserts finiteness (`composition.rs:263`):
  `f64::NAN.datomize(...)` aborts the process. A Nexus computing a NaN and
  replying would crash rather than fault.
- `Compositional::from_positions` is `unreachable!()` on `String`, `i64`,
  `f64`, `bool`, `Vec`, `Option`, `Result`, `Meaning`, `Symbol`, `Separator`,
  `Problem`, `Extent`, `ErrorLayer`, `ErrorKind`, `Error`, and on every derived
  enum. It is a **public trait method**; calling it panics. In a crate that
  sets `unsafe_code = "forbid"`, sixteen public methods are landmines.

### 1.6 The error types mislabel their own paths

`Vision/datom.md` — "An error names the layer that raised it and the path of
the datom where it arose; the extent is the protos node at that path" — and
`Intent/context.md` — "no layer carries a fact that belongs to another".

Witnessed (`probe4`, R2), walking each datomized tree and comparing every
node's `path` field with its actual position:

```
Tree::Node (derived):              0 mismatches
protos::Extent (hand-written):     3 mismatches
datom_codec::Error (hand-written): 1 mismatch
```

**The derive is correct; the hand-written impls are wrong.**
`composition.rs:519-529` builds `Extent`'s children at `at.child(0)` /
`at.child(1)` when their real position under the `Extent.` head is
`at.child(1).child(0)` / `at.child(1).child(1)`; `core.rs:377-387` and
`composition.rs:764-773` label the variant body `at` instead of `at.child(1)`.
Two conventions coexist in one file; `protos::Error::datomize` uses the correct
one, `protos::Extent::datomize` does not.

Consequence: `Potential::reader_extent(path)`
(`core.rs:444-448`) resolves a path against the real protos tree
(`ProtosExtenting::at`, `core.rs:112-123`, which descends a `Headed` only at
index 1). A path taken from an `Extent` error datom resolves to the wrong node
or to `None`. The types whose whole job is to report where something went wrong
report the wrong where.

### 1.7 `+4` is accepted as an Integer

`Vision/datom.md`: "An integer is written as bare decimal, 0, 42, -42: ASCII
digits, no leading plus, no leading zero except 0 itself."

`Scalar for i64` (`composition.rs:836-852`) guards leading zeros and `-0`, then
calls `i64::from_str`, which accepts a leading `+`. Witnessed (`probe2`, Q7):

```
"0"   -> Ok(0)
"-0"  -> Err(Value)     "007" -> Err(Value)     "9223372036854775808" -> Err(Value)
"+4"  -> Ok(4)          *** accepted, and re-textualizes as "4"
```

Two texts for one value, in a format whose stated virtue is that the text
carries only the data.

### 1.8 A Meaning is silently accepted and silently destroyed in a String position

`Vision/datom.md`: "Strings are strings and Meaning is Meaning: a position of
type String expects a plain string and nothing else."

`Scalar for String` (`composition.rs:795-807`) accepts `Form::Bare`,
`Form::String` **and `Form::Meaning`**. Witnessed (`probe`, P7):

```
"(a (b) c)" read as String -> "a (b) c" -> retextualized "«a (b) c»"
```

The parentheses are consumed and the value comes back as a different text of a
different type. Vision's postponement clause ("today a parenthesized text lands
as a plain String") authorises the leniency — but `Form::Meaning` and the
`Meaning` type *are* implemented here, so the crate has both the distinction
and the path that defeats it. That is a compatibility path, held open inside a
design that is elsewhere strict. See 3.2.

### 1.9 `#[rustfmt::skip]` guards only the first item of each generated group

`ethos-zero/src/generation.rs:875-878` states the intent — "each generated item
is excluded individually" — and `:925` emits
`#( #[rustfmt::skip] #items )*`. But entries of `items` are `TokenStream`s that
may each hold several Rust items (an enum with inline payloads emits its
`_Data` structs and the enum together), so the attribute lands on the first
item of the group only.

Witnessed by counting the committed generated output:

```
src/ethos-zero.rs            items=8  skips=4
src/error.rs                 items=6  skips=4
tests/generated/nested-collision.rs  items=7  skips=2
tests/generated/tree-types.rs        items=11 skips=8
```

Latent, not active: both the committed text and the freshness comparison come
from prettyplease, so the tests pass. It becomes a failing freshness gate the
first time rustfmt runs over a generated file.

### 1.10 `ARITY` is a required constant that nothing reads

`Vision/datom.md` gives the design explicitly:

```rust
let positions = self.positions(T::ARITY, budget)?;   // this form, as a struct of that arity
```

so that "the reading of the tree, arity, budget, locus, lives in one place and
no type repeats it". The released `Composable for Datom`
(`core.rs:234-241`) does not pass `ARITY`; `DatomPositioning::positions`
(`core.rs:210`) takes a `&'static str` label instead, and arity is checked
incrementally by `position()` / `finish()`.

Witnessed: `grep -rn ARITY src/ crates/ tests/` filtered of declarations
returns **nothing** — the only reference anywhere is `Box`'s
`const ARITY: Integer = T::ARITY;`, itself unread. Every derived type must
declare a constant the machinery never consults, and the declared values are
inconsistent (`String` 0, `Symbol` 1 though it composes as a scalar, `Vec` -1,
every derived enum 1). The arity error it was meant to feed reports
`expected: self.next + 1` (`core.rs:166-168`) — the position it wanted, not the
arity the type declares.

---

## 2. Fidelity — statement by statement

### 2.1 protos against `Vision/protos.md` — largely faithful

Faithful and witnessed or read:

| Vision statement | code |
|---|---|
| Four layers, root type is the `Protos` enum | `core.rs:28-50`; `lib.rs` exports `Protos` |
| Five delimiter pairs; `« »` opaque; curly quotes not delimiters | `Enclosure` {Braced, Bracketed, Angled} `core.rs:14-19`, `Boundary` {Guillemets, Parentheses} `core.rs:20-24`; no curly quote anywhere |
| The map is dropped entirely | no map form exists in protos or datom-codec |
| Structure is headed, enclosed, opaque or bare | `core.rs:28-50` |
| Separators period, exclamation, colon; heads daisy-chain | `core.rs:8-13`, `core.rs:361-378` |
| Angle brackets are a real delimiter | `Enclosure::Angled` |
| Every `Protos` node carries its extent; the budget lives on the reader | `Extent` on all four variants; `ReaderBudget` `core.rs:68-71`, `Reader` `core.rs:163-168` |
| "The word is error, not fault" | `Error` / `Problem` `core.rs:51-66`; no `Fault` in the API |
| The composition carries no position | no positional field on corporate types |
| Canonical print spaces the delimiters | `core.rs:568-588`; witnessed `{a b}` → `{ a b }`, `{ }` → `{}` |

Witnessed additionally (`probe3`): over 48 557 randomly generated accepted
texts, print → reparse → print is a fixpoint with **zero** instabilities, and
`Canonicalizable::canonicalize()` agrees exactly with a fresh parse of the
canonical text in every case. The reader/writer pair is sound in the
text-first direction. The 1.1 defect lives strictly in the build-first
direction.

Departures:

- **`Problem::MissingHead` is unreachable.** Witnessed (`probe`, P3): `.foo`,
  `..`, `a..b`, `.` all parse as `Bare`, none faults. The two sites that could
  raise it (`core.rs:368`, `core.rs:382`) are guarded by conditions that cannot
  hold. This follows from commit `b543678` "Keep invalid separator chains as
  bare structures", which is deliberate; the dead variant left behind is not.
- **The error vocabulary misreports.** `a. b` is a head whose body is missing;
  it is reported as `Multiple` at offset 3 (witnessed, P3). `.{ }` likewise.
- **Angle constraints attach only when a separator follows.** Witnessed
  (`probe`, P4):

  ```
  "Vector<Integer>"             -> parse ERR Multiple
  "[ Scores.Vector<Integer> ]"  -> Headed(Scores,.,Bare "Vector") + Enclosed(Angled,[Integer])
                                   canonical reprint: "[ Scores.Vector <Integer> ]"
  "Foo<Bar>.{ x }"              -> one Headed with constraints  (correct)
  ```

  So `Vector<Integer>` — written as one type throughout `Vision/ethos.md` and
  the ethos skill — is **two sibling structures** at the protos layer, and the
  canonical protos print of an ethos file inserts a space that was not in the
  source. `Vision/protos.md` says angles are "a real protos delimiter" and
  `Vision/ethos.md` says "Angle brackets hold the constraints"; neither
  sanctions the split. See §4 for whether ethos-zero's re-join is exact.

### 2.2 datom-codec against `Vision/datom.md`

Faithful (read, and witnessed by `probe4`/`probe2` round-trips):

- `pub struct Datom { path, form }` and the six-armed `Form` match Vision's
  snippet exactly, including `Form::String` and `Form::Meaning`
  (`core.rs:8-22`).
- Braces are structs, brackets are vectors, a head alone is a bare variant, a
  head with a body is a carrying variant, chained heads nest
  (`composition.rs:70-130`). Witnessed: `Node.{ Leaf.1 Node.{ Leaf.2 Leaf.3 } }`,
  `Ok.Leaf.9`, `Some.[ Left.1 Right.y Neither ]` all round-trip identically.
- `Vector`, `Option`, `Result`, `Box` bear the kinds once, generically;
  `Option`/`Result` read as ordinary variants. `None` is bare, `Some.42`
  carries (`composition.rs:452-495`).
- A single-field variant carries its type's own form; a multi-field variant
  carries an inline struct (`derive/src/lib.rs:137-141`). Witnessed.
- Derive on generic, recursive and Option/Result-shadowing types is correct
  (witnessed, `probe4` R1: `Either<A,B>`, `Tree`, and an enum whose variants
  are literally named `Some`, `None`, `Ok`, `Err` — all round-trip).
- Strings are bare when they contain no space and no delimiter, guillemets
  otherwise; a bare run may carry characters that are syntax elsewhere
  (`composition.rs:142-155`; witnessed `a.b`, `a:b` round-trip bare).
- Integer canonicality on leading zeros and `-0` is enforced; Decimal is
  finite and point-mandatory.
- Errors are datomizable and name their layer.

Departures beyond §1:

- **A decimal is recognised by the structure, not by the position.**
  `Vision/datom.md` states the rule twice: "What a structure means, struct,
  vector, string, integer, variant, is said by the position it sits in, never
  by the structure alone." `Forming::Headed` (`composition.rs:147-155`) merges
  a headed structure into `Form::Bare` when *the head parses as an i64 and the
  body is all ASCII digits* — a content sniff at the datom layer, before any
  type is known. Witnessed (`probe`, P5):

  ```
  "3.14"    -> Bare("3.14")                      (the sniff fires)
  "-0.5"    -> Bare("-0.5")
  "3.14.15" -> Variant("3", Bare("14.15"))       (the sniff half-fires)
  "1.x"     -> Variant("1", Bare("x"))
  ```

  The root cause is the protos separator rule making `3.14` a `Headed`
  structure. The chosen repair guesses; a positional design would let the
  Decimal position re-join, exactly as the String position already does
  (`compose_bare_string`, `composition.rs:171-241`, which *is* Vision-conformant
  and is the correct sibling of this hack).

- **`Datomizable` names two different conversions.** It carries an associated
  `Output` (`core.rs:137-140`) so that `Protos` can implement it as a fallible
  descent (`Output = Result<Datom, Error>`, `composition.rs:132-137`) while a
  corporate value implements it as an infallible ascent (`Output = Datom`).
  `Intent/conversion.md`: "A kind names one conversion and is borne by the type
  that undergoes it." Note that `Vision/protos.md`'s own table assigns
  `Datomizable` to both `Protos` and to a composition, and its snippet gives
  them **different signatures** (`datomize(&self)` vs `datomize(&self, at)`) —
  the Vision statement is not literally implementable as written. See §5.

- **`protos::Error` datomizes under the head `ProtosError`**
  (`composition.rs:769`) while `ErrorKind`'s corresponding variant is named
  `Structural` (`core.rs:93`). Two names for one thing.

- **`Option::compose` accepts a second spelling of `None`**
  (`composition.rs:487`): a `None` variant whose body is an empty bare run, in
  addition to the bare `None` Vision prescribes. That text cannot be produced
  by protos (`None.` is a `MissingBody` fault) nor by the writer, so the branch
  is unreachable — a redundant acceptance in a format whose claim is one text
  per value.

- **Duplicated machinery.** `projection.rs:19-84` reimplements canonical byte
  lengths that `protos::Canonicalizable::canonicalize` (`protos/src/core.rs:616-707`)
  already computes, keyed by a `HashMap<usize, usize>` of raw pointer addresses
  (`projection.rs:36`). The two agree today (verified by inspection of both
  formulas); nothing keeps them agreeing.

### 2.3 Intent

- **`Intent/mandatoryTraits.md` — every method call lives under a trait.**
  Witnessed: all three repositories' `src/` trees pass both of ethos-zero's
  greps (no module-level free functions, no inherent impl blocks). But only
  ethos-zero *runs* those checks (`ethos-zero/checks/no-free-functions.sh`,
  `no-inherent-methods.sh`); protos and datom-codec have no such check, and the
  check's scope is `$src/src`, so `datom-codec/crates/datom-codec-derive/src`
  — which has three module-level free functions, two of them forced by Rust's
  proc-macro ABI and one (`fields`, `derive/src/lib.rs:5`) not — would be
  exempt even if the check were adopted. The gate exists in one repository of
  three.
- **`Intent/anatomy.md` — "Datom and Ethos Zero are the parts that must be
  solid."** Against that standard, §1.1, §1.3, §1.4, §1.5 and §1.6 all land in
  datom-codec.
- **`Intent/context.md`** — violated by §1.6.
- **`Intent/conversion.md`** — tension at §2.2, `Datomizable`.

---

## 3. Is this the terminal best shape, or a compromise?

Seeking disconfirmation of the flow's claim of closure, five things say the
design is not settled.

### 3.1 The same design point was reversed three days after the release

datom-codec HEAD is **not** the released revision. `f2cc068` (0.25.6, released)
is followed by `9bffbf1`, `0078b24`, `99a9e8c` (0.25.7). The whole behavioural
delta is one line (read, `git diff f2cc068 99a9e8c -- src/composition.rs`):

```rust
 '{' | '}' | '[' | ']' | '<' | '>' | '«' | '»' | '(' | ')' | ';'
+    | '.' | '!' | ':'
```

— every `String` containing a separator is now **quoted**, never bare. The
accompanying test diff rewrites the canonical form of ten values:

```
(".a", ".a")  ->  (".a", "«.a»")
("a:b:c", "a:b:c")  ->  ("a:b:c", "«a:b:c»")
("https://example.org/a", …)  ->  ("«https://example.org/a»")
```

Three consequences.

1. The released 0.25.6 conforms to the current `Vision/datom.md` on this point
   ("a bare run may contain characters that are syntax elsewhere, the colon
   among them"); **0.25.7 contradicts it.** One of the two must be wrong and
   the living has not been asked which.
2. The entire bare-dotted-string machinery in the released crate — the
   `compose_bare_string` variant-chain re-join (`composition.rs:171-241`), the
   commits `199fd17` "Resolve bare dotted strings at typed positions" and
   `f2cc068` "Complete bare String punctuation roundtrips", and protos's own
   `b543678` "Keep invalid separator chains as bare structures" which was made
   *for* it — is abandoned in the writing direction three days later while the
   reader keeps accepting it. A reader accepting a form no writer produces is
   the definition of a compatibility path.
3. **It was shipped as a patch bump.** 0.25.6 → 0.25.7 changed the canonical
   wire text of every string containing `.`, `!` or `:`. That is a breaking
   change under a patch version.

`flows/857335/reports/release-registry.json` pins datom-codec at
`f2cc068` / 0.25.6, and protos 0.29.1 and ethos-zero 6.1.6 both pin that same
revision in their manifests. The registry's picture of the stack was already
stale when this audit began.

### 3.2 Compatibility paths left open

Searching the three `src/` trees and `.ethos` files for
`compat|legacy|backward|deprecat|for now|temporar|transitional|fallback|TODO|FIXME|HACK|workaround`
returns **nothing** — the code carries no self-declared debt, which is good
hygiene. The paths that are there are unmarked:

- `Form::Meaning` accepted in a String position (§1.8) — sanctioned by Vision's
  postponement clause, but the crate implements the distinction *and* the path
  that defeats it.
- `Option`'s second `None` spelling (§2.2).
- The bare-dotted-string reader after the 0.25.7 writer reversal (§3.1).
- Four non-compiling test files kept in git (§1.2) — the clearest instance of
  an older shape preserved rather than replaced, and the direct cause of §1.1.

### 3.3 The decimal sniff is a compromise, not a terminal shape

§2.2. Structure decides meaning in exactly one place, against a Vision
statement repeated twice, and it is observably wrong on `3.14.15` and `1.x`.

### 3.4 The angle-bracket split is a compromise

§2.1. `Vector<Integer>` is one type in Vision and two structures in protos.
Whatever re-joins them is a layer doing the layer below's job.

### 3.5 `ARITY` is Vision's design, half-built

§1.10. Vision states the mechanism; the code declares the constant, does not
build the mechanism, and consults the constant nowhere.

---

## 4. ethos-zero against `Vision/ethos.md`

A statement-by-statement sweep of `Vision/ethos.md` against ethos-zero's source
was delegated within this audit; its findings are relayed here and the three
material defects were re-verified by this flow directly. Its probe files are at
`flows/f6db8d/witnesses/substrate/probe-ethos/`.

### 4.1 What is faithful

Every one of these is implemented, with the cited site:

| Vision statement | site |
|---|---|
| Three roots, Library/Signal/Sema, nothing else | `src/lib.rs:154-162`, `:604-623`; retired roots fault `Problem::Root` at `src/conception.rs:84-89` |
| No version in a file | implemented by absence; a `Version.1` header is refused as a protos `Multiple` |
| Section order and count — Library 4, Signal 4, Sema 2 | `src/conception.rs:243-256`, `:257-276`, `:277-288`; wrong count → arity fault `:100-105` |
| Sweet form converted mechanically **before** the ethos reader runs | `src/actualization.rs:13-27`; the conversion is a pure text splice, `src/canonicalization.rs:14-68`; a braced file passes through unchanged `:33,:64-67`; extents mapped back across the seam so faults point at the authored text `:76-98` |
| Imports `source:Name` and `source:[ A B ]` | `src/conception.rs:315-333` |
| Field naming: snake case; constructed type-first; repeated as first/second | `src/generation.rs:367-385`, `:387-393`, `:421-444` |
| Inline payloads get `_Data`, recursively, ancestry after the first level | `src/generation.rs:463-477` — the ancestry prefix is added only when the enclosing identity already ends `_Data` |
| A variant named as a defined type carries that type | `src/generation.rs:482-490` |
| Every struct and enum derives the datom kinds; aliases do not | `src/generation.rs:557-570`, `:587`, `:605`; aliases bare at `:649-659` |
| Signal derives behind `#[cfg_attr(feature = "datom", …)]` | `src/generation.rs:561-562`, selected at `:633`,`:646`; proven by `tests/signal_without_datom.rs`, which compiles a generated signal crate with no datom-codec dependency |
| Receivers `.` self, `!` mut self, `:` no self | `src/conception.rs:430-438`, lowered `src/generation.rs:729-733` |
| Capability inputs bracket + yield bracket holding exactly one type | `src/conception.rs:503-525`; the one-type rule enforced at `:494-496`, `:518-520` |
| Complex kind: superkinds / associated types / **constants as `[ NAME.Type ]`** / capabilities | `src/conception.rs:553-565`; constants `:459-475`, uppercase enforced `src/checking.rs:1060-1065` |
| Kind identity is name plus constraints; constraints are kinds, never types | `src/conception.rs:542-545`, `:421-429`; lowered `src/generation.rs:202-231`; `Role::Kind` enforced `src/checking.rs:545-560`; a data declaration with constraints refused `:929-934` |
| Associations: name, dot, bracket of kinds; compile-time assertion, body hand-written | `src/conception.rs:568-590`; assertion `src/generation.rs:851-856` |
| Signal/Sema associations implied and never written | no associations section exists for them, `src/conception.rs:269-274`, `:283-286` |
| Canonical spacing | inherited, not reimplemented: `src/protosization.rs:342-355` delegates to the protos writer |

This is a high rate of fidelity, and the harder statements — the mechanical
sweet-form conversion with extent remapping, the `_Data` ancestry rule, the
datom-free Nexus build — are the ones done well.

### 4.2 Defects

**(a) A Signal declaring a type named `Query` emits invalid Rust, silently.**
Generation emits `pub enum Query` (`src/generation.rs:896-902`, per ethos.md
276, 306) but the duplicate table and reserved-name check seed **`Request`**,
not `Query` (`src/checking.rs:119-123`, `:480-489`). Re-verified directly by
this flow: the probe Signal declaring `Query.{ String }` generates a file
containing both `pub struct Query` (line 26) and `pub enum Query` (line 35).
Nothing rejects it; the failure surfaces as a `rustc` error in a downstream
crate. The reserved-name check and the generator disagree about the name of the
type the generator makes.

**(b) Sema cannot declare a record type named `Record`, against Vision.**
`Sema::check` reserves `Record` (`src/checking.rs:504-507`) although generation
emits no `Record` type for Sema at all (`src/generation.rs:917-921`). The probe
`Sema [] [ Record.{ String Integer } ]` is refused with
`Conceptual.{ [ 1 2 0 0 ] Duplicate.Record }`. `Vision/sema.md` names Sema's
second section "record types" and reserves nothing.

This is untested in the repository: the only sema fixture,
`fixtures/entry-sema.ethos`, is written under the **Library** root despite its
comment, and the Sema test at `src/lib.rs:837-850` only actualizes, never
generates — so the Sema generation path has no coverage.

**(c) `Self` in a struct position panics the process.** `Self` is a Vision
intrinsic (ethos.md:133) and checking accepts it in a type role
(`src/checking.rs:579`), but the derived field name is `self`, which cannot be a
raw identifier, and `Ident::new_raw` aborts at `src/generation.rs:438`:
`` `r#self` cannot be a raw identifier ``. A whole-file fault is owed; a panic
is delivered. Third panic path in the substrate, after §1.5's two.

**(d) The printer emits a shape the reader cannot read.** A sourced generic
`external:Vector<String>` in a struct position is refused
(`Expected.Reference`), yet `src/protosization.rs:65-75` prints exactly that
shape. Not a Vision violation — Vision never writes the form — but the ascent
and descent of ethos-zero's own printer disagree.

**(e) Off-by-one in fault paths for bounded associated types.** In
`AssociatedTypes`, `index += 1` at `src/conception.rs:229` precedes the
`.place(…)` calls at `:230` and `:235`.

**(f) §1.9's `#[rustfmt::skip]` grouping** — independently reproduced by the
sweep (`tests/generated/tree-types.rs`: `B_Data` and `Nested` unguarded inside
`pub enum Tree`'s token stream, `src/generation.rs:612-616`).

### 4.3 Emitted or accepted beyond what Vision sanctions

- **`Sized` is a tenth intrinsic** (`src/lib.rs:409-410`, `:647`, `:652-672`;
  `src/checking.rs:567-582`). Vision lists exactly nine.
- **Unconditional `Clone, Debug, PartialEq`** on every generated type
  (`src/generation.rs:566`), and on Signal additionally an unconditional
  `#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, …)]`
  (`src/generation.rs:561`). rkyv appears nowhere in `Vision/ethos.md`;
  `Vision/signal.md` names rkyv as the wire form, so the intent is traceable,
  but the derive set is unstated.
- **`where Self: Sized`** added to any capability mentioning `Self`
  (`src/generation.rs:751-755`, `:762-782`). Vision's expected Rust for
  `create:[ Self ]` is plain `fn create() -> Self;` (ethos.md:360).
- **An import-rename form `std:Clonable.Clone`** (`src/lib.rs:209-216`,
  `src/conception.rs:293-306`), used by `fixtures/processable-kinds.ethos`.
  Vision's Imports section describes only two forms.
- **Hardcoded `std` rewrites** for `Clone` and `Send`
  (`src/generation.rs:141-148`).
- **`TYPE_DECLARATION_LIMIT = 512`** (`src/checking.rs:23`, `:464-466`), a
  budget Vision does not state.
- **A tenth-ordinal fallback** — repeated types run `first`…`tenth`, then
  `position_11_string`.
- **`#![allow(dead_code, non_camel_case_types, non_snake_case)]`**
  (`src/generation.rs:924`).
- **A whole boxing rule** (`src/generation.rs:238-356`) emitting
  `std::boxed::Box<…>` for recursion. Vision says nothing about indirection —
  reasonable and necessary, but unstated.
- **One qualification leak**: the boxing path re-emits the container by its bare
  ethos name (`src/generation.rs:336`), so `Option<Integer>` in a
  recursion-capable position becomes `Option<i64>` rather than
  `std::option::Option<i64>`. Visible side by side in
  `tests/generated/tree-types.rs`. It compiles only because `Option` is in the
  prelude — against Vision's "the generated code carries no `use` statements;
  each imported name is written fully qualified".
- **`Vector <String>` with a space is accepted** as one reference — see 4.4.

### 4.4 `Vector<Integer>` — how the split is repaired, and at what cost

Following §2.1: `Vector<Integer>` unfollowed by a separator is two protos
siblings. ethos-zero repairs this with **four separate adjacency scanners**,
one per list context — type/argument lists `src/conception.rs:128-153`,
declaration lists `:157-181`, variant lists `:185-208`, associated-type lists
`:212-242` — each a loop that peeks at `index + 1` for an `Enclosure::Angled`
sibling and consumes two nodes as one.

The re-join is structurally exact for everything Vision's examples contain and
it recurses, so `Vector<Option<Result<String Integer>>>` reads correctly. Three
inexactnesses: it keys on adjacency of shapes, not on absence of whitespace, so
`Vector <String>` is silently accepted; it does not cover `Headed(Colon)` +
Angled, which is defect 4.2(d); and 4.2(e).

**A canonical reprint does not reproduce the source.** `LockPaths.Vector<LockPath>`
reprints as `LockPaths.Vector <LockPath>` — **with a space** — and this is
unavoidable under the current design: `reference_nodes`
(`src/protosization.rs:73-74`) pushes the name and the Angled enclosure as two
*siblings*, and the protos writer puts exactly one space between siblings. The
reprint therefore cannot produce Vision's own spelling (`Vector<String>`,
ethos.md 160, 213, 238, 349). Comments are dropped and the file collapses to one
line.

The round trip is **concept-exact and text-lossy**: reading the reprint yields a
`File` equal to the original (`src/lib.rs:819-835`, `:934-955`, both passing),
precisely because the space-blind re-join accepts the spaced form back. The
text-losslessness is bought by the same laxness that is defect-adjacent.

`src/protosization.rs:33-35` records that the alternative was considered and
rejected — "emitting a headed `Item<...>.` invents a separator and cannot be
read back". That comment is the clearest statement in the whole substrate that
this is a **compromise forced from below**: either protos gains an unseparated
qualified head, or ethos owns its own writer instead of delegating to the protos
one. Neither was done; the space in the canonical print is the residue.

One place where the code is arguably righter than Vision:
`Processable<[Clonable Sendable] Serializable>` reprints as
`Processable<[ Clonable Sendable ] Serializable>`, which obeys ethos.md:424-428
("a space inside every bracket at both ends when non-empty") where Vision's own
examples at ethos.md:63-64 and :80 do not. Worth putting to the living as a
Vision correction rather than a code one.

## 5. The instructions given to agents describe a design that no longer exists

Not in the audited slice, but it is the highest-leverage thing found, and it
bears directly on whether this substrate can be built on.

The `protos`, `datom` and `ethos` skills — loaded by every agent before
touching this substrate, including by this audit — describe the
**pre-distillation** design:

| skill says | Vision and the released code say |
|---|---|
| six delimiter pairs | five |
| `« »` is a map, key value by position | `« »` is the opaque string delimiter |
| `“ ”` curly quotes are the string | curly quotes are not delimiters at all |
| `Name.« K V »` is a map alias; `Roles.« Text Integer »` → `BTreeMap` | "The key-value map … is dropped entirely from protos and its dialects" |
| `Protoform`, `Delineation`, `Structural`, `Conceptual`, `Corporal`, `Actualizable`, `Embodied`, `Fault` | `Protos`, `Protosizable`, `Textualizable`, `Datomizable`, `Composable`, `Compositional`, `Error` |
| `Datomic::incorporate` | `Compositional::from_positions` |
| the text type is `Text` | the text type is `String` |
| ethos has **two** roots, Library and Signal | **three**: Library, Signal, Sema |
| constants as `« CAPACITY Integer »` | `[ CAPACITY.Integer ]` |
| `Library.{ 0 1 0 }` — a version in the file | "An ethos file carries no version" |

This is not a generation lag: the authored sources in
`/git/github.com/LiGoldragon/Curriculum/skills/{protos,datom,ethos}.md` were
last touched **2026-09-04**, while `Vision/protos.md` changed 2026-09-09 and
`Vision/{datom,ethos,signal,nexus}.md` on 2026-09-10. The generated
`.claude/` and `.agents/` trees faithfully carry the stale authored text; the
`.codex/` and `.pi/` trees carry no dialect skills at all.

An agent following the protos skill will write `Boundary::CurlyQuotes` and
`Protoform` and will not compile; an agent following the datom skill will emit
guillemet maps into a dialect that has no map; an agent following the ethos
skill will write a version header into a file format that forbids one. The
substrate is released and the instructions for using it are five days behind
it.

---

## 6. Green gates — reproducible

Witnessed, `cargo test --offline` at each pinned revision, everything green:

| repository | tests | result |
|---|---|---|
| protos 0.29.1 | 18 | all pass |
| datom-codec 0.25.6 | 31 | all pass |
| ethos-zero 6.1.6 | 42 (17 + 7 + 5 + 3 + 8 + 2) | all pass |

The green-gate claims **are** reproducible locally. Three qualifications:
protos's 18 is of 48 committed test functions, the other 30 being unbuildable
(§1.2); nothing in any of the three suites exercises the build → print → parse
direction that §1.1 breaks; and ethos-zero's Sema **generation** path is
uncovered — the only sema fixture is written under the Library root and the
Sema test only actualizes (§4.2(b)), which is why §4.2(b) survived the gate.

Not attempted: Nix builds, per the brief's prohibition. Nix-only checks
(`ethos-zero/checks/*.sh`, `protos|datom-codec/checks/generated-contract.sh`)
were read and their grep bodies run by hand against the clones (§2.3); the
freshness tests, which are the substance of the contract check, run inside
`cargo test` and pass.

---

## 7. Hypotheses — not established

- The guillemet writer's missing backslash branch (§1.1) was most likely lost in
  the curly-quote → guillemet migration: the parentheses writer, whose property
  test survived, is correct, and the guillemet reader, which was written fresh,
  is correct. Only the writer, which inherited the escape-free curly-quote
  behaviour, is not. **Unverified** — the commit history was not bisected.
- `#[rustfmt::skip]` being emitted per group rather than per item (§1.9) is
  most likely an unnoticed consequence of `items` holding multi-item
  `TokenStream`s, not an intent. The comment at `generation.rs:875-878` states
  the per-item intent, which is evidence for this but not proof.
- The 0.25.7 reversal (§3.1) reads as a response to a concrete failure — the
  test it adds is `option_string_with_protos_separators_round_trips` with the
  value `"5::7/128"`, which looks like a real address or path from a consumer.
  **Unverified**; the flow that made it was not traced.

## 8. Unknowns — left unknown

- **Which of 0.25.6 and 0.25.7 the living wants.** `Vision/datom.md`, last
  edited 2026-09-10, says a bare run may hold a colon; 0.25.7, committed after,
  quotes it. Whether the Vision statement is superseded, or the code diverged,
  cannot be told from the records. **This needs the living.**
- **Whether `Datomizable` is meant to name two conversions.**
  `Vision/protos.md`'s own table and snippet are internally inconsistent on
  this (§2.2). The code's associated-`Output` resolution is reasonable and
  unsanctioned. **This needs the living.**
- **Whether `Vector<Integer>` splitting into two protos structures is accepted
  or unnoticed.** No psyche record was found either way; searches covered
  `Vision/`, `vision-raw/` and `flows/*/vision/`. The consequence — that a
  canonical ethos reprint writes `Vector <LockPath>` with a space, and so cannot
  reproduce Vision's own spelling (§4.4) — needs a ruling: either protos gains
  an unseparated qualified head, or ethos stops delegating its writer.
- **Whether `Sized` is meant to be a tenth intrinsic**, and whether the
  unconditional rkyv, `Clone/Debug/PartialEq` and `where Self: Sized` emissions
  are wanted (§4.3). Each is defensible and none is written down.
- **Whether the Signal query enum is named `Query` or `Request`.** The
  generator says `Query`, the reserved-name check says `Request`, and
  `Vision/ethos.md` says `Query` while the ethos skill says `Request` (§4.2(a),
  §5). This one is a live defect either way.
- Why `Generation_Error` is hand-authored with the derived-name marker.
- Whether the protos orphan tests were knowingly parked or simply forgotten.

## 9. Agreement with the two interrupted audits

Both prior audits (`flows/857335/reports/skeptical-{opus,sol}.md`) are
interruption records, not verdicts: both were killed before any report existed.
These were read only after the findings above were formed.

`skeptical-opus.stdout` contains a single result line — an aborted stream, no
findings.

`skeptical-sol.stdout` contains six agent messages before abort. Three of its
partial findings **agree independently** with this audit:

1. "Protos disables automatic tests and registers only `tests/protos.rs`; four
   substantial test files are present but never built" — §1.2, agreement.
   Sol treated them as non-evidence; this audit additionally witnessed that
   they no longer compile and identified the orphaned property test as the
   direct cause of §1.1.
2. "Derived unit enum variants bypass the composition budget entirely" — §1.3,
   agreement. Sol had it source-demonstrated only; witnessed here.
3. "`Decimal` ascent can panic for non-finite `f64`, contradicting the total
   ascent contract" — §1.5, agreement. Witnessed here.

Sol was then blocked: "The managed filesystem is enforcing read-only access
even inside the authorized witness directory, so no new scratch or Cargo target
could be created." That constraint did not apply to this run, which is why the
behavioural probes exist.

Sol also recorded a **disagreement** worth surfacing: "The loaded domain skill
text reflects a newer vocabulary than the ten appended authorities in places,
so I will not treat it as the audit standard." This audit finds the opposite
direction (§5) — the skills are *older* than `Vision/`, by five days at the
authored source. The likely reconciliation is that Sol compared the skills
against the **digested snapshot** of the ten documents, which had itself gone
stale (§0), rather than against current `Vision/`. Either way the conclusion is
the same: the skills and the Vision disagree, and the Vision governs.

No prior finding was contradicted.

---

## 10. Verdict

The substrate is **coherent, well-shaped, and defective in ways that would bite
in production**.

What is genuinely good, and should be said plainly: the layer separation is
real and holds; the `Protos` enum, the extent-on-every-node discipline and the
budget-on-the-reader discipline are faithfully built; the print/reparse fixpoint
holds over 48 557 generated texts with zero instabilities; the derive is correct
on generic, recursive and name-shadowing types where the hand-written impls are
not; the three-root ethos Vision landed on 2026-09-10 is already implemented;
the datom-free Nexus build is real and tested; and all three suites are green
and reproducible.

Against closure, in order of severity:

- **§1.1 is a shipping data-corruption defect.** Any string carrying both a
  delimiter and a backslash is written as text that will not read back, at a
  measured 9.2 % of built guillemet strings. It must be fixed before anything
  depends on this substrate.
- **§1.2 is why §1.1 shipped**, and §1.2 is itself an instance of the compromise
  Spirit forbids: an older shape kept instead of replaced. The property test
  that would have caught §1.1 is one of the thirty dead tests.
- **§4.2(a) makes ethos-zero emit invalid Rust silently** for any Signal that
  declares a type named `Query`, because the generator and the reserved-name
  check disagree about which name the generator uses.
- §1.3, §1.4, §1.5, §1.6, §4.2(b) and §4.2(c) are each independently sufficient
  to say the substrate is not finished. Three of them are panics on public
  surfaces in crates that forbid unsafe code.
- **§3.1 shows the design was still moving after the release was declared**, in
  a direction that contradicts the Vision distilled the day before, under a
  patch version bump, leaving a reader that accepts a form no writer produces.
- **§5 means the substrate cannot currently be built on correctly by any agent
  following its own skills.**

This is not the terminal best shape. It is a good shape carrying four unmarked
compatibility paths, one dead half-built Vision mechanism (`ARITY`), two places
where a layer does the work of the layer below (the decimal sniff, the four
angle-bracket re-join scanners), a canonical print that cannot reproduce the
notation Vision writes, and a documentation layer pointing at a design that was
abandoned five days before the release.

The most telling single line in the whole substrate is the comment at
`ethos-zero/src/protosization.rs:33-35`, recording that the right shape was
considered and could not be printed because protos would not read it back. That
is a compromise forced from below and consciously accepted — the clearest
evidence that the substrate is best-so-far, not terminal.

Four questions are for the living and cannot be settled from the records: which
of 0.25.6 and 0.25.7 is wanted for bare strings; whether `Datomizable` is meant
to name two conversions; whether the ethos canonical print is allowed to differ
from the notation Vision writes; and whether the Signal query enum is `Query` or
`Request`.

## Sources

- Authority: `/home/li/primary/Vision/{protos,datom,ethos,signal,sema,nexus}.md`,
  `/home/li/primary/Intent/{anatomy,conversion,context,mandatoryTraits}.md`,
  re-hashed against `flows/857335/witnesses/skeptical-audit-authority.json`
  (four mismatches, §0).
- Raw psyche read for context: `flows/564f55/vision/{datom,ethos,designPractice,archive-*}.md`,
  `flows/564f55/notion/datom.md` (a notion; rules nothing, and nothing here rests on it).
- Code, at the three pinned revisions, in scratch clones under
  `flows/f6db8d/witnesses/substrate/{protos,datom-codec,ethos-zero}/`.
- Probe transcripts and test-suite results: `flows/f6db8d/witnesses/substrate/probes.md`;
  probe crates `probe/`, `probe2/`, `probe3/`, `probe4/` in the same directory.
- Delegated ethos sweep (§4): probe files and generated output at
  `flows/f6db8d/witnesses/substrate/probe-ethos/`, reprint harness at
  `probe-ethos/reprint/`. §4.2(a), (b) and (c) re-verified directly by this flow.
- Upstream history beyond the release: `/git/github.com/LiGoldragon/datom-codec`
  commits `f2cc068..99a9e8c`.
- Skill drift: `/git/github.com/LiGoldragon/Curriculum/skills/{protos,datom,ethos}.md`
  and the generated `.claude/`, `.agents/`, `.codex/`, `.pi/` trees.
- Prior audits, read after findings were formed:
  `flows/857335/reports/skeptical-{opus,sol}.md`,
  `flows/857335/witnesses/skeptical-{opus,sol}.stdout`,
  `flows/857335/reports/release-registry.json`.

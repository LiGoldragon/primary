# Substrate review — protos 0.30.0, datom-codec 0.26.1, ethos-zero 7.0.1

Read-only subflow of main flow f6db8d. No repository was edited, committed,
locked, Nix-built or deployed. Everything below was formed first from the code
and the diffs against `b543678c`, `f2cc0685` and `4695ee0c`; the four fix
reports were read only afterwards, and the comparison is §6.

Claims are marked **witnessed** (this flow ran it and saw the output here) or
**relayed** (read from a fix report, not re-run here). Probe sources are in
`flows/f6db8d/witnesses/substrate-review/`; scratch clones at the three
released revisions were built under this session's scratchpad.

---

## 1. Observations — witnessed

### 1.1 The three gates reproduce green

Scratch clones at `e8701521`, `18129314`, `212b3590`, `cargo test` on each:

| repo | targets | result |
|---|---|---|
| protos | `protos` 18, `delineation` 15, `deep` 4, `textualization` 12, `scale` 6 probes | all pass |
| datom-codec | `composition` 9, `core` 32 | all pass |
| ethos-zero | lib 17, `cli` 7, `ethos` 11, `freshness` 3, `generated` 9, `signal_without_datom` 2 | all pass |

Nix checks were not run (the brief forbids Nix builds); those gates are
**relayed** from the fix reports.

### 1.2 Every fix does what its report claims

I traced each claim into the diff and, where it is a behavioural claim,
into a probe of my own. All hold:

- The escape rule is one rule, stated once on `Escaping for Boundary`
  (`protos/src/core.rs`), read by the reader's single `\\` branch and written by
  `print_opaque`, which `Canonicalizable` also calls to measure an opaque leaf —
  so the writer and the measurer cannot drift. `escapes()` is
  `['\\', '»']` / `['\\', '(', ')']`; `forced()` is every `»` for guillemets and
  only the unbalanced parentheses for parentheses, matching the stated rule
  exactly.
- `Clone`, `PartialEq` and `Debug` are iterative. Witnessed on a **200 000-deep**
  built tree: clone, compare, `{:?}` and `{:#?}` all complete without a stack
  overflow. `Clone`'s stack order is correct — the `Headed` step pops the body
  before the constraints, matching the order they were pushed.
- datom-codec's `ARITY`/`from_positions` are gone from the trait and from every
  impl; `unreachable!()` in `src/` + `crates/` goes **19 → 2**.
- Every datomized node carries the path it sits at. Witnessed independently of
  the crate's own test, by walking `protos::Error`, a multi-field variant and a
  Sema-shaped record and comparing each node's `path` with its position:
  no disagreement.
- ethos-zero's `Query` rename is a rename of the *check*, not the generator —
  `Name::try_from("Query")` in `generation.rs` is unchanged across the diff, so
  the fix made the reservation agree with what was already emitted.
- Sema's `Checkable` gathered declared names from section **2** while checking
  section **1**; both are 1 now, and `fixtures/entry-sema.ethos` moved from a
  `Library` root with four sections to a `Sema` root with two.

### 1.3 My own adversarial probes find no round-trip defect

`witnesses/substrate-review/protos-probe.rs`, `datom-codec-probe.rs`:

| probe | cases | result |
|---|---|---|
| every text over `a . : \ < > { } ( ) « » ; ␠ 1` up to length 3, read then printed | 398 accepted | every one reprints itself up to canonical spacing and comment stripping; the 7 residual differences are all the Vision spacing rule (`{a}` → `{ a }`, `{ }` → `{}`, `< >` → `<>`) |
| `Held { text }` through datomize → protosize → textualize → actualize, `".*"` | 4 096 | all round-trip, backslashes included |
| the same over every string of length ≤ 3 from `a . : ! \ < > « » ( ) ; ␠ { }` | 3 616 | all round-trip |
| finite `f64` through the same chain | 4 096 | all round-trip |
| every variant shape: `Empty`, `Braced {}`, `Parens()`, `One(i64)`, `Two(i64, String)` | 5 | all round-trip |
| a generic `Generic<T> { held, also: Vec<T> }` and a Sema-shaped `Record`/`Entry` pair | 2 | round-trip |
| a `Form::Meaning` at a `String` position | 1 | refuses with `Form { expected: String, found: Meaning }` — the §1.8 removal is a clean refusal, not silence |
| a 100 000-link `Some.` chain under a depth cap of 512 | 1 | refuses, does not recurse |

The backslash was the audited hole and it is closed in both directions.
Note that datom-codec's own property alphabet did gain the backslash at the
repin commit (`tests/composition.rs:252`), closing the TODO its fix report
left open — **witnessed in the source**, and the repin report claims it.

### 1.4 Code size

Rust lines, tracked files, pre → post:

| | src | tests |
|---|---|---|
| protos | 771 → **1 083** (+312) | 1 163 → 1 286 |
| datom-codec | 1 834 → **1 767** (−67) | 971 → 1 256 |
| ethos-zero | 4 411 → **4 436** (+25) | 877 → 987 |

Net source **+270**, essentially all of it `protos/src/traversing.rs` (297
lines). Net tests **+518**. datom-codec is the only one that shrank, and it
shrank while removing 17 dishonest stubs — the clearest win of the night.

---

## 2. The seven decisions against Vision

### Consistent with Vision, quoting the line

**The protos escape rule.** `Vision/protos.md`, "String, escape, error":

> A closing guillemet inside a string is escaped with a backslash, so the
> ascent never refuses.
> ```
> «she said \»no\» and left»
> ```

Minimal escaping reproduces that example byte for byte; universal escaping
would not. The backslash-escapes-itself extension fills a Vision *silence* (no
line forbids it) and is forced by the round trip. `« »` being "opaque, every
glyph content" argues for keeping content as near verbatim as the boundary
allows, which is what minimal escaping does. **Consistent.**

**The bare-string delimiting set.** `Vision/datom.md`, "Syntax":

> In such a position a string is written bare when it contains no space and no
> delimiter … Because the position already knows it holds a string, a bare run
> may contain characters that are syntax elsewhere, the colon among them.

The set added — begins with, ends with, or holds two adjacent `.` `!` `:` — is
not punctuation taste; it is exactly the set protos reads back as something
else. `a:b:c` and `https://example.org/a` stay bare, which is the sentence's
own demand. **Consistent**, and witnessed exhaustively (§1.3).

**Decimal by position.** `Vision/datom.md`, "Syntax":

> What a structure means, struct, vector, string, integer, variant, is said by
> the position it sits in, never by the structure alone.

The removed code sniffed `Form::Bare` digits at the *datom* layer, before any
type was known. **Consistent**, and the removed shape directly contradicted
that line.

**`Query` as the Signal enum.** `Vision/ethos.md`:

> ```rust
> pub enum Query { Lock(LockRequest), Release(LockId) }
> ```
> Head then symbol is a variant of `Query` or `Response` in a Signal's first
> two sections …

and `Vision/signal.md`: "A Signal declares queries and responses". **Consistent.**

**Freeing Sema's `Record`.** `Vision/ethos.md`, "Roots":

> Signal's sections are queries and responses, since there is communication;
> Sema's are record types, the rest to be decided.

`Vision/sema.md` shows `[ Lock.{ … } ]` as the record types and reserves no
name; `Vision/ethos.md` itself uses `Record.{ String Integer }` as an ordinary
*Library* type name twice. **Consistent.**

**`Self` boxing / field naming.** `Vision/ethos.md`:

> Intrinsic names known without import: String, Integer, Decimal, Boolean,
> Meaning, Vector, Option, Result, Self.

Vision sanctions `Self` in a position and says nothing about the field
spelling. Naming the field for the enclosing type is a decision *beyond*
Vision, not against it, and it keeps a construct Vision sanctions where the
audit had proposed refusing the file. **Consistent** (no line to violate).

**Iterative traversal.** No Vision line speaks to it. It follows the crate's
own precedent — `Drop`, printing and canonicalization were already written with
explicit stacks — and the spirit line "when more correctness is introduced …
the gain in correctness more than makes up for the added machinery". **No
conflict**, at a cost of +297 lines (§4.1).

### In conflict with the letter of Vision

**ARITY removal.** This is the one. `Vision/protos.md`:

> ```rust
> impl Compositional for Person { const ARITY: Integer; fn from_positions(p: Positions<'_>) -> Result<Self, Error>; }
> ```

and `Vision/datom.md`, twice:

> ```rust
> let positions = self.positions(T::ARITY, budget)?;   // this form, as a struct of that arity, else an error at this path
> T::from_positions(positions)
> ```
> ```rust
> const ARITY: Integer = 2;
> ```

Both the constant and the capability are named in Vision and both are gone.
I searched `flows/*/vision/`, `flows/*/notion/` and `vision-raw/` for
`from_positions`, `Compositional` and `positions(` — **nothing**. No raw record
supersedes these two files, so they stand as the only authority.

The subflow's argument (its decision 3) is that the surrounding prose is what
Vision wants —

> the reading of the tree, arity, budget, locus, lives in one place and no type
> repeats it

— and that the snippet is not implementable for scalars, containers and enums,
which is true and is why sixteen impls were `unreachable!()`.

**My own reading, offered as this flow's inference, not as a finding:** the new
shape satisfies the letter of that prose sentence less well, not better. Before,
`budget.spend` and `positions(…)` sat once, in the trait's default `compose`.
Now every generated `compose` opens with `budget.spend(&datom.path)?;
datom.positions(#arity)?` — the tree-reading, the arity and the budget are
repeated in every derived impl, just in generated text rather than in the trait.
What was genuinely won is honesty: 19 `unreachable!()` → 2. The subflow says so
itself and names the open question — whether `Compositional` should split into a
positional kind and a scalar kind. **That split is the thing to put to the
living.** Until then the released substrate contradicts two Vision files that
have not been amended.

---

## 3. Regressions, compatibility paths, parallel shapes

I looked for all three and found **no regression and no compatibility path**.
Every removal is a removal, not a fork:

- `Form::Meaning` no longer reads as a `String` — a refusal, witnessed, not a
  fallback.
- `Option::None` spelled as an empty bare body is gone, and the derive no
  longer emits that spelling, so the two sides moved together.
- `Positions::finish` is gone, replaced by an up-front arity check, not
  shadowed by one.
- `autotests = false` is gone rather than kept beside an explicit list.
- ethos-zero's four adjacency scanners became one `Constraining`, and the four
  call sites now differ only in meaning.

**Parallel shapes that remain** are in §4.

---

## 4. Where there could be less code

### 4.1 Six explicit-stack traversals over one enum (protos)

`Drop` (`dropping.rs`), `Clone`, `PartialEq`, `Debug` (`traversing.rs`),
printing and canonicalization (`core.rs`) are six hand-written stack walks over
`Protos`, each with its own step enum. `PrintStep { Form, Text, Glyph, Space }`
and `ShowStep { Form, Text, Owned }` are the *same machine* with a different
leaf rendering; `Debug`'s ~100 lines exist only to reproduce by hand the text
the derive used to emit. One `Stepping` kind over `Protos` — the node's children
and its interleaved text — would carry all six and is the single largest
reduction available in the substrate. This is where the night's +270 source
lines live.

### 4.2 A now-unreachable refusal (datom-codec)

`Positioning::position` still raises its own `ErrorKind::Arity` when a caller
asks past the end, but `DatomPositioning::positions(arity)` validates the exact
count before any position is read, so no in-tree caller can reach it. The fix
report keeps it deliberately (its contradiction 4) as the honest refusal for a
hand-written caller. Noted as the second place less code is available, should
`Positions` ever become constructible only through `positions(arity)`.

### 4.3 `src/projection.rs` still reimplements protos's byte lengths

Keyed by a `HashMap` of raw pointer addresses. Two formulas that agree today
with nothing keeping them agreeing. Disclosed by the fix report (contradiction
3) and untouched; I confirm it is still there.

---

## 5. Defects found

| # | severity | where | what |
|---|---|---|---|
| **D1** | medium | protos `e8701521` | `protos-kinds.ethos` has **no Nix check**, and `generated-contract/protos-kinds.rs` is **not its output at all** — it declares `Serial`, `Classifying` and `crate::Glyph`, names from an older design, while `protos-kinds.ethos` declares `BoundedProtosizable`, `Protosizable`, `Textualizable`, `Canonicalizable`. Dead, misleading committed evidence beside a live declaration. Pre-existing (absent at `b543678c` too), but the sibling datom-codec fix closed precisely this gap in its own repo by adding `generated-kinds-contract`; protos, released the same night, did not, and its report does not mention it. **Witnessed**: `flake.nix` at both revisions contains no `kinds` check; the two files' contents disagree entirely. |
| **D2** | medium | substrate-wide | **Nothing checks the committed contracts against the generator that was just released.** protos and datom-codec pin ethos-zero **6.1.2** (`daf0072…`) for `generated-contract`; ethos-zero's own `dependency-ethos` check only asserts each declaration *generates without error* (`checks/dependency-ethos.sh` — it never compares output). **Witnessed**: building `ethos-zero` 7.0.1 and running it over `protos.ethos`, `protos-kinds.ethos`, `datom-codec.ethos` and `datom-codec-kinds.ethos` produces output differing from every committed contract — 7.0.1 emits `#[rustfmt::skip]` on each item and `Clone, Debug, PartialEq` derives the committed files lack. The gates are green against a generator two majors behind. |
| **D3** | low | ethos-zero `212b3590` | The pinned release uses **"fault"** throughout (`src/lib.rs` ×6, `src/generation.rs`, `error.ethos`, README) against `Vision/protos.md`: "The word is error, not fault, through the chain." The ethos-zero fix *added* a new occurrence — the `Constraining` doc comment, "so a fault still points at the authored position". Corrected only afterwards, on `main` at `da58504` (which is version **8.0.0**, a major the substrate does not pin). **Witnessed** by grep at the released revision. |
| **D4** | low | datom-codec `18129314` | `f64::datomize` of a non-finite value writes `NaN` / `inf` / `-inf`, text no Decimal position will read back. **Witnessed**: `{ NaN }` → `Value { expected: "Decimal", value: "NaN" }`. The writer now accepts what the reader refuses, silently, where it previously panicked loudly. `Vision/datom.md` — "A composition becomes text by the open chain" — implies the text is readable. Disclosed as the fix's decision 4 with the terminal shape named (a finite Decimal type, an ethos-zero change first); recorded here so it is not lost. |
| **D5** | low (quality) | protos | Six parallel stack traversals; `PrintStep` and `ShowStep` are one machine written twice. §4.1. |
| **D6** | low (quality) | datom-codec | `Positioning::position`'s `Arity` refusal is unreachable through every in-tree caller. §4.2. |

**Open for the living, not a defect:** the ARITY removal contradicts two
unamended Vision files (§2). The question the subflow named — splitting
`Compositional` into a positional kind and a scalar kind — is the shape that
would let Vision and the code agree again.

## Hypotheses formed and disconfirmed

Recorded so they are not re-formed:

- *That protos's bare-run delimiting set is asymmetric.* The first pass breaks a
  run on `< > { } [ ] « » ( ) ;` and the second omits `<`. **Disconfirmed**: `<`
  is dispatched inside the loop to the constraints branch, which parses the
  angled enclosure and rewinds if no separator follows. Witnessed: `a<b>.c`
  reads as a constrained head; `{ a<b> }` reads as two siblings and reprints
  `{ a <b> }`, exactly as ethos-zero's `Constraining` comment describes.
- *That `Vector<Integer>` failing at top level is a new breakage.* **Disconfirmed**:
  pre-existing, and both the protos and ethos-zero reports name it openly.

## Unknowns

- Whether the Nix gates all four reports record actually passed. Not re-run
  here (the brief forbids Nix builds); **relayed**, and consistent with the
  `cargo` gates I did reproduce.
- Why the substrate's contract checks were left on ethos-zero 6.1.2 through a
  6 → 7 major bump. The repin report notes the generator pin exists and states
  it was deliberately untouched; it does not say whether the drift was
  considered. Cause unknown — possibly a deliberate bootstrap ordering
  (7.0.1 depends on protos 0.30.0, so its generator cannot also gate it),
  possibly an oversight. Both are live.

---

## 6. Against the fix reports

Read after forming the above. **The four reports are accurate.** I found no
claim overstated and no change beyond what is described. Three things stand out:

- Each report discloses its own worst problem. datom-codec's names the ARITY
  Vision conflict verbatim and says the living may want the constant back;
  ethos-zero's lists five things left standing including the `#[rustfmt::skip]`
  latency that turns out to be the mechanism of **D2**; protos's names
  `Problem::MissingHead` as apparently unreachable and `Vector<Text>` as
  `Multiple`. None of this had to be volunteered.
- The seen-failing-first discipline is real and recorded per test in all three
  fix reports, with the shrunk minimal inputs quoted.
- datom-codec's report notes its commit carries no `Co-Authored-By` trailer and
  why it was not rewritten. Worth the main flow's eye, not mine.

What the reports do **not** carry: D1 (protos's ungated, stale
`protos-kinds` contract) and D2 (the substrate-wide generator-pin drift). Both
sit in the seam between the subflows' slices, which is where one would expect
them.

---

## Sources

- `/home/li/primary/Vision/protos.md`, `datom.md`, `ethos.md`, `signal.md`,
  `sema.md` — read whole; the authority for §2, quoted inline.
- `flows/*/vision/`, `flows/*/notion/`, `vision-raw/` — searched for `arity`,
  `from_positions`, `Compositional`, `positions(`; nothing bears on the trait.
- `/git/github.com/LiGoldragon/{protos,datom-codec,ethos-zero}` — the diffs
  `b543678c..e8701521`, `f2cc0685..18129314`, `4695ee0c..212b3590`, read whole
  for `src/`, `crates/`, `tests/`, `flake.nix`, `Cargo.toml` and the `.ethos`
  declarations; this flow's own reading.
- Scratch clones at the three released revisions under this session's
  scratchpad — `cargo test` on each, the generator built and run over all four
  dependency declarations, and the probes below. This flow's own witnesses.
- `flows/f6db8d/witnesses/substrate-review/protos-probe.rs` and
  `datom-codec-probe.rs` — the probe sources for §1.3, §1.2 and D4.
- `flows/f6db8d/reports/{protos-fix,datom-codec-fix,ethos-zero-fix,substrate-repin}.md`
  — read after §1–§5 were formed; compared in §6. Their Nix gate results are
  relayed, not witnessed here.
- `flows/f6db8d/reports/substrate-audit.md` — the audit that drove the fixes;
  its section numbers are used as the fix reports use them.

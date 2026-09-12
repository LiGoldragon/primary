# Arity: where the reading of a tree lives

Subflow of main flow f6db8d, 2026-09-12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: reintroduce arity where it makes most sense, with `Compositional`
carrying it as the living's ruling leans; decide on ontological grounds whether
`Compositional` splits; implement in datom-codec; cascade to ethos-zero, signal
and every consumer on the final heads.

**Witnessed** means this thread read or ran it. **Relayed** means carried from a
dispatched subflow's report without re-observation.

## 1. The design note

### What was asked of the design

`Vision/protos.md:85` writes the kind on the corporate side as

> ```rust
> impl Compositional for Person { const ARITY: Integer; fn from_positions(p: Positions<'_>) -> Result<Self, Error>; }
> ```

and its kinds table names `Compositional` as the kind that "states its own
positions, so a datom can compose it". `Vision/datom.md:120` gives the
mechanism:

> ```rust
> let positions = self.positions(T::ARITY, budget)?;   // this form, as a struct of that arity, else an error at this path
> T::from_positions(positions)
> ```

and `:141` the derived constant. The sentence those snippets serve is
`Vision/datom.md:113`:

> the reading of the tree, arity, budget, locus, lives in one place and no type
> repeats it.

datom-codec 0.26.x had removed both `ARITY` and `from_positions`
(`reports/datom-codec-fix.md`, decision 3), because the single kind
`Compositional` is borne by scalars, containers and enums as well as by
structs, and for those there is no arity and there are no positions: the
released crate had declared `String` 0, `Symbol` 1, `Vec` −1 and every enum 1,
and sixteen `from_positions` were `unreachable!()`. `reports/substrate-review.md`
§2 recorded that the removal satisfied the letter of the Vision sentence less
well, not better — the tree-reading, the arity and the budget moved out of the
trait's one default and into every derived impl — and named the open question
for the living: **whether `Compositional` splits into a positional kind and a
scalar kind.**

### The decision

`Compositional` splits, but not into a positional kind and a scalar kind. It
splits into **the act and the declaration**, which stand as genus and
differentia, not as two coordinate species:

- **`Composing`** — a type a datom composes into. Borne by everything: the
  scalars, the containers, the enums, and every positional type.
- **`Compositional: Composing`** — a type whose datom form is a struct of
  positions. It carries `const ARITY: Integer` and `fn from_positions(Positions<'_>)`,
  and it reads nothing.
- **`Composable`** on `Datom` — unchanged in name, and now carrying the second
  capability `compose_positions<T: Compositional>`, which *is* the one reading:
  the budget it spends, the arity it demands, the positions it hands out, and
  the path it refuses at. Six lines, in one place.

`Positions<'a>` now carries the `&'a mut Budget` it is read against, exactly as
`Vision/datom.md:120` writes it (`self.positions(T::ARITY, budget)`), so
`from_positions(positions)` takes no budget of its own and `position()` takes no
argument.

A derived struct therefore emits a statement and a dispatch, and no reading:

```rust
impl Compositional for Locus {
    const ARITY: Integer = 2;
    fn from_positions(mut p: Positions<'_>) -> Result<Self, Error> {
        Ok(Locus { path: p.position()?, extent: p.position()? })
    }
}
impl Composing for Locus {
    fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error> {
        Composable::compose_positions(datom, budget)
    }
}
```

### Why not a positional kind and a scalar kind

Rejected, on three grounds.

1. **The residue is not scalar.** What is not positional is not "the scalars":
   it is `String`, `i64`, `f64`, `bool`, `Meaning`, *and* `Vec`, `Option`,
   `Box`, `Result`, *and* every enum. A `Vec` has no arity and is not a scalar;
   an enum dispatches on a head and is not a scalar. A kind named for scalars
   would have been a kind named after a third of what it holds.
2. **The two are not coordinate.** A struct is composed *as well as* positional.
   Two sibling species would have made "is composed" say nothing common about
   them, and `Datom::compose<T>` would have had no single bound to be generic
   over. Composing is the genus; stating positions is one differentia of it.
3. **Rust coherence forbids the blanket that a sibling split would want.**
   `impl<T: Compositional> Composing for T` conflicts with `impl Composing for
   String`, because the compiler cannot know `String` is not `Compositional`.
   Supertyping plus a one-line generated dispatch is the shape that survives
   that, and it keeps the reading itself in a single place regardless.

### Why the constant is honest now, where it was not before

Before, every type had to name an arity and sixteen of them lied. Now only a
type that *has* positions bears the kind that names them, and `ARITY` is read by
`compose_positions` and by nothing else. The refusal it raises —
`ErrorKind::Arity { expected, found }` at the struct's own path, before any
position is read — is unchanged in behavior and now derives from a declared
constant rather than from a literal baked into macro output.

### The anonymous positional type

A multi-field variant's payload is a struct of positions with no name of its
own. Rust has a name for an anonymous positional type: a tuple. So the tuples
bear `Compositional` (arities two through twelve), and a derived enum reads a
multi-field payload as the tuple it is:

```rust
"Pair" => { let (a, b) = Composable::compose_positions::<(i64, String)>(body, budget)?; ... }
```

This was the last place the tree-reading was repeated per variant in generated
text; it is now the same one reading. The ascent is symmetric — the tuples bear
`Datomizable`, and `&T: Datomizable` where `T: Datomizable`, so the derived
`datomize` places a multi-field payload through the tuple as well.

The alternative considered and rejected was generating a hidden named struct per
multi-field variant: ontologically identical, strictly more code, and it leaks a
type nothing else can name.

### The derive is renamed

`#[derive(Compositional)]` is `#[derive(Composing)]`. For a struct the derive
emits both impls; for an enum it emits only `Composing`, because an enum is not
positional. The name that covers both inputs is the ability the derive confers.
Every derive site in the estate is ethos-zero-generated, so the rename costs a
regeneration and no hand edit.

### What the psyche was consulted on

`flows/f6db8d/vision/arity.md` (the ruling: "reintroduce arity where it makes
most sense (sounds like it should be in compositional)") and
`flows/f6db8d/vision/designPractice.md` ("the vision is imperfect. Use common
sense and research good ontology and software anatomy"). `Vision/protos.md`,
`Vision/datom.md`. `flows/*/vision/`, `flows/*/notion/` and `vision-raw/` were
searched for `from_positions`, `Compositional` and `ARITY` by
`reports/substrate-review.md` §2 and found empty; this thread did not re-run
that search and relays it.

## 2. What was written, in order

1. `src/core.rs` — `Composing` added; `Compositional` given `ARITY` and
   `from_positions` and made a subkind of `Composing`; `Composable` given
   `compose_positions`; `Positions` given the budget; `DatomPositioning::positions`
   given the budget; `Error` and `ErrorKind` rewritten to compose through the
   one reading.
2. `src/composition.rs` — every intrinsic impl moved to `Composing`;
   `protos::Extent` and `protos::Error` now read their bodies through
   `compose_positions`.
3. `src/positional.rs` (new) — the tuple impls and `&T: Datomizable`.
4. `crates/datom-codec-derive/src/lib.rs` — the derive renamed and rewritten to
   state positions rather than read them.
5. `datom-codec-kinds.ethos`, `datom-codec.ethos`, both generated contracts,
   `README.md`, `src/lib.rs`.

## 3. Tests, seen failing first

Three tests were added to `tests/composition.rs` and each was seen failing
against the pre-change head `627db67f` in a scratch clone (witnessed):

| test | how it failed before |
|---|---|
| `a_positional_type_states_its_arity_and_never_reads_the_tree` | `error[E0576]: cannot find method or associated constant ARITY in trait Compositional`; `error[E0599]: no method named compose_positions` |
| `a_tuple_is_the_positional_type_a_multi_field_variant_payload_has_no_name_for` | the same two refusals |
| `every_node_of_a_multi_field_variant_spends_the_composition_budget` | ran, and failed on behavior: `called Result::unwrap_err() on an Ok value: Pair(7, "seven")` — the old code composed a four-node value on a three-unit budget |

The third is the one behavioral change in the wire-facing direction: a
multi-field variant's payload struct is a node, and it now spends one budget
unit of its own like every other node.

## 4. A skill and its implementation disagree

Witnessed: the `ethos` skill writes an associated constant in a complex kind as
`« CAPACITY Integer »`. ethos-zero 8.0.1 refuses that
(`GenerationRejected.{ … Conceptual.{ [ 2 3 1 2 ] Expected.Section } }`) and
reads constants as a bracket of headed forms, `[ ARITY.Integer ]`
(`ethos-zero/src/conception.rs:467`, `src/generation.rs:570`). The
implementation's form was used. This is recorded, not resolved: which of the two
is wrong is a question for whoever owns the skill text.

## 5. Revisions

### Producers

| repository | before | after |
|---|---|---|
| protos | 0.30.1 `171b21f65337983ab624b7b906397a4f1f92c5a3` | unchanged — it declares no datom kind |
| datom-codec | 0.26.3 `627db67f2655efd9f786864009955005fd8ab2ad` | **0.27.0** `6dccc76b75918a91d3370a9d4fe88aa7dd567876` |
| ethos-zero | 8.0.1 `de3d9928b156f2e1a92d060b7817af201abfdbef` | **9.0.0** `b232d35e03011161fe7ec9129ad99a9914413348` |
| signal | 3.0.2 `8f9a0deb701cebbea518679548df4a795affc918` | **4.0.0** `48ae17b485f2781e8ec1ca02a7fe04ad28a37f9f` |

Each of the three was gated by this thread with `cargo test`, `cargo fmt
--check`, `cargo clippy --all-targets -- -D warnings`, `cargo doc --no-deps` and
`nix flake check -L`, all green; every `nix flake check` ran on **Prometheus**,
the remote builder, which was reachable throughout. Every push was confirmed by
`git ls-remote` against the real GitHub remote (witnessed).

Bumps: datom-codec and ethos-zero and signal all carry a breaking kinds or
generated-code change, so each took a breaking bump under its own scheme
(0.26.3 → 0.27.0 pre-1.0; 8.0.1 → 9.0.0; 3.0.2 → 4.0.0).

### Consumers

Every row below was carried out by a subflow dispatched by this thread, under
its own Orchestrate lock over the repository's real path, and is **relayed**
from that subflow's report — except the rows this thread did itself
(signal-upgrade, terminal-cell), and except every `after` revision and version
in the table, which this thread re-read directly with `git ls-remote
git@github.com:LiGoldragon/<repo>.git main` and `git show <sha>:Cargo.toml`
(witnessed).

| repository | before | after | gate |
|---|---|---|---|
| claude-answers | 0.7.1 | **0.8.0** `c0c56a00503ab0b7a4dc6b7ed1c0a9964c5d6a22` | green, `nix flake check` on Prometheus |
| curriculum-deploy | 0.6.2 | **0.6.3** `37128c6d005425af58af0f609567c9759b850c2b` | green, Prometheus |
| horizon-rs | 0.10.1 | **0.11.0** `e5820bb5685d104c23e2795ed278f363cebb6ddc` | green, Prometheus |
| signal-domain | 2.0.1 | **3.0.0** `0289b88bbdaadc7e957dc55c612f2132d93463e6` | green, Prometheus |
| signal-terminal | 2.0.1 | **3.0.0** `82ffb06a0c3cf2af31d4a0e59e1e15dd5efa5905` | green, Prometheus |
| signal-upgrade | 2.0.1 | **3.0.0** `4762886625ea4161e489d055418c67db06aecaac` | green, Prometheus (this thread) |
| terminal-cell | 2.0.0 | **3.0.0** `9ff9a7e129ea8aa366d3844e66cca8875516ab32` | green, Prometheus (this thread) |
| signal-ethos-zero | — | **no change** | declares none of the four producers; its `src/generated/signal.rs` is hand-written, not ethos-zero output |
| meta-signal-ethos-zero | — | **no change** | the same |

## 6. Still behind, and why

### Held by a sibling f6db8d subflow at the time of this sweep

Witnessed by `orchestrate 'Observe.Locks'`, run by this thread during the
sweep. Each row is a repository a sibling of this subflow holds for other work;
none was touched.

| repository | lock |
|---|---|
| signal-persona | 1281 `SignalPersonaFrameShare` |
| signal-message | 1274 `SignalMessageFrameUnfork` |
| signal-harness | 1282 `SignalHarnessFrameShare` |
| signal-mind | 1283 `SignalMindFrameShare` |
| signal-mirror | 1295 `SignalMirrorSignalSpelling` |
| meta-signal-mirror | 1296 `MetaSignalMirrorSignalSpelling` |
| message | 1236 `MessageDatomMigration` |
| meta-signal-message | 1235 `MetaSignalMessageDatomMigration` |
| persona | 1237 `PersonaDatomLanding` |
| mentci | 1243, mentci-lib 1244, signal-mentci 1240, meta-signal-mentci 1241 |
| criome | 1242, meta-signal-criome 1239, signal-criome 1311 |
| lojix | 1226 `LojixAnatomy` |
| CriomOS | 1227 `F6db8dCriomosLojixLanding` |
| orchestrate | 1260 `OrchestrateNexusActor` |
| nexus | 1261 `NexusSituatedPermissive` |
| datom-codec, ethos-zero | 1298 `F6db8dFiniteDecimal`, 1308 `F6db8dEthosZeroDecimalDerives` — taken **after** this work landed and released, by a sibling continuing on these heads |

### Blocked by a held repository, not by anything in this change

These declare `signal-persona`, `signal-message` or `signal-router`, which are
held above. Cargo admits one resolved version of each crate in a graph, so
repinning them now would mean either a duplicate-version compile failure or
repinning a repository this subflow does not hold. Witnessed by reading each
`Cargo.toml`.

- introspect, signal-introspect, meta-signal-introspect
- signal-harness, signal-mind
- signal-system, meta-signal-system, system
- terminal

### Excluded by the brief

CriomOS, CriomOS-home, lojix, orchestrate and the persona, mentci, message,
router and mirror families, together with every running service. Nothing in any
of them was read or written.

### One head moved under the sweep

Witnessed: a sibling f6db8d subflow landed **signal 5.0.0
`7bcb0949cdaa4501651ed519625eba48e283fac0`** ("Bound the frame validator's
nesting depth") on top of this work's signal 4.0.0 while the consumer sweep was
running. Every consumer this sweep repinned therefore carries signal 4.0.0
`48ae17b4…` — current for the arity change, one commit behind signal's head for
the validator change. Recorded, not chased: chasing it would repin a set this
subflow gated against a different head.

## 7. Two client observations, relayed not witnessed

Four dispatched subflows independently reported that the installed `orchestrate`
client refuses a multi-word Datom string in guillemets, splitting it on
whitespace and raising an arity fault, and that curly quotes or a bare word work
instead. **This thread did not reproduce it** — every lock this thread took used
a guillemet-quoted multi-word reason and was accepted, and every release printed
the reason back intact. The two observations are both first-hand and they
disagree; the difference is not explained here. It is recorded for whoever owns
the client.

One subflow reported that `recompose.py` is not sufficient in a repository whose
committed generated file was last emitted by an ethos-zero older than 8.0.1,
because 9.0.0 also adds derives and `#[rustfmt::skip]` that the older generator
did not; it regenerated for real through the repository's own freshness path
instead. Every repository whose generated file was current at 8.0.1 had the
rewrite confirmed byte-exact by its own `build.rs` assertion.

## Sources

- Brief of main flow f6db8d to this subflow, 2026-09-12.
- `flows/f6db8d/vision/arity.md`, `flows/f6db8d/vision/designPractice.md` — the
  two rulings, read in full by this thread (witnessed).
- `Vision/protos.md:78-90`, `Vision/datom.md:110-150` — read in full by this
  thread (witnessed).
- `flows/f6db8d/reports/substrate-review.md` §1.2-§1.4, §2, §3, §4;
  `reports/datom-codec-fix.md` §1.5, §1.10, decisions 3-6, "Contradictions left
  standing" — read by this thread (witnessed); the account of what 0.26.x
  removed and why is relayed from them.
- `flows/f6db8d/reports/consumer-sweep.md` — read in full by this thread for the
  consumer list, the skip precedent and the push-verification precedent
  (witnessed).
- datom-codec, ethos-zero, signal and protos working trees and their
  `origin/main` — read and edited by this thread (witnessed).
- `ethos-zero/src/conception.rs:467`, `src/generation.rs:570,736` — read by this
  thread for the associated-constant form (witnessed).
- The scratch clone of datom-codec at `627db67f` with the new tests copied in —
  run by this thread; the three failure transcripts in §3 are its output
  (witnessed).
- `nix flake check -L` for datom-codec, ethos-zero, signal, signal-upgrade and
  terminal-cell — run by this thread, each on Prometheus (witnessed).
- `orchestrate 'Observe.Locks'` — run by this thread before dispatching and
  again during the sweep (witnessed); §6's lock table is its output.
- Each dispatched subflow's final report to this thread — relayed for that
  repository's gate detail, regeneration mechanism and version reasoning. Every
  landed revision and version in §5 was re-read by this thread from the real
  GitHub remote with `git ls-remote` and `git show <sha>:Cargo.toml`, not
  relayed.

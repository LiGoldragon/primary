# Substrate decisions implemented: the depth ceiling, the finite decimal, the single ascent

Subflow of main flow `f6db8d`, 2026-09-12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: wait out the sibling arity cascade, then implement from
`reports/design-decisions.md` in order — (a) item 7's security finding in
`signal`, (b) A7 / item 7's finite Decimal and the Eq/Hash/Default derive
decision in `ethos-zero`, (c) item 1's single `Datomizable` in `datom-codec`,
(d) item 2's newtype cutover only if bounded enough to finish. Each under an
Orchestrate lock, producers before consumers, tests seen failing first, full
Nix gate, version bump, push main.

**Witnessed** means this thread ran it or read it. **Relayed** means carried
from another report without re-observation.

---

## 0. The gate this thread waited on

`reports/arity.md` names the heads its cascade landed. This thread polled
`Observe.Locks` until no `f6db8d` lock covered `datom-codec`, `ethos-zero` or
`signal`, and independently confirmed each head against its real remote with
`git ls-remote` before building on it (witnessed):

| repository | head the sibling landed | confirmed on remote |
|---|---|---|
| protos 0.30.1 | `171b21f65337983ab624b7b906397a4f1f92c5a3` | yes |
| datom-codec 0.27.0 | `6dccc76b75918a91d3370a9d4fe88aa7dd567876` | yes |
| ethos-zero 9.0.0 | `b232d35e03011161fe7ec9129ad99a9914413348` | yes |
| signal 4.0.0 | `48ae17b485f2781e8ec1ca02a7fe04ad28a37f9f` | yes |

`reports/arity.md` was still being written when this thread began: its
**Consumers** section was empty and it carried no `## Sources`. Both had landed
by the time this thread reported, and §6 works from the completed list.

---

## 1. (a) `signal`: the frame validator now declares a depth

### The finding, re-verified rather than relayed

`design-decisions.md` §7(d) names this the finding that outranks the rest.
It is correct, and this thread confirmed the mechanism in rkyv's own source
rather than taking it on report (witnessed,
`rkyv-0.8.16/src/validation/archive/validator.rs:108-110`):

```rust
    pub fn new(bytes: &'a [u8]) -> Self {
        Self::with_max_depth(bytes, None)
    }
```

and `rkyv-0.8.16/src/api/high/checked.rs:28-30`, the validator every
`rkyv::from_bytes` builds:

```rust
fn validator(bytes: &[u8]) -> Validator<ArchiveValidator<'_>, SharedValidator> {
    Validator::new(ArchiveValidator::new(bytes), SharedValidator::new())
}
```

So the ceiling exists in rkyv and is switched off by default, and `signal`'s
one production read path — `Restorable::restore`, `src/portable.rs:71` — went
through it. `FrameCapacity` bounded the body's *bytes* and nothing bounded its
*depth*.

### Seen failing first

`tests/depth_ceiling.rs` declares a self-reaching `Nest` enum carrying the
bound attributes rkyv's derive cannot infer, builds a nest iteratively so the
test's own construction cannot be what overflows, and restores it. Against the
unwired code (witnessed):

```
test a_nest_within_the_ceiling_restores ... ok
test the_ceiling_refuses_rather_than_the_byte_capacity ... FAILED
test a_nest_past_the_ceiling_is_refused ... FAILED

an archive nested 256 levels deep past the 64 level ceiling was read
instead of refused
```

That failure *is* the security finding, observed rather than argued: a 256-level
archive was walked without complaint.

### What was written

`MAXIMUM_SIGNAL_DEPTH = 64` — Cap'n Proto's figure — beside
`MAXIMUM_SIGNAL_BYTES`, so the two ceilings a peer's frame is read under sit
together and neither lives in a consumer. A `SignalDepth` carrying a
`NonZeroUsize`, and a `DepthBounding` kind whose `validator` builds exactly the
pair `from_bytes` would have built, with the depth declared. `Restorable` gains
`restore_within(SignalDepth)` as its one required capability and keeps
`restore()` as the default at the shared ceiling.

The three tests pass. The whole suite passes under `--features datom,transport`.

### Cost, stated

An archive nested past 64 that previously walked the stack now returns a typed
refusal. Nothing should have been relying on that, but it is a behaviour
change, and the bump is breaking for it.

**signal 4.0.0 → 5.0.0**, `7bcb0949cdaa4501651ed519625eba48e283fac0`, pushed to
`main` and confirmed with `git ls-remote` (witnessed). `nix flake check` green
on **Prometheus** (witnessed). Orchestrate lock 1268, released. signal moved
once more afterwards, to **6.0.0**, for the substrate repin in §5.

---

## 2. (b) The finite decimal

### What D4 actually was

`substrate-review.md` D4 reads as a writer defect. Reading both halves of the
code makes it sharper than that (witnessed, datom-codec `6dccc76`): the
*reader* held the whole rule — `Scalar for f64` refused a non-canonical run, a
missing point, and any value failing `is_finite` — and the *writer*,
`Datomizable for f64`, held none of it and emitted whatever `to_string` gave.
The two halves of one rule lived in two places and only one of them had it.

A check added to the writer would have made three places to keep in step. The
terminal shape is a type in which the unwritable value does not exist.

### What was written

`datom_codec::Decimal` (`src/decimal.rs`): a private `f64`, a `TryFrom<f64>`
that refuses every non-finite value in the crate's own error vocabulary, and
`-0.0` normalized to `0.0` so `Eq`, `Hash` and `Ord` agree. It is `Eq` —
soundly, because `NaN` is the only `f64` for which equality is not reflexive
and no `Decimal` holds one — `Hash`, and `Ord` through `total_cmp`.

**`f64` bears no datom kind at all now.** `Datomizable`, `Composing` and
`Scalar` were all removed from it. That is what makes the defect
unrepresentable rather than merely unlikely, and it is the change with the
blast radius: any consumer writing `f64` in a datom position must write
`Decimal`.

The test names the property that was false before and is true now: every value
a `Decimal` can hold makes the round trip whole, and no non-finite value can
become one. It was confirmed to discriminate by mutating the finiteness guard
and watching it fail (witnessed):

```
assertion `left == right` failed: NaN has no datom text and must not become a Decimal
  left: Ok(Decimal(NaN))
 right: Err(NotFinite)
```

### The derive set, as item 7 resolves it once Decimal is finite

`design-decisions.md` §7(a) makes the conditional `Eq`/`Hash` an interim to be
skipped entirely if Decimal is fixed first. It was fixed first, so no
conditional machinery was written and none is needed. `ethos-zero` now emits,
on every declared type in every root:

```
Clone, Debug, PartialEq, Eq, Hash
```

unconditionally, plus rkyv's three for a Signal root. **Never `Copy`** — a wire
type's size is not part of its contract. **Never `Default`** — a default is a
policy the consumer holds, not a value the wire carries; the aggregator already
wrote that rule as `DefaultingPolicy` and the generator now follows it.

`DatomDeriving` was implemented on `bool`, which §7's implementation plan flags
as the "traits live on data-bearing types" rule broken in miniature. The `bool`
is now a `Carriage` enum with `Archived` and `Plain` variants, and a `Carrying`
kind on `File` says which a root is.

### What the unconditional `Eq`/`Hash` cost, and where

Nothing resisted it, but three protos types and one datom-codec type had to
gain `Hash` first — found by the compiler, not by a survey:

- `protos::Error`, `protos::Problem`, `protos::ReaderBudget` — every other
  protos type already derived it. **protos 0.30.1 → 0.31.0**, additive.
- `datom_codec::Meaning` — the other intrinsic-backing type this crate owns.

### The gap this leaves, named rather than buried

A Signal contract archives its types, so `Decimal` and `Meaning` need rkyv
derives; they sit behind a new `rkyv` feature on datom-codec.

**The archived form is validated for its bit pattern and not for finiteness.**
A peer's archive can therefore carry a non-finite decimal past the validating
constructor. Closing it needs a `bytecheck::Verify` impl, and `Verify` is an
`unsafe trait` that datom-codec's `unsafe_code = "forbid"` does not admit. This
thread did not bend that policy on its own authority.

The gap is **no wider than what it replaces** — before `Decimal` existed a
Signal contract archived a raw `f64` and no reader refused a non-finite one at
all — so this is an improvement that stops short of complete, not a regression.
**It is a question for the living**: either the unsafe policy admits one
documented `Verify`, or bytecheck grows a safe predicate hook. Recorded in the
type's own doc comment as well as here.

A second consequence worth the living's eye: a generated Signal contract now
names `datom_codec::Decimal` **outside** the `datom` feature gate, exactly as it
already named `datom_codec::Meaning`. `Vision/ethos.md` says a Signal's datom
kinds are gated "so the Nexus compiles its contract without datom-codec". That
remains true only for contracts using neither intrinsic. The alternative —
moving both types to `protos`, which has no dependencies at all — was
considered and not taken, because `Meaning` already set the datom-codec
precedent and splitting the two homes would be worse than either. Named for the
living, not decided.

---

## 3. (c) `Datomizable` names one conversion

`Intent/conversion.md` — *"A kind names one conversion and is borne by the type
that undergoes it"* — outranks the Vision table that gave `Datomizable` two
bearers. The code had reconciled them with an associated `Output`, which made
a `T: Datomizable` bound constrain nothing.

The descent already had its own kind under the right name and was merely
shadowed: `DatomForming::datom_form`. The forwarder
(`src/composition.rs:165-170`) was a one-line call into it and is deleted.
`Datomizable` loses `type Output` and returns `Datom`.

### The Vision lines affected, quoted for the living

`design-decisions.md` §1 asks that these be quoted in the report. They are, from
`/home/li/primary/Vision/protos.md`:

Line 72, the table row — **superseded**:

> | `Protos` | `Datomizable`, or `Ethosizable` further on | its concept |

Line 81, the snippet line — **superseded**:

> ```rust
> impl Datomizable   for Protos { fn datomize(&self) -> Result<Datom, Error>; }
> ```

Line 84, which the code now matches exactly, minus the associated type:

> ```rust
> impl Datomizable   for Person { fn datomize(&self, at: Path) -> Datom; }
> ```

Lines 65-66, the naming rule that **generates** the collision and wants
amending rather than deleting:

> ## Kinds are borne by the type converted and named for the layer it becomes
>
> No type bears a kind two layers away. A chain is written in the open
> where it is used, never folded into a kind on its first type.

The rule is direction-blind: descent `Protos → Datom` and ascent
`composition → Datom` both "become datom", so it mints one name for two
conversions, and the same collision hits `Protosizable` (borne by `String`
descending and by `Datom` ascending, lines 79 and 82). §1's proposed amendment
— an ascending kind named for the layer it becomes, a descending kind named for
the act of forming it, because descent may fail and ascent may not — removes
the whole class. **This thread implemented the consequence; the Vision lines
are still owed and only the living can write them.**

`Vision/datom.md` line 132 — *"a single-field variant carries its type's own
form"* — is **unaffected** by (c), and is the line item 2 turns on.

The bundling `Datomic` super-kind §1 offers as optional was **not** added:
nothing depends on it, and a name with no capability earns its place only when
something asks for it.

---

## 4. (d) The newtype cutover: not started, and the measure for that

`design-decisions.md` §2's own implementation plan calls the change
*"a whole-estate cutover and should be scheduled as one, not repository by
repository"*, because `X.T` becoming `pub struct X(pub T)` changes the **rkyv
archive** of every Signal contract in the estate: *"Every Nexus and every client
must be rebuilt together."*

The brief's condition is whether that cutover is *bounded enough to complete
with gates in this session*. It is not, and this session produced the measure
rather than an estimate:

- The substrate change alone — four repositories, seven releases — took every
  gate this session could obtain from a build host that was running up to
  thirty-one concurrent flake checks, and the living twice ordered local jobs
  stopped while it was in flight.
- §2 step 4 names **223 arity-1 brace matches across 45 `.ethos` files**, whose
  discrimination between a type declaration and a variant payload §2 itself
  calls *"the one genuinely delicate part of this change"*.
- And §5 above shows that a single derive-set change propagated through four
  repositories by way of three compile failures nobody predicted. The newtype
  change is strictly larger and changes the wire, which the derive change did
  not.

The brief's fallback — *"implement the producer side behind nothing and stop
before consumers"* — was **also not taken**, deliberately. Landing a generator
that rewrites every `X.T` into a newtype would break the archive of every
consumer in the estate at once while fourteen of them are pinned to the old
generator and twenty-nine are held by siblings. A producer side landed alone
here is not a bounded producer change; it is an estate-wide break with nothing
on the other side of it. §6 records what a scheduled cutover inherits instead.

## 5. Revisions

### Producers, all landed and all verified on their real remotes

Every row: `nix flake check -L --max-jobs 0` green on **Prometheus**, pushed to
`main`, and the pushed revision confirmed with `git ls-remote` against the real
GitHub remote (witnessed, each one).

| repository | before | after |
|---|---|---|
| protos | 0.30.1 `171b21f6` | **0.31.0** `1febca7836bf8d5f5973a302fdd50aa9c84c159b` |
| datom-codec | 0.27.0 `6dccc76b` | **0.31.0** `09e2a9d52bf7f2f11e51d15cb6c3177f72c6c927` |
| ethos-zero | 9.0.0 `b232d35e` | **10.0.0** `4bf73cae8d4f5a2072c76a11cd2f00aa3fe9f8e3` |
| signal | 4.0.0 `48ae17b4` | **6.0.0** `9d8b2b8c3f8e1096319c73e2c178f6b91cffb757` |

Bumps, each breaking under its own scheme: signal 5.0.0 for the new refusal and
`Restorable`'s changed required capability, then 6.0.0 for the repin and the
regenerated taxonomy; datom-codec for `f64` losing its datom kinds and
`Datomizable` losing `Output`; ethos-zero for every generated type's derive set
and every Decimal position's Rust type; protos additively, but it sits under
three breaking dependents.

### The order the cascade forced, recorded because it was not the order planned

The brief's order was signal, then ethos-zero, then datom-codec. The actual
dependency order turned out to be **protos → datom-codec → ethos-zero →
signal**, and it was discovered one compiler error at a time rather than by
survey:

1. `Eq`/`Hash` unconditional needed `Hash` on `protos::Error`, `Problem` and
   `ReaderBudget` — surfaced by ethos-zero's own generated `src/error.rs`.
2. Bumping protos put **two protos versions in ethos-zero's graph**, because
   datom-codec still pinned the old one, so datom-codec's intrinsic impls
   belonged to the wrong `protos::Extent`. Witnessed:
   `the trait bound `Extent: Composing` is not satisfied`, and `cargo tree -d`
   showing protos 0.30.1 and 0.31.0 side by side. Producers before consumers is
   not a style rule here; a skipped level makes two crates.
3. `datom_codec::Error`, `ErrorKind`, `ErrorLayer`, `Datom`, `Form` and `Budget`
   each needed `Hash` as well — surfaced by ethos-zero's generated
   `src/ethos-zero.rs`.

So datom-codec took four releases, not one: 0.28.0 (finite Decimal, single
ascent), 0.29.0 (the rkyv feature), 0.30.0 (repin protos), 0.31.0 (Hash on the
public data types).

### One thing the derive change broke that no decision anticipated

`#[rustfmt::skip]` on a generated item does **not** stop rustfmt reformatting
that item's other attributes. Once the derive list grew past prettyplease's
width, prettyplease broke it across lines and rustfmt wanted it rejoined, so
`ethos-zero`'s own `fmt` check failed on its committed projection — witnessed
in the gate log before the fix. The generator now writes the derive list on one
line, which is the form rustfmt wants, so the projection passes the same gate
every authored file does. Worth recording because every repository in the estate
regenerates through this and would have failed its own `fmt` check identically.

## 6. The consumer set, and what is still behind

`reports/arity.md` §5 lists the sixteen consumers its own sweep repinned, and
§6 lists what that sweep could not reach. Those rows are **relayed** from it.

### The consumer set this thread was to repin, and did not

Every producer landed (§5), so nothing blocks the repin any more. But it was
**not done**, and the reason is not only the session's budget: the repin is not
a pin bump.

The fourteen that need it — all currently on datom-codec 0.27.0, ethos-zero
9.0.0, **signal 4.0.0**:

claude-answers, curriculum-deploy, horizon-rs, signal-domain, signal-terminal,
signal-upgrade, terminal-cell, clavifaber, chroma, signal-forge,
signal-aggregator, signal-spirit, meta-signal-upgrade, meta-signal-terminal.

(signal-ethos-zero and meta-signal-ethos-zero declare none of the producers and
need nothing — relayed from `arity.md` §5.)

`arity.md` §6 already records half this gap in its own words: *"a sibling f6db8d
subflow landed signal 5.0.0 … while the consumer sweep was running. Every
consumer this sweep repinned therefore carries signal 4.0.0 … one commit behind
signal's head for the validator change."* That sibling was this thread, and
signal has since moved again, to 6.0.0.

Each of the fourteen is behind by **four** things, and two of them are code:

1. **signal 6.0.0** — the depth ceiling, plus the substrate repin. A pin bump.
2. **ethos-zero 10.0.0** — every generated contract regenerates with a new
   derive set. A regeneration, gated by each repository's own freshness path.
   `arity.md` §7 warns, relayed, that a repository whose committed projection
   predates 8.0.1 cannot be rewritten by `recompose.py` and must regenerate for
   real; that warning now applies more widely, because 10.0.0 adds derives
   again.
3. **datom-codec 0.31.0** — **`f64` bears no datom kind at all.** Any consumer
   with an `f64` in a datom position must change it to `Decimal`, and
   `Decimal::try_from` is fallible, so the call site changes shape, not just its
   type. **This thread did not survey which of the fourteen have one**, and that
   survey is the first thing the next flow should run — it decides whether this
   is fourteen pin bumps or fourteen code changes.
4. **Any consumer archiving a `Decimal` or a `Meaning`** must enable
   `datom-codec/rkyv`, which is a new feature and therefore a manifest change,
   not a version bump.

### What this thread will not claim

It did not verify that any consumer still builds against the final heads. The
producers gate each other and gate themselves; nothing here is evidence about
the fourteen.

### Repositories a sibling holds, which a sweep must skip

Witnessed by `orchestrate 'Observe.Locks'` during this thread's work, and
consistent with `arity.md` §6: signal-persona, signal-message, signal-harness,
signal-mind, signal-mirror, meta-signal-mirror, message, meta-signal-message,
persona, mentci, mentci-lib, signal-mentci, meta-signal-mentci, criome,
signal-criome, meta-signal-criome, lojix, CriomOS, orchestrate, nexus,
repository-ledger, signal-repository-ledger, meta-signal-repository-ledger,
router, signal-router, meta-signal-router, sema-engine, triad-runtime, spirit.

Plus the set `arity.md` §6 records as blocked by one of those rather than by
any change: introspect, signal-introspect, meta-signal-introspect,
signal-system, meta-signal-system, system, terminal.

### What a later flow should do, in order

1. **Survey the estate for `f64` in datom positions.** This decides the shape of
   everything after it and nothing else can start honestly without it.
2. **Repin the fourteen** to protos 0.31.0, datom-codec 0.31.0, ethos-zero
   10.0.0 and signal 6.0.0, regenerating each committed projection through the
   repository's own freshness path rather than by text rewrite, and adding
   `datom-codec/rkyv` wherever a contract names Decimal or Meaning.
3. **Skip the held set** below, and re-read `Observe.Locks` first: it moved
   several times during this session.
4. **(d), scheduled as one cutover**, per `design-decisions.md` §2's own plan
   and §4 above.
5. **Put the two questions in §2 to the living**: whether
   `unsafe_code = "forbid"` bends for one `bytecheck::Verify` so a peer's
   archive cannot carry a non-finite decimal, and whether `Decimal` and
   `Meaning` belong in protos rather than datom-codec now that a generated
   Signal contract names them outside the `datom` gate.
6. **Ask for a redeploy of the Orchestrate daemon**, per §7.

## 7. Two things observed in passing

- **The running Orchestrate daemon splits a guillemeted string on every space,
  and current protos does not.** This thread reproduced the refusal other flows
  reported, and then characterized it exactly rather than leaving it open.

  Witnessed, four probes at one sitting:

  ```
  «a»          -> Locked.{ 1320 P f6db8d [ /tmp/p ] «a» }
  «a b»        -> invalid request: … Arity(4, 5)
  «a b c»      -> invalid request: … Arity(4, 6)
  «a b c d»    -> invalid request: … Arity(4, 7)
  ```

  The arity found is `3 + word count`. So the guillemets *are* recognized — a
  single-word opaque locks and prints back with its delimiters — and every
  space **inside** them still breaks the run into another position. That is
  precisely the rule `Vision/datom.md` states as *"never inside the guillemets,
  where a space is content"*.

  It is not a grammar question and not an encoding one: the request bytes were
  confirmed to carry U+00AB/U+00BB as `c2 ab` / `c2 bb` (witnessed, `od -c`),
  and **protos 0.31.0 reads the same text correctly** — `«a b c»` protosizes to
  one opaque and reprints byte-identical (witnessed, a scratch example run
  against the local crate). The defect is therefore in the *deployed daemon's*
  older protos, not in the substrate as it now stands.

  That resolves the disagreement `arity.md` §7 leaves open — four of its
  subflows refused, the arity thread itself not — without needing either side to
  be wrong about what it saw: the two were talking to a binary whose behaviour
  differs from the source. **What is owed is a redeploy, which this thread is
  forbidden to do**, and until then every flow must write one-word lock reasons.
  Every lock this thread took carries one.

- **The remote builder.** Prometheus was reachable throughout and every
  `nix flake check` in this report ran there, forced with `-j0`. The user's own
  account cannot open the builder connection
  (`nix-ssh@prometheus…: Permission denied`); the daemon holds the host key and
  distributes, which a probe derivation confirmed before any real build.

## Sources

- `/home/li/primary/flows/f6db8d/reports/design-decisions.md` §1, §2, §7 — the
  decisions implemented; read whole for those sections.
- `/home/li/primary/flows/f6db8d/reports/arity.md` — the heads to start from;
  its Consumers section was empty when read.
- `/home/li/primary/flows/f6db8d/reports/open-items.md` A1, A7, A9, A10 —
  the open items these close or touch.
- `/home/li/primary/flows/f6db8d/reports/substrate-review.md` §5 D4 — the
  defect the finite Decimal closes.
- `/home/li/primary/Vision/protos.md` lines 65-66, 72, 79-85;
  `/home/li/primary/Vision/datom.md` line 132; `/home/li/primary/Vision/ethos.md`
  line 133 — quoted above where superseded or owed.
- `/home/li/primary/Intent/conversion.md` — read whole; the authority for (c).
- `/home/li/primary/flows/f6db8d/vision/designPractice.md` — the standing
  authorisation to use researched anatomy where Vision is imperfect.
- rkyv 0.8.16 source in the local registry:
  `src/validation/archive/validator.rs`, `src/api/high/checked.rs`,
  `examples/json_like_schema.rs` — witnessed, not relayed; the depth finding and
  the recursive-derive bound stack come from these.
- `bytecheck-0.8.3/src/lib.rs:221` — `Verify` is an `unsafe trait`; the reason
  the archived finiteness check was not written.

# The final sweep: what reached the heads, and why the rest cannot be a sweep at all

Subflow of main flow `f6db8d`, 2026-09-12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: wait until no `f6db8d` lock covers `signal`, read
`reports/exchange-protocol.md`, take the newest heads by `git ls-remote`, then
carry every consumer across the estate to those heads — producers before
consumers. Survey every `f64` in a datom position per repository before
repinning and convert it honestly. Regenerate contracts from ethos-zero.
Delete any compatibility path. Gate `nix flake check -L --max-jobs 0` per
repository, bump per versioning, push main, verify. Skip repositories a
sibling holds and list them with the lock.

**Witnessed** means this thread ran it or read it on this machine. **Relayed**
means a dispatched subflow reported it and this thread did not re-observe it;
where a relayed claim was load-bearing this thread re-read the source and says
so.

## 1. The heads, and the one that moved twice while the sweep ran

Confirmed by `git ls-remote` against the real GitHub remotes (witnessed, each):

| producer | version | revision |
|---|---|---|
| protos | 0.31.0 | `1febca7836bf8d5f5973a302fdd50aa9c84c159b` |
| datom-codec | 0.31.0 | `09e2a9d52bf7f2f11e51d15cb6c3177f72c6c927` |
| ethos-zero | 10.0.0 | `4bf73cae8d4f5a2072c76a11cd2f00aa3fe9f8e3` |
| nexus | — | `c495f2acbfff57e017092b9cc1fbf9f73ca2badf` |
| signal | 7.0.0 | `66e7b153706696c2cfbb2abcf931a5e83aec91af` |

`signal` moved twice during the sweep: `9d8b2b8c` (6.0.0) was the head when
this thread began polling, `e1a83028` appeared with *"Own the protocol above
the archive: the exchange layer"*, and `66e7b153` — *"Prove the envelope
against the shape a real contract root has"* — is the head the sweep targets.
This thread witnessed all three. A subflow told to target `e1a83028` was
corrected to `66e7b153`; no repository landed on the intermediate commit.

The `signal` lock (1341, `F6db8dSignalExchangeProtocol`) was held for most of
this thread's life. `reports/exchange-protocol.md` appeared at 06:48 and was
read before any signal-bearing repository was touched.

## 2. The `f64` survey, which the brief made the precondition

`reports/substrate-decisions.md` §6 named this survey as the first thing the
next flow should run, because it decides whether the remaining work is pin
bumps or code changes. It was run first, across the whole estate rather than
per repository (witnessed):

```
grep -rn '\bf64\b' --include='*.rs' --include='*.ethos'
```

Sixteen repositories contain an `f64` at all. Of those, only **one** has one in
a datom position, and the discriminator is not the grep but the two things that
make a position a datom position — a `Decimal` in an `.ethos` source, or a
field of a type bearing datom-codec's derives:

```
grep -rln 'Decimal' --include='*.ethos'
-> horizon-rs/lib/ethos/horizon.ethos
-> ethos-zero/fixtures/signal-decimal.ethos
-> ethos-zero/fixtures/placed-types.ethos
```

The two `ethos-zero` hits are the producer's own fixtures. **`horizon-rs` is
the only consumer in the estate with an `f64` in a datom position**, and it has
four, all in `FixedLocation`.

Every other `f64` in the estate sits outside a datom position, and the reason
is structural rather than incidental: `whisrs`, `chronos`, `nota`/`dotos`,
`relative-age-display`, `listener`, `brightness-ctl`, `agent`, `mentci-egui`,
`kameo` and `structural-codec` are on the **dotos/schema-rust** stack, whose
codec is not datom at all. `chroma`'s twenty-five are DBus calls, solar-angle
arithmetic, and two `f64` in `StoredLocation`, which is rkyv-archived for redb
persistence — not a datom position (relayed by the chroma subflow, and
independently confirmed here: `chroma/src/generated.rs` contains no `f64` and
`chroma.ethos` declares no `Decimal`).

**One thing worth the living's eye, found by the survey rather than sought.**
`chroma`'s `StoredLocation` holds two bare `f64` that are archived to disk and
read back, and nothing refuses a non-finite one. It is outside the datom
contract, so `Decimal` does not reach it, and it is therefore exactly the
defect `Decimal` was introduced to make unrepresentable — surviving in a
neighbouring codec. Named, not fixed; fixing it is a redb storage change, not a
repin.

### horizon-rs, the one honest conversion

`ethos/horizon.ethos` declares `FixedLocation.{ Decimal Decimal Decimal
Decimal }`. Under ethos-zero 9.0.0 those generated as `f64`; under 10.0.0 they
generate as `datom_codec::Decimal`. Three sites had to change and each was
decided on its own terms:

- `lib/src/generated/horizon.rs` — regenerated, not edited.
- `lib/src/projection/node.rs:270-277` — the projection builds a
  `FixedLocationView` whose fields are the `f64` that serde and rkyv carry out
  to Nix. `Decimating::float()` widens each back. This is the direction that
  cannot fail: a `Decimal` is finite by construction, so the widening cannot
  produce a value the view could not hold, and the comment at the call site
  says so rather than leaving a reader to wonder why an unwrap was safe.
- `lib/tests/contract.rs:403-407` — the other direction, which *can* fail.
  `Decimal::try_from` is fallible, so the test builds its literals through a
  helper that states the warrant in the expectation text: `Decimal::try_from(value).expect("a finite literal is a decimal")`.

**And one compatibility path deleted.** `lib/Cargo.toml` declared
`datom = ["dep:datom-codec", "dep:protos"]`, a feature whose whole claim was
that the crate compiles without datom-codec. That claim is now false: the
generated contract names `datom_codec::Decimal` *outside* the gate. Rather than
keep a feature that lies, `datom-codec` became a plain dependency and the gate
was left holding only what it still governs — the datom kinds themselves. This
is the local instance of the gap `substrate-decisions.md` §2 raised for the
living; it is recorded there as a question and here as a consequence.

`datom-codec/rkyv` was enabled, because `FixedLocation` is archived.

## 3. What the sweep found that changes its shape

Three findings, each of which redrew the work. They are the substance of this
report; the table is downstream of them.

### 3a. The estate is two substrates, and only one of them is sweepable

Counting `protos` versions across every `Cargo.lock` in the estate (witnessed)
splits the repositories cleanly:

- **protos 0.29–0.31 with `datom-codec` present** — the datom stack. Sweepable.
- **protos 0.5.x with `signal-frame` present and no `datom-codec`** — the
  retired stack: `agent`, `cloud`, `core-nomos`, `criome`, `logos-engine`,
  `mentci-egui`, `meta-signal-agent`, `meta-signal-cloud`,
  `meta-signal-mentci-client`, `meta-signal-mind`, `nomos-engine`, `router`,
  `rust-logos`, `schema-rust`, `sema-engine`, `signal-agent`, `signal-cloud`,
  `signal-logos`, `signal-mentci-client`, `signal-sema-storage`,
  `signal-version-handover`, `spirit-ethos`, `textual-rust` — twenty-three,
  plus `mentci`, which straddles both with four coexisting protos revisions.

protos 0.5.1 is not an old pin of today's protos; it is a different generation
that depends on `content-identity` and `signal-frame`. These reach protos
through `dotos`, `nota` or `schema-rust`. **Carrying them to protos 0.31.0 is
not a repin — it is a migration off a retired producer**, and it is the same
wall earlier flows hit on `router`, `criome`, `mentci` and
`repository-ledger`. Counting them as "consumers behind" overstates what a
sweep can reach by more than twenty repositories.

### 3b. Two directory names in the sweep set were not repositories

Derived from directory names under `/git/github.com/LiGoldragon`, the consumer
set contained two entries that are aliases of **producers**. This was my error
in constructing the set, and it nearly moved a producer.

- **`datom`** — its checkout's `origin` is `git@github.com:LiGoldragon/datom-codec.git`, and
  `git ls-remote` on `datom` and on `datom-codec` return the same head,
  `09e2a9d5`. It is a second checkout of datom-codec. A subflow had begun
  editing it — bumping datom-codec's own `ethos-zero` flake input and
  regenerating its contract — before the correction arrived. Nothing was
  committed: `main` still equalled the remote. This thread restored the three
  files with `jj restore`, confirmed `jj st` clean and
  `git rev-parse refs/heads/main` equal to the remote head, and released the
  lock (all witnessed). Had that landed, every consumer pin the sweep was
  converging on would have been invalidated mid-flight.
- **`signal-standard`** — `git ls-remote` on `signal-standard` and on `signal`
  both return `66e7b153`. It is `signal` under an old name, and GitHub serves
  one ref set through both spellings. A push through it would have landed on
  `signal`'s `main` inside lock 1341. A lock appeared on that path twice and
  was released both times.

An audit of every checkout's `origin` against its directory name (witnessed)
found one further alias pair class and two mirror hazards:

```
datom                    -> datom-codec.git
repository-ledger        -> gitolite@localhost:repository-ledger
signal-repository-ledger -> gitolite@localhost:signal-repository-ledger
```

and, by identical heads, `dotos`/`nota`, `rust-logos`/`textual-rust`,
`core-ethos`/`core-schema` are each one repository under two names. The two
`gitolite@localhost` remotes are the hazard `file-editing` names explicitly: a
push there moves a mirror, not GitHub, and `origin` cannot be trusted as the
verification target. Every push in this sweep was verified against the
`https://github.com/LiGoldragon/<repo>` URL.

### 3c. A daemon cannot be repinned apart from its contracts

The most consequential finding, established independently three times.

`introspect`, `system` and `terminal` each call `actualize`/`textualize`
generically over their contracts' generated types, in their own
`src/datom_text.rs`. Those calls cross a `datom_codec::Composing`/`Datomizable`
trait boundary. Moving a daemon's datom-codec pin while its contract stays put
places two incompatible instances of those traits in one graph — a compile
break, not a lint.

The mechanism that makes this bite in the gate is sharper, and the diagnosis
that circulated for it was **wrong**. Three subflows reported gates failing at
the deps-vendoring step on `datom-codec` rev `6dccc76b` and concluded the
revision had been garbage-collected from GitHub. It has not been. Witnessed:

```
git fetch --depth 1 https://github.com/LiGoldragon/datom-codec.git 6dccc76b75918a91d3370a9d4fe88aa7dd567876
git cat-file -t FETCH_HEAD -> commit
```

The real cause: the Nix build sandbox has **no network**, and crane vendors git
dependencies from `Cargo.lock` alone. When a repository's own pins move forward
but a contract it pins by fixed rev still demands the older `datom-codec`, the
lock no longer lists that revision and the sandbox cannot obtain it. The fix is
to move the depended-on contract in the same pass — not to keep both revisions,
which resolves and then fails to compile for the trait reason above. This
matters because the two diagnoses imply opposite actions: one says nothing can
be done, the other says the closure is simply incomplete.

So the unit of work is the **closure**, not the repository. And the closure is
sometimes wider than it looks: `meta-signal-introspect` pins `signal-introspect`
*and* `signal-persona` by fixed rev, so its closure is four repositories deep.

## 4. `links = "signal"`: why the remainder is one wave and not a sweep

`reports/exchange-protocol.md` §9 supplies the constraint that governs
everything still outstanding: `signal` declares `links = "signal"`, and cargo
admits one package per `links` key per dependency graph. A contract left on an
older `signal` therefore **cannot co-resolve** with anything on 7.0.0 — a stale
pin is a hard resolution failure, not deferred debt. §9 also names what each
contract must gain besides the pin: a one-line `impl Contracted for Query`
naming the `ETHOS` constant it already exports.

This makes the signal-bearing half of the estate a single atomic wave, which
that report says should be one actor's single pass.

**The rule for membership, and a correction I owe two subflows.** Acting on the
coordinator's instruction to repin "every contract and consumer", I told two
subflows to move signal in repositories that do not contain it. Both refused
and read the tree instead, and both were right. The membership test is exact:

```
grep -c '^name = "signal"$' <repo>/Cargo.lock
```

`meta-signal-terminal`, `meta-signal-upgrade`, `signal-terminal`,
`signal-domain`, `signal-upgrade` and `harness` all return 0 — they generate
through ethos-zero and never depend on the signal crate, so `links = "signal"`
cannot bind them. `signal-terminal`'s own `links = "signal-terminal"` is that
crate naming itself, not a dependency. Reading the tree beat my relayed claim,
and the subflows that declined an instruction they could not verify behaved
correctly.

The wave's actual membership, with the revision each held when surveyed
(witnessed):

| signal version held | repositories |
|---|---|
| 5.0.0 `7bcb0949` | mentci-lib, message, meta-signal-criome, meta-signal-mentci, meta-signal-message, meta-signal-mirror, meta-signal-persona, meta-signal-repository-ledger, meta-signal-router, meta-signal-system, persona, signal-criome, signal-harness, signal-introspect, signal-mentci, signal-message, signal-mind, signal-mirror, signal-repository-ledger, signal-router, signal-system |
| 4.0.0 `48ae17b4` | aggregator, meta-signal-aggregator, meta-signal-spirit, signal-aggregator, signal-forge, signal-spirit, signal-spirit-judge |
| 3.0.2 `8f9a0deb` | lojix, meta-signal-lojix, orchestrate, signal-lojix, meta-signal-orchestrate, signal-orchestrate |
| **7.0.0 `66e7b153`** | **signal-persona** |

`signal-forge` holds its pin as `branch = "main"` — the one mutable pin left,
and the spelling hazard the pin-string rule exists for.

## 5. What landed

Every row: `nix flake check -L --max-jobs 0` (with `--keep-going` where the
subflow passed it) green on **Prometheus**, pushed to `main`, and the pushed
revision confirmed against the GitHub remote with `git ls-remote`.

`horizon-rs` was done by this thread and is witnessed throughout. The rest were
done by dispatched subflows; their gate results are relayed, and the pushed
revision and resulting pins of each were **re-read by this thread** from the
remote, so the landing itself is witnessed even where the gate is not.

| repository | version | pushed revision |
|---|---|---|
| horizon-rs | 0.11.0 → **0.12.0** | `8c11dfaa19accda0e1d0d8708542a13ed788ea0a` |
| clavifaber | 0.5.0 → **0.6.0** | `4b7190055ba5deeb8443f0fb974037d7ebdfc770` |
| triad-runtime | 0.10.0 → **0.10.1** | `4b8582bd8a00ec4a177d1bca729ff731a5365b62` |
| terminal-cell | 3.0.0 → **3.0.1** | `9cab87cc28749e16c518800a2de5287b923a6520` |
| signal-domain | 3.0.0 → **4.0.0** | `a6d5048130d7c5bf7f202ee1cd1a94bf15908408` |
| signal-terminal | 3.0.0 → **4.0.0** | `a3e4f96bf2eb2095e377a73a31ee927ef3e6b44f` |
| signal-upgrade | 3.0.0 → **4.0.0** | `6566d4a6f3d491212172c3560f23f7f0d8b9348f` |
| meta-signal-terminal | 3.0.0 → **4.0.0** | `40219a6dec2a8e5dbe4a3720226bf563cea6c36b` |
| meta-signal-upgrade | 3.0.0 → **4.0.0** | `f7b3e8d84bb419d5d3a6809b714334cf9807a959` |
| signal-persona | 4.0.0 → **5.0.0** | `3462a0afc533f5dcfbee8d3802d17b594accc14f` |

`signal-persona` is the only one carrying **signal 7.0.0** and the `Contracted`
impl; this thread confirmed its lock entry reads
`version = "7.0.0"` at `66e7b153` (witnessed). It is the wave's first member.

### Two version surfaces corrected rather than accepted

`triad-runtime` and `terminal-cell` were first landed with their versions
unchanged, on the argument that neither crate's own public surface moved. A
changed dependency revision is a package change, which `versioning` says the
version surface must reflect, and the estate's own recorded convention for a
pure repin is a patch bump. Both were re-gated and re-landed with the bump.
Recorded because the deviation was reasoned, not careless, and because the
correction cost two more full gates.

### One split left standing, deliberately

`terminal-cell`'s lock now carries protos at `1febca78` **and** `171b21f6`
**and** `9bce5ed8`, and datom-codec at `09e2a9d5` **and** `6dccc76b`
(witnessed, re-read from the pushed head). The old copies are demanded by
`ethos-zero` 9.0.0 reached through `signal-terminal`'s older revision, and by
`schema-rust`'s own fixed pin. Collapsing them means editing manifests that
repository does not own. Per the pin-string rule the subflow moved only
revisions and left the spelling and the split alone, and said so — which is the
right call, and the reason `terminal-cell` is green while still split.

## 6. What did not land, and exactly why

### Blocked on a closure member, not on itself

| repository | blocked on |
|---|---|
| introspect | `signal-introspect`, which cannot gate until its `signal` pin moves to 7.0.0 |
| system | `signal-system` and `meta-signal-system`, both on signal 5.0.0 |
| meta-signal-introspect | `signal-introspect` **and** `signal-persona`, pinned by fixed rev |
| harness | `signal-terminal`'s republish — now available at `a3e4f96b`, so this one is unblocked and was re-dispatched |
| mentci | its own tree is still the pre-Datom 0.5.0 dotos crate; it has **no `flake.nix`**, so no gate exists |

`signal-introspect` is the clearest case and worth stating exactly, because it
shows the two constraints meeting: it pins `signal` at `7bcb0949`, whose own
manifest demands `datom-codec` `6dccc76b`; repinning the producers without
moving `signal` leaves the lock unable to satisfy that demand in a network-less
sandbox. It cannot be gated green **except** as part of the signal wave.

### chroma: a red the repin was not shown to cause

`chroma`'s repin, regeneration, `f64` survey and version bump are complete but
**not landed**. Its `checks.sandbox-terminal` and
`checks.set-dark-theme-example` failed twice, non-deterministically, at two
different expected colours — a timing profile, not a wrong value.

The subflow did the right experiment and reported its limit honestly: a control
build of the pre-repin head succeeded, but that result was **substituted** from
the binary cache rather than built fresh, and `--rebuild` forces a local build
which `--max-jobs 0` correctly refuses. So there is no same-conditions
comparison available on a cold machine, and no number of re-runs can produce
one.

What the experiment did establish is a real defect:
`scripts/chroma-sandbox-terminal`'s `await_ghostty_background` polls to a
15-second **wall-clock** deadline. `testing` is explicit — *a test waits on the
tested event, never on the clock* — and under a shared builder carrying this
flow's concurrent gates that is exactly the test that yields an unattributable
red. It is pre-existing, unchanged by the repin, and it is the thing standing
between the sweep and an answer. The subflow was directed to fix the wait,
keeping a generous bound so a hung daemon still cannot run forever, and then
let the gate speak. `chroma` was not landed on a red nobody could account for,
and no check was weakened to reach green.

### Excluded, with the reason

| repository | reason |
|---|---|
| `datom` | duplicate checkout of the producer `datom-codec`; edits reverted, nothing pushed |
| `signal-standard` | alias of the producer `signal`; a push there lands on `signal` |
| `mirror` | **deprecated by the living**, 2026-09-10, commit `74ed002` |
| `spirit` | deprecated; 21 mutable pins that must move together or not at all |
| the retired-stack twenty-three | on protos 0.5.x via dotos/nota/schema-rust; migration, not repin (§3a) |

`mirror` deserves its own line because a subflow refused my instruction to land
it if green, and was right to. Its own `main` carries, from the living:

> The living marked Mirror deprecated on 2026-09-10. Retain this repository as
> historical evidence, not an active development or stack migration target.
> Do not add new consumers or resume the unfinished migration without new
> explicit direction.

This thread fetched and read that commit directly rather than taking it on
report (witnessed). A dependency repin is the resumption that notice forbids.
Nothing in `Vision/` or `Intent/` supersedes it.

### Held by a sibling, with the lock

Witnessed by `orchestrate 'Observe.Locks'` at the time of reporting:

| repository | lock |
|---|---|
| CriomOS | 1227 `F6db8dCriomosLojixLanding` |
| CriomOS-home | 1322 `F6db8dCriomosHomeLanding`, 1331 `F6db8dCriomosHomeOrchestrateRepin` |
| orchestrate, nexus | 1368 `F6db8dOrchestrateExchange` (the exchange-protocol port) |
| lojix and its contracts | excluded by the brief |

Earlier in this thread's life the sibling set was far larger — locks on
`message`, `persona`, `signal-message`, `signal-system`, `meta-signal-system`,
`meta-signal-persona`, `signal-introspect`, `meta-signal-message`, `lojix`,
`signal`, `nexus` and `orchestrate` were all observed and have since been
released. The set above is the state at reporting, and §5 of
`substrate-decisions.md`'s twenty-nine-strong held list no longer describes it.

## 7. What the next flow should do, in order

1. **Run the signal 7.0.0 wave as one pass**, over exactly the repositories
   whose `Cargo.lock` contains the `signal` package (§4). Each contract gets
   the four producer pins **and** `signal` `66e7b153` **and** its one-line
   `impl Contracted for Query`. Nothing in that set can be gated green alone,
   so a repository-by-repository schedule will report failure after failure for
   a reason that is not in any of them.
2. **Then the daemons**, each with its contracts in the same pass: `introspect`,
   `system`, `terminal`, `persona`, `message`. `terminal` is ready now — both
   its contracts are landed and neither pins signal.
3. **Convert `signal-forge`'s `branch = "main"`** pin to a rev inside the wave,
   in the canonical spelling, since the wave is the one pass that can do it
   safely.
4. **Put the retired stack to the living.** Twenty-three repositories plus
   `mentci` are on protos 0.5.x with `signal-frame`. `reports/exchange-protocol.md`
   §9 records thirty-five repositories still declaring `signal-frame` and says
   plainly that "being deleted estate-wide" describes an intention, not a state.
   Whether they are migrated, retired, or left as evidence is a decision, not a
   sweep.
5. **Fix `chroma`'s clock-dependent test** and re-gate, then land its repin.
6. **Ask whether `chroma`'s `StoredLocation` should refuse a non-finite value**
   (§2), and whether `datom-codec`'s own flake should advance its `ethos-zero`
   input from 9.0.0 `b232d35e` to 10.0.0 `4bf73cae` — found while a subflow was
   in the wrong repository, but true and unacted-on.
7. **Redeploy the Orchestrate daemon.** The deployed 0.30.0 still splits a
   guillemeted lock reason on every space; every lock this thread and its
   subflows took used a one-word reason for that reason. The checkout is at
   0.35.0. `substrate-decisions.md` §7 established the defect is in the deployed
   binary's older protos, not in current protos.

## 8. Two things about the method, since they cost real time

**A subflow that stops without a foreground blocker is not resumed by
anything.** Six subflows stopped mid-gate having armed a background waiter,
and each had to be woken by message to read its own gate's exit status. On a
cold machine where every check is a remote build, the pattern that works is a
foreground `until` loop on the log file, not a notification the agent will not
be awake to receive.

**Prometheus was the whole clock.** Every compile in this report ran there
under `--max-jobs 0`; no local cargo was run anywhere. With this flow's own
subflows plus siblings' gates in flight, a single `nix flake check` took long
enough that the wall-clock cost of the sweep was set almost entirely by builder
contention — which is also what made `chroma`'s 15-second test unattributable.
The two facts are the same fact.

## Sources

- `/home/li/primary/flows/f6db8d/reports/exchange-protocol.md` §4, §7, §9, §10
  — the `links = "signal"` constraint, the `Contracted` requirement, and the
  direct-consumer list; read for those sections.
- `/home/li/primary/flows/f6db8d/reports/substrate-decisions.md` §5, §6, §7 —
  the heads to start from, the fourteen-behind list, the Orchestrate guillemet
  defect.
- `/home/li/primary/flows/f6db8d/reports/arity.md`,
  `consumer-sweep.md`, `terminal-migration.md`, `aggregator-migration.md`,
  `landings-consumers.md` — read for per-repository regeneration paths, gate
  attributes and the pin-string rule; `landings-consumers.md` §4 is the
  authority for the canonical spelling and §7 for the cold-machine gate.
- `/home/li/primary/NON_MANAGEMENT_AGENTS.md`,
  `/home/li/primary/SKILL_VARIABLES.md` — boundaries and variables.
- `git ls-remote` against `https://github.com/LiGoldragon/<repo>` for every
  producer and every landed consumer — witnessed, and the authority for every
  revision in §1 and §5.
- `/git/github.com/LiGoldragon/mirror` commit `74ed002` — the living's
  deprecation notice, fetched and read directly.
- `/git/github.com/LiGoldragon/datom-codec/src/decimal.rs` — the `Decimal` API
  the horizon-rs conversion is written against.
- `Vision/` and `Intent/` searched for `mirror` and for a superseding ruling;
  nothing found.

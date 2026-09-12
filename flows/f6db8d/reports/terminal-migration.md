# Terminal estate migration — the branch-pinned consumers onto the Datom heads

Subflow of main flow f6db8d, 2026-09-11/12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: move `terminal`, `mentci`, `introspect`, `persona` and every sibling
consumer of the contracts released tonight — excluding spirit, mirror,
harness, listener, router, repository-ledger, chroma and any running daemon's
repository whose wire a deploy would need — onto the final producer heads,
following `reports/datom-migration.md`'s method; and deal with the dirty files
found in `terminal` without discarding them.

**Witnessed** means this flow read or ran it on this machine. **Relayed**
means a dispatched subflow of this flow ran it and reported it back. Where a
gate result is relayed, the table says so.

## 1. The dirty files — what they actually were

The brief asked whether `terminal`'s uncommitted files were flow 857335's
preliminary consumer edits, and said to build on them if so and otherwise set
them aside on `f6db8d-found-dirt`. They were not 857335's edits. Three
findings, all witnessed:

**They move backward, not forward.** `git diff` in `terminal` changes
`nota-text` to `dotos-text`, the `nota` dependency to `dotos`, and three
`branch = "main"` pins (`signal-frame`, `meta-signal-terminal`,
`signal-terminal`, `schema-rust`) to older immutable revisions — it also adds
a `[patch."https://github.com/LiGoldragon/signal-terminal.git"]` block
pointing at the same source it patches, which is the self-contradictory patch
`reports/removals.md` §4 recorded as blocking `cargo check` there. The
committed HEAD carries the *newer* `nota` naming; the working tree carries the
*older* `dotos` naming. No migration onto tonight's heads looks like that.

**The same reversal sits in two more repositories.** `introspect` (14 files)
and `meta-signal-introspect` (6 files) carried the identical `nota` → `dotos`
reversal with old immutable pins restored. The brief named only `terminal`'s
ten files; the condition was wider — `terminal` itself had seventeen dirty
files by the time this flow observed it, not ten.

**The timestamps settle it.** Every dirty file's mtime is **2026-07-31**.
Flow 857335 ran on 2026-09-10. The content is six weeks older than the flow it
was attributed to, and older than the `dotos` → `nota` rename commits that
landed on each repository's main in June 2026. `jj`'s reflog in all three
shows only `export from jj` entries and no stash. The most economical reading
is a working tree written from a pre-rename state on 2026-07-31 and never
updated when the rename landed; a second possible cause is a deliberate
restoration of old pins abandoned mid-way. This flow did not determine which,
and leaves the cause unknown.

Set aside, not discarded, and verified on the real remotes with
`git ls-remote https://github.com/LiGoldragon/<repo>.git f6db8d-found-dirt`:

| repository | files | `f6db8d-found-dirt` |
|---|---|---|
| terminal | 17 | `71c1e72134b575061d8a2cd1e4d0f27a1c156d09` |
| introspect | 14 | `03767b417aa9f6af19f6d6ad7e28fd78410e814d` |
| meta-signal-introspect | 6 | `56a6e8e799b11f1f81408ff86b420142fb2246a7` |

Each working copy was then returned to its own `main` with `jj new main`.

## 2. The psyche's warrant for deleting, not shimming

Distilled Vision, `Vision/datom.md:239-243` (witnessed):

> Everything moves to Datom: all of the stack, Horizon, Lojix, everything; no
> Dotos file remains. Datom's own line of descent is NOTA, which also passed
> through the temporary name Dotos; that old notation stays behind, frozen,
> and may be called legacy.

Raw vision behind it, `flows/01a03d6e/vision/archive-dotosFiles.md:9`
(witnessed): *"There should be no Dodos files anymore"* — with the
speech-to-text correction `Dodos` → `Dotos` recorded beside the quote. And
`flows/019feb93/vision/threeStacks.md:9` (witnessed), the psyche naming the
condition for retirement: the generated Rust for signal, nexus and sema types
is what must exist *"before the old Schema + NOTA stack can be retired"*.

So `nota-text` and `dotos-text` features, `signal-frame` envelopes,
`schema-rust` build-time codegen and the `nota`/`dotos` crates are deleted
where this flow touched them, never aliased and never kept behind a feature.

## 3. The real diagnosis — mutable branch pins, not staleness

`reports/periphery-audit.md` §6 relayed six branch-pinned consumers as
*broken now*. This flow re-derived that set directly rather than inheriting
it, by grepping every `Cargo.toml` under `/git/github.com/LiGoldragon/` for a
`branch = "main"` pin on a contract that moved tonight (witnessed). The result
corrects the inherited list in three ways:

- **`kin` does not exist.** `git ls-remote https://github.com/LiGoldragon/kin.git`
  returns `Repository not found`; no directory under
  `/git/github.com/LiGoldragon/` matches `*kin*`; and
  `reports/periphery-audit.md` itself never uses the word — grepped, no hit,
  there or in `removals.md`, `consumer-sweep.md` or `open-items.md`. The name
  reached this flow through its own brief's summary of the audit, not from the
  audit. One of the six named consumers names no repository, and this flow
  found nothing it could plausibly be a shorthand for. Recorded as an
  observation against the brief's premise rather than silently dropped.
- **Rev-pinned siblings are not broken.** `signal-harness`, `signal-mind`,
  `signal-system`, `meta-signal-harness` and `meta-signal-persona` all pin
  `signal-persona` by *immutable rev* at an old revision. They still resolve
  and still build. They are stale, on the retired stack, and will need moving
  — but they are not part of tonight's breakage, and this flow did not move
  them.
- **Two siblings the audit did not name are broken.** `meta-signal-system`
  and `system` both branch-pin `signal-persona`, and `persona-spirit`
  branch-pins `signal-persona` and `meta-signal-upgrade`.

The genuinely broken, in-scope set is therefore: `terminal`, `introspect`,
`mentci`, `persona`, `meta-signal-introspect`, `meta-signal-system`, `system`,
`persona-spirit`. `terminal-cell` is rev-pinned and not broken, but is
`terminal`'s own dependency and was moved with it. `harness`, `router` and
`spirit` carry the same branch-pin breakage and were left untouched because
the brief excludes them.

**The disease is the mutable pin itself**, and a repin that lands another
`branch = "main"` re-arms it. Every dispatch in this flow was instructed to
convert *every* LiGoldragon branch pin it met to an immutable rev, not only
the ones that had moved.

## 4. Not a repin — a port

`reports/datom-migration.md`'s method was written for consumers that were
already on the Datom stack and needed their pins refreshed. It does not
describe this estate. Witnessed by reading each `Cargo.toml` and `src/`:
`terminal`, `introspect`, `persona`, `mentci`, `system`, `terminal-cell`,
`meta-signal-introspect` and `meta-signal-system` sit on the **retired**
stack — `signal-frame` envelopes with `signal_channel!`, the `nota`/`dotos`
text crates and their cargo features, `schema-rust` build-time codegen,
`triad-runtime` and `sema-engine`. The contracts they consume have been
rewritten into ethos-generated, protos/datom-codec, rkyv-framed crates.

Moving them is a port of each consumer's Rust onto a different generated
surface, not a version bump. `meta-signal-terminal` at
`a9b18ee853a449709fd908bb4c2d16c8f7fd15ff` (2.0.1) was used as the exemplar
target shape throughout — `ethos/signal.ethos`, a `build.rs` asserting the
committed `src/generated/signal.rs` against a fresh `ethos-zero` generation,
`examples/canonical.datom`, and the rkyv `Signal`/`Signalizable`/
`ByteViewable`/`Restorable` surface in `src/lib.rs`.

## 5. Deployment safety

Witnessed: every `systemd.user.services.*` declared anywhere in
`/git/github.com/LiGoldragon/CriomOS-home` is one of `active-network-widget`,
`aggregator-daemon`, `chroma-daemon`, `codex-artifact-gateway`,
`codex-remote-control`, `criomos-ui-priority`, `listener`, `message-daemon`,
`orchestrate-nexus`, plus `spirit-daemon` and `spirit-judge` in
`modules/home/profiles/min/spirit.nix`. **None** of the repositories this flow
moved has a deployed unit. Nothing was deployed, no running service was
touched, and no process was killed.

## 6. The table

The gate is the full local gate in every case: `cargo test --all-features`,
`cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`,
`cargo doc --no-deps --all-features`, and `nix flake check -L --builders ''`.
Each row's gate result is **relayed** from the dispatched subflow that held
that repository's lock, except `meta-signal-introspect`'s follow-up fix in §8,
which this flow ran itself. Every `after` sha and version in the table was
re-read by this flow directly with `git ls-remote
https://github.com/LiGoldragon/<repo>.git main` and `git show <sha>:Cargo.toml`,
not taken from the subflows' claims.

### Landed on main, full gate green

| repository | before | after | gate |
|---|---|---|---|
| terminal | 0.2.0 `061a36a1` | **0.3.0** `e1d85788` | green |
| introspect | 0.3.0 `07556777` | **1.0.0** `7eb98451` | green |
| meta-signal-introspect | 0.1.0 `eec60c42` | **2.0.0** `3d0fd975` | green |
| meta-signal-system | 0.1.0 `f64d2f1b` | **2.0.0** `17591d96` | green |
| terminal-cell | 1.0.0 `e44c41a3` | **2.0.0** `bd1defd9` | green |
| signal-harness | 0.5.1 `90e2878d` | **2.0.0** `49d16a31` | green |
| system | 0.1.0 `72839da6` | **1.0.0** `7056335d` | green |

### Landed on the pushed branch `f6db8d-datom-migration`

| repository | before | after (branch) | why not main |
|---|---|---|---|
| persona | 0.2.0 `9469b0a1` | **0.4.0** `651fe75f` | one nix check red on unmigrated `message`; see §12 |
| mentci | 0.5.0 `235b1b44` | **0.6.0** `c9a111d4` | contracts emit only encoded names; see §11 |
| criome | `2f4dded8` | `e644d251` | same chain as `mentci` |
| mentci-lib | `ace52c8d` | `2e89543d` | same chain as `mentci` |

## 7. What the wave deleted

Across the repositories above, and adding no compatibility path anywhere: the
`nota` and `dotos` dependencies; every `nota-text` / `dotos-text` cargo
feature, including `default = ["nota-text"]` defaults, `#[cfg_attr(feature =
…)]` gates and `required-features` binary declarations; every `signal-frame`
`signal_channel!` envelope and the `Frame`/`FrameBody`/`ExchangeIdentifier`/
`Reply`/`SubReply` transport surface it carried; every hand-written
`NotaEncode`/`NotaDecode`/`DotosEncode`/`DotosDecode` impl and derive; roughly
thirty hand-written newtypes in `signal-harness` whose `::new()` constructors
the generated type aliases replace; `examples/canonical.dotos` files; and in
`system`, the retired `schema-rust` `build.rs` daemon emitter together with
its `schema/*.schema` sources.

One deletion is a design decision rather than a cleanup, and the subflow that
made it said so: `system`'s meta socket carried a **try-meta-then-fall-back-to-
supervision decode** — the exact compatibility path the brief names. With bare
rkyv frames there is no discriminator between two contracts on one socket, so
an undiscriminated dual decode is not a wire at all. The subflow kept the meta
contract and dropped the persona lifecycle plane from that socket. Relayed,
and flagged here because it changes what `system`'s supervision socket speaks,
not merely how it encodes.

## 8. Three defects found in already-landed work

**A wrong canonical file that nothing read — found, fixed, and gated.**
The `meta-signal-system` subflow reported that `meta-signal-introspect`'s
`examples/canonical.datom`, landed green forty minutes earlier by a sibling of
this flow, carried `Configured.3` and
`ConfigurationRejected.UnknownPeerComponent`. Both are single-field ethos
structs, so the correct Datom heads are `Configured.{ 3 }` and
`ConfigurationRejected.{ UnknownPeerComponent }`. **Witnessed by this flow**:
that repository's `tests/contract.rs` never read the canonical file at all —
its `datom` test round-trips a constructed `Query` — so the file sat outside
its own gate and the error was invisible to it. This flow wrote a test that
actualizes every canonical line into `Query` or `Response`, **saw it fail on
`Configured.3`**, fixed the two lines, saw it pass, ran the full gate green
(`all checks passed!`) and landed it on main at `3d0fd975`. The version stayed
2.0.0: the wire did not change, only a wrong example and its missing gate.

**Guillemets, not curly quotes — the `datom` skill is wrong where it stands.**
Relayed from the `signal-harness` subflow, and consistent with what
`reports/datom-migration.md` §2 already recorded: at protos 0.30.1 /
datom-codec 0.26.3 the codec emits and reads **`« »`** for quoted strings. That
subflow's first canonical file used the skill's `“ ”` and its own gating test
caught it on the first run. The skill this flow loaded still documents curly
quotes. Whether the reader accepts `“ ”` anywhere was not determined and is
left unknown.

**A payload-carrying variant where a tag was meant — witnessed, not fixed.**
The `signal-harness` subflow found that in ethos-zero 8.0.1 a *bare* enum
variant whose name matches a declared type generates a **payload-carrying**
variant rather than a tag: `Kind.[ Foo ]` with `Foo` declared emits
`Foo(Foo)`. It located the mechanism at `ethos-zero/src/generation.rs:501`,
where `Variant::Bare(name)` checks `scope.file.declaration(name)`. It renamed
its own colliding tags and then inferred that `meta-signal-terminal` 2.0.1 had
shipped the unintended form.

**This flow verified that inference directly and it is correct.** At
`meta-signal-terminal` `a9b18ee8`, `ethos/signal.ethos` declares
`MetaTerminalOperationKind.[ CreateSession RetireSession ]` while `CreateSession`
and `RetireSession` are both declared types, and `src/generated/signal.rs:82-85`
accordingly reads:

```rust
pub enum MetaTerminalOperationKind {
    CreateSession(CreateSession),
    RetireSession(RetireSession),
}
```

Its `examples/canonical.datom` shows the consequence on the wire:
`MetaTerminalRequestUnimplemented.{ operator RetireSession.operator NotBuiltYet }`
— the terminal name appears twice, once as the record's own field and again
inside the operation *kind*, which should be naming which operation was
unimplemented, not re-carrying its payload.

This flow did **not** fix it, and the reason is a judgment worth stating. The
fix is a wire change to a contract another flow landed green, so it is a major
bump that breaks every consumer — and `terminal`, the consumer most affected,
was mid-port against that exact contract in a dispatched subflow while this was
found. Changing a wire contract under an in-flight consumer port would have
been worse than leaving a recorded defect. It is recorded here with its
evidence, unfixed, for whoever picks up `meta-signal-terminal` next. Whether
the same collision exists in other contracts landed tonight was not swept.

## 9. The chain that had to be untied first — `links = "signal-persona"`

`persona` is the estate's most connected consumer and it could not be landed
by a repin at all. Relayed from the subflow that hit it, and the mechanism is
worth stating because it shaped the rest of the night:

`signal-persona` declares `links = "signal-persona"` in its manifest, and
cargo permits exactly **one** package with a given `links` key in a dependency
graph. Once `persona` pinned signal-persona 2.0.1 directly, four contracts
that still pinned *older* signal-persona revisions by immutable rev put four
distinct signal-persona packages in the graph, and cargo refused at
**resolution**, before compiling anything:

```
error: failed to select a version for `signal-persona`.
package `signal-persona` links to the native library `signal-persona`,
but it conflicts with a previous package which links to `signal-persona` as well
```

No edit inside `persona` could fix that. This is exactly the shape
`reports/datom-migration.md` §5 recorded around `signal`, recurring: **one
knot upstream holds a whole consumer hostage, and resolution failure masks
every compile error behind it.** It also corrects §3's reading above — those
four rev-pinned siblings were *not* broken in themselves, but they were the
reason a named target could not land. Being individually fine is not the same
as being collectively resolvable.

This flow therefore dispatched all four as unblockers, out of the brief's
literal repository list but squarely on its critical path. All four landed on
main, green:

| blocker | before | after | gate |
|---|---|---|---|
| signal-harness | 0.5.1 `90e2878d` | **2.0.0** `49d16a31` | green |
| meta-signal-persona | 0.3.1 `7891445e` | **2.0.0** `88657088` | green |
| signal-mind | 0.8.0 `cf5d22c0` | **2.0.0** `7a08e51d` | green |
| signal-system | 0.2.0 `2acbdfd8` | **2.0.0** `60392314` | green |

The same pattern appeared a second time, around `mentci`, and is recorded in
§11.

## 10. A defect in ethos-zero's generation, found three times independently

Three subflows hit the same thing without knowing of each other, which is why
it is stated here as a finding rather than as one delegate's note.

**In ethos-zero 8.0.1, a *bare* enum variant whose name matches a declared
type generates a payload-carrying variant, not a tag.** `Kind.[ Foo ]`, with
`Foo` declared elsewhere in the file, emits `Foo(Foo)`. The `signal-harness`
subflow located the mechanism at `ethos-zero/src/generation.rs:501`, where
`Variant::Bare(name)` checks `scope.file.declaration(name)` and emits
`#variant(#ty)` when the name resolves.

What makes it dangerous is the failure mode:

- **The recursive case is loud.** `signal-mind` had
  `ChannelMessageKind::AdjudicationRequest` collide with a declared
  `AdjudicationRequest`, which made the type infinitely sized and failed with
  E0072.
- **The non-recursive case is silent.** `signal-mind`'s `ItemKind::Note`
  generated `Note(Note)` and compiled cleanly. It is a corrupted wire that no
  gate catches.

`signal-mind` swept its whole file and fixed both by renaming the *payload
type* (`AdjudicationRequest` → `AdjudicationSubmission`, `Note` → `ItemNote`),
never the wire-facing variant, so every variant reads as before.
`signal-system` checked every bare tag against the declared-type list before
generating and confirmed it was clean — and observed precisely why: its
request head names are not themselves declared types, whereas
`meta-signal-terminal`'s are.

This is a generator sharp edge, not a per-repository mistake. Until ethos-zero
either rejects the collision or requires an explicit payload marker, every
ethos author must check bare tags against the declared-type list by hand. The
`meta-signal-terminal` instance in §8 is the one known unfixed case.

## 11. `mentci` — two nested blockers, neither of them mentci's

`mentci` was the hardest of the four named repositories, and none of what
stopped it was in its own code. The port itself was done early and pushed to
`f6db8d-datom-migration` at `4edaf70d` (0.5.0 → 0.6.0). Then:

**First blocker — three contracts unbuildable for months.** Witnessed by the
mentci subflow and confirmed independently by the repair subflow:
`meta-signal-criome`, `signal-mentci` and `meta-signal-mentci` each carried a
`build.rs` importing `schema_rust::bootstrap::BootstrapInterfaceGeneration`, a
symbol schema-rust deleted in commit `dbfc39c` when it redesigned its
bootstrap pipeline. A mass repin had bumped each repository's `schema-rust`
pin **without porting its build script**, and the same break sat on each
repository's own `main` head — so it could not be cleared by repinning
forward. Every consumer of any of the three has been unbuildable since.

The repair subflow chose to correct the bad pin rather than port three build
scripts forward, and its reasoning is the right one to record: schema-rust
0.17's `generate()` now prepends a blake3 source digest into the emitted Rust,
so porting would have changed each contract's **committed generated wire
surface** — a major, wire-breaking change spent entirely on a stack the estate
is deleting. It also corrected the inherited trace: the two mentci
repositories had never been on `9e36587c` at all but on `6643352`, so the
sibling's proposed restore rev would have been a second wrong pin. It named
the terminal-best shape without starting it — all three should become
ethos-generated contracts — and said plainly that its repair deletes no
`dotos-text` feature and no envelope, so the brief's standing deletion order
is *not* carried out by that work.

| repository | before | after | gate |
|---|---|---|---|
| meta-signal-criome | 0.8.0 `8ec549ae` | **0.8.1** `5acfedaf` | green (no flake in the other two) |
| signal-mentci | 0.4.1 `71dca1d5` | **0.4.2** `293ea752` | green except `nix flake check` — **no `flake.nix` exists** |
| meta-signal-mentci | 0.3.1 `832107f2` | **0.3.2** `b063a33d` | same |

**Second blocker — the `links` pattern again.** `criome` pins
`meta-signal-criome` at the same old broken revision `mentci` pinned directly,
and `meta-signal-criome` declares `links = "meta-signal-criome"`. So bumping
mentci alone fails resolution: `criome` and `mentci` must be repinned
together. That joint repin was dispatched and is recorded in the table.

Two further breakages the repair subflow found that nobody had reported:
`meta-signal-mentci`'s repin had *also* moved `dotos` `80c7b17` → `b3c2c76`
while `signal-standard` stayed on `80c7b17`, splitting `DotosDecode` across
two crate versions; and each repository's own `dependency_boundary` test had
been left asserting its pre-repin revisions. Both corrected.

**Third blocker, and the one that settles `mentci` for tonight.** The joint
repin cleared the `links` collision — witnessed: `cargo update -w` in `mentci`
had failed outright with the `links = "meta-signal-criome"` refusal and now
resolves, with exactly one `kameo 0.20.0` in the lock. Clearing it uncovered
something larger that the early build-script failure had been masking.

Relayed from the repin subflow, which read the sources directly: **all four
contract crates in that chain emit only the strict encoded-name projection.**
`signal-criome` `b85fe340` declares `pub struct z2VdZ4(String)` and
`pub struct z2VUiL { pub field_0: z2VZMH, … }`; `signal-mentci` `293ea752`
declares `pub enum z2VYMA`, `pub struct z2VNJM`. Not one human-named contract
type exists under any name a consumer could write — `CriomeReply`,
`AuthorizationDenial`, `MentciRequest`, `PaneContent`, `ComponentSocketKind`,
`SignatureScheme` are all absent, and `signal-criome`'s `lib.rs` does not even
re-export `schema::lib::*`. `criome`'s 13,801 lines import roughly 150 such
names; `mentci-lib` about 30. The result is 163 errors in `criome` and 22 in
`mentci-lib`, and rustc never reaches `mentci`'s own code at all.

The repin subflow also corrected two things in its own brief, which this flow
had written from the prior subflow's report: `criome`'s main is `2f4dded8`,
not `2eb5050` — `2eb5050` is the ancestor that *performed* the half-finished
mass repin — and the joint repin needs **four** repositories, not two, because
`mentci-lib` pins `meta-signal-criome` too. It took a second lock for it.

The honest reading, and it is an inference this flow endorses: the contract
repair in the table above is real and does what it claims — it restores those
repositories' *build scripts*. The scratch consumer that verified it only
*pinned* the contracts; it never exercised their consumer surface, and that
surface does not exist. Reaching a green `mentci` needs a Datom-stack
`signal-criome` and `meta-signal-criome` authored first — ethos source,
ethos-zero generation, human-named types — and then a port of a 13.8k-line
daemon. That is repository-scale migration, not a repin, and it is not
something to start at the end of a night. **`mentci` is the one named
repository this flow could not land**, and it is recorded as such rather than
dressed up.

## 12. `persona` — the deepest port, one leg short

Relayed from the persona subflow, which held lock 1223 and released it before
reporting. `persona` 0.2.0 `9469b0a1` → **0.4.0 `651fe75f`** on
`f6db8d-datom-migration`; `main` verified still at `9469b0a1` by this flow's
own `git ls-remote`.

Four of the five gate legs are green: `cargo test --all-features` (75 passed),
`cargo fmt --check`, `cargo clippy --all-targets --all-features -D warnings`,
`cargo doc --no-deps --all-features`. The fifth, `nix flake check -L
--builders ''`, evaluates fully and builds every package and check **except
one**: `persona-message-daemon-stamps-origin-via-tap`, which fails with

```
message-write-configuration: decode Dotos request: expected ConfigurationWriteRequest to be a brace block
```

That check starts the real `message-daemon` built from `message` 0.11.1 and
decodes its output with persona's `wire-decode-message`. `message` is
unmigrated — `git ls-remote` shows only `main`, `messenger-thread-slot`,
`nota-dependency-rename`, `synchronizer`, no migrated branch. The subflow's
own inference, which this flow endorses: repairing the text form would move
the failure one step later, because persona's decoder now reads a bare
length-prefixed rkyv `signal_message::Query` while the 0.11.1 daemon writes a
`signal-frame` envelope over signal-message 0.8.1 — different bytes by
construction. The check is unpassable until `message` migrates onto
signal-message 2.0.1.

Counter-evidence that persona's own wire is sound, and it is the reason this
is recorded as a cross-repository blocker rather than a persona defect: the
subflow built persona's seven self-contained wire checks individually —
`wire-message-channel-round-trip`, `wire-stamped-submission-round-trip`,
`wire-inbox-query-round-trip`, `wire-chain-summary` and three rejection
witnesses — all green under the new envelope.

**Scale.** The `links` diagnosis in §9 had been masking the real work. Behind
it were **187 compile errors across 15 modules** plus the whole test suite —
persona's entire contract adaptation layer, not a call-site sweep. Deleted
outright: the `upgrade` crate (unresolvable — every dependency a branch pin,
written against meta-signal-upgrade 0.2.3 against a 2.0.1 main; persona now
owns its version state in `src/upgrade/` on signal-upgrade 2.0.1); `build.rs`
and the `schema-rust` build-dependency (schema-rust 0.17.0 deleted
`NexusDaemonShape`, `WorkingListenerTier` and the whole `build::Generation*`
API, so `src/schema/daemon.rs` stands as ordinary source and the freshness
gate is gone); `src/generated_contract.rs` and its 19 import sites;
the `message` dependency, which alone dragged in signal-harness 0.5.1,
signal-persona 0.3.1, schema-rust 0.15.1, protos 0.5.1, core-logos and
rust-logos; `dotos` entirely, manifest and lock, the whole text surface moved
to datom-codec; `signal-frame` as a declared contract; and the
`signal_channel!` envelopes in `transport.rs`, `supervision_readiness.rs`,
`persona_component_fixture.rs` and four `wire-*` binaries — both wires are one
request and one reply per connection, so exchange identity, lane and batch
were ceremony over a wire that never used them. Also two dead
dev-dependencies, two unreachable error variants, and a test that grepped
source text for forbidden words, which the `testing` skill forbids as a
change-detector. Graph result: **zero branch pins** in `Cargo.toml` and
`Cargo.lock`, exactly one copy of every contract, schema-rust and core-logos
gone.

**What legitimately survives.** `wire-router-client.rs` still speaks
signal-frame because signal-router 0.7.0 is unmigrated; signal-frame remains
in the lock only transitively, via sema-engine, signal-router and
triad-runtime. `sema-engine` and `triad-runtime` themselves remain: both are
load-bearing runtime scaffolds — the manager store's storage kernel and the
daemon's argv/binding surface — with no migrated replacement published. They
are not contracts, so the brief's deletion order does not reach them.

**A defect found and deliberately not fixed, recorded for whoever migrates
`spirit`.** `src/direct_process.rs` carries a hand-written mirror of spirit's
daemon configuration and rkyv-serializes it to a file the spirit daemon reads,
and it does not match: spirit decodes `signal_spirit::SpiritDaemonConfiguration`
(`socket_path`, `meta_socket_path`, `database_path`, `trace_socket_path`,
`authorization_mode`, `guardian_agent_configuration`) while persona writes nine
differently-named fields. The guard test
`constraint_spirit_launch_writes_engine_scoped_daemon_configuration` passes
only because it decodes with **persona's own mirror type** — it round-trips
persona against itself and proves nothing. This is silent corruption of
exactly the kind this migration exists to end. The subflow left it because
signal-spirit main is already 3.0.1 while `spirit` still pins the
pre-migration `b37fc963`, so encoding against either target now creates work
to undo. This flow agrees with that judgement and records the defect rather
than half-fixing it.

**Independent confirmation of the single-field note.** The subflow did not
take the brief's warning on trust: it added a round-trip test that prints what
the codec emits, and it printed `{ { /run/persona/manager.sock } { … } { … } }`
— `{ value }`, no head, exactly as warned. The flake now hands
`persona-write-configuration` that form, and every canonical text in persona's
tests is built by the codec that reads it back, none spelled by hand.

## 13. What this flow could not land, stated plainly

Two of the five named repositories did not reach `main`, and neither for a
reason inside itself:

- **`mentci`** — its contract chain (`signal-criome`, `meta-signal-criome`,
  `signal-mentci`, `meta-signal-mentci`) emits only the strict encoded-name
  projection. No human-named contract type exists for a consumer to import.
  Reaching green needs those contracts authored as Datom-stack ethos sources
  first, then a port of a 13.8k-line daemon. §11.
- **`persona`** — one nix check, blocked on the unmigrated `message`
  repository's wire. §12.

Both are pushed and verified on `f6db8d-datom-migration` so no work is lost
and the next flow starts from the port, not from the diagnosis.

## 14. A correction applied after the table was first written

The terminal subflow, on a second pass, corrected this flow's own table: it had
listed terminal's *before* sha as `71c1e721`, which is the `f6db8d-found-dirt`
commit this flow created, not the port's base. This flow verified the
correction rather than accepting it — `git merge-base --is-ancestor 71c1e721
e1d85788` is **false** while `061a36a1` is **true** — and the same mistake was
present for `introspect` (`03767b41` is its found-dirt commit; its real base is
`07556777`). `meta-signal-introspect`'s `eec60c42` checked out as a genuine
ancestor. Both rows are corrected above. The lesson is the flow's own: a
bookmark this flow set is not a base it built on, and a sha's provenance is
checked with `merge-base`, not recalled.

One thing left untouched deliberately, reported by that subflow and not
altered here: another subflow's in-flight repin of `terminal` onto a *newer*
wave (`protos 1febca78`, `datom-codec 09e2a9d5` 0.31.0, `signal-terminal
a3e4f96b`, version `0.3.1`) sits uncommitted in that repository's
`Cargo.toml`/`Cargo.lock`, building on this landing. Committing another
agent's unverified work onto `main` and reverting it are both wrong; it stays
as found. `main` at `e1d85788` is unaffected, re-verified after the edit
appeared.

## Sources

Every revision, version and branch state named in this report was re-read by
this flow directly against the real remotes with
`git ls-remote https://github.com/LiGoldragon/<repo>.git` and
`git show <sha>:Cargo.toml`, never taken from a subflow's claim. Gate results
are **relayed** from the subflow that held each repository's lock, except
`meta-signal-introspect`'s §8 fix and its gating test, which this flow wrote
and ran itself, and the `git ls-remote` verifications throughout.

- `/home/li/primary/flows/f6db8d/reports/datom-migration.md` — the method this
  wave follows: repin, regenerate, delete, fix what breaks.
- `/home/li/primary/flows/f6db8d/reports/removals.md`,
  `periphery-audit.md`, `consumer-sweep.md` — the inherited consumer list,
  which this flow re-derived rather than trusted (§3).
- `/home/li/primary/Vision/datom.md:239-243` — the psyche's warrant for
  deleting rather than shimming (§2), quoted verbatim there.
- `/git/github.com/LiGoldragon/meta-signal-terminal` at `a9b18ee8` — the
  exemplar target shape propagated into every dispatch.
- `/git/github.com/LiGoldragon/terminal`, `introspect`,
  `meta-signal-introspect` at branch `f6db8d-found-dirt` — the found dirt,
  preserved and pushed, never discarded (§1).
- CriomOS-home `systemd.user.services.*` — the enumeration behind the
  deployment-safety finding (§5).
- Subflow final reports, in this session's transcript: terminal, introspect,
  meta-signal-system, meta-signal-persona/signal-mind/signal-system, the
  mentci chain repair, the joint criome repin, and persona (lock 1223).

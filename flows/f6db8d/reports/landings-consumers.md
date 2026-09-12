# Landing the pushed consumer branches — and the substrate that moved underneath them

Subflow of main flow f6db8d, 2026-09-12, thread
`f6db8d14-1dfe-472d-914e-9c441f852834`.

Brief: land or finish five pushed branch families in dependency order —
`message`/persona, the mentci chain, router, the mirror contracts, and the
repository-ledger family — each under an Orchestrate lock, per the living's
"land the branches" and "go with your suggestions", with the flow's own
suggestion (`reports/stack-membership.md`) that everything moves to Datom and
never to dotos.

**Witnessed** means this flow read or ran it on this machine. **Relayed**
means a dispatched subflow reported it. Every revision, version and branch
state in the tables below was re-read by this flow directly with
`git ls-remote` and `git show <sha>:Cargo.toml`, never taken from a subflow's
claim.

## 1. The wave's governing fact: the producer front moved two majors mid-flight

The brief named four final producer heads. Three of them were superseded while
the wave was landing against them. Witnessed by `git ls-remote`:

| producer | brief's head | head at the cut | version |
|---|---|---|---|
| protos | `171b21f6` | `171b21f6` — unchanged | 0.30.1 |
| datom-codec | `627db67f` 0.26.3 | **`6dccc76b`** | **0.27.0** |
| ethos-zero | `de3d9928` 8.0.1 | **`b232d35e`** | **9.0.0** |
| signal | `8f9a0deb` 3.0.2 | **`7bcb0949`** | **5.0.0** |

`8f9a0deb` is an ancestor of `7bcb0949` (witnessed) — nothing was rewritten.
The two commits between them are `48ae17b` "Derive Composing; repin
datom-codec 0.27.0 and ethos-zero 9.0.0; bump 4.0.0" and `7bcb094` "Bound the
frame validator's nesting depth and refuse over-deep archives".

This flow **ruled to advance**, and the ruling was not a preference:

- The living ruled arity's return this morning, typed,
  `flows/f6db8d/vision/arity.md`: *"reintroduce arity where it makes most
  sense (sounds like it should be in compositional)."* The old front is the
  one standing against Vision — `reports/substrate-review.md` had recorded
  that removing ARITY contradicted `Vision/protos.md:85` and
  `Vision/datom.md:120,141` by the letter.
- The brief itself said to check `git ls-remote` at release time and prefer
  newer heads.
- Decisively: the sibling session was **already** repinning the estate to the
  arity-split substrate. Witnessed in `Observe.Locks` — claude-answers (1273),
  chroma (1284), horizon-rs (1285), signal-upgrade (1287), curriculum-deploy
  (1291), signal-domain (1294), clavifaber (1297), later signal-aggregator
  (1306). Since `signal` declares `links = "signal"` and cargo admits one
  package per `links` key per graph, a contract left on 3.0.2 would **fail at
  resolution** against every sibling-repinned consumer. Staleness here is not
  a debt owed later; it is immediate estate-wide incoherence.

**The cut line, spelled without a `.git` suffix:** protos `171b21f6` ·
datom-codec `6dccc76b` · ethos-zero `b232d35e` · signal `7bcb0949`.

Three workstreams independently verified that the 8.0.1 → 9.0.0 regeneration
changes **one token per type**, `Compositional` → `Composing`, and leaves
`examples/canonical.datom` **byte-identical**. The repository-ledger
workstream proved it by snapshotting `src/generated/signal.rs` before
repinning and diffing after — identical in both its repositories. **The wire
text does not move across this cut.**

Not chased further: lock 1298 `F6db8dFiniteDecimal` was held on datom-codec
when this wave closed, so `datom-codec 6dccc76b` may already be superseded.
Recorded so the next sweep knows exactly what to move.

## 2. What landed

All versions and revisions below witnessed by this flow against GitHub.

### Contracts on the cut

| repository | before | after | gate |
|---|---|---|---|
| signal-mirror | 2.0.1 `e60b7667` | **4.0.0 `9ac66bd4`** | five legs green, Prometheus |
| meta-signal-mirror | 2.0.1 `adf6be61` | **4.0.0 `cc3bd06e`** | five legs green, Prometheus |
| signal-repository-ledger | 0.1.0 `894335a0` | **0.5.0 `3c75a8b3`** | five legs green, Prometheus |
| meta-signal-repository-ledger | 0.1.0 `977c9e9b` | **0.5.0 `c69d5c4e`** | five legs green, Prometheus |
| signal-criome | 0.15.1 `feda1b1a` | **2.0.0 `5bfa61b5`** | five legs green, Prometheus |
| meta-signal-criome | 0.8.1 `5acfedaf` | **1.0.0 `8a150125`** | five legs green, Prometheus |
| signal-mentci | 0.4.2 `293ea752` | **1.0.0 `ba63ccfb`** | five legs green, Prometheus |
| meta-signal-mentci | 0.3.2 `b063a33d` | **1.0.0 `f491134e`** | five legs green, Prometheus |
| signal-persona | 2.0.1 `48118557` | **4.0.0 `5ed07a66`** | five legs green, Prometheus |
| signal-harness | 2.0.0 `49d16a31` | **4.0.0 `17bdd58b`** | green; build host unwitnessed (see §6) |
| signal-mind | 2.0.0 `7a08e51d` | **3.0.0 `5d5352b2`** | five legs green, Prometheus |
| signal-router | 0.7.0 `03ed6bc2` | **5.0.0 `f8fd1644`** | five legs green, Prometheus |
| meta-signal-router | `286ab234` | **4.0.0 `25a92c6d`** | five legs green, Prometheus |
| signal-message | 2.0.1 `2da9c6dd` | **3.0.0 `6b833f88`** | five legs green, Prometheus |
| meta-signal-message | 0.3.1 `d4c8d96c` | **0.6.0 `d9b219c2`** | five legs green, Prometheus |
| signal-introspect | 2.0.1 `8de16e35` | **3.0.0 `ccea830f`** | five legs green |
| signal-system | 2.0.0 `60392314` | **3.0.0 `5ae2944e`** | five legs green |
| meta-signal-system | 2.0.0 `17591d96` | **3.0.0 `18e9599e`** | five legs green |
| meta-signal-persona | 2.0.0 `88657088` | **3.0.0 `bfe4c964`** | five legs green |

### Consumers and runtime scaffolds

| repository | before | after | gate |
|---|---|---|---|
| message | 0.11.1 `38345dae` | **0.12.0 `6a52b9b8`** | five legs green, Prometheus |
| mentci-lib | 0.3.1 `ace52c8d` | **1.0.0 `dcb5fce8`** | five legs green, Prometheus |
| repository-ledger | `0580eff4` / mirror `4153fd84` | **0.4.1 `09617918`** on both | five legs green, Prometheus |
| triad-runtime | 0.7.0 `02cdd49d` | **0.10.0 `b7cffcb2`** | five legs green, Prometheus |
| sema-engine | 0.15.1 `27e814a7` | **0.16.0 `516f01fe`** | five legs green, Prometheus |

`sema-engine` is **exempt from the cut** — witnessed dependency enumeration:
blake3, rkyv, sema, signal-sema, thiserror, none of the four front producers.

### Branches deleted after landing

`f6db8d-datom-migration` in signal-mirror, meta-signal-mirror and mentci-lib;
both `f6db8d-nota-pins` branches in the repository-ledger family. All
deletions verified by `git ls-remote` returning no such ref.

## 3. What did not land, and why each is a boundary rather than a failure

**`router` — unmigrated, pristine at `f60d4e33`, nothing pushed.** Nine of its
producers landed on the cut. Router itself was not ported because the port is
20,500 lines and, critically, the front moved two majors mid-flight — a port
onto the stale pin set would have had to be redone in full. Deployment checked
independently twice: router has **no deployed unit**; `PersonaRouter` appears
only in two CriomOS test fixtures, and
`CriomOS-home/modules/home/profiles/min/message.nix:42` says verbatim "No
router daemon is deployed."

**`criome` and `mentci` — unlanded, branches preserved at `e644d251` and
`c9a111d4`.** The blocker is not size; it is that **the replacement is
undecided by the living**. Witnessed: criome's whole socket transport
(`src/transport.rs:13-16`) rests on `signal_frame::{ExchangeIdentifier,
ExchangeLane, LaneSequence, SessionEpoch, NonEmpty, Reply, SubReply,
RequestPayload, StreamEventIdentifier, SubscriptionTokenInner}`, and
`signal-frame` is being deleted estate-wide. `signal` 5.0.0 does **not**
replace it — its `src/frame.rs` provides a four-byte length prefix and nothing
else, and its own `src/lib.rs` says *"The protocol layered on top of the rkyv
archive is not decided; nothing here anticipates it."* `Vision/signal.md`
agrees: *"The protocol is to be decided."* Porting criome therefore means
**inventing the exchange, subscription and streamed-event protocol the living
has not ruled on**. The order is forced besides: `mentci` depends on `criome`
as a library crate, so mentci cannot compile until criome is ported. Scale
behind that blocker: 22,280 lines, 464 `Type::new(...)` call sites, 129
`.as_str()` sites, ~180 accessor calls, ~700 root-type occurrences.

**`repository-ledger`'s `build.rs` stays on `schema-rust`** — and this
corrects two earlier reports. Witnessed: `repository-ledger` is **not
blocked**. Its full gate is green, 17 tests pass, all Nix checks pass; only
`cargo update` fails. `nota-pins.md` and `stack-membership.md` both carried
the opposite claim. The migration was refused on a mechanical finding, not a
preference: **Ethos Zero cannot emit what that `build.rs` emits.** `File` has
exactly two variants, `Library` and `Signal`
(`ethos-zero/src/generation.rs:900,911`), and
`git grep -i 'daemon|nexus|listener|socket'` over its `src/` returns **one
hit, a doc comment**. What the script generates is 284 lines of triad-runtime
daemon scaffolding, not a Signal contract. This matches the living's own
framing of Ethos Zero as *"version 0, which means no daemon yet. No Nexus."*
There is no generation to migrate *to*, and the existing freshness gate works,
so trading it away for persona's disposition would be pure loss.

**`persona` — does not land; branch preserved at `651fe75f`, main at
`9469b0a1`.** Its gate cleared the blocker it was dispatched against and hit a
second one that had been hidden behind it.

The `message` blocker named in `terminal-migration.md` §12 is **gone** — the
`message` 0.12.0 migration cleared it, and
`persona-message-daemon-stamps-origin-via-tap` does not appear in the failure.
What fails is `persona-router-daemon-accepts-stamped-submission`, which starts
the real router daemon built from `router-0.11.0`:

```
thread 'main' panicked at src/bin/wire_router_client.rs:92:10:
read reply length prefix: Error { kind: UnexpectedEof, message: "failed to fill whole buffer" }
```

Mechanism, witnessed by this flow in `router` at `f60d4e33`:
`WorkingInput::decode` (`src/daemon.rs:300-309`) tries
`WorkingSignalMessageInput::decode` first, which calls
`SignalMessageFrame::decode(body)?` — a **signal-frame envelope** — and on
failure tries the router-observation arm, which requires an envelope too, then
returns **`signal_error`, the first arm's error**, discarding the second's.
Persona sends `request.signalize()`, a bare rkyv archive with a four-byte
prefix and no envelope. So both arms fail, router closes without replying, and
persona's client reads EOF.

Two corrections to the inherited record follow, both verified by this flow:

- **The check was already red at `651fe75f`, before this wave touched
  persona.** `git diff 651fe75f <closure> -- src/bin/wire_emit_message.rs` is
  **empty** — persona's sender did not change — and
  `git show 2da9c6dd:src/lib.rs | grep -cE 'ContractMarker|encode_request_frame|signal_frame'`
  returns **0**, so signal-message 2.0.1, persona's own pin at `651fe75f`,
  carried no envelope machinery at all.
- **The `signal-router` repin is not implicated.** The failing decode is the
  signal-*message* arm, tried first, and its error is the one returned. Any
  envelope-free sender fails against this daemon regardless of
  `signal-router`'s version.

The closure work was pushed to a **new** branch, `f6db8d-arity-front`
`09ee526c` — persona 0.5.0, verified on the remote — leaving
`f6db8d-datom-migration` undisturbed at `651fe75f`. No compatibility path was
added and `router` was not touched.

**The `--keep-going` enumeration: 106 of 111 checks green on Prometheus, five
red.** Three are the router framing mismatch above
(`persona-router-daemon-accepts-stamped-submission`,
`-rejects-unstamped-submission`, `-serves-inbox-after-submit`). The other two,
`persona-daemon-launches-nix-built-message-router-topology` and
`-prototype-topology`, fail at `test -S "$manager_socket"` after a ten-second
deadline **with zero output**, because under `set -eu` the script dumps the
daemon's logs only on the death path. **Their cause was not determined and is
left unknown** — whether a tight deadline on a loaded remote builder or a real
hang was not established. That the checks hide their own evidence is itself a
defect (§8).

**Persona's own wire is sound**, which is what makes this cross-repository
rather than a persona defect: all seven self-contained witnesses built green
under the cut — `wire-message-channel-round-trip`,
`wire-stamped-submission-round-trip`, `wire-inbox-query-round-trip`,
`wire-chain-summary`, `wire-malformed-bytes-decode-rejects`,
`wire-truncated-frame-decode-rejects`, `wire-wrong-frame-kind-decode-rejects`.

### One check was removed, and it needs stating plainly

`persona-message-daemon-stamps-origin-via-tap` — the very check
`terminal-migration.md` §12 built its whole account on — was **deleted**, with
the reason recorded where it stood. The justification, which this flow
verified independently rather than accepting:

`git grep -icE 'router_socket_path|router_socket|forward.*router'` over
`message`'s `src/` returns **nothing at `38345dae` and nothing at
`6a52b9b8`**; `git log --all -S router_socket_path -- src/` finds no commit
that ever added it; `src/engine.rs:62` at `38345dae` answers
`Input::SubmitStamped(_)` with `MessageRequestUnimplemented`; and commit
`1acb379` (v0.9.0) says it outright — *"router out of the local loop"*. So
**`message` has never contained router-forwarding code at any revision**, the
tap could never capture anything, and §12's wire-format diagnosis of this
check was wrong.

This flow accepts the removal: the check asserted behavior that does not exist
and could never pass, and building forwarding is a feature with open design
questions that must not be smuggled in as a fix for a red check. The
`wire-tap-router` shim was kept — it is the instrument, not the defect. **The
cost is recorded honestly: deleting it also deletes a standing statement that
router-forwarding is wanted.** Whoever takes up message/router forwarding
should know the intent existed and where it was expressed.

## 3a. Three of the four boundaries reduce to one question for the living

Stated this way because it is a better account of the remainder than "four
things did not land".

`persona` is blocked on `router`. `router`, `criome` and `mentci` are each
blocked on the same thing: **the protocol above the bare rkyv frame is
undecided.** Witnessed, `signal` 5.0.0's own `src/lib.rs`: *"The protocol
layered on top of the rkyv archive is not decided; nothing here anticipates
it."* `Vision/signal.md` agrees: *"Signal is portable rkyv plus whatever
protocol is standardized on top of it. The protocol is to be decided."*

Every one of those three consumers needs exchange identity, subscription and
streamed-event semantics that `signal-frame` used to supply and `signal` 5.0.0
deliberately does not. `signal-frame` is being deleted estate-wide. So the
work is not four ports; it is **one design decision, then three ports**.

`Vision/nexus.md`'s Routing section already says where part of the answer
lives — *"an enum that wraps the objects, held in the signal repository"* — so
the discriminator has a ruled home even though the protocol around it does
not. That is the narrowest form of the question: what, above the rkyv archive
and the four-byte prefix, does `signal` own?

The fourth boundary, `repository-ledger`'s `build.rs`, is unrelated and is
settled on its own evidence (§3).

## 4. The night's most important finding: cargo source identity is the pin string, not the commit

Proved independently, from three directions, by three workstreams.

`?branch=main#fd7909d1` and `?rev=fd7909d1` name the **same commit** and are
**two different cargo sources** — separate package instances, separate feature
resolution, mutually non-interchangeable Rust types.

- **Router**, witnessed: converting twelve `branch = "main"` pins to the exact
  revs its own lockfile already resolved — behaviorally a no-op — produced a
  `links = "signal-persona"` resolution failure, and then, with that left
  mutable, **31 compile errors** (`no method named to_nota`, `?` could not
  convert to `signal_frame::FrameError`) because the lock already held three
  `signal-frame` copies under three source spellings and a fourth stopped
  features unifying. The package set was byte-identical in name, version and
  sha. Router's main resolves today **only** by the accident that its mutable
  pin string matches its dependency's mutable pin string.
- **repository-ledger**, witnessed: pinning `signal-repository-ledger` to the
  rev its own lockfile already used produced **`E0308: mismatched types`**,
  because the meta contract still pinned it by branch.
- **The mentci chain**, witnessed in the pre-migration trees: `criome` and
  `mentci-lib` pinned `meta-signal-criome.git`, `mentci` pinned
  `meta-signal-criome` with **no suffix** — one commit, two cargo sources,
  under a `links` key that admits one. A resolution refusal waiting on the
  first graph holding all three.

**The escalation, measured by a router subflow:** converting a direct mutable
pin can buy **zero** protection while still splitting the graph, because the
crate usually also arrives *transitively* by another mutable pin. Measured in
`spirit`: pinning triad-runtime to `895d2e6b` yields 0.6.1 (by rev) **and**
0.8.1 (by branch) both in the lock; pinning to `02cdd49d` yields 0.6.1 (by
branch) **and** 0.8.1 (by rev) both in the lock. Either way a mutable copy
survives and moves on the next refresh. The shared transitive root there is
**`schema-rust`, itself pinned `branch = "main"`**, carrying triad-runtime
into harness, mind, persona-spirit, repository-ledger, spirit, spirit-judge,
upgrade and router alike.

**The rule this wave now operates under**, and it supersedes the
"convert every mutable pin to a rev" instruction this flow put in all five
briefs:

1. Source identity is the pin **string**, not the commit.
2. Converting a direct pin while the crate also arrives transitively by a
   mutable pin **splits** the entry and leaves the mutable copy mutable.
3. Pin conversion is therefore safe **only across a whole producer closure in
   one pass, rooted at the shared transitive root, in one identical spelling**.
   A half-converted graph is strictly worse than a fully-mutable one.

**The canonical spelling is `https://github.com/LiGoldragon/signal` — no
`.git`, no `signal-standard` alias.** Witnessed in signal-aggregator,
meta-signal-aggregator and aggregator, locking to
`git+https://github.com/LiGoldragon/signal?rev=…`. GitHub redirects
`signal-standard.git` to `signal.git` and both return byte-identical ref sets
— which is exactly what makes the two spellings dangerous rather than
harmless.

## 5. The frame: imported from `signal`, never vendored

The wave found the estate genuinely split. Witnessed by this flow, reading
each `main:src/lib.rs` and `main:Cargo.toml`: **five of seven** migrated
contracts declared their own `pub struct Signal<T>` with **no `signal`
dependency** — signal-persona, signal-harness, signal-mind, signal-message,
signal-terminal. Only signal-aggregator and signal-mirror imported it. This
flow ruled for importing **from two examples, with the majority against it**,
and only afterwards found the warrant.

The warrant is distilled Vision, `Vision/nexus.md`, "Routing":

> Signals cross the network through a router. The router tells signal types
> apart by an enum that wraps the objects, held in **the signal repository,
> which every component depends on**. That repository also holds what every
> signal needs in common — the handshake payload among it.

"Which every component depends on" rules that contracts depend on `signal`;
"what every signal needs in common" is what the frame is. The vendoring five
are drift. The in-repo comment presenting vendoring as the design
(`terminal` 0.3.0, `src/frame.rs`) is an agent's prose — the weakest written
psyche — not the living.

The de-fork was **proved, not asserted**: each de-forked contract gained a
test carrying *two contracts' frames through one transport function*, the
thing the vendored copies made impossible, and each was seen failing first
with `E0308` between the two `Signal` structs. The mirror workstream separately
reproduced the `links` collision in a scratch crate
(`cargo generate-lockfile` → "package `signal` links to the native library
`signal`, but it conflicts with a previous package").

`signal`'s own `Cargo.toml` names the canonical spelling in its `repository`
field and declares `links = "signal"` — the `links` key is what *enforces* one
shared frame per graph, which is the property a wire wants. It bites only when
consumers pin different revs, which is the mutable-pin disease, not a reason
to fork.

**Ten repositories still vendor the frame** (witnessed): signal-introspect,
signal-system, signal-upgrade, signal-spirit-judge, signal-terminal,
meta-signal-persona, meta-signal-introspect, meta-signal-system,
meta-signal-terminal, meta-signal-upgrade. That is a larger remainder than the
wave has recorded anywhere.

## 6. The estate is not yet co-resolvable

Witnessed at the time of writing: the mirror pair (4.0.0) and ledger pair
(0.5.0) and the router/mentci producers are on signal 5.0.0 `7bcb0949`; the
**aggregator trio** (signal-aggregator 0.8.0, meta-signal-aggregator 0.6.0,
aggregator 0.6.0) and the **lojix trio** (signal-lojix 5.0.0,
meta-signal-lojix 6.0.0, lojix 5.0.0) are still on 3.0.2 `8f9a0deb`. A graph
holding one of each fails on `links = "signal"` — witnessed:
`signal-mirror` 4.0.0 + `signal-aggregator` 0.8.0 still does not resolve, now
on version rather than spelling.

This is owned, not abandoned: the sibling session holds lock 1306
(`F6db8dSignalAggregatorComposing`) advancing signal-aggregator now, alongside
its seven consumer repins. This flow did **not** dispatch into it, to avoid
collision. Until every member reaches the cut, router's graph in particular
cannot resolve — it holds `signal-mirror` behind its `witness` feature
alongside `signal-router` and `signal-criome`.

**`spirit` carries 21 `branch = "main"` pins**, two of them on the mirror
contracts. The mirror workstream deliberately refused to convert two of
twenty-one, on the producer-closure rule: a partial conversion neither gates
green nor reduces the disease. It needs one actor doing all 21 against the
finished cut. `spirit` is also **deprecated** — the psyche marked it
2026-09-10 as "legacy semantic donor, not an active development or stack
migration target" (relayed).

**Tonight's producer work sharpened the disease where it remains.** Router
pins signal-persona, signal-harness and signal-mind at `branch = "main"`
(Cargo.toml:61,64,65); those mains are now 4.0.0, 4.0.0 and 3.0.0 while
router's lock still holds 0.2.0/0.3.0/0.8.0. Router still builds today, but
the gap its mutable pins span grew by three majors tonight. The same is true
of `harness`, `persona-spirit` and `spirit`. That is a cost of the path taken
and it argues for doing the router port soon.

## 7. Gate regimes — two, and they must not be conflated

The gate definition **changed mid-wave on the living's order**, and results
are labeled accordingly.

- **Before the cold-machine order**: the full five legs — `cargo test
  --all-features`, `cargo fmt --check`, `cargo clippy --all-targets
  --all-features -- -D warnings`, `cargo doc --no-deps --all-features`, and
  `nix flake check -L` on Prometheus. Every workstream reported using plain
  `nix flake check -L`; **`--builders ''` was used nowhere** — the mentci
  workstream confirmed that explicitly.
- **After it**: this machine stays cold. No local cargo or builds of any
  kind. The only gate is `nix flake check -L --max-jobs 0`, which runs those
  legs on Prometheus. Local nix and cargo processes were killed **by PID** by
  the coordinator; this flow killed nothing and ran no local build.

Everything in §2 except the last three rows was gated under the first regime
and is reported as obtained. A local green is **not** relabeled as a
Prometheus green.

**A standing caution about every "failed on exactly one check" claim in this
estate.** `terminal-migration.md` §12 reported that persona's gate
"evaluates fully and builds every package and check **except one**." Witnessed
correction: that was really *except the first one it hit*. `nix flake check`
stops at the first failure unless `--keep-going` is passed, and
`persona-message-daemon-stamps-origin-via-tap` was masking
`persona-router-daemon-accepts-stamped-submission` behind it. **No
single-failure claim in these reports is reliable unless `--keep-going` was
used**, and this wave's persona gate was rerun with it for exactly that reason.

One witness gap, volunteered by the subflow that caused it: `signal-harness`'s
`nix flake check` was piped through `tail -5`, losing the log, so the gate is
green but **which derivations ran on Prometheus is unwitnessed** for that run.

Two repositories have **no `flake.nix`** and therefore no nix gate available;
that is stated rather than papered over.

## 8. Defects found and not fixed

- **criome's `flake.nix` carries five `runCommand` grep checks over its own
  sources** — change-detectors the `testing` skill forbids. Two will rot on
  the migration: `criome-signal-criome-contract-boundary` (`flake.nix:123-130`)
  and `criome-authorization-slots-are-store-minted` (`flake.nix:141-150`),
  which forbids a constructor that ceases to exist, so the guard silently
  stops guarding. `signal-harness/checks/no-free-functions.sh` and
  `no-inherent-methods.sh` are the same shape, pre-existing.
- **`impl CanonicalBytes for ObjectDigest` (criome `src/language.rs:868`)
  becomes an impl on bare `String`.** All seven digest aliases are now
  `signal::ObjectDigest = String`, so the type-level distinction between
  digest kinds is gone. Only one impl exists, so nothing collides today — but
  this feeds BLS signing preimages. **Whether domain separation rested on that
  distinction was not determined.** Whoever ports criome must check.
- **`signal::ComponentKind` carries no `Mentci` variant.** Nothing in the
  chain needs it, so no local narrowing was declared to route around it; the
  gap is recorded in `meta-signal-mentci/ARCHITECTURE.md`. Adding it is a
  major in `signal`, which has spent two majors tonight.
- **`meta-signal-mirror` declares two unreachable contract types**
  (`ConfigurationWrite`, `ConfigurationArchivePath`) — reachable from no
  request or reply root, so they can never cross the wire. Its
  `ContentAddressing.[ Opaque SemaVersionedLog ]` carries retired "Sema"
  vocabulary in a wire-facing head.
- **Both mirror contracts and both ledger contracts use `String` where the
  Ethos intrinsic is `Text`.**
- **`cargo fmt --check` disagrees between the repo toolchain (1.89) and the
  Nix fmt leg (nightly 1.100)** — witnessed once in mentci-lib.
- **The `ethos` skill documents the Signal root as generating
  `Request`/`Reply`; ethos-zero generates `Query`/`Response`** — witnessed at
  `ethos-zero/src/generation.rs:917,924`. Curriculum was under another flow's
  lock (1231), so it was not edited.
- **`/git/.../ethos-zero/target/release/ethos-zero` is a live working-copy
  build under another flow's lock and moved mid-run**, producing one contract
  deriving `Composing` while three derived `Compositional`; `build.rs` caught
  it loudly. Never generate from that binary — build the pinned generator into
  a scratch clone.
- **`router` `f60d4e33`'s `Cargo.lock` carries `signal-frame` 0.3.0 at two
  sources at once** — `?branch=main#fd7909d1…` and `?rev=01676293…`. A live
  instance of §4's central finding sitting in an unmigrated repository, which
  is evidence the disease is not hypothetical anywhere it remains. Its
  `signal-message` is locked at 0.4.0 `95343930` through a `?branch=main`
  source, and `signal-frame`, `signal-message`, `signal-harness` and
  `triad-runtime` are all `branch = "main"` in its manifest.
- **`triad-runtime` 0.10.0 pins `kameo f491b45d` while kameo main is
  `3486e4f6`**, putting two kameo packages in persona's graph. Pre-existing at
  `651fe75f`; the fix is upstream in triad-runtime.
- **`persona`'s two topology checks hide their own evidence** — logs are dumped
  only on the death path under `set -eu`, which is why their failure cause
  could not be determined.
- **`message` and `persona` pin `signal-message`/`meta-signal-message` at
  revisions that are now main's *parents*** — main moved by docs-only
  `UPGRADES.md` commits. Witnessed as gate-neutral: the derivation path is
  byte-identical before and after
  (`7di8iv1xylakqar5r3x2md1sglr707a4-message-test-0.12.0.drv`), because the
  crane source filter excludes `.md`. Recorded rather than chased.
- **`triad-runtime` is pinned at 0.9.0 `2abec178` in `message` and 0.10.0
  `b7cffcb2` in `persona`** — separate cargo graphs, so no conflict, but an
  untidiness flagged rather than hidden.
- Carried forward unfixed from earlier reports and still standing: persona's
  `src/direct_process.rs:36` `mod spirit_daemon_configuration`
  spirit-configuration mirror, whose guard test round-trips persona against its
  own mirror type and proves nothing. Evidence that it is a mirror and not the
  contract: repinning persona's entire closure did not break it.

## 8a. One change that is not a port

`message`'s durable store schema moved **3 → 4 with the additive list left
empty**, so a v3 store **fails closed** rather than being re-stamped and
misread. Every durable record embeds producer types whose archived rkyv layout
changed across the cut. The subflow made this call deliberately and said so:
the alternative is silent corruption of a production store — and `message` is
the one repository in this wave with a deployed unit. A test was written and
**seen failing** when v3 was put back in the additive list.

This is the only change in the wave that is a design decision rather than a
port, and it is flagged because it changes what a deployed daemon does with
existing data. Nothing was deployed; the CriomOS-home pin was not advanced.

## 9. This flow's own faults

- **It ruled the frame question from two examples when five of seven contracts
  did the opposite**, and only sought the disconfirming evidence after ruling.
  The ruling survived on origin rather than repetition, but the order of
  operations was wrong — seek disconfirming evidence before ruling, not after.
- **It twice inferred ownership from co-location and was twice wrong.** It told
  the mentci workstream the competing writer in `signal-criome` was most likely
  its own nested delegate; it was the router workstream on its own critical
  path. It then attributed a stubbed `--impure --override-input` nix gate to
  the message workstream; the process tree showed it descended from PID 184327,
  a **separate `claude` process** gating CriomOS-home, sharing only the
  session-keyed scratchpad. Both times the subflow checked the parentage and
  was right. Ownership is established by lock and by process tree, never by
  "who else would be here".
- **It instructed the wave to spell the signal pin `signal.git`**, which by the
  wave's own central finding would have created a second cargo source and a
  `links` collision. Caught by a subflow and corrected; no workstream landed it.
- **Its brief's exemplar wording** ("the rkyv `Signal`/`Signalizable`/
  `ByteViewable`/`Restorable` surface in `src/lib.rs`") read as an instruction
  to vendor the frame, and pointed at `meta-signal-terminal`, which does vendor
  it. Corrected in all five workstreams after a subflow flagged the mismatch.
- **Its brief asserted `meta-signal-message` was already 2.0.0 on the Datom
  stack.** It was 0.3.1 on schema-rust, dotos and signal-frame. Caught by this
  flow before dispatch.
- **Its brief scoped the mentci contracts at two**; four were required. The
  evidence — 165/158 references in criome, 22/55 in mentci, 2/3 in mentci-lib,
  144 distinct human names — confirms `terminal-migration.md` §11 was right.
- **It offered `--builders ''` as a fallback** in all five briefs, against the
  coordinator's later note. Never taken by any workstream.
- **It relayed `terminal-migration.md` §12's persona diagnosis as if settled**,
  including its account of `persona-message-daemon-stamps-origin-via-tap` as a
  wire-format mismatch. Both halves were wrong: the check could never pass
  because `message` has never had router-forwarding code, and "failed on
  exactly one check" was an artifact of no `--keep-going`. This flow should
  have required the enumeration before carrying the single-failure claim into
  five briefs.

## 9a. Corrections this wave makes to earlier reports

Each verified by this flow, not relayed:

| report | claim | correction |
|---|---|---|
| `terminal-migration.md` §12 | persona's gate fails "on exactly one check" | on the *first* check; no `--keep-going`. Five are red, three router-framing and two undetermined |
| `terminal-migration.md` §12 | the tap check fails on wire format | it can never pass — `message` has no router-forwarding code at any revision |
| `terminal-migration.md` §11 | the mentci chain needs two contracts fixed | four; 144 distinct human names imported from the two criome contracts alone |
| `datom-migration.md` / brief | `meta-signal-message` is 2.0.0 on the Datom stack | 0.3.1 on schema-rust, dotos, signal-frame, with name-table hashed type names |
| `datom-migration.md` | signal-mirror/meta-signal-mirror are "red on the signal-standard→signal rename" | both branches were strict *ancestors* of already-green mains; the rename redirects and cannot break anything. Original redness unreproducible, cause unknown |
| `nota-pins.md`, `stack-membership.md` | `repository-ledger` is blocked behind the schema-rust wall | not blocked: 17 tests pass, all Nix checks pass; only `cargo update` fails |
| `nota-pins.md` | signal-repository-ledger's main diverged from its mirror | already resolved; `meta-signal-repository-ledger` has **no mirror at all** |
| `aggregator-migration.md` | a bare variant spelling a declared type is a generator defect | ruled Vision (`flows/564f55/vision/archive-ethos.md`); the collision is the ethos author's error |


## 10. Deployment safety

Witnessed independently by this flow: the deployed CriomOS-home user units are
`active-network-widget`, `aggregator-daemon`, `chroma-daemon`,
`codex-artifact-gateway`, `codex-remote-control`, `criomos-ui-priority`,
`listener`, `message-daemon`, `orchestrate-nexus`, plus spirit's and niri's.

Of every repository in this wave, **only `message` has a deployed unit**, and
it was migrated and pushed but never deployed. `repository-ledger` and
`router` were each confirmed to have none. Nothing was deployed, no running
service was touched, and this flow killed no process — by pattern or
otherwise. The one nix process left alive is `nix-daemon`, a system service.

## Sources

- Brief of main flow f6db8d to this subflow, 2026-09-12.
- `flows/f6db8d/reports/terminal-migration.md` §11, §12 — the mentci and
  persona boundaries this wave inherited; §11's four-contract claim confirmed.
- `flows/f6db8d/reports/aggregator-migration.md` — router's prior diagnosis
  and the six producers it named.
- `flows/f6db8d/reports/nota-pins.md`, `stack-membership.md` — the rejected
  dotos direction, and the two claims about `repository-ledger` being blocked
  that §3 corrects.
- `Vision/datom.md:239-243` — "Everything moves to Datom … no Dotos file
  remains"; read by this flow (witnessed). Distilled Vision.
- `Vision/nexus.md`, "Routing" — the warrant for importing the shared frame
  (§5); read by this flow (witnessed). Distilled Vision.
- `Vision/signal.md` — "The protocol is to be decided" (§3); witnessed.
- `flows/f6db8d/vision/arity.md`, `designPractice.md` — the living's typed
  rulings of 2026-09-12; witnessed.
- `flows/564f55/vision/archive-ethos.md` — "If a variant is already defined as
  a type somewhere else, then that other type becomes the data it carries";
  witnessed. The bare-variant behavior is ruled Vision, **not** a generator
  defect, and this flow corrected all five briefs on that point.
- `orchestrate 'Observe.Locks'` before and throughout; locks 1232–1247,
  1281–1283, 1295–1296, 1299–1300, 1323–1326 and the sibling set 1226/1227/
  1231/1234/1273/1284/1285/1287/1291/1294/1297/1298/1306 observed.
- `git ls-remote` and `git show <sha>:Cargo.toml` against
  `https://github.com/LiGoldragon/<repo>.git` for every revision and version
  in every table; `ps -eo pid,ppid,args` for the process-tree attribution in
  §9 — all witnessed by this flow.
- Subflow final reports, in this session's transcript: message/persona, the
  mentci chain, router, the mirror contracts, the repository-ledger family.
  Gate results are **relayed** from the subflow that held each lock, except the
  revision, version, branch, spelling and process-tree verifications above.

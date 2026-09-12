# Orchestrate: shared frame, Datom-free Nexus, no migration tool, Nexus authority

Flow f6db8d, subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834`, 2026-09-11
night. Work carried out on `main` in each repository, under Orchestrate locks,
from clean workspaces cloned from the shared checkouts. Nothing was deployed. The
running Orchestrate service was used only as its own lock service, through
`Observe.Locks`, four `Lock`s and four `Release`s on its ordinary socket, as
an ordinary client.

Throughout: **witnessed** means this flow ran it and read the result;
**relayed** means another flow or agent reported it and is named.

---

## 1. Released revisions

| repository | version | revision |
|---|---|---|
| `signal` | 3.0.1 | `2276ec4227a08526cb667f475827368d02accc72` |
| `signal-orchestrate` | 3.0.1 | `c783b72706575451fe4416d1598b2adf9859d333` |
| `meta-signal-orchestrate` | 3.0.1 | `707f4cb82963c02b4e6aabd4d8e17d7b7bb81da9` |
| `orchestrate` | 0.32.0 | `054ce581b22edf3373f5a4ae95b93d48b0ed0bd9` |

The three contracts were released twice: `3.0.0` carried the substance, and
`3.0.1` is a pin-only follow-up taken when `ethos-zero` main moved again mid-
work. Generation is byte-identical across both generator revisions, so nothing
was regenerated and no public surface moved between them.

Substrate pinned by all four, at the revisions their mains carried at release
time:

| repository | version | revision |
|---|---|---|
| `protos` | 0.30.0 | `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb` |
| `datom-codec` | 0.26.1 | `18129314966c5043ee659de452b6f976fa319b21` |
| `ethos-zero` | 8.0.0 | `da58504926dabe4680bb7863d812846b0f845d86` |
| `nexus` | 0.1.1 | `a84bfa960c0d5c02d30048c4bbbc67dfef79a67c` |
| `sema-engine` | 0.15.1 | `27e814a721439af67721c530d48b4d2101141f74` |

Witnessed in `orchestrate/Cargo.lock`: exactly one `ethos-zero`, one
`datom-codec` and one `protos` entry. The "two `ethos-zero` revisions in one
lockfile" and "two `datom-codec` entries at different revisions" defects the
audit recorded at `1bc55af1` are closed.

**Two corrections to the record.**

The brief says *"regenerate contracts from ethos-zero 7.x"* and also *"repin to
the newest revisions on their mains at release time"*. Those instructions came
apart during the night: `ethos-zero` main moved `c8a68369` (7.0.0) →
`212b3590` (7.0.1) → `da585049` (**8.0.0**) while this work was under way, a
sibling flow holding lock 1125 over it. The repin instruction is the operative
one — it is what keeps one generator revision in the estate — so 8.0.0 is
pinned. Generation was checked against `da585049` for every one of the five
ethos files in scope — both contracts, the shared taxonomy, both client
libraries — and is byte-identical to what `4695ee0c` (6.1.6) produced; at
`c8a68369` and `212b3590` the equality was established by the contracts'
own build scripts, which assert the committed projection against a fresh
generation and fail the build otherwise. So nothing turns on the choice
beyond the pin itself.

Consequently the three contract repin commit messages name the generator as
"Ethos Zero 7.0.1 da585049". The **revision is correct** and is what pins;
the **version label is wrong** — `da585049` is 8.0.0. The messages were not
rewritten, because they were already pushed and rewriting shared history to
fix a label is a worse trade than recording the correction here.

The `3.0.0` and `0.32.0` bumps are breaking; the `3.0.1` follow-ups are pin-only
patches. No compatibility path exists anywhere in the change: a client built
before this release is not understood by the Nexus, and that is the intent.

## 2. What was found already done

Two of the four ordered items had been partly landed by a sibling flow between
the runtime audit and this work, and the audit's revisions are no longer main.
Witnessed by fetching each origin:

- `signal` exists as a repository (`626e407b`, 2.0.0) and already owns the
  big-endian frame, the portable `Signal<T>` and the shared taxonomy.
- `signal-orchestrate` main had moved to `7408fb6f` (2.0.0), taking its frame
  and kinds from `signal` and already declaring ordinary
  `Configure.OrchestrateNexusConfiguration`, `MetaConfigureDone.Boolean`,
  `ConfigurationReceipt`, and
  `ConfigurationRejectionReason.[ MetaConfigureOccurred InvalidConfiguration ]`
  — the vocabulary the WIP branch had begun.
- `meta-signal-orchestrate` main had moved to `d8e03501` (2.0.2), with
  `ReverseMetaConfiguration` and `OrdinaryConfigurationReopened`.
- `orchestrate` main was still `1bc55af1` (0.31.0) and pinned the *old*
  `signal-orchestrate 1.0.4` and `meta-signal-orchestrate 1.0.0`.

So the ordinary and meta contracts were ready and unconsumed. Nothing in the
Nexus used them.

## 3. The dirty shared checkouts

Witnessed at `/git/github.com/LiGoldragon/orchestrate`: `HEAD` detached at
`1bc55af1` (main, 0.31.0) with ten modified files, and
`git diff flow857335-nexus-lifecycle-wip -- .` empty — the working tree is
byte-identical to the uncompiled WIP commit `cf0dfef2`. Confirms the runtime
audit §9.9.

`signal-orchestrate` and `meta-signal-orchestrate` are **now clean**, at the
new mains above; the dirt the audit recorded there has been superseded.

The `orchestrate` dirt was left exactly as found. All work was done in
`git clone --shared` workspaces under this session's scratchpad, pushed to
`origin/main` directly. Anyone building from the shared `orchestrate` checkout
still builds the WIP, not the release; that remains for the living to clear.

## 4. The four ordered items

### 4.1 The frame length prefix

Confirmed the defect before changing it. `signal/src/frame.rs` writes
`u32::to_be_bytes` and reads `u32::from_be_bytes`, and its header says why:
Orchestrate hand-rolled the prefix, Lojix took `triad-runtime`'s codec, the two
disagreed, and big-endian was kept. Orchestrate at `1bc55af1` wrote
`to_le_bytes` at three production sites —
`crates/orchestrate-nexus/src/transport.rs:140,161`,
`crates/orchestrate/src/main.rs:164,169`,
`crates/orchestrate-meta/src/main.rs:164,169` — and at five test sites, which
is why its suite could not catch it: fixture and subject shared the mistake.

Done: Orchestrate now frames through `signal` and owns no framing. Deleted
`SignalPayload`, `PayloadReading`, `PayloadWriting`, both clients' byte-level
`Exchanging` bodies, and the five `MAXIMUM_SIGNAL_BYTES` redefinitions;
`FrameCapacity::default()` is the one capacity. Every test — the two client
boundary tests and the live two-socket test — now writes and reads with
`signal`, so a byte-order divergence fails rather than cancelling out.

A new test states the property rather than assuming it:
`live_nexus::a_little_endian_prefix_is_not_the_shared_frame` sends a valid
`Observe.Locks` archive behind a little-endian prefix and asserts no frame
comes back, then sends the same query through the shared crate and asserts it
*is* answered. The second half is what makes the first half discriminating: a
test that only asserts silence would pass against a Nexus that answers
nothing at all.

Precisely what was witnessed of this test: its first run failed — the Nexus
reads the byte-swapped prefix as 16 777 216, finds it past the 8 MiB frame
capacity, and drops the connection, so the socket read returns
`ConnectionReset` rather than an empty body. The assertion was corrected to
accept either outcome, since both mean no frame came back, and the test then
passed. It was **not** run against the pre-change little-endian Nexus; that
Nexus is gone from every workspace, and the claim it would have answered rests
on reading `transport.rs:140` at `1bc55af1`, not on an experiment.

### 4.2 The Nexus is Datom-free as built

Reproduced the audit's finding on the new pins, witnessed:

```
cargo tree --workspace --edges normal -i protos
  → orchestrate-nexus v0.32.0 is a dependent,
    via signal-orchestrate[datom] → datom-codec → protos
cargo tree --package orchestrate-nexus --edges normal
  → no datom-codec, no protos
```

The cause is not the manifest, which was always clean; it is that
`flake.nix` built with `cargoExtraArgs = "--workspace"`, and Cargo unifies
features across the members of one build. The clients enable the contracts'
`datom` feature, so the contracts were compiled with Datom on and the Nexus
linked them.

Done: the package is two Cargo resolutions rather than one.
`packages.nexus` builds `--package orchestrate-nexus`; `packages.clients`
builds `--package orchestrate --package orchestrate-meta`;
`packages.default` is their `symlinkJoin` and still carries every binary the
previous package did, less `orchestrate-store-migrate`. Test, clippy and doc
checks stay on `--workspace`, since the test binaries are not the artefact.

The witness is the `datom-free-nexus` check, which runs `cargo tree` on the
*same* resolution the Nexus package is built from — `--package
orchestrate-nexus` — and fails if `datom-codec` or `protos` appears. It also
resolves the client configuration and fails if Datom is *absent* there, so a
run where the command has silently stopped resolving anything cannot pass as
a green result.

### 4.3 The migration was written for the wrong generation

The reasoning, and what was kept.

The audit established (witnessed by it, re-read by me in the sources) that
`5f016531` — the deployed 0.30.0 — and `1bc55af1` — the released 0.31.0 —
carry textually identical `StoredConfiguration`, `StoredLock` and
`StoredAllocator` types and identical family constants
(`orchestrate_configuration_v2`, `locks_v2`, `lock_id_allocator_v2`), and that
in *both* revisions the tuple `Previous*` types read the **pre-0.30** families.
`orchestrate-store-migrate` required exactly one row in those pre-0.30
configuration and allocator families (`MigrationSourceInvariant`); 0.30.0
carries the identical `open()` guard that refuses to start if they are
non-empty, and 0.30.0 started. So the tool would have refused the very store it
was written for, and the elaborate migrate-validate-promote runbook addressed a
transition that had already happened on 2026-09-08.

Deleted: `crates/orchestrate-nexus/src/bin/orchestrate_store_migrate.rs` and
its `[[bin]]` block; `MigratesPreviousSignal` and `migrate_previous_signal`;
`PreviousConfigure`, `PreviousLock`, `PreviousStoredConfiguration`,
`PreviousStoredLock`, `PreviousStoredAllocator`; the three `PREVIOUS_*_TABLE`
constants; the `PreviousSignalMigrationRequired`, `MigrationSourceInvariant`
and `MigrationTargetNotEmpty` refusals; and the two tests that exercised them
(`migration_source_failure_preserves_v1_records`,
`previous_signal_rows_require_an_explicit_migration`) with their `Historical*`
fixture types. The README and ARCHITECTURE paragraphs that described the tool,
and ARCHITECTURE's false claim that "the normal open path never reads old tuple
records", went with them.

Kept, as what a real 0.30-or-0.31 to 0.32 cutover needs — `store::cutover`, one
module, one read. Locks and the allocator carry across untouched, their
families being identical. The one thing that changed is where configuration
lives: this release moves it into the standard Nexus metadata tree together
with the record of whether the privileged Configure occurred, so a store that
still has the separate `orchestrate_configuration_v2` row seeds its metadata
tree from that row on first open rather than from the executable's defaults,
and the row is retracted in the same commit. After one open the reader is never
reached again, and it is not registered at all on a store that never had the
family.

Also kept, deliberately: `orchestrate-upgrade-preflight` and the pre-0.25
`active_path_locks` guard. Reasons, in order of weight: it is a *refusal*, not
a migration — no PathLock row is ever materialised as a Lock, because a
PathLock has no Flow and inventing one would attribute a coordination fact to
a flow that never claimed it; it is a different generation from the one the
order names; and `CriomOS-home/checks/orchestrate-service-path/default.nix`
asserts the binary is present in the package, so removing it would break an
evaluation of a repository this flow must not edit and would require a deploy
to repair. It was improved rather than removed: the count now returns zero
without registering the family when a store never had it, so a fresh store's
durable catalogue carries only its own three families.

### 4.4 The Nexus authority failures

The audit names seven: three in its §3.2 and four more in §3.3. Mapped against
this release, so "which of the seven remain" has an unambiguous answer.

| # | audit | the failure | state after 0.32.0 |
|---|---|---|---|
| 1 | §3.2 | the engine is `Arc<Mutex>` + Tokio, not Kameo | **remains** |
| 2 | §3.2 | no durable record that the meta Configure occurred | **closed** |
| 3 | §3.2 | no ordinary Configure, no meta reversal | **closed** |
| 4 | §3.3a | Observe is one-shot; the shape is the forbidden polling one | **closed** |
| 5 | §3.3b | the meta socket is privileged in name only | **closed** |
| 6 | §3.3c | the `nexus` library is unused, and the ontology was not designed first | **half** — the library is used; the ontology does not exist |
| 7 | §3.3d | no router, no shared signal repository | **half** — the repository exists; the wrapping enum and handshake do not |

Four closed, one open, two half. Detail below.

**Implemented.**

**#5 — mode and peer check on the meta socket.** Both sockets used to bind
identically — no mode, no umask control, no peer check — and were
`srwxr-xr-x` live. The meta socket is now bound `0600` and the ordinary one
`0660` (mode set after bind, since a Unix socket takes its permissions from
a umask the Nexus does not own). A meta connection is answered only when
`SO_PEERCRED` reports the socket's own owning user; anyone else receives
`PeerRefused.PeerRejection { PeerUserId }` and the connection closes. The
refusal is vocabulary, not a dropped connection, which is why
`meta-signal-orchestrate` needed a contract change. The owning user is read
from the socket file the Nexus itself just created, so there is no second
source of truth to drift from, and no `unsafe` anywhere (the crate forbids
it). The same admission check runs on the ordinary socket too, where the
authority admits whoever the filesystem let through — so the decision is
uniform across sockets and neither arm of the rule is a path nothing takes.
Witnessed by `live_nexus::the_privileged_socket_is_bound_for_its_owner_alone`
and `transport::socket::tests` — with the gap in §5 on the refusing branch.

**#2 and #3 — a durable record of whether the privileged Configure occurred,
and the ordinary Configure it gates.** There was
none: `StoredConfiguration` was two strings, and `HandlesMeta` treated an
unchanged `Configure` as a no-op, so even a marker keyed on "a Configure
arrived" would not have fired. The store now keeps the standard Nexus
metadata tree — `nexus::ConfigurationState<StoredConfiguration>`, so the
lifecycle rule is the shared library's and not a second copy — in
`orchestrate_nexus_metadata_v1`. Ordinary `Configure` is accepted while the
record is unset and refused with `MetaConfigureOccurred` afterwards;
`ReverseMetaConfiguration` on the meta socket unsets it. Every transition
persists before it answers.
Witnessed by `configuration_authority.rs`: the full open→closed→reopened
cycle, survival across a restart, and refusal of an unbindable
configuration on both surfaces.
This also closes the third named failure, **no ordinary Configure and no
meta reversal**.

**#4 — Observe as a subscription.** The signal contract carries it without new
vocabulary, and that is the point. `Observe` no longer answers once and
closes: the Nexus writes the state on open and one further `Observed` frame
for every later change, on the same connection, until the peer closes it.
The subscription **is** the connection — no token, no `Unwatch`, no
registry of handles to leak. That is deliberately unlike Lojix, whose
`SubscriptionToken` and `Unwatch` vocabulary the audit found to be a counter
increment and an echo with no subscriber registry behind them; a vocabulary
that promises what the implementation does not do is worse than none.
`NexusCore` announces the whole observation rather than a delta, so a
subscriber joining mid-stream and one that has followed from the start hold
the same value. A subscriber that falls past the backlog is re-sent the
current state, which is the value it would have converged on.
Witnessed by `live_nexus::observe_delivers_the_state_on_open_and_every_later_change`,
seen failing once with announcements suppressed before being trusted. The
socket read is bounded at ten seconds so a frame the Nexus never sends fails
the test instead of hanging the harness.

**#6, first half — the `nexus` library is now used.**
`nexus::ConfigurationState` and `nexus::Configurable` carry the
configuration lifecycle; the rule is stated once, in the shared library,
and Orchestrate states it nowhere.

**Not implemented, and why.**

**#1 — Kameo.** `Vision/nexus.md`: *"The engine inside a Nexus is driven by Kameo
actors. The standards of their use are still to be designed. Arc-Mutex is
permitted."* The standards are still undesigned, and the WIP branch that
`shutdown-runtime.md` said would begin the Kameo processor declared
`kameo = "0.20"` and used it nowhere. Writing actors against undesigned
standards would be inventing the standard by accident, in the repository
least suited to owning it. What was done instead is to make the swap cheap
and local: `NexusCore` is the only thing that touches the store, `Applies`
and `Announcing` are the whole surface, and the transport decides nothing.
Becoming an actor is a change of `core.rs` alone.
**Remains open.** It needs the Kameo standards first.

**#6, second half — the universal ontology designed before implementation.**
`nexus` 0.1.1 is
131 lines covering the configuration lifecycle only — no effect or `Apply`
trait, no actor or dataflow ontology, no socket or signal surface — and it
postdates both runtimes it was meant to found by four and a half hours. That
ontology does not exist and cannot be written from inside one component: it
is a design task for the `nexus` repository, and `Vision/nexus.md` places it
before implementation, not after. This release names the concept in the one
place it could — `Applies<Entering>`, once per contract, following Vision's
*"An object enters a Nexus for the effect… the name is open, Apply liked"* —
so that when the shared trait is designed there is one site to move.
**Remains open**, in `nexus`, not here.

**#7 — no router, no wrapping enum, no handshake payload.** The `signal` repository now exists and holds the
frame, the portable `Signal<T>` and a cross-component taxonomy, which is
part of what Vision's "Routing" paragraph asks for; the wrapping enum that
lets a router tell signal types apart, and the handshake payload, are not
there. Orchestrate has no edges to any other Nexus today, so it could not
have driven the design of either.
**Remains open**, in `signal`.

One further gap, not among the seven, recorded because this release made it
visible: **the default CLIs do not follow the subscription.** They take one
positional Datom and print one value, so `orchestrate 'Observe.Locks'` ends at
the state on open — which is what the orchestrate skill documents and what
callers depend on. A CLI that streamed would need an output protocol for a
sequence of typed values that has not been designed. Recorded as a known
limit, with the reason, at the `Exchanging` implementation in both clients.

## 5. Gates

Per repository, full local gate: `cargo test`, `cargo fmt --check`,
`cargo clippy --all-targets -- -D warnings`, `cargo doc`, and
`nix flake check -L --builders ''` — the last on the final content of each
repository, after every edit, so no green result is from a superseded tree.

| repository | `nix flake check -L --builders ''` |
|---|---|
| `signal` 3.0.0 | all checks passed |
| `signal` 3.0.1 | all checks passed |
| `signal-orchestrate` 3.0.0 | all checks passed |
| `signal-orchestrate` 3.0.1 | all checks passed |
| `meta-signal-orchestrate` 3.0.0 | all checks passed |
| `meta-signal-orchestrate` 3.0.1 | all checks passed |
| `orchestrate` 0.32.0 | all checks passed, including `datom-free-nexus`: *"orchestrate-nexus links neither datom-codec nor protos as built"* |

Two `orchestrate` runs failed before the passing one and are recorded because
a reader should not have to infer a clean first attempt. The first failed
`checks.fmt` — the new `store/` and `transport/` modules were untracked, so
crane's `cleanSource` did not see them and `cargo fmt` could not resolve the
module tree; fixed by snapshotting the working copy. The second failed
`checks.clippy` with *"the argument `--workspace` cannot be used multiple
times"* — `workspaceArgs` already carried `--workspace` in `cargoExtraArgs`
and the clippy check added its own; fixed by giving clippy, doc and build
`commonArgs`.

Three of the new tests were seen failing under a deliberate defect before
being trusted: the subscription test with the announcement in `NexusCore`
suppressed (it then fails on the bounded read rather than hanging, which is
why the read is bounded); the cutover test with the carried configuration
replaced by the executable defaults; the `PeerRejection` round trip against a
different user id. The little-endian refusal test failed on its first run for
the reason recorded in §4.1 and was corrected, which is a weaker witness —
stated as such there.

The refusing branch of the peer check needs care, because a single-user test
process cannot exercise it end to end: refusing the Nexus's own user is
exactly what the Nexus must not do, and obtaining a second uid needs privilege
this session was not given. What is witnessed is the rule rather than the
whole path —
`transport::socket::tests::the_privileged_authority_admits_its_owner_and_nobody_else`
asserts that `SocketAuthority::Privileged` admits its owner and refuses every
other user including root, and was seen failing under a deliberately
permissive rule. The step from that rule to a closed connection —
`SO_PEERCRED` → `admits` → `PeerRefused` — is exercised only on its admitting
branch, by every live test. **Recorded as a real gap: the refusing wire path
has no end-to-end witness.**

The socket modes are asserted twice: as the rule
(`the_privileged_socket_mode_grants_nothing_beyond_its_owner`) and against a
live Nexus's socket files
(`live_nexus::the_privileged_socket_is_bound_for_its_owner_alone`).

### New durable gates

- `orchestrate/checks.datom-free-nexus` — `cargo tree` on the Nexus
  resolution the package is built from.
- `orchestrate/checks.configuration-authority` — the ordinary/meta
  configuration lifecycle and its durability across a restart.
- `orchestrate` `live_nexus` gained the socket modes, the subscription, and
  the little-endian refusal.
- `orchestrate` `store::cutover::tests` — a 0.30/0.31-shaped store opening as
  0.32 and carrying its configuration and Locks.
- `signal/tests/dependency_boundary.rs` no longer repeats pinned versions and
  revisions; it reads the pin from the manifest and asserts the resolved graph
  agrees, and asserts each of `datom-codec` and `protos` resolves to exactly
  one version. It was a change-detector that had to be edited on every repin;
  it is now a graph assertion that survives one.

## 6. What remains

Ordered by what a later flow would want first.

1. **The `orchestrate` shared checkout is still dirty** with the WIP
`cf0dfef2`, now three releases behind main. Anyone building from
`/git/github.com/LiGoldragon/orchestrate` builds the WIP. Left untouched as
ordered; it needs the living's word, since discarding it discards whatever
that flow intended to finish.

2. **0.32.0 is not deployable without CriomOS-home changes**, and was not
deployed. `CriomOS-home/flake.nix:138` still pins `5f016531` — **0.30.0**,
not 0.31.0 — and `checks/orchestrate-service-path/default.nix:74` asserts a
binary named `meta-orchestrate`, while the package has built
`orchestrate-meta` since 0.31.0. That is not a regression of this release;
it is the unresolved Vision conflict this flow already put to the living
(`Vision/orchestrate.md` says *"meta-orchestrate"*, `Vision/nexus.md` says
*"The meta CLI is named component-meta"*). Nothing here should be deployed
until the living settles the name.

3. **Kameo** — open, and correctly so: the standards of actor use are
undesigned, and `nexus` is where they belong. `core.rs` is the only file
that would change.

4. **The universal actor-and-dataflow ontology** — open, in `nexus`.
`Applies<Entering>` names the concept locally so there is one site to move.

5. **The router, the wrapping enum, the handshake payload** — open, in
`signal`. Orchestrate has no edges to drive their design.

6. **The default CLIs do not follow the subscription** — they print the state
on open and exit. A streaming CLI needs an output protocol for a sequence
of typed values that has not been designed.

7. **The two client `main.rs` files remain near-duplicates** (~190 lines each,
differing in the contract, the socket variable and three strings). The
defect this mattered for is gone — framing now comes from `signal`, so a
mistake cannot double — but the CLI scaffolding is still written twice. A
shared client library would be a fourth crate and was outside this brief.

8. **`sema-engine` has a real subscription surface**
(`subscribe`, `SubscriptionSink`, `SubscriptionDelta`) that this release
does not use; announcements are a `tokio::sync::broadcast` in `NexusCore`.
That is sound while the Nexus is the single writer, and it keeps the
change stream where the ontology puts it. Worth revisiting when the actor
design lands.

## 7. Locks

Acquired 1126 `OrchestrateFrameAndAuthority`, 1127
`SignalOrchestrateEthosSevenRepin`, 1128 `MetaSignalOrchestrateEthosSevenRepin`,
1129 `SignalSharedFrameRepin`, all on flow `f6db8d`, each over the repository
root it edits. All four released after the pushes; each returned `Released`
with the complete Lock.

Lock 1125 `EthosZeroProtosDatomCodecRepin` was already held by a sibling over
`ethos-zero`; this flow only pinned that repository's published revisions and
never edited it. The two repin names say "Ethos Zero 7.x" because that is
what the brief said; see the correction in §1.

The shared checkouts were not updated and are now behind their pushed mains
(`signal` at `626e407`, `signal-orchestrate` at `7408fb6`,
`meta-signal-orchestrate` at `d8e0350`, `orchestrate` at `1bc55af1` with its
ten dirty WIP files). The three contract checkouts are clean and a `git pull`
brings them current; `orchestrate` needs the dirt resolved first, which is
§6.1.

No Bead was delegated to this subflow, and none was opened or closed. The one
open Bead in `orchestrate` — `orchestrate-de0`, *"ProtoformStack merged on
main everywhere, orchestrate documented, and deployed"* — was left alone: its
completion requires a deployment this flow is forbidden to perform.

## Sources

- `Vision/nexus.md`, `Vision/signal.md`, `Vision/orchestrate.md`, and the
  `nexus`, `nexus-rationale` and `orchestrate` skills — read in full, this
  flow.
- `flows/f6db8d/reports/runtime-audit.md` §§3.1, 3.2, 3.3, 4.1, 4.2, 9.7, 9.9 —
  relayed; §3.1's feature-unification finding and §9.9's dirty-checkout finding
  independently re-witnessed by this flow on the current revisions.
- `flows/f6db8d/reports/unused-survey.md` §2.3 (`orchestrate-store-migrate` is
  dead estate-wide) and §4.2 (the endianness split, the three `datom-codec`
  pins) — relayed; the endianness claim re-witnessed against
  `signal/src/frame.rs` and the three Orchestrate production sites.
- `signal/src/frame.rs`, `signal/src/transport.rs`, `signal/src/portable.rs` —
  read, this flow.
- `nexus/src/configuration.rs` — read in full, this flow.
- `sema-engine/src/lib.rs`, `src/engine.rs`, `src/mutation.rs`,
  `src/subscribe.rs` — read for the API surface, this flow.
- `CriomOS-home/flake.nix:138` (pins orchestrate `5f016531`, 0.30.0) and
  `CriomOS-home/checks/orchestrate-service-path/default.nix:72-90` — read, not
  edited, this flow.
- `orchestrate 1bc55af1` and `flow857335-nexus-lifecycle-wip cf0dfef2` — read
  by `git show` and `git diff`, this flow.
- The Orchestrate lock service — `Observe.Locks`, four `Lock`s, four
  `Release`s, as an ordinary client.

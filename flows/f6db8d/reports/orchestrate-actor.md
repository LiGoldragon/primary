# Orchestrate 0.34.0: the actor boundary, the socket claim, and the carried store

Subflow of main flow `f6db8d`, 2026-09-12. Brief: implement items 3 and 6 of
`reports/design-decisions.md`, and item 8 as far as it bears on Orchestrate, in
`orchestrate` from a clean clone under a lock; make any change the decisions
need in the `nexus` library first, under its own lock; every behaviour with a
test seen failing first, including an isolated-daemon test on scratch paths;
full gate; bump; push main.

Marks used below: **witnessed** — this thread ran the command or opened the
file and the text is what came back; **relayed** — a named report says so, not
re-verified here; **this flow's inference** — reasoning of this thread, not a
ruling and not an observation.

## What landed

| repository | from | to | revision |
|---|---|---|---|
| `nexus` | 0.1.1 `a84bfa9` | 0.2.0 | `1fedfb6d` |
| `nexus` | 0.2.0 | 0.3.0 | `4ed2696c` |
| `orchestrate` | 0.33.1 `c8a2882` | 0.34.0 | `2266b06e` |

No wire change. `signal-orchestrate` 3.0.2 and `meta-signal-orchestrate` 3.0.2
are pinned exactly as 0.33.1 pinned them, and 0.33.1's two clients speak to
this Nexus unchanged. **Witnessed**, `git ls-remote` on 2026-09-12: every
producer this repository pins is at its remote head except `datom-codec`,
whose head `6dccc76` is ahead of the pinned `627db67`. That is the sibling's
arity release; this landing does not touch it, because the Nexus links neither
`datom-codec` nor `protos` and no contract was regenerated here.

## The design as implemented

### Nexus Core is the actor, and it owns the store

`NexusCore` implements `kameo::Actor` with `Args = OrchestrateStore`. It holds
the store **by value**. The `Arc<Mutex<OrchestrateStore>>` is gone, and with it
the possibility of anything else in the process reaching the store: the only
way in is a message. That is decision 6's Rule 1 exactly — one unit of
consistency, one actor, and the boundary drawn at the state rather than at the
connection.

Sockets and sessions stay tasks (Rule 2). The listener loop is one task holding
both `UnixListener`s; each accepted connection is a spawned task holding a
clone of `ActorRef<NexusCore>`. A session that fails ends its own connection
and is recorded against the socket it arrived on; the listener keeps listening.

Authority is the message type the session can construct (Rule 3). A session
serving the ordinary contract can only ever build an `OrdinaryQuery`; the meta
operations are unreachable from it. Nothing checks a flag.

The mailbox is bounded at 64 (Rule 4). Announcement fan-out is the existing
`broadcast::Sender`, which never makes the core await a subscriber — a
subscriber that falls behind is told it lagged and re-reads the current state.

Two new message types carry what `Announcing` used to: `Attending`, whose reply
is the opening observation **and** the subscription receiver taken in one step
of the core, and `Overtaking`, which re-reads for a subscriber that lagged.
Taking both halves of a subscription in one actor step is a correctness gain
the decision did not ask for and the previous shape could not have: 0.33.1
subscribed and then read the opening state under two separate lock
acquisitions, and its own comment conceded that a change committed between them
would be delivered twice.

`FoundedCore` pairs the `ActorRef` with the `JoinHandle` of the task that owns
the actor. It exists because the store is now inside the actor: a restart, or
anything else that must open the store again, has to wait for that task to end,
not merely for the reference to go away. `Founding::settled` is stop-then-wait.

### Sockets are claimed, not probed

`SocketClaim` takes an advisory `flock` on `<socket>.claim` beside the socket,
before the socket is touched, and holds it for the life of the process.
Whatever is at the socket path is then this process's to remove, because
nothing else holds the claim. A second Nexus is refused by name with
`TransportError::SocketAlreadyActive`.

Both paths are claimed before either is bound, so a Nexus that loses the race
for its second socket has not already taken the first away from whoever won it.

`rustix::fs::flock` is the call. It is safe, and the workspace forbids
`unsafe_code`; `libc::flock` would have required lifting that.

### The observed record and the copy guard

`nexus::Situation` records, once both binds succeed, the absolute path of the
store file actually opened, the socket paths actually bound, and the process,
boot and host that bound them. It lives in its own sema family,
`orchestrate_nexus_situation_v1`, and is written and never read as
configuration.

On open, before the store hands back any socket path, a recorded situation
whose `store_path` differs from the path just opened is a copy, and
`OrchestrateStore::open` returns `StoreError::CarriedStore { recorded, opened }`
naming both. The Nexus exits.

Of the decision's two offered responses, refusing to start is the only correct
one, and this is **this flow's inference** rather than the decision's argument:
binding the built-in defaults instead does not help in the witnessed case,
because a copy opened by the same user on the same machine derives *the same*
built-in defaults — the production paths — and would take them anyway.

### The meta socket's default name

`META_SOCKET_FILE` is now `orchestrate-meta.sock`, following the living's
ruling (`flows/f6db8d/vision/metaCli.md`, typed 2026-09-12: *"meta cli names is
<component>-meta"*). The ruling is about the CLI; extending it to the socket
file is **this flow's inference**, taken under the standing authorisation in
`flows/f6db8d/vision/designPractice.md`, and it is deploy-visible only for a
fresh store — see **What a deploy now needs**.

### `SIGTERM` and `SIGINT`

0.33.1 built a shutdown channel and bound its sender to a name it then never
used (`let _shutdown_sender = shutdown_sender;`), so nothing ever sent on it:
`serve_until` could not return, and every stop was a kill. This is a defect
found while implementing, not one the decisions name. `Termination` now turns
either signal into that shutdown.

The stop drops sessions first, so that how long it takes to return depends on
nothing a peer does — an open subscription and a peer that connected without
speaking would both otherwise hold it — and then stops the core gracefully and
waits on its task, so that by the time serving returns the store is closed and
both claims are the next process's to take. What that order costs is named
under **What is still owed**.

### The per-contract refusal (decision 6's D-9 defect)

`Refusing` is implemented on the response types: `MetaResponse::peer_refusal`
names the peer, `OrdinaryResponse::peer_refusal` is `None`. `Session::admitted`
is generic over the response type, so a session can only ever write its own
contract's frame.

## Deviations from the decisions, and why

**1. `Applies<Entering>` is deleted rather than kept beside `Message`.** The
decision says `Applies` becomes `Message`; item 8 separately plans to lift
`Applies` into `nexus` at 0.4.0. Implemented as the decision says. The
consequence is worth recording: `kameo::Message<T> { type Reply; fn handle }`
**is** `Applies<Entering> { type Effect; fn apply }`, from the library the
psyche already ruled is the actor layer. Item 8's step 3 is therefore moot for
any Nexus that is a Kameo actor — lifting `Applies` into `nexus` would put a
second name on a kind the actor library already defines. That is **this flow's
inference**, offered to the living, not acted on beyond this repository.

**2. The ordinary contract gained no `PeerRefused`.** The decision's test
wording ("a refusal on the ordinary socket carries an *ordinary* contract
frame") implies adding the variant to `signal-orchestrate`. It was not added.
The ordinary authority admits whoever the filesystem let through — that is what
*ordinary* means — so the variant would be wire vocabulary that can never be
sent, against the `nexus` skill's closed-vocabulary rule. `Option<Self>` says
honestly that this contract has nothing to name a refused peer with, and the
exception is noted at the site. The defect the decision found is closed either
way: a session can no longer write a meta frame onto a socket bearing the
ordinary contract. A contract that later gains a refusing socket gains the
vocabulary at the same time.

**3. No `ObserveBinding` → `BindingObserved` on the meta contract.** The
decision lists this under wire impact so the meta CLI can answer "where is it
actually listening". The brief's scope for item 3 names three things — the
observed record, the copy guard, the flock — and not this. Adding it means a
`meta-signal-orchestrate` regeneration and release, which would couple this
landing to the in-flight `datom-codec` arity release. It is owed and is listed
under **What is still owed**.

**4. No store UUID; the guard compares paths.** The decision recommends a
creation-time UUID and calls the path comparison "the cheap version". The path
comparison is what landed. The UUID as the decision describes it does not
actually add detection: a UUID minted at store creation is carried by the copy
unchanged, so comparing the store's UUID against the record's UUID — both
inside the same file — always matches. Detecting a same-path copy on another
machine needs a comparison against something *outside* the store; `Situation`
records the host and boot identity so that comparison is available, but nothing
guards on them, because guarding on the host would refuse to start a Nexus
whose machine was merely renamed. **This flow's inference**, and the residual
gap is named under **What is still owed**.

**5. Sessions are not a Kameo-supervised child set.** The decision says the
`JoinSet` "becomes a supervised child set". Sessions are tasks, not actors, so
Kameo supervision does not apply to them. What landed is what the decision
actually wanted from it: the two `eprintln!` calls became a `SessionEnding`
value that names the socket the session arrived on, recorded by the listener. A
session that *panicked* cannot name its socket — the value carrying the name
went with it — and says so rather than guessing.

**6. The Kameo fork is untouched.** The decision recommends crates.io 0.22.2
and dropping the fork, and marks A19 the living's call. `kameo = "0.22"` from
crates.io is what this repository now depends on, matching the implementation
plan and lojix's existing patch-out. Nothing here removes or changes the fork,
and A19 is not decided by this landing.

**7. The runtime is two-threaded.** 0.33.1 used `new_current_thread`. The core
is one actor and its durable step is synchronous, so on a single-threaded
runtime that step stalls the listeners as well as the mailbox. Two workers: one
for the durable step, one that keeps accepting. This is Rule 4's intent reached
without `spawn_blocking`, which cannot be used here because a handler's `&mut
self` cannot cross that boundary.

## The tests, and what each was seen failing against

Every test below was written before the behaviour existed and run once to see
it fail. **Witnessed** in this thread:

| test | first failure seen |
|---|---|
| `nexus/tests/authority.rs` (2) | `no Permissive in the root`, `no SocketAuthority in the root` |
| `nexus/tests/situation.rs` (4) | `no Situation in the root`, `no Situating`, `no Situated` |
| `tests/carried_store.rs` (3) | `no Situates in store`, `no variant named CarriedStore`; then `RecordNotFound` on the first `situate` |
| `tests/socket_claim.rs` (5) | `unresolved imports ... Claiming, SocketClaim` |
| `tests/stopping.rs` (1) | with `self.core.settled().await` removed: `the stopped Nexus let its store go: Engine(Sema(Database(DatabaseAlreadyOpen)))` |
| `live_nexus.rs::removing_the_socket_file_...` | with the claim replaced by a file-existence probe: `the path is still held by the Nexus serving on it, socket file or no socket file` |
| `live_nexus.rs::a_nexus_refuses_to_serve_a_store_carried_from_somewhere_else` | no `CarriedStore` existed to be named |
| `live_nexus.rs::a_terminated_nexus_stops_cleanly_...` | no signal handling existed; a `SIGTERM`ed Nexus did not exit successfully |
| `session.rs::a_refused_peer_on_the_ordinary_contract_is_never_sent_a_meta_frame` | no `serve_one_ordinary` and no `Refusing` existed |

`live_nexus.rs` is the isolated-daemon suite — twelve tests, five of them new
here. They start the real
`orchestrate-nexus` executable with `XDG_STATE_HOME` and `XDG_RUNTIME_DIR`
pointed at a `tempfile::tempdir()`, exchange real `signal` frames over its two
real sockets, and stop it by the process id the test's own `Child` holds —
never by a name or path pattern, because a scratch Nexus and a deployed one are
the same executable. The second-Nexus helper is bounded at ten seconds and
kills by the id it holds if the child does not exit, since a second Nexus that
*does not* exit is exactly the defect under test and an unbounded wait would
hang rather than report.

One test was written, seen pass against both the correct and the incorrect
implementation, and **deleted**: a `graceful_stop.rs` asserting that queued
`tell`s survive a graceful stop. With a bounded mailbox, `tell().await`
completes only when there is room, so by the time the last one is sent the
actor has already drained the rest, and `kill()` passed the assertion too. It
confirmed nothing and was replaced by `stopping.rs`, which drives the real
transport and *is* a witness.

## The gate

**Witnessed.** `nix flake check` on `orchestrate`, 45 checks including the
seven pre-existing test checks and the three new ones — `socket-claim`,
`carried-store`, `stopping` — plus `fmt`, `clippy -D warnings`, `doc` with
`RUSTDOCFLAGS=-D warnings`, and `datom-free-nexus`: **all checks passed**.
`nix flake check` on `nexus`: **all checks passed**.

Both were invoked with the Prometheus remote builder configured
(`--builders 'ssh-ng://prometheus x86_64-linux - 32 1 big-parallel,benchmark,nixos-test,kvm'`).
Both runs reported `cannot build on 'ssh-ng://prometheus': error: failed to
start SSH connection to 'prometheus'` and fell back to building locally, so
**both green results are local ones**. `nix store info --store
ssh-ng://prometheus` answered `Version: 2.34.6, Trusted: 1` at the start of
this thread, so the builder is configured and was intermittently unreachable
during these runs rather than absent. Infrastructure reports are ground either
way — green is green, wherever it ran — but the remote builder was in practice
not used, and that is worth someone looking at.

Both were run twice: once before the last three comment-only edits, and once
on the exact tree that was pushed. Both runs were green; the recorded result is
the second.

`datom-free-nexus` still passes with `kameo` and `rustix` added: the Nexus
links neither `datom-codec` nor `protos` as built, and the clients still link
both.

## What a deploy now needs

Relayed from `AGENTS.md` and `UPGRADES.md` as written in this landing; **not
deployed by this thread**, which touched no live service, socket or store.

1. **Bump the `orchestrate` input in CriomOS-home**, rebuild, and
   `systemctl --user restart orchestrate-nexus`. A sibling may have repinned
   CriomOS-home to 0.33.1; this is a breaking bump they will re-pin.
2. **No store migration and no wire change.** The situation family is new and
   empty in an existing store; the first start under 0.34.0 writes it for the
   path the store is already at.
3. **Two new files appear in the runtime directory**: `orchestrate.sock.claim`
   and `orchestrate-meta.sock.claim`, mode `0600`, empty, not sockets. Any
   `tmpfiles` or cleanup rule that sweeps `$XDG_RUNTIME_DIR/orchestrate-nexus`
   must leave them alone while the service runs.
4. **The restart is now graceful.** The Nexus stops on `SIGTERM`, finishes the
   work it has taken, and releases its store and both claims before exiting
   successfully — so `systemctl restart` no longer waits out `TimeoutStopSec`
   and then `SIGKILL`s.
5. **The deployed store keeps `meta-orchestrate.sock`.** The socket paths live
   in the metadata tree, so the new default name reaches a fresh store only.
   Nothing outside the Nexus needs changing for the existing deployment. To
   move the deployed meta socket to the new name, meta-`Configure` both paths
   and restart — and note that the wrapper supplying `ORCHESTRATE_SOCKET` and
   anything else naming the old path must move in the same step.
6. **Do not relocate the store file.** A store opened anywhere other than where
   it records having been bound refuses to start. The remedy stated in the
   error is to open it where it records itself, or remove it.
7. **Witnessed, unrelated to this landing but in the way of a deploy**: the
   installed `orchestrate` client on this host accepts a multi-word Lock reason
   in curly quotes (`“…”`) and rejects guillemets with
   `Corporate(..., Arity(4, 5))`, while this repository's `AGENTS.md` states the
   opposite — guillemets accepted, curly quotes refused. The installed client is
   therefore an older generation than 0.33.1. **Witnessed** against a 0.34.0
   client built here and a scratch Nexus on temporary XDG roots:
   `Lock.{ A f6db8d [ /tmp/x ] «two words» }` answers
   `Locked.{ 1 A f6db8d [ /tmp/x ] «two words» }`, and the same reason in curly
   quotes answers `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }` —
   exactly the reverse of the installed client. **Deploying 0.34.0 therefore
   flips the delimiter every flow is currently typing.** The `orchestrate`
   skill's copyable example uses guillemets and would start working; the
   curly-quote form in use today would stop. The skill must move in the same
   step as the deploy, or every Lock with a multi-word reason breaks.

## What is still owed

- **`ObserveBinding` → `BindingObserved` on the meta contract**, so the
  situation record can be read by a client or a human rather than only compared
  internally. A minor bump on `meta-signal-orchestrate`, and the reason the
  decision's "what a client or a human reads to find the running Nexus" is not
  yet true.
- **A recovery path for a deliberately relocated store.** The refusal is
  correct and it is a dead end: the record lives inside the store, and the
  Nexus that would let you change it will not start. Neither the decision nor
  this landing designs the way out. This wants the living.
- **The same-path-different-machine copy.** `Situation` records host and boot
  identity; nothing guards on them, because a renamed machine would then be
  unstartable. Whether that trade is right is a question, not a finding.
- **A peer mid-request when the Nexus is stopped.** Sessions are dropped
  before the core is stopped, so that how long `serve_until` takes to return
  depends on nothing a peer does — an open subscription, or a peer that
  connected and said nothing, would otherwise hold it. The cost is that a peer
  whose request the core had already committed may lose the reply and have to
  ask again. Letting request sessions drain while dropping subscriptions is the
  fix; it was not built, because the drain is a race this thread could not
  witness deterministically, and untested behaviour is worse than a named
  limit.
- **Separate mailboxes or admission control for the two sockets.** The decision
  recommends it as a follow-on: one pathological ordinary client filling the
  64-slot mailbox can lock out the admin path. Not urgent while the ordinary
  socket is `0o660` on a single-user machine; unchanged here.
- **Item 8's remaining lifts** — `Applies` (see deviation 1), `Announcing` plus
  the cursor-bearing subscription, and the daemon shape — are untouched. Only
  `Permissive` (nexus 0.2.0) and `Situated` (nexus 0.3.0) were lifted, which is
  what bears on Orchestrate.

## Sources

All witnessed by this thread on 2026-09-12 unless marked otherwise.

- `flows/f6db8d/reports/design-decisions.md` §3 (lines 511-754), §6 (1196-1455),
  §8 (1807-2017) — the decisions implemented here, and the source of every
  quotation of a decision above.
- `flows/f6db8d/vision/designPractice.md` — the living's standing
  authorisation for design judgement where Vision is imperfect.
- `flows/f6db8d/vision/metaCli.md` — the living's ruling, typed 2026-09-12,
  that the meta CLI is `<component>-meta`.
- `orchestrate` at `7b965a0` (0.33.1 `c8a2882` plus a bead-filing commit), a
  clean clone from `git@github.com:LiGoldragon/orchestrate.git` — the state
  every "0.33.1 did X" statement above is read from.
- `nexus` at `a84bfa9` (0.1.1), a clean clone from
  `git@github.com:LiGoldragon/nexus.git`.
- `git ls-remote` on `signal-orchestrate`, `meta-signal-orchestrate`, `signal`,
  `ethos-zero`, `datom-codec`, `protos`, `sema-engine`, `nexus`, `kameo` — the
  producer-head comparison in **What landed**.
- kameo 0.22.2 source in the local cargo registry — `Actor`, `Message`,
  `Spawn`, `PreparedActor`, `ActorRef::stop_gracefully`, `SendError`,
  `Reply for Result<T, E>`, and the bounded-mailbox default of 64.
- rustix 1.1.4 source — `fs::flock` is safe and behind the `fs` feature.
- `signal-orchestrate/ethos/signal.ethos` and
  `meta-signal-orchestrate/ethos/*.ethos`, read from clean clones — the
  ordinary contract has no `PeerRefused`; the meta contract has one.
- `cargo test --offline -p orchestrate-nexus`, `cargo fmt --check`,
  `cargo clippy --workspace --all-targets -- -D warnings`, and
  `nix flake check` with the Prometheus remote builder — the gate.
- `orchestrate 'Observe.Locks'` and `systemctl --user is-active
  orchestrate-nexus` after the stray-process cleanup — the live service was
  untouched throughout.

## Released revisions

- `nexus` 0.2.0 — `1fedfb6d` (socket authority lifted)
- `nexus` 0.3.0 — `4ed2696c04a1aa064e9573e3b1f197b140c7644e`, `main` on
  `git@github.com:LiGoldragon/nexus.git`, confirmed by `git ls-remote` against
  the real remote URL
- `orchestrate` 0.34.0 — `2266b06e56c3af885317f9c086a55293c7d414b8`, `main` on
  `git@github.com:LiGoldragon/orchestrate.git`, confirmed by `git ls-remote`
  against the real remote URL

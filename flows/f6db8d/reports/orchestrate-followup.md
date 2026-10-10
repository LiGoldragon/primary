# Orchestrate follow-up: the cutover authority, the refusing peer, and what the versions shipped

Flow f6db8d, subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834`, 2026-09-11
night. Scope: the eleven defects of `reports/orchestrate-review.md`, restricted
to those that are code in `orchestrate`, `signal-orchestrate` and
`meta-signal-orchestrate`, plus the UPGRADES record each contract owes.

Throughout: **witnessed** means this thread ran it and read the result;
**relayed** means another flow or agent reports it and is named. Work was done
in `git clone --shared` workspaces under this session's scratchpad, pushed to
`origin/main` directly; no shared checkout was touched, no service was started
or stopped, and no deploy was performed. The live Orchestrate Nexus was used
only as its own lock service, as an ordinary client.

## 1. Released revisions

| repository | version | revision | wire |
|---|---|---|---|
| `orchestrate` | 0.33.0 | `3926ba353f90369ef665f144b376e6596d93561a` | unchanged |
| `signal-orchestrate` | 3.0.1 (unchanged) | `45ff2d4105c31028373d2b4fd789a13db071d437` | unchanged |
| `meta-signal-orchestrate` | 3.0.1 (unchanged) | `969c7d2d59396d76e4bcb195eda8c5ca88147f4c` | unchanged |

The two contract commits are documentation only. Per the versioning rule a
docs-only change that is not runtime-visible takes no bump, so both crates
remain 3.0.1 — the same public surface as the released 3.0.1, at a new
revision. `orchestrate` takes a minor: its store behaviour changed, its wire
did not, and 0.32.0's clients speak to it unchanged.

## 2. The high defect that was code: D-4

**What the review found.** After the cutover of a 0.30.0 store,
`meta_configure_done` is `False`, so `Vision/nexus.md` makes `Configure`
accessible on the ordinary socket, and an ordinary peer can repoint both socket
paths; the running instance keeps its bindings and the next restart obeys the
new ones, stranding every client. Witnessed by the review against a real
0.30.0-written store.

**What the brief proposed, and where it is wrong.** The brief's premise — *"a
store that carried a configuration row was configured by the privileged path in
its generation"* — does not hold as stated, and the difference matters enough to
record. Witnessed by reading `5f016531:src/store.rs:551-563`, the deployed
0.30.0: on first open a store with no configuration row is **asserted with the
executable's defaults**, unconditionally. So the presence of a row proves only
that the store was opened, never that a meta `Configure` arrived. The literal
question Vision's record asks — *"whether the meta Configure was ever done"* —
is unanswerable for a carried store.

**What Vision requires.** `Vision/nexus.md`, "First configuration", in full:

> A Nexus keeps a standard metadata tree. In it a type records whether the meta
> Configure was ever done; that record is reversed only on the meta socket, and
> while it is unset Configure is accessible on the ordinary socket.

The record's authority function is to hold open a bootstrap window, and the
window belongs to a Nexus that has never been configured by anyone. 0.30 and
0.31 had **no ordinary `Configure` at all** — witnessed in
`5f016531:src/store.rs`, whose ordinary request enum is `Lock`, `Release`,
`Observe` and nothing else. Every value a carried configuration row can hold
therefore came from the privileged path: the executable's own constant, or a
meta `Configure`. The ordinary bootstrap window was never open in that store's
life, and re-opening it at cutover would grant an authority the store never
had. So the cutover records Configure as done — for the reason the record
exists, not for the literal fact, and the distinction is written into
`store::cutover`'s header rather than smoothed over.

**The change.** `store::mod::SeedsMetadata::seed_metadata` now seeds a carried
configuration through `nexus::Configurable::meta_configure` rather than
`from_default`; a store with no previous configuration family is untouched and
still seeds open. One `match`, in the one place a store's metadata tree is ever
created.

**Tests, three, each seen failing first.**

- `store::cutover::tests::a_previous_generation_store_carries_its_configuration_and_its_locks`
  — its assertion was inverted, from "the cutover cannot claim one" to the
  record being set. Seen failing against the old seeding.
- `store::cutover::tests::a_carried_store_refuses_ordinary_configure_until_the_meta_socket_reopens_it`
  — new: an ordinary `Configure` against a carried store answers
  `ConfigurationRefused.MetaConfigureOccurred`, the refused configuration does
  not take, and only `ReverseMetaConfiguration` reopens it. Seen failing
  against the old seeding, where the repointing was accepted.
- `live_nexus::a_resumed_previous_generation_store_keeps_ordinary_configure_shut`
  — new, and the answer to *"test it against a 0.30.0-shaped store"*: it writes
  a store in the deployed 0.30.0 shape (the three families, schema labels and
  record fields of `5f016531`), starts the **real `orchestrate-nexus`
  executable** on it, and drives the whole thing over the sockets — the carried
  Lock is served, the ordinary repointing is refused, the meta reversal reopens,
  and the ordinary surface then accepts. The store's configuration row is what
  the Nexus binds, so the test also witnesses §3.4's binding-from-the-store
  behaviour as a fact.

This is one step weaker than the review's own witness, which ran the *deployed
0.30.0 binary* to write the store. That cannot be a durable test: the
repository cannot depend on an executable of a previous generation. The shape
equivalence is asserted by reading both sources, as the review and the audit
did independently.

**Deploy consequence.** The runbook item the review asked for — a meta
`Configure` as the first act after the first 0.32.0 start — is no longer
needed, because the surface it was closing is already closed. It is recorded in
`UPGRADES.md` either way.

## 3. The peer refusal, turned into durable tests

The review corrected `orchestrate-work.md` §5: the refusing branch of the meta
socket's peer check *is* reachable without privilege, through the subordinate
uid range `/etc/subuid` already grants. Both halves are now in the repository.

**`transport::session::tests`, two tests, run everywhere.** A real privileged
socket is bound, a real connection accepted, the peer's credential read with
`SO_PEERCRED`, and the real `Session` served. A peer who is not the socket's
owner receives `PeerRefused.PeerRejection` naming it — before it has written
anything — and the connection then closes with nothing following. Its companion
drives the same path with the owner admitted and gets a contract reply, so the
refusal is the rule's doing and not the harness's. The socket's owner is
*named* by the test rather than read from the file: `OwnsSocket` gained a
`#[cfg(test)]` `named` constructor, because a single-user test process has no
second user to borrow and the rule under test is about two numbers differing.
Seen failing with `Privileged::admits` made unconditionally true.

**`tests/second_user_peer.rs`, the review's technique, durable.** It reads the
current user's subordinate range from `/etc/subuid`, runs a copy of the test
binary under
`unshare --map-user=0 --map-users=1:<first>:1 … setpriv --reuid=1`, and that
process — whose credential in the Nexus's own namespace is the subordinate id —
connects to the meta socket of a real isolated Nexus and writes down the first
frame it is sent. The parent restores it and asserts
`PeerRefused(PeerRejection { peer_user_id: <first> })`. Witnessed green on this
host, and seen failing when the expected id was changed: the frame carried
`peer_user_id: 100000`, exactly the review's observation, now reproduced by the
repository rather than by a transcript.

Two honest qualifications, both in the test's own header. It relaxes the meta
socket to `0666` for the one exchange, because `0600` refuses `connect(2)`
before the rule is reached — in production the peer check is the defence
against a peer the file mode alone cannot stop. And its requirement is
explicit: `/etc/subuid`, `newuidmap`, `unshare` and `setpriv`. **A Nix build
sandbox grants none of them** — it runs as one unprivileged user with no
subordinate range, and no unprivileged process can invent one — so where the
requirement is unmet the test says so and ends rather than reporting a refusal
it did not see. The new `checks.peer-authority` runs it; in the sandbox that
check exercises the harness and reports the absence, and the named-owner
witness inside `checks.test` is what covers the rule and the wire path there.
This is a genuine limit of the gate, stated rather than hidden.

## 4. The version record: D-1, and the delimiter inside it

Verified rather than relayed. `git diff 7408fb6 c783b72 -- src/` in
`signal-orchestrate` is **empty**: `Query`, `Response`, every payload and every
rkyv archive are byte-for-byte 2.0.0, and the only `ethos/` change is a comment.
`meta-signal-orchestrate` `d8e0350..707f4cb` adds exactly one `Response`
variant, `PeerRefused.PeerRejection`. `signal` `626e407..2276ec4` changes only
pins and one test, so its own 3.0.0 did not move the frame either. Both
contracts' `UPGRADES.md` now carry the missing entry: what shipped, that the
wire did not change (or changed once, additively), and that 3.0.x was chosen to
mirror `signal`'s number — which the `nexus` skill's *"the crate's semver is the
wire's semver"* forbids. The numbers are pushed and pinned, so the entries are
the correction rather than a rewrite.

The one consumer-visible change hiding in those repins is the Datom string
delimiter, and I witnessed it in both directions rather than taking the
review's word: the client built at the current pins answers a curly-quoted Lock
reason with `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }` and accepts
the same reason in guillemets; `protos 2d999f17`, the revision the deployed
0.30.0 pins, documents curly quotes as the opaque-string boundary, and
`protos e8701521`, the current pin, uses `«»`. Both contracts' entries name it,
`orchestrate/UPGRADES.md` names it as a deploy-day break, and
`orchestrate/AGENTS.md` — which taught curly quotes for this repository's own
CLIs — now teaches guillemets and says what the old form produces.

**The four generated copies of the `orchestrate` skill still teach curly
quotes.** That is `Curriculum/skills/orchestrate.md` plus a regeneration, in a
repository outside this brief's scope and this flow's locks. It remains, and it
is the defect most likely to be met by an agent on deploy day.

## 5. Defects not closed, and why

| defect | disposition |
|---|---|
| D-1 high | documented in both contracts, as above |
| D-2 high | half: fixed inside `orchestrate` (`AGENTS.md`, `UPGRADES.md`); the `Curriculum` skill and its four generated copies remain, out of scope |
| D-3 high | `CriomOS-home/checks/orchestrate-service-path` — another repository, and blocked behind the unsettled CLI name |
| D-4 high | closed, §2 |
| D-5 medium | a design choice; see §6 |
| D-6 medium | recorded for the living by the brief's own instruction; see §6 |
| D-7 low | open: no gate greps the built Nexus binary, and `checks.build`/`checks.test` run the `--workspace` resolution rather than the package's |
| D-8 low | open: `ConfigurationRejection`/`ConfigurationRejectionReason` declared in both contracts |
| D-9 low | open: `Admitting::admitted` writes a meta-contract frame from a socket-agnostic trait, correct only while `Ordinary::admits` is total |
| D-10 low | open: `ConfigurationRejection` no longer names the configuration it refused |
| D-11 informational | open: the shared `orchestrate` checkout still holds the WIP `cf0dfef2`, now four releases behind main; untouched again this thread |

## 6. For the living, not decided here

1. **Binding comes from the store, not from XDG.** A store copy makes any
   instance try to bind the production socket paths; `prepare_socket` refuses a
   live socket but removes a stale one, so a stray instance started while the
   service is down takes the production paths. Witnessed again by this thread's
   own live test, which relies on exactly that to bind inside a temporary
   directory. The executable's XDG defaults decide only where a *fresh* store
   looks. Whether that is the intended relation between the built-in default
   configuration and the persisted one is a design question; `Vision/nexus.md`
   says the built-in default *"is what gives the socket path on which the
   Configure signal arrives"*, which reads as if the default should win for
   binding, and the implementation has the store win. Unresolved.
2. **The meta CLI's name.** `Vision/orchestrate.md`: *"a deployment without
   meta-orchestrate is wrong"*. `Vision/nexus.md`: *"The meta CLI is named
   component-meta"*. The package has built `orchestrate-meta` since 0.31.0 and
   `CriomOS-home` wraps `meta-orchestrate`; the socket file is still named
   `meta-orchestrate.sock`. Nothing deploys until this is settled. Untouched by
   this thread.
3. **The subscription reaches no consumer (D-5).** Both CLIs read one frame and
   exit, and the `orchestrate` skill tells every agent to re-ask
   `Observe.Locks` — the polling shape Vision forbids. A streaming CLI needs an
   output protocol for a sequence of typed values, which has not been designed;
   so does the question of whether the CLI is the right consumer at all, or
   whether the estate's followers should be Nexuses with an edge. A design
   choice, not a fix.
4. **Whether a carried store should keep its bootstrap window** is the judgment
   in §2. It is made and shipped, with its reasoning in the code, because the
   alternative is a live stranding hazard; but the reading of Vision that
   supports it is a reading, and the living may prefer the literal record with
   a different remedy (for instance, a deployment that configures through the
   meta socket at first start, which this change makes unnecessary).

## 7. Gates

Full local gate per repository, on the final content of each tree.

| repository | `cargo test` | `fmt` | `clippy -D warnings` | `doc` | `nix flake check -L --builders ''` |
|---|---|---|---|---|---|
| `orchestrate` 0.33.0 | pass | clean | clean | clean | all checks passed, `peer-authority` included |
| `signal-orchestrate` 3.0.1 | pass | clean | clean | clean | all checks passed |
| `meta-signal-orchestrate` 3.0.1 | pass | clean | clean | clean | all checks passed |

New durable gate: `orchestrate/checks.peer-authority`. Tests added: three on
the cutover authority (one an inversion of an existing assertion), two on the
refusing wire path, one on the kernel's own answer for a second user. Every one
of them was seen failing before it was trusted; the two that needed a
deliberate defect to fail are named in §2 and §3 with the defect used.

## 8. Locks

Lock 1169 `OrchestrateCutoverAuthorityFixes`, flow `f6db8d`, over
`/git/github.com/LiGoldragon/orchestrate`,
`/git/github.com/LiGoldragon/signal-orchestrate` and
`/git/github.com/LiGoldragon/meta-signal-orchestrate`. `Observe.Locks` was read
first: no lock was held over any of the three, and none appeared during the
work. Released after the pushes; the release is recorded in the return.

No Bead was delegated to this subflow, and none was opened or closed.

## Sources

- `Vision/nexus.md` and `Vision/orchestrate.md` — read in full, this thread;
  "First configuration" quoted verbatim in §2.
- The `subflow`, `spirit`, `behavior`, `orchestrate`, `nexus`, `file-editing`,
  `testing`, `versioning`, `flow-evidence` and `psyche` skills — loaded through
  the Skill tool, this thread.
- `flows/f6db8d/reports/orchestrate-review.md` and
  `flows/f6db8d/reports/orchestrate-work.md` — read in full, relayed; every
  claim this report acts on was re-witnessed here except where §2 says
  otherwise.
- `orchestrate 5f016531:src/store.rs` — the deployed 0.30.0 — read for the
  cutover premise, this thread; `:551-563` is the defaults-seeding the brief's
  premise turns on, and the ordinary request enum is read from the same file.
- `orchestrate 054ce581`: `store/{mod,cutover,record,transition}.rs`,
  `transport/{mod,session,socket}.rs`, `core.rs`, `configuration.rs`,
  `defaults.rs`, `lib.rs`, `tests/{live_nexus,configuration_authority}.rs`,
  `flake.nix`, `Cargo.toml`, `AGENTS.md`, `README.md`, `ARCHITECTURE.md`,
  `UPGRADES.md` — read, this thread; the edited ones are listed in §1's
  revision.
- `nexus a84bfa96:src/configuration.rs` — read in full, this thread, for the
  lifecycle trait the fix goes through.
- `signal-orchestrate` `git diff 7408fb6 c783b72`, `meta-signal-orchestrate`
  `git diff d8e0350 707f4cb`, `signal` `git diff 626e407 2276ec4` — read, this
  thread.
- `protos 2d999f17:src/anatomy.rs:158` (curly quotes) and
  `protos e8701521:src/core.rs:126` (guillemets) — read, this thread; the
  behaviour witnessed by running the built `orchestrate` client both ways.
- The subordinate-uid technique — witnessed end to end by this thread, first in
  a standalone probe reading `SO_PEERCRED`, then as the repository test.
- The Orchestrate lock service — one `Observe.Locks`, one `Lock`, one
  `Release`, as an ordinary client.

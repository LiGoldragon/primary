# Skeptical review of Orchestrate 0.32.0 and its three contracts

Flow f6db8d, read-only subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834`,
2026-09-11 night. Scope: `signal` 3.0.1 `2276ec42`, `signal-orchestrate` 3.0.1
`c783b727`, `meta-signal-orchestrate` 3.0.1 `707f4cb8`, `orchestrate` 0.32.0
`054ce581`, reviewed against `Vision/nexus.md`, `Vision/orchestrate.md`,
`Vision/signal.md`, `Intent/*.md`, and the `nexus`, `nexus-rationale` and
`orchestrate` skills.

Method. The diffs against `orchestrate 1bc55af1`, `signal-orchestrate 0efc9fda`
and `meta-signal-orchestrate 7d81bd96` were read and the release was driven in an
isolated instance **before** `reports/orchestrate-work.md` was opened; the
comparison in §7 was written after. All four repositories were fetched from
`origin` — none of the released revisions existed in the shared checkouts.

Throughout: **witnessed** means this thread ran it and read the result;
**relayed** means another flow or agent reports it and is named. The raw
transcript is `witnesses/orchestrate-review/live-cutover-and-clients.md`.

**Disclosed at once: this review took the live Orchestrate Nexus down for 21
seconds.** A `pkill -f` written to stop the scratch 0.30.0 instance matched the
live systemd user service as well, because both run the same `/nix/store` path.
The service was restarted with `systemctl --user start orchestrate-nexus` at
21:36:09 and is healthy; no store was written by the kill and the lock set was
intact. This was my error and a breach of the brief's "no running-service
changes". It is recorded rather than smoothed over, and it is also the sharpest
illustration of §3.4 below: nothing about this deployment distinguishes the
production Nexus from a copy of it.

---

## 1. Does each claimed closure hold?

Seven claims. **Six hold. One holds on the wire and in the Nexus but not for any
consumer.**

### 1.1 The frame is `signal`'s — holds, witnessed

The Nexus and both clients carry no length prefix of their own; framing is
`signal::{FrameReading, FrameWriting, AsyncFrameReading, AsyncFrameWriting}` with
`FrameCapacity::default()`. The five local `MAXIMUM_SIGNAL_BYTES` constants and
both hand-rolled `Exchanging` bodies are gone. Read at `054ce581`:
`transport/session.rs`, `crates/orchestrate/src/main.rs`,
`crates/orchestrate-meta/src/main.rs`.

Witnessed on the wire, both directions: a 0.32.0 client against a running 0.30.0
Nexus fails, and a 0.30.0 client against a running 0.32.0 Nexus fails. Neither
hangs and neither silently succeeds; each reports a typed client failure. The
byte-order change is from little- to big-endian, confirmed by reading
`1bc55af1:transport.rs:140,161` (`to_le_bytes`/`from_le_bytes`) against
`signal/src/frame.rs` (`to_be_bytes`/`from_be_bytes`).

### 1.2 The Nexus is Datom-free as built — holds, and I verified it more strongly than the repository does

Witnessed on the artefact, not on the manifest and not only on the resolution:
`cargo build --package orchestrate-nexus` yields a binary in which `strings` finds
zero occurrences of `datom_codec`, `datom-codec` or `protos`, and `nm -C` finds
39 apparent hits every one of which is a false positive on `Atomic` inside
`sema_engine` symbol names. The same source built with `--workspace` yields 1240
`datom` strings. So the two-resolution split in `flake.nix` is load-bearing and
the claim is true of the shipped executable.

The repository's own `datom-free-nexus` check asserts this with `cargo tree`,
which is a resolution assertion — one step stronger than reading a manifest, one
step weaker than reading the binary. It is sound because the Nix package builds
the same resolution the check resolves. I would still rather the check grep the
built artefact, since that is the thing the claim is about. See defect D-7.

### 1.3 The migration deletion, with a correct cutover for the real 0.30.0 store — holds, witnessed against a genuine 0.30.0 store

This is the claim I tried hardest to break, and it survived.

Source comparison first. `5f016531:src/store.rs` — the deployed 0.30.0 — and
`054ce581:crates/orchestrate-nexus/src/store/record.rs` agree exactly on
`SCHEMA_VERSION` (1), on `locks_v2` / `lock_id_allocator_v2` /
`orchestrate_configuration_v2`, on the family names `orchestrate-lock`,
`orchestrate-lock-id-allocator`, `orchestrate-configuration`, on the schema
labels `orchestrate-lock-v2`, `orchestrate-lock-id-allocator-v2`,
`orchestrate-configuration-v2`, and on the field shapes of `StoredLock`,
`StoredAllocator` and `StoredConfiguration`. So the cutover's premise is exact.

Then the experiment the repository's unit test cannot do: the *deployed 0.30.0
executable* was run against an isolated XDG to write a genuine 0.30.0 store, two
Locks were taken through the *deployed 0.30.0 client*, and the 0.32.0 Nexus was
started on that same file. Both Locks came back with their ids, flows, paths and
reasons intact, the allocator continued at 3, and a second open read the metadata
tree rather than the retracted configuration row. This is a stronger witness than
`store::cutover::tests`, which synthesises the 0.30 shape from the current
crate's own types.

The one-time reader is a forward read, not a fallback: it runs only when the
metadata tree is empty, and only when `catalog().is_registered(&CONFIGURATION_
TABLE)` — so a store that never had the family never gains it. The row is
retracted in the same commit as the seed.

Separately witnessed on the **real live store**: a copy of
`~/.local/state/orchestrate-nexus/orchestrate-nexus.sema`, opened by the 0.32.0
Nexus, cut over and then tried to bind `/run/user/1001/orchestrate-nexus/
orchestrate.sock` — proving it read the production configuration row. It was
refused only because the live Nexus held that socket. That is §3.4's defect, not
a cutover defect, but it is also the closest thing to a production cutover
rehearsal available without stopping the service.

**Unknown.** Whether the live store's pre-0.30 families (`orchestrate_
configuration`, `locks`, `lock_id_allocator`) and `active_path_locks` are empty.
`strings` on the live store shows all six table names and `active_path_locks`
present in the catalogue, but a Sema file is append-only, so a name proves
registration and not live rows. The audit's deduction — 0.30.0 carries a guard
that refuses to start if the pre-0.30 families are non-empty, and it started —
is sound, and 0.32.0 keeps the `active_path_locks` half of that guard. But
0.32.0 no longer registers or reads the three pre-0.30 families at all: if any
row survived there, it would now be silently ignored rather than refused. I could
not test this without opening the live store, which the brief forbids. I judge
the risk low and the audit's deduction good; I record it as unknown rather than
adopt it.

### 1.4 The Configure record — holds, witnessed

`nexus::ConfigurationState<StoredConfiguration>` lives in
`orchestrate_nexus_metadata_v1`, keyed `metadata`, and every transition persists
before it answers (`store/transition.rs`). Witnessed durable across a restart of
the isolated Nexus, and witnessed as `False` immediately after the cutover of a
0.30.0 store — which is correct, because 0.30.0 kept no such record and inventing
one would be a claim nobody made.

### 1.5 Ordinary Configure and meta reversal — holds, witnessed end to end

The whole cycle, driven with the released CLIs over the two scratch sockets:
`ConfigurationAccepted.{ … False }` → meta `Configured.{ … True }` → ordinary
`ConfigurationRefused.{ MetaConfigureOccurred }` → meta
`OrdinaryConfigurationReopened.{ … False }` → ordinary `ConfigurationAccepted`
again. Invalid configurations are refused on both surfaces with
`InvalidConfiguration`. This is exactly `Vision/nexus.md`'s "First configuration"
paragraph, including the part that is easy to skip — that the record is reversed
only on the meta socket.

### 1.6 The Observe subscription — holds in the Nexus, **does not reach any consumer**

Witnessed: `live_nexus::observe_delivers_the_state_on_open_and_every_later_
change` spawns the real `orchestrate-nexus` binary, connects a real socket, and
reads the opening `Observed`, then an unprompted `Observed` after a `Lock`, then
another after a `Release`. That is Vision's subscription, and the choice to make
the connection *be* the subscription — no token, no `Unwatch` — is the better
design than the vocabulary-without-implementation shape the audit found in Lojix.

But `Vision/nexus.md` forbids polling on the grounds that *a correct system goes
quiet when nothing changes*, and no consumer of Orchestrate goes quiet. Both CLIs
read exactly one frame and exit; the `orchestrate` skill tells every agent to
re-ask `Observe.Locks`; no other client exists. So the forbidden shape is still
what the estate does — the Nexus simply now *permits* the right one. The release
records this honestly as a known limit. I agree with the substance and disagree
with the accounting: this failure is half closed, not closed, and calling it
closed is what would let a later flow believe the polling problem is solved.

### 1.7 Socket modes and the peer check — holds, and I closed the gap the release left open

Modes witnessed on a live Nexus: `srw-------` meta, `srw-rw----` ordinary, set
after bind because a Unix socket takes its mode from a umask the Nexus does not
own. Against the live 0.30.0, both are `srwxr-xr-x` — so today anyone on the host
can open the production meta socket. That is a real improvement.

**The refusing branch, which `orchestrate-work.md` §5 records as having no
end-to-end witness, does have one now.** `/etc/subuid` grants `li:100000:65536`,
so an unprivileged user namespace with `unshare --map-users` yields a genuinely
different kernel uid, and `SO_PEERCRED` translates it back to 100000 in the
Nexus's namespace. Connecting from that identity produced the frame
`00 00 00 12 | 03 a0 86 01 00 00 …` — big-endian length 18, `Response`
discriminant 3 (`PeerRefused`), `PeerUserId` 100000 — sent before the peer wrote
anything. The report's stated reason for the gap, *"obtaining a second uid needs
privilege this session was not given"*, is incorrect; it needed only the subuid
range the host already grants. **This is a correction to the report, and the
technique is a durable test the repository could have.**

The honest qualification, which the release does not make: I had to chmod the
scratch meta socket to 0666 for that one exchange, because 0600 refuses the
`connect(2)` before the check is reached. In production the only peer that can
reach the check is root. The peer check is therefore defence against root
specifically — worth having, and narrower than "the meta socket authorises its
peers" suggests.

---

## 2. Is anything a compatibility path or a parallel shape?

**No compatibility path exists.** I looked for one in each place it would hide.

- The wire breaks outright in both directions (§1.1) and nothing negotiates.
- `store::cutover` is a one-time forward read guarded by catalogue registration,
  not a fallback: no 0.30 row is ever served to a peer, and after one open the
  reader is unreachable.
- `store::legacy` is a refusal, never an importer, and its own header says so.
  Its `orchestrate-upgrade-preflight` binary is kept partly because a check in a
  repository this flow may not edit names it — an obligation to a consumer rather
  than a compatibility path, and declared as such.
- `git grep -niE 'compat|fallback|deprecat'` over the three contract repositories
  returns nothing on the wire surface.

**Three parallel shapes, all small:**

1. `ConfigurationRejection` and `ConfigurationRejectionReason` are declared twice
   — once in `signal-orchestrate` (`[ MetaConfigureOccurred InvalidConfiguration ]`)
   and once in `meta-signal-orchestrate` (`[ InvalidConfiguration ]`) — with the
   same names and the same field. The meta contract already imports
   `OrchestrateNexusConfiguration` and `ConfigurationReceipt` from the ordinary
   one, so the machinery to share these exists and was not used. The meta socket
   genuinely cannot answer `MetaConfigureOccurred`, so the narrower enum is
   defensible; two types of the same name in two crates that already depend on
   each other is not.
2. The two client `main.rs` files remain near-duplicates. The release names this
   itself. The defect that made it dangerous — a doubled framing mistake — is
   gone.
3. `Admitting::admitted` answers with a `meta_signal_orchestrate::Response`
   whatever socket it is serving. It is correct today only because
   `SocketAuthority::Ordinary::admits` is unconditionally `true`, so the ordinary
   socket never reaches the write. A third authority would emit a meta frame on an
   ordinary connection, and nothing in the types would stop it. The refusal is not
   tied to the contract by type.

One thing that is *not* a parallel shape and reads like one:
`ConfigurationRejection` no longer carries the configuration it rejected. A peer
that pipelines cannot tell which value was refused. That is a loss of vocabulary
richness, deliberate or not, and worth a sentence somewhere.

---

## 3. What breaks for the live service's clients on deploy

The live service is `orchestrate-0.30.0` (`/nix/store/hnzql8g…`), PID under
`systemd --user`, sockets `/run/user/1001/orchestrate-nexus/{orchestrate,meta-
orchestrate}.sock`, store `~/.local/state/orchestrate-nexus/orchestrate-nexus.sema`.
Witnessed.

### 3.1 Who speaks to Orchestrate

Relayed from a fan-out survey of the 188 repositories under `/git/github.com/
LiGoldragon/` plus `/home/li/primary`, run by a subagent of this thread on the
**shared checkouts as they stood before my fetches**, so its revision statements
describe local HEADs and some are stale. The set is small and I re-verified the
load-bearing entries myself:

| consumer | how it speaks | state |
|---|---|---|
| `CriomOS-home` | packages, wraps, and runs the whole thing | **the only deploying consumer**, verified by me |
| `CriomOS` | flake input + a rev assertion in `checks/lojix-ownership` | verified by me |
| `mind` | `meta-signal-orchestrate` on `branch = "main"`, speaks `Create`/`Retire`/`Refresh` over a `Frame` | relayed; that vocabulary has not existed for several generations — already broken |
| `orchestrator-judge`, `signal-orchestrator-judge` | path deps requesting `nota-text` / `dotos-text` features | relayed; already unbuildable |
| `persona` | unpinned flake input, invokes `/bin/orchestrate-daemon` | relayed; that binary was removed at 0.23.0 — already broken |
| the `orchestrate` skill (4 generated copies) + `datom`, `edit-coordination` skills | the CLI, by name and by argument syntax | verified by me |

So on the wire, **nothing that currently works breaks**, because the only working
clients ship inside the orchestrate package itself. The three external crate
consumers are a generation or more behind and are already dead. That is the good
news and it is genuine.

### 3.2 What a deploy would actually need

Everything below is a concrete, verified requirement.

1. **`CriomOS-home/flake.nix:138`** pins `5f016531` — **0.30.0**, not 0.31.0.
   Move it to `054ce581`.
2. **`CriomOS/flake.nix:32`** pins the same rev, and
   **`CriomOS/checks/lojix-ownership/default.nix:8`** hardcodes
   `expectedOrchestrateRevision = "5f016531…"`, asserting at `:196-197` that both
   lockfiles carry it. All three move together or the gate fails.
3. **The binary name.** `CriomOS-home/modules/home/profiles/min/orchestrate.nix`
   wraps `${orchestratePackage}/bin/meta-orchestrate`; the package has built
   `orchestrate-meta` since 0.31.0. This fails at *build* time in `makeWrapper`,
   not at check time. `checks/orchestrate-service-path/default.nix:74` asserts the
   same name again. **`Vision/orchestrate.md` says a deployment without
   `meta-orchestrate` is wrong; `Vision/nexus.md` and the `nexus` skill say the
   meta CLI is `component-meta`.** The release correctly refuses to guess. This is
   a live Vision conflict and the living must settle it before any deploy.
4. **`checks/orchestrate-service-path/default.nix:115-116` will fail on content,
   not only on the name.** It asserts
   `test "$configured" = 'Configured.{ <ordinary> <meta> }'`, and the meta reply
   is now a `ConfigurationReceipt`: `Configured.{ { <ordinary> <meta> } True }`.
   Witnessed. Nobody has mentioned this; fixing the binary name alone leaves the
   check red.
5. **The Datom string delimiter.** Witnessed: the 0.32.0 client refuses
   `“curly quoted”` with `Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }`
   and requires `«guillemets»`. The `orchestrate` skill — in
   `Curriculum/skills/orchestrate.md` and its three generated copies — documents
   curly quotes explicitly, with a "copyable multi-word reason example" that will
   fail. The live 0.30.0 client accepts curly quotes. **Every agent in the estate
   taking a multi-word-reason Lock breaks on deploy day, with an error message
   that names neither quotes nor the reason field.** This did not arrive with
   0.32.0 — both the 0.31.0 and the 0.32.0 `protos` pins use guillemets — but the
   live service is 0.30.0, so the deploy is when it lands. It appears in no
   `UPGRADES.md`, in no deployment note, and in no report I read.
   *The skill is generated read-only evidence; the fix belongs in
   `Curriculum/skills/orchestrate.md` and a regeneration.*
6. **Do a meta `Configure` immediately after first start** — see §3.3.
7. Socket names, env var names (`ORCHESTRATE_SOCKET`,
   `ORCHESTRATE_META_SOCKET`), store path, `Observed.Locks.[]` for an empty
   observation, and `orchestrate-upgrade-preflight`'s output line
   (`active legacy PathLock rows: 0`, creating no store) are all **unchanged**.
   Witnessed. That is a real and deliberate continuity.
8. `orchestrate-store-migrate` disappears from the package. Nothing in the
   estate invokes it (relayed, and `checks/orchestrate-service-path` does not
   assert it).

### 3.3 A deploy-day hazard nobody has named: ordinary Configure is open by default

After the cutover of the real 0.30.0 store, `meta_configure_done` is `False` —
necessarily, since 0.30.0 kept no such record. While it is `False`,
`Vision/nexus.md` says Configure is accessible on the ordinary socket, and it is.
Witnessed: an ordinary peer repointed the Nexus to `/tmp/o6d/alt-{o,m}.sock`; the
running instance kept its bindings, and after a restart it bound the new paths
and left the old socket files behind as dead files. The wrapper's
`ORCHESTRATE_SOCKET` is fixed, and systemd's `RuntimeDirectory=orchestrate-nexus`
manages only the old directory.

So any peer that can open the ordinary socket can permanently strand every client
at the next restart, and `Restart=on-failure` will not help because the Nexus
starts successfully. The remedy is one command — a meta `Configure` with the
intended paths, immediately after the first 0.32.0 start, which closes the
ordinary surface — and it should be in the deploy runbook. The design is
Vision-sanctioned; the deployment consequence is not written down anywhere.

*Hypothesis, not witnessed:* a `RuntimeDirectoryMode=0700` parent plus
`StateDirectoryMode=0700` means "any peer" today is effectively "any process of
user li", which is a much smaller set than the 0660 ordinary mode suggests. I did
not test whether another local user can traverse `/run/user/1001`.

### 3.4 Binding comes from the store, not from the environment

Witnessed (§1.3): a copy of a production store makes any instance anywhere try to
bind the production socket paths. `prepare_socket` refuses when the socket is
live, which is the right guard and is what saved me — but it *removes* a stale
socket file, so a stray instance started while the service is down takes the
production paths. Combined with the fact that the production and scratch Nexuses
are the same `/nix/store` path (which is how I killed the live service), a
store copy is not an inert artefact. This is not a regression — 0.30.0 behaves the
same way — but 0.32.0 documents the cutover as "one read" and does not mention
that the read decides where the Nexus binds.

---

## 4. Which of the seven authority failures remain, and is the report accurate?

`runtime-audit.md` names seven: three in §3.2, four in §3.3. My verdict against
the release's own table:

| # | the failure | report | mine |
|---|---|---|---|
| 1 | Kameo | remains | **agree, remains.** No `kameo` at `054ce581`, witnessed. The report's defence — that writing actors against undesigned standards invents the standard by accident, and that `core.rs` is the only file that would change — is sound, and `Vision/nexus.md` does permit Arc-Mutex. |
| 2 | no durable meta-Configure record | closed | **agree, closed.** Witnessed §1.4. |
| 3 | no ordinary Configure, no meta reversal | closed | **agree, closed.** Witnessed §1.5. |
| 4 | Observe is one-shot; polling | closed | **disagree: half.** Closed in the Nexus and the contract, witnessed. No consumer subscribes; the estate still polls (§1.6). |
| 5 | meta socket privileged in name only | closed | **agree, closed** — with the refusing branch now witnessed (§1.7), which the report records as an open gap, and with the qualification that in production only root can reach it. |
| 6 | `nexus` library unused, ontology not designed first | half | **agree, half.** `nexus` 0.1.1 is unchanged since 2026-09-10, two files covering the configuration lifecycle only; witnessed. `Applies<Entering>` is named in `orchestrate/src/core.rs`, which is the right place to leave a marker and the wrong place for the trait to live. |
| 7 | no router, no shared signal repository | half | **agree, half.** `signal` now exists and holds the frame, the portable `Signal<T>`, and a `ComponentKind`/`AuthorizedObjectInterest` taxonomy — witnessed. The wrapping enum a router would dispatch on, and the handshake payload, are absent, and Orchestrate does not depend on the taxonomy at all. |

**Four closed, one open, two half — and by my reading four closed, one open,
three half**, the third half being the subscription.

On the report's accuracy more generally: it is unusually good. It names its own
weak witness (the little-endian test corrected after a first failure), it records
two runs that failed before the green one, it declares the peer-refusal gap
rather than glossing it, it corrects a version label in its own pushed commit
messages, and it separates what it did from what a sibling flow had already
landed. I found nothing in it that overstates. I found three things it
understates or gets wrong:

- The peer-refusal gap is closeable and its stated reason is incorrect (§1.7).
- "Four closed" should be "four closed, three half" (§1.6).
- "The `3.0.0` and `0.32.0` bumps are breaking" is **false for
  `signal-orchestrate`** — see D-1.

---

## 5. Less code or more?

**More, in Orchestrate. Less, in the estate, per unit of capability.**

Witnessed counts. `crates/orchestrate-nexus/src` 1553 → 2054 lines (+32%); its
tests 487 → 778; all `.rs` in the workspace 2692 → 3468 (+776). Against that:
`store.rs` 1066 lines became six files of ~900; `transport.rs` 224 became three
of ~482. The contracts shed 68 duplicated lines each into `signal`, which holds
~120 lines once for what six crates each carried — that is a real estate-wide
deletion, and it is the change that removed the class of defect (a hand-rolled
prefix that tests shared) rather than an instance of it.

Deleted and not replaced: the migration binary and its whole `Previous*` family,
three `PREVIOUS_*_TABLE` constants, three migration refusals, two tests, five
`MAXIMUM_SIGNAL_BYTES` definitions, eight hand-rolled prefix sites, and
`OrdinaryOutcome` — a wrapper enum with one variant, which is exactly the kind of
thing the trait-first rule is supposed to prevent from being written.

Added: the metadata tree, the configuration lifecycle, the subscription, the
socket authority, `NexusCore`. Four new capabilities and one relocation of the
store boundary. The growth is where the new authority lives, which is the
defensible place for it. The split of `store.rs` and `transport.rs` into modules
is not growth — it is the same work, findable.

Verdict: this is correctness paying for its machinery, in the sense the spirit
skill means. The one place I would push back is that `crates/orchestrate-nexus/
src/core.rs` names `Applies` and `Announcing` locally when both belong in
`nexus`, so the ontology debt is now carried in two repositories instead of one.

---

## 6. Against Intent

`Intent/anatomy.md`, `context.md`, `conversion.md`, `data.md`,
`mandatoryTraits.md`, `protosParsing.md` were read. Nothing in this release
contradicts them, and two are directly served: the mandatory-traits rule (every
method under a trait, `fn main` the only free function — verified by reading each
new module, with `Applies`, `Announcing`, `Configures`, `Bindable`, `Attributable`,
`Permissive`, `OwnsSocket`, `Admitting`, `Exchanging`, `Subscribing`, `Carrying`,
`Familial`, `Storing`, `KeepsMetadata`, `SeedsMetadata` all extracted), and the
conversion rule (no text on the wire, the CLI the only textualizer). The
`Applies<Entering>` naming follows `Vision/nexus.md`'s *"the name is open, Apply
liked"*.

---

## 7. Where my view and `reports/orchestrate-work.md` differ

Formed independently and compared afterwards, as the brief directs. We agree on
every closure, on the cutover premise, on the Datom-free finding and its cause,
on the migration deletion, on the Vision name conflict, and on the deployment
blockers 1–3. Six differences:

1. The Datom delimiter change (§3.2.5) — absent from the report, from
   `UPGRADES.md`, and from the deployment list. The largest practical
   deploy-day defect I found.
2. The `orchestrate-service-path` check fails on the `Configured` reply shape as
   well as the binary name (§3.2.4) — absent everywhere.
3. Ordinary Configure is open after cutover and can strand every client
   (§3.3) — absent everywhere.
4. Binding comes from the store, not the environment (§3.4) — absent.
5. The peer-refusal gap is closed, and the report's reason for it is wrong
   (§1.7).
6. The subscription is half closed, not closed (§1.6); and the contract version
   numbers do not mean what the report says they mean (D-1).

---

## 8. Summary

Orchestrate 0.32.0 is the best work in this lane so far. It closes four of the
seven authority failures the audit named, moves two more from zero to half, is
honest about the one it leaves open and about why, deletes a migration tool that
was written for a generation that no longer exists, and replaces it with a
cutover I verified against a store written by the actually-deployed binary. The
Datom-free claim, which the audit showed the previous release could not support,
is now true of the artefact — I checked the binary, not the manifest and not the
dependency graph. The wire break is total and deliberate and nothing that
currently works depends on the old wire.

What it is not is deployable. Six concrete things must change outside this
repository first, one of them is a Vision conflict only the living can settle,
and two of them — the string delimiter and the `Configured` reply shape — are not
written down anywhere and would be discovered on deploy day by an agent whose
lock request has just failed.

### Defects, by severity

**D-1 — high — the contract versions do not mean what semver says.**
`signal-orchestrate` went 2.0.0 → 3.0.0 → 3.0.1 with **no wire change at all**:
`git diff 7408fb6 c783b727 -- src/generated/ ethos/` is comment-only plus
dependency repins. `meta-signal-orchestrate` went 2.0.2 → 3.0.1 with one appended
`Response` variant — additive, a minor. Both were set to 3.0.x to match `signal`'s
number. The `nexus` skill says *"the crate's semver is the wire's semver, and
consumers pin it"*; mirroring a dependency's number breaks that, and it makes
every consumer treat a non-breaking release as breaking. Compounding it: neither
`UPGRADES.md` has any entry for 2.0.0 → 3.0.0, though both have entries for every
prior step, so the version that actually shipped is the one nothing documents.
There *is* a consumer-visible change hiding in those repins — the Datom delimiter
— which would justify a major for a reason nobody recorded. Witnessed.

**D-2 — high — multi-word Lock reasons break, and the skill still teaches the old
syntax.** §3.2.5. Fix `Curriculum/skills/orchestrate.md` and regenerate before
deploy, and say it in `UPGRADES.md`. Witnessed.

**D-3 — high — `CriomOS-home/checks/orchestrate-service-path` fails on the
`Configured` reply shape**, independently of the binary name. §3.2.4. Witnessed.

**D-4 — high — after cutover, any ordinary peer can permanently repoint the
sockets.** §3.3. The design is Vision-sanctioned; the deploy needs a meta
`Configure` as its first act and nobody has written that down. Witnessed.

**D-5 — medium — the subscription reaches no consumer.** §1.6. Recorded by the
release as a limit; my objection is to counting it as a closed failure.
Witnessed.

**D-6 — medium — binding comes from the store, so a store copy is a socket
hazard**, and a Configure repoint leaves dead socket files at the old path.
§3.4. Not a regression; undocumented. Witnessed.

**D-7 — low — the Datom-free gate asserts a resolution, not a binary.** I
verified the stronger claim holds (§1.2); the check could too, and a check that
tests the thing the claim is about does not go stale when the build shape
changes again. Also: `checks.build`, `checks.test` and every live test run the
`--workspace` resolution, so **no gate exercises the binary the package ships** —
and I witnessed that the two resolutions produce materially different binaries.

**D-8 — low — `ConfigurationRejection` and `ConfigurationRejectionReason` are
declared twice** in two crates that already share types. §2.

**D-9 — low — the peer refusal is written on the meta contract from a
socket-agnostic trait.** Correct today only because `Ordinary::admits` is total.
§2.

**D-10 — low — `ConfigurationRejection` no longer names the configuration it
refused.** §2.

**D-11 — informational — the shared `orchestrate` checkout is still dirty with
the abandoned WIP `cf0dfef2`**, three releases behind main; anyone building from
`/git/github.com/LiGoldragon/orchestrate` builds the WIP. Recorded by the release
as needing the living's word. Witnessed — I had to clone from it and check out
`054ce581` explicitly.

### What I could not determine

- Whether the live store still holds rows in the three pre-0.30 families that
  0.32.0 no longer reads (§1.3). Low risk, unresolved.
- Whether another local user can traverse `/run/user/1001` to reach the 0660
  ordinary socket (§3.3).
- The external consumers' current revisions: the survey ran against checkouts
  that predate my fetches, so `mind`, `persona` and the two judge repos are
  reported at stale local HEADs. Their *incompatibility* does not depend on
  that — they are generations behind — but the exact revisions do.

No file in any reviewed repository was edited, no lock taken, no Nix build run,
no deploy performed. Nothing was committed or pushed: the harness forbids it for
this thread, so `reports/orchestrate-review.md` and
`witnesses/orchestrate-review/` are written and left uncommitted.

---

## Sources

- `Vision/nexus.md`, `Vision/orchestrate.md`, `Vision/signal.md`, and
  `Intent/anatomy.md`, `context.md`, `conversion.md`, `data.md`,
  `mandatoryTraits.md`, `protosParsing.md` — read in full, this thread.
- The `spirit`, `behavior`, `flow-evidence`, `nexus`, `nexus-rationale`,
  `orchestrate`, `psyche`, `testing` and `subflow` skills — loaded through the
  Skill tool, this thread.
- `orchestrate` `git diff 1bc55af1 054ce581` in full, and `054ce581`'s
  `store/{mod,cutover,legacy,record,transition}.rs`,
  `transport/{mod,session,socket}.rs`, `core.rs`, `configuration.rs`,
  `ordinary.rs`, `defaults.rs`, `main.rs`, `flake.nix`, `UPGRADES.md`,
  `ARCHITECTURE.md`, `README.md`, `AGENTS.md`, `tests/live_nexus.rs` — read, this
  thread.
- `signal-orchestrate` `git diff 0efc9fda c783b727` and `git diff 7408fb6
  c783b727`; `meta-signal-orchestrate` `git diff 7d81bd96 707f4cb8` and `git diff
  d8e0350 707f4cb8`; `signal` `2276ec42:src/{lib,frame,portable,taxonomy}.rs`,
  `ethos/signal.ethos`, `Cargo.toml`; `nexus` `a84bfa96:src/lib.rs` and its log —
  read, this thread. All four repositories fetched from `origin`; none of the
  released revisions existed in the shared checkouts.
- `orchestrate 5f016531:src/store.rs` — the deployed 0.30.0 — read for the
  cutover premise, this thread.
- `CriomOS-home/flake.nix:138`, `modules/home/profiles/min/orchestrate.nix`,
  `checks/orchestrate-service-path/default.nix` — read, not edited, this thread.
- The live service: `systemctl --user status/start`, `journalctl --user`, `ps`,
  `ls /run/user/1001/orchestrate-nexus`, one `Observe.Locks` before and after,
  and one file copy of the store — this thread. The 21-second outage is recorded
  at the head of this report.
- `witnesses/orchestrate-review/live-cutover-and-clients.md` — the isolated
  0.32.0 Nexus over a 0.30.0-written store, all client drives, the peer refusal,
  and the binary inspection. This thread.
- `flows/f6db8d/reports/runtime-audit.md` §§3.1–3.3, 4.1–4.2, 6, 8 — relayed; its
  store-layout equivalence finding re-witnessed independently here, both in the
  sources and against a genuine 0.30.0 store.
- `flows/f6db8d/reports/orchestrate-work.md` — relayed, read only after §§1–6 of
  this review were formed.
- The consumer survey in §3.1 — relayed from a subagent of this thread over
  `/git/github.com/LiGoldragon/` and `/home/li/primary`; its `CriomOS`,
  `CriomOS-home` and skill entries re-verified by me, its `mind`, `persona` and
  judge-repo entries not.

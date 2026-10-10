# Runtime audit — flow 857335's Orchestrate, Lojix, Horizon and Nexus work

Scope: the runtime slice of flow 857335, audited 2026-09-11 by subflow thread
`f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d. Read-only throughout: no
repository, service, store, lock or configuration was written. Repositories were
read with `git show <rev>:<path>` without checkout. The live service was read
through `systemctl --user show`, `ps`, `ls`, `strings` and one ordinary
`Observe.Locks`. One tarball export of orchestrate `1bc55af1` was made into
scratch and only `cargo tree --offline` was run against it.

Throughout: **witnessed** means this flow read it directly; **relayed** means it
is reported by another flow or agent and named as such. Observations,
hypotheses and unknowns are kept separate in each section.

---

## 1. Summary of what disconfirms the flow's claims

Ordered by weight.

1. **The shipped `orchestrate-nexus` binary links Datom and Protos.** The flow's
   central Datom-free-daemon claim rests on a witness command that cannot detect
   the condition it was chosen to prove. Witnessed, decisive. §3.1
2. **The whole migration and cutover design rests on a misreading of the
   deployed store.** Deployed 0.30.0 and released 0.31.0 have byte-identical
   durable record layouts and table identities. No migration is required, and the
   prepared migration tool would fail against the live store. Witnessed,
   decisive. §4
3. **The gap audit names three authority failures; there are at least seven.**
   The unnamed ones include the forbidden polling shape, the absent Kameo engine
   on the WIP branch that was supposed to carry it, the unused Nexus library, and
   an entirely unauthorised meta socket. Witnessed. §3
4. **The Lojix gaps declared "closed" are three-fifths closed.** Three closures
   hold cleanly; Kameo holds only in part; the Horizon edge holds with a
   build-graph caveat. Two invariants the gap audit does not mention —
   subscription and traits-first — are unmet at the very revision it calls "the
   trait-surface correction." The blanket closure sentence is not supportable.
   Relayed from a parallel sub-audit with citations. §9
5. **The prepared deployment patch is incomplete and would break the CriomOS
   gate.** Witnessed. §8
6. **The ordered sequence was inverted and its gate never closed.** The living
   ordered audit before port; the port landed first, the compliance audit
   followed it by five and a half hours, and the two skeptical audits that were
   then ordered as a gate were interrupted and never produced a report.
   Witnessed. §7
7. **The live service is not as the reports left it.** The machine rebooted; the
   service restarted under a new PID; the store has been written as recently as
   two hours before this audit. Version and sockets are unchanged. Witnessed. §6

One finding recurs across both runtimes and is worth naming on its own: **nothing
in this stack observes by subscription.** Orchestrate has no subscription
vocabulary at all; Lojix has a complete one whose implementation is a counter and
a closed connection. `Vision/nexus.md` forbids polling, and every consumer of
either Nexus polls, because there is nothing else to do. §3.3a, §9.6

Nothing found here impugns the port's *wire* work, which is clean. §3.4.

---

## 2. What the flow claimed

Relayed, from `/home/li/primary/flows/857335/reports/`:

- `runtime-port.md` — Orchestrate 0.31.0 on main at `1bc55af1`; three packages;
  "no routed envelope or compatibility decoder"; "The daemon's normal Cargo
  dependency edges contain neither Datom nor Protos"; the generated named
  records "are not treated as archive-compatible with the 0.30 tuple records";
  `orchestrate-store-migrate` "is not a daemon compatibility path"; a two-copy
  migrate-validate-promote cutover runbook; production read-only checked and
  "remained active as PID 2323".
- `nexus-gap-audit.md` — three open Orchestrate authority requirements (no
  Kameo; no durable record of whether meta Configure occurred; no ordinary
  Configure and no meta reversal). Lojix/Horizon gaps declared **closed** at
  Horizon 0.8.0 `e4871220` and Lojix 1.0.0 `e2c7bdc5` / 1.0.1 `b8f7a8cc`.
- `cutover-preparation.md`, `port-preparation.md` — sequencing, protected paths,
  and the requirement for an isolated-copy migration probe before cutover.
- `shutdown-runtime.md` — clean releases, three preserved WIP bookmarks, a
  remaining-work list, and all flow-857335 locks released.

---

## 3. Does released Orchestrate 0.31.0 match Vision/nexus?

Authority read in full: `Vision/nexus.md`, `Vision/signal.md`, `Vision/sema.md`,
`Vision/orchestrate.md`, and the `nexus` and `nexus-rationale` skills.

### 3.1 The daemon is not Datom-free in the form that ships — witnessed

This is the sharpest finding and it inverts a claim the flow treated as proven.

`runtime-port.md` states: *"The daemon's normal Cargo dependency edges contain
neither Datom nor Protos."* Its witness (`witnesses/runtime-port.md`) is:

```
cargo tree -p orchestrate-nexus --edges normal | rg 'datom|protos'  →  no matches
```

That command resolves features for `orchestrate-nexus` **alone**. The Nix
package does not build it alone. `orchestrate 1bc55af1:flake.nix:37`:

```nix
packageArgs = commonArgs // { cargoExtraArgs = "--workspace"; };
```

Under Cargo's resolver-2/3 feature unification, one `--workspace` build unifies
features across the three members. `orchestrate` and `orchestrate-meta` both
enable the signal crates' `datom` feature. Reproduced offline against an
unmodified export of `1bc55af1`:

| resolution | `signal-orchestrate` features | `meta-signal-orchestrate` features |
|---|---|---|
| `-p orchestrate-nexus` (the flow's witness) | *(empty)* | *(empty)* |
| `--workspace` (what the package builds) | `datom` | `datom` |

and `cargo tree --workspace -e normal -i protos` lists `orchestrate-nexus
v0.31.0` as a normal-edge dependent, through
`signal-orchestrate[datom] → datom-codec → protos` and the same path via
`meta-signal-orchestrate`.

So the released daemon, as packaged, is compiled with the Datom feature and
links `datom-codec` and `protos`. The manifest is clean; the artefact is not.
The flow's gate could not have caught this, because the command chosen is
insensitive to workspace feature unification.

Witness: `witnesses/runtime/daemon-datom-feature-unification.txt`.

Note this is a build-shape defect, not a wire defect: no text reaches the
socket either way (§3.4). The violation is of "the Datom-free
`orchestrate-nexus` service" as a *fact about the shipped executable*, which the
flow asserted and did not establish.

### 3.2 The three named authority failures — all confirmed, with a correction

**Kameo — confirmed, and worse than reported.** `Vision/nexus.md`: *"The engine
inside a Nexus is driven by Kameo actors. The standards of their use are still
to be designed. Arc-Mutex is permitted."* Arc-Mutex is permitted *inside* that
design, not as its replacement. `1bc55af1:Cargo.toml` contains no `kameo`. The
engine is `Arc<Mutex<OrchestrateStore>>` behind two `tokio` listener futures
(`crates/orchestrate-nexus/src/transport.rs:31-52, 84-124`).

The correction the flow's own reports do not make: the WIP branch that
`shutdown-runtime.md` says will "implement the Kameo-owned effect processor"
does not begin it. `cf0dfef2:Cargo.toml:26` adds `kameo = "0.20"`, and
`git grep -n 'kameo\|Actor' cf0dfef2 -- 'crates/**/*.rs'` returns **no match**.
The dependency is declared and unused; the transport at `cf0dfef2` is the same
`Arc<Mutex>` one-shot, changed only by trait renames
(`TransportBinding`→`Bindable`, `PayloadReading`→`Readable`, …).

**No durable first-configuration record — confirmed.** `Vision/nexus.md` requires
a standard metadata tree in which *"a type records whether the meta Configure was
ever done."* At `1bc55af1`, `StoredConfiguration` is two socket path strings
(`store.rs:81-90`); there is no marker and no metadata tree. Further: `HandlesMeta`
(`store.rs:649-669`) treats `Configure` with an unchanged value as a no-op, so
even a marker keyed on "a Configure arrived" would not fire.

**No ordinary Configure, no meta reversal — confirmed.** The released ordinary
contract `signal-orchestrate 1.0.4` (`0efc9fda:ethos/signal.ethos`) declares
queries `Lock`, `Release`, `Observe` only. The meta contract declares `Configure`
only. `HandlesOrdinary` (`store.rs:633-644`) and `HandlesMeta` match.

The WIP branches do begin this: `signal-orchestrate@e3ea414c` adds ordinary
`Configure.OrchestrateNexusConfiguration`, `MetaConfigureDone.Boolean`,
`ConfigurationReceipt`, and `ConfigurationRejectionReason.[ MetaConfigureOccurred
InvalidConfiguration ]`; `orchestrate@cf0dfef2:store.rs` imports
`nexus::{Configurable, ConfigurationState, ConfigurationTransitionError}`. That
work is unreleased and, by the flow's own words, uncompiled.

### 3.3 Four further authority failures the gap audit does not name — witnessed

**(a) Observation is not a subscription; the shape is the forbidden one.**
`Vision/nexus.md`: *"State is observed by subscription: the subscriber receives
the state on open, then each change as it happens"* and *"Polling is forbidden;
a correct system goes quiet when nothing changes."* At `1bc55af1`,
`transport.rs:176-187` reads exactly one frame, writes exactly one reply, and
returns — the connection closes. `Observed.Observation` is a point-in-time
snapshot; the orchestrate skill itself says so ("It is not a subscription").
The only way a caller tracks lock state is to re-ask, which is polling.

This is not addressed on the WIP branch either: `e3ea414c`'s contract still has
`Observe.ObserveSelection` → `Observed.Observation` and adds no stream,
subscription token, or unsubscribe vocabulary. `shutdown-runtime.md` lists
subscription under remaining work; `nexus-gap-audit.md`, which presents itself as
the authoritative gap list and says it *"supersedes any closure wording in
earlier chronological reports"*, omits it.

**(b) The meta socket is privileged in name only.** `Vision/nexus.md`: the meta
socket is *"the root user of the Nexus."* `transport.rs:41-75` binds both sockets
identically: no `chmod`, no umask control, no `SO_PEERCRED` check, no
authorization of any kind. The two sockets differ only by filename and by which
contract they decode. Witnessed live, both are `srwxr-xr-x` in
`/run/user/1001/orchestrate-nexus/`. Compare Lojix, whose startup configuration
takes an explicit mode per socket (`432`/`384` in the lojix skill's tested form).
`shutdown-runtime.md` lists "explicit ordinary/meta socket modes and owner peer
authorization" as remaining work; `nexus-gap-audit.md` omits it.

**(c) The Nexus library is not used, and the ontology was not designed first.**
`Vision/nexus.md`: *"The nexus repository is the library that defines the core of
a Nexus component"*, and *"The basic ontology of an actor and dataflow system is
designed before implementation."* `1bc55af1:Cargo.toml` has no `nexus`
dependency. The ordering is witnessed: `orchestrate` 0.31.0 was committed
2026-09-10 03:28 +0200; `nexus` 0.1.1 `a84bfa96` at 07:53 +0200 — four and a half
hours *after* the runtime it was supposed to found. And `nexus` 0.1.1 is 121
lines in two files covering the configuration lifecycle only: no effect/`Apply`
trait, no actor or dataflow ontology, no socket or signal surface. The universal
ontology that Vision places before implementation does not exist.

**(d) No router, no shared signal repository.** `Vision/nexus.md` "Routing"
requires a signal repository holding the wrapping enum and the common handshake
payload, *"which every component depends on."* Neither exists in the Orchestrate
port. This may be deliberately deferred — I found no record either way (§8).

### 3.4 What is genuinely conformant — witnessed

Stated plainly because the failures above should not be read as a verdict on the
whole port.

- Three packages: Datom-free-by-manifest `orchestrate-nexus`, ordinary
  `orchestrate`, privileged `orchestrate-meta`. Vision's "one datom-converting
  CLI per socket" is met.
- Zero-argument startup with executable-owned defaults, XDG-derived, rejecting
  every argument (`defaults.rs:30-52`); a fresh store is seeded with those
  defaults and an existing store resumes its own (`store.rs:588-605`). This is
  exactly Vision's "Configuration" paragraph.
- Pure binary wire: one little-endian `u32` length prefix, one rkyv archive,
  validated on receive, 8 MiB cap, no version byte, no envelope, no second
  decoder, no text (`transport.rs:126-208`). Typed refusals are vocabulary
  (`LockRejection`, `ReleaseRejection`), not strings.
- Traits-first is taken seriously: `ordinary.rs` is an explicit trait ontology,
  and `fn main` is the only free function in each crate.
- The signal repos are vocabulary-only, authored in Ethos, closed enums, verbs in
  verb form with past-tense replies. The ordinary contract's wire vocabulary is
  unchanged across 1.0.0→1.0.4 (`git diff 8bdd51f 0efc9fd -- ethos/` is empty);
  only the Rust framing API moved.

### 3.5 Relayed, from the parallel compatibility sweep

Not independently re-verified by me except where marked.

- `orchestrate 1bc55af1:Cargo.lock` carries **two `ethos-zero` revisions**
  simultaneously — 6.1.0 `6e5ad400` (pulled by `signal-orchestrate 1.0.4` and
  `meta-signal-orchestrate 1.0.0` as their build-time generator) and 6.1.2
  `daf00729` (pulled by `orchestrate` and `orchestrate-meta`). **Witnessed by me
  at `Cargo.lock:151-153, 165-167`.** The three ported repos do not agree on
  their code generator; the signal crates were not re-cut against the generator
  Orchestrate now pins.
- The same lockfile carries **two `datom-codec` 0.25.4 entries** at different
  revisions, an artefact of a `.git` URL-suffix mismatch defeating Cargo source
  unification.
- The WIP branches commit **absolute local `path =` dependencies**
  (`cf0dfef2:Cargo.toml`, `eb6df08e:Cargo.toml:13`), which are not reproducible.
- `ethos-monolith` does not exist as a repository and nothing depends on it; the
  order's phrase names a repo already gone.
- No compatibility surface exists in either signal repo at any of the four
  revisions: `git grep -niE 'compat|legacy|fallback|deprecat|_v1|_v2|old'` over
  `src/`, `ethos/`, `tests/` returns zero hits.
- Four further consumers sit a whole contract generation or more behind and were
  not updated: `mind` (`Cargo.toml:50`, `branch = "main"`, no rev, locked to
  `signal-orchestrate 0.5.0` / `meta-signal-orchestrate 0.4.0` on the
  pre-Ethos-Zero `nota`/`schema-rust` chain), `orchestrator-judge` and
  `signal-orchestrator-judge` (path deps requesting a `nota-text` feature the
  current crate does not have), and `persona` (fully unpinned, invoking a
  `/bin/orchestrate-daemon` the tree no longer produces).

---

## 4. Was porting done without compatibility paths?

**On the wire: yes, cleanly.** §3.4 and §3.5.

**In the store: the claim is inaccurate as written, and the premise under it is
wrong.**

### 4.1 The daemon does read old layouts at startup — witnessed

`1bc55af1:store.rs:25-28` compiles three previous-generation table names and one
legacy table name into the daemon. `OpensStore::open` — the runtime startup path,
called from `main.rs:13` — registers `PREVIOUS_CONFIGURATION_TABLE` and
`PREVIOUS_LOCKS_TABLE` in the durable catalog and queries them (`store.rs:532-556`),
then does the same for `active_path_locks` (`:564-577`), returning
`PreviousSignalMigrationRequired` or `LegacyActiveLocks` if either is non-empty.

This is a **refusal gate, never a fallback**: no old row is ever materialised as
a new one. The flow's substantive claim — that `orchestrate-store-migrate` and
`orchestrate-upgrade-preflight` are standalone offline binaries not invoked by
the daemon — is correct; I read both `main`s. But the shipped documentation
overstates it. `ARCHITECTURE.md:57` says *"The normal open path never reads old
tuple records"*, and the doc comment at `store.rs:394-396` says
*"This method is the only legacy reader."* Both are false as stated. That is a
documentation defect of the kind later readers build on — and, given the next
finding, one that did mislead.

### 4.2 The premise of the entire migration is wrong — witnessed, decisive

`runtime-port.md` asserts that 0.31.0's *"generated named records are not treated
as archive-compatible with the 0.30 tuple records"*, and cites historical
Orchestrate `5f016531` `src/store.rs` as supplying *"the deployed tuple
`Configure`, tuple `Lock`, and allocator Sema layouts."*

`5f016531` **is** the deployed 0.30.0 — the same revision
`CriomOS-home/flake.nix:138` pins today. And what it actually stores is not tuple
records. Comparing `5f016531:src/store.rs` with
`1bc55af1:crates/orchestrate-nexus/src/store.rs`:

- The table and family constants are **identical, line for line**:
  `orchestrate_configuration_v2`, `locks_v2`, `lock_id_allocator_v2`, with
  `PREVIOUS_*` naming the pre-0.30 tables and `active_path_locks` the 0.24-era one.
- The active rkyv record structs `StoredConfiguration`, `StoredLock`,
  `StoredAllocator` are **textually identical**.
- The tuple `PreviousConfigure` / `PreviousLock` / `PreviousStored*` types are
  **also identical between the two**, and in *both* revisions they read the
  pre-0.30 tables — not anything 0.30.0 writes.

Independently corroborated from the deployed artefact itself:
`strings -a /nix/store/hnzql8g…-orchestrate-0.30.0/bin/orchestrate-nexus` yields
`locks_v2`, `orchestrate_configuration_v2`, `lock_id_allocator_v2`,
`orchestrate-configuration-v2`, `orchestrate-lock-v2`, alongside the v1 and
path-lock-v1 guard labels.

**The flow read its own cited source as describing the deployed shape when it
describes that revision's own legacy readers.** The tuple layout it "audited"
was retired before 0.30.0 was deployed — the live store still carries a
`.pre-v2-20260908T111047+0200.bak` from when 0.30.0 performed that very
migration on 2026-09-08.

Two consequences follow.

**0.31.0 requires no migration to open the live store.** Its record layout and
family identities are byte-identical to the running version's.

**`orchestrate-store-migrate` would fail against the live store.** It requires
exactly one row in the *pre-0.30* configuration and allocator tables
(`MigrationSourceInvariant`, `store.rs:433-440`). Those tables are provably
empty: the deployed 0.30.0 carries the identical `open()` guard that refuses to
start if they are non-empty, and it started — `orchestrate-nexus ready`,
`ActiveState=active`, `MainPID=2094`, 2026-09-10 13:30:08. The same deduction
resolves the legacy `active_path_locks` question: the `strings` hits in the live
`.sema` are retracted rows in an append-only log, not live records, because
0.30.0's `LegacyActiveLocks` guard also passed. *(This inference is mine; it is
sound only if the deployed binary is built from `5f016531`, which the unmodified
`flake.nix:138` pin and the matching error strings in the binary both support.)*

So the elaborate two-copy migrate-validate-promote runbook in `runtime-port.md`,
and `port-preparation.md`'s step 4 demanding a consistent live snapshot before
migration, address a transition that already happened three days before the port
began. The real cutover question — whether 0.31.0 opens the live store as-is —
was never asked.

Witnesses: `witnesses/runtime/store-layout-equivalence.txt`,
`witnesses/runtime/live-store-generation.txt`.

---

## 5. Is the synthetic migration witness meaningful?

**No — and for a reason stronger than the flow's own caveat.**

The flow disclosed one limitation honestly: the installed Sema stack offers no
online file-export, the store is on plain ext4, and so *"this work does not claim
that the synthetic store is a current live snapshot."* That caveat is correct and
correctly stated.

But the deeper problem is §4.2. `witnesses/runtime-port.md` describes
`previous_signal_rows_require_an_explicit_migration` as constructing *"exact
historical tuple archives via types independent of the migration reader."* Those
tuple archives are the **pre-0.30** shape. The live store left that shape on
2026-09-08 under 0.30.0's own migration. The test therefore exercises a
transition that (i) the live store has already completed, (ii) cannot recur, and
(iii) is not the transition a 0.30→0.31 cutover would perform — because that
cutover performs no store transition at all.

The witness is a valid unit test of a code path. It is not evidence about the
cutover, and the report presents it as the flow's migration evidence. Its
weakness is not that it is synthetic rather than live; it is that it tests the
wrong generation.

The Bubblewrap namespace witness is a different matter and is sound: it
demonstrates that a candidate holding production absolute socket paths can be
exercised without binding the host's production sockets. That technique remains
useful whether or not a migration is involved.

---

## 6. Is the live service as the reports left it?

Observed 2026-09-11 17:07 −0600.

| | reports | now | |
|---|---|---|---|
| version | 0.30.0 | 0.30.0, `/nix/store/hnzql8g…-orchestrate-0.30.0` | unchanged |
| PID | 2323 | **2094** | **changed** |
| started | 2026-09-09 21:49:23 CEST | 2026-09-10 13:30:08 CST | **restarted** |
| sockets | ordinary + meta under `/run/user/1001/orchestrate-nexus/` | same two paths, recreated 2026-09-10 13:30:08 | paths unchanged |
| store | 638,976 bytes | 638,976 bytes, **mtime 2026-09-11 15:06:42** | size unchanged, contents written |
| deployed pin | `5f016531` | `5f016531`, `flake.nix` unmodified | unchanged |

The machine rebooted at 2026-09-10 13:29 — the Prometheus wind-down recorded in
the flow's log — and the service restarted under a new invocation. `PID 2323`
should not be carried forward as a live identifier; it now belongs to
`criomos-lock-listener`, an unrelated process.

Store size is not a witness of unchanged state: Sema preallocates, so 638,976
bytes persists across writes. The mtime shows the store was written two hours
before this audit — other flows are actively acquiring and releasing.

An ordinary `Observe.Locks` returned 35 locks, none owned by flow 857335,
consistent with `shutdown-runtime.md`'s final release claim. Highest observed
lock id 1019; the 1020–1070 range the flow reserved and released is absent.

0.31.0 has never been built on this host: no `/nix/store/*orchestrate-0.31*`
exists.

Witness: `witnesses/runtime/live-service.txt`.

---

## 7. Was the ordered sequencing honored?

**No, and the flow says so about one half of it while its own artefacts show the
other half.**

The living's order, relayed and witnessed in `flows/564f55/log.md:15`:

> tell him to port orchestrate to the new stack when he's audited it against the vision.

and at `:16`, the later instruction for *"an against-the-vision skeptical audit"*
by Opus 5 medium plus a Sol medium subflow audit; `:30` records the intended
order as the two skeptical audits *"then the port."*

The timeline, witnessed (git author times are +0200, file mtimes local −0600):

| | |
|---|---|
| 2026-09-10 03:28 +0200 | orchestrate 0.31.0 `1bc55af1` **committed to main** |
| 2026-09-09 19:38 −0600 (= 03:38 +0200) | `reports/runtime-port.md` written, 10 min later |
| 2026-09-10 01:02 −0600 (= 09:02 +0200) | `reports/nexus-gap-audit.md` written — **5h34m after the port landed** |
| 2026-09-10 07:53 +0200 | `nexus` 0.1.1 library committed — after both |
| 2026-09-10 09:13 +0200 | the three WIP branches committed, 11 min after the gap audit |
| 2026-09-10 01:30 −0600 | both skeptical-audit records written as **interruption records** |

The flow's own log is candid about the second half: *"It would be false to claim
these two audits preceded that work."* It does not say the same about the first:
the compliance audit against Vision that the living made a precondition of
porting was performed on an already-published release.

Both skeptical audits were launched as systemd user units and interrupted by
SIGINT when Prometheus went offline. Neither produced a final report; both
`reports/skeptical-opus.md` and `reports/skeptical-sol.md` say so explicitly and
say *"Resume or rerun the independent audit before further Orchestrate
implementation."* That gate is still open. No independent skeptical audit of this
runtime has ever been completed — which is consistent with the defects in §3.1
and §4.2 surviving into a published release and a prepared deployment patch.

I note in the flow's favour that it held further Orchestrate implementation after
the interruption and did not treat the unfinished audits as passed.

Witness: `witnesses/runtime/sequencing.txt`.

---

## 8. The prepared deployment patch

Read at `/home/li/primary/flows/857335/reports/orchestrate-deployment.patch`;
unapplied, and `CriomOS-home/flake.nix:138` still carries the old pin.

**It would break the CriomOS gate.** `CriomOS/checks/lojix-ownership/default.nix:8`
hardcodes `expectedOrchestrateRevision = "5f016531…"` and asserts at `:196-197`
that **both** `CriomOS/flake.lock` and `CriomOS-home/flake.lock` carry it. The
patch changes CriomOS-home's lock and touches nothing in CriomOS. Applying it as
prepared fails that assertion.

**It renames a deployed user-facing binary.** `meta-orchestrate` →
`orchestrate-meta`. Within CriomOS-home the patch is complete — the module
wrapper and both checks are updated, and I found no other Nix or skill consumer
of the old name. But `Vision/orchestrate.md:7` still reads *"a deployment without
meta-orchestrate is wrong"*, while `Vision/nexus.md` says *"The meta CLI is
named component-meta."* These two Vision statements conflict on the name. A
relayed record (`flows/01a03603/reports/decisionLedger.md:39`, not verified by
me) reportedly orders the `meta-orchestrate` spelling as more specific than the
generic convention. **This should go to the living before the rename ships.**
The socket file keeps the old spelling (`meta-orchestrate.sock`) under either
name, which the patch leaves inconsistent with the new binary name.

**An unexplained quoting asymmetry.** The patch changes the check's `Configure`
call to wrap both socket paths in Datom curly quotes
(`Configure.{ «…» «…» }`) but leaves the adjacent ordinary `Lock` call's
absolute paths bare. If the current Datom surface requires quoting for absolute
paths, the bare paths in the `Lock` call — and in the orchestrate skill's
documented form, and in every caller now on the wire — break at cutover. If it
does not, the `Configure` change is unnecessary. I could not determine which
without building. **Unknown.**

**It carries no store step.** Given §4.2 that is very likely correct — but it is
correct by accident, since the flow's reports call for a migrate-and-promote
runbook the patch does not implement.

Witness: `witnesses/runtime/consumer-pins.txt`.

---

## 9. Lojix, Horizon and Nexus — were the "closed" gaps closed?

Audited at the brief's revisions by a parallel read-only sub-audit of this flow.
Findings in §9.1–§9.5 are **relayed** from it with the file:line it cites;
§9.6–§9.7 I re-verified or established myself.

`nexus-gap-audit.md` declares: *"Lojix's Horizon consumer and Nexus-shape gaps
are closed at Horizon 0.8.0 `e4871220` and Lojix 1.0.0 `e2c7bdc5`, followed by
the trait-surface correction in Lojix 1.0.1 `b8f7a8cc`"*, listing five closures.
**Three of the five hold cleanly. One holds only in part. One holds on the wire
with a caveat. And the blanket sentence is not supportable, because two
invariants the audit does not mention are unmet at that revision.**

Every claimed version number is correct: lojix 1.0.1, horizon-lib 0.8.0, nexus
0.1.1, signal-lojix 1.1.0, meta-signal-lojix 2.2.0.

### 9.1 Separate Nexus / client / offline-tool packages — **closed**

`lojix@b8f7a8cc:Cargo.toml:11` — five workspace members producing `lojix-nexus`,
`lojix`, `lojix-meta`, and five offline tools. Two sockets, one CLI per socket,
meta CLI named `lojix-meta`. This matches the Nexus authority exactly, and it is
the shape Orchestrate 0.31.0 also achieves.

### 9.2 Persistent configuration and exact meta-Configure transitions — **closed**

The strongest part of the flow's work, and it survived every check. The durable
`ConfigurationState { desired_configuration, meta_configure_occurred }` lives in
Lojix's own sema table `nexus_configuration`
(`lojix:src/lib.rs:40, 557, 1124-1130`); ordinary `Configure` is refused with
`OrdinaryConfigureClosed` once the marker is set
(`nexus:src/configuration.rs:57-75`); `ReverseConfiguration` appears **only** on
the meta contract (`meta-signal-lojix@901e5da6:ethos/signal.ethos:7`) and
ordinary `Configure` is on the ordinary contract
(`signal-lojix@3a57717e:ethos/signal.ethos:6`) with `MetaConfigureOccurred`
reported in every receipt.

This is precisely the "First configuration" paragraph of `Vision/nexus.md`,
realised. It is also exactly what Orchestrate 0.31.0 lacks (§3.2) — so the
pattern exists and works; Orchestrate simply has not adopted it.

### 9.3 Copy-only historical-store migration — **closed**

`lojix:src/lib.rs:2727-2754` validates, refuses if the target exists, `fs::copy`s,
opens the copy, and on failure removes only the target. The source is never
opened for write, renamed or deleted. Driven by a separate offline binary
(`tools/src/lojix-migrate-configuration.rs`). Opening a legacy store in place is
refused, not silently upgraded.

### 9.4 Kameo-driven processing — **closed only in part**

Kameo is present and two actors exist (`DeployJobs`, `TestJobs`,
`lojix:src/daemon.rs:590, 849, 1133, 1201`). But:

- The **ordinary socket never touches an actor**. `serve_ordinary`
  (`src/daemon.rs:420-443`) drives `execute_request` directly on the connection
  task; Configure, Query, CheckHostKeyMaterial, Watch and Unwatch all go that way.
- On the meta socket only `Deploy` and `Test` reach an actor (`:455-463`);
  `Configure`, `ReverseConfiguration`, `Pin`, `Unpin`, `Retire` do not (`:464-468`).
- Even for `Deploy`, the actor is an admission gate and a counter, not the
  processor: `launch_pipeline` (`:646-656`) does
  `tokio::spawn(async move { engine.drive_submitted_deploy().await; … })`. The
  engine runs on a bare Tokio task; the actor only decrements a count.

So `Vision/nexus.md`'s *"The engine inside a Nexus is driven by Kameo actors"* is
not what the code does. Lojix is nearer than Orchestrate — which has no Kameo at
all — but "closed" overstates it.

### 9.5 The Horizon consumer edge — **closed on the wire, with a build-graph caveat**

Horizon 0.8.0 emits final generated types; `lojix:Cargo.toml:29` pins
`horizon-lib` with `default-features = false`, turning off horizon's
`default = ["datom"]`; the already-actualized value crosses the wire as
`ActualizedDeploySubmission.{ DeploySubmission Option<HorizonDefinition> }`
(`meta-signal-lojix:ethos/signal.ethos:33`); text decoding lives in the meta CLI
(`clients/meta/src/lib.rs:90-104`), not the Nexus. A grep of the Nexus-path
modules found no wire-side text decoding.

Caveat, and it echoes §3.1 in a different key: `signal-lojix@3a57717e:Cargo.toml:8,20-21`
and `meta-signal-lojix@901e5da6:Cargo.toml:8,21-22` declare `build = "build.rs"`
with `ethos-zero` as a **build-dependency**, and `ethos-zero` pulls
`datom-codec` and `protos`. Build-dependencies are not dev-dependencies, so
Datom and Protos sit in the Nexus's non-dev graph as build edges even at
`default-features = false`. They do not reach the emitted binary. Unlike
Orchestrate's case this is generation-time only — but it means neither project's
"Datom-free daemon" claim is true without qualification.

A second caveat: `lojix/Cargo.toml:15` sets `default = ["tools"]`, so any
consumer depending on `lojix` without `default-features = false` gets Datom and
Protos. The separation rests on build-flag discipline, not a structural boundary.

### 9.6 Two invariants the gap audit does not mention, and which are unmet

**Observation is not a subscription in Lojix either.** The same failure as
Orchestrate's (§3.3a), and here it is disguised by a complete-looking contract.
`signal-lojix:ethos/signal.ethos:8,11,18,84` declares `WatchDeployments`,
`Unwatch`, and `Watching.SubscriptionOpened { SubscriptionToken CommitSequence }`.
The implementation (`lojix:src/schema_runtime.rs:2695-2711`) allocates a counter
value from a bare `AtomicU64::fetch_add` and returns one reply. There is no
subscriber registry anywhere in the tree — no channel, no broadcast, no list of
open watches. `close_subscription` (`:2712-2717`) echoes the token back without
checking it, so the declared `SubscriptionTokenUnknown` and
`SubscriptionAlreadyClosed` rejections are unreachable. The transport forecloses
streaming regardless: `serve_ordinary` reads one body, writes one frame, closes.

A `WatchDeployments` peer therefore receives neither the state on open nor any
change — only an integer and an EOF. The `CommitSequence` / `EventLogPosition`
fields on every reply, together with `Query.ByEventLog`, are exactly a
cursor-polling API: re-issuing `Query.ByEventLog` is the only way to follow
changes. The lojix skill states the consequence plainly — *"The current `lojix`
executable exchanges one request for one reply and exits. It cannot consume
ongoing subscription events… re-query."*

Credit where due: the Nexus's own deploy observer *is* event-driven —
`src/schema_runtime.rs:6066-6086` subscribes to zbus
`receive_property_changed::<String>("ActiveState")` before its first read. Clock
polling does exist, but only in the offline bootstrap tool
(`src/bootstrap.rs:1216-1233, 1274-1291`, a 100 ms sleep loop over systemd unit
state), not on the Nexus path.

**Traits-first and no-free-functions are broadly unmet at the revision the audit
calls "the trait-surface correction."** Relayed counts, with the caveat that the
counting script is approximate (±) though each named site is cited:

- ~112 module-level non-`main` `fn` definitions outside `#[cfg(test)]`; ~47 even
  excluding the `feature = "tools"` bootstrap module. Named offenders on the
  Nexus path: `src/daemon.rs:36,43` (`decode_meta_request`, `encode_meta_response`
  — wire codec verbs with no owning noun), `src/daemon.rs:108`
  (`async fn run_daemon`, ~60 lines of daemon lifecycle as a floating verb,
  called from `impl Runnable for Daemon` one line above), `src/lib.rs:262`
  (`single_inline_datom_argument`, public API), and nine validators at
  `src/lib.rs:615-681`.
- `canonical_nix_store_root` and `credential_like` each appear **three times**
  (`src/lib.rs:637,681`; `src/adapters.rs:762,780`; `src/schema_runtime.rs:54,73`).
  Triplication is the missing-type signal the skill describes.
- **19 zero-sized types whose sole behavior is an identity function.**
  `src/schema_runtime.rs:101-147` and `:175-235` define `Watching`,
  `WatchRejected`, `Queried`, `DeployAccepted`, `Pinned`, `Tested` and thirteen
  more, each as `pub struct X; impl X { pub fn new(p: P) -> P { p } }` — a ZST
  with an inherent method returning its argument unchanged, whose `new` does not
  return `Self`, with `#[allow(clippy::new_ret_no_self)]` at `:94` and `:150`
  silencing the lint that catches exactly this. The header calls them
  "deliberately value-only shims." Against *"A zero-sized type with behavior is a
  namespace pretending to be a thing"*, these are the textbook case.
- No in-code exception notes of the form the skill requires were found at these
  sites.

### 9.7 The nexus library, and a naming trap — witnessed by me

§3.3c already records that `nexus` 0.1.1 is 131 lines covering the configuration
lifecycle only, and postdates both runtimes it was meant to found. Lojix does
use it, but at exactly five sites (`lojix:src/lib.rs:40, 1104, 1156, 1173, 1188`).

A trap worth recording for anyone auditing after us: everywhere **else** in
Lojix, `nexus::` is not the library. `src/daemon.rs:52` and
`src/schema_runtime.rs:27` both do `use crate::runtime_flow::{self as nexus, …}`,
so `nexus::SignalInput`, `nexus::NexusAction` and dozens more are local Lojix
types. There is a third `nexus` — `pub mod nexus` inside `src/runtime_flow.rs:417`,
reached as `nexus::nexus::Nexus<…>`. Grepping `nexus::` would substantially
overestimate how much Nexus core is shared. The actual reusable engine
abstraction is `triad-runtime` (`src/runtime_flow.rs:423-445`), not `nexus`.

Two further observations on the released revisions:

- `lojix/Cargo.toml:39,44` tracks `triad-runtime` and `sema-engine` by
  `branch = "main"` — **unpinned**. A revision called a clean 1.0.1 release does
  not pin two of its core runtime dependencies.
- At lojix main `23f09f2`, `Cargo.toml:3` is still `1.0.1` although all three
  pinned contracts moved (signal-lojix 1.1.0→1.2.0, meta 2.2.0→2.3.0, horizon
  0.8.0→0.9.0). Under *"the crate's semver is the wire's semver, and consumers
  pin it"*, a consumer pinning lojix 1.0.1 now gets two different wire
  vocabularies under one version number.

### 9.8 The audited revisions are no longer main — witnessed by me

Every Lojix-side revision in the brief has been superseded on `origin/main` by
later work (the Chroma/fixed-location series): lojix `b8f7a8cc` → `23f09f2`
(8 commits), horizon-rs `e4871220` → `8f4240e` (7 commits), signal-lojix
`3a57717e` → `3322cf0` (5), meta-signal-lojix `901e5da6` → `6302a91` (6). The
Orchestrate-side revisions are still main. Relayed: the later Lojix commits touch
no production `src/`, so none of §9.1–§9.7 changes; horizon-rs gained a
fixed-location projection and bumped to 0.9.0.

### 9.9 The shared Orchestrate checkouts are dirty with the WIP — witnessed by me

`shutdown-runtime.md` records *"`jj status` after push: clean."* It is not clean
now. `/git/github.com/LiGoldragon/orchestrate` has HEAD at `1bc55af1` (main,
0.31.0) with ten modified files whose content is **byte-identical to the WIP
commit `cf0dfef2`** (`git diff cf0dfef2 -- .` is empty). `signal-orchestrate` and
`meta-signal-orchestrate` carry the same shape of dirt.

So anyone building Orchestrate from the shared checkout builds the WIP the flow
itself calls *"an intentionally unfinished, uncompiled checkpoint… not suitable
for main or deployment"* — not the 0.31.0 release. Whether this dirt is the
flow's own residue or a later flow's in-flight work I could not establish; it is
recorded here so no one mistakes the checkout for the release. **Unknown.**

---

## 10. Hypotheses

Named as hypotheses because I did not establish them.

1. **The Datom-linking daemon (§3.1) is a gate-design failure, not an
   implementation one.** The manifest expresses the right intent. A gate that
   asserted on the *built artefact* — e.g. that the packaged `orchestrate-nexus`
   contains no Protos symbols — would have caught it; the per-package `cargo
   tree` cannot. The same shape of gate would also catch regressions.
2. **The migration misreading (§4.2) is what an audit performed after the fact
   cannot catch.** The port was designed against a remembered shape of the
   deployed store rather than a read one, and the compliance audit that followed
   checked the new code against Vision, not the new code against the running
   system. A pre-port read of `5f016531:src/store.rs` — the very file the report
   cites — would have shown it.
3. **The duplicate `ethos-zero` revisions (§3.5) indicate the port is mid-flight,
   not settled.** The WIP branches move to a *third* generator revision. The fix
   is to finish the sequence and re-cut the signal crates, not to patch the lock.
4. **The unnamed gaps in `nexus-gap-audit.md` were omitted because it was written
   against the released code, while the fuller list in `shutdown-runtime.md` was
   written against the remaining work.** Two documents with different scopes, one
   of which claims to supersede the other. The superseding claim is the problem;
   the shorter list is not the authoritative one.
5. **The Lojix claims were checked against manifests and file names rather than
   against behavior.** Relayed, and the split fits: the three closures verifiable
   from a manifest or a small focused module — separate packages, configuration
   lifecycle, copy-only migration — hold cleanly, while the two requiring a read
   of what the runtime actually does — Kameo, and the unstated subscription and
   traits invariants — do not. The same pattern produced §3.1 in Orchestrate: a
   manifest-level check standing in for an artefact-level fact.
6. **The Lojix watch surface was designed contract-first and its transport was
   never built.** Relayed. The vocabulary is complete and coherent — token,
   commit sequence, three rejection reasons, a close/closed pair — while two of
   the rejections are unreachable and the connection model is structurally
   single-frame. If so, making `Observe` a subscription is a change to the
   connection model in `daemon.rs`, not a small engine fix, and the same is true
   of Orchestrate. A report calling that gap closed understates the work
   substantially.
7. **The 19 identity-function ZSTs look like scaffolding from an earlier port**
   that routed through per-variant wire types and was later flattened to
   `payload → payload`. Relayed, untested: if so they are deletable by replacing
   `ordinary::Watching::new(x)` with `x`, removing the largest single cluster of
   skill violations in the tree along with two lint suppressions.

---

## 11. Unknowns

Kept unknown.

- **Whether the Datom quoting change in the deployment patch is required, and
  what it implies for existing bare-path callers** (§8). Determining it needs a
  build.
- **Whether 0.31.0 in fact opens the live store cleanly.** My §4.2 conclusion is
  a deduction from identical guards and layouts, not an execution. Confirming it
  needs an isolated copy and a run, which is outside this audit's authority — and
  is the probe `port-preparation.md` step 4 should have specified.
- **Whether `mind`, `orchestrator-judge`, `signal-orchestrator-judge` and
  `persona` are live, dormant, or retired** (§3.5). Their pins are witnessed;
  their status is not. "Update every consumer" bears on them only if they are
  consumers in fact.
- **Whether the absent router and shared signal repository (§3.4d) are
  deliberately deferred.** I found no record either way.
- **Which name the living wants for the meta CLI** (§8). Two Vision statements
  conflict and a relayed decision ledger sides with the older one.
- **Whether the dirt on the shared Orchestrate checkouts is this flow's residue
  or a later flow's in-flight work** (§9.9). Witnessed that it is byte-identical
  to the WIP commits; its provenance is not established.
- **Whether `triad-runtime`'s listener could support a streaming connection
  without changes to Lojix** (§9.6). Relayed as unknown by the sub-audit, which
  did not audit `triad-runtime` or `sema-engine` — both of which Lojix 1.0.1
  tracks by `branch = "main"`, unpinned.
- **Whether any out-of-tree consumer polls the Lojix ordinary socket.** The
  sub-audit found no in-repo consumer of `WatchDeployments` at all; a CriomOS unit
  or deploy script could be re-issuing `Query.ByEventLog` unseen.
- **The exact free-function count in Lojix** (§9.6). The ~112 figure comes from a
  brace-depth script and should be read as an order of magnitude; each
  individually named site is cited.
- **The cause of the 0.30.0 package containing `orchestrate-store-migrate` and
  `orchestrate-upgrade-preflight`**, which `runtime-port.md` presents as part of
  0.31.0's five executables. Both are present in the deployed 0.30.0 `bin/`. Not
  a contradiction — but it means those two binaries are not new work of this
  port, and the report does not say so.

---

## 12. What I did not audit

- I ran no build, no test, and no Nix evaluation; every "passed" figure in the
  flow's witnesses is relayed, not verified.
- I did not decode the live `.sema` archive; §4.2's conclusion about its contents
  is a deduction from the running binary's guards.
- I did not audit Ethos Zero, Datom, Protos, Sema Engine or `triad-runtime`,
  which are outside this slice.
- I did not search psyche exhaustively for superseding records on the meta CLI
  name or on routing.
- §9 is relayed from a sub-audit of this flow, not read by me line by line. I
  verified its version claims, its revision-currency claims and the Orchestrate
  working-tree finding myself; the Lojix source citations stand on its reading.
- I did not re-audit Spirit. Note only that `reports/spirit-nexus-audit.md`
  records five Spirit Nexus gaps found on 2026-09-10, and that later the same day
  the living ordered Spirit and Mirror marked deprecated — so that audit's
  subject is superseded and its effort does not bear on this slice.

---

## Sources

**Witnessed by this flow**

- Live system, 2026-09-11 17:07 −0600: `systemctl --user show orchestrate-nexus`,
  `journalctl --user -u orchestrate-nexus`, `ps -p 2094`, `who -b`,
  `ls /run/user/1001/orchestrate-nexus/`,
  `ls /home/li/.local/state/orchestrate-nexus/`,
  `strings -a /nix/store/hnzql8g1ybpbxk1gqfrdmjfji6winm7x-orchestrate-0.30.0/bin/orchestrate-nexus`,
  and one ordinary `orchestrate 'Observe.Locks'`.
- `/git/github.com/LiGoldragon/orchestrate` at `1bc55af1859e41a7a8310f05c6b3588b8da47a65`:
  `Cargo.toml`, `Cargo.lock`, `flake.nix`, `ARCHITECTURE.md`, and
  `crates/orchestrate-nexus/src/{main,lib,defaults,transport,store,ordinary}.rs`,
  `crates/orchestrate/src/main.rs`, `crates/orchestrate-nexus/tests/live_nexus.rs`.
- Same repository at `5f016531e765d9b679a86cc47a2d75eaca43d624` (deployed 0.30.0):
  `Cargo.toml`, `src/store.rs`.
- Same repository at `cf0dfef298e20e0733f142c3a74a9b16aced7fd9`
  (`flow857335-nexus-lifecycle-wip`): `Cargo.toml`, and `git grep` for
  `kameo`/`Actor` across its `crates/`.
- `/git/github.com/LiGoldragon/signal-orchestrate` at `0efc9fda` and `e3ea414c`,
  and `/git/github.com/LiGoldragon/meta-signal-orchestrate` at `7d81bd96` and
  `eb6df08e`: `Cargo.toml` and `ethos/signal.ethos`; version history of
  `signal-orchestrate` 0.18.0→1.0.4 and `git diff 8bdd51f 0efc9fd -- ethos/`.
- `/git/github.com/LiGoldragon/nexus` at `a84bfa960c0d5c02d30048c4bbbc67dfef79a67c`:
  `Cargo.toml`, `src/lib.rs`, `src/configuration.rs`.
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:138`,
  `modules/home/profiles/min/orchestrate.nix`,
  `checks/orchestrate-service-path/default.nix`,
  `checks/orchestrate-wrapper-fallback/default.nix`.
- `/git/github.com/LiGoldragon/CriomOS/checks/lojix-ownership/default.nix:8,195-197`.
- Revision currency and working-tree state of `orchestrate`, `signal-orchestrate`,
  `meta-signal-orchestrate`, `lojix`, `horizon-rs`, `nexus`, `signal-lojix` and
  `meta-signal-lojix`: `git branch --contains`, `git log <rev>..origin/main`,
  `git status --porcelain`, and `git diff cf0dfef2 -- .`.
- `cargo tree --offline` against an unmodified tarball export of orchestrate
  `1bc55af1` in scratch; no build, no network.
- Authority: `/home/li/primary/Vision/{nexus,signal,sema,orchestrate}.md`; the
  `nexus`, `nexus-rationale`, `orchestrate`, `lojix`, `spirit`, `behavior`,
  `psyche` and `flow-evidence` skills.
- Order provenance: `/home/li/primary/flows/564f55/log.md:15-16,30`;
  `/home/li/primary/flows/857335/log.md`.

**Relayed, read as claims**

- `/home/li/primary/flows/857335/reports/{runtime-port,nexus-gap-audit,cutover-preparation,port-preparation,shutdown-runtime,spirit-nexus-audit,skeptical-opus,skeptical-sol}.md`
  and `witnesses/runtime-port.md`.
- `/home/li/primary/flows/857335/reports/orchestrate-deployment.patch`.
- Two parallel read-only sub-audits launched by this flow — one on surviving
  compatibility paths and consumer pins, one on Lojix/Horizon/Nexus fidelity at
  lojix `b8f7a8cc`, horizon-rs `e4871220`, nexus `a84bfa96`, signal-lojix
  `3a57717e` and meta-signal-lojix `901e5da6`. Findings attributed to them are
  marked relayed in §3.5 and §9; the load-bearing ones I re-verified are marked
  witnessed. Neither sub-audit wrote to any repository or service.

**This flow's own witnesses**

- `/home/li/primary/flows/f6db8d/witnesses/runtime/live-service.txt`
- `/home/li/primary/flows/f6db8d/witnesses/runtime/store-layout-equivalence.txt`
- `/home/li/primary/flows/f6db8d/witnesses/runtime/live-store-generation.txt`
- `/home/li/primary/flows/f6db8d/witnesses/runtime/daemon-datom-feature-unification.txt`
- `/home/li/primary/flows/f6db8d/witnesses/runtime/orchestrate-authority-gaps.txt`
- `/home/li/primary/flows/f6db8d/witnesses/runtime/consumer-pins.txt`
- `/home/li/primary/flows/f6db8d/witnesses/runtime/sequencing.txt`

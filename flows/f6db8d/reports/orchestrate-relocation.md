# A relocated Orchestrate store: what it is, who declares it, and where the declaration lives

Subflow of main flow `f6db8d`, 2026-09-12. Brief: `reports/orchestrate-actor.md`
landed orchestrate 0.34.0 with a store copy guard whose consequence is a dead
end — a deliberately relocated store cannot start, because the observed-location
record lives inside the store and only a running Nexus can change it. Design the
recovery on ontological grounds; research how Postgres, etcd and systemd handle
a moved data directory and choose; implement, with an isolated-daemon test on
scratch paths showing copy refused, move accepted after the declared recovery,
and tampering detected; full gate; bump; push main.

Marks used below: **witnessed** — this thread ran the command or opened the file
and the text is what came back; **relayed** — a named source says so, not
re-verified here; **this flow's inference** — reasoning of this thread, neither
a ruling nor an observation.

## The answer in one paragraph

0.34.0 recorded the store's **path**, and a path is an address rather than an
identity. That single conflation is the whole dead end: record only the address
and every change of address looks alike, so a move is refused for exactly the
reason a copy is. The store file has an identity of its own and the filesystem
will give it — device and inode — and recording that splits the one refused case
into three. The same address is **settled**, whatever file is there now. The same
file at a new address has **moved**: one file cannot be two claimants, so there
is nobody for it to be mistaken for and nothing for anyone to declare — the
commonest relocation there is, `mv` within a filesystem, now needs no ritual at
all. Only a *different* file at a new address is **carried**, and that remains
refused, because it is a copy as far as anything can tell — including when it is
a move that crossed a filesystem and arrived as new bytes exactly as a
duplication does. For that residue there is a declaration: the owner says which
one store this is and where it now lives, writing it **into the store** through
a second executable that opens the store file with **no Nexus running**, having
first been made to show that nothing remains at the origin and nothing holds the
sockets. The declaration names one move, is honoured by that move alone, and is
spent by the commit that records the new address.

## The ontology

### What a relocation is

When a store is found somewhere other than where its own record says it was
bound, there are exactly two possible worlds:

1. **A duplication.** The file at the recorded address still exists, or its
   Nexus still runs. Two claimants now bear one record, and the socket paths in
   that record belong to the one still serving.
2. **A relocation.** There is one store; only its address changed. Its identity
   is untouched.

The distinguishing fact — *is there still another claimant* — is not in the
store. It cannot be: the store holds only what it was told, and both worlds tell
it the same thing. This is why 0.34.0 could not decide and why no amount of
recording inside the store, on its own, ever could.

But part of the distinction *is* available, and 0.34.0 threw it away. A
duplication makes a **new file**; a `rename` does not. So the identity question
"is this the same store" has an answer for the case that matters most, and only
the cases where the bytes were carried without the file remain genuinely
undecidable. That is **this flow's inference**, and it is the load-bearing move
of this design.

### Who is entitled to declare one

The owner, and only the owner — meaning here whoever may write the store file.

Not the Nexus, by inference from an absence. The tempting shortcut is: if
nothing is at the recorded address and nothing holds the sockets, accept
silently. It is *safe in fact* and wrong in entitlement, for two reasons.
**First, an absence is evidence and not consent**: `rm` and the second half of
`mv` leave the same empty path behind, so a guard that read consent off an empty
path would consent on behalf of whoever deleted a file. **Second, it admits
every stale copy whose original has since gone** — a restored backup is exactly
that shape — with nobody having said anything, on a machine where the original
was later moved away and the sockets happen to be free. It is also the same
mistake 0.34.0's socket claim was built to stop making: *"the question is 'does
this path belong to somebody else', and connecting to the socket answers a
different one"* (**witnessed**, `transport/socket.rs` module doc). "Is the
origin gone" answers "is there a file there right now", not "did the owner move
this store". **This flow's inference.**

Not an ordinary peer either: the ordinary authority admits whoever the
filesystem let through, and a store's identity is not an ordinary matter.

### Where the declaration lives, so that a copy is still refused

**Inside the store.** A sidecar beside the store is copied along with it by
every means that produces a dangerous copy — `cp -r`, `rsync`, `tar`, a snapshot
of the directory — so a sidecar would admit precisely the copies it exists to
refuse. It is also unauthenticated text that a stale declaration could leave
standing indefinitely.

Inside the store the declaration is copied too, and is harmless there, because
it does not grant a permission — **it names a transition**: the store that was
at *origin* is now at *destination*. A copy taken afterwards is at neither end
of it. A declaration lifted into some other store names a move that store never
made. And a declaration that admitted any destination would be the guard given
up rather than recovered from. So `Relocated::admits` requires both ends to
match and to differ from each other (**witnessed**, `nexus/src/relocation.rs`).

The one thing that cannot work is the shape the brief offered as a candidate: **a
declaration carried in the meta Configure on first start.** It fails twice.
Structurally, the Nexus finds its store *before* it reads its configuration —
which is the living's own ordering, *"first it should try to get its state from
the default location for its Sema database"* (**relayed**,
`flows/01a03d6e/vision/archive-nexus.md`, 2026-08-26) — so the meta socket a
client would ask through is named by the very store whose right to those paths
is in doubt. A refused store that opened its meta socket in order to ask
permission would have bound, in order to ask, the paths belonging to the Nexus
still serving at the original. And even setting that aside, 0.34.0 already
established that a copy opened by the same user on the same machine derives *the
same* built-in defaults, so falling back to defaults does not separate the cases.
**This flow's inference**, resting on the living's ordering.

## What the research said, and where it changed the design

Relayed from a research subflow of this thread, which cited primary sources for
every claim; the citations are listed under **Sources**. Not re-verified against
those sources by this thread, except where marked.

| | Who may declare a move | Where the declaration lives | Server running? |
|---|---|---|---|
| PostgreSQL | nobody — the question is not asked | nowhere durable; `postmaster.pid` line 2 is rewritten each start, `pg_control` has **no path field at all** | n/a |
| etcd | the operator, via an offline tool that rewrites identity | *inside the data*: `NodeID`/`ClusterID` in the WAL metadata record | **no** — `etcdutl` "operate[s] directly on etcd data files" |
| systemd | systemd itself, from *configuration*, for state dirs; the image builder, offline, for machine identity | `/etc/machine-id`, outside every data store, with the three-valued alphabet absent / `uninitialized` / empty | offline for identity |

Three findings changed or confirmed the design:

**1. etcd is the closest analogue and it is this design.** The sanctioned ritual
for "this data is now a different claimant" is `etcdutl snapshot restore`, an
**offline** tool that rewrites identity inside the data, and its justification is
stated negatively in exactly our terms: *"Restoring overwrites some snapshot
metadata (specifically, the member ID and cluster ID) … This metadata overwrite
prevents the new member from inadvertently joining an existing cluster."* etcd
also offers the shape the brief floated as a candidate — a declaration made to a
running server, `--force-new-cluster` — and files it under **"Unsafe feature:"**,
documented as "strongly discouraged … it will panic if other members from
previous cluster are still alive". That is independent, cited support for
refusing the meta-socket candidate on grounds beyond our own circularity.

**2. `pg_resetwal`'s interlock is the lock file, and that inverted the tool's
world-check into its strongest half.** Postgres documents that `pg_resetwal`
*"will refuse to start up if it finds a server lock file in the data
directory"*. The lock file is thus the interlock for the **offline tool**, not
only for the server. 0.34.0 had already put an advisory `flock` beside each
socket path; taking those claims in the relocation tool is the same inversion,
and it closes a hole the origin check cannot see — a store can be unlinked while
the Nexus serving from it runs on from the open file, so an absent origin is no
proof of an absent claimant.

**3. Postgres identifies `$PGDATA` by `dev_t`/`ino_t`, not by path** — in the
shared-memory header, with `PGSharedMemoryAttach` rejecting a segment whose
device and inode do not match as `SHMSTATE_FOREIGN`. The consequence is that a
same-filesystem `mv` is transparent to Postgres and needs no ritual, while a
copy gets a new inode. **This is the finding that reshaped the record**, and it
arrived from research rather than from our own reasoning. Postgres pays for it
by having no durable location record at all, so "copied" is invisible to it too;
we keep the record and get both.

**No sidecar anywhere.** None of the three uses an operator-written sidecar for
move-versus-copy. The nearest thing, `/etc/machine-id`, is a sidecar to the
*machine* rather than to any data store.

### One check made before adopting the inode

An inode identity is dead machinery if the store rewrites its own file, so this
was **witnessed** before the design was taken, in a scratch test since deleted:
a store opened, situated, given forty Locks, closed and reopened kept
`dev=66306 ino=34756431` throughout — the sema engine writes in place. Had it
not, the `Moved` case would have been unreachable and only the declaration would
have landed.

## What the psyche has and has not said

A psyche search of `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/` and
`flows/*/notion/` was run by a subflow of this thread. **Relayed**: the psyche
has said **nothing** about relocating or moving a store, about store copies,
about sidecar files, about any concrete store path (the string `.sema` does not
occur in the corpus), about machine or host identity as a property of a Nexus,
or about **any privileged offline tool that operates on a store without the
Nexus running**. `Vision/nexus.md` states that *"The nexus and sema documents
are undesigned"*, and the standing instruction for this exact situation is the
living's, typed 2026-09-12: *"I cant really answer much right now, but the
vision is imperfect. Use common sense and research good ontology and software
anatomy to make better design decisions."*

Two pieces of psyche bear on the design and are recorded as tensions rather
than as endorsement:

- **The meta socket is the only privileged surface the psyche has described.**
  *"one of these sockets, the meta-socket, is going to be privileged. And sort
  of like any system needs a root user"* — **relayed**,
  `flows/e06e4c07/vision/archive-nexus.md`. Every authority statement in the
  corpus routes through it, and the psyche has never sanctioned a path that
  bypasses the running Nexus. The argument for doing so here is the psyche's own
  ordering (store first, configuration out of it), which makes the store
  structurally prior to the meta socket and therefore makes the meta socket
  unable to settle a question about the store's identity without circularity.
  **This flow's inference**, and the point most worth the living's attention.
- **"There should be no bootstrap binary."** **Relayed**,
  `flows/01a03d6e/vision/archive-nexus.md`. `orchestrate-relocate` is not one:
  the Nexus still starts with no arguments and no helper, every time, and the
  tool is reached only after the operator has physically moved a file. Its
  sibling `orchestrate-upgrade-preflight` is the existing precedent in this
  repository for a second executable that opens the store without a Nexus. Still
  a tension worth naming.

## What landed

| repository | from | to | revision |
|---|---|---|---|
| `nexus` | 0.3.0 `4ed2696c` | 0.4.0 | `c15344e26cf4258426fae3b03240d7e7c3a1b5fa` |
| `nexus` | 0.4.0 | 0.5.0 | `c495f2acbfff57e017092b9cc1fbf9f73ca2badf` |
| `orchestrate` | 0.34.0 `a73ccec3` | 0.35.0 | _see **Released revisions**_ |

### In `nexus`

`Relocation` with `Relocating`/`Relocated` — the declaration type, universal
because every Nexus binds sockets it must not steal and every Nexus's store can
be carried. `admits` requires both ends of the move to match and to differ from
each other; the same-address case is refused because the only open such a
declaration could be consulted for is one that was never refused, so it can
only ever be a forgery aimed at some other open.

`StoreIdentity` with `Identifying` — a store file as the filesystem names it,
plus the address it was reached by. Two unnamed identities are never the same
file: an absence is not something two addresses can share, and treating it as
one would let every unreadable identity match every other.

`Situation` now carries a `StoreIdentity` instead of a path string, and
`Situated::is_carried -> bool` becomes `Situated::bearing -> Bearing` with
`Settled`, `Moved` and `Carried`. The address decides first and the file second:
the address first because the danger is two stores answering at one set of
socket paths and a store at its own address is the one those paths belong to —
which is why a **restore in place** is `Settled` though the file is new — and
then the file, because at any other address the question is one store under a
new name or a second copy of it.

### In `orchestrate`

`orchestrate_nexus_situation_v2` replaces `v1`. A store still carrying `v1` is
refused by name (`StoreError::SupersededSituation`) rather than admitted with no
guard, because `v1` was written by a generation that could not tell a move from
a copy. 0.34.0 was never deployed — the deploy is listed as owed in
`reports/orchestrate-actor.md` — so no real store is expected to reach this
branch; it exists so that one which does is refused rather than silently
unguarded. Backward compatibility is not a design variable, so the family is
replaced rather than migrated.

`orchestrate_nexus_relocation_v1` holds at most one row and usually none: its
own family for the same reason the situation is its own, being neither desired
state nor observed state but an instruction, written by nobody the Nexus can
hear from and read exactly once by the open it was written for.

`OrchestrateStore::open` consults the declaration **only** when the bearing is
`Carried`, and refuses a non-matching one as `UnrelatedRelocation` — distinct
from `CarriedStore`, because "you have not declared this" and "you declared a
different move" are different things for an operator to be told.

`Situates::situate` now writes the new situation and retracts any standing
declaration **in one atomic commit**. So a store can never come to rest with the
old address recorded and the instruction still standing, and an instruction can
never outlive the move it named. The declaration deliberately survives a *failed*
bind, so that a socket that happened to be busy does not cost the operator the
declaration.

`recovery.rs` and the `orchestrate-relocate` executable: the offline declaration
and the two world-checks it must pass. It takes no arguments, deriving the store
path exactly as the Nexus does, so it can only ever act on the store the Nexus
would open — following `orchestrate-upgrade-preflight`. The socket claims it
takes to answer "is anything serving" are held only for the length of the
question and dropped before anything is written: it is asking whether the paths
are free, not taking them. Every refusal leaves the store exactly as it was.

**No wire change, and no new verb.** `signal-orchestrate` 3.0.2 and
`meta-signal-orchestrate` 3.0.2 are pinned exactly as 0.34.0 pinned them, no
contract was regenerated, and `meta-signal-orchestrate` was not touched. That is
a consequence of the ontology rather than a convenience: the operation cannot go
through a running Nexus, so there is no wire for it to be a verb on. It is also
why no producer was repinned — see **Producer heads**.

## Deviations from the brief, and why

**1. No `orchestrate-meta` verb, and the binary is not named `orchestrate-meta`.**
The brief offered "a privileged `orchestrate-meta` verb that runs against the
store file without a Nexus". A verb is wire vocabulary and there is no wire
here; and `orchestrate-meta` is the name of the meta CLI under the living's
ruling that *"meta cli names is <component>-meta"* (**relayed**,
`flows/f6db8d/vision/metaCli.md`). Naming an offline store tool the same thing
as the socket client would put one name on two kinds. `orchestrate-relocate`
names what it does.

**2. `meta-signal-orchestrate` was not regenerated from ethos-zero**, because no
verb was added — see above. The conditional in the brief ("if a verb is added")
was not met.

**3. The declaration does not pin the destination's file identity.** Considered
and declined: the declaration exists precisely for the case where file identity
was *not* preserved, so binding it to file identity at one end only is
asymmetric and buys little — it would catch an operator who declared and then
swapped the file at the destination, at the cost of making a legitimate
re-restore require a re-declaration. **This flow's inference.**

**4. `nexus` took two releases rather than one.** 0.4.0 is the declaration type;
0.5.0 is the store-as-file reshaping, which was adopted only after the inode
probe above. Each was gated and pushed on its own. The first is a strict
addition; the second changes `Situation`'s shape and `Situated`'s methods, and
**witnessed** by grep across `/git/github.com/LiGoldragon`, the only other
repository pinning `nexus` is `lojix`, which pins `a84bfa9` (0.1.1) and does not
mention `Situation` anywhere — so nothing outside `orchestrate` was broken and
`lojix` was left alone.

## The tests, and what each was seen failing against

**Witnessed**, every test below written before the behaviour existed.

| suite | first failure seen |
|---|---|
| `nexus/tests/relocation.rs` (6) | `no Relocation in the root`, `no Relocating`, `no Relocated` |
| `nexus/tests/situation.rs` (11) | `no Bearing in the root`, `no Identifying`, `no StoreIdentity`; `no method named bearing`, `no method named store` |
| `orchestrate` `tests/relocation.rs` (8) | _see **The gate**_ |
| `orchestrate` `tests/carried_store.rs` (8, four new) | _see **The gate**_ |
| `orchestrate` `tests/live_nexus.rs` (15, three new) | _see **The gate**_ |

The three the brief asked for, all in `live_nexus.rs`, driven through the real
`orchestrate-nexus` and `orchestrate-relocate` executables on `tempfile`
scratch roots via `XDG_STATE_HOME` and `XDG_RUNTIME_DIR`, stopped by the process
id the test's own `Child` holds and never by a name or path pattern:

- **copy refused** — `a_copied_store_is_refused_and_will_not_be_declared_a_move`.
  A real Nexus serves, stops; its store is `cp`'d to a second pair of roots
  leaving the original in place. `orchestrate-relocate` refuses and names the
  original, and the Nexus started on the copy still exits naming both
  addresses. Both halves, because a Nexus that refuses correctly and a tool that
  admits wrongly are the same outage.
- **move accepted after the declared recovery** —
  `a_carried_store_serves_again_with_its_state_once_the_move_is_declared`. A
  Nexus takes a Lock, is stopped with `SIGTERM`, and its store's bytes are
  carried to new roots without the file (`cp` then `rm`, which is what a
  cross-filesystem `mv` does). The undeclared start is refused first, which is
  the assertion that the absence alone is not consent. Then
  `orchestrate-relocate` declares, and the relocated Nexus starts and serves the
  same Lock.
- **tampering detected** — the tail of that same test, plus
  `a_declaration_does_not_admit_a_third_path` and the spent-declaration
  assertions in `carried_store.rs`. After the move completes, a copy of the
  relocated store is refused as the copy it is, naming both addresses rather
  than merely failing to bind, and cannot be declared either. A copy taken
  *before* the move completed carries the declaration and is refused as
  `UnrelatedRelocation` with all four paths named.
- **the socket half of the warrant** —
  `a_relocation_is_refused_while_the_nexus_is_still_serving`. The store is
  unlinked from under a Nexus that goes on serving from the open file, which is
  exactly the case the origin check cannot see. The tool refuses, names the held
  socket, and the Nexus it declined to displace is still answering.

`tests/relocation.rs` is the offline tool's own suite: each refusal is asserted
to have **left the store unchanged**, because a recovery tool that half-wrote a
declaration would be worse than one that refused.

## The gate

_Recorded below once the run completed; see **The gate, as run**._

## The operator procedure

_See **The operator procedure, as landed**._

## Sources

- `flows/f6db8d/reports/orchestrate-actor.md` — the 0.34.0 landing this
  continues, and the source of every "0.34.0 did X" statement.
- `flows/f6db8d/vision/designPractice.md`, typed 2026-09-12 — the living's
  standing authorisation for design judgement where Vision is imperfect.
- `flows/f6db8d/vision/metaCli.md`, typed 2026-09-12 — the meta CLI is
  `<component>-meta`.
- Psyche search of `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/`,
  `flows/*/notion/` by a subflow of this thread — the quotations from
  `flows/01a03d6e/vision/archive-nexus.md` (2026-08-26),
  `flows/e06e4c07/vision/archive-nexus.md`, and `Vision/nexus.md`, and the list
  of what the psyche has not said.
- Research subflow of this thread, with primary citations:
  PostgreSQL `src/include/utils/pidfile.h`, `src/backend/utils/init/miscinit.c`,
  `src/backend/port/sysv_shmem.c`, `src/include/storage/pg_shmem.h`,
  `src/include/catalog/pg_control.h`, and
  <https://www.postgresql.org/docs/current/app-pgresetwal.html>;
  etcd `server/etcdserver/bootstrap.go`, `etcdutl/snapshot/v3_snapshot.go`,
  `etcdutl/README.md`, `server/etcdmain/help.go`, and
  <https://etcd.io/docs/v3.6/op-guide/recovery/>;
  systemd `src/core/exec-invoke.c`, `src/libsystemd/sd-journal/journal-file.c`,
  machine-id(5), systemd-firstboot(1), and <https://systemd.io/BUILDING_IMAGES/>.
  **Not re-verified against those sources by this thread.**
- `orchestrate` at `a73ccec3` and `nexus` at `4ed2696c`, the local checkouts
  under lock — the state every "0.34.0 did X" statement is read from.
- `git ls-remote` against the real remote URLs of `nexus`, `orchestrate`,
  `meta-signal-orchestrate`, `signal-orchestrate`, `ethos-zero`, `datom-codec`,
  `protos`, `signal`, `sema-engine` — **Producer heads** and every pushed
  revision.

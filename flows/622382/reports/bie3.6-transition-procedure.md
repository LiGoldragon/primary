# bie3.6 — Flow transition: flow-nexus-040 (0.40.4) to declared flow-nexus.service (0.40.7)

Revised 2026-10-29 at about 21:50 CST, to the rulings of Psyche core Primary
aad413 (relayed by c267bd), set out in §R. Nothing here has been run. The
only production contact was the read-only `Metaflows`, `Configuration`,
`ReadSendOutcomes` and `ReadQueueDeliveries` reads in §B.

Every claim is marked one of three ways:
- **read**: from a source, with file:line, or from the command that showed it
- **inferred**
- **relayed**: from another flow, not checked first-hand

The CriomOS-home change list for Mind core Secondary's hand is a separate
file: `/home/li/primary/flows/622382/reports/bie3.6-criomos-home-changes.md`.

## R. Rulings in force (aad413, its words, condensed only by omission)

- **(a)** "The guard goes in the declaration: flow-nexus.service has an
  ExecStartPre that refuses to start while a Nexus answers Metaflows on the
  socket path … message-nexus.service keeps WantedBy=default.target … The
  transient unit is stopped by hand before the declared one starts."
- **(b)** "The durable rollback state is the previous Home generation, kept:
  rollback is switching back to it and starting the transient unit by the
  recorded command."
- **(c)** "The window is minutes: old store kept until sign-off, work 0.40.7
  accepted in the window is lost on rollback and tolerated; the trackers
  re-nudge what was lost. No replay machinery."
- **(d)** "0.40.7 lands on flow main first; CriomOS-home pins only main
  commits … the new store is seeded by replaying the declarations through
  meta Configure, a Tertiary writes that replay … One Home hand: Mind core
  Secondary …, in order, never raced."
- **(1)** "9 fields is the target, the 0.40.7 shape; the ninth,
  CurriculumNexusPath, is the socket the running 0.40.4 answers in its meta
  Configuration readback, taken from there, not guessed."
- **(2)** "Re-adopt and seed: the counters for flow ids and delivery ids are
  seeded past the old maximum plus a margin …; every awake seat is
  re-adopted by BindSeat, by a Notice to each awake flow asking it to run
  BindSeat on its own address, the trackers first; the flow histories are
  tolerated lost tonight, the transcripts remaining the ledger, named as a
  loss in the night report and as a line in the V1 to V5 store migration
  bead."
- **(3)** "Transient unit by its recorded command first, then the switch back."
- **(4)** "Activate the new Home first, its guard refusing while 0.40.4
  answers, then the hand stop … The replay from the flow-meta Configuration
  snapshot of 38 declarations is right."

## A. Counter seeding: 0.40.7 has no way to do it. This is a code change.

Read at flow `25d260b`, the 0.40.7 re-pin. Paths are under
crates/flow-nexus/src/.

**Meta Configure.** meta-signal-flow `34adbb9` src/generated/signal.rs:100-109
is `pub enum ConfigurationChange { Models, Thresholds, LeaveOuts, Nexus,
SendServers, Metaflows, Investigation, DefaultMinutes }`. None of these sets
any counter. (read)

**Logical-delivery ids.**
- `allocate_logical_cursor` (store/logical_delivery.rs:1145-1161) returns
  `cursor: 1` when the `flow_nexus_logical_delivery_counter` row is absent.
- Ids are `format!("logical-delivery-{cursor:020}")` (:688, :904).
- The counter is only ever written by allocation (:612-616, :712-722,
  :805-811).

(read)

**Queue-attempt and send-outcome ids.** They have their own counters
(store/queue_delivery.rs:62,934, seeded `next_request: 2`, `next_attempt: 4`
in its fixture region; store/send_outcome.rs:16,371). They appear to follow
the same pattern: no write path but allocation (inferred from the same
structure; not traced line by line).

**Flow-number counter.**
- `FlowStoreState { next_flow_number }` (store.rs:1418-1419) is seeded `1` at
  both store creations (:3904, :4742) and advanced only in `reserve_start`
  (:6720-6756).
- `reserve_start` is reached only from `Query::Start` as
  `"legacy-test-start"` (:5091-5096).

(read)

**Store open.** It seeds and never imports counters. Nothing in `Engine::open`
or the upgrade paths takes a counter value from outside (read: store.rs:4038
names "seeding defaults, importing an older store, or settling prior work",
and its body copies no counter in; inferred from the absence of any counter
argument in `EngineOpen`).

**The six-character FlowIds are not a store counter.**
- A Claude launch's FlowId is claimed through `flow-id` against claim markers
  `flows/.<FlowId>.flow-id` (herdr/reservation.rs:1-9, :64-72; a released
  claim is removed only if its lane is empty, :74-95).
- A BindSeat "claims its FlowId through `flow-id` … No synthetic `flow-…` id
  is minted for it" (UPGRADES.md `25d260b`:359-364).
- 709 claim markers exist in `/home/li/primary/flows` (read: `ls -a`).

(read) So a new store does not reissue a six-character FlowId, because those
claims live on disk, outside the store (inferred).

**Claude session ids.** They are SHA-256 of the ordinary socket path and the
launch request id (herdr/reservation.rs:16-56). Launch request ids are
`"launch".minted_id()`, which uses nanoseconds plus a process counter
(sending.rs:135-153, :480). So they do not repeat across stores (inferred).

**Conclusion.** Seeding the logical-delivery counter, and the queue-attempt
and send-outcome counters, "past the old maximum plus a margin" needs a code
change in Flow. One example would be a meta `Configure` arm or a seed
argument on the configure-only start. No such path exists in 0.40.7
`25d260b`. Ruling (2)'s flow-id half has nothing to seed in practice: the
FlowIds anyone cites are the six-character claim aliases, which do not
restart. The `flow-{:016x}` counter only names legacy `Query::Start`
launches.

## B. Old maxima, read from production (2026-10-29 21:47–21:48 CST)

Reads, through 0.40.4's own clients only:
`flow Metaflows`, `flow-meta Configuration`, `flow-meta ReadSendOutcomes`, and
`flow-meta 'ReadQueueDeliveries.<Address>'` for all 31 listed Addresses.

| id family | highest seen | where seen |
|---|---|---|
| logical-delivery | `logical-delivery-00000000000000014574` | ReadSendOutcomes; queues max 14560 |
| queue-attempt | `queue-attempt-0000000000000f08` (3848) | ReadQueueDeliveries |
| send-outcome | `send-outcome-000000000000056e` (1390) | ReadSendOutcomes |
| `flow-{:016x}` legacy flow id | none in any read | none |
| six-character FlowId | not a counter (§A); 709 claim markers on disk | `ls -a /home/li/primary/flows` |

(read) These are the highest **seen**. None of these reads exposes the
counter rows themselves, so each figure is a lower bound on the counter at
21:48. The ids keep rising until the old Nexus stops. The figure to seed past
must be read again in C2, immediately before the hand stop (inferred).

## C. V1 to V5 store migration bead

No open or closed bead in `/home/li/primary` is that migration (read: `bd
list --all`, `bd search` for V1, V5, migration, store migration and Memory,
plus a JSON scan of every title, description, design and acceptance for V1
to V5).

The only bead naming it is primary-6qh5 (closed, "flow-ethos and
signal/meta-signal pins built on Prometheus"). Its description quotes the
order: "with the V1 to V5 store migration as a separate batch afterwards".
Nearest open neighbours:
- primary-npl, "Flow's database is Memory: its store path, type names and
  configuration say Memory"
- primary-utz8, "Flow 0.40.6 … migrated to production under the durable
  transition"

The line ruling (2) assigns has no bead to land in yet. Creating one is for
the coordinator; I made no bead write.

## D. The replay's Nexus datom

`/home/li/primary/flows/622382/reports/declaration-replay.datom`, line 1
(read):

```datom
Configure.Nexus.{ /home/li/primary { /nix/store/ma56d8…-codex-stable-flow-client/bin/codex-stable-flow-client /home/li/.codex-next /home/li/.codex-next/app-server-control/app-server-control.sock [ gpt-5.6-sol gpt-5.6-luna ] } { /nix/store/nmr4py…-codex-next-flow-client/bin/codex-next-flow-client /home/li/.codex-next-8mkkxq293hk2 /home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock [ gpt-6.1-sol gpt-6-sol gpt-6-luna gpt-6-astra ] } [ { Claude [ / «!» # ] [ esc esc ] [ enter ] } { Codex [ / «!» ] [ esc ] [] } ] [ Psyche ] /run/user/1001/message/message.sock /nix/store/4gnyn6…-message-0.20.4/bin/message-nexus /run/user/1001/flow40-rt/curriculum/curriculum.sock 60 }
```

**Nine positions**, which is the shape of meta-signal-flow `34adbb9`
ethos/signal.ethos:263:
1. source root
2. stable Codex
3. next Codex
4. harness profiles
5. meta aspects
6. message socket
7. message binary
8. **CurriculumNexusPath = `/run/user/1001/flow40-rt/curriculum/curriculum.sock`**
9. lease 60

**Matches the readback.** The 0.40.4 `flow-meta Configuration` readback at
21:47:35 CST carries the same curriculum socket, and the replay's Nexus body
appears byte for byte inside the readback (read: substring test).

**Rest of the replay.** It holds 7 `Configure.*` datoms: Nexus, Models,
Thresholds, LeaveOuts, SendServers, Metaflows and Investigation. It has no
`DefaultMinutes`, so 0.40.7 seeds 30.
The readback has 38 metaflow declarations, 17 of them Maintained (read:
parse of the readback).

**Gap: transient curriculum unit.** The ninth position is served by the
*transient* `curriculum-nexus-040.service` (`XDG_RUNTIME_DIR=/run/user/1001/flow40-rt`;
read: `systemctl --user cat`). The declared Flow unit `Requires` the
*declared* `curriculum-nexus.service` (CriomOS-home `origin/main` flow.nix:96),
which serves `/run/user/1001/curriculum/curriculum.sock`. The declared Flow
would read through a transient Curriculum that no declaration keeps alive
(inferred). This is open question Q2.

**Home overwrites the replay at each start.** The Home initialize re-applies
its own `Configure.Nexus` at every start (CriomOS-home default.nix:123).
That line must carry the same ninth value, or every start overwrites the
replayed one (inferred from the order: initialize runs after the seed).

## 0. Current state (read 2026-10-29 21:40–21:48 CST)

- **Live Nexus.** `flow-nexus-040.service` is transient and active, PID
  4141427.
  - ExecStart: `/nix/store/9sjii9ynba06nbslwgfki4y83fzax98f-flow-0.40.4/bin/flow-nexus "{ «/run/user/1001/flow/flow.sock» «/run/user/1001/flow/flow-meta.sock» «/home/li/.local/state/flow-040/flow.sema» None }"`.
  - Environment: HOME, XDG_RUNTIME_DIR, PATH, and
    `FLOW_CORE_PRESENTATION_PROMPT=/home/li/primary/flows/e3c8c1/presentation-role.md`.
  - `KillMode=control-group`, `CollectMode=inactive`.
- **Seats.** `Metaflows` lists 31 metaflows: **21 Awake** and 10 Asleep. The
  Awake seats:
  - Field: `{ Field PrimaryCommitting Quaternary }` 4f319f, `{ Field core Primary }`
    22786a, `{ Field core Secondary }` c2b552, `{ Field core Tertiary }`
    eeb644, `{ Field flow Secondary }` 4d05d1, `{ Field tracker Quaternary }`
    bc6c73.
  - Mind: `{ Mind core Primary }` 854b87, `{ Mind core Secondary }` a5d5f5,
    `{ Mind flow Primary }` 568a32, `{ Mind flow Secondary }` bddc36,
    `{ Mind obsidian Primary }` ce1f02.
  - Psyche: `{ Psyche ethos-nexus Secondary }` 3e1ca4, `{ Psyche core Primary }`
    aad413, `{ Psyche core Quaternary }` 9d3dcc, `{ Psyche core Secondary }`
    c267bd, `{ Psyche core Tertiary }` 718f48, `{ Psyche flow Secondary }`
    622382, `{ Psyche tracker Quaternary }` 411196, `{ Psyche obsidian Primary }`
    0c5d27, `{ Psyche obsidian Secondary }` 6aa500,
    `{ Psyche research Secondary }` 265b93.

  (read)
- **Declared Flow unit.** `flow-nexus.service` is Home generation 1090
  `jg7bk51`, running 0.39.0 on `flow-03521`. It is enabled and inactive. A
  hand-written drop-in sets the e3c8c1 prompt. `message-nexus.service` is
  enabled and inactive, with `Requires`/`PartOf`/`WantedBy=flow-nexus.service`.
  (read)
- **Collision witnessed.** The 18:57 activation of jg7bk51 queued starts of
  both declared units; they failed only on the Curriculum dependency. At
  11:22, a declared start wrote `flow-03521/flow.sema` with 0.39.0 before it
  refused on the socket. (read: journal)
- **Startup order.** Configure-only opens the store before it claims the
  socket (flow `fbf6954` main.rs:300, :310). So the guard must precede
  initialize (inferred).
- **No duplicate seat at start.** At start, an Asleep metaflow is woken only
  if its queue holds a `Wake` entry or a successor intent
  (waking.rs:1426-1433 at `25d260b`; read). A seeded store holds neither, so
  0.40.7 launches no seat at start for the 17 Maintained metaflows (inferred
  from that). A `Wake` Send to an Address 0.40.7 sees as Asleep would
  launch a second seat beside its live pane (inferred). That is why
  re-adoption comes before anyone sends Wake (§4 C6).

## 1. Switch gate

All six must hold (Mind flow Primary, accepted):

1. This transition is written in full.
2. The exact Home artifact has been built on Prometheus.
3. The capsule-first rollback has passed for the exact candidate and the
   seeded-store migration (§6).
4. The Memory, the old `flow-nexus-040` unit definition and the old store are
   preserved.
5. The new unit answers `Metaflows`.
6. b6d9ab is the sole operator, with the sequence in §4.

## 2. Preconditions

- **P1. One Home hand.** Mind core Secondary finishes the STT pin and
  reports. The change-list items then go through it, in order. That hand
  builds on Prometheus and activates. This procedure builds no Home.
- **P2. 0.40.7 on flow main.** CriomOS-home pins that main commit. Flow
  `origin/main` was 0.40.0 (`6de10c1`) at the time of reading. (read)
- **P3. Counter seeding exists in Flow (§A).** It must land in the same
  0.40.7 main commit, or ruling (2)'s seeding cannot be done. This is for the
  coordinator to take up.
- **P4. The replay** (§D) is the Tertiary's file from the 0.40.4
  `Configuration` snapshot, 38 declarations, with Nexus in 9 positions. It is
  regenerated at C2 if the declarations change before the cutover.
- **P5. The previous Home generation** is the one current immediately before
  the bie3.6 0.40.7 activation. It is kept and rooted. It should carry the
  guard (change-list item 1).

Names used below:
- `W=/home/li/primary/flows/622382/witnesses/bie3.6-<UTC>`
- `OLD=/nix/store/9sjii9ynba06nbslwgfki4y83fzax98f-flow-0.40.4`
- `NEW` = the flow-0.40.7 path in the artifact
- `NEWSTATE=/home/li/.local/state/<new stateDirectory>`
- `STORE=$NEWSTATE/flow.sema`
- `PREV` = the previous generation's store path

## 3. Preparation (no runtime change)

**A1. Record and root.**
```sh
mkdir -p "$W"
systemctl --user cat  flow-nexus-040.service > "$W/040.cat"
systemctl --user show flow-nexus-040.service > "$W/040.show"
tr '\0' '\n' < /proc/4141427/environ > "$W/040.environ"
nix-store --add-root /home/li/.local/state/flow-040/flow-0.40.4.gcroot --indirect -r "$OLD"
readlink -f /home/li/.local/state/nix/profiles/home-manager > "$W/previous-generation"
PREV=$(cat "$W/previous-generation")
nix-store --add-root /home/li/.local/state/flow-040/previous-home.gcroot --indirect -r "$PREV"
```
- Check: `nix-store -q --roots` of `$OLD` and of `$PREV` each list the new
  gcroot.

**A2. Read the artifact.** The hand gives `<out>`.
`<out>/home-files/.config/systemd/user/flow-nexus.service` must show:
- the guard as the first ExecStartPre
- `NEW` and `NEWSTATE`
- a Configure.Nexus in initialize with the §D curriculum socket in position 8

**A3. Capsule rehearsal (§6)** passes with this `NEW`.

## 4. Cutover

b6d9ab is sole operator. The window is minutes. The order is ruling (4):
activate first, the guard refuses, then the hand stop.

**C1. Quiet state.**
```sh
pgrep -af 'home-manager-generation/activate' || echo none
systemctl --user is-active flow-nexus-040.service flow-nexus.service message-nexus.service
ss -xlp | grep /run/user/1001/flow/
```
- Check: no activation in flight; `active inactive inactive`; only PID
  4141427 on the sockets.

**C2. Final snapshot of the old Nexus**, read-only, through 0.40.4's clients.
```sh
"$OLD/bin/flow" Metaflows > "$W/before.metaflows"
"$OLD/bin/flow-meta" Configuration > "$W/before.configuration"
"$OLD/bin/flow-meta" ReadSendOutcomes > "$W/before.sendoutcomes"
grep -o '{ { [A-Za-z]* [A-Za-z-]* [A-Za-z]* }' "$W/before.metaflows" | sed 's/^{ //' |
  while read -r a; do "$OLD/bin/flow-meta" "ReadQueueDeliveries.$a"; echo; done > "$W/before.queue"
for f in before.sendoutcomes before.queue; do
  grep -oE 'logical-delivery-[0-9]+|queue-attempt-[0-9a-f]+|send-outcome-[0-9a-f]+' "$W/$f"
done | sort -u > "$W/before.ids"
```
- `before.queue` is what the trackers re-nudge (ruling (c)).
- `before.ids` gives each family's maximum to seed past (§B).
- If the declarations differ from P4's, the Tertiary regenerates the replay
  from `before.configuration`.

**C3. Seed the new store**, on a private socket, while 0.40.4 still serves.
```sh
install -d -m 700 "$NEWSTATE"
while IFS= read -r q; do
  systemd-run --user --wait --collect --pipe --quiet -E XDG_RUNTIME_DIR=/run/user/1001 \
    sh -c '"$0/bin/flow-nexus" --configure-only "{ $1/seed.sock $1/seed-meta.sock $2 None }" & c=$!
           while [ ! -S "$1/seed-meta.sock" ]; do sleep 0.05; done
           FLOW_META_SOCKET="$1/seed-meta.sock" "$0/bin/flow-meta" "$3"; wait $c' \
    "$NEW" "$W" "$STORE" "$q"
done < <replay datoms, one per line> | tee "$W/seed.replies"
# then the counter seed, in whatever form P3 lands, past before.ids plus the margin
"$NEW/bin/flow-store-check" "{ $STORE }"
```
- The replay holds Purposes with newlines inside `«»`. It is split as
  `declaration-replay.sh` splits it (newline outside guillemets), not by
  `read -r`.
- The `declaration-replay.sh` script itself refuses `/run/user/1001/flow/*`
  and takes a running meta socket. Run under the configure-only form above,
  it is equivalent (inferred).
- Check: every reply is `Configured.Replaced` or `Configured.Unchanged`, the
  counter seed answers, and flow-store-check prints `Opens.<STORE>`.

**C4. Activate the 0.40.7 generation** (ruling (4)). The hand runs
`<out>/activate`.
- sd-switch starts `flow-nexus.service`. The guard finds 0.40.4 answering and
  refuses, so initialize never touches `STORE`.
- `message-nexus.service` fails on its dependency.
- Check:
  - The journal shows the guard's refusal.
  - `sha256sum "$STORE"` equals its digest after C3.
  - PID 4141427 still answers `Metaflows`.
  - `systemctl --user cat flow-nexus.service` names `NEW` and `NEWSTATE`.

**C5. Hand stop, then start.**
```sh
systemctl --user stop flow-nexus-040.service
sha256sum /home/li/.local/state/flow-040/flow.sema > "$W/old.after-stop.sha256"
ss -xlp | grep /run/user/1001/flow/             # must be empty
systemctl --user reset-failed flow-nexus.service message-nexus.service
systemctl --user start flow-nexus.service message-nexus.service
```
- Check:
  - The 0.40.4 unit is collected.
  - The guard passes. Initialize applies Home's families to the non-empty
    store and skips Metaflows (default.nix:79-80,128-131 at `origin/main`).
  - `wait-declared-flow-ready` exits 0, and the new MainPID is on both sockets.

**C6. Re-adopt the awake seats**, trackers first (ruling (2)).
- **Order:** `{ Psyche tracker Quaternary }` 411196 and
  `{ Field tracker Quaternary }` bc6c73 first, then the other 19 Awake seats
  from `before.metaflows`.
- **What each seat runs:** `flow 'BindSeat.{ <own Address> }'`, which answers
  `Bound.<FlowId>` (UPGRADES.md `25d260b`:359-364).
- **Witness for each seat:** `"$NEW/bin/flow" Metaflows` shows the Address
  `Awake.<same FlowId as before>`.
- **How the Notice reaches a seat is open (Q1).** It cannot go through 0.40.7
  as a Send. To 0.40.7 these Addresses are Asleep, so:
  - a `Wake` Send would launch a second seat (inferred, §0)
  - a queued Send would sit until the very BindSeat it asks for, since an
    adopted seat is handed its queue at adoption (UPGRADES.md `25d260b`:71)

  Two ways it could go:
  - through 0.40.4 before the hand stop, as a pressing Notice saying "when
    `flow Metaflows` answers again, run BindSeat on your own Address", with
    each delivery witnessed by `ReadQueueDeliveries` before C5
  - or typed into each pane through Herdr after C5

**C7. Acceptance.**
```sh
"$NEW/bin/flow" Metaflows > "$W/after.metaflows"
"$NEW/bin/flow-meta" Configuration > "$W/after.configuration"
sha256sum /home/li/.local/state/flow-040/flow.sema | diff - "$W/old.after-stop.sha256"
```
- Check:
  - `Metaflows` answers.
  - The 31 Addresses are present.
  - The 21 seats are Awake with their FlowIds.
  - The 38 declarations equal the replay, apart from Home's families.
  - The first new logical-delivery id is above `before.ids`.
  - The old store is unchanged.

**C8. Sign-off.**
- Record the time.
- `before.queue` goes to the trackers.
- The loss of flow histories goes into the night report and into the V1 to V5
  bead once one exists (§C).
- `flow-040/`, both gcroots and `PREV` stay.

## 5. Rollback

**Trigger.** Roll back on any of these:
- C3: a refused Configure or counter seed, or flow-store-check not `Opens`
- C4: activation fails, or the guard does not refuse, or `STORE` changes
- C5: unit not active, a failed ExecStartPre or ExecStartPost, or
  `start-limit-hit`
- C6: a BindSeat refused, or a second seat launched
- C7: any check failing

The trigger holds until C8. Work accepted by 0.40.7 is lost and tolerated.

**Commands** (ruling (3): the transient first, then the switch back):
```sh
systemctl --user stop flow-nexus.service message-nexus.service
ss -xlp | grep /run/user/1001/flow/            # must be empty
sha256sum /home/li/.local/state/flow-040/flow.sema | diff - "$W/old.after-stop.sha256"
systemd-run --user --unit=flow-nexus-040 \
  --description='Flow Nexus 0.40.4 queue emergency' \
  -p WorkingDirectory=/home/li \
  -E HOME=/home/li -E XDG_RUNTIME_DIR=/run/user/1001 \
  -E PATH=/home/li/.nix-profile/bin:/etc/profiles/per-user/li/bin:/run/current-system/sw/bin \
  -E FLOW_CORE_PRESENTATION_PROMPT=/home/li/primary/flows/e3c8c1/presentation-role.md \
  /nix/store/9sjii9ynba06nbslwgfki4y83fzax98f-flow-0.40.4/bin/flow-nexus \
  '{ «/run/user/1001/flow/flow.sock» «/run/user/1001/flow/flow-meta.sock» «/home/li/.local/state/flow-040/flow.sema» None }'
"$OLD/bin/flow" Metaflows | diff - "$W/before.metaflows"
"$PREV/activate"
systemctl --user is-active flow-nexus-040.service flow-nexus.service
ss -xlp | grep /run/user/1001/flow/
```
- Check:
  - The restored Nexus answers `Metaflows` equal to before. The old store
    holds the seats' old bindings, so no re-adoption is needed (inferred).
  - After `$PREV/activate`, the previous unit's start is refused, by its guard
    or by the socket refusal witnessed at 11:22.
  - Only the 0.40.4 PID is on the sockets.

## 6. Capsule rehearsal (proposed, not run)

The capsule (`/home/li/worktrees/flow-ethos-76e6eb/capsule/flow-capsule.clj`)
gets a takeover mode:
`flow-capsule --takeover <0.40.4 package> <0.40.7 package>`.

- **T0. Old side as a transient unit.** Run the 0.40.4 package by
  `systemd-run --user --unit=flow-capsule-old-<ts>` on the capsule's sockets
  and store, configured 0.40.4-shape, 9-position Nexus.
- **T1. State to lose and to re-adopt.**
  - A Maintained Secondary is Awake.
  - A Quaternary is busy.
  - A queued `Soft.Notice` waits for the Quaternary.
  - Several Sends raise the logical-delivery counter.
- **T2. Snapshot.** Through the 0.40.4 clients, the same reads as C2.
- **T3. Replay and seed.** The Tertiary's replay script works on T2's
  `Configuration`, then the C3 seed, the counter seed (once P3 exists), and
  flow-store-check.
- **T4. Activate first.** Start a declared-like transient unit:
  - `-p ExecStartPre=<artifact guard> -p ExecStartPre=<capsule initialize>`
  - `-p ExecStartPost=<artifact ready>`
  - `-p Restart=on-failure`

  Witness: the guard refuses, the new store is byte-identical, and the old
  side still answers.
- **T5. Hand stop, then start.** Witness the old unit collected, the new
  unit active and ready, and the old store digest unchanged.
- **T6. Re-adopt.**
  - In the Secondary's pane, run `flow 'BindSeat.{ <its Address> }'`.
  - Witness `Awake.<same FlowId>`, and that no second seat was launched.
  - Witness that a Send sent `Wake` to the not-yet-bound Quaternary
    *does* launch a second seat. This shows why C6 comes first.
- **T7. Ids.** Witness that the first new logical-delivery id is above T2's
  maximum.
- **T8. Losses.** Witness that the T1 queued Notice is absent and Past is
  empty.
- **T9. Rollback.** Run the R commands in capsule form: stop the new unit,
  start the old one by its recorded command, then stand in for the switch
  back with an unguarded declared-like start that is refused at the socket.
  `Metaflows` and `ReadQueueDeliveries` equal T2, and the queued Notice is
  present.
- **T10. Teardown.** As today, plus every `flow-capsule-*` unit stopped and
  none listed.

## 7. Open questions

- **Q1.** How does the BindSeat Notice reach the 21 seats? Through 0.40.4
  before the stop, or typed through Herdr after it (C6)? Through 0.40.7 it
  either launches a duplicate (`Wake`) or waits behind the adoption it asks
  for.
- **Q2.** The ninth position names the transient `curriculum-nexus-040`
  socket, as ruled. Does the declared Flow then depend on a transient
  Curriculum, while its unit `Requires` the declared one?
- **Q3 (§A).** Counter seeding is a Flow code change. Should it be one meta
  `Configure` arm covering the logical-delivery, queue-attempt and
  send-outcome counters, with what margin?
- **Q4 (§C).** No V1 to V5 store migration bead exists. Who creates it?
- **Q5.** Every Wake Send between C5 and the end of C6 would duplicate a
  seat. That includes the trackers' beats, which is why the trackers go
  first. Is a hold on other senders' Wake Sends needed for that interval?

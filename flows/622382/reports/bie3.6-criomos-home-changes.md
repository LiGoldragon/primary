# bie3.6 — CriomOS-home changes, in order, for Mind core Secondary's hand

These changes go through one Home hand. Mind core Secondary finishes the STT
pin and reports it first. Then the items below go through that same hand, in
this order, never raced. (ruling (d), aad413)

Every file:line is at CriomOS-home `origin/main` `20994fa5`. Nothing was
changed. The procedure is
`/home/li/primary/flows/622382/reports/bie3.6-transition-procedure.md`.

## 1. Guard ExecStartPre

**What it does.** It refuses to start `flow-nexus.service` while a Nexus
answers `Metaflows` on `$XDG_RUNTIME_DIR/flow/flow.sock`. (ruling (a))

**Where it lands.**
- `packages/flow-deployment/default.nix`:
  - Add a new `guard = pkgs.writeShellApplication { name = "refuse-second-flow-owner"; … }`
    beside `initialize` (:69-70).
  - Add `guard` to the passthru `inherit` list (:189-198).
- `modules/home/profiles/min/flow.nix:107`: `ExecStartPre` becomes a list,
  guard first: `[ "${deployment.guard}/bin/refuse-second-flow-owner" "${deployment.initialize}/bin/initialize-declared-flow" ]`.
- `checks/flow-service-path/default.nix:34` asserts the single ExecStartPre
  string and is updated to match.

**Why the guard runs first.** Initialize opens and writes the declared store
before its own socket refusal. The journal shows this for `flow-03521` at
11:22 on 2026-10-29. (read; flow `fbf6954` main.rs:300 then :310)

**How it should test "answers".** It should treat any accepted connection on
either Flow socket as an owner, not only a reply the client can parse. The
client in the declaration may be newer than the server it meets. (inferred;
Q6 in the procedure)

**Message Nexus.** `message-nexus.service` keeps `WantedBy=default.target`
(`modules/home/profiles/min/message.nix:54-57`), with no change. (ruling (a))

**Suggested order (inferred).** Activate this item as its own generation,
before item 2. The kept previous generation then carries the guard, and
switching back to it in a rollback cannot seat a second owner.

## 2. Pin to a flow main commit

**Where it lands.** `flake.nix:126` `flow.url` moves from `b878b1b` (0.39.0,
on branches only; read) to the flow **main** commit that carries 0.40.7. The
`flake.lock` `flow` node is updated with it.

**Status.** At the time of reading, flow `origin/main` is 0.40.0 (`6de10c1`).
0.40.7 is only on `flow-ethos-76e6eb` (`fbf6954`, re-pinned `25d260b`). This
item waits on 0.40.7 landing on main. (ruling (d))

**Also needed in that commit.** The pinned main commit must also carry the
counter-seeding change ruling (2) needs, which 0.40.7 `25d260b` lacks
(procedure §A).

## 3. Configure shape: 9 positions (ruling (1))

**Where it lands.** `packages/flow-deployment/default.nix:123`, the
`Configure.Nexus` line.

**The change.** Insert the eighth position, CurriculumNexusPath,
between `${message}/bin/message-nexus` and `60`. Its value is taken from the
running 0.40.4's meta `Configuration` readback, not guessed. At 2026-10-29
21:47:35 CST it read `/run/user/1001/flow40-rt/curriculum/curriculum.sock`
(read). The replay carries the same value (procedure §D).

**Why it matters.** Initialize re-applies this line at every start, so the
declared line must carry the same value, or each start overwrites the
replayed one (inferred).

**The type.** meta-signal-flow `34adbb9` `ethos/signal.ethos:263` and
`src/generated/signal.rs:49-59`, with `curriculum_nexus_path` at :57 (read).

**Open.** That socket is served by the transient `curriculum-nexus-040`,
while flow.nix:96 `Requires = [ "curriculum-nexus.service" ]` names the
declared Curriculum on `/run/user/1001/curriculum/curriculum.sock`. This is
procedure Q2.

## 4. State directory

**Where it lands.**
- `modules/home/profiles/min/flow.nix:40` `stateDirectory` default changes
  from `"flow-03521"` to the new directory. The name is the hand's choice; the
  procedure calls it `NEWSTATE`.
- It is used at flow.nix:90 (`flowOpensItsStore`) and :108 (ExecStart).
- `packages/flow-deployment/default.nix:5` has the default argument and :78
  has `store=`.
- `checks/flow-service-path/default.nix:17,42,99-101,109,125,156-164` name
  `flow-03521` and are updated with it.

The file name stays `flow.sema` as on main (flow.nix:90,108; default.nix:78).

**Ruling.** "The new state directory [is] the 0.40.7 shape" (ruling (d)). The
new store is seeded by the replay before the unit starts. That is procedure
step C3, not a Home change.

## 5. Declaration-reset removal

**Where it lands.** `packages/flow-deployment/default.nix:79-80`
(`initialize_metaflows` set when the store is empty) and :128-131 (the
`metaflows.clj` `Configure.Metaflows` from `primary/config/main-flow`).

**State on main.** It already applies only to an empty store (read). A store
seeded by the replay is non-empty, so it is skipped.

**Removing it.** Removing it entirely makes the replay the only seeding path.
A fresh store with no replay then starts with no metaflows (inferred).
Removal also drops the `${./metaflows.clj}` use, whose file stays or goes
with it.

## 6. Drop-in

**Where it lands.** Nowhere in Home, as things stand: the drop-in
`~/.config/systemd/user/flow-nexus.service.d/no-presentation-role.conf` is not
Home's. It sets
`FLOW_CORE_PRESENTATION_PROMPT=/home/li/primary/flows/e3c8c1/presentation-role.md`.

**On main.** `modules/home/profiles/min/flow.nix:104-106` declares only
`PATH` in `Environment`; `c1a0b09` removed the prompt (read). The drop-in
would still apply the e3c8c1 value to the 0.40.7 unit (inferred: systemd
drop-in precedence).

**Choice, unruled.**
- Declare the wanted value at flow.nix:104-106 and remove the drop-in by hand
  before procedure step C5.
- Or remove the drop-in and run with no prompt variable.

## 7. Kept previous generation

**Where it lands.** No CriomOS-home line governs Home generation expiry or GC.
A grep of `modules/` and `lib/` at `origin/main` finds no `autoExpire`,
`nix.gc` or `expire-generations` (read).

**How it is kept.** By the procedure: step A1 records the generation current
just before the 0.40.7 activation and roots it with `nix-store --add-root
…/flow-040/previous-home.gcroot`. Rollback runs its `activate`. (ruling (b))

**If a declared keep is wanted**, it is a new option. It is not proposed here.

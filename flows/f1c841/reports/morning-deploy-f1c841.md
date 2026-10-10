# Morning deploy f1c841: four deployments held for the living's ruling

Nothing was built, switched, restarted or deployed for this report. The only commands run were reads: git and jj on the repositories, `systemctl --user show/cat`, `readlink /proc/<pid>/exe`, `ss -xlp`, `ls`, `cmp`, `nix profile list`. One side effect: `nix-store -q --roots` removed three stale temporary-roots files left by dead processes under `/nix/var/nix/temproots/`. Nix did that by itself, and it affects nothing live.

The four deployments:

- **(a)** orchestrate 0.36.1 Home switch. Copied from `flows/3ec648/reports/morning-deploy.md` as it stands.
- **(b)** Flow: 0.12.2 → 0.19.0, and retiring one of the two running flow-nexus.
- **(c)** message-daemon 0.14.0 → message-nexus 0.17.1 in the stable slot.
- **(d)** The installed `claude` wrapper, which forces `--dangerously-skip-permissions`.

Every step marked **unverified** was derived from source or UPGRADES and was not run.

## The live state, witnessed 2026-10-03 (read-only)

| Unit | Running executable (`/proc/<pid>/exe`) | Sockets | Store |
|---|---|---|---|
| `orchestrate-nexus` | `0grjjmjc…-orchestrate-nexus-0.35.0` | `%t/orchestrate-nexus/` | unchanged |
| `flow-nexus` (pid 1965136) | `c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2` | `/run/user/1001/flow/flow.sock`, `flow-meta.sock` | `~/.local/state/flow/flow.sema` |
| `flow-nexus-next` (pid 1965133) | `7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4` | `/run/user/1001/flow-next/flow/…` | `~/.local/state/flow-next/.local/state/flow/flow.sema` |
| `flow-configuration-next` | oneshot, `active (exited)` | — | — |
| `message-daemon` (pid 13885) | `i66j8l0vk6i3bhd0r968dbm7ckllnryf-message-0.14.0/bin/message-daemon` | `/run/user/1001/message/message.sock` (0660), `message-owner.sock` | `~/.local/state/message/messenger.sema` |
| `message-nexus-next` (pid 90762) | `3v8qs8h4ydmcrjjw29arzb0qk9qxqicq-message-0.17.0` | `/run/user/1001/message-next/message/…`; `message-next/flow` → `/run/user/1001/flow-next/flow` | `~/.local/state/message-next/.local/state/message/message.sema` |

- The Home generation is `home-manager-1039-link` → `xp12f872…`, unchanged since 3ec648. CriomOS-home `main` is still `0025894f`. Its flake pins:
  - `flow` `9fcd625a` (0.14.0)
  - `flow-next` `bc464e5e` (0.17.4)
  - `message` `930c5169` (0.14.0)
  - `message-next` `481b579f` (0.17.0)
- The stable `flow-nexus` does not run what Home declares. Its fragment's ExecStart is `j689l77b…-flow-0.14.0`. The hand-written drop-in `~/.config/systemd/user/flow-nexus.service.d/override.conf` (regular file, mtime 2026-09-25 20:52, not a store link) resets it to `c044v5pa…-flow-0.12.2`. The user `nix profile` holds an element `flow` → the same 0.12.2. The `flow` and `flow-meta` on PATH resolve there.
- `message-next` and `message-next-meta` in `~/.local/bin` are hand-written shell wrappers, not Nix. They point at `nwrvnmk7…-message-0.17.0`, a different store path from the running `3v8qs8h4…`. `flow-next` and `flow-next-meta` come from Home (`v7ay3kxp…-flow-next-clients`).
- `ss -xp` showed no connected peer on `/run/user/1001/flow/` or `/run/user/1001/message/` at the moment of reading. Only the LISTEN rows were present.
- Live problem found: `cmp ~/.local/state/message/messenger.sema messenger.sema.message-0.14.0.preopen` reports that the two **differ**. message.nix's `ExecStartPre` preservation script exits 1 in that case ("existing snapshot differs from live store"). **Any restart of the 0.14.0 `message-daemon` would therefore fail before it starts.** That includes a rollback to it. This was derived from the script text and not run.

## (a) orchestrate 0.36.1 Home switch (copied)

The section below is `flows/3ec648/reports/morning-deploy.md` at Primary commit `b362dc00`, copied as it stands. The only change is that its headings are moved down two levels to sit under this one. It was not re-derived.

Its artifact store paths:

| Role | Store path | Status, re-read 2026-10-03 |
|---|---|---|
| Activate | `/nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation` | Present |
| Rollback (live) | `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation` | Present; still `home-manager-1039-link` |
| New Nexus | `/nix/store/b2585m3pkgy8yxsxdpahsazz11rlvnrm-orchestrate-0.36.1` | Present |
| Check | `/nix/store/saghazavysnmbk3qfy4ybfmiq9r69bgm-orchestrate-wrapper-fallback` | Not re-read |

**Added pre-condition (new, from the re-read):** `rn8fzfbw…` has exactly one GC root. It is the out-link `/tmp/claude-1001/-home-li-primary/3ec6480d-…/scratchpad/home-branch`, which lives in 3ec648's scratchpad under `/tmp`. A reboot or a garbage collection before the switch could remove the artifact. Before activating, run `ls -d /nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation`. If it is gone, rebuild with the command in the copied section and compare the hash before activating.

The running orchestrate-nexus is still 0.35.0 (`0grjjmjc…`).

### Morning deploy: orchestrate 0.36.1 Home switch on ouranos

Nothing was switched or restarted tonight, and the live Nexus was not touched. The CriomOS-home branch `3ec648-orchestrate-0.36` (commit `feebd281a0bdd02fc67ef410677f612ce467990c`, pushed, not merged) does two things. It repins `orchestrate` to `bc5cd36e81df395ed1f84e2e3e98d5a6ee90bf8c` (0.36.1). It also makes the installed `orchestrate` and `orchestrate-meta` wrappers honour a caller-set `ORCHESTRATE_SOCKET` / `ORCHESTRATE_META_SOCKET`, falling back to `XDG_RUNTIME_DIR` otherwise. Its parent is Home `main` `0025894f`, which is the source of the live generation.

#### Built store path

`/nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation`

- It was built on Prometheus (`--max-jobs 0`) in the user unit `3ec648-home-build` (MemoryMax=8G, RuntimeMaxSec=7200). The build used `homeConfigurations.li.activationPackage` with Lojix's ouranos user-environment inputs: `--override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system` and `--override-input horizon path:…/user-environment/horizon`.
- Control: the same command at `main` `0025894f` produced `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation`. That is exactly the live Home generation (`~/.local/state/nix/profiles/home-manager` -> `home-manager-1039-link`). The method therefore reproduces live.
- `nix store diff-closures` from live to the new generation shows only `orchestrate`, `orchestrate-clients` and `orchestrate-nexus` moving from 0.35.0 to 0.36.1. The unit's ExecStart is now `/nix/store/b2585m3pkgy8yxsxdpahsazz11rlvnrm-orchestrate-0.36.1/bin/orchestrate-nexus`, so sd-switch restarts `orchestrate-nexus` during the switch.

#### Pre-switch condition

```sh
orchestrate 'Observe.Locks'
```

Switch only when the answer is `Observed.Locks.[]`. The wire break is total: a 0.35 client cannot talk to a 0.36 Nexus, and the reverse fails too. A flow that holds a Lock across the switch could still release it afterwards, because the store carries it. However, any running script that captured a 0.35 client path would fail. Wait until no Lock is held.

#### Switch command

```sh
/nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation/activate
```

This activates the exact artifact that was built and checked. The Home Manager activation sets the `home-manager` profile to it as generation 1040 and runs sd-switch. Lojix's `Current` for ouranos UserEnvironment is already stale (`y2mh…`, not the live `xp12f872…`), and this switch does not refresh it. To deploy through Lojix instead, CriomOS-home must first merge this branch to `main`, and a CriomOS revision must pin it. The CriomOS `main` `6485b64e` currently pins Home `acf6d376`, which is older than live. Then use `lojix-meta 'Deploy.UserEnvironment.{ goldragon ouranos li … HomeManagerNixProfileV1 ActivateNow RequireImmutable … }'` at that CriomOS revision. That route is not prepared here.

#### Post-switch checks

1. `systemctl --user status orchestrate-nexus` shows it running from `…-orchestrate-0.36.1`.
2. `orchestrate 'Observe.Locks'` answers `Observed.Locks.[]` (exit 0) from the 0.36.1 Nexus over the new wire.
3. The meta socket. The live store predates 0.34.0 and binds the legacy `meta-orchestrate.sock`, and the store persists that path across the restart. A plain `orchestrate-meta` call would therefore answer `Unreachable.{ …/orchestrate-meta.sock … }`. The procedure is in `flows/3ec648/witnesses/orchestrate-meta-socket.md`. The new wrapper honours the caller's value, so the installed client reaches the legacy name:

   ```sh
   ORCHESTRATE_META_SOCKET=/run/user/1001/orchestrate-nexus/meta-orchestrate.sock \
     orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
   orchestrate 'Observe.Locks'   # still Observed.Locks.[] before the restart
   systemctl --user restart orchestrate-nexus
   orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
   ```

   The first call answers `Configured`, and the running Nexus keeps serving the old path until the restart. The last call, made after the restart through the plain wrapper, must answer `Configured.{ { …/orchestrate.sock …/orchestrate-meta.sock } True }` (exit 0). That proves the designed meta socket is bound. Finish with `orchestrate 'Observe.Locks'` once more.

The meta sequence was witnessed against 0.35.0 in the sandbox. Against 0.36.1 it rests on two points: the store format is unchanged (UPGRADES 0.36.1), and the `Configure` form is the same in the 0.36.1 README.

#### Rollback

Go back to the previous generation, the live `xp12f872…` (0.35.0). The 0.36.1 Nexus does not change the store format, so 0.35.0 opens it again:

```sh
/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate
```

(equivalently `home-manager-1039-link/activate`). sd-switch restarts `orchestrate-nexus` back onto 0.35.0. Check it with `orchestrate 'Observe.Locks'`. If the meta Configure was already done, 0.35.0 binds `orchestrate-meta.sock`, which matches its wrapper too.

#### Checks run on the branch

- `checks.x86_64-linux.orchestrate-wrapper-fallback` passed (`/nix/store/saghazavysnmbk3qfy4ybfmiq9r69bgm-orchestrate-wrapper-fallback`). It now covers three cases: a caller-set value wins over `XDG_RUNTIME_DIR`; with no caller value, `XDG_RUNTIME_DIR` decides; with neither, `/run/user/<uid>` is used. The extended check was first run against the unchanged wrapper and failed there. `orchestrate-service-path` also passed.
- The built wrapper itself, with `ORCHESTRATE_SOCKET=/tmp/claude-1001/none/o.sock`, answered `Unreachable.{ /tmp/claude-1001/none/o.sock … }`. It honours the caller's value with the real 0.36.1 client.
- `nix flake check --keep-going` (same overrides, Prometheus) exited 1. Six checks failed, and every one also fails at `main` `0025894f` with the identical derivation:
  - `ai-agent-launch-orchestration`: eval assertion `elem codexCliPackage profile.home.packages`.
  - `codex-remote`: `46jy25yi…-codex-remote-contract.drv`.
  - `codex-remote-control-vm`: socket mode `stat … = 600` assertion.
  - `session-variables`: `m5q07sci…-home-session-variables.drv`.
  - `pkgs-mentci`: `meta-signal-mentci` build script, `q61c1w84…-mentci-0.5.0.drv`.
  - `main-contract-pins`: depends only on that same failing mentci derivation.

  None of them involves orchestrate. Every other check passed.

UPGRADES.md on the branch records the breaking switch.

#### Flow upgrade (not part of this switch)

Relayed from the coordinator and not verified here. Flow 0.18.0 (`main` `ae050272`) no longer reads `FLOW_SOURCE_ROOT` or `FLOW_CODEX_*`. CriomOS-home still exports them, in `modules/home/profiles/min/flow.nix:81-89` (stable) and `modules/home/profiles/min/flow-message-next.nix:114-122,150-` (next slot). A fresh next-slot store seeds `~/.local/state/flow-next/primary` as its source root and needs a meta `Configure` after start. This branch does not change Flow (`flow` stays `9fcd625a` and `flow-next` stays `bc464e5e`). The living rules on that upgrade separately.

#### Sources

- CriomOS-home branch `3ec648-orchestrate-0.36` `feebd281`. Its parent is `main` `0025894f`.
- orchestrate `bc5cd36e81df` UPGRADES.md (0.35.0 to 0.36.0, 0.36.0 to 0.36.1) and README.md.
- `flows/3ec648/witnesses/orchestrate-meta-socket.md`.
- `flows/d5b96b/reports/codex-rotation-complete.md`, which records the live generation `xp12f872` built from Home `0025894f`.
- Lojix `Query.ByNode.{ goldragon ouranos None }` (ordinary socket), for Current `y2mh…`.
- Build logs: user units `3ec648-home-build` and `3ec648-main-control`. The logs are in the session scratchpad.

*(End of the copied section.)*

## (b) Flow: 0.12.2 → 0.19.0, and retiring one flow-nexus

### What flow's UPGRADES state (main `4f3670ef`, workspace version 0.19.0)

- **0.17.0–0.17.4.** Each says "Deploy beside Message 0.17.0, or do not deploy at all". 0.17.0 says: "an older Message cannot decode the new refusals."
- **0.18.0.** No wire or storage change, again "Deploy beside Message 0.17.0, or do not deploy at all". Configuration now reaches the Nexus only over its meta socket:
  - `FLOW_SOURCE_ROOT` and `FLOW_CODEX_{STABLE,NEXT}_{CLIENT,SOCKET,HOME,MODELS}` are no longer read.
  - "A store that adopted them earlier keeps the adopted values; a new store seeds its defaults from `HOME` and must be sent `Configure` for anything else."
  - "A next-slot Nexus started under `HOME=~/.local/state/flow-next` from a fresh store therefore needs a `Configure` carrying the real source root and Codex endpoints."
  - Claude readiness is read under `CLAUDE_CONFIG_DIR`, else `$HOME/.claude`.
- **0.19.0.** "Wire change, no storage change. Rebuild and restart the Nexus, `flow` and `flow-meta` together; an older client and a 0.19.0 Nexus do not read each other's frames."
  - Contracts move to signal-flow 8.0.0 (`c297d987`) and meta-signal-flow 12.0.0 (`69f9c146`), on signal 7.0.0, from signal-flow 7.0.0 (`1c9e4b30`) and meta-signal-flow 11.0.0 (`2ac045c2`).
  - `QueueTurnEnd` is answered `TurnEndRejected.QueueRefused`.
  - The 0.19.0 section names no Message version.
- **The README at 0.19.0** says the binary starts with no arguments. Its defaults are:
  - store `$HOME/.local/state/flow/flow.sema`
  - sockets `$XDG_RUNTIME_DIR/flow/flow.sock` and `flow-meta.sock`
  - source root `$HOME/primary`
  - Codex socket `$HOME/.codex/app-server-control/app-server-control.sock`

  "A new store persists these; a populated store resumes what it holds; meta `Configure` is the only way to change them."

### The Message coupling

Message is a client of Flow on both of Flow's sockets: Vet, Deliver and ResolvePeer on the meta socket, and `Observe.Agent` on the ordinary one.

- message `7ffd4a2` (0.17.1) pins `signal-flow` `1c9e4b30` and `meta-signal-flow` `2ac045c2`. Those are the 0.17/0.18 contracts, on signal 5.0.0. Its UPGRADES (0.16.0→0.17.0) say "Deploy with Flow 0.17.0".
- **No Message on main is built against Flow 0.19.0's contracts.**
- The contracts' own UPGRADES say the generated Rust and "the rkyv archive of every value" are unchanged. Flow 0.19.0's UPGRADES say the frames of an older client and a 0.19.0 Nexus are not mutually readable, and that signal-flow's `Query`/`Response` archives change.
- Taken at Flow's word, Message 0.17.x cannot talk to Flow 0.19.0. The Nexus that Message reaches must stay on 0.17.x/0.18.0 until Message is repinned onto signal-flow 8.0.0 and meta-signal-flow 12.0.0. That release does not exist. **Unverified:** no Message-to-Flow-0.19 exchange was run.
- A deployable intermediate with no coupling break is flow 0.18.0 (`ae050272`). It is the same wire as 0.17.4 and drops the variables.

### Which flow-nexus the modules make natural to retire

**Retire the stable 0.12.2 under `$XDG_RUNTIME_DIR/flow/`.** Keep the next slot (`$XDG_RUNTIME_DIR/flow-next/flow/`) as the one that is upgraded.

1. The 0.12.2 is not what any module declares. `modules/home/profiles/min/flow.nix` declares 0.14.0 (`ExecStart = "${cfg.package}/bin/flow-nexus"`, input `flow` `9fcd625a`). A hand drop-in plus a `nix profile` element override it. Any Home change that touches the unit, or the removal of the drop-in, already changes what runs.
2. Only the next slot is paired with a Message.
   - `flow-message-next.nix` gives `message-nexus-next` its Flow as `nextPeers.flow = flow.next` (the live link `message-next/flow → flow-next/flow`).
   - It configures next Flow with the next Message's executable as `MessageNexusPath` (`flowConfigurationUnit flow.next message.next`).
   - The stable Message (message-daemon 0.14.0) cannot reach a Flow older than 0.14.0: "A `message` on this pin cannot talk to a Flow Nexus older than 0.14.0" (message UPGRADES 0.13.0→0.14.0).
3. Only the next slot has the meta `Configure` the 0.18+ Flow needs, in the oneshot `flow-configuration-next`.
4. The next slot's store already holds a configuration adopted under 0.16–0.17. It "opens unchanged" through 0.18.0 and 0.19.0 ("no storage change").
5. The rolling the lib describes (`lib/stable-next-service.nix:13-15`: "point stable's package at next's once next is trusted, move the callers to the stable socket, and the next slot is free") is the later step. It comes after the new version has proved itself in the next slot. It is not a reason to put 0.19.0 into the 0.12.2's slot and onto the 0.12.2 store. Whether 0.19.0 opens a 0.12.2-written store is **unverified**. 0.15.0 states only "a 0.14 store opens unchanged."

"Flow in the profile 0.12.2 → 0.19.0" is better done as removal than as an upgrade. The `nix profile` element `flow` is outside the declarative source (nix-workflow: what Home owns is changed through Home). A 0.19.0 `flow` on PATH can talk to no running Nexus until one at `$XDG_RUNTIME_DIR/flow/` runs 0.19.0. Callers who need a CLI use `flow-next` and `flow-next-meta` from Home.

### What the modules must change

In `modules/home/profiles/min/flow-message-next.nix` (next slot):

- `flowNexusUnit`, `Environment`, lines 114-122: delete `FLOW_SOURCE_ROOT` and the eight `FLOW_CODEX_*` entries. They are not read from 0.18.0 on.
  - Keep `instance.anchorEnvironment` (`HOME=~/.local/state/flow-next`, `XDG_RUNTIME_DIR=%t/flow-next`, and the real XDG homes).
  - Keep `CLAUDE_CONFIG_DIR=${homeDirectory}/.claude`, which 0.18.0 reads for readiness, and `CODEX_HOME` and `PATH`.
- `ExecStart = "${instance.package}/bin/flow-nexus"` (line 125) stays as it is: no arguments.
- Store seed: none to add while the existing store is kept. A *fresh* next store would seed the source root `~/.local/state/flow-next/primary` and the Codex socket `~/.local/state/flow-next/.codex/app-server-control/app-server-control.sock`. Both are wrong.
- `flow-configuration-next` (lines 191-241) corrects that on every start. It is `PartOf` the Nexus, so it re-runs when the Nexus restarts. Its datom states `/home/li/primary` and both Codex endpoints whole. meta-signal-flow 12.0.0 keeps the vocabulary unchanged, so the same `Configure` datom stays valid. **Unverified against 0.19.0.**
- Dead bindings: `occupiedNextFlowUnit` and `occupiedNextFlowConfigurationUnit` (lines 131-183) are defined and never referenced. They can go.
- The comment at lines 18-21 ("next is Flow 0.17.0 and Message 0.17.0") should be updated.

In `flake.nix`/`flake.lock`:

- `flow-next` `bc464e5e` → `ae050272` (0.18.0, beside Message 0.17), or → `4f3670ef` (0.19.0, only with a repinned Message).
- `message-next` `481b579f` → `7ffd4a2` (0.17.1: "No wire, store or command-line change").

In `modules/home/profiles/min/flow.nix` (retiring the stable 0.12.2):

- Set `criomosHome.flow.enable` to `false` for li, or drop the module's import. This removes the `flow-nexus` unit and the `flow` 0.14.0 package from Home.
- If instead the stable unit is kept for a later roll, its `Environment` lines 81-89 must also lose `FLOW_SOURCE_ROOT`/`FLOW_CODEX_*`, and it needs a `Configure` of its own.
- Dead bindings `occupied`, `occupiedFlow`, `occupiedStableClient`, `occupiedNextClient` and `occupiedPath` (lines 21-30) are unused.
- The unmerged branch `flow-stable-0122-declarative-56ae53` (`4d88df78`, 2026-09-26) declared the override instead. It is superseded by retirement.

### The restart-together requirement of 0.19.0

The Nexus, `flow` and `flow-meta` of the same build must start together. In the next slot this happens in one Home activation:

- The new `ExecStart` store path makes sd-switch restart `flow-nexus-next`.
- `flow-next-clients` (`flow.next.clients`, built from the same `instance.package`) swaps in with the generation.
- `flow-configuration-next`'s script calls `${flowInstance.package}/bin/flow-meta`, the same build, and re-runs through `PartOf`.
- **What is not in step:** `message-nexus-next`, the third client of that Nexus, built against 0.17's contracts. Any process or script holding an old `flow-next` store path also fails.

**Unverified:** that sd-switch restarts `flow-configuration-next` after the Nexus within the same activation.

### B1. Retire the stable 0.12.2

**Pre-conditions**

```sh
readlink /proc/$(systemctl --user show flow-nexus -p MainPID --value)/exe
#   /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus
ss -xp | grep '/run/user/1001/flow/flow'          # no output: no connected peer
cat ~/.config/systemd/user/flow-nexus.service.d/override.conf
#   ExecStart=  /  ExecStart=/nix/store/c044v5pa…-flow-0.12.2/bin/flow-nexus
nix profile list | grep -A1 '^Name: *flow$'       # Store paths: …c044v5pa…-flow-0.12.2
```

Also confirm that no seat the living cares about is held only by the 0.12.2 store. `flow 'List.{}'` on the 0.12.2 CLI lists them. **Unverified:** that 0.12.2's `List` writes nothing. That guarantee is stated from 0.14.0 on.

**Command sequence** (the Home part is unverified; nothing is built)

1. In CriomOS-home, on a branch whose parent is the generation that is live at the time (main `0025894f`, or `feebd281` if (a) went first): disable `criomosHome.flow` for li. Build `homeConfigurations.li.activationPackage` on Prometheus with the Lojix overrides (the method in (a)). Read `nix store diff-closures` from live; it must show only `flow` 0.14.0 leaving.
2. `<new-generation>/activate`. sd-switch stops and removes `flow-nexus.service`. This step is **unverified**: the orphan drop-in directory remains.
3. Remove the hand state, in this order:
   ```sh
   systemctl --user stop flow-nexus 2>/dev/null || true
   cp --reflink=auto ~/.local/state/flow/flow.sema ~/.local/state/flow/flow.sema.flow-0.12.2.retired
   mv ~/.config/systemd/user/flow-nexus.service.d/override.conf ~/.local/state/flow/override.conf.retired
   rmdir ~/.config/systemd/user/flow-nexus.service.d
   systemctl --user daemon-reload
   nix profile remove flow
   ```
   Order matters, as recorded in `flows/da88cf/reports/prometheus-return.md`. Removing the drop-in while the Home unit still exists would drop the service back to its 0.14.0 base unit and restart it.

**Post-checks**

```sh
systemctl --user status flow-nexus               # Unit flow-nexus.service could not be found.
ls /run/user/1001/flow                           # No such file or directory
command -v flow flow-meta                        # nothing (or Home's, if kept)
flow-next 'List.{}'                              # Listed.[ … ]   exit 0 — next slot untouched
systemctl --user is-active flow-nexus-next message-nexus-next   # active active
```

**Rollback**

1. `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate`, or the generation that was live before step 2.
2. `install -m 600 ~/.local/state/flow/override.conf.retired ~/.config/systemd/user/flow-nexus.service.d/override.conf` (after `mkdir -p` of the directory).
3. `nix profile install /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`.
4. `systemctl --user daemon-reload && systemctl --user restart flow-nexus`.
5. Check with `readlink /proc/$(systemctl --user show flow-nexus -p MainPID --value)/exe`.

The store was never touched. The path `c044v5pa…` must still exist. It has no GC root once the profile element is removed, so keep it rooted before step 3 with `nix-store --add-root ~/.local/state/flow/flow-0.12.2.root -r /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`.

### B2. Next slot to 0.18.0, or to 0.19.0

**Pre-conditions**

```sh
readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe   # …7z15aqi4…-flow-0.17.4
ls -l ~/.local/state/flow-next/.local/state/flow/flow.sema                        # present: resumed, not seeded
systemctl --user is-active flow-configuration-next                               # active
flow-next 'List.{}'                                                               # Listed.[ … ]
```

- No delivery in flight: no recipient `Parked` or `Submitted` in message-next. A restarted Message "resumes every recipient still `Submitted` or `Parked`", so this is a courtesy, not a requirement.
- For 0.19.0 only: a Message release pinned on signal-flow 8.0.0 and meta-signal-flow 12.0.0 exists, and `message-next` is moved to it in the same generation. **Without it, do not deploy 0.19.0.**
- Copy the store aside: `cp --reflink=auto ~/.local/state/flow-next/.local/state/flow/flow.sema ~/.local/state/flow-next/.local/state/flow/flow.sema.flow-0.17.4.predeploy`.

**Command sequence** (unverified; nothing is built)

1. Make the CriomOS-home change: the environment edits above, plus `flow-next` → `ae050272`, or `4f3670ef` together with the repinned Message.
2. Build on Prometheus as in (a), then read `nix store diff-closures`.
3. `<new-generation>/activate`. sd-switch restarts `flow-nexus-next`, then `flow-configuration-next` (`PartOf`), and `message-nexus-next` if its package moved.

**Post-checks**

```sh
readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe   # …-flow-0.18.0 or …-flow-0.19.0
systemctl --user show flow-configuration-next -p ActiveState,Result              # active, success
journalctl --user -u flow-configuration-next -n 3                                # Configured.{ … }
flow-next 'List.{}'                                                              # Listed.[ … ] exit 0, same flows as before
flow-next 'QueueTurnEnd.{ s-check t-check None }'                                # 0.19.0 only: TurnEndRejected.QueueRefused
systemctl --user show flow-nexus-next -p Environment | grep -c FLOW_             # 0
```

**Unverified:** the `QueueTurnEnd` datom shape, read from the signal-flow 8.0.0 ethos as `TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }`.

End-to-end Message check, run by the living from a plain terminal outside any flow's pane:

```sh
message-next-meta 'Send.{ [ <a live flow id> ] Soft Text.«deploy check» }'
```

The meta Send is stamped Owner (README). It must answer `Submitted.{ m-… [ { <id> … } ] }`, and the letter must appear in that flow's pane. An answer of `FlowUnreachable` means the coupling broke.

**Rollback**

- Activate the previous generation. sd-switch puts `flow-nexus-next` back on `7z15aqi4…-flow-0.17.4`.
- No storage change in 0.18.0 or 0.19.0 means 0.17.4 opens the store again. Configuration written by a `Configure` under 0.18/0.19 is the same vocabulary.
- If the store fails to open, stop the unit, `cp` the `.flow-0.17.4.predeploy` copy back over `flow.sema`, and start the unit.
- Check with `flow-next 'List.{}'`.

## (c) message-daemon 0.14.0 → message-nexus 0.17.1 (stable slot)

### What message's UPGRADES spell out (main `7ffd4a2`, 0.17.1)

From "What the deployer changes", for "a unit still on the 0.14.0 shape (CriomOS-home `message.nix`, unit `message-daemon`)":

- `ExecStart`: `message-daemon <state>/message-daemon.signal` becomes `message-nexus` with **no argument**. "Given any argument the Nexus exits non-zero before it opens a store or binds a socket."
- `ExecStartPre`: drop `message-write-configuration`. The executable persists its defaults in `~/.local/state/message/message.sema` on first start. `message-daemon.signal` and `messenger.sema` are never read.
- Environment: `HOME` and `XDG_RUNTIME_DIR` only. `MESSAGE_SOCKET`, `MESSAGE_META_SOCKET`, `FLOW_SOCKET` and `FLOW_META_SOCKET` are ignored by the Nexus.
  - Its own sockets are `$XDG_RUNTIME_DIR/message/message.sock` and `message-owner.sock` (both 0600, per the README).
  - It expects Flow at `$XDG_RUNTIME_DIR/flow/flow.sock` and `flow-meta.sock`.
- Other paths are set with `message-meta 'Configure.{ <ordinary> <meta> <flow> <flow-meta> [ Psyche ] }'`, "from outside any flow's pane". Moving Message's own sockets answers `NexusRestartRequired`.
- Client wrappers: `meta-message` is now `message-meta`.

0.14.0→0.15.0 adds two points:

- Store: "The old `messenger.sema` is never opened; move it aside, nothing is migrated." Inbox, threads, the agent registry, the cluster relay and the flow-delivery park are retired.
- "Flow must admit Message on its meta socket: run Message outside any flow's pane (it then resolves as the owner), and configure Flow's `MessageNexusPath` to the `message-nexus` executable."

### What `modules/home/profiles/min/message.nix` does today (CriomOS-home `0025894f`)

- Unit `message-daemon`, `RuntimeDirectory = "message"`. `ExecStartPre`:
  - first `message-preserve-live-store` (lines 65-110)
  - then `message-write-configuration-request %t/message/message.sock %t/message/message-owner.sock %t/router/router.sock` (lines 56-64, 142-145)
- `ExecStart = "${messagePackage}/bin/${daemonBinary} ${signalPath}"` (line 146). The `daemonBinary` option (lines 119-126) admits `"message-nexus"`, but the unit would still pass the `.signal` argument, and 0.17.1 refuses any argument. **Flipping the option alone does not deploy 0.17.1.**
- `messageProfilePackage` (lines 18-30):
  - runs `rm $out/bin/message $out/bin/meta-message`
  - wraps `${messagePackage}/bin/meta-message`
  - `writeConfigurationScript` execs `${messagePackage}/bin/message-write-configuration`

  0.17.1's workspace has the binaries `message`, `message-meta` and `message-nexus` only, so the profile package and the script **would fail to build** against the 0.17.1 package. This was derived from `crates/*/Cargo.toml` and not built.
- Input `message` is `930c5169` (0.14.0).

### What the module must change

The smallest change that follows the UPGRADES and the existing next-slot shape is to make the stable Message the stable instance of the pair `flow-message-next.nix` already computes. `message.stable` has `serviceUnit = "message-nexus"`, `runtimeDirectory = "message"`, an empty `anchorEnvironment`, and no peers. In message.nix, or by moving the unit into flow-message-next.nix:

- `systemd.user.services.message-nexus = messageNexusUnit message.stable flow.stable;` gives:
  - `ExecStart = …/bin/message-nexus`
  - `RuntimeDirectory = message`
  - no `ExecStartPre` beyond the peer-links script, which is empty with no peers
- Remove the `message-daemon` unit, `writeConfigurationScript`, `preserveLiveStoreScript`, the `daemonBinary` option and `messageProfilePackage`.
- Install `message.stable.clients`: `message` and `message-meta` with the socket variables preset to `${XDG_RUNTIME_DIR}/message/…`.
- `message` input `930c5169` → `7ffd4a2`.
- If (b) retires the stable Flow, `flow.stable` names a Flow that no longer runs. The stable Message's `After`/`Wants` should then name `flow-nexus-next`, and its Flow paths are set by meta `Configure` (below). **Unverified:** whether a module design that points a stable Message at the next Flow is wanted, rather than retiring message-daemon outright and keeping message-next as the only Message.

The renamed unit is a deliberate break: sd-switch stops `message-daemon` and starts `message-nexus`.

### Pre-conditions

```sh
readlink /proc/$(systemctl --user show message-daemon -p MainPID --value)/exe
#   /nix/store/i66j8l0vk6i3bhd0r968dbm7ckllnryf-message-0.14.0/bin/message-daemon
ss -xp | grep '/run/user/1001/message/'           # no output: no connected peer (witnessed 2026-10-03)
ls ~/.local/state/message/message.sema            # absent: 0.17.1 will seed a fresh store
```

- A Flow at `/run/user/1001/flow/` that speaks signal-flow 7.0.0 and meta-signal-flow 11.0.0 (0.17.x/0.18.0), **or** a plan to `Configure` the Flow paths to `/run/user/1001/flow-next/flow/…` right after start. The 0.12.2 at `/run/user/1001/flow/` speaks signal-flow 5.1.0, which 0.17.1 cannot use. A Flow 0.19.0 cannot be used either (see (b)).
- The living accepts that the 0.14.0 ledger (inbox, threads, registry) is not carried forward. Copy it aside:
  ```sh
  cp --reflink=auto ~/.local/state/message/messenger.sema ~/.local/state/message/messenger.sema.message-0.14.0.retired
  ```
- There is no 0.14.0 CLI datom pre-check here. The 0.14.0 README's only example is `message 'QueryDeliveryReceipts.{ event-42 [ target-a target-b ] }'`, and its answer for unknown ids is **unverified**.

### Command sequence (unverified; nothing is built)

1. Make the CriomOS-home change above on a branch from the live generation's source. Build on Prometheus as in (a), then read `nix store diff-closures`: `message` 0.14.0 leaves and `message` 0.17.1 arrives.
2. `<new-generation>/activate`. sd-switch stops `message-daemon` and starts `message-nexus`.
3. Only if the Flow paths must point at the next slot, run this from a plain terminal outside any flow's pane:
   ```sh
   message-meta 'Configure.{ /run/user/1001/message/message.sock /run/user/1001/message/message-owner.sock /run/user/1001/flow-next/flow/flow.sock /run/user/1001/flow-next/flow/flow-meta.sock [ Psyche ] }'
   #   Configured.{ { /run/user/1001/message/message.sock /run/user/1001/message/message-owner.sock /run/user/1001/flow-next/flow/flow.sock /run/user/1001/flow-next/flow/flow-meta.sock [ Psyche ] } Applied }
   ```
   The answer form is from meta-signal-message `14f57596` `tests/contract.rs`. Flow paths take effect on the next call (`Applied`).

**Unverified:** that next Flow admits a second Message. Its `MessageNexusPath` names the next Message's executable only. A unit outside any pane resolves as the owner per the 0.15.0 notes, and that was not run with two Messages.

### Post-checks

```sh
systemctl --user is-active message-nexus message-daemon            # active / inactive (or unknown unit)
readlink /proc/$(systemctl --user show message-nexus -p MainPID --value)/exe   # …-message-0.17.1/bin/message-nexus
ls -l /run/user/1001/message/                                      # message.sock, message-owner.sock, both srw-------
ls -l ~/.local/state/message/message.sema                          # created
message 'QueryReceipts.m-000000'                                   # MessageRejected.UnknownMessage
message-next 'QueryReceipts.m-000000'                              # MessageRejected.UnknownMessage — next pair untouched
```

`QueryReceipts.MessageId` and `MessageRejected.MessageRejection` with `UnknownMessage` come from signal-message `d5742005` `ethos/signal.ethos:31-39`. **Unverified:** the bare `m-000000` token shape and the exit code.

End-to-end check, which delivers a real letter, so it is the living's call. From a plain terminal:

```sh
message-meta 'Send.{ [ <a live flow id> ] Soft Text.«deploy check» }'
#   Submitted.{ m-… [ { <id> … } ] }
```

The letter must appear in that pane. An answer of `FlowUnreachable` means the Flow paths or the admission are wrong.

### Rollback

1. Activate the previous generation. sd-switch stops `message-nexus` and starts `message-daemon` 0.14.0.
2. **That start fails** today. Its `ExecStartPre` preservation script finds `messenger.sema.message-0.14.0.preopen` differing from `messenger.sema` (cmp witnessed 2026-10-03) and exits 1. Before activating the rollback, move the stale snapshot aside, as the 56ae53 recovery did on 2026-09-26:
   ```sh
   mv ~/.local/state/message/messenger.sema.message-0.14.0.preopen \
      ~/.local/state/message/messenger.sema.message-0.14.0.preopen.$(date +%Y%m%dT%H%M%S%z).$(sha256sum ~/.local/state/message/messenger.sema.message-0.14.0.preopen | cut -c1-16)
   ```
3. Check with `systemctl --user is-active message-daemon` and `ss -xlp | grep /run/user/1001/message/`.
4. The 0.17.1 store `message.sema` stays on disk unread by 0.14.0.

The same snapshot fault applies to **any** activation that restarts `message-daemon` while it is kept, including (a) if its closure touched message, which it does not.

## (d) The installed `claude` wrapper forcing `--dangerously-skip-permissions`

### Where it is defined (CriomOS-home `0025894f`)

- **The flag:**
  - `owned-agents/claude-code/default.nix:51-68`, in `postFixup`, runs `wrapProgram $out/bin/claude --argv0 claude --add-flags "--dangerously-skip-permissions" …`.
  - The live result is `/nix/store/qsq3lh2i05dz77dakipwy9f1fkssq1zw-claude-code-2.1.284/bin/claude`. Its last line is `exec -a "claude" ".../.claude-wrapped" --dangerously-skip-permissions "$@"`.
- **Selected as** `config.criomos.corePackages.claude` (`modules/home/core-packages.nix:16-19`). It is consumed by:
  - `home.packages`, in `modules/home/profiles/min/codex-remote-control.nix:46-47`
  - claude-desktop, at lines 37-39 of the same file
  - the PATH of both Flow Nexus units (`flow.nix:35-40`, `flow-message-next.nix:68-73`)
  - the `core-checkup` unit's PATH (`field-monitoring.nix:32,206`)
  - `direct-claude` (`modules/home/profiles/min/default.nix:307-317`). It execs the wrapped `claude` with `--dangerously-skip-permissions` again, so the flag appears twice.
- **Two more layers set bypass independently of the flag:**
  - `codex-remote-control.nix:51-56`: a Home activation (`hexis` `mkManagedConfig`) writes `permissions.defaultMode = "bypassPermissions"` into `~/.claude/settings.json` with mode `always`, rewriting it on every activation. Live `jq .permissions.defaultMode ~/.claude/settings.json` reads `"bypassPermissions"`.
  - Flow itself launches every Claude seat with `--settings '{"permissions":{"defaultMode":"bypassPermissions"}}'` (flow `4f3670ef` `crates/flow-nexus/src/herdr/launch.rs:129-136`; UPGRADES 0.10.7).
- Today a caller can get a requested mode only by calling the unwrapped `.claude-wrapped` directly. The 3ec648 semi-sandbox does that: `flows/3ec648/witnesses/semi-sandbox-capsule.sh:12,77`, with `--permission-mode default`.

### What a change does to every seat and sandbox flow

- **Any edit to the wrapper changes the `claude-code` store path.** That changes the `PATH=` in `flow-nexus` and `flow-nexus-next`, so **sd-switch restarts both Flow Nexuses** in that activation. It also changes `core-checkup` and claude-desktop.
- Running seats keep the `claude` process they were started with. Only new launches see the change.
- Seats launched by Flow keep bypass through Flow's `--settings`, whatever the wrapper does.
- Hand-launched `claude` keeps bypass through `settings.json` unless the managed default is also changed.
- **Unverified:** the precedence of a caller's `--permission-mode` over the `settings.json` `defaultMode`, and over `--dangerously-skip-permissions` when both are given. It was not run here.

### The choices, by number

1. **Keep.** No change, no restart. Every seat and sandbox flow stays in bypass. A sandbox that needs a mode keeps calling `.claude-wrapped` by store path, as 3ec648's capsule does. That path changes with every claude-code bump.
2. **Honour a requested mode.** Delete `--add-flags "--dangerously-skip-permissions"` at `owned-agents/claude-code/default.nix:54`.
   - The default stays bypass through `settings.json` and Flow's `--settings`, so no seat changes behaviour.
   - A caller that passes `--permission-mode default|acceptEdits|plan` to the installed `claude` gets it (precedence **unverified**).
   - `direct-claude` keeps its own explicit flag.
   - Cost: one activation that restarts both Flow Nexuses. Schedule it with (b) so the Nexuses restart once.
3. **Default to another mode.** Choice 2, plus three more changes:
   - set `codex-remote-control.nix:54` to the chosen mode (`default` or `acceptEdits`)
   - a Flow release that drops or makes configurable the `bypassPermissions` `--settings` in `launch.rs:136`
   - a decision on `direct-claude`

   **Consequence (unverified, inferred):** unattended seats would stop at permission prompts. Flow's receipt and brief continuation type into a composer that may then hold a permission dialog. Primary's `CLAUDE.md` "bypass-mode preference for Bash" also assumes bypass. This is the only choice that changes how every seat behaves.

### Pre-conditions, sequence, post-checks and rollback (choice 2)

**Pre-conditions**

```sh
tail -1 "$(readlink -f "$(command -v claude)")"     # … .claude-wrapped"  --dangerously-skip-permissions "$@"
jq -r .permissions.defaultMode ~/.claude/settings.json   # bypassPermissions
```

No Flow `Start` should be in flight, because the activation restarts the Flow Nexuses. Check that no seat is being launched at the time.

**Command sequence** (unverified): edit line 54, build on Prometheus as in (a), then `<new-generation>/activate`.

**Post-checks**

```sh
tail -1 "$(readlink -f "$(command -v claude)")"     # no --dangerously-skip-permissions
jq -r .permissions.defaultMode ~/.claude/settings.json   # still bypassPermissions
systemctl --user is-active flow-nexus-next flow-configuration-next message-nexus-next   # active ×3
```

Behaviour check, unverified: in a throwaway directory run

```sh
claude -p --permission-mode default 'create the file x.txt containing y'
```

It must report a permission denial and leave no `x.txt`. The same call without `--permission-mode` creates it.

**Rollback:** activate the previous generation. The wrapper path returns and the Flow Nexuses restart again.

## Order, if more than one is ruled

Each later Home generation must be built from a branch whose parent is the source of the generation then live. Otherwise one activation silently undoes another, and each rollback target must be named anew.

The coupled order:

1. **(a)** orchestrate is independent of Flow and Message.
2. **B1** retires the 0.12.2.
3. **(d)**, if choice 2, folded into the same generation as B2 so the Flow Nexuses restart once.
4. **B2 to 0.18.0** together with `message-next` → 0.17.1.
5. **(c)** comes last and only if a stable Message is still wanted beside message-next.

**Flow 0.19.0 waits for a Message repinned on signal-flow 8.0.0 and meta-signal-flow 12.0.0.** No such Message exists on message main `7ffd4a2`.

## Sources

- CriomOS-home `/git/github.com/LiGoldragon/CriomOS-home`, `origin/main` `0025894f6238d1b71f0afacee5f3502c2b55caa1`:
  - `modules/home/profiles/min/flow.nix`, `flow-message-next.nix`, `message.nix`, `codex-remote-control.nix`, `default.nix`, `field-monitoring.nix`
  - `modules/home/core-packages.nix`, `lib/stable-next-service.nix`, `owned-agents/claude-code/default.nix`, `flake.lock`
- CriomOS-home branches: `3ec648-orchestrate-0.36` `feebd281`, and `flow-stable-0122-declarative-56ae53` `4d88df78` (unmerged).
- flow `4f3670ef75fef61e503d8e95f40f71da6b2fff5f`: `UPGRADES.md` (0.10.7–0.19.0), `README.md`, `crates/flow-nexus/src/herdr/launch.rs`. Version lines of `9fcd625a` (0.14.0), `bc464e5e` (0.17.4) and `ae050272` (0.18.0).
- message `7ffd4a27406441dbaa2bd2accf8991c4ee22749f`: `UPGRADES.md` (0.11.1–0.17.1), `README.md`, `Cargo.toml` (pins), `crates/*/Cargo.toml` (binaries). `930c5169` `README.md` (0.14.0).
- signal-flow `c297d987` `UPGRADES.md` and `ethos/signal.ethos`. meta-signal-flow `69f9c146` `UPGRADES.md`. signal `main` `UPGRADES.md` (7.0.0).
- signal-message `d5742005` `README.md` and `ethos/signal.ethos`. meta-signal-message `14f57596` `README.md`, `ethos/signal.ethos` and `tests/contract.rs`.
- Live host, read-only, 2026-10-03:
  - `systemctl --user show/cat` for `flow-nexus`, `flow-nexus-next`, `flow-configuration-next`, `message-daemon`, `message-nexus-next`
  - `/proc/<pid>/exe`, `ss -xlp`, `ss -xp`
  - `ls` of the runtime and state directories
  - `cmp` and `sha256sum` of `~/.local/state/message/messenger.sema*`
  - `nix profile list`, `command -v` of the clients
  - `~/.claude/settings.json` `.permissions`
  - `nix-store -q --roots` of `rn8fzfbw…` and `b2585m3p…`
- Primary:
  - `flows/3ec648/reports/morning-deploy.md` at `b362dc00`, copied into (a)
  - `flows/3ec648/witnesses/semi-sandbox-capsule.sh`
  - `flows/da88cf/reports/prometheus-return.md` and `inventory-system.md`, for the override and profile history
  - `flows/1bc255/reports/manual-state-audit-2026-09-30.md`
- Skills loaded: subflow, flow-evidence, knowledge-nexus, knowledge-flow, nix-workflow, compensation-primary-commit.

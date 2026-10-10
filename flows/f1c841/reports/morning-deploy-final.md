# Morning deploy f1c841, final: four deployments held for the living's ruling

This report replaces `reports/morning-deploy-f1c841.md` where they differ. It
keeps that report's form: for each deployment, pre-conditions, command sequence,
post-checks and rollback.

Nothing was built, switched, activated, restarted or deployed to write it. The
only things run were reads: git on the repositories, plus `systemctl --user
show/is-active`, `readlink /proc/<pid>/exe`, `ls`, `cmp`, `ss -xp` and `nix
profile list` on the host. Every step marked **unverified** comes from source
or UPGRADES and was not run.

**No Home generation has been built for Flow 0.22.0 or Message 0.19.0.** The
only built Home candidates are the two orchestrate ones in (a).
"What building one would take" is in (b).

The four deployments:

- **(a)** orchestrate: two candidates, 0.36.1 (`rn8fzfbw…`, 3ec648's) or 0.37.0 (`qda5pkid…`, f1c841's). Switch to one, not both in turn.
- **(b)** Flow: retire the stable 0.12.2, and move the next slot 0.17.4 → **0.22.0**.
- **(c)** Message: next slot 0.17.0 → **0.19.0** in the same generation as (b). Optionally, the stable `message-daemon` 0.14.0 → 0.19.0.
- **(d)** The installed `claude` wrapper. The three choices are unchanged.

## The live state, re-read 2026-10-03 (read-only)

| Unit | Running executable (`/proc/<pid>/exe`) | Sockets |
|---|---|---|
| `orchestrate-nexus` (pid 1944) | `0grjjmjc…-orchestrate-nexus-0.35.0`. ExecStart `6ynfv0hy…-orchestrate-0.35.0/bin/orchestrate-nexus` resolves there | `orchestrate.sock`, legacy `meta-orchestrate.sock` |
| `flow-nexus` (pid 1965136) | `c044v5pa…-flow-0.12.2`, through the hand drop-in `~/.config/systemd/user/flow-nexus.service.d/override.conf` | `/run/user/1001/flow/` |
| `flow-nexus-next` (pid 1965133) | `7z15aqi4…-flow-0.17.4` | `/run/user/1001/flow-next/flow/` |
| `flow-configuration-next` | oneshot, `active` | — |
| `message-daemon` (pid 13885) | `i66j8l0v…-message-0.14.0/bin/message-daemon` | `/run/user/1001/message/` |
| `message-nexus-next` (pid 90762) | `3v8qs8h4…-message-0.17.0` | `/run/user/1001/message-next/message/` |

- **Home generation.** `home-manager-1039-link` → `xp12f872…`. CriomOS-home `origin/main` is still `0025894f`.
- **Home flake pins.**
  - `flow` `9fcd625a` (0.14.0)
  - `flow-next` `bc464e5e` (0.17.4)
  - `message` `930c5169` (0.14.0)
  - `message-next` `481b579f` (0.17.0)
  - `harness` `d0224279` (0.3.4)
  - `orchestrate` `9070cbb8` (0.35.0)
- **Profile element.** `nix profile list` still holds `flow` → `c044v5pa…-flow-0.12.2`.
- **No connected peers.** `ss -xp` shows no connected peer on `/run/user/1001/flow/` or `/run/user/1001/message/`.
- **The message-daemon fault still stands.** `cmp ~/.local/state/message/messenger.sema messenger.sema.message-0.14.0.preopen` reports "differ: byte 169". Any restart of `message-daemon` 0.14.0 fails in its `ExecStartPre` preservation script, and that includes a rollback onto it. This is derived from the script text and was not run.
- **GC roots.** Both orchestrate candidates and the rollback generation are present, each held by a durable root in `~/.local/state/f1c841/gcroots/`:
  - `hm-candidate-orchestrate-0.36.1`
  - `hm-candidate-orchestrate-0.37.0`
  - `hm-rollback`

## (a) orchestrate: two candidates

### What differs

| | 0.36.1 (3ec648) | 0.37.0 (f1c841) |
|---|---|---|
| CriomOS-home branch | `3ec648-orchestrate-0.36` `feebd281` (parent `main` `0025894f`) | `f1c841-orchestrate-0.37` `61abe3fb` (parent `feebd281`) |
| orchestrate rev | `bc5cd36e` | `c7c44cb3` |
| Home generation | `/nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation` | `/nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation` |
| Nexus | `b2585m3p…-orchestrate-0.36.1` | `kjs1zikz…-orchestrate-0.37.0` |
| Pins | signal 7.0.0, signal-orchestrate and meta-signal-orchestrate 4.0.0, ethos-zero 13.0.0, protos 0.31.0 | signal 8.0.0, 5.0.0 / 5.0.0, ethos-zero 16.0.0, protos and datom-codec 0.32.2 |
| Wire | total break from 0.35.0, both directions | the same as 0.36.1: "No wire change on either socket and no store change" (orchestrate UPGRADES 0.36.1→0.37.0). Same total break from 0.35.0 |
| Client output | multi-line replies | every reply on one line (protos 0.32 `compact`) |
| Caller-set socket wrappers | yes | yes, carried over unchanged |
| `diff-closures` from live | only `orchestrate`, `orchestrate-clients`, `orchestrate-nexus` move | the same three, 0.35.0 → 0.37.0 |

### What is witnessed for each

| Fact | 0.36.1 | 0.37.0 |
|---|---|---|
| Generation built from the branch, with Lojix overrides on Prometheus; the control build at `0025894f` reproduces live `xp12f872…` | witnessed (3ec648) | witnessed, same command (`f1c841-home-build-037`, success) |
| The generation's own binaries start, answer `Observe.Locks` and meta `Configure` on a fresh store | **not witnessed** for the generation's binaries. orchestrate-test at `bc5cd36e` was green (fresh, populated-store, old-meta-name with the legacy name set by 0.36.x) | witnessed: sandbox `env -i` with the generation's Nexus and `home-path/bin` clients |
| The new release resumes a store **0.35.0 wrote**, with legacy `meta-orchestrate.sock`, a held Lock and the allocator | **not witnessed** | witnessed: orchestrate-test `b8e2b971`, `orchestrate-live-orchestrate` (0.35.0 is the exact live store path `6ynfv0hy…`) |
| Rollback: 0.35.0 resumes a store the new release served | **not witnessed** | witnessed: orchestrate-test `b8e2b971`, `orchestrate-rollback` (Lock held, overlap refused, next Lock numbered 2, meta socket served) |
| Installed wrappers honour `ORCHESTRATE_SOCKET`/`ORCHESTRATE_META_SOCKET` | witnessed (`orchestrate-wrapper-fallback` check, plus an `Unreachable` probe) | carried over unchanged. In the sandbox they were driven with no caller value |
| `nix flake check` on the branch | six failures, every one also failing at `main` `0025894f` | not re-run |

Not witnessed for either candidate:

- the three-step path live (0.35.0) → new release → 0.35.0
- a store of the live store's size and history
- Release of a resumed Lock
- a SIGKILL before rollback

### Pre-conditions (either candidate)

```sh
ls -d /nix/store/<candidate>-home-manager-generation   # rn8fzfbws25svmzpkfh2c9k7khnlzrx9 or qda5pkid3fa8aj1s32wqk8xcmd029dwm
readlink ~/.local/state/nix/profiles/home-manager       # home-manager-1039-link (else name the rollback anew)
orchestrate 'Observe.Locks'                             # must answer Observed.Locks.[]
```

Wait until no Lock is held. A held Lock survives in the store, but a script that captured a 0.35 client path fails against the new wire.

### Command sequence

```sh
/nix/store/<candidate>-home-manager-generation/activate
```

sd-switch restarts `orchestrate-nexus` onto the new Nexus. Not run.

### Post-checks (unverified on the live host)

```sh
readlink -f /proc/$(systemctl --user show -p MainPID --value orchestrate-nexus)/exe   # …-orchestrate-nexus-0.36.1 / -0.37.0
orchestrate 'Observe.Locks'                                                           # Observed.Locks.[]  exit 0
ORCHESTRATE_META_SOCKET=/run/user/1001/orchestrate-nexus/meta-orchestrate.sock \
  orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
orchestrate 'Observe.Locks'                                                           # still Observed.Locks.[]
systemctl --user restart orchestrate-nexus
orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
#   Configured.{ { /run/user/1001/orchestrate-nexus/orchestrate.sock /run/user/1001/orchestrate-nexus/orchestrate-meta.sock } True }  exit 0
orchestrate 'Observe.Locks'                                                           # Observed.Locks.[]
```

- **0.37.0.** The Configure through the legacy name is witnessed against 0.37.0 on a store 0.35.0 wrote (`resumed-meta-at-legacy`).
- **0.36.1.** It rests on the unchanged store format and the unchanged `Configure` form.

### Rollback

```sh
/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate   # = home-manager-1039-link, rooted by hm-rollback
orchestrate 'Observe.Locks'
```

- **0.37.0.** 0.35.0 reopening the store is witnessed in orchestrate-test.
- **0.36.1.** It is relayed from UPGRADES only.
- **Meta socket after rollback.** If the meta Configure was done, 0.35.0 binds `orchestrate-meta.sock`, which matches its wrapper.
- **Between the candidates.** A switch from 0.37.0 back to the 0.36.1 candidate is wire- and store-compatible. 0.37.0 opening a store 0.36.1 served is witnessed in `orchestrate-previous-orchestrate`.

**Cleanup after the ruling:** delete the unused link under `~/.local/state/f1c841/gcroots/`.

## (b) Flow: retire the stable 0.12.2; next slot 0.17.4 → 0.22.0

### What flow's UPGRADES require of a deployer (main `2fa51db8`, workspace 0.22.0)

| Release | Restart Nexus with `flow` and `flow-meta` together? | Store | Deployer effect |
|---|---|---|---|
| 0.19.0 | **Yes**: "an older client and a 0.19.0 Nexus do not read each other's frames" | unchanged ("no stored record holds either") | signal-flow 8.0.0 / meta-signal-flow 12.0.0. `QueueTurnEnd` answered `TurnEndRejected.QueueRefused`. Replies are one line. The exchange layer is not spoken; frames are still plain `Signal` frames |
| 0.20.0 | No: "No wire, storage or deployment change" | unchanged | only the Nexus's library surface (the Operation root) |
| 0.21.0 | **Yes**: "an older client and a 0.21.0 Nexus do not read each other's frames" | **changes**: "A 0.20.0 store opens unchanged: the events live in a new table" (`flow_nexus_flow_events`) | `Report` and meta `ReadEvents`. The new `flow-hook` executable sits beside `flow`. Every Claude launch's `--settings` carries `flow-hook` on SessionStart, PostToolUse (`*`) and Stop. Pane preparation unsets an inherited `FLOW_ID` |
| 0.22.0 | **Yes**: "Rebuild and restart the Nexus, `flow` and `flow-meta` together". The wire is unchanged from 0.21.0 | unchanged: "no table or row format changes" | A Claude launch's FlowId is claimed at Reserve by `flow-id claude --flows-root <root> --parent-session <session>`. Spawn exports `FLOW_ID=<FlowId>` and passes `--session-id <session>`. A failed claim answers `StartRejected.BindingRefused` before any pane opens. "make sure `flow-id` is on the Nexus's PATH" |

The 0.18.0 entry (no wire or store change; `FLOW_SOURCE_ROOT`/`FLOW_CODEX_*` no longer read; a fresh store needs a `Configure`) still applies on the way from 0.17.4. **No 0.19–0.22 entry names a Message version**; the coupling is stated on Message's side (see (c)).

#### Effects on launched seats (0.21.0 + 0.22.0)

- **Claude seats launched by 0.22.0.**
  - Each new Claude seat gets `FLOW_ID` in its pane environment from before the harness starts.
  - Flow chooses its session id, a UUIDv5 from the launch request id, and passes it as `--session-id`.
  - Flow writes the claim marker `<source root>/flows/.<FlowId>.flow-id` at Reserve. The source root is `/home/li/primary`, from the next slot's `Configure`.
  - `flow-hook` reports `Started`, `ToolUsed.«tool»` and `Stopped`.
- **Seats running across the restart.** They keep the settings they were launched with: no hook, and no Flow-given `FLOW_ID`. They report nothing.
- **Attempts in flight across the restart.** An attempt reserved before 0.22.0 holds no FlowId, and is "resumed or reported pending as before, never respawned". The UPGRADES says this of 0.21.0. From a 0.17.4 store it is **unverified**.
- **Where the hook's Reports go: inferred, unverified, and important for the next slot.**
  - `flow-hook` runs the `flow` beside it (`${package}/bin/flow`, not the `flow-next` wrapper).
  - That `flow` reaches `FLOW_SOCKET`, or else `$XDG_RUNTIME_DIR/flow/flow.sock` (`crates/flow/src/main.rs`).
  - Nothing in flow-nexus sets `FLOW_SOCKET` in the pane. A pane's environment comes from the Herdr server, whose `XDG_RUNTIME_DIR` is presumably `/run/user/1001`.
  - So a seat launched by the **next-slot** Nexus would send its Reports to `/run/user/1001/flow/flow.sock`. That is the stable 0.12.2 today, and nothing after B1.
  - The hook always exits 0, so the seat is unharmed. But `ReadEvents` on the next Nexus would show the flow with an empty events vector.
  - Reports reach the right Nexus only once 0.22.0 serves `/run/user/1001/flow/`, which is the later stable/next roll, or once the pane's environment carries `FLOW_SOCKET`.
  - The post-check below tells the two cases apart.
- **The Codex limitation.**
  - A Codex launch reserves no FlowId and binds as before.
  - Its session id is named by the app server after the harness starts, so Flow cannot claim first.
  - The hook is Claude-only.
  - So nothing reports for Codex seats, and they get no Flow-given `FLOW_ID` (`reports/flow-message-signal8.md`, "Red and open").
- **Session-id collision (red, open).** The session id is a pure function of the launch request id. Another store that reuses a request id would choose the same session.
- **`flow-id` on the Nexus PATH.** `flowRuntimePath` already holds `inputs.harness` (0.3.4, `d0224279`). flow-test witnessed the claim with harness 0.4.0 (`8604a073`). `git diff d0224279 8604a073 -- src/flow_id.rs` is formatting only: borrow sigils, brace layout and import order. So 0.3.4 should accept Flow's UUIDv5 claim. That is derived from the diff and **not run** with 0.3.4.
- **Unverified: a seat that also claims for itself.** A seat whose own startup protocol runs `flow-id claude` again for the same session would meet the existing marker. Whether that returns the same alias was not run.

### What the CriomOS-home modules must change

In `modules/home/profiles/min/flow-message-next.nix` (main `0025894f`):

1. **`flowNexusUnit` `Environment` (lines 114-122).** Delete `FLOW_SOURCE_ROOT` and the eight `FLOW_CODEX_*` entries; none has been read since 0.18.0.
   - Keep `instance.anchorEnvironment`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME` and `PATH`.
   - `PATH` must keep `inputs.harness` for `flow-id`.
   - `ExecStart = "${instance.package}/bin/flow-nexus"` stays, with no arguments. `flow-hook` is found beside it in the same package (`crates/flow/Cargo.toml` bin `flow-hook`; flake `cargoExtraArgs = "--workspace"`), so **no hook setting is written by Home**.
2. **`flow-configuration-next`.** It is unchanged in shape. meta-signal-flow 14.0.0's `Configuration.{ OrdinarySocketPath MetaSocketPath SourceRoot StableCodex NextCodex Vector<HarnessProfile> MetaAspects MessageNexusPath }` is identical to 11.0.0's (ethos read).
   - Its datom names `${message.next.package}/bin/message-nexus`, so moving `message-next` changes the unit, and it re-runs.
   - **Unverified against 0.22.0:** that the existing store's configuration is resumed and the oneshot answers `Configured`.
3. **Dead bindings.** `occupiedNextFlowUnit` and `occupiedNextFlowConfigurationUnit` (lines 131-183) are unreferenced and can go.
4. **The comment at lines 18-21** ("next is Flow 0.17.0 and Message 0.17.0") becomes "Flow 0.22.0 and Message 0.19.0".

In `flake.nix`/`flake.lock`:

- `flow-next` `bc464e5e` → `2fa51db8` (0.22.0).
- `message-next` `481b579f` → `ce3eb6c6` (0.19.0). This is required by the coupling in (c).

`modules/home/profiles/min/flow.nix` (B1):

- Set `criomosHome.flow.enable = false` for li, or drop the import. This removes `flow-nexus` and the `flow` 0.14.0 package.
- If the unit is instead kept for a later roll, lines 81-89 lose `FLOW_SOURCE_ROOT`/`FLOW_CODEX_*`, and the unit needs a `Configure` of its own.

### Which flow-nexus to retire

**Retire the stable 0.12.2 at `/run/user/1001/flow/`; upgrade the next slot.** The reasons stand as given in `morning-deploy-f1c841.md` (b), re-read today:

- **Nothing declares the 0.12.2.** It runs only through the hand drop-in and the `nix profile` element. Home declares 0.14.0.
- **Only the next slot is paired with a Message.** `nextPeers.flow = flow.next`, and `flow-configuration-next` admits `message.next`'s executable.
- **Only the next slot has the meta `Configure`** that 0.18+ requires.
- **The next store already holds the adopted configuration.** 0.18–0.22 say the store opens unchanged; for 0.21.0 the events go in a new table.
- **Whether 0.22.0 opens a 0.12.2-written store is unverified.**

One cost follows: hook Reports from next-slot seats land on the stable socket path (above) until the later roll moves 0.22.0 into the stable slot.

### What building the Flow/Message generation would take (not done)

1. A CriomOS-home branch whose parent is the source of the generation live at that moment:
   - `0025894f` if (a) is not taken
   - `feebd281` after the 0.36.1 switch
   - `61abe3fb` after the 0.37.0 switch

   Make the module edits above, plus B1's `enable = false`, plus (d) if ruled, in **one** generation, so the Flow Nexuses restart once. Then run `nix flake update flow-next message-next` after editing the two URLs.
2. Build on Prometheus in a bounded user unit, exactly as (a) did:
   ```sh
   nix build --max-jobs 0 '.#homeConfigurations.li.activationPackage' \
     --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system \
     --override-input horizon path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon
   ```
   This also compiles flow 0.22.0 and message 0.19.0, with their ethos-zero 16 build steps.
3. Read `nix store diff-closures` from live. Expect:
   - `flow` 0.14.0 leaves
   - `flow-next` 0.17.4 → 0.22.0
   - `message-next` 0.17.0 → 0.19.0
   - and, with (d), `claude-code`

   Nothing else should move.
4. Root the result: `nix-store --add-root ~/.local/state/f1c841/gcroots/hm-candidate-flow-0.22 --indirect -r <path>`.
5. Witness the generation's own binaries in a sandbox before the morning, with a fresh `HOME`/`XDG_RUNTIME_DIR`:
   - start the generation's `flow-nexus`, then `message-nexus`
   - run `message 'Send.{ [ 7d41e0 ] Soft Text.hello }'` → `SendRejected.SenderUnknown`
   - run `message-meta …` → `SendRejected.UnknownRecipient.7d41e0`

   This is the pair already witnessed with debug builds in `flow-message-signal8.md`. Also start the generation's 0.17.4 Nexus on a store 0.22.0 has served, to witness the rollback.
6. Optionally run the branch's `nix flake check` with the same overrides. Six checks already fail at `main`.

### B1. Retire the stable 0.12.2 (unchanged from the previous report)

**Pre-conditions**

```sh
readlink /proc/$(systemctl --user show flow-nexus -p MainPID --value)/exe   # …c044v5pa…-flow-0.12.2/bin/flow-nexus
ss -xp | grep '/run/user/1001/flow/flow'                                   # no output
cat ~/.config/systemd/user/flow-nexus.service.d/override.conf              # ExecStart= / ExecStart=…c044v5pa…-flow-0.12.2/bin/flow-nexus
nix profile list                                                           # Name: flow → …c044v5pa…-flow-0.12.2
nix-store --add-root ~/.local/state/flow/flow-0.12.2.root -r /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2
```

Also confirm that no seat the living cares about is held only by the 0.12.2 store. Use the 0.12.2 `flow 'List.{}'`; that it writes nothing is **unverified**.

**Command sequence** (unverified; part of the one generation above)

1. `<new-generation>/activate`. sd-switch stops and removes `flow-nexus.service`; the drop-in directory remains.
2. Then:
   ```sh
   systemctl --user stop flow-nexus 2>/dev/null || true
   cp --reflink=auto ~/.local/state/flow/flow.sema ~/.local/state/flow/flow.sema.flow-0.12.2.retired
   mv ~/.config/systemd/user/flow-nexus.service.d/override.conf ~/.local/state/flow/override.conf.retired
   rmdir ~/.config/systemd/user/flow-nexus.service.d
   systemctl --user daemon-reload
   nix profile remove flow
   ```
   Do not remove the drop-in while the Home unit still exists: the unit would fall back to 0.14.0 and restart.

**Post-checks** (unverified)

```sh
systemctl --user status flow-nexus        # Unit flow-nexus.service could not be found.
ls /run/user/1001/flow                    # No such file or directory
command -v flow flow-meta                 # nothing
```

**Rollback**

1. Activate the previous generation.
2. `mkdir -p ~/.config/systemd/user/flow-nexus.service.d && install -m 600 ~/.local/state/flow/override.conf.retired ~/.config/systemd/user/flow-nexus.service.d/override.conf`
3. `nix profile install /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`
4. `systemctl --user daemon-reload && systemctl --user restart flow-nexus`
5. Check with `readlink /proc/$(systemctl --user show flow-nexus -p MainPID --value)/exe`.

The 0.12.2 store was never touched.

### B2. Next slot 0.17.4 → 0.22.0 (with C1 in the same generation)

**Pre-conditions**

```sh
readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe   # …7z15aqi4…-flow-0.17.4
ls -l ~/.local/state/flow-next/.local/state/flow/flow.sema                        # present: resumed, not seeded
systemctl --user is-active flow-configuration-next                               # active
flow-next 'List.{}'                                                               # Listed.[ … ]  (note the rows)
command -v flow-id; ls -d /home/li/primary/flows                                  # the claim helper and flows root exist
cp --reflink=auto ~/.local/state/flow-next/.local/state/flow/flow.sema ~/.local/state/flow-next/.local/state/flow/flow.sema.flow-0.17.4.predeploy
```

- No `flow-next 'Start…'` in flight, and no seat being launched.
- No message-next delivery the living cares about in flight. A restarted Message resumes `Submitted`/`Parked`.
- The generation was built as above, and its diff-closures read.

**Command sequence** (unverified)

```sh
<new-generation>/activate
```

sd-switch restarts:

- `flow-nexus-next` (new ExecStart)
- `flow-configuration-next` (`PartOf`; datom changed)
- `message-nexus-next` (new ExecStart)

`flow-next-clients` and `message-next-clients` swap in with the same builds. That satisfies "restart Nexus, `flow` and `flow-meta` together" and Message's "start Flow first, then Message", since `message-nexus-next` is `After=flow-nexus-next`. **Unverified:** that sd-switch orders the three restarts that way within one activation.

**Post-checks** (unverified)

```sh
readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe   # …-flow-0.22.0/bin/flow-nexus
systemctl --user show flow-configuration-next -p ActiveState,Result              # ActiveState=active Result=success
journalctl --user -u flow-configuration-next -n 3                                # Configured.{ … }
systemctl --user show flow-nexus-next -p Environment | grep -c FLOW_             # 0
flow-next 'List.{}'                                                              # Listed.[ … ] exit 0, the same rows as before
flow-next 'QueueTurnEnd.{ s-check t-check None }'                                # TurnEndRejected.QueueRefused (datom shape from the ethos)
ls "$(dirname "$(readlink -f "$(command -v flow-next)")")"                       # wrapper dir; the package beside flow-nexus holds flow-hook
```

Launch check, which opens a real seat, so it is the living's call. Start one small Claude flow through `flow-next 'Start…'`, then:

```sh
flow-next-meta 'ReadEvents.<its FlowId>'
#   EventsRead.{ <id> [ Started … ] }   — Reports reach the next Nexus
#   EventsRead.{ <id> [] }              — Reports went to /run/user/1001/flow/ (see "Where the hook's Reports go")
ls /home/li/primary/flows/.<its FlowId>.flow-id                                   # the claim Flow made at Reserve
```

Then, in that seat's pane, `printenv FLOW_ID` gives its FlowId.

**Rollback** (unverified)

1. Activate the previous generation. `flow-nexus-next` returns to `7z15aqi4…-flow-0.17.4` and `message-nexus-next` to `3v8qs8h4…-message-0.17.0`. Both CLIs return with them.
2. **The store risk.** No UPGRADES entry states that 0.17.4 opens a store that 0.21.0+ has given the new `flow_nexus_flow_events` table. If `flow-nexus-next` fails to start:
   ```sh
   systemctl --user stop flow-nexus-next
   cp ~/.local/state/flow-next/.local/state/flow/flow.sema.flow-0.17.4.predeploy ~/.local/state/flow-next/.local/state/flow/flow.sema
   systemctl --user start flow-nexus-next
   ```
   Flows launched under 0.22.0 are then absent from the restored store.
3. Check with `flow-next 'List.{}'`.

Seats launched under 0.22.0 keep their hook settings. After the rollback their Reports reach no Nexus that knows `Report`, and the hook exits 0.

## (c) Message: next slot 0.17.0 → 0.19.0

### The Flow–Message coupling, as the UPGRADES state it

- **message 0.17.1 → 0.18.0:** "Message 0.18.0 and Flow 0.19.0 are deployed together. Neither reads the other's older frames: Message 0.17.x … cannot talk to Flow 0.19.0, and Message 0.18.0 cannot talk to Flow 0.18.0 or earlier." "Every client on the host that speaks to either socket must be 0.18.0 / 0.19.0 at the same time."
- **message 0.18.0 → 0.19.0:** "Message 0.19.0 holds exactly the contract revisions Flow 0.22.0 holds":
  - signal-message 10.0.0 `b94d907c`
  - meta-signal-message 0.10.0 `81e12b23`
  - signal-flow 10.0.0 `f95034de`
  - meta-signal-flow 14.0.0 `54eb5618`
  - signal 8.0.0 `f35460de`

  "Deploy with Flow 0.22.0: rebuild both, start Flow first, then Message. No unit, store or configuration change." Message's own wire is unchanged from 0.18.0, and "a 0.18.x store opens unchanged".
- **Flow's side** names no Message version from 0.19.0 on.

**What was witnessed instead of claimed.**

- In `reports/message-repin.md`, Message 0.18.0 **and** Message 0.17.1 (`c00hqwp5…-message-0.17.1`) each decoded Flow 0.19.0's replies over the real sockets:
  - `SendRejected.SenderUnknown` (ResolvePeer)
  - `SendRejected.UnknownRecipient.7d41e0` (Vet)
- So "Message 0.17.x cannot talk to Flow 0.19.0" is a **claim**, contradicted on those two paths. Deliver, Observe, and a reply that holds an appended signal-flow 8.0.0 variant were not tested.
- Message 0.19.0 against Flow 0.22.0 gave the same two replies (debug builds, `reports/flow-message-signal8.md`).
- **Not witnessed:** Message 0.17.x or 0.18.0 against Flow 0.21/0.22, where meta-signal-flow 13.0.0 appended `ReadEvents`.
- **Ruling basis:** deploy them as the UPGRADES pair them, Flow 0.22.0 with Message 0.19.0, in one generation.

### C1. message-next 0.17.0 → 0.19.0 (the message half of B2)

**Module change:** the flake input `message-next` → `ce3eb6c6` only. 0.15.0 onward needs no unit change: `messageNexusUnit` runs `message-nexus` with no arguments, with `HOME` and `XDG_RUNTIME_DIR`. The 0.17.0 store opens unchanged through 0.17.1, 0.18.0 and 0.19.0.

**Pre-conditions**

```sh
readlink /proc/$(systemctl --user show message-nexus-next -p MainPID --value)/exe   # …3v8qs8h4…-message-0.17.0/bin/message-nexus
readlink /run/user/1001/message-next/flow                                          # /run/user/1001/flow-next/flow
cp --reflink=auto ~/.local/state/message-next/.local/state/message/message.sema ~/.local/state/message-next/.local/state/message/message.sema.message-0.17.0.predeploy
```

- **Wrappers.** The hand-written `~/.local/bin/message-next` and `message-next-meta` point at `nwrvnmk7…-message-0.17.0`. After the switch they would speak 0.17's wire to a 0.19.0 Nexus. Remove them, or confirm that Home's `message-next-clients` come first on PATH: `command -v message-next`.

**Command sequence:** the same activation as B2. Unverified.

**Post-checks** (unverified)

```sh
readlink /proc/$(systemctl --user show message-nexus-next -p MainPID --value)/exe   # …-message-0.19.0/bin/message-nexus
readlink -f "$(command -v message-next)"                                           # Home's message-next-clients wrapper, not ~/.local/bin
message-next 'QueryReceipts.m-000000'                                              # MessageRejected.UnknownMessage (token shape unverified)
```

End-to-end check, a real letter, so the living's call. From a plain terminal outside any pane:

```sh
message-next-meta 'Send.{ [ <a live flow id> ] Soft Text.«deploy check» }'
#   Submitted.{ m-… [ { <id> … } ] }   and the letter appears in that pane
#   FlowUnreachable                     — the coupling or the admission broke
```

**Rollback:** the same activation as B2's rollback. Reopening the store with 0.17.0 after 0.19.0 is inferred from "no stored record's archive changes" (0.18.0, 0.19.0) and is **unverified**. If the open fails, stop the unit, restore the `.message-0.17.0.predeploy` copy, and start the unit.

### C2. The stable `message-daemon` 0.14.0 → 0.19.0 (optional)

The unit change in the previous report (c) stands, with the target now `ce3eb6c6`:

- `ExecStart` takes no argument.
- Drop `message-write-configuration` and the preservation script.
- Remove `messageProfilePackage`: it references binaries that no longer exist, so it would fail to build (derived, not built).
- Install `message.stable.clients`.
- The unit is renamed `message-nexus`.

New since then: a stable Message 0.19.0 can use only a Flow 0.22.0.

- After B1, no Flow serves `/run/user/1001/flow/`. Run `message-meta 'Configure.{ /run/user/1001/message/message.sock /run/user/1001/message/message-owner.sock /run/user/1001/flow-next/flow/flow.sock /run/user/1001/flow-next/flow/flow-meta.sock [ Psyche ] }'` from outside any pane.
- Next Flow admits the `MessageNexusPath` its Configure names. If stable and next Message are the same 0.19.0 package, the executable path is identical. Whether that admits both is **unverified**.
- The 0.14.0 ledger is not migrated. Copy `messenger.sema` aside first.
- The rollback onto 0.14.0 **fails** unless the differing `messenger.sema.message-0.14.0.preopen` is moved aside first. Use the `mv` given in the previous report's (c).

Unverified throughout. Whether a second, stable Message is wanted at all, or message-daemon is simply retired with message-next as the only Message, is the living's ruling.

## (d) The installed `claude` wrapper: choices unchanged

The definitions, consumers and choices in `morning-deploy-f1c841.md` (d) stand. Re-read:

- CriomOS-home `main` is still `0025894f`, so `owned-agents/claude-code/default.nix:51-68` and `codex-remote-control.nix:51-56` are as cited there.
- In flow 0.22.0 the seat's bypass mode is in `claude_flag_settings`, `crates/flow-nexus/src/herdr/launch.rs` ~line 176: `"permissions": { "defaultMode": "bypassPermissions" }`. The same flag settings now also carry the `flow-hook` hooks.
- Flow never passes `--dangerously-skip-permissions` itself, per the comment at `CLAUDE_SKIP_PERMISSIONS_FLAG`.

The choices:

1. **Keep.** No change and no restart. Every seat stays in bypass. A sandbox that needs a mode calls `.claude-wrapped` by store path.
2. **Honour a requested mode.** Delete `--add-flags "--dangerously-skip-permissions"` (line 54).
   - The default stays bypass through `settings.json` and Flow's flag settings.
   - A caller's `--permission-mode` takes effect; its precedence is **unverified**.
   - The `claude-code` path changes. That changes the Flow Nexus units' `PATH`, which restarts them, so fold it into the B2 generation.
3. **Default to another mode.** Choice 2, plus:
   - `codex-remote-control.nix:54` set to the chosen mode
   - a Flow release that drops or parameterises the `bypassPermissions` in `claude_flag_settings`
   - a decision on `direct-claude`

   Unattended seats would stop at permission prompts (inferred, unverified).

Pre-conditions, sequence, post-checks and rollback for choice 2 are as in the previous report:

- Pre-condition: `tail -1 "$(readlink -f "$(command -v claude)")"` shows the flag.
- Afterwards it does not, and `jq -r .permissions.defaultMode ~/.claude/settings.json` still reads `bypassPermissions`.
- Behaviour check, unverified: in a throwaway directory, `claude -p --permission-mode default 'create the file x.txt containing y'` is refused and leaves no `x.txt`.
- Rollback: activate the previous generation.

## Order, if more than one is ruled

Each later generation's branch must have the source of the then-live generation as its parent. Otherwise one activation undoes another, and each rollback target is named anew.

1. **(a)**, 0.36.1 or 0.37.0. It is independent of Flow and Message, and it is the only deployment with a built, rooted artifact.
2. **One generation for B1 + B2 + C1, and (d) if choice 2.** It is built from (a)'s branch. Not built yet.
3. **C2**, last, only if a stable Message is still wanted.

## Sources

- **This flow's reports:**
  - `reports/morning-deploy-f1c841.md` (form; (b)–(d) carried)
  - `reports/morning-deploy-orchestrate-037.md`
  - `reports/orchestrate-rollback-witness.md`
  - `reports/message-repin.md` ("Witness: Message against a real Flow 0.19.0", "Correction to the brief")
  - `reports/flow-message-signal8.md` (versions, pins, live witness, flow-claude-hook, "Red and open")
  - `witnesses/gc-roots.md`
- **3ec648:** `flows/3ec648/reports/morning-deploy.md` (via the copied (a)) and `flows/3ec648/reports/orchestrate-test.md` (0.36.1 checks at `bc5cd36e`).
- **flow `2fa51db8`:**
  - `UPGRADES.md` (0.18.0–0.22.0) and `README.md`
  - `Cargo.toml` (pins)
  - `crates/flow/Cargo.toml` (bin `flow-hook`), `crates/flow/src/hook.rs`, `crates/flow/src/main.rs` (socket default)
  - `crates/flow-nexus/src/herdr.rs` (`harness_hook`, `flow_id_executable`, `flows_root`)
  - `crates/flow-nexus/src/herdr/launch.rs` (`claude_flag_settings`, `CLAUDE_INHERITED_ENVIRONMENT`)
  - `flake.nix`
- **message `ce3eb6c6`:** `UPGRADES.md` (0.14.0–0.19.0) and `Cargo.toml`.
- **meta-signal-flow `54eb5618`:** `UPGRADES.md` (12.0.0–14.0.0); `ethos/signal.ethos` against `2ac045c2` (Configuration unchanged).
- **signal-flow `f95034de`:** `ethos/signal.ethos` (`ListRequest.{}`, `TurnEndRequest`, `Report`).
- **orchestrate `c7c44cb3`:** `UPGRADES.md` (0.36.1→0.37.0).
- **harness:** `d0224279` against `8604a073`, `src/flow_id.rs` diff and `UPGRADES.md`.
- **CriomOS-home `origin/main` `0025894f`:**
  - `flake.lock`
  - `modules/home/profiles/min/flow-message-next.nix`
  - `modules/home/profiles/min/flow.nix`
  - `lib/stable-next-service.nix`
- **CriomOS-home branches:** `origin/3ec648-orchestrate-0.36`, `origin/f1c841-orchestrate-0.37`.
- **Live host, read-only, 2026-10-03:**
  - `systemctl --user show -p MainPID/ExecStart` and `is-active` for the six units
  - `readlink /proc/<pid>/exe`
  - `readlink` of the home-manager profile
  - `ls /run/user/1001/orchestrate-nexus/`
  - `cmp` of `messenger.sema` against its `.preopen`
  - `ls ~/.local/state/f1c841/gcroots/`
  - `ls -d` of the three generations
  - `ss -xp`
  - `nix profile list`
  - `ls` of the flow-nexus drop-in
- **Skills loaded:** subflow, flow-evidence, knowledge-nexus, nix-workflow, breaking-upgrades, compensation-primary-commit.

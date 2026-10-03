# Deployment: orchestrate 0.37, flow 0.23, message 0.19 as the regular versions

Subflow of f1c841, 2026-10-03, on ouranos. Ruling: the living, STT ~06:40,
"Everything can get deployed … I want all this deployed, made as the regular
version in [CriomOS] in our home." The `claude` wrapper's bypass is not in
scope and was not touched.

Every reply below is copied from the terminal at the time given (local time,
-06:00).

## Before (06:39)

- Home profile: `home-manager-1039-link` → `xp12f872…-home-manager-generation`.
- `orchestrate-nexus` → `0grjjmjc…-orchestrate-nexus-0.35.0`; sockets `orchestrate.sock`, legacy `meta-orchestrate.sock`.
- `flow-nexus` → `c044v5pa…-flow-0.12.2` (hand drop-in), `/run/user/1001/flow/`.
- `flow-nexus-next` → `7z15aqi4…-flow-0.17.4`, `/run/user/1001/flow-next/flow/`; `flow-configuration-next` active.
- `message-daemon` → `i66j8l0v…-message-0.14.0`, `/run/user/1001/message/`.
- `message-nexus-next` → `3v8qs8h4…-message-0.17.0`, `/run/user/1001/message-next/message/`.
- `nix profile list`: `flow` → `c044v5pa…-flow-0.12.2`, `home-manager-path` → `acj63i96…`.
- PATH: `orchestrate`, `orchestrate-meta` → `v42cxgyd…-orchestrate-0.35.0-profile`; `flow`, `flow-meta` → `c044v5pa…-flow-0.12.2`; `flow-next` → `v7ay3kxp…-flow-next-clients`; `message` → `sh4cyk13…-message-0.14.0-profile`; `message-meta` → `i66j8l0v…-message-0.14.0`; `message-next`, `message-next-meta` → hand-written `~/.local/bin/` wrappers.
- `orchestrate 'Observe.Locks'` (06:39): two Locks held, 11715 FlowNext and 11716 Sema018, both FlowId f1c841 (this flow's own subflows). Told f1c841 through hm-send (`Transported.{ f1c841 working }`, 06:39); the coordinator answered that both will release.

- Rows, before: the stable 0.12.2 store lists 26 flows (17 Active, 9 Pending); the next 0.17.4 store lists 5 (`flow-next 'List.{}'`). The brief moves the next store to the regular path; the 0.12.2 store is retired aside, not merged (its rows are not served after step 3). Full listings: session scratchpad `flow-0122-list-before.txt`, `flow-next-list-before.txt`.
- `message-next 'QueryReceipts.m-0000'` (06:42) through the hand wrapper: `message-next[3]: /nix/store/nwrvnmk7…-message-0.17.0/bin/message: inaccessible or not found` — the wrapper's target was already garbage-collected.

## Choice: three activations, not one

1. `qda5pkid…` (orchestrate 0.37.0 only), gated on an empty Lock list.
2. `2hnqcg3q…` (adds next Flow 0.23.0 and next Message 0.19.0). Its orchestrate unit is identical to (1)'s, so orchestrate is not restarted again.
3. A generation built from CriomOS-home main carrying a new commit that makes the pair regular.

Why separate: each has its own witnessed rollback target (xp12f872 → qda5pkid → 2hnqcg3q), the orchestrate switch alone is gated on other seats' Locks, and a red Flow/Message post-check then never forces orchestrate back across the total wire break.

## The regular-slot commit (CriomOS-home 9497e4fb, on 4b863bb5)

- `profiles/min/flow-message-next.nix` → `flow-message.nix`: the stable slot of `lib/stable-next-service.nix` runs as `flow-nexus`, `flow-configuration`, `message-nexus` on the user's own anchors (sockets `%t/flow/`, `%t/message/`; stores `~/.local/state/flow/flow.sema`, `~/.local/state/message/message.sema`; clients `flow`, `flow-meta`, `message`, `message-meta`). The next slot is off (`criomosHome.flowMessage.next.enable = false`). The dead `occupiedNext*` bindings are removed.
- `flake.nix`/`flake.lock`: `flow` → `636214e5` (0.23.0), `message` → `ce3eb6c6` (0.19.0); `flow-next`/`message-next` unchanged (same revisions, unused while next is off).
- Removed: `profiles/min/flow.nix` (Flow 0.14 `flow-nexus`), `profiles/min/message.nix` (Message 0.14 `message-daemon`), and their checks `flow-service-path`, `message-service-path`. `checks/flow-message-next` → `checks/flow-message` (regular units, regular CLIs on a fresh store, next units distinct when on). `herdr-agent-executable` no longer imports `flow.nix`.
- `UPGRADES.md`: entry "Flow 0.23.0 and Message 0.19.0 become the regular pair; next slot off" with the activation steps below.
- Tension, noted: the compensation-update skill says promotion keeps the Next endpoint's state root and socket and never moves its state. The brief orders the stores moved to the regular paths and the regular socket names. The brief governs; the stores are moved closed, and each store is first reconfigured to the regular socket paths through its own running Nexus.

## State reached when the living ordered the seat wound down (06:53)

**Nothing was switched, activated, restarted, stopped or moved on the host.** No store was copied or moved; no drop-in, profile element or wrapper was touched. The running set is exactly "Before" above (re-read 06:53: `orchestrate-nexus` 0.35.0, `flow-nexus` 0.12.2, `flow-nexus-next` 0.17.4, `message-daemon` 0.14.0, `message-nexus-next` 0.17.0; profile `home-manager-1039-link`). Every Nexus answers as before. No rollback was needed.

Done:

- CriomOS-home commit `9497e4fb249004cd53c14fa97c981830e26a5a3b` (the regular-slot commit above), on `4b863bb5` → `61abe3fb` → `feebd281` → main `0025894f`. Pushed as branch `f1c841-regular`. **Not merged to main.** Worktree `~/wt/github.com/LiGoldragon/CriomOS-home/regular-f1c841` (jj workspace `regular-f1c841`); its lock 11723 is released.
- Its generation, built on Prometheus (`--max-jobs 0`, user unit `f1c841-home-build-regular`, Result=success, 06:53) with the usual `--override-input system`/`horizon` from `/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/`: `/nix/store/1rj6l1lnizjnkjivjmrmwwbnhlkgjd34-home-manager-generation`, GC-rooted as `~/.local/state/f1c841/gcroots/hm-candidate-regular`.
- `nix store diff-closures 2hnqcg3q… 1rj6l1ln…`: `flow` 0.14.0 and `message` 0.14.0 leave; `flow-configuration-next`, `flow-nexus-next`, `message-nexus-next`, `message-daemon` units and their scripts leave; `flow-configuration.service` and `message-nexus.service` arrive. Orchestrate does not move.
- Checks built with the same overrides, both green: `checks.x86_64-linux.flow-message` (`i1kdv0v1…-flow-message`: regular Flow, its configuration and regular Message on a fresh store; `flow 'List.{}'` → `Listed.[]`, `message-meta` Send → `SendRejected.UnknownRecipient.7d41e0`, `message` → `MessageRejected.UnknownMessage`) and `checks.x86_64-linux.herdr-agent-executable`.
- The Lock gate opened at 06:46 (11715 FlowNext and 11716 Sema018 released). At 06:53 only `11766 PrimaryPublish 5578cc` (sentinel) was held.

Not done (all of steps 1–4 on the host):

- Step 1 (orchestrate 0.37.0) not activated.
- Step 2 (next Flow 0.23.0 / Message 0.19.0) not activated; next stores not copied.
- Step 3 not done. Written but **not run**: the sandbox witness of the migration, `~/.local/state/f1c841/regular-witness/sandbox-regular.sh <1rj6l1ln-generation> <2hnqcg3q-generation>` (next units make stores, both are reconfigured to the regular paths through their running Nexuses, the stores are moved, the regular units start on them, restart resumes). Run it before step 3.
- Step 4: main not moved; no generation from main activated.

Found on the way:

- Both stores record their socket paths and resume them (flow `crates/flow-nexus/src/lib.rs:438` takes the ordinary socket from `store.configuration()`; message `crates/message-nexus/src/configuration.rs`: "a populated store resumes what it holds, and meta Configure changes it"; message's record also holds Flow's socket paths, today `/run/user/1001/message-next/flow/…`). A moved next store would bind the next paths again; hence the reconfigure-before-move step.
- The hand-written `~/.local/bin/message-next` wrapper already fails (its 0.17.0 target is gone from the store).
- The 0.12.2 stable store holds 26 flows; moving the next store (5 flows) to the regular path leaves those 26 unserved (preserved aside). The brief chose the next store; flagged for the living.

## Next commands, for the successor (in order, each witnessed)

1. `orchestrate 'Observe.Locks'` → must be `Observed.Locks.[]`. Then `/nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation/activate` and the post-checks of `morning-deploy-orchestrate-037.md` (meta Configure through `meta-orchestrate.sock`, restart, Configure through the wrapper, `Observe.Locks`; `readlink -f $(command -v orchestrate)` → `vsj5mw3j…-orchestrate-0.37.0-profile`). Rollback: `xp12f872…/activate` (root `hm-rollback`).
2. Pre-checks, store copies and switch of `morning-deploy-flow-message.md` (`2hnqcg3q…/activate`, then start `flow-nexus-next`, `flow-configuration-next`, `message-nexus-next`); move `~/.local/bin/message-next{,-meta}` to `~/.local/state/f1c841/retired-wrappers/`. Leave the stable 0.12.2 running until 3. Rollback: that report's.
3. Run `sandbox-regular.sh` above; if green:
   - copy both next stores closed again (`.pre-regular`), with the next pair stopped, then restart them; or reconfigure first while running:
   - `flow-next-meta` with the datom of the new `flow-configuration` unit (from `1rj6l1ln…/home-files/.config/systemd/user/flow-configuration.service`, `%t` → `/run/user/1001`) → expect `Configured.{ … NexusRestartRequired }`;
   - `message-next-meta 'Configure.{ /run/user/1001/message/message.sock /run/user/1001/message/message-owner.sock /run/user/1001/flow/flow.sock /run/user/1001/flow/flow-meta.sock [ Psyche ] }'`;
   - stop `message-nexus-next flow-nexus-next message-daemon flow-nexus`; move `~/.config/systemd/user/flow-nexus.service.d/override.conf` → `~/.local/state/flow/override.conf.retired` (rmdir the drop-in dir; `daemon-reload`); `nix profile remove flow`;
   - move aside (never delete) `~/.local/state/flow/flow.sema` and `launch-bundles/` (0.12.2) and `~/.local/state/message/messenger.sema.message-0.14.0.preopen`; move `~/.local/state/flow-next/.local/state/flow/*` → `~/.local/state/flow/` and `~/.local/state/message-next/.local/state/message/message.sema` → `~/.local/state/message/`;
   - `1rj6l1ln…/activate` (or the generation rebuilt from main, step 4), then `systemctl --user start flow-nexus flow-configuration message-nexus`;
   - post-checks: `/proc/<pid>/exe` of `flow-nexus` → `v945vrls…-flow-0.23.0`, of `message-nexus` → `np57gg4b…-message-0.19.0`; `ls /run/user/1001/flow /run/user/1001/message`; `flow 'List.{}'` = the 5 rows of `flow-next-list-before.txt`; `message 'QueryReceipts.m-0000'` → `MessageRejected.UnknownMessage`; `command -v flow message` → the `flow-clients`/`message-clients` wrappers.
   - Rollback: stop the three regular units, move the stores back (or restore the closed copies), restore the drop-in and `nix profile install /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`, activate `2hnqcg3q…`, start the next pair. message-daemon 0.14.0 cannot be restarted while its differing `.preopen` sits in place (known fault).
4. Land: fast-forward CriomOS-home main to `9497e4fb` if main is still `0025894f` (else duplicate the four commits onto it), push, rebuild from main (expect the same `1rj6l1ln…` if main equals the branch), activate that one, root the previous generation under `~/.local/state/f1c841/gcroots/`.

Running seats keep their old environment (`FLOW_SOCKET`, hooks) until relaunched.

## Sources

- Reports read: `reports/morning-deploy-final.md`, `morning-deploy-orchestrate-037.md`, `morning-deploy-flow-message.md`, `orchestrate-rollback-witness.md` (first 80 lines).
- CriomOS-home `4b863bb5`: `lib/stable-next-service.nix`, `modules/home/profiles/min/{flow,flow-message-next,message}.nix`, `checks/{flow-message-next,flow-service-path,message-service-path,herdr-agent-executable,main-contract-pins}`, `flake.nix`, `UPGRADES.md`, `modules/home/default.nix`; grep of `/home/li/primary/CriomOS` for the options (none).
- flow `636214e5` (`/nix/store/q9cfswk0…-source`) `crates/flow-nexus/src/lib.rs`, `herdr.rs`; message `ce3eb6c6` (`/nix/store/dgffb5mv…-source`) `crates/message-nexus/src/configuration.rs`, `tests/configuration_lives_in_the_store.rs`.
- Live reads: `systemctl --user is-active/show`, `/proc/<pid>/exe`, `ls` of runtime and state directories, `nix profile list`, `command -v`, `flow 'List.{}'`, `flow-next 'List.{}'`, `orchestrate 'Observe.Locks'`.
- Build log `home-build-regular.log`, `check-regular.log` (session scratchpad).

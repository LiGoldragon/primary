# Preparation custody handed to e60c75

The four exact preparation scopes were handed off successfully. This changes custody only; body, writer and allocation authorization remain separate.

## Positive identity and supported observations

`flow-meta-0.51 'Inspect.{ Mind versionZero Secondary }'` returned Awake.e60c75, Past[0bf458534808d05351], native01a1adb8-ec6e-7a40-ad9d-b55e60c756d8 and default/wS5:p1/term_65f8e9a5aecfaea. Registry origin remains Unbound; no bound process was invented.

Supported `herdr --session default pane process-info --pane wS5:p1` observed foregroundPID1801831 with actual Codex argv `--remote unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock ... resume 01a1adb8-ec6e-7a40-ad9d-b55e60c756d8`; `pane get` confirmed terminal, labels and working status. Kernel `/proc/1801831` supplied UID1001 and start token28707919. Supported `ResolvePeer.{ 1801831 1001 28707919 }` returned `PeerResolved.{ e60c75 Mind Medium gpt-6.1-sol }`. This is the actual native frontend, not the tool's app-server ancestor substituted as harness PID. No binding mutation occurred.

## Artifacts and exact scope

`custody-artifacts.json` records eight exact expected HEAD/tree pairs, clean tracked/untracked states, own .git, no alternates/hardlinked Git objects. Registry-source redb88/88 manifest entries passed, archive/manifest/license hashes match recorded bases. Protos exact commit/tree remains shallow with original incomplete-parent-history caveat. Every HEAD/tree/clean state and redb manifest was rechecked immediately before handoff. No source byte was changed.

Fresh old lock snapshot matched exact owners d05351, names, paths and reasons. Each supported release was followed once by acquisition of the identical name/paths/reason under e60c75, then an observed poststate. No failure, competitor, retry or takeover occurred.

| Old lock | New lock | Scope |
|---|---|---|
|25605|25611|Flow preparation|
|25607|25612|Sema/Engine/ordinary/meta dependency preparation|
|25608|25613|Registry-source redb preparation|
|25610|25614|Datom/Protos preparation|

Full old, release, acquisition and poststate receipts are in `handoff-receipts.json`, including final identity and artifact checks. Its SHA256 is db9c64e8e442e96e4a68b82ba8843b62a7201d4b2c2c77466888186ab17037da. Raw supported observations are `fresh-inspect.datom`, `herdr-process-info.json`, `herdr-pane.json`, `resolve-native-peer.txt`, and `custody-locks-observed.datom`.

Predecessor child native status remains UNKNOWN, not ended. Existing new reader recover_pins remains report-only; no implementation writer or independent final reviewer has been installed by this handoff.

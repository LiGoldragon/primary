# Fable recovery launch packet

This packet prepares exactly one medium-effort Psyche Fable successor of
`b7ba00`. It preserves the predecessor and creates no state until the native
batch launcher starts from a Herdr-managed pane.

The launcher validates the profile and every listed source hash, reserves a
new native UUID and an isolated Claude job directory, starts one remote-control
Claude agent, then accepts exactly one native bootstrap prompt. A failed start
is recorded in the state file; do not rerun it against that file.

Run this command only from the real managed default pane (`HERDR_ENV=1`), after
confirming that the default session still has workspace `w1`:

```sh
cd /home/li/wt/primary/56ae53 && node tools/native-batch-refresh.mjs start --manifest flows/56ae53/fable-recovery/launch-manifest.json --state flows/56ae53/fable-recovery/state.json
```

The state path is intentionally absent before launch. The command creates it
exclusively, so its existence means no second start may be attempted. After a
native-pending receipt, use the matching deployed Flow 0.16 Start/Bind path to
claim the successor's Flow identity and then verify Message binding, title,
and remote accessibility. The installed Flow client is 0.12.2 and is not that
path.

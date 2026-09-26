# Opus recovery launch packet

This packet prepares exactly one medium-effort Psyche Opus successor of
`e167d8`. It has no shared state with the Fable packet and creates no seat.

Run only after the managed Herdr shell path is available and the separate
Fable launch state has been judged:

```sh
cd /home/li/wt/primary/56ae53 && node tools/native-batch-refresh.mjs start --manifest flows/56ae53/opus-recovery/launch-manifest.json --state flows/56ae53/opus-recovery/state.json
```

`state.json` must be absent before the command. Its creation is the exclusive
launch reservation; do not retry a state that records an attempt.

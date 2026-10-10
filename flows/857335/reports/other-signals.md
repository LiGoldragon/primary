# Other signal consumers

## Terminal Cell v1.0.0

`terminal-cell` main is `e44c41a39866f645853364e85eff2f8e2256e722`. It ports the terminal control socket from retired `Input`/`Output` and `signal-frame` envelopes to named `Query`/`Response` values transported as length-prefixed `Signal<T>` archives. The receiver restores peer bytes; malformed archives map to invalid-data socket errors.

The twelve daemon witnesses cover control mode, attach-plane separation, PTY resize/capture/exit, input gates, prompt-pattern injection and dirty rejection, lifecycle snapshots/deltas, and replay. Full local targets passed.

## Harness v0.4.0

Harness main `722b68b3579b0235120ca098a0cddefa379d9945` replaces the terminal delivery frame exchange with length-prefixed `Signal<Query>` and `Signal<Response>` bytes. Its 21 spawned daemon/socket cases are runtime evidence; source-text truth checks are static policy only. The first explicit gate selection was invalid because it guessed absent `build`/`fmt`/`clippy` attributes (exit 1); the corrected build selected every declared current-system check and exited 0.

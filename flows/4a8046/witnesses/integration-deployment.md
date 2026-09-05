# Wispr-only integration and deployment witness

Date of observation: 2026-09-05.

## Outcome

The user-scoped Wispr-only deployment completed successfully as Lojix
deployment 198 (`Completed / Succeeded`, terminal event `5172`). It activates
consumer `a97e9efa1f5ccc3fa2d2b4c3f6cf9eac9fe8ee9b` and Home producer
`adc53c35650a8669373376c13f763a8f2be7b5b7`. It retains Codex 0.153.3; no
Codex update was deployed.

Both public mains were fast-forwarded after a fresh fetch showed their
expected bases: Home main moved from `a83210d3e0afd44fcdb9fa893fa582a22913146f`
to `adc53c35650a8669373376c13f763a8f2be7b5b7`, then consumer main moved from
`14a246f5b64c31d1208d9edd76f05acd9b4828b1` to
`a97e9efa1f5ccc3fa2d2b4c3f6cf9eac9fe8ee9b`. No peer revision was
overwritten.

## Delivered source and validation

The Home revision is derived from the existing 0.153.3 baseline. Its only
changes are the Wispr reconnect state handling in `WisprStatusState.luau` and
its state-behavior check, plus removal of the three retired VSCodium lock
nodes (`claude-code-vsix`, `codex-chatgpt-vsix`, and `visualjj-vsix`) already
absent from `flake.nix`. The Codex hash manifest is byte-identical to the
baseline and declares version `0.153.3`. It retains Wispr Flow provider
`033231a1255024447c6a4183c41f4ea9c1fa063f`.

The consumer changes only its locked Home input to that revision. Its
Lojix-projected target evaluation succeeded. The relevant immutable-source
checks completed successfully with the projected `system` and `horizon`
inputs, configured remote builders, `max-jobs 0`, and `fallback false`:

* `wispr-status-widget` —
  `/nix/store/g71nhyxashl11nakw3bl2849yh4pj2lr-wispr-status-widget`
* `wispr-status-niri-rule` —
  `/nix/store/9ms6g81y2kaj8y5nhq52gd1s877b5maf-wispr-status-niri-rule`
* `wispr-flow-profile-tier` —
  `/nix/store/1d56r52qcykpawvby7z4icrhvjhvpp7p`

## Live convergence after deployment 198

The ledger records deployment 198 for exactly the consumer source above. The
current Home generation changed from
`/nix/store/wc70jrsx59lc6z5kqjy4a6d6hrjp6j20-home-manager-generation` to
`/nix/store/2p1r0svfbfhwmlvxv6z6ch5ygrs4as04-home-manager-generation`.
The profile root is
`/nix/store/prs01bm2rkxfvggc4sdld4vz5rksirz1-profile`.

`codex-remote-control.service` is active/running with `NRestarts=0`. Its
0.153.3 store executable agrees with its sole main process, PID 4096266, and
that process owns
`/home/li/.codex/app-server-control/app-server-control.sock`. The profile
command reports `codex-cli 0.153.3`.

Live Wispr UI verification remains in progress. The verifier restarted Wispr
for the v2 sockets and reloaded Niri configuration after its initial receiver
fixture used an invalid title field. Noctalia is still a process started before
the Home activation, so it must be reloaded or restarted before the updated
widget can be observed. Orchestrate target lock 784 remains held through this
owned UI/audio cleanup.

## Superseded Codex 0.153.4 history

The earlier Codex 0.153.4 candidate remains preserved on pushed deferred
bookmarks: Home `fbceccc76dd9a161b79846c8c960788578a0bdf4` and consumer
`7a440b495003c60a8d32a23425390f18052280ec`. It was superseded by the user's
explicit scope change and is not deployed.

Its profile-only realization 196 was stopped by SIGTERM to the verified
flow-owned Nix client PID 4142873 only; its Nix daemon, remote-build, SSH,
and system services were not signalled. It terminated as
`Failed.(Build FlakeReferenceMalformed)`. Its pre-activation native request
197 was likewise stopped by SIGTERM to its verified evaluator PID 31949 only
and terminated as `Failed.(Eval FlakeReferenceMalformed)`. Neither changed
the live target; deployment 195 remained current until successful 198.

## Coordination and sources

The proposal was the existing regular file
`/git/github.com/LiGoldragon/goldragon/proposal.datom`; the target was
`UserEnvironment.li` on `goldragon/ouranos` over the configured direct
transport. The isolated Home and consumer integration worktrees were clean,
removed after landing, and their source locks 781 and 780 were released.

* `flows/4a8046/witnesses/activation-readiness.md`
* Lojix ledger queries for deployments 195–198
* Final immutable Home and consumer sources above

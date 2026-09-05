# Wispr control repair integration and deployment witness

Date of observation: 2026-09-05.

## Outcome

The current deployment is Lojix deployment 201: it was admitted at
`(5253 5253)`, reached `Completed / Succeeded` at terminal event `(5286 5286)`,
and its terminal ledger is `(5290 5290)`. It activates consumer
`a099bf95a7f6f998cb0e4801d5305a5ba4be6323`, Home producer
`3c08f1c749e94f5a4a03548b95d94c22df5cb210`, and the unchanged Wispr provider
`e97b9587a7186ad74c5d84b2da6abfb86645b68d` (`1.6.774+criomos.11`). The active
Home generation is
`/nix/store/jrfx55b6qlfcq5l7lpz2agnkg743r943-home-manager-generation`.

Deployment 201 changes only the local Wispr presentation mapping: valid RMS
uses bounded `sqrt(rms) * 3.0`, which raises quiet speech while preserving zero,
the existing unavailable reset, and the 450ms freshness reset. The installed
local plugin widget resolves to
`/nix/store/2p16jnk6vf7l8ksj7srcr83yd7a8hyza-hm_BarWidget.luau`; an authorized
Noctalia user-service restart followed by `noctalia msg config-reload` left
`criomos/wispr-status [local] 2.0.0 enabled`. Codex remains active at 0.153.3;
no Codex update was deployed.

Deployments 198–200 are historical evidence. Deployment 200 repaired meter
telemetry, and the user then directly confirmed that the `.11` waves move but
are too faint. Deployment 201 raises visual sensitivity for that already-moving level. All producer and consumer mains were fast-forwarded after fresh
fetches and no peer revision was overwritten.

## Historical deployment 198 source and validation

The initial Home revision was derived from the existing 0.153.3 baseline. Its
only
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
command reported `codex-cli 0.153.3`.

The later live acceptance of this initial deployment failed: the exact
control CLI returned `unavailable`, Meta+X did not toggle hands-free, and the
meter had no observed scalar movement. Those observations led to the repaired
provider below; they are not evidence of final acceptance. Target lock 784
remains held through the owned UI/audio cleanup.

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

## Historical deployment 199 control repair, gates, and runtime

The post-198 live acceptance exposed the deployed `.9` control ordering bug:
the exact current package archive returned the typed control reply
`ok:false,error:"unavailable"`. Its signed payload attempted optional bridge
registration before Electron readiness, when the bridge did not exist. This is
separate from the deferred Codex update; Codex remains 0.153.3.

Provider main now carries `c83e8d98178dec43d3119a2af1d2b6d17dfe4e49`, which
bumps Wispr to `1.6.774+criomos.10`, parks the real hands-free action during
its lexical initialization, and registers it when the bridge starts. The
cached original `.9` archive reproduced `unavailable`; the exact `.10` archive
then completed typed socket start and stop transitions. The provider's remote
gates are terminal and valid: status bootstrap
`/nix/store/khxcd7snf40hj8zij021x7abzr46r2qg-wispr-flow-status-bootstrap`
and linux-patches
`/nix/store/11yvi1blfl3kvwhx5xj7rwypv7rkdx2r-wispr-flow-linux-patches`
(46/46 Bats). The standalone remote-gate package output is
`/nix/store/2lzwmfyx4s168x4p00ck5p8c1qv2kiij-wispr-flow-1.6.774+criomos.10`.

Home main was fast-forwarded from `adc53c35650a8669373376c13f763a8f2be7b5b7`
to `0b5637635839558b4cbfb9b4d65021cf2481ee3a`; its immutable projected
`wispr-flow-profile-tier` gate is valid at
`/nix/store/kbjnpc918yp9fa4cwxbbyiqywf21hnjc-wispr-flow-profile-tier`.
Consumer main was then fast-forwarded from
`a97e9efa1f5ccc3fa2d2b4c3f6cf9eac9fe8ee9b` to
`30fe10e1d4287d6084845c3b5a0642abcd1175b1`. Each main moved forward after a
fresh fetch; no peer revision was overwritten.

The candidate's complete emitted Codex unit fields agree with the current
unit: description, `WantedBy=default.target`, `.153.3` ExecStart,
`Restart=always`, `RestartSec=2s`, `UMask=0077`, working directory
`/home/li/primary`, and empty environment/reload/restart triggers. The
consumer activation-package evaluation used the same immutable projected
system and horizon paths as the profile gate. Native `ActivateNow` deployment
199 was admitted as `DeployAccepted.(199 (5177 5177))` and reached `Completed
/ Succeeded` at terminal event `(5210 5210)`.

The final Home generation is
`/nix/store/47gqslp0x717dgjnmja36w4q6211i4zx-home-manager-generation`. Its
profile package `/nix/store/f4cfs1aws1sl1cl7l6yjv6348zm5y8gc-wispr-flow`
references the actually running provider
`/nix/store/rjr5m73a1djz05qjfs9wl55svzp2k07x-wispr-flow-1.6.774+criomos.10`.
After the normal Wispr service restart and Niri reload, Wispr Electron PID
166012 owns both v2 sockets and runs that `.10` path; the generated Meta+X
binding points to the same current-profile CLI. `codex-remote-control` remains
active as 0.153.3 with PID 4096266 and `NRestarts=0`. The live verifier now
completed the final UI/audio acceptance and restored the current RØDE AI-Micro
source 159 (volume 0.96), focus, and runtime state; no fixture files or
transient processes remain. The repaired control path passed: the exact CLI
returned `hands_free:true`, and a real Meta+X cycle held hands-free for more
than five seconds and stopped back to idle. The meter did not pass. With
stream 165 positively linked to loopback 75 and an 8.95-second synthetic
playback completed, v2 status remained `capture: unavailable, rms: null`; the
Wispr UI showed a red microphone and five static gray bars. Deployment 199 is
therefore successful and the control repair is accepted, while meter
acceptance remains an open concrete failure. Target lock 784 was released
after cleanup.

## Meter repair deployment 200

Provider main `e97b9587a7186ad74c5d84b2da6abfb86645b68d` is the immutable
`1.6.774+criomos.11` meter repair. It moves the v2 meter-object guard ahead
of the ordinary PCM decode in the packaged renderer handler. The prior `.10`
handler reproduced the live `TypeError: undefined is not iterable` at
`Array.from(e.data[0])`; the repaired packaged-handler test forwarded both
capture states, preserved ordinary PCM handling, and rejected the old guard
placement. The final provider gates passed: status bootstrap
`/nix/store/ja56q7dri7b7s4micg4033g91aja57qd-wispr-flow-status-bootstrap`
and linux patches
`/nix/store/caxb223z7517csyk747q7l8zwh5x4shr-wispr-flow-linux-patches`
(48/48 Bats).

Home main `3f58325f97aa11ef6f0b3dd475084603d126c38d` pins that provider and
consumer main `55a9fa7fadb103b8f2fbdda694403f9172c84f1e` pins Home. The
immutable projected profile check passed at
`/nix/store/ki1fzcaza9zgmj8fcrqxa1l24h0syaay-wispr-flow-profile-tier`.
Each producer was landed before its consumer, after a fresh fetch, without
overwriting peer work.

Native `ActivateNow` deployment 200 was admitted as
`DeployAccepted.(200 (5215 5215))` and reached `Completed / Succeeded` at
terminal event `(5248 5248)` (ledger `(5252 5252)`). The active Home
profile/current-home generation is
`/nix/store/l0wvbddw9h6473sd8nb3sascf4in20pc-home-manager-generation` and
its `wispr-flow` wrapper resolves to the repaired package
`/nix/store/drrrcy4vbli1yyw2ikfcf5xhm6cbrsq5-wispr-flow-1.6.774+criomos.11`.
Activation left the pre-existing `.10` Electron process running, so it was
terminated with a scoped graceful `SIGTERM` after exact executable identity
verification, then Wispr was launched in transient user scope
`wispr-flow-activation-200.scope`. The resulting main PID 209954 and both v2
sockets resolved to the exact `.11` executable. This was an ordinary app
restart only; no Nix, Lojix, SSH, or system service was stopped/restarted.
`codex-remote-control.service` remained active on its
`codex-0.153.3` ExecStart throughout.

The verifier's one bounded post-activation fixture did not reach recording:
a real ydotool Meta+X dispatch left v2 at `idle/hands_free:false` and created
no new input stream. It therefore performed no playback, reroute, screenshot,
or meter assertion. Cleanup completed: source 70 was unmuted at 0.94; the
user's default source 159 (RØDE AI-Micro, 0.96) remained unchanged; the
fixture daemon, socket, WAV, plan, and temporary files were removed; v2 ended
idle. Consequently deployment 200 and `.11` runtime convergence are proven,
but this fixture supplies neither a final live meter pass nor a meter failure. The user later directly confirmed that the `.11` Wispr waves do move, but are too faint during ordinary speech. That observation supersedes the incomplete ydotool result as the current live rendering outcome; the next scoped Home-only change adjusts visual sensitivity without changing capture truth, silence reset, or freshness.


## Visual sensitivity deployment 201

Home main `3c08f1c749e94f5a4a03548b95d94c22df5cb210` replaces the prior linear
`rms * 2.75` meter scale with `sqrt(rms) * 3.0` and contains a behavioral
low-RMS contract: rms `0.01` renders the center bar at 9px rather than the
idle 4px baseline. Existing checks retain clipped high-RMS behavior, exact
zero reset, unavailable reset, sequence handling, and the 450ms stale-sample
reset. The exact immutable widget gate passed at
`/nix/store/yaa1k1c5pqv01nf85a0kbdhy41xf5654-wispr-status-widget`; the
projected profile-tier gate passed at
`/nix/store/ki1fzcaza9zgmj8fcrqxa1l24h0syaay-wispr-flow-profile-tier`.

Consumer main `a099bf95a7f6f998cb0e4801d5305a5ba4be6323` pins that Home revision.
Native `ActivateNow` deployment 201 completed successfully as recorded above.
The final immutable widget file and enabled local plugin were verified after
Noctalia refresh. This confirms deployment and code loading, while avoiding a
new audio fixture; the user’s direct report remains the evidence that the
meter itself is moving.

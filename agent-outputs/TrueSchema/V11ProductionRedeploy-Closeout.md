# TrueSchema V11 production redeploy closeout

Status: deployed and verified.

## Target

- Session/Lane: TrueSchemaEvolution / TrueSchemaV11ProductionRedeploy.
- Target: cluster `goldragon`, node `ouranos`, user `li`.
- Shape/action: Lojix `UserEnvironment ActivateNow`.
- Source policy: `RequireImmutable`.
- Deploy ref: `github:LiGoldragon/CriomOS?rev=f0fed0b742a19ce3cd8a377570aa7338412294e8`.
- Proposal source: `/git/github.com/LiGoldragon/goldragon/datom.nota`.
- Builder/substituters: `None` / `[]`.

## Preflight evidence

- Local identity: user `li`, host `ouranos`.
- Lojix query for `goldragon/ouranos` showed current rollback generation after failed ref; latest rollback row was CriomOS rev `f428aa60df725802f92b6db7cbcdb0bb7125beca`; old failed row was `e29d87f919d446324749b0f4983a52dc4e38703b` and was not reused.
- `spirit "(Version)"` returned `(VersionReported 0.21.0)` before deploy.
- Current `spirit-daemon.service` was active; `ExecStartPre` exited successfully and most recent predeploy startup log showed `(Current (21 0))`.
- Socket entries existed in `/home/li/.local/state/spirit`: `spirit.sock` and `meta-spirit.sock`.
- CriomOS ref `f0fed0b742a19ce3cd8a377570aa7338412294e8` pins CriomOS-home `3e5854b4d492e91d0b309f4bf4a13a6247ec368e`.

## Pre-deploy data/rollback snapshot

State directory: `/home/li/.local/state/spirit`.

Live/archive at preflight:

- `spirit.sema`: size `987136`, sha256 `09a2773e790c9a7031561e2d0f5d27e5826501caaaa09ce35f2f767fb6e51443`.
- `spirit.archive.sema`: size `1617920`, sha256 `4d206a3da4bfde6d1cd2edb9cec9412d5a3de70143a7f62ca8131327125f26f4`.

Newest migration backups before this deploy:

- `spirit.schema-old-backup-12.sema`: size `5111808`, sha256 `8787530cbab67920872738e6bf96abfdc9bd9b6496063a06db261b026d255edf`.
- `spirit.archive.schema-old-backup-4.sema`: size `1732608`, sha256 `00743eaae60d497497f4c5c6ba800c4a7db4260eed4ee4102b92b09edeaed5ab`.

Existing explicit predeploy/probe backups:

- `spirit.sema.predeploy-v11-20260702T164051`: size `5111808`, sha256 `14812b26ef126ab6c6e02b8e6153f2f23f0f979012beecbe5bb4edadf6adb022`.
- `spirit.archive.sema.predeploy-v11-20260702T164051`: size `1732608`, sha256 `e90da73115aaa04cecb0b088aaae4a56ce90ab9c0c7a9219670064620b72cc4a`.
- `spirit.sema.pre-redeploy-backup`: size `3874816`, sha256 `b2dccafdd3cff1a3b4d2877776d337a6860096fd581ea8ac50a39a7a91d5b8f0`.

## Deployment result

- Submitted through current `meta-lojix` `Deploy (UserEnvironment ...)` interface.
- Admission result: `(DeployAccepted (48 (343 343)))`.
- Lojix row `48` reached `UserEnvironment LiveActivation Current` for immutable ref `f0fed0b742a19ce3cd8a377570aa7338412294e8`.
- Home profile moved from generation `850` to generation `851`.

## Verification

- `spirit "(Version)"` after activation returned `(VersionReported 0.23.0)`.
- `spirit "(Help Domain)"` returned a domain list beginning with `All`; `All` is present.
- `systemctl --user show spirit-daemon.service` reported `ActiveState=active`, `SubState=running`, `Result=success`, and `ExecStartPre` status `0`.
- Socket files after activation: `spirit.sock` and `meta-spirit.sock` under `/home/li/.local/state/spirit`.
- Recent `spirit-daemon.service` journal shows stop/start for activation and startup migration output `(Migrated (23 932))` before the daemon started.
- `systemctl --user is-active agent-daemon.service spirit-daemon.service` returned `active` for both units.

## Post-deploy data snapshot

Live/archive after migration:

- `spirit.sema`: size `999424`, sha256 `d4df2cdef182c1a44273bd73be7a77367988c52eda926d9e05ed9fc94ce8f946`.
- `spirit.archive.sema`: size `1622016`, sha256 `55b0aef8136a6eeab0f1e234003f8a5e16520fa26314667d8f44e163c65f4fe5`.

Newest migration backups created by this deploy:

- `spirit.schema-old-backup-13.sema`: size `987136`, sha256 `88a03b220888344bac9197fe1011844d50161d43b56acfffa6ca4a9acbf1ea00`.
- `spirit.archive.schema-old-backup-5.sema`: size `1617920`, sha256 `1a43d172a1ef899642f387f2d5f9a00cd2d486275166f8fb050c95d7a55fb0c5`.

## Rollback note

After this successful migration, generation rollback alone is insufficient for pre-v13/old Spirit. To run old Spirit, stop `spirit-daemon.service`, restore the newest live and archive migration backups (`spirit.schema-old-backup-13.sema` and `spirit.archive.schema-old-backup-5.sema`) over the live/archive paths, then start the old Spirit generation.

## Closeout status

- Deployment target claims were held through deployment and verification; release follows artifact finalization.
- Primary workspace had unrelated pre-existing uncommitted `agent-outputs/MindLiveJudgeEval` and `agent-outputs/PersistentSpiritMirror` files; this closeout file is the only file authored by this lane.

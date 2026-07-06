# TrueSchemaDomainAllProductionDeploy Recovery

## Scope
Production incident recovery for Session `TrueSchemaEvolution`, Lane `TrueSchemaDomainAllProductionDeploy` in Recovery mode.
Target: `goldragon / ouranos / li`; Lojix UserEnvironment deployment id `46` previously current/activated; Spirit user daemon failed.

## Coordination
- `meta-orchestrate "(Register ((TrueSchemaEvolution TrueSchemaDomainAllProductionDeploy ([operating-system-implementer] Structural) recovery-production-spirit-service) Recovery))"` returned `LaneAlreadyRegistered ... RecoveryInherited`.
- Initial broad claim including `/home/li/primary` rejected due unrelated lane claims.
- Exact artifact claim accepted:
  - `orchestrate "(Claim (TrueSchemaDomainAllProductionDeploy [(Path /home/li/primary/agent-outputs/TrueSchema/DomainAllProductionDeploy-Recovery.md)] production-recovery-closeout-artifact))"`

## Running log
Recovery started; non-destructive inspection first.
$ (cd /git/github.com/LiGoldragon/CriomOS && bd list --status open | head -60)

$ (cd /git/github.com/LiGoldragon/CriomOS-home && bd list --status open | head -60)

## Current Lojix and Spirit service inspection
$ lojix "(Query (ByNode (goldragon ouranos None)))"
(Queried ([(10 10 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (11 11 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (12 12 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (13 13 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (14 14 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (15 15 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (16 16 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (17 17 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (18 18 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (19 19 goldragon ouranos CompleteHost LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (2 2 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (20 20 goldragon ouranos CompleteHost LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (21 21 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (22 22 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (23 23 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (24 24 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (25 25 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (26 26 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (27 27 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (28 28 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (29 29 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (3 3 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (30 30 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (31 31 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (32 32 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (33 33 goldragon ouranos CompleteHost BootOnceProfile Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (34 34 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (35 35 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (36 36 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (37 37 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (39 39 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (4 4 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (40 40 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (41 41 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=dfe281772f194f25aae86005bd3f498b8f996e0b github:LiGoldragon/CriomOS/dfe281772f194f25aae86005bd3f498b8f996e0b?narHash=sha256-tetDLkgL3CB7OQrIsFtVuoVr/L/X3kDpy%2BdDOjQ68wY%3D dfe281772f194f25aae86005bd3f498b8f996e0b))) (42 42 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=e532486dbbdaf5d2b9446452176c073996828cce github:LiGoldragon/CriomOS/e532486dbbdaf5d2b9446452176c073996828cce?narHash=sha256-t1xbbKGaWClY1x5OBMECYKPQlivfafx8TpXb97ABPhk%3D e532486dbbdaf5d2b9446452176c073996828cce))) (43 43 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=437c4c7404bf5c25a9f528faac02168f3fd97f89 github:LiGoldragon/CriomOS/437c4c7404bf5c25a9f528faac02168f3fd97f89?narHash=sha256-%2BXrZ5zd6l0IQch7%2BuDQBbbynnrA1tO200pfjnA8Ux80%3D 437c4c7404bf5c25a9f528faac02168f3fd97f89))) (44 44 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=a9fa20425b354e2460fd036274a73867c841ff31 github:LiGoldragon/CriomOS/a9fa20425b354e2460fd036274a73867c841ff31?narHash=sha256-DdGG8zDB3MVbrAuqbNx6yWZKJprvpukdhzK4%2BykkdBs%3D a9fa20425b354e2460fd036274a73867c841ff31))) (45 45 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=f428aa60df725802f92b6db7cbcdb0bb7125beca github:LiGoldragon/CriomOS/f428aa60df725802f92b6db7cbcdb0bb7125beca?narHash=sha256-XnV9ScuPRPeNTBJMbXv0yr7sqx9v1kfTfnyECMiQ%2B0I%3D f428aa60df725802f92b6db7cbcdb0bb7125beca))) (46 46 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=e29d87f919d446324749b0f4983a52dc4e38703b github:LiGoldragon/CriomOS/e29d87f919d446324749b0f4983a52dc4e38703b?narHash=sha256-SEgbPJEz%2BwmhRj3vSH/3iJPudKVmJIYC5Kz6/WAVJ58%3D e29d87f919d446324749b0f4983a52dc4e38703b))) (5 5 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (6 6 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (7 7 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (8 8 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision []))) (9 9 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable legacy-lojix-0.3.10-store-row-without-source-revision legacy-lojix-0.3.10-store-row-without-source-revision [])))] (332 332)))

$ systemctl --user status spirit-daemon.service --no-pager --full
× spirit-daemon.service - Spirit schema-derived daemon
     Loaded: loaded (/home/li/.config/systemd/user/spirit-daemon.service; enabled; preset: ignored)
     Active: failed (Result: start-limit-hit) since Mon 2026-07-06 15:21:43 CEST; 6min ago
   Duration: 1d 1h 11min 17.003s
 Invocation: 9bf2616b222741aa96fe0098f5d034c5
    Process: 4100907 ExecStartPre=$NIX_STORE_PATH (code=exited, status=1/FAILURE)
   Mem peak: 2M
        CPU: 28ms

Jul 06 15:21:43 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 5.
Jul 06 15:21:43 ouranos systemd[3929]: spirit-daemon.service: Start request repeated too quickly.
Jul 06 15:21:43 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'start-limit-hit'.
Jul 06 15:21:43 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.

$ systemctl --user cat spirit-daemon.service
# /home/li/.config/systemd/user/spirit-daemon.service -> $NIX_STORE_PATH
[Install]
WantedBy=default.target

[Service]
Environment=PATH=/home/li/.nix-profile/bin:/run/current-system/sw/bin:/run/wrappers/bin
ExecStart=$NIX_STORE_PATH $NIX_STORE_PATH
ExecStartPre=$NIX_STORE_PATH
Restart=on-failure
RestartSec=2s

[Unit]
After=agent-daemon.service
Conflicts=persona-spirit-daemon.service
Conflicts=persona-spirit-daemon-v0.1.0.service
Conflicts=persona-spirit-daemon-v0.1.1.service
Conflicts=persona-spirit-daemon-v0.2.0.service
Conflicts=persona-spirit-daemon-v0.3.0.service
Conflicts=persona-spirit-daemon-v0.4.0.service
Conflicts=persona-spirit-daemon-v0.4.1.service
Conflicts=persona-spirit-daemon-v0.4.2.service
Conflicts=persona-spirit-daemon-v0.5.0.service
Conflicts=persona-spirit-daemon-v0.5.1.service
Conflicts=persona-spirit-daemon-v0.5.2.service
Conflicts=persona-spirit-daemon-next.service
Description=Spirit schema-derived daemon
StartLimitBurst=5
StartLimitIntervalSec=60
Wants=agent-daemon.service

$ systemctl --user show spirit-daemon.service -p Id -p LoadState -p ActiveState -p SubState -p Result -p ExecStartPre -p ExecStart -p Restart -p NRestarts -p FragmentPath
Id=spirit-daemon.service
LoadState=loaded
ActiveState=failed
SubState=failed
FragmentPath=/home/li/.config/systemd/user/spirit-daemon.service
Restart=on-failure
Result=start-limit-hit
NRestarts=5
ExecStartPre={ path=$NIX_STORE_PATH ; argv[]=$NIX_STORE_PATH ; ignore_errors=no ; start_time=[Mon 2026-07-06 15:21:41 CEST] ; stop_time=[Mon 2026-07-06 15:21:41 CEST] ; pid=4100907 ; code=exited ; status=1 }
ExecStart={ path=$NIX_STORE_PATH ; argv[]=$NIX_STORE_PATH $NIX_STORE_PATH ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }

$ journalctl --user-unit=spirit-daemon.service -b -n 220 --no-pager --output=short-iso
2026-07-02T23:58:07+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-02T23:58:07+02:00 ouranos 2rvz762i425bdksvjrvnl0g3na9vda9r-spirit-startup-state[3982]: (Current (21 0))
2026-07-02T23:58:07+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-03T01:01:36+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-03T01:01:36+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-03T01:01:36+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-03T01:01:36+02:00 ouranos 2rvz762i425bdksvjrvnl0g3na9vda9r-spirit-startup-state[109840]: (Current (21 0))
2026-07-03T01:01:36+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-03T16:12:33+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-03T16:12:33+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-03T16:12:33+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-03T16:12:33+02:00 ouranos pix34afwbxb1clkyflx6lzcvz9pihi4v-spirit-startup-state[850507]: (Current (20 0))
2026-07-03T16:12:33+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-03T16:18:12+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-03T16:18:12+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-03T16:18:12+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-03T16:18:12+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-04T01:49:16+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-04T01:49:16+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-04T01:49:17+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-04T01:49:17+02:00 ouranos pix34afwbxb1clkyflx6lzcvz9pihi4v-spirit-startup-state[1433109]: (Current (20 0))
2026-07-04T01:49:17+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-04T13:35:32+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-04T13:35:32+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-04T13:35:33+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-04T13:35:33+02:00 ouranos pix34afwbxb1clkyflx6lzcvz9pihi4v-spirit-startup-state[1624585]: (Current (20 0))
2026-07-04T13:35:33+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-05T14:10:14+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-05T14:10:14+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-05T14:10:14+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-05T14:10:14+02:00 ouranos fj793m1cc7yr1rqcxbn31vp9zsjn808z-spirit-startup-state[3008609]: (Current (20 0))
2026-07-05T14:10:14+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.
2026-07-06T15:21:31+02:00 ouranos systemd[3929]: Stopping Spirit schema-derived daemon...
2026-07-06T15:21:31+02:00 ouranos systemd[3929]: Stopped Spirit schema-derived daemon.
2026-07-06T15:21:32+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:32+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4098048]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:32+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:32+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:32+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:34+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 1.
2026-07-06T15:21:34+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:34+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4098687]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:34+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:34+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:34+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:36+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 2.
2026-07-06T15:21:36+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:36+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4099331]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:36+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:36+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:36+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 3.
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:38+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4100156]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 4.
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:41+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4100926]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 5.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: spirit-daemon.service: Start request repeated too quickly.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'start-limit-hit'.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.

## Store files and startup script inspection
$ readlink -f ~/.config/systemd/user/spirit-daemon.service && sed -n "1,240p" "$(readlink -f ~/.config/systemd/user/spirit-daemon.service)"
unit_path=$NIX_STORE_PATH
[Install]
WantedBy=default.target

[Service]
Environment=PATH=/home/li/.nix-profile/bin:/run/current-system/sw/bin:/run/wrappers/bin
ExecStart=$NIX_STORE_PATH $NIX_STORE_PATH
ExecStartPre=$NIX_STORE_PATH
Restart=on-failure
RestartSec=2s

[Unit]
After=agent-daemon.service
Conflicts=persona-spirit-daemon.service
Conflicts=persona-spirit-daemon-v0.1.0.service
Conflicts=persona-spirit-daemon-v0.1.1.service
Conflicts=persona-spirit-daemon-v0.2.0.service
Conflicts=persona-spirit-daemon-v0.3.0.service
Conflicts=persona-spirit-daemon-v0.4.0.service
Conflicts=persona-spirit-daemon-v0.4.1.service
Conflicts=persona-spirit-daemon-v0.4.2.service
Conflicts=persona-spirit-daemon-v0.5.0.service
Conflicts=persona-spirit-daemon-v0.5.1.service
Conflicts=persona-spirit-daemon-v0.5.2.service
Conflicts=persona-spirit-daemon-next.service
Description=Spirit schema-derived daemon
StartLimitBurst=5
StartLimitIntervalSec=60
Wants=agent-daemon.service

$ exec_start_pre=$(systemctl --user show -P ExecStartPre spirit-daemon.service); script=${exec_start_pre#path=}; script=${script%% ;*}; sed -n "1,220p" "$script"
script={ path=$NIX_STORE_PATH

$ find ~/.local/state/spirit -maxdepth 1 -printf "%f\t%y\t%s bytes\t%TY-%Tm-%Td %TH:%TM:%TS\n" | sort
spirit.archive.schema-old-backup-0.sema	f	311296 bytes	2026-06-16 13:41:23.4738409220
spirit.archive.schema-old-backup-1.sema	f	303104 bytes	2026-06-17 16:05:28.8318039990
spirit.archive.schema-old-backup-2.sema	f	143360 bytes	2026-06-20 15:20:32.6274243540
spirit.archive.schema-old-backup-3.sema	f	278528 bytes	2026-06-28 22:20:13.3695617180
spirit.archive.schema-old-backup-4.sema	f	1732608 bytes	2026-07-02 16:41:12.0649936880
spirit.archive.sema	f	1617920 bytes	2026-07-03 10:09:25.5738492100
spirit.archive.sema.gc-prebackup-zerocert-20260629T163121	f	356352 bytes	2026-06-29 16:30:53.8136819220
spirit.archive.sema.predeploy-20260628T183555	f	278528 bytes	2026-06-28 15:33:03.0512456840
spirit.archive.sema.predeploy-20260628T221924	f	278528 bytes	2026-06-28 15:33:03.0512456840
spirit.archive.sema.predeploy-v11-20260702T164051	f	1732608 bytes	2026-07-02 16:40:53.5352357770
spirit.archive.sema.preremoval-631-20260630T000025	f	774144 bytes	2026-06-29 16:31:58.2096064870
spirit.archive.sema.preremoval-o7zt-20260630T141137	f	1732608 bytes	2026-06-30 12:13:27.1156678050
spirit.config.rkyv	f	269 bytes	2026-06-13 10:07:18.8984486110
spirit	d	4096 bytes	2026-07-06 15:21:32.2459063110
spirit.guardian.sema	f	21499904 bytes	2026-06-12 15:57:35.7422862180
spirit.guardian.v2.sema	f	6295552 bytes	2026-06-12 17:01:28.3787851380
spirit.guardian.v3.sema	f	5705728 bytes	2026-06-15 10:12:28.4294399200
spirit.guardian.v4.sema	f	50204672 bytes	2026-06-28 17:50:23.8584894500
spirit.guardian.v5.sema	f	1085440 bytes	2026-07-06 15:07:45.1624100370
spirit.pre-0.12-recovery-20260613T100634+0200.sema	f	1355776 bytes	2026-06-13 09:59:13.7809939750
spirit.schema-1-backup-0.sema	f	1253376 bytes	2026-06-10 18:16:55.2490006220
spirit.schema-old-backup-0.sema	f	1212416 bytes	2026-06-10 18:36:37.7148785940
spirit.schema-old-backup-10.sema	f	3874816 bytes	2026-06-20 15:20:32.0630440240
spirit.schema-old-backup-11.sema	f	7163904 bytes	2026-06-28 22:20:11.4428161520
spirit.schema-old-backup-12.sema	f	5111808 bytes	2026-07-02 16:41:11.7551036030
spirit.schema-old-backup-1.sema	f	1208320 bytes	2026-06-10 19:56:58.5050655940
spirit.schema-old-backup-2.sema	f	1220608 bytes	2026-06-10 21:13:19.3158100120
spirit.schema-old-backup-3.sema	f	1224704 bytes	2026-06-11 11:21:05.2282783440
spirit.schema-old-backup-4.sema	f	1220608 bytes	2026-06-11 17:16:29.4061896790
spirit.schema-old-backup-5.sema	f	1355776 bytes	2026-06-13 10:06:49.9174230960
spirit.schema-old-backup-6.sema	f	3579904 bytes	2026-06-14 23:09:52.5372843040
spirit.schema-old-backup-7.sema	f	4050944 bytes	2026-06-15 10:15:06.6539438240
spirit.schema-old-backup-8.sema	f	4505600 bytes	2026-06-16 13:41:22.6194624880
spirit.schema-old-backup-9.sema	f	4882432 bytes	2026-06-17 16:05:28.2919665650
spirit.sema	f	987136 bytes	2026-07-06 15:21:41.1499390550
spirit.sema.gc-prebackup-zerocert-20260629T163121	f	5124096 bytes	2026-06-29 13:51:32.8898357700
spirit.sema.predeploy-20260628T183555	f	7163904 bytes	2026-06-28 17:50:23.8604894620
spirit.sema.predeploy-20260628T221924	f	7163904 bytes	2026-06-28 18:41:12.8715833350
spirit.sema.predeploy-v11-20260702T164051	f	5111808 bytes	2026-07-02 16:40:53.5321364520
spirit.sema.pre-redeploy-backup	f	3874816 bytes	2026-06-20 09:53:13.0677298910
spirit.sema.preremoval-631-20260630T000025	f	5124096 bytes	2026-06-29 18:18:16.7385171060
spirit.sema.preremoval-o7zt-20260630T141137	f	5111808 bytes	2026-06-30 12:53:05.2631312020

$ ls -l ~/.local/state/spirit
total 136068
-rw-r--r-- 1 li users   311296 Jun 16 13:41 spirit.archive.schema-old-backup-0.sema
-rw-r--r-- 1 li users   303104 Jun 17 16:05 spirit.archive.schema-old-backup-1.sema
-rw-r--r-- 1 li users   143360 Jun 20 15:20 spirit.archive.schema-old-backup-2.sema
-rw-r--r-- 1 li users   278528 Jun 28 22:20 spirit.archive.schema-old-backup-3.sema
-rw-r--r-- 1 li users  1732608 Jul  2 16:41 spirit.archive.schema-old-backup-4.sema
-rw-r--r-- 1 li users  1617920 Jul  3 10:09 spirit.archive.sema
-rw-r--r-- 1 li users   356352 Jun 29 16:30 spirit.archive.sema.gc-prebackup-zerocert-20260629T163121
-rw-r--r-- 1 li users   278528 Jun 28 15:33 spirit.archive.sema.predeploy-20260628T183555
-rw-r--r-- 1 li users   278528 Jun 28 15:33 spirit.archive.sema.predeploy-20260628T221924
-rw-r--r-- 1 li users  1732608 Jul  2 16:40 spirit.archive.sema.predeploy-v11-20260702T164051
-rw-r--r-- 1 li users   774144 Jun 29 16:31 spirit.archive.sema.preremoval-631-20260630T000025
-rw-r--r-- 1 li users  1732608 Jun 30 12:13 spirit.archive.sema.preremoval-o7zt-20260630T141137
-rw-r--r-- 1 li users      269 Jun 13 10:07 spirit.config.rkyv
-rw-r--r-- 1 li users 21499904 Jun 12 15:57 spirit.guardian.sema
-rw-r--r-- 1 li users  6295552 Jun 12 17:01 spirit.guardian.v2.sema
-rw-r--r-- 1 li users  5705728 Jun 15 10:12 spirit.guardian.v3.sema
-rw-r--r-- 1 li users 50204672 Jun 28 17:50 spirit.guardian.v4.sema
-rw-r--r-- 1 li users  1085440 Jul  6 15:07 spirit.guardian.v5.sema
-rw-r--r-- 1 li users  1355776 Jun 13 09:59 spirit.pre-0.12-recovery-20260613T100634+0200.sema
-rw-r--r-- 1 li users  1253376 Jun 10 18:16 spirit.schema-1-backup-0.sema
-rw-r--r-- 1 li users  1212416 Jun 10 18:36 spirit.schema-old-backup-0.sema
-rw-r--r-- 1 li users  3874816 Jun 20 15:20 spirit.schema-old-backup-10.sema
-rw-r--r-- 1 li users  7163904 Jun 28 22:20 spirit.schema-old-backup-11.sema
-rw-r--r-- 1 li users  5111808 Jul  2 16:41 spirit.schema-old-backup-12.sema
-rw-r--r-- 1 li users  1208320 Jun 10 19:56 spirit.schema-old-backup-1.sema
-rw-r--r-- 1 li users  1220608 Jun 10 21:13 spirit.schema-old-backup-2.sema
-rw-r--r-- 1 li users  1224704 Jun 11 11:21 spirit.schema-old-backup-3.sema
-rw-r--r-- 1 li users  1220608 Jun 11 17:16 spirit.schema-old-backup-4.sema
-rw-r--r-- 1 li users  1355776 Jun 13 10:06 spirit.schema-old-backup-5.sema
-rw-r--r-- 1 li users  3579904 Jun 14 23:09 spirit.schema-old-backup-6.sema
-rw-r--r-- 1 li users  4050944 Jun 15 10:15 spirit.schema-old-backup-7.sema
-rw-r--r-- 1 li users  4505600 Jun 16 13:41 spirit.schema-old-backup-8.sema
-rw-r--r-- 1 li users  4882432 Jun 17 16:05 spirit.schema-old-backup-9.sema
-rw-r--r-- 1 li users   987136 Jul  6 15:21 spirit.sema
-rw-r--r-- 1 li users  5124096 Jun 29 13:51 spirit.sema.gc-prebackup-zerocert-20260629T163121
-rw-r--r-- 1 li users  7163904 Jun 28 17:50 spirit.sema.predeploy-20260628T183555
-rw-r--r-- 1 li users  7163904 Jun 28 18:41 spirit.sema.predeploy-20260628T221924
-rw-r--r-- 1 li users  5111808 Jul  2 16:40 spirit.sema.predeploy-v11-20260702T164051
-rw-r--r-- 1 li users  3874816 Jun 20 09:53 spirit.sema.pre-redeploy-backup
-rw-r--r-- 1 li users  5124096 Jun 29 18:18 spirit.sema.preremoval-631-20260630T000025
-rw-r--r-- 1 li users  5111808 Jun 30 12:53 spirit.sema.preremoval-o7zt-20260630T141137

$ file ~/.local/state/spirit/*.sema 2>/dev/null
$ script=$(systemctl --user show -p ExecStartPre --value spirit-daemon.service | sed -n "s/.*path=\\([^ ;]*\\).*/\\1/p"); sed -n "1,220p" "$script"
script=$NIX_STORE_PATH
#!$NIX_STORE_PATH
set -eu

state_directory=/home/li/.local/state/spirit
database_path=/home/li/.local/state/spirit/spirit.sema

$NIX_STORE_PATH -p "$state_directory"
$NIX_STORE_PATH -f \
  /home/li/.local/state/spirit/spirit.sock \
  /home/li/.local/state/spirit/meta-spirit.sock

$NIX_STORE_PATH \
  "($database_path)"



$ start=$(systemctl --user show -p ExecStart --value spirit-daemon.service | sed -n "s/.*path=\\([^ ;]*\\).*/\\1/p"); "$start" --version || true
start=$NIX_STORE_PATH
spirit-daemon: daemon argument error: expected a signal-encoded file path

$ command -v spirit; spirit "(Version)"
/home/li/.nix-profile/bin/spirit
spirit: transport error: transport IO error: No such file or directory (os error 2)
$ find ~/.local/state/spirit/spirit -maxdepth 2 -printf "%p\t%y\t%s bytes\t%TY-%Tm-%Td %TH:%TM:%TS\n" | sort
$ ls -l /nix/var/nix/profiles/per-user/li | sed -n "1,160p"
ls: cannot access '/nix/var/nix/profiles/per-user/li': No such file or directory

$ readlink /nix/var/nix/profiles/per-user/li/home-manager-45-link; readlink /nix/var/nix/profiles/per-user/li/home-manager-46-link
$ ls -l /nix/var/nix/profiles/per-user 2>&1 | sed -n "1,120p"
total 4
drwxr-xr-x 2 root root 4096 Jul 10  2025 root

$ ls -l ~/.local/state/nix/profiles 2>&1 | sed -n "1,160p"
total 116
lrwxrwxrwx 1 li users 21 Jul  6 15:21 home-manager -> home-manager-849-link
lrwxrwxrwx 1 li users 67 Jun 28 18:41 home-manager-821-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jun 28 22:20 home-manager-822-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jun 29 16:21 home-manager-823-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jun 30 10:52 home-manager-824-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jun 30 12:44 home-manager-825-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  1 14:59 home-manager-826-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  1 15:27 home-manager-827-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  1 18:50 home-manager-828-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  1 19:23 home-manager-829-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  2 12:09 home-manager-830-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  2 14:15 home-manager-831-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  2 15:50 home-manager-832-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  2 16:06 home-manager-833-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  2 16:32 home-manager-834-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  2 16:42 home-manager-835-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  3 10:34 home-manager-836-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  3 16:12 home-manager-837-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  4 01:14 home-manager-838-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  4 13:35 home-manager-839-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  5 14:10 home-manager-840-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  5 14:14 home-manager-841-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  5 14:24 home-manager-842-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  5 15:54 home-manager-843-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  6 09:47 home-manager-844-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  6 10:41 home-manager-845-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  6 11:01 home-manager-846-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  6 11:12 home-manager-847-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  6 14:32 home-manager-848-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 67 Jul  6 15:21 home-manager-849-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 17 Jul  4 13:36 profile -> profile-1991-link
lrwxrwxrwx 1 li users 51 Jun 28 18:41 profile-1943-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 28 22:20 profile-1944-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 28 22:20 profile-1945-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 29 16:21 profile-1946-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 29 16:21 profile-1947-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 29 16:23 profile-1948-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 29 16:23 profile-1949-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 30 10:52 profile-1950-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 30 10:52 profile-1951-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 30 12:44 profile-1952-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jun 30 12:44 profile-1953-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 14:59 profile-1954-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 14:59 profile-1955-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 15:27 profile-1956-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 15:27 profile-1957-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 19:04 profile-1958-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 19:04 profile-1959-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 19:23 profile-1960-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 19:23 profile-1961-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 19:24 profile-1962-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  1 19:24 profile-1963-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 12:09 profile-1964-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 12:09 profile-1965-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 14:15 profile-1966-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 14:15 profile-1967-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 15:50 profile-1968-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 15:50 profile-1969-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:06 profile-1970-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:06 profile-1971-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:32 profile-1972-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:32 profile-1973-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:42 profile-1974-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:42 profile-1975-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:55 profile-1976-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 16:55 profile-1977-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 23:57 profile-1978-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  2 23:57 profile-1979-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  3 16:12 profile-1980-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  3 16:12 profile-1981-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  3 16:20 profile-1982-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  3 16:20 profile-1983-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 01:14 profile-1984-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 01:14 profile-1985-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 01:49 profile-1986-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 01:49 profile-1987-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 13:35 profile-1988-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 13:35 profile-1989-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 13:36 profile-1990-link -> $NIX_STORE_PATH
lrwxrwxrwx 1 li users 51 Jul  4 13:36 profile-1991-link -> $NIX_STORE_PATH
$ for gen in 848 849; do echo home-manager-$gen; find "$HOME/.local/state/nix/profiles/home-manager-$gen-link" -maxdepth 3 -path "*/spirit-daemon.service" -print; done
home-manager-848
home-manager-849

$ sed -n "1,80p" ~/.local/state/nix/profiles/home-manager-848-link/home-files/.config/systemd/user/spirit-daemon.service
[Install]
WantedBy=default.target

[Service]
Environment=PATH=/home/li/.nix-profile/bin:/run/current-system/sw/bin:/run/wrappers/bin
ExecStart=$NIX_STORE_PATH $NIX_STORE_PATH
ExecStartPre=$NIX_STORE_PATH
Restart=on-failure
RestartSec=2s

[Unit]
After=agent-daemon.service
Conflicts=persona-spirit-daemon.service
Conflicts=persona-spirit-daemon-v0.1.0.service
Conflicts=persona-spirit-daemon-v0.1.1.service
Conflicts=persona-spirit-daemon-v0.2.0.service
Conflicts=persona-spirit-daemon-v0.3.0.service
Conflicts=persona-spirit-daemon-v0.4.0.service
Conflicts=persona-spirit-daemon-v0.4.1.service
Conflicts=persona-spirit-daemon-v0.4.2.service
Conflicts=persona-spirit-daemon-v0.5.0.service
Conflicts=persona-spirit-daemon-v0.5.1.service
Conflicts=persona-spirit-daemon-v0.5.2.service
Conflicts=persona-spirit-daemon-next.service
Description=Spirit schema-derived daemon
StartLimitBurst=5
StartLimitIntervalSec=60
Wants=agent-daemon.service
$ old_pre=$(awk -F= "/^ExecStartPre=/{print \\$2}" ~/.local/state/nix/profiles/home-manager-848-link/home-files/.config/systemd/user/spirit-daemon.service); sed -n "1,220p" "$old_pre"
old_pre=$NIX_STORE_PATH
#!$NIX_STORE_PATH
set -eu

state_directory=/home/li/.local/state/spirit
database_path=/home/li/.local/state/spirit/spirit.sema

$NIX_STORE_PATH -p "$state_directory"
$NIX_STORE_PATH -f \
  /home/li/.local/state/spirit/spirit.sock \
  /home/li/.local/state/spirit/meta-spirit.sock

$NIX_STORE_PATH \
  "($database_path)"



$ old_start=$(awk -F= "/^ExecStart=/{print \\$2}" ... | awk "{print \\$1}"); "$old_start" --version || true
old_start=$NIX_STORE_PATH
spirit-daemon: daemon argument error: expected a signal-encoded file path
$ ls -l ~/.local/state/nix/profiles/home-manager-848-link/{home-path,home-files}/ 2>&1 | sed -n "1,120p"
lrwxrwxrwx 2 root root 62 Jan  1  1970 /home/li/.local/state/nix/profiles/home-manager-848-link/home-files -> $NIX_STORE_PATH
lrwxrwxrwx 6 root root 61 Jan  1  1970 /home/li/.local/state/nix/profiles/home-manager-848-link/home-path -> $NIX_STORE_PATH

$ readlink -f ~/.local/state/nix/profiles/home-manager-848-link/home-path/bin/spirit
$NIX_STORE_PATH
$ sed -n "1,80p" "$(readlink -f ~/.local/state/nix/profiles/home-manager-848-link/home-path/bin/spirit)"
#!$NIX_STORE_PATH
export SPIRIT_SOCKET=/home/li/.local/state/spirit/spirit.sock
exec $NIX_STORE_PATH "$@"

$ spirit --help | sed -n "1,120p"
spirit: invalid NOTA input: unknown Input variant --help

## Readability probes on copied stores
$ old_migrate=$(awk "/spirit-migrate-store/ {print \\$1}" "$old_pre"); run old migrator on copies of current and latest named v11/predeploy stores
old_migrate=$NIX_STORE_PATH
## copied current (987136 bytes 2026-07-06 15:21:41.149939055 +0200)
(Current (21 0))
## copied predeploy-v11 (5111808 bytes 2026-07-02 16:40:53.532136452 +0200)
(Migrated (21 932))
## copied schema-old-backup-12 (5111808 bytes 2026-07-02 16:41:11.755103603 +0200)
(Migrated (21 932))
## copied archive-current (1617920 bytes 2026-07-03 10:09:25.573849210 +0200)
(Current (1494 0))
## copied archive-predeploy-v11 (1732608 bytes 2026-07-02 16:40:53.535235777 +0200)
spirit-migrate-store: migrated spirit store: referent name is not lowercase kebab-case: CriomOS
## copied archive-schema-old-backup-4 (1732608 bytes 2026-07-02 16:41:12.064993688 +0200)
spirit-migrate-store: migrated spirit store: referent name is not lowercase kebab-case: CriomOS

## Recovery decision
Root cause is target migration binary rejecting schema 11 (`spirit-migrate-store: unrecognized spirit store schema version: 11`). The existing live `spirit.sema` and archive sibling are still readable by the previous v11 migrator on copied files. Fix-forward would require implementing and validating schema-11-to-13 migration; rollback to the previous immutable CriomOS ref is the minimal safe production restore and does not require overwriting the live store.

Target cluster/node/user: `goldragon / ouranos / li`.
Deployment shape/action: `UserEnvironment ActivateNow`.
Source revision policy: `RequireImmutable`.
Rollback source: `github:LiGoldragon/CriomOS?rev=f428aa60df725802f92b6db7cbcdb0bb7125beca` (previous current Lojix generation 45).
Builder/substituters: `None` / `[]`.
Data expectation: do not copy backups unless old daemon cannot read the current v11 live store; the copied-store probe showed it can.

## Rollback deploy
$ meta-lojix "(Deploy (UserEnvironment (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS?rev=f428aa60df725802f92b6db7cbcdb0bb7125beca ActivateNow RequireImmutable None [])))"
(DeployAccepted (47 (332 332)))

## Rollback status polling
poll 1: 2026-07-06T15:38:11+02:00
poll 2: 2026-07-06T15:38:16+02:00
poll 3: 2026-07-06T15:38:21+02:00
poll 4: 2026-07-06T15:38:26+02:00
poll 5: 2026-07-06T15:38:31+02:00
poll 6: 2026-07-06T15:38:36+02:00
poll 7: 2026-07-06T15:38:41+02:00
poll 8: 2026-07-06T15:38:46+02:00
poll 9: 2026-07-06T15:38:52+02:00
poll 10: 2026-07-06T15:38:57+02:00
poll 11: 2026-07-06T15:39:02+02:00
poll 12: 2026-07-06T15:39:07+02:00
poll 13: 2026-07-06T15:39:12+02:00
poll 14: 2026-07-06T15:39:17+02:00
poll 15: 2026-07-06T15:39:22+02:00
poll 16: 2026-07-06T15:39:27+02:00
poll 17: 2026-07-06T15:39:32+02:00
poll 18: 2026-07-06T15:39:37+02:00
poll 19: 2026-07-06T15:39:42+02:00
poll 20: 2026-07-06T15:39:47+02:00
poll 21: 2026-07-06T15:39:52+02:00
poll 22: 2026-07-06T15:39:57+02:00
poll 23: 2026-07-06T15:40:02+02:00
poll 24: 2026-07-06T15:40:08+02:00
(47 47 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=f428aa60df725802f92b6db7cbcdb0bb7125beca github:LiGoldragon/CriomOS/f428aa60df725802f92b6db7cbcdb0bb7125beca?narHash=sha256-XnV9ScuPRPeNTBJMbXv0yr7sqx9v1kfTfnyECMiQ%2B0I%3D f428aa60df725802f92b6db7cbcdb0bb7125beca)

## Post-rollback service verification and restart if needed
$ systemctl --user status spirit-daemon.service --no-pager --full
● spirit-daemon.service - Spirit schema-derived daemon
     Loaded: loaded (/home/li/.config/systemd/user/spirit-daemon.service; enabled; preset: ignored)
     Active: active (running) since Mon 2026-07-06 15:39:54 CEST; 28s ago
 Invocation: 2bc205bef4a34cf596a511418d74d272
    Process: 4120931 ExecStartPre=$NIX_STORE_PATH (code=exited, status=0/SUCCESS)
   Main PID: 4120942 (spirit-daemon)
      Tasks: 15 (limit: 37854)
     Memory: 1.9M (peak: 4.8M)
        CPU: 54ms
     CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/spirit-daemon.service
             └─4120942 $NIX_STORE_PATH $NIX_STORE_PATH

Jul 06 15:39:54 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
Jul 06 15:39:54 ouranos fj793m1cc7yr1rqcxbn31vp9zsjn808z-spirit-startup-state[4120940]: (Current (21 0))
Jul 06 15:39:54 ouranos systemd[3929]: Started Spirit schema-derived daemon.

$ test -S ~/.local/state/spirit/spirit.sock && echo socket-present || echo socket-missing
socket-present

$ spirit "(Version)"
(VersionReported 0.21.0)

$ systemctl --user show spirit-daemon.service -p ActiveState -p SubState -p Result -p ExecStartPre -p ExecMainPID
ActiveState=active
SubState=running
Result=success
ExecMainPID=4120942
ExecStartPre={ path=$NIX_STORE_PATH ; argv[]=$NIX_STORE_PATH ; ignore_errors=no ; start_time=[Mon 2026-07-06 15:39:54 CEST] ; stop_time=[Mon 2026-07-06 15:39:54 CEST] ; pid=4120931 ; code=exited ; status=0 }

$ journalctl --user-unit=spirit-daemon.service -b -n 20 --no-pager --output=short-iso
2026-07-06T15:21:36+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 3.
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:38+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4100156]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:38+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 4.
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:21:41+02:00 ouranos ynhfxp8pjsv4as73nn9jmmsprvwxbw2z-spirit-startup-state[4100926]: spirit-migrate-store: unrecognized spirit store schema version: 11
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: spirit-daemon.service: Control process exited, code=exited, status=1/FAILURE
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'exit-code'.
2026-07-06T15:21:41+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: spirit-daemon.service: Scheduled restart job, restart counter is at 5.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: spirit-daemon.service: Start request repeated too quickly.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: spirit-daemon.service: Failed with result 'start-limit-hit'.
2026-07-06T15:21:43+02:00 ouranos systemd[3929]: Failed to start Spirit schema-derived daemon.
2026-07-06T15:39:54+02:00 ouranos systemd[3929]: Starting Spirit schema-derived daemon...
2026-07-06T15:39:54+02:00 ouranos fj793m1cc7yr1rqcxbn31vp9zsjn808z-spirit-startup-state[4120940]: (Current (21 0))
2026-07-06T15:39:54+02:00 ouranos systemd[3929]: Started Spirit schema-derived daemon.

$ lojix "(Query (ByNode (goldragon ouranos None)))" | grep deployment 47
(47 47 goldragon ouranos UserEnvironment LiveActivation Current $NIX_STORE_PATH (Some (RequireImmutable github:LiGoldragon/CriomOS?rev=f428aa60df725802f92b6db7cbcdb0bb7125beca github:LiGoldragon/CriomOS/f428aa60df725802f92b6db7cbcdb0bb7125beca?narHash=sha256-XnV9ScuPRPeNTBJMbXv0yr7sqx9v1kfTfnyECMiQ%2B0I%3D f428aa60df725802f92b6db7cbcdb0bb7125beca)

## Source evidence for fix-forward blocker
The deployed failing ref pins Spirit rev `eaab51304e30500e3a5e1e022ac7f0475843e754` (local checkout `/git/github.com/LiGoldragon/spirit-trueschema` has that commit as `spirit: adopt Domain::All runtime and v12 store migration`). Its `src/production_migration.rs` declares schema 13 current and a v12 previous reader, but no v11 previous reader; production's live store was schema 11.

Commands inspected:
- `grep -n "SPIRIT_STORE_V.*SCHEMA_VERSION\|SPIRIT_SCHEMA_VERSION" /git/github.com/LiGoldragon/spirit-trueschema/src/{production_migration.rs,store/mod.rs}`
- `sed -n '2800,2858p' /git/github.com/LiGoldragon/spirit-trueschema/src/production_migration.rs`

Conclusion: fix-forward needs a real schema-11-to-13 migration and production-copy validation, not a service/env tweak.

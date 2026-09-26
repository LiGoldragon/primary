# Branch inventory — deploy-path repositories (da88cf)

Scanned 2026-09-25 read-only. Branch list from `git ls-remote --heads` on the real remote; ahead/behind = `git rev-list --left-right --count <remote-main>...<head>` computed on the local canonical clone, only when both objects are present locally (never fetched). Classes: merged-not-deleted (ahead 0); unmerged-small (≤5 ahead); unmerged-large; `stale(Nd)` appended when unmerged and last commit >14 days old; `hotfix-or-pin-like` appended by name/subject match (pin, fix, hotfix, revert, usb-bus). `herdr` has no canonical checkout (only packaged in CriomOS-home); `Message` is the lowercase `message` repository.

## CriomOS

Remote: `ssh://git@github.com/LiGoldragon/CriomOS`; base: remote main d193bafca (present locally); heads: 84

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| FinalWisprHomePin | 1c0f7ef34 | 0/71 | 2026-09-04 | li | Advance Home Wispr provider to 1.6.774+criomos.3 | merged-not-deleted, hotfix-or-pin-like |
| IntelWifiGeolocationStabilizationOs | 2368fe955 | 2/333 | 2026-07-17 | li | CriomOS: use builder-compatible home input | unmerged-small, stale(70d) |
| LandDeployWisprStatus | 173589dae | 1/74 | 2026-09-04 | li | Pin CriomOS Home Wispr status consumer | unmerged-small, stale(21d), hotfix-or-pin-like |
| LandDeployWisprStatusFix | 9067535f9 | 2/74 | 2026-09-04 | li | Advance Home Wispr status provider | unmerged-small, stale(21d) |
| ListenerHistoryRetentionDeployment | 572f4d703 | 0/356 | 2026-07-15 | li | CriomOS: deploy bounded Listener history (GPT-5 direct) | merged-not-deleted |
| NormalizeHomeImmutableLock | edabfa914 | 1/73 | 2026-09-04 | li | Normalize Home immutable lock | unmerged-small, stale(21d) |
| RegistryMaintenanceDeployment | daa71cef7 | 0/308 | 2026-07-19 | li | criomos: deploy current Orchestrate daemon | merged-not-deleted |
| WisprStatus4 | d869176d8 | 0/70 | 2026-09-04 | li | Advance Home Wispr provider to 1.6.774+criomos.4 | merged-not-deleted |
| ZeusBirdLedgerCriomOS | 059af0ab2 | 3/346 | 2026-07-16 | li | CriomOS: advance home repair and spirit migration | unmerged-small, stale(71d) |
| bluetooth-microphone-reliability-pin | dcc3cf90a | 1/395 | 2026-07-10 | li | CriomOS: pin Bluetooth microphone home policy | unmerged-small, stale(77d), hotfix-or-pin-like |
| bounded-state-production-os | 1a318380d | 1/352 | 2026-07-16 | li | CriomOS: pin bounded-state component closure (GPT-5.6; medium) | unmerged-small, stale(72d), hotfix-or-pin-like |
| cloud-designer-cloud-node-image | d25ae5fa1 | 3/470 | 2026-06-20 | li | CriomOS: cloud-node.nix cleanups (audit 75) — drop redundant grub/firewall/netwo | unmerged-small, stale(97d) |
| cloud-designer-web-host-epic | 12f61415a | 4/464 | 2026-06-22 | li | web-host: add missing Zola template to test fixture (render was broken) | unmerged-small, stale(95d) |
| consumer-wispr-control-pin-4a8046 | 30fe10e1d | 0/59 | 2026-09-05 | li | Pin repaired Wispr control Home revision | merged-not-deleted, hotfix-or-pin-like |
| consumer-wispr-meter-pin-4a8046 | 55a9fa7fa | 0/58 | 2026-09-05 | li | Pin Wispr meter Home revision | merged-not-deleted, hotfix-or-pin-like |
| core-checkup-criomos-cf7879 | 8c63087c5 | 2/22 | 2026-09-15 | li | Use string type for projected roster path | unmerged-small |
| criome-auth-integration | bf30751f6 | 0/458 | 2026-06-28 | li | CriomOS: integrate criome (T2) + persona-router (T3) modules | merged-not-deleted |
| criome-service-module | 304ba0a22 | 0/460 | 2026-06-28 | li | CriomOS: criome daemon NixOS service module + single-node witness test (T2) | merged-not-deleted |
| criomos-pi-subagents-training | 32133a92a | 0/335 | 2026-07-17 | li | CriomOS: pin compact async Pi home policy (Terra; high) | merged-not-deleted, hotfix-or-pin-like |
| criomos-update-2026-07-08 | df154b6b2 | 6/396 | 2026-07-09 | li | CriomOS: repin home mentci recovery | unmerged-large, stale(78d), hotfix-or-pin-like |
| disable-claude-workflows | 1a7a7635f | 1/316 | 2026-07-18 | li | criomos: pin Claude workflow home configuration (operating-system-implementer; s | unmerged-small, stale(69d), hotfix-or-pin-like |
| disk-retention-2e28d8 | 107adcb76 | 1/43 | 2026-09-10 | li | CriomOS: collect old Nix profiles daily | unmerged-small, stale(16d) |
| disk-retention-integration-2e28d8 | 11d41d7e7 | 0/38 | 2026-09-10 | li | CriomOS: collect old Nix profiles daily | merged-not-deleted |
| enable-vm-hosting-prometheus | ec198d46f | 3/483 | 2026-06-19 | li | CriomOS: test-vm-host route prefix is family-aware (/128 for IPv6 guest IP, /32  | unmerged-small, stale(98d) |
| f6db8d-lojix-start | c4c830c10 | 0/31 | 2026-09-11 | li | Start the Lojix Nexus CriomOS pins | merged-not-deleted, hotfix-or-pin-like |
| f6db8d-remote-only-builds | dbf2daaf4 | 1/32 | 2026-09-12 | li | nix: max-jobs=0 for non-builder hosts (goldragon); keep trusted-users, builders- | unmerged-small |
| field-astra-5f38bc-flow-pins | 88900f266 | 12/3 | 2026-09-24 | li | Pin Herdr Codex next-home integration | unmerged-large, hotfix-or-pin-like |
| field-usb-ygg-ndp-9ddcbc | 73ba25c85 | 0/9 | 2026-09-23 | li | Preserve USB Yggdrasil neighbour discovery | merged-not-deleted |
| field-wifi-wan-recovery-753e69 | 114fcbd10 | 0/13 | 2026-09-21 | li | Recover router WAN DHCP after late upstream availability | merged-not-deleted |
| field/flow-message-deploy-eb7bae | 90702b6e9 | 1/6 | 2026-09-24 | li | Pin green Flow and Message Home packet | unmerged-small, hotfix-or-pin-like |
| flow-final-aba74675-luna6 | 203273f58 | 13/3 | 2026-09-25 | li | Pin managed Home profile to final Flow release | unmerged-large, hotfix-or-pin-like |
| flow-main-opencode-luna6 | c0b02d8af | 14/3 | 2026-09-25 | li | Pin managed Home to Flow main and OpenCode release | unmerged-large, hotfix-or-pin-like |
| flow07-ouranos-b7da5d | 58b4c6b98 | 15/3 | 2026-09-25 | li | criomos: pin Flow 0.7 Home consumer | unmerged-large, hotfix-or-pin-like |
| horizon-driven-intercom | 5d3c04223 | 3/306 | 2026-07-20 | li | CriomOS: authorize Agent Intercom tunnel identities | unmerged-small, stale(67d) |
| horizon-flake-integration-542442 | de02ef17a | 15/54 | 2026-09-06 | li | CriomOS: consume Clavifaber Datom publication producer | unmerged-large, stale(19d) |
| horizon-module-consumer-fix-542442 | 8bbc75d3f | 4/54 | 2026-09-06 | li | CriomOS: read projected disk and VM host fields | unmerged-small, stale(20d), hotfix-or-pin-like |
| horizon-module-migration-542442 | 9be86763a | 2/54 | 2026-09-05 | li | CriomOS: test typed VM testing capability | unmerged-small, stale(20d) |
| horizon-test-vm | 42bc62b30 | 6/547 | 2026-06-16 | li | test-substrate: prose matches code — vmTypeModule is NOT composed on the hermeti | unmerged-large, stale(101d) |
| integration-deployment-4a8046 | 7a440b495 | 2/61 | 2026-09-05 | li | Pin finalized Home activation revision | unmerged-small, stale(20d), hotfix-or-pin-like |
| integration-deployment-4a8046-wispr | a97e9efa1 | 0/60 | 2026-09-05 | li | Pin Wispr-only Home activation revision | merged-not-deleted, hotfix-or-pin-like |
| listener080recovery | 736bb5a69 | 1/369 | 2026-07-11 | li | CriomOS (GPT-5; recovery): pin Listener 0.8.0 home input | unmerged-small, stale(76d), hotfix-or-pin-like |
| no-baked-test-defaults | 92c45b582 | 0/436 | 2026-07-03 | li | CriomOS: production lojix daemon carries no baked test-op fixture | merged-not-deleted |
| orchestrateRedeploy | f981c6d99 | 1/291 | 2026-07-26 | li | criomos: hand orchestrate ownership to CriomOS-home | unmerged-small, stale(61d) |
| persona-router-module | a99a3488b | 0/460 | 2026-06-28 | li | persona-router: NixOS service module + role-policy witness | merged-not-deleted |
| pi-child-intercom-injection-os | d5b9749e5 | 2/381 | 2026-07-10 | li | CriomOS: pin packaged Pi extension recovery (GPT-5.6-sol high) | unmerged-small, stale(77d), hotfix-or-pin-like |
| pi-operator-web-host-testing | 297d7e0f3 | 3/464 | 2026-06-22 | li | CriomOS: add WebHost fixture template witness | unmerged-small, stale(95d) |
| pi-subagents-fork-home-pin | 731d5bed9 | 0/370 | 2026-07-10 | li | CriomOS: pin maintained pi-subagents fork home revision (generalist; source-guid | merged-not-deleted, hotfix-or-pin-like |
| pi-subagents-home-consumer-pin | b48ab57e6 | 0/350 | 2026-07-16 | li | CriomOS: pin approved CriomOS-home forward-port (gpt-5.6; source-guided) | merged-not-deleted, hotfix-or-pin-like |
| pi-subagents-managed-deployment | 7f7a8308b | 0/345 | 2026-07-16 | li | CriomOS: pin managed pi-subagents home profile (Pi operating-system-implementer; | merged-not-deleted, hotfix-or-pin-like |
| primary-2v5c.15-criomos-spirit | e29d87f91 | 1/416 | 2026-07-06 | li | spirit: pin Domain All stack and pre-start migration | unmerged-small, stale(81d), hotfix-or-pin-like |
| primary-2v5c.19-criomos-spirit-v11 | f0fed0b74 | 2/416 | 2026-07-06 | li | CriomOS: pin fixed Spirit v11 migration stack | unmerged-small, stale(81d), hotfix-or-pin-like |
| primary-99n-criomos | 98bc81475 | 0/129 | 2026-08-28 | li | Move graphical portal selection to Edge | merged-not-deleted |
| prometheus-usb-bus-property-5f38bc | da85c4a9e | 13/3 | 2026-09-24 | li | Bind USB downlinks by stable udev bus role | unmerged-large, hotfix-or-pin-like |
| prometheus-usb-downlink-5f38bc | de5ac1b79 | 1/3 | 2026-09-24 | li | Bind declared USB LAN hardware to router bridge | unmerged-small |
| proposal/348e7b-core-checkup-consumer | eb614bf96 | 12/22 | 2026-09-16 | li | Fix duplicate Home wrapper import | unmerged-large |
| proposal/348e7b-heartbeat-consumer | 7f9f7be2a | 13/22 | 2026-09-16 | li | Enable bounded heartbeat with observed cluster lane paths | unmerged-large |
| proposal/348e7b-prometheus-single-model | 9d93d6218 | 65/22 | 2026-09-16 | li | Pin primary Qwen-only LargeAi catalog for Prometheus deployment | unmerged-large, hotfix-or-pin-like |
| proposal/348e7b-prosody-activation | 38c5bd51e | 64/22 | 2026-09-16 | li | Map Prosody credentials to materialized SOPS keys | unmerged-large |
| proposal/5f4fea-model-presets | 0cb51527f | 2/22 | 2026-09-15 | li | Record bounded module evaluation for model proposal | unmerged-small |
| proposal/6852f4-message-flow-consumer | 67315859c | 4/22 | 2026-09-17 | li | Update Lojix Home revision assertion for Message Flow candidate | unmerged-small |
| proposal/cf7879-core-checkup-criomos | 8276eab23 | 6/22 | 2026-09-15 | li | Publish immutable Core Checkup roster artifact | unmerged-large |
| proposal/prometheus-service-provider-poc | e7f2ab71e | 51/22 | 2026-09-16 | li | Record bounded Prometheus VM test receipt | unmerged-large |
| push-nunnpqxsnpyk | 4e0155cef | 3/225 | 2026-08-10 | li | CriomOS: enable Lojix on PersonaDevelopment hosts | unmerged-small, stale(46d) |
| push-ptyxoyrumuxu | f0d90e513 | 6/225 | 2026-08-10 | li | CriomOS: pin rejected-deploy wire fix | unmerged-large, stale(46d), hotfix-or-pin-like |
| push-qsnppzslsszr | 1ec9a8783 | 2/225 | 2026-08-09 | li | CriomOS: pin current CriomOS-home before deployment | unmerged-small, stale(47d), hotfix-or-pin-like |
| push-wvnpprzzxqrn | 2fb323b0f | 0/135 | 2026-08-27 | li | CriomOS: pin collision-free Codex Home release | merged-not-deleted, hotfix-or-pin-like |
| push-zzquoxwosqqw | 72bdf77e1 | 1/225 | 2026-08-09 | li | CriomOS: make NordVPN NetworkManager profiles native and current | unmerged-small, stale(47d) |
| remove-lojix-timeout-consumer | a4322cd14 | 0/156 | 2026-08-23 | li | lojix: remove effect timeout configuration | merged-not-deleted |
| repair-pi-package-and-activate-pin | cc914b12d | 2/395 | 2026-07-10 | li | CriomOS: synchronize pinned Home transitive inputs (operating-system-implementer | unmerged-small, stale(77d), hotfix-or-pin-like |
| restore-orchestrate-system-pin | eb48e20a0 | 0/366 | 2026-07-11 | li | CriomOS: pin repaired Orchestrate home runtime | merged-not-deleted, hotfix-or-pin-like |
| solar-location-chroma-os-pin | a27b2f9fb | 3/348 | 2026-07-16 | li | CriomOS: pin Chroma solar reconciliation home (gpt-5.6-terra; high) | unmerged-small, stale(71d), hotfix-or-pin-like |
| solar-location-repair-os | c448fc8f3 | 2/348 | 2026-07-16 | li | CriomOS: synchronize criomos-home lock identity (operating-system-implementer; s | unmerged-small, stale(71d) |
| solar-time-status-bar-criomos | 1ab350501 | 3/348 | 2026-07-16 | li | CriomOS: pin solar clock tooltip fix (gpt-5.6-terra; high) | unmerged-small, stale(71d), hotfix-or-pin-like |
| spirit-judge-source-ready-deploy-20260710 | aef97cbc3 | 9/369 | 2026-07-11 | li | CriomOS: materialize validated judge pin graph (gpt-5.6; source-guided) | unmerged-large, stale(76d), hotfix-or-pin-like |
| spirit-single-root-integration | e658bf55b | 0/249 | 2026-08-03 | li | CriomOS: pin maintained Spirit 0.25.1 release root | merged-not-deleted, hotfix-or-pin-like |
| test/laptop-colemak-keyd | 7ba01aea6 | 1/447 | 2026-07-02 | li | CriomOS: refresh laptop Colemak test home input | unmerged-small, stale(85d) |
| usb-gateway-consumer-6db4fe | 9842f51a8 | 1/14 | 2026-09-21 | li | CriomOS: add source-only USB IPv4 gateway consumer and policy check | unmerged-small |
| vm-guest-networking | 658b20849 | 1/443 | 2026-07-03 | li | CriomOS: make same-host TestVm guests network-reachable (guest tap binding + hos | unmerged-small, stale(85d) |
| wispr-keyboard-uaccess | de309b676 | 0/121 | 2026-08-30 | li | Grant active seat keyboard event access | merged-not-deleted |
| wispr-meter-visibility-4a8046 | a099bf95a | 0/57 | 2026-09-05 | li | Pin stronger Wispr meter visibility | merged-not-deleted, hotfix-or-pin-like |
| wispr-noctalia-deploy-01a06da9 | 0b690db58 | 0/69 | 2026-09-04 | li | Advance Home Noctalia startup repair | merged-not-deleted |
| wispr-recovery-4e296a-os | 840ed01d1 | 0/68 | 2026-09-04 | li | CriomOS: advance Home Wispr recovery inputs | merged-not-deleted |
| worktree-scaffold-path | 237ae64c0 | 2/310 | 2026-07-19 | li | CriomOS: pin GnuPG-enabled orchestrate home service | unmerged-small, stale(68d), hotfix-or-pin-like |

Worktrees:
```
/git/github.com/LiGoldragon/CriomOS                                                d193baf (detached HEAD)
/home/li/wt/github.com/LiGoldragon/CriomOS/field-medium-eb7bae-flow-message-deploy 90702b6 [field/flow-message-deploy-eb7bae]
/home/li/wt/github.com/LiGoldragon/CriomOS/field-wifi-wan-recovery-753e69          114fcbd [field-wifi-wan-recovery-753e69]
/tmp/core-checkup-criomos-consumer                                                 1434386 (detached HEAD)
/tmp/criomos-wan-main-753e69                                                       d8c765d (detached HEAD)
```
jj workspaces:
```
ChromaNoctaliaDeployIntegration: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/ChromaNoctaliaDeployIntegration vkrxnnyu b4de2c5e (no description set)
CriomOS: zvyvynqx 343eb0fc (empty) (no description set)
CriomOS-wispr-integration: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-wispr-integration pkktnptk 50286391 (empty) wispr integration system workspace
CriomOS-wispr-runtime: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-wispr-runtime wzqzmxkt cd3668a8 (empty) (no description set)
CriomOSChromaHomePin: vtkzxtqz 828797eb (empty) (no description set)
CriomOSMainIntegration: wsyqmrnk fc3e3def (empty) (no description set)
DotosMapKeyCompatibility: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/DotosMapKeyCompatibility lktmttoy aac1caaa (no description set)
FinalWisprHomePin-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/FinalWisprHomePin-81c0dc wpkpvumw 0b91629d (empty) (no description set)
IntegrateLojix0191: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/IntegrateLojix0191 wkymzkxu 31e62527 (no description set)
LandDeployWisprStatus-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/LandDeployWisprStatus-81c0dc lzqmpmqu 6654bda8 (empty) (no description set)
LandDeployWisprStatusFix-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/LandDeployWisprStatusFix-81c0dc xywxprlr e4c85946 (empty) (no description set)
NormalizeHomeImmutableLock-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/NormalizeHomeImmutableLock-81c0dc msuurwtu 91540240 (empty) (no description set)
SolarClockLiveRecoveryCriomOS: qpstkwxm 28d931ba (empty) (no description set)
SolarTimeStatusBarCriomOS: wxmrrkqu a579c206 (empty) (no description set)
WisprStatus4-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/WisprStatus4-81c0dc ztvryvpk f9a15dd6 (empty) (no description set)
ZeusVscodiumDeployment: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/zeus-vscodium-deployment xuswlysm 26e4477b (no description set)
core-checkup-cf7879: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/core-checkup-cf7879 rkxqrwnw 059dbf2a (empty) (no description set)
core-checkup-consumer-final: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/core-checkup-consumer-final lwwztsvq e87c41b3 (empty) (no description set)
criomos-ms2130-control: ../../../../tmp/criomos-ms2130-control utpukkpt dc7809be (empty) (no description set)
criomos-preflow-control: ../../../../tmp/criomos-preflow-control pznowlty 9b1920d6 (empty) (no description set)
criomos-verification-4a8046: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-verification-4a8046 mpvsnwoz b845b96d (empty) (no description set)
criomosDotosRepair: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/criomosDotosRepair oooywuno ac1fae57 (no description set)
default: . zlqlkuuw c336dce3 (empty) (no description set)
default-opener-nhb-pin: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/default-opener-nhb-pin ulmnzotp cca3a57b (no description set)
disk-retention-2e28d8: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/disk-retention-2e28d8 vmxrsvqo 028f94f2 (empty) (no description set)
dotos-upper-integration: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/dotos-upper-integration vskktpnr 6a19062c (no description set)
f6db8d-lojix: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/f6db8d-lojix-start lkuywvvm 1cb3985d (empty) (no description set)
field-astra-5f38bc-flow-pins: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/field-astra-5f38bc-flow-pins qtzporlz 88900f26 field-astra-5f38bc-flow-pins | Pin Herdr Codex next-home integration
fixlojixbootownership: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/fixlojixbootownership urqrpsnq 9984cd64 (no description set)
flow-id-claude-parity: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/flow-id-claude-parity skkmxrvz 6047fe18 (empty) (no description set)
flow0106-b7da5d: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/flow0106-b7da5d wsvrunvp 12ecdbd7 (empty) (no description set)
flow07-b7da5d: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/flow07-b7da5d punwkyrp df3e4f25 (empty) (no description set)
home-orchestrate-main-pin: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/home-orchestrate-main-pin uqywwzyp 7f808934 (no description set)
horizon-datom-integration-542442: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/horizon-datom-integration-542442 wttyllol 5b982b38 (empty) (no description set)
horizon-flake-integration-542442: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/horizon-flake-integration-542442 zyyunwqv 05cd1684 (empty) (no description set)
horizon-leaner-shape: rpyxmqks 981f4fa6 (empty) (no description set)
horizon-module-migration-542442: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/horizon-module-migration-542442 owxulwlq 130fda94 (empty) (no description set)
horizon-re-engineering: rszlqmxq 10243a9e (empty) (no description set)
horizon-test-vm: tolnwyxq 119580a6 (empty) (no description set)
item49-core-checkup-capability: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/item49-core-checkup-capability ulqqorxm 6dce4b49 (empty) (no description set)
lojix-breaking-upgrade-docs: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/lojix-breaking-upgrade-docs lovywlul 975989ac (no description set)
lojix-ownership-mjl6-criomos: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/lojix-ownership-mjl6 xmxwnput 77bc525f (no description set)
luna6-flow06-aba-active: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/luna6-flow06-aba-active otknpouw 2f6c0244 (empty) (no description set)
luna6-flow06-aba74675: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/luna6-flow06-aba74675 tsvwxrlr ea18542b (empty) Luna6 isolated Flow 0.6 Home pin
modifier-architecture-20260811: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/modifier-architecture-20260811 wpzpomtk e3dd17fc (no description set)
pi-child-intercom-os: wuuzxywn 924f0929 (empty) (no description set)
prometheus-usb-bus-property-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/prometheus-usb-bus-property-5f38bc qsylxsly 6d6447ed (empty) (no description set)
prometheus-usb-downlink-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/prometheus-usb-downlink-5f38bc kpxkpzll d96ece57 (empty) (no description set)
remove-lojix-timeout-consumer: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/remove-lojix-timeout-consumer wkoukzqw d6d4f593 (no description set)
repair-home-dependency-chain-20260811: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/repair-home-dependency-chain-20260811 uzwlutlx 6a0e9f19 (no description set)
schema-rust-main-repair: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/schema-rust-main-repair xorxrtrw 7a40b601 (no description set)
tailnet-repair-da88cf: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/tailnet-repair-da88cf nmpynkwo 4ebc725e (empty) (no description set)
usb-downlink-non-router: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/usb-downlink-non-router uywumnuw 674bf3d8 (empty) (no description set)
usb-downlink-source-fix: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/usb-downlink-source-fix ynklwmnu e92a336e USB downlink activation source fix
wifi-country-da88cf: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/wifi-country-da88cf yrmwklop d69a7f43 (no description set)
wispr-noctalia-deploy-01a06da9: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/wispr-noctalia-deploy-01a06da9 yylnmxym b9132175 (empty) (no description set)
wispr-system-consumer: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-wispr-system-consumer snrktqpn 19b90c4a (empty) (no description set)
xmpp-chime-cf7879: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS/xmpp-chime-cf7879 rxuzszuu a66aaf78 (empty) (no description set)
```

## CriomOS-home

Remote: `ssh://git@github.com/LiGoldragon/CriomOS-home`; base: remote main 478b4ea04 (present locally); heads: 107

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| AdaptiveWindowWrapping | 18684d17a | 1/402 | 2026-07-19 | li | home: wrap Markdown at window width | unmerged-small, stale(68d), hotfix-or-pin-like |
| AddActiveNetworkWidget | e0375d41e | 0/386 | 2026-07-22 | li | home: add active NetworkManager widget | merged-not-deleted |
| CodexExplicitCommands-8a5caa | c40ff0cde | 0/60 | 2026-09-05 | li | Fix Codex remote argv fixture | merged-not-deleted |
| HardenActiveNetworkWidget | 4d6de296d | 0/384 | 2026-07-22 | li | home: reject inconsistent active network status | merged-not-deleted |
| IntelWifiGeolocationStabilizationHome | 36c1e23e4 | 2/427 | 2026-07-17 | li | home: use builder-compatible Orchestrate pin | unmerged-small, stale(70d), hotfix-or-pin-like |
| ListenerHistoryRetentionHome | bfb3a7294 | 1/449 | 2026-07-15 | li | home: deploy bounded listener history (GPT-5 direct) | unmerged-small, stale(72d) |
| PiExtensionReliability20260711 | 875af6ec7 | 0/459 | 2026-07-11 | li | CriomOS-home (gpt-5.6; source-guided): assert current pi fork revisions | merged-not-deleted |
| PlannotatorHomeIntegration | 476db8a6d | 0/59 | 2026-09-05 | li | fix: preserve Plannotator Bun payload | merged-not-deleted |
| ProtoformStack | f8d5c5d7b | 0/84 | 2026-09-04 | li | Point orchestrate at datomic a27f9b8e train rev e631bad9 | merged-not-deleted |
| RegistryMaintenanceDeployment | 5512ce442 | 0/402 | 2026-07-19 | li | home: add Git to Orchestrate daemon PATH | merged-not-deleted |
| StrengthenActiveNetworkChecks | 62d3d68a3 | 0/383 | 2026-07-22 | li | home: strengthen active network checks | merged-not-deleted |
| ZeusBirdLedgerHome | e20433c78 | 3/438 | 2026-07-16 | li | home: provision orchestrate workspace before service start | unmerged-small, stale(71d) |
| bluetooth-microphone-reliability | 5699c72d3 | 2/490 | 2026-07-10 | li | home: assert capture policy matching (operating-system-implementer; source-guide | unmerged-small, stale(77d) |
| bounded-state-production-home | 49c0842a6 | 1/443 | 2026-07-16 | li | home: pin bounded-state component revisions (GPT-5.6; medium) | unmerged-small, stale(72d), hotfix-or-pin-like |
| claude-default-bypass-5f38bc | c6419c84e | 6/7 | 2026-09-24 | li | feat: declare Claude bypass permission default | unmerged-large |
| claude-launch-rule-5f38bc | 3c8686290 | 4/7 | 2026-09-24 | li | Make managed Claude launchers bypass and child-session safe | unmerged-small |
| claude/workspace-agent-remote-access-zjj9rb | a169204a2 | 1/46 | 2026-09-09 | Claude | Add cdp-stdin-type: deliver stdin text into a Chromium tab over the DevTools Pro | unmerged-small, stale(16d) |
| codex-4a8046 | 590bb0842 | 1/69 | 2026-09-05 | li | Update Codex to 0.153.4 | unmerged-small, stale(20d) |
| codex-remote-control-owner-gate | db4afa912 | 0/146 | 2026-08-28 | li | Block unmanaged Codex remote control | merged-not-deleted |
| criomos-home-pi-subagents-training | a77722c46 | 0/429 | 2026-07-17 | li | home: deploy compact async pi role policy (Terra; high) | merged-not-deleted |
| criomos-home-spirit-bypass | fd30494e8 | 0/599 | 2026-06-21 | li | CriomOS-home: repin spirit 7fc267cb->711cf79e (bounded nota-next parser; no OOM  | merged-not-deleted, hotfix-or-pin-like |
| criomos-home-update-2026-07-08 | 61731b881 | 4/504 | 2026-07-09 | li | home: repin mentci update branches | unmerged-small, stale(78d), hotfix-or-pin-like |
| desktop-wakeability | 499198607 | 0/359 | 2026-07-26 | li | Home: make Desktop Intercom witness Nix-safe | merged-not-deleted |
| disable-claude-workflows | 0d0d90563 | 1/412 | 2026-07-18 | li | home: disable Claude workflows (operating-system-implementer; source-guided) | unmerged-small, stale(69d) |
| discard/CriomOS-home-remove-runtime-role-enforcement-terra | 07fa42ed4 | 1/392 | 2026-07-20 | li | criomos-home: restore Listener delivery feedback | unmerged-small, stale(67d) |
| emacs-markdown-visual-wrap | 95011c161 | 0/404 | 2026-07-19 | li | emacs: enable Markdown visual word wrapping | merged-not-deleted, hotfix-or-pin-like |
| emacs-syntax-highlighting-fix | 038dcb948 | 0/506 | 2026-07-08 | li | home: restore classic Rust font lock for Emacs | merged-not-deleted, hotfix-or-pin-like |
| emergency-live-theme-extension-fix | 1a9036db3 | 1/530 | 2026-07-06 | li | home: harden live theme extension startup | unmerged-small, stale(81d), hotfix-or-pin-like |
| f6db8d-lojix-start | 0176de5f6 | 0/36 | 2026-09-11 | li | Read the architecture Horizon actually projects | merged-not-deleted |
| f6db8d-removals | 4cb132ec0 | 1/37 | 2026-09-11 | li | Remove unused fzf theme variants, dead compositor stack, and primary-generated-s | unmerged-small |
| f6db8d-rust-relock | 37db5a8bb | 1/37 | 2026-09-12 | li | Relock rust-overlay 892c035d -> ab777f90; interactive Rust 1.96.0 -> 1.97.1 | unmerged-small |
| field-astra-5f38bc-flow-pins | 04446e78d | 16/7 | 2026-09-24 | li | Integrate Herdr Codex next-home hook repair | unmerged-large, hotfix-or-pin-like |
| field/agent-intercom-cleanup-eb7bae | ba5bcac8d | 3/5 | 2026-09-24 | li | Assert normalized cleanup environment | unmerged-small |
| field/codex-next-9e735b | aa86cb50d | 9/7 | 2026-09-24 | li | field-codex-next-9e735b / Unpack code mode host | unmerged-large |
| field/flow-deploy-9ddcbc | c4fa2395f | 2/7 | 2026-09-24 | li | Pin and select validated Flow Nexus release | unmerged-small, hotfix-or-pin-like |
| field/flow-message-consumers-9ddcbc | e1096a164 | 0/9 | 2026-09-21 | li | Prepare inactive Flow and Message Home consumers | merged-not-deleted |
| field/flow-message-deploy-eb7bae | 904185761 | 3/7 | 2026-09-24 | li | Compose green Flow and Message deployment | unmerged-small |
| fix-pi-launcher-ownership | a1e796ded | 0/492 | 2026-07-10 | li | Retain Pi agent launcher update arrangement | merged-not-deleted, hotfix-or-pin-like |
| flow-final-2586ea19-luna6 | bbdf439c1 | 18/7 | 2026-09-25 | li | Pin Flow Nexus to repaired launch fixture release | unmerged-large, hotfix-or-pin-like |
| flow-final-aba74675-luna6 | 8bfcf39c5 | 17/7 | 2026-09-25 | li | Pin Flow Nexus to final Claude Start release | unmerged-large, hotfix-or-pin-like |
| flow-main-opencode-luna6 | 77c3ac393 | 20/7 | 2026-09-25 | li | Integrate OpenCode package with Flow main launch repair | unmerged-large |
| flow07-home-b7da5d | e6f60a145 | 21/7 | 2026-09-25 | li | home: pin Flow 0.7.0 release | unmerged-large, hotfix-or-pin-like |
| generalist-budget-rollback | 9133b3bd6 | 0/394 | 2026-07-20 | li | home: repin generated Generalist rollback | merged-not-deleted, hotfix-or-pin-like |
| herdr-codex-next-5f38bc | 301e3d000 | 8/7 | 2026-09-24 | li | Declare Herdr Codex integration for next home | unmerged-large |
| home-datom-renovation-from-main-542442 | 654144d71 | 7/54 | 2026-09-06 | li | CriomOS-home: pin current Chroma Datom producer | unmerged-large, stale(20d), hotfix-or-pin-like |
| home-horizon-shape-542442 | e71729ec6 | 10/54 | 2026-09-06 | li | Home: guard Codex membership check evaluation | unmerged-large, stale(19d) |
| home-horizon-users-vector-542442 | ad20d9540 | 3/54 | 2026-09-06 | li | Pin corrected Orchestrate migration | unmerged-small, stale(20d), hotfix-or-pin-like |
| home-wispr-control-pin-4a8046 | 0b5637635 | 0/65 | 2026-09-05 | li | Pin repaired Wispr control bridge | merged-not-deleted, hotfix-or-pin-like |
| home-wispr-meter-pin-4a8046 | 3f58325f9 | 0/64 | 2026-09-05 | li | Pin Wispr meter handler repair | merged-not-deleted, hotfix-or-pin-like |
| horizon-driven-intercom | 3f187cc79 | 2/395 | 2026-07-20 | li | Home: verify Agent Intercom tunnel identity | unmerged-small, stale(67d) |
| integrate-claude-codex-emacs | 9479fd0a8 | 0/401 | 2026-07-19 | li | home: refresh Claude Codex Pi and Markdown wrapping | merged-not-deleted, hotfix-or-pin-like |
| integration-deployment-4a8046 | fbceccc76 | 4/67 | 2026-09-05 | li | Prune retired VSCodium flake inputs | unmerged-small, stale(20d) |
| integration-deployment-4a8046-wispr | adc53c356 | 0/66 | 2026-09-05 | li | Deploy Wispr reconnect without Codex upgrade | merged-not-deleted |
| listener080recovery | 334b9e08c | 1/467 | 2026-07-11 | li | CriomOS-home (GPT-5; recovery): pin Listener 0.8.0 | unmerged-small, stale(76d), hotfix-or-pin-like |
| live-theme-control-crash-fix | a83434c46 | 0/528 | 2026-07-05 | li | home: close live theme startup race | merged-not-deleted, hotfix-or-pin-like |
| main-before-rollback-db267d | fde8a2d2b | 10/54 | 2026-09-06 | li | Flow db267d: read the projected machine arch field Horizon actually emits | unmerged-large, stale(19d), hotfix-or-pin-like |
| opencode-home-b7da5d | fd2b16093 | 18/7 | 2026-09-25 | li | home: install OpenCode for testing capability | unmerged-large |
| opencode-home-b7da5d-repaired-flow | 926d9d6e5 | 19/7 | 2026-09-25 | li | home: install OpenCode for testing capability | unmerged-large |
| openrouter-seed-5f38bc | 812877557 | 4/7 | 2026-09-24 | li | feat: seed OpenRouter in the agent daemon configuration | unmerged-small |
| pi-child-intercom-injection-home | 5144ff87b | 2/478 | 2026-07-10 | li | pi-intercom: retain packaged inbound boundary (GPT-5.6-sol high) | unmerged-small, stale(77d) |
| pi-extension-fork-evidence | 9dfe98d17 | 0/451 | 2026-07-14 | li | docs: record Pi fixture review harness termination (skill-editor; source-guided) | merged-not-deleted |
| pi-subagents-acceptance-reliability | e9ede4faa | 0/470 | 2026-07-10 | li | home: preserve reviewed read-only scout results | merged-not-deleted |
| pi-subagents-deployment | ff7ab9b8c | 0/443 | 2026-07-16 | li | home: repin merged pi-subagents fork (operating-system-implementer; source-guide | merged-not-deleted, hotfix-or-pin-like |
| pi-subagents-fork-migration | c8209627d | 0/468 | 2026-07-10 | li | CriomOS-home: pin maintained pi-subagents fork (generalist; source-guided) | merged-not-deleted, hotfix-or-pin-like |
| pi-subagents-managed-deployment | d871a47f8 | 0/437 | 2026-07-16 | li | home: deploy managed pi-subagents role policy (Pi operating-system-implementer;  | merged-not-deleted |
| pi-subagents-runner-reliability-home | 4f5eceb03 | 0/469 | 2026-07-10 | li | pi-subagents (gpt-5.6-sol): preserve async terminal result reconciliation | merged-not-deleted |
| preserve/cf7879-core-checkup-home-pre-rewrite | 3ba10f1c7 | 1/27 | 2026-09-15 | li | Proposal: add generic pinned core checkup Home timer | unmerged-small, hotfix-or-pin-like |
| preserve/criomos-home-judge-launcher-20260720 | aeb831ecc | 1/471 | 2026-07-20 | li | preserve: retain Spirit judge session-launcher work (Generalist, task-directed) | unmerged-small, stale(67d) |
| preserve/pi-child-intercom-home-20260716 | eb5e239a2 | 1/479 | 2026-07-16 | li | preserve: safe-save dirty pi-child-intercom-home worktree 20260716 | unmerged-small, stale(71d) |
| preserve/pi-child-intercom-home-jj-20260716 | a2f31ff1c | 1/479 | 2026-07-10 | li | pi-child-intercom-injection-home | unmerged-small, stale(77d) |
| preserve/pi-subagents-notification-repin-home-jj-20260716 | 8206086bb | 1/468 | 2026-07-11 | li | pi-subagents-notification-repin | unmerged-small, stale(76d), hotfix-or-pin-like |
| primary-2v5c.15-criomos-home-spirit | 132b9c9f2 | 1/526 | 2026-07-06 | li | (("Update", "spirit-lock"), ("Pin", "Domain All stack"), ("Ready", "home check p | unmerged-small, stale(81d), hotfix-or-pin-like |
| primary-2v5c.19-criomos-home-spirit-v11 | 3e5854b4d | 2/526 | 2026-07-06 | li | (("Update", "spirit-lock"), ("Pin", "fixed v11-to-v13 migration"), ("Ready", "sp | unmerged-small, stale(81d), hotfix-or-pin-like |
| primary-99n-home | 59d842387 | 0/144 | 2026-08-28 | li | Remove obsolete Agent Intercom Home service gates | merged-not-deleted |
| prompt-relay-a07f01a-luna6 | f1cc3d500 | 21/7 | 2026-09-25 | li | Pin prompt relay to typed deregistration release | unmerged-large, hotfix-or-pin-like |
| proposal/348e7b-activation | 98e7f199d | 1/26 | 2026-09-16 | li | Compose core checkup with current relay Home deployment | unmerged-small |
| proposal/348e7b-core-old-message | 4eaf22574 | 6/26 | 2026-09-16 | li | bind resume cwd to reviewed thread | unmerged-large |
| proposal/348e7b-heartbeat | f27275149 | 7/26 | 2026-09-16 | li | Package isolated primary heartbeat with pinned runtime and opt-in timer | unmerged-large, hotfix-or-pin-like |
| proposal/348e7b-layer-access | 2b068e073 | 2/26 | 2026-09-16 | li | Use recorded cwd for Codex layer resume | unmerged-small |
| proposal/6852f4-default-effort-medium | bfea9669a | 1/24 | 2026-09-17 | li | Set generated Codex and Pi default effort to medium | unmerged-small |
| proposal/6852f4-flow-home-introduction | 2f1679a86 | 1/24 | 2026-09-17 | li | Add declarative Flow Nexus Home profile | unmerged-small |
| proposal/6852f4-herdr-toast-delivery | df4d00b9e | 0/25 | 2026-09-17 | li | Declare Herdr terminal toast delivery | merged-not-deleted |
| proposal/6852f4-message-flow-home | 02a3b5de7 | 5/24 | 2026-09-17 | li | Document coupled Message Flow adoption boundary | unmerged-small |
| proposal/cf7879-core-checkup-home | b158bba8d | 1/27 | 2026-09-15 | li | Proposal: add generic pinned core checkup Home timer | unmerged-small, hotfix-or-pin-like |
| proposal/cf7879-core-checkup-home-closure | c030ed49b | 8/27 | 2026-09-16 | li | Use exported Nix closure graph for core checkup proof | unmerged-large |
| proposal/cf7879-core-checkup-home-closure-fix | 17dd7595d | 13/27 | 2026-09-16 | li | Propose successor core-checkup harness snapshot | unmerged-large, hotfix-or-pin-like |
| proposal/cf7879-core-checkup-home-recovery-20260915 | 92e2da4c9 | 6/27 | 2026-09-15 | li | Correct pinned core checkup source revision metadata | unmerged-large, hotfix-or-pin-like |
| proposal/cf7879-home-cluster-relay | 56aa9cdac | 18/27 | 2026-09-16 | li | Pin Home relay adapter to roster-short attach fix | unmerged-large, hotfix-or-pin-like |
| push-tnqmxztqqmks | ba0de9f84 | 0/157 | 2026-08-27 | li | Avoid raw Codex collision in VSCodium Home profile | merged-not-deleted |
| restore-delivery-feedback | 07fa42ed4 | 1/392 | 2026-07-20 | li | criomos-home: restore Listener delivery feedback | unmerged-small, stale(67d) |
| restore-orchestrate-forward-repair | dc0a8943e | 0/463 | 2026-07-11 | li | CriomOS-home: pin latest Orchestrate runtime | merged-not-deleted, hotfix-or-pin-like |
| solar-location-chroma-home-pin | 26b3f431a | 3/443 | 2026-07-16 | li | home: pin Chroma solar reconciliation log (gpt-5.6-terra; high) | unmerged-small, stale(71d), hotfix-or-pin-like |
| solar-location-repair-home | c52e796ec | 1/443 | 2026-07-16 | li | home: disable Noctalia IP location (operating-system-implementer; source-guided) | unmerged-small, stale(71d) |
| solar-time-status-bar-home | 3a3004f65 | 3/443 | 2026-07-16 | li | home: fix solar clock tooltip hover state (gpt-5.6-terra; high) | unmerged-small, stale(71d) |
| spirit-judge-source-ready-home-20260710 | 8cc609ebc | 3/467 | 2026-07-11 | li | home: require remote Spirit deployment check execution (gpt-5.6; source-guided) | unmerged-small, stale(76d) |
| test/laptop-colemak-keyd | a8b98fb09 | 0/557 | 2026-07-02 | li | CriomOS-home: split Pi subagent profiles | merged-not-deleted |
| toolchain-refresh | bd4d6125c | 3/402 | 2026-07-19 | li | home (gpt-5.6; recovery): remove deferred changes from Pi update | unmerged-small, stale(68d) |
| wispr-meter-visibility-4a8046 | 3c08f1c74 | 0/62 | 2026-09-05 | li | Correct Wispr meter clipping expectations | merged-not-deleted, hotfix-or-pin-like |
| wispr-noctalia-startup-01a06da9 | 59e9a1ad2 | 7/79 | 2026-09-04 | li | Preload managed Noctalia plugins | unmerged-large, stale(21d) |
| wispr-noctalia-startup-test-01a06da9 | fc4289a2a | 6/79 | 2026-09-04 | li | Test Noctalia plugin-state reconciliation | unmerged-large, stale(21d) |
| wispr-provider-fetch-81c0dc | 26999bd90 | 2/79 | 2026-09-04 | li | Use provider-owned Wispr installer fetch | unmerged-small, stale(21d) |
| wispr-recovery-4e296a | 8021ae5d4 | 8/79 | 2026-09-04 | li | home: pin Wispr recovery provider revision | unmerged-large, stale(21d), hotfix-or-pin-like |
| wispr-status-consumer-81c0dc | 5f1f149f9 | 1/79 | 2026-09-04 | li | Add Noctalia Wispr status consumer | unmerged-small, stale(21d) |
| wispr-status-entry-ids-81c0dc | 463099b81 | 3/79 | 2026-09-04 | li | Separate Wispr Noctalia entry identifiers | unmerged-small, stale(21d) |
| wispr-status-reconnect-4a8046 | ff111978e | 1/69 | 2026-09-05 | li | Reset Wispr meter freshness after reconnect | unmerged-small, stale(20d) |
| worktree-scaffold-path | 2888bc093 | 2/404 | 2026-07-19 | li | home: provide GnuPG to orchestrate daemon | unmerged-small, stale(68d) |

Worktrees:
```
/git/github.com/LiGoldragon/CriomOS-home                                                   478b4ea0 (detached HEAD)
/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-codex-next-9e735b                    aa86cb50 [field/codex-next-9e735b]
/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-medium-eb7bae-agent-intercom-cleanup ba5bcac8 [field/agent-intercom-cleanup-eb7bae]
/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-medium-eb7bae-flow-message-deploy    90418576 [field/flow-message-deploy-eb7bae]
```
jj workspaces:
```
ChromaNoctaliaDeployIntegration: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/ChromaNoctaliaDeployIntegration kywxrqrn 53f19fa8 (empty) Continue integration
CriomOS-home: wmrtykuv 4c18405e (empty) (no description set)
CriomOS-home-ProtoformStack-6329f1: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/CriomOS-home-ProtoformStack-6329f1 xuvzwqzp f38b4c23 (empty) (no description set)
CriomOS-home-wispr-integration: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home-wispr-integration poxzurkx f4ef040a (empty) (no description set)
CriomOS-home-wispr-overlay: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home-wispr-overlay nqymrors 6b19ef1c (empty) (no description set)
CriomOSHomeChromaPin: yvqmmumq 0301f5f5 (empty) (no description set)
CriomOSHomeMainIntegration: zkrkmllr 340cc78a (empty) (no description set)
SolarClockLiveRecoveryHome: krpmxpmp e021a2ce (empty) (no description set)
SolarTimeStatusBarHome: oorwvrxn 290c7d2a (empty) (no description set)
chroma-upgrade-33a4d4: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/chroma-upgrade-33a4d4 nozmxolx 854cf407 (empty) (no description set)
claude-answers-datom-542442: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/claude-answers-datom-542442 wnynxnku 348cf32a (empty) (no description set)
claude-launch-rule: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/claude-launch-rule prywtsqt 2ce47a81 (empty) (no description set)
cluster-operator-pi-yolo: opmuqvyu 0754b131 (empty) (no description set)
codium-symbol-nav-2026-06-01: kwxrtplm 3629c4a1 (empty) (no description set)
core-checkup-cf7879-v2: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/core-checkup-cf7879-v2 kzvpmmlz/0 b8ec0f10 proposal/cf7879-core-checkup-home* | (divergent) Proposal: add generic pinned core checkup Home timer
criomos-home-no-flow-check.J7iNlO: nsrwzwtp d62d5645 (empty) (no description set)
default: . qyvzppwy bc3b82a5 (no description set)
emacs-eln-and-warnings-2026-06-01: yxlvloqp 1e3eb0e6 (empty) (no description set)
emacs-symbol-nav-and-startup-2026-06-01: ploummot f1401912 (empty) (no description set)
f6db8d-lojix: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/f6db8d-lojix-start mtqquwtn f84a0049 (empty) (no description set)
field-astra-5f38bc-flow-pins: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/field-astra-5f38bc-flow-pins nsltqzxs 04446e78 field-astra-5f38bc-flow-pins | Integrate Herdr Codex next-home hook repair
flow-id-claude-parity: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-id-claude-parity mrwpyqmr 1d9d8b27 (empty) (no description set)
flow0106-b7da5d: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/flow0106-b7da5d ssqstpqr 2e6c131a (empty) (no description set)
flow07-b7da5d: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/flow07-b7da5d rqkrssvy 083df21a (empty) (no description set)
herdr-codex-next-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/herdr-codex-next-5f38bc tmlupkwq 0e13f340 (empty) (no description set)
home-baseline-bird-542442: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/home-baseline-bird-542442 prxkulys 1578bd56 (empty) b12 bird isolation witness
home-canonical-llm-packages: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/home-canonical-llm-packages xysxxwkl 3ff3938d (no description set)
home-horizon-shape-542442: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/home-horizon-shape-542442 myzmlktt 263d4d1b (empty) (no description set)
home-wt: zslykwvk b97fe315 (empty) (no description set)
horizon-leaner-shape: ppkotnml aa183587 (empty) (no description set)
horizon-re-engineering: kquozlzv 96635ec1 (empty) (no description set)
luna6-flow06-aba-active: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/luna6-flow06-aba-active vkqyvlnp f1331767 (empty) (no description set)
luna6-flow06-aba74675: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/luna6-flow06-aba74675 myonkqvy 6f6787d3 (empty) Luna6 isolated Flow 0.6 consumer pin
noctalia-wispr-status-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/noctalia-wispr-status-81c0dc rzyzrzyn 7fa02a4a (empty) (no description set)
primary-99n-home: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/primary-99n-home nuuuwmuw 59d84238 primary-99n-home | Remove obsolete Agent Intercom Home service gates
wispr-flow-criomos4-main-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-flow-criomos4-main-81c0dc mryqzklo e382ef96 (empty) (no description set)
wispr-noctalia-startup-01a06da9: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-noctalia-startup-01a06da9 kktmrksn 03316f1b (empty) (no description set)
wispr-provider-fetch-main-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-provider-fetch-main-81c0dc tvpqtrml 379e8fa3 (empty) (no description set)
wispr-status-consumer-main-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-status-consumer-main-81c0dc zlvnqxxt 7ffa5e52 (empty) (no description set)
wispr-status-entry-ids-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-status-entry-ids-81c0dc zzwympyl 1ea3c48a (empty) (no description set)
wispr-status-final-main-81c0dc: ../../../../home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-status-final-main-81c0dc xqvlzomp 03bce5ab (empty) (no description set)
```

## CriomOS-lib

Remote: `ssh://git@github.com/LiGoldragon/CriomOS-lib`; base: remote main 6db67c3bd (present locally); heads: 5

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| horizon-leaner-shape | 82a0e2b48 | 5/9 | 2026-05-30 | li | criomos-lib: clarify transitional lan constants | unmerged-small, stale(118d) |
| models-da88cf | 6db67c3bd | 0/0 | 2026-09-25 | li | Restore Gemma beside Qwen3.5 in llm.json per the living's 09-16 word | merged-not-deleted |
| proposal/f55ec8-prometheus-single-model | c74b22240 | 0/1 | 2026-09-16 | li | Keep only Qwen3.5-122B on LargeAi nodes, the living's word 2026-09-16 | merged-not-deleted |
| system-operator-pre-reconcile-2026-05-27 | 82a0e2b48 | 5/9 | 2026-05-30 | li | criomos-lib: clarify transitional lan constants | unmerged-small, stale(118d) |

Worktrees:
```
/git/github.com/LiGoldragon/CriomOS-lib 6db67c3 (detached HEAD)
```
jj workspaces:
```
default: . kpsrqorn ae1c6680 (empty) (no description set)
horizon-leaner-shape: ppuzpwln 96f4b417 (empty) (no description set)
horizon-re-engineering: kxztmont 34dfaa1e (empty) (no description set)
```

## horizon-rs

Remote: `ssh://git@github.com/LiGoldragon/horizon-rs`; base: remote main b45d6ad48 (present locally); heads: 11

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| cloud-designer-cloud-node-species | 750f8cf6e | 0/49 | 2026-06-20 | li | node: delete the TypeIs one-hot; derive BehavesAs from NodeSpecies directly | merged-not-deleted |
| cloud-designer-web-host | 4a0e29fe5 | 0/45 | 2026-06-20 | li | proposal: add NodeService::WebHost — typed website-hosting capability | merged-not-deleted |
| horizon-datom-node-542442 | 05879e7c1 | 0/19 | 2026-09-05 | li | Horizon: preserve typed VM testing capability | merged-not-deleted |
| horizon-driven-intercom | 1f583e1ce | 0/35 | 2026-07-20 | li | Horizon: project Agent Intercom gateway SSH identity | merged-not-deleted |
| horizon-test-vm | 214e6816d | 0/54 | 2026-06-16 | li | horizon: multi-host test-VM nodes (super_nodes) + SCOPED image-exchange keys (Un | merged-not-deleted |
| lojix-canonical-nota-pin-horizon | a6300bccc | 1/39 | 2026-07-16 | li | horizon: pin canonical NOTA (GPT-5.4, high) | unmerged-small, stale(71d), hotfix-or-pin-like |
| primary-99n-schema-data | c70915eb5 | 0/25 | 2026-08-28 | li | Remove obsolete Agent Intercom node services | merged-not-deleted |
| prometheus-usb-downlink-5f38bc | fed0a12a3 | 1/7 | 2026-09-24 | li | Expose declared router USB LAN MAC address | unmerged-small |
| proposal/cf7879-core-checkup-capability | 76f2c05c6 | 1/25 | 2026-09-15 | li | Add typed Core Checkup node service | unmerged-small |
| usb-gateway-6db4fe | 37416e10c | 0/21 | 2026-09-21 | li | Enforce one USB IPv4 gateway per node | merged-not-deleted |

Worktrees:
```
/git/github.com/LiGoldragon/horizon-rs                     b45d6ad (detached HEAD)
/home/li/wt/github.com/LiGoldragon/horizon-opencode-7e8542 ee8d6f8 (detached HEAD)
```
jj workspaces:
```
DotosMapKeyCompatibility: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/DotosMapKeyCompatibility smnyyltt f4c0de87 (empty) (no description set)
default: . zyuotyxm 4cd63e92 (empty) (no description set)
horizon-40d-eval: ../../../../home/li/wt/horizon-40d-eval skxprpps 0ef72f44 (empty) (no description set)
horizon-datom-node-542442: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-datom-node-542442 ovlxkzrr d211a768 (empty) (no description set)
horizon-leaner-shape: pqrkywqu b628d4af (empty) (no description set)
horizon-primary-api-correction-753e69: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-primary-api-correction-753e69 pkrornpq 4c875fc5 (empty) (no description set)
horizon-re-engineering: wkxxzrox 8dfba851 (empty) (no description set)
item49-core-checkup-capability: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/item49-core-checkup-capability nutolnur 32655540 (empty) (no description set)
p99n-horizon-main: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/p99n-horizon-main qovnurww ec844250 (empty) (no description set)
post-terminus-horizon-data: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/post-terminus-horizon-data twtykonp 078fb469 (empty) (no description set)
primary-99n-schema-data: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/primary-99n-schema-data pvqtkyks c13f2a97 (empty) (no description set)
prometheus-usb-downlink-40d-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/prometheus-usb-downlink-40d-5f38bc svwrpusp 4ab79986 (empty) (no description set)
prometheus-usb-downlink-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/prometheus-usb-downlink-5f38bc umuqmwvq 137eed7e (empty) (no description set)
tailnet-repair-da88cf: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/tailnet-repair-da88cf wlqklxmq f35ffea4 (no description set)
usb-gateway-main-merge-753e69: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/usb-gateway-main-merge-753e69 mqlplwon 090f2bd8 (empty) (no description set)
xmpp-chime-cf7879: ../../../../home/li/wt/github.com/LiGoldragon/horizon-rs/xmpp-chime-cf7879 proqpovs 28b748b8 (empty) (no description set)
```

## goldragon

Remote: `ssh://git@github.com/LiGoldragon/goldragon`; base: remote main 8c4d03de7 (present locally); heads: 12

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| cloud-designer-cloud-node-data | 2bfca41c0 | 4/26 | 2026-06-20 | li | cloud-node-data: mark doris unprovisioned — placeholder host key, awaiting a rol | unmerged-small, stale(97d) |
| enable-vm-hosting-prometheus | 84c7f9e66 | 0/26 | 2026-06-19 | li | goldragon: enable VM hosting on prometheus + durable TestVm node; migrate datom  | merged-not-deleted |
| generic-nodes-542442 | 74754e32a | 0/5 | 2026-09-06 | li | (("CommitType", "migration"), ("Action", "retire active legacy proposal and role | merged-not-deleted |
| goldragon-horizon-synchronizer-542442 | 1f49f8dea | 0/3 | 2026-09-06 | li | (("CommitType", "documentation"), ("Action", "correct Synchronizer validation in | merged-not-deleted, hotfix-or-pin-like |
| horizon-driven-intercom | 3a618e9bf | 1/18 | 2026-07-20 | li | (("CommitType", "cluster"), ("Action", "add Agent Intercom roles"), ("Verdict",  | unmerged-small, stale(67d) |
| primary-99n-schema-data | 5bc563bf9 | 1/10 | 2026-08-28 | li | (("Remove", "horizon-data"), ("Action", "delete obsolete Agent Intercom node ser | unmerged-small, stale(28d) |
| prometheus-usb-downlink-5f38bc | 1781f079a | 1/0 | 2026-09-24 | li | Declare Prometheus USB LAN hardware identity | unmerged-small |
| proposal/348e7b-horizon-40d | 2bd1d1074 | 2/2 | 2026-09-16 | li | (("Upgrade", "horizon"), ("Lock", "40d04d2504fee619e9b2b2564b8a769a3a9d6049"), ( | unmerged-small |
| proposal/348e7b-prosody-accounts | 980d0aaa2 | 2/2 | 2026-09-16 | li | (("Secret", "prosody"), ("Map", "existing ciphertext to Lojix flat exports"), (" | unmerged-small |
| proposal/cf7879-core-checkup-ouranos | 0056f55b8 | 2/10 | 2026-09-15 | li | Select Core Checkup for ouranos | unmerged-small |
| usb-gateway-data-753e69 | a911515c6 | 4/10 | 2026-09-21 | li | (("CommitType", "data"), ("Action", "assign Ouranos USB IPv4 gateway"), ("Verdic | unmerged-small |

Worktrees:
```
/git/github.com/LiGoldragon/goldragon 8c4d03d (detached HEAD)
```
jj workspaces:
```
default: . mrwksmvp f7837ad9 (empty) (no description set)
generic-nodes-542442: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/generic-nodes-542442 stvuynqo e1bfb11f (empty) (no description set)
goldragon-horizon-retire-542442: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/goldragon-horizon-retire-542442 plkkwtvt 572db640 (empty) (no description set)
goldragon-main-canonical: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/goldragon-main-canonical rnwyuwxq 3d7ebd67 (empty) (no description set)
goldragon-opencode-7e8542: ../../../../home/li/wt/github.com/LiGoldragon/goldragon-opencode-7e8542 moklnzyu d40c82de (empty) (no description set)
goldragonCanonicalProposal: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/lojix-canonical-proposal nlkqukmv d52a9be0 (empty) (no description set)
horizon-leaner-shape: xzkmmmvz 7d19d8d6 (empty) (no description set)
horizon-re-engineering: kmvrwyuq d72e5ba5 (empty) (no description set)
item49-core-checkup-capability: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/item49-core-checkup-capability wtsymwwo d066b3de (empty) (no description set)
p99n-gold-main: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/p99n-gold-main pznusqtz 4a023b35 (empty) (no description set)
post-terminus-goldragon-data: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/post-terminus-horizon-data lvnnlwyu 2cf49de9 (empty) (no description set)
primary-99n-schema-data: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/primary-99n-schema-data zpnknsqt 65179c54 (empty) (no description set)
prometheus-usb-downlink-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/prometheus-usb-downlink-5f38bc vmsmvstw fc93fab7 (empty) (no description set)
tailnet-repair-da88cf: ../../../../home/li/wt/github.com/LiGoldragon/goldragon/tailnet-repair-da88cf suqttyoq 68bdc554 (empty) (no description set)
```

## lojix

Remote: `git@github.com:LiGoldragon/lojix.git`; base: remote main c4bba4fa1 (present locally); heads: 30

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| ZeusBirdLedgerLojix | 585af00c3 | 2/98 | 2026-07-16 | li | lojix: capture remote ledger observations | unmerged-small, stale(71d) |
| bounded-lifecycle-remediation | 83dc757bd | 12/98 | 2026-07-17 | li | lojix: remediate bounded release closure (GPT-5.4, high) | unmerged-large, stale(71d) |
| certification-blocker-repair | 1dbcab656 | 16/98 | 2026-07-19 | li | lojix: make test check output deterministic (Generalist, source-guided) | unmerged-large, stale(69d) |
| deployment-compatibility-preflight | 5441998d8 | 15/98 | 2026-07-17 | li | lojix: gate deployment compatibility and active closure health (GPT-5.4, high) | unmerged-large, stale(71d) |
| discard/disposable-rehearsal | 533b96b8e | 15/98 | 2026-07-17 | li | lojix: attribute release health and evaluation failures (Generalist, source-guid | unmerged-large, stale(70d) |
| disposable-rehearsal | 533b96b8e | 15/98 | 2026-07-17 | li | lojix: attribute release health and evaluation failures (Generalist, source-guid | unmerged-large, stale(70d) |
| finish-lojix-rewrite | a1afde514 | 2/98 | 2026-07-16 | li | lojix: pin canonical contracts and regenerate schema roots (GPT-5.4, high) | unmerged-small, stale(71d), hotfix-or-pin-like |
| horizon-leaner-shape | 746672305 | 23/176 | 2026-06-13 | li | lojix: port horizon branch to signal-frame | unmerged-large, stale(104d) |
| horizon-re-engineering | c39dc90e1 | 12/176 | 2026-05-16 | li | lojix: add generic real build smoke runner | unmerged-large, stale(132d) |
| live-deploy-test-chain | 384197875 | 2/139 | 2026-06-19 | li | live bracket: detached guest activation, host-untouched runNixOSTest proof (GREE | unmerged-small, stale(98d) |
| lojix-bounded-lifecycle-release-milestone-9 | 38dc8971e | 11/98 | 2026-07-16 | li | lojix: release bounded local checkpoint lifecycle (GPT-5.4, high) | unmerged-large, stale(71d) |
| lojix-canonical-dependency-closure | 55fa843f9 | 3/98 | 2026-07-16 | li | lojix: unify canonical runtime dependency closure (GPT-5.4, high) | unmerged-small, stale(71d) |
| lojix-canonical-external-adapters-milestone-3 | b53c8000c | 5/98 | 2026-07-16 | li | lojix: migrate canonical external contract adapters (GPT-5.4, high) | unmerged-small, stale(71d) |
| lojix-canonical-integration-tests-milestone-7 | a31eb9bfa | 9/98 | 2026-07-16 | li | lojix: assert canonical nexus schema identities (GPT-5.4, high) | unmerged-large, stale(71d) |
| lojix-canonical-persistence-recovery-milestone-6 | 425676c77 | 8/98 | 2026-07-16 | li | lojix: migrate canonical persistence recovery identities (GPT-5.4, high) | unmerged-large, stale(71d) |
| lojix-canonical-routed-contact-milestone-4 | b4a7111d9 | 6/98 | 2026-07-16 | li | lojix: assert canonical routed contact mapping (GPT-5.4, high) | unmerged-large, stale(71d), hotfix-or-pin-like |
| lojix-canonical-runner-daemon-milestone-5 | 780bcc9dc | 7/98 | 2026-07-16 | li | lojix: migrate canonical runner and daemon fields (GPT-5.4, high) | unmerged-large, stale(71d) |
| lojix-canonical-schema-milestone-2 | 4ef451022 | 4/98 | 2026-07-16 | li | lojix: regenerate canonical six-slot schema roots (GPT-5.4, high) | unmerged-small, stale(71d) |
| lojix-horizon-contract-7091ea | ac672dab1 | 2/7 | 2026-09-21 | li | Align Lojix workspace with current Horizon contracts | unmerged-small |
| lojix-horizon-datom31-00f95a | a67f57739 | 2/0 | 2026-09-24 | li | Align Lojix with Horizon Datom 0.31 contracts | unmerged-small |
| lojix-lifecycle-completion | 897362f07 | 1/98 | 2026-07-16 | li | lojix: resume durable jobs before admission (GPT-5.4, high) | unmerged-small, stale(71d) |
| lojix-schema-one-reconstruction-milestone-8 | 780c1fc41 | 10/98 | 2026-07-16 | li | lojix: reconstruct schema one stores read-only (GPT-5.4, high) | unmerged-large, stale(71d) |
| prometheus-usb-downlink-5f38bc | 387c13b51 | 1/0 | 2026-09-24 | li | Pin Horizon USB LAN identity producer | unmerged-small, hotfix-or-pin-like |
| proposal/horizon-contract-repin-8565e8 | 6b299ec17 | 3/0 | 2026-09-21 | li | Lojix: parse authored Horizon proposal into coherent typed Signal graph | unmerged-small, hotfix-or-pin-like |
| proposal/remote-builder-fallback-false | 476bc56eb | 1/7 | 2026-09-19 | li | lojix: forbid local fallback for remote closure builds | unmerged-small |
| push-schema-concept-lojix | 9d804e46b | 23/176 | 2026-05-24 | li | schema: add v0.1 concept schema | unmerged-large, stale(124d) |
| schema-deep | 5145ae61c | 2/172 | 2026-05-27 | li | schema-deep: add source staging actor plane | unmerged-small, stale(121d) |
| schema-deep-iteration-2 | 9a84cbca4 | 2/172 | 2026-05-30 | li | lojix: add schema deep iteration runtime | unmerged-small, stale(118d) |
| system-operator-contained-test-poc | 1dfa71432 | 5/132 | 2026-06-23 | li | lojix: add contained cluster root and criome gate witness | unmerged-small, stale(94d) |

Worktrees:
```
/git/github.com/LiGoldragon/lojix c4bba4f (detached HEAD)
```
jj workspaces:
```
DotosMapKeyCompatibility: ../../../../home/li/wt/github.com/LiGoldragon/lojix/DotosMapKeyCompatibility uvwsoyrq 80e3c9c1 (empty) (no description set)
default: . ppnwwrvk f361aa1a (empty) (no description set)
fixlojixbootownership: ../../../../home/li/wt/github.com/LiGoldragon/lojix/fixlojixbootownership zwpnkmnl 75829925 (empty) (no description set)
flow857335-legacy-fixture: ../../../../tmp/lojix-legacy-fixture-857335 yzmyslzv c2174e05 (no description set)
lojix-current-fixtures-542442: ../../../../home/li/wt/github.com/LiGoldragon/lojix/lojix-current-fixtures-542442 tvrolkos ce44b941 (empty) (no description set)
lojix-datom-horizon-542442: ../../../../home/li/wt/github.com/LiGoldragon/lojix/lojix-datom-horizon-542442 rwmwsmyn 29089cf9 (empty) (no description set)
lojix-datom-ingress-542442: ../../../../home/li/wt/github.com/LiGoldragon/lojix/lojix-datom-ingress-542442 zmtyylsw d6f55c6b (empty) (no description set)
lojix-v4-inspector-542442: ../../../../tmp/lojix-v4-inspector-542442 nuwqnsqz 11f60b4d (empty) (no description set)
lojixCanonicalMigration: ../../../../home/li/wt/github.com/LiGoldragon/lojix/lojix-canonical-migration stquwuny 4cb68ff0 (empty) (no description set)
modifier-architecture-20260811: ../../../../home/li/wt/github.com/LiGoldragon/lojix/modifier-architecture-20260811 ltooxrpz de7abd45 (empty) (no description set)
p99n-lojix-main: ../../../../home/li/wt/github.com/LiGoldragon/lojix/p99n-lojix-main rzzysnwm 2ceb3f44 (empty) (no description set)
prometheus-usb-downlink-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/lojix/prometheus-usb-downlink-5f38bc yttozknn 67c416d5 (empty) (no description set)
remove-effect-timeout: ../../../../home/li/wt/github.com/LiGoldragon/lojix/remove-effect-timeout zzuwlutl db4585c3 (empty) (no description set)
```

## flow

Remote: `git@github.com:LiGoldragon/flow.git`; base: remote main 34aaf7875 (present locally); heads: 47

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| claude-launch-rule-00f95a | 784b59f99 | 0/26 | 2026-09-24 | li | Make Claude native launches explicit and isolated | merged-not-deleted |
| f2-g5-38de5b | 4671f8d4b | 0/18 | 2026-09-25 | li | Flow 0.7.1: version answer and remotely controllable Claude launches | merged-not-deleted |
| field-pending-recovery-753e69 | 481b6909e | 22/59 | 2026-09-22 | li | Add fail closed pending Flow start decision helper | unmerged-large |
| flow/00f95a-system-prompt-start | aae2b197c | 11/59 | 2026-09-25 | li | Add Flow Start system-prompt adapter primitives | unmerged-large |
| flow/basic-commands-00f95a | 54856835f | 0/27 | 2026-09-24 | li | Add basic Flow send stop and list commands | merged-not-deleted |
| flow/e798f3-launch-adapter | fd1dae690 | 10/59 | 2026-09-25 | li | Commit e798f3's work found under lock 3847 before stale release | unmerged-large |
| flow/launch-profile-47764b | be898a478 | 0/58 | 2026-09-23 | li | Compose typed Flow launch prompts | merged-not-deleted |
| flow/native-herdr-launch-47764b | 33b9f608c | 0/34 | 2026-09-23 | li | Reject malformed first prompt before native submit | merged-not-deleted |
| flow/pane-presentation-00f95a | 7cc19af0a | 0/25 | 2026-09-24 | li | Witness Flow Send presentation in the exact pane | merged-not-deleted |
| flow/refresh-runtime-47764b | 22c4141be | 6/30 | 2026-09-24 | li | Authenticate refresh reconciliation from successor | unmerged-large |
| flow/retry-created-pane-00f95a | e41621af8 | 1/25 | 2026-09-24 | li | Recover durable created pane after Flow Start binding refusal | unmerged-small |
| flow/start-store-47764b | 33b9f608c | 0/34 | 2026-09-23 | li | Reject malformed first prompt before native submit | merged-not-deleted |
| flow/system-prompt-bundle-00f95a | 2586ea19b | 0/21 | 2026-09-25 | li | Repair all Flow bundle launch fixtures | merged-not-deleted |
| flow/transcript-schema-repin-47764b | 4c985b672 | 0/53 | 2026-09-23 | li | Repin final transcript boundary graph | merged-not-deleted, hotfix-or-pin-like |
| g2-g3-38de5b | 470dcc472 | 0/15 | 2026-09-25 | li | Flow 0.8.0: one lean first prompt | merged-not-deleted |
| g6-38de5b | 8f8a71a4d | 0/14 | 2026-09-25 | li | Flow 0.8.1: Codex main-flow bundle at the top of the first block | merged-not-deleted |
| g8-g9-nexus-38de5b | 28a78d24f | 0/13 | 2026-09-25 | li | Flow 0.9.0: Replace, LaunchStatus and Observe.Launch | merged-not-deleted |
| i1-g10-38de5b | 972d8d229 | 0/16 | 2026-09-25 | li | flow-nexus: format main.rs | merged-not-deleted |
| launch-findings-38de5b | bbf5fa163 | 0/12 | 2026-09-25 | li | Flow 0.10.0: stacked Claude commands, native title after claim, no auto-mode off | merged-not-deleted |
| mind-astra-independent-fixture-repair-f5a74e | d4107dd25 | 1/22 | 2026-09-25 | li | Repair LaunchProfile bundle fixtures | unmerged-small, hotfix-or-pin-like |
| mind-medium-delivery-dispatch-2c61af | 6d23cd7ec | 15/59 | 2026-09-21 | li | Dispatch delivery permit queries through Flow Nexus | unmerged-large |
| mind-medium-flow-preacquire-auth-2c61af | c77ccd937 | 21/59 | 2026-09-22 | li | Fail closed Flow delivery acquire on unverified socket peer | unmerged-large |
| mind-medium-observe-sessions-2c61af | d66bbea25 | 8/59 | 2026-09-21 | li | Re-export normalized session observation facade | unmerged-large |
| mind-medium-tester-selector-2c61af | 5afb64f2c | 22/59 | 2026-09-22 | li | Select authored testing skill for tester alias with exact cardinality | unmerged-large |
| mind-medium-typed-input-proposal-2c61af | 4660aa0bb | 23/59 | 2026-09-22 | li | Propose namespaced tester skill selection metadata | unmerged-large |
| mind-sol-00f95a-confirm | 18b03f5e8 | 1/28 | 2026-09-24 | li | Confirm existing Flow bindings from durable evidence | unmerged-small |
| mind-sol-00f95a-confirm-runtime | d5e1305bf | 3/28 | 2026-09-24 | li | Fail closed for unmanifested existing-flow skills | unmerged-small |
| mind-sol-00f95a-recovery | 87e41bc66 | 1/28 | 2026-09-24 | li | Add durable requester-neutral Field recovery admission | unmerged-small |
| mind-sol-00f95a-recovery-manifest | 279fcdc07 | 2/28 | 2026-09-24 | li | Pin Lojix recovery manifest contract inputs | unmerged-small, hotfix-or-pin-like |
| mind-sol-6288d1-bind-existing-v2 | 6ed7d1742 | 0/29 | 2026-09-24 | li | Add verified existing-flow binding | merged-not-deleted |
| mind-sol-6288d1-clippy | 82bf8003a | 0/33 | 2026-09-24 | li | Fix collapsible exact-session response check | merged-not-deleted |
| mind-sol-6288d1-codex-next | 149120f82 | 0/28 | 2026-09-24 | li | mind-sol-6288d1-codex-next / Route Codex by immutable endpoint | merged-not-deleted |
| mind-sol-6288d1-delayed-receipt | df1c0c5c2 | 0/32 | 2026-09-24 | li | Fix delayed receipt promotion fixture | merged-not-deleted |
| mind-sol-6288d1-gate-integration | 456045364 | 0/30 | 2026-09-24 | li | Integrate receipt fixture gate fixes | merged-not-deleted |
| mind-sol-6288d1-receipt-cursor | a80dc79f9 | 0/32 | 2026-09-24 | li | Fix receipt cursor regression fixture | merged-not-deleted |
| native-main-replacement-eb7bae | 5179906c2 | 17/59 | 2026-09-23 | li | Add receipt-backed native MAIN replacement fixture | unmerged-large |
| night-messaging-0ab019 | e387576f5 | 1/59 | 2026-09-19 | li | Use a single Datom payload for the Flow CLI | unmerged-small |
| night-messaging-flow-delivery-store-f72ab7 | 92d0694f3 | 6/59 | 2026-09-21 | li | Allow verified binding replay history update | unmerged-large |
| night-messaging-flow-lock-keys-f72ab7 | cd752e0f2 | 21/59 | 2026-09-22 | li | Emit resolved Flow Git source keys | unmerged-large |
| night-messaging-flow-lock-resolver-f72ab7 | db85d3294 | 20/59 | 2026-09-22 | li | Add remote Flow lock resolver and crash ownership fixture | unmerged-large |
| night-messaging-flow-meta-v3-pin-f72ab7 | d9427ec81 | 18/59 | 2026-09-21 | li | Pin Flow to repinned meta delivery producer | unmerged-large, hotfix-or-pin-like |
| night-messaging-flow-producer-pins-f72ab7 | b3592cf6c | 7/59 | 2026-09-21 | li | Pin Flow consumers to delivery signal producers | unmerged-large, hotfix-or-pin-like |
| night-messaging-flow-runtime-f72ab7 | cc9e7f9d9 | 5/59 | 2026-09-21 | li | Add Flow Nexus kernel peer runtime dependency | unmerged-small |
| night-messaging-flow-store-ownership-f72ab7 | bb36630b8 | 16/59 | 2026-09-21 | li | Test Flow store exclusive live ownership | unmerged-large |
| night-messaging-flow-store-ownership-v2-f72ab7 | aa13ff690 | 17/59 | 2026-09-21 | li | Test Flow store alias and raw engine ownership | unmerged-large |
| night-messaging-flow-tombstone-f72ab7 | 87bd74bd4 | 19/59 | 2026-09-21 | li | Test Flow completed-attempt tombstone refusal | unmerged-large |

Worktrees:
```
/git/github.com/LiGoldragon/flow                                       5e1382f (detached HEAD)
/home/li/wt/github.com/LiGoldragon/flow/launch-profile-47764b          be898a4 [flow/launch-profile-47764b]
/home/li/wt/github.com/LiGoldragon/flow/start-store-47764b             33b9f60 [flow/start-store-47764b]
/home/li/wt/github.com/LiGoldragon/flow/transcript-schema-repin-47764b 4c985b6 [flow/transcript-schema-repin-47764b]
/tmp/field753-flow-pending                                             481b690 [field-pending-recovery-753e69]
```
jj workspaces:
```
bind-existing-runtime-47764b: ../../../../home/li/wt/github.com/LiGoldragon/flow/bind-existing-runtime-47764b ylwmuksk 50786ffa (empty) Implement privileged existing Flow binding
claude-launch-rule-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/flow/claude-launch-rule-00f95a rlmtmmow 142253c5 (empty) (no description set)
default: . nxuskrzm c9023950 (empty) (no description set)
field-herdr-codex-session-5f38bc: ../../../../home/li/wt/github.com/LiGoldragon/flow/field-herdr-codex-session-5f38bc uzmowxxp 0369985a (empty) (no description set)
luna6-flow06-404d1ee: ../../../../home/li/wt/github.com/LiGoldragon/flow/luna6-flow06-404d1ee luurkzlz 0377ce3e (empty) Luna6 isolated immutable Flow 0.6 activation build workspace
marker-pane-witness-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/flow/marker-pane-witness-00f95a zqrwlzls 41220f68 (empty) (no description set)
mind-low-launch-e798f3: ../../../../home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3 ovtytwzt 9514b2f9 (empty) (no description set)
mind-medium-delivery-2c61af: ../../../../home/li/wt/github.com/LiGoldragon/flow/mind-medium-delivery-2c61af wurquuzv 8ee58b2f (empty) (no description set)
mind-sol-00f95a-bind-evidence: ../../../../home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-bind-evidence wmyozssp 4a2a9736 (empty) (no description set)
mind-sol-00f95a-confirm: ../../../../home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-confirm myurskuo 4dcafe6c (empty) (no description set)
mind-sol-00f95a-flow-basics: ../../../../home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-flow-basics wmoyvyxv 5fd439a2 (empty) (no description set)
mind-sol-00f95a-recovery: ../../../../home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-recovery lqmoosum 355e9d24 (empty) (no description set)
native-herdr-launch-47764b: ../../../../home/li/wt/github.com/LiGoldragon/flow/native-herdr-launch-47764b ytrwtsrs 161a8edd (empty) (no description set)
night-messaging-0ab019: ../../../../home/li/wt/github.com/LiGoldragon/flow/night-messaging-0ab019 sxrosuuy c899629b (empty) (no description set)
root-replacement-eb7bae: ../../../../home/li/wt/github.com/LiGoldragon/flow/root-replacement-eb7bae zmyyzlup 5179906c native-main-replacement-eb7bae | Add receipt-backed native MAIN replacement fixture
```

## messenger-clj

Remote: `ssh://git@github.com/LiGoldragon/messenger-clj.git`; base: remote main dfcf91f0f (present locally); heads: 4

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| clojure | 9176503a8 | 0/11 | 2026-09-25 | li | Make HM presentation ledger test order independent | merged-not-deleted |
| m1-sender-aspect-model-38de5b | 5171131d4 | 3/8 | 2026-09-25 | li | Require the launcher receipt to name the registering Flow | unmerged-small |
| m6-nix-38de5b | dd358c455 | 1/8 | 2026-09-25 | li | Build messenger-clj on clj-build; run the bb tests as a flake check | unmerged-small |

Worktrees:
```
/git/github.com/LiGoldragon/messenger-clj 7474199 (detached HEAD)
```
jj workspaces:
```
clojure-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/HackyMessenger/clojure-00f95a tlqumyqw 45251577 (empty) (no description set)
default: . qtsuqswm 06de0baa (empty) (no description set)
messenger-clj-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/messenger-clj/rename-00f95a sxkoxspq 17cbf279 (empty) (no description set)
route-identity-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/messenger-clj/route-identity-00f95a mxyvnwrx 4bbb8244 (empty) (no description set)
```

## field-clj

Remote: `ssh://git@github.com/LiGoldragon/field-clj.git`; base: remote main 75d77597b (present locally); heads: 1

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|

Worktrees:
```
/git/github.com/LiGoldragon/field-clj 75d7759 (detached HEAD)
```
jj workspaces:
```
default: . yyznsuqr 62ad901a (empty) (no description set)
```

## clj-build

Remote: `git@github.com:LiGoldragon/clj-build`; base: remote main 9c1778b23 NOT local; using local origin/main a1544de56; heads: 1

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|

Worktrees:
```
/git/github.com/LiGoldragon/clj-build a1544de (detached HEAD)
```
jj workspaces:
```
default: . puszmtpw 40bc0a3c (empty) (no description set)
```

## aggregator

Remote: `git@github.com:LiGoldragon/aggregator.git`; base: remote main cc3ec4fd5 NOT local; using local origin/main 01fba5e7b; heads: 2

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| f6db8d-cargo-update | 7ef8d506e | 1/5 | 2026-09-11 | li | cargo update (lockfile only) — FAILED | unmerged-small |

Worktrees:
```
/git/github.com/LiGoldragon/aggregator 01fba5e (detached HEAD)
```
jj workspaces:
```
default: . knowwnzm 0b348c80 (empty) (no description set)
```

## message

Remote: `git@github.com:LiGoldragon/message.git`; base: remote main 933064073 (present locally); heads: 40

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| cluster-relay-cf7879 | 08208fd89 | 0/38 | 2026-09-15 | li | Require explicit relay source and executor identities | merged-not-deleted |
| flow-delivery-poc | 5d917535e | 2/47 | 2026-09-16 | li | Make the flow park lose no words: atomic landing, arrival order, conflict refusa | unmerged-small |
| flow/message-lifecycle-hold-47764b | 75356175b | 1/1 | 2026-09-24 | li | Hold Pending Flow deliveries before transport | unmerged-small |
| flow/message-lifecycle-v3-47764b | a283368d1 | 3/1 | 2026-09-24 | li | Consume typed Flow v3 recipient dispositions | unmerged-small |
| integrated-messenger-poc-34d94e | a778465f9 | 17/50 | 2026-09-14 | li | Count safe retry attempts and reconcile ambiguous prompt delivery | unmerged-large |
| message-store-migration-cf7879 | 6de830a52 | 3/47 | 2026-09-15 | li | Block v3 rollout on unresolved pending delivery | unmerged-small |
| messenger-fixture-34d94e | 220bef242 | 0/51 | 2026-09-13 | li | Prove v4 ledger migration preserves catalog identity | merged-not-deleted, hotfix-or-pin-like |
| messenger-thread-slot | 82f55d64a | 0/74 | 2026-07-10 | li | messenger: carry explicit thread name through daemon + CLI (message v0.6.0) | merged-not-deleted |
| mind-sol-00f95a-recipient-presentation | 8aa6d7b46 | 3/1 | 2026-09-24 | li | Present hash-free recipient datoms at Herdr boundary | unmerged-small |
| mind-sol-6288d1-message-v2-pending | a8c6a924d | 2/1 | 2026-09-24 | li | Integrate Pending delivery hold with Flow v2 signal | unmerged-small |
| mind-sol-6288d1-signal-flow-v2 | 2951857c7 | 1/1 | 2026-09-24 | li | Pin Message to Flow v2 signal | unmerged-small, hotfix-or-pin-like |
| night-messaging-delivery-gate-draft-f72ab7 | 8a6e88ff1 | 1/0 | 2026-09-20 | li | Checkpoint untested in-memory delivery gate draft | unmerged-small |
| night-messaging-message-delivery-f72ab7 | 580021b93 | 2/0 | 2026-09-21 | li | Draft durable single-recipient Message delivery attempts | unmerged-small |
| night-messaging-message-flow-permit-f72ab7 | f6bf5a1c3 | 4/0 | 2026-09-21 | li | Add typed Message Flow permit bridge seam | unmerged-small |
| night-messaging-message-flow-permit-transport-f72ab7 | 18e14e357 | 7/0 | 2026-09-21 | li | Transport Flow permit queries over Message Flow socket | unmerged-large |
| night-messaging-message-lock-keys-f72ab7 | 917934a2f | 10/0 | 2026-09-22 | li | Emit resolved Message Git source keys | unmerged-large |
| night-messaging-message-lock-resolver-f72ab7 | 94965050a | 9/0 | 2026-09-22 | li | Add remote Message lock resolver | unmerged-large |
| night-messaging-message-producer-pins-f72ab7 | af8567cea | 3/0 | 2026-09-21 | li | Pin Message to delivery signal successors | unmerged-small, hotfix-or-pin-like |
| night-messaging-message-refusal-pin-f72ab7 | 5f85191a0 | 5/0 | 2026-09-21 | li | Pin Message to typed delivery refusal producer | unmerged-small, hotfix-or-pin-like |
| night-messaging-message-visibility-borrow-f72ab7 | f3f03755a | 8/0 | 2026-09-22 | li | Preserve delivery submission while selecting visibility | unmerged-large |
| night-messaging-message-visibility-f72ab7 | 3ba5d9465 | 6/0 | 2026-09-21 | li | Refuse unauthorized Raw and unavailable FlowLocked delivery | unmerged-large |
| nota-dependency-rename | e62acf5ad | 0/81 | 2026-06-29 | li | message update nota dependency names | merged-not-deleted |
| proposal/6852f4-schema3-converter | da9792a2f | 12/13 | 2026-09-17 | li | Make schema3 publication commit boundary final | unmerged-large |
| proposal/6852f4-schema3-probe | 3effa3d1e | 8/13 | 2026-09-17 | li | Refuse empty schema3 probe inputs | unmerged-large |
| proposal/6852f4-schema3-probe-stage-classifier | ef8f09e81 | 9/13 | 2026-09-17 | li | Classify schema3 probe failure stages | unmerged-large |
| proposal/6852f4-schema3-probe-stage-consumer | 02a115ce3 | 10/13 | 2026-09-17 | li | Report typed schema3 probe failure stages | unmerged-large |
| proposal/cf7879-message-cluster-datom-cli | 5df05aa78 | 1/50 | 2026-09-16 | li | Verify producer ClusterMessage Datoms before adapter delivery | unmerged-small |
| proposal/cf7879-message-cluster-datom-cli-forward | 181412aeb | 0/12 | 2026-09-16 | li | Verify producer ClusterMessage Datoms before adapter delivery | merged-not-deleted |
| proposal/cf7879-message-cluster-send | 9d8cdbb29 | 1/12 | 2026-09-16 | li | Send verified ClusterMessage Datoms through Flow prompt-relay routes | unmerged-small |
| proposal/cf7879-message-cluster-send-forward | 5e0e0e8a7 | 2/12 | 2026-09-16 | li | Add Codex acknowledgments to Flow ClusterMessage send bridge | unmerged-small |
| proposal/cf7879-message-idle-normal-signed-upstream | 12b48e4ef | 0/37 | 2026-09-15 | li | Cover repeated public idle announcements | merged-not-deleted |
| proposal/cf7879-message-ordinary-claude-parser-preserved-2ba7a9d3 | 2ba7a9d33 | 1/27 | 2026-09-16 | li | Exclude serialized relay records from source selection | unmerged-small |
| proposal/cf7879-message-ordinary-claude-parser-preserved-78ad6915 | 78ad69159 | 1/24 | 2026-09-16 | li | Restrict cross-session relay envelope exclusion | unmerged-small |
| proposal/cf7879-message-ordinary-claude-parser-signed-upstream | a6f65ed03 | 0/16 | 2026-09-16 | li | Prove parked relay identity follows source | merged-not-deleted |
| proposal/cf7879-message-peer-integration | b472dce49 | 0/10 | 2026-09-16 | li | Include cluster fixtures in Nix source | merged-not-deleted |
| proposal/cf7879-message-relay-nix-checks-signed-upstream | 612cf22b4 | 0/36 | 2026-09-15 | li | Add focused Nix checks for idle and relay fixtures | merged-not-deleted |
| proposal/cf7879-message-relay-readiness | fe0d04561 | 0/13 | 2026-09-16 | li | Isolate Message daemon process tests from HOME | merged-not-deleted |
| proposal/cf7879-process-boundary-home-isolation-v2 | b8df67c89 | 1/20 | 2026-09-16 | li | Isolate Message daemon process tests from HOME | unmerged-small |
| synchronizer | 846318b16 | 0/75 | 2026-07-10 | li | synchronizer: repoint message onto consolidated nota.git track + note messenger  | merged-not-deleted |

Worktrees:
```
/git/github.com/LiGoldragon/message 55657f4 (detached HEAD)
```
jj workspaces:
```
893603-receipt-query: ../../../../home/li/wt/github.com/LiGoldragon/message/893603-receipt-query rlzxlrtk 26a2b21c (empty) (no description set)
cluster-relay-cf7879: ../../../../home/li/wt/github.com/LiGoldragon/message/cluster-relay-cf7879 syonqywp 14a30920 (empty) (no description set)
default: . wxvqsmrv f28c8b60 (empty) (no description set)
designer-doc-drift-2026-06-07: ntqlvwmu 21531a5d (empty) (no description set)
integrated-messenger-poc-34d94e: ../../../../home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e xovkzrtv e334fb47 (no description set)
message-lifecycle-47764b: ../../../../home/li/wt/github.com/LiGoldragon/message/message-lifecycle-47764b vmpmovxs 01573c4f (empty) (no description set)
messenger-fixture-34d94e: ../../../../home/li/wt/github.com/LiGoldragon/message/messenger-fixture-34d94e syplvylw ca969a4c (empty) (no description set)
mind-astra-47764b-message-v3-contract: ../../../../home/li/wt/github.com/LiGoldragon/message/mind-astra-47764b-message-v3-contract qloopktx a283368d flow/message-lifecycle-v3-47764b | Consume typed Flow v3 recipient dispositions
mind-sol-00f95a-recipient-presentation: ../../../../home/li/wt/github.com/LiGoldragon/message/mind-sol-00f95a-recipient-presentation uwwootvs bdd1afa5 (empty) (no description set)
night-messaging-0ab019: ../../../../home/li/wt/github.com/LiGoldragon/message/night-messaging-0ab019 pzkpuwml 14a4b18a (empty) (no description set)
store-migration-cf7879: ../../../../home/li/wt/github.com/LiGoldragon/message/store-migration-cf7879 pzsxyxpk 9935031a (empty) (no description set)
```

## ethos-zero

Remote: `git@github.com:LiGoldragon/ethos-zero.git`; base: remote main cf7dd128b NOT local; using local origin/main 89a1ee836; heads: 6

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| ProtoformStack | 185f13a90 | 0/42 | 2026-09-04 | li | Pin datomic a27f9b8e: structural faults datomize without Debug | merged-not-deleted, hotfix-or-pin-like |
| e3-bootstrap-wip-01a04a30 | b24d7d7ff | 2/61 | 2026-08-29 | li | Emit native rkyv wire contracts from Interface files | unmerged-small, stale(28d) |
| ethos-zero-datom-nexus-542442 | 7b016f767 | 5/23 | 2026-09-06 | li | Test the Nexus offline converter from the workspace check | unmerged-small, stale(20d) |
| ethos-zero-signal-frame-542442 | bcf728bbe | 2/23 | 2026-09-05 | li | Map imported structural wire faults into generated contract faults | unmerged-small, stale(20d) |
| fix3-rkyv-recursion-38de5b | cc3e84f17 | 0/1 | 2026-09-25 | li | Regenerate inline-collision with per-item rustfmt skip; bump 11.0.0 | merged-not-deleted |

Worktrees:
```
/git/github.com/LiGoldragon/ethos-zero                                                             4bf73ca (detached HEAD)
/home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-keepgoing-6329f1                          8bcb0b9 (detached HEAD)
/tmp/claude-1001/-home-li-primary/6329f1fb-e1d1-423e-92b8-f4f786184fb4/scratchpad/ethos-zero-build 185f13a (detached HEAD)
```
jj workspaces:
```
close-e2-proof-gaps: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/close-e2-proof-gaps kyonlxnr fb1badf5 (empty) (no description set)
default: . lvkprnkm b547c1e3 (empty) (no description set)
e2-default-correction-01a04a30: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e2-default-correction-01a04a30 lznnplow 0c900355 (empty) (no description set)
e2-real-interfaces: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e2-real-interfaces woxskqlq 449b841c (empty) (no description set)
e3-bootstrap-integration: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e3-bootstrap-integration uxrsqkyz b7c2139b (empty) (no description set)
e3-nexus-runtime: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero-e3-nexus-runtime vmrxxxrp 22566dc3 (empty) (no description set)
e3-runtime-audit: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e3-runtime-audit ozvnsxpl 1ad4c8c7 (empty) (no description set)
e3-runtime-final-audit: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e3-runtime-final-audit xzunxsov 0663115d (empty) (no description set)
e3-runtime-ordering: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e3-runtime-ordering qvumrqvs b8b19c60 (empty) (no description set)
e3-wire-producer-01a04a30: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e3-wire-producer-01a04a30 rvmlnysz 7419277e (empty) (no description set)
e3-wire-producer-correction: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/e3-wire-producer-correction kknpnkww f579dc42 (empty) (no description set)
ethos-binding-542442: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-binding-542442 kozswvxo be1909c5 (empty) (no description set)
ethos-zero-ProtoformStack-6329f1: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-ProtoformStack-6329f1 kxrrwvyz 66319c42 (empty) (no description set)
ethos-zero-derives-6329f1: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-derives-6329f1 oulpzxrl e9e099f2 (empty) (no description set)
ethos-zero-e3-wire-root-envelope: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero-e3-wire-root-envelope svlompux 35e0ccbf (empty) (no description set)
ethos-zero-signal-frame-542442: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-signal-frame-542442 qussvkvn 887aad73 (empty) (no description set)
horizon-named-fields: ../../../../home/li/wt/github.com/LiGoldragon/ethos-zero/horizon-named-fields pnuklkso bf3e7144 (empty) (no description set)
```

## signal-flow

Remote: `git@github.com:LiGoldragon/signal-flow.git`; base: remote main 79792ace9 NOT local; using local origin/main 74a47edc3; heads: 13

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| flow/basic-commands-00f95a | 569f14203 | 0/9 | 2026-09-24 | li | Add basic Flow command contract | merged-not-deleted |
| flow/launch-profile-47764b | 8e821aff4 | 0/15 | 2026-09-23 | li | Add typed Flow launch profile contract | merged-not-deleted |
| flow/lifecycle-contract-47764b | afcdf076a | 1/10 | 2026-09-24 | li | Define typed Flow refresh lifecycle contract | unmerged-small |
| flow/lifecycle-implementation-refusal-47764b | fa326ac00 | 2/10 | 2026-09-24 | li | Add honest unavailable refresh implementation refusal | unmerged-small |
| flow/pane-presentation-00f95a | 7ba21d091 | 0/8 | 2026-09-24 | li | Add typed Flow presentation receipts | merged-not-deleted |
| flow/start-store-47764b | edfea8712 | 0/10 | 2026-09-23 | li | Bind native skill selections to launch receipts | merged-not-deleted |
| flow/system-prompt-bundle-00f95a | ab7033227 | 0/7 | 2026-09-25 | li | Add Flow system-prompt bundle file to launch profile | merged-not-deleted |
| mind-sol-6288d1-escalation-contract | 755186e97 | 3/10 | 2026-09-24 | li | Add same-aspect delivery escalation contract | unmerged-small |
| night-messaging-flow-delivery-signal-f72ab7 | c601a92dd | 1/16 | 2026-09-21 | li | Author Flow delivery permit Signal contract draft | unmerged-small |
| night-messaging-flow-delivery-signal-v2-f72ab7 | 22e9b80c0 | 2/16 | 2026-09-21 | li | Generate Flow delivery permit signal contract v2 | unmerged-small |
| night-messaging-flow-delivery-signal-v3-f72ab7 | 1a8bb1986 | 3/16 | 2026-09-21 | li | Represent optional delivery permits in Flow signal v3 | unmerged-small |
| night-messaging-flow-verifier-refusal-f72ab7 | 68fd1ad9e | 4/16 | 2026-09-22 | li | Add Flow verifier-unavailable refusal | unmerged-small |

Worktrees:
```
/git/github.com/LiGoldragon/signal-flow                              968ae3b (detached HEAD)
/home/li/wt/github.com/LiGoldragon/signal-flow/launch-profile-47764b 8e821af [flow/launch-profile-47764b]
/home/li/wt/github.com/LiGoldragon/signal-flow/start-store-47764b    edfea87 [flow/start-store-47764b]
```
jj workspaces:
```
default: . yopoxxyy 5180d929 (empty) (no description set)
marker-pane-witness-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/signal-flow/marker-pane-witness-00f95a wootkvxr 80c1b238 (empty) (no description set)
mind-astra-47764b-lifecycle-contract: ../../../../home/li/wt/github.com/LiGoldragon/signal-flow/mind-astra-47764b-lifecycle-contract wmtnqupz fa326ac0 flow/lifecycle-implementation-refusal-47764b | Add honest unavailable refresh implementation refusal
mind-sol-00f95a-basic-commands: ../../../../home/li/wt/github.com/LiGoldragon/signal-flow/mind-sol-00f95a-basic-commands rwptrtmp e444c9d0 (empty) (no description set)
night-messaging-0ab019: ../../../../home/li/wt/github.com/LiGoldragon/signal-flow/night-messaging-0ab019 vzvrttxy f03ffc78 (no description set)
```

## meta-signal-flow

Remote: `git@github.com:LiGoldragon/meta-signal-flow.git`; base: remote main aa489f6ab NOT local; using local origin/main fbfe89702; heads: 15

| branch | rev | ahead/behind | last commit | author | subject | class |
|---|---|---|---|---|---|---|
| flow/basic-commands-00f95a | 23b12fdbf | 0/10 | 2026-09-24 | li | Repin meta Flow contract for basic commands | merged-not-deleted, hotfix-or-pin-like |
| flow/bind-existing-47764b | 164ae716d | 0/12 | 2026-09-24 | li | Add privileged existing Flow binding contract | merged-not-deleted |
| flow/launch-profile-47764b | 465577e2f | 0/21 | 2026-09-23 | li | Repin meta Flow signal contract | merged-not-deleted, hotfix-or-pin-like |
| flow/lifecycle-refusal-pin-47764b | 1539513d9 | 0/13 | 2026-09-24 | li | Repin privileged Flow contract to honest refresh refusal | merged-not-deleted, hotfix-or-pin-like |
| flow/lifecycle-v3-47764b | 9cd6fb93d | 0/15 | 2026-09-24 | li | Repin privileged Flow contract to lifecycle v3 | merged-not-deleted, hotfix-or-pin-like |
| flow/lifecycle-v3-digest-47764b | fcf0a0b24 | 0/14 | 2026-09-24 | li | Bind privileged wire digest to lifecycle v3 | merged-not-deleted |
| flow/pane-presentation-00f95a | 85a5d40c4 | 0/9 | 2026-09-24 | li | Repin Flow presentation receipt contract | merged-not-deleted, hotfix-or-pin-like |
| flow/start-store-47764b | 192e1a8a7 | 0/16 | 2026-09-23 | li | Repin native skill receipt schema | merged-not-deleted, hotfix-or-pin-like |
| flow/system-prompt-bundle-00f95a | a34bc6528 | 0/8 | 2026-09-25 | li | Repin Flow signal contract for bundle launch profile | merged-not-deleted, hotfix-or-pin-like |
| mind-astra-47764b-confirm-existing | 9ae6e6205 | 1/11 | 2026-09-24 | li | Add existing flow confirmation contract | unmerged-small |
| mind-medium-meta-flow-v3-2c61af | c61099aa7 | 2/22 | 2026-09-21 | li | Repin meta Flow Signal contract to v3 | unmerged-small, hotfix-or-pin-like |
| mind-medium-privileged-registration-2c61af | 93d867a27 | 1/22 | 2026-09-21 | li | Add privileged binding registration correlation contract | unmerged-small |
| mind-sol-00f95a-confirm | 7a4eb7772 | 3/11 | 2026-09-24 | li | Refuse existing bindings without native evidence | unmerged-small |
| mind-sol-6288d1-bind-v2 | 71e92386a | 0/11 | 2026-09-24 | li | Adapt existing binding contract to Flow v2 | merged-not-deleted |

Worktrees:
```
/git/github.com/LiGoldragon/meta-signal-flow                                aa61040 (detached HEAD)
/home/li/wt/github.com/LiGoldragon/meta-signal-flow/bind-existing-47764b    164ae71 [flow/bind-existing-47764b]
/home/li/wt/github.com/LiGoldragon/meta-signal-flow/confirm-existing-47764b 9ae6e62 [mind-astra-47764b-confirm-existing]
/home/li/wt/github.com/LiGoldragon/meta-signal-flow/launch-profile-47764b   465577e [flow/launch-profile-47764b]
/home/li/wt/github.com/LiGoldragon/meta-signal-flow/start-store-47764b      192e1a8 [flow/start-store-47764b]
```
jj workspaces:
```
default: . lzptpmrs a194d8d8 (empty) (no description set)
marker-pane-witness-00f95a: ../../../../home/li/wt/github.com/LiGoldragon/meta-signal-flow/marker-pane-witness-00f95a syqntntv b26faa49 (empty) (no description set)
mind-astra-47764b-lifecycle-v3: ../../../../home/li/wt/github.com/LiGoldragon/meta-signal-flow/mind-astra-47764b-lifecycle-v3 sokmqywy 1539513d flow/lifecycle-refusal-pin-47764b | Repin privileged Flow contract to honest refresh refusal
mind-medium-privileged-registration-2c61af: ../../../../home/li/wt/github.com/LiGoldragon/meta-signal-flow/mind-medium-privileged-registration-2c61af lvkkmsuw 11a75743 (empty) (no description set)
mind-sol-00f95a-basic-commands: ../../../../home/li/wt/github.com/LiGoldragon/meta-signal-flow/mind-sol-00f95a-basic-commands nurpnzqw 5f6311c5 (empty) (no description set)
mind-sol-00f95a-confirm: ../../../../home/li/wt/github.com/LiGoldragon/meta-signal-flow/mind-sol-00f95a-confirm smsvmnuk 2e25563f (empty) (no description set)
```

## primary

Remote: `git@github.com:LiGoldragon/primary.git`; base: remote main d2eb5a239 (present locally); heads: 106 (105 non-main). Listed by family, not individually.

| family | count | newest commit | merged (ahead 0) | unmerged |
|---|---|---|---|---|
| draft/* | 2 | 2026-09-15 | 0 | 2 |
| field* | 11 | 2026-09-23 | 5 | 6 |
| flow/* | 14 | 2026-09-19 | 3 | 11 |
| integration-deployment-4a8046-* | 4 | 2026-09-05 | 3 | 1 |
| other | 9 | 2026-09-22 | 5 | 4 |
| preserve/* | 7 | 2026-07-07 | 0 | 7 |
| proposal/* | 25 | 2026-09-17 | 1 | 24 |
| push-* | 33 | 2026-09-25 | 30 | 3 |

Family `other`: claude/workspace-agent-remote-access-zjj9rb core-checkup-cf7879 group-17-5f4fea harness-visual-indicators-753e69 primary-next-source-inventory-893603 psyche-harness-vision-753e69 relay-parser-cf7879 transitive-network-topology-753e69 worktree-flow-48cff7 

Worktrees:
```
/home/li/primary                                                     c85d1e6d4 (detached HEAD)
/home/li/.codex/worktrees/8673/primary                               69f687a38 (detached HEAD)
/home/li/.codex/worktrees/e217/primary                               b91e511f5 (detached HEAD)
/home/li/primary/.claude/worktrees/flow-840e42                       ac3682fe2 [worktree-flow-840e42] locked
/home/li/wt/github.com/LiGoldragon/primary/field-6db-report-20260921 1b8d1d4cf (detached HEAD)
/home/li/wt/github.com/LiGoldragon/primary/field-census-6db4fe       8c38d3b53 (detached HEAD)
/home/li/wt/github.com/LiGoldragon/primary/field-world-6db4fe        b57a43de0 (detached HEAD)
/home/li/wt/primary-5f4fea                                           88a058623 [flow/5f4fea]
/home/li/wt/primary-5f4fea-disk-retention                            f6b6c4729 [proposal/5f4fea-disk-retention]
/home/li/wt/primary-5f4fea-flow-assembler-full-context               46c6bae43 [proposal/5f4fea-flow-assembler-full-context]
/home/li/wt/primary-5f4fea-g11g12                                    ef9cf86d9 [draft/5f4fea-g11g12]
/home/li/wt/primary-5f4fea-item30                                    321050ff6 [proposal/5f4fea-item30-launcher]
/home/li/wt/primary-5f4fea-main-flow-projection                      a983f1699 [proposal/5f4fea-main-flow-projection]
/home/li/wt/primary-5f4fea-main-subflow-projection                   a983f1699 [proposal/5f4fea-main-subflow-projection]
/home/li/wt/primary-cf7879                                           88a058623 (detached HEAD)
/home/li/wt/primary-eae736-closure                                   197997d0e [flow/eae736]
/home/li/wt/primary-fd0f97                                           fb6e00b82 [flow/fd0f97]
/home/li/wt/primary/field-census-9ddcbc                              fdb2c1c0f [field-census-9ddcbc]
/home/li/wt/primary/field-checkup-shadow-9ddcbc                      244f338ef [field-checkup-shadow-9ddcbc]
/home/li/wt/primary/field-high-main-merge-753e69                     9427c0cd8 [field-high-main-merge-753e69]
/home/li/wt/primary/field-high-refresh-753e69                        a0fa9d530 [field-astra-refresh-03e825-753e69]
/home/li/wt/primary/field-merge-9ddcbc                               1cb65aa2c [field/merge-9ddcbc]
/home/li/wt/primary/field-network-main-753e69                        c078012e2 [field-network-main-753e69]
/home/li/wt/primary/field-rollout-plan-9ddcbc                        5da0093c2 [field/rollout-plan-9ddcbc]
/home/li/wt/primary/harness-visual-indicators-753e69                 443550140 [harness-visual-indicators-753e69]
/home/li/wt/primary/psyche-harness-vision-753e69                     47ce0aa71 [psyche-harness-vision-753e69]
/home/li/wt/primary/psyche-harness-vision-main-753e69                706080d0f [psyche-harness-vision-main-753e69]
/home/li/wt/primary/transitive-network-topology-753e69               8433b2193 [transitive-network-topology-753e69]
/tmp/field753-primary-fallback                                       4c0469d4f [field-flow-fallback-753e69]
/tmp/field753-primary-oVpaNZ                                         5579e9cb7 [field-flow-preflight-753e69]
```
jj workspaces:
```
MigrateFlow01a02400: swwtwwuu 90d9419b (empty) (no description set)
MindJudgePromptRewrite-NarrowThirdPass: ../primary-worktrees/MindJudgePromptRewrite-NarrowThirdPass yyossuqo 08a3fc0f mind-judge-prompt-third-pass
MindJudgePromptRewrite-TargetedSecondPass: ../primary-worktrees/MindJudgePromptRewrite-TargetedSecondPass usvyxuqr 4a5b3d4f mind-judge-targeted-second-pass
SessionMigrationWave5A: vpzymqzt f6e17c85 (empty) (no description set)
VisionMigrationWave5B: wskptssk 30ce57b6 (empty) (no description set)
cf7879: ../wt/github.com/LiGoldragon/primary/cf7879 vqtpuryx 71e7a656 (empty) (no description set)
cf7879-jj-law: ../wt/github.com/LiGoldragon/primary/cf7879-jj-law zsmqnzyz c1586f8f (empty) (no description set)
claude-env-6db4fe: ../wt/github.com/LiGoldragon/primary/claude-env-6db4fe wmklqoys 9d96416f (empty) (no description set)
claude-prompt-hook-cf7879: ../wt/github.com/LiGoldragon/primary/claude-prompt-hook-cf7879 nzyovqux 6de3528a (empty) (no description set)
claude-successor-840e42: ../wt/github.com/LiGoldragon/primary/claude-successor-840e42 vwxrntkz ba30ad9e (empty) (no description set)
clusterrelay-context-cf7879: ../wt/github.com/LiGoldragon/primary/clusterrelay-context-cf7879 ssoppkpm c64d583f (empty) (no description set)
core-bootstrap-cf7879: ../wt/github.com/LiGoldragon/primary/core-bootstrap-cf7879 trmxwvto 0731ea99 (empty) (no description set)
core-checkup-cf7879: ../wt/github.com/LiGoldragon/primary/core-checkup-cf7879 qyyuommu 13fb3c4d core-checkup-cf7879 | (empty) Integrate harness facts with roster policy runner
core-e43002: ../wt/github.com/LiGoldragon/primary/core-e43002 zvrvuqom 3ba2bb95 (empty) (no description set)
core-harness-facts-cf7879: ../wt/github.com/LiGoldragon/primary/core-harness-facts-cf7879 wsusnukq 5b04df60 (empty) (no description set)
curriculum-deploy-datom-pin-542442: ../wt/github.com/LiGoldragon/primary/curriculum-deploy-datom-pin-542442 lnuurztv 5898fa71 (empty) (no description set)
curriculum-testing-continuity-6db4fe: ../wt/github.com/LiGoldragon/primary/curriculum-testing-continuity-6db4fe pkmtmlwo fc2aa73f (empty) (no description set)
default: . mvnuxops 777d6ba1 (no description set)
fable-bootstrap-enforcement: ../wt/github.com/LiGoldragon/primary/fable-bootstrap-enforcement qvyzkltx bbdca8d7 (empty) (no description set)
fable-receipt-handoff: ../wt/github.com/LiGoldragon/primary/fable-receipt-handoff tsqkyvuq 6c8dacf4 (empty) (no description set)
field-opencode-terra-1cb440: ../wt/primary-field-opencode-terra-1cb440 nuszvnvy 2d647c2c (empty) (no description set)
flow-architecture-01a05e95: ../wt/github.com/LiGoldragon/primary/flow-architecture-01a05e95 pzkqxuty de2bf9b0 (empty) (no description set)
flow-id-01a05e95: ../wt/github.com/LiGoldragon/primary/flow-id-01a05e95 ptzykyxn 50ac709b (empty) (no description set)
flow-message-vm-6db4fe: ../wt/github.com/LiGoldragon/primary/flow-message-vm-6db4fe pnnovrmq 6b53caaa (empty) (no description set)
group-17-5f4fea: ../wt/github.com/LiGoldragon/primary/group-17-5f4fea zoqyxqpt e312cc2f (empty) (no description set)
heartbeat-cf7879: ../wt/github.com/LiGoldragon/primary/heartbeat-cf7879 tootwtzl 2157d698 (empty) (no description set)
jj-global-law-cf7879: ../wt/github.com/LiGoldragon/primary/jj-global-law-cf7879 yzkyvrox 19db9ccb (empty) (no description set)
mainflow-launch-fix-cf3553: ../wt/github.com/LiGoldragon/primary/mainflow-launch-fix-cf3553 pottwkru 54218fc0 (empty) (no description set)
messaging-relay-25c4ac: ../primary-worktrees/messaging-relay-25c4ac wopuqsol 10bc6820 (empty) (no description set)
migrate-historical-child-flows: ../wt/github.com/LiGoldragon/primary/migrate-historical-child-flows uwlkmyux 11dd7df2 (empty) (no description set)
mind-judge-fixture-label-cleanup: ../primary-worktrees/mind-judge-fixture-label-cleanup mxzlpzwx 702c2932 mind judge fixture label cleanup
mind-live-judge-eval-rerun: qqnqzrwn 501a31a9 (empty) mind-live-judge-eval-rerun
mind-vision-00f95a: ../wt/primary/mind-vision-00f95a qvzoykyx 2594a810 (empty) (no description set)
mind-vision-main-00f95a: ../wt/primary/mind-vision-main-00f95a vyrroquy bed3525c (empty) (no description set)
primary-840e42-3b1574: ../wt/primary/primary-840e42-3b1574 wkyzykut 396070bf (empty) (no description set)
primary-field-reaping: ../wt/primary-field-reaping pntkqrkq 534e354f (empty) (no description set)
primary-fix-audit-stale-repo-operator: vnrmzllx ad45409a (no description set)
primary-fix-audit-stale-repo-operator-v2: ooutproq 6290d4b9 (empty) (no description set)
primary-integration-witness-final-4a8046: ../wt/github.com/LiGoldragon/primary-integration-witness-final-4a8046 pqukxrmn 14c6b834 (empty) (no description set)
primary-next-report-893603: ../primary-worktrees/primary-next-report-893603 otxsovpz 351498a4 (empty) (no description set)
primary-orchestrate-release.Gg5sgR: wsrsnrvo 6be2bde3 (empty) (no description set)
prompt-datom-cf7879: ../wt/github.com/LiGoldragon/primary/prompt-datom-cf7879 pykyrxry 9caafa8d proposal/cf7879-prompt-relay-datom | Bind transcript renderer to the selected source event
relay-gate-cf7879: ../wt/github.com/LiGoldragon/primary/relay-gate-cf7879-v2 qvlmotpy 86f98d65 (empty) (no description set)
relay-parser-cf7879: ../wt/github.com/LiGoldragon/primary/relay-parser-cf7879 mxkuntun 65184238 (empty) (no description set)
remove-project-hooks-01a033a6: ../wt/github.com/LiGoldragon/primary/remove-project-hooks-01a033a6 uxutyxvv 8fd25992 (empty) (no description set)
restore-carried-peer-state-01a033a6: ../wt/github.com/LiGoldragon/primary/restore-carried-peer-state-01a033a6 vttyusun e99bf080 (empty) (no description set)
testing-worker-report-6db4fe: ../wt/github.com/LiGoldragon/primary/testing-worker-report-6db4fe qkqsyyqv 5b2cbc14 (empty) (no description set)
wake-adapter-cf7879: ../wt/github.com/LiGoldragon/primary/wake-adapter-cf7879 zswwssrm 009e048c (empty) (no description set)
```

## Deploy-path findings

**Prometheus build source.** CriomOS `prometheus-usb-bus-property-5f38bc` (da85c4a9e) is 13 ahead / 3 behind main d193bafca. Only its tip commit (`Bind USB downlinks by stable udev bus role`; touches `checks/router-usb-downlink-binding`, `modules/nixos/network/networkd.nix`, `modules/nixos/router/default.nix`; no flake.lock change) is the USB fix. The other 12 are Home/Flow/Message/Herdr pins inherited from `field-astra-5f38bc-flow-pins` (88900f266, an ancestor), superseded by main's own Home pin (main's 3 extra commits: Flow 0.10.7 Home pin, field-clj on Ouranos). So a main deploy must carry da85c4a as a single commit rebased onto main, not a merge of the branch; otherwise main's generation lacks the USB bus-role binding Prometheus now runs.

**Competing USB approach.** `prometheus-usb-downlink-5f38bc` exists in CriomOS (de5ac1b79, 1/3, changes flake.lock+flake.nix), horizon-rs (fed0a12a3, 1/7, MAC exposure), goldragon (1781f079a, 1/0, Prometheus USB LAN hardware identity), lojix (387c13b51, 1/0, Horizon repin). This is the MAC/identity-based chain; it is not an ancestor of the bus-property branch. Merge-or-discard decision needed: if bus-role supersedes it, all four are discard candidates; merging the goldragon one alone changes cluster data without the consumer.

**Ouranos.** CriomOS `flow07-ouranos-b7da5d` (15/3) → `flow-main-opencode-luna6` (14/3) → `flow-final-aba74675-luna6` (13/3) are a stacked Home-pin chain on top of `field-astra-5f38bc-flow-pins`; main already pins Flow 0.10.7 Home, so these look superseded (discard candidates) unless OpenCode Home install is wanted. Matching CriomOS-home branches: `flow07-home-b7da5d`, `opencode-home-b7da5d(-repaired-flow)`, `flow-main-opencode-luna6`, `flow-final-*-luna6`, `prompt-relay-a07f01a-luna6` (17–21 ahead / 7 behind). goldragon `usb-gateway-data-753e69` (4/10, assigns Ouranos USB IPv4 gateway) and CriomOS `usb-gateway-consumer-6db4fe` (1/14) are unmerged; horizon-rs `usb-gateway-6db4fe` is merged.

**messenger-clj (38de5b).** `m1-sender-aspect-model-38de5b` 5171131d4, 3 ahead / 8 behind, 2026-09-25, unmerged-small. `m6-nix-38de5b` dd358c455, 1 ahead / 8 behind, 2026-09-25, unmerged-small (builds messenger-clj on clj-build, flake check). Local `main` bookmark f541c15 differs from origin/main dfcf91f (used origin). If the Ouranos Home consumes messenger-clj via Nix, m6 matters.

**CriomOS-lib** `models-da88cf` 6db67c3bd is 0/0 = main tip (merged-not-deleted; delete-safe).

## Unknowns

- clj-build, aggregator, ethos-zero, signal-flow, meta-signal-flow: the real remote main is NOT present locally (not fetched per brief); ahead/behind are against the older local origin/main, so unmerged counts may be overstated and "behind" understated. `merged-not-deleted` there still holds only if remote main fast-forwarded.
- No branch object was missing locally; every non-main head was computable.
- jj workspaces with non-empty "(no description set)" working copies may hold uncommitted work (CriomOS has ~14 such); not inspected.
- herdr: no canonical checkout; not scanned.

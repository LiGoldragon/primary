# Polling-removal source inventory and plan (stage 1)

Inventory only. No source edit, build, fetch, push, deployment, service action, or host mutation was performed.

## Isolation and revision witness

- CriomOS-home worktree: `/git/worktrees/criomos-home-polling-705e10`, branch `polling-removal-705e10`, clean base `689d72daa2da4e2c66c61e60d74474207327003f` from the already-present `refs/remotes/origin/main`.
- CriomOS worktree: `/git/worktrees/criomos-polling-705e10`, branch `polling-removal-705e10`, clean base `031b3dc68b552470e0fe62bd14fe8e6222b6c4b7` from the already-present `refs/remotes/origin/main`.
- The dirty canonical checkouts were read only for status. CriomOS-home canonical `main` was 84 commits behind its local `origin/main` and dirty; CriomOS canonical was on `flow-home-opencode-42265e` and dirty. Neither was used as an edit base.
- The supplied deployed CriomOS revision equals the isolated CriomOS base. The supplied pinned Home revision equals the isolated Home base. There is no source-revision gap at either boundary.
- Both lock files select nixpkgs `0e251e24a4f24e036a084b6b4b2d2491af4167f4`, nar hash `sha256-yNJd40f11EzXBjSByCB7IPpeFFAdeoSKKM67dGkfFoU=`. The already-present matching source is `/nix/store/31w94yhfpllma9jnlgavjkzsfs548ijx-source`; it was inspected without evaluation or network access.
- The brief's proposal path `/nix/store/s7vz81gm2mncm03mk3z7a0s5zm2kb915-horizon-definition/horizon-definition.datom` is absent. Existing Horizon store artifacts describe the node cohort below, but I cannot witness which is the named 0.16 proposal. This is an evidence gap, not a source blocker.

Host variants visible in the existing Horizon artifacts are `ouranos`, `balboa`, `mirror-alpha`, `mirror-beta`, `prometheus`, `tiger`, `vm-testing`, `zeus`, plus `live-install-graphical` and `live-install-minimal`. Home-presence variants are `li@ouranos`, `li@tiger`, `bird@tiger`, `li@zeus`, and `bird@zeus`. `prometheus` is the Router variant. TailnetClient variants are `ouranos`, `mirror-alpha`, `mirror-beta`, `prometheus`, and `vm-testing`.

## Account ledger

Each entry says what the job does, its cadence, why its presence is observed or inferred, and its proposed fate. `Observed` means the ouranos runtime worker saw the deployed unit. Other host claims are source projections and are labelled hypotheses.

### Ouranos first

1. **ouranos — Nix GC:** deletes old store paths daily. Observed active as `nix-gc.timer`; source is `CriomOS/modules/nixos/nix/retention-agent.nix:25-29`. Replace with an operator-invoked GC command; remove the timer and make automatic GC explicitly false. Retention policy needs an explicit on-demand command/options decision so deletion does not become silent.
2. **ouranos — Nix store optimisation:** deduplicates store files automatically through `nix.settings.auto-optimise-store = true` at `retention-agent.nix:23`. This is automatic work rather than a timer. Replace with operator-invoked `nix-store --optimise`; explicitly set it false.
3. **ouranos — firmware metadata refresh:** calls `fwupdmgr refresh` hourly with up to one hour random delay. Observed active; source enable is `CriomOS/modules/nixos/metal/default.nix:657-660`, and locked nixpkgs adds `fwupd-refresh.timer` at `nixos/modules/services/hardware/fwupd.nix:190-214`. Keep fwupd available, mask/disable its refresh timer, and expose the existing refresh command on demand.
4. **ouranos — filesystem trim:** trims mounted filesystems weekly. Observed active. It is an implicit locked-nixpkgs default: `nixos/modules/services/misc/fstrim.nix:16-48` defaults `services.fstrim.enable` to true. Explicitly set it false; on-demand `fstrim` remains available.
5. **ouranos — logrotate:** checks btmp/wtmp rotation hourly. Observed active. Locked nixpkgs supplies default btmp/wtmp settings at `nixos/modules/system/boot/systemd.nix:871-886`; those make `services.logrotate.enable` true, and `services/logging/logrotate.nix:309-318` uses `startAt = "hourly"`. Explicitly disable logrotate. Whether btmp/wtmp should be rotated on demand or left to a new event design needs a decision.
6. **ouranos — system tmpfiles cleanup:** removes aged temporary files 15 minutes after boot and daily thereafter. Observed active from upstream systemd; locked nixpkgs imports it at `nixos/modules/system/boot/systemd/tmpfiles.nix:231-244`. Mask `systemd-tmpfiles-clean.timer`; keep boot/setup semantics and the on-demand `systemd-tmpfiles --clean` capability.
7. **ouranos — per-user tmpfiles cleanup:** removes aged user temporary files 5 minutes after user-manager startup and daily thereafter. Observed active for `li`. Locked nixpkgs defaults `systemd.user.tmpfiles.enable = true` at `nixos/modules/system/boot/systemd/user.nix:127-138` and wants the timer at lines 226-228. Set it false; whether that option also removes wanted boot setup that is still desired must be checked in the source edit.
8. **ouranos — XFS scrub:** the upstream Sunday 03:10 timer is linked but inactive. Its declaration enters because CriomOS globally supports XFS (`modules/nixos/normalize.nix:95-101`) and locked nixpkgs adds the xfsprogs package units (`tasks/filesystems/xfs.nix:12-24`). Explicitly mask `xfs_scrub_all.timer`; retain manual `xfs_scrub_all` if wanted.
9. **ouranos — NetworkManager cloud setup:** the five-minute upstream timer is linked but inactive. NetworkManager is enabled for this desktop; its package carries the timer. Explicitly mask `nm-cloud-setup.timer`; NetworkManager dispatcher events remain the event mechanism.
10. **ouranos — Home zoekt refresh/index:** fetches every git origin and reindexes after 5 minutes, then every configured 15 minutes. Source declaration is unconditional for every Min-or-larger home at `CriomOS-home/modules/home/profiles/min/zoekt-index.nix:13-42,63-88`. The runtime worker saw only a failed linked service and no trigger, so deployment presence is not observed. Delete the timer and interval option. Desired replacement is a changed-repository hook, but the emitting hook and repository coverage need design.
11. **ouranos — context-skills backstop:** fetches three belief repositories and regenerates skills after 1 minute, then every 2 minutes. Source is `modules/home/profiles/min/context-skills.nix:35-58` plus the fetches in `packages/context-skills/regenerate.sh:3-20`; observed runtime preserved the event-driven `.path` unit, while no user timer was present. Delete the timer and periodic-fetch rationale; preserve the existing ref-path trigger. Remote changes that do not move a local ref need an explicit existing push/receive hook or a design decision.
12. **ouranos — Field Luna heartbeat:** runs bounded retirement/archive maintenance after 5 minutes and every 30 minutes, alongside an event path. Source is `profiles/min/field-luna-heartbeat.nix:18-45`; it is off unless enabled and was not observed. Delete only the timer and preserve the Hacky Messenger path trigger.
13. **ouranos — five Field monitoring jobs:** core checkup (30 min), Field census (5 min), checkup shadow (30 min), Luna research (30 min), and flow-98eb43 monitor (5 min) are independently option-gated at `profiles/min/field-monitoring.nix:98-156,182-336`; none was observed and all default off. Delete all five timer declarations. The first four need event/on-demand ownership decisions; the flow-scoped 98eb43 monitor should be gone with no replacement.
14. **ouranos — tailnet enrollment readiness loop:** on TailnetClient nodes, startup samples `tailscale status` once per second for up to 30 seconds before deciding whether to enroll (`CriomOS/modules/nixos/network/tailscale.nix:35-52`). Source hypothesis; not shown as a periodic unit. Replace with a tailscaled readiness/event contract or a single CLI operation that owns its own readiness; choice needs design.
15. **ouranos li edge UI — active-network RSSI:** the helper queries `iw ... link` every 5 seconds while Wi-Fi is active (`active_network_helper.py:188-194,313-378`). Source hypothesis. Replace with NetworkManager/nl80211 change signals, or drop live RSSI if no event carries it; needs design.
16. **ouranos li edge UI — active-network socket reconnect:** a one-second QML retry timer reconnects the local status socket (`active-network/BarWidget.qml:70-106`). Source hypothesis. Replace with socket activation/lifecycle coupling or a native connection-state notification; needs design.
17. **ouranos li edge UI — solar clock status:** reads Chroma status every minute (`solar-time/BarWidget.qml:42-71`). Source hypothesis. Replace with a Chroma-published solar-clock change event; decide whether live seconds are dropped or driven by an existing UI clock event.
18. **ouranos li edge UI — listener and transcript reconnects:** three `while true; socat ...; sleep 1` streams retry local sockets (`listener-level/level.luau:164-207`, `transcript-panel.luau:44-61`). Source hypothesis. Replace with supervised/socket-activated streams or native reconnect events; needs design.
19. **ouranos li edge UI — wispr reconnect and staleness:** a `while true` one-second reconnect loop plus a one-second staleness callback lives at `wispr-status/WisprStatusService.luau:1-47`. Source hypothesis. Replace disconnect with stream EOF state and lifecycle supervision; staleness must be emitted by the producer or removed.
20. **ouranos li edge UI — listener/wispr redraw intervals:** Noctalia callbacks redraw at 70/110/120/1000 ms to decay meters and expire transient state (`listener-level/level.luau:135-161`, `wispr-status/BarWidget.luau:83-96`). Source hypothesis. Replace with input events and explicit one-shot completion/expiry events, or simplify away animation/expiry; needs design.
21. **ouranos li edge session — lock-listener discovery:** `criomos-lock-listener` polls loginctl every two seconds without a bound before beginning its D-Bus monitor (`profiles/min/niri.nix:121-143`). Source hypothesis. Pass the session object path at service start or bind service lifetime to the graphical session; needs design.
22. **ouranos li commands — bounded readiness polling:** screenshot waits for a file 20×50 ms (`niri.nix:68-83`); Flow configuration waits for a socket 100×50 ms (`flow-nexus-version.nix:171-207`); browser automation waits for CDP 60×0.5 s or 30×0.5 s (`profiles/max/browser-use.nix:205-231,270-299`). These are source hypotheses, not recurring services. Replace with command completion/inotify, systemd socket readiness, and process-owned readiness respectively; exact interfaces need design.
23. **ouranos li edge session — delayed lock action:** `criomos-lock-session` sleeps once for three seconds before powering off monitors (`niri.nix:112-120`). This is a one-shot delay rather than polling, but it is a sleep-service declaration within the requested audit. Replace with a compositor/lock state event or remove the delayed power-off; needs design.
24. **ouranos — Codex manager heartbeat instruction:** `flow-nexus-config/metaflows.datom:23-31` tells an on-demand flow to self-pace from hourly checks. It is a periodic polling declaration in configuration data. Remove the heartbeat brief or replace it with usage-limit and flow-state events; this is likely psyche-governed text and needs main/Fable direction before changing.

### Other system host variants

25. **balboa, mirror-alpha, mirror-beta, prometheus, tiger, vm-testing, zeus, live-install-graphical, live-install-minimal — Nix GC and automatic optimisation:** the aggregate imports `retention-agent.nix` for every target, so each variant declares the same daily GC and automatic optimisation as ouranos. Source hypothesis. Apply the same explicit off/on-demand policy to all variants.
26. **balboa, mirror-alpha, mirror-beta, prometheus, tiger, vm-testing, zeus, live-install-graphical, live-install-minimal — fwupd refresh:** `metal/default.nix` enables fwupd without a hardware-kind guard, so all variants inherit the upstream refresh timer. Source hypothesis. Apply one cluster-wide timer mask while retaining on-demand fwupd where the package makes sense.
27. **balboa, mirror-alpha, mirror-beta, prometheus, tiger, vm-testing, zeus, live-install-graphical, live-install-minimal — fstrim:** locked nixpkgs defaults it on for every configuration. Source hypothesis. Set `services.fstrim.enable = false` once in the aggregate policy.
28. **balboa, mirror-alpha, mirror-beta, prometheus, tiger, vm-testing, zeus, live-install-graphical, live-install-minimal — logrotate:** locked nixpkgs btmp/wtmp defaults create the hourly timer in every configuration. Source hypothesis. Disable it once in the aggregate policy.
29. **balboa, mirror-alpha, mirror-beta, prometheus, tiger, vm-testing, zeus, live-install-graphical, live-install-minimal — system and user tmpfiles cleanup:** upstream system timer is imported for every target and the global user timer defaults enabled for every user manager. Source hypothesis. Mask system cleanup and set user tmpfiles timer policy false cluster-wide.
30. **balboa, mirror-alpha, mirror-beta, prometheus, tiger, vm-testing, zeus, live-install-graphical, live-install-minimal — XFS scrub declaration:** every target globally supports XFS, so xfsprogs contributes its weekly timer even when the installed filesystem is Ext4/Btrfs and the unit remains inactive. Source hypothesis. Mask it once cluster-wide.
31. **NetworkManager variants — nm-cloud-setup:** any variant whose projection sets `enableNetworkManager` receives the package's five-minute linked timer. Exact enabled host set was not evaluated; ouranos is witnessed. Mask it cluster-wide by unit name so host classification cannot reintroduce it.
32. **prometheus — router WAN lease recovery:** checks for carrier without a default route at 2 minutes after boot and every 2 minutes after each run (`CriomOS/modules/nixos/router/default.nix:329-344,428-437`). Source hypothesis from the Router trait. Replace with a networkd lease/carrier event hook; exact event interface needs design.
33. **mirror-alpha, mirror-beta, prometheus, vm-testing — tailnet readiness loop:** the same 30×1-second startup loop as ouranos applies through TailnetClient capability. Source hypothesis. One shared replacement covers all five clients.

### Other Home host variants

34. **li@tiger, bird@tiger, li@zeus, bird@zeus — zoekt:** all four homes are Max, so each declares the same 5-minute initial/15-minute recurring fetch-and-index job as li@ouranos. Source hypothesis. One removal plus a changed-repository hook design covers all five homes.
35. **AgentStack homes among li@tiger, bird@tiger, li@zeus, bird@zeus — context-skills:** declaration follows `criomosHome.curriculum.enable`, which `CriomOS/modules/nixos/userHomes.nix:22-31` derives from the user's `AgentStack` capability. The available datom was not decoded/evaluated far enough to assign every user-host pair. For every matching pair, remove the two-minute timer and preserve the path unit; remote-update triggering needs design.
36. **li@tiger, bird@tiger, li@zeus, bird@zeus — opt-in Field Luna heartbeat:** each home can declare the 30-minute timer when enabled. Source hypothesis; default off. Remove the timer from the reusable module and retain its path trigger.
37. **li@tiger, bird@tiger, li@zeus, bird@zeus — opt-in Field monitoring:** each home can independently enable the same five timers listed for ouranos. Source hypothesis; default off. Delete their timer declarations from the reusable module, with the same four design decisions and flow-98eb43 deletion.
38. **li@tiger, bird@tiger, li@zeus, bird@zeus — edge UI periodic work:** tiger and zeus are Edge nodes and all four homes are present there, so each inherits the active-network RSSI query/reconnect, solar status timer, listener/transcript/wispr reconnect loops, staleness callback, and redraw intervals listed for li@ouranos. Source hypothesis. The replacements must be shared plugin/helper designs rather than per-host branches.
39. **li@tiger, bird@tiger, li@zeus, bird@zeus — edge session/command waits:** each inherits the lock-listener loop, screenshot bounded wait, one-shot lock delay, Flow socket wait, and browser CDP waits where the Large/Max and endpoint predicates hold. Source hypothesis. Replace at their shared source definitions.
40. **homes with Flow metaflow configuration — Codex heartbeat:** each installed configuration carries the hourly self-paced heartbeat brief. Source hypothesis. Remove/replace once at the configuration datum after psyche authority is confirmed.

## Negative inventory and gaps

- No tracked CriomOS or CriomOS-home cron/anacron declaration was found. Runtime `/etc/crontab`, `/etc/anacrontab`, `/etc/cron.*`, and `crontab` were unavailable, so unmanaged cron remains an observation gap. The source change should explicitly set the NixOS cron enable option false if present in this nixpkgs revision.
- No tracked `updatedb`/locate schedule was found and no runtime timer was reported. The source change should explicitly disable the locate service/default so a future module cannot reintroduce it implicitly.
- No separate journal-vacuum timer was found in source or runtime. Journald size/retention enforcement occurs in the daemon rather than a declared periodic unit. No periodic declaration is currently identified; if the requirement also excludes write-triggered retention, that is a separate policy decision.
- `context-skills.path` is a filesystem event unit and is to be preserved. NetworkManager/DBus observers, socket readers, and ordinary daemons are likewise event-driven unless an internal periodic loop above was found.
- Crash-recovery `RestartSec` and protocol timeouts are not schedules. They remain unless the final ruling treats every delayed retry as periodic work.
- Tests/checks contain short sleeps and polling fixtures. They do not run on hosts, but the literal completed-state phrase “no timer/periodic declarations remain anywhere” could include them. Main must rule whether source tests are in scope; if yes, the change expands well beyond host declarations.

## Bounded source change plan after mainGO

1. Add one CriomOS cluster policy module and import it from `modules/nixos/criomos.nix`. It will explicitly disable automatic GC/optimisation, fstrim, logrotate, system/user tmpfiles cleanup timers, locate/updatedb, cron, and mask the upstream `fwupd-refresh`, `nm-cloud-setup`, and `xfs_scrub_all` timers. Keep the corresponding commands/services available only where on-demand use requires them.
2. Remove the router WAN timer while retaining its one-shot service only if an approved network event invokes it.
3. Replace/remove the TailnetClient readiness sampling loop at its one shared definition.
4. In Home, remove all eight timer declarations and the zoekt interval option: zoekt, context-skills, Field Luna heartbeat, and five Field monitoring timers. Preserve `context-skills.path` and `field-luna-heartbeat.path`. Remove the periodic-fetch wording and any service fetch that remains reachable only through a periodic caller.
5. Implement only approved event/on-demand replacements. Do not invent hooks: zoekt changed-repository emission, remote context ref arrival, router lease events, and four non-flow-scoped monitoring jobs are design gates.
6. Replace the operational UI/session/readiness loops at their shared definitions once their event interfaces are chosen. Remove the obsolete Codex heartbeat datum only with psyche authority.
7. Update checks that assert timers or interval options. Add a lightweight source/evaluated-unit gate that rejects timer declarations, `startAt`, calendar/active schedules, and the named upstream timers. Build/evaluation belongs to the post-GO stage.

## Design blockers to send through main → Mindnix/Fable

1. **Zoekt:** which changed-repository event is authoritative, and how do pushes/fetches outside the indexed checkout reach it?
2. **Context skills:** which existing receive/push hook moves local refs for changes originating elsewhere? The current `.path` is sufficient only after a local ref changes.
3. **Router WAN:** which networkd event interface invokes the recovery oneshot, including late DHCP availability without a periodic check?
4. **Monitoring:** what events or explicit operator commands replace core-checkup, census, shadow checkup, and Luna research? Flow-98eb43 has a clear gone/no-replacement disposition.
5. **UI:** should live RSSI, solar seconds, microphone decay, transient expiry, and automatic socket reconnect be simplified away, or which producer events replace time sampling?
6. **Readiness:** choose contracts for tailscaled, Flow configuration socket, browser CDP, screenshot completion, and graphical-session identity.
7. **Retention:** approve exact on-demand GC/logrotate/tmpfiles/fstrim/XFS commands and ownership. “No silent retention” requires those choices to be explicit.
8. **Scope:** confirm whether non-host test polling and the psyche-authored Codex heartbeat datum are part of “anywhere.”

Stage 1 is complete subject to these design rulings. Source implementation is intentionally waiting for mainGO.

## Final-ruling account addendum (authoritative per-job entries)

This addendum supersedes grouped ledger entries and the earlier tentative scope blockers. Identical host declarations are grouped by host list; each line is one distinct job.

- **All ten system variants — Nix GC:** daily deletion; ouranos observed, other variants inferred from the shared module; purpose is store retention; schedule removed, manual `nix-collect-garbage` remains.
- **All ten system variants — scheduled Nix optimiser:** locked nixpkgs can create `nix-optimise.timer`; source-inferred; purpose is deduplication; explicitly disabled, while write-triggered `auto-optimise-store` stays.
- **All ten — fstrim:** weekly discard; ouranos observed, others inferred from nixpkgs default; explicitly disabled, manual `fstrim` remains.
- **All ten — fwupd refresh:** hourly metadata refresh; ouranos observed, others inferred from shared fwupd enable; timer masked, manual `fwupdmgr refresh` remains.
- **All ten — logrotate:** hourly btmp/wtmp rotation; ouranos observed, others inferred; explicitly disabled pending on-demand use.
- **All ten — system tmpfiles cleanup:** boot+daily age cleanup; ouranos observed, others inferred; cleanup timer masked while boot setup stays.
- **All user managers on all ten — user tmpfiles cleanup:** startup+daily age cleanup; li@ouranos observed, others inferred; timer alone masked while user tmpfiles setup stays enabled.
- **All ten — XFS scrub:** weekly upstream package timer; linked/inactive on ouranos, inferred elsewhere; timer masked, manual scrub remains.
- **NetworkManager variants — nm-cloud-setup:** five-minute upstream package timer; linked/inactive on ouranos; timer masked while dispatcher events stay.
- **All ten — updatedb:** locate module's daily-capable job; absent in source/runtime, explicitly disabled to hold that state.
- **All ten — cron:** scheduler; absent in source/runtime, explicitly disabled to hold that state.
- **prometheus — WAN lease recovery:** two-minute route check; source-inferred; timer removed, callable repair retained manually because a netlink/networkd listener is a separate design.
- **All five Home variants — zoekt indexing:** formerly initial+15-minute whole-tree fetch/index; source-inferred; schedule, fetch, scan, and interval options removed; single-repository no-fetch hook command added. Installing post-commit/post-merge hooks in independently owned repositories remains a specific mutation/ownership gap.
- **AgentStack Home variants — context skills:** formerly two-minute remote fetch/regeneration; path trigger observed on li@ouranos; timer and implicit fetch removed, local-ref path event retained, remote fetch is manual.
- **All five Home variants when enabled — Field Luna heartbeat:** 30-minute retirement/archive run; source-inferred/default-off; timer removed, lifecycle path event retained.
- **All five when enabled — core checkup:** 30-minute endpoint/unit assessment; source-inferred/default-off; timer removed, callable service retained manually.
- **All five when enabled — Field census:** five-minute census snapshot; source-inferred/default-off; timer removed, callable service retained manually.
- **All five when enabled — Field checkup shadow:** 30-minute three-aspect assessment; source-inferred/default-off; timer removed, callable service retained manually.
- **All five when enabled — Field Luna research:** 30-minute bounded source research; source-inferred/default-off; timer removed, callable service retained manually.
- **All five — flow-98eb43 monitor:** five-minute flow-scoped census; source-inferred/default-off; option, service, timer, generated script, and checks removed with no replacement.
- **TailnetClient variants — tailnet readiness:** up to 30 one-second status samples; source-inferred; remains a debt because tailscaled exposes no witnessed sd_notify/socket readiness contract in this source scope.
- **All five edge homes — active-network RSSI:** five-second `iw` sampling; source-inferred; remains a producer-interface gap pending supplicant/iwd signal wiring.
- **All five edge homes — active-network socket reconnect:** one-second retry alarm; source-inferred; remains a debt pending inotify/socket-activation wiring.
- **All five edge homes — solar status:** one-minute status read; source-inferred; remains a Chronos producer/alarm interface gap.
- **All five edge homes — listener status reconnect:** one-second socket retry loop; source-inferred; remains an inotify/socket-activation gap.
- **All five edge homes — listener transcript reconnect (widget):** one-second socket retry loop; source-inferred; remains an inotify/socket-activation gap.
- **All five edge homes — listener transcript reconnect (panel):** one-second socket retry loop; source-inferred; remains an inotify/socket-activation gap.
- **All five edge homes — wispr reconnect:** one-second socket retry loop; source-inferred; remains an inotify/socket-activation gap.
- **All five edge homes — wispr staleness:** one-second age check; source-inferred; remains pending producer state-change expiry.
- **All five edge homes — listener meter animation:** 70/110/1000 ms callbacks; source-inferred; remains pending a witnessed display-frame callback API.
- **All five edge homes — wispr meter animation:** 70/120/1000 ms callbacks; source-inferred; remains pending a witnessed display-frame callback API.
- **All five edge homes — lock-listener session discovery:** unbounded two-second loginctl sampling; source-inferred; remains pending graphical-session identity delivery.
- **All five edge homes — screenshot readiness:** 20×50 ms file checks; source-inferred; remains pending inotify conversion.
- **Home Flow configuration — Nexus socket readiness:** 100×50 ms socket checks; source-inferred; remains pending socket activation/inotify conversion.
- **Large/Max endpoint homes — browser-agent CDP readiness:** 60×0.5 s HTTP checks; source-inferred; remains pending producer readiness announcement.
- **Large/Max endpoint homes — browser bridge readiness:** 30×0.5 s HTTP checks; source-inferred; remains pending producer readiness announcement.
- **All five edge homes — screen-off delay:** one three-second alarm after lock; source-inferred; classified as an event and retained.
- **Homes carrying metaflows — Codex heartbeat:** hourly self-paced usage/status checks; source-inferred; the entire Tertiary heartbeat declaration was removed by final ruling.
- **Test-only polling waits:** bounded waits in checks/gates remain as explicitly ruled debt; they do not run on hosts.
- **All ten — journal retention:** size-bounded write-triggered daemon work; observed as no timer; retained as event work.

## Source-edit receipt

Applied in the two isolated branches after GO. No build, Nix evaluation, fetch, push, deployment, or host action was run. Lightweight witnesses passed: `git diff --check` in both worktrees, `bash -n packages/context-skills/regenerate.sh`, a source scan finding no operational Nix `OnCalendar`/`OnUnitActiveSec`/`OnUnitInactiveSec`/`OnBootSec`/`startAt`/explicit timer declaration, and focused scans proving context regeneration has no fetch and zoekt has neither fetch nor whole-tree scan/interval.

The remaining polling source locations are deliberately named in the final-ruling ledger as producer/API design gaps. Therefore this delta is a schedule-removal completion, not a claim that all polling is removed.

## Event/readiness delta receipt

Implemented after the immutable schedule commits:

- Tailnet enrollment now blocks on the installed Tailscale 1.102.2 `tailscale wait --timeout=30s` readiness command, then reads backend state once. The installed daemon is `Type=notify`; the former 30 one-second samples are gone.
- Screenshot completion uses one `inotifywait` close-write event and one one-second alarm, then validates the file once.
- Flow configure-only socket readiness uses one inotify create/move event and one five-second alarm, then validates socket ownership once; the 100 samples are gone.
- The lock listener starts with the graphical-session event, resolves its session once, and then blocks on logind D-Bus. Its unbounded two-second discovery loop and restart retry are gone. The approved three-second screen-off alarm remains.
- Listener status, listener transcript widget, listener transcript panel, and Wispr status reconnect on filtered inotify socket-creation events. Their one-second retry loops are gone.
- Active-network reconnect blocks on filtered directory/socket creation events before reconnecting. Its one-second QML retry timer is gone.

Specific inspected gaps still open:

- **Wi-Fi dBm:** `active_network_helper.py` already consumes NetworkManager D-Bus property/state signals, but obtains dBm only from `iw dev INTERFACE link`; NetworkManager's access-point `Strength` property is a percentage and cannot preserve the displayed dBm. The missing contract is a wired wpa_supplicant/iwd dBm property-change signal for the active BSS.
- **Solar crossing:** the installed widget-facing Chroma contract used here is only `chroma GetSolarClock`, returning current offset/day validity. No next-crossing timestamp or subscription is present at this callsite. Chronos must expose the next computed crossing/alarm event before the minute query can be replaced without losing the live feature.
- **Animation/staleness:** the Noctalia plugin surface present in these sources exposes `function update()` plus `setUpdateInterval`; no display-frame callback appears in the installed plugin source carried here. Wispr events carry samples/state but no producer expiry event. The missing contracts are a frame callback while animating and an explicit producer state/expiry transition.
- **Browser CDP:** `browser-agent-chrome` execs Chrome and the bridge execs its relay; consumers only have the HTTP `/json/version` probe. Neither wrapper exposes sd_notify, a readiness fd, socket activation, nor a readiness record. The missing contract is a producer-owned readiness notification for each process; the existing HTTP sample loops remain pending it.
- **Zoekt hooks (resolved after the event-stage inventory):** installed Git 2.55 documents additive `hook.<name>.command` configuration with repeated `hook.<name>.event` values, including `post-commit` and `post-merge`. Home commit `f5ce296546c611e715c6182698a7ce7ce18638bd` declares one `zoekt-index` command for those two events through `programs.git.settings`; it does not set `core.hooksPath`, fetch, or mutate repository-owned hook files. This exact commit is published on the Home `main` branch.

## Schedule-publication closure gate

- The published Home history is `689d72daa2da4e2c66c61e60d74474207327003f` → `e7b52831d7d188cd4ec471dd7346fb177988b7b2` → `f5ce296546c611e715c6182698a7ce7ce18638bd`. Both pushes were fast-forwards; neither was forced or retried.
- The unpublished CriomOS publication worktree still has schedule commit `d56c11437f02343fa94dc08e92399761f0f879c8` at `HEAD`. Its lockfile working change updates only the `criomos-home` locked `rev`, `lastModified`, and `narHash`, pinning `f5ce296546c611e715c6182698a7ce7ce18638bd` with `sha256-gjCotjthuEvbR2Ca9GplZbRlGaeA2zUpU3sxHlmF54E=`. No other lock node changed.
- Duplicate `nix.gc.automatic` and `nix.optimise.automatic` assignments have been removed locally from `retention-agent.nix`; the cluster policy remains their single declaration.
- `boot.tmp.cleanOnBoot = true` is preserved only in `publication/boot-tmp-cleanOnBoot-gated.patch` (SHA-256 `d2057e48c58c392fa86fe26cc979ded4e4aa873a023756621cbfee9eca577dac`). The published source omits it. Boot cleanup therefore remains off as a named temporary debt while every affected owner verifies preservation and gives an explicit disposition. No move, deletion, expiration, or reboot was performed.
- First-stage GC remains manual as a named temporary debt; no `min-free` or `max-free` value is in the published commit. A later, separate unpublished threshold commit, `e1f579e35c33f1205baa4240244358d1208041d3`, declares 64/160 GiB for ouranos, 128/384 GiB for prometheus, and 32/96 GiB for zeus in one per-node map; unmeasured hosts remain manual. It is based directly on published `7e12333fa7c3f792ba791364d6563bf0b76ec7ef` and awaits its own review/publication chain.
- CriomOS commit `7e12333fa7c3f792ba791364d6563bf0b76ec7ef` contains only the schedule commit history, the final Home pin, and duplicate-policy consolidation. It was pushed once as a fast-forward from `031b3dc68b552470e0fe62bd14fe8e6222b6c4b7`; remote `main` was then observed at exactly `7e12333fa7c3f792ba791364d6563bf0b76ec7ef`. This author performed no realization, build, evaluation, activation, or host mutation.

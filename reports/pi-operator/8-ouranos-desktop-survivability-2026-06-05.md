# Ouranos desktop survivability

Date: 2026-06-05
Role: pi-operator
Host: `ouranos`

This report merges the full 2026-06-05 arc: the UI-freeze incident that triggered the work, the Linux resource-priority research that informed the design, the rescue-terminal `session.slice` deploy bug and its repair, and the staged component-specific UI-priority policy that was implemented. The durable design conclusions have landed in `CriomOS-home` (`INTENT.md` "Desktop survivability", `skills.md` "Desktop survivability safety"/"Nix output redaction helpers", and `modules/home/profiles/min/ui-priority.nix` + the rescue-terminal binding). This report retains the incident forensics and the reusable research catalog (mechanism families, deferred experiments, sources), which are not in any permanent doc.

## Part 1: UI-freeze incident forensics

Incident window: previous boot ending at about 14:59:50 CEST.

### Summary

The previous boot did not show a kernel panic, kernel OOM kill, watchdog lockup, or clean shutdown. It ended after a user power-key event at 14:59:40, with a new boot at 15:00:23. The logs show graphical-session starvation: Niri/libinput reported one input-processing backlog sample of 20.8 seconds at 14:56:38, and systemd-journald logged repeated memory-pressure cache flushes from 14:57:47 through the hard reboot. Psyche observation corrects the severity framing: the visible UI/input freeze was minutes-long, roughly five minutes or more, with touchpad movement still waiting to be processed. The 20.8 second log line is a logged symptom, not the freeze duration.

The most likely trigger was the `lojix-run` `HomeOnly Build` smoke started for `bird` on `zeus`. It began at 14:29:55 and was still writing stderr at 14:58:36. It had planned 54 local derivation builds plus a 3.3 GiB unpacked closure fetch, copying many paths from the Prometheus substituter with repeated 5-6 second download timeouts, overlapping the first Niri lag reports, PipeWire underruns, and the final memory-pressure cluster.

The strongest contributing factor: `ouranos` had no swap at incident time. `systemd-oomd` logged that memory-pressure handling is degraded without swap. Under combined agent load plus Nix copy/build/eval pressure, the compositor and audio stack were not protected from starvation.

A secondary problem was a broken `persona-spirit-daemon-v0.1.1.service` restart loop: restart counter 29,385 by 14:58:06, still looping after reboot. Each instance was small, unlikely to be the sole cause of a whole-UI freeze, but it produced continuous process churn and log volume. The old failing side-by-side user service was stopped at runtime after reboot; current production/newer Spirit daemons stayed running.

### Evidence

**Boot and shutdown:**
- Previous boot: 2026-05-28 13:55:47 through 2026-06-05 14:59:50.
- Current boot: started 2026-06-05 15:00:23.
- `systemd-logind` recorded `Power key pressed short` at 14:59:40.
- No kernel log evidence of OOM kill, panic, soft lockup, hung task, GPU reset, thermal shutdown, or watchdog reset.

**UI starvation** (sparse journal samples, lower bounds):
- 14:50:28 — event processing lagging by 51 ms.
- 14:50:56-14:50:58 — timer events lagging ~2.7-2.9 s, event processing lagging 1.18 s.
- 14:56:38 — event processing lagging by 20.8 seconds.
- 14:58:59 — touchpad frame errors, likely after the session was already badly delayed.
- Psyche observation: user-visible Niri/touchpad backlog roughly five minutes or more, movement still not visibly processed.
- PipeWire logged many ALSA broken-pipe/resync messages starting at 14:52 — consistent with realtime/audio starvation under system pressure, not an isolated webcam/camera package issue.

**Memory pressure:** `systemd-journald` logged `Under memory pressure, flushing caches` repeatedly in the final minutes (14:57:47, 14:57:51, 14:58:06, 14:58:39, 14:58:43, 14:58:47, then 12 times in the 14:59 minute before the hard reboot). Earlier memory-pressure messages were sparse and clustered around unrelated moments, so the final cluster is incident-specific. Current boot: 30 GiB RAM, 0 B swap at the time, `systemd-oomd` warning of degraded pressure usage without swap.

**`lojix-run`:** run directory `~/.local/state/lojix-runs/20260605122955-homeonly-zeus/`; request `HomeOnly goldragon zeus bird ... CriomOS-home rev 4d202ba64dff... Build None None`. Started 14:29:55; `stdout.log` stayed empty; `stderr.log` last modified 14:58:36. Nix planned 54 local derivation builds and 156 fetched paths (3.3 GiB unpacked). The fetch set included broad graphical/profile packages (`cameractrls`, OBS, Krita, GIMP, Calibre, libvirt-related) plus side-by-side Spirit service derivations. Substituter fetches from Prometheus timed out repeatedly near the log tail. The intended "small HomeOnly Build smoke" was a broad profile closure operation under a cache state where many packages had to be fetched/unpacked and some derivations still had to build locally.

**Spirit v0.1.1 restart loop:** repeatedly starting, failing with `InvalidDaemonConfiguration`, restarting; counter reached 29,385 at 14:58:06; some instances consumed seconds of CPU over tens of seconds of wall time. After reboot it resumed the loop; stopped at runtime with `systemctl --user stop persona-spirit-daemon-v0.1.1.service`. Active production/newer Spirit services stayed running.

### Ruled out

No kernel OOM kill; no panic/BUG/Oops/soft-lockup/hung-task log; no clean shutdown sequence before reboot; no evidence `cameractrls` itself crashed the UI (the issue was the broad Home profile build/fetch path, not the webcam-control package at runtime); no evidence Home activation ran (this was the `Build` smoke, not `Activate`).

### Immediate mitigation applied

Stopped the broken old `persona-spirit-daemon-v0.1.1.service` runtime restart loop after reboot; left the pushed `cameractrls` commits intact (both CriomOS-home and CriomOS working copies clean); did not resume the HomeOnly deployment after the freeze.

### Follow-up recommendations (these fed the research and policy below)

1. Add swap or zram on `ouranos` (done — see Part 2).
2. Put agent and Nix build workloads in resource-limited scopes: lower CPU/IO priority and memory ceilings for interactive-session agent work.
3. Make `lojix-run` resource-safe by default on interactive machines: `systemd-run --user` scope, low IO/CPU priority, explicit timeout/progress heartbeat, possibly confirmation when the planned closure is multi-GiB or has many local derivations.
4. Add a preflight check before any deploy/build smoke reporting planned build/fetch counts, asking before continuing on an interactive machine under active multi-agent load.
5. Fix or retire side-by-side old Spirit daemon slots so a failed legacy daemon cannot restart forever. At minimum add `StartLimitBurst`/`StartLimitIntervalSec`; better, disable broken obsolete slots by profile generation.
6. Prefer remote builders or the target/Prometheus for heavy closure realization when the operator workstation is the active UI machine.
7. Pause further Zeus HomeOnly activation until the resource-safety changes or an explicitly quiet window.

## Part 2: Linux desktop resource-priority research and freeze prevention

### User intent

The goal is not merely to add swap. The goal is to make the computer remain operable during resource pressure: the compositor/desktop shell, launcher, terminal emulator, and core interactive programs should retain enough CPU, IO, and memory priority that the user can still inspect the machine, close or kill work, and continue operating the desktop. The research surveyed older, newer, experimental, theoretical, and production Linux approaches without assuming one mechanism up front.

### Short answer

`ouranos` is more protected now than during the freeze because it has both compressed RAM swap and a disk swap fallback active:
- `/dev/zram0`: about 7.7 GiB, priority 5
- `/swapfile`: 32 GiB, priority -1

That materially improves memory-pressure behavior because `systemd-oomd` works best with swap: the system spends enough time in reclaim/swap pressure for `systemd-oomd` to react before kernel-space OOM or livelock. The `systemd-oomd` manual says swap is highly recommended; without it the system can enter livelock too quickly to respond. But swap/zram is not a complete UI-freeze prevention strategy. The freeze mechanism can be CPU contention, IO pressure, memory reclaim, swap thrash, or all together. The next layer is explicit cgroup/slice policy: protect session-critical UI work and demote build/agent/batch work.

### Current `ouranos` observations (live host after swap/zram activation)

- Systemd: 260.1.
- Cgroup v2 controllers at root: `cpuset cpu io memory hugetlb pids rdma misc dmem`.
- `systemd-oomd` enabled: `Swap Used Limit: 90%`, default memory pressure limit `60%` for `30s`, several `app-ghostty-surface-transient-*.scope` cgroups monitored for memory pressure.
- User slices show the standard systemd desktop shape: `session.slice` CPUWeight=100, `app.slice` CPUWeight=100, `background.slice` CPUWeight=30; `niri.service` in `session.slice`.
- `nix-daemon.service` already has `CPUSchedulingPolicy=idle`, `IOSchedulingClass=best-effort`, `IOSchedulingPriority=7`; live process reports `SCHED_IDLE` and best-effort IO priority 7.
- NVMe scheduler reports `none` active, with `mq-deadline` and `kyber` available; `bfq` not listed for the current device.

Implication: basic pieces are present. The missing part is stronger policy around session-critical UI versus bulk workloads, and explicit handling for target-side activation work such as swapfile formatting.

### Mental model: why a desktop freezes without a kernel crash

The earlier incident looked like starvation rather than a panic. Under memory pressure the kernel reclaims page cache and swaps anonymous pages; under IO pressure, even starting a terminal or reading executable/library pages can block behind heavy writes. If all interactive tasks stall waiting for memory or IO, the mouse/keyboard/compositor may appear frozen even though the kernel is not dead. The production answer is not to make the UI realtime by default (realtime CPU/IO can starve the rest of the system). It is layered: (1) give the kernel a pressure valve — zram, disk swap, sane swappiness; (2) use cgroups to classify work by importance; (3) use pressure/OOM policy to shed low-priority work before livelock; (4) use IO and CPU weights/scheduling for background work; (5) keep an emergency interactive path outside the heavy workload cgroup.

### Mature mechanism family 1: systemd cgroups and desktop slices

Systemd's desktop integration defines three standard user slices: `session.slice` (essential graphical-session processes), `app.slice` (normal applications), `background.slice` (low-priority background tasks). The purpose: assign different priorities so the session runs smoothly under load, reserving memory to session processes, preferentially killing background tasks, and assigning different memory/CPU/IO priorities. Useful resource-control options:
- `CPUWeight=`: relative CPU share among siblings; range 1-10000, default 100; `idle` supported on cgroup v2.
- `IOWeight=`: relative block IO share; range 1-10000, default 100.
- `MemoryLow=`/`MemoryMin=`: memory protection; reclaim prefers unprotected cgroups first. `MemoryLow` weaker and safer than `MemoryMin`.
- `MemoryHigh=`: throttling limit, the main mechanism to control memory use; usage can exceed it but the cgroup is heavily slowed and reclaimed.
- `MemoryMax=`: hard last-line limit; prefer `MemoryHigh` first, `MemoryMax` as defense.
- `ManagedOOMMemoryPressure=`/`ManagedOOMSwap=`: opt cgroups into `systemd-oomd` policy.

Near-term production shape for `ouranos`: keep `niri`, desktop shell/panel, launcher, interaction portals, and a minimal rescue terminal in a protected session-critical slice; keep normal apps in `app.slice`; move agents, local builds, indexing, large deploy/eval work, and batch shell commands into `background.slice` or a dedicated `workload.slice` with lower CPU/IO weight and memory pressure policy.

Important caution: boosting an entire terminal cgroup also boosts the shell and every heavy child launched inside it. If a terminal window is where Codex/Nix/agents run, boosting the whole Ghostty app scope makes the heavy work more dangerous. Prefer either protecting only the terminal emulator/rescue terminal path and running heavy commands in separate background scopes, or keeping Ghostty as a normal app while heavy agent/build wrappers automatically move themselves into a demoted scope.

### Mature mechanism family 2: `systemd-oomd`, PSI, proactive kill policy

The kernel PSI documentation describes pressure stall information quantifying CPU, memory, and IO contention via `/proc/pressure/{cpu,memory,io}` and per-cgroup pressure files, with `some` and `full` stall metrics. `systemd-oomd` uses cgroup v2 and PSI to act before kernel-space OOM; it monitors cgroups with `ManagedOOMSwap=` or `ManagedOOMMemoryPressure=` set to `kill` and kills an eligible descendant cgroup when thresholds are exceeded. Two desktop details: swap makes `systemd-oomd` more effective (without it pressure rises abruptly and the machine may livelock before user space reacts); cgroup granularity matters (if all work is in one large terminal/session scope, OOM policy can kill too much; if each agent/build is a separate scope, the system kills one bad workload rather than the whole desktop). `ouranos` now has swap and `oomctl` shows per-Ghostty app scopes monitored; the remaining question is policy: which cgroups are eligible for pressure kills, which are protected, how aggressively background work is terminated.

### Mature mechanism family 3: IO scheduling, IO weights, `ionice`

IO pressure was a major problem during swapfile activation: creating and formatting the disk swapfile drove very high IO pressure while `mkswap` ran. IO control layers: `IOWeight=`/cgroup v2 `io.weight` (proportional IO share); `io.max` (hard byte/IOPS throttling); per-process IO priority via `ionice`/`ioprio_set`; device scheduler choices (BFQ, mq-deadline, kyber, none). BFQ is historically relevant — its kernel documentation targets personal-system responsiveness under background workloads like source builds, updates, file copies, VMs, with low-latency heuristics privileging interactive/soft-realtime apps. But the current `ouranos` NVMe scheduler showed `none` active with `mq-deadline`/`kyber` available, no BFQ; so BFQ is not an immediate assumption. Safe near-term path: use cgroup IO limits/weights where supported; run known heavy target-side commands with low IO priority; make `lojix` activation steps resource-aware rather than avoiding `lojix`; avoid assuming BFQ unless a kernel/device experiment confirms it. The `ionice` documentation warns realtime IO can starve the system; for background deploy/build tasks prefer idle or low best-effort priority; for UI avoid realtime IO except narrow audio/video cases with known bounds.

### Mature mechanism family 4: CPU scheduler policy, nice, SCHED_IDLE/BATCH, autogroup

Classic `nice` helps per-process CPU fairness but not memory pressure, cgroup containment, or IO stall. Better CPU tools for bulk work: `SCHED_IDLE` (extremely low-priority; Nix daemon already uses it on `ouranos`); `SCHED_BATCH` (non-interactive batch policy, sometimes better throughput than `nice` while reducing interactivity impact); `CPUWeight=` (cgroup proportional CPU sharing); `CPUQuota=` (hard cap; useful for runaway jobs but too blunt alone). Linux autogroup historically improved desktop interactivity by grouping tasks by session (often per terminal window); it helps old "compile in one terminal while using another" scenarios but is insufficient here because many heavy processes can share one terminal/app scope and the failure involved memory/IO pressure, not only CPU fairness.

### Production tools and daemons

- **`systemd-run` scopes:** `systemd-run --user --scope --slice background ...` is the most direct production tool for launching one command in its own cgroup with explicit resource properties. Ideal for agent/build wrappers: keeps the terminal interactive while the heavy child is accounted and killable separately.
- **`systemd-cgtop`, `oomctl`, PSI tools:** `systemd-cgtop` reports by cgroup (less misleading than per-process RSS); `oomctl` shows what `systemd-oomd` monitors; `psi-notify`/`psitop` surface pressure before the desktop feels frozen.
- **`ananicy-cpp`:** auto-priority daemon with rules for renicing, CPU scheduler, IO class/nice, OOM score, cgroups, autogroup, systemd integration. Useful when programs are not launched through controlled wrappers/scopes. For this workspace it is a possible later classifier, not the first mechanism — declarative Nix/systemd slice policy and explicit wrappers come first; `ananicy-cpp` is more heuristic and could fight declarative placement if introduced too early.
- **GameMode:** Feral GameMode temporarily changes CPU governor, IO priority, niceness, scheduler behavior, and scripts for a specific foreground process. Architectural lesson: a scoped request/daemon model works. The exact tool is game-oriented, not general desktop survival policy.
- **`earlyoom`:** simpler than `systemd-oomd`, effective on desktops with avoid/prefer regexes, but less cgroup-native. Since `ouranos` uses modern systemd and cgroup v2, prefer tuning `systemd-oomd` first before adding a second OOM daemon.

### Newer and experimental mechanisms (tracked, deferred)

- **Utilization clamping (`uclamp`):** lets user space hint min/max CPU performance for tasks/cgroups; Android-style top-app/background policy is a documented use case. Local probing did not show `cpu.uclamp.*` files in the current user app cgroup, so not an immediate assumption; worth tracking but not the first production layer.
- **`latency_nice`:** scheduler-hint proposal to give latency-sensitive tasks CPU sooner without realtime policy. Research set only; local probing did not show a visible `latency_nice` field. Future/patch/kernel-version path until confirmed in the actual `ouranos` kernel and systemd/Nix exposure.
- **`sched_ext`:** BPF-defined schedulers loadable/unloadable dynamically, reverting to default on errors/stalls. Powerful active research/production-experiment infrastructure, far too broad for the first safety fix; later lab experiment.

### Nix and deploy-specific findings

`nix-daemon` on `ouranos` is already `SCHED_IDLE` and low best-effort IO priority, and NixOS docs say these daemon scheduling settings propagate to build processes. So the disaster was not simply "Nix daemon lacks idle priority." Remaining hazards: local evaluation, flake fetching/unpacking, deploy-wrapper work, and activation phases can consume resources outside the actual builder process; target-side activation steps like creating/formatting a large swapfile are not Nix builds and are not protected by `nix-daemon` scheduling; shell-launched agents can live in an interactive terminal cgroup unless explicitly moved; remote builder use helps local CPU/RAM pressure but can still generate local copy/unpack/activation IO. Nix has experimental `use-cgroups` support for running builds inside cgroups — worth testing later, especially if per-build memory accounting/limits matter, but it should not replace systemd slice policy around the deploy command and agent shells.

### Recommended design for `ouranos` (phased)

- **Phase 0 — keep current protection:** keep the zram + disk swap policy and `systemd-oomd` enabled, giving a memory pressure valve and reaction time.
- **Phase 1 — protect the critical UI path with systemd user slices:** declarative user-manager drop-ins for the standard desktop slices — raise `session.slice` relative priority above normal apps/background; add modest `MemoryLow=` protection for session-critical UI; keep `background.slice` lower than `app.slice` and much lower than `session.slice` for CPU/IO; keep/tune `ManagedOOMMemoryPressure=` on app/background descendants, not on the critical session slice. Candidate critical processes: `niri`, shell/panel (likely `quickshell`), launcher, notification/portal components needed to recover the desktop, one explicitly designated rescue terminal (only if heavy children can be kept from inheriting the protected cgroup). NOTE: the live incident in Part 3 proved that making Home Manager own `session.slice` is a logout hazard; Phase 1 was superseded by the safer runtime-applied approach (Part 4).
- **Phase 2 — demote heavy work by construction:** a workspace wrapper for heavy interactive commands launching them in a background/workload scope (agents/Codex sub-workloads, Nix builds/checks, large local eval/deploy smoke, cache cleanup/scans, indexing, bulk repo operations). Use systemd scopes rather than just `nice` so the workload is visible in `systemd-cgtop`, killable as a group, and receives CPU/IO/memory policy together.
- **Phase 3 — make `lojix` resource-aware, not avoided:** `lojix` deployment is not the problem; the problem is unbounded resource pressure in particular phases. `lojix-run` remains the human-facing deploy report surface; the improvement is resource-aware execution — local build/eval/copy phases in a low-priority systemd scope on a desktop host; target-side activation phases that can create heavy IO (swapfile creation/formatting) through root SSH in a low-priority target-side scope; deploy reports include pressure/elapsed warnings and identify long target-side steps; branch refs use `main` for operator-facing deploy requests.
- **Phase 4 — pressure visibility and emergency controls:** `psi-notify` or equivalent for desktop warnings when memory/IO pressure crosses thresholds; a launcher entry/hotkey for `systemd-cgtop` or a small pressure dashboard; a launcher entry/hotkey to kill the current background/workload scope (not random UI processes); a convention that agents and bulk commands display their cgroup/scope name in logs/reports.
- **Phase 5 — evaluate IO scheduler and deeper scheduler experiments later:** after cgroup/slice policy exists, test whether changing the NVMe scheduler from `none` to `mq-deadline`, `kyber`, or a kernel with BFQ materially improves interactive IO latency under synthetic pressure, in a controlled benchmark not during normal work. Track but defer: `uclamp` if exposed; `latency_nice` if available/controllable; `sched_ext` schedulers; `ananicy-cpp` as a classifier if declarative placement is insufficient.

### Open design questions

1. Should the rescue terminal be a dedicated terminal instance/window, or all Ghostty windows considered core UI? (Resolved toward dedicated — see Parts 3-4 — because boosting all Ghostty scopes also boosts heavy agent children.)
2. How much memory should be reserved/protected for the interactive session? Conservative start: 1-2 GiB via `MemoryLow`, validated under pressure.
3. What should be killed first under pressure: individual agent scopes, all background work, browser tabs/app scopes, or deploy jobs?
4. Should the first implementation be local to `ouranos` or expressed as a Horizon-projected desktop capability so future desktops inherit it?

### Sources

- systemd desktop slice model: https://systemd.io/DESKTOP_ENVIRONMENTS/
- systemd resource control manual: https://www.man7.org/linux/man-pages/man5/systemd.resource-control.5.html
- systemd-oomd manual: https://www.man7.org/linux/man-pages/man8/systemd-oomd.service.8.html
- PSI kernel documentation: https://www.kernel.org/doc/html/latest/accounting/psi.html
- BFQ kernel documentation: https://docs.kernel.org/block/bfq-iosched.html
- Block IO priority kernel documentation: https://docs.kernel.org/6.9/block/ioprio.html
- Utilization clamping kernel documentation: https://docs.kernel.org/scheduler/sched-util-clamp.html
- sched_ext kernel documentation: https://docs.kernel.org/scheduler/sched-ext.html
- KDE app-as-systemd-service memory control: https://blogs.kde.org/2024/10/18/limit-application-memory-usage-with-systemd/
- ETH D-PHYS workstation resource-control policy: https://readme.phys.ethz.ch/linux/workstation/resource_control/
- NixOS swap/zram documentation: https://wiki.nixos.org/wiki/Swap
- Nix resource-restricted rebuild discussion: https://discourse.nixos.org/t/feature-request-performance-restricted-rebuilds/59569
- Nix `use-cgroups` setting: https://nix.dev/manual/nix/2.34/command-ref/conf-file.html
- ananicy-cpp: https://github.com/EvoXCX/ananicy-cpp
- Feral GameMode: https://github.com/FeralInteractive/gamemode

## Part 3: Rescue-terminal slice incident and repair

### What went wrong

The intended change was a dedicated rescue terminal and research-backed resource protection for the minimum desktop path needed to keep the computer operable. The unsafe implementation overreached: it added Home Manager ownership of the standard user slices `session.slice` and `background.slice`. The dangerous one is `session.slice` — the live Niri compositor runs under it, along with the user D-Bus bus and PipeWire. A live `HomeOnly Activate` then reconciled user systemd units. Reconciling a live slice that contains the compositor can stop or replace that slice, terminating the compositor and logging the user out. That is a deploy bug and an unacceptable activation behavior, not normal `HomeOnly Activate` behavior.

### Observed state after the incident

No leftover `lojix`, activation, or Home Manager deployment process was visible after logout. The active home profile did contain Home-managed files for both `session.slice` and `background.slice`, confirming the local profile was left in the unsafe shape. The live UI cgroup layout showed:
- `niri.service` under `session.slice`: compositor and window manager; absolutely critical.
- `dbus-broker.service` under `session.slice`: user session bus; critical for desktop IPC.
- `pipewire.service`/`wireplumber.service` under `session.slice`: audio/media; useful for full session health, not the first survival target.
- `quickshell`/Noctalia under an `app.slice` transient app scope: shell/panel/launcher; critical for normal desktop operation.
- `mako` under an `app.slice` transient app scope: notifications; useful but not core recovery.
- `xdg-desktop-portal*` and permission/document portal services: app integration; useful for normal session operation.
- Ghostty app scopes under `app.slice`: ordinary terminals; should not all be boosted because agent/build children live under them.

### Immediate repository repair

The repaired Home profile removes all Home Manager ownership of `session.slice` and `background.slice`. The rescue terminal remains, but only as a specific launch path:
- Niri binding: `Mod+Ctrl+Return`.
- Command: `criomos-rescue-terminal`.
- Launch mechanism: a fresh transient `systemd-run --user --scope` for the rescue terminal instance.
- Resource policy attached to that transient scope, not to a Home-owned live desktop slice.
- The launcher no longer asks for `session.slice`; it lets the user manager place the transient scope normally and applies protection to that specific scope.

The repaired profile evaluates with no declared `systemd.user.slices` entries and no `session.slice`/`background.slice` references in the edited Home modules, while retaining the rescue terminal binding and the reusable Nix-store redaction helper.

### What not to do (at the time)

Do not run another live `HomeOnly Activate` from the unsafe profile path while the current graphical session matters. The corrected commit prevents future pinned profiles from carrying broad slice ownership, but transitioning away from the bad generation still needs a safe method because the active Home generation already contains the bad slice unit files. Safe cleanup options to choose deliberately: activate only from a logged-out or throwaway graphical session; use a Home activation mode that updates files without stopping/restarting user units, if verified; or handle the stale user slice files manually with a tested non-disruptive path. The next activation should be treated as a recovery step, not a normal profile update.

### Next design direction (realized in Part 4)

Favor specific recovery components, not broad live slices: protect the compositor/session path without making Home Manager own `session.slice`; protect Noctalia/Quickshell launcher/shell through a specific transient scope or a stable app-unit policy that does not restart it under the active session; protect one rescue terminal only, not all Ghostty terminal scopes; demote future agent/build/deploy workloads into explicit background/workload scopes; add pressure visibility and kill controls for those workload scopes. This preserves the original goal: the user can still operate the computer during resource pressure, inspect what is happening, and close or kill heavy work without the resource policy itself becoming a logout hazard.

## Part 4: Staged UI-priority policy implementation

### Implemented (landed in CriomOS-home)

CriomOS-home has a staged, component-specific UI-priority module at `modules/home/profiles/min/ui-priority.nix`, imported by `modules/home/default.nix`, enabled only for Horizon `edge` desktop roles. No live Home activation, Niri reload, or deployment was run while implementing it. (Module and rescue-terminal binding are present in the repo; the durable rule is captured in `CriomOS-home/INTENT.md` "Desktop survivability" and `skills.md` "Desktop survivability safety".)

### What the module installs

Two commands: `criomos-ui-priority-apply`, `criomos-ui-priority-status`. A oneshot user service `criomos-ui-priority.service`, wanted by `graphical-session.target`, intended to run after the graphical session exists and apply runtime resource properties to specific units/scopes.

### Safety boundary

The module does not declare `systemd.user.slices` and does not own `session.slice` or `background.slice`. The apply command uses `systemctl --user set-property --runtime`, applying runtime cgroup properties to already-existing units/scopes instead of writing persistent drop-ins for live parent slices or restarting the compositor.

### Components targeted

Stable user services by name: `niri.service`, `dbus-broker.service`, `xdg-desktop-portal.service`, `xdg-desktop-portal-gtk.service`, `xdg-document-portal.service`, `xdg-permission-store.service`, `pipewire.service`, `wireplumber.service`. Transient app scopes by process command-line discovery: Noctalia/QuickShell, Mako. The rescue terminal remains protected independently by its own transient `systemd-run --user --scope` launch path and `Mod+Ctrl+Return` Niri binding.

### Validation performed (repository-only)

Nix parse for the new and aggregate module passed. CriomOS evaluation with local CriomOS-home override showed: UI-priority apply/status packages present; `criomos-ui-priority.service` present; `Mod+Ctrl+Return` rescue binding present; `systemd.user.slices` remains empty. CriomOS Home activation package build passed with local override. Generated apply/status scripts passed `bash -n`. No live application of the policy was performed.

### Remaining deployment warning

The active running Home profile had previously been activated with bad generated user slice files. Main is repaired and now has staged component-specific policy, but the next live activation should still be treated as a recovery/safety operation. Do not run it in an active high-value agent session without a deliberate safe window.

## Where the durable conclusions landed

- `CriomOS-home/INTENT.md` "Desktop survivability": rescue terminal as a separate keybinding, do-not-own-`session.slice`, component-specific runtime-applied UI-priority policy.
- `CriomOS-home/skills.md` "Desktop survivability safety": the `session.slice` activation hazard and the `ui-priority.nix` rule; "Nix output redaction helpers": `redact-nix-store-paths` / `with-nix-store-redaction`.
- `CriomOS-home/modules/home/profiles/min/ui-priority.nix` and the `Mod+Ctrl+Return` rescue-terminal binding: the implemented policy.

What remains only here (not in permanent docs): the incident forensics (Part 1), and the reusable research catalog with deferred experiments and sources (Part 2). The follow-up that has NOT landed: swap/zram is in place but the broader Phase 2 (demote-by-construction workload wrapper), Phase 4 (pressure visibility/kill controls), and the legacy Spirit daemon `StartLimitBurst` fix remain open operator work.

# Linux desktop resource priority and freeze prevention on `ouranos`

Date: 2026-06-05
Role: pi-operator

## User intent

The goal is not merely to add more swap. The goal is to make the computer remain operable during resource pressure: the compositor/desktop shell, launcher, terminal emulator, and other core interactive programs should retain enough CPU, IO, and memory priority that the user can still inspect the machine, close or kill work, and continue operating the desktop.

The research should not assume one specific mechanism up front. It should survey older, newer, experimental, theoretical, and production Linux approaches to preventing UI freezes.

## Short answer

`ouranos` is more protected now than it was during the freeze because it has both compressed RAM swap and a disk swap fallback active:

- `/dev/zram0`: about 7.7 GiB, priority 5
- `/swapfile`: 32 GiB, priority -1

That materially improves memory-pressure behavior because `systemd-oomd` works best with swap enabled: the system spends enough time in reclaim/swap pressure for `systemd-oomd` to react before kernel-space OOM or livelock. The `systemd-oomd` manual explicitly says swap is highly recommended, and that without swap the system can enter livelock too quickly for `systemd-oomd` to respond in time.

But swap/zram is not a complete UI-freeze prevention strategy. The freeze mechanism can be CPU contention, IO pressure, memory reclaim, swap thrash, or all of them together. The next layer should be explicit cgroup/slice policy: protect session-critical UI work and demote build/agent/batch work.

## Current `ouranos` observations

These are current-state observations from the live host after the swap/zram activation.

- Systemd: 260.1.
- Cgroup v2 controllers available at the root: `cpuset cpu io memory hugetlb pids rdma misc dmem`.
- `systemd-oomd` is enabled and reports:
  - `Swap Used Limit: 90%`
  - default memory pressure limit: `60%` for `30s`
  - several `app-ghostty-surface-transient-*.scope` cgroups monitored for memory pressure.
- User slices currently show the standard systemd desktop shape:
  - `session.slice`: `CPUWeight=100`
  - `app.slice`: `CPUWeight=100`
  - `background.slice`: `CPUWeight=30`
  - `niri.service` is in `session.slice`.
- `nix-daemon.service` already has:
  - `CPUSchedulingPolicy=idle`
  - `IOSchedulingClass=best-effort`
  - `IOSchedulingPriority=7`
  - The live `nix-daemon` process reports `SCHED_IDLE` and best-effort IO priority 7.
- The NVMe scheduler currently reports `none` active, with `mq-deadline` and `kyber` available; `bfq` was not listed for the current device.

Implication: some basic pieces are already present. The missing part is stronger policy around the session-critical UI versus bulk workloads, and explicit handling for target-side activation work such as swapfile formatting.

## Mental model: why a desktop freezes without a kernel crash

The earlier incident looked like starvation rather than a panic: no kernel OOM kill, no panic, and no clean shutdown marker; there was memory pressure and a large local build/deploy workload.

Linux can appear frozen while still trying to make progress. Under memory pressure the kernel may reclaim page cache and swap anonymous pages; under IO pressure, even starting a terminal or reading executable/library pages can block behind heavy writes. If all interactive tasks stall waiting for memory or IO, the mouse/keyboard/compositor may appear frozen even though the kernel is not dead.

The production answer is not “make the UI realtime” by default. Realtime and IO realtime can starve the rest of the system and create new failure modes. The production answer is usually layered:

1. Give the kernel a pressure valve: zram, disk swap, and sane swappiness.
2. Use cgroups to classify work by importance.
3. Use pressure/OOM policy to shed low-priority work before the whole machine livelocks.
4. Use IO and CPU weights/scheduling for background work.
5. Keep an emergency interactive path outside the heavy workload cgroup.

## Mature mechanism family 1: systemd cgroups and desktop slices

Systemd’s desktop integration documentation defines three standard user slices:

- `session.slice`: essential processes for the graphical session.
- `app.slice`: normal applications.
- `background.slice`: low-priority background tasks.

The same document states the purpose directly: assign different priorities so the session can run smoothly under load, including reserving memory to session processes, preferentially killing background tasks, and assigning different memory/CPU/IO priorities.

Systemd resource-control options are cgroup controls. The useful ones here are:

- `CPUWeight=`: relative CPU share among sibling cgroups; range 1-10000, default kernel weight 100; `idle` is also supported on cgroup v2.
- `IOWeight=`: relative block IO share among sibling cgroups; range 1-10000, default 100.
- `MemoryLow=` / `MemoryMin=`: memory protection; reclaim prefers unprotected cgroups first. `MemoryLow` is weaker and safer than `MemoryMin`.
- `MemoryHigh=`: throttling limit; systemd describes this as the main mechanism to control memory use. Usage can exceed it if unavoidable, but the cgroup is heavily slowed and reclaimed from.
- `MemoryMax=`: hard last-line limit; systemd recommends using `MemoryHigh` first and `MemoryMax` as defense.
- `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=`: opt cgroups into `systemd-oomd` policy.

For `ouranos`, the near-term production shape should be:

- Keep `niri`, desktop shell/panel, launcher, portals needed for interaction, and maybe a minimal rescue terminal in a protected session-critical slice.
- Keep normal apps in `app.slice`.
- Move agents, local builds, indexing, large deploy/eval work, and batch shell commands into `background.slice` or a dedicated `workload.slice` with lower CPU/IO weight and memory pressure policy.

Important caution: boosting an entire terminal cgroup also boosts the shell and every heavy child process launched inside it. If a terminal window is where Codex/Nix/agents run, boosting the whole Ghostty app scope can accidentally make the heavy work more dangerous. Prefer either:

- protect only the terminal emulator/rescue terminal path and run heavy commands in separate background scopes, or
- keep Ghostty as a normal app while making heavy agent/build wrappers automatically move themselves into a demoted scope.

## Mature mechanism family 2: `systemd-oomd`, PSI, and proactive kill policy

The kernel PSI documentation describes pressure stall information as a way to quantify CPU, memory, and IO contention. It exposes `/proc/pressure/{cpu,memory,io}` and per-cgroup pressure files, with both `some` and `full` stall metrics.

`systemd-oomd` uses cgroup v2 and PSI to take corrective action before kernel-space OOM. It monitors cgroups with `ManagedOOMSwap=` or `ManagedOOMMemoryPressure=` set to `kill`; if thresholds are exceeded, it kills an eligible descendant cgroup.

Two details matter for desktops:

- Swap makes `systemd-oomd` more effective. Without swap, pressure rises more abruptly and the machine may livelock before user space can react.
- Cgroup granularity matters. If all work is in one large terminal/session scope, OOM policy can kill too much. If each agent/build is a separate scope, the system can kill one bad workload rather than the whole desktop.

`ouranos` now has swap, and `oomctl` shows per-Ghostty app scopes monitored. The remaining question is policy: which cgroups should be eligible for pressure kills, which should be protected, and how aggressively background work should be terminated.

## Mature mechanism family 3: IO scheduling, IO weights, and `ionice`

IO pressure was a major problem during swapfile activation: the disk swapfile was created and formatted, and the machine saw very high IO pressure while `mkswap` ran.

Linux has multiple IO control layers:

- `IOWeight=` / cgroup v2 `io.weight`: proportional IO share among cgroups.
- `io.max`: hard byte/IOPS throttling at the cgroup layer.
- Per-process IO priority through `ionice` / `ioprio_set`.
- Device scheduler choices such as BFQ, mq-deadline, kyber, or none.

BFQ is especially relevant historically and theoretically because its kernel documentation explicitly targets personal-system responsiveness under background workloads such as source builds, software updates, file copies, and VMs. BFQ has low-latency heuristics that privilege interactive and soft-realtime applications.

But the current `ouranos` NVMe scheduler did not list BFQ; it showed `none` active with `mq-deadline` and `kyber` available. That means BFQ is not an immediate assumption. IO policy still matters, but the safe near-term path is:

- use cgroup IO limits/weights where supported,
- run known heavy target-side commands with low IO priority,
- make `lojix` activation steps resource-aware rather than avoiding `lojix`,
- avoid assuming BFQ unless a kernel/device experiment confirms it is available and beneficial.

The `ionice` manual/kernel documentation warns that realtime IO can starve the system. For background deploy/build tasks, the safer direction is idle or low best-effort priority. For UI, avoid realtime IO except for narrow audio/video cases with known bounds.

## Mature mechanism family 4: CPU scheduler policy, nice, SCHED_IDLE/BATCH, and autogroup

Classic `nice` helps CPU fairness per process but does not address memory pressure, cgroup-level containment, or IO stall by itself.

Better CPU tools for bulk work:

- `SCHED_IDLE`: extremely low-priority CPU policy; Nix daemon already uses it on `ouranos`.
- `SCHED_BATCH`: non-interactive batch policy, sometimes better for throughput than `nice` while reducing interactivity impact.
- `CPUWeight=`: cgroup-level proportional CPU sharing between slices/scopes.
- `CPUQuota=`: hard cap; useful for runaway background jobs, but too blunt if used as the only tool.

Linux autogroup historically improved desktop interactivity by grouping tasks by session, often corresponding to terminal windows. It helps old “compile in one terminal while using another terminal” scenarios, but it is not enough for this workspace because many heavy processes can live under the same terminal/app scope and because the failure involved memory/IO pressure, not only CPU fairness.

## Production tools and daemons

### `systemd-run` scopes

`systemd-run --user --scope --slice background ...` is the most direct production tool for launching one command in its own cgroup with explicit resource properties. It is ideal for agent/build wrappers because it lets the user keep the terminal interactive while the heavy child is accounted and killable separately.

### `systemd-cgtop`, `oomctl`, PSI tools

`systemd-cgtop` is useful during pressure because it reports by cgroup and is less misleading than per-process RSS views. `oomctl` shows what `systemd-oomd` is monitoring. PSI tools such as `psi-notify` or `psitop` can surface pressure before the desktop feels frozen.

### `ananicy-cpp`

`ananicy-cpp` is an auto-priority daemon with rules for renicing, changing CPU scheduler, changing IO class/nice, setting OOM score, cgroups, autogroup, and systemd integration. It is useful when programs are not launched through controlled wrappers or systemd scopes.

For this workspace, `ananicy-cpp` is a possible later classifier, not the first mechanism. The first mechanism should be declarative Nix/systemd slice policy and explicit wrappers for known heavy work. `ananicy-cpp` is more heuristic/ruleset-driven and could fight declarative placement if introduced too early.

### GameMode

Feral GameMode is a production example of a daemon/library that temporarily changes CPU governor, IO priority, niceness, scheduler behavior, and scripts for a specific foreground process. Its lesson is architectural: a scoped request/daemon model works. The exact tool is game-oriented, not a general desktop survival policy.

### `earlyoom`

`earlyoom` is simpler than `systemd-oomd` and can be effective on desktops, especially with avoid/prefer regexes. It is less cgroup-native than `systemd-oomd`. Since `ouranos` already uses modern systemd and cgroup v2, prefer tuning `systemd-oomd` first before adding a second OOM daemon.

## Newer and experimental mechanisms

### Utilization clamping (`uclamp`)

Kernel `uclamp` lets user space hint minimum and maximum CPU performance points for tasks or cgroups. Android-style top-app/background policy is one of the documented use cases: boost active interactive work and cap background work, especially on heterogeneous/mobile systems.

Local probing did not show `cpu.uclamp.*` files in the current user app cgroup, so this is not an immediate implementation assumption. It remains worth tracking because it maps closely to “top app stays responsive,” but it should not be the first production layer on `ouranos`.

### `latency_nice`

`latency_nice` is a scheduler-hint proposal/work that aims to let latency-sensitive tasks get CPU time sooner without realtime policy. It belongs in the research set, but local probing did not show a visible `latency_nice` field for the current process. Treat it as a future/patch/kernel-version research path until confirmed available in the actual `ouranos` kernel and systemd/Nix exposure.

### `sched_ext`

`sched_ext` allows BPF-defined schedulers that can be loaded/unloaded dynamically and revert to the default scheduler on errors or stalls. It is powerful and active research/production-experiment infrastructure, but it is far too broad for the first safety fix. It belongs in “later lab experiment,” not near-term desktop safety.

## Nix and deploy-specific findings

`nix-daemon` on `ouranos` is already configured as `SCHED_IDLE` and low best-effort IO priority, and NixOS documentation says these daemon scheduling settings propagate to build processes. That means the earlier disaster was not simply “Nix daemon lacks idle priority.” Additional hazards remain:

- Local evaluation, flake fetching/unpacking, deploy wrapper work, and activation phases can still consume resources outside the actual builder process.
- Target-side activation steps like creating/formatting a large swapfile are not Nix builds and are not protected by `nix-daemon` scheduling.
- Shell-launched agents can live in an interactive terminal cgroup unless explicitly moved.
- Remote builder use helps local CPU/RAM pressure but can still generate local copy/unpack/activation IO.

Nix also has experimental `use-cgroups` support for running builds inside cgroups. That is worth testing later, especially if per-build memory accounting/limits become important. It should not replace systemd slice policy around the deploy command and agent shells.

## Recommended design for `ouranos`

### Phase 0: Keep current protection

Keep the newly projected zram + disk swap policy and keep `systemd-oomd` enabled. This gives `ouranos` a memory pressure valve and gives `systemd-oomd` time to react.

### Phase 1: Protect the critical UI path with systemd user slices

Add declarative user-manager drop-ins for the standard desktop slices:

- Raise `session.slice` relative priority above normal apps/background work.
- Add modest `MemoryLow=` protection for session-critical UI components.
- Keep `background.slice` lower than `app.slice` and much lower than `session.slice` for CPU and IO.
- Keep or tune `ManagedOOMMemoryPressure=` on app/background descendants, not on the critical session slice itself.

Candidate critical processes:

- `niri`
- shell/panel process, likely `quickshell`
- launcher
- notification/portal components needed to recover the desktop
- one explicitly designated rescue terminal, if we can prevent heavy children from inheriting the protected cgroup

### Phase 2: Demote heavy work by construction

Add a workspace wrapper for heavy interactive commands that launches them in a background/workload scope:

- agents/Codex sub-workloads,
- Nix builds/checks,
- large local eval/deploy smoke runs,
- cache cleanup/scans,
- indexing and bulk repository operations.

This wrapper should use systemd scopes rather than just `nice`, so the workload is visible in `systemd-cgtop`, can be killed as a group, and can receive CPU/IO/memory policy together.

### Phase 3: Make `lojix` resource-aware, not avoided

The correction from the user is important: `lojix` deployment is not the problem. The problem is unbounded resource pressure in particular phases.

`lojix-run` should remain the human-facing deploy report surface. The improvement should be resource-aware execution:

- local build/eval/copy phases run in a low-priority systemd scope when executed on a desktop host;
- target-side activation phases that can create heavy IO, such as swapfile creation/formatting, run through root SSH in a low-priority target-side scope;
- deploy reports include pressure/elapsed warnings and identify long target-side steps;
- branch refs use `main` for operator-facing deploy requests, per latest correction.

### Phase 4: Add pressure visibility and emergency controls

Add a lightweight pressure UI/CLI layer:

- `psi-notify` or equivalent for desktop warnings when memory/IO pressure crosses thresholds.
- A launcher entry/hotkey for `systemd-cgtop` or a small pressure dashboard.
- A launcher entry/hotkey to kill the current background/workload scope, not random UI processes.
- A convention that agents and bulk commands display their cgroup/scope name in logs/reports.

### Phase 5: Evaluate IO scheduler and deeper scheduler experiments later

After the cgroup/slice policy exists, test whether changing the NVMe scheduler from `none` to `mq-deadline`, `kyber`, or a kernel with BFQ materially improves interactive IO latency under synthetic pressure. Do this in a controlled benchmark, not during normal work.

Track but defer:

- `uclamp` if exposed by the deployed kernel/systemd stack.
- `latency_nice` if available and controllable.
- `sched_ext` schedulers for desktop interactivity experiments.
- `ananicy-cpp` as a classifier if declarative systemd placement is insufficient.

## Concrete next implementation surfaces

Likely repositories/surfaces:

- `CriomOS-home`: user-level systemd drop-ins for `session.slice`, `app.slice`, `background.slice`, pressure notification tooling, and terminal/launcher policy.
- `CriomOS`: system-level `systemd-oomd`, Nix daemon, target-side activation policy, possible hostcritical/system-service slices.
- `lojix-cli` / `CriomOS-home` `lojix-run`: resource-aware local and target-side deploy wrapping while preserving lojix as the deploy mechanism.
- `goldragon` / Horizon projection if the policy should be role/capability-driven rather than host-local.

## Open design questions

1. Should the “rescue terminal” be a dedicated terminal instance/window, or should all Ghostty windows be considered core UI? Dedicated is safer because boosting all Ghostty scopes can also boost heavy agent children.
2. How much memory should be reserved/protected for the interactive session? A conservative starting point is 1-2 GiB via `MemoryLow`, but it should be validated under pressure.
3. What should be killed first under pressure: individual agent scopes, all background work, browser tabs/app scopes, or deploy jobs?
4. Should the first implementation be local to `ouranos`, or expressed as a Horizon-projected desktop capability so future desktops inherit it?

## Sources

- systemd desktop slice model: https://systemd.io/DESKTOP_ENVIRONMENTS/
- systemd resource control manual: https://www.man7.org/linux/man-pages/man5/systemd.resource-control.5.html
- systemd-oomd manual: https://www.man7.org/linux/man-pages/man8/systemd-oomd.service.8.html
- PSI kernel documentation: https://www.kernel.org/doc/html/latest/accounting/psi.html
- BFQ kernel documentation: https://docs.kernel.org/block/bfq-iosched.html
- Block IO priority kernel documentation: https://docs.kernel.org/6.9/block/ioprio.html
- Utilization clamping kernel documentation: https://docs.kernel.org/scheduler/sched-util-clamp.html
- sched_ext kernel documentation: https://docs.kernel.org/scheduler/sched-ext.html
- KDE app-as-systemd-service memory control discussion: https://blogs.kde.org/2024/10/18/limit-application-memory-usage-with-systemd/
- ETH D-PHYS workstation resource-control policy: https://readme.phys.ethz.ch/linux/workstation/resource_control/
- NixOS swap/zram documentation: https://wiki.nixos.org/wiki/Swap
- Nix resource-restricted rebuild discussion: https://discourse.nixos.org/t/feature-request-performance-restricted-rebuilds/59569
- Nix `use-cgroups` setting: https://nix.dev/manual/nix/2.34/command-ref/conf-file.html
- ananicy-cpp: https://github.com/EvoXCX/ananicy-cpp
- Feral GameMode: https://github.com/FeralInteractive/gamemode

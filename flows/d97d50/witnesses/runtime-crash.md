# ChatGPT Desktop runtime-crash witness

Flow: `d97d50`  
Host: `ouranos`  
Observed: 2026-09-03 (CEST)

## Method

This is a read-only runtime investigation. I inspected the live process list, user/system journals, `coredumpctl` metadata and stack traces, the active Nix package and wrapper chain, the current Wayland/GPU/CPU identity, and the current package's JavaScript/native-runtime artifacts. I also performed bounded launches with newly created temporary `HOME`/XDG directories and no conversation data. The first reproduction used a temporary Chromium user-data directory but inherited the real `HOME`; that caveat is recorded below. No conversation contents, browser database contents, or secrets were read, and no existing user process was killed.

## Observations

### Repeated live exit

The current package has five recent `SIGILL` coredumps:

- 2026-09-02 22:12:36, PID 2035255
- 2026-09-02 22:14:20, PID 2036372
- 2026-09-02 22:14:50, PID 2037054
- 2026-09-03 13:56:25, PID 2306246
- 2026-09-03 13:57:48, PID 2307431

All use the current executable
`/nix/store/p3vjdpavgmgqv92wga4palispkbyw17j-chatgpt-unwrapped-26.831.21537/lib/chatgpt/.ChatGPT-wrapped`, all have signal 4 with `ILL_ILLOPN`, and all identify the crashing thread as `git`. Their command line is the packaged executable with `--ozone-platform=wayland`.

A bounded launch of the current wrapper at approximately 14:06 reproduced the same exit. Its coredump (PID 2332312, TID 2333375) records the command line with `--ozone-platform=wayland --user-data-dir=/tmp/chatgpt-runtime-wayland.8tiuCe --enable-logging=stderr --v=1`; the `git` thread again received `SIGILL`.

The repeated stack shape is:

```
#0  .ChatGPT-wrapped + 0xb2d1527
#1  node::GetNodeReport(...) + 0xb2d1e1a
#2  .ChatGPT-wrapped + 0xb2d5ac6
#3+ V8/JIT frames
...
#20 v8::Function::Call(...)
#23 v8::Module::Evaluate(...)
#36 node::worker::MessagePort::OnMessage(...)
#38 uv__io_poll
#39 uv_run
```

The current binary disassembles offset `0xb2d1527` as `ud1 eax,DWORD PTR [eax+0x2]`. The bytes are inside the native `node::TriggerNodeReport` symbol, adjacent to the `node::GetNodeReport` symbol; the same intentional undefined-instruction region is reached by the coredump RIP. This is an explicit undefined-instruction trap in a Node report/fatal path, not evidence of a random GPU page fault or an AVX instruction that the CPU cannot execute. No debugger was available (`gdb` and `eu-addr2line` were absent), so register values and the exact caller argument are unknown.

The older 26.825.51511 package also produced a 2026-09-02 17:48:08 coredump with signal `SIGSEGV` in a thread named `git`. Its stack is largely unsymbolized, so it establishes recurrence of a Git-worker failure pattern across versions but does not establish that its memory fault and the current Node trap have the same immediate cause.

### Current package boundary

The active `chatgpt` profile resolves to the Nix 26.831.21537 package. Its `resources/app.asar` is a regular read-only file with SHA-256
`9745ec1195897c019533d08e8415ab81a3c4e59e845403fdfea42ce1272fe954`, and `resources/codex` is the regular packaged 0.152.1 executable. The ASAR package metadata names the product `Codex` and version `26.831.21537`. The active package therefore matches the vendor archive identity observed by the parent stock-boundary work; no customized ASAR or external Codex symlink was found in this runtime.

The outer profile wrapper invokes the package and unconditionally appends `--ozone-platform=wayland`. The desktop entry itself only invokes `chatgpt %U`. This is the retained Wayland adaptation, separate from the stock ASAR/Core boundary.

The packaged main code creates Node workers as `new Worker(..., {name: this.id, workerData: {workerId: this.id, ...}})`. The packaged worker code has a Git-specific worker identity/path (`workerId === \`git\`` and Git operations), corroborating that the coredump's `git` thread is an application worker rather than the Chromium renderer. This source inspection does not identify which Git operation or input reached the fatal report path.

### Exact historical process-report mapping

The historical `SKIP_PROCESS_REPORT` patch is a byte-length-preserving replacement of `isLinux() && process.report` with `false /* nix:skip report */`. In the current vendor ASAR, that exact text occurs in `/node_modules/@parcel/watcher/node_modules/detect-libc/lib/process.js`; its file-relative match maps to ASAR absolute byte offset 11,010,554 (the prior patch record rounds/identifies the region as 11,010,555). The helper then calls `process.report.getReport()` before inspecting the report's `header` or `sharedObjects`.

The current Git worker dynamically imports `@parcel/watcher` for Linux working-tree watches and selects the `inotify` backend. The stock `@parcel/watcher/index.js` calls `detect-libc`'s `familySync()` to select the glibc native binding. A package-wide static search found no other `process.report` occurrence. This directly maps the coredump's native `GetNodeReport`/`TriggerNodeReport` trap to the historical patch target and makes Git working-tree watcher initialization the leading caller path, but does not prove that this specific run reached the report fallback.

As a bounded source-only check, the vendored `detect-libc` code was evaluated in memory with an instrumented `process.report`: on this host's ordinary Node executable, `familySync()` returned `glibc` without invoking the report, while `versionSync()` invoked the report once after its filesystem fallback. No application source caller of `versionSync()` was found. This check did not run the Electron process and therefore leaves the exact runtime caller unresolved.

### Environment and journal evidence

The desktop session is Wayland (`WAYLAND_DISPLAY=wayland-1`, `DISPLAY=:0`) on Linux 7.1.8. The GPU is Intel Meteor Lake-P using `i915`; the CPU is an Intel Core Ultra 5 125U with AVX/AVX2/AVX-VNNI flags. In the journal windows surrounding the two 13:56–13:58 crashes, systemd-coredump records the signal-4 exits, but there is no matching `i915` hang/reset, GPU fault, Wayland protocol fatal, Electron fatal, or Node textual fatal message. The app scopes report normal process resource accounting before coredump collection.

### Disconfirming bounded probes

With a completely temporary `HOME` and XDG state, direct launches of the inner packaged `ChatGPT` binary survived the 15-second bound in each of these modes:

- explicit Wayland (`--ozone-platform=wayland`)
- explicit X11 (`--ozone-platform=x11`)
- Wayland with `--disable-gpu --disable-gpu-compositing`

The GPU-disabled run emitted the expected application error that GPU access was disabled, then remained alive until the timeout. The Wayland and X11 runs reached normal app/renderer/app-server initialization and also remained alive until timeout. No coredump for these isolated probes was added. These are bounded startup probes only: they did not exercise authenticated UI actions or a long-running session.

The first real-HOME reproduction is weaker as an isolation test: Electron logged that the requested temporary user-data path was a late change and that native startup had selected `/home/li/.config/Codex`. It crashed in the same `git`/Node-report path. This makes existing profile/state involvement plausible, but the launch did not prove it, and a data-preserving real-profile A/B was intentionally not attempted.

### `ELECTRON_RUN_AS_NODE` discriminator (inconclusive)

The requested minimal discriminator was attempted against the active `.ChatGPT-wrapped` binary with `ELECTRON_RUN_AS_NODE=1`, temporary `HOME`/XDG state, and the one-line `process.report.getReport()` expression. The ten-second report invocation returned timeout status `124`; its stderr/stdout instead contain the normal application startup marker, and no one-line result or Node-script exit occurred. The same-binary no-report control (`process.stdout.write("control-ok\\n")`) also returned timeout status `124`, emitted the application startup marker, and never emitted `control-ok`.

One coredump was produced during the first bounded invocation, but it is not the target failure: PID 2363532, TID 2363573 (`Chrome_ChildIOT`), signal `SIGTRAP`, command line `--type=gpu-process --ozone-platform=x11 ...`; its stack is a Chromium GPU-child stack with no `git` thread and no `GetNodeReport`. No new main-process `SIGILL` coredump was produced. Therefore this attempt establishes that this packaged binary ignored or otherwise did not honor `ELECTRON_RUN_AS_NODE=1` at this entry point; it neither confirms nor refutes `SKIP_PROCESS_REPORT`.

## Interpretation

The strongest diagnosis supported by direct evidence is: the packaged application's internal Git worker enters a native Node/V8 report/fatal path, which executes an intentional `ud1` trap and brings down the Electron process. The native trap maps exactly to the only stock JavaScript `process.report` target, vendored `detect-libc` under `@parcel/watcher`; Git working-tree watcher initialization is the leading caller path. This is a runtime/application failure in the Git worker path; the evidence does not show a generic unsupported CPU instruction, GPU reset, or Wayland initialization fault.

Existing profile state may be a trigger because the real-HOME reproduction failed while fresh temporary profiles survived the short bound. That remains a hypothesis. Wayland may still influence the untested full session, but the isolated Wayland probe surviving alongside X11 and GPU-disabled probes weakens it as the primary cause.

## Unknowns and proof gaps

- The exact JavaScript Git operation, input, or native Node report condition that selected the trap is not identified.
- It is not proven whether the crashing Electron instance reached `detect-libc` through `familySync()`'s report fallback, a `versionSync()` path not found statically, or another native/runtime route; no second `process.report` caller was found in the ASAR.
- The run-as-node probe could not reach the requested expression: both the report and no-report controls launched the GUI and timed out, so no direct isolated `process.report.getReport()` versus control comparison exists.
- No debugger/register inspection or symbolized V8 frames was possible because no debugger/symbolizer is installed.
- A clean temporary profile was observed for only 15 seconds and without authenticated conversation/workspace actions; this does not prove long-run stability.
- A real-profile A/B or profile repair was not performed because it could alter user state and the brief prohibited runtime/data mutation.
- The package's own stderr did not expose a textual fatal reason before the coredump; the system journal likewise has no more specific cause.
- The older 26.825 SIGSEGV and current 26.831 SIGILL share the `git` thread name, but their different immediate fault types leave their relationship unresolved.

## Parent-facing conclusion

The current stock package is genuinely crashing shortly after startup, repeatedly and reproducibly, with `SIGILL` in a `git` worker at Node's `GetNodeReport`/`TriggerNodeReport` trap. The trap's exact historical patch target is the vendored `detect-libc` process-report helper used by `@parcel/watcher`; the Git working-tree watcher is the leading static call-path candidate, not a fully proven dynamic caller. Existing profile state may activate it. The evidence does not support treating the current vendor ASAR/Core as customized, nor does it establish Wayland or GPU as the root cause. Decisive proof would require non-mutating capture of the Git worker's triggering operation or debugger state.

## Sources

- `coredumpctl --json=short info 2035255 2036372 2037054 2306246 2307431 2332312`
- `coredumpctl info 2332312` and the corresponding 26.825 coredump 1603053
- `journalctl --since '2026-09-03 13:55:30' --until '2026-09-03 13:59:00'`
- Active package: `/nix/store/p3vjdpavgmgqv92wga4palispkbyw17j-chatgpt-unwrapped-26.831.21537/`
- Bounded probe logs: `/tmp/chatgpt-probe-wayland.vH6FlV/stderr.log`, `/tmp/chatgpt-probe-x11.BYx1Wy/stderr.log`, `/tmp/chatgpt-probe-disable-gpu.J7ev7P/stderr.log`
- Run-as-node discriminator logs: `/tmp/chatgpt-process-report-probe.rzzl0w/report.stderr`, `/tmp/chatgpt-process-report-probe.rzzl0w/report.stdout`, `/tmp/chatgpt-process-report-probe.rzzl0w/control.stderr`, `/tmp/chatgpt-process-report-probe.rzzl0w/control.stdout`; coredump PID 2363532
- Psyche records consulted: `Vision/x11.md`, `flows/01a038be/vision/archive-x11.md`, `flows/01a03e39/vision/lastSuggestion.md`, and the parent stock-boundary witnesses under `flows/4ad49f/`

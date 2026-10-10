# ChatGPT Desktop failure-mechanism analysis

This report relays the read-only analysis performed by child flow
`/root/failure_mechanisms` for parent flow `d97d50`. The parent read the
child's final response but did not independently repeat its ASAR/code
inspection; statements below are therefore attributed child-flow findings,
not parent-witnessed facts. The separate live witness
`../witnesses/runtime-crash.md` supplies the direct crash evidence.

## Child-flow conclusion

The child found that a disappearing window alone would not establish a native
crash. In the stock Linux application, the window becomes visible before
SQLite and app-server initialization, and several later failure paths can
deliberately quit Electron. The live runtime witness subsequently established
a real `SIGILL`, so these clean-shutdown mechanisms remain useful code-path
context rather than the diagnosis of the observed incident.

## Mechanisms found in the stock application

- The extracted stock startup code calls `ensureWindow()`, shows the window,
  and only then initializes SQLite and connects to the app server. A database
  startup failure can display an error and call `app.quit()`; app-server
  startup failure is another possible post-window shutdown path.
- On Linux, `window-all-closed` calls `app.quit()` unless an override is
  enabled. Renderer/window destruction can therefore look like an application
  crash even when the main process takes an orderly shutdown path.
- Renderer diagnostics listen for `render-process-gone`, `did-fail-load`, and
  `unresponsive`, and make one renderer-recovery reload attempt. Repeated
  renderer failure, failed reload, or primary-window destruction can reach the
  Linux no-window shutdown.
- Chromium child failures are classified separately. GPU and launch-failed
  child exits are treated as recoverable/nonfatal; other child failures are
  fatal-reported. That kept GPU/Wayland failure plausible before the live
  witness, but did not prove it.
- The wrapper passes `--ozone-platform=wayland`, twice only when
  `NIXOS_OZONE_WL` is also set. No no-sandbox or GPU-disable flag is present.
  Static binary support for Wayland, sandboxing, and GPU paths establishes no
  failure by itself.
- A second-instance exit exists, but the packaged-Linux path inspected by the
  child does not request the single-instance lock under its normal platform
  conditions. The child therefore rated this mechanism low probability unless
  those conditions differ at runtime.
- The current package has the stock vendor ASAR and a regular bundled Core,
  ruling down missing-Core and locally patched-ASAR corruption.

## Exact process-report mapping

In a follow-up requested by the parent, the failure-mechanisms child inspected
the retired patch and current stock bundle. It found that the historical
`SKIP_PROCESS_REPORT` target replaced `isLinux() && process.report` with
`false`, disabling `process.report.getReport()` in `detect-libc/lib/process.js`
nested under `@parcel/watcher`. The current stock bundle contains that exact
guarded call. The Git worker dynamically imports `@parcel/watcher` for Linux
working-tree watches, and the watcher synchronously calls
`detect-libc.familySync()` while selecting its native binding.

That static path is structurally consistent with the runtime witness's
repeated `SIGILL` in the `git` thread at Node `GetNodeReport` and
`TriggerNodeReport`. It is also the only `process.report` occurrence found in
the ASAR. The child nevertheless found disconfirming uncertainty: the active
binary exposes a detectable glibc interpreter, so the ordinary `familySync()`
path should identify glibc before its report fallback. An unobserved loader
condition, an unfound `versionSync()` route, or another native report/fatal
route may be involved. The parent therefore infers that the restored
process-report path is the leading cause, but does not call the exact dynamic
caller proven.

The runtime child attempted the smallest proposed discriminator by invoking
the packaged binary with `ELECTRON_RUN_AS_NODE=1` against both a report call
and a no-report control. Both launched the GUI and timed out with status `124`;
neither executed its one-line marker. One separate GPU-child `SIGTRAP` occurred
without a Git/report stack. This attempt neither confirms nor refutes the
process-report hypothesis.

## Version follow-up

The declarative-state child separately verified the current signed OpenAI
Debian metadata: its `InRelease` is dated 2026-09-02 and its amd64 index names
ChatGPT `26.901.20858`, SHA-256
`42a6477f22f4136d62321eda7b4697a79da1eb66d61dcb85ab0420860a1a5223`.
The active package is older at `26.831.21537`. That child found no causal link
between age and the exit: the inspected Linux updater marks an update ready
after comparing packaged metadata and relaunches only when installation is
invoked; it does not force exit merely because an update exists.

## Discriminators proposed by the child

1. Capture the foreground child's real wait status; `0` supports orderly quit,
   while signals or conventional `134`/`139` codes support a native abort or
   fault and `137` suggests kill/OOM.
2. Filter startup diagnostics for lifecycle, renderer, GPU, load, SQLite, and
   app-server markers without reading conversation content.
3. Inspect coredump/Crashpad and journal metadata for `SIGSEGV`, `SIGABRT`,
   `SIGILL`, OOM, or a minidump.
4. If renderer diagnostics exist, use the recorded reason and exit code to
   distinguish crash, OOM, launch failure, kill, and clean exit.
5. Compare a bounded isolated-profile run with the real-profile behavior to
   distinguish profile-triggered Git/app-server failure from display/runtime
   failure without changing the real profile.

The runtime child performed items 2, 3, and a bounded form of 5; its direct
witness establishes repeated `SIGILL` in the application's Git worker and
weakens the display-stack hypotheses.

## Source and provenance

- Child flow `/root/failure_mechanisms`, final response delivered 2026-09-03.
- Child flow `/root/declarative_state`, signed-repository follow-up delivered
  2026-09-03.
- [Runtime crash witness](../witnesses/runtime-crash.md)
- [Declarative state report](declarative-state.md)
- [Remembered live stock witness](../../4ad49f/witnesses/live-stock-desktop.md)

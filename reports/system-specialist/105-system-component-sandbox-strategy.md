# System Component Sandbox Strategy

Role: system-specialist  
Date: 2026-05-10

## Summary

We need a reusable sandbox ladder, not one universal sandbox.

Recommended shape:

1. **Pure Nix checks** remain the first gate for every component.
2. **Desktop-lite local sandbox** runs on the workstation for fast GUI-adjacent
   tests. It has two explicit modes: an isolated nested/headless desktop, and a
   host-display mode that deliberately binds the real Wayland socket while
   keeping home, state, runtime, services, and process supervision separate.
3. **Prometheus real-host runner** uses `systemd-nspawn` or a NixOS VM when a
   test needs real systemd/user-service behavior.
4. **Full NixOS VM tests** are mandatory for compositor, terminal lifecycle,
   Ghostty reload, browser, or anything that can plausibly crash the real
   desktop.

This is the important safety line for default runs:

> Host desktop sockets are never inherited accidentally. A scenario may ask for
> host-display mode, but then the test is explicitly accepting compositor
> integration risk and the runner binds only the named socket(s), not the whole
> host runtime directory.

So the local "systemd spawn sandbox" should use systemd primarily as a
supervisor and cgroup boundary. The actual test boundary is private home/state
paths, a private runtime dir, and an explicit D-Bus/display policy. In
isolated mode the display is nested/headless. In host-display mode the display
socket is intentionally projected into the sandbox, while the rest of the
environment stays disposable.

## Why The Previous Incident Changes The Bar

The WezTerm incident was not only a terminal bug. It exposed that our testing
surface was using the real desktop as the laboratory.

For Chroma specifically, the dangerous host surfaces are:

- `WAYLAND_DISPLAY` / `DISPLAY`: talks to the real compositor.
- `DBUS_SESSION_BUS_ADDRESS`: can reload real user services, including Ghostty.
- `XDG_RUNTIME_DIR`: contains the real Wayland socket, user bus, Chroma socket,
  portal sockets, and app IPC.
- `NIRI_SOCKET`, `SWAYSOCK`, `HYPRLAND_INSTANCE_SIGNATURE`: compositor control
  sockets.
- `~/.config`, `~/.local/state`, `~/.cache`: real Chroma/Ghostty/browser/editor
  state.
- `/dev/pts` or terminal inventory: must remain forbidden.

The correct invariant is:

> Test runners may launch terminals and browsers, but those applications must
> believe they are in a disposable desktop session whose services and files are
> owned by the test.

## Tier 0 — Pure Nix / Source Witnesses

This is already the workspace discipline from `skills/testing.md`.

Use it for:

- actor topology scans;
- hard constraints like "no `/dev/pts`", "no raw `tokio::spawn` actor
  runtime", "no shell apply command";
- config parser tests;
- rkyv/NOTA wire fixtures;
- state-store writer/reader chained derivations;
- fake D-Bus services where the behavior is "did Chroma send the right DBus
  method?", not "did Ghostty repaint?".

Chroma should keep most of its tests here. For example, a private
`org.freedesktop.systemd1` D-Bus shim can witness that
`GhosttyThemeConcern` called `ReloadUnit("app-com.mitchellh.ghostty.service",
"replace")` without ever contacting the host user manager.

Expose through `checks.<system>.*` and `nix flake check`.

## Tier 1 — Local Desktop-Lite Sandbox

This is the frictionless local lane the user was asking for. It is not a
malicious-code sandbox. It is an accident-containment sandbox: spawned
processes, config files, state files, service units, and logs live in a
disposable run, while selected integration sockets can be shared when the test
requires them.

It should be a Nix-owned runner, likely:

```text
nix run .#sandbox-desktop-lite -- <scenario.nota>
```

The runner starts one transient user unit with `systemd-run --user` so logs,
cgroups, cleanup, timeouts, and resource limits are owned by systemd. Inside
that unit it creates a disposable environment:

- `HOME=$TMPDIR/home`
- `XDG_CONFIG_HOME=$TMPDIR/home/.config`
- `XDG_STATE_HOME=$TMPDIR/home/.local/state`
- `XDG_CACHE_HOME=$TMPDIR/home/.cache`
- `XDG_RUNTIME_DIR=$TMPDIR/run`
- private `DBUS_SESSION_BUS_ADDRESS` from `dbus-run-session` or
  `dbus-broker-launch`
- display policy:
  - `Display Isolated` means no inherited `WAYLAND_DISPLAY`, `DISPLAY`,
    `NIRI_SOCKET`, `SWAYSOCK`, or `HYPRLAND_INSTANCE_SIGNATURE`
  - `Display HostWayland` binds exactly the current host Wayland socket into
    the private runtime dir and sets `WAYLAND_DISPLAY` to that socket name
- optional nested/headless Wayland compositor

Use systemd execution properties for containment where available:

- `Type=exec`
- `RuntimeMaxSec=...`
- `KillMode=mixed`
- `MemoryMax=...`
- `TasksMax=...`
- `PrivateTmp=yes`
- `PrivateIPC=yes`
- `PrivateNetwork=yes` for tests that do not need network
- `ProtectHome=yes` or an explicit temp `HOME`
- `BindReadOnlyPaths=` only for the Nix store and required fixtures
- `TemporaryFileSystem=` for writable disposable paths

But systemd-run alone is not enough. `systemd-run --user` creates a transient
service in the user's systemd instance. If that service inherits the real
session bus or runtime dir, it can still mutate the real desktop accidentally.
The runner must actively replace those variables and then project back only the
named sockets the scenario requested.

For host-display mode, prefer `systemd-run --user` as the supervisor with a
mount namespace helper such as bubblewrap inside it. That keeps the same user
identity, which makes binding the Wayland socket practical, while still hiding
the host home tree and building a private runtime dir. `systemd-nspawn` can
also bind Wayland sockets, but it is heavier and UID/device handling is more
awkward for fast local desktop integration tests.

### Desktop-Lite Compositor

For tests that need a Wayland server but not the real compositor, use a
headless/nested compositor.

Candidates:

- **wlroots headless backend** for compositor-driven tests. wlroots documents a
  headless backend with no outputs or inputs by default, and explicit headless
  outputs can be added.
- **Sway with wlroots headless/pixman** for a pragmatic first compositor if we
  need a real Wayland session quickly.
- **Weston headless** if the test only needs generic Wayland clients and not
  Niri behavior.
- **Niri in a VM** for Niri-specific behavior. I would not make local nested
  Niri the first target unless we first prove its headless/nested path is stable
  in our stack.

The desktop-lite lane is appropriate for:

- "Chroma writes the right isolated Ghostty config file";
- "Chroma's fake systemd D-Bus reload actor receives the right reload call";
- "a terminal process can start in a disposable Wayland session";
- "a browser can start with a temp profile and never touch the real profile";
- screenshot or pixel smoke tests against nested output.
- "an app can draw on the real display from a private home/runtime tree"
  when the scenario explicitly asks for `Display HostWayland`.

It is not enough for:

- testing that real Ghostty's systemd integration reloads running windows;
- testing compositor crash hazards;
- testing Niri/libwayland failure modes;
- anything where a failure could still take down real user work.

Host-display mode reduces ordinary process/config blast radius. It cannot
guarantee that a compositor or libwayland bug will not affect the live session,
because the sandboxed client is still a real client of the live compositor.

## Tier 2 — Prometheus `systemd-nspawn` Runner

This is the right real-host container lane.

Prometheus is a powerful NixOS/CriomOS machine. Horizon already marks non-edge
builders with `big-parallel` and `kvm`, and `goldragon/datom.nota` shows
Prometheus as a 128 GB x86_64 metal machine. There is already an open BEADS
task, `primary-mm0`, specifying a Clavifaber Prometheus integration runner with
`systemd-nspawn`.

Use this lane when a test needs:

- a real systemd PID 1 inside the sandbox;
- a real user manager inside the sandbox;
- NixOS module activation;
- system services plus user services;
- key material / cert lifecycle tests;
- network namespace behavior;
- service restart/reload semantics that are too fake for Tier 1.

Recommended runner shape:

```text
nix run .#test-on-prometheus -- <scenario.nota>
```

Behavior:

1. Build the test closure locally or through the normal Nix remote-builder path.
2. Copy or realize it on Prometheus.
3. Create an ephemeral NixOS container root from a flake output.
4. Start it with `systemd-nspawn --boot --volatile=overlay` or equivalent
   `.nspawn` configuration.
5. Run the scenario inside the container.
6. Copy artifacts back.
7. Tear the machine down, regardless of success or failure.

Use `--volatile=overlay` / tmpfs state so a failed run does not accumulate
state. Use bind mounts only for:

- `/nix/store` read-only;
- the test closure;
- an artifact output directory;
- explicit device nodes only when the scenario genuinely requires them.

Do not bind the user's real `/home/li`, real `/run/user/$UID`, real Wayland
socket, or real session bus into nspawn.

## Tier 3 — Full NixOS VM

Use a full VM for the tests that matter most to avoiding another terminal
disaster.

NixOS tests start QEMU/KVM VMs and mount the host Nix store, so VM startup is
not as expensive as a traditional disk-image workflow. The NixOS manual also
documents interactive test-driver mode for debugging.

Use this lane for:

- Chroma + Ghostty reload integration with real Ghostty user service;
- Chroma + browser + terminal smoke tests;
- Niri/libwayland/compositor interaction tests;
- full CriomOS-home activation-risk tests;
- "launch several terminals, switch theme, prove terminals survive" tests;
- anything that might crash, kill, or wedge GUI clients.

This should be the default for reproducing any past WezTerm/Niri failure mode.
If it crashes, it crashes the VM, not the operator's session.

## How This Integrates Into The Repos

### Shared Runner Component

Create a small shared runner component rather than copying shell scripts into
every repo.

Possible names:

- `criomos-sandbox`
- `sandboxer`
- `sandbox-runner`

My preference is **`criomos-sandbox`** because the noun names the platform
boundary it owns.

It should expose one Nota CLI:

```text
criomos-sandbox '<Scenario ...>'
```

Initial scenario vocabulary:

```nota
(DesktopLite
  (Name ChromaGhosttyReload)
  (Packages [ chroma ghostty dbus wlroots ])
  (Wayland Headless)
  (Network Off)
  (TimeoutSeconds 30))

(Nspawn
  (Name ClavifaberHostLifecycle)
  (Host prometheus)
  (Root NixOsClosure)
  (TimeoutSeconds 300))

(NixosVm
  (Name ChromaTerminalSurvival)
  (Host prometheus)
  (Interactive false)
  (TimeoutSeconds 300))
```

The CLI should produce an artifact bundle every time:

```text
artifacts/
  scenario.nota
  manifest.nota
  stdout.txt
  stderr.txt
  journal/
  xdg-home/
  screenshots/
  dbus-calls.nota
  actor-trace.nota
  result.nota
```

The artifact bundle is the witness. The chat output should only say where it
landed and whether the typed result was pass/fail.

### Chroma

Add three flake outputs over time:

- `checks.<system>.sandbox-no-host-sockets`
- `apps.<system>.test-desktop-lite`
- `apps.<system>.test-on-prometheus`

Chroma-specific witnesses:

- sandbox env contains no host `WAYLAND_DISPLAY`, `DBUS_SESSION_BUS_ADDRESS`,
  `XDG_RUNTIME_DIR`, or compositor sockets;
- `SetTheme` returns immediately;
- isolated `XDG_CONFIG_HOME/ghostty/config.ghostty` changes;
- fake `org.freedesktop.systemd1` receives exactly one bounded `ReloadUnit`;
- no host Ghostty service sees a reload;
- no `/dev/pts`, OSC, or terminal inventory access occurs;
- repeated `SetTheme` calls do not serialize unrelated concerns.

### Clavifaber

`primary-mm0` is already pointed in the right direction:

- pure Nix writer/reader chain for key/cert/redb artifacts;
- Prometheus runner using `systemd-nspawn`;
- real-host runner shares the same witness reader as the pure test path.

The adjustment from this report is: put the Prometheus/nspawn mechanics in the
shared runner instead of making Clavifaber invent the whole transport.

### CriomOS / CriomOS-home

CriomOS should own the system capability:

- packages needed for `systemd-nspawn`, nested/headless compositor testing,
  D-Bus proxying, and VM acceleration;
- remote-builder features (`kvm`, `big-parallel`) already flow through
  horizon;
- optional system module enabling safe test machines or unprivileged nspawn
  support if we need it.

CriomOS-home should own user-facing test packages only if the test is about the
home profile itself. It should not become the generic sandbox framework.

## Hard Constraints For The Sandbox Runner

These should become tests.

1. **No host desktop sockets by default.** A sandbox run fails if it inherits
   host `WAYLAND_DISPLAY`, `DISPLAY`, `DBUS_SESSION_BUS_ADDRESS`,
   `XDG_RUNTIME_DIR`, `NIRI_SOCKET`, `SWAYSOCK`, or
   `HYPRLAND_INSTANCE_SIGNATURE`. Host-display mode is an explicit scenario
   field, and it binds only the selected socket into a private runtime dir.

2. **No host home by default.** A sandbox run fails if `$HOME`, `$XDG_CONFIG_HOME`,
   `$XDG_STATE_HOME`, or `$XDG_CACHE_HOME` points outside the run directory.

3. **No host Ghostty reload.** Chroma desktop-lite tests use a fake systemd D-Bus
   service or an isolated user manager. They do not call the host user's
   `app-com.mitchellh.ghostty.service`.

4. **Every mutable path is under the artifact root.** If the runner writes
   outside the artifact/run directory, the test fails.

5. **Timeouts are typed, not shell folklore.** Every scenario has a timeout in
   its Nota record. The runner enforces it at the systemd unit/container/VM
   boundary.

6. **Artifact bundle or it did not happen.** Every run emits a `result.nota`,
   logs, and the concrete witness artifacts relevant to the scenario.

7. **VM for crash-risk tests.** If a test can plausibly kill terminals,
   compositor clients, browser sessions, or the whole desktop, it runs in a
   NixOS VM, not the local desktop-lite sandbox.

## Implementation Sequence

1. Add `criomos-sandbox` as a small Rust/Nix component with a Nota scenario
   parser and artifact manifest writer.
2. Implement `DesktopLite` with:
   - transient `systemd-run --user` supervision;
   - private XDG dirs;
   - private D-Bus session;
   - no inherited desktop sockets;
   - fake systemd D-Bus service for Chroma reload tests.
3. Wire Chroma `apps.<system>.test-desktop-lite` to `criomos-sandbox`.
4. Implement `Nspawn` on Prometheus for Clavifaber's `primary-mm0`.
5. Add `NixosVm` runner for terminal/browser/compositor survival tests.
6. Make each repo expose its own named flake outputs; the shared runner is only
   the harness, not the repository's test policy.

## Sources

- Workspace test discipline: `skills/testing.md`.
- Chroma Ghostty/Kameo state:
  `reports/system-specialist/104-chroma-ghostty-kameo-state.md`.
- WezTerm incident analysis:
  `reports/system-specialist/101-chroma-wezterm-crash-suspects.md`.
- Clavifaber sandbox task: BEADS `primary-mm0`.
- NixOS manual, test driver / QEMU/KVM tests:
  <https://nixos.org/manual/nixos/stable/index.html#sec-running-nixos-tests>
- systemd-run transient units:
  <https://www.freedesktop.org/software/systemd/man/systemd-run.html>
- systemd.exec sandboxing and path controls:
  <https://man7.org/linux/man-pages/man5/systemd.exec.5.html>
- systemd-nspawn containers:
  <https://man7.org/linux/man-pages/man1/systemd-nspawn.1.html>
- bubblewrap sandbox model and D-Bus warning:
  <https://github.com/containers/bubblewrap>
- xdg-dbus-proxy:
  <https://github.com/flatpak/xdg-dbus-proxy>
- wlroots headless backend:
  <https://wlroots.pages.freedesktop.org/wlroots/wlr/backend/headless.h.html>
- Ghostty systemd / D-Bus integration:
  <https://ghostty.org/docs/linux/systemd>
- Ghostty GTK single-instance behavior:
  <https://ghostty.org/docs/help/gtk-single-instance>

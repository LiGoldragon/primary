# Chroma end-to-end sandbox harness — results

System-designer lane. 2026-06-04. Host `ouranos` (live Wayland desktop).

## Intent anchors

- **Spirit 2623 — sandbox UI end-to-end testing.** This run is the
  manifestation of that intent: stand up a fully isolated Wayland +
  DBus sandbox and drive the modernized `chroma` through every axis
  without touching the live `:0` session or the live `wl-gammarelay-rs`.
- **Spirit 2620 — report commit discipline** (whole working copy,
  inline message, no `$EDITOR`, set + push `main`).
- Honest reporting: every axis is reported as observed. Where the
  sandbox platform could not exercise an axis end-to-end, that is
  stated plainly and the partial verification that WAS achieved is
  named — no axis is reported as a pass on the strength of a
  CLI `Accepted` alone.

## One-paragraph verdict

The modernized `chroma` (origin/next) builds clean and runs correctly
inside a fully isolated sandbox. **Isolation was proven** and the live
session was untouched before, during, and after. **Theme** flips were
verified at the file level (state file + ghostty config rewrite),
round-trip dark→light→dark. **Warmth and brightness** were verified at
the **DBus wire level** — chroma issues exactly the right
`Set rs.wl.gammarelay {Temperature,Brightness}` calls with the right
value types — but could **not** be verified by reading the gammarelay
property back, because the **headless wlroots backend does not support
the `wlr-gamma-control` protocol**: `wl-gammarelay-rs` reports
`gamma_control::Event::Failed`, drops its only output, and then neither
applies nor retains the property. That is a sandbox-platform limitation,
not a chroma defect.

## Build

| Item | Result |
|---|---|
| Source | `~/wt/github.com/LiGoldragon/chroma/next` (branch `next`, pre-existing worktree) |
| Command | `cargo build --bins` |
| Outcome | **PASS**, exit 0, `Finished dev profile` |
| Artifacts | `target/debug/chroma` (CLI), `target/debug/chroma-daemon` (daemon) |

Note: the daemon binary is named `chroma-daemon` (hyphen) per
`Cargo.toml`, not `chroma_daemon`.

## Harness as built (reproducible / CI-able)

All sandbox artifacts live under `/tmp/chroma-sbx/`. Tools obtained
ephemerally via `nix shell nixpkgs#sway nixpkgs#bc` (sway 1.11 also
provides `swaymsg`); `grim`, `ghostty`, `wl-gammarelay-rs`, `busctl`,
`dbus-run-session`, `dbus-monitor` already on the host.

Isolation model — three nested layers:

1. **DBus isolation.** Everything runs inside `dbus-run-session -- ...`,
   which mints a fresh session bus. The sandbox `wl-gammarelay-rs`
   claims `rs.wl-gammarelay` on THAT bus; the sandbox `chroma-daemon`'s
   `Connection::session()` resolves to THAT bus. The live bus
   (`unix:path=/run/user/1001/bus`) is passed to the OUTER driver only,
   used solely to read-verify the live gammarelay from outside.
2. **Wayland isolation.** A nested `sway` headless compositor
   (`WLR_BACKENDS=headless WLR_LIBINPUT_NO_DEVICES=1`) creates its own
   `wayland-1` socket inside a sandbox `XDG_RUNTIME_DIR`. The live
   `:0` / `wayland-1` desktop is never connected to.
3. **Filesystem isolation.** Sandbox `HOME`, `XDG_CONFIG_HOME`,
   `XDG_STATE_HOME`, `XDG_DATA_HOME`, `XDG_RUNTIME_DIR` all point under
   `/tmp/chroma-sbx/home` and `/tmp/chroma-sbx/run`, so the daemon's
   redb state, the ghostty config rewrite, and the UDS socket never
   touch the user's real dotfiles.

Driver invocation (outer):

```sh
LIVE_DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1001/bus" \
  nix shell nixpkgs#sway nixpkgs#bc \
  --command bash /tmp/chroma-sbx/outer.sh
```

`outer.sh` records the live gammarelay, arms a background watcher for
the isolation gate, then runs `dbus-run-session -- bash inner.sh`.
`inner.sh` (the sandbox body): starts sway headless → captures
`WAYLAND_DISPLAY` from the sandbox runtime dir → starts the sandbox
`wl-gammarelay-rs` and confirms it registers on the sandbox bus →
executes the isolation gate → launches ghostty → starts
`chroma-daemon` (config via `CHROMA_CONFIG=/tmp/chroma-sbx/config.nota`)
→ drives the CLI per axis with timing and DBus readback → teardown.

The full scripts and the chroma config (`config.nota`, a NOTA
`(Config (Theme ...) (Warmth (Schedule (Manual Neutral))) (Brightness
(Schedule (Manual Bright))))` with `Terminal` + `Ghostty` theme
concerns and base16 dark/light palettes) are in `/tmp/chroma-sbx/`.

## Isolation gate — PASS

Before running chroma, `inner.sh` set the SANDBOX gammarelay
temperature to a sentinel (4321 K). The outer watcher then read the
LIVE bus:

```
[outer] LIVE before: Temp=q 6500 Brightness=d 1
[inner] ISOLATION_PROBE sandbox set to 4321 -> reads q 6500
[outer] ISOLATION_GATE: sandbox set to 4321; LIVE reads Temp=q 6500 (expect q 6500)
```

The live gammarelay stayed at 6500 K while the sandbox was being
written — buses are separate. (The sandbox readback also showing 6500
rather than 4321 is the same headless-gamma-control limitation
described below, not a failure of the gate: the point of the gate is
that the LIVE value did not move, which it did not.)

## Per-axis verification matrix

| Axis | CLI call | CLI result | Observed | Verdict |
|---|---|---|---|---|
| Warmth | `(SetWarmthKelvin 3000)` then `6500` | `Accepted`, ~8 ms each | gammarelay property stayed `q 6500`; **DBus trace shows `Set Temperature variant uint16 3000` then `uint16 6500`** | **PASS at wire level**, NOT readback-observable (see limitation) |
| Brightness | `(SetBrightnessPercent 50)` then `100` | `Accepted`, ~8 ms each | gammarelay property stayed `d 1`; **DBus trace shows `Set Brightness variant double 0.5`** | **PASS at wire level**, NOT readback-observable |
| Theme | `(SetTheme Light)` then `(SetTheme Dark)` | `Accepted`, ~8 ms each | state file `current-mode` flipped `dark`→`light`; ghostty `config.ghostty` head became `background = ffffff` (light template); flipped back on `Dark` | **PASS at file level**, NOT screenshot-observable |
| State round-trip | `GetState` | `(State Dark 6500 100)` | typed reply parses, reflects daemon's in-memory state | **PASS** |
| Ramp (optional) | `(StartWarmthRampKelvin (4000 (Seconds 2)))` | `rc=1 NotaParse UnexpectedToken expected u64 got LParen` | n/a | **FAIL (test-input error)** — my ramp NOTA was malformed for the positional schema; not a daemon fault |

### Wire-level proof (warmth + brightness)

A separate `dbus-monitor --session destination=rs.wl-gammarelay
interface=org.freedesktop.DBus.Properties` capture, taken while the
sandbox chroma drove the axes, shows chroma issuing exactly:

```
member=Set  rs.wl.gammarelay  Temperature  variant uint16 3000
member=Set  rs.wl.gammarelay  Brightness   variant double 0.5
member=Set  rs.wl.gammarelay  Temperature  variant uint16 6500
```

Correct interface, path `/`, property names, value types (`q`/`d`),
and values. This is the strongest available proof short of a working
gamma surface: the chroma→gammarelay contract is exercised end-to-end.

## Why warmth/brightness are not readback-observable in this sandbox

`wl-gammarelay-rs` log on the sandbox output:

```
New output: 51
Output 51: name = "HEADLESS-1"
Output 51: gamma_control::Event::Failed
Output 51 removed
```

The wlroots **headless backend does not implement the
`wlr-gamma-control-unstable-v1` protocol**. gammarelay binds the
output, the `gamma_control` setup fails, gammarelay drops the output,
and is then left with zero outputs. With no output it has nothing to
apply a gamma LUT to AND it does not retain the DBus property value —
so a `Set Temperature 3000` followed by a `Get` returns 6500. This was
reproduced both with the pixman renderer and the GL renderer; it is a
property of the headless backend, independent of chroma. (As the task
already noted, warmth/brightness are post-composite gamma LUTs that
`grim` cannot see anyway; the intended verification was the property
readback, which the platform defeats.)

Implication for CI: to observe gammarelay readback you need a backend
that supports gamma-control — a real DRM session, or a nested backend
that proxies gamma-control (sway's nested `wayland` backend on a host
compositor that itself exposes gamma-control). The wire-level
`dbus-monitor` assertion is the backend-independent substitute and is
the recommended CI gate.

## Why theme is not screenshot-observable in this sandbox

The theme axis has two halves: (1) write the new ghostty config +
state files, (2) tell the running ghostty to reload via its GTK DBus
action `com.mitchellh.ghostty / reload-config`. Half (1) succeeded and
is verified on disk. Half (2) failed:

```
chroma-daemon ghostty theme concern error: daemon: ghostty reload-config action timed out
```

The ghostty launched in the headless sandbox never registered a
responsive `com.mitchellh.ghostty` GTK application on the sandbox bus
(GTK app registration failed against the nested session;
`error registering application`). All four `grim -o HEADLESS-1`
screenshots are valid 1280x720 PNGs but **mean luminance 0 (pure
black)** — ghostty's OpenGL renderer started but never painted visible
content onto the headless framebuffer. So no on-screen colour flip
could be captured. The daemon's own behaviour is correct: it writes
the config and fires the reload; in a real session a live ghostty
would consume both. The 1 s reload timeout is graceful (logged, not a
panic, daemon keeps serving).

## Errors / freezes / responsiveness

- **No panics, no hangs, no freezes.** Every CLI call returned in
  3–9 ms; the daemon kept serving after the ghostty-reload timeouts.
- Daemon stderr contained only the expected `ghostty reload-config
  timed out` lines (one per theme apply) and, at teardown, GTK/
  xdg-desktop-portal "connection is closed" noise from ghostty being
  killed as the bus tore down — harmless teardown artifacts.
- Geoclue / sleep-watcher paths did not fire (manual schedules, no
  geolocation needed) — no system-bus access attempted for those in a
  way that affected the run.
- One test-input bug on my side: the optional ramp used malformed NOTA
  (`(StartWarmthRampKelvin (4000 (Seconds 2)))`); the kelvin field is a
  bare positional `u64`, so the daemon correctly rejected it with a
  parse error. Not exercised further.

## Teardown + live-session-untouched confirmation

`inner.sh` killed the daemon, ghostty, sandbox gammarelay, and ran
`swaymsg exit`; `dbus-run-session` then tore down the sandbox bus.
Outer driver, reading the LIVE bus:

```
[outer] LIVE before:          Temp=q 6500 Brightness=d 1
[outer] ISOLATION_GATE: ...   LIVE reads Temp=q 6500
[outer] LIVE after teardown:  Temp=q 6500 Brightness=d 1
```

An independent read of the live bus mid-run (from a separate shell)
also returned `q 6500 / d 1`. **The live `wl-gammarelay-rs` was
6500 K / 1.0 throughout and nothing persists on `:0`.**

## Recommendations

- **CI gate for warmth/brightness:** assert on the `dbus-monitor`
  `Set` trace, not the property readback — it is backend-independent
  and proved decisive here. Keep a readback check only behind a real
  DRM / gamma-control-capable backend.
- **CI gate for theme:** assert on the written `config.ghostty` and
  `current-mode` state file (deterministic), and treat the ghostty
  reload as best-effort. A screenshot gate needs a compositor where
  ghostty actually paints — not the headless backend.
- **Optional harness improvement:** add a tiny DBus stub that claims
  `rs.wl.gammarelay` and simply retains the property, to also assert
  the round-trip value the daemon believes it set (complements the
  wire trace).

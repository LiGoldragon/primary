# Item 46 audit — the "thin Mentci client on Slint"

## Verdict

**Must change before the living can try it on a phone, and must be built
before it can be tried on Linux.** Nothing about Android exists. The only
part that is *witnessed working* is a 66-line pure-Rust unit test of a
fixture that never touches Slint.

Claim by claim:

- `896f36e2…` **exists** — witnessed, it is the branch's first commit.
- `8827f18c` "added an actual window event loop, software backend and
  bounded offline fixture queue" — **half true**. It added an `examples/`
  file that calls `window.run()` and it turned on `renderer-winit-software`.
  It did **not** compile: `8827f18c`/`daa4fe4` put `#[derive(Debug)]` on
  `pub const MAX_QUEUED_REPLIES`, which is not valid Rust. The tip commit
  `1760571` is a one-line deletion of that derive. So the "window event
  loop" landed in a tree that could not build, and was fixed two commits
  later.
- `1760571` "now builds remotely" — **claimed only, no receipt found.**
  I grepped `origin/flow/cf7879`, `origin/flow/efa157` and `origin/main`
  for `1760571`, `daa4fe4`, `slint-connection-poc`: zero hits. The flow
  log's newest Slint entries still say "Compilation remains pending" and
  "one exact-source retry is running". No file in the repository or in
  `flows/cf7879/` names this source with a build result.
- "its separate behavioral check passed 4/4, CLI exit 0" — **true, and I
  reproduced it**, but it proves far less than it sounds: see §3.
- The Slint half is **unbuilt here and unbuildable here**: `cargo build
  --offline --features slint-poc --example slint_connection_poc` fails at
  `failed to download bindgen v0.72.1`. `target/debug/examples/` is empty;
  the deps in `target/debug/deps` predate `1760571` by two hours. No one
  has witnessed this window open, on any platform.

## 1. What the source is

One branch, `proposal/cf7879-slint-connection-poc`, in **mentci-lib**
(`/home/li/wt/github.com/LiGoldragon/mentci-lib/cf7879-slint-connection-poc`,
= `origin/proposal/cf7879-slint-connection-poc`, tip `1760571`). No new
crate and no new repository: it adds three files to the existing
`mentci-lib` crate, **264 lines of hand-written Rust** (136 `src/slint_poc.rs`,
62 `examples/`, 66 `tests/`), plus 5475 lines of `Cargo.lock` and 17 of
`flake.nix`.

Slint **1.17** (lock resolves 1.17.1), optional behind a `slint-poc`
feature, `default-features = false`, features `std, compat-1-2,
backend-winit, renderer-winit-software`.

**Targets declared: none.** No `[target.*]` table, no `.cargo/config.toml`,
no `cargo-apk`, no `xbuild`, no NDK, no `AndroidManifest`, no
`android-activity`, no `crate-type = ["cdylib"]`. A repo-wide grep for
`android|cargo-apk|xbuild|ndk|aarch64-linux-android` outside `Cargo.lock`
returns exactly one hit: a prose sentence in `ARCHITECTURE.md:71`. The
Linux target is implicit (host default) and is the only one.

## 2. What the loop and backend do

`examples/slint_connection_poc.rs` declares an inline `slint::slint!`
component — a `Window` with two `Text` lines, a `TextInput` and a
`Button` — sets the state to `Offline(TransportUnavailable)` before the
window opens, wires the button to `queue_user_reply`, and calls
`window.run()`. That is a real winit event loop with the software
renderer, and it is the whole UI: four widgets, no navigation, no list of
messages, no approval surface, no scrollback. It is a fixture with a
window around it, not a client.

It has never been compiled (see Verdict). Also note `flake.nix` adds only
`pkg-config` + `fontconfig` to `buildInputs`; winit's X11/Wayland
libraries (`libxkbcommon`, `libX11`, `libGL`) are absent, so even a green
`nix flake check` on the `slint-connection-poc` build leg would not mean
the window opens on the living's machine.

## 3. The fixture queue and the 4/4 check

`src/slint_poc.rs` is a `Vec<QueuedReply>` with a `ConnectionState` enum.
"Bounded" = `MAX_QUEUED_REPLIES = 8`, `MAX_REPLY_BYTES = 1024`; over
either, `queue_user_reply` returns `QueueFull`/`TooLong`. Entries leave
only via `acknowledge_transport_acceptance(id)`, which no production code
calls.

I ran it: `cargo test --offline --test slint_connection_poc` →
**4 passed, 0 failed**. The four tests are genuine behavioral assertions
over a real invariant the living cares about — a reply typed offline is
not silently dropped, and reconnecting does not by itself claim delivery
— not change-detectors. But the invariant is cheap, because the code
under test is a bounded `Vec` with no transport to lie about. **The tests
do not link Slint, do not open a window, and do not exercise a single
line of `examples/`.** "4/4, exit 0" is not evidence that anything Slint
works.

## 4. Connection to the cloud harness

**None.** No socket, no `mentci-daemon` client, no persona socket, no
datom message, no server mode, no local-debug-server mode, no provider
call. The module doc says so outright: "without opening a socket,
invoking a model, or treating a queued reply as accepted." `slint_poc` is
deliberately disjoint from the crate's real `ObservationModel`,
`ApprovalModel`, `RenderDatom` and `CriomeVerdict` — it consumes none of
the `signal-mentci` / `meta-signal-criome` types the rest of the crate is
built on. It is a parallel toy, not a thin head on the existing model.

## 5. Android

Nothing runs on Android and nothing is configured for it (§1). The
living's "Slint Android project with Linux and Android target" is, at
`1760571`, a Linux-only example behind an off-by-default cargo feature.

## 6. Nix

`flake.nix` gains two `checks`: `slint-connection-poc`
(`craneLib.cargoBuild`, `--features slint-poc --example
slint_connection_poc`) and `test-slint-connection-poc`
(`craneLib.cargoTest --test slint_connection_poc`). No `packages` output
builds the example, so there is nothing installable or runnable from the
flake — `packages.default` is still the library. Note that
`cargoArtifacts` is `buildDepsOnly commonArgs` *without* `slint-poc`, so
the Slint dependency tree is built inside the check rather than cached,
which is consistent with the flow log's reports of long remote builds.
**No remote build receipt naming `1760571` — or any of these commits —
exists in any branch I can see.**

## Files read

- `/home/li/wt/github.com/LiGoldragon/mentci-lib/cf7879-slint-connection-poc/Cargo.toml`
- `…/src/slint_poc.rs`, `…/src/lib.rs` (head), `…/examples/slint_connection_poc.rs`, `…/tests/slint_connection_poc.rs`
- `…/flake.nix` (whole, and its diff against `dcb5fce`)
- `…/Cargo.lock` (slint entry only)
- `origin/flow/cf7879:flows/cf7879/reports/to-840e42.md`, `…/log.md`, `…/handoff/claude-successor-840e42-ready/{system-prompt,user-prompt}.md`
- Commands run: `git log/diff/show` in the mentci-lib worktree; `cargo test --offline --test slint_connection_poc` (4/4 pass); `cargo build --offline --features slint-poc --example slint_connection_poc` (fails offline).

# Lojix Daemon Production Situation

Variant: Update

## Frame

The psyche asked for a current situation report after the install-first Zeús
handoff in
`reports/system-operator/220-lojix-daemon-install-zeus-deploy-handoff-2026-06-14.md`.
This update checks the production surface, related worktrees, reports, source
repos, open Beads, and local runtime state.

No Spirit capture: this was a current-state work order, not durable intent.

## Current conclusion

The source stack is current and substantially ready for an install-first smoke:
`lojix` main now has the modern daemon shape, two CLIs, binary startup, the
configuration writer, and durable `sema-engine` store self-resume. The
production host surface has not consumed it yet: no installed binaries, no
systemd unit, no `/run/lojix` sockets, and CriomOS-home still installs the
legacy `lojix-run` wrapper around `lojix-cli`.

The next real work is exactly the ordered maintainer chain from the handoff:
package/install first, then smoke the installed daemon/socket contract, then
validate Zeús through that installed daemon.

## Verified source heads

Fetched the relevant repos on 2026-06-14; nothing changed remotely during this
inspection.

- `lojix` main: `efbc5ea8`, clean.
- `signal-lojix` main: `c33e2be4`, clean.
- `meta-signal-lojix` main: `defade02`, clean.
- `CriomOS` main: `b45afb8b`, clean.
- `CriomOS-home` main: `aa4e16c7`, clean.
- `lojix-cli` main: `fc2ff028`; the checkout has a local deleted `result`
  symlink/file only, not source work.

The `lojix` repo still has no repo-local `flake.nix` or Nix checks on main.
That remains the largest installation blocker.

## Current daemon source shape

Current `lojix` main is newer than the older 2026-06-10 audit reports:

- `src/bin/lojix-daemon.rs` accepts one signal/rkyv startup file and rejects
  inline NOTA / `.nota` daemon startup through the component argument boundary.
- `src/bin/lojix-write-configuration.rs` is the NOTA-to-rkyv bootstrap edge.
- `src/bin/lojix.rs` is the ordinary-socket CLI.
- `src/bin/meta-lojix.rs` is the owner/meta-socket CLI.
- `src/client.rs` uses `LOJIX_ORDINARY_SOCKET` and `LOJIX_OWNER_SOCKET`, with
  defaults `/run/lojix/ordinary.sock` and `/run/lojix/owner.sock`.
- `src/lib.rs` now defines `Store::open(...)` over `sema_engine::SemaDatabase`
  and documents `Engine::open` as the self-resume path for persisted rows and
  commit sequence.

So the stale concerns from `reports/operator/359-lojix-modern-component-audit-2026-06-10.md`
about NOTA daemon startup and in-memory state are no longer current for main.
The caveat that remains current is that main lacks a Nix package/check/install
surface.

## Production installation state

Local runtime state is unchanged from the handoff:

- `command -v lojix-daemon`: absent.
- `command -v lojix`: absent.
- `command -v meta-lojix`: absent.
- `command -v lojix-write-configuration`: absent.
- `command -v lojix-run`: present at the Home profile path.
- `/run/lojix`: absent.
- User systemd units matching `lojix*`: none loaded.
- System systemd units matching `lojix*`: none loaded.

CriomOS-home still wires the production operator path to `lojix-cli`:

- `CriomOS-home/flake.nix` input `lojix-cli`.
- `CriomOS-home/packages/lojix-run/default.nix` wraps
  `${lojixCli}/bin/lojix-cli`.
- `CriomOS-home/modules/home/profiles/min/default.nix` installs `lojix-cli`
  and `lojix-run`.

No current production module installs or starts `lojix-daemon`.

## Worktrees

Related worktrees found:

- `~/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape`, clean at
  `74667230`.
- `~/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape`, clean at
  `355d2053`.
- `~/wt/github.com/LiGoldragon/CriomOS/horizon-test-vm`, clean at `9543da26`.
- `~/wt/github.com/LiGoldragon/CriomOS/next` and
  `~/wt/github.com/LiGoldragon/CriomOS-home/next` exist on disk but are not jj
  repos on this machine.

The `horizon-leaner-shape` Lojix worktree has a useful old Nix flake and
daemon smoke scripts, but it predates the current main shape. It uses the old
single-socket `/run/lojix/daemon.sock` model and text `.nota` daemon
configuration files. Treat it as historical implementation evidence only, not
as the install shape to land.

## Beads

The three maintainer Beads are still open and ordered:

- Package/install daemon stack first: `primary-bplu`.
- Smoke installed daemon service and socket contract: `primary-4jtb`, blocked
  by `primary-bplu`.
- Validate Zeús deploy through installed daemon: `primary-3eu2`, blocked by
  `primary-4jtb`.

Direct `bd show` hit the known embedded-Dolt writer lock for two of the three
reads during this inspection. The visible `tools/orchestrate status` list and
the successful `primary-4jtb` read both confirm the intended dependency chain.
All orchestration lanes were idle at inspection time.

## Practical next action

System-maintainer should start with `primary-bplu`: add a Nix package/check
surface for `lojix` main that builds the four binaries with `nota-text` enabled,
then wire an installed service around rkyv startup generation. The final smoke
must use installed binaries and `/run/lojix/*` sockets, not `target/debug`.

System-operator should not revive `horizon-leaner-shape` for this work except
to borrow proven Nix packaging/test idioms; its daemon contract is stale.

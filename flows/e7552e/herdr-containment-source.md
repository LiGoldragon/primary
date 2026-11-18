# Installed Herdr0.8.2 — bounded private launch-path evidence

This is source-only; no server, session, native or transient unit was started.
Actual runtime membership and empty-unit witnesses remain required after admission.

## Exact installed inputs

Executable: `/nix/store/9x03bz0q0a978zrzcshrlmmb4fvcmdb6-herdr-0.8.2/bin/herdr`.
`nix-store -q --deriver` identifies
`/nix/store/ii9l7qb3yc1gnxadwwqbyb0hdmi0m8qg-herdr-0.8.2.drv`.
Its read-only `nix derivation show` names:
- source `/nix/store/3jhxk12n1hhjw4a8y4a6fwiqaf37ydp6-source`;
- patch `/nix/store/kwavh83rncsz0sjqxd7pj6z68f9mi9gx-codex-executable-selection.patch`.

Local upstream `/git/github.com/herdrdev/herdr` has tag `v0.8.2`, annotated
object34ba52cc6ff3b723e6fc0130485ec24582dbe205, commit
`9eb521456ac0d19d3ab3d9d7cea3cca10baa8a4c`.
The source store's Cargo.toml, Cargo.lock, src/main.rs,
src/server/headless.rs, src/pty/backend/unix.rs, src/app/agents.rs and
vendor/portable-pty/src/unix.rs each compare byte-for-byte with that tag's file.
This binds the examined paths to that upstream commit, not an unexamined
whole-tree equivalence or a reproducible binary claim. The derivation's immutable
source-plus-patch is the authoritative installed input set.

## Explicit private server and pane path

At installed source `src/main.rs:588`, the explicit `server` subcommand calls
`server::headless::run_server` directly. It precedes the later default
`server::autodetect::auto_detect_launch` branch. Thus the packet's explicit
`herdr --session proposal2-e7552e server` is not the default attach-or-spawn
path. In `src/server/headless.rs:5045`, run_server initializes its sockets,
configuration and event loop in that process. Its separately requested handoff
import path is not the packet's command.

`src/pty/backend/unix.rs:12–40` opens a native PTY and calls the slave's
`spawn_command`. The vendored `portable-pty/src/unix.rs:228–299` uses a standard
process Command, installs stdio and pre_exec signal/tty setup, calls setsid,
then cmd.spawn. setsid changes session/process-group membership, not cgroup
membership. No cgroup move or external systemd launch appears in this examined
pane spawn path.

`src/app/agents.rs:145–230` starts an agent by encoding its command and sending
bytes into the existing pane PTY. The installed patch replaces the default
executable selection with allowlisted absolute executable resolution, records
that executable and extends the request/config vocabulary. It does not replace
this launch with a systemd service in its examined agent-start body.

These paths support inherited membership in a dedicated operator-owned user
service/scope for ordinary private launches. They do not prove a native binary,
its shell initialization, a plugin, an unexamined branch or a subsequent command
never creates an external process/service. Native prompts remain bounded and
production access is not denied by an OS filesystem sandbox.

## Required runtime witness and cleanup contract

Field must place the entire private controller and all four services under one
unique operator-created transient unit, record its InvocationID and ControlGroup,
and retain ownership of that exact invocation through cleanup. Before signals,
recheck unit identity; stop only that exact unit, never a reused PID/PGID or
production unit. Read each actual private server/appserver/native/PTY-shell
process's /proc identity and cgroup at the native-ready and successor cuts,
correlating the private Herdr pane/session/native identity from agent list/get.
A process outside that exact group is a failed containment witness and must be
handled only by its still-proved live identity, not guessed ownership.

Close the exact two synthetic Flow identities (and actual successor) through
private Flow first, retain private Herdr agent/pane closure, then stop the owned
unit and require its kernel cgroup to be empty/removed after its terminal event.
A top-process pidfd/exit alone proves no descendant containment or cleanup.
Retain evidence and the slot on uncertainty. No runtime proof is claimed here.

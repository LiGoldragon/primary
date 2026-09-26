# `codex-remote-control-next` ownership investigation

Scope: passive observation on `ouranos` only, 2026-09-25. No unit, socket,
configuration, or session was changed. Times below are CST (`-06:00`).

## Finding

The reported restart loop is real. At 2026-09-25 21:37, the declared user unit
was `activating (auto-restart)`, `Restart=on-failure`, `RestartSec=2s`, and
`NRestarts=42845` (it was 42806 at the preceding observation). Its journal
records the precise error: `app-server control socket is already in use at
/home/li/.codex-next/app-server-control/app-server-control.sock`.

The contending owner is not a stale pathname. It is the running transient
`codex-remote-control-next-recovery.service`, created through `systemd-run`:

* systemd reports it `Transient=yes`, active since 2026-09-24 13:49:04, with
  main PID 1998991 and `KillMode=control-group`;
* its actual command has the same isolated next home and exact same configured
  endpoint as the declared service;
* the configured endpoint is a symlink created at 13:49:04 to a private daemon
  socket under `/tmp/codex-daemon-1001/<redacted-id>`; PID 1998991 has the
  listening descriptor for that target and multiple connected descriptors;
* the recovery unit currently has 863 tasks in its cgroup. This is direct
  evidence of a live service and clients, not evidence about the identity or
  intent of any individual user.

The transient journal first shows a `systemd-run` start at 2026-09-24 13:45:31
using an earlier `codex-next-0.158.0-alpha.9` store output. That invocation was
stopped at 13:49:04 and another `systemd-run` start used the current store
output. The retained journal has no initiating client PID, terminal, command
line, or actor attribution. Thus the mechanism and bounded time are witnessed;
who submitted the request is unknown.

Proof grades: **W** for unit state, restart count, journal errors, transient
metadata, endpoint indirection, and listening PID; **I** for the matching
authored-source checkout below; **U** for the submitting actor and for a
runtime derivation-to-worktree provenance link.

## Declarative path

`systemctl --user cat` resolves the enabled fragment through:

1. `/home/li/.config/systemd/user/codex-remote-control-next.service`
2. `/nix/store/zv4s8czixqg1kfd5ra2xcvvbw5fp64p0-home-manager-files/.config/systemd/user/codex-remote-control-next.service`
3. `/nix/store/qdc1vmw9v01gd9hfxy6vkn3gym496p2v-codex-remote-control-next.service/codex-remote-control-next.service`

The active Home Manager profile link is
`/home/li/.local/state/nix/profiles/home-manager -> home-manager-1032-link`.
The generated unit output derives from
`/nix/store/hgrx10rixd6741sz9xky7sjh8ykg46gf-codex-remote-control-next.service.drv`.
The linked unit file was updated at 2026-09-24 18:43:09.

The matching authored module is
`/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-astra-5f38bc-flow-pins/modules/home/profiles/min/codex-next.nix`:

* lines 10–13 define the package, isolated home, endpoint, and prepare script;
* lines 64–76 declare `systemd.user.services.codex-remote-control-next`, its
  `CODEX_HOME`, `ExecStartPre`, `ExecStart`, restart policy, and enablement.

That checkout is at `04446e78d46531a042edbeace68eb72d6e3bacd3`
(`Integrate Herdr Codex next-home hook repair`, 2026-09-24 18:31:55 CST). Its
preceding file-touching commit is `bde3bb7faf24` (`Configure Flow stable and
next Codex runtime endpoints`). The source text reproduces the active fragment
fields, and its timestamp precedes the unit-link update by about 12 minutes.
Nix store metadata does not embed the originating checkout revision, so this
is a strong temporal/textual match, not proof that this checkout was the exact
evaluation input. The sender's claim about CriomOS-home main is compatible with
the evidence: the declaration was found in a worktree, not established on main.

## Proposed declared repair

Change the service declaration at the module above, inside
`systemd.user.services.codex-remote-control-next.Unit`, to declare the
recovery unit mutually exclusive:

```nix
Unit = {
  Description = "Codex Remote Control next server";
  Conflicts = [ "codex-remote-control-next-recovery.service" ];
  After = [ "codex-remote-control-next-recovery.service" ];
};
```

This makes the declared service the sole systemd owner after an intentional
transition: systemd will stop the conflicting transient before starting the
declared service. The `After` ordering makes that handoff order explicit.
The same source should retain one canonical endpoint and should not add an
unconditional `ExecStartPre` socket unlink. The current conflict is a live
listener behind an endpoint symlink; unlinking it while PID 1998991 lives does
not transfer the listener safely and can strand clients or create two daemon
namespaces.

This is a proposed source change only. It has not been evaluated, built,
activated, or tested in this investigation.

## Safe-transition conditions

Stopping the transient now would stop its main process and, because
`KillMode=control-group`, its observed 863-task cgroup. The live listening
socket and its connected descriptors would disappear with it. Existing Codex
sessions served by that app server would therefore lose their server process;
whether individual clients can reconnect or resume is not established here.

Do not transition while the recovery cgroup has active session work or open
client connections. A later operator should first witness all of the following
without sending a request to the app server:

1. an agreed maintenance window and confirmation from owners of live sessions;
2. recovery `TasksCurrent` and the socket's connected-descriptor count have
   reached an agreed quiescent baseline;
3. a backed-up, reviewable declaration containing the `Conflicts`/`After`
   handoff, with its intended Home Manager generation identified;
4. a rollback plan that restores the prior known-good generation if the
   declared service does not become the single listener.

Only then should an authorized activation and one controlled stop/start be
performed. A successful transition must be witnessed by the declared unit
remaining active, the transient unit absent/inactive, the endpoint resolving
to the declared server's listener, and `NRestarts` remaining stable.

## Sources

* Live read-only systemd: `systemctl --user cat/show/status` for both units;
  fragment, transient metadata, restart count, cgroup policy, and timestamps.
* Live read-only journal: `journalctl --user -u
  codex-remote-control-next{,-recovery}.service`, 2026-09-24 12:00–14:00 and
  2026-09-25 21:33–21:36.
* Live passive endpoint inspection: directory metadata and `lsof -a -p
  1998991 -U`; no connection was opened.
* Generated source chain and derivation: paths listed in “Declarative path”;
  `nix-store -q --deriver/--references` only on those known paths.
* Authored candidate source and revision: the CriomOS-home worktree and lines
  specified above, inspected with `jj`.

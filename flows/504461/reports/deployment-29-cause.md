# Deployment 29 causal diagnosis

## Conclusion

Deployment 29 is durably terminal as `Failed.{ Activate ActivationFailed }`.
The only recorded activation result is the Home Manager generation
`/nix/store/f5kp8yn2q9r5912i9hywaqdkjv0rdbhp-home-manager-generation/activate`,
exit status `1`, with an empty captured error string. The evidence does not
identify the command that returned `1`, so no single cause is established.

The leading, time-correlated hypothesis is that an activation-induced restart
of `flow-nexus.service` installed a unit without
`FLOW_CODEX_STABLE_CLIENT`, causing an immediate panic and a restart loop.
This is a causal candidate, not a proved cause of the activation script's exit
status. A separate second activation window shows the Codex-next service
repeatedly failing because its control socket already existed. That window is
also not durably bound to deployment 29.

## Method and scope

At 2026-09-26, this report used only passive interfaces on Ouranos:

- `lojix 'Query.ByDeployment.{ 29 }'`
- `lojix 'Query.ByEventLog.{ 680 765 }'`
- read-only user-journal queries over 2026-09-24 activation windows
- `stat`, `readlink`, and read-only inspection of the recorded generation's
  `activate` script and Home Manager profile links.

No build, evaluation, deployment request, activation, service change, profile
change, cleanup, or source/configuration edit was performed. The report does
not use current pins as evidence about deployment 29.

## Durable deployment evidence

The deployment query returned one record:

```text
{ 29 29
  { UserEnvironment.li goldragon ouranos UserEnvironment
    UserEnvironment.ActivateNow LiveActivation RequireImmutable
    Some.90702b6e9aa3aa9b82b4f17c5f2bd566d0abc030 }
  Some.{ 698 698 }
  Failed Some.{ 722 722 }
  Some.Failed.{ Activate ActivationFailed
    Some.{ Some.{
      /nix/store/f5kp8yn2q9r5912i9hywaqdkjv0rdbhp-home-manager-generation/activate
      [] Some.1 }
      «» False } } }
```

Thus the durable record proves admission-state marker 698, terminal-state
marker 722, failure at `Activate`, exit status 1, and an empty error field. It
does not include wall-clock timestamps, stdout/stderr, the failing command, or
a target-side service result. The event-log query returned no events in the
requested 680 through 765 range, so it supplies no additional chronology.

The generation script exists. Its metadata has Nix's fixed timestamp
`1969-12-31T18:00:01-06:00`, which cannot date execution. Its text confirms
that it runs Home Manager activation and that `hmDriverVersion=0`; it does not
itself identify which activation stage produced exit 1.

## First versus second local activation windows

### First window: 2026-09-24 16:14:28 CDT

Profile links were written at `16:14:28.953862973` and
`16:14:28.986863026`:

```text
.nix-profile-8-link-5-link -> c0dj6b...-profile
.nix-profile-8-link-6-link -> njw418...-profile
```

At `16:14:28.159954`, `hm-activate-li[2670141]` logged `Starting Home
Manager activation`. At `16:14:29.136551`, it logged:

```text
Stopping units: codex-remote-control.service, flow-nexus.service, message-daemon.service
```

At `16:14:29.914646`, it logged that it was starting those units plus
`criomos-ui-priority.service` and `set-SSH_AUTH_SOCK.service`. Twenty
milliseconds later, at `16:14:29.934776`, Flow Nexus panicked:

```text
FLOW_CODEX_STABLE_CLIENT must be configured
```

Systemd recorded exit status `101` and then repeated restarts. The repeated
same panic is observed through at least 16:16:xx. This is direct evidence of a
degraded Flow Nexus after this Home Manager activation window.

### Second window: 2026-09-24 16:43:48 CDT

Profile links were written at `16:43:48.408161916` and
`16:43:48.436915791`:

```text
.nix-profile-8-link-7-link -> c0dj6b...-profile
.nix-profile-8-link-8-link -> xrajzr...-profile
```

At `16:43:48.353573`, `hm-activate-li[2786984]` logged the compatibility
stage; at `16:43:48.565717`, it stopped `flow-nexus.service`; and at
`16:43:48.765613`, it started `codex-remote-control-next.service`,
`criomos-ui-priority.service`, `flow-nexus.service`, and
`set-SSH_AUTH_SOCK.service`.

At `16:43:48.828674`, Codex-next reported that its app-server control socket
was already in use. Systemd recorded status `1/FAILURE` and repeated the
service restart throughout the inspected window. This is direct evidence of a
Codex-next socket collision after the second Home Manager window.

Neither journal window names deployment 29 or the recorded
`f5kp8y.../activate` path. The links show profile mutations, but not the
identity of the Lojix deployment that caused them. They must not be collapsed
into one attempt or asserted as a proven deployment-29 chronology.

## Ranked hypotheses

1. **Flow Nexus unit environment omission during the first activation window —
   plausible, not proved.** The activation stopped and started Flow Nexus; the
   restarted process immediately and repeatedly panicked because
   `FLOW_CODEX_STABLE_CLIENT` was absent. This is the strongest contemporaneous
   service failure. Disconfirming limit: Home Manager logged the start request
   before the panic, and the durable record does not expose the activation
   script's failing command or connect this window to deployment 29.

2. **Codex-next control-socket collision during the second activation window —
   plausible for that window, not proved for deployment 29.** The restart was
   requested by Home Manager, then the service failed with the exact existing
   socket error and continued to restart. Disconfirming limit: it concerns a
   different service and the journal has no deployment identifier or recorded
   generation path.

3. **Profile-link clobber as the primary cause — unproved and weak.** Both
   windows have paired profile-link writes and later links supersede them.
   That establishes profile activity, not a failed link operation. No inspected
   journal line reports a link error, and the durable error string is empty.

4. **An unrecorded activation-script stage — unresolved.** The recorded
   generation script has many stages, and the durable result contains neither
   its stderr nor an internal stage name. This remains possible precisely
   because the available evidence cannot identify the exit-1 producer.

## Current profile state and limits

At inspection, `/home/li/.nix-profile` resolves through
`.nix-profile-8-link` to
`/nix/store/i69j84zxsjxppa0ihq1x2ch1y5rga74m-profile`, written at
`2026-09-25T20:52:09.178849630-06:00`. It is later than both September 24
windows, so it is not evidence of deployment 29's resulting profile.

`hm-activate-li.service` has no installed unit file, and a direct
unit-journal query returned no retained unit entries. The logs used above came
from the persistent user journal. No journal record of the exact recorded
generation path was found. Lojix's event log returned no relevant retained
events. Therefore the following remain unknown:

- exact wall-clock start and finish for deployment 29;
- whether either local window was deployment 29;
- the exact command that exited 1;
- whether either service failure propagated to the activation script;
- the target profile and runtime state immediately after deployment 29.

## Sources

- Lojix ordinary query observed 2026-09-26: `Query.ByDeployment.{ 29 }`.
- Lojix ordinary query observed 2026-09-26: `Query.ByEventLog.{ 680 765 }`.
- Ouranos user journal, ISO-precise windows 2026-09-24 16:14:20–16:16:20 and
  16:43:35–16:45:00 CDT.
- Ouranos profile-link metadata observed 2026-09-26.
- `/nix/store/f5kp8yn2q9r5912i9hywaqdkjv0rdbhp-home-manager-generation/activate`,
  read only.

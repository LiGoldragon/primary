# Activation readiness witness

Date of observation: 2026-09-05. This witness is a read-only inspection of the
Lojix ledger, the local profile and Home Manager roots, the user service, the
running process, and the daemon journal. No deployment, activation, restart,
rollback, profile switch, or Home activation was performed. The only command
that executed a managed application was the diagnostic `codium
--list-extensions` invocation described below; it exited with status 1 before
the activation workflow could proceed.

## Current ledger state

The running daemon is Lojix 0.20.3 from
`/nix/store/m0a78avygnw9ywxvhnk8ldmdrn8kmdgz-lojix-0.20.3/bin/lojix-daemon`.
The Lojix source checkout is clean at `main@origin` revision
`d3c0ac9032250e0b12ade7d8c71a8fc8311ab5bf`.

The ordinary-socket queries returned these records:

* Deployment 189 is `UserEnvironment.li` on `goldragon/ouranos`,
  `ActivateNow / LiveActivation / RequireImmutable`, target
  `840ed01...f8b`, and is `Completed / Succeeded`.
* Deployment 190 has the same activation mode and target
  `bc0dc048844ebee2bf442ffa050fc9eda02bc417`. It was accepted at event 4948,
  failed at event 4972, and is durably
  `Failed(Activate, ActivationFailed)`.
* Deployment 191 is a successful `Realize / ProfileOnly` for the CriomOS
  consumer revision `f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`.
* Deployment 192 is a successful `Realize / ProfileOnly` for target
  `f8cda8539d01b38ab689de44be2ec3195f34e6d4`.

`Query.ByGeneration.(189)` reports deployment 189 as the node's `Current`
generation. `Query.ByGeneration.(191)` and `(192)` return no generation
listing, as expected for profile-only realizations. The failed deployment's
event range is not recoverable through the ordinary ledger query:
`Query.ByEventLog.(4948 4972)` returned an empty event vector. The daemon
journal around the failure contains only:

```
lojix deploy pipeline effect failed at Activate
lojix deploy pipeline reached a terminal state
```

Therefore deployment 190 proves a failed activation and its durable boundary,
but does not prove the underlying activation command or hook that failed. The
stored candidate activation script does identify a concrete failure path:
both the candidate
`/nix/store/m09spn0qw2xsarggbdqyn2m8ycc78c29-home-manager-generation/activate`
and the current generation's script run
`/nix/store/g015rx9m69kmsfmjn1ksr2v4sffpfzaq-vscodium-casual-managed/bin/codium --list-extensions` when the
immutable extension manifest changes. Running that exact managed wrapper
read-only now exits 1 with:

```
criomos-codium: Managed extension state is inconsistent. Contact the system steward; no extension collision was overwritten.
```

The user manifest currently hashes identically to the candidate m09 manifest,
while the current-home generation 189 carries a different manifest. That is
consistent with the earlier partial activation having advanced the file before
the hook failed. The direct reproduction makes this hook failure a concrete
explanation for deployment 190, although the old ledger cannot retain the
original command's stderr.

The current CriomOS checkout is at `main@origin` `fd6e2752`, whose flake pins
CriomOS-home `befd92780ffe4c0ed9de002d73ec7aff158d4d91`. The earlier successful
profile-only deployment 191 used CriomOS `f3d8b2ca...`; therefore its success
does not establish the latest consumer/Home pair. Home now has three separate
post-`5be71211` commits relevant to this activation: `befd9278` (now the
Home `main@origin`) removes the broken VSCodium hook, `590bb084` updates Codex
to 0.153.4, and `dc3f3f97` resets the Wispr microphone freshness cursor on
reconnect. The latter two remain siblings of befd, so the final evaluated Home
input must be a descendant carrying the required subset together; pinning only
one of them silently drops the others. The provider revision
`033231a1255024447c6a4183c41f4ea9c1fa063f` is the
requested provider identity from the flow brief and must be checked against
the final proposal before activation; it is not inferred from deployment
190's older target.

## Current live state

The profile and process are split across generations:

* `/home/li/.nix-profile` resolves to
  `/nix/store/b1bwfma32f037fsnhpx3n6s2skwbpx6r-profile`; its `codex` resolves
  to `/nix/store/2rzjdcncylii9dsv718sh48f96dv87ag-codex/bin/codex` and reports
  `codex-cli 0.153.3`.
* The Home Manager `current-home` GC root still resolves to
  `/nix/store/4idm37b4awlkk1yj3w6j61cn3a0hinih-home-manager-generation`, the
  generation recorded by deployment 189.
* `systemctl --user show codex-remote-control.service` reports an active unit
  whose `ExecStart` is the 0.153.3 path
  `/nix/store/2ha03shy4vc7hvf4xnmd4vp6v81p1ng7-codex-0.153.3/bin/codex`, with
  `MainPID=3137277`, `NRestarts=0`.
* PID 3137277 is still executing
  `/nix/store/dm1j71ksfqhsbirdqqnjkx9lk26w7i4i-codex-0.153.2/bin/codex`
  (its resolved executable is the corresponding `.codex-wrapped`), with the
  remote-control socket listening.

This is a concrete leftover activation boundary: the loaded unit and profile
describe 0.153.3 while the live owner process is 0.153.2. A successful final
activation that carries the requested Codex update must reconcile this owner,
including a restart when the executable path changes. The post-activation
proof must independently compare the loaded unit, profile binary, process
executable and reported version, socket ownership, and restart count. A
successful Lojix ledger result alone is insufficient to establish that
convergence.

## Lojix failure-reporting limitation

In the current source, `EffectFailure` in `src/runtime_flow.rs` carries a
detail string. `NixCommand::run` supplies command output in that string, but
`fail_pipeline` and `fail_test_pipeline` in `src/schema_runtime.rs` print only
the effect stage and discard it. The deployment phase event constructor also
accepts `_detail: Option<String>` and ignores it. The current terminal schema
has failure stage and terminal reason but no failure detail field. Thus a
future activation failure will still have the same bounded evidence shape: a
durable terminal failure plus a generic journal line, without the command
diagnostic in the ledger.

This is a real observability defect, but it is not a prerequisite for proving a
successful activation. Repairing it durably would require a coordinated signal
schema/wire/store change, not a safe one-line change in this activation lane.
The necessary activation-side repair is to ensure the final Home revision
includes committed `befd9278` (so it no longer invokes the broken VSCodium
hook) and to reconcile the Codex owner process described above. No Lojix source
repair, test, deployment, restart,
rollback, profile switch, or Home activation was begun. If the requested
activation fails again, capture profile, generation, unit, process, socket,
journal, and ledger state immediately and stop before any retry or rollback;
do not infer the cause from `ActivationFailed` alone.

## Exact next gate

Before activation, the parent flow must finish the coordinated provider and
consumer revision, combine the required sibling Home commits into one
evaluated input, evaluate/build it through the remote builder path, and reserve
the explicit proposal and transport:

```
/git/github.com/LiGoldragon/goldragon/proposal.datom
ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome
```

The activation request must target `UserEnvironment.li` on
`goldragon/ouranos`. After it completes, require all of the following
independent observations before calling the request ready:

1. Lojix reports the new deployment `Completed / Succeeded` and the node's
   `Current` generation is the requested target.
2. The Home Manager current-home root and `/home/li/.nix-profile` resolve to
   the new generation/profile, and the generated Codex unit contains the final
   requested Codex version.
3. The active Codex process is the executable and version declared by that
   unit, has one owner of the expected socket, and remains stable after the
   restart window (`NRestarts` does not continue increasing).
4. The deployment journal and Lojix event range are captured as evidence. If
   the result is a failure, treat the missing effect detail as an unresolved
   diagnostic gap and do not retry from the terminal record alone.

## Sources

Method: direct local reads and read-only commands; Lojix queries were sent
through the ordinary socket. No claim above relies on the earlier deployment
interpretation except where it is explicitly called a hypothesis.

* `/git/github.com/LiGoldragon/lojix/src/runtime_flow.rs`
* `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
* Home revisions `befd92780ffe4c0ed9de002d73ec7aff158d4d91`,
  `590bb08428a09596d9d5fbc3adf054d0027bc567`, and
  `dc3f3f9779eb36ae460676754c565c9c13a338a8`
* `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
* `/home/li/.nix-profile`, `/home/li/.local/state/home-manager/gcroots/current-home`
* `systemctl --user show codex-remote-control.service`
* `/proc/3137277/cmdline`, `/proc/3137277/exe`
* Lojix `Query.ByDeployment`, `Query.ByGeneration`, and `Query.ByEventLog`
  results at ledger position 5018
* `journalctl -u lojix-daemon.service --since '2026-09-05 01:50:00'
  --until '2026-09-05 01:50:30' -o cat`

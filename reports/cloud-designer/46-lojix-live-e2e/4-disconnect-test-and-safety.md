# 46 · Lojix live e2e (S5) — disconnect test, resources, safety/rollback

cloud-designer, READ-ONLY reconnaissance, 2026-06-13. Dimension 4 of the
live-e2e grounding (frame: `0-frame-and-method.md`). Every claim cites a file
read or a command run. Nothing live was mutated: no VM run, no deploy, no
`nixos-rebuild`, no `nix copy` to a host, no service start/stop, no write on
Prometheus. The only Prometheus contact was read-only inspection
(`nproc`/`free`/`nixos-version`/`ls`/`is-system-running`) and a read-only
`nix eval`.

## The two disconnect surfaces (both must be proven)

up9q bundles two independent survival properties
(`reports/cloud-designer/45-lojix-activation-survival/3-disconnect-survival-model.md:37-53`;
lojix `INTENT.md:82-86`):

- **S4b — client -> daemon.** The deploy is owned by a daemon-lifetime job
  actor, decoupled from the owner-socket connection task; killing the
  `meta-lojix` client mid-deploy cannot cancel the pipeline.
- **S4a — daemon -> target.** BootOnce activation runs inside a target-side
  `systemd-run --collect` transient unit owned by PID 1; the daemon's ssh
  to the VM dropping mid-activation leaves the unit running to completion.

## S4b proof — client -> daemon survival

Grounding (lojix `src/daemon.rs`):
- `serve_owner` decodes the owner frame and, for `Deploy`, calls
  `submit_deploy` — NOT the inline pipeline (`daemon.rs:321-326`). The comment
  is explicit: "A `Deploy` decouples from this connection task; the deploy-job
  actor owns the pipeline, this task only submits and replies the accepted
  handle" (`daemon.rs:321-324`).
- `submit_deploy` `ask`s the daemon-lifetime `DeployJobs` actor (`ActorRef`
  on `LojixRuntime`, not the connection task) and returns the immediate
  `Deployed`/`DeployRejected` reply (`daemon.rs:343-367`). "Dropping it (a
  client disconnect) cannot cancel the spawned pipeline" (`daemon.rs:348-350`).
- `DeployJobs::launch_pipeline` spawns the full effect chain as an independent
  `tokio::spawn` on the daemon runtime: "Because the task is spawned on the
  runtime (not the owner connection's task), dropping the connection ... never
  cancels it. THIS is the decoupling" (`daemon.rs:524-537`).

### Concrete S4b disconnect test

1. Issue a `BootOnce` `Deploy` via `meta-lojix` against the VM node. Capture
   the `Deployed (AcceptedDeploy ...)` reply — it carries the
   `DeploymentIdentifier` and `DatabaseMarker`
   (`meta-signal-lojix/schema/lib.schema:114`).
2. Mid-deploy (after the immediate reply, while build/copy/activate run), drop
   the client. Two equivalent kills: `meta-lojix` already returned and exited
   (the request is fire-and-forget — the reply lands *before* any pipeline
   effect, `daemon.rs:344-350`), so to test an *in-flight* connection drop,
   issue from a shell whose connection you sever (kill the `ssh`/socket carrying
   the client), OR simply observe that the already-exited client left the job
   running. The decoupling means there is no client connection held open across
   the pipeline to begin with — the reply is synchronous-on-admit.
3. Confirm the daemon carried the deploy to completion via the ordinary-socket
   `Query` / event log (the daemon's own state, not the client):
   - Event log: `lojix "(ReadEventLog (EventLogRange <from> <until>))"` -> a
     `DeploymentPhaseEvent` stream advancing `Submitted -> Building -> Built ->
     Copying -> Activating? -> Activated` for that `DeploymentIdentifier`
     (`signal-lojix/schema/lib.schema:90-99`). Note: there is **no `Activating`
     event-log phase emitted** — `Activating` is only the durable job-row resume
     cursor; the log goes `Copying` then `Activated` (`schema_runtime.rs:984-987`).
   - Live-set: `lojix "(Query (ByNode <selector>))"` -> a `Generation` in the
     `BootPending` slot for BootOnce (`signal-lojix/schema/lib.schema:57,60-70`;
     `schema_runtime.rs:1802` maps BootOnce -> `BootPending`).
   The success criterion is that these show completion **with the client gone**.

## S4a proof — daemon -> target survival (BootOnce transient unit)

Grounding (`lojix/src/schema_runtime.rs`):
- `systemd_run_invocation` wraps the boot-once script in
  `systemd-run --unit=<name> --collect --wait --service-type=oneshot /bin/sh
  -c <script>` over ssh (`schema_runtime.rs:2459-2471`). "owned by PID 1, not
  the dispatcher's ssh, so a network blip that kills the ssh leaves the unit
  running on the target to completion" (`schema_runtime.rs:2380-2382`);
  "if it dies the unit runs to completion regardless" (`2456-2458`).
- The boot-once script is headless-safe rollback: `OLD` = `bootctl status`
  Current Entry (running gen), set the new closure +
  `switch-to-configuration boot`, then `bootctl set-default $OLD` +
  `bootctl set-oneshot $NEW` (`schema_runtime.rs:2435-2453`). reboot 1 lands
  NEW; reboot 2+ auto-returns to OLD.

### FINDING — the live unit name is time/pid, not the deterministic cursor

The unit actually placed on the target is
`lojix-boot-once-{seconds:x}-{process:x}` — `run_boot_once` calls
`self.unit_name()` (`schema_runtime.rs:2544-2550`, `2421-2428`), and
`run_activate_generation` carries no unit name on the command
(`schema_runtime.rs:1778-1795`). The persisted resume cursor, by contrast, is
the deterministic `lojix-boot-once-deploy-{deployment_identifier}`
(`schema_runtime.rs:512-517`), recorded into the `DeployJob` row and surfaced by
`DeployJobResumption::PollActivationUnit { unit }`
(`schema_runtime.rs:546-554,565-582`). **These two names do not match.** So:
- For the disconnect *observation*, the real unit is the time/pid form —
  observe with a glob, not the cursor name.
- The daemon-restart resume path that intends to `journalctl -u <cursor-unit>`
  (`daemon.rs:548-569` leaves S5 to wire this) would poll a unit name the live
  activation never used. Flag this as an S4b/S5 reconcile gap to the synthesis
  and operator: either thread the deterministic name into
  `systemd_run_invocation`, or have resume glob `lojix-boot-once-*`.

### Concrete S4a disconnect test (observe on the VM)

1. During a BootOnce deploy, while activation is running, drop the daemon->VM
   ssh (e.g. kill the daemon's `ssh`/`nix` child to the VM, or blip the VM's
   network briefly).
2. On the VM, confirm the transient unit completed independently:
   `ssh <vm> 'systemctl status "lojix-boot-once-*"'` (while running) and
   `ssh <vm> "journalctl -u 'lojix-boot-once-*'"` — expect the boot-once
   script's final line `boot-once: oneshot=<NEW> persistent-default=<OLD>`
   (`schema_runtime.rs:2452`) and the unit reaching `dead`/auto-reaped
   (`--collect`). `--collect` means the finished unit may already be reaped;
   the journal entries (matched by glob) are the durable evidence.

## Resources — Prometheus has ample headroom

Read-only `ssh prometheus.goldragon.criome` (2026-06-13):
- `nproc` = **32**; `free -h` = **124Gi total, 121Gi available** (3.0Gi used).
- `nixos-version` = `26.05.20260422.0726a0e (Yarara)`;
  `systemctl is-system-running` = `running`.
- `/dev/kvm` = `crw-rw-rw- root kvm 10,232` — KVM present (matches
  `reports/cloud-designer/43-routed-microvm-standup/2-host-state.md:36-39`).

Bounds: a NixOS VM at 2-4 GiB RAM + the toplevel-closure build trivially fit in
121Gi available / 32c. The real consumer is **disk**, not RAM: the VM disk
image (a few GiB qcow2) + the built toplevel closure + `nix copy`'d store paths
all land in `/nix/store` and the VM image file. Pick a temp location with room
(prefer `/tmp` or a scratch dir on a large filesystem); the only practical bound
to watch is store/scratch free space for the closure + image, not CPU/RAM.

## qemu / nix availability on Prometheus

- `command -v qemu-system-x86_64 virsh` -> **not on PATH** (confirms
  `43/2-host-state.md:48`). The VM must be run via nix, not a system qemu.
- `nix` = `/run/current-system/sw/bin/nix`, version **2.34.6** (present).
- Read-only `nix eval --raw nixpkgs#qemu.outPath` on Prometheus resolved to
  `/nix/store/7yf84vnnsnvdi7r8g2grfpafnq17mp8y-qemu-10.2.2` — qemu is
  build/runnable via nix without touching the host system config. (A
  pre-existing flake-registry warning is benign and unrelated.)

## Safety / rollback — Prometheus system untouched

- **The VM is throwaway.** Reset = kill the qemu process and delete the disk
  image file; nothing persists. The deployed generation lives only inside the
  VM's `/nix` + bootloader, discarded with the image.
- **BootOnce inside the VM self-heals.** Even mid-VM, a broken generation
  reverts on the next reboot (reboot 1 = NEW one-shot, reboot 2 = persistent
  OLD), `schema_runtime.rs:2435-2453` — but since the VM is disposable, the real
  reset is deleting the image.
- **Prometheus's own config is never mutated.** The runbook runs qemu via `nix`
  (no host package install), the lojix daemon as an unprivileged user process,
  and issues NO `nixos-rebuild` / `nix copy` / `switch-to-configuration` against
  Prometheus itself. The `nix copy` target is `ssh-ng://<vm>`, never the host.
  Prometheus is the LargeAiRouter (`43/2-host-state.md:18`); no networking or
  system change touches it.
- **The lojix daemon + state dir are throwaway.** `lojix-write-configuration`
  takes the ordinary-socket path, owner-socket path, **`state_directory_path`**,
  and modes as a NOTA `ConfigurationWriteRequest`
  (`src/bin/lojix-write-configuration.rs:27-35,90-104`); sockets default to
  `/run/lojix/{ordinary,owner}.sock` but are env-overridable
  (`LOJIX_ORDINARY_SOCKET` / `LOJIX_OWNER_SOCKET`, `src/client.rs:22-25,36-40`).
  Point all of socket paths + `state_directory_path` at a temp dir (e.g.
  `/tmp/lojix-e2e/...`); the daemon's durable SEMA store lives there and is
  deleted on teardown. On restart the daemon self-resumes from that persisted
  state (`ARCHITECTURE.md:127-128`; `reconcile_persisted_jobs`
  `daemon.rs:548-569`).

## Success verification (the deploy actually landed in the VM)

1. **Inside the VM** (ssh in): `nixos-version`, `readlink /run/current-system`,
   `systemctl is-system-running` — the running/booted generation is the
   deployed closure. For BootOnce, the deployed generation is the one-shot
   default; reboot the VM once, then re-check `readlink /run/current-system`
   to confirm it booted the NEW generation.
2. **Event log** (ordinary socket): `lojix "(ReadEventLog (EventLogRange
   <from> <until>))"` shows a `DeploymentPhaseEvent` reaching **`Activated`**
   for the `DeploymentIdentifier` (`signal-lojix/schema/lib.schema:90-99`).
3. **Live-set / generation query**: `lojix "(Query (ByNode <selector>))"` ->
   `GenerationListing` with the generation in its slot
   (`BootPending` for BootOnce, `signal-lojix/schema/lib.schema:57,60-70`;
   `schema_runtime.rs:1802`). Optionally `meta-lojix "(Pin ...)"` then re-query
   to confirm the pin moves it to the `Pinned` slot.
4. **BootOnce transient-unit journal** on the VM (also the S4a evidence):
   `ssh <vm> "journalctl -u 'lojix-boot-once-*'"` shows the `boot-once:
   oneshot=... persistent-default=...` completion line.

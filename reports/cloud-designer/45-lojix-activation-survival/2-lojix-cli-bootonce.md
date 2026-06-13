# 45/2 — lojix-cli BootOnce parity: the exact production activation to port

cloud-designer recon sub-agent, 2026-06-13. READ-ONLY; nothing mutated, no
live deploy. Grounds the S4 work: make the lojix daemon copy+activate a real
closure (today reject-guarded/stubbed) and survive an SSH disconnect (Spirit
`up9q`). Every claim is `file:line` from the jj-colocated checkouts under
`/git/github.com/LiGoldragon`. Spirit gate: task-only recon → no capture.

Repos read:
- `lojix-cli` — production orchestrator (the activation source of truth).
- `lojix` — the new daemon that must replicate it (current gap quoted below).
- `CriomOS` — confirmed deploy entry point is lojix-cli, not CriomOS itself.

## Where the production activation lives

All in `lojix-cli/src/activate.rs` (`SystemActivation` / `HomeActivation`),
`copy.rs` (`ClosureCopy`), `host.rs` (`SshTarget`), with the action enum in
`build.rs` and the gating in `deploy.rs::finish_deploy`. CriomOS is only the
blueprint — its `docs/GUIDELINES.md:270-272` names
`lojix-cli '(Deploy … (Action switch))'` / `--action boot` as the entry point;
there is no activation logic on the CriomOS side.

## The action enum (`build.rs:10-36`)

`SystemAction = Eval | Build | Boot | Switch | Test | BootOnce`.
`produces_closure()` = all but `Eval` (`build.rs:26-28`); `activates()` =
`Boot | Switch | Test | BootOnce` (`build.rs:30-35`). `HomeMode = Build |
Profile | Activate`, `activates()` = `Profile | Activate` (`build.rs:39-49`).
`finish_deploy` runs copy→activate only when `action.activates()` (System) or
mode ≠ Build (Home) (`deploy.rs:165-203`); `Eval`/`Build` stop at the closure.

## Per-action behavior (the parity bar)

- **Eval** — no closure, no copy, no activate (`deploy.rs:157-159`).
- **Build** — closure realized; pipeline stops, no copy/activate
  (`deploy.rs:181`).
- **Test** (`activate.rs:58-65`, run via `run_simple`) — `ssh` runs ONLY
  `{store}/bin/switch-to-configuration test`. No profile set, no bootloader
  touch (`requires_efi_reconcile()` false, `activate.rs:160-162`).
- **Boot / Switch** (`activate.rs:58-69`) — one ssh:
  `nix-env -p /nix/var/nix/profiles/system --set {store} && {store}/bin/switch-to-configuration <boot|switch>`,
  THEN an **EFI reconcile** (`requires_efi_reconcile()` true): ssh
  `readlink /nix/var/nix/profiles/system` → parse `system-N-link`
  (`SystemProfileLink`, `activate.rs:376-387`) → derive
  `nixos-generation-N.conf` → ssh `bootctl set-default <entry>` + ssh
  `bootctl set-oneshot ''` (`activate.rs:177-230`). Reason: s-t-c writes
  `loader.conf` default but not the EFI `LoaderEntryDefault` var, so a stale
  one-shot from a prior BootOnce could otherwise hijack the next boot
  (`activate.rs:149-159`).
- **BootOnce** (`activate.rs:128-147`, dispatched by `run_boot_once`
  `activate.rs:232-255`) — the disconnect-survival mechanism, below.

## The exact systemd-run transient-unit command (`activate.rs:135-147`)

```
ssh -o BatchMode=yes root@<node>.<cluster>.criome \
  'systemd-run --unit=<unit> --collect --wait --service-type=oneshot /bin/sh -c <script>'
```

`--unit=` is `lojix-boot-once-<secs:x>-<pid:x>` — time+pid so concurrent
deploys don't collide and the operator can grep the right journal unit after a
drop (`unit_name()`, `activate.rs:75-82`). The unit is owned by **PID 1**, so
an ssh blip that kills the ssh leaves the unit running to completion on the
target; ssh holds open only as a live stdout/stderr feedback channel and
`--wait` returns the unit's exit code (`activate.rs:16-28`). `--collect` lets
the failed/finished transient unit be garbage-collected rather than lingering.
There is **no `--pipe`/`--pty`** — stdio inherits the ssh channel directly
(`run_boot_once` uses `inherit_stdio`, `activate.rs:240-243`). On any ssh error
the deployer is told to re-attach: `ssh <target> journalctl -u <unit>.service`
(`activate.rs:236-251`).

## The boot-once entry-staging script (`boot_once_script()`, `activate.rs:92-126`)

Runs inside the transient unit on the target. Seeds `PATH` explicitly
(`/run/current-system/sw/bin:/run/wrappers/bin:$PATH`) because NixOS transient
units get a minimal PATH (`activate.rs:110`). Then:

1. `CLOSURE='{store}'`
2. `OLD=$(bootctl status | awk -F': *' '/Current Entry:/ {print $2}')` then
   `[ -n "$OLD" ]` — OLD = the **running** generation's entry (the EFI
   `LoaderEntrySelected`/Current Entry, NOT `loader.conf`'s `default`, which
   can be a stale "next intended boot") (`activate.rs:84-91,113-114`).
3. `nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"`
4. `"$CLOSURE/bin/switch-to-configuration" boot`
5. `SYSTEM_LINK=$(readlink /nix/var/nix/profiles/system)`, sed
   `system-([0-9]+)-link` → `GENERATION`, `NEW="nixos-generation-$GENERATION.conf"`
   — NEW derived from the **system profile symlink target** (canonical
   latest-installed generation), not from `bootctl` Default Entry which can be
   stale or a no-op on same-closure redeploy (`activate.rs:101-108,117-119`).
6. Asserts `[ -f /boot/loader/entries/$NEW ]` and `[ "$NEW" != "$OLD" ]`.
7. `bootctl set-default "$OLD"` + `bootctl set-oneshot "$NEW"`.

Net: **reboot 1 lands NEW; reboot 2+ auto-returns to OLD** — headless-safe
rollback, because the persistent default never leaves the known-good running
generation.

NOTE — drift from report 39 §"Activation mechanics": report 39 said BootOnce
derives NEW from `bootctl status` Default Entry; the current source derives NEW
from the `readlink` of the system profile (`activate.rs:117-119`) and reads OLD
from Current Entry. Trust the source.

## The copy command (`copy.rs:35-51`, addressing `host.rs:49-55`)

```
nix copy --substitute-on-destination [--from ssh-ng://<builder>] --to ssh-ng://root@<domain> <store_path>
```

`--substitute-on-destination` is **always** passed: the target pulls
**signed** paths from the cluster Nix cache (substituters sign over HTTP),
falling back to direct transfer only on a miss — raw daemon-to-daemon transfer
of locally-built paths arrives unsigned and is rejected under `require-sigs`
(`copy.rs:19-25`). Three cases (`copy.rs:35-67`): source Dispatcher → `--to`
only; source Builder == target → **skip** (already present); source Builder ≠
target → `--from ssh-ng://<builder> --to ssh-ng://<target>` streamed through
the dispatcher's nix-daemon. `ssh_uri()` is always
`ssh-ng://root@<node>.<cluster>.criome` from the projected horizon's
`criome_domain_name` — never a bare node name (`host.rs:20-21,49-51`).

## Home activation (`activate.rs:266-353`)

`nix-env -p $HOME/.local/state/nix/profiles/home-manager --set <store>` (as the
target user, `remote_profile_invocation` `activate.rs:282-288`), then for
`Activate` run `<store>/activate`. **Local fast-path**: skips ssh entirely when
the dispatcher already is the requested USER on the target node
(`is_local_context`: USER/LOGNAME match + `hostname -s` == node,
`activate.rs:331-352`).

## Secrets in the activation path

None at activate-time. Secrets are an **eval-time flake input** only:
`artifact.rs::SecretsDir` copies 3 hardcoded `.sops` files
(`router-wifi-sae-passwords`, `router-backup-wifi-password`,
`local-llm-api-token`) into a content-addressed flake, existence-gated on
`<proposal-dir>/secrets/router-wifi-sae-passwords.sops`
(`artifact.rs:155-189`), injected via `--override-input secrets`
(`build.rs:323-329`). The copy/activate path moves only the already-built
closure; no secret materialization happens there.

## Host / target identity + reachability resolution

The deploy target is ALWAYS `horizon.node` (the viewpoint node); there is no
`--target` flag (`deploy.rs:104-106`). `SshTarget::from_node` builds
`root@<criome_domain_name>` (`host.rs:20-21,35-40`). Remote command shape is
fixed `ssh -o BatchMode=yes <user>@<domain> <command>`
(`host.rs:57-64`) — BatchMode means no interactive prompt; reachability is
whatever the key/agent already provides (no probing, no retries, no timeout —
`deploy.rs:86-88`). Builder identity resolves separately
(`resolve_builder_target`, `deploy.rs:49-64`): self→target ssh, sibling→ must
have `is_remote_nix_builder=true`.

## What the lojix daemon must replicate (current gap — all reject-guarded/stubbed)

- **Reject guard** (`lojix/src/schema_runtime.rs:559-575`): System deploys
  accept only `Eval | Build`; Home only `Build`; everything activating returns
  `DeployRejectionReason::UnsupportedDeployAction`. Comment at
  `schema_runtime.rs:555-558`: "Activating actions remain rejected because
  copy/activate is not yet target-safe; accepting them would write false
  live-set state." This is the guard to remove once parity lands.
- **Broken copy stub** (`schema_runtime.rs:1886-1896`):
  `nix copy --to ssh-ng://<node_name> <closure>` — bare `node_name`, NO
  `--substitute-on-destination`, no `--from` builder case, no `root@<domain>`.
  Must become `copy.rs`'s signed-path, three-case copy with the
  `criome_domain_name` SshTarget.
- **Broken activate stub** (`schema_runtime.rs:1898-1908`):
  `ssh <node_name> 'nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"'`
  — `$CLOSURE` is an **unexpanded shell var** (never set), bare `node_name`,
  NO `switch-to-configuration`, no per-action branch, no BootOnce, no EFI
  reconcile. Must become the full `SystemActivation` machinery.
- **State-machine scaffold already exists** to hang it on
  (`schema_runtime.rs:128-145` Copying→Activate→Activated→RecordGenerationActivated;
  `activate_generation_command` `schema_runtime.rs:357-375`), so the daemon
  records phases — it just runs the wrong/stubbed commands.

Replication checklist for S4:
1. Port `SshTarget` addressing (`root@<criome_domain_name>`, never bare node).
2. Port `ClosureCopy` (always `--substitute-on-destination`; three-case
   from/to; skip when builder==target).
3. Port per-action System activation: Test (s-t-c test only), Boot/Switch
   (profile set + s-t-c + EFI reconcile via readlink→set-default→clear-oneshot),
   BootOnce (the `systemd-run --unit --collect --wait --service-type=oneshot`
   PID-1 transient unit + Current-Entry/readlink rollback script).
4. Port Home Profile/Activate incl. the local fast-path.
5. Drop the reject guard for activating actions once the above are target-safe.
6. The **disconnect-survival** primitive (Spirit `up9q`) is specifically the
   BootOnce `systemd-run --collect --wait` transient unit + the
   journalctl re-attach affordance — the daemon currently has none of it.

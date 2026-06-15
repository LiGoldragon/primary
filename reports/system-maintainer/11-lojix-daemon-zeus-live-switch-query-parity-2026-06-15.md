# Lojix daemon Zeús live-switch and query parity closeout — 2026-06-15

## Result

Zeús live `Switch` through the installed `meta-lojix` daemon reached terminal success after three fixes landed and were deployed on Ouranos:

1. `goldragon` proposal NOTA was canonicalized so the daemon-pinned Horizon decoder no longer rejects bare-eligible bracket strings.
2. `lojix` 0.3.4 changed closure copy to use the dispatcher-to-target Nix copy path with `--substitute-on-destination`, avoiding unsupported direct `root@prometheus` source SSH.
3. `CriomOS` now starts `lojix-daemon.service` with the operator SSH agent socket, so daemon-owned target copy can authenticate to Zeús like the interactive operator shell.

After those fixes, the installed daemon submitted Zeús `FullOs Switch`, copied the closure, activated Zeús, recorded a current live generation, and ordinary `lojix` query returned that current generation. The original empty-query symptom is fixed for a real terminal activation.

## Evidence

Commands were run from Ouranos against the installed daemon and Zeús root SSH. Store paths are intentionally redacted.

- Installed daemon after the local production switch: `lojix-daemon.service` active, running `lojix` 0.3.4, with `SSH_AUTH_SOCK=/run/user/1001/gnupg/S.gpg-agent.ssh` in its service environment.
- Zeús Switch submission via installed `meta-lojix` returned `(Deployed (1 (32 32)))` as the admission reply.
- During the deploy, ordinary query initially remained empty while the detached pipeline was still building/copying/activating.
- Zeús target state then moved: `/nix/var/nix/profiles/system` and `/run/current-system` both resolved to the same new Zeús system generation, with mtimes around `2026-06-15 11:21:39 +0200`.
- Final ordinary query returned:

```text
(Queried ([(1 1 goldragon zeus FullOs Switch Current [redacted-zeus-system-generation])]
  (43 43))
```

- Daemon journal terminal output after the same retry reported terminal `Deployed(...)` rather than `DeployRejected(...)`.
- `systemctl is-system-running` on Zeús returned `running` after activation.

## Fixes landed

- `goldragon` main:
  - `5486c2efbaef` — canonicalize bare optional strings.
  - `71a466626b5b` — canonicalize remaining bare cluster strings.
- `lojix` main:
  - `9d4eae3bdbb2` — bump to 0.3.4 for target-only closure copy.
- `CriomOS` main:
  - `fc17f340517d` — pin lojix 0.3.4.
  - `c208535ee872` — initial service SSH-agent environment attempt; this expanded to root in a system service and was superseded.
  - `a9089ca8c0f5` — derive the daemon SSH agent path from the operator UID and set `li`'s UID default to 1001 on PersonaDevelopment nodes.

## Validation

- `goldragon/datom.nota` projected with `horizon-cli --cluster goldragon --node zeus` after canonicalization.
- Focused `lojix` unit tests passed:
  - `copy_from_dispatcher_uses_to_only_with_substitute`
  - `copy_remote_builder_still_uses_dispatcher_to_target_copy`
  - `copy_builder_equals_target_still_runs_idempotent_target_copy`
  - `remote_build_uses_daemon_machine_file_and_disables_local_fallback`
- `cargo fmt --check` passed in `lojix`.
- `nix flake check --no-build` passed in `lojix` for packages, checks, formatter, and devShell outputs.
- Installed smoke after the final Ouranos switch:
  - binaries present: `lojix-daemon`, `lojix`, `meta-lojix`, `lojix-write-configuration`.
  - `/run/lojix/ordinary.sock`: `0660 li:users`.
  - `/run/lojix/owner.sock`: `0600 li:users`.
  - `/run/lojix/startup.rkyv`: `0600 li:users`.
  - `/var/lib/lojix`: `0750 li:users`.
  - `lojix-daemon.service`: active.

## Remaining notes

- `meta-lojix` still prints `Deployed` at admission time because the contract names the accepted deploy handle `Deployed(AcceptedDeploy)`. This is survivable only because the daemon now logs terminal pipeline output and ordinary query exposes current state after terminal activation. A future contract split between admission and terminal success is still a design cleanup.
- Zeús Home Manager generation symlinks did not move in this `FullOs` system activation; the live-set query records a `FullOs` generation and the system profile switched. If Home activation parity is required as a separate acceptance criterion, track it separately rather than reopening the empty-query bug.
- The daemon service currently depends on the operator user's GPG SSH agent socket being present. This matches the installed operator workstation use case and fixes the live blocker, but a future key-management design should make daemon deploy credentials first-class rather than ambient user-agent state.

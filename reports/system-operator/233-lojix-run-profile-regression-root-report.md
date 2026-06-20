# Lojix-run profile regression root report

## Incident

On 2026-06-20, the active Home profile regressed from the fixed
`lojix-run-0.3.10` wrapper back to `lojix-run-0.1.0`. The stale wrapper embedded
`lojix-cli-0.1.0`, so a profile activation could undo the earlier migration to
the current `lojix` daemon/toolchain.

## Root cause

The earlier fix landed on `CriomOS-home/main`, but a later activation used the
temporary flake ref:

`github:LiGoldragon/CriomOS-home/criomos-home-spirit-bypass`

That branch still pointed at commit `51a19beb`, whose lock file consumed
`lojix-cli` at `41c2ec8f` and had no `lojix` input. The deployment request at
`~/.local/state/lojix-runs/20260620132833-deploy-ouranos/request.nota` activated
that bypass ref, so Home Manager installed the older wrapper again.

This was not a Nix profile mystery. It was a flake-ref selection problem:
`main` was fixed; the exact branch used by the later deployment was not.

## Fix applied

`CriomOS-home` now has both `main` and `criomos-home-spirit-bypass` at commit
`dee7d730` (`home: keep spirit bypass on fixed lojix-run line`).

The current branch metadata resolves as:

- `CriomOS-home/criomos-home-spirit-bypass`: `dee7d730`
- `lojix`: `aaea314c`
- `lojix-cli`: absent
- `spirit`: `7fc267c`

The active profile was reactivated through the corrected bypass ref. The active
`/home/li/.nix-profile/bin/lojix-run` now resolves to `lojix-run-0.3.10` and
embeds `lojix-0.3.10/bin/meta-lojix`.

## Verification

- Remote `CriomOS-home/criomos-home-spirit-bypass#checks.x86_64-linux.lojix-run`
  builds successfully.
- The corrective activation run directory is
  `~/.local/state/lojix-runs/20260620175154-deploy-ouranos`; its rewritten
  request is `Deploy (Home ...)`, and the daemon returned `Deployed`.
- A follow-up active-profile `Build` probe using the same bypass ref also
  returned `Deployed` from run directory
  `~/.local/state/lojix-runs/20260620175258-deploy-ouranos`.
- `systemctl --failed` and `systemctl --user --failed` both report zero failed
  units after activation.
- `spirit Version` reports `0.15.0`.
- `lojix-daemon.service` is active and running `lojix-0.3.10`.

## Residue findings

### Unmanaged Spirit sandbox daemon

During investigation, PID `698978` was running
`spirit-daemon /tmp/spirit-sb2/config.rkyv`. Its sockets were
`/tmp/spirit-sb2/spirit.sock` and `/tmp/spirit-sb2/meta.sock`, and its store
file was `/tmp/spirit-sb2/spirit.sema`.

Production Spirit is a separate PID and uses
`~/.local/state/spirit/spirit.sock`, `~/.local/state/spirit/meta-spirit.sock`,
and `~/.local/state/spirit/spirit.sema`.

Final state: no `/tmp/spirit-sb2` daemon is running and no `/tmp/spirit-sb2`
socket is listening. The `/tmp/spirit-sb2` directory and socket pathnames remain
on disk.

Risk: low for production interference, because the production socket and store
paths are separate and the sandbox daemon is no longer running. Low operational
residue remains because stale socket pathnames can confuse later audits.

Recommended cleanup: after confirming no one still needs the sandbox artefacts,
archive or remove `/tmp/spirit-sb2`.

### Ghostty transient scope

`app-ghostty-surface-transient-7999.scope` previously showed
`Result=oom-kill`, with a memory peak of 19.2G and swap peak of 20.8G. After the
latest activation, the failed-unit lists are clear.

Risk: low as a current system-health issue. It is evidence of memory pressure
earlier today, not an active failed unit now.

Recommended cleanup: none required unless it recurs. If it recurs, inspect the
workload launched inside that transient Ghostty scope rather than treating it as
a Home profile failure.

### Lojix-daemon child process leak

After accepted deploy receipts, `lojix-daemon` still had two child `nix eval`
processes evaluating the corrected bypass ref. They were blocked under the
daemon after the client had already received success. A later final check showed
that both evaluator children had drained.

Risk: low as current residue, because no evaluator child remained at final
check. Medium as a possible `lojix` lifecycle bug if it recurs under repeated
deploy/build probes.

Recommended cleanup: none for the final state. If the pattern recurs, inspect
`lojix` child lifecycle and completion semantics. `lojix` is currently locked by
`system-designer`, so I did not patch it here.

## Prevention

Production Home activations are only as current as the flake ref they name. A
temporary branch used for a production activation must be advanced to the same
safety line as `main` before reuse, or the activation should name `main`.

The concrete guard for this incident is now in place: the reused bypass ref no
longer contains `lojix-cli`.

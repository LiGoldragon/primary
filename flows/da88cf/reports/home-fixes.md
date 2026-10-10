# Home declared fixes: codex-next handoff, Lojix socket, flake registry

Subflow of da88cf, 2026-09-25, on ouranos. **No source was committed.**
Two of the three fixes need files held by sibling da88cf integration locks,
which refused this subflow's lock. The third needs no change: its declaration
is already correct. No bookmark was pushed and no lock is held. Nothing was
deployed, activated, restarted, stopped or unlinked.

## Lock outcome

- `Lock.{ HomeDeclaredFixes da88cf [ …/CriomOS-home/modules/home/profiles/min/codex-next.nix ] … }`
  → `LockRejected.PathOverlap`. The holder is **6846 MainIntegrationCriomOSHome da88cf**
  («Integrate deploy-path branches onto main»), which holds codex-next.nix, flake.nix, flake.lock and 22 other paths.
- The same request with `…/CriomOS/modules/nixos/nix/client.nix` → `LockRejected.PathOverlap`.
  The holder is **6834 MainIntegrationCriomOS da88cf**, which holds the whole `/git/github.com/LiGoldragon/CriomOS`.
- The canonical CriomOS-home checkout's `@` is that integration in progress:
  `xxpktyxk` «Integrate the Prometheus Home line (Herdr, Message, Codex next, Claude bypass repairs) with Flow 0.12.2 and messenger-clj main».
  It is a merge of main `5f14f9da` with `field-astra-5f38bc-flow-pins` `04446e78` and is still conflicted.
  So this subflow worked in its own jj workspace, which is now forgotten and deleted.

## Fix 1: codex-remote-control-next

- **File:** `modules/home/profiles/min/codex-next.nix`. **It does not exist on CriomOS-home main (`5f14f9da`).**
  It exists only on `field-astra-5f38bc-flow-pins` (`04446e78`), which is being merged by lock 6846.
  The fragment chain in f5a74e (`~/.config/systemd/user/…` → `…home-manager-files` → `qdc1vmw9…-codex-remote-control-next.service`) leads to this module.
  The deployed system's flake registry independently names `criomos-home` rev `04446e78d465…`, which confirms that the active generation was built from that branch.
- **Before** (branch 04446e78, `systemd.user.services.codex-remote-control-next.Unit`): `Description` only. `Service.Restart = "on-failure"`, `RestartSec = 2s`.
- **After** (proposed, not committed; this is f5a74e's shape):
  ```nix
  Unit = {
    Description = "Codex Remote Control next server";
    Conflicts = [ "codex-remote-control-next-recovery.service" ];
    After = [ "codex-remote-control-next-recovery.service" ];
  };
  ```
  Also add `StartLimitIntervalSec`/`StartLimitBurst` in `Unit` (for example 60 s / 5) so that a socket still held elsewhere ends in a clean `failed` state instead of 42,845 restarts.
  f5a74e's evidence supports Conflicts. It shows the holder is a live listener behind a symlinked endpoint, not a stale path, so ExecStartPre unlinking and socket activation are both wrong here. StartLimit is the bounded failure for any other holder.
- **Evidence:** `flows/f5a74e/reports/codex-next-unit.md`, which gives W grades for the restart count, the journal "control socket is already in use", and the transient PID 1998991 holding the listener. Inventory D1 is the other source.
- **Check:** not run, because no edit was made.
- **Activation:** the recovery unit had `KillMode=control-group` and 863 tasks. Activating a generation with `Conflicts=` and then starting the declared unit stops the transient and every attached session.
  Detect a quiet window without contacting the app server:
  - `systemctl --user show codex-remote-control-next-recovery -p TasksCurrent` is at an agreed baseline;
  - `lsof -a -p <MainPID> -U` shows no connected peers beyond the listener;
  - no `codex-next` sessions are live (for example, `pgrep -f 'CODEX_HOME=.*codex-next'` and no recent writes under `~/.codex-next/sessions`);
  - the owners of the live sessions confirm.

  Then activate, do one `systemctl --user start codex-remote-control-next`, and witness: the declared unit is active, the transient is inactive, the endpoint resolves to the declared listener, and `NRestarts` stays stable. Rollback: the previous HM generation.

## Fix 2: Lojix owner socket (no change needed)

- **Declaration (CriomOS main `d193bafc`, `modules/nixos/lojix.nix`):** `ownerSocketPath` is readOnly with default `"${cfg.runtimeDirectoryPath}/meta.sock"` (line 109, since `c4c830c1` 2026-09-11). `environment.variables.LOJIX_OWNER_SOCKET = cfg.ownerSocketPath` (line 209) reads that same option, so the value is not retyped anywhere.
  `checks/lojix-ownership` asserts `/run/lojix/meta.sock`. CriomOS-home declares no LOJIX variable, and its `system-projection-boundary` check forbids one.
- **The deployed system is already correct:** `/etc/set-environment` (→ `15vf2nm7…-set-environment`, linked 2026-09-24 18:43) exports `LOJIX_OWNER_SOCKET="/run/lojix/meta.sock"`. `/run/lojix/meta.sock` exists.
- **The live `owner.sock` is stale runtime state:** `systemctl --user show-environment` holds `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock`. The user systemd manager has been running since **2026-09-10 13:30**, before the 09-11 change, and every process it spawns (Herdr, the flows) inherits the value.
- **Activation:** there is no source fix. A fresh login session clears it. Without a relogin, `systemctl --user set-environment LOJIX_OWNER_SOCKET=/run/lojix/meta.sock` fixes new children (this is a live change, left to an authorized operator), and running processes keep the old value until they restart.

## Fix 3: flake registry

- **File:** CriomOS `modules/nixos/nix/client.nix`, `mkFlakeEntry` (lines 34–47). It is held by lock 6834.
- **Cause:** `owner`/`repo` are read from `input.sourceInfo`, but a locked github input's `sourceInfo` carries only `outPath`, `rev`, `narHash` and `lastModified`. `filterAttrs` drops the nulls.
  The deployed `2573ls7j…-criomos-flake-registry.json` therefore has entries `{type="github"; rev=…}` with no owner or repo, and every `nix` call warns `input attribute 'owner' is missing`.
- **Before:**
  ```nix
  to = filterAttrs (_: v: v != null && v != "") {
    type = input.sourceInfo.type or "github";
    owner = input.sourceInfo.owner or null;
    repo = input.sourceInfo.repo or null;
    rev = input.sourceInfo.rev or null;
  };
  ```
- **After** (proposed, not committed). This takes owner and repo from the flake's own lock node. `rev` stays taken from `sourceInfo`, so a deploy-time `--override-input` still registers what was actually built:
  ```nix
  flakeLock = builtins.fromJSON (builtins.readFile ../../../flake.lock);
  lockedInput = name: flakeLock.nodes.${flakeLock.nodes.${flakeLock.root}.inputs.${name}}.locked;
  mkFlakeEntry = name: input: {
    from = { id = name; type = "indirect"; };
    to = filterAttrs (_: v: v != null && v != "") {
      inherit (lockedInput name) type owner repo;
      rev = input.sourceInfo.rev or null;
    };
  };
  ```
- **Check (shape only):** `registry-proposal.nix` in the scratchpad computes the entries from CriomOS main's `flake.lock` with the same `lockedInput`.
  `nix --option flake-registry <proposal.json> registry list` parses cleanly:
  `global flake:nixpkgs github:LiGoldragon/nixpkgs/0e251e24…`, `home-manager github:nix-community/home-manager/c554d344…`, `brightness-ctl github:LiGoldragon/brightness-ctl/5274f993…`, `criomos-home github:LiGoldragon/CriomOS-home/478b4ea0…`.
  No CriomOS system evaluation was run, because no edit was made.
- **User-level pin:** `~/.config/nix/registry.json` now reads `{"flakes": null, "version": 2}`, so the `horizon → path:/tmp/flake-false-test/payload-stub` pin from inventory G2 is already gone. That removal belongs to another subflow; this subflow did not touch the file.
- **Activation:** an ordinary CriomOS system switch. Witness it with `nix registry list` printing no warning.

## Sources

- `flows/f5a74e/reports/codex-next-unit.md`; `flows/da88cf/reports/inventory-system.md` (D1, G2, G3, J).
- `orchestrate 'Observe.Locks'` and the two `LockRejected.PathOverlap` replies above.
- `jj log`/`jj diff --stat main..field-astra-5f38bc-flow-pins` in `/git/github.com/LiGoldragon/CriomOS-home` (origin `ssh://git@github.com/LiGoldragon/CriomOS-home`).
- CriomOS main `d193bafc`: `modules/nixos/lojix.nix`, `modules/nixos/nix/client.nix`, `flake.lock`, `checks/lojix-ownership`.
- Live, read-only: `/etc/set-environment`, `systemctl --user show-environment`, the user-manager start time, `ls /run/lojix`, `/nix/store/2573ls7j…-criomos-flake-registry.json`, `nix registry list`, `~/.config/nix/registry.json`.

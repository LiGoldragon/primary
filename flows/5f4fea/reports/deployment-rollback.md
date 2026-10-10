# Production rollback — source witness and proposal

Status: proposal only. Nothing installed, regenerated, or deployed. Source evidence delegated to persona_read, 2026-09-15. Newer explicit items 11–13 and 17 authorize sandbox prototypes; older provisional records do not revoke that authorization.

## Current authored skills (whole)

Source: /git/github.com/LiGoldragon/Curriculum/skills/breaking-upgrades.md

```markdown
---
description: A breaking change must be deployed.
dependencies: [documentation-placement]
---

Document how to deploy each breaking change in the repository's `UPGRADES.md`.
Land the documentation with the breaking change.
If deployment fails or partially fails, correct the documentation before continuing.
```

Source: /git/github.com/LiGoldragon/Curriculum/skills/operating-system.md

```markdown
---
description: The operating system itself must change.
dependencies: [lojix]
---

This is a declarative operating system. Change it by editing its declarative source, named in the AGENTS.md of the workspace you are in, then rebuilding. A change made directly to running system state is lost at the next rebuild.

Before debugging installed software, update it to its latest release.

Use `lojix` and `meta-lojix` for deployment and observation; their exact typed contract and terminal verification are defined by the `lojix` instructions.

Require explicit psyche approval before a reboot or emergency runtime mutation.
```

## Existing machinery

Inspected local revisions: Lojix 0bb3d66c96ff53da82a7bf0e077545ad399d44fb; CriomOS 2985c813cae8f077845873149252f7dbc0575e8d; CriomOS-home caffe9a17cc5830d64f838f7d5cf74d9b2b5bf3a. These are local source revisions, not a claim about active host generations.

Lojix /git/github.com/LiGoldragon/lojix/src/adapters.rs:231:
```rust
shared_unit_enum!(HostDeployAction {
    TestActivation,
    ScheduleBootOnce,
    Realize,
    SetBootProfile,
    Evaluate,
    ActivateNow
});
```
There is no Rollback action in this enum. Rollback appears as GenerationSlot state. The earlier helper claim of a typed Rollback action was corrected.

Lojix src/schema_runtime.rs:5503–5512, selected literal lines:
```sh
OLD=$(bootctl status | awk -F': *' '/Current Entry:/ {print $2}')
nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"
"$CLOSURE/bin/switch-to-configuration" boot
NEW=$(awk '$1 == "default" {print $2; exit}' /boot/loader/loader.conf)
bootctl set-default "$OLD"
bootctl set-oneshot "$NEW"
```
This preserves the old default and schedules one candidate boot; it is not a cancelable rollback countdown. At src/schema_runtime.rs:5517–5519:
```rust
/// BootOnce ssh call: wraps the boot-once script in `systemd-run --wait`.
/// ssh holds open as a live stdout/stderr channel; if it dies the unit runs
/// to completion regardless (`detached_invocation()`).
```
No countdown timer or completed external-watch cancellation operation was found in the inspected source. This is a bounded source-search result, not proof that every host lacks unrelated recovery machinery. No live host generation or timer inventory was collected.

Lojix src/runtime_model.rs:232–252 models DeploymentLifecycle through Completed/Rejected/Failed and failure stages including Activate and Daemon. tests/failure_evidence.rs:169–177 asserts ActivationFailed and stage Activate; lines 187–229 retain ssh command/exit evidence while filtering planted credential-like stderr. Failure recording does not itself prove automatic recovery.

CriomOS modules/nixos/lojix.nix:216–220:
```nix
systemd.services.lojix = {
  description = "Lojix Nexus";
  wantedBy = [ "multi-user.target" ];
  wants = [ "network-online.target" ];
  after = [ "network-online.target" ];
```
The manual reset-store service at lines 246–254 has no wantedBy and conflicts with lojix.service; it is store reset, not OS rollback.

CriomOS modules/nixos/normalize.nix:184–189:
```nix
services = {
  openssh = {
    enable = true;
    # Keys only — no password auth, ever.
    settings.PasswordAuthentication = false;
    ports = [ 22 ];
```
CriomOS modules/nixos/network/tailscale.nix:11–15:
```nix
config = lib.mkIf (nodeServices.has (node.services or [ ]) "TailnetClient") {
  # Phase 1 scaffolding only: enrollment remains manual.
  services.tailscale = {
    enable = true;
    openFirewall = true;
```
These declarations do not establish that the currently reachable session uses Tailscale, or that an external host can cancel a deployment.

## Proposed skill placement

Put the production countdown rule in breaking-upgrades: it applies to production changes beyond OS rebuilds. Keep the existing OS declarative/Lojix and reboot rules. A separate Curriculum proposal branch and exact diff remain required; no generated skill tree is to change before wording approval.

Proposed wording: Before deploying a breaking change to production, arm an automatic countdown rollback to the last known working stack. Cancel the countdown only after a witness confirms that both network connectivity and remote access work on the new stack, from the host itself or a watch flow on another host. Do not deploy a change that can lose remote access without that timeout. Record the rollback target, timeout, cancellation authority, and witness in UPGRADES.md.

The witness must identify the candidate stack so that a response from the old stack cannot cancel recovery. Cancellation must use a defined authority; this proposal does not invent an existing Lojix cancel operation.

## Pipeline and candidates

POC: prove the typed behavior with fixtures. Sandbox: exercise integration and failure/recovery using isolated resources. Production: after the living rules on the candidate, use a recorded rollback target and armed timeout where breaking, then retain the new stack only after the required network and remote-access witness.

| Candidate | Enough direction now | Remaining gate |
|---|---|---|
| Persona | Isolated three-crate Signal/Nexus launch/ledger compile-test draft, explicit item 13 | Architecture review, real adapters, recovery proof; no activation |
| Quota collector | Report-only tool and fixture Nix check, explicit item 11 | Passing checks and review; scheduler/hook not authorized |
| Assembler | Two output shapes, provenance and fixture comparison, explicit item 12 | Skill-interface ruling and deployment review; neither output launched |
| Fan-out | Transcript lookup and fixture transport prototype, explicit item 17 | Default endpoints and whole-response versus pointer ruling; no hook |
| Countdown rollback | Anatomy and authored skill proposal, explicit item 18 | Approved wording and implemented/tested recovery mechanism |

Vision anchors: flows/05c604/vision/deployment.md (countdown/pipeline), flows/05c604/vision/messages.md (fan-out), flows/05c604/vision/launch.md (one-call launch), flows/05c604/vision/quota.md (quota work). Prototype authorization is also carried by the explicit current peer work-item messages. None of these source witnesses establishes production readiness.

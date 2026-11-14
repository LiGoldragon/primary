# ACPI model fix: deployment pending

The model-only fix is committed and pushed as `52e55e913abcad018a63324cbc6092ea91c43764`, branch `fix/acpi-gpe6d-329917`, based on fetched origin/main `8549edbb689578887dfc8531e75579bfcb93790e`. The isolated worktree is `/home/li/worktrees/criomos-acpi-329917`; foreign shared-checkout changes were untouched.

Three added lines select `ThinkPadT14Gen5Intel` in the existing `boot.kernelParams` composition and add `acpi_mask_gpe=0x6D`. Nix parsing and `git diff --check` passed. Evaluation of the Lojix-materialized node's `boot.kernelParams` confirmed the parameter with the existing parameters.

Lojix accepted Evaluate deployment 234, then returned terminal `Failed.{ Eval EvaluationFailed ... }`. A separate assertion query against its materialized inputs established the precise blocker: `OpenCode testing requires inputs.secrets.sopsFiles.opencodeServerPassword`. The request used `NoSecrets`; no secrets were read. Supported secrets-input metadata/owner routing was requested from Mind core and Mind criomosHome.

No Realize, copy, activation, wake-control change, BIOS operation or reboot was performed. The intended activation is BaseHost SetBootProfile, leaving reboot to the living. Preflight root SSH confirmed the local target hostname and that GPE6D remained masked at 68,562,418.

Exact shared model-source lock: 25660. Git/worktree lock 25661 was released after publication. Completion remains a terminal successful Lojix deployment, not Evaluate admission or this source commit.

## Route B ruling and second source commit

Psyche selected a fix-only branch from the running generation's source, `NoSecrets`, then `SetBootProfile`; no full-main deployment. Query.ByGeneration 153 returned Current BaseHost, source `cbbbb2f9f15536f8710741ca6b7e2a2506bbaf31`, successful deployment 153, and a recorded closure matching the live system link. Git dates that source 2026-10-19; the system label's 20260813 is not proof of its source/build date.

The isolated branch `fix/acpi-gpe6d-live-329917` adds the same three lines on that recorded source: commit `8dd756205f0f0428fabb1538884ecc0bb946cd9b`, pushed. Main retention was also completed: `52e55e913abcad018a63324cbc6092ea91c43764` is now pushed to main.

Evaluate 235 (full-main revision with the existing encrypted-file directory) terminally succeeded but remains history only; no realization or activation followed. Route B Evaluate 236 (recorded-live source plus fix, current Goldragon proposal, NoSecrets) terminally failed evaluation. The exact failed assertion remains `OpenCode testing requires inputs.secrets.sopsFiles.opencodeServerPassword`.

Route B therefore needs the original generation's immutable Horizon/input provenance, or a further scope ruling. The ordinary Query.ByGeneration response exposes closure/source revision and deployment terminal, not original proposal path/hash, producer revision or generated-input references. No private Memory access or capability deletion was attempted. Git lock 25662 was released. No build, copy, activation or reboot occurred.

## Completed: authorized route A

Psyche ruled route A after determining the original generation input was unavailable. Deployment 237 used immutable main `52e55e913abcad018a63324cbc6092ea91c43764`, BaseHost, the supported existing encrypted-files directory passed directly to Lojix, and `SetBootProfile`. No secret contents reached this flow.

`Query.ByDeployment.{ 237 }` returned `Completed`, `Some.Succeeded`, generation 237 `BootPending`, database marker 5266. A read-only root check verified OS generation 195 is the bootloader default and its options include `acpi_mask_gpe=0x6D`. The old runtime generation 194 remains running. The GPE6D counter is still 68,562,418, masked. No reboot, BIOS operation or wake-control change was performed. Only the living reboots.

The exact 90-minute task was closed with Done to Mind core Secondary. Source lock 25660 and both Git reservations were released. Post-reboot counter verification remains for the living's reboot; it was not asserted as performed.

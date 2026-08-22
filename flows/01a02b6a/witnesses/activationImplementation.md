# Zeus activation implementation witness

Read-only inspection of `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
and Nixpkgs `switch-to-configuration-ng`. No request was submitted and no
target, daemon, deployment, or boot state was changed.

## Lojix action boundaries

The host action predicates and activation-effect mapping are in
`schema_runtime.rs:1113-1152` and `1550-1572`:

| Action | Closure / copy | Target command and durable slot |
| --- | --- | --- |
| `Evaluate` | evaluates a derivation only; no realized closure or copy | no target command; terminal success is evaluation evidence |
| `Realize` | evaluates and realizes/builds the closure; no copy | no target command; terminal success is build evidence |
| `TestActivation` | builds and copies candidate | `<closure>/bin/switch-to-configuration test`; slot `Recent` |
| `ActivateNow` | builds and copies candidate | target system profile `nix-env --set`, then `switch-to-configuration switch`; slot `Current` |
| `SetBootProfile` | builds and copies candidate | target system profile `nix-env --set`, then `switch-to-configuration boot`; slot `BootPending` |
| `ScheduleBootOnce` | builds and copies candidate | sets candidate profile and runs `boot`, restores old EFI default, sets candidate EFI one-shot; slot `BootPending` |

Pipeline continuation (`schema_runtime.rs:3118-3188, 3467-3515`) records
`Activating`, runs the target command, records `Activated`, and only then
commits durable `GenerationActivated`. A failed activation is terminal
`Failed` at the Activate stage (`schema_runtime.rs:3340-3380`), and does not
prove that the target was unchanged.

`TestActivation` is the only host action that exercises the candidate
activation before assigning the persistent system profile and boot default.
It is therefore the smallest meaningful pre-switch activation proof, but it
is not a dry run: Nix's `test` mode still executes the generated activation
script (`switch-to-configuration-ng/src/src/main.rs:1543-1560`), which may
modify `/etc`, accounts, systemd units, and runtime state. `Realize` is the
smallest target-mutation-free stage and is useful as a build proof; the next
deployment cannot carry its Lojix identity forward, although Nix may reuse
the realized store path/cache.

`SetBootProfile` is not a pre-switch proof. It persistently changes the system
profile and boot default while deliberately avoiding current-runtime
activation. `ScheduleBootOnce` changes the system profile and schedules a
candidate for the next reboot while restoring the old persistent default; it
does not itself activate or reboot (`schema_runtime.rs:5357-5376`).

## Target postconditions

For a successful activation request, require both a Lojix terminal `Succeeded`
and target observations appropriate to the action. The expected slot is
materialized by `schema_runtime.rs:4401-4429`; controller durability alone is
not target proof.

- `TestActivation`: candidate activation command exited successfully;
  system profile, `/run/current-system`, `/run/booted-system`, and bootloader
  default should remain at the pre-test generation. Inspect service/unit and
  activation-journal deltas because runtime changes can still occur.
- `ActivateNow`: system profile, current-system and booted-system links should
  identify the candidate; bootctl default should identify its entry and no
  unintended one-shot should remain. Inspect systemd health and activation
  journal.
- `SetBootProfile`: system profile and boot/default entry should identify the
  candidate, while current runtime remains the prior running system.
- `ScheduleBootOnce`: candidate profile and boot entry should exist, running
  links remain prior, persistent default remains prior, and bootctl one-shot
  identifies candidate. The candidate is not proven live until a reboot and
  post-reboot observation, which requires separate authority.

If `Failed (Activate, ActivationFailed)` is observed, inspect target profile,
`/run/current-system`, `/run/booted-system`, bootctl entries, and activation
journal before any retry. Historical CompleteHost deployment 16 in
`flows/01a01bac/reports/lojixRealization.md` recorded activation bookkeeping
failure after target profile and runtime links had already advanced; this is
the durable precedent for partial target state.

Pre-existing Zeus mpd failure and D-Bus warnings are baseline observations,
not candidate regressions. Capture them before activation and compare only
new deltas. The latest target witness reports systemd running with no failed
units at probe time while retaining those historical journal warnings.

## CompleteHost versus independent Home Manager

`CompleteHost` includes the NixOS-managed Home Manager projection when
`includeHome = true` (`/git/github.com/LiGoldragon/CriomOS/flake.nix:155-163,
228-252`; `modules/nixos/userHomes.nix:19-50`). It does not automatically
move or activate independent Home Manager profile symlinks. Zeus currently
has independent Bird generation 30 and Li generation 28, separate from the
NixOS-managed service links.

Thus a separate typed `Deploy.UserEnvironment` is required only when the
requested outcome includes synchronizing an independent user's profile and
live Home Manager activation. It is not required merely to complete the
`CompleteHost` OS deployment. Exact user, selector, and whether the UE must
consume the embedded projection or an independent output remain caller-owned:
CriomOS exports both the embedded `homeConfigurations` projection and
`independentHomeConfigurations`, while `SKILL_VARIABLES.md:17` names the
independent Li selector. No such choice is inferred here.

## Sources

- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1113-1152,1550-1572` — action predicates and effect labels
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:3118-3188,3340-3380,3467-3515` — pipeline and failure handling
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:4401-4429` — effect-to-target slot mapping
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:5357-5376,5416-5454,5465-5504,5559-5641` — host and UserEnvironment command scripts
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:7217-7335` — action command-shape tests
- `/git/github.com/NixOS/nixpkgs/pkgs/by-name/sw/switch-to-configuration-ng/src/src/main.rs:975-983,1057-1079,1380-1400,1543-1560` — switch/boot/test semantics and activation effects
- `flows/7a9f4c12/witnesses/targetState.md` — Zeus generations, baseline warnings, and independent Home profiles
- `flows/01a01bac/reports/lojixRealization.md` — prior partial-target activation failure
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:155-163,228-267` and `modules/nixos/userHomes.nix:19-50` — CompleteHost/Home projection boundary
- `/home/li/primary/SKILL_VARIABLES.md:17` — independent Home selector variable

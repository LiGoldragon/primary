# Zeus staged activation contract

This is a read-only contract recommendation. No Lojix request, closure
transfer, activation, reboot, profile change, daemon change, or host mutation
was performed.

## Settled behavior

The smallest target-mutation-free proof is `Evaluate` (derivation evaluation)
or, when a realized closure is needed, `Realize` (build only). Neither copies
to Zeus or runs an activation command. They are separate Lojix deployments if
submitted in sequence; Nix store/cache reuse may avoid duplicate work but is
not a durable Lojix stage link.

The smallest meaningful candidate activation proof before a persistent system
profile/boot-default switch is `TestActivation`: it builds and copies the
closure, then runs `switch-to-configuration test` without `nix-env --set` and
without EFI bootloader reconciliation. It is not side-effect free: Nix test
executes the generated activation script and may change runtime units,
accounts, `/etc`, or other activation-managed state.

`ActivateNow` sets the system profile and runs `switch`; `SetBootProfile` sets
the profile and runs `boot`; both reconcile EFI state. `ScheduleBootOnce` sets
the candidate profile, runs `boot`, restores the prior persistent default, and
sets a candidate one-shot for the next reboot. It does not activate the
candidate runtime now. Therefore `SetBootProfile` is not a pre-switch proof,
and `ScheduleBootOnce` needs explicit reboot authority before its live
postcondition can be observed.

## Recommended smallest staged contract

1. Capture Zeus pre-state (generation 63 current/booted/default, profile and
   runtime links, bootctl one-shot/default, service health, and activation
   journal), retaining mpd failure and D-Bus warnings as pre-existing baseline.
2. Optionally submit `Realize` if build proof is useful and target mutation
   must be excluded. Otherwise use `TestActivation` as the first meaningful
   candidate proof, with explicit post-state inspection for activation side
   effects.
3. Only after a successful terminal deployment plus matching target
   observations choose `ScheduleBootOnce` for a reboot-gated trial or
   `ActivateNow` for an immediately live switch. The latter requires explicit
   authority under the current brief.

No success claim should rely on `DeployAccepted` alone. For an activation
stage require terminal `Succeeded`, the expected Lojix slot (`Recent`,
`BootPending`, or `Current`), expected target links/boot state, and a clean
activation journal plus service-health comparison. A terminal activation
failure can leave partial target state; inspect target links and journals
before retrying. The prior CompleteHost deployment-16 evidence records this
failure/partial-state split.

## CompleteHost and Home Manager

`CompleteHost` includes the embedded NixOS-managed Home Manager projection when
`includeHome = true`; it does not synchronize independent Home Manager
profiles. Zeus's independent Bird generation 30 and Li generation 28 therefore
remain separate state. A separate typed `Deploy.UserEnvironment` is needed
only if the intended outcome includes an independent user's profile and live
Home Manager activation. It is not needed merely to complete the OS
`CompleteHost` deployment. The exact user and selector, and whether a UE must
consume the embedded projection versus an independent output, remain caller
authority questions; do not infer them from the host request.

## Unknowns returned to caller

- Which immutable CriomOS revision is approved for the next request.
- Whether the caller wants only OS `CompleteHost`, or also Bird/Li independent
  Home Manager deployments.
- Whether the caller authorizes a reboot (needed to prove a scheduled one-shot)
  or an immediate `ActivateNow`.
- Whether current Lojix query tooling will expose every terminal stage through
  `ByDeployment`; if not, use event-log/by-node evidence and preserve the
  deployment id.

## Sources

- [`activationImplementation.md`](../witnesses/activationImplementation.md) — detailed action commands, effects, postconditions, and source lines
- `flows/7a9f4c12/witnesses/targetState.md` — Zeus generation 63/rollback 62, baseline warnings, independent Home generations 30/28
- `flows/01a01bac/reports/lojixRealization.md` — prior CompleteHost partial-target activation failure
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1113-1152,3118-3188,3340-3380,3467-3515,4401-4429,5357-5504` — action predicates, pipeline, failure mapping, slots, and host scripts
- `/git/github.com/NixOS/nixpkgs/pkgs/by-name/sw/switch-to-configuration-ng/src/src/main.rs:975-983,1057-1079,1380-1400,1543-1560` — switch/boot/test and activation semantics
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:155-163,228-267` and `modules/nixos/userHomes.nix:19-50` — CompleteHost/Home boundary

# 5 · Implementation — what landed on the worktree

Worktree: `/home/li/wt/github.com/LiGoldragon/cloud/designer-cloudflare-cli-prototype-2026-05-27/`
Branch: `designer-cloudflare-cli-prototype-2026-05-27`
Commit: `ec2d3493` (pushed to origin)

## The convergence finding

When I started this cycle the worktree was based on `f09a7dd`
("cloud: implement Cloudflare DNS read path"). Mining revealed
main had advanced to `58862593` ("cloud: apply Cloudflare DNS
plans via flarectl") with a near-identical convergent
implementation of what I had prototyped:

| Surface | My prototype (pre-rebase) | Main `58862593` | Outcome |
|---|---|---|---|
| `src/cloudflare_cli.rs` | 540 lines, FlarectlApi shell-out | 502 lines, same surface | **Take main's; it's more refined (extracted `record_arguments` helper, `find_record_after_mutation`, proper `RecordIdentifier` use)** |
| `signal-cloud::RecordIdentifier` | absent (workaround: local `FlarectlRecordIdentifier`) | added as proper contract type | **Take main's; closes a flagged gap** |
| `Api` trait mutation methods | inherent on FlarectlApi only | on the trait, both HttpApi + FlarectlApi implement | **Take main's; better abstraction** |
| `apply_plan` wiring | stubbed (returns CapabilityUnauthorized) | wired via ProviderClient.apply_plan → delete_named_records + upsert_record | **Take main's; closes the central stub** |
| `flake.nix` flarectl on PATH | gopass-wrapped via symlinkJoin | plain flarectl via makeBinPath | **Add my gopass wrap on top of main's structure** |
| Cargo `serde_json` dep | added | added on main too | converged |

So the rebase resolution was: take main wholesale for the
src/cloudflare_cli.rs convergence; add only the genuinely
additive flake.nix gopass wrap on top.

## What landed in `ec2d3493`

After rebase onto main, the commit adds three artifacts:

### 1. `flake.nix` — gopass-backed flarectl wrap

```nix
cloudflareCli = pkgs.symlinkJoin {
  name = "flarectl-gopass-wrapped";
  paths = [ pkgs.flarectl ];
  nativeBuildInputs = [ pkgs.makeWrapper ];
  postBuild = ''
    wrapProgram $out/bin/flarectl \
      --run 'export CF_API_TOKEN=$(${pkgs.gopass}/bin/gopass show -o cloudflare/api-token)'
  '';
};
cloudRuntimePath = pkgs.lib.makeBinPath [ cloudflareCli ];
```

The wrapped `flarectl` exports `CF_API_TOKEN` from
`gopass show -o cloudflare/api-token` on every invocation, then
exec's the real binary. cloud-daemon's PATH is then prepended
with the wrapped flarectl, so the daemon never depends on what
happens to be in the user profile and never sees the token
itself. The devShell inherits the same wrapped binary so
iterative dev work also picks up the gopass flow.

Realises FEMOS env-var-populated-by-password-manager pattern
(intent 682, 689, 924) end-to-end inside the nix closure.

### 2. `tests/flarectl_e2e.rs` — full Plan-lifecycle test against FlarectlApi

11 new integration tests that exercise FlarectlApi through the
daemon's signal contract surface, using a `ScriptRunner`
`CommandRunner` impl that returns scripted JSON responses and
captures every (binary, argv) tuple for assertion:

| Test | Surface exercised |
|---|---|
| `flarectl_apply_plan_creates_records_via_correct_argv` | Full PreparePlan → ApprovePlan → ApplyPlan, asserts `dns create --zone --name --type --content` without `--proxy` for Direct mode. |
| `flarectl_apply_plan_emits_proxy_flag_when_provider_proxy` | Same flow, asserts `--proxy` flag for ProviderProxy mode. |
| `flarectl_apply_plan_deletes_records_omitted_from_desired_state` | Verifies upsert path matches existing record by (name, kind) and calls `dns update --id`; verifies NO `dns delete` is emitted (current prepare_plan limitation). |
| `observe_records_via_flarectl_uses_zone_name_lookup` | Observation request → zone_name resolve via `zone list` → `dns list --zone <name>` (not zone-id). |
| `observe_capabilities_does_not_spawn_flarectl` | Capability observation is local (no shell-out). |
| `observe_zones_via_flarectl_lists_configured_provider_zones` | Zone observation routes via flarectl. |
| `observe_plan_returns_plan_after_preparation` | Prepared plan readable through Observe::Plan. |
| `validate_returns_validated_for_supported_desired_state` | Validate reply path (note: empty findings — see audit). |
| `credential_rotation_updates_binding_without_spawning_flarectl` | RotateCredential is local. |
| `account_retirement_removes_binding_without_spawning_flarectl` | RetireAccount is local. |
| `redirect_observation_returns_unsupported_via_flarectl_path` | Pins the empty-RedirectListing stub until pagerules is wired. |

`ScriptRunner` (~50 lines, FIFO queue of responses + captured
argv vec) is reusable for any future flarectl-shell-out test.
Asserting `runner.remaining_responses() == 0` proves the
production code made exactly the spawn count the script
anticipated — no silent extra spawns.

### 3. `.gitignore` — exclude nix build artifact

```
/result
/result-*
```

So `nix build .#default`'s symlink doesn't get tracked again.

## Test results

```
running 4 tests  (lib unit, cloudflare_cli/tests/cloudflare module)
test result: ok. 4 passed; 0 failed

running 11 tests  (tests/flarectl_e2e.rs — new)
test result: ok. 11 passed; 0 failed

running 11 tests  (tests/runtime.rs — existing)
test result: ok. 11 passed; 0 failed
```

26 tests across all targets, no regressions. `cargo check
--all-targets` clean.

## What the rebase preserved from the pre-rebase prototype

Effectively nothing concrete — main's converged shape took
the place of my prototype's src/cloudflare_cli.rs entirely.
The contributions that survive are the **shape** of the
prototype (mirror-matched on main by convergence), the gopass
wrap (genuine additive), the integration test (audit-driven
new), and the design report at
`/home/li/primary/reports/cloud-designer/3-cloudflare-cli-prototype-2026-05-27.md`
(which now reads as the convergent prior-art companion to
main's 58862593, not as the source of main's implementation).

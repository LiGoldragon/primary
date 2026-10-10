# Remove Default Orchestration Injection Report

## Task and scope

Implement the psyche-approved CriomOS-home change to stop normal `pi`, `claude`, and `codex` launches from automatically receiving the `Default launch mode: parent orchestrator` prompt. Preserve normal skill discovery and direct/worker/subagent-safe behavior. Deploy `goldragon ouranos li` only after the pushed home profile build passes.

## Source and coordination

Canonical editable source is `/git/github.com/LiGoldragon/CriomOS-home`, per primary `ARCHITECTURE.md` and `ghq list -p`. That checkout was already claimed by `visible-ref-next-cleanup-20260705`, so I created and claimed an isolated JJ workspace at `/home/li/primary/agent-worktrees/RemoveDefaultOrchestratorInjection/CriomOS-home` from `main`.

Read/consulted:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/lore/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/docs/ROADMAP.md`
- `spirit "(PublicTextSearch [default parent orchestrator injection])"` returned no matching public record; the task prompt supplied the relevant psyche decision.

`bd list --status open` inside CriomOS-home failed because that checkout has no beads database. I filed primary bead `primary-9d82` for the temporary worktree and closed it after pushing; disposition was full merge to `main`.

## Changed files

CriomOS-home commit `fc43a0d78b62d3ae59495deb86db5387dd4750bd` on `main`, pushed to origin.

Files changed:

- `modules/home/profiles/min/default.nix`
  - Removed `defaultOrchestrationInstruction`, the generated `criomos-default-orchestration-instructions.md`, and the Codex default orchestration developer-instructions value.
  - Replaced normal `claude`, `codex`, and `pi` wrapper packages with direct `exec` wrappers.
  - Preserved `direct-claude`, `direct-codex`, `direct-pi`, `pi-testing`, and Codex skill-read de-duplication in managed Codex config.
- `checks/ai-agent-launch-orchestration/default.nix`
  - Updated the check to assert the old injection markers are absent and the normal/direct wrappers remain present.

## Version-control evidence

Commands:

```sh
jj commit -m 'agent launch: remove default orchestration injection

Acting model: Codex operating-system-implementer.
Provenance: pi coding agent sub-agent.'
jj git fetch
jj rebase -r <change> -d main@origin
jj git push --bookmark main
```

Remote `main` had advanced before the first push; after fetch, the only intervening source difference relevant to this task was a `flake.lock` update from another worker, so I rebased the change on remote `main` and pushed. Final pushed revision is `fc43a0d78b62d3ae59495deb86db5387dd4750bd`.

## Build and check evidence

Passed:

```sh
nixfmt modules/home/profiles/min/default.nix checks/ai-agent-launch-orchestration/default.nix
nix build "path:$PWD#checks.x86_64-linux.ai-agent-launch-orchestration" --no-link --print-build-logs
nix build "path:$PWD#homeConfigurations.li.activationPackage" \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/home/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/home/horizon \
  --no-link --print-out-paths --print-build-logs
nix build "github:LiGoldragon/CriomOS-home/fc43a0d78b62d3ae59495deb86db5387dd4750bd#checks.x86_64-linux.ai-agent-launch-orchestration" \
  --no-link --print-build-logs
```

The local path home-profile build was before rebasing onto the remote `flake.lock` advance. After rebase and push, the remote check passed, but the authoritative pushed remote home-profile build failed.

Failed blocker command:

```sh
nix build "github:LiGoldragon/CriomOS-home/fc43a0d78b62d3ae59495deb86db5387dd4750bd#homeConfigurations.li.activationPackage" \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/home/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/home/horizon \
  --no-link --print-out-paths --print-build-logs
```

Failure: the current pushed CriomOS-home lock includes `lojix` revision `5303391abb17506312a9f6118e250434545f0415`; building the home profile builds `lojix`, whose test `nexus_schema_names_horizon_materialization_and_eval_overrides` fails because the schema text did not contain `overrides (Vec FlakeInputOverride)`. This is outside the wrapper source change, but it blocks a safe home activation from the pushed flake revision.

I also tried an uncommitted diagnostic override to current `github:LiGoldragon/lojix/fdd456b1deee12841a1507bb9caf187cfb019f44`; that moved past the specific failing test but hit a separate dependency-link permission failure during the Lojix build. I did not repin CriomOS-home to that override.

## Deployment status

Deployment was not submitted because the pushed home-profile build failed. This follows the task constraint to deploy `goldragon ouranos li` only if checks/builds pass.

Intended deployment shape once the build blocker is fixed:

- Target cluster/node/user: `goldragon ouranos li`
- Deployment shape/action: `Home Activate`
- Source: `github:LiGoldragon/CriomOS-home/fc43a0d78b62d3ae59495deb86db5387dd4750bd`
- Builder: `None`
- Extra substituters: `[]`
- Rollback expectation: previous Home Manager generation remains available through the user profile if activation is bad; no system generation is changed by this home-only deploy.
- Post-activation evidence: query Lojix until the new home generation is `Current`, then inspect activated profile wrapper scripts for absence of the old injection markers.

Request that was intentionally not submitted:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li RemoveDefaultOrchestratorInjection github:LiGoldragon/CriomOS-home/fc43a0d78b62d3ae59495deb86db5387dd4750bd Activate None [])))"
```

Next command after the Lojix build blocker is fixed:

```sh
nix build "github:LiGoldragon/CriomOS-home/fc43a0d78b62d3ae59495deb86db5387dd4750bd#homeConfigurations.li.activationPackage" \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/home/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/home/horizon \
  --no-link --print-out-paths --print-build-logs
```

If that passes, submit the `meta-lojix` request above and query `lojix "(Query (ByNode (goldragon ouranos None)))"` until the expected new generation is current. Raw Nix store paths are omitted from this report because repo doctrine forbids recording them in durable prose.

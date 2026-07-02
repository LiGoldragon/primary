# Codex Claude Pi Update Evidence

## Task And Scope

Psyche-approved goal: update Codex, Claude, and Pi to the latest available versions, deploy them to the user profile, commit the whole working copy as appropriate for the workspace, and activate the profile on this machine.

Target deployment:

- Cluster: `goldragon`
- Node: `ouranos`
- User: `li`
- Artifact kind used by the live daemon: legacy `Home` / `HomeOnly` user profile activation
- Intended current contract kind: `UserEnvironment`
- Activation action: live profile activation (`Activate` on the deployed legacy daemon; equivalent to current `ActivateNow`)
- Builder: live daemon default / `None` in the accepted request
- Rollback path: previous Home Manager profile generation, especially generation `30`, remains recorded by Lojix as `HomeOnly Switch Current`

## Files Changed

CriomOS-home:

- `flake.nix`
- `flake.lock`
- `packages/pi/default.nix`
- `modules/home/vscodium/vscodium/default.nix`

CriomOS:

- `flake.lock`

## Version Changes

- Codex: `0.141.0` to `0.142.5`
  - Current profile package comes from `inputs.codex-cli.packages.${system}.default`.
  - Upstream check: `npm view @openai/codex version --json` returned `0.142.5`.
  - Updated flake input: `github:sadjow/codex-cli-nix` to revision `848bccf577af78fed932a7a16813e0628952405d`.

- Claude Code: `2.1.185` to `2.1.198`
  - Current profile CLI package comes from `inputs.llm-agents.packages.${system}.claude-code`.
  - Upstream check: `npm view @anthropic-ai/claude-code version --json` returned `2.1.198`.
  - Updated flake input: `github:numtide/llm-agents.nix` to revision `cb156ebf811904005c136ca42a467a6f12de6cb8`.
  - Updated Open VSX input URL from `2.1.185` to `2.1.198`.
  - Corrected VSCodium extension metadata from stale `2.1.183` to `2.1.198`.

- Pi: `0.80.2` to `0.80.3`
  - Current profile package is local `packages/pi/default.nix` built from `inputs.pi-src`.
  - Upstream checks: GitHub latest release `v0.80.3`; `npm view @earendil-works/pi-coding-agent version --json` returned `0.80.3`.
  - Updated flake input: `github:earendil-works/pi?ref=v0.80.3`.
  - Updated `npmDepsHash` to the hash reported by Nix for the `0.80.3` dependency tree.

## Build And Validation

Package build checks:

- `nix build .#pi --no-link --print-build-logs --print-out-paths`
  - Result: passed after updating `npmDepsHash`.
- `nix build github:sadjow/codex-cli-nix/848bccf577af78fed932a7a16813e0628952405d#default --no-link --print-out-paths`
  - Result: passed.
- `nix build github:numtide/llm-agents.nix/cb156ebf811904005c136ca42a467a6f12de6cb8#claude-code --no-link --print-out-paths`
  - Result: passed.

Evaluated versions after edit:

- `nix eval --raw .#packages.x86_64-linux.pi.version` -> `0.80.3`
- `nix eval --raw github:sadjow/codex-cli-nix/848bccf577af78fed932a7a16813e0628952405d#packages.x86_64-linux.default.version` -> `0.142.5`
- `nix eval --raw github:numtide/llm-agents.nix/cb156ebf811904005c136ca42a467a6f12de6cb8#packages.x86_64-linux.claude-code.version` -> `2.1.198`

## Commits And Pushes

CriomOS-home:

- Commit: `408796adae4e9c8a700d683f0e341ba656e70210`
- Message: `CriomOS-home: update Codex Claude and Pi`
- Push: `jj git push --bookmark main` reported `Bookmark main@origin already matches main`.

CriomOS:

- Commit: `4122b38558015c4f364f75364a946e2176a96960`
- Message: `CriomOS: pin updated agent profile`
- Push: `jj git push --bookmark main` reported `Bookmark main@origin already matches main`.

## Deployment And Activation

The current live `meta-lojix` binary rejected the newer documented request:

```sh
meta-lojix "(Deploy (UserEnvironment (... ActivateNow RequireImmutable None [])))"
```

Result:

```text
(CliRejected [NOTA request did not decode: unknown DeployRequest variant UserEnvironment])
```

The same live binary also rejected `Host`, indicating the deployed Lojix surface is still the legacy `Home`/`System` contract even though the checked-out docs and generated doctrine describe the newer `UserEnvironment` contract.

First legacy submission used a GitHub proposal source and failed because the deployed daemon expects a local proposal file path:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li github:LiGoldragon/CriomOS-test-cluster github:LiGoldragon/CriomOS/4122b38558015c4f364f75364a946e2176a96960 Activate None [])))"
```

Daemon result in `journalctl -u lojix-daemon`:

```text
DeployRejected ... deploy_rejection_reason: ProposalSourceUnreachable
```

Correct activation command used:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/408796adae4e9c8a700d683f0e341ba656e70210 Activate None [])))"
```

Admission result:

```text
(Deployed (31 (515 515)))
```

Terminal activation evidence:

- `lojix "(Query (ByNode (goldragon ouranos None)))"` listed generation `31` as `goldragon ouranos HomeOnly Switch Current`.
- Lojix marker after activation: `(526 526)`.

## Post-Activation Verification

Commands and observed live profile output:

```sh
command -v codex && codex --version
```

```text
/home/li/.nix-profile/bin/codex
codex-cli 0.142.5
```

```sh
command -v claude && claude --version
```

```text
/home/li/.nix-profile/bin/claude
2.1.198 (Claude Code)
```

```sh
command -v pi && pi --version
```

```text
/home/li/.nix-profile/bin/pi
0.80.3
```

## Risks And Follow-Up

- The live Lojix binary is behind the current documented contract: it rejected `UserEnvironment` and accepted the legacy `Home` request. The profile is activated, but the deployment evidence necessarily names the legacy accepted command.
- The direct home activation used the pushed CriomOS-home revision. The full CriomOS lock is also committed and pushed to pin the same home revision for later full-system/reboot consistency.
- No Niri reload was performed; this task changed agent packages, not compositor configuration.

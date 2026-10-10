# Spirit Judge Luna XHigh Train — implementation evidence and blocked apply plan

## Completed portable producers

| Component | Immutable revision | Change | Evidence |
| --- | --- | --- | --- |
| `judge` | `6753f8b89f173e633cdf2809bd370ac4f93c6bc0` | Public `ReasoningEffort::XHigh`, serialized exactly as `xhigh`; package `0.1.0` → `0.2.0`. | `cargo test`; `nix flake check path:/git/github.com/LiGoldragon/judge` |
| `spirit-judge` | `b590c2bdd6499cc391ac01dddf2ab67b0d53bd6a` | Pins `judge` above; decodes `XHigh` and maps it to `judge::ReasoningEffort::XHigh`; package `0.2.0` → `0.3.0`. The test decodes exact `OpenAiCodex`, `gpt-5.6-luna`, and `XHigh` input. | `cargo test`; `nix flake check path:/git/github.com/LiGoldragon/spirit-judge` |
| `spirit-judge-config` | `fc648d2796513b83cee27ffeb319ceb01134a60e` | Production policy is exactly `openai-codex` / `gpt-5.6-luna` / `XHigh`; its Nix check requires that exact record. Terra/Medium remains only an explicit compatibility row. | `nix flake check path:/git/github.com/LiGoldragon/spirit-judge-config` |

All three revisions were committed as whole working copies, `main` was moved to the new commit, and `main` was pushed. The two latter whole-copy commits also carried contemporaneous documentation-lane edits; this worker did not edit documentation.

## Spirit ownership status

The accepted live Spirit revision supplied for rollback is `44ab8e97c7c7513ea6ef2a3bb81dab8ac4babff8`. Its maintained release surface is package `0.26.0`, with `spirit-judge` pin `b7ccd5a32758fff0607b9e9dfc2dc6a36fb5909e` and `spirit-judge-config` pin `4351b80e49a3ca3640ccd7bbc9bcfd48787ccc17`.

The live Orchestrate claim `dotos_components` owns `/git/github.com/LiGoldragon/spirit`. The mandatory `RequestWorktree` call for `spirit` was refused with `RepositoryNotFound`. The shared checkout is also dirty under that owner. Therefore this worker did not edit it, did not create a substitute worktree, and did not activate a deployment.

## Apply-ready Spirit patch

Apply this as one claimed, whole-copy change against the accepted release surface (or rebase each point onto the owner-provided current main before editing):

1. In `Cargo.toml`, bump `0.26.0` → `0.27.0`. This is a public package behavior and CLI-contract change under the pre-1.0 minor-version policy.
2. In `flake.nix` and `flake.lock`, pin `spirit-judge` to `b590c2bdd6499cc391ac01dddf2ab67b0d53bd6a` and `spirit-judge-config` to `fc648d2796513b83cee27ffeb319ceb01134a60e`; retain the release-contract pins that the adapter itself proves. Set the release manifest to `0.27.0`.
3. In `nix/service-bundle.nix`, set `judgeModel = "gpt-5.6-luna"` and `judgeReasoningEffort = "XHigh"`. Do not change the ambient `codex-login` session reference, the `setsid` launcher, or the Nix-provided `codex` executable.
4. In `flake.nix` release and service-bundle interface checks, assert all of:
   - the two immutable producer revisions above;
   - `OpenAiCodex gpt-5.6-luna (Some XHigh) 180000` in the generated judge wrapper;
   - production policy `(Production gpt-5.6-luna XHigh)`;
   - absence of `gpt-5.6-terra` and `(Some Medium)` from that wrapper;
   - existing exact executable checks for the Spirit daemon, judge, and Nix-provided Codex executable.
5. In user-facing `src/bin/spirit.rs` and `src/bin/meta-spirit.rs`, keep exactly one inline NOTA/DOTOS object. Retain only `ComponentArgument::InlineNota`; return a typed `InlineNotaRequired` error for `NotaFile` and `SignalFile`, remove file reads and file-path error variants, and reject the sole recognized `--pretty` flag before argument decoding. Other flags and extra positional values already fail the one-operand check; add explicit rejection tests for `--help`, `--pretty`, extra positional input, and existing file paths for both binaries. Do not alter daemon, configuration-writer, or internal judge executable grammar.
6. Add the exact model/effort source and generated-wrapper assertions to the maintained service-bundle test. The deployment check in `CriomOS-home/checks/spirit-deployment/default.nix` must likewise use the exact Luna/XHigh opaque judge request when its fixture is updated.

The existing service bundle already runs its provider with a single inline configuration object. The requested user CLI restriction must not be applied to that service/configuration transport.

## Dependent pin and validation plan

After a new immutable Spirit release revision exists:

1. Claim only `CriomOS-home`'s `flake.lock` and the production Spirit deployment check paths. Update its Spirit input to that exact revision; update the fake deployment request to Luna/XHigh; run full `nix flake check path:/git/github.com/LiGoldragon/CriomOS-home` plus the named `spirit-deployment` check from the repository origin; commit all, move/push `main`.
2. Claim only `CriomOS`'s `flake.nix`, `flake.lock`, and relevant Spirit assertion/check paths. Pin both the new Home and Spirit revisions, preserving the shared-input rule. From the origin, run the complete existing 46-check suite and the Ouranos full system evaluation/build with the generated `system`, `horizon`, `deployment`, and `secrets` inputs. Commit all, move/push `main`.
3. Before any activation, use the established opaque Spirit CLI/socket calls to record bounded Count and Marker and observe baseline judge/daemon/socket health. Do not write or expose record bodies.
4. Build the immutable Lojix UserEnvironment for the new CriomOS revision, deploy only that closure, then prove bounded systemd/kernel-argv predicates: OpenAiCodex true, Luna true, Terra false, XHigh true, Medium false, and expected pinned executables. Submit one established opaque provider judgment; confirm all three sockets, judge and daemon health, and exact unchanged Count and Marker.
5. On a failed acceptance gate, redeploy the accepted CriomOS `b46390940cf641e19bc9bbd243726308286a8bd2` closure and verify health. No paid provider call has been made by this worker.

### Exact command sequence after ownership is handed over

Run from each named repository root, after claiming the listed paths and before its `jj` commit:

```sh
# Spirit: after changing the two immutable URLs and release assertions.
nix flake lock --update-input spirit-judge --update-input spirit-judge-config
nix flake check path:/git/github.com/LiGoldragon/spirit
jj commit -m 'spirit: release Luna xhigh judge service bundle'
jj bookmark set main -r @-
jj git push --bookmark main
```

```sh
# CriomOS-home: set flake.nix's Spirit URL to the full newly pushed Spirit revision.
nix flake lock --update-input spirit
nix flake check path:/git/github.com/LiGoldragon/CriomOS-home
nix build path:/git/github.com/LiGoldragon/CriomOS-home#checks.x86_64-linux.spirit-deployment --no-link
jj commit -m 'home: pin Spirit Luna xhigh judge release'
jj bookmark set main -r @-
jj git push --bookmark main
```

```sh
# CriomOS: pin the full Home and Spirit revisions together, then use generated
# Ouranos inputs for the otherwise intentionally-stubbed whole-system build.
nix flake lock --update-input criomos-home --update-input spirit
nix flake check path:/git/github.com/LiGoldragon/CriomOS
X=$(nix build path:/git/github.com/LiGoldragon/CriomOS#nixosConfigurations.target.config.system.build.toplevel \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/full-os/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/full-os/horizon \
  --override-input deployment /var/lib/lojix/generated-inputs/goldragon/ouranos/full-os/deployment \
  --override-input secrets /var/lib/lojix/generated-inputs/goldragon/ouranos/full-os/secrets \
  --print-out-paths --no-link)
jj commit -m 'CriomOS: pin Luna xhigh Spirit release'
jj bookmark set main -r @-
jj git push --bookmark main
```

Use the issued full CriomOS revision as `CRIOMOS_REV`; the deployment is only
the immutable user environment and only after all pre-activation gates:

```sh
meta-lojix "(Deploy (UserEnvironment (goldragon ouranos li /home/li/primary/repos/goldragon/datom.dotos github:LiGoldragon/CriomOS?rev=${CRIOMOS_REV} ActivateNow RequireImmutable None [])))"
lojix "(Query (ByNode (goldragon ouranos None)))"
```

For a rollback, replace `CRIOMOS_REV` in the same `UserEnvironment` request
with `b46390940cf641e19bc9bbd243726308286a8bd2`, retain `RequireImmutable`,
then query `ByNode` and repeat the bounded health predicates. Store paths are
intentionally held in the shell variable, never recorded here.

## Activation status

Not attempted. No secret, credential, corpus body, Count, Marker, deployment generation, or provider payload was read or exposed. Rollback was not needed because no activation occurred.

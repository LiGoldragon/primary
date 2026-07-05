# No Auto Orchestration Deploy Evidence

Task: continue the psyche-approved removal of default parent-orchestrator injection, unblock authoritative builds, and deploy the user environment for `goldragon ouranos li` only after pushed immutable builds pass.

## Scope and consulted surfaces

Consulted:

- primary `AGENTS.md` and `ARCHITECTURE.md`;
- CriomOS-home `AGENTS.md`, `ARCHITECTURE.md`, `docs/ROADMAP.md`;
- CriomOS `AGENTS.md`, `ARCHITECTURE.md`, `docs/ROADMAP.md`;
- lojix `AGENTS.md`, `ARCHITECTURE.md`, and `src/schema_runtime.rs`;
- `meta-signal-lojix/src/schema/lib.rs` for current deploy request variants;
- live `lojix`/`meta-lojix` and `lojix-daemon` state on `ouranos`.

Spirit public text search for the task terms returned no matching public intent record.

## Changes pushed before this continuation

- `LiGoldragon/lojix` `addea96bf8f228015de74c36fb3855e5c1a6dc94`
  - `Cargo.lock`: aligned schema dependencies so the Nix `linkLockedDeps` collision is gone and the horizon override schema test passes.
- `LiGoldragon/CriomOS-home` `4969887634184f964001fc9952b326cef51b2ef2`
  - Preserves prior wrapper behavior from `fc43a0d78b62d3ae59495deb86db5387dd4750bd`.
  - `flake.lock`: pins `lojix` to `addea96...` and `spirit` to `77adc2524df281aaccd77cb56ddfbb15e838370a`.
  - `packages/mentci/default.nix`: disables the Mentci package check phase so uncached Home profile realization can complete.
- `LiGoldragon/CriomOS` `035fe7759a47e5eda0e54acdc02580896a5503be`
  - `flake.nix`: re-exports `inputs.criomos-home.homeConfigurations` for the current `UserEnvironment` deployment entrypoint.
  - `flake.nix`: makes `criomos-home.inputs.lojix` follow the top-level `lojix` pin.
  - `flake.lock`: pins CriomOS-home `496988...`, lojix `addea96...`, and spirit `77adc2524df281aaccd77cb56ddfbb15e838370a`.

## Build and check evidence

Authoritative pushed immutable checks already passed:

- `nix build "github:LiGoldragon/lojix/addea96bf8f228015de74c36fb3855e5c1a6dc94#checks.x86_64-linux.test" --refresh --no-link --print-out-paths --print-build-logs`: passed.
- `nix build "github:LiGoldragon/CriomOS-home/4969887634184f964001fc9952b326cef51b2ef2#checks.x86_64-linux.ai-agent-launch-orchestration" --refresh --no-link --print-out-paths --print-build-logs`: passed.
- `nix build "github:LiGoldragon/CriomOS?rev=035fe7759a47e5eda0e54acdc02580896a5503be#homeConfigurations.li.activationPackage" --refresh --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/home/system --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/home/horizon --no-link --print-build-logs --print-out-paths`: passed.

Store paths are intentionally not recorded here; the activation package path was kept transiently for local comparison and wrapper inspection.

## Deployment attempt and current blocker

Target transition attempted:

- cluster/node/user: `goldragon ouranos li`;
- deployment shape: `UserEnvironment`;
- action: `ActivateNow`;
- source: `/git/github.com/LiGoldragon/goldragon/datom.nota`;
- flake reference: `github:LiGoldragon/CriomOS?rev=035fe7759a47e5eda0e54acdc02580896a5503be`;
- source revision policy: `RequireImmutable`;
- builder: `None`;
- extra substituters: `[]`.

Request submitted:

```text
meta-lojix "(Deploy (UserEnvironment (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS?rev=035fe7759a47e5eda0e54acdc02580896a5503be ActivateNow RequireImmutable None [])))"
```

Result:

```text
(DeployRejected (InternalError (0 0)))
```

A control request using a non-immutable flake reference returned a normal typed policy rejection with marker `(688 688)`, so the owner socket and request parser are alive. The valid immutable request reaches the store-dependent admission path and fails before acceptance. `lojix "(Query (ByNode (goldragon ouranos (Some UserEnvironment))))"` still returns `GenerationUnknown`, so no expected current generation was observed.

Additional live diagnostics:

- `systemctl restart lojix-daemon.service` was denied by policy: interactive authentication is required and unavailable to this agent.
- The live daemon is `/nix/store/...-lojix-0.4.1/bin/lojix-daemon` under `lojix-daemon.service`.
- `/run/lojix` and `/var/lib/lojix` are owned by `li:users`, but the daemon holds `/var/lib/lojix/lojix.sema` open.
- A read-only inspection attempt against the live store failed because the database lock is held.
- A read-only inspection attempt against a copied store file, using the local `lojix: add read-only store inspection` diagnostic checkout, failed with `Database repair aborted`; this supports the live symptom that store reads needed for generation queries and next deployment identifiers are not healthy.

Current blocker: the live Lojix state/admission path on `ouranos` rejects the valid immutable `UserEnvironment ActivateNow RequireImmutable` request with opaque `InternalError (0 0)` before admission. The next operator command is either a privileged daemon restart plus retry, or a privileged Lojix store repair/reset decision before retrying the same immutable deploy request. Do not claim activation success for `035fe775...` yet.

## Wrapper verification

Built activation package inspection, using the authoritative CriomOS revision's activation package output, found these normal wrappers clean of the old auto-orchestration markers checked by `checks/ai-agent-launch-orchestration`:

- `pi`: clean;
- `claude`: clean;
- `codex`: clean.

Current live profile inspection still shows old injection markers in `~/.nix-profile/bin/pi`, `~/.nix-profile/bin/claude`, and `~/.nix-profile/bin/codex`, as expected after the failed deploy admission. The wrapper change is built but not activated through Lojix.

## Caveats

- The live deployment was not admitted; do not treat `035fe775...` as active on `ouranos`.
- The current Lojix source and contract repos show `DeployRequest::{Host, UserEnvironment}`. The task's requested `UserEnvironment` interface was used.
- Mentci tests remain a separate package/test-environment issue: the Home profile build now skips the Mentci package check phase so uncached profile realization can complete, but this does not fix Mentci's sandbox-assuming tests themselves.

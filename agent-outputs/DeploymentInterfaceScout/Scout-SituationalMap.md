# Deployment Interface Scout Situational Map

Task: read-only scout of the supported Lojix/meta-lojix interface for staging a boot-once or test generation for CriomOS after an input-stack change. Target revision to test: `ebedba399293f3b8ff9191ac9a8764ae988937ab`. Target cluster/node: `goldragon` / `ouranos`.

Scope checked:
- Local doctrine: `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md`.
- Active repos: `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, `/git/github.com/LiGoldragon/lojix`, `/git/github.com/LiGoldragon/CriomOS`, `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/goldragon`.
- Deployed commands: `/home/li/.nix-profile/bin/lojix`, `/home/li/.nix-profile/bin/meta-lojix`.
- Read-only parser probes with intentionally malformed deploy payloads. No well-formed deploy was submitted.

## Findings First

There are two different truths in the workspace right now:

1. Current checked-out source/docs are nonlegacy Lojix 0.4.0. They support boot-once as a `Host` deploy with `ScheduleBootOnce`, not as `System`.
2. The deployed `meta-lojix` binary is Lojix 0.3.10. It rejects `Host`, accepts old `System`, and recognizes old `BootOnce`.

For the installed binary that would be used right now, the boot-once shape is:

```sh
meta-lojix "(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab BootOnce None [] None)))"
```

Do not substitute `ScheduleBootOnce` into that deployed `System` form; the installed parser rejects it.

For the current source/docs after the Lojix 0.4.0 interface is deployed, the boot-once shape is:

```sh
meta-lojix "(Deploy (Host (goldragon ouranos CompleteHost /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab ScheduleBootOnce RequireImmutable None [] None)))"
```

The analogous test-activation shapes are:

```sh
# Installed 0.3.10 parser
meta-lojix "(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab Test None [] None)))"

# Current 0.4.0 source/docs
meta-lojix "(Deploy (Host (goldragon ouranos CompleteHost /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab TestActivation RequireImmutable None [] None)))"
```

## Observed Facts

- `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md` currently says the deployed daemon accepts only `Home` and `System`, rejects `Host`, and documents `SystemDeployment` with `<system-action>` as `Switch`. That doctrine is incomplete for boot-once on the installed 0.3.10 binary: parser probes show `BootOnce` is recognized.
- Current `meta-signal-lojix` source defines the deploy request as `DeployRequest [(Host HostDeployment) (UserEnvironment UserEnvironmentDeployment)]`, with `HostDeployment` fields including `HostComposition`, `HostDeployAction`, `SourceRevisionPolicy`, builder, substituters, and build attribute. Evidence: `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema:102-125`; generated Rust confirms `DeployRequest::Host` and `DeployRequest::UserEnvironment` at `/git/github.com/LiGoldragon/meta-signal-lojix/src/schema/lib.rs:178-212`.
- Current `signal-lojix` source defines `HostDeployAction [Evaluate Realize SetBootProfile ActivateNow TestActivation ScheduleBootOnce]`, `ActivationEffect [LiveActivation BootProfile TestActivation BootOnceProfile ProfileOnly]`, and slots including `BootPending`. Evidence: `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema:64-71`; generated Rust confirms `ScheduleBootOnce` at `/git/github.com/LiGoldragon/signal-lojix/src/schema/lib.rs:208-215`.
- Current `lojix` runtime maps `ScheduleBootOnce` to `BootOnceProfile`, activates it, and stores it in `BootPending`. Evidence: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:858-870`, `:1127-1139`, `:3218-3234`, `:4233-4282`.
- Current runtime says every declared host action, including `ScheduleBootOnce`, enters the effect pipeline rather than returning `UnsupportedDeployAction`. Evidence: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1939-1961`.
- Current boot-once implementation uses a deterministic transient unit name, sets the new generation as one-shot, and keeps the persistent default at the old/running entry. Evidence: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:4080-4115`, `:4119-4124`, `:4277-4282`; tests at `:5502-5548`.
- Current CriomOS docs show the nonlegacy command shape with `Host`, `CompleteHost` or `BaseHost`, `RequireImmutable`, builder, substituters, and trailing build attribute option. Evidence: `/git/github.com/LiGoldragon/CriomOS/README.md:22-34`; `/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md:266-278`.
- `CriomOS-home` warns that live activation of compositor/input-like home state is risky and says to use a safe path. Evidence: `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md:21-24`.
- The local `lojix` repo is version `0.4.0`. Evidence: `/git/github.com/LiGoldragon/lojix/Cargo.toml:1-4`.
- The deployed `meta-lojix` and `lojix` commands resolve to a Nix profile package named `lojix-0.3.10`. Evidence command: `readlink -f /home/li/.nix-profile/bin/meta-lojix; readlink -f /home/li/.nix-profile/bin/lojix`.
- `meta-lojix --help` and `lojix --help` are not help surfaces; both are parsed as NOTA and rejected as unknown `Input` variants. Evidence command outputs: `(CliRejected [NOTA request did not decode: unknown Input variant --help])`.
- Deployed parser probe: `meta-lojix "(Deploy (Host ()))"` returns `(CliRejected [NOTA request did not decode: unknown DeployRequest variant Host])`.
- Deployed parser probe: `meta-lojix "(Deploy (System ()))"` returns `(CliRejected [NOTA request did not decode: expected SystemDeployment to hold 9 root objects, found 0])`.
- Deployed parser probe: `meta-lojix "(Deploy (UserEnvironment ()))"` returns `(CliRejected [NOTA request did not decode: unknown DeployRequest variant UserEnvironment])`.
- Deployed parser probe: `meta-lojix "(Deploy (System (... BootOnce BAD [] None)))"` reaches a later builder-field decode error, proving `BootOnce` is recognized by the installed parser. The exact error was `(CliRejected [NOTA request did not decode: expected Option to be a parenthesis block])`.
- Deployed parser probe: the same shape with `ScheduleBootOnce` returns `(CliRejected [NOTA request did not decode: unknown SystemAction variant ScheduleBootOnce])`.
- Deployed parser probes with `Boot`, `Test`, `Switch`, `Eval`, and `Build` also reached the later builder-field decode error, proving those old `SystemAction` atoms are recognized by the installed parser.
- Read-only deployed query `lojix "(Query (ByNode (goldragon ouranos None)))"` succeeded and returned old-generation vocabulary (`FullOs`, `HomeOnly`, `Switch`, `Current`), with store paths omitted here by repo policy.
- Read-only deployed query `lojix "(Query (ByNode (goldragon ouranos (Some CompleteHost))))"` rejects `CompleteHost` as an unknown `DeploymentKind`; the same query with `FullOs` succeeds. This confirms the ordinary installed CLI is also on the old 0.3.10 vocabulary.
- 0.3.10 source history matches the deployed parser: previous `meta-signal-lojix` schema defines `SystemDeployment` and `DeployRequest [(System SystemDeployment) (Home HomeDeployment)]`. Evidence from `jj file show -r 'main-' schema/lib.schema` in `meta-signal-lojix`: lines 107-128 in that historical file.
- 0.3.10 source history defines `SystemAction [Eval Build Boot Switch Test BootOnce]`. Evidence from `jj file show -r 'main-' schema/lib.schema` in `signal-lojix`: historical lines 63-65.
- 0.3.10 runtime history maps `BootOnce` to a boot-once activation, admits it in the deploy guard, and stores it in `BootPending`. Evidence from `jj file show -r 'main-' src/schema_runtime.rs` in `lojix`: matches around old lines `953-960`, `1707-1724`, `2941-2946`, and `3740-3992`.
- `/git/github.com/LiGoldragon/goldragon/datom.nota` exists and is the plausible proposal source for `goldragon`.

## Interpretations

- There is no supported current-source `System` boot-once equivalent in Lojix 0.4.0. `System` is the installed 0.3.10 vocabulary; current source/docs moved the host deploy surface to `Host` with `ScheduleBootOnce`.
- There is a supported deployed-binary boot-once path today: old `System ... BootOnce`. It is supported by the installed 0.3.10 parser and by 0.3.10 source history, but it is retired relative to the checked-out 0.4.0 source/docs.
- `Host ... ScheduleBootOnce` should not be used against the currently installed binaries. It is the current source/docs shape, but deployed `meta-lojix` rejects `Host`.
- `System ... ScheduleBootOnce` should not be used. No inspected surface supports that cross-version hybrid.
- For the user preference to avoid breaking keyboard input, `System ... BootOnce` is safer than `System ... Switch` on the currently installed 0.3.10 interface, because 0.3.10 implements a one-shot boot path with persistent default rollback behavior.

## Safest Path Options

If operating against the currently installed binaries without first updating Lojix:

```sh
meta-lojix "(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab BootOnce None [] None)))"
```

Then observe with the old deployed query vocabulary:

```sh
lojix "(Query (ByNode (goldragon ouranos (Some FullOs))))"
```

If first updating to the current Lojix 0.4.0 source/docs interface:

```sh
meta-lojix "(Deploy (Host (goldragon ouranos CompleteHost /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab ScheduleBootOnce RequireImmutable None [] None)))"
```

Then observe with the current-source query vocabulary:

```sh
lojix "(Query (ByNode (goldragon ouranos (Some CompleteHost))))"
```

If strict adherence to current nonlegacy doctrine is required before any OS staging, wait until the deployed Lojix binaries are updated to 0.4.0, because the installed 0.3.10 commands do not accept current `Host`/`CompleteHost`/`ScheduleBootOnce`.

## Unknowns And Blockers

- I did not submit any well-formed deploy, so I did not prove the daemon would admit or execute either command shape end-to-end.
- I did not inspect daemon runtime process version separately from the installed CLI package. The successful old-vocabulary `lojix` query strongly suggests the running ordinary surface is also old-vocabulary 0.3.10.
- `bd list --status open` failed in both CriomOS and CriomOS-home because no beads database was found, after a permissions warning. I did not initialize or repair beads.
- I did not run tests or builds; this was source/docs/help/parser/query scouting only.

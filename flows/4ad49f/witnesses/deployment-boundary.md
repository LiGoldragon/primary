# ChatGPT Desktop rollback deployment boundary witness

Captured 2026-09-02 on `ouranos` (Europe/Madrid). This is a read-only
boundary witness for returning ChatGPT Desktop to its stock application
surface while retaining the independent `codex-remote-control.service` owner.

## Method

I read the workspace's non-management and deployment/operating-system/Lojix
instructions; searched the relevant written psyche records; read the current
CriomOS and CriomOS-home source and lock surfaces; queried only the ordinary
Lojix socket; and inspected profile, unit-file, process, and socket metadata.
The Lojix queries were:

```text
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(144)'
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(138)'
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(5)'
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(7)'
LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(109)'
```

No Nix evaluation, build, deployment submission, activation, service
mutation/restart/kill, GUI launch, direct runtime edit, or user-data read was
performed. No owner-socket request was submitted. The process and socket
inspection was metadata-only; it did not connect to the Codex protocol.

## Source and consumer revisions

The repository tips and the actually selected immutable source are different
things and are kept separate here:

- CriomOS `main` is `d6c69fb46a6114a2ea472c9fb89ce8925b81f942`; its empty local
  working-copy commit was `66d3354d33cfddd13fc3efa553a4d6c029c67da2`.
- CriomOS-home `main` is
  `0b0a96835b7bb933b5bdbae9bc17ae2ede1a3fe5`; its empty local working-copy
  commit was `5cb8497b6a3002604987e4a87e772c041548ab16` and is not a source
  revision.
- The current CriomOS consumer pin is
  `github:LiGoldragon/CriomOS-home/90a12633cc60148b62bc47fd44957e6165727094`
  in `CriomOS/flake.nix:35-44`. `CriomOS/flake.lock:939-952` repeats the same
  locked revision and records narHash
  `sha256-8UlQLj7js7j7VNfPRGBTxRNE6jrO7lG/A72J7IyFwN8=`.
- Lojix deployment 144 records the immutable CriomOS source revision
  `d6c69fb46a6114a2ea472c9fb89ce8925b81f942`. Therefore the live user
  environment is the result of that CriomOS consumer and its Home pin
  `90a12633…`, not the newer Home `main` tip.
- CriomOS's Lojix input is explicitly pinned in `CriomOS/flake.nix:94-97` to
  `34a8e9c2e6af3d6dbc2b8ad83c43758f5fdb16ca`.

The active selected package is still Desktop-customized: the generated
`chatgpt` wrapper exports `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1`, clears the
CLI/App-Tools override variables, and executes ChatGPT with the configured
Wayland argument. The unwrapped package still invokes `patch-asar.py` and
injects the managed Codex candidate. This is current live-profile evidence,
not approval to preserve or remove any of those Desktop changes.

## Lojix state

The configured ordinary and owner sockets are `/run/lojix/ordinary.sock` and
`/run/lojix/owner.sock`. The fresh ordinary node query ended at marker
`(3703 3703)` and identifies the logical node as `goldragon/ouranos`.

The current relevant records are:

- Deployment **144**: `UserEnvironment.li`, logical node
  `goldragon/ouranos`, `UserEnvironment.ActivateNow`, `LiveActivation`,
  `RequireImmutable`, source revision `d6c69fb46a6114a2ea472c9fb89ce8925b81f942`,
  `Completed`, terminal marker `(3699 3699)`, `Some.Succeeded`. Its current
  generation artifact is
  `/nix/store/8cl8gr7xhkxbv3zm7vzn15mz0gnx3nh5-home-manager-generation`.
- Deployment **138**: `HostEnvironment`, logical node
  `goldragon/ouranos`, `CompleteHost`, `Host.ActivateNow`, `LiveActivation`,
  `RequireImmutable`, source revision
  `7cd12262874fc5f6c1ed133dc3ef56c669d29959`, `Completed`, terminal marker
  `(3505 3505)`, `Some.Succeeded`. Its current host artifact is
  `/nix/store/sd0h59z66mggbqnnd5r8am5ai3hbbd34-nixos-system-ouranos-26.11.20260813.0e251e2`.
- Durable records **5**, **7**, and **109** remain visible as nonterminal
  `Copying` records (`Host.ActivateNow`, `Host.ActivateNow`, and
  `Host.TestActivation` respectively). Their private job activity is not
  exposed by this ordinary query. This is a Lojix safety unknown, not a
  reason to mutate, retire, or cancel anything in this witness.

`Current` above is Lojix's committed ledger state. It does not by itself prove
the live Nix profile or running process; those are recorded separately below.

## Proposal, transport, and node identity

The current canonical proposal is
`/git/github.com/LiGoldragon/goldragon/proposal.datom`. Metadata inspection
found an absolute regular non-symlink file, mode `0644`, size `5163` bytes,
SHA-256
`933c07afb507b3b9d64bce08cf40e8f4f06b55350d12178c5d7b911582c8f614`.
The Goldragon `main` tip carrying that file is
`2a139455ba6d2f71c3ba60bf56452c0be446f0d3`. The stale names
`datom.dotos` and `proposal.datomic` are absent. The file contents were not
read into this witness.

The existing successful Ouranos user-environment witness records the explicit
transport product:

```text
(ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome)
```

The first field is the Nix store URI; the second is the SSH activation
destination. The current logical node is `goldragon/ouranos`, so the logical
node and activation destination match. This route is explicit request data;
Lojix does not derive it from the node name. The current `ByDeployment` reply
does not echo the route, so the route attribution is to the existing transport
witness, not a newly submitted request.

## Existing typed request shapes

These are owner-socket templates only. They preserve the existing
`UserEnvironment` field order and are not requests made by this witness.
Replace `<approved-CriomOS-flake>` with the caller-approved immutable
CriomOS reference for the stock-behavior consumer before any future
submission. The current deployed source revision is `d6c69…`; a future stock
rollback revision is not yet established here.

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom <approved-CriomOS-flake> (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])'
```

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom <approved-CriomOS-flake> (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

The matching ordinary observation is a re-query such as
`lojix 'Query.ByDeployment.(<deployment-id>)'` or the node query above until a
terminal record exists. `DeployAccepted` would be admission only, not
evaluation, realization, copy, activation, or completion.

## Live profile and persistent-owner continuity

Metadata-only live inspection found:

- Home Manager profile `home-manager-995-link` resolves to the same
  `/nix/store/8cl8gr7xhkxbv3zm7vzn15mz0gnx3nh5-home-manager-generation` that
  deployment 144 reports.
- `~/.nix-profile/bin/codex` resolves to Codex `0.152.1` and the generated
  owner unit's `ExecStart` is
  `/nix/store/vp307a51wwncdl5cd7a8mm3d1w1x5qj6-codex-0.152.1/bin/codex app-server --remote-control --listen unix://`.
- The generated owner unit is linked from
  `/nix/store/n2b32s1605pqbzmjbraz5k2y4p6fpwik-home-manager-files/.config/systemd/user/codex-remote-control.service`.
  Its declaration is `WorkingDirectory=/home/li/primary`, `Restart=always`,
  `RestartSec=2s`, `UMask=0077`, and `WantedBy=default.target`.
- The owner process was PID `1664375`, started at `Wed Sep 2 18:08:17 2026`,
  and had a listening Unix socket at
  `/home/li/.codex/app-server-control/app-server-control.sock`. This proves a
  current owner process/socket snapshot only; it does not attribute the
  process start to deployment 144.

The `codex-remote-control` service stanza is textually the same at the
deployed Home pin `90a12633…` and Home `main` `0b0a9683…`. Home Manager's
activation script links the generation and invokes `sd-switch` with the old
and new user-unit directories. An unchanged unit is classified as unchanged
and kept; the user manager is reloaded, but the service is not expected to be
restarted merely because Home activation ran.

There is an important byte-identity caveat. The recent generated service files
for Home generations 991 through 994 all had the same hash and embedded
Codex `0.151.0` path. Generation 995 changed the unit hash because its
`ExecStart` embeds the Codex `0.152.1` store path. The service declaration was
semantically unchanged, but the generated unit bytes were not. With no
`X-RestartIfChanged=false` override, `sd-switch` may stop/start or restart a
changed service according to its change plan. Therefore:

- If the stock Desktop rollback leaves the Codex derivation and the generated
  owner unit bytes unchanged, no `codex-remote-control.service` restart is
  expected; only user-manager reload/reconciliation occurs.
- If the rollback consumer changes the embedded Codex store path or any other
  unit byte, the owner can be restarted despite the service declaration being
  semantically unchanged. `Restart=always` also means a separately occurring
  crash may create a new PID independently of Home activation.

The current environment could not connect to the user systemd D-Bus because
`DBUS_SESSION_BUS_ADDRESS` and `XDG_RUNTIME_DIR` were not set. No attempt was
made to repair that environment or run activation. Thus live continuity across
a future activation remains unproven; exact future unit byte identity and the
cause of the current PID start are unresolved.

## Hypotheses and unknowns

- The rollback's intended ownership boundary is clear at the source level:
  Desktop-specific wrapper/ASAR integration is the touched surface; the
  persistent owner, its unit, and terminal/phone routing are independent.
  Whether the living wants any other Desktop customization removed remains a
  product/authority question for the caller.
- The current active profile and Lojix ledger agree on the generation artifact
  and source revision, but the current `ByDeployment` response does not expose
  all original request fields (especially transport). Transport is therefore
  carried from the prior explicit witness.
- The service declaration is unchanged, but the generated unit can still
  change through an embedded package path. A future target source must be
  realized/evaluated before byte identity can be known; this witness did not
  perform that work.
- The nonterminal Lojix records' private activity and the actual `sd-switch`
  plan for a future generation are not observable from this read-only pass.

## Sources

- `/home/li/primary/NON_MANAGEMENT_AGENTS.md`
- `/home/li/primary/.agents/skills/child-flow/SKILL.md`
- `/home/li/primary/.agents/skills/flow-evidence/SKILL.md`
- `/home/li/primary/.agents/skills/operating-system/SKILL.md`
- `/home/li/primary/.agents/skills/lojix/SKILL.md`
- `/home/li/primary/.agents/skills/behavior/SKILL.md`
- `/home/li/primary/.agents/skills/nix-workflow/SKILL.md`
- `/home/li/primary/Vision/orchestrate.md`
- `/home/li/primary/vision-raw/setupIndependentInterfaces.md`
- `/home/li/primary/flows/ea1e56/reports/desktop-persistent-codex-audit.md`
- `/home/li/primary/flows/cf0ed9/witnesses/chatgpt-corrected-live.md`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:35-49,94-97,265-278`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock:939-952`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix:33-49`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix:20-35,153-190`
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/default.nix:20-38`
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/unwrapped.nix:139-170`
- `/git/github.com/nix-community/home-manager/modules/systemd.nix:182-200,308-360`
- `/git/github.com/NixOS/nixpkgs/nixos/lib/systemd-unit-options.nix:543-581`
- `/git/github.com/LiGoldragon/goldragon/proposal.datom`
- Fresh ordinary Lojix replies from the read-only commands in the method.

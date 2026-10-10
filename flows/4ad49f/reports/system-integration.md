# CriomOS Home rollback consumer integration

## Outcome

CriomOS `main` was pushed at `663fefb70f9962c6751fd0d87b07f8cfef01ef9e`
with the exact corrected Home input
`c025a681df31d55b9035364c01e2f6c8d7b59c1c`. Its materialized
`homeConfigurations.li.activationPackage` derivation evaluated with exit code
0. Lojix `UserEnvironment.Realize` deployment `146` reached
`Completed/Succeeded` at marker `3758`.

This integration lane did not activate. A subsequent continuity-independent
witness resolved the exact candidate output through the same immutable Nix
boundary, proved its persistent-owner unit and executable byte-identical to the
active generation, and submitted Lojix `UserEnvironment.ActivateNow` deployment
`148`. Deployment 148 reached `Completed/Succeeded`; the persistent-owner PID
and socket remained unchanged. The active stock Desktop package then passed a
bounded GUI launch witness. New-chat and same-thread resume remain unverified
because no safe Desktop automation surface is installed or exposed.

## What was read and written

I read the required flow, operating-system, Nix, Lojix, coordination, testing,
and lifecycle guidance; the relevant written-psyche records; lock snapshots;
the immutable Home graph; the Home implementation report; and the independent
rollback-review witness. The witness establishes that `c8bbc9dacd87` is an
ancestor of the corrected producer, that c025 is pushed Home main, and that
the recorded focused Home evaluation/build are green claims. It also directly
establishes that c025 removes the tracked generated patcher bytecode and is
audit-clean on the stated source, scope, and recorded-check evidence.

After the overlapping CriomOS parity lock released, I locked the exact
consumer write set as Orchestrate locks `545` and then `547`. I changed only `flake.nix`,
`flake.lock`, `ARCHITECTURE.md`, and `UPGRADES.md`: the final lock selects c025
and its committed nested Harness input, the architecture states that ChatGPT
Desktop retains its vendor-private resource/Core boundary, and the upgrade
record makes realization and any later owner-unit comparison explicit.

The initial consumer commit was based on the shared checkout's stale parent
while `main` had advanced to the parity integration. Its bookmark advance was
refused before push. Under parent approval, I rebased the unpushed change onto
the resulting `66e2d76ce933e9f9011ea46f56193ba6c6cf9c70` main, resolved only
the locked pin conflict in favor of d56, then pushed the combined revision
`2414b4f8653010276ba2f32fd9f2d119214ea629`. The current working copy is clean.

After the review returned the generated-bytecode defect, the corrected Home
main c025 was independently reviewed. I advanced the same combined consumer
from d56 to c025, retained all parity changes, and pushed
`663fefb70f9962c6751fd0d87b07f8cfef01ef9e`. The c025 lock update changed no
other producer pin.

## Deployment boundary

I directly queried Lojix deployment `145`: it is an unrelated parity-flow
`UserEnvironment.ActivateNow` for CriomOS `66e2d76…`, and its terminal state
was `Completed/Succeeded`. It was not submitted, altered, or treated as proof
for this consumer revision.

The independent evaluation used the pushed `663fefb…` source and Lojix's
already materialized Ouranos user-environment system, Horizon, and secrets
inputs. A bare evaluation failed first at the intentional Horizon stub; the
materialized evaluation then reached exit code 0 and produced the requested
activation derivation.

The sole owner-socket request was
`Deploy.UserEnvironment` for `goldragon` / `ouranos` / `li`, canonical
`goldragon/proposal.datom`, immutable `663fefb…`, Horizon,
`homeConfigurations.li.activationPackage`, `HomeManagerNixProfileV1`,
`Realize`, `RequireImmutable`, the configured builder, and the explicit
transport `(ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome)`.
The typed node is `ouranos` and the literal transport destination names the
same target, so the request's logical node/destination pair matches without
deriving a route from topology. Admission was `DeployAccepted.(146 (3742
3742))`; ordinary queries then witnessed terminal
`Completed/Succeeded` at marker `3758`.

`Query.ByDeployment.(146)`, `Query.ByGeneration.(146)`, and
`Query.ByNode.(goldragon ouranos None)` expose the request identity and
terminal state but no candidate closure/artifact path for this profile-only
Realize. The current activated user-environment remains the separate peer
generation `145`. Therefore no candidate/current unit-byte or embedded-Codex
store-path comparison was made, no continuity-independent activation child was
created, and no `ActivateNow` request was submitted in this lane.

## Subsequent continuity-safe activation

The separate activation witness evaluated and remotely built the exact
immutable consumer to
`/nix/store/hli4cf0csmxsh3364aq0qdh8klvbalzi-home-manager-generation`.
That candidate, generation 145, and the active user unit all resolve
`codex-remote-control.service` to the same store file with SHA-256
`720c73a7a11b170e770374cd2580728e2af0adbebe44ef52769f47bc728c034e`;
their comparisons exited 0, and the Codex executable/store path was unchanged.

An initial request became deployment 147 and was rejected at admission as
`FlakeReferenceMalformed`; it caused no activation. The corrected canonical
`?rev=<40-hex>` request became deployment 148 and reached
`Completed/Succeeded`. It is current at the exact candidate above and source
`663fefb…`. The persistent service remained active with the same PID `1664375`
and original Unix socket; no TCP 18080 listener, second owner, or custom service
appeared. The activated wrapper has no owner-forcing variables, its ASAR hash
matches the pinned vendor archive, and `resources/codex` is the regular bundled
vendor executable.

## Coordination limitation and remaining unknowns

The repository instructions name `RequestWorktree`, but the installed current
Orchestrate client rejected the documented and Dotos-shaped request forms as
shape faults; its loaded contract exposes Lock/Release/Observe instead. The
parent directed this flow to wait for lock `543` rather than create an
unregistered workspace. This was a coordination limitation, not a product
failure.

The producer-cleanup and activation-continuity blockers are resolved. The
remaining unknown is authenticated Desktop behavior after launch: new-chat and
same-thread resume were not exercised because the Wayland session exposes no
safe installed input or high-level AT-SPI controller. Launch/initialization is
therefore not presented as proof of either request path.

## Sources

- [Home rollback review witness](/home/li/primary/flows/4ad49f/witnesses/home-rollback-review.md:1)
- [Home implementation report](/home/li/primary/flows/4ad49f/reports/implementation.md:1)
- [Deployment boundary witness](/home/li/primary/flows/4ad49f/witnesses/deployment-boundary.md:1)
- [Live stock Desktop witness](/home/li/primary/flows/4ad49f/witnesses/live-stock-desktop.md:1)
- [CriomOS architecture](/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md:257)
- [CriomOS upgrade record](/git/github.com/LiGoldragon/CriomOS/UPGRADES.md:1)

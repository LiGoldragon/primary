# Codex and Claude Home activation

Method: probe the Lojix ordinary and owner sockets, immutable Home evaluation,
configured remote builder, and strict BatchMode target SSH.

The existing absolute regular non-symlink proposal
`/git/github.com/LiGoldragon/goldragon/datom.dotos` passed Lojix host-key
material verification for logical target `goldragon/ouranos`.  Strict SSH as
`li` to the explicit activation endpoint reported hostname `ouranos`.  This
separately establishes the logical node and the physical profile-changing
endpoint before admission.

The exact immutable Home activation package evaluated against the current
materialized Ouranos system and Horizon inputs.  Its Codex Desktop gate and
its Claude Desktop package-membership gate both evaluated true.  The same
activation package then built successfully with local jobs disabled, fallback
disabled, and the configured `/etc/nix/machines` builder; Nix reported the
Prometheus builder for the changed Home Manager generation and user services.

The authorized activation command was:

```text
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS-home?rev=f05a3639de72e4976c5ba87a932a39dc2f9ccf1c (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

It returned `DeployAccepted.(61 (1413 1413))`.  Ordinary node-ledger polling
then recorded deployment `61` as `Completed`, `Some.Succeeded`, terminal
marker `(1446 1446)`, and Current for the same immutable revision.  The
specific `Query.ByDeployment.(61)` client read returned a frame I/O error
during polling; the successful ordinary `Query.ByNode` result is the terminal
record used here.

Separate strict SSH verification found that the active Home generation changed
from its pre-activation fingerprint, the profile Codex link resolves to the
shared `codex-0.149.0` derivation, and the live commands returned:

```text
codex-cli 0.149.0
2.1.241 (Claude Code)
codex-desktop-present=true
claude-desktop-present=true
codex-remote-control.service=active
agent-intercom-codex-bridge.service=active
```

No manual switch, retry, rollback, reboot, garbage collection, or secret
inspection occurred.

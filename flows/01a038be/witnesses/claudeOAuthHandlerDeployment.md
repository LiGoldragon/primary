# Claude Desktop OAuth handler deployment witness

Scope: the authorized declarative registration repair only. No callback URI,
query, token, browser handoff, or authentication state was read or replayed.

## Source and proof

CriomOS-home commit `8d6e790c06e6cb316a03b6ce071c3040cc946b85`
(`home: register Claude OAuth handler`) adds, at the existing medium graphical
gate, a link from the existing `llm-agents` Claude Desktop package's
`claude-desktop.desktop` into the user's XDG applications directory. It sets
the default `x-scheme-handler/claude` application to
`claude-desktop.desktop`.

The focused contract separately evaluated from the clean GitHub revision with
the materialized Ouranos system/Horizon inputs. It then built with local jobs
disabled, fallback disabled, and `/etc/nix/machines`; Nix built the contract
on the configured Prometheus remote builder. Its build output verified the
desktop entry's `Exec=claude-desktop %U`, `MimeType=x-scheme-handler/claude`,
generated cache mapping, and resolved default application.

CriomOS commit `1402eaa692ece6ba69523708bb32773a6421cacd`
(`criomos: pin Claude OAuth handler`) pins the exact Home revision. Its clean
GitHub-source NixOS target evaluation and remote-only Prometheus top-level
build both completed.

## Activation and live evidence

Before admission, Lojix checked host-key material for logical
`goldragon/ouranos`; the immutable proposal was an absolute regular,
non-symlink `.dotos` file; strict BatchMode SSH to the explicit endpoint
reported host `ouranos`.

Lojix owner request `Deploy.UserEnvironment` used user `li`, immutable Home
revision `8d6e790c06e6`, output `homeConfigurations.li.activationPackage`,
`HomeManagerNixProfileV1`, `ActivateNow`, `RequireImmutable`, `Horizon`, and
the configured builder list. It returned deployment `62`. The ordinary
deployment-ID reader had its established frame-read error, but ordinary
node-ledger observation recorded deployment `62` as `Completed`,
`Some.Succeeded`, and Current for the same revision.

```text
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS-home?rev=8d6e790c06e6cb316a03b6ce071c3040cc946b85 (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
DeployAccepted.(62 (1451 1451))
```

Post-terminal strict SSH showed a changed profile fingerprint and all of:

```text
desktop-entry=present
Exec=claude-desktop %U
MimeType=x-scheme-handler/claude
x-scheme-handler/claude=claude-desktop.desktop;
default=claude-desktop.desktop
```

No manual Home Manager switch, retry, rollback, reboot, garbage collection,
or OAuth interaction occurred.

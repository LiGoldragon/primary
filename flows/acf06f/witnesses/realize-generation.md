# CriomOS Home realization generation witness

## Method

I read the required non-management, subflow, operating-system, Nix, Lojix,
secrets, evidence, coordination, and file-editing instructions; the current
flow log and its written-psyche record; and the established Lojix deployment
boundary witnesses. I then performed read-only source, proposal, host-key, and
ordinary-socket checks before submitting exactly one owner-socket request.

The source preflight established that GitHub and the local CriomOS `main`
bookmark both identify
`f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`. The proposal path
`/git/github.com/LiGoldragon/goldragon/proposal.datom` is absolute, regular,
and not a symlink. `CheckHostKeyMaterial` returned
`KeyMaterialChecked.(ouranos [] (4976 4976))` for `goldragon/ouranos` and that
proposal. The separately queried node ledger identified the same logical node;
the explicit transport was therefore used verbatim:

```text
(ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome)
```

The previous user-environment record (`190`) has the daemon's
`UserEnvironment.ActivateNow` shape and output family. Earlier successful
canonical proposal witnesses establish the accepted immutable source syntax
`github:LiGoldragon/CriomOS?rev=<40-hex>` and selector
`(homeConfigurations.li.activationPackage)`; slash-revision syntax is recorded
as malformed.

The sole state-changing request was:

```text
Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359 (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable None [])
```

It used `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock` and `meta-lojix`. No
`ActivateNow`, host deployment, `Direct` input, wrapper/file request, builder,
or extra substituter was used. I observed it only through repeated
`LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix
'Query.ByDeployment.(191)'` queries.

## Typed states

Admission is `DeployAccepted.(191 (4977 4977))`; admission alone did not prove
realization. The first three ordinary queries recorded `Building`. The terminal
ordinary query and `Query.ByGeneration.(191)` each recorded:

```text
Queried.([] [(191 191 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359) Some.(4977 4977) Completed Some.(4993 4993) Some.Succeeded)] (4997 4997))
```

Thus deployment and generation `191` are terminally `Completed` /
`Succeeded`; this is Lojix realization state, not activation evidence.

The post-terminal `Query.ByNode.(goldragon ouranos None)` separately retains
user-environment deployment `189` as the Lojix `Current` activation record;
deployment `190` remains terminally failed at activation, and `191` is the
completed profile-only realization. The observed live profile links resolve to
`/nix/store/b1bwfma32f037fsnhpx3n6s2skwbpx6r-profile` and
`/nix/store/m09spn0qw2xsarggbdqyn2m8ycc78c29-home-manager-generation`, not a
newly activated `191` profile. No live-profile, service, microphone, or source
mutation was performed by this witness.

## Sources

- `/home/li/primary/flows/acf06f/log.md`
- `/home/li/primary/flows/acf06f/vision/wisprInteraction.md`
- `/home/li/primary/flows/4ad49f/witnesses/deployment-boundary.md`
- `/home/li/primary/flows/4ad49f/witnesses/live-stock-desktop.md`
- GitHub API commit probe for `LiGoldragon/CriomOS` revision `f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`
- Fresh `meta-lojix` and ordinary `lojix` typed replies recorded above

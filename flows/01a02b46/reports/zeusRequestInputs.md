# Zeus request inputs

The exact mechanical request values for a `goldragon/zeus` complete-host
deployment are:

| Field | Exact value | Evidence status |
| --- | --- | --- |
| builder | `Some.@/etc/nix/machines` (Prometheus: `ssh-ng://nix-ssh@prometheus.goldragon.criome`) | witnessed configuration and successful deployment shape |
| Nix system | `x86_64-linux` | witnessed Nix configuration and Zeus proposal |
| extra substituters | `[]` | successful durable deployment shape; global Nix substituters remain daemon configuration |
| proposal source | `/git/github.com/LiGoldragon/goldragon/datom.dotos` | witnessed current setup variable and regular-file check |
| composition | `CompleteHost` | host system deployment contract |
| input mode | `Horizon` | successful durable deployment shape and proposal materializer |
| selector | `(nixosConfigurations.target.config.system.build.toplevel)` | current CriomOS output |
| backend | `NixosSystemdBootV1` | Zeus NixOS/systemd-boot target |
| source policy | `RequireImmutable` | successful production deployment shape |
| transport | `(ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome)` | dual-route strict-SSH witness |

The current CriomOS main revision is `d04f6dafce19b7b4f093c35716739f36d75973ba`,
and Ouranos deployment 27 completed using that immutable revision. Selecting
that revision for Zeus remains caller-owned authority; it is the only unresolved
value below and is marked `<approved-CriomOS-flake>` in the templates.

## Exact typed templates

These are owner-socket requests. They are templates, not submissions. Replace
only `<approved-CriomOS-flake>` with one caller-approved immutable flake
reference such as the current candidate above.

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos <approved-CriomOS-flake> (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 Evaluate RequireImmutable Some.@/etc/nix/machines [])'
```

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos <approved-CriomOS-flake> (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 Realize RequireImmutable Some.@/etc/nix/machines [])'
```

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos <approved-CriomOS-flake> (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 TestActivation RequireImmutable Some.@/etc/nix/machines [])'
```

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos <approved-CriomOS-flake> (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

`<approved-CriomOS-flake>` is intentionally not valid Dotos until replaced by
the approved `github:LiGoldragon/CriomOS?rev=<40-hex-revision>` string. No other
field is unresolved. `meta-lojix` admission is not completion; observe the
returned deployment identifier through ordinary `lojix` until a terminal
record, and keep controller generation state separate from target profile
state.

## Staged requests and artifact reuse

Evaluate, Realize, TestActivation, and ActivateNow are not phases addressed by
one shared deployment handle. Each submitted request is a separate durable
deployment and generation. Evaluate only evaluates; Realize evaluates and
realizes; TestActivation and ActivateNow evaluate, realize, copy, and activate.
Lojix does not pass one stage's closure path into the next stage. Nix may reuse
the same store path through its local store or configured substitutes when the
inputs are identical, but each stage still receives a new deployment identity
and produces its own terminal record.

No request was constructed or submitted by this flow.

## Sources

- `flows/01a02b6a/witnesses/nixConfiguration.md`
- `flows/01a02b6a/witnesses/requestValues.md`
- `flows/01a02b6a/witnesses/stagedSemantics.md`
- `/home/li/primary/SKILL_VARIABLES.md`
- `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
- `/git/github.com/LiGoldragon/lojix/src/lib.rs`

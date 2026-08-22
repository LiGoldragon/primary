# Zeus request values

Method: read `/home/li/primary/SKILL_VARIABLES.md`,
`/git/github.com/LiGoldragon/Curriculum/skills/lojix.md`,
`/git/github.com/LiGoldragon/CriomOS/flake.nix`,
`/git/github.com/LiGoldragon/CriomOS/flake.lock`,
`/git/github.com/LiGoldragon/goldragon/datom.dotos`, and the durable query and
command evidence in `flows/01a01bac` and the canonical deployment transcript.

Observed and settled mechanically:

- Cluster/node: `goldragon` / `zeus`.
- Proposal source: `/git/github.com/LiGoldragon/goldragon/datom.dotos`; `stat`
  identifies it as an absolute regular non-symlink file.
- Host composition: `CompleteHost`. CriomOS's public host output is
  `nixosConfigurations.target`; the complete-host path is the system toplevel.
- Input mode: `Horizon`. The proposal is materialized into Horizon/system/
  deployment/secrets inputs before evaluation.
- Host selector: `(nixosConfigurations.target.config.system.build.toplevel)`.
- NixOS backend: `NixosSystemdBootV1`.
- Source policy: `RequireImmutable`.
- Remote builder field: `Some.@/etc/nix/machines`.
- Extra substituters: `[]`.
- Deployment transport, encoded as the required positional product, is
  `(ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome)`: direct IP for
  Nix closure transfer and DNS destination for activation. Both endpoints were
  independently strict-SSH witnessed as the same Zeus host in
  `flows/7a9f4c12`.
- Current CriomOS main is `d04f6dafce19b7b4f093c35716739f36d75973ba`; successful
  durable Ouranos deployment 27 used the same immutable revision and completed
  with the same Horizon/selector/backend/builder/extra-vector shape. That is a
  current source candidate, not caller approval to deploy Zeus.

The only unresolved request field is therefore the authority choice of the
immutable CriomOS flake revision. The current candidate is:

```text
github:LiGoldragon/CriomOS?rev=d04f6dafce19b7b4f093c35716739f36d75973ba
```

This report does not choose that candidate for a Zeus mutation.

## Sources

- `/home/li/primary/SKILL_VARIABLES.md` — current setup variables
- `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md` — authored field order
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:254-283` — output selectors
- `/git/github.com/LiGoldragon/CriomOS/flake.lock` — pinned CriomOS-home/Lojix
- `/git/github.com/LiGoldragon/goldragon/datom.dotos` — cluster proposal
- `flows/01a01bac/witnesses/userEnvironmentDeployment.md` — successful durable deployment 27
- `flows/7a9f4c12/reports/zeusDualRoutePreflight.md` — exact Zeus transport evidence
- `flows/01a02b6a/witnesses/nixConfiguration.md` — current builder/substituter witness
- `flows/01a02b6a` — this flow

# Direct Datom consumer witness

The owned direct migrations use current datom-codec and Protos instead of the
legacy datomic family. Each source was migrated in an isolated locked workspace,
committed and pushed before its declarative owner changed.

| Source | Published revision | Durable checks |
| --- | --- | --- |
| Claude Answers | `3a14cb12f885932de35a7ef7793e8a99a796c67f` | Typed Datom queries and generated schema; remote Nix tests, format, clippy, and package build. |
| Curriculum deploy | `7cc3cb53a10ab6ada383ea647c1ac87d1409266d` | Typed role/inventory roots; remote Nix test, format, clippy, package, and configured Curriculum fixture checks. |

CriomOS-home owns the Claude Answers declarative reference. Primary’s flake is
the actual Curriculum deploy owner and ran `check-skills` with configured
Curriculum inputs; no synthetic operating-system input was added. The direct
manifests and their effective lock closures resolve current datom-codec
`41a3c073d5c5cdcb3ebb1a5c842e8c068145fdb2` and current Protos
`2d999f173334`.

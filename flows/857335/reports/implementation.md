# Implementation

Protos 0.27.0 is landed on `main` at `9b54a72f0a0c`. It replaces the
parallel situation tree with extent-bearing `Protos` nodes, parses the
approved structural and opaque delimiters, and prints canonical text.

Datom and Ethos Zero are in active integration. Datom's replacement core and
derive package exist in the working copy, but its policy gate and scalar
headed-run semantics remain unfinished. Ethos Zero has migrated its generator
shape but awaits the final Datom pin before its compilation and generated
outputs can be witnessed.

Consumer locks 991 through 1000 cover the independently editable consumers.
Lojix is not editable: Lock 990, owned by flow `f7941a`, overlaps its source
and integration-test paths: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
and `/git/github.com/LiGoldragon/lojix/tests/deploy_transport_integration.rs`.

Consumer inspection shows these are source migrations, not manifest-only
repins. Orchestrate and curriculum-deploy include generated tuple types and
the superseded Datomic/Corporal chain. Claude-answers uses an older, separate
Datomic surface. The signal repositories use still older Protos Input/Output
and Realize vocabulary. Their final migration therefore depends on the new
Ethos-generated contracts, rather than a mechanical revision replacement.

## Sources

- `/home/li/primary/Vision/protos.md`
- `/home/li/primary/Vision/datom.md`
- `/home/li/primary/Vision/ethos.md`
- `/home/li/primary/flows/564f55/reports/landing.md`
- Remote Nix witnesses from `/git/github.com/LiGoldragon/protos`

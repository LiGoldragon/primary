# Implementation

## Ethos Zero migration

Ethos Zero now pins Datom at `f0aeeaa8ea8bdbbd0b9d7b96a35e9e3b3e4a9452`
and Protos at `1bf659e5489cf1ac05cc293ee2e8068774fb48bd`.  The latter preserves
the four Protos variants and represents a qualified headed form with optional
angled constraints on `Headed`; bare type applications remain adjacent bare
and angled structures for Ethos to consume conceptually.

The authored contract and fixtures have begun the required `Text` to `String`
transition. The next conceptual model is `Library { imports, types, kinds,
associations }`, with `Signal` retaining its query, response and type sections.
The inherited `Types`/`Kinds`, `Delineation`, `Protoform`, and `Situated`
implementations are obsolete and are being replaced rather than bridged.

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

## Current witness

Ethos now pins Protos `5fc62050d92728ad254d722f21ffed8dd27f357b` and
Datom `a352a4331194066918c38196305602d6a90774ff`; Cargo and the flake lock
resolve those public revisions. The generated CLI contract uses `Query` and
`Response`, imports Datom's typed `Error`, and keeps a separate typed
`Generation_Error` for the Ethos layer. `cargo check --bin ethos-zero` passed
after regeneration.

The current five library behavior tests pass. The fixture regeneration test
first failed on nested inline enums, then on comments before a sweet root, and
then on retired qualified import punctuation. The reader now consumes attached
angle forms in variants as well as declarations, canonicalization finds the
first non-comment root, and all fixture products were regenerated through the
library. The remaining all-target failures are the legacy generated integration
test harness, which still imports retired Protos/Datom APIs and asserts tuple
layouts.

The former ascent was a placeholder that discarded all Library children and
published zero extents. It is now a full structural projection with computed
extents, witnessed by a nonempty Library/Signal round-trip. Position and
capability references now project adjacent Bare plus Angled sequences,
including nested Vector/Option/Result. Alias and source-qualified generic
references now use their parent-list sequence projection as well; the witness
covers `SyntaxError.Vector<FilePath>`, an imported `external:Vector<FilePath>`,
and grouped kind identity constraints.

Retired `Types` and `Kinds` roots are removed from the public File/Root model,
reader, checking, generation, and ascent. Sema now carries exactly its two
specified sections: imports and bracketed record-type declarations; a behavior
test witnesses Sema ascent and rejects both retired roots. Nexus is not added:
the layout beyond its stated imports/input/output remains unspecified.

## Sources

The governing Vision and Intent were inlined verbatim in the user's dispatch;
the filesystem copies below are cited as matching locations, not as the
authority used for implementation.

- `/home/li/primary/Vision/protos.md`
- `/home/li/primary/Vision/datom.md`
- `/home/li/primary/Vision/ethos.md`
- `/home/li/primary/flows/564f55/reports/landing.md`
- Remote Nix witnesses from `/git/github.com/LiGoldragon/protos`

## Depth-safety coordination

On 2026-09-10, the historic lock 987 was absent from the live Orchestrate
snapshot. Reacquisition was initially refused because lock 1008, owned by this
same flow, overlapped Datom's source set. With the main flow's authorization,
1008 was released and the fresh whole-repository lock 1020 was granted for
`/git/github.com/LiGoldragon/datom-codec` and
`/git/github.com/LiGoldragon/protos`. It is the active reservation for the
final Protos and Datom depth-safety repair.

Protos `0.28.1`, commit `d038d20730dc5bfad32119477be3bc8778d5ca5f`, is on
main. It removes the uncompiled pre-Protos modules, installs iterative tree
destruction, and has actual 100,000-node print-and-drop witnesses; no deep
output tree is forgotten. Its configured remote Nix gate passed.

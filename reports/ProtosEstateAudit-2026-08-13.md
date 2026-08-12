# Protos estate audit — 2026-08-13

## Scope and method

This report's initial snapshot audits the 175 physical Git checkouts directly
under `/git/github.com/LiGoldragon` on 2026-08-13. They represent 171
canonical GitHub remote identities: `CriomOS-home-spirit-main-f53aacdd` is a
second worktree of `CriomOS-home`; `core-schema` redirects to `core-ethos`,
`nota` redirects to `dotos`, and `textual-rust` redirects to `rust-logos`.
Every physical path remains in the table, but aliases are not counted as
separate canonical remotes. This is the complete initial checkout estate,
rather than the smaller and stale inventory in
`protocols/repos-manifest.dotos`.

Evidence was taken from each checkout's origin, current HEAD, `Cargo.toml` and
`flake.nix` presence, entry documents, source outlines, and direct Cargo
dependency scan. The audit also reviewed the earlier physical-state report
`reports/ThreeStacksCurrentState-2026-08-10.md`; it is useful historical
measurement, not present authority. No build or deployment is asserted merely
from a manifest edge.

The classification deliberately separates a component's *destination* from
what its present checkout implements. “Component, legacy-wired” means a
component or component contract that may belong to the correct-new destination
but currently has a direct Cargo edge to `nota`, `schema`, or `dotos`; it is
not classified as a correct-new implementation. “Component-associated, no
direct notation edge observed” is similarly not positive evidence of
correct-new implementation.

## Governing statements

- Intent: Protos parsing is a contextual, two-way structural walk; a met shape
  selects a type context, and the parent resumes at its saved position.
  `psyche/Intent/protosParsing.md`, approved 2026-08-13.
- Datom carries strictly typed data only, not generics or Rust generation.
  It uses curly quotes for legacy text, parentheses for the Meaning delimiter,
  and `Map.[…]`; Meaning's full shape and vocabulary remain open.
- Protos is the shared style; its shared contextual parsing machinery belongs
  in `protos`. The implementation has distinct discrimination, per-type
  context, and shared walk-driver planes. Trait names, read/write split,
  Meaning shape, and canonicality placement remain open.
- The old Schema + NOTA estate remains legacy. The incorrect new estate is
  frozen reference, not a dependency source. New work moves forward to Datom;
  Ethos generates committed Rust; Ethos and Datom are different languages that
  may share a substrate, not a parser.
- A component is a daemon speaking Signal with its own Sema store and ordinary
  and meta signal surfaces. The future psyche component contains its Ethos
  source; `spirit-ethos` was ruled an erroneous separate repository.

## Observations

### Correct-new witnesses

`datom` at `3c5c6f2` is a Rust crate for text serialization/deserialization.
It has `Document`/`Block` parser-tree types and `DatomEncode`/`DatomDecode`
traits. Its README still documents pipe text, parenthesized ordinary strings,
and `Map.(…)`; those are direct evidence of the stale rename-port, not the
ruled Datom surface.

`ethos-rust` at `62f098c` is an active emission-boundary scaffold. It defines
`ComponentGeneration`, `GeneratedComponent`, and the three artifact paths
`signal.rs`, `nexus.rs`, and `sema.rs`; its implementation expressly says the
actual generator is a later phase. It has no dependency on frozen repositories.

`protos` at `d06c4a9` is currently a small implementation-free Cargo contract
package. It has `capsule.rs`, `population.rs`, `textual_capsule.rs`,
`interface.rs`, and `wire_identity.rs`; its only dependencies are
`content-identity`, `rkyv`, and `signal-frame`. It owns generic Capsule,
EncodedPopulation, TextualCapsuleAssociation, and a closed six-family numeric
`ContractId`/`WireRevision` registry. Its own README and ARCHITECTURE state it
has no parser, printer, evaluator, structural parsing, component engine,
name-table, or language-specific data. This is an exact present inventory, not
a conclusion about what further material must remain there.

### Dependency evidence

The direct Cargo source scan finds 20 checkouts pinning `nota`, 67 pinning
`schema`, and more than 100 pinning `dotos`; only `datom` pins `datom`, and
only `ethos-rust` pins `ethos-rust`. The component estate is therefore not
evidence of correct-new generated-source adoption. The frozen-reference roster
has no newest commit after the 2026-08-10 freeze ruling in this snapshot.

`protocols/repos-manifest.dotos` calls itself authoritative but still lists
`schema-next` and `schema-rust-next` as active, despite the explicit ruling
that those names are relics. It omits checked-out `datom`, `ethos-rust`, and
`protos`, among other physical estate entries.

## Exact checkout-path mapping

The following is the marking-agent input. Every physically checked-out path is
listed exactly once. Status describes current evidence, never an inferred
authority to rename, remove, or rewire a repository.

| Checkout path | Stack / current status |
| --- | --- |
| `/git/github.com/LiGoldragon/ArtificialIntelligence` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/BookOfGoldragon` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/BookOfLuna` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/CriomOS` | Out of Protos implementation scope: operating-system source |
| `/git/github.com/LiGoldragon/CriomOS-emacs` | Out of Protos implementation scope: operating-system source |
| `/git/github.com/LiGoldragon/CriomOS-home` | Out of Protos implementation scope: operating-system source |
| `/git/github.com/LiGoldragon/CriomOS-home-spirit-main-f53aacdd` | Duplicate worktree of CriomOS-home; not a separate repository |
| `/git/github.com/LiGoldragon/CriomOS-lib` | Out of Protos implementation scope: operating-system library |
| `/git/github.com/LiGoldragon/CriomOS-pkgs` | Out of Protos implementation scope: package source |
| `/git/github.com/LiGoldragon/CriomOS-test-cluster` | Out of Protos implementation scope: operating-system test environment |
| `/git/github.com/LiGoldragon/TheBookOfSol` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/agent` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/aggregator` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/arca` | Out of Protos implementation scope: general tooling |
| `/git/github.com/LiGoldragon/brightness-ctl` | Out of Protos implementation scope: device tool |
| `/git/github.com/LiGoldragon/caraka-samhita` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/chroma` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/chronos` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/claude-answers` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/clavifaber` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/cloud` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/content-identity` | Incorrect-new frozen reference: shared identity substrate |
| `/git/github.com/LiGoldragon/core-ethos` | Incorrect-new frozen reference: in-process Ethos core |
| `/git/github.com/LiGoldragon/core-logos` | Incorrect-new frozen reference: WholeLogos core |
| `/git/github.com/LiGoldragon/core-nomos` | Incorrect-new frozen reference: lowering core |
| `/git/github.com/LiGoldragon/core-schema` | Canonical alias of `core-ethos`; shared remote is incorrect-new frozen reference: in-process Ethos core |
| `/git/github.com/LiGoldragon/criome` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/criomos-horizon-config` | Out of Protos implementation scope: operating-system data |
| `/git/github.com/LiGoldragon/datom` | Correct-new active: provisional Datom codec; divergence primary-xqb.8.1 |
| `/git/github.com/LiGoldragon/domain-criome` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/dotos` | Incorrect-new frozen reference: old successor text parser/codec |
| `/git/github.com/LiGoldragon/dotos-config` | Incorrect-new frozen reference: Dotos configuration adapter |
| `/git/github.com/LiGoldragon/dotos-text-query` | Incorrect-new frozen reference: Dotos query utility |
| `/git/github.com/LiGoldragon/ethos-engine` | Incorrect-new frozen reference: central-storage daemon embryo |
| `/git/github.com/LiGoldragon/ethos-rust` | Correct-new active: Ethos-to-Rust emission-boundary scaffold |
| `/git/github.com/LiGoldragon/forge` | Out of Protos implementation scope: general tooling |
| `/git/github.com/LiGoldragon/golden-bridge` | Incorrect-new frozen reference: migration bridge |
| `/git/github.com/LiGoldragon/goldragon` | Out of Protos implementation scope: data |
| `/git/github.com/LiGoldragon/harness` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/hexis` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/horizon-rs` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/introspect` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/judge` | Out of Protos implementation scope: general tooling |
| `/git/github.com/LiGoldragon/kameo` | Out of Protos implementation scope: upstream fork |
| `/git/github.com/LiGoldragon/kameo-testing` | Out of Protos implementation scope: upstream test utility |
| `/git/github.com/LiGoldragon/kibord` | Out of Protos implementation scope: keyboard configuration |
| `/git/github.com/LiGoldragon/language-engine-witness` | Incorrect-new frozen reference: language witness |
| `/git/github.com/LiGoldragon/library` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/listener` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/logos-engine` | Incorrect-new frozen reference: central-storage daemon embryo |
| `/git/github.com/LiGoldragon/logos-runtime` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/lojix` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/lore` | Out of Protos implementation scope: content |
| `/git/github.com/LiGoldragon/mentci` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/mentci-egui` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/mentci-lib` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/message` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-agent` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-aggregator` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-cloud` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-criome` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-domain-criome` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-harness` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-introspect` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-listener` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-lojix` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-mentci` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-mentci-client` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-message` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-mind` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-mirror` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-orchestrate` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-persona` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-repository-ledger` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-router` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-spirit` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-system` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-terminal` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-upgrade` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/meta-signal-version-handover` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/mind` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/mind-judge` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/mind-judge-config` | Component-associated configuration; no direct notation edge observed |
| `/git/github.com/LiGoldragon/mind-tests` | Component-associated tests; no direct notation edge observed |
| `/git/github.com/LiGoldragon/mirror` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/name-table` | Incorrect-new frozen reference: naming substrate |
| `/git/github.com/LiGoldragon/nomos-engine` | Incorrect-new frozen reference: in-process assembly library |
| `/git/github.com/LiGoldragon/nomos-types` | Incorrect-new frozen reference: stream schemas |
| `/git/github.com/LiGoldragon/nota` | Canonical alias of `dotos`; shared remote is incorrect-new frozen reference: old successor text parser/codec. Legacy NOTA survives as historical stack/consumer vocabulary, not a separate current canonical remote. |
| `/git/github.com/LiGoldragon/orchestrate` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/orchestrator-judge` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/orchestrator-judge-config` | Component-associated configuration; no direct notation edge observed |
| `/git/github.com/LiGoldragon/persona` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/persona-spirit` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/pi-intercom` | Out of Protos implementation scope: intercom tool |
| `/git/github.com/LiGoldragon/pi-session-namer` | Out of Protos implementation scope: session tool |
| `/git/github.com/LiGoldragon/pi-subagents` | Out of Protos implementation scope: agent tool |
| `/git/github.com/LiGoldragon/pi-subagents-nicobailon` | Out of Protos implementation scope: agent tool worktree |
| `/git/github.com/LiGoldragon/protos` | Correct-new active, current contracts-only role; divergences primary-xqb.8.9 and .10 |
| `/git/github.com/LiGoldragon/protos-engine` | Incorrect-new frozen reference: integration/conformance orchestration |
| `/git/github.com/LiGoldragon/qmkBinaries` | Out of Protos implementation scope: firmware asset |
| `/git/github.com/LiGoldragon/raw-discovery` | Incorrect-new frozen reference: structural discovery substrate |
| `/git/github.com/LiGoldragon/relative-age-display` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/release-train-dogfood` | Incorrect-new frozen reference: release-train witness |
| `/git/github.com/LiGoldragon/rename-propagator` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/repository-ledger` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/router` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/rust-build` | Out of Protos implementation scope: Rust build tooling |
| `/git/github.com/LiGoldragon/rust-logos` | Incorrect-new frozen reference: Rust textual emitter |
| `/git/github.com/LiGoldragon/schema` | Legacy Schema + NOTA production/reference |
| `/git/github.com/LiGoldragon/schema-language` | Legacy Schema + NOTA production/reference |
| `/git/github.com/LiGoldragon/schema-rust` | Legacy Schema + NOTA production/reference emission boundary |
| `/git/github.com/LiGoldragon/sema` | Component-associated daemon; no direct notation edge observed |
| `/git/github.com/LiGoldragon/sema-engine` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/sema-storage` | Incorrect-new frozen reference: central storage topology |
| `/git/github.com/LiGoldragon/sema-translator` | Incorrect-new frozen reference: in-memory naming authority |
| `/git/github.com/LiGoldragon/signal` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-agent` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-aggregator` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-cloud` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-criome` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-derive` | Component-support contract; no direct notation edge observed |
| `/git/github.com/LiGoldragon/signal-domain` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-domain-criome` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-ethos` | Incorrect-new frozen reference: old Ethos vocabulary |
| `/git/github.com/LiGoldragon/signal-forge` | Component contract; no direct notation edge observed |
| `/git/github.com/LiGoldragon/signal-frame` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-harness` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-introspect` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-listener` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-logos` | Incorrect-new frozen reference: old Logos vocabulary |
| `/git/github.com/LiGoldragon/signal-lojix` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-mentci` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-mentci-client` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-message` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-mind` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-mind-judge` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-mirror` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-nomos` | Incorrect-new frozen reference: old Nomos vocabulary |
| `/git/github.com/LiGoldragon/signal-orchestrate` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-orchestrator-judge` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-orchestrator-message` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-persona` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-repository-ledger` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-router` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-sema` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-sema-storage` | Incorrect-new frozen reference: central-storage vocabulary |
| `/git/github.com/LiGoldragon/signal-sema-translator` | Incorrect-new frozen reference: translator vocabulary |
| `/git/github.com/LiGoldragon/signal-spirit` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-spirit-judge` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-standard` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-system` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-terminal` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-upgrade` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/signal-version-handover` | Component contract, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/skills` | Protos-adjacent agent tooling, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/spirit` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/spirit-ethos` | Incorrect-new frozen reference; separate source divergence primary-xqb.8.12 |
| `/git/github.com/LiGoldragon/spirit-judge` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/spirit-judge-config` | Component-associated configuration; no direct notation edge observed |
| `/git/github.com/LiGoldragon/standards` | Out of Protos implementation scope: domain standards |
| `/git/github.com/LiGoldragon/structural-codec` | Incorrect-new frozen reference: structural evaluator |
| `/git/github.com/LiGoldragon/structural-codec-derive` | Incorrect-new frozen reference: generated codec experiment |
| `/git/github.com/LiGoldragon/substack-cli` | Out of Protos implementation scope: standalone CLI |
| `/git/github.com/LiGoldragon/synchronizer` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/system` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/terminal` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/terminal-cell` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/textual-rust` | Canonical alias of `rust-logos`; shared remote is incorrect-new frozen reference: Rust textual emitter |
| `/git/github.com/LiGoldragon/tree-sitter-dotos` | Incorrect-new frozen reference: editor grammar, not Datom parser |
| `/git/github.com/LiGoldragon/tree-sitter-ethos` | Incorrect-new frozen reference: editor grammar |
| `/git/github.com/LiGoldragon/triad-runtime` | Out of Protos implementation scope: generic runtime (legacy-wired) |
| `/git/github.com/LiGoldragon/upgrade` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/version-projection` | Component, legacy-wired current checkout |
| `/git/github.com/LiGoldragon/whisrs` | Out of Protos implementation scope: upstream fork |

## Evidence-backed divergences and tracker mapping

| Divergence | Evidence and governing statement | Tracker outcome |
| --- | --- | --- |
| Datom is a stale port rather than the ruled contextual codec. | Its README documents pipe text, ordinary parenthesized strings and `Map.(…)`; source builds an intermediate `Document`/`Block` tree. Intent requires contextual direct typed structural transcoding; Vision rules curly-quote legacy strings, Meaning parentheses, `Map.[…]`, and no pipe strings. | Existing `primary-xqb.8.1` (linked discovered-from this audit) |
| The authoritative repository manifest presents a false estate. | It retains active `schema-next`/`schema-rust-next`, omits actual correct-new checkouts, and does not cover the audit's physical estate. ThreeStacks explicitly rules the `-next` names relics. | New `primary-xqb.8.8` |
| Protos excludes the very shared structural parsing mechanism that Vision locates there. | README/ARCHITECTURE say “no parser/printer/evaluator/structural parsing”; current source contains contracts only. Vision says shared context switching belongs in Protos; Intent now fixes the parsing principle. | New `primary-xqb.8.9` |
| Protos actively owns a superseded numeric signal registry. | `WireContractFamily` allocates ContractId/WireRevision 1–6; the 2026-08-11 ruling supersedes that scheme with the universal signal enum plus handshake surface. | New `primary-xqb.8.10`, blocked by `primary-xqb.8.3` |
| Production components retain legacy/frozen notation dependencies. | Direct Cargo scan: 20 Nota, 67 Schema, and 100+ Dotos consumers; Datom and Ethos-rust have no consumers outside themselves. Vision says migrate everything forward to Datom and frozen repos are reference-only. | New `primary-xqb.8.11` |
| `spirit-ethos` remains a standalone active-source shape after the psyche-component ruling. | Its README calls it canonical authored Ethos roots; ThreeStacks states that it should not have existed and the source belongs in the psyche component. | New `primary-xqb.8.12`, blocked by `primary-xqb.8.4` |
| Repositories lack visible stack/status entry markings. | The path mapping above is the first estate-wide mapping; entry documents do not uniformly state legacy/frozen/correct-new status. | Existing `primary-xqb.8.7` (linked discovered-from this audit) |

Each row is exactly one tracker outcome. No finding is created for an open
design fork, a missing future repository whose name is unruled, or an editor
grammar that is not the Datom parser.

## Unknowns and non-findings

- Protos's final remainder is intentionally unknown. This audit does not decide
  whether its current Capsule or population contracts stay, move, or retire;
  nor does it decide trait names, Meaning anatomy, canonicality tiers, or the
  one-trait/pair question.
- The universal signal repository's name and exact enum schema are unruled.
  No repository is proposed or named here.
- The Meaning shape and annotation vocabulary are open under
  `primary-xqb.8.5`; this audit does not touch that decision bead.
- No direct Cargo edge proves a runtime path or durable-state ownership. The
  current component mappings are source-dependency evidence, not deployment
  claims.
- Tree-sitter grammars are editor grammars. Their existence is not treated as a
  second Datom parser without evidence that they implement Datom decoding.
- `schema-next`, `schema-rust-next`, `tree-sitter-schema`, `nexus`, and
  `nexus-cli` appear in the manifest but are not among the 175 checkouts; this
  report records the discrepancy and does not infer deletion, creation, or
  remote state.

## Validation witnesses

- Initial checkout inventory: `find /git/github.com/LiGoldragon -mindepth 1
  -maxdepth 1 -type d` followed by per-directory `.git`/origin/HEAD
  inspection: 175 physical checkouts, 171 canonical remote identities (one
  duplicate worktree and three redirect aliases).
- Mapping coverage: compare the 175 inventory basenames with the first column
  of the table above; every basename occurs once.
- Dependency witness: scan every `Cargo.toml` for direct
  `github.com/LiGoldragon/{nota,schema,dotos,datom,ethos-rust}` sources.
- History witness: inspect `git log -1` for each frozen-reference repository;
  no listed frozen repo has a newest commit after 2026-08-10 in the snapshot.

## Current-directory reconciliation

The later current inventory contains 219 top-level directories: the 175
initial physical paths, 42 Jujutsu integration/workflow worktrees, and two
non-repository report directories. The 42 worktrees are not new canonical
repositories and the two report directories have neither `.git` nor `.jj`.
No repository was removed or inferred from this reconciliation.

The 42 integration/workflow worktrees are:
`CriomOS-home-laptop-colemak-merge`, `CriomOS-home-listener-criome-recovery`,
`CriomOS-home-listener-zddv4`, `CriomOS-home-spirit-domain-all`,
`CriomOS-listener-criome-recovery`, `CriomOS-spirit-domain-all`,
`CriomOS-spirit-judge-deploy`, `CriomOS-test-cluster-spirit-domain-all`,
`lojix-inspect-store`, `mentci-current-graph-integration`,
`mentci-dependency-cascade`, `mentci-lib-cargo-migration`,
`mentci-lib-mentci-signal-family-migration`,
`meta-signal-criome-cargo-source-repair`,
`meta-signal-criome-mentci-contract-migration`,
`meta-signal-mentci-cargo-source-repair`,
`meta-signal-mentci-client-cargo-source-repair`,
`meta-signal-mentci-client-mentci-signal-family-migration`,
`meta-signal-mentci-mentci-signal-family-migration`,
`meta-signal-mind-mind-judge-diagnostic`,
`meta-signal-orchestrate-session-lane-clear`,
`meta-signal-spirit-schema-dotted-syntax-pilot`, `mind-domain-all-repin`,
`orchestrate-session-lane-storage`, `orchestrate-writer-ordering`,
`pi-subagents-nested-roles-preference-training`,
`pi-subagents-nicobailon-closeout`,
`pi-subagents-nicobailon-optional-list-consistency`,
`schema-structural-pipe-retirement`, `signal-criome-cargo-source-repair`,
`signal-criome-mentci-contract-migration`,
`signal-domain-schema-dotted-syntax-pilot`, `signal-mentci-cargo-source-repair`,
`signal-mentci-mentci-signal-family-migration`,
`signal-message-cargo-source-repair`, `signal-persona-cargo-source-repair`,
`signal-router-cargo-source-repair`,
`signal-spirit-schema-dotted-syntax-pilot`,
`signal-terminal-dependency-cascade`, `spirit-judge-hardening`,
`spirit-schema-dotted-syntax-pilot`, and `terminal-cell-dependency-cascade`.

The non-repository report directories are
`persona-role-SchemaTrainExpansion-reports` and
`persona-role-general-code-implementer-reports`.

# Spirit surface-removal downstream audit

Date: 2026-08-03

## Ruling audited

The canonical design ruling is recorded in
`/home/li/primary/design/Spirit/SpiritSurfaceRemoval-2026-08-03.md:15-35`:

- “I want certainty, privacy and referents gone”.
- “just throw the corresponding data out of the migrated database.”

The clean migration preserves each surviving record's identity and substance,
but omits certainty and privacy fields and indexes, deletes every referent row,
index, and alias, and creates no in-database compatibility shadow or archive.
The separately retained pre-migration backup is rollback material, not part of
the migrated database or its compatibility surface.

This is architecture and data-migration matter, not general psyche intent.

## Executive finding

The deployed release predates the ruling. All three removed dimensions remain
structural in the active contract, core daemon, database families, migration,
judge chain, prompt doctrine, manuals, examples, and tests. This is not a small
documentation drift: removing any one surface without the others produces an
unbuildable or semantically split system.

```text
signal-spirit current contract
  Entry + Query + operations
      | certainty / privacy / referents
      v
spirit Nexus -> SEMA -> current database
      |                records + referents + migration count
      v
signal-spirit-judge -> spirit-judge -> spirit-judge-config
      | admission metadata    | referent-registration family
      v                       v
generated agent doctrine, checks, manuals, examples, runtime tests
```

The clean target cuts those edges at the contract root, projects legacy input
records into the smaller current record, and never writes the discarded fields
or registry into the new database.

## Active owning surfaces

| Owner | Evidence | Required disposition |
| --- | --- | --- |
| `signal-spirit` contract | `schema/signal.schema:44-45,66-72,106-108,155-158,167,188-206,226-259` | Remove `ChangeCertainty`, `PrivateRecords`, `RegisterReferent`, their outputs/rejections, the three entry/query dimensions, and all referent registry types. Regenerate derived Rust; do not hand-edit `src/schema/`. |
| `signal-spirit` repository doctrine | `skills.md:24-31,37-49,66-76` | Replace the certainty/privacy lifecycle and query invariants with the smaller entry and explicit lifecycle rules proposed below. |
| `signal-spirit` examples/tests | `examples/canonical.dotos:2-20,28-43`; `tests/generated_contract.rs`, `tests/instance_schema.rs`, `tests/validation.rs` | Rewrite current fixtures to the new positional shape and prove removed heads/types are rejected. Preserve only explicitly versioned historical fixtures. |
| `spirit` SEMA | `schema/sema.schema:27-32,41-46,56-64` | Delete current certainty/referent write variants, `StoredReferent`, `MigratedReferentCount`, and `ReferentsFamily`. The migration marker records surviving-record count only. |
| `spirit` Nexus | `schema/nexus.schema:35-39,50-60,63-74,78-94,103-104`; `src/nexus.rs:20-29,66,261,281-284,297-303,491-599,641-697,907-983,1285-1295,1341-1351,1392-1459` | Remove implied-referent registration, referent guardian routing, certainty mutation, and fallback privacy/certainty synthesis. |
| `spirit` store | `src/store/family_directory.rs:12-45`; `src/store/error.rs:33-40`; `src/store/mod.rs` | Current family directory contains records and migration markers only. Remove current referent validation, canonicalization, registry, and query joins. |
| `spirit` render path | `src/render.rs:14-16,41-49,84-85,172-243,335-336` | Redesign or retire the referent-addressed renderer. It currently requires referents and hard-codes exact-zero privacy and a minimum certainty floor. |
| `spirit` current migration | `src/production_migration.rs:89-114,197,248-373,393-422,2800-2801,2946,3018,3052-3066` | Read the old fields only on the source side; construct current records without them; do not call `import_referent`; do not create a referent family/count. Assert zero removed-dimension storage in the destination. |
| `spirit` active documentation | `ARCHITECTURE.md:59-80,152-159,491-553,581-620,685-715,1001-1018`; `README.md:55-107`; `manual.md:305-366,420-451,490-499` | Rewrite current-shape and lifecycle claims. The existing docs currently teach all three removed concepts as canonical behavior. |
| `signal-spirit-judge` contract | `schema/signal.schema:6-32,46-47`; `src/lib.rs:13-110,210-291`; `skills.md:3,7-8` | Delete the referent-registration judgment family and `UnclearPrivacy`. Admission contains no removed record metadata. Keep diagnostic redaction/content hashing as provider-boundary safety. |
| `spirit-judge` adapter | `src/lib.rs:55-56,193-241,292-435,492-522`; `src/witness.rs:4-72,149`; `ARCHITECTURE.md:1-38` | Remove referent prompt loading, lowering, parsing, and replies. Remove record-field privacy/certainty handling. Keep fail-closed provider handling and redacted diagnostics. |
| `spirit-judge-config` prompts | `ARCHITECTURE.md:18-26`; `prompts/intent-admission/{record-shape,checklist,burden-ladder,justification-shape,rejection-reasons,few-shot}.md`; `prompts/referent-registration/` | Replace the seven-field record doctrine; delete certainty/privacy admission gates and rejection reasons; remove the referent-registration prompt family and manifest entries. Retain testimony, matter-vs-spirit classification, importance, domains/kind, fail-closed parsing, and diagnostic redaction. |
| `meta-signal-spirit` tests | `tests/frame.rs:3-23`; `tests/round_trip.rs:12-61` | Update test construction after the ordinary contract changes. There is no production implementation of the three concepts here. |
| `CriomOS-home` generated-profile check | `checks/pi-harness-profile/default.nix:376-393` | Replace the stale “proposed privacy” approval clauses after their source doctrine changes; exact proposed strings appear below. |
| `CriomOS` cutover doc | `docs/spirit-judge-cutover.md:45-52` | Keep the confidential backup procedure, but replace “record and referent corpus is unchanged” with destination-schema migration evidence: surviving record identities/substance match and the destination has no removed fields or referent family. |

## Historical decoder boundary

Version-pinned source readers such as
`spirit/src/production_migration/v13.rs:543-582,609-617,659-674,696-873`
may have to name and decode the legacy fields long enough to read the old store.
That is source-format knowledge, not compatibility storage. The acceptable
boundary is:

```text
legacy backup/store
  decode old record + old referent family
                |
                | discard certainty, privacy, referents
                v
new record projection -> fresh current database
                         records + migration marker only
```

The legacy reader must not export those dimensions into the current contract,
current record type, migration marker, or destination tables. Frozen versioned
schemas may remain as historical decoder fixtures. They must not be treated as
current examples or generated into the active API.

## Exact owning-skill proposals

No skill was edited. These lines require later explicit psyche approval.

### `signal-spirit/skills.md`

Replace the current `Entry` certainty/privacy bullet at lines 24-31 with:

> `Entry` is one top-level statement without client-provided capture time. It
> carries domains, kind, description, and importance only. Restatement is
> represented by repeated `Entry` records, not nested vectors.
>
> Core Spirit has no certainty, privacy, or referent dimension; none may
> re-enter through operations, queries, migration, or compatibility storage.

Replace the `ChangeCertainty`/exact-zero collection bullets at lines 37-49 and
the certainty/privacy query bullets at lines 66-76 with:

> Lifecycle is expressed through typed record operations; no record field
> doubles as a removal sentinel.
>
> Observation may filter only on dimensions present in the current record
> contract. Historical migration readers may decode removed legacy fields solely
> to discard them; current contracts and migrated databases must not store or
> expose them.

This preserves the current skill's contract ownership, changes the entry and
lifecycle invariants, and removes the legacy dimensions from every active path.

### `signal-spirit-judge/skills.md`

Replace line 3 with:

> Contract-local operation root: `JudgeAdmission`; there is no
> referent-registration judgment family.

Add after it:

> Admission packets and verdicts contain no certainty, privacy, or referent
> metadata. Provider-boundary redaction and content hashing remain operational
> safety, not Spirit record classification.

This removes the obsolete judge family while preserving provider-boundary
confidentiality controls.

### generated workspace Spirit-recording skill

The current source is
`/git/github.com/LiGoldragon/skills/skills/intent-log.md:1-8`; an existing
separate change is expected to rename that capability to `spirit-log`. Whether
applied before or after that rename, add:

> Before capture or mutation, use only psyche-approved record wording and
> scope. Do not synthesize confidence, access-boundary, or named-particular
> metadata.

This preserves the skill's rare-record and owning-surface routing rules while
removing agent invention of the three deleted dimensions.

### `psyche-interraction` source skill

Add after `/git/github.com/LiGoldragon/skills/skills/psyche-interraction.md:20`:

> Before a core Spirit capture or mutation, show the psyche the exact proposed
> record wording and scope, then receive explicit approval.

This preserves approval-gated mutation and replaces the generated doctrine's
obsolete request for a “proposed privacy” value.

After regeneration, update the `CriomOS-home` profile witnesses to expect:

```text
show the psyche the exact proposed core Spirit record wording and scope,
and receive explicit approval.
```

and:

```text
Reject a submission brief unless it evidences that the exact proposed core
Spirit record wording and scope were shown to and explicitly approved by the
psyche. Never invent missing record fields.
```

## Workspace doctrine proposal

This is not a skill edit, but the generated workspace doctrine currently says
“never private or personal substance to public Spirit” at `AGENTS.md:26-28` and
“public Spirit records” at `AGENTS.md:73-74`. Those phrases imply a privacy tier
inside core Spirit. Proposed replacement:

> Capture through core Spirit is the exception, not the reflex: record only
> that unbending directive will. Material requiring an access boundary belongs
> to a separate higher-layer Spirit component in its own environment.

and:

> Private information is closed by default and stays out of public reports,
> core Spirit records, commits, and chat.

The second line is an external handling rule; it does not restore privacy as a
core record field.

## Uses that must not be mass-removed

The word match is broader than the Spirit schema concept. These rules remain:

- `/git/github.com/LiGoldragon/skills/skills/general-instructions.md:5` returns
  unresolved privacy questions to the caller. This is general safety doctrine.
- `/git/github.com/LiGoldragon/skills/skills/repository-lifecycle.md:9-10`
  protects private repositories and visibility. This is publication security.
- `CriomOS/modules/nixos/spirit.nix:195-208,239-243` enforces owner-only files
  and directories. This is operating-system access control.
- `CriomOS/docs/spirit-judge-cutover.md:41-52` keeps provider data out of logs
  and the rollback backup confidential. This is deployment safety.
- `signal-spirit-judge` and `spirit-judge` diagnostic redaction/hash rules protect
  provider-boundary content. They remain even after record `Privacy` disappears.
- Append-only design logs and frozen source-version schemas remain historical
  evidence. They are not current contract claims.

`persona-spirit` also has a separate `Certainty` field
(`skills.md:64-68`, `src/actors/classifier.rs:4-62`). It does not use core
`signal-spirit`'s privacy or referent dimensions. Treat it as a separately owned
domain contract: if it feeds core Spirit, its adapter must project certainty
away; do not mass-edit the independent schema without an explicit boundary
ruling.

## Recommended implementation order

1. Change the active `signal-spirit` schema and regenerate its Rust contract.
2. Change judge contract/config/adapter and core Nexus/SEMA/store together.
3. Make migration project old records to the smaller current shape and prove the
   destination has no removed fields, indexes, aliases, or referent table.
4. Rewrite active manuals, examples, repository skills, generated doctrine, and
   profile checks; retain clearly marked historical decoders and logs.
5. Rebuild every downstream repository and deploy only after backup, rehearsal,
   destination inspection, and rollback evidence.

The indivisible contract cut is the current dilemma: compatibility cannot be
kept inside the migrated database, while all current consumers still require
the legacy dimensions. The safe bridge exists only on the source side of a
one-way migration.

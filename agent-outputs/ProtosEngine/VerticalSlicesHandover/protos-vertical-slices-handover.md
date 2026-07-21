# Protos vertical-slices handover

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

## Focus

Carry the Protos language engine and component-porting work forward as fully audited, fully tested vertical slices that merge progressively into `main` in every affected repository. Do not build another accumulating feature-branch train. A slice is complete only when its source, contracts, storage behavior where applicable, daemon path, and truthful acceptance evidence have landed on `main`.

## Psyche-settled vision

- **EncodedForm is the truth.** It is stringless typed data. Identity, content hashing, wire data, and Nomos transformation use encoded values and encoded identifiers, never embedded names.
- **TextualForm is a two-way pivot and a file index.** A manifest resolves the source-file set. Reading is source files -> TextualForm -> EncodedForm plus NameTree. Emission is EncodedForm plus StructureTree plus NameTree -> TextualForm -> files. One StructureTree drives both directions; it is not an emission-only artifact.
- **Name ownership is separate from encoded structure.** Each component owns one NameTable for its own EncodedForm. A composed table owns one home namespace slice and borrows completed source slices without copying or renumbering. NameTable composition must remain compatible with per-slice tables and namespace slicing; do not reintroduce `extend_from`-style flattening.
- **Nomos is a stringless typed transformer.** It transforms schema encoded values to Logos encoded values. Name lookup, identifier allocation, ordinal-derived Rust field names, and emission literals are at the NameTable/emission boundary, not inside the transform.
- **Identifiers are closed namespace variants carrying `u16` local values.** Equal local values in different variants are distinct. Standard Logos objects have their own namespace. Do not use flat integer identifiers or assume one global table.
- **Signal repositories own encoded-form contracts.** The schema, Logos, and other encoded contract types used by daemons live in the relevant signal contract repositories and are authored through the language pipeline.
- **Protos syntax is strict positional syntax.** It has no field names anywhere. Expected type plus position supplies slot identity. Delimiters retain their settled roles, capitalization is semantic, and typed inner blocks are re-read under their expected type. Do not invent syntax; use codec-emitted, round-tripped artifacts.
- **The shared structural library is the consolidated `protos` repository.** The retired standalone machinery repositories are `content-identity`, `name-table`, `raw-discovery`, `structural-codec`, and `structural-codec-derive`. Consumers must use `protos`, not parallel type universes.
- **The Rust textual-form realization stays split.** `core-logos` owns the encoded Rust value family and `textual-rust` is its Rust textual mouth. Do not move this realization under a Logos source subdirectory.
- **There are no transparent language aliases.** An encoded type has one canonical name. Do not add NameTree-only alias admission, Rust `type` compatibility aliases, or alias lowering. Keep real domain data about alternate referents distinct from language aliases.
- **Working programs are acceptance.** Byte-exact golden comparison is removed. A compiler, daemon, and process test must exercise the generated output on the real path.
- **Lineage B is the only generator.** The path is `core-schema -> core-nomos -> core-logos -> textual-rust`. `schema-language` and `schema-rust` are deprecated and must not receive new rules or compatibility work. Delete them only after every consumer is ported and no consumer remains.

### Settled authoring boundaries

- Dependencies/imports are typed manifest edges, not an in-document imports slot.
- A schema document has the accepted trailing seventh positional slot for the vector of closed streaming relations. The relation carries its opener, acknowledgement, token, event, and close-token references positionally.
- Interface alternatives use one ordered unit-or-one-payload algebra. The payload is optional; wire discriminant remains declaration position.
- Generic actor mechanics belong to shared runtime. The generator projects typed mail and frame adapters, not a general schema-authored implementation-block language.
- Exact lawful authored forms must come from the codec-backed source artifacts named below. The settled data shape does not license memory-authored syntax.

## Settled Nomos macro rule

The closed escape set has exactly two primitives on the `$` base sigil:

- `$x` realizes one typed value at a hole of that value's type.
- `$@xs` splices a typed vector at a vector-element position. It accepts a vector of the element type, flattens exactly one level, and may contribute zero elements.

Splice is statically rejected in fixed-arity records and enum variant payloads. Type passing uses ordinary realization. Name synthesis is not an escape: derived names belong to NameTable/emission, and fresh identity is opaque central allocation. There is no hygiene control, no nested quote level, and no other escape kind. Recursive macro invocation remains a surface form, not an escape primitive. Ill-typed escapes are rejected while checking a macro definition, before expansion.

The macro-definition grammar beyond this closed escape rule is not carried as settled here. Do not invent a macro declaration, input/body, quoting, or recursion spelling; request a codec-backed source-surface ruling if a vertical slice needs one.

## Newest Spirit ruling: privacy through environment isolation

Spirit privacy is achieved through **environment isolation**, not through daemon data or daemon logic. The same privacy-naive Spirit daemon serves one environment and its store. Criome controls which environment a principal may reach. Criome environment representation, cluster identity, quorum behavior, and access-control design are out of scope for this handover; do not invent them in Spirit or in a language-engine slice.

Therefore v14 removes every Spirit privacy field, privacy filter, private/public operation split or prefix, public-record naming assumption, and privacy-specific daemon diagnostic. A daemon exposes the records in its own store; it does not decide whether a record is public or private. This is a settled architectural change, not a request for a compatibility mode.

Certainty is also absent from v14 Spirit domain data. Everything admitted to Spirit is inherently high-certainty. Remove `Certainty` and `ChangeCertainty`; an Entry retains `Importance`, and `BumpImportance` remains. Do not carry a certainty field or operation forward merely to preserve a v13 shape.

Operational confidentiality remains mandatory and is different from the rejected Spirit-domain privacy logic. Agents must keep production snapshots, environment paths, record contents, values, counts, hashes, credentials, sockets, logs, and temporary runtime material out of commits, durable artifacts, and reports. An isolated candidate snapshot is still required before any production migration proof; that operational control does not justify privacy filtering inside the daemon.

## Accepted Spirit v14 design, amended by environment isolation

Spirit v14 is an accepted base redesign, not an implemented or accepted port. The detailed redesign artifact is superseded wherever it assumed privacy or certainty inside Spirit; workers must apply this handover delta rather than implementing those earlier assumptions verbatim.

- Split the daemon into explicit Signal admission, SpiritNexus, SpiritSema, OwnerPolicy, SubscriptionBroker, per-subscription Delivery actors, and effect actors. The ordinary and meta paths stay distinct at their listener and authority boundaries.
- SpiritSema is the sole owner of mutable durable state and the only database writer. Nexus owns decisions and in-flight request state, not a database handle. A committed change is emitted only after successful commit.
- Version 14 retains two authoritative application-record family roles, `IntentRecord` and `ReferentRecord`. Subscription state, runtime policy, migration bookkeeping, stashes, and mail ledgers are not application record families. Their final v14 fields and operations must be authored without the removed privacy and certainty concepts; do not treat the pre-ruling record shape as current.
- Archive is a lifecycle state in the authoritative store. Any separate archive store is a retryable projection and does not determine truth.
- Subscription backpressure closes the affected subscription with a typed failure. Do not silently lose events.
- Generate contracts, record types, typed actor mail, and frame adapters. Put generic actor mechanics in the shared runtime; do not grow a general schema-authored Rust method-body or trait-definition language for Spirit.
- The frozen version-13 reader and isolated consistent snapshot remain the migration mechanism, but the fold is blocked on explicit environment routing: one privacy-tagged v13 store must route into per-environment v14 stores. Inventory and present the actual v13 privacy variants and target environments for psyche authority. Do not infer, design, or implement routing. Once ruled, reject source values that cannot map lawfully. Never raw-copy a live-mutating database.
- Spirit alternate referents are live domain behavior. A canonical referent can have alternate referents that participate in collision checking and query canonicalization. This is persisted and wire-visible domain data, not the rejected Protos language-alias feature.

The detailed accepted base design and its source evidence are in `agent-outputs/ProtosEngine/SpiritSemaRedesign/spirit-sema-daemon-redesign.md`; its privacy and certainty assumptions are amended by the ruling above.

## Directly verified implementation state

All revisions below were read from the current local Jujutsu bookmarks during this handover. They are retained, pushed candidates ahead of each repository's current `main`, not evidence that they have been integrated.

For `protos`, `core-schema`, `core-logos`, `textual-rust`, and `core-nomos`, this handover also ran the full named x86_64-linux Nix check derivations (`build`, `test`, `doc`, `fmt`, and `clippy`) with `nix build ... --no-link --print-build-logs`; each command exited successfully. The command does not establish all-system acceptance.

| Repository | Bookmark or retained state | Exact revision | Direct verification in this handover |
| --- | --- | --- | --- |
| `protos` | `no-alias-migration` | `e9983d6220856a011886145ed0ef0cc41c9bf597` | Full named Nix check derivations passed. Includes the namespaced identifier, composed canonical-only NameTable, manifest/TextualForm work, and removal of transparent aliases. |
| `core-schema` | `NoAliasesProducers` | `cee7f0873c8ccfba0afe09cbb40de531c9e73077` | Full named Nix check derivations passed. Its retained chain includes EncodedForm naming, manifest support, seven-slot document work, interface alternatives, and streaming-relation data. |
| `core-logos` | `NoAliasesProducers` | `7fabf6d42f458963c6b4bf526284ba88087a71c7` | Full named Nix check derivations passed. Its retained chain includes EncodedForm naming, Logos standard identifiers, eager boundary naming, and removal of transparent type-alias items. |
| `textual-rust` | `no-alias-generators` | `89536fe677d45f2624cd5e6e4675fb4314fff309` | Full named Nix check derivations passed. It rejects transparent type aliases while preserving structural newtypes and wrappers. |
| `core-nomos` | `NomosEscapeSet` | `440466e2cefb5f7d589c4ca3f9bde8637f6bede7` | Full named Nix check derivations passed. It is descendant of the canonical no-alias generator revision and implements the closed escape rule. |
| `signal-sema-storage` | `NoAliasesSignalSemaStorage` | `4fa7256fe5bfe6d4d85b3acceb028d3ae529f6ef` | Pushed and observed. It is the current retained storage-contract candidate, but its full Nix check was not repeated during this handover. |
| `signal-nomos` | `NoAliasesSignalNomos` | `e23379576c91b7ce78617a8328301afed5d41c79` | Pushed and observed; Nix was not repeated here. |
| `signal-logos` | `NoAliasesSignalLogos` | `811a85e287efef8472f76a0d810902b0b6e4c21d` | Pushed and observed; Nix was not repeated here. |
| `signal-schema` | retained `noaliasesnomosengine` parent | `5e985cccbb30d87b3d58bbe6c97759c870d0232f` | Pushed and observed; Nix was not repeated here. |
| `sema-storage` | `NoAliasesSemaStorage` | `77e69960b76183b4c2c2a7fa1bf189ef4b3bb3c7` | Pushed and observed; Nix was not repeated here. |
| `schema-engine` | `NoAliasesSchemaEngine` | `37eb6fbb8a1feea0bd4ae9ca08390f4c4b73d178` | Pushed and observed; Nix was not repeated here. |
| `logos-engine` | `NoAliasesWitnessReady` | `fec1130b120dc488674b475e182310e321824f25` | Pushed and observed. It descends from `91fad6d06e697510e39196bbf44319bb91e537ce`, which pins the closed Nomos escape set. It is not accepted because the witness currently fails. |
| `nomos-engine` | `NoAliasesWitnessReady` | `ea017db26d136ad97638d8177c96e94dade40f7f` | Pushed and observed. It descends from `3fa44a91d41d34790a44733b01c68aa58c69a0b6`, which adopts the closed escape set. It is not accepted because the witness currently fails. |
| `language-engine-witness` | `NoAliasesWitness` working copy | uncommitted candidate; parent `main` is `2daef51e1eda` | The working copy has intentional pin, lockfile, flake, and end-to-end-test changes. It pins the candidate revisions above. It is not a mergeable or passing result. |

The checked five producer flakes passed for the local x86_64-linux system. Their flake output reported other incompatible systems as omitted; this is not multi-system acceptance.

The retained witness `Cargo.lock` was inspected directly. The package names `content-identity`, `name-table`, `raw-discovery`, and `structural-codec` all resolve from `https://github.com/LiGoldragon/protos.git` at `e9983d6220856a011886145ed0ef0cc41c9bf597`; no retired standalone repository source was found in that lock file. This is a candidate one-universe proof only, because the witness test fails and none of these retained branches is yet progressively merged.

## Current hard blocker: persisted Logos provenance

This is the gate before the first language-engine vertical slice can pass.

Direct source inspection shows that `signal-sema-storage/src/lib.rs` at the retained `NoAliasesSignalSemaStorage` revision stores a Logos payload as encoded items plus its Logos NameTable bytes. It carries neither the source Schema document identity nor the source Schema NameTable identity.

`logos-engine/src/lib.rs` at the retained `NoAliasesLogosEngineEscape` revision restores the Logos home slice and generated `LogosStandard` slice. It has no source Schema slice to borrow. That conflicts with the composed-table rule whenever a Logos item refers to Schema identifiers.

The exact current witness command was run during this handover:

```text
nix build .#checks.x86_64-linux.test --no-link --print-build-logs
```

It ran two end-to-end tests: the manifest/lock consistency test passed; the four-process Schema -> Nomos -> Logos recovery test failed. Logos rejected projection because the composed NameTable did not borrow `Schema`, and the test timed out waiting for the push. This is real failed acceptance evidence, not a transport error.

The only proposed normal fix is a **typed content-identity relation** on a persisted Logos document:

- carry the exact source Schema document identity and the exact source Schema NameTable identity;
- let Nomos persist both identities from the transform input;
- on Logos projection, fetch that source document, verify document kind and NameTable identity, then compose the Logos home slice, fetched Schema slice, and generated `LogosStandard` slice;
- return typed errors for an absent source, wrong kind, identity mismatch, or composition failure;
- never embed or copy a borrowed Schema slice into a Logos archive.

### Open psyche decisions

These have **not** been ruled:

1. **Typed source relation:** accept or reject the content-identity relation on persisted Logos payloads.
2. **Existing Logos records:** regenerate or migrate records that lack this provenance. A migration requires an external verified provenance mapping; reconstruction must never be guessed.
3. **Spirit v13-to-v14 environment routing:** after an inventory presents the actual v13 privacy variants and the target environments, rule how one privacy-tagged v13 store routes into per-environment v14 stores. Do not infer a destination, collapse tiers, or implement routing before this authority decision.

The first two decisions block the language-engine witness. The third independently blocks the Spirit migration fold. Until the relevant decisions are made, do not patch a fallback, copy names into Logos archives, infer environment routing, or claim the affected working-program acceptance.

## Source-form and design artifacts

- `agent-outputs/ProtosEngine/SpiritSemaRedesign/spirit-sema-daemon-redesign.md`: accepted Spirit v14 design, actor/state boundaries, migration proof requirements, and review evidence.
- `/home/li/wt/github.com/LiGoldragon/core-schema/ProtosSourceFormsProposal/SOURCE_SURFACE_DECISION.md`: codec-backed source-surface proposal for interface alternatives and closed streaming relations. It is a proposal-branch artifact, not `main`.
- `/home/li/wt/github.com/LiGoldragon/core-schema/ProtosSourceFormsProposal/SOURCE_SURFACE_CANDIDATES.md`: exact codec-emitted and round-tripped candidate forms. Do not replace these with memory-authored examples.
- `/home/li/wt/github.com/LiGoldragon/protos/no-alias-migration/name-table/ARCHITECTURE.md`: owned-slice archival rule, composable borrowing, namespaced identifiers, and canonical-only naming.
- `/home/li/wt/github.com/LiGoldragon/signal-sema-storage/NoAliasesSignalSemaStorage/src/lib.rs`: current `DocumentPayload` shape that lacks Logos provenance.
- `/home/li/wt/github.com/LiGoldragon/logos-engine/NoAliasesLogosEngineEscape/src/lib.rs`: current persisted-name recomposition boundary.
- `/home/li/wt/github.com/LiGoldragon/language-engine-witness/NoAliasesWitness/tests/e2e.rs`, `Cargo.toml`, and `flake.nix`: retained witness candidate and its truthful denominator.
- `protocols/repos-manifest.nota`: authoritative repository inventory.

## Progressive-main integration discipline

Use this process for every slice:

1. Cross-examine every retained candidate against current `main` before landing. Treat an old base, stale pin, failed check, or changed contract shape as new evidence, not as permission to merge.
2. Land and push a green producer to its repository's `main` before a consumer pins it. A new consumer may depend only on a merged producer revision, never on a private retained branch family.
3. After every rebase or pin change, rerun the repository's full Nix check. If the slice crosses a public contract, also run its contract and wire checks; if it crosses a store, run storage-open, upgrade, and restart checks.
4. Merge one coherent vertical slice at a time across its producer-to-consumer graph. The slice is not done when a producer compiles in isolation.
5. Once the slice is green on `main`, push all affected `main` bookmarks, run the end-to-end acceptance denominator, conclude its worktrees as merged, and delete its handoff material. Do not retain a shadow train after landing.
6. Do not use compatibility aliases, conversion bridges, copied NameTable slices, legacy generator fallbacks, or a hidden bypass to make an intermediate slice pass. Keep old/new interoperability only at a deliberately retained and versioned external boundary; otherwise reject obsolete forms explicitly.

## Required vertical slices

### 1. Language-engine document persistence and projection

**Scope:** schema document creation through manifest/TextualForm reading, encoded Schema and NameTable persistence, Nomos transform, persisted Logos provenance, reload, recomposed names, Rust projection, and the four-daemon witness.

**Gate:** the two Logos provenance decisions above.

**Acceptance:**

- full Nix checks in every changed producer and consumer repository;
- codec round trips for the actual authored document forms and typed errors for missing/mismatched source provenance;
- a storage-layout and wire audit that names the version change and record treatment;
- a Rust review covering typed errors, no string manipulation inside Nomos, no aliases, and no copied borrowed slices;
- witness `nix build .#checks.x86_64-linux.test --no-link --print-build-logs` passing its complete denominator, including document creation, cross-process persistence/reload, and Rust projection;
- operational-confidentiality review confirming no Spirit production data is accessed and no candidate paths, contents, values, counts, hashes, credentials, sockets, or logs enter durable outputs. This is not a review of removed Spirit domain privacy logic.

Land its producer and consumer commits progressively on `main` before calling the machinery consolidated or the pipeline self-hosting.

### 2. Consolidated machinery retirement

**Scope:** after slice 1 proves one live type universe, land the consolidated Protos dependency graph and remove every remaining pin to the five retired standalone machinery repositories.

**Acceptance:**

- Cargo and Nix locks resolve all five package names from `protos` only;
- all direct and daemon consumers compile with one compatible machinery universe;
- the working-program witness passes on merged `main` revisions;
- repository and dependency audit confirms no consumer remains before deleting retired repositories.

Do not delete a retired repository merely because a candidate lock file is clean.

### 3. First complete component port

**Scope:** choose the smallest truthful component that can be ported completely before Spirit. The component must have a contract, daemon path, and behavior acceptance small enough to understand without unapproved language or storage work.

**Acceptance:**

- contract types are authored through Lineage B and emitted from the shared pipeline;
- daemon code uses the generated contract on its live request path;
- its old generator build dependency and generated-output path are removed, not wrapped;
- full Nix, contract/wire, and component process checks pass on `main`;
- independent Rust/Nix/contract audits record exact denominators.

The candidate selection is an implementation investigation, not authority to port Spirit prematurely.

### 4. Spirit contract and daemon port to v14

**Scope:** after the generic vertical slice and first component port demonstrate the pipeline honestly, apply the accepted actor and two-family storage base design as amended by environment isolation. Spirit remains privacy-naive: it serves one environment/store and has no privacy fields, filters, public/private operation splits, public-record naming assumptions, or privacy-specific diagnostics. Remove `Certainty` and `ChangeCertainty`; retain `Importance` and `BumpImportance`. Do not implement Criome environment, cluster, quorum, or access-control design here.

**Gate:** the independent v13-to-v14 environment-routing authority decision in the open-decision list. Do not implement the migration fold until actual v13 privacy variants and target environments have been inventoried and ruled.

**Acceptance:**

- one writer SpiritSema, distinct ordinary/meta admission and owner policy, nonblocking subscription delivery, typed Close backpressure, and commit-driven events are all on the live path;
- v14 record families and archive lifecycle are generated/implemented without legacy generator fallback, privacy/certainty carryover, or an environment-routing guess;
- every intentional signal, storage, or wire version change is explicit and audited;
- full Rust, Nix, signal-contract, wire, storage, actor-topology, and operational-confidentiality audits pass;
- no compatibility shim is added merely to preserve an obsolete generated API.

### 5. Isolated Spirit production-snapshot migration and behavior proof

**Scope:** only after slice 4 is merged, version-14 migration code is complete, and the v13-to-v14 environment-routing decision is explicitly implemented, use a supported consistent snapshot to test the frozen-v13-reader fold into the ruled per-environment stores.

**Acceptance:**

- a private candidate snapshot is used only for this operational proof; original production source stays unmodified;
- typed migration rejection categories, the ruled routing result, candidate reopen, ordinary/meta/streaming operations, delivery close/failure behavior, candidate-only mutation, restart, and original-integrity checks pass;
- all required commands run through Nix with truthful denominators;
- candidate data, runtime files, sockets, logs, and temporary snapshot material are removed afterward;
- reports contain no private content, paths, counts, hashes, credentials, or record values. This is operational confidentiality, not a requirement to restore Spirit domain privacy logic.

### 6. Repeat complete ports and delete deprecated generators

**Scope:** port components one at a time under the slice-3 standard until every consumer uses Lineage B.

**Acceptance:**

- each port has its own merged working-program evidence and audits;
- repository inventory and dependency search prove no consumer remains for `schema-language` or `schema-rust`;
- delete the deprecated generators only in a merged `main` slice after the final consumer has been accepted.

## Audit requirements for every slice

Select the applicable audits before declaring a slice complete:

- **Rust:** typed domain errors, ownership and actor boundaries, no hidden panics, no compatibility aliases, no handwritten duplicate contract types, and no strings in Nomos transformation.
- **Nix:** full flake checks after final pins/rebases, deterministic check outputs where derivations are rebuilt, and Nix-owned acceptance evidence rather than bare inner-loop tests.
- **Contract and wire:** encoded layout/version changes named; archive and frame round trips; bidirectional old/new operations only where a versioned compatibility boundary is deliberately retained.
- **Storage:** sole-writer ownership, record-family discipline, migration/reopen/restart behavior, archive lifecycle truth, and no silent relabeling of incompatible layouts.
- **Operational confidentiality:** no production data before the isolated-snapshot slice; no candidate or production values, paths, counts, hashes, credentials, sockets, or logs in durable outputs. This protects agent and runtime handling; it does not reintroduce Spirit domain privacy fields, filtering, or operation splits.
- **Design:** a slice must remove a special case rather than hide it. Material source-syntax, wire, storage, authority, or deployment changes require explicit psyche acceptance before implementation.

## Minimum next briefs

1. **Decision briefs, no code:** present the two Logos-provenance decisions and, separately, the Spirit v13-to-v14 environment-routing decision. The routing brief must inventory actual v13 privacy variants and candidate target environments; it must not invent Criome design or infer destinations. Do not ask workers to invent a storage layout or routing rule before acceptance.
2. **Language-engine persistence vertical-slice Generalist, after Logos decisions:** implement the typed relation or the ruled alternative from `signal-sema-storage` through Nomos, Logos, and witness; integrate producers and consumers into `main` in order; obtain the slice-1 audits and denominator.
3. **Independent slice audit:** review the final source, Nix, storage/wire version surface, operational-confidentiality boundary, and witness denominator before merge. Return concrete defects with paths and severities.
4. **First-component selection Scout:** identify the smallest truthful component candidate using the canonical repository inventory, existing contract/daemon shapes, and absence of unapproved source or storage changes.
5. **Spirit v14 Generalist, only after prior gates and the routing ruling:** apply the accepted base design as amended by environment isolation; port Spirit in merged vertical slices without privacy/certainty carryover, then schedule the isolated-snapshot proof only after its migration code and routing behavior are accepted and merged.

## Review findings and residual risks

- **Blocker — `signal-sema-storage/src/lib.rs:353` and `logos-engine/src/lib.rs:108`:** persisted Logos payloads lack the identities needed to reborrow the Schema NameTable. The direct witness Nix build fails before working-program acceptance.
- **High — retained candidates are not progressive-main integration:** the producer, signal, engine, and witness revisions are currently ahead of their repository `main` bookmarks. They are not a merged release and must be cross-examined before landing.
- **Medium — producer verification is local-system only:** the five direct Nix named-check builds passed on x86_64-linux while reporting other systems omitted. Do not present that as multi-system acceptance.
- **Low — Protos Nix evaluation warns about missing Crane package name/version metadata:** its named checks still passed, but the warning should be resolved before treating the packaging surface as polished.
- **Medium — Spirit v14 remains unported and was re-founded:** the accepted base design has no daemon/storage implementation or snapshot proof yet. Its pre-ruling privacy/certainty assumptions are superseded by environment isolation; workers must not implement them verbatim.
- **Blocker — Spirit v13-to-v14 environment routing is unresolved:** the actual v13 privacy variants and target environments have not been inventoried and presented for authority. The migration fold must not infer destinations or collapse tiers.
- **Residual risk — source-surface artifacts are not `main`:** the codec-backed interface and streaming source-form artifacts remain proposal-branch evidence and must be incorporated only through a merged vertical slice.

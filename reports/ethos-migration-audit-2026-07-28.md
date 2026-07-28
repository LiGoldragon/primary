# Schema → Ethos / Protos migration audit — 2026-07-28

## Scope and method

Read-only audit of `/home/li/primary` and `/git/github.com/LiGoldragon` on
2026-07-28. No build, test, fetch, mutation, deployment, or VCS operation was
performed. This matters: the test discussion below distinguishes declared test
gates, historical claims, and a freshly observed pass.

Claims are grouped as observations (directly witnessed), hypotheses (useful
interpretations not proven by a runnable witness), and unknowns. Repository
directory names and source/dependency metadata were treated as stronger evidence
than old reports; the official primary inventory was also checked and found to
conflict with the current directory/repo-name evidence.

## Executive finding

The intended family is three languages over Protos:

```text
Ethos (sweet declaration syntax)
  -> Nomos (string-free typed-data transformation)
  -> Logos (encoded program, projected to Rust only at the text edge)
       all using the Protos NameTree + StructureTree machinery
```

That is an explicit psyche ruling in `reports/DesignVision-2026-07-28.md`, not
an inference from code. The implementation is a partially-real, internally
Schema-named prototype of that family. It has useful working-shaped libraries
and three daemon implementations, but its persistence topology, identity
authority, naming, and component-consumer boundary conflict with the current
vision. It is not yet a replacement for the `schema` / `schema-rust` generator
on which Mind, Orchestrate, Messenger, Router, Spirit, and many wire-contract
crates presently rely.

The safe near-term conclusion is therefore: **do not gate those components on
Ethos migration.** Keep the current Schema generator as the compatibility
compiler while exercising the Ethos → Nomos → Logos vertical witness separately.

## Authoritative naming and repository state

### Observations

1. The current psyche design record calls the languages **Ethos → Nomos →
   Logos**, calls the common substrate **Protos**, and says the repo rename was
   directed. It specifically reports `core-ethos`, `ethos-engine`,
   `signal-ethos`, and `tree-sitter-ethos` as executed names
   (`reports/DesignVision-2026-07-28.md`, §§10–13).
2. Corresponding current checkout directories exist:
   `core-ethos`, `ethos-engine`, `signal-ethos`, `tree-sitter-ethos`, `protos`,
   and `protos-engine`.
3. The designated authoritative inventory, `protocols/repos-manifest.nota`,
   instead lists only `schema-next`, `schema-rust-next`, and `tree-sitter-schema`
   under the Schema family (lines 42–46). Those directory names do not exist in
   the inspected ghq root. Per the workspace contract the manifest is formally
   authoritative for membership, but it is materially stale for this rename and
   cannot currently identify the checked-out Ethos repositories.
4. The rename is only partial inside the implementation:
   `core-ethos/Cargo.toml` declares package/library/repository
   `core-schema`; `ethos-engine/Cargo.toml` declares `schema-engine` and
   depends on `core-schema`, `schema-language`, and `signal-schema`; and
   `signal-ethos/Cargo.toml` declares `signal-schema`. Their architecture and
   README titles retain the same names.
5. `protos` is a Rust workspace containing the foundation crates
   `content-identity`, `name-table`, `raw-discovery`, and `structural-codec`
   (plus its derive/fixture crates). `protos-engine` is explicitly a source-free
   Nix integration/conformance sink, not a Rust engine or package
   (`protos-engine/AGENTS.md`, `ARCHITECTURE.md`, and `README.md`).

### Conclusion

Use **Ethos / Nomos / Logos / Protos** for intended architecture and external
planning. Treat **schema / schema-rust / schema-language / core-schema /
signal-schema / schema-engine** as the present compatibility and source-level
vocabulary. Do not claim the latter has already been semantically renamed.

The inventory discrepancy is an operational blocker for any automated migration
or release-train selection; resolving it needs a narrow inventory decision/update,
not an inference by a component implementer.

## The three languages: evidence, not extrapolation

| Language | Ruled purpose | Implemented evidence | Material gap |
| --- | --- | --- | --- |
| Ethos | Schema’s dedicated, sweet declaration syntax. | `core-ethos` has stringless `CoreSchema`, `TextualSchema`, a universe bridge, authority-assignment tests, and textual round-trip tests. `ethos-engine` has a Signal → Nexus → Sema-shaped daemon and a two-front-end equivalence test. | Package/wire/daemon names are Schema; normal daemon ingest takes legacy Schema text and bypasses the authority-bound path. No component-facing Ethos contract/generator is present. |
| Nomos | String-free transformer from Ethos encoded data to Logos encoded data; transformers are typed data. | `core-nomos::MacroPackage` applies typed macro packages; tests cover pipeline/enriched/prelude/typed-transform boundaries. `nomos-engine` fetches a stored TypeSchema and persists Nomos/Logos documents. | No `TextualNomos`; engine unconditionally selects an enriched fixture package and persists `NomosPackage::WireFixture`, not an authored/selected durable package. It uses the old shared storage daemon model. |
| Logos | Stringless encoded program, then Rust only as a textual projection. | `core-logos` is a closed typed Rust-subset algebra with identity, name-table, and textual tests. `logos-engine` fetches `DocumentPayload::Logos` and projects it through `textual-rust`; its relay subscribes to Nomos events. | Projection currently assembles a `String` module head and uses `textual-rust`/`prettyplease`-era machinery. There is no demonstrated component generator replacing `schema-rust`. It too uses central shared storage. |

### Important disconfirming evidence

The vision says every engine is a stateful daemon with its own embedded Sema DB
and a separate translator daemon for name-to-integer authority. In contrast,
`ethos-engine/src/lib.rs`, `nomos-engine/src/lib.rs`, and
`logos-engine/src/lib.rs` each construct a `SemaPlane` that opens a Unix socket
to `signal-sema-storage`; their CLIs default to sibling sockets under
`/tmp/new-language-engine`. This is wired code, not merely an architecture
document. It directly disproves any claim that the presently checked-out engines
already embody the per-daemon Sema topology.

The same source also shows the ordinary Ethos-facing daemon request
`IngestTypeSchema` calling `LegacySchemaIngest::migrate_text` and storing its
parse-order name table. The authority-bound `ParsedSchema` path is exercised by
tests, but source comments explicitly mark ordinary ingestion as an offline
lean. Thus the identity authority is **contract/test-only for the daemon’s
normal ingress**, not wired behavior.

## Real behavior classification

| Surface | Classification | Witness |
| --- | --- | --- |
| Protos raw discovery, name table, structural codec and conformance harness | Wired library behavior | Source and extensive unit/integration test sets in `protos/*/tests`. |
| Core Ethos textual decode/encode and universe-signature validation | Wired library behavior | `core-ethos/src/{textual,universe}.rs`; tests include `textual_roundtrip`, `universe_bridge`, `authority_assignment`, `derived_conformance`. |
| Legacy and native parser agreement under one authority | Test-only vertical witness | `ethos-engine/tests/equivalence.rs`; it creates a temporary authority store and asserts equal Core content identity. |
| Ethos daemon ingestion to stored TypeSchema | Wired prototype path | `ethos-engine/src/lib.rs`; legacy text in, central Sema socket out. |
| Nomos transform and Logos store | Wired prototype path with fixed fixture choice | `nomos-engine/src/lib.rs`; `MacroPackage::enriched_fixture()` is selected unconditionally. |
| Logos-to-Rust projection and Nomos event relay | Wired prototype path | `logos-engine/src/lib.rs` and `src/bin/logos-engine.rs`. |
| Translator/name-authority daemon | Conceptual / undesigned | Explicitly listed as undesigned in `DesignVision` §"Undesigned". |
| Textual Nomos | Deferred | `core-nomos/README.md` explicitly says it parses/prints no Nomos text. |
| Ethos replacement for Schema Rust emission | Not implemented | No Ethos consumer generator was found; every inspected generator-dependent production component imports `schema-rust`. |
| Protos-engine integration | Wired conformance assembly, not engine behavior | Its lock/direction/shape and exact Spirit witness checks are real Nix declarations, but it has no component source and does not run the three engines as one family. |

## Test and build state

### Observations

- `protos`, `core-ethos`, `core-nomos`, `core-logos`, `ethos-engine`,
  `nomos-engine`, `logos-engine`, `schema`, `schema-language`, and `schema-rust`
  declare Nix checks for build, test, documentation, formatting, and Clippy.
  `signal-ethos` additionally names round-trip and doctest checks.
- `protos-engine` declares lock-policy, dependency-direction, repository-shape,
  ShellCheck, Spirit owner-suite, and exact `PublicTextSearch` process witness
  checks; its intended canonical entry is `nix run .#check-all`.
- The core libraries contain real test suites rather than only README claims.
  The engine repos declare generic Cargo test checks but have no independently
  observed current pass in this audit; `ethos-engine` has the dedicated
  equivalence test, while `nomos-engine` and `logos-engine` have no `tests/`
  directory in the inspected checkout.
- A historical report records a passing `nota` flake check on 2026-07-15. It is
  neither the present source revision nor an Ethos/three-engine integration
  witness, so it is not carried forward as a current green result.

### Unknown

No fresh build/test result is established. Running the gates would create build
state and could fetch inputs, outside this audit’s read-only/no-fetch scope.
The next implementation lane should run each owning flake gate at the exact
published pins and add one isolated process witness spanning all three daemons.

## Dependents that still require Schema

The currently functioning Persona-side stack is materially coupled to
`schema-rust` generation, not to Ethos:

| Dependent | Direct evidence | Consequence |
| --- | --- | --- |
| Mind | `mind/Cargo.toml` build-depends on `schema-rust` (branch `main`) and patches `schema`/`schema-cc`; its architecture calls `build.rs` the schema-rust driver. | Cannot swap naming or generator transitively without a compatible generated-runtime contract. |
| Orchestrate | `orchestrate/Cargo.toml` build-depends on `schema-rust`; `build.rs` invokes `GenerationDriver::daemon_runtime` for committed generated artifacts. | Its live orchestration work must remain on the current compiler surface. |
| Messenger (current repo `message`) | `message/Cargo.toml` build-depends on `schema-rust`; `build.rs` emits/checks Signal/Nexus/Sema/daemon Rust artifacts. | Same: no Ethos migration prerequisite for its current daemon. |
| `signal-message` and `signal-orchestrate` | Each build script invokes schema-rust contract generation and exposes schema directories over Cargo metadata. | These are the immediate generator seam for the two component daemons. |
| Router and Spirit | Both pin `schema` and `schema-rust`; Spirit also pins `schema-language` and vendors the sources in its flake. | They are broader legacy-generator dependents, outside the named four but decisive for a compatible migration. |
| Persona | Cargo references Schema/Rust (currently a `drop-next` branch) and its architecture says the schema-engine upgrade is scheduled. | It is not evidence of Ethos adoption. |
| Nomos/Logos prototype engines | `nomos-engine` imports `signal-schema`; their storage payloads import `core-schema`. | The purported new family is itself still Schema-named internally. |

`signal-mind` itself does not directly import Schema in its manifest, but Mind
does. The requested term **Logics** did not appear as a canonical repository or
component in the inspected evidence; the closest live exact names are
`logos-engine` and `core-logos`. It should not be silently normalized.

## Blockers to using Ethos as the component compiler

1. **No replacement compiler contract.** Existing components require
   `schema-rust`'s checked-in artifact/freshness workflow, Cargo schema-directory
   metadata, signal-frame surfaces, and daemon/runtime emission. No equivalent
   Ethos → Logos → Rust component-generator surface was found.
2. **Storage topology mismatch.** All three prototype engines use one central
   `signal-sema-storage` socket, conflicting with the ruled per-daemon embedded
   Sema DB and translator-daemon model.
3. **Authority path is not normal ingress.** The identified online canonical
   path is test/library reachable but ordinary Ethos engine ingestion is legacy,
   parse-order, and explicitly marked a lean.
4. **Nomos package selection/ownership is stubbed.** The engine has no request
   selector and applies an enriched fixture while storing a different fixed
   package marker.
5. **No end-to-end three-daemon executable witness.** The per-engine code is
   individually wired, but no checked witness proves Ethos ingest → Nomos
   transform → Logos Rust projection under isolated state.
6. **Name and inventory split.** Current directory/design names, internal
   package names, and the manifest disagree. Automated dependency/release work
   cannot safely choose one without an explicit inventory ruling.
7. **Legacy generator drift remains a separate risk.** Existing primary reports
   record historical `schema`/`schema-rust` dependency and generated-artifact
   drift. This audit did not rerun it, so it must not be conflated with Ethos
   readiness or used as evidence that Ethos is ready to replace it.

## Smallest credible compatibility path

This is a compatibility **boundary**, not a proposed semantic compromise:

1. Declare and keep `schema` + `schema-rust` as the supported component compiler
   for Mind, Orchestrate, Messenger, Router, Spirit, and their signal contracts.
   Pin existing known-good revisions rather than broadening migration scope.
2. Treat `Ethos → Nomos → Logos` as a parallel, isolated vertical slice. Use
   the existing `spirit-min`/equivalence fixture to prove: canonical identity
   binding, one selected typed Nomos package, persisted Logos, Rust projection,
   compilation, and behavior. Give each daemon temporary local storage/socket
   state only.
3. Introduce no global package rename and no blanket source rewrite. The first
   explicit hand-off criterion is a component-facing generated contract that
   can replace one `schema-rust` generated crate with equivalent behavior.
4. Migrate one leaf signal contract only after that witness passes; keep the
   old generator as the fallback compiler for every other component. A claim of
   “no compatibility adapters” belongs only to the later Spirit-port acceptance
   target in the design record, not to the prerequisite needed to avoid blocking
   current components now.

This decouples operational progress from the language migration without claiming
that Schema and Ethos already have interchangeable semantics.

## Questions only the psyche can answer

These are intentionally not resolved here:

1. Is `schema` now only a historical implementation name, or does the ruled
   “schema is the sugar, sweet syntax” retain an enduring distinct layer inside
   Ethos? The design record explicitly preserves a contradiction rather than
   resolving it by inference.
2. Does **Logics** mean Logos, a separate component, or something else?
3. Which repository names should the authoritative manifest carry: only Ethos
   names, the current Schema package names, or an explicit alias/migration
   representation? This is needed before automated work can safely select repos.
4. What is the translator daemon’s final name, wire contract, storage, sharing,
   mint/bind flow, and stale-entry policy across the three engines?
5. What is the root enum variant set for the unified namespace, and whether any
   external ontology is adopted?
6. Is a Rust capsule required, and what is the final capsule/manifest relation?
7. Does the required first component migration permit a bounded temporary
   compatibility compiler, or must the first port meet the later strict
   no-adapter Spirit acceptance criterion? The evidence supports the two stages
   but does not authorize collapsing them.

## Suggested next evidence

Before implementation, obtain a single decision on questions 1–3 and then run,
at exact pins, the owning Nix gates plus a new isolated three-daemon process
witness. That witness must disprove the current central-storage assumption by
showing per-daemon local state and a real translator authority; otherwise it
only validates the old prototype under new names.

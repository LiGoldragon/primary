# Context handover — True Schema and deterministic schema evolution

## Focus

Continue the deterministic schema evolution work from the current settled design point: **True Schema** as the canonical decoded semantic layer for authored `.schema`, with schema diff/help/Rust/encoding derived from it.

The earlier SEMA/redb compatibility discussion led here because deterministic store upgrade needs decoded schemas as data, not generated Rust or ad hoc component migrations.

## Settled psyche intent and constraints

- Best end-shape governs; existing code is implementation terrain, not design authority.
- True Schema is the canonical decoded semantic layer for the schema language.
- Authored `.schema` decodes into True Schema at schema decoding time.
- Encoding also goes through True Schema; normalized explicit `.schema` output is acceptable and does not need to preserve authored sugar.
- `schema-rust` consumes True Schema and does not generate it.
- Generated Rust is a projection, not schema authority or comparable schema data.
- Lazy and eager schema loading should use the same resolver/decoder/cache machinery; eager is lazy driven to completion.
- Help/docs data must be pure typed data and pass through normal NOTA/schema decoding; rendered strings are allowed only at the final display/projection boundary.
- Help projection is positional and label-free.

Spirit grounding used earlier:
- `w312`: deterministic derivable mechanisms belong in code/schema machinery, not agent judgment.
- `10pz`: do not preserve bad legacy shapes through silent compatibility paths.
- `gni3`: agent-authored handovers/reports are clues, not psyche-authorized design authority.

## Product component correction — current authoritative design

A prior synthesis line saying products are “ordered type-reference vectors” is incomplete/superseded.

Correct model:

- Product components are ordered.
- Canonical authored syntax prefers implicit component identity derived from the type name:

```nota
Entry { Domains EntryKind Description Referents }
```

- Explicit `field.Type` is allowed/required only when the same type appears more than once in one product and positions need disambiguation:

```nota
TimeRange { start.Time end.Time }
```

- Redundant explicit fields are invalid. This must be refused when types are unique:

```nota
Entry {
  domains.Domains
  kind.EntryKind
  description.Description
  referents.Referents
}
```

- If `field` is just the camel/lowercase-derived version of `Type`, it is invalid/redundant.
- If a type appears only once in the product, any explicit field name is invalid.
- True Schema must store valid explicit disambiguators from `field.Type`, because canonical re-encoding and schema evolution need them.
- Help displays canonical positional component syntax, including `field.Type` only where required. It does not display labels, name/type pairs, headings, or wrapper heads.

Schema evolution implication:
- Diffs must track both component identity and position. If a component is inserted at position X and later positions shift, the engine should detect insertion plus moves, not misread every shifted component as unrelated replacement.
- Positional insertion/move is not automatically safe for wire/storage. It requires explicit upgrade/default/backfill/projection rules.

Durable amendment: `agent-outputs/TrueSchema/ProductComponents-Amendment.md`.

## Confirmed help projection example

For `(Help Entry)`, the intended sequential positional output shape is:

```nota
{ Domains EntryKind Description Referents }
(Vector Domain)
[Belief Principle Preference Constraint]
Text
(Vector Reference)
```

Semantics:
- first row is the immediate positional component syntax;
- following rows are same-order expansions;
- `(Help Domain)` inspects `Domain` itself;
- no field labels, no `(Name Type)` pairs, no `Name:` headings, no `(Entry ...)` wrapper;
- do not invent names like `Kind` or collapse named types unless the selected help mode explicitly expands them from True Schema.

## Completed implementation before True Schema design

In `/git/github.com/LiGoldragon/upgrade`:

- `primary-xi6z.1`: deterministic SEMA schema diff awareness API.
  - Commits on `drop-next`: `d4724bc5a20a`, then audit fix `4e432ab7444d`.
  - Added fields in existing families now conservatively require explicit upgrade rules.
  - Audited accepted.
- `primary-xi6z.2`: authored `.schema` adapter into `SemaSchemaSnapshot`.
  - Commit: `8ae7fc1066a9` on bookmark `primary-xi6z.2`.
  - Uses schema parser/lowering, not generated Rust.
  - Audited accepted.

These slices are useful pressure tests, but True Schema is now the intended foundation. Future diff work should move to True Schema values/closures rather than typed snapshots assembled downstream.

## Design artifacts

- `agent-outputs/TrueSchema/Plan-TrueSchemaDesign.md` — initial True Schema design report.
- `agent-outputs/TrueSchema/DesignWave-Synthesis.md` — synthesis of data model, loader, help, and proof-test design wave. It is superseded where it conflicts with the product component correction.
- `agent-outputs/TrueSchema/ProductComponents-Amendment.md` — latest amendment for product components, `field.Type` validity, help impact, and evolution impact.
- `agent-outputs/TrueSchema/ContextHandover.md` — this handover.

## Recommended next rediscovery path

Read the product-component amendment first, then the design-wave synthesis. Treat both as design artifacts to question, not implementation authority.

Likely next vertical slice to weave, if approved in the fresh session:

1. Introduce `TrueSchema` as the public decoded semantic type, repairing/renaming the current `SpecifiedSchema` idea without creating a parallel layer.
2. Add decode entrypoints returning True Schema.
3. Add canonical normalized `.schema` encode fixpoint through True Schema.
4. Add binary/NOTA round-trip tests for True Schema.
5. Add proof tests that Rust top-level emission consumes True Schema and compatibility entrypoints delegate.
6. Include product-component validity tests: implicit unique types, valid duplicate `field.Type`, invalid redundant `field.Type`, and insertion/move diff identity expectations if the slice reaches diff-facing facts.

Do not start by implementing help daemon, production upgrade execution, or full lazy/eager loader unless the fresh session chooses a different slice.

## Open questions

- Should current public `Schema` eventually become `TrueSchema`, with the current `Schema` renamed/internalized?
- Should raw composite references such as direct `Optional<T>` in product positions be allowed, or should products require meaningful named types except valid duplicate disambiguators?
- Is `Text` a primitive or a schema-declared alias/newtype in the intended help examples?
- How should recursive/cyclic help expansion render by default?
- Which storage-coordinate changes belong in whole-schema hash versus a separate storage-binding hash?
- Should cross-package closure hashes inline dependency nodes or record dependency closure hashes as edges?

## Lane status

The design-amendment worker completed and wrote `ProductComponents-Amendment.md`. No True Schema tracker weaving or schema repo implementation has started in this lane. This handover ends the active orchestration/design lane.

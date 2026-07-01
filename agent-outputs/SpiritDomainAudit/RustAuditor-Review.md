# Rust Auditor Review: Spirit Domain Data Variant Audit

## Task And Scope

Audit question: determine whether `signal-spirit`, generated contract code, and the NOTA parser/codec incorrectly accept data-bearing enum variants as bare atoms, specifically around the scout-cited examples `(Technology (Software Data))` and `(Technology (Software (Data SchemaEvolution)))`.

Repository inspected: `/git/github.com/LiGoldragon/signal-spirit`.

No source or test files were changed. Existing tests and live read-only Spirit CLI queries were sufficient to prove the behavior.

## Findings

### Finding 1: Scout Conflated Two Spirit Surfaces; Parser Is Not Broken

Severity: High for orchestration decision, not a code defect.

Direct answer: this is not evidence that the NOTA parser is broken. In current `signal-spirit`, `Data` is an optional-payload `Domain` variant and therefore is intentionally accepted as a bare terminal domain tag. Separately, the generated `DomainScope` query surface has an explicit `All` variant and requires `(Data All)` for the general scope. The scout citation is valid for a `Domain` value, but invalid as a `PublicRecords` domain scope query.

Evidence:

- `/git/github.com/LiGoldragon/signal-spirit/schema/domain.schema:36-41` defines `Software` variants, with `Data` declared as `(Data (Optional DataLeaf))`.
- `/git/github.com/LiGoldragon/signal-spirit/schema/domain.schema:53` defines `DataLeaf [Persistence Serialization Formats Modeling SchemaEvolution Migration]`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:969-974` generates `pub enum Software { ... Data(Option<DataLeaf>), ... }`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:991-997` decodes the bare atom `"Data"` as `Software::Data(None)`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:1052-1061` decodes `(Data <leaf>)` as `Software::Data(Some(<DataLeaf>))`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:1190-1195` encodes `Software::Data(None)` as bare `Data`, and only emits a payload field when `Some`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:2148-2155` generates a separate `SoftwareScope` with `All` and `Data(DataLeafScope)`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:3799-3825` converts `Software::Data(None)` into `SoftwareScope::Data(DataLeafScope::All)`.

Command evidence:

- `spirit "(PublicRecords ((Full [(Technology Software)]) None))"` failed with `spirit: invalid NOTA input: unknown TechnologyScope variant Software`, proving `TechnologyScope::Software` is not accepted bare.
- `spirit "(PublicRecords ((Full [(Technology (Software Data))]) None))"` failed with `spirit: invalid NOTA input: unknown SoftwareScope variant Data`, proving the query scope surface rejects bare `Data`.
- `spirit "(PublicRecords ((Full [(Technology (Software (Data All)))]) None))"` returned `(Error [no matching record])`, proving the explicit `All` scope shape parses and reaches the query path.

Expected correction:

- Mind should not copy the scout-cited `(Technology (Software Data))` as a query/scope pattern.
- If Mind needs explicit general-case taxonomy scopes, imitate `DomainScope` style: `(Technology (Software (Data All)))`.
- If Mind needs Spirit-like record classification tags, then copying `Optional` leaf variants means choosing the existing Spirit convention where a bare parent tag represents the general/terminal classification.

### Finding 2: Generated Code Correctly Distinguishes Required Payloads From Optional Payloads And Leaf Variants

Severity: None; observed generated behavior matches schema.

Evidence:

- `/git/github.com/LiGoldragon/signal-spirit/schema/domain.schema:31-34` defines `Technology` with `(Hardware (Optional HardwareLeaf))` and `(Software)`. This means `Hardware` may be bare but `Software` carries a required `Software` payload.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:741-744` generates `Technology::Hardware(Option<HardwareLeaf>)` and `Technology::Software(Software)`.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:750-761` accepts bare `Hardware` and rejects any other bare `Technology` atom.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:763-787` requires two fields for non-bare `Technology` decoding and decodes `Software` from the second field.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:969-974` shows `Software::Theory` is a true leaf while `Software::Data(Option<DataLeaf>)` is optional data-bearing.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:1936-1948` shows `DataLeaf` is a leaf enum with `SchemaEvolution` as one leaf.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:1263-1369` traced decoding records bare `Data` as `EnumPayload(Some(Optional(None)))`, not as a leaf with no payload metadata.
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs:1626-1653` traced decoding records `(Data SchemaEvolution)` as `EnumPayload(Some(Optional(Some(...))))`.

Interpretation:

The generated contract is doing what the schema says: optional payload variants accept no payload, required payload variants require one, and pure leaves are distinct. There is no generated-code evidence that a required payload variant is being accepted bare.

### Finding 3: Existing Tests Explicitly Bless Bare `Data` As A Domain Tag

Severity: High if the desired future doctrine is explicit `All`; otherwise no defect.

Evidence:

- `/git/github.com/LiGoldragon/signal-spirit/tests/generated_contract.rs:430-439` test `terminal_value_domain_tags_round_trip_through_nota` parses `(Technology (Software Data))` into `Domain::Technology(Technology::Software(Software::Data(None)))` and asserts it encodes back to the same string.
- `/git/github.com/LiGoldragon/signal-spirit/tests/generated_contract.rs:444-458` test `curated_leaf_domain_tags_round_trip_through_nota` parses `(Technology (Software (Data SchemaEvolution)))` into `Software::Data(Some(DataLeaf::SchemaEvolution))` and asserts round-trip text.
- `/git/github.com/LiGoldragon/signal-spirit/tests/generated_contract.rs:490-500` test `terminal_value_domains_convert_to_scope_all` asserts `Software::Data(None)` converts to a scope that contains `Software::Data(Some(DataLeaf::SchemaEvolution))`.
- `/git/github.com/LiGoldragon/signal-spirit/tests/instance_schema.rs:132-146` test `bare_optional_leaf_variant_traces_an_empty_optional` documents the same behavior for `Programming`: a bare optional leaf variant traces as `Optional(None)`.

Commands run:

- `cargo test --features nota-text terminal_value_domain_tags_round_trip_through_nota --test generated_contract` passed: 1 passed, 0 failed.
- `cargo test --features nota-text curated_leaf_domain_tags_round_trip_through_nota --test generated_contract` passed: 1 passed, 0 failed.
- `cargo test --features nota-text terminal_value_domains_convert_to_scope_all --test generated_contract` passed: 1 passed, 0 failed.
- `cargo test --features nota-text pure_terminal_theory_domain_round_trips_through_nota --test generated_contract` passed: 1 passed, 0 failed.
- `cargo test --features nota-text bare_optional_leaf_variant_traces_an_empty_optional --test instance_schema` passed: 1 passed, 0 failed.
- `cargo test --features nota-text domain_path_traces_expected_types_down_the_real_taxonomy --test instance_schema` passed: 1 passed, 0 failed.

Minimal proof test:

The existing minimal passing proof is `terminal_value_domain_tags_round_trip_through_nota` at `/git/github.com/LiGoldragon/signal-spirit/tests/generated_contract.rs:430-439`. No new test was needed.

## Residual Risks

- The current Spirit schema has a dual convention: record `Domain` tags use optional payloads where bare parent tags mean the general classification, while `DomainScope` query filters use explicit `All`. That is easy for agents to confuse.
- If the psyche's desired universal rule is "all data-bearing/general-case variants must be explicit with `All`", then Spirit's `Domain` schema and its tests intentionally violate that desired rule. The responsible layer would be schema design plus blessed tests, not the parser or generated decoder.
- If the intended rule is only "query scopes must be explicit", current Spirit already enforces it; the scout citation was the problem.

## Checked Evidence

Files consulted:

- `/git/github.com/LiGoldragon/signal-spirit/schema/domain.schema`
- `/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema`
- `/git/github.com/LiGoldragon/signal-spirit/src/schema/domain.rs`
- `/git/github.com/LiGoldragon/signal-spirit/tests/generated_contract.rs`
- `/git/github.com/LiGoldragon/signal-spirit/tests/instance_schema.rs`
- `/git/github.com/LiGoldragon/signal-spirit/AGENTS.md`

Read-only intent/context query:

- `spirit "(PublicTextSearch [Spirit domain schema data variants NOTA])"` returned public records including `w312`, whose relevant conclusion is that deterministic classification/encoding belongs in code or schema-derived machinery rather than agent judgment.

Version/state checks:

- `jj status --no-pager` in `/git/github.com/LiGoldragon/signal-spirit` reported a clean working copy before the audit.

## Recommendation

For the next orchestration step: unblock Mind only if it uses the explicit scope pattern for query/filter semantics, e.g. `(Technology (Software (Data All)))`. Do not let Mind imitate Spirit's optional `Domain` classification pattern as the answer to the psyche's challenge unless the psyche explicitly accepts bare parent tags as terminal/general classifications. Spirit/NOTA does not need a parser fix from this evidence; a doctrine or schema-design decision is needed about whether Spirit's existing `Optional` domain-tag convention should remain allowed.

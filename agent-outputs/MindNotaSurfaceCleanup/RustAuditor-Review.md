# Rust Auditor Review

## Findings

No defects found.

The three reported changes satisfy the intended NOTA surface cleanup:

- `Accepted` is a direct payload: `signal-mind/tests/round_trip.rs:1392` through `signal-mind/tests/round_trip.rs:1395` asserts `(Accepted k9x8)`.
- `NotFound` is a bare unit variant: `signal-frame/tests/channel_macro.rs:184` through `signal-frame/tests/channel_macro.rs:193` asserts `NotFound`, and `signal-mind/tests/round_trip.rs:1403` through `signal-mind/tests/round_trip.rs:1405` asserts the same for `MindReply`.
- `Found` carries the public projection only: `signal-mind/src/lib.rs:1305` through `signal-mind/src/lib.rs:1308` defines `Found(KnowledgeRecord)` and `NotFound`; `signal-mind/src/knowledge.rs:81` through `signal-mind/src/knowledge.rs:98` keeps `accepted_by` and `accepted_at` on `AcceptedKnowledge` while projecting `KnowledgeRecord { identity, subject, statement }`.
- Runtime query replies use that projection: `mind/src/knowledge.rs:525` through `mind/src/knowledge.rs:531` maps stored `AcceptedKnowledge` through `AcceptedKnowledge::public_record` before `MindReply::Found`.
- The default command output path falls back to the generated contract codec for these replies: `mind/src/command.rs:184` through `mind/src/command.rs:190`; `mind/src/text.rs:1311` through `mind/src/text.rs:1314` does not add a bespoke text projection for `Accepted`, `Found`, or `NotFound`.
- Unit reply support does not loosen data-carrying positional payload handling. The macro-generated decoder accepts atom blocks only through unit-variant arms and still requires exactly two outer fields for payload variants in `signal-frame/macros/src/emit.rs:846` through `signal-frame/macros/src/emit.rs:878`. The underlying NOTA helper enforces exact field counts in `nota-next/src/codec.rs:243` through `nota-next/src/codec.rs:257`.

## Scope

Task: independent Rust audit for the Mind-family accepted-knowledge NOTA cleanup.

Reported commits inspected:

- `/git/github.com/LiGoldragon/signal-frame` `0027ea3cef353b1c168ca6862e40c6077a853642`
- `/git/github.com/LiGoldragon/signal-mind` `16a70dfd7f696b3e51080dbc2d086726fdaa8c75`
- `/git/github.com/LiGoldragon/mind` `290a63288bf68d14c40a056d89526fd1d9d2b41a`

All three worktrees were clean after inspection.

## Evidence Consulted

Files inspected included:

- `/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs`
- `/git/github.com/LiGoldragon/signal-frame/macros/src/model.rs`
- `/git/github.com/LiGoldragon/signal-frame/macros/src/parse.rs`
- `/git/github.com/LiGoldragon/signal-frame/macros/src/validate.rs`
- `/git/github.com/LiGoldragon/signal-frame/tests/channel_macro.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/schema_drift.rs`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/command.rs`
- `/git/github.com/LiGoldragon/mind/src/text.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`
- `/git/github.com/LiGoldragon/nota-next/src/codec.rs`

Spirit query: public text search for Mind/NOTA accepted-knowledge reply intent returned broad architecture/process records only; no specific accepted-knowledge reply directive was found. The audit therefore used the task brief and repository architecture/code as the operative behavior contract.

## Checks Run

- `/git/github.com/LiGoldragon/signal-frame`: `cargo test --features nota-text unit_reply --test channel_macro`
  - Result: passed, 2 tests.
- `/git/github.com/LiGoldragon/signal-mind`: `cargo test knowledge_verdicts_and_replies_round_trip --test round_trip`
  - Result: passed, 1 test.
- `/git/github.com/LiGoldragon/signal-mind`: `cargo test old_keyed_unkeyed_and_get_by_identity_surfaces_do_not_parse --test round_trip`
  - Result: passed, 1 test.
- `/git/github.com/LiGoldragon/signal-mind`: `cargo test concept_schema_declares_accepted_knowledge_roots --test schema_drift`
  - Result: passed, 1 test.
- `/git/github.com/LiGoldragon/mind`: `cargo test accepted_knowledge_submit_mints_identity_and_get_finds_record --test actor_topology`
  - Result: passed, 1 test.

Note: an initial `signal-frame` test command without `--features nota-text` matched zero tests because `tests/channel_macro.rs` is feature-gated. That no-op run was not counted as evidence.

## Residual Risks And Follow-Ups

Residual test hardening: `signal-mind` positively asserts the new reply shapes, and macro inspection proves strictness, but there is no direct negative test for the immediately retired reply spellings `(Accepted (k9x8))`, `(Found ((k9x8 Component [Mind stores accepted knowledge.] operator 1790000000000000100)))`, or `(NotFound (none))`. Adding those to `signal-mind/tests/round_trip.rs` would make the regression boundary more explicit.

Versioning note: `signal-frame` remains `0.3.0` and `signal-mind` remains `0.7.0` while public contract shapes changed. Both crates are `publish = false`, and downstream `mind` pins `signal-mind` to the exact cleanup revision, so this is not a current release defect. If these surfaces become externally versioned artifacts, the contract version surface should move with this breaking NOTA shape change.

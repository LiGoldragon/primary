# Adjacent NOTA Consumers

## Scope

Audited and edited only the assigned adjacent consumer repositories:

- `/git/github.com/LiGoldragon/nexus`
- `/git/github.com/LiGoldragon/nexus-cli`
- `/git/github.com/LiGoldragon/chronos`
- `/git/github.com/LiGoldragon/chroma`

No subagents were spawned. I avoided locked Persona/signal repositories. Reports are exempt from the claim flow; this is the only report file written for this subtask.

## Changed files

### nexus

Changed by this task:

- `Cargo.lock`
- `spec/grammar.md`
- `spec/examples/flow-graph.nexus`
- `spec/examples/patterns-and-edits.nexus`
- `spec/examples/tier-0-canonical.nexus`
- `tests/parser.rs`
- `tests/renderer.rs`

Notes:

- `Cargo.lock` now pins `nota-codec` to merged main `538555e895529e2884b7d37d20c66aadc2a49c08` and `nota-derive` to `8323149593b95d6e90c1fdde54e9aba58803337c`.
- Normal authored Nexus examples/tests now use bracket strings for string payloads such as node names, diagnostics, graph titles, and slot-binding replies.
- Added constraint-style witnesses:
  - `apostrophe_node_names_do_not_require_quote_delimiters`
  - `diagnostic_messages_with_apostrophes_render_as_bracket_strings`
- Pre-existing dirty work was present before this task in `ARCHITECTURE.md` and `spec/grammar.md`; I did not revert it. `spec/grammar.md` now contains both that pre-existing prose work and this task's bracket-string edits.

### nexus-cli

No files were changed by this task.

Audit result:

- No direct `nota-codec` Cargo pin found.
- No normal authored NOTA examples/tests/fixtures using quotation-mark string delimiters found.
- The working copy already had a dirty `ARCHITECTURE.md` from another thread; I did not edit it.

### chronos

Changed by this task:

- `AGENTS.md`
- `Cargo.lock`
- `README.md`
- `flake.lock`
- `src/bin/chronos.rs`
- `src/location.rs`
- `src/request.rs`
- `src/response.rs`
- `tests/location.rs`
- `tests/request.rs`
- `tests/response.rs`

Notes:

- `Cargo.lock` now pins `nota-codec` to merged main `538555e895529e2884b7d37d20c66aadc2a49c08` and `nota-derive` to `8323149593b95d6e90c1fdde54e9aba58803337c`.
- Replaced local `NotaSum` derives with `NotaEnum`.
- Converted empty request/reply struct variants to unit variants, and updated CLI/docs/tests from parenthesized unit forms like `(GetTime)` to bare unit forms like `GetTime`.
- Updated the `Location` validation test to current tagless `NotaRecord` form.
- Added constraint-style witness:
  - `error_messages_with_apostrophes_do_not_require_quote_delimiters`
- `flake.lock` was created by `nix flake check` because the repo had no lock file at the start of this task.

### chroma

Changed by this task:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `Cargo.lock`
- `README.md`
- `scripts/chroma-sandbox-terminal`
- `src/bin/chroma.rs`
- `src/config.rs`
- `src/daemon.rs`
- `src/request.rs`
- `src/response.rs`
- `tests/config.rs`
- `tests/request.rs`
- `tests/response.rs`

Notes:

- `Cargo.lock` now pins `nota-codec` to merged main `538555e895529e2884b7d37d20c66aadc2a49c08` and `nota-derive` to `8323149593b95d6e90c1fdde54e9aba58803337c`.
- Replaced local `NotaSum` derives with `NotaEnum`.
- Converted empty request/reply struct variants to unit variants, and updated unit request/reply examples from parenthesized forms to bare forms where required.
- Converted normal authored config examples, fixtures, and sandbox-generated config from quoted strings to bracket strings.
- Added bracket-string support to Chroma's custom config AST reader by normalizing bracket strings before the existing lexer path.
- Added/kept constraint-style witnesses:
  - `config_paths_with_apostrophes_do_not_require_quote_delimiters`
  - `error_messages_with_apostrophes_do_not_require_quote_delimiters`

## Tests

### Passed

- `/git/github.com/LiGoldragon/chronos`: `nix flake check --print-build-logs`
  - Passed after the `NotaEnum`/unit-variant updates.
- `/git/github.com/LiGoldragon/chroma`: `nix flake check --print-build-logs`
  - Passed, including the `sandbox-terminal` flake check.

Inner-loop only, not final evidence:

- `/git/github.com/LiGoldragon/chronos`: `cargo test --locked` passed before the final Nix check.
- `/git/github.com/LiGoldragon/chroma`: `cargo test --locked` passed before the final Nix check.

### Blocked

- `/git/github.com/LiGoldragon/nexus`: `nix flake check --print-build-logs` failed before Nexus tests ran.

Failure:

- Transitive locked dependency `signal` at `36dd4bc9` still imports removed `nota_codec::NotaSum`.
- Failing files in the vendored dependency:
  - `signal-0.1.0/src/edit.rs:20`
  - `signal-0.1.0/src/query.rs:12`

Reason not fixed here:

- Signal/Persona repositories were explicitly outside this subagent's owned scope and were under active lock by another lane.
- Updating Nexus's `signal` pin safely belongs to the signal migration owner after that repo has been migrated to current `nota-codec`.

### Not run

- `/git/github.com/LiGoldragon/nexus-cli`: no Nix check run because this task made no file changes there and found no direct NOTA parse/CLI surface needing a witness.

## Remaining quote exceptions

- Rust string literals remain where they are ordinary Rust values, expected strings, error messages, environment variable names, regexes, shell strings, DBus/XML strings, or non-NOTA prose.
- Legacy quote-string decode support was not removed from any codec consumer.
- Nexus still contains normal Rust literals such as `.to_string()` values; authored NOTA examples and expected NOTA output were converted where clear.
- Chroma's config reader currently normalizes bracket strings into quoted text internally before feeding its existing custom AST lexer. This is an implementation bridge, not an authored NOTA exception.

## Blockers and next actions

- The Nexus check is blocked on migrating or refreshing the locked `signal` dependency. Next action: signal migration owner updates `signal` away from `NotaSum`, then Nexus refreshes its `signal` lock and reruns `nix flake check --print-build-logs`.
- Decide whether Chronos should keep the newly generated `flake.lock`. It was produced by the required Nix check and left in place for visibility rather than silently deleting a build-system side effect.
- Nexus-cli needs no bracket-string migration action in this pass unless a future change adds direct authored NOTA examples or a direct `nota-codec` parse surface.

## Coordinator follow-up

After this subreport landed, the coordinator reviewed, committed, and
pushed the verified adjacent-consumer changes that had passed Nix:

- `chronos` `3ad63337`
  (`chronos: migrate NOTA examples to bracket strings`);
  `nix flake check --print-build-logs` passed.
- `chroma` `04c55e5f`
  (`chroma: migrate NOTA examples to bracket strings`);
  `nix flake check --print-build-logs` passed.

The Nexus work remains uncommitted. Its checkout had unrelated
pre-existing dirty work, and the bracket-string migration check is
blocked before Nexus tests run because the locked `signal` dependency
at `36dd4bc9` still imports removed `nota_codec::NotaSum` in
`edit.rs` and `query.rs`.

Tracker: bead `primary-36iq.6.2` covers the stale Nexus `signal`
dependency refresh required before this migration slice can close.

# Assistant-Text Getter on ClaudeRecoveredTurn — Implementation Evidence

Bead: primary-og38.2. Repo: `LiGoldragon/harness` (ghq path
`/git/github.com/LiGoldragon/harness`), branch `main`, commit `0d69e52d01b5`.

## Task

Add a public assistant-text getter to `harness/src/claude.rs`'s recovered-turn
type so consumers can source the assistant response text from the parsed
transcript instead of parsing the Claude CLI `result` line. The type's actual
name in source is `ClaudeRecoveredTurn` (the task brief called it
`RecoveredTurn`).

## Getter signature

```rust
impl ClaudeRecoveredTurn {
    /// The assistant response text this turn already parsed from the
    /// transcript, so consumers can source it directly instead of parsing
    /// the Claude CLI `result` line. `None` when the turn observed no
    /// assistant text; multiple assistant text fragments are joined with a
    /// blank line, in observation order.
    pub fn assistant_text(&self) -> Option<String>
}
```

Method on the data-bearing type (`ClaudeRecoveredTurn`), per
abstractions/rust-methods discipline — not a free helper.

## Surprise: the existing generic text collector is noisy for this purpose

`assistant_text_fragments` (the private field backing the getter) was
originally populated from `ClaudeJsonLine::text_fragments()`, a generic
recursive collector (`JsonLookup::strings_for_keys(&["text","content","stdout"])`)
that walks the whole JSON record and grabs every string value reachable
through those three keys. For an assistant record shaped like
`{"message":{"content":[{"type":"text","text":"..."}]}}`, this collector also
picks up the content-block's own `"type":"text"` discriminator as a bogus
fragment (a literal string `"text"`), and for `tool_use` blocks it recurses
into `input` and grabs unrelated strings (tool names, file paths, tool
arguments). A naive `assistant_text()` built directly on that field returned
`"FINAL_MARKER hello there\n\ntext"` in a first test run — visibly wrong.

Fix (still scoped to `claude.rs`, no re-parsing at the call site): added a
precise extractor used only for assistant text, reusing the existing
`JsonLookup` type rather than inventing a new parser:

```rust
// JsonLookup
fn text_block_strings(&self) -> Vec<String> { ... }
fn collect_text_block_strings(&self, value: &Value, strings: &mut Vec<String>) {
    // walks the record tree; on {"type":"text","text":"..."} pushes only
    // the "text" value and stops recursing into that object; recurses
    // through everything else (including tool_use blocks, picking up
    // nothing from them unless they themselves nest a real text block).
}

// ClaudeJsonLine
fn assistant_text_content(&self) -> Vec<String> {
    JsonLookup::new(&self.value).text_block_strings()
}
```

`ClaudeRecoveredTurn::observe_record` now populates `assistant_text_fragments`
from `record.assistant_text_content()` instead of the generic
`text_fragments()` result, for assistant-typed records only. The general
`text_fragments`/`contains_text`/`user_prompt_text_fragments` paths are
untouched (out of scope; other tests depend on their permissive substring
behavior for markers like `TOOL_MARKER` living inside tool_result content).

## Files changed

- `src/claude.rs`: added `JsonLookup::text_block_strings` +
  `collect_text_block_strings`, `ClaudeJsonLine::assistant_text_content`,
  `ClaudeRecoveredTurn::assistant_text`, and repointed the assistant-fragment
  branch of `observe_record` to the new extractor.
- `tests/claude_artifact_observer.rs`: added
  `claude_artifact_observer_recovered_turn_exposes_assistant_text`, using a
  fixture shaped like the existing `PROMPT_MARKER`/`FINAL_MARKER` fixtures
  (one user record, one assistant record with a single `text` content block),
  asserting `turn.assistant_text().as_deref() == Some("FINAL_MARKER hello there")`.

## Verification

- `cargo build --lib` — clean.
- `cargo test --test claude_artifact_observer` — 8 passed, 0 failed (all
  pre-existing tests plus the new one green; pre-existing tests unaffected
  because the noisy-fragment fix only removes noise, it does not remove the
  marker text those tests check for via `contains_text`/`has_completed_marked_turn`).
- `cargo build` (whole crate, all bins) — clean.
- `cargo fmt --check` — clean.
- `cargo clippy --lib --tests` — fails, but on a **pre-existing** issue
  unrelated to this change: a `#[deny(clippy::never_loop)]` violation at
  `wait_for_next_snapshot` (line ~369, far from anything touched here).
  Confirmed pre-existing by running `cargo clippy --lib` against the
  unmodified parent commit (`f07c4dfe`, before this bead's edits) — same
  failure. Left unfixed as out of scope for this bounded getter/test change;
  worth its own bead if clippy-clean is a repo goal.

## Repo / commit

- Repo: `LiGoldragon/harness`, ghq path `/git/github.com/LiGoldragon/harness`.
- Branch: `main`.
- Commit: `0d69e52d01b5` — "claude: add assistant-text getter to
  ClaudeRecoveredTurn". Pushed to origin (`jj git push --bookmark main`
  confirmed the bookmark moved `f07c4dfe17dd` → `0d69e52d01b5`).
- Working copy left clean (`jj status`: "The working copy has no changes").

## Bead

`primary-og38.2` closed with the evidence above. It blocks
`primary-og38.4` (push-based streaming transcript subscriber), which can now
proceed since the getter it depends on exists.

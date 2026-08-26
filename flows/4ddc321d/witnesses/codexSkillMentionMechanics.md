# Codex CLI 0.149.1: What `$SkillName` does programmatically

Witness record for tag `rust-v0.149.1` in `/git/github.com/openai/codex`.

## Verdict

Typing `$SkillName` in user input causes the harness to:

1. Parse the `$name` token from the text at the harness level (not the model).
2. Match it against the loaded skill catalog.
3. Read the matched skill's SKILL.md from disk (or package provider).
4. Inject the full SKILL.md body into the conversation as a user-role message
   fragment, wrapped in `<skill><name>...</name><path>...</path>...content...</skill>` tags.

This injection happens before the model sees the turn. The model does not need
to use tools to read the skill; its content is already present in the turn's
messages.

Separately, the "## Skills" catalog (names, descriptions, paths -- not bodies)
is placed in a developer-role message as part of the world state, and the
catalog's "How to use skills" instructions tell the model it should read
SKILL.md via tools. That instruction text is a fallback path for when the
harness injection did not fire (e.g., the model decides to use a skill on its
own from the catalog description rather than from a user mention). It does not
describe the primary `$`-mention path.

## Detailed findings

### 1. `$` mention parsing exists at harness level and triggers content injection

The `$` sigil is parsed from user text by `extract_tool_mentions()` in
`codex-rs/skills/src/mentions.rs`. The constant `TOOL_MENTION_SIGIL` is `'$'`.
The parser extracts plain `$name` tokens and linked `[$name](path)` forms.

Method: code read `codex-rs/skills/src/mentions.rs`

The extracted mentions are consumed in two selection paths:

**Host skills path** (`codex-rs/skills/src/selection.rs`):
`collect_explicit_skill_mentions()` iterates `UserInput::Text` items, calls
`extract_tool_mentions(text)`, and matches plain names against loaded
`SkillMetadata` entries. Returns `Vec<SkillMetadata>` of matched skills.

Method: code read `codex-rs/skills/src/selection.rs`

**Extension skills path** (`codex-rs/ext/skills/src/selection.rs`):
A parallel `collect_explicit_skill_mentions()` does the same against a
`SkillCatalog`. It processes `UserInput::Skill` (structured, from autocomplete)
first, then scans `UserInput::Text` with `extract_tool_mentions()`.

Method: code read `codex-rs/ext/skills/src/selection.rs`

### 2. Selected skills have their SKILL.md bodies read and injected

In `codex-rs/ext/skills/src/extension.rs` (lines ~450-510), for each entry
returned by `collect_explicit_skill_mentions`, the extension calls
`self.read_main_prompt(entry, ...)` which reads the SKILL.md content. The
result is wrapped in a `SkillInstructions` fragment and pushed to `fragments`.

In `codex-rs/core/src/session/turn.rs` (lines ~810-845), the host path calls
`skills_snapshot.load_skill_prompts(&mentioned_skills)` which reads each
skill's SKILL.md text and wraps it in a `SkillInstructions` fragment.

The fragments are converted to `ResponseItem::Message` via
`ContextualUserFragment::into_boxed_response_item()` and added to the turn's
injection items.

Method: code read `codex-rs/ext/skills/src/extension.rs`
Method: code read `codex-rs/core/src/session/turn.rs`
Method: code read `codex-rs/ext/skills/src/host_prompt.rs`

### 3. The injected fragment role and shape

`SkillInstructions` (defined in `codex-rs/ext/skills/src/fragments.rs`)
implements `ContextualUserFragment` with:

- `role()` returns `"user"` -- the body is injected as a user-role message.
- `markers()` returns `("<skill>", "</skill>")`.
- `body()` renders as:
  ```
  <skill>
  <name>{name}</name>
  <path>{path}</path>
  {SKILL.md contents}
  </skill>
  ```

This is distinct from `AvailableSkillsInstructions` (the catalog), which:

- `role()` returns `"developer"` -- the catalog is in the developer/system stratum.
- `markers()` use `SKILLS_INSTRUCTIONS_OPEN_TAG` / `SKILLS_INSTRUCTIONS_CLOSE_TAG`.
- Body contains `## Skills` with `### Available skills` listing name + description + path
  per skill, plus optional `### How to use skills` usage instructions.

The catalog does NOT contain SKILL.md bodies. It contains only names,
descriptions, and file/package locators.

Method: code read `codex-rs/ext/skills/src/fragments.rs`
Method: code read `codex-rs/ext/skills/src/catalog_prompt.rs`
Method: code read `codex-rs/context-fragments/src/fragment.rs`

### 4. The TUI autocomplete is an additional mechanism, not the only one

The TUI provides a `$`-triggered autocomplete popup
(`codex-rs/tui/src/bottom_pane/chat_composer.rs`, `sync_mention_popup`). When a
user selects a skill from the popup, the TUI creates a `UserInput::Skill {
name, path }` structured item (`codex-rs/tui/src/chatwidget/input_submission.rs`
line ~210).

However, plain `$name` text that was NOT selected from the popup is ALSO parsed
by `extract_tool_mentions` at the selection layer. Both paths (structured
`UserInput::Skill` from autocomplete and plain `$name` in `UserInput::Text`)
lead to skill body injection.

Method: code read `codex-rs/tui/src/chatwidget/input_submission.rs`
Method: code read `codex-rs/tui/src/bottom_pane/chat_composer.rs`

### 5. The model instructions describe a fallback, not the primary path

The base context instructions in `codex-rs/models-manager/models.json` say:

> "Trigger rules: If the user names an available skill (with `$SkillName` or
> plain text) OR the task clearly matches an available skill's description, you
> must use that skill for that turn."

And under "How to use a skill":

> "1) After deciding to use a skill, the main agent must read its `SKILL.md`
> completely before taking task actions."

These instructions describe what the model should do when it decides to use a
skill -- particularly when it picks one from the catalog by description match
rather than from a user `$` mention. For `$`-mentioned skills, the harness has
already injected the body before the model sees the turn; the model's tool-read
step would be redundant (though not harmful).

The catalog's "How to use skills" section is conditionally included based on
`include_skills_usage_instructions` from the model info configuration.

Method: code read `codex-rs/models-manager/models.json`
Method: code read `codex-rs/ext/skills/src/catalog_prompt.rs`

### 6. Unknowns

- **Server-side behavior**: The OpenAI Responses API endpoint may do additional
  processing of the `<skill>` tags or the `UserInput::Skill` structured items
  before or after they reach the model. This cannot be established from local
  code.

- **Feature flags**: The code contains feature-gated paths
  (e.g., `Feature::MentionsV2` which switches the sigil from `$` to `@`). The
  active feature set at runtime depends on server-side configuration and cannot
  be fully determined from the local source.

- **Dynamic skill selection**: A `dynamic_skill_selector` module exists under
  `codex-rs/ext/skills/src/` with various ranking strategies (BM25, LRU,
  character n-gram). Whether and when this fires to inject skills without an
  explicit `$` mention is governed by configuration not fully visible in local
  code.

# Codex CLI 0.149.1: Channel wire format and history retention

Witness record for tag `rust-v0.149.1` in `/git/github.com/openai/codex`.

## Verdict

Commentary and final are both `ResponseItem::Message` with `role: "assistant"`,
differentiated only by `phase: Option<MessagePhase>`. They are the same item
type in the same stratum -- the assistant's output. Commentary is retained in
conversation history and replayed to the model in subsequent turns, identically
to final-answer messages. Both are dropped after compaction.

## Detailed findings

### 1. MessagePhase enum has two variants

`codex-rs/protocol/src/models.rs` lines 893-901:

```rust
pub enum MessagePhase {
    Commentary,
    FinalAnswer,
}
```

The doc comment reads: "Classifies an assistant message as interim commentary or
final answer text."

Method: code read `codex-rs/protocol/src/models.rs`

### 2. ResponseItem::Message carries phase as an optional field

`codex-rs/protocol/src/models.rs` lines 940-965:

```rust
Message {
    id: Option<ResponseItemId>,
    role: String,
    content: Vec<ContentItem>,
    phase: Option<MessagePhase>,
    internal_chat_message_metadata_passthrough: Option<...>,
}
```

The comment reads: "Optional output-message phase (for example: 'commentary',
'final_answer'). Availability varies by provider/model."

Both commentary and final messages share the same `ResponseItem::Message`
variant; phase is a field value, not a structural type distinction.

Method: code read `codex-rs/protocol/src/models.rs`

### 3. BEM (realtime) path maps three channels to two phases

`codex-rs/core/src/realtime_conversation/bem.rs` lines 10-14:

```rust
("analysis", "[ANALYSIS]", MessagePhase::Commentary),
("commentary", "[COMMENTARY]", MessagePhase::Commentary),
("final", "[FINAL]", MessagePhase::FinalAnswer),
```

Analysis and commentary both map to `MessagePhase::Commentary`. The wire
channel is a bracket-prefixed text stream (`[ANALYSIS]...`, `[COMMENTARY]...`,
`[FINAL]...`) parsed by the `ChannelParser`.

Method: code read `codex-rs/core/src/realtime_conversation/bem.rs`

### 4. is_api_message admits all non-system messages without phase filtering

`codex-rs/core/src/context_manager/history.rs` lines 575-596:

```rust
fn is_api_message(message: &ResponseItem) -> bool {
    match message {
        ResponseItem::Message { role, .. } => role.as_str() != "system",
        // ... all other variants return true except CompactionTrigger and Other
    }
}
```

The function matches on `role` only. There is no branch on `phase`. Commentary
messages pass this filter identically to final-answer messages.

This function gates `record_items_with_metadata` (line 175), which is the entry
point for recording items into conversation history.

Method: code read `codex-rs/core/src/context_manager/history.rs`

### 5. Compaction drops all assistant messages regardless of phase

`codex-rs/core/src/compact_remote_v2.rs` lines 527-557:

```rust
fn is_retained_for_remote_compaction_v2(item: &ResponseItem) -> bool {
    // ... AgentMessage handling ...
    let ResponseItem::Message { role, .. } = item else {
        return false;
    };
    matches!(role.as_str(), "user" | "developer" | "system")
}
```

Assistant-role messages (both commentary and final_answer) are not retained
after compaction. They are replaced by an encrypted compaction summary.

Method: code read `codex-rs/core/src/compact_remote_v2.rs`

### 6. HTTP transport sends full history; no phase filtering

`codex-rs/core/src/client.rs` (around line 580-640): the HTTP path sends all
history items as `input` in every request. No `previous_response_id` is used.
No phase-based filtering occurs in the serialization path.

Method: code read `codex-rs/core/src/client.rs`

### 7. Reasoning items are encrypted and replayed

`codex-rs/protocol/src/models.rs` lines 976-988: `ResponseItem::Reasoning`
carries `encrypted_content: Option<String>` and `summary: Vec<...>`. These
items pass `is_api_message` and are replayed. The client receives plaintext
summaries but encrypted reasoning tokens; the server decrypts them on replay.

Method: code read `codex-rs/protocol/src/models.rs`

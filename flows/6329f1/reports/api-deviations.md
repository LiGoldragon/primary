# API deviations

Report for flow 6329f1.

## Port findings

### ethos-zero Library mode omits standard derives

ethos-zero 1.1.0 emits `#[derive(Archive, RkyvSerialize, RkyvDeserialize, Clone, Debug, PartialEq, Eq)]` for Signal roots but no derives for Library roots. Library consumers that need Clone, Copy, PartialEq or Eq on generated types must add them in a separate extension module (curriculum-deploy uses `src/generated_ext.rs` with a `unit_enum_traits!` macro for the four unit enums).

This is by design: Library types are plain Rust types, and the consumer adds whatever derives they need. A future ethos-zero could accept an optional derives section.

### Meaning/Text boundary in legacy Curriculum data

The Curriculum's `roles.datom` uses `(...)` parenthesized text for string values. The new protos parser reads `(...)` as opaque Parentheses boundaries, and the new datomic layer conceives these as `Datom::Meaning`, not `Datom::Text`. The `Corporal<Datom>` impl for `Text` (String) does not accept Meaning.

curriculum-deploy normalizes Meaning to Text before incorporation via `DatomNormalizing::normalize_meaning_to_text`. This bridge is application-level: it affects only the roles.datom reading path and will become unnecessary when the Curriculum data switches to curly quotes.

### Paths starting with `.` in datom

Paths like `.codex/agents/retired.toml` begin with a `.` separator character. The new protos parser produces a `MissingHead` fault for bare runs starting with a separator. The datomic layer's `datomize` for Text correctly curly-quotes such paths (they fail `is_bare_safe`). Old inventory files with unquoted dotted paths cannot be read by the new parser; `clean_previous_roles` falls back to skipping cleanup.

## Sources

- curriculum-deploy src/generated_ext.rs (derive workaround)
- curriculum-deploy src/runtime.rs:DatomNormalizing (Meaning normalization)
- protos 56c683ec src/lib.rs:parse_bare_run (MissingHead on leading separator)
- datomic a27f9b8e src/lib.rs:BareSafety (bare-safety rules)
- ethos-zero 31c5984c src/lib.rs:type_declaration_tokens (Signal vs Library derives)

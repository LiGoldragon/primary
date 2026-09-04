# API deviations

Report for flow 6329f1.

## Port findings

### ethos-zero Library mode omits standard derives

ethos-zero 1.1.0 emits derives for Signal roots but none for Library roots.
Library consumers that need Clone, Copy, PartialEq or Eq on generated types
add them in a separate extension module. curriculum-deploy uses
`src/generated_ext.rs` with a `unit_enum_traits!` macro for four unit enums.

### Paths starting with `.` in datom

Paths like `.codex/agents/retired.toml` begin with a `.` separator character.
The new protos parser faults on bare runs starting with a separator. The
datomic `datomize` for Text correctly curly-quotes such paths (they fail
`is_bare_safe`). Old inventory files with unquoted dotted paths cannot be
read; `clean_previous_roles` falls back to skipping cleanup gracefully.

### ~~Meaning/Text boundary~~ (resolved)

The Curriculum's roles.datom used `(...)` parenthesized text for string
values. Resolved by migrating the Curriculum data to canonical datom:
strings are now curly-quoted or bare. No normalization bridge in
curriculum-deploy.

## Sources

- curriculum-deploy src/generated_ext.rs (derive workaround)
- protos 56c683ec src/lib.rs (MissingHead on leading separator)
- datomic a27f9b8e src/lib.rs (bare-safety rules)
- ethos-zero 31c5984c src/lib.rs (Signal vs Library derives)
- Curriculum 143125b1 roles.datom (migrated data)

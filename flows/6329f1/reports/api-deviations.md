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

## repin2

### Situated import blocked by missing derives on protos::Situated

datomic 0.9.0 exports `Situated<F>` with Corporal<Datom> and Datomic, but
`protos::Situated<F>` (which datomic re-exports structurally) lacks
PartialEq and Eq derives. The ethos-zero Library emitter requires all
imported types to support the standard Library derives
(Clone/Debug/PartialEq/Eq). Orchestrate's client.ethos and
meta_client.ethos cannot import `datomic:Situated`; they keep a locally
declared Situated struct with identical shape. A protos change adding
PartialEq/Eq to Situated would resolve this.

### ethos-zero auto-boxes recursive types

ethos-zero 1.2.0 detects recursive type positions and automatically boxes
them, emitting `datomic::impl_datomic_box!` for the boxed type.
claude-answers' ethos source changed from `Grep.{ Box<Query> Text }` to
`Grep.{ Query Text }` because the explicit `Box<>` prevented the macro
emission. This is a change in authored ethos sources, not just generated
output.

### ~~ethos-zero Library mode omits standard derives~~ (partially resolved)

ethos-zero 1.2.0 now emits `#[derive(Clone, Debug, PartialEq, Eq)]` for
Library types. curriculum-deploy's generated_ext.rs reduced from the full
unit_enum_traits! macro to four bare `impl Copy` lines. Copy is not
emitted by the Library emitter; manual impls are still needed where Copy
is required.

## Sources

- curriculum-deploy src/generated_ext.rs (derive workaround)
- protos 56c683ec src/lib.rs (MissingHead on leading separator)
- datomic a27f9b8e src/lib.rs (bare-safety rules)
- datomic e4430bfe src/lib.rs (Situated Corporal/Datomic, impl_datomic_box!)
- ethos-zero 31c5984c src/lib.rs (Signal vs Library derives)
- ethos-zero 8bcb0b94 src/lib.rs (Library derives, recursive boxing)
- Curriculum 143125b1 roles.datom (migrated data)
- orchestrate 1c0dd769 ethos/client.ethos (Situated stays local)
- claude-answers a2edb677 claude-answers.ethos (Box<Query> -> Query)

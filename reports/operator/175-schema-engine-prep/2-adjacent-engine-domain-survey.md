# 175.2 — Adjacent, engine, and domain survey

## Adjacent Persona Components

The adjacent component pass covered Terminal, Harness, Introspect, System, Persona Pi, and repository-ledger style repos. Several have many binaries or daemon-only surfaces; the schema files therefore record concept-level signal roots rather than attempting to replace hand-written contracts.

Important finding: the schema pilot should not assume every component has a thin CLI today. The schema files should describe the signal tree, not the executable inventory.

## Engine and Upgrade Stack

The engine and upgrade stack is where schema work becomes operational:

- `upgrade` now carries the sandbox Spirit migration test app and schema checker.
- `signal-version-handover` and `version-projection` are the bridge for live version transitions.
- `sema-engine` is the storage execution substrate that will need schema-header and commit-sequence awareness in later work.

The concept schemas mark version `0.1` today. They do not claim that each repo already has schema-generated code.

## Libraries and Domain Repos

The library/domain pass covered signal, nota, forge, Criome, Lojix, horizon, and codec/derive crates. These schemas are intentionally lighter than component schemas:

- codec and derive crates expose language/compiler surfaces;
- signal and sema crates expose common vocabulary;
- domain repos expose domain-specific message trees.

The immediate purpose is to give the future schema engine one concept file per repo to discover and validate.


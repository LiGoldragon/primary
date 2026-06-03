# Skill — engine report

*A repeatable situation report for a code engine: size, schema, generated
surfaces, interfaces, runtime paths, witnesses, and tooling state.*

## What this skill is for

Use this skill when the psyche asks for an "engine situation", codebase
situation, component-size overview, interface map, or fast-readable report of
how a schema-derived/runtime engine currently works.

`skills/engine-analysis.md` is the deep architecture lens. This skill is the
standard measurement and presentation pass that makes the current code readable
quickly.

The report's main readability question: do the types name the work? Schema
should name the interface; generated Rust should name the objects and traits;
handwritten code should mostly match typed input, decide, call the next typed
interface, and return typed output.

## Standard report sections

An engine report carries:

1. **Current understanding.** One compact statement of what the engine is now,
   not its history.
2. **Component ledger.** Repos, role, process/binary status, storage, and
   whether each part is hooked, stubbed, contract-only, conceptual, or stale.
3. **Size ledger.** Production Rust, generated Rust, test Rust, authored
   schema, assembled schema, generated fixtures, public type count, and test
   count.
4. **Schema-to-code ledger.** For every `.schema` and checked-in `.asschema`,
   show where it lowers/emits and how much Rust it generates.
5. **Interface ledger.** Root enums, engine traits, contract traits,
   trace/help/config interfaces, and exact method signatures with file links.
6. **Runtime path.** One or more small diagrams showing the live call path.
7. **Witness ledger.** Tests by architectural claim and proof layer. Positive
   grep is never proof; use compile, runtime, process-boundary, trace, or
   artifact witnesses.
8. **Tooling state.** Which introspection tools were used, what worked, what
   failed, and what should be installed or configured next.

## Psyche-variant reports

When the engine report is written for the psyche to read directly, it is a
`Psyche` report in the `skills/reporting.md` sense. It starts from first
principles before it names gaps:

- what the engine is;
- what the schema defines;
- what Rust was generated from that schema;
- what handwritten code remains;
- what tests prove live use;
- what still needs to move into schema emission or shared runtime code.

Show the actual code for the important interfaces and paths, not only line
counts. Quote central intent by its bracket-quoted summary per
`skills/intent-log.md`; the record number is only the address.

## Measurement definitions

- **Production Rust**: `src/**/*.rs`, excluding generated `src/schema/**`.
- **Generated Rust**: checked-in `src/schema/**/*.rs`.
- **Test Rust**: `tests/**/*.rs`.
- **Authored schema**: `.schema` files.
- **Assembled schema**: `.asschema` files.
- **Generated fixtures**: checked-in `*.generated.rs` or `*_generated.rs`
  outside `src/schema/**`.
- **Public type count**: a rough inventory of `pub struct`, `pub enum`, and
  `pub trait` declarations. It is a size signal, not a proof.
- **Test count**: `#[test]`, `#[tokio::test]`, and `#[test_case]` markers.

Use `tools/engine-situation` for the first size ledger:

```sh
tools/engine-situation
tools/engine-situation /git/github.com/LiGoldragon/spirit-next
```

## Tool pattern

Use tools in this order:

1. `tools/engine-situation` — quick size/type/test ledger.
2. `tokei` — language-level size when a repo has mixed languages.
3. `leta workspace add` — once per repo before LSP-backed inspection.
4. `leta files` — readable file tree with line counts.
5. `leta show <Symbol>` — exact symbol body and signatures.
6. `leta calls --from <Symbol>` — call hierarchy for a live path.
7. `leta refs <Symbol>` — use sites when checking whether an interface is
   referenced.
8. `rust-analyzer symbols < path/to/file.rs` — fallback symbol inventory for
   one file.
9. `rust-analyzer analysis-stats <repo>` — optional semantic stats; useful but
   noisy, so quote only the summary.

If `leta` loses connection, run `leta daemon restart` and repeat a narrower
query. Broad regex searches are useful for discovery but less reliable than
specific `leta show` and `leta calls` queries.

## Visual rules

Engine reports use multiple small diagrams, not one giant graph. Each graph
answers one question and stays around four to eight nodes. Node labels are
single-line, two to five words, and never contain manual `\n` or `<br/>`
breaks. Put file paths, commit IDs, and long type names in nearby prose or a
table, not inside Mermaid nodes.

## Proof discipline

Inventory commands (`rg`, `leta grep`, public type counts) tell the reader what
exists. They do not prove that the architecture is live. A live-use claim needs
one of the witnesses from `skills/architectural-truth-tests.md`: a type-system
assertion, a runtime test, a trace-socket event, a process-boundary test, a
database artifact reader, or a removal-breaks-behavior witness.

## See also

- `skills/engine-analysis.md` — deeper engine analysis passes.
- `skills/architectural-truth-tests.md` — proof-of-usage ladder.
- `skills/mermaid.md` — graph readability and syntax.
- `skills/testing.md` — Nix-backed witness discipline.

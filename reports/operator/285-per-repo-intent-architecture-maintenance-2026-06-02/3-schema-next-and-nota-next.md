# schema-next and nota-next Findings

## schema-next State

Checked revision:

- commit `99078b20` on `main`
- description: `schema: collapse macro library data mirrors`

The working copy was clean.

Read:

- `AGENTS.md`: thin shim to workspace `AGENTS.md`.
- `INTENT.md`: present and current.
- `ARCHITECTURE.md`: present and current.

Missing:

- `skills.md`: absent.

`schema-next` already reflects the adjacent intent that matters for the trace
and triad work:

- schema owns type-name vocabulary while NOTA owns raw structure;
- Signal, Nexus, and SEMA schemas share the same authored shape;
- Nexus is the execution/decision/mail plane between Signal and SEMA;
- async mail remains actor-object flow, not collapsed procedural steps;
- `Asschema` is live macro-free data and serializes through NOTA/rkyv;
- macro-node structure is delegated toward `nota-next`;
- strict key/value schema syntax is the current authored path.

No schema-next edit is needed for the typed trace object slice. Trace object
emission is downstream in `schema-rust-next`; schema-next's current role is
preserving the root/interface objects and structural macro data that the Rust
emitter consumes.

## nota-next State

Checked revision:

- commit `f5906bae` on `main`
- description: `nota: make FieldEncode data-bearing`

The working copy was clean.

Read:

- `AGENTS.md`: thin shim to workspace `AGENTS.md`.
- `INTENT.md`: present and current.
- `ARCHITECTURE.md`: present and current.

Missing:

- `skills.md`: absent.

`nota-next` already reflects the adjacent intent that matters for this pass:

- NOTA owns raw delimiter structure and value codec shapes;
- NOTA does not decide schema semantics;
- known-root document-body parsing is owned by NOTA, not schema string joins;
- shared `NotaDecode` / `NotaEncode` are the codec traits generated Rust can
  derive for text-facing clients;
- `Box<T>` is storage indirection only and does not create a NOTA value shape;
- macro nodes are reusable structural patterns with captures and no-match
  diagnostics, while consumers own vocabulary and lowering.

No nota-next edit is needed for the typed trace object slice. The zero-NOTA
daemon/text CLI separation is a consumer configuration and dependency-boundary
issue in `spirit-next` and `schema-rust-next`; `nota-next` correctly stays the
text/codec substrate, not daemon runtime logic.

## Follow-Up

All four audited repos lack root `skills.md`. The immediate task did not
require creating those files, and creating four new skills files would be a
broader documentation-shape change. The practical future target is:

- `schema-rust-next/skills.md`: local regeneration, fixture, and emitter-test
  discipline.
- `spirit-next/skills.md`: feature matrix, Nix checks, daemon/CLI test
  commands, and schema regeneration loop.
- `schema-next/skills.md`: strict authored syntax, macro-node tests, and
  asschema artifact checks.
- `nota-next/skills.md`: parser/codec test conventions and macro-node
  substrate boundaries.

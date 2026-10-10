# Constraint Witness And Next Stack Port Audit

[Audit implementation against intent for missing constraint witnesses; when load-bearing intent is not expressed in constraints, add tests that prove the intended path instead of leaving the intent as prose.]

[Default behavior — when something changes in context that would correct a fresh-in-context report, the agent EDITS the report directly rather than narrating I should edit this report. Action over narration.]

[If a report has NOT been committed yet, edit in place freely. If a report HAS been committed and the edit is major, rename to a versioned filename like 493-v2-...]

## Scope

This session audits current next-stack code for load-bearing intent that is not yet expressed as executable constraints, then implements the most immediate witnesses.

The first production-facing control case is `spirit-next`, because it already consumes `schema-next`, `schema-rust-next`, `nota-next`, and `triad-runtime` through a real CLI / daemon / Signal / Nexus / SEMA path.

## Method

1. Read workspace and repo intent before editing.
2. Capture new durable intent through Spirit.
3. Dispatch sidecar audits for schema/triad constraints and component-port readiness.
4. Locally inspect `spirit-next` tests, flake checks, scripts, schema artifacts, and generated Rust.
5. Add runtime witnesses where intent was still only prose or source-shape assertion.
6. Keep grep checks only as negative guards against retired surfaces; avoid positive grep as architectural proof.
7. Run the cargo feature matrix and, where feasible, the local Nix stack proof.

## Current Local Slice

The implemented slice focuses on the recent alias-vs-newtype intent:

- bare schema bindings such as `Record Entry` and `Rejected SignalRejection` are direct payload aliases, not wrapper structs;
- the CLI/daemon path renders direct payload NOTA such as `(Rejected (EmptyTopic (0 0)))`, not nested wrapper output;
- local next-stack Nix scripts override `triad-runtime` as well as `nota-next`, `schema-next`, and `schema-rust-next`;
- `spirit-next` flake no longer advertises positive source greps as architecture proof.

## Sidecar Reports

- `1-schema-triad-constraint-gap-audit.md` audits schema/triad/runtime constraint gaps.
- `2-component-port-readiness-audit.md` audits adjacent component port readiness and recommends `upgrade` before `introspect`, with `persona` later.

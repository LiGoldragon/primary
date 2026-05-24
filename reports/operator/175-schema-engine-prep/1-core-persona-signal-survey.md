# 175.1 — Core persona signal survey

## Core Shape

The survey confirmed the active triad naming rule:

- daemon/runtime repo carries the bundled thin CLI where one exists;
- `signal-<component>` is the ordinary working signal;
- `owner-signal-<component>` is the policy signal.

The older `persona-*` prefix is not universal in repo names. The live workspace contains `mind`, `router`, `message`, `orchestrate`, `terminal`, `harness`, and similar daemon repos without the `persona-` prefix. Spirit is the notable `persona-spirit` repo.

## Spirit

Spirit is the strongest current pilot target. The concept schema roots reflect:

- ordinary signal roots: `State`, `Record`, `Observe`, `Watch`, `Unwatch`;
- owner signal roots: `Inspect`, `Version`, `Handover`;
- sema roots: `Assert`, `Match`, `Subscribe`, `Validate`.

The concept schema stays intentionally conservative. It names roots and primary node types, but does not try to encode the full current Rust shape until the schema engine can assemble and verify it.

## Mind, Router, Message, Orchestrate

The survey found enough shape to create conservative concept files:

- Mind: task/item/adjudication style state and owner inspection.
- Router: route/adjudication forwarding and observer shape.
- Message: daemon submission and validation shape.
- Orchestrate: task/session/chain coordination shape.

The generated files use the schema-language skeleton, not handcrafted Rust mirrors. They are markers and starting points for the later schema-engine pass.


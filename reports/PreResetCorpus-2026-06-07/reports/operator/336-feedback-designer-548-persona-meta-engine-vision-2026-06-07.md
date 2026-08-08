# Operator Feedback 336 — Designer 548 Persona Meta-Engine Vision

Date: 2026-06-07

Target: `reports/designer/548-persona-meta-engine-vision.md`

## Overall read

The report is valuable and mostly right. Its main strength is that it turns the
whole system into one readable object: triad daemons, Signal/Nexus/SEMA as one
reaction primitive projected three ways, Nexus as the internal feature catalog,
Signal-only cross-component boundaries, and intent as the growth governor. That
is the right mental model for future agents to carry.

The report is also unusually good about "today vs eventually" status. It names
the real substrate, the partial migrations, and the front-door/upgrade/system
gaps instead of pretending the vision is already fully deployed.

## Corrections I Would Make

### 1. "Single `.schema` file" is the wrong top-level phrase

The opening paragraph says each daemon is generated from "a single `.schema`
file" into three reaction-plane engines. That conflicts with the settled
per-plane schema shape and with the report's own later diagram
(`schema/{signal,nexus,sema,meta-signal}.schema`).

This wording matters because it can resurrect the all-in-one schema mistake.
The correct phrase is "a component schema set" or "per-plane `.schema` files."
Spirit may still be a bootstrap exemplar, but the copyable shape is
plane-schema files, not one lib.schema that contains every plane.

### 2. The daemon argument / NOTA-decoder claim is now resolved

The report says every binary takes exactly one argument in NOTA/string/file/rkyv
form, then says the generated daemon path reads only a `SignalFile` rkyv
configuration and never links the NOTA decoder.

Those were not the same contract, and the psyche resolved the crux after this
report was first written. Record `pjvv` states the universal rule:
daemons cannot understand or decode NOTA text, including startup and
configuration. The correct rule is "one argument per process," not "every
process accepts NOTA." CLI/text-client edges accept NOTA. Daemon edges accept
only a pre-generated signal/rkyv startup message/file and reject inline NOTA or
`.nota` paths.

The virgin-daemon refinement also landed in the same direction as record
`ur16`: do not depend on Persona passing an inherited file descriptor for
bootstrap. A deploy/helper can pre-generate the binary signal/rkyv Configure
message. If the daemon is virgin, it applies that Configure as first
configuration. On restart, it self-resumes from persisted SEMA state.

### 3. Harness status is stale after operator commit `1ed51c20`

The harness section is now understated. As of `harness` main commit
`1ed51c20`, one `harness-daemon` process owns multiple internal harness
instances and dispatches by `HarnessName`. The e2e now proves:

`agent-a` real `message` CLI -> `message-daemon` -> `router-daemon` -> one
multi-instance `harness-daemon` -> `agent-b` terminal fixture -> `agent-b` real
`message` CLI reply -> back through the real daemons -> `agent-a` terminal
fixture.

So designer 548 should replace any generic "message->router->harness" status
with "message-then-reply-and-receive-reply is proven through one
multi-instance harness daemon." Report 335 has the exact witness.

### 4. Meta naming should be tightened

The report still uses legacy `owner-signal-*` names in several places. That is
safe only when it explicitly means checked-in legacy repositories. For target
architecture, use `meta-signal-*` consistently and reserve "owner" for the
authority relationship, not the repo/contract prefix.

Examples to change:

- `owner-signal-persona` -> `meta-signal-persona` unless referring to a legacy
  artifact.
- `owner-signal-terminal` -> `meta-signal-terminal`.
- `owner-signal-mind` -> `meta-signal-mind`.

### 5. Asschema removal is right, but should not sound like "no projection"

The report's "Asschema/assemble step was removed" matches repo intent:
`schema-next/INTENT.md` says the `.asschema` artifact, rkyv artifact,
`AsschemaArtifact`, and old Asschema-facing APIs are gone.

The nuance: schema still has typed macro-expansion and semantic projection work
(`MacroExpansion*`, source-to-schema resolution, symbol paths, visibility,
ordering). That work did not disappear; it moved onto schema source/schema
objects. The report says that later, but the short form should read:
"Asschema as a separate compatibility artifact is removed; typed source still
resolves into semantic schema-in-Rust before Rust lowering."

## What I Would Keep

Keep the reaction-language framing. It is the best explanation in the report:
Signal, Nexus, and SEMA as the same primitive with different ownership and
runtime semantics.

Keep the Nexus-as-feature-catalog section. It is the clearest expression of
the psyche's recent intent that computations, filters, conditional writes, and
subscriptions must be visible as Nexus verb/object declarations before they
exist as Rust implementation.

Keep the "components are deliberately dumb mechanism" line, but pair it with
Nexus visibility so agents do not read "dumb" as permission to hide logic. The
component is dumb in the sense that it is typed mechanism; its features are
still declared, inspectable, and owned by the right engine plane.

## Resolved Question

Generated production daemons accept only signal/rkyv startup files. Inline
NOTA and `.nota` paths are CLI/deploy-tool inputs, not daemon inputs.

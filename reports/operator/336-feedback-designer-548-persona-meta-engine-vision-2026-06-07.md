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

### 2. The daemon argument / NOTA-decoder claim needs a crux resolved

The report says every binary takes exactly one argument in NOTA/string/file/rkyv
form, then says the generated daemon path reads only a `SignalFile` rkyv
configuration and never links the NOTA decoder.

Those are not the same contract. The workspace hard rule currently says every
binary accepts one argument that may be inline NOTA, a NOTA file, or a signal
rkyv file. If generated daemons intentionally accept only a rkyv config file,
that is a design change that needs to be explicit and reflected in the skill.
If not, `schema-rust-next`'s emitted `DaemonCommand` is short of the
single-argument rule.

My lean: keep the universal "one argument" rule, but make the production daemon
configuration path prefer binary rkyv for deployment. Do not phrase "never
links NOTA decoder" as universal unless the psyche explicitly narrows daemon
startup forms.

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

## One Important Question

Do generated production daemons have to accept all three single-argument forms
(inline NOTA, NOTA file, signal/rkyv file), or only signal/rkyv config files?

This is the only point where designer 548 appears to conflict with the current
workspace hard rule. I would not let that ambiguity harden in a meta-engine
vision document.


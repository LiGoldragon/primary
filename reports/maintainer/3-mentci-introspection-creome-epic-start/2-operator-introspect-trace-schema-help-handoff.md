# Operator handoff — introspect, tracing, schema help

## Current state

- `introspect` exists and is more than a draft: it has daemon/CLI/meta-CLI architecture, a Kameo root, an `introspect.sema` store through `sema-engine`, and a first live `RouterClient` witness path.
- It is still incomplete for the new Mentci goal: manager/terminal clients are scaffolds; the broader trace ingestion/query plane is not yet the universal component-observation backend.
- `skills/component-triad.md` already defines the trace direction: typed trace frames, no daemon printline fallback, trace-enabled builds, triad-runtime helpers, and optional trace sinks.
- Existing Spirit record `80bl` already states the intended Mentci/introspect query shape: component type, message type, and schema-derived signal input/output shape.

## Design target

Mentci should query introspect as the interactive observation/debugging surface. Introspect should ingest schema-defined trace/observation events from components, persist them, and support query/filter dimensions that map to component and signal-schema structure.

## Likely repos

- `/git/github.com/LiGoldragon/introspect`
- `/git/github.com/LiGoldragon/signal-introspect`
- `/git/github.com/LiGoldragon/meta-signal-introspect`
- schema/trace support in schema-next/schema-rust-next/triad-runtime if present
- component contracts whose trace/observe events should be ingested first: Mentci, Criome, Spirit, router/message as available

## Work items

1. Audit existing trace feature state: which crates still have `testing-trace`, trace sockets, trace event enums, or trace clients.
2. Define first `signal-introspect` query extensions for:
   - component kind / component identifier,
   - message or operation kind,
   - signal input/output object names,
   - time/order/correlation key where available.
3. Wire one real component source into introspect beyond router summary, preferably a trace/event source that Mentci can display.
4. Make schema-generated help discoverable through a library/API that Mentci-lib can call rather than scrape CLI text.
5. Keep component observations component-owned; introspect wraps/correlates, it does not become a shared bucket of every component’s private schema.

## Validation

- `cargo test` / `nix build` for `introspect`, `signal-introspect`, and touched trace/schema crates.
- A process-boundary witness: component emits typed observation/trace → introspect stores/query returns it → Mentci or a CLI can render it.
- Source scan: no polling loop; no peer DB opens; no daemon-side printline trace fallback.

## Compact implementation prompt

Audit and revive the trace/introspect path so Mentci can query component behavior. Start by inventorying existing optional trace features and schema-help surfaces, then add the smallest real introspect query path by component/message/schema object. Prove one typed event crosses a daemon boundary into introspect and can be queried/rendered. Keep observation push-based and component-owned.

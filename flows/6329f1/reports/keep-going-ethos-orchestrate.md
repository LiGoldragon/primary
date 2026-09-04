# Keep-going: ethos-zero import resolution and orchestrate generated ClientFailure

Subflow of 6329f1.

## ethos-zero 1.1.0 (31c5984c7fda)

### What was changed

The emitter resolves imported names to their source module path. A resolution
table is built from the concept's imports and threaded through every emitter
function that produces type tokens. When a `Named` type expression or an
`Applied` constructor matches an imported name, the emitter qualifies it with
the source module (e.g. `datomic::Fault`, `protos::Extent`,
`signal_orchestrate::Refusal`). Intrinsic names (Text, Integer, Decimal,
Boolean, Meaning, Symbol) still take precedence over imports. Intrinsic
constructors (Vector, Option, Result) are unaffected.

A proptest generates random `Concept::Library` values (structs, enums, aliases,
nested type expressions up to depth 2) and verifies the protosize-print-read
round-trip.

Version bumped 1.0.0 to 1.1.0 (feature addition, backward compatible).
Self-description ethos and bootstrap module regenerated.

### Witnessed results

```
cargo test: 43 passed (37 existing + 5 import resolution + 1 proptest)
cargo clippy --all-targets -- -D warnings: clean
cargo fmt --check: clean
nix flake check -L --builders 'ssh://prometheus': all checks passed
```

## orchestrate 0.28.0 (d47382d79710)

### What was changed

The hand-written `ClientFailure` enum and its `Corporal`/`Datomic` impls are
replaced by generated Library ethos files:

- `ethos/client.ethos` imports `protos:[ Extent ]`, `datomic:[ Fault ]`,
  `signal_orchestrate:Refusal`
- `ethos/meta_client.ethos` imports `protos:[ Extent ]`, `datomic:[ Fault ]`,
  `meta_signal_orchestrate:Refusal`

Both define `Situated` locally as `Situated.{ Option<Extent> Fault }` and
`ClientFailure.[ Unreadable.Situated Unreachable.{ Text Text } Refused.Refusal ]`.

Generated Rust is committed at `src/generated/client.rs` and
`src/generated/meta_client.rs`. A freshness test (`tests/client_freshness.rs`)
proves each committed module matches ethos-zero formatted emit output.

The no-argument self-description now prints the client Library's canonical text
from its ethos concept (actualized and protosized through ethos-zero's
`Printing` kind) instead of a hand-written commented block.

ethos-zero pinned at 31c5984c7fda (1.1.0). Version bumped 0.27.0 to 0.28.0.
UPGRADES.md entry added.

### Why Situated is local, not imported as a generic

The brief asked for `datomic:[ Situated Fault ]` with `Situated<Fault>` resolving
to `datomic::Situated<datomic::Fault>`. The ethos-zero import resolution feature
supports this: the emitter would correctly qualify both the constructor and its
argument. However, the generated `Corporal<Datom>` impl for `ClientFailure` calls
`<datomic::Situated<datomic::Fault> as Corporal<Datom>>::incorporate(...)`, which
requires a blanket `impl<F: Datomic> Corporal<Datom> for Situated<F>` in datomic.
That impl does not exist, and adding it to orchestrate violates orphan rules
(both `Situated` and `Fault` are foreign types). The smallest honest shape is to
define `Situated` locally with the same field layout; the datom text is
byte-identical, and the CLI converts `protos::Situated` to the local struct at
the actualize error boundary.

### Why Refusal can be imported

`signal_orchestrate::Refusal` already carries generated `Corporal<Datom>` and
`Datomic` impls from ethos-zero's wire envelope emission. Importing it by name
works because the impl is in the signal crate, not in orchestrate.

### Witnessed results

```
cargo test: 14 passed (2 lib + 6 live_nexus + 4 ordinary_lock_contract + 2 freshness)
cargo clippy --all-targets -- -D warnings: clean
cargo fmt --check: clean
nix flake check -L --builders 'ssh://prometheus': all checks passed
```

### Verbatim stderr (client_failures_are_datom_on_stderr, byte-identical to 0.27.0)

```
Unreadable.{ Some.{ 5 13 } Structural.{ { 5 13 } Unclosed.Braced } }
Unreadable.{ None Corporal.{ [] Shape.{ Variant Nonsense } } }
Unreachable.{ /no/such.sock \u{201C}No such file or directory (os error 2)\u{201D} }
```

## Judgment calls

1. **Situated local, not imported generic**: see above. The ethos-zero language
   feature is complete (import resolution works for generic constructors), but
   the downstream impl is missing in datomic. Choosing the local definition
   avoids a datomic change while preserving identical datom text.

2. **Two ethos files**: each CLI imports Refusal from its own signal crate, so
   `ethos/client.ethos` and `ethos/meta_client.ethos` are separate files.

3. **Version 1.1.0 for ethos-zero**: import resolution is a backward-compatible
   feature addition; existing ethos files without imports emit identical Rust.

4. **Version 0.28.0 for orchestrate**: the generated code replaces hand-written
   code; the datom text and wire are unchanged, but the source structure differs.

## Deployment

The deployer would:
1. Bump the CriomOS flake input `orchestrate` to `d47382d79710`.
2. Deploy via Lojix `Deploy.UserEnvironment` with `ActivateNow`.
3. The activation restarts `orchestrate-nexus` automatically.

See `flows/6329f1/reports/deployment.md` for the established procedure.

## Left undone

1. **Blanket `Corporal<Datom>` and `Datomic` for `Situated<F>` in datomic**:
   adding `impl<F: Datomic> Corporal<Datom> for Situated<F>` and
   `impl<F: Datomic> Datomic for Situated<F>` to datomic would allow importing
   `Situated` as a generic type directly (`datomic:[ Situated Fault ]` then
   `Situated<Fault>` in type position). The ethos-zero emitter already resolves
   this correctly; only the downstream impl is missing.

## Sources

- ethos-zero origin/main 185f13a (starting point)
- orchestrate origin/main 281e070 (starting point)
- Vision/ethos.md (import syntax, kind identity)
- flows/6329f1/log.md (design spec)
- flows/6329f1/reports/ethos-zero.md (ProtoformStack rewrite context)
- flows/6329f1/reports/signals-orchestrate.md (ClientFailure hand-written context)

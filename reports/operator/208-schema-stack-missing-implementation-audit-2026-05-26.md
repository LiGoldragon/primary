# 208 — Schema stack missing implementation audit

## Findings

### P1 — `spirit-next` still hand-writes the signal frame and route table

`spirit-next/src/transport.rs:13` defines `InputRoute` manually, and
`spirit-next/src/transport.rs:97` through `spirit-next/src/transport.rs:127`
hand-map generated `Input` / `Output` variants to short-header constants. The
frame encoder and decoder are also hand-written in
`spirit-next/src/transport.rs:137` through `spirit-next/src/transport.rs:211`.

This proves the process boundary, but it is not yet the intended architecture
where schema-derived Rust emits the signal frame behavior, header dispatch,
message identifiers, caller/process-origin metadata, and route matching. The
header constants are generated; the header-consuming transport is not.

Consequence: changing `schema/spirit.schema` can generate new surface types and
constants, but the runtime route table still needs manual edits. That is the
main interface-generation gap.

### P1 — `schema-next` is not yet a real fixed-point macro engine

`schema-next/src/engine.rs:59` through `schema-next/src/engine.rs:63` hard-code
two macro implementations as fields on `SchemaEngine`. `lower_document` in
`schema-next/src/engine.rs:75` through `schema-next/src/engine.rs:100` expects
exactly three root objects and lowers imports, surfaces, and namespace in a
single pass.

The `SchemaMacro` trait exists, and `MacroPosition` reaches `lower`, but there
is no macro registry, no imported macro namespace, no recursive expansion until
macro-free, no macro output re-entry, and no `.asschema` serialization.

Consequence: the current parser can lower the Spirit MVP syntax, but it cannot
yet host schema languages as first-class macro spaces.

### P1 — imports are parsed but not resolved

`schema-next/src/engine.rs:103` through `schema-next/src/engine.rs:135` only
accepts an even brace map of local-name/source-name atoms. The resulting
`ImportDeclaration` stores a `TypeReference`, but nothing resolves paths,
selective imports, import-all, collision checks, exports, or global qualified
names.

Consequence: Spirit currently works because its import section is empty
(`spirit-next/schema/spirit.schema:1`). Shared schema libraries, cross-schema
type reuse, and conflict rejection remain unimplemented.

### P1 — upgrade/downgrade from schema diff is absent

`schema-next/src/asschema.rs:39` through `schema-next/src/asschema.rs:45`
stores identity, imports, surfaces, and namespace. There is no schema hash,
stored canonical `.asschema`, diff engine, upgrade plan, `UpgradeFrom`,
`DowngradeTo`, default-field annotation, discard annotation, or incompatible
change failure.

Consequence: the new stack cannot yet do the full main/next upgrade path
described in the upgrade work. The Spirit pilot is schema-generated at build
time, but it does not yet derive migration logic from two schemas.

### P1 — Spirit is not production-feature equivalent to v0.3

`spirit-next/src/store.rs:9` through `spirit-next/src/store.rs:45` is an
in-memory vector store. It has no redb database, no persisted schema header, no
daemon-created timestamp, no multi-topic vector support, no multi-record
result set, no topic-list/count query, and no migration from production
Spirit.

The current schema also shows the limitation directly:
`spirit-next/schema/spirit.schema:11` uses one `Topic`, and
`spirit-next/schema/spirit.schema:13` defines `RecordSet [Entry]`, a newtype
around one entry rather than a vector of entries.

Consequence: `spirit-next` is a running concept, not a drop-in replacement for
current production Spirit.

### P2 — generated Rust still uses reusable helper free functions

`schema-rust-next/src/lib.rs:126` through `schema-rust-next/src/lib.rs:181`
emit private helper functions into every generated module:
`parse_nota_root`, `expect_children`, `parse_text`, `format_text`, and
`parse_integer`. The checked fixture confirms those helpers exist at
`schema-rust-next/tests/fixtures/spirit_generated.rs:66` through
`schema-rust-next/tests/fixtures/spirit_generated.rs:145`.

Private local helpers are sometimes legitimate, but this is not just one
module's incidental helper logic. These are reusable generated behaviors that
should become methods or trait impls on generated reader/writer objects, scalar
types, or a data-bearing codec object.

Consequence: the method-on-real-object discipline is documented, but the
emitter does not fully embody it yet.

### P2 — output-source fixture testing is too loose

`schema-rust-next/tests/emission.rs:10` through
`schema-rust-next/tests/emission.rs:27` checks that emitted source contains a
few substrings. It does not compare emitted output byte-for-byte against the
checked fixture included at `schema-rust-next/tests/emission.rs:4` through
`schema-rust-next/tests/emission.rs:7`.

Consequence: formatter drift, missing impl blocks, reordered output, or
accidental helper changes can pass if the broad substrings remain. The intended
three-way witness is: emit exact fixture, compile fixture, run behavior through
fixture.

### P2 — `nota-next` exposes structural pieces but not a reusable shape matcher

`nota-next/src/parser.rs:61` through `nota-next/src/parser.rs:167` exposes
object predicates and child lookup methods. That is the correct recursion
floor. What is missing is a composable matcher API for common macro-position
queries: "parenthesis with two objects", "second object is square bracket",
"all children qualify as symbols", "brace has even key/value entries", and
similar shape contracts.

Consequence: schema macros currently reassemble these checks manually in
`schema-next/src/engine.rs:225` through `schema-next/src/engine.rs:371`.
That keeps the MVP small, but it does not yet provide the reusable NOTA method
library the schema macro system wants.

### P2 — component triad split is not represented in the running pilot

`spirit-next` is one crate containing generated signal data, CLI, daemon,
transport, engine, and store. That is useful for a pilot, but the target shape
is still three repositories: runtime component, ordinary signal schema/contract,
and core/owner signal schema/contract.

Consequence: the pilot proves schema-generated types can cross a daemon
boundary, but it does not yet prove the component-triad dependency shape.

### P3 — tests report green, but current audit did not force fresh builds

I ran:

- `nix flake check` in `nota-next`
- `nix flake check` in `schema-next`
- `nix flake check` in `schema-rust-next`
- `scripts/check-local-schema-stack` in `spirit-next`

All returned `all checks passed`. In this environment, those runs reported
`running 0 flake checks`, which means the command validated the flake outputs
and found no failing check, but did not visibly rebuild the derivations during
this audit run. The stronger prior witness in report 207 did build the
`spirit-next` local override path.

Consequence: current status is green, but future audit automation should have
a no-cache or artifact-producing mode if we need proof that the checks rebuilt
from scratch.

## What Is Implemented Well

`nota-next` is a credible recursion floor: it parses balanced delimiters,
spans, atoms, comments, and pipe text without importing schema semantics.

`schema-next` has the right first public shape: `Asschema` is order-preserving,
fields are private at the canonical root, `MacroPosition` reaches `lower`, and
field names derive from type names.

`schema-rust-next` emits visible Rust source from `Asschema`, not a hidden Rust
macro, and emits rkyv derives, NOTA parse/display methods, and short-header
constants.

`spirit-next` proves a real CLI/daemon process boundary: one NOTA argument at
the CLI edge, length-prefixed frame plus 64-bit header plus rkyv payload on the
socket, generated `Input`/`Output` at both ends, and terse replies.

The local override stack check now gives the right iteration loop: edit
`nota-next`, `schema-next`, or `schema-rust-next`, then run the consumer check
from `spirit-next`.

## Highest-Value Next Slice

The next implementation slice should make one currently hand-written boundary
schema-derived, with a strong Nix witness.

Recommended order:

1. Move the short-header route table and frame codec out of
   `spirit-next/src/transport.rs` into `schema-rust-next` emission.
2. Emit a generated codec object, not free helper functions.
3. Add an exact generated-source fixture comparison in `schema-rust-next`.
4. Update `spirit-next` so transport calls the generated codec and route
   methods.
5. Add a Nix check that fails if `spirit-next` manually matches `Input` or
   `Output` variants for transport routing.

That slice directly closes the largest gap between "schema emits data types"
and "schema creates the interface that lets components talk."

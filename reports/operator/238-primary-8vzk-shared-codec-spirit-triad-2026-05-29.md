# 238 — primary-8vzk shared codec and Spirit triad implementation

## Scope

This pass continued bead `primary-8vzk`: make the current NOTA/schema stack less
pretend and more load-bearing for `spirit-next`.

The working target was:

```text
.schema files
  -> schema-next Asschema data
  -> schema-rust-next emitted Rust source
  -> schema-emitted Signal / Nexus / SEMA nouns
  -> hand-written actor methods over those nouns
  -> real CLI + daemon over rkyv frames + durable .sema database
```

I also folded in the actionable findings from
`reports/designer/425-implementation-avoidance-audit/1-findings.md`.

## Landed repos

`nota-next`

- Commit `c5894905` — `nota: add shared value codec`.
- Added shared `NotaDecode` / `NotaEncode` over `nota_next::Block`.
- Added shared structural support for `String`, `u64`, `bool`, `Vec<T>`,
  `BTreeMap<K,V>`, and `Option<T>`.

`schema-next`

- Commit `f1761b72` — `schema: replace witness goldens with typed assertions`.
- Commit `72a573ab` — `schema: add Path scalar reference`.
- Commit `bd85ca0f` — `schema: refresh triad design example names`.
- Removed `.witness.txt` fixture dependence and added Nix guards against it.
- Added `TypeReference::Path` as a reserved scalar alongside `String`,
  `Integer`, and `Boolean`.
- Removed stale `SemaCommand` / `SemaResponse` names from the design test in
  favor of `SemaInput` / `SemaOutput`.

`schema-rust-next`

- Commit `90b91309` — `schema-rust: use shared nota codec emission`.
- Commit `415482cf` — `schema-rust: encode mail support identifiers with shared codec`.
- Commit `c1fc8674` — `schema-rust: emit Path scalar alias`.
- Commit `fc4ab0ee` — `schema-rust: advance schema-next design example cleanup`.
- Generated Rust now imports the shared `nota-next` codec surface instead of
  emitting a private reader per generated file.
- Generated schema types implement `NotaDecode` / `NotaEncode`; compatibility
  inherent methods remain.
- Generated support identifiers (`MessageIdentifier`, `OriginRoute`) now use
  the same codec path.
- Removed the line-format witness fixtures and the old local helper surface.

`spirit-next`

- Commit `01e130dd` — `spirit: regenerate triad runtime from current schema stack`.
- Rewrote `schema/lib.schema` into current pipe declaration syntax.
- Regenerated checked-in `src/schema/lib.rs` from `schema-rust-next`.
- Updated flake locks to the current schema stack.
- Updated docs and Nix guards away from old executor / in-memory / bracket
  declaration wording.

## Proof

Substrate checks:

- `nota-next`: `cargo test`; `nix flake check`.
- `schema-next`: `cargo test`; `nix flake check`; later design-only cleanup
  also passed `cargo test --test design_examples` and `nix flake check`.
- `schema-rust-next`: `cargo test`; `nix flake check --option builders '' --max-jobs 2`.

Consumer checks:

- `spirit-next`: `cargo test`.
- `spirit-next`: `nix flake check --option builders '' --max-jobs 2`.
- `spirit-next`: `scripts/check-local-schema-stack --option builders '' --max-jobs 2`.
- `spirit-next`: `NIX_CONFIG='builders =' scripts/run-nix-integration-tests`.

The last command ran the actual ignored Nix integration tier:

```text
9 passed; 0 failed
```

Those tests build the Nix package, launch the Nix-built daemon, invoke the
Nix-built CLI, send real rkyv frames over a Unix socket, parse CLI stdout back
through schema-emitted `Output::from_str`, and verify durable `.sema` behavior.

## What 425 now says after implementation

Resolved:

- The shared codec gap is no longer in-progress; generated readers use the
  shared `nota-next` traits.
- `.witness.txt` line-format goldens are deleted and guarded against in both
  schema repos.
- The scalar `Path` gap is implemented in `schema-next` and emitted by
  `schema-rust-next`.
- The stale `SemaCommand` / `SemaResponse` example names are removed.

Still open:

- The roots model is not implemented. `Asschema` still has the fixed
  `input` / `output` pair plus namespace, rather than `roots:
  Vec<RootDeclaration>`.
- Mail support nouns (`MessageSent`, `NexusMail`, `MessageProcessed`,
  `OriginRoute`) are still generated support surface, not authored shared core
  schema.
- Upgrade/diff logic remains only trait surface and tests, not real database
  migration behavior.

## My critique

This is now a real bootstrap slice, not an implementation-avoidance slice. The
tests are anchored in data and process boundaries:

- `.schema` files are real fixtures.
- lowering yields typed `Asschema`, not text witnesses.
- Rust source is emitted and checked in.
- runtime behavior uses generated nouns (`signal::Input`, `nexus::Input`,
  `sema::Input`, `schema::Plane`, `MailLedgerEvent`, `DatabaseMarker`).
- the CLI/daemon proof crosses a real Unix socket with rkyv bytes and a durable
  `.sema` file.

The biggest remaining architectural mismatch is roots. The current generated
runtime is useful and working, but the assembled schema model is still shaped
around the older fixed reactive pair. The next serious model pass should change
Asschema first, then make Spirit consume that model, instead of adding more
runtime code on top of the fixed pair.

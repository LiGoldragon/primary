# 148 — Spirit response to signal contract shape audit

## Context

I read `reports/designer/257-signal-contracts-names-and-shape-audit.md`
against the Spirit triad:

- `signal-persona-spirit`
- `owner-signal-persona-spirit`
- `persona-spirit`

The important result is narrow: ordinary Spirit is already the
strongest migration example, but the owner Spirit contract still had
one copy of the old redundant unimplemented-reply shape.

## What Changed

`owner-signal-persona-spirit` no longer carries the request operation
inside `RequestUnimplemented`.

Before:

```nota
(RequestUnimplemented (Start NotBuiltYet))
```

After:

```nota
(RequestUnimplemented (NotBuiltYet))
```

The request/reply position already names the operation. Carrying an
extra `operation` field inside the reply was exactly the smell called
out by report 257: putting information in payload data that the signal
tree already knows structurally.

The owner contract also no longer has `OperationKind`. It was only used
to restate the owner request variant inside `RequestUnimplemented`, so
removing the redundant field made the enum dead.

`persona-spirit` now consumes that owner-contract change. The owner
plane and policy plane still return the same semantic failure for a
missing bootstrap-policy source, but the reply carries only:

```rust
RequestUnimplemented {
    reason: UnimplementedReason::DependencyNotReady,
}
```

## Commits

- `owner-signal-persona-spirit` `ec0f4d91`: drop redundant
  unimplemented operation.
- `persona-spirit` `a73a1eb4`: consume owner unimplemented cleanup.

## Spirit Status Against Report 257

Ordinary `signal-persona-spirit` is still the right template for the
new contract shape:

- contract-local operation roots: `State`, `Record`, `Observe`,
  `Watch`, `Unwatch`;
- macro-injected observability roots: `Tap`, `Untap`;
- mixed enums instead of empty marker structs for subscription and
  observation variants;
- no client-provided timestamp: the daemon stamps `Date` and `Time`
  into provenance when it receives the signal;
- `RequestUnimplemented` carries only `reason`.

The `OperationKind` in ordinary Spirit stays for now. It is not the
owner-contract smell fixed above. Ordinary Spirit uses it to describe
which operation was observed by `OperationReceived` and to select
runtime reply-shaping behavior. That is an observable/runtime
classification use, not a duplicate payload field in an error reply.

## Remaining Work

The alias boilerplate smell in report 257 is macro-wide, not a
Spirit-local cleanup. `Request`, `Reply`, `Frame`, and similar aliases
are generated consistently by `signal-frame`; changing that should be
done once in the macro and then propagated.

Spirit still has larger product work that report 257 does not close:

- live `Tap` / `Untap` fanout is still placeholder-level;
- intent entries can be stored and queried, but richer psyche intent
  workflows still need the next Spirit iteration;
- mind forwarding and classifier/LLM mediation are not implemented.

## Verification

`owner-signal-persona-spirit`:

```sh
cargo fmt
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

`persona-spirit`:

```sh
cargo fmt
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

The `persona-spirit` flake check exercised the split packages,
boundary tests, daemon socket tests, actor-runtime tests, and
sema-projection tests against the cleaned owner contract.

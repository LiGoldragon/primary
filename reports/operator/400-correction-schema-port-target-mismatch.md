# Correction — Schema Port Target Mismatch

## What went wrong

The operator sweep mixed up two targets:

1. **Implemented mainline schema stack** — current `nota-next`, `schema-next`,
   `schema-rust-next`, schema-cc generated resolver, positional syntax, generated
   standard scalar newtype impls, and current NOTA canonicalization.
2. **New trait / impl schema language design** — the `{| |}` trait/impl
   construct, generic frame expansion as the component-codegen path, and any
   method/body-as-data frontier.

The sweep ported repositories to target 1. The psyche was asking for target 2.

That means the statement "port to the latest schema design" was answered with
"port to the latest implemented mainline schema stack." That was not precise
enough and became false once the conversation's intended target was the
trait/impl design.

## Actual implementation state

Implemented on code-repo main and safe to call shipped:

- schema-cc co-located in `schema-next` and generating the live parenthesis
  reference resolver.
- current positional schema syntax and current NOTA canonical string rules.
- schema-rust standard generated scalar newtype impls where already supported.
- component repos refreshed to compile/test against current mainline
  `schema-next` / `schema-rust-next` / `nota-next` where the sweep touched them.

Not implemented on main and not valid to call shipped:

- trait declarations as usable schema syntax.
- `{| |}` trait/impl parsing/lowering/emission in schema-next/schema-rust-next.
- component schemas rewritten to trait/impl declarations.
- method bodies as schema data beyond prototype/demonstration branches.
- component-wide codegen replacement of hand-written trait/impl surfaces.

## Dirty state at pause

Two code repos have uncommitted operator/subagent work from the mistaken sweep:

- `/git/github.com/LiGoldragon/agent`
  - dirty: `Cargo.lock`
  - nature: local dependency refresh toward current agent contracts and schema
    compiler pins; command was interrupted before final Nix result/commit.
- `/git/github.com/LiGoldragon/harness`
  - dirty: `Cargo.lock`, `src/configuration.rs`, `src/supervision.rs`
  - nature: subagent follow-up to consume `signal-harness` `64642c04`; cargo
    check passed after local source fixes, but tests failed in
    `tests/message_router_harness_e2e.rs` on old startup type construction.
  - not committed, not pushed.

Do not treat either as landed.

## What should happen next

Stop broad component porting.

The correct next technical slice is:

1. Define the smallest implemented trait/impl schema slice in `schema-next` and
   `schema-rust-next`.
2. Prove it in one repo with a real schema and generated Rust, not a report-only
   prototype.
3. Run cargo + Nix gates.
4. Only then begin porting components to that new syntax.

The component sweep ledger remains useful as a maintenance record, but it is not
evidence that trait/impl schema design has landed.

## Operator accountability

The failure was not in the tests. The failure was target selection and language:
I reported "latest schema design" when I should have said "latest implemented
mainline schema stack." That hid the fact that trait/impl syntax was not on
main. Future updates must name which surface is being updated:

- implemented mainline stack;
- prototype/design branch;
- or newly landed trait/impl schema support.

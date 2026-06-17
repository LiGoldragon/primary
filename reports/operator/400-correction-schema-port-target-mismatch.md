# Correction — Schema Port Target Mismatch

## What went wrong

The operator sweep mixed up two targets:

1. **Implemented mainline schema stack** — current `nota-next`, `schema-next`,
   `schema-rust-next`, schema-cc generated resolver, positional syntax, generated
   standard scalar newtype impls, and current NOTA canonicalization.
2. **The component-codegen schema design** — the `(| |)` generic frame path
   for declaring reusable interface frames, plus any later `{| |}` role /
   implementation relationship frontier.

The sweep ported repositories to target 1. The psyche was asking for target 2.

That means the statement "port to the latest schema design" was answered with
"port to the latest implemented mainline schema stack." That was not precise
   enough and became false once the conversation's intended target was the
   component-codegen design.

## Actual implementation state

Implemented on code-repo main and safe to call shipped:

- schema-cc co-located in `schema-next` and generating the live parenthesis
  reference resolver.
- current positional schema syntax and current NOTA canonical string rules.
- schema-rust standard generated scalar newtype impls where already supported.
- `(| |)` generic frame declaration/application support in `schema-next`, with
  reaction-frame lowering and expansion tests green.
- `schema-rust-next` emission for generic frame declarations and application
  roots, with targeted reaction-frame tests green.
- component repos refreshed to compile/test against current mainline
  `schema-next` / `schema-rust-next` / `nota-next` where the sweep touched them.

Implemented/proven in the Designer `reaction-expand` worktrees, but **not
integrated on code-repo main**:

- pipe-brace role/marker relationship syntax such as
  `EntryHandleIsAuditable {| Auditable EntryHandle |}`.
- opt-in mechanical `Deref` body data such as
  `(reference (field self payload))`.
- the fixture proof in
  `/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand/tests/pipe_delimiter_demo.rs`.

Not integrated on main and not valid to call shipped:

- the `reaction-expand` trait/role relationship slice.
- component schemas rewritten to use the proven frame/role syntax.
- component-wide codegen replacement of hand-written role/trait surfaces.
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

1. Use the already-main `(| |)` frame path as the port target.
2. Keep the next slice narrow: component schemas should adopt frame expansion
   and generated structural surfaces; do not chase arbitrary implementation
   bodies.
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
- or newly landed schema support for a specific construct.

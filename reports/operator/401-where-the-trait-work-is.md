# 401 — Where the trait work is

## Short answer

The `(| |)` generic-frame work is real and is on code-repo main. The stranded
work is the later `{| |}` role / implementation relationship prototype, which
is not the current port target.

- `schema-next` worktree:
  `/home/li/wt/github.com/LiGoldragon/schema-next/reaction-expand`
- `schema-rust-next` worktree:
  `/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand`

The current code-repo mains contain the generic frame path and standard
structural emission. They do not contain the `reaction-expand` pipe-brace
relationship syntax as a shipped surface.

## What was built

The relevant mainline slice is not "full Rust trait declarations" and not a
general method language. The useful built work is:

- generic frame declarations with `(| |)`;
- component bindings that expand those frames into concrete owned `Input` /
  `Output` enums;
- generated Rust engine traits and runtime support from the schema target;
- scalar newtype standard impls where enabled.

The later prototype work, not on main, also includes:

- pipe-brace role/marker relationships such as
  `EntryHandleIsAuditable {| Auditable EntryHandle |}`;
- opt-in mechanical `Deref` where the body is a tiny shape-proven expression
  tree, e.g. `(reference (field self payload))`.

The proof fixture is:

`/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand/tests/fixtures/pipe-demo/schema/ledger.schema`

It contains:

```nota
EntryHandleIsAuditable {| Auditable EntryHandle |}
EntryHandleDeref {| Deref EntryHandle [ (deref (reference (field self payload))) ] |}
```

The witness test is:

`/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand/tests/pipe_delimiter_demo.rs`

It asserts that the schema emits:

```rust
impl Auditable for EntryHandle {}

impl std::ops::Deref for EntryHandle {
    type Target = Statement;
    fn deref(&self) -> &Self::Target { &self.0 }
}
```

and then compiles and exercises the generated code.

## What is on main

`/git/github.com/LiGoldragon/schema-next` main has:

- `Root::Application` and `RootApplication`;
- `Schema::declared_frame_body`;
- `Schema::expand_application_root`;
- reaction-frame and generics tests.

`/git/github.com/LiGoldragon/schema-rust-next` main has:

- generic reaction-frame emission tests;
- application-root lowering that expands a frame root into a concrete root enum
  when the frame resolves;
- scalar standard-newtype impl tests.

Targeted verification on June 17, 2026:

- `schema-next`: `cargo test --test reaction --test generics` passed
  23 tests.
- `schema-rust-next`:
  `cargo test --test reaction_frame_emission --test standard_newtype_impls`
  passed 7 tests.

## What I got wrong

I used "not done" to mean "the pipe-brace relationship prototype is not on
main." That was the wrong object. The `(| |)` generic-frame work is on main.
The missing step is component porting onto that mainline path.

I also let the internal noun `ImplDeclaration` confuse the conversation. In the
prototype, that is the Rust struct name for the lowered pipe-brace relationship
object. The psyche-facing concept is role/trait relationship syntax, not a
mandate to design a broad implementation language.

## Actual next step

Stop chasing the pipe-brace implementation path for this port. Use current
`schema-next` and `schema-rust-next` main, preserving the narrow scope from
reports 397 and 666:

1. frame expansion;
2. scalar standard impls default-on where already proven;
3. generated structural interface surfaces;
4. then one component port and full cargo/Nix proof.

Only after that is green should the rest of the components be ported.

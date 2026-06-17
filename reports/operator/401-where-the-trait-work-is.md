# 401 — Where the trait work is

## Short answer

The work is real, but it is stranded on worktrees/feature changes rather than
main.

- `schema-next` worktree:
  `/home/li/wt/github.com/LiGoldragon/schema-next/reaction-expand`
- `schema-rust-next` worktree:
  `/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand`

The current code-repo mains do not contain that slice. They contain the latest
implemented mainline compiler stack, but not the `reaction-expand` role/trait
relationship syntax as a shipped surface.

## What was built

The relevant slice is not "full Rust trait declarations" and not a general
method language. The useful built work is:

- generic frame declarations with `(| |)`;
- component bindings that expand those frames into concrete owned `Input` /
  `Output` enums;
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

`/git/github.com/LiGoldragon/schema-next` main is at `abae95f9`
(`schema-next: refresh nota dependency`). It has pipe-brace as a recognized
delimiter and architecture text about the future trait/impl construct, but not
the `reaction-expand` implementation.

`/git/github.com/LiGoldragon/schema-rust-next` main is at `e2e20b66`
(`schema-rust-next: refresh schema dependency`). It has current runtime
role-trait codegen and standard schema emission, but not the pipe-brace
relationship slice from `reaction-expand`.

## What I got wrong

I used "not done" to mean "not on main." That was the wrong word. The work was
done as executable prototype/worktree material and documented as proven. The
missing step is mainline integration and component porting.

I also let the internal noun `ImplDeclaration` confuse the conversation. In the
prototype, that is the Rust struct name for the lowered pipe-brace relationship
object. The psyche-facing concept is role/trait relationship syntax, not a
mandate to design a broad implementation language.

## Actual next step

Stop the broad component sweep. Harvest `reaction-expand` onto current
`schema-next` and `schema-rust-next` main, preserving the narrow scope from
reports 397 and 666:

1. frame expansion;
2. scalar standard impls default-on where already proven;
3. role/marker relationship emission;
4. opt-in mechanical `Deref`;
5. typed errors for unsupported emitter cases;
6. then one component port and full cargo/Nix proof.

Only after that is green should the rest of the components be ported.

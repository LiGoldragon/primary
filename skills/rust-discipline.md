# Skill — Rust discipline (index)

*Behavior lives on types. Domain values are typed. Boundaries take
and return one object. Errors are enums you implement by hand.*

---

## What this skill is for

This is the index for Rust discipline in the workspace. The
substance lives in five focused sub-files under `skills/rust/`;
the cross-cutting Rust applications of `skills/naming.md` and
`skills/actor-systems.md` stay here so the Rust enforcement is
visible at one entry point.

These skills are *how to write* Rust in this workspace. For the
canonical interactive/user-profile Rust toolchain, see
CriomOS-home's `packages/rust-toolchain/default.nix` and
`skills.md`. For per-repo Rust crate shape (Cargo.toml shape,
cross-crate dependencies, pin strategy, Nix packaging), see
lore's `rust/style.md` and `rust/nix-packaging.md`.

---

## The rules in one sentence

**Behavior lives on types. Domain values are typed. Boundaries
take and return one object. Errors are enums you implement by
hand.**

---

## Toolchain Authority

The workspace-wide interactive Rust toolchain is owned by
CriomOS-home, not by Primary and not by ad hoc repo devshells.
The canonical package is
`CriomOS-home.packages.<system>.rust-toolchain`, defined at
CriomOS-home's `packages/rust-toolchain/default.nix` and pinned by
`CriomOS-home/flake.lock`.

User profiles should install that package rather than bare
`pkgs.cargo`, `pkgs.rustc`, `pkgs.rustfmt`, or hand-picked Rust
components. It provides `cargo`, `rustfmt` / `cargo fmt`,
`clippy`, `rust-analyzer`, and `rust-src` for day-to-day agent
work.

Individual Rust application repos may still pin their own build
toolchain through their flake when reproducibility requires it.
That repo-local build pin does not become the profile toolchain
authority.

---

## Sub-files

| Sub-file | Covers |
|---|---|
| `skills/rust/methods.md` | methods-on-types, no ZST holders, domain newtypes, one-type-per-concept, no string typification, one-object-in-out, constructors, trait domains, direction-encoded names |
| `skills/rust/errors.md` | typed `Error` enum per crate via `thiserror` |
| `skills/rust/storage-and-wire.md` | redb + rkyv durable state and binary wire (signaling, NOTA projection, anti-patterns, sema-family) |
| `skills/rust/parsers.md` | no hand-rolled parsers; use a real library |
| `skills/rust/crate-layout.md` | CLIs as daemon clients, one crate per repo, tests in separate files, module layout, documentation |

---

## Naming — full English words

The cross-language rule, the offender table, and the six permitted
exception classes live in `skills/naming.md`. Rust enforcement
keeps `self` as the implicit receiver (universal across the
language; leave it) and applies the rule to everything else you
create:

```rust
// Wrong — cryptic in-group dialect
let mut lex = Lexer::new(input);
let tok = lex.next_tok()?;
let kd = tok.kind();
let ctx = ParseCtx::new(&kd);
let de = Deser::with_ctx(ctx);

// Right — every name reads as English
let mut lexer = Lexer::new(input);
let token = lexer.next_token()?;
let kind = token.kind();
let context = ParseContext::new(&kind);
let deserializer = Deserializer::with_context(context);
```

---

## No crate-name prefix on types

The cross-language rule lives in `skills/naming.md` §"Anti-pattern:
prefixing type names with the crate name". Rust applies it without
exception — the Rust API Guidelines call this **C-CRATE-PREFIX**,
and the standard library is the canonical reference (`Vec`,
`HashMap`, `Arc`, `Cell`, `Mutex` — never `StdVec`, `StdHashMap`,
`StdArc`). Workspace pattern: `signal::Request`, `chroma::Error`;
never `SignalRequest` or `ChromaError`.

---

## Actors: logical units with kameo

When a Rust component is a daemon, state engine, router, watcher,
delivery engine, database owner, or long-lived service, the
workspace's actor discipline (`skills/actor-systems.md`) and the
Kameo framework usage (`skills/kameo.md`) carry the rules. Read
both before writing the runtime. The reason to use actors is
**logical cohesion**, not performance: an actor is the unit you
reach for when you want a coherent plane of logic with owned state,
a typed message protocol, and a defined lifecycle.

Rust-side enforcement summary:

- Actor type carries data fields (Kameo's `Self IS the actor`); no
  public ZST actor nouns.
- One `impl Message<Verb> for Actor` per verb; no monolithic `Msg`
  enum, no untyped channels.
- One actor per file when the actor is durable enough to name.
- Handlers do not block. Use `DelegatedReply<R>` or a dedicated
  blocking-plane actor; see `skills/kameo.md` §"Blocking-plane
  templates" for the three concrete shapes.
- Never `tell` a handler whose `Reply = Result<_, _>` unless
  `on_panic` is overridden (see `skills/kameo.md` §"The
  tell-of-fallible-handler trap").
- No `Arc<Mutex<T>>` between actors — send a message to whoever
  owns the state.
- Errors at component boundaries are the crate's typed `Error`
  enum (per `skills/rust/errors.md`), never `anyhow`/`eyre`.
- The default public consumer surface is `ActorRef<MyActor>`;
  domain wrappers earn their place per `skills/kameo.md` §"Public
  consumer surface — ActorRef<A> or domain wrapper".

Plain sync code is fine for stateless one-shot CLIs, build tools,
and library crates with no concurrent state. If a CLI needs durable
state, supervision, subscriptions, or shared runtime context, it is
a daemon client per `skills/rust/crate-layout.md` §"CLIs are daemon
clients".

---

## See also

- `skills/rust/methods.md` — methods/types/objects discipline.
- `skills/rust/errors.md` — typed Error enum per crate.
- `skills/rust/storage-and-wire.md` — redb + rkyv.
- `skills/rust/parsers.md` — no hand-rolled parsers.
- `skills/rust/crate-layout.md` — crate organization, CLIs as
  daemon clients.
- `skills/abstractions.md` — cross-language methods-on-types rule.
- `skills/naming.md` — cross-language naming, framework-category-
  suffix anti-pattern.
- `skills/actor-systems.md` — actor discipline.
- `skills/kameo.md` — Kameo 0.20 framework usage.
- `skills/beauty.md` — beauty as criterion.
- `skills/micro-components.md` — one capability per crate per repo.
- `lore/rust/style.md` — Cargo.toml, cross-crate deps, pin strategy.
- `lore/rust/rkyv.md` — rkyv tool reference.
- `lore/rust/nix-packaging.md` — crane + fenix flake layout.
- `/git/github.com/LiGoldragon/kameo-testing` — worked Kameo examples.

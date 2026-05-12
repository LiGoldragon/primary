# Skill — Rust crate layout

*CLIs are daemon clients. One Rust crate per project per repo.
Tests live in separate files. One concern per file.*

---

## What this skill is for

When organizing a Rust crate's surface — CLI vs daemon, source
file structure, test placement, module layout, documentation —
this skill is the discipline.

For the index pointing at the wider Rust discipline, see
`skills/rust-discipline.md`.

---

## CLIs are daemon clients

Command-line interfaces in this workspace are clients. When a tool
needs durable state, supervision, subscriptions, long-lived actors,
or shared runtime context, that state lives in a daemon and the CLI
talks to it. Do not reopen "one-shot CLI owns the runtime" as an
architecture option unless the user explicitly asks to break this
rule.

Shape:

- daemon owns the root actor, durable database, subscriptions, and
  runtime lifecycle;
- CLI parses one input object, sends a typed request to the daemon,
  waits for one typed reply, renders it, and exits;
- tests may use in-process harnesses for speed, but production
  architecture stays daemon-first.

Every non-contract stateful component or daemon exposes a thin CLI
control surface, even when the CLI is not user-facing. The CLI is a
test and operations boundary: it parses one typed input object,
sends the component's production request to the daemon, prints one
typed reply or artifact path, and exits. It does not own durable
state, open the component database directly, or bypass the daemon's
actor/message path.

Read-only inspection CLIs are the narrow exception. A component may
ship an explicitly named inspection client that opens the component's
Sema database to render test artifacts or operational state. It must
not mutate state, allocate identity, drive effects, or become the
production request path; effect-bearing commands still go through the
daemon.

Contract crates are the exception: they are libraries of typed
wire vocabulary. They do not need a daemon CLI merely to be
testable; their tests are round-trip, schema, and compile-time
witnesses unless they deliberately ship a generator or inspection
tool.

Example: the Persona command-line mind is `mind` as a thin client to
the long-lived `persona-mind` daemon. The daemon owns `MindRoot` and
`mind.redb`; the CLI owns argv/env decoding and reply rendering.

---

## One Rust crate per repo

Rust crates live in their own dedicated repos and are consumed
via flake inputs. Don't inline a Rust crate inside a non-Rust
repo (e.g. under a NixOS-platform repo's `packages/`). A Rust
crate has its own toolchain pin, its own Cargo lockfile, its own
test surface, its own release cadence, and its own style
obligations. Inlining one inside a heterogeneous repo couples
those concerns to the host repo's churn for no gain. Consume via
flake input instead.

A workspace of related Rust crates (e.g. lib + cli) belongs in
**one** repo together. The split is per *project*, not per crate.

**Cross-crate Cargo.toml deps use `git = "..."`, never `path
= "../..."`.** A repo's Cargo.toml that references a sibling
repo via `path = "../sibling"` makes the repo non-portable —
fresh clones don't reproduce, Cargo.lock doesn't pin the rev,
nix flake check can't fetch through the sandbox. The
canonical home for this rule is `skills/micro-components.md`
§"Cargo.toml dependencies"; this section is the Rust crate's
side of the same rule.

For the toolchain reference (Cargo.toml conventions, cross-crate
dependencies, git-URL deps, pin strategy), see lore's
`rust/style.md`.

---

## Tests live in separate files

Unit tests do **not** go in a `#[cfg(test)] mod tests` block at
the bottom of the source file. They live in a sibling file under
`tests/` at the crate root, named for the module they exercise.

```
src/
├── cert.rs
├── tree.rs
└── error.rs
tests/
├── cert.rs      # integration tests for Cert
└── tree.rs      # integration tests for Tree
```

This keeps the source file focused on behavior, lets the test
file grow without bloating the source file, and forces tests to
exercise the public API (integration tests can't reach private
items — which is the right pressure: if something is hard to test
from outside, the API needs work, not the test). Private-helper
tests are rare and can go in a small `tests_internal` module with
a clear boundary; if you find yourself reaching for many, that's
a signal the helper wants to be its own type with a public
constructor.

One test file per source file. Don't collect tests from multiple
modules into a single `tests/common.rs` unless the shared
fixtures genuinely apply to more than one module.

---

## Module layout

One concern per file. Typical crate:

```
src/
├── lib.rs        # re-exports + crate-level doc (//!)
├── error.rs      # Error enum + impls
├── types.rs      # domain newtypes + small structs
├── <thing>.rs    # one file per major type / subsystem
└── main.rs       # only if the crate is a binary; only free fn lives here
```

Impls live in the same file as the type they're for. Don't split
types and impls across files.

### Split traits into their own files when they accumulate

When a single file grows past ~300 lines because traits have
piled up on a type, split each trait impl into its own file. The
file for a type holds the type definition + its inherent impls;
each separate file holds one trait impl for that type, named for
the trait.

```
src/cert/
├── mod.rs              # type definition + inherent impls (Cert::new, fields)
├── from_str.rs         # impl FromStr for Cert
├── display.rs          # impl Display for Cert
├── try_from_pem.rs     # impl TryFrom<Pem> for Cert
└── serde_impls.rs      # impl Serialize + Deserialize for Cert (paired traits)
```

This is the deliberate trade-off **explicit code is fine; long
files are not**. Splitting trait impls into separate files keeps
any single file readable, makes the type's surface discoverable
from the directory listing, and prevents impl blocks from growing
into a wall of unrelated behavior.

Use this pattern when traits accumulate. Don't pre-split a type
with two trait impls — that's premature ceremony. Split when a
file is becoming hard to navigate.

---

## Documentation

Doc comments are impersonal, timeless, precise. Document the
contract; don't restate the signature.

```rust
impl Cert {
    /// Issue a server certificate against this CA.
    ///
    /// The CA's signing key must be an Ed25519 key resolvable via the
    /// local GPG agent. The server keypair is ECDSA P-256, generated fresh.
    pub fn issue_server(&self, request: ServerCertRequest) -> Result<Self, Error> { … }
}
```

Module-level docs go in `//!` at the top of `lib.rs` or `///` at
the top of a single-purpose module file. Skip docs on obvious
boilerplate: getters, `From` impls, internal helpers.

No examples in doc comments unless the API is non-obvious. No
personal voice. No future tense. Present indicative only.

---

## See also

- `skills/rust-discipline.md` — Rust discipline index.
- `skills/micro-components.md` — one capability per crate per repo.
- `lore/rust/style.md` — Cargo.toml conventions, cross-crate
  deps, pin strategy.
- `lore/rust/nix-packaging.md` — crane + fenix flake layout.
- `skills/rust/methods.md` — what goes inside the source files.

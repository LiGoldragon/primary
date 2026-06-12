# CODING discipline — implementer checklist

A held-in-context distillation of the Rust + schema rules for the
lojix production refresh. Source files (all settled at the
`027c5c1f` tight-teaching corpus rewrite, 2026-06-07; `naming.md`
also touched `a2728b25` 2026-06-08 for a Spirit-contract rename
only — no CODING drift since):
`skills/rust-discipline.md` + `skills/rust/{methods,errors,storage-and-wire,parsers,crate-layout}.md`,
`skills/abstractions.md`, `skills/actor-systems.md`,
`skills/enum-contact-points.md`, `skills/naming.md`,
`skills/kameo.md`, `skills/typed-records-over-flags.md`.

## Non-negotiables (hard fails)

- [ ] **Method-only — no free functions.** Every production `fn`
  (including `const fn` / `async fn`) is a method/associated fn on a
  non-zero-sized data-bearing type, or a trait impl. Only exemptions:
  `fn main()` and `#[cfg(test)]`. No module-level helpers, no private
  module-scope `fn` — even a small private helper goes inside an
  `impl`. (`rust/methods.md` §"Methods on types"; the local-helper
  carve-out from `abstractions.md` does NOT apply in Rust.)
- [ ] **No ZST namespace holders.** `pub struct Foo; impl Foo { fn
  work(data) }` is a free function in disguise. Test: erase the
  type's name from the type system — if its job vanishes, it was a
  namespace; find/invent the real owning noun. Legit ZSTs are narrow:
  `PhantomData`, external-framework markers (trait-impl methods only,
  delegating to a data-bearing partner), type-level state-machine
  positions. (`rust/methods.md` §"No ZST method holders".)
- [ ] **Typed domain values, not primitives.** A value with identity
  beyond its bits gets a newtype (`Md5([u8;16])`, not `String`). The
  wrapped field is **private**; construction via `new`/`TryFrom`,
  access via `AsRef`. No `pub` inner field. (`rust/methods.md`
  §"Domain values are types".)
- [ ] **Typed per-crate `Error` enum via `thiserror`.** Each crate
  owns `src/error.rs` with structured variants carrying message data;
  foreign errors convert via `#[from]`. **`anyhow`/`eyre`/`Box<dyn
  Error>` never cross a component boundary** — they erase the type and
  kill pattern-matching. (`rust/errors.md`.)
- [ ] **No hand-rolled parsers.** Any named format (JSON, TOML, YAML,
  XML, PEM, DER, base64, hex, HTTP, URL…) uses a real library — never
  `find()`/`split()`/slice chains. Carve-outs only: single-char
  `split(',')`, `parse::<u64>()`, `lines()` with no nesting/escapes/
  quoting. Novel format ⇒ its own parser crate with a typed API.
  (`rust/parsers.md`.)
- [ ] **redb + rkyv for storage and wire.** In-process = typed Rust
  values (no serialization). Process↔process = **rkyv** length-prefixed
  archives, validated on receive via `rkyv::access`. Durable state =
  **redb tables of rkyv values**, one redb file per component, through
  the component-owned Sema layer. NOTA text is a human-facing
  *projection*, never the inter-component wire and never re-parsed in
  the daemon. No `serde_json` between Rust components.
  (`rust/storage-and-wire.md`.)
- [ ] **No blocking in actor handlers.** Sleeping, mutex/RwLock blocks,
  blocking IO/process/CPU, polling, sync waits on callback-capable
  actors are forbidden inside a normal handler — the mailbox stops and
  becomes a hidden lock. Move the wait into a dedicated supervised
  actor; pick one of the three kameo blocking-plane templates by shape
  (`spawn_blocking`+`DelegatedReply` / dedicated OS thread /
  `tokio::process`+timeout). No `Arc<Mutex<T>>` between actors — send a
  message to the state's single owner. (`actor-systems.md` §"Blocking
  is a design bug", §"No shared locks".)
- [ ] **Enum-vs-enum contact points are named.** When two enums meet
  under `match`, the cross-product IS the relationship — make it a
  nested `match` or a named trait (`Reaches<Right>`, `Contact<Other>`,
  `Dispatch<Token>`). Never spread the matrix across `if` chains,
  string predicates (`starts_with`), sentinel `u8`s, or boolean flags.
  Trait earns ceremony at >~8 cells or multi-site reuse; otherwise a
  nested `match`. (`enum-contact-points.md`.)
- [ ] **Schema-emitted nouns own the methods.** In the schema-derived
  stack the schema declares the types (`Input`/`Output`, operation
  payloads, `SemaCommand`/`SemaResponse`, route/header enums); emitted
  Rust gives declarations + codecs + dispatch tables; **agent-written
  Rust attaches behavior as methods on those emitted nouns**. Don't
  hand-edit generated mirrors — change the `.schema` and regenerate.
  Don't write free functions taking emitted types as args. Engine
  traits (`SignalEngine`/`NexusEngine`/`SemaEngine`) impl on REAL
  data-bearing types, never ZST namespaces. (`abstractions.md`
  §"Schema-emitted nouns"; `actor-systems.md` §"Engine traits".)
- [ ] **Full-English identifiers; no redundant ancestry.** Spell every
  name as an English word (`identifier` not `id`, `lexer` not `lex`,
  `context` not `ctx`) — six narrow exceptions only. AND drop ancestry
  the namespace already supplies: `Request` not `ChromaRequest`,
  `Entry` not `IntentEntry`, `size` not `profileSize` inside
  `Profile`. No crate-name prefixes (C-CRATE-PREFIX), no
  framework-category suffixes (`*Actor`, `*Message`, `*Handler`).
  Repeated category words across siblings (`*Query` ×5) are schema
  smells wanting a parent enum. (`naming.md`.)
- [ ] **kameo lifecycle.** `Self` IS the actor (`type Args = Self`),
  data fields on the actor type, one `impl Message<Verb> for Actor`
  per verb (no monolithic `Msg` enum). One actor per file when durable
  enough to name; tests in `tests/`. Supervision is declarative and
  part of the design — every actor in a tree with a typed failure
  policy. **Never `tell` a fallible handler** (`Reply = Result<_,_>`)
  unless `on_panic` recovers `PanicReason::OnMessage` — it crashes the
  actor by default; `ask` instead. **Restart reconstructs from `Args`,
  not memory** — durable state lives in sema/redb (default
  `RestartPolicy::Never` for transient state). Release owned resources
  BEFORE death notifications; wait on `wait_for_shutdown()` terminal
  outcome, never `is_alive()`/mailbox closure. (`kameo.md`,
  `actor-systems.md`.)

## Companion rules

- [ ] **Typed records over flags.** A `bool` whose "yes" carries data
  is a hidden record — use `Option<Record>`, sum enum with data
  variants, or a typed enum replacing a multi-flag struct. Booleans
  with no payload (`online: bool`) stay. (`typed-records-over-flags.md`.)
- [ ] **One object in, one object out.** Methods take ≤1 explicit
  object arg (`self` implicit) and return one object; multi-arg ⇒
  define a struct. No anonymous tuples at type boundaries (tuple
  newtypes OK). Verb on the input (`Request::download`), not a free
  fn. (`rust/methods.md` §"One object in".)
- [ ] **One concept = one type.** No `-Details`/`-Info`/`-Extra`/`-Raw`
  companion-type pairs; fix the thin base type, project via a method
  (`item.summary()`) not a parallel struct. (`rust/methods.md` §"One
  type per concept".)
- [ ] **Don't hide typification in strings.** No `starts_with("m-")`
  dispatch, no string-prefix kind checks — use a sum enum. The system
  mints identity/commit-time/sender; the agent supplies only content.
  (`rust/methods.md` §"Don't hide typification".)
- [ ] **Use existing trait domains.** `FromStr`/`Display`/`From`/
  `TryFrom`/`AsRef`/`Iterator` over inherent reinventions. Constructors
  are associated fns (`new`/`with_*`/`from_*`/`build`). Direction-encoded
  names (`from_*`/`to_*`/`as_*`). (`rust/methods.md`.)
- [ ] **Crate layout.** CLIs are thin daemon clients (parse one object,
  send typed request, render one reply, exit). One Rust crate per repo;
  cross-crate deps via `git = "..."`, never `path =`. Tests in `tests/`
  sibling files, not `#[cfg(test)] mod tests`. One concept per file;
  impls beside their type. (`crate-layout.md`.)
- [ ] **rkyv schema discipline.** Append-only fields; never reorder
  (layout changes silently). Enum variants append last under
  `#[repr(u8)]`; express semantic order via manual `Ord`/`order_rank`,
  never `#[derive(Ord)]` on declaration order. Version-skew guard
  (`schema_version, wire_version`) checked at boot, hard-fail on
  mismatch. Pin the exact rkyv feature set across all crates.
  (`storage-and-wire.md` §"Schema discipline".)
- [ ] **Actors all the way down.** A plane is actor-shaped when it has
  a typed domain name, a failure mode callers act on, and is testable
  with synthetic input. ZST/`State=()` one-shot forwarders are NOT
  actors (the state field names the noun the actor is). Default
  state-bearing substrate is `sema-engine`, not raw `sema`.
  (`actor-systems.md`.)

## Freshness note

No CODING-discipline change since the 2026-06-07 corpus rewrite
(`027c5c1f`). Toolchain authority is
`CriomOS-home.packages.<system>.rust-toolchain`; kameo is **0.20**
(use the `kameo-push-only-lifecycle` fork for the lifecycle contract;
leave the `remote` feature off). Default mailbox capacity is 64 (not
the doc-claimed 1000). `spawn_in_thread` on a supervised state-bearing
actor is a known trap in 0.20 — stay on `.spawn()`.

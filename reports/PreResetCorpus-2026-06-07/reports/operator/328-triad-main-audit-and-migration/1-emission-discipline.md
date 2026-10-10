# triad_main audit — dimension 1: emission discipline

Audit of the emitted daemon module (`triad_main`, designs 542/543) against
standard **4np2** (schema→Rust lowering uses real Rust macro infrastructure —
`quote!`/`proc-macro2` `TokenStream`/`ToTokens` — NOT a hand-rolled string code
generator) and **de8i** (lowering is methods/`ToTokens` on the schema/model
nouns; cross-object logic is its own type, not a god-struct).

Read on branch `origin/designer-daemon-emit-2026-06-06`. The emitter source is
the checked-out worktree
`/home/li/wt/github.com/LiGoldragon/schema-rust-next-daemon-emit/src/daemon_emit.rs`;
the emitted output is `spirit:src/schema/daemon.rs` on the same branch.

## Verdict in one paragraph

The string-emission flaw is **real, confirmed, and a blocker against 4np2**:
`daemon_emit.rs` builds the entire 415-line emitted daemon module as raw Rust
source text, with **zero** `quote!` and **zero** `ToTokens`, using a
line-buffer writer (404 `self.line(...)` calls). This is exactly the pattern
Gap 1 (`4ac90de`, already on `schema-rust-next` `main`) eliminated everywhere
else by replacing `RustWriter` with `RustModuleRenderer` + ~30 per-section
`ToTokens` nouns routed through `prettyplease`. The daemon emitter is the one
un-migrated island — and crucially it was **branched before Gap 1 landed**, so
its `lib.rs` still carries the old `RustWriter` too. There is a **second,
structural** flaw (de8i): all 14 emission methods live on one
`DaemonModuleWriter` god-struct rather than on per-section model nouns. The
**emitted output itself is sound** — clean, idiomatic, correct, with the three
543-noted emitter bugs (rkyv bounds, `MutexGuard` borrow-split) genuinely
fixed; the only output-level wrinkle is that the string path keeps non-doc `//`
comments and exact hand-authored layout that the prettyplease seam would drop.
The rewrite is **mechanical and well-scoped** (the target seam already exists
and is proven), estimated **medium effort**, with no section that genuinely
resists tokenization.

## 1. The string-emission flaw — characterized

### How it builds Rust

`DaemonModule::render` (daemon_emit.rs:187) constructs a `DaemonModuleWriter`
and returns `writer.finish()` — a `String`. `DaemonModuleWriter`
(daemon_emit.rs:197) is a line-buffer:

```rust
struct DaemonModuleWriter {
    output: String,
    generator_name: String,
}

fn line(&mut self, line: impl AsRef<str>) {   // :210
    self.output.push_str(line.as_ref());
    self.output.push('\n');
}
fn blank(&mut self) { self.output.push('\n'); }   // :215
fn finish(self) -> String { self.output }          // :219
```

Every section is emitted by pushing **string literals of Rust source** one line
at a time. Representative — the `ComponentDaemon` trait header
(daemon_emit.rs:298-303):

```rust
self.line("pub trait ComponentDaemon: Sized + 'static {");
self.line("    type Configuration: DaemonConfiguration;");
self.line("    type ConfigurationError: std::fmt::Display;");
self.line("    type Engine;");
self.line(
    "    type Error: std::fmt::Display + From<FrameError> + From<SignalFrameError> + From<ListenerError>;",
);
```

The few non-literal spots use `format!` to interpolate a shape value into a
source string — e.g. the import path (daemon_emit.rs:271-273) and the octal
socket mode (daemon_emit.rs:473-475):

```rust
self.line(format!(
    "            let socket_mode = configuration.meta_socket_mode().unwrap_or_else(|| SocketMode::new(0o{mode:o}));"
));
```

The doc-comment on the writer (daemon_emit.rs:194-196) is explicit that this is
deliberate mirroring of the old style: *"mirroring the `RustWriter` line/blank
style used by the rest of the emitter so the emitted source reads the same
way."* That rationale is now stale — Gap 1 retired `RustWriter`.

### The actual counts (checked, falsifiable)

Run in the worktree against `src/daemon_emit.rs`:

| Construct | Count | Meaning |
|---|---|---|
| `quote!` | **0** | no token macro at all |
| `ToTokens` | **0** | no token-stream noun |
| `self.line(` | **404** | raw source-string pushes |
| `self.blank(` | **54** | blank-line pushes |
| `push_str` | 1 | (the `line` impl itself) |
| `format!` | 6 | string interpolation into source |
| total lines | 807 | |

Compare `schema-rust-next` `origin/main` `src/lib.rs` after Gap 1: **121**
`quote!`, **0** `self.line(`, `RustWriter` absent (replaced by
`RustModuleRenderer`). The daemon emitter is wholly outside that migration.

### The 807-line structure (which function emits what)

daemon_emit.rs is two halves. Lines **1–192** are legitimately-typed model
nouns and are fine: `NexusDaemonShape` (:33), `WorkingListenerTier` (:73),
`MetaListenerTier` (:94), `SocketModeBits` (:110), `DaemonStreamShape` (:127,
with `DaemonStreamShape::reference_type_name` doing the `TypeReference` →
type-name mapping at :138), and `DaemonModule` (:160). These carry data and
have real methods — no issue.

Lines **194–807** are the offending half: the `DaemonModuleWriter` god-struct
and its 14 string-emitting methods, dispatched from `render` (:227):

| Method | Line | Emits |
|---|---|---|
| `emit_imports` | 251 | `use` blocks (single vs multi vs stream) |
| `emit_component_daemon_trait` | 283 | the `ComponentDaemon` hook trait (the largest section) |
| `emit_command` | 382 | `DaemonCommand` argv→config→run |
| `emit_daemon` | 426 | `DaemonBinder` trait + blanket impl |
| `emit_single_bind` / `emit_multi_bind` | 450 / 460 | the `bind` bodies |
| `emit_working_transport` | 494 | `WorkingTransport` length-prefixed codec |
| `emit_subscriptions` | 526 | option-B `EmittedSubscriptions` registry/publish/deliver |
| `emit_runtime` | 620 | `GeneratedDaemonRuntime` + the decode→execute→encode spine |
| `emit_listener_tier_enum` | 676 | `ListenerTier` enum + `Display` |
| `emit_single_runtime_impl` / `emit_multi_runtime_impl` | 694 / 714 | the `DaemonRuntime` / `MultiListenerRuntime` impls |
| `emit_daemon_error` | 742 | `DaemonError` enum + `From` conversions |
| `emit_exit_helper` | 795 | `DaemonEntry::run_to_exit_code` |

**FLAW E1 (blocker, 4np2).** The entire emitted-source half is string-based.
Fix: rewrite as `ToTokens` nouns (see §2).

**FLAW E2 (major, de8i).** All 14 emission methods hang off one
`DaemonModuleWriter` — a god-struct whose only data is `output: String` +
`generator_name`. de8i requires the per-section syntax to live on its own model
noun; on `main` this is exactly what ~30 `*Tokens` structs do
(`SignalFrameImplTokens`, `NexusEngineTraitTokens`, `PlaneNamespaceTokens`, …).
The daemon emitter collapses all sections into one writer. Fix: the §2 rewrite
resolves E1 and E2 together — each `emit_*` becomes a `*Tokens` noun.

## 2. Scoping the token rewrite

### The target seam already exists and is proven

On `schema-rust-next` `main`, `RustModule::render` (lib.rs:238) keeps a thin
`RustModuleRenderer` whose `output: String` exists ONLY for the `// @generated`
header (prettyplease drops non-doc comments) and blank spacing. Every code
section is a `ToTokens` noun routed through one method (lib.rs:3507-3517):

```rust
fn finish(self) -> String { self.output }

fn emit_item_tokens(&mut self, tokens: TokenStream) {
    let file = syn::parse2::<syn::File>(tokens).expect("generated Rust item tokens parse");
    let source = prettyplease::unparse(&file);
    self.output.push_str(source.trim_end());
    self.output.push('\n');
}
```

`emit_type` etc. just do
`self.emit_item_tokens(RustDeclarationTokens::new(...).into_token_stream())`
(lib.rs:3538). The daemon emitter must join this same seam.

### One-to-one mapping: each `emit_*` → a `*Tokens` noun

| Current string method | Becomes ToTokens noun | Notes |
|---|---|---|
| `emit_component_daemon_trait` | `ComponentDaemonTraitTokens` (holds `stream: Option<&DaemonStreamShape>`, `has_meta: bool`) | conditional assoc types/methods become `if`-guarded `quote!` fragments folded into the body |
| `emit_command` | `DaemonCommandTokens` | no conditionals — a single `quote!` block |
| `emit_daemon` + `emit_single_bind` + `emit_multi_bind` | `DaemonBinderTokens` (holds the `NexusDaemonShape`) | the multi `bind` body interpolates `SocketMode::new(0o{mode:o})` via a `Literal`; single/multi pick the body |
| `emit_working_transport` | `WorkingTransportTokens` | static — one `quote!` |
| `emit_subscriptions` | `EmittedSubscriptionsTokens` | the largest imperative body; still pure `quote!` (see hard parts) |
| `emit_runtime` + spine | `GeneratedDaemonRuntimeTokens` | the `if stream.is_some()` interleaving becomes pre-built `quote!` fragments spliced with `#fragment` |
| `emit_listener_tier_enum` | `ListenerTierTokens` | static |
| `emit_single_runtime_impl` / `emit_multi_runtime_impl` | `DaemonRuntimeImplTokens` | one noun, single/multi selects the trait + `handle_stream` arms |
| `emit_daemon_error` | `DaemonErrorTokens` | thiserror `#[error(...)]` attrs are emitted as token attributes (cf. main's existing thiserror emission) |
| `emit_exit_helper` | `DaemonEntryTokens` | static |
| `emit_imports` | `DaemonImportsTokens` | OR keep as `use` items routed through `emit_item_tokens` like main's `RustImportTokens` |

Composition: a top-level `DaemonModuleTokens` (replacing the writer's `render`)
either implements `ToTokens` by `quote!`-splicing the section nouns
(`#trait_tokens #command_tokens …`) and goes through one `emit_item_tokens`
call, OR — matching main exactly — `DaemonModule::render` builds a thin
renderer, writes the `// @generated` header via `line`, then routes each section
noun through `emit_item_tokens` for per-item prettyplease formatting. The latter
is the closer match to the Gap-1 shape and is recommended.

### Hard parts — and why none genuinely resists tokenization

1. **Imperative method bodies with `match`/`if let`/early return** (the spine in
   `emit_runtime`, the `publish`/`deliver` bodies in `emit_subscriptions`).
   These look like "logic" but `quote!` tokenizes arbitrary Rust statements
   verbatim — `quote! { match listener { ListenerTier::Working => …, } }` is
   exactly as valid as a type definition. main already emits comparably
   imperative bodies (`NexusEngineTraitTokens` at lib.rs:2114,
   `SignalMailLifecycleSupportTokens` at lib.rs:2416). **Not a real obstacle.**

2. **The `expect("...")` / `Error::other("subscription frame encode")` string
   literals inside emitted bodies** (daemon_emit.rs:565, 612). Inside `quote!`
   these are just literal tokens — `quote! { .expect("subscription state lock") }`
   round-trips fine. **Not an obstacle.**

3. **Conditional section content** (`if stream.is_some()`, `if
   shape.is_multi_listener()`). Today these branch `self.line` calls. In tokens
   they become pre-built `TokenStream` fragments (`let stream_fields = if … {
   quote!{ subscriptions: EmittedSubscriptions<Daemon>, } } else {
   TokenStream::new() };`) spliced with `#stream_fields`. This is the dominant
   pattern in main's conditional emitters. **Not an obstacle.**

4. **The octal socket-mode literal** `0o{mode:o}` (daemon_emit.rs:473). Emit as
   `proc_macro2::Literal::u32_unsuffixed(mode)` or build the `0o…` literal token;
   trivial. **Not an obstacle.**

5. **The `// @generated` header and the explanatory non-doc `//` comments**
   inside `publish` (daemon_emit.rs:572-575). prettyplease **drops non-doc
   comments**, so the header must go through the renderer's `line()` (as main
   does), and the in-body `//` explanation comments will be **lost** in the
   token path. This is the one genuine behavioral change — see §3.

**Effort: medium.** ~600 lines of string emission → ~12 `ToTokens` nouns of
`quote!`. Mechanical and pattern-matched to ~30 existing examples on main. The
goldens in `tests/daemon_emission.rs` already compare whitespace-and-comma-
insensitively (`assert_code_contains` compacts out whitespace and commas,
daemon_emission.rs:11-21), so prettyplease reformatting will **not** break them
— a significant de-risking. The estimate is on the order of a focused day, not
a multi-day rewrite, precisely because the seam and the noun pattern are already
established and the tests tolerate reformatting.

### Important sequencing note (not strictly this dimension, but load-bearing)

This worktree's `lib.rs` is the **pre-Gap-1** version — it still contains
`RustWriter` (the daemon-emit branch was cut before `4ac90de` landed). Checked:
`grep RustModuleRenderer src/lib.rs` → no match in the worktree, but
`origin/main:src/lib.rs` has it. So the branch must first be **rebased onto the
post-Gap-1 `main`** (resolving the 1342-line `lib.rs` divergence) before — or as
part of — the daemon token rewrite; otherwise there is no `RustModuleRenderer` /
`emit_item_tokens` seam in this branch to route the new daemon `*Tokens` through.
The operator landing plan in report 543 (triad-runtime → schema-rust-next →
spirit) already regenerates lockfiles against fresh upstreams, but does not call
out that the schema-rust-next branch predates Gap-1 and needs the rebase +
token rewrite before it is 4np2-clean. **This is the key cross-cutting finding
for the migration.**

## 3. Emitted-output quality

Read `spirit:src/schema/daemon.rs` (multi-listener + stream, 415 lines) on the
branch. The generated module is **clean, correct, and idiomatic**:

- Triad-faithful: `GeneratedDaemonRuntime` owns the `Engine` and (option B) the
  `EmittedSubscriptions`; the spine `handle_working_stream` is a tidy
  decode (`Input::decode_signal_frame`) → execute (`Daemon::handle_working_input`)
  → encode (`output.encode_signal_frame`) → register/publish. No durable state
  leaks into the decision plane.
- **No stringly identifiers in the output.** `ListenerTier` is a real enum with
  a `Display` impl; routing is `match listener { ListenerTier::Working => …,
  ListenerTier::Meta => … }` — no string prefixes, no `starts_with`. The only
  string literals in the output are `Display` text (`"working"`/`"meta"`) and
  `expect`/`Error::other` messages, all legitimate.
- **The three 543-noted emitter bugs are genuinely fixed in the output.** The
  `StreamEvent` assoc type carries the full rkyv `Archive` +
  `for<'archive> Serialize<HighSerializer<…>>` bounds (emitted daemon.rs trait
  body); the `publish` body does the `let state = &mut *guard;` reborrow with an
  explanatory comment so the disjoint `registry`(shared)/`publisher`(exclusive)
  borrows split — the `MutexGuard`-`Deref` borrow-conflict fix. The spirit bin
  is a true one-liner: `fn main() { SpiritDaemon::run_to_exit_code() }`
  (`spirit:src/bin/spirit-daemon.rs`).
- Single-argument rule honored: `DaemonCommand::configuration` accepts only
  `ComponentArgument::SignalFile` and rejects `InlineNota`/`NotaFile` with
  `ArgumentError::ExpectedSignalFile` (emitted daemon.rs, `configuration`).

**Output wrinkle (minor → nit).** Because the output is string-built, it is
**not prettyplease-formatted** and preserves the exact hand-authored layout —
e.g. the two separate `use triad_runtime::{ … }` blocks (emitted daemon.rs:6-11
and :13-15) that prettyplease would merge, the hand-chosen line wraps, and the
**non-doc `//` explanatory comments** inside `publish`. Once the emitter moves
to the token/prettyplease seam, the emitted file will be **reformatted** (blocks
merged, wraps normalized) and those in-body `//` comments will be **dropped**.
This is not a correctness defect — it is the expected diff when the file is
regenerated post-rewrite, and the spirit freshness guard will simply need a
regenerate pass. It is worth flagging only so the regenerated diff is not
mistaken for a regression, and so the value of the in-body explanation comment
(the borrow-split rationale) is preserved by moving it to a doc comment on the
emitted method or the emitter noun. **FLAW E3 (nit).**

## Severity-tagged flaw list

- **E1 — blocker (4np2).** `daemon_emit.rs` emits the entire daemon module as
  raw source strings: 0 `quote!`, 0 `ToTokens`, 404 `self.line` + 6 `format!`.
  Fully string-based, the one island Gap 1 did not migrate. *Fix:* rewrite the
  14 `emit_*` methods as `quote!`-based `*Tokens` nouns routed through the
  `RustModuleRenderer::emit_item_tokens` → prettyplease seam (§2 mapping).
- **E2 — major (de8i).** All section logic sits on one `DaemonModuleWriter`
  god-struct (output: String) instead of per-section model nouns. *Fix:*
  resolved by the same rewrite — each section becomes its own `ToTokens` noun,
  matching main's ~30 `*Tokens` structs.
- **E3 — nit (output formatting).** The emitted file keeps hand-authored layout
  and non-doc `//` comments that the token/prettyplease path will reformat/drop.
  *Fix:* expected regen diff; promote the load-bearing borrow-split `//` comment
  to a doc/`#[doc]` comment on the emitter noun so it survives, and regenerate
  the spirit golden after the rewrite.
- **(Cross-cutting, migration sequencing) — major.** This worktree's `lib.rs`
  predates Gap 1 (`RustWriter` still present; no `RustModuleRenderer`). The
  daemon token rewrite has no seam to route through until the branch is rebased
  onto post-Gap-1 `main`. *Fix:* rebase schema-rust-next's daemon-emit branch
  onto `main` (`4ac90de`) first, then do the token rewrite; fold into report
  543's step-2 landing.

## Verdict

- **String-emission flaw severity: BLOCKER against 4np2** (E1) — unambiguous and
  total; the daemon emitter is 100% string-based with zero token infrastructure.
- **Rewrite scope: medium, mechanical, low-risk.** The target seam exists and is
  proven on main; ~12 `ToTokens` nouns of `quote!`; the goldens already tolerate
  reformatting. Nothing in the daemon module genuinely resists tokenization.
  Must be preceded by a rebase onto post-Gap-1 `main`.
- **Emitted output otherwise sound: YES.** Clean, idiomatic, triad-faithful,
  single-argument-compliant, with the three 543 bugs genuinely fixed. The only
  output-level consequence of the rewrite is cosmetic reformatting plus the loss
  of in-body non-doc comments, which is expected and easily preserved.

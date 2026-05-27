# Rust method-rule audit + fix — 2026-05-27

Enforced AGENTS hard override (intent record 882, Maximum): no free
functions outside `fn main` / `#[cfg(test)]`, no ZST namespace holders.
Audited the seven in-scope repos and landed fixes on the two
designer-authored.

## Designer-authored — fixes landed

### `nota-next` — branch `designer-no-free-fns-2026-05-27` from `main`

Commits:

| Short id | Subject |
|---|---|
| `aca226d6` | parser: move char-classification helpers onto Delimiter and Atom |

Violations fixed in `src/parser.rs`:

- `fn is_opening_delimiter(char) -> bool` → `Delimiter::is_opening_character(char) -> bool`
- `fn is_closing_delimiter(char) -> bool` → `Delimiter::is_closing_character(char) -> bool`
- `fn is_symbol_character(char) -> bool` → `Atom::is_symbol_character(char) -> bool`

Call sites in `AtomClassification::classify` and `Parser::parse_*`
updated. All 5 integration tests pass. No ZSTs in `src/`.

Pushed to `origin/designer-no-free-fns-2026-05-27`.

### `schema-next` — branch `designer-no-free-fns-2026-05-27` from `designer-finish-macro-engine-2026-05-26`

Note: `main` already had a commit "add root schema and remove
free-function helpers" (0a777dde) post-dating the feature branch.
Per instruction, I audited the feature branch (which still carried
the violations) and built the fix on top of it.

Commits (oldest first):

| Short id | Subject |
|---|---|
| `fa47557a` | asschema: move canonical-NOTA emission onto each declaration type |
| `9dc01512` | macros, engine: move atom_name onto Name as try_from_symbol_block |
| `bfb0f220` | engine: dissolve namespace ZSTs; move lowering verbs onto data-bearing nouns |

Free functions removed (all in `src/`):

| Was | Now |
|---|---|
| `fn canonical_surface(&RootSurface)` | `RootSurface::to_canonical_nota` |
| `fn canonical_type(&TypeDeclaration)` | `TypeDeclaration::to_canonical_nota` |
| `fn canonical_field(&FieldDeclaration)` | `FieldDeclaration::to_canonical_nota` |
| `fn canonical_variant(&EnumVariant)` | `EnumVariant::to_canonical_nota` |
| `fn canonical_macro(&MacroDeclaration)` | `MacroDeclaration::to_canonical_nota` |
| `pub(crate) fn atom_name(&Block)` | `Name::try_from_symbol_block` |
| `fn try_parse_macro_declaration(&Name, &Block)` | `MacroDeclaration::try_from_namespace_pair` |
| `fn try_parse_macro_call(&Name, &Block, &MacroRegistry)` | `NamespaceMacroCall::try_from_namespace_pair` |
| `fn parse_import_value(Name, &Block)` | `ImportDeclaration::try_from_namespace_pair` |
| `fn parse_path_block(&Block)` | `ImportDeclaration::path_from_block` (private) |
| `fn derive_source_name_from_path(&Path)` | `Name::from_path_stem` |
| `fn lower_surface_variant(&Block)` | `EnumVariant::try_from_variant_block` |
| `fn lower_fields(&Block)` | `FieldDeclaration::try_list_from_block` |
| `fn lower_enum_variants(&Block)` | `EnumVariant::try_list_from_block` |

ZSTs removed (both pure namespace holders):

- `struct SurfaceMacro;` — work moved to `RootSurface::matches_block` +
  `RootSurface::try_from_surface_block`; static name to
  `RootSurface::PASS_NAME`. Field removed from `SchemaEngine` /
  `ChildEngine`.
- `struct TypeDeclarationMacro;` — work moved to
  `TypeDeclaration::matches_namespace_pair` +
  `TypeDeclaration::try_from_namespace_pair`; static name to
  `TypeDeclaration::PASS_NAME`. Field removed from `SchemaEngine` /
  `ChildEngine`.

New types added to `asschema.rs`:

- `pub(crate) struct NamespacePair<'block>` — two-reference helper for
  the name+definition pair fed to `TypeDeclaration::try_from_namespace_pair`
  (replaces the engine-private `SyntheticPair`; satisfies the one-object-in
  rule on the methods).

All 21 unit/integration tests pass. No free functions or ZSTs in `src/`.

Pushed to `origin/designer-no-free-fns-2026-05-27`.

## Operator-authored — punch list (do not edit)

`schema-rust-next`, `spirit`, `signal-spirit`, `core-signal-spirit`:
all CLEAN — no free functions, no ZSTs in `src/` of any.

`spirit-next` has the following violations (designer must NOT edit per
psyche 2026-05-24; forwarding for operator):

### `spirit-next/src/transport.rs`

| Line | Item | Suggested fix |
|---|---|---|
| 45 | `pub fn exchange(socket_path, input) -> Result<(OutputRoute, Output), TransportError>` | Add data-bearing `pub struct DaemonClient { socket_path: PathBuf }` carrying the connection target; method `DaemonClient::exchange(&self, &Input)`. |
| 54 | `pub fn write_input(&mut impl Write, &Input)` | Method on `Input`: `Input::write_to(&self, &mut impl Write) -> Result<(), TransportError>`. |
| 58 | `pub fn read_input(&mut impl Read) -> Result<(InputRoute, Input)>` | Associated function on `Input`: `Input::read_from(&mut impl Read) -> Result<(InputRoute, Self), TransportError>`. |
| 62 | `pub fn write_output(&mut impl Write, &Output)` | Method on `Output`: `Output::write_to`. |
| 66 | `pub fn read_output(&mut impl Read) -> Result<(OutputRoute, Output)>` | Associated function on `Output`: `Output::read_from`. |
| 70 | `fn write_frame(&mut impl Write, Vec<u8>)` | Private inherent on the frame newtype — invent `struct LengthPrefixedFrame(Vec<u8>)` and `LengthPrefixedFrame::write_to(&self, &mut impl Write)` + `LengthPrefixedFrame::read_from(&mut impl Read) -> Result<Self, _>`. |
| 79 | `fn read_frame(&mut impl Read) -> Result<Vec<u8>, _>` | Same as line 70 — paired methods on the new `LengthPrefixedFrame`. |

### `spirit-next/src/daemon.rs`

| Line | Item | Suggested fix |
|---|---|---|
| 42 | `pub fn run_daemon(Configuration) -> Result<(), DaemonError>` | Method on a new `pub struct Daemon { configuration: Configuration, engine: Engine }` — `Daemon::run(self) -> Result<(), DaemonError>`. |
| 63 | `fn handle_stream(UnixStream, &Engine)` | Method on `Daemon`: `Daemon::handle_stream(&self, UnixStream)`. |
| 70 | `fn remove_stale_socket(&Path)` | Either method on `Daemon::remove_stale_socket(&self)` or `impl Configuration { fn remove_stale_socket(&self) }`. |

### `spirit-next/src/config.rs`

| Line | Item | Suggested fix |
|---|---|---|
| 56 | `fn text_from_block(&Block) -> Result<String, ConfigurationError>` | Method on `Configuration` (it's the sole caller): `Configuration::text_from_block(&Block) -> Result<String, ConfigurationError>` as associated function. Or, since it's a `Block` → `String` projection used only for configuration loading, a `pub(crate) trait BlockProjection { fn try_to_text(&self) -> Result<String, ConfigurationError>; }` implemented on `Block`. |

### `spirit-next/src/bin/spirit-next.rs`

| Line | Item | Suggested fix |
|---|---|---|
| 12 | `fn run() -> Result<...>` | `fn main()` is allowed; the `fn run()` helper is a free function. Inline it into `fn main()` or wrap in `struct ClientCli { argument: String }` with `ClientCli::run(self)`. |
| 30 | `fn read_single_argument(&str) -> Result<String, _>` | Same fix — associated function on the new `ClientCli` type. |

### `spirit-next/src/bin/spirit-next-daemon.rs`

| Line | Item | Suggested fix |
|---|---|---|
| 12 | `fn run() -> Result<...>` | Inline into `main()` or wrap in `struct DaemonCli { argument: String }`. |

### `spirit-next/build.rs`

| Line | Item | Suggested fix |
|---|---|---|
| 6 | `fn main()` only — `fn main()` is allowed in build scripts. **No violation.** |

## Surprises

- **schema-next main is ahead of the feature branch.** Main (0a777dde,
  2026-05-27 10:26) was committed *after* the feature branch
  (bc7dc05c, 2026-05-26 18:41) and explicitly carries the message
  "add root schema and remove free-function helpers". Main already has
  zero free fns / zero ZSTs in `src/`. I built the fix on the feature
  branch as instructed, but the operator will need to reconcile the
  two histories (likely merge / rebase the feature branch's macro
  engine work onto the cleaner main, then re-apply my no-free-fns
  fixes if the engine code on main hasn't yet absorbed the feature).
- **`build.rs:31` in spirit-next uses `RustEmitter.emit_file(...)`.** That
  syntax compiles only if `RustEmitter` is a unit struct — and the
  cached cargo checkout at `~/.cargo/git/checkouts/.../9984703/src/lib.rs`
  has `pub struct RustEmitter;`. The local
  `/git/.../schema-rust-next/src/lib.rs` has been upgraded to
  `pub struct RustEmitter { generator_name: &'static str }`. Once
  spirit-next consumes the new schema-rust-next via cargo update, that
  line will break compilation. The fix in build.rs is
  `RustEmitter::default().emit_file(&asschema)`. Operator should
  schedule the update.
- **Two `RustEmitter` shapes diverge live.** Local schema-rust-next has
  the data-bearing version; spirit-next still pulls the unit-struct
  version. Worth a note for the operator pipeline.
- No schema-emitted code violated the rule — the `RustEmitter` in
  schema-rust-next emits structs / enums with fields, never unit-struct
  namespace placeholders.

## JJ commit short-ids — recap

- **nota-next** branch `designer-no-free-fns-2026-05-27`:
  - `aca226d6` parser: move char-classification helpers onto Delimiter and Atom
- **schema-next** branch `designer-no-free-fns-2026-05-27`:
  - `fa47557a` asschema: move canonical-NOTA emission onto each declaration type
  - `9dc01512` macros, engine: move atom_name onto Name as try_from_symbol_block
  - `bfb0f220` engine: dissolve namespace ZSTs; move lowering verbs onto data-bearing nouns

Both feature branches pushed to `origin`.

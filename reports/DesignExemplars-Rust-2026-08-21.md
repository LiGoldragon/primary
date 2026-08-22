# Design Exemplars: Rust — 2026-08-21

Research for the software-design skill. Source: five parallel web-research agents plus
synthesis. Each claim is annotated with its source repo and file where established.

Scope: Rust projects only, as ordered. The vision being tested:
- types-first; contents before behavior
- spine is From/TryFrom conversions, demand-driven, end-result first
- at least four parts: inputs/receiving, coherent input type, coherent output type, output as simple operation
- capabilities on the type that contains their subject
- output never sprawled; reviewable in one place under one trait
- no service objects

Part 1 is findings. Part 2 is interpretation for the skill.


## Part 1: Findings


### 1. wasm-encoder (bytecodealliance/wasm-tools)

**Source:** https://github.com/bytecodealliance/wasm-tools, crate `wasm-encoder`

The central type:

```rust
// crates/wasm-encoder/src/lib.rs
pub struct Module {
    pub(crate) bytes: Vec<u8>,
}
```

`Module::new()` writes the 8-byte WASM magic and version header into `bytes` immediately. There
is no intermediate structured representation; the module accumulates its encoding directly.

The `Encode` trait governs all output:

```rust
pub trait Encode {
    fn encode(&self, sink: &mut Vec<u8>);
}
```

Every primitive, every integer type (as LEB128), every composite type has exactly one
`impl Encode`. Blanket impls cover `&T`, `[T]`, `Option<T>`.

The `Section` trait is a supertrait of `Encode`:

```rust
pub trait Section: Encode {
    fn id(&self) -> u8;

    fn append_to(&self, dst: &mut Vec<u8>) {
        dst.push(self.id());
        self.encode(dst);
    }
}
```

Every section type — `TypeSection`, `FunctionSection`, `CodeSection`, `ExportSection`,
`ImportSection`, `GlobalSection`, `MemorySection`, `TableSection`, `DataSection`,
`ElementSection`, `StartSection`, `TagSection`, `NameSection`, `CustomSection` — implements
both traits. Internally each section is also a `bytes: Vec<u8>` accumulator plus a count:

```rust
pub struct TypeSection {
    bytes: Vec<u8>,
    num_added: u32,
}

impl Encode for TypeSection {
    fn encode(&self, sink: &mut Vec<u8>) {
        encode_section(sink, self.num_added, &self.bytes);
    }
}
impl Section for TypeSection {
    fn id(&self) -> u8 { SectionId::Type.into() }
}
```

The `Module` API:

```rust
pub fn section(&mut self, section: &impl Section) -> &mut Self {
    self.bytes.push(section.id());
    section.encode(&mut self.bytes);
    self
}

pub fn finish(self) -> Vec<u8> {
    self.bytes
}
```

Full call site:

```rust
let mut types = TypeSection::new();
types.ty().function([ValType::I32, ValType::I32], [ValType::I32]);

let mut functions = FunctionSection::new();
functions.function(0);

let mut module = Module::new();
module.section(&types).section(&functions);

let wasm_bytes = module.finish();
```

**What is absent:** No From/TryFrom between stages. Sections are not built from each other via
typed conversions — they are accumulated via a builder API. The `section()` call appends bytes
immediately rather than deferring to a coherent in-memory structured representation.
`finish()` merely moves the `Vec<u8>` out. There is also no structured in-memory
representation of the WASM module — the "assembly" is in the bytes themselves.


### 2. syn (dtolnay/syn)

**Source:** https://github.com/dtolnay/syn

The top-level type:

```rust
// src/file.rs
pub struct File {
    pub shebang: Option<String>,
    pub frontmatter: Option<Frontmatter>,
    pub attrs: Vec<Attribute>,
    pub items: Vec<Item>,
}
```

`Item` is an enum where every variant wraps a dedicated concrete struct:
`Item::Const(ItemConst)`, `Item::Enum(ItemEnum)`, `Item::Fn(ItemFn)`, `Item::Impl(ItemImpl)`,
`Item::Struct(ItemStruct)`, `Item::Trait(ItemTrait)`, `Item::Type(ItemType)`,
`Item::Use(ItemUse)`, `Item::Verbatim(TokenStream)`, and others. Each inner struct has concrete
typed fields: `ItemConst` has `const_token`, `ident`, `ty: Box<Type>`, `expr: Box<Expr>`.
`Expr` follows the same pattern with ~40 variants.

The `Parse` trait is capability declared on the type that contains its subject:

```rust
pub trait Parse: Sized {
    fn parse(input: ParseStream) -> Result<Self>;
}
pub type ParseStream<'a> = &'a ParseBuffer<'a>;
```

Implementation on `File`:

```rust
// src/file.rs
impl Parse for File {
    fn parse(input: ParseStream) -> Result<Self> { ... }
}
```

Every AST type implements `Parse` on itself. `ParseBuffer` is a cursor over tokens; it is
passed in but not owned by the parsed type. The `ToTokens` trait provides the reverse
direction, also implemented on each AST type.

Entry points are free functions:

```rust
syn::parse2::<T>(tokens: proc_macro2::TokenStream) -> Result<T>  // T: Parse
syn::parse_str::<T>(s: &str) -> Result<T>                        // T: Parse
syn::parse_file(s: &str) -> Result<File>
```

**What is absent:** The entry point is a free function, not `T::from(tokens)` or
`T::try_from(tokens)`. No From/TryFrom in the parsing chain. `ParseBuffer` is the only
coordination type; there are no manager, registry, or coordinator service types.


### 3. object crate — write side (gimli-rs/object)

**Source:** https://github.com/gimli-rs/object

The in-memory write type:

```rust
// src/write/mod.rs
pub struct Object<'a> {
    format: BinaryFormat,
    architecture: Architecture,
    sub_architecture: Option<SubArchitecture>,
    endian: Endianness,
    sections: Vec<Section<'a>>,
    standard_sections: HashMap<StandardSection, SectionId>,
    symbols: Vec<Symbol>,
    symbol_map: HashMap<Vec<u8>, SymbolId>,
    comdats: Vec<Comdat>,
    pub flags: FileFlags,
    pub mangling: Mangling,
}
```

Everything accumulates into `Object`. Key builder methods:

```rust
pub fn add_section(...) -> SectionId
pub fn section_id(StandardSection) -> SectionId
pub fn append_section_data(SectionId, &[u8], align: u64) -> u64
pub fn add_symbol(Symbol) -> SymbolId
pub fn add_relocation(SectionId, Relocation) -> Result<()>
```

Emit is a method on the type:

```rust
pub fn write(&self) -> Result<Vec<u8>>
pub fn emit(&self, buffer: &mut dyn WritableBuffer) -> Result<()>
pub fn write_stream<W: io::Write>(&self, w: W) -> Result<(), Box<dyn error::Error>>
```

`write()` calls `emit()` internally. `emit()` dispatches on `self.format` to private
format-specific writers (`coff_write`, `elf_write`, `macho_write`).

The read side is a completely separate type:

```rust
// src/read/any.rs
pub enum File<'data, R: ReadRef<'data> = &'data [u8]> {
    Coff(coff::CoffFile<'data, R>),
    Elf32(elf::ElfFile32<'data, Endianness, R>),
    Elf64(elf::ElfFile64<'data, Endianness, R>),
    MachO32(macho::MachOFile32<'data, Endianness, R>),
    MachO64(macho::MachOFile64<'data, Endianness, R>),
    // ...
}

impl<'data, R: ReadRef<'data>> File<'data, R> {
    pub fn parse(data: R) -> Result<Self> { ... }
}
```

Read and write share vocabulary in `crate::common` (`BinaryFormat`, `Architecture`,
`SectionKind`, `SymbolKind`) but have no shared code. No From/TryFrom connects them.

**What is absent:** `emit()` dispatches internally on `self.format` without a governing
trait across the whole pipeline. There is no From/TryFrom between read and write sides.
No single trait makes "all object file writers" uniform at the section level the way
`Section: Encode` does in wasm-encoder.


### 4. rustc — stage types and CodegenBackend (rust-lang/rust)

**Source:** https://github.com/rust-lang/rust, compiler subtree; https://rustc-dev-guide.rust-lang.org/overview.html

Named stage types:

| Stage | Rust type | Crate |
| --- | --- | --- |
| Token stream | `rustc_ast::tokenstream::TokenStream` | `rustc_ast` |
| AST | `rustc_ast::ast::Crate` | `rustc_ast` |
| HIR (per item) | `rustc_hir::hir::MaybeOwner<'hir>` | `rustc_hir` |
| THIR (per body) | `rustc_middle::thir::Thir<'tcx>` | `rustc_middle` |
| MIR (per body) | `rustc_middle::mir::Body<'tcx>` | `rustc_middle` |
| Codegen output | `CompiledModules` | `rustc_codegen_ssa` |

The coherent in-memory world is `TyCtxt<'tcx>`: the single context holding all HIR, types, MIR
bodies, and trait solutions. Every query goes through it. The entire MIR for the crate is fully
materialized in this context before codegen begins.

Transitions between stages are not From/TryFrom; they are registered queries:

```rust
// compiler/rustc_ast_lowering/src/lib.rs
fn lower_to_hir(tcx: TyCtxt<'_>, def_id: LocalDefId) -> hir::MaybeOwner<'_>

// compiler/rustc_mir_build/src/builder/mod.rs
pub(crate) fn build_mir_inner_impl<'tcx>(tcx: TyCtxt<'tcx>, def: LocalDefId) -> Body<'tcx>
```

All stage transitions are demand-driven through the query system (a salsa-like incremental
computation framework) rather than explicit sequential calls.

The output side is concentrated behind one trait:

```rust
// compiler/rustc_codegen_ssa/src/traits/backend.rs
trait CodegenBackend {
    fn codegen_crate<'tcx>(&self, tcx: TyCtxt<'tcx>) -> Box<dyn Any>;

    fn join_codegen(&self, ongoing_codegen: Box<dyn Any>, sess: &Session,
                    incr_comp_session: Option<&IncrCompSession>,
                    outputs: &OutputFilenames, crate_info: &CrateInfo)
                    -> (CompiledModules, WorkProductMap);

    fn link(&self, sess: &Session, compiled_modules: CompiledModules,
            crate_info: CrateInfo, metadata: EncodedMetadata,
            outputs: &OutputFilenames);
}
```

Called from exactly one orchestrator: `Linker` in `compiler/rustc_interface/src/queries.rs`.
The entire emission path is reviewable under this one trait plus one struct.

The driver (`compiler/rustc_driver_impl/src/lib.rs`) reads roughly:

```rust
interface::run_compiler(config, |compiler| {
    let krate = passes::parse(sess);               // -> ast::Crate
    let linker = create_and_enter_global_ctxt(compiler, krate, |tcx| {
        let _ = tcx.resolver_for_lowering();       // triggers expansion + name res
        passes::write_dep_info(tcx);
        tcx.ensure_ok().analysis(());              // type check, borrow check, MIR
        let linker = Linker::codegen_and_build_linker(tcx, codegen_backend);
        Some(linker)
    });
    if let (Some(linker), session) = linker {
        linker.link(sess, session, codegen_backend);
    }
})
```

These six meaningful calls are wrapped in ~200 lines of flag handling and early-exit boilerplate.

**What is absent:** No From/TryFrom between stages; the query system is demand-driven but
not typed-conversion-driven. The driver does not read as `parse() -> ast::Crate -> hir::Crate
-> ...`; stages are triggered lazily behind `analysis()`. The 200-line boilerplate makes main
difficult to read as a clean chain.


### 5. axum — FromRequest pipeline (tokio-rs/axum)

**Source:** https://github.com/tokio-rs/axum

Two extraction traits form an explicit typed pipeline:

```rust
pub trait FromRequestParts<S>: Sized {
    type Rejection: IntoResponse;
    fn from_request_parts(parts: &mut Parts, state: &S)
        -> impl Future<Output = Result<Self, Self::Rejection>>;
}

pub trait FromRequest<S, M = private::ViaRequest>: Sized {
    type Rejection: IntoResponse;
    fn from_request(req: Request, state: &S)
        -> impl Future<Output = Result<Self, Self::Rejection>>;
}
```

The handler macro expansion for `async fn handler(a: A, b: B, c: C) -> R` produces:

```rust
let (mut parts, body) = req.into_parts();
let a = A::from_request_parts(&mut parts, &state).await?;
let b = B::from_request_parts(&mut parts, &state).await?;
let c = C::from_request(req, &state).await?;
handler(a, b, c).await.into_response()
```

The last line is the whole pipeline: each argument type extracts itself (capability on the
type, via its own FromRequest impl), the handler is called, the result converts to a response
via `IntoResponse`. The `Router<S>` wraps a `PathRouter` behind an `Arc` and implements
Tower's `Service` trait — thin, not a service object in the anti-pattern sense.

**What is absent:** The pipeline is async, not synchronous From/TryFrom. The conversion is
driven by the macro expansion over handler function arguments, not by main(). The coherent
output type is `Response`, but its assembly is not explicit — `into_response()` is called
immediately on the handler result. This is request-handling, not a compilation pipeline, so
there is no deferred coherent output type before writing.


### 6. Gleam compiler — Module\<Info, Definitions\> (gleam-lang/gleam)

**Source:** https://github.com/gleam-lang/gleam

Stage discrimination via type parameter:

```rust
// compiler-core/src/ast/...
pub struct Module<Info, Definitions> {
    pub name: EcoString,
    pub documentation: Vec<EcoString>,
    pub type_info: Info,
    pub definitions: Definitions,
    pub names: Names,
    pub unused_definition_positions: HashSet<u32>,
}

pub type UntypedModule = Module<(), Vec<TargetedDefinition>>;
pub type TypedModule   = Module<type_::ModuleInterface, TypedDefinitions>;
```

The same parameterization recurs at every node level: `UntypedFunction = Function<(), UntypedExpr>`,
`TypedFunction = Function<Arc<Type>, TypedExpr>`. The type parameter is the stage discriminator.
At compile time, you cannot accidentally use an untyped node where a typed one is expected.

The build-level pipeline uses wrapper types:

- `Parsed` — returned by `parse_module`; carries `UntypedModule` plus `ModuleExtra`
- `UncompiledModule` — bundles `UntypedModule` with path, mtime, dependencies, source
- `Module` (build-level) — bundles `TypedModule` with the same metadata
- `Compiled` — holds `Vec<Module>` plus `cached_module_names`

The transition from `UntypedModule` to `TypedModule` is an explicit method call:

```rust
ModuleAnalyzerConstructor { ... }
    .infer_module(ast, line_numbers, path.clone())
// returns Outcome<TypedModule, Vec1<Error>>
```

No From/TryFrom anywhere in the pipeline. Orchestration is an imperative `for` loop over
`Vec<UncompiledModule>`, with a shared `im::HashMap<EcoString, ModuleInterface>` for
cross-module type information.

Codegen (Erlang or JavaScript backends): files are written immediately per module inside the
loop. There is no coherent output type that holds the full generated program in memory before
any file is written. The `Compiled` struct holds typed ASTs but not generated code.

**What is absent:** From/TryFrom conversions. Coherent in-memory output before writing. The
piecemeal write is a direct violation of the vision's "output never sprawled" rule.


### 7. Cargo — BuildContext / BuildRunner (rust-lang/cargo)

**Source:** https://github.com/rust-lang/cargo

Named types at every stage boundary:

| Stage | Type | File |
| --- | --- | --- |
| Input | `CompileOptions` | `ops/cargo_compile/mod.rs` |
| Resolved deps | `WorkspaceResolve<'gctx>` | `ops/resolve.rs` |
| Unit plan | `UnitGraph` + `Vec<Unit>` (roots) | `compiler/unit_graph.rs` |
| Frozen plan | `BuildContext<'a, 'gctx>` | `compiler/build_context/mod.rs` |
| Mutable executor | `BuildRunner<'a, 'gctx>` | `compiler/build_runner/mod.rs` |
| Output | `Compilation<'gctx>` | `compiler/compilation.rs` |

`UnitGraph` is the coherent pre-execution representation:

```rust
pub type UnitGraph = HashMap<Unit, Vec<UnitDep>>;
```

Each `Unit` is an interned `Rc<UnitInner>` holding package, target, profile, kind, mode,
features, and a dep_hash. `BuildContext` wraps `UnitGraph` alongside all static build info; its
doc comment reads: "After a BuildContext is built, the next stage of building is handled in
BuildRunner." The immutable/mutable boundary is explicit in the design.

Top-level call chain inside `compile_ws`:

```rust
let resolve   = ops::resolve_ws_with_opts(ws, ...)?;
let (roots, unit_graph) = {
    let gen = UnitGenerator { ws, packages, resolve, ... };
    let roots = gen.generate_root_units()?;
    let graph = build_unit_dependencies(..., &roots, ...)?;
    rebuild_unit_graph_shared(interner, graph, &roots, ...)
};
let bcx   = BuildContext::new(ws, ..., roots, unit_graph, ...)?;
let runner = BuildRunner::new(&bcx)?;
runner.compile(exec)   // -> CargoResult<Compilation>
```

Key signatures:

```rust
pub fn compile<'a>(ws: &Workspace<'a>, options: &CompileOptions) -> CargoResult<Compilation<'a>>
pub fn create_bcx<'a, 'gctx>(...) -> CargoResult<BuildContext<'a, 'gctx>>
impl BuildRunner {
    pub fn new(bcx: &'a BuildContext<'a, 'gctx>) -> CargoResult<Self>
    pub fn compile(mut self, exec: &Arc<dyn Executor>) -> CargoResult<Compilation<'gctx>>
}
```

**What is absent:** All transitions are explicit function calls, not From/TryFrom. The
`BuildRunner` is a mild service object (it holds collaborators and exposes an imperative
`compile` method). There is no From-chain that would read as end-result-first.


### 8. serde / serde_json — Value and Serialize (serde-rs/serde)

**Source:** https://github.com/serde-rs/serde, https://github.com/serde-rs/json

The coherent in-memory type:

```rust
// serde_json/src/value/mod.rs
pub enum Value {
    Null,
    Bool(bool),
    Number(Number),
    String(String),
    Array(Vec<Value>),
    Object(Map<String, Value>),
}
```

The Serialize impl on Value is a clean match dispatch:

```rust
// serde_json/src/value/ser.rs
impl Serialize for Value {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer,
    {
        match self {
            Value::Null      => serializer.serialize_unit(),
            Value::Bool(b)   => serializer.serialize_bool(*b),
            Value::Number(n) => n.serialize(serializer),
            Value::String(s) => serializer.serialize_str(s),
            Value::Array(v)  => v.serialize(serializer),
            Value::Object(m) => {
                let mut map = serializer.serialize_map(Some(m.len()))?;
                for (k, v) in m { map.serialize_entry(k, v)?; }
                map.end()
            }
        }
    }
}
```

One impl, one match, one arm per variant. The type drives its own serialization.

The Deserialize side requires a Visitor helper struct. Inside the Deserialize impl for Value:

```rust
struct ValueVisitor;  // private helper, NOT Value itself

impl<'de> Visitor<'de> for ValueVisitor {
    type Value = Value;
    fn visit_bool<E>(self, value: bool) -> Result<Value, E> { Ok(Value::Bool(value)) }
    // ...
}
```

The Visitor is a construction delegate, separate from the type being built. This is forced by
the double-dispatch architecture: the Deserializer drives the Visitor (calling `visit_*`
methods), so the Visitor must be a consumed value passed in. The target type cannot serve as
its own Visitor because it does not yet exist during construction.

**What is absent:** On the deserialization side, the Visitor helper is a service-like separate
struct. The overall call sites (`serde_json::to_string`, `serde_json::from_str`) are free
functions rather than type conversions.


### 9. rust-analyzer — HIR types as thin ID wrappers (rust-lang/rust-analyzer)

**Source:** https://github.com/rust-lang/rust-analyzer

The HIR types are zero-overhead ID wrappers with no stored data:

```rust
// crates/hir/src/lib.rs
pub struct Module   { pub(crate) id: ModuleId }
pub struct Struct   { pub(crate) id: StructId }
pub struct Field    { pub(crate) parent: Variant, pub(crate) id: LocalFieldId }
```

All capability comes from methods that take the database:

```rust
impl Struct {
    pub fn module(self, db: &dyn HirDatabase) -> Module { ... }
    pub fn name(self, db: &dyn HirDatabase) -> Name { ... }
    pub fn fields(self, db: &dyn HirDatabase) -> Vec<Field> { ... }
    pub fn ty(self, db: &dyn HirDatabase) -> Type<'_> { ... }
}
```

The architecture is a lazy memoized query graph (salsa), not a pipeline. Any query can
invoke any other query it depends on; salsa handles incremental invalidation. The crate
boundaries (`hir-expand`, `hir-def`, `hir-ty`, `hir`) correspond to logical phases but share
one `RootDatabase`. These are the opposite of service objects: pure zero-cost ID tokens.

**What is absent:** The database-as-context pattern (every method takes `db: &dyn HirDatabase`)
means capabilities are not self-contained on the type — they require an external context
parameter. This is a deliberate trade-off for incrementality, not a service object, but it
is different from the vision's "capability on the type that contains its subject."


### 10. logos — enum IS the spec (maciejhirsz/logos)

**Source:** https://github.com/maciejhirsz/logos

logos is a lexer generator driven entirely by the token type definition. The user declares an
enum and derives `Logos`; the derive macro generates the entire lexer implementation from the
enum variants and their pattern attributes. No separate grammar file, no separate parser
definition — the enum IS the complete specification.

The `Logos` trait:

```rust
pub trait Logos<'source>: Sized {
    type Extras;
    type Source: Source + ?Sized + 'source;
    type Error: Default + Clone + PartialEq + Debug + 'source;

    fn lex(lexer: &mut Lexer<'source, Self>) -> Option<Result<Self, Self::Error>>;

    fn lexer(source: &'source Self::Source) -> Lexer<'source, Self>
    where Self::Extras: Default {
        Lexer::new(source)
    }
}
```

The `Lexer` struct:

```rust
pub struct Lexer<'source, Token: Logos<'source>> {
    source: &'source Token::Source,
    token_start: usize,
    token_end: usize,
    pub extras: Token::Extras,
    // ...
}
```

`Lexer` is an iterator:

```rust
impl<'source, Token> Iterator for Lexer<'source, Token>
where Token: Logos<'source>
{
    type Item = Result<Token, Token::Error>;
    fn next(&mut self) -> Option<Result<Token, Token::Error>> {
        self.token_start = self.token_end;
        Token::lex(self)
    }
}
```

A minimal user definition:

```rust
#[derive(Logos, Debug, PartialEq)]
#[logos(skip r"[ \t\n\f]+")]
enum Token {
    #[token("fast")]
    Fast,

    #[token(".")]
    Period,

    #[regex("[a-zA-Z]+")]
    Text,
}

fn main() {
    let mut lex = Token::lexer("fast.");
    assert_eq!(lex.next(), Some(Ok(Token::Fast)));
    assert_eq!(lex.next(), Some(Ok(Token::Period)));
    assert_eq!(lex.next(), None);
}
```

The entry point `Token::lexer(input)` is a method on the trait itself — the call is on the
type, not on a separate factory. No From/TryFrom; the pipeline is derive macro → iterator
protocol. Errors surface as `Result` items in the iteration, not as a separate parsing step.

This is the most radical instance of "type IS the spec" in the survey: the enum definition —
the shape of the type — generates the complete runtime implementation. Nothing outside the
type definition is needed to describe what the lexer recognizes.


### 11. walrus — Module as four-part machine (rustwasm/walrus)

**Source:** https://github.com/rustwasm/walrus

walrus is a WASM module transformation library. Its architecture maps directly onto the
vision's four-part machine.

Entry points (named constructors, no From/TryFrom):

```rust
pub fn from_buffer(wasm: &[u8]) -> Result<Module>
pub fn from_buffer_with_config(wasm: &[u8], config: &ModuleConfig) -> Result<Module>
pub fn from_file<P>(path: P) -> Result<Module>
```

The coherent input type:

```rust
// src/module/mod.rs
pub struct Module {
    pub imports:   ModuleImports,
    pub tables:    ModuleTables,
    pub types:     ModuleTypes,
    pub funcs:     ModuleFunctions,
    pub globals:   ModuleGlobals,
    pub locals:    ModuleLocals,
    pub exports:   ModuleExports,
    pub memories:  ModuleMemories,
    pub tags:      ModuleTags,
    pub data:      ModuleData,
    pub elements:  ModuleElements,
    pub start:     Option<FunctionId>,
    pub producers: ModuleProducers,
    pub customs:   ModuleCustomSections,
    pub debug:     ModuleDebugData,
    pub name:      Option<String>,
    pub(crate) config: ModuleConfig,
}
```

Every section of the WASM module is a named typed field. The transformation operates on this
type. Emit:

```rust
pub fn emit_wasm(&mut self) -> Vec<u8>
pub fn emit_wasm_file<P>(&mut self, path: P) -> Result<()>
```

Full four-part round-trip:

```rust
// Part 1 + 2: input bytes → coherent Module
let mut module = walrus::Module::from_buffer(&wasm_bytes)?;

// Part 3: transform (operates on Module fields directly)
// e.g. module.funcs.by_name("foo").unwrap().kind = ...

// Part 4: emit as single operation
let output = module.emit_wasm();   // -> Vec<u8>
```

Parse lives in `src/parse.rs`, emit in `src/emit.rs`, wired through `Module`'s own methods.
No trait unifies parsing and emission; the common ground is the `Module` type itself.

**What is absent:** No From/TryFrom (`from_buffer` is a named constructor, not
`Module::try_from(bytes)`). `emit_wasm` takes `&mut self` — it mutates the module during
final serialization, which suggests some finalization step is entangled with emission rather
than being a pure read. No single trait governs all the section-level emission the way
`Encode` does in wasm-encoder.


### 12. bat — Controller and Printer (sharkdp/bat) [counter-example]

**Source:** https://github.com/sharkdp/bat

The central type:

```rust
// src/controller.rs
pub struct Controller<'a> {
    config: &'a Config<'a>,
    assets: &'a HighlightingAssets,
}

impl Controller<'_> {
    pub fn run(&self, inputs: Vec<Input>, output_handle: Option<&mut OutputHandle<'_>>) -> Result<bool>
}
```

This is a textbook service object: it holds collaborators (config, assets) and exposes an
imperative `run` method. It represents a process, not a thing that exists.

Output generation is split across four methods on the `Printer` trait:

```rust
fn print_header(...)
fn print_snip(...)
fn print_line(...)
fn print_footer(...)
```

Output is four side-effectful write calls distributed across the lifetime of a `Printer`
instance. There is no coherent in-memory output type; bytes go out on each call.

The `run()` function in `src/bin/bat/main.rs` is ~80 lines of cascading `match`/`if` over
CLI flags, manually dispatching to different code paths. Each step is a manual call, not a
typed conversion. The schema is between the lines.

bat hits three of the vision's violations simultaneously: service-object naming
(`Controller::run`), output sprawled over four trait methods rather than a single typed
conversion, and an imperative main that hides the schema in procedural logic.


### 11. axum Router — NOT a counter-example

The `Router<S>` wraps a `PathRouter` behind an `Arc` and implements Tower's `Service` trait.
Despite the name, it is thin and does not hold collaborators or expose an imperative `run`
method. It is a type, not a service. The handler pipeline documented in §5 is the real design.


## Part 2: Interpretation for the Skill


### The four-part machine: where each exemplar maps

The vision's four parts — (1) inputs/receiving, (2) coherent input type, (3) coherent output
type, (4) output as a simple operation — are shown in partial form across multiple projects,
and no single project shows all four cleanly in a From/TryFrom chain. The skill should
acknowledge this: the vision is ahead of what the ecosystem has done, which is exactly why it
is a design target rather than an existing convention.

**Coherent input type before doing work:**
walrus's `Module::from_buffer(&bytes) -> Result<Module>` is the clearest example of a
complete four-part machine: raw input (bytes) → coherent typed module (all sections as named
typed fields) → transform operations → `emit_wasm()` single output call. Cargo's
`BuildContext` is the planning-pipeline counterpart: immutable, fully assembled before
handing to the executor. Its doc comment even says so explicitly. The read side of the
`object` crate (`read::File::parse(data) -> Result<Self>`) also matches: bytes go in, a
coherent typed representation comes out, and work happens on that type.

**Coherent output type before writing:**
The object crate's `write::Object` is the cleanest example in the set. Everything accumulates
into the type; `write()` emits it in one call. wasm-encoder's `Module` also demonstrates this,
though its "structured representation" is a byte buffer rather than a typed graph. Neither uses
From/TryFrom to build the output type; they use builder accumulation. The skill can quote these
as partial exemplars: the principle (cohere before write) is demonstrated; the conversion spine
(From/TryFrom) is not.

**Output reviewable in one place under one trait:**
wasm-encoder's `Encode` / `Section` trait pair is the sharpest example anywhere in the set.
Every section type implements `Encode`; `module.section(&s)` calls `s.encode(...)` uniformly.
All output logic lives at the same call site. rustc's `CodegenBackend` (three methods, one
trait, one orchestrator struct) is the large-scale counterpart.

**Capabilities on the type that contains their subject:**
syn's `Parse` trait is the canonical example: `impl Parse for File` — File declares its own
parseability; the cursor is passed in but not the subject. serde's `Serialize` impl on `Value`
is the serialization counterpart: one match, all arms, capability on the type. axum's
`FromRequest` is the request-extraction counterpart: the extracted type declares how to extract
itself.

**Type IS the spec (types-first, contents before behavior):**
logos is the most radical exemplar: the enum definition IS the complete lexer grammar; the
derive macro generates the entire runtime implementation from the type. Nothing outside the
type definition describes what the lexer recognizes. syn's `File` → `Vec<Item>` →
`ItemFn { sig: Signature, block: Block, ... }` is the most quotable example of a type tree
where the structure IS the grammar at the AST level. Gleam's `Module<Info, Definitions>` with
type aliases `UntypedModule` / `TypedModule` is the most quotable example of using type
parameters as stage discriminators.

**No service objects:**
The object crate's write side has none. syn has none (ParseBuffer is a cursor, not a
coordinator). In contrast, bat's `Controller` is the textbook negative case to quote
against.

**The spine is conversions:**
This is the vision's most distinctive claim, and it is the one least reflected in the
ecosystem as surveyed. No project in this set builds its top-level pipeline as
`TryFrom<(A, B)>` chains. axum's `FromRequest` comes closest (it is typed conversion of
inputs) but is async and macro-driven. The ecosystem convention is explicit function calls or
builder accumulation. The skill should name this gap: the vision is a stronger discipline
than anything currently common, and that is the point.

**Output never sprawled:**
bat's `Printer` (four methods, side-effectful, scattered across a session) is the negative
exemplar to quote. Gleam's piecemeal codegen (write per module, inside a loop, no coherent
output type) is the second. wasm-encoder's `module.finish()` is the positive exemplar.

**Main is a few lines tying the spec together:**
rustc's six meaningful driver calls (inside 200 lines of boilerplate) is the closest existing
approximation. Cargo's `compile_ws` (six chained calls: resolve → unit generation → graph →
BuildContext → BuildRunner → compile) is a clean positive example without the boilerplate
problem. Neither reads as pure TryFrom chain. The vision's main sketch — `let output =
OutputType::try_from((a, b))?;` — is not demonstrated in any surveyed project.


### Quotable code for the skill

**logos token enum** — the type IS the spec, in the most literal sense:

```rust
#[derive(Logos, Debug, PartialEq)]
#[logos(skip r"[ \t\n\f]+")]
enum Token {
    #[token("fast")]  Fast,
    #[token(".")]     Period,
    #[regex("[a-zA-Z]+")] Text,
}
// Token::lexer("fast.") -> Lexer<Token> -> Iterator<Item=Result<Token, ()>>
```

The enum shape IS the complete grammar. The derive macro generates everything.

**walrus four-part machine** — the vision's structure shown in the smallest real program:

```rust
let mut module = walrus::Module::from_buffer(&wasm_bytes)?;  // bytes -> coherent input type
// ... transform module fields ...
let output = module.emit_wasm();                              // coherent type -> bytes
```

**wasm-encoder Encode trait** — the single-trait output principle in the smallest possible
space:

```rust
pub trait Encode {
    fn encode(&self, sink: &mut Vec<u8>);
}
pub trait Section: Encode {
    fn id(&self) -> u8;
}
```

Every section type implements both. `module.section(&s)` is the single call site.

**syn Parse on self** — capability declared on the type:

```rust
impl Parse for File {
    fn parse(input: ParseStream) -> Result<Self> { ... }
}
```

**serde Serialize on Value** — clean match, all output logic in one impl:

```rust
impl Serialize for Value {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer {
        match self { ... }   // one arm per variant, nothing escapes
    }
}
```

**rustc CodegenBackend** — output trait reviewable in one definition:

```rust
trait CodegenBackend {
    fn codegen_crate<'tcx>(&self, tcx: TyCtxt<'tcx>) -> Box<dyn Any>;
    fn join_codegen(&self, ...) -> (CompiledModules, WorkProductMap);
    fn link(&self, ...);
}
```

**Gleam stage typing** — type parameter as stage discriminator:

```rust
pub type UntypedModule = Module<(), Vec<TargetedDefinition>>;
pub type TypedModule   = Module<type_::ModuleInterface, TypedDefinitions>;
```

**bat Controller** — service object to quote against:

```rust
pub struct Controller<'a> {
    config: &'a Config<'a>,
    assets: &'a HighlightingAssets,
}
impl Controller<'_> {
    pub fn run(&self, inputs: Vec<Input>, ...) -> Result<bool>
}
```

Holds collaborators, exposes `run`. This is a step wearing the clothes of a thing.


### Gaps the skill should acknowledge

The From/TryFrom conversion spine — the vision's most distinctive claim — is not demonstrated
in any real project at the top level. Axum's `FromRequest` is the closest analogous structure
(typed extraction of inputs from a request), and it is the best available illustration, but it
is async and inverted (inputs come in, not outputs go out). The skill should name this directly:
the vision is a design target, not a description of existing practice, and the examples above
are mined for the _principles_ they embody, not for the exact spelling.


## Sources

- rustc driver, stages, CodegenBackend: https://github.com/rust-lang/rust (compiler/ subtree)
  + https://rustc-dev-guide.rust-lang.org/overview.html
- Gleam Module<Info, Defs>, pipeline, codegen: https://github.com/gleam-lang/gleam
- wasm-encoder Encode/Section/Module: https://github.com/bytecodealliance/wasm-tools
  (crates/wasm-encoder/)
- Cranelift Function/VCode/CompiledCode: https://github.com/bytecodealliance/wasmtime
  (cranelift/ subtree)
- syn File/Item/Parse: https://github.com/dtolnay/syn
- serde Value/Serialize/Visitor: https://github.com/serde-rs/serde + https://github.com/serde-rs/json
- object write::Object, read::File: https://github.com/gimli-rs/object
- cargo BuildContext/BuildRunner/UnitGraph: https://github.com/rust-lang/cargo
- rust-analyzer HIR types, RootDatabase: https://github.com/rust-lang/rust-analyzer
- axum FromRequest/FromRequestParts/IntoResponse: https://github.com/tokio-rs/axum
- logos Logos trait, Lexer, derive macro: https://github.com/maciejhirsz/logos
- walrus Module, from_buffer, emit_wasm: https://github.com/rustwasm/walrus
- bat Controller/Printer: https://github.com/sharkdp/bat


## Supplement — 2026-08-21 (second pass)

Research fills the Cranelift gap from the Sources list and adds two compiler-shaped Rust
tools (oxc, ruff) as further evidence. Method: web research against live GitHub source,
`context.rs`, `compile.rs`, `vcode.rs`, `machinst/mod.rs` for Cranelift; `compiler.rs`
and `semantic/src/lib.rs` for oxc; `linter.rs` and `ruff_python_parser/src/lib.rs` for
ruff.


### S1. Cranelift — Function / VCode\<MachInst\> / CompiledCode

**Source:** https://github.com/bytecodealliance/wasmtime (cranelift/ subtree)

The three stage types:

**Function** — the CLIF IR; the coherent input:

```rust
// cranelift/codegen/src/ir/function.rs
pub struct Function {
    pub name: UserFuncName,
    pub stencil: FunctionStencil,
    pub params: FunctionParameters,
}
```

`FunctionStencil` holds the complete dataflow graph (`dfg: DataFlowGraph`), layout
(`layout: Layout`), signature, stack slots, global values, and source locations.
`FunctionParameters` stores fields that do not affect stencil caching — base source
location and user-defined function references. `Function` is the complete CLIF IR: fully
signed, populated, and named before any machine-code lowering. It implements `Deref` /
`DerefMut` to `FunctionStencil` for field access convenience.

**VCode\<I: VCodeInst\>** — lowered machine-level IR; the internal coherent output:

```rust
// cranelift/codegen/src/machinst/vcode.rs
pub struct VCode<I: VCodeInst> {
    insts: Vec<I>,
    operands: Vec<Operand>,
    operand_ranges: Ranges,
    block_ranges: ...,   // per-block instruction ranges
    block_succs: ...,    // CFG successors
    block_preds: ...,    // CFG predecessors
    srclocs: ...,
    clobbers: ...,
    constants: ...,
    // ...
}
```

`VCodeInst` bounds: `MachInst + MachInstEmit`. `I` is the architecture-specific
instruction type (e.g. `x64::Inst`, `aarch64::Inst`). VCode holds the complete lowered
instruction sequence with register operands resolved by regalloc, but not yet binary-encoded.

**CompiledCode** — the final output:

```rust
// cranelift/codegen/src/machinst/mod.rs
pub type CompiledCode = CompiledCodeBase<Final>;

pub struct CompiledCodeBase<T> {
    pub buffer: MachBufferFinalized<T>,   // machine bytes + relocations
    pub vcode: Option<String>,            // disassembly if requested
    pub value_labels_ranges: ValueLabelsRanges,
    pub bb_starts: Vec<CodeOffset>,
    pub bb_edges: Vec<(CodeOffset, CodeOffset)>,
}
```

`MachBufferFinalized<Final>` contains the raw machine bytes and relocation records. This is
the public output type: bytes are not relocated; callers read relocations from
`compiled_code.buffer.relocs()`.

The transitions:

```rust
// cranelift/codegen/src/context.rs
pub struct Context {
    pub func: Function,
    pub cfg: ControlFlowGraph,
    pub domtree: DominatorTree,
    pub loop_analysis: LoopAnalysis,
    pub(crate) compiled_code: Option<CompiledCode>,
    pub(crate) regalloc_ctx: regalloc2::Ctx,
    pub want_disasm: bool,
}

// Public entry point
pub fn compile(
    &mut self,
    isa: &dyn TargetIsa,
    ctrl_plane: &mut ControlPlane,
) -> CompileResult<'_, &CompiledCode>
```

Inside `compile_stencil()` the internal chain is:

1. `optimize()` — optimization passes run on `self.func` in place
2. `isa.compile_function(&self.func, ...)` calls the internal free function:

```rust
// cranelift/codegen/src/machinst/compile.rs
pub fn compile<B: LowerBackend + TargetIsa>(
    f: &Function,
    domtree: &DominatorTree,
    regalloc_ctx: &mut regalloc2::Ctx,
    b: &B,
    abi: Callee<<<B as LowerBackend>::MInst as MachInst>::ABIMachineSpec>,
    emit_info: <B::MInst as MachInstEmit>::Info,
    sigs: SigSet,
    ctrl_plane: &mut ControlPlane,
) -> CodegenResult<VCode<B::MInst>>
```

3. `VCode::emit()` — encodes the instruction sequence, producing `EmitResult` containing
   `MachBufferFinalized`, block offsets, and optional disassembly text
4. `CompiledCodeStencil::apply_params(&self.func.params)` → `CompiledCode` — applies
   `FunctionParameters` to finalize the stencil into `CompiledCodeBase<Final>`

The caller sees only `Function` going in and `&CompiledCode` coming out; `VCode<I>` is
entirely internal to the pipeline.

**Four-part mapping:**

| Part | Cranelift type | Notes |
|---|---|---|
| (1) inputs/receiving | `Function` assembled by caller | `FunctionBuilder` API or direct field writes |
| (2) coherent input | `Function` | Complete CLIF IR: DFG, layout, signature, params |
| (3) coherent output | `VCode<I>` | All machine instructions + operands; regalloc applied |
| (4) single emission | `CompiledCode` | Machine bytes produced by `VCode::emit()` + `apply_params()` |

Parts 1 and 2 collapse to the same type (`Function`): the coherent input is what the
caller assembles. Part 3 (`VCode<I>`) is hidden from callers; only part 4 is public.

**What is absent:** No From/TryFrom at any stage boundary. `Context::compile()` is a
mutating method that stores its result into `self.compiled_code: Option<CompiledCode>` and
returns a borrow from self — not a typed conversion. `Context` is a mild service object:
it holds `cfg`, `domtree`, `loop_analysis`, and `regalloc_ctx` alongside the data and
exposes an imperative `compile()` method. The two-step finalization
(`CompiledCodeStencil::apply_params()` → `CompiledCode`) is internal machinery that gives
a clean stencil/params separation, but this design detail is invisible at the call site.
`VCode<I>` is the clearest coherent-output type found in the entire survey — complete,
typed, architecture-parameterized — but its concealment means the caller cannot treat
the pipeline as three explicit named stages.


### S2. oxc — ParserReturn / Program / CodegenReturn

**Source:** https://github.com/oxc-project/oxc

oxc is a JavaScript/TypeScript toolchain in Rust: parser, linter (oxlint), transformer,
minifier, formatter. The `CompilerInterface` trait names each stage boundary explicitly.

Named stage return types:

| Stage | Return type | Key contents |
|---|---|---|
| Parse | `ParserReturn<'a>` | `program: Program<'a>`, `errors: Vec<OxcDiagnostic>` |
| Semantic | `SemanticBuilderReturn<'a>` | `semantic: Semantic<'a>`, diagnostics |
| Transform | `TransformerReturn` | diagnostics; AST mutated in place |
| Codegen | `CodegenReturn<'a>` | generated source string |

The central AST type:

```rust
// crates/oxc_ast/src/ast/program.rs
pub struct Program<'a> {
    pub source_text: &'a str,
    pub source_type: SourceType,
    pub hashbang: Option<Hashbang<'a>>,
    pub directives: Vec<'a, Directive<'a>>,
    pub body: Vec<'a, Statement<'a>>,
    // ...
}
```

All AST nodes are arena-allocated via `bumpalo`; the `'a` lifetime threads through every
type. The `CompilerInterface` trait gives an explicit hook after each stage:

```rust
// crates/oxc/src/compiler.rs
pub trait CompilerInterface {
    fn parse_options(&self) -> ParseOptions { ... }
    fn transform_options(&self) -> Option<&TransformOptions> { None }
    fn compress_options(&self) -> Option<CompressOptions> { None }
    fn mangle_options(&self) -> Option<MangleOptions> { None }
    fn codegen_options(&self) -> Option<CodegenOptions> { None }

    fn after_parse(&mut self, ret: &mut ParserReturn) -> ControlFlow<()>;
    fn after_semantic(&mut self, ret: &mut SemanticBuilderReturn) -> ControlFlow<()>;
    fn after_transform(&mut self, program: &mut Program<'_>, ret: &mut TransformerReturn)
        -> ControlFlow<()>;
    fn after_codegen(&mut self, ret: CodegenReturn);
}
```

`compile()` chains: parse → isolated-declarations (opt) → semantic → transform (opt) →
compress (opt) → mangle (opt) → codegen. Each `after_*` hook gives a named boundary and
a `ControlFlow<()>` short-circuit.

**Four-part mapping:**

| Part | oxc type | Notes |
|---|---|---|
| (1) inputs/receiving | `&str` + `Allocator` | source text enters the arena |
| (2) coherent input | `Program<'a>` from `ParserReturn` | complete AST; all syntax present |
| (3) coherent output | none — `Program<'a>` is mutated | transform stages mutate the AST in place |
| (4) single emission | `CodegenReturn<'a>` from `Codegen::build(program)` | one call; generates source string |

Part 3 is the gap: oxc does not construct a distinct coherent output type. Instead,
transform passes mutate `Program<'a>` in place, and the final codegen reads the mutated
AST directly. There is a coherent input (`Program`) and a single emission (`CodegenReturn`),
but no intermediate type that holds the transformed result before emission.

**What is absent:** No From/TryFrom. `Compiler` holds `printed: String` and
`errors: Diagnostics` and drives the pipeline imperatively — a mild service object. The
`after_*` hooks and the per-stage return types (`ParserReturn`, `SemanticBuilderReturn`,
`CodegenReturn`) are the cleanest stage-boundary naming in the survey; they make each
boundary a named type rather than a raw function return. But the absence of a coherent
output type means the vision's three-part output structure (coherent input → coherent
output → single emission) is only half present.


### S3. ruff — Parsed\<ModModule\> / Vec\<Diagnostic\> accumulation

**Source:** https://github.com/astral-sh/ruff

ruff is a Python linter and formatter in Rust. The parse stage is clean; the linting
output side is a counter-example.

The parse output type:

```rust
// crates/ruff_python_parser/src/lib.rs
pub struct Parsed<T> {
    syntax: T,
    tokens: Tokens,
    errors: Vec<ParseError>,
    unsupported_syntax_errors: Vec<UnsupportedSyntaxError>,
}
```

Parsing entry points:

```rust
pub fn parse_module(source: &str) -> Result<Parsed<ModModule>, ParseError>
pub fn parse_unchecked(source: &str, options: ParseOptions) -> Parsed<Mod>
```

`Parsed<T>` is a coherent bundle: syntax tree, token stream, and all parse errors in one
type. This is the cleanest "coherent input type" in the supplement — it bundles everything
that arrived from the parse in a single named type, typed to its AST root (`ModModule`,
`ModExpression`, `Mod`).

The linting entry points:

```rust
// crates/ruff_linter/src/linter.rs
pub fn lint_only(
    path: &Path,
    package: Option<PackageRoot<'_>>,
    settings: &LinterSettings,
    noqa: flags::Noqa,
    source_kind: &SourceKind,
    source_type: PySourceType,
    source: ParseSource,
) -> LinterResult

pub struct LinterResult {
    pub diagnostics: Vec<Diagnostic>,
    has_valid_syntax: bool,
}
```

The internal `check_path()` function accepts a `Parsed<ModModule>` and a mutable
`Vec<Diagnostic>` accumulator, then runs six independent checker passes — token-based,
filesystem-based, logical-line, AST, import, and physical-line — each appending to the
accumulator. `LinterResult` wraps the accumulated vec at the end.

**Four-part mapping:**

| Part | ruff type | Notes |
|---|---|---|
| (1) inputs/receiving | source text + path + settings | |
| (2) coherent input | `Parsed<ModModule>` | complete syntax tree + tokens + parse errors |
| (3) coherent output | none | `Vec<Diagnostic>` accumulated across six passes |
| (4) single emission | `LinterResult` | wraps the vec after accumulation |

Part 3 is the violation. There is no type that represents "all diagnostics assembled"
before any are produced; the accumulation is distributed across six independent checker
passes operating on a shared mutable vec. This is the pattern the psyche named directly
— "output sprawled over everywhere."

**What is absent:** No From/TryFrom. No coherent output type before writing. The
`Parsed<T>` parse output is a positive exemplar — cleaner than any parse-stage type in
the first pass because it is generic over the root AST node and bundles tokens alongside
the tree. The linting output side is the sharpest counter-example for the
output-never-sprawled principle in the full survey: the sprawl is not four methods on one
type (as in bat's `Printer`) but six independent checker passes sharing a mutable
accumulator, with no type boundary between them.


### Closing note: does the second pass change the headline finding?

The first pass concluded: "No project in this set builds its top-level pipeline as
TryFrom<(A, B)> chains. ... The vision is a design target, not a description of existing
practice."

The second pass confirms this unchanged. None of the three new subjects use From/TryFrom:

- Cranelift: `Context::compile()` is a mutating method. `VCode<I>` is the most fully
  developed internal coherent-output type in the survey, but it is hidden from callers and
  the stage boundary is an imperative function call (`compile<B>(f: &Function, ...) ->
  CodegenResult<VCode<B::MInst>>`), not a typed conversion.
- oxc: `CompilerInterface::compile()` is a sequential imperative chain with explicit
  named stage hooks. Per-stage return types are the closest the ecosystem has produced to
  named stage types at the API surface. Still no From/TryFrom.
- ruff: `check_path()` is a monolithic function with a mutable accumulator. The furthest
  from the vision's output-side discipline.

The second pass does sharpen one point from the first pass. Cranelift's `VCode<I>` is
the best existing demonstration that the coherent-output-type position (part 3) has a
viable design: a fully typed, architecture-parameterized, register-allocated instruction
sequence, complete before binary encoding begins. It is absent from the public API only
because `Context` wraps and conceals it. If `VCode<I>` were public, the Cranelift
pipeline would read as a three-type chain (`Function` → `VCode<I>` → `CompiledCode`)
with explicit typed stage names — the closest thing to the vision's structure found
anywhere in the survey. The missing piece remains the From/TryFrom spelling and the
public exposure of the intermediate stage.

**Amended headline:** No project in the extended survey spells its top-level pipeline as
From/TryFrom chains; Cranelift's `Function` → `VCode<I>` → `CompiledCode` is the
clearest existing demonstration that the three-type pipeline structure is feasible,
though the intermediate type is concealed and the transitions are imperative function
calls.


### Additional sources (supplement)

- Cranelift Context/compile/CompiledCode: https://github.com/bytecodealliance/wasmtime
  (cranelift/codegen/src/context.rs, machinst/compile.rs, machinst/vcode.rs, machinst/mod.rs)
- Cranelift Function: https://github.com/bytecodealliance/wasmtime
  (cranelift/codegen/src/ir/function.rs)
- oxc Compiler/CompilerInterface/stage types: https://github.com/oxc-project/oxc
  (crates/oxc/src/compiler.rs, crates/oxc_semantic/src/lib.rs)
- ruff Parsed<T>/linter pipeline: https://github.com/astral-sh/ruff
  (crates/ruff_python_parser/src/lib.rs, crates/ruff_linter/src/linter.rs)


## Supplement — 2026-08-22 (logos production replacement)

Replaces the toy logos example from §10 (three variants lifted from logos's own README).
All three candidates below were witnessed by reading the project's actual source file via
raw.githubusercontent.com. None is a README, demo, or test fixture.


### Primary: taplo — SyntaxKind (tamasfe/taplo)

**Standing:** taplo is the dominant Rust TOML toolkit — parser, formatter, LSP server, and
VS Code extension. The `taplo` crate has 1,583,257 downloads on crates.io; the project
has 2,368 GitHub stars (as of 2026-08-22). It is shipped as the TOML backend in the
Taplo VS Code extension (1M+ installs) and is used by cargo-fmt alternatives and several
build-tool ecosystems.

**Source:** `https://github.com/tamasfe/taplo`, file `crates/taplo/src/syntax.rs`
**Witnessed at commit:** `4c8ecf43fa808d2814658a13eee93b02b99faced` (2026-03-11, "Allow leading zeros in dates")
**Verified by:** fetching `raw.githubusercontent.com/tamasfe/taplo/<commit>/crates/taplo/src/syntax.rs` directly.

```rust
#[derive(Logos, Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[repr(u16)]
pub enum SyntaxKind {
    #[regex(r"([ \t])+")]
    WHITESPACE = 0,

    #[regex(r"(\n|\r\n)+")]
    NEWLINE,

    #[regex(r"#[^\n\r]*")]
    COMMENT,

    #[regex(r"[A-Za-z0-9_-]+", priority = 2)]
    IDENT,

    #[regex(r"[*?A-Za-z0-9_-]+")]
    IDENT_WITH_GLOB,

    #[token(".")]  PERIOD,
    #[token(",")]  COMMA,
    #[token("=")]  EQ,

    #[regex(r#"""#, lex_string)]
    STRING,

    #[regex(r#"""""#, lex_multi_line_string)]
    MULTI_LINE_STRING,

    #[regex(r#"'"#, lex_string_literal)]
    STRING_LITERAL,

    #[regex(r#"'''"#, lex_multi_line_string_literal)]
    MULTI_LINE_STRING_LITERAL,

    #[regex(r"[+-]?[0-9_]+", priority = 4)]
    INTEGER,

    #[regex(r"0x[0-9A-Fa-f_]+")]  INTEGER_HEX,
    #[regex(r"0o[0-7_]+")]        INTEGER_OCT,
    #[regex(r"0b(0|1|_)+")]       INTEGER_BIN,

    #[regex(r"[-+]?([0-9_]+(\.[0-9_]+)?([eE][+-]?[0-9_]+)?|nan|inf)", priority = 3)]
    FLOAT,

    #[regex(r"true|false")]
    BOOL,

    // [trim: DATE_TIME_OFFSET regex — 220-char RFC 3339 offset datetime pattern]
    DATE_TIME_OFFSET,

    // [trim: DATE_TIME_LOCAL regex — same pattern without timezone suffix]
    DATE_TIME_LOCAL,

    // [trim: DATE regex — ISO 8601 calendar date, leap-year aware]
    DATE,

    #[regex(r#"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:(?:\.|,)\d+)?"#)]
    TIME,

    #[token("[")] BRACKET_START,
    #[token("]")] BRACKET_END,
    #[token("{")] BRACE_START,
    #[token("}")] BRACE_END,

    #[error]
    ERROR,

    // CST-only composite nodes — no logos attributes; the parser constructs these
    // from sequences of the lexer variants above:
    KEY,
    VALUE,
    TABLE_HEADER,
    TABLE_ARRAY_HEADER,
    ENTRY,
    ARRAY,
    INLINE_TABLE,
    ROOT,
}
```

The full datetime regexes (trimmed above) are 180–220 characters each; they are ISO 8601
patterns correct to the leap-year rule. The `priority =` annotations on IDENT, INTEGER, and
FLOAT resolve scan-time ambiguity (e.g. `2024-01-01` must not be tokenized as INTEGER minus
INTEGER).

**What this shows:** The enum doubles as both the logos-driven lexer token set and the full
CST node vocabulary. The trailing variants (KEY through ROOT) carry no logos attributes; the
parser assembles them from sequences of the attributed variants. The derive generates the
entire lexer state machine from the attributed subset alone. The callback arguments
(`lex_string`, `lex_multi_line_string`) handle TOML's multi-line and escape-sequence rules
inside the derived machine — the enum shape hands off to a function only where the pattern
language is insufficient.


### Runner-up 1: protox-parse — Token\<'a\> (andrewhickman/protox)

**Standing:** protox is a pure-Rust protobuf compiler, a drop-in alternative to `protoc`
for use with prost-build and tonic-build. `protox-parse` has 4,627,019 crates.io downloads,
pulled in by the prost/tonic ecosystem. GitHub stars are modest (121) because the crate is
consumed as a library dependency, not a developer tool. Shipped real protobuf compilation in
production prost-build pipelines.

**Source:** `https://github.com/andrewhickman/protox`, file `protox-parse/src/lex/mod.rs`
**Witnessed at commit:** `8da890916797268f38d88fbd45648d1e804ff399` (2026-07-27, "Bump logos and prost-reflect to newer versions")

The enum (22 variants, complete — no trimming needed):

```rust
#[derive(Debug, Clone, Logos, PartialEq, Eq)]
#[logos(extras = TokenExtras)]
#[logos(skip r"[\t\v\f\r ]+")]
#[logos(subpattern exponent = r"[eE][+\-]?[0-9]+")]
pub(crate) enum Token<'a> {
    #[regex("[A-Za-z_][A-Za-z0-9_]*")]
    Ident(&'a str),
    #[regex("0",                              |_| 0)]
    #[regex("0[0-7]+",                        |lex| int(lex, 8, 1))]
    #[regex("[1-9][0-9]*",                    |lex| int(lex, 10, 0))]
    #[regex("0[xX][0-9A-Fa-f]+",             |lex| int(lex, 16, 2))]
    IntLiteral(u64),
    #[regex("0[fF]",                          float)]
    #[regex("[1-9][0-9]*[fF]",               float)]
    #[regex(r"[0-9]+\.[0-9]*(?&exponent)?[fF]?", float)]
    #[regex(r"[0-9]+(?&exponent)[fF]?",      float)]
    #[regex(r"\.[0-9]+(?&exponent)?[fF]?",   float)]
    FloatLiteral(EqFloat),
    #[regex(r#"'|""#, string)]
    StringLiteral(Cow<'a, [u8]>),
    #[token(".")]  Dot,
    #[token("-")]  Minus,
    #[token("+")]  Plus,
    #[token("(")]  LeftParen,
    #[token(")")]  RightParen,
    #[token("{")]  LeftBrace,
    #[token("}")]  RightBrace,
    #[token("[")]  LeftBracket,
    #[token("]")]  RightBracket,
    #[token("<")]  LeftAngleBracket,
    #[token(">")]  RightAngleBracket,
    #[token(",")]  Comma,
    #[token("=")]  Equals,
    #[token(":")]  Colon,
    #[token(";")]  Semicolon,
    #[token("/")]  ForwardSlash,
    #[regex(r"(//|#)[^\n]*\n?", line_comment, allow_greedy = true)]
    LineComment(Cow<'a, str>),
    #[token(r"/*", block_comment)]
    BlockComment(Cow<'a, str>),
    #[token("\n")]
    Newline,
}
```

Notable: every variant has a logos attribute — the enum is a pure specification with no
synthesized variants. `Token<'a>` borrows directly from the source buffer (`&'a str`,
`Cow<'a, [u8]>`) — zero allocation per token. `#[logos(subpattern exponent = ...)]` factors
a shared sub-regex across five float variants; this is a logos feature not shown in any
README example.


### Runner-up 2: starlark-rust — Token (facebook/starlark-rust)

**Standing:** A Rust implementation of the Starlark language (Bazel's/Buck2's configuration
language), maintained by Meta. Ships as the Starlark LSP and is the runtime under Buck2.
1,010 GitHub stars; `starlark_syntax` crate has 797,743 downloads.

**Source:** `https://github.com/facebook/starlark-rust`, file `starlark_syntax/src/lexer.rs`
**Witnessed at commit:** `a5250ca38645c0cd3cd9c0d19789dabf01d87d89` (2026-05-20, "f-string expressions")

The `Token` enum has approximately 80 variants. About 55 carry `#[token]`/`#[regex]`
attributes (the logos-driven set); the remainder — `Indent`, `Dedent`, `String`, `Bytes`,
`Int`, `FStringStart`, `FStringText`, `FStringExprStart`, `FStringExprEnd`, `FStringBang`,
`FStringEnd` — are synthesized by a wrapper iterator that consumes the logos output and
handles Python-style indentation and multi-token string/f-string assemblies. The two-tier
design (logos-driven + synthesized) is the standard logos pattern for context-sensitive
tokens. At 80 variants the full enum is too large to quote at skill scale; the taplo and
protox-parse enums above are the better teaching targets.


### Sources (supplement 2026-08-22)

- taplo SyntaxKind: https://github.com/tamasfe/taplo (crates/taplo/src/syntax.rs)
  commit 4c8ecf43fa808d2814658a13eee93b02b99faced
- protox-parse Token: https://github.com/andrewhickman/protox (protox-parse/src/lex/mod.rs)
  commit 8da890916797268f38d88fbd45648d1e804ff399
- starlark-rust Token: https://github.com/facebook/starlark-rust (starlark_syntax/src/lexer.rs)
  commit a5250ca38645c0cd3cd9c0d19789dabf01d87d89


## Supplement — 2026-08-22 (argv-derive family: machine from type's shape, naming assessed)

Addendum per coordinator direction: witness the argv-derive family as a second specimen of
"machine from type's shape" — a struct decorated with a derive macro becomes the complete CLI
grammar. The psyche flagged `FromArgs` (argh) for explicit naming assessment against "a name
describes what a value IS at the moment it exists" and the From/TryFrom doctrine. Sources
witnessed by fetching raw.githubusercontent.com directly at pinned commits.


### Design principle demonstrated

`#[derive(Logos)]` and `#[derive(Parser)]`/`#[derive(FromArgs)]` are the same architectural
move in two different domains: the type's shape IS the complete grammar; the derive generates
the entire runtime machine from that shape. For logos the machine is a lexer state machine.
For argv-derive the machine is a command-line argument parser that also generates `--help`
output. In both cases: no separate grammar file, no separate schema definition, no factory
object. The type IS the spec.


### Crate 1: clap derive — `Parser` and `Args` (clap-rs/clap)

**Standing:** 1,064,902,869 crates.io downloads; 16,651 GitHub stars. The dominant Rust CLI
library by a wide margin. clap_derive is the derive layer that was merged from structopt.

**Derive entry points — `clap_derive/src/lib.rs`**
**Witnessed at commit:** `6982fb1c98c7247e38a6d4f04191b94e30497e7b`

```rust
#[proc_macro_derive(Parser, attributes(clap, structopt, command, arg, group))]
pub fn parser(input: TokenStream) -> TokenStream { ... }

#[proc_macro_derive(Args, attributes(clap, command, arg, group))]
pub fn args(input: TokenStream) -> TokenStream { ... }

#[proc_macro_derive(Subcommand, attributes(clap, command, arg, group))]
pub fn subcommand(input: TokenStream) -> TokenStream { ... }

#[proc_macro_derive(ValueEnum, attributes(clap, value))]
pub fn value_enum(input: TokenStream) -> TokenStream { ... }
```

**Real shipped user: fd (sharkdp/fd)**
**Standing:** 44,164 GitHub stars — one of the most starred Rust CLI tools.
**Source:** `src/cli.rs` at commit `ee20f426ddf338ac7ead5c5f00ea49258005caaf`

```rust
#[derive(Parser)]
#[command(
    name = "fd",
    version,
    about = "A program to find entries in your filesystem...",
    max_term_width = 98,
    args_override_self = true,
    group(ArgGroup::new("execs").args(&["exec", "exec_batch", "list_details"])
        .conflicts_with_all(&["max_results", "quiet", "max_one_result"])),
)]
pub struct Opts {
    /// Include hidden directories and files in the search results (default:
    /// hidden files and directories are skipped). Files and directories are
    /// considered to be hidden if their name starts with a `.` sign (dot).
    /// The flag can be overridden with --no-hidden.
    #[arg(long, short = 'H', help = "Search hidden files and directories", long_help)]
    pub hidden: bool,

    #[arg(long, overrides_with = "hidden", hide = true, action = ArgAction::SetTrue)]
    no_hidden: (),

    /// Show search results from files and directories that would otherwise be
    /// ignored by '.gitignore', '.ignore', '.fdignore', or the global ignore file.
    /// The flag can be overridden with --ignore.
    #[arg(long, short = 'I', help = "Do not respect .(git|fd)ignore files", long_help)]
    pub no_ignore: bool,

    // [trim: ~20 more fields following the same pattern — bool flags, Option<T> options,
    //  Vec<T> repeating flags, PathBuf positionals, with doc-comments as long-help text]
}
```

The generating rules baked into the derive: `bool` field → on/off flag; `Option<T>` field →
optional value; `Vec<T>` field → repeating flag; `PathBuf` / `String` with no `long`/`short`
→ positional argument. Doc-comments on fields become `--help` text. `#[arg(long_help)]` uses
the doc-comment as the long-help variant; `help = "..."` overrides the short-help line.
`(trimmed — fd/src/cli.rs has ~120 fields)`

**Naming assessment — `Parser`:**

The struct IS the parsed configuration — an `Opts` instance holds `hidden: bool`,
`no_ignore: bool`, a path pattern, etc. It IS parsed arguments.

`Parser` names a mechanism: "something that parses." The struct does not parse; the derived
implementation parses to produce the struct. The name inverts identity: a struct IS a result,
not a mechanism. An `Opts` that was produced by parsing IS parsed options, not a parser.

Compare: `#[derive(Args)]` (used on sub-structs that get flattened into a parent) is
correctly named — the struct IS args. `#[derive(Parser)]` on the root struct applies
the mechanism name to the result. This is a consistent violation of "a name describes what a
value IS at the moment it exists": at the moment an `Opts` value exists, it is not parsing
anything; it IS a set of parsed options.

Note: the `structopt` attribute still listed in `Parser`'s attribute list (`attributes(clap,
structopt, ...)`) is a backward-compat remnant from the structopt merger. It does not affect
names but shows how migration compatibility embeds historical naming into the derive.


### Crate 2: argh — `FromArgs` (google/argh)

**Standing:** 15,350,997 crates.io downloads; 1,949 GitHub stars. Google's internal CLI
arg parser for Rust, extracted from the Fuchsia codebase.

**`FromArgs` trait — `argh/src/lib.rs`**
**Witnessed at commit:** `939affd3acc60395bb34749cabb80cc19bcd20eb`

```rust
pub trait FromArgs: Sized {
    fn from_args(command_name: &[&str], args: &[&str]) -> Result<Self, EarlyExit>;

    fn redact_arg_values(
        _command_name: &[&str],
        _args: &[&str],
    ) -> Result<Vec<String>, EarlyExit> {
        Ok(vec!["<<REDACTED>>".into()])
    }
}

pub trait TopLevelCommand: FromArgs {}
```

Two methods: `from_args` constructs `Self` from the argv chain; `redact_arg_values` returns
flag names with values stripped (for telemetry). `TopLevelCommand` is a zero-method marker
supertrait gating `from_env()`.

**Real shipped user: termscp (veeso/termscp)**
**Standing:** 3,051 GitHub stars — TUI SSH/SCP/SFTP/S3 file manager.
**Source:** `src/cli.rs` at commit `08c51a32cc43e68ec2498ba0dcf184375fc501de`

```rust
#[derive(Default, FromArgs)]
#[argh(description = "...")]
pub struct Args {
    #[argh(subcommand)]
    pub nested: Option<ArgsSubcommands>,
    /// resolve address argument as a bookmark name
    #[argh(option, short = 'b')]
    pub bookmark: Vec<String>,
    /// enable TRACE log level
    #[argh(switch, short = 'D')]
    pub debug: bool,
    /// provide password from CLI
    #[argh(option, short = 'P')]
    pub password: Vec<String>,
    /// disable logging
    #[argh(switch, short = 'q')]
    pub quiet: bool,
    // [trim: further fields]
}
```

The generating rules: field-level doc-comment (`///`) becomes `--help` text. `#[argh(switch)]`
→ boolean flag; `#[argh(option)]` → value-taking flag; `#[argh(positional)]` → positional;
`#[argh(subcommand)]` → dispatches to a nested `FromArgs` enum.

**Naming assessment — `FromArgs`:**

`FromArgs` follows the pattern of Rust's `From<T>` trait: "this type can be constructed from
[something]." It names a construction route, not the value's identity. The struct implementing
`FromArgs` IS parsed command-line arguments; the name tells you *how it was obtained*, not
*what it is*.

Against the From/TryFrom doctrine: `FromArgs` is a bespoke single-purpose conversion trait
doing the job that `TryFrom<(&[&str], &[&str])>` would do if `TryFrom` accepted two inputs.
The technical reason it exists separately — `from_args` takes two parameters
(`command_name, args`) which cannot map onto `TryFrom`'s single input — is real, but the
result is a private conversion trait that duplicates the shape of a standard one without
being part of the standard conversion infrastructure.

Against "a name describes what a value IS at the moment it exists": at the moment an `Args`
value (e.g. termscp's `Args`) exists, it IS parsed arguments — flags that have been read,
validated, and stored. `FromArgs` names the capability used to construct it, not what it is.
The struct name `Args` is well chosen (the user named it); the trait name `FromArgs` is where
the identity drift lives.

The name `TopLevelCommand` is a pure capability marker with no behavioral content — it
describes a role in the command hierarchy, which is closer to what the value IS (a top-level
command) than a construction-route name.


### Comparison across the family

| Derive | Names what the value IS? | Doctrine verdict |
|---|---|---|
| `Options` (gumdrop) | Yes — "a set of options" | Correct |
| `Args` (clap sub-struct) | Yes — "a set of arguments" | Correct |
| `Bpaf` (bpaf) | Neutral — library name | Uninformative but not wrong |
| `FromArgs` (argh) | No — names construction route | Follows From<T> convention but drifts from identity |
| `Parser` (clap root) | No — names mechanism, not result | Inverted: the struct IS parsed config, not a parser |

The two well-named derives (`Options`, `Args`) are less deployed than the two poorly named
ones (`Parser`, `FromArgs`). The dominant ecosystem name (`Parser`) is the worst on the
doctrine's terms.


### Does any argv-derive candidate beat the current best candidates?

**For the logos/lexer slot** (currently: taplo `SyntaxKind`): no. The argv-derive family is
a different domain and a different slot. taplo is unchanged as the logos specimen.

**For a second "machine from type's shape" slot**: clap's `Parser` derive with fd's `Opts`
has stronger standing than any single logos example — 1B downloads and a 44K-star reference
project — and demonstrates the same architectural principle (struct shape IS grammar, derive
generates complete runtime machine). The naming critique makes it simultaneously a positive
exemplar (for the design principle) and a critique target (for the doctrine violation). argh
+ termscp is the cleaner, smaller example when the naming complexity would distract.

Neither slot displaces the other. The skill draft can place logos (taplo `SyntaxKind`) and
argv-derive (clap `Parser` / fd `Opts`) as two specimens of the same principle in different
domains, with the naming assessment on `Parser` and `FromArgs` as an explicit callout.


### Sources (supplement 2026-08-22, argv-derive)

- argh FromArgs trait: https://github.com/google/argh (argh/src/lib.rs)
  commit 939affd3acc60395bb34749cabb80cc19bcd20eb
- argh_derive proc-macro: https://github.com/google/argh (argh_derive/src/lib.rs)
  commit 939affd3acc60395bb34749cabb80cc19bcd20eb
- termscp Args struct: https://github.com/veeso/termscp (src/cli.rs)
  commit 08c51a32cc43e68ec2498ba0dcf184375fc501de
- clap_derive Parser/Args/Subcommand/ValueEnum: https://github.com/clap-rs/clap (clap_derive/src/lib.rs)
  commit 6982fb1c98c7247e38a6d4f04191b94e30497e7b
- fd Opts struct: https://github.com/sharkdp/fd (src/cli.rs)
  commit ee20f426ddf338ac7ead5c5f00ea49258005caaf
- bpaf Bpaf derive: https://github.com/pacak/bpaf
- gumdrop Options trait: https://github.com/murarth/gumdrop

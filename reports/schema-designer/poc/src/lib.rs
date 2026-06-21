//! Self-contained POC for the client-side schema "help" projection.
//!
//! Settled design (Spirit `6th4` + the design exchange):
//!   * Help is resolved **entirely client-side**. The daemon never sees a Help
//!     request; nothing about Help lives in the daemon's `Input` contract.
//!   * `(Help X)` resolves to an **actualized typed help data-tree** — a value
//!     of [`HelpTree`], a Rust type, NOT a string. The CLI renders NOTA from
//!     that typed value at the text edge.
//!   * The whole [`HelpModel`] family and [`HelpTree`] derive rkyv
//!     UNCONDITIONALLY, so the typed tree is embeddable / transmittable as
//!     binary even on a daemon (default, no-`nota-text`) build. Only the NOTA
//!     rendering and the CLI recognizer are gated behind `feature = "nota-text"`.
//!   * Each `(Help X)` shows exactly ONE structural level, naming child types;
//!     the reader recurses by navigating (`(Help child)`). Scalars surface at
//!     the newtype boundary as `(Description String)`. Container elements stay
//!     named references: `(Domains (Vec Domain))`.
//!
//! In the real system the model is projected live from each contract's embedded
//! `*_SCHEMA_SOURCE` via `schema_next::SchemaSource::from_schema_text`. This POC
//! is self-contained, so `generated` hand-writes what schema-rust-next would
//! project for a representative spirit subset and builds the same `HelpModel`.

pub mod generated;

#[cfg(feature = "nota-text")]
pub mod render;

/// A schema identifier — a bare NOTA atom that renders verbatim and carries no
/// ancestry. Stands in for `schema_next::Name`.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Name(String);

impl Name {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl From<&str> for Name {
    fn from(text: &str) -> Self {
        Self(text.to_owned())
    }
}

/// The whole projected help table: the Input root table, then the Output root
/// table, then every declaration body. The CLI holds one of these and resolves
/// queries against it.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct HelpModel {
    roots: Vec<RootHelp>,
    declarations: Vec<DeclarationHelp>,
}

/// One top-level root: a request root (Input) or a reply root (Output), its
/// family discriminant, and its immediate argument shape.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct RootHelp {
    name: Name,
    position: RootPosition,
    payload: RootPayload,
}

impl RootHelp {
    pub fn new(name: Name, position: RootPosition, payload: RootPayload) -> Self {
        Self { name, position, payload }
    }

    pub fn name(&self) -> &Name {
        &self.name
    }

    pub fn position(&self) -> RootPosition {
        self.position
    }

    pub fn payload(&self) -> &RootPayload {
        &self.payload
    }
}

/// Groups the bare-`Help` index into the Input table then the Output table.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Copy, Debug, Eq, PartialEq)]
pub enum RootPosition {
    Input,
    Output,
}

/// A root's immediate argument: nothing (a bare variant), or a single reference
/// to the payload type. The payload type is itself Help-able.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum RootPayload {
    Unit,
    Reference(TypeShape),
}

/// One declared type and its body.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct DeclarationHelp {
    name: Name,
    body: DeclarationBody,
}

impl DeclarationHelp {
    pub fn new(name: Name, body: DeclarationBody) -> Self {
        Self { name, body }
    }

    pub fn name(&self) -> &Name {
        &self.name
    }

    pub fn body(&self) -> &DeclarationBody {
        &self.body
    }

    /// Project this declaration into one actualized help node (one level).
    fn entry(&self) -> HelpEntry {
        let shape = match self.body() {
            DeclarationBody::Structure(fields) => HelpShape::Structure(fields.clone()),
            DeclarationBody::Newtype(inner) => HelpShape::Reference(inner.clone()),
            DeclarationBody::Enumeration(variants) => HelpShape::Enumeration(variants.clone()),
        };
        HelpEntry::new(self.name().clone(), shape)
    }
}

/// The three declaration body kinds the one-level render keys on:
///   * `Structure` — ordered field TYPES (all newtypes), expands to `{ ... }`.
///   * `Newtype` — a single reference / scalar; opens one step (`(X String)`).
///   * `Enumeration` — variant list, expands to `[ ... ]`.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum DeclarationBody {
    Structure(Vec<TypeShape>),
    Newtype(TypeShape),
    Enumeration(Vec<VariantShape>),
}

/// One enum variant: its name and an optional payload shape.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct VariantShape {
    name: Name,
    payload: Option<TypeShape>,
}

impl VariantShape {
    pub fn new(name: Name, payload: Option<TypeShape>) -> Self {
        Self { name, payload }
    }

    pub fn name(&self) -> &Name {
        &self.name
    }

    pub fn payload(&self) -> &Option<TypeShape> {
        &self.payload
    }
}

/// A leaf / container type reference. The container heads render to echo the
/// schema source (`Vec` / `Optional` / `Map`); the internal variant names are
/// the canonical schema-next spellings. Recursive, so the rkyv derive uses the
/// `omit_bounds` idiom on the recursive fields.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
#[rkyv(serialize_bounds(
    __S: rkyv::ser::Writer + rkyv::ser::Allocator,
    __S::Error: rkyv::rancor::Source,
))]
#[rkyv(deserialize_bounds(__D::Error: rkyv::rancor::Source))]
#[rkyv(bytecheck(bounds(__C: rkyv::validation::ArchiveContext)))]
pub enum TypeShape {
    Text,
    Integer,
    Boolean,
    Path,
    ByteString,
    FixedByteString(u64),
    Named(Name),
    Vector(#[rkyv(omit_bounds)] Box<TypeShape>),
    Optional(#[rkyv(omit_bounds)] Box<TypeShape>),
    Scope(#[rkyv(omit_bounds)] Box<TypeShape>),
    Mapping(
        #[rkyv(omit_bounds)] Box<TypeShape>,
        #[rkyv(omit_bounds)] Box<TypeShape>,
    ),
    Application(Name, #[rkyv(omit_bounds)] Vec<TypeShape>),
}

impl HelpModel {
    pub fn new(roots: Vec<RootHelp>, declarations: Vec<DeclarationHelp>) -> Self {
        Self { roots, declarations }
    }

    pub fn roots(&self) -> &[RootHelp] {
        &self.roots
    }

    pub fn declarations(&self) -> &[DeclarationHelp] {
        &self.declarations
    }

    pub fn root_named(&self, name: &Name) -> Option<&RootHelp> {
        self.roots.iter().find(|root| root.name() == name)
    }

    pub fn declaration_named(&self, name: &Name) -> Option<&DeclarationHelp> {
        self.declarations.iter().find(|declaration| declaration.name() == name)
    }

    /// Resolve a query to the actualized typed help-tree. This is the heart of
    /// the design: the result is a typed [`HelpTree`] value (rkyv-serializable),
    /// not a string. Rendering NOTA from it is a separate, `nota-text`-only step.
    /// Bare `Help` is every root expanded one level; `(Help X)` is one node.
    pub fn resolve(&self, query: &HelpQuery) -> Result<HelpTree, HelpError> {
        match query.name() {
            None => Ok(HelpTree::Index(
                self.roots().iter().map(|root| self.expand_root(root)).collect(),
            )),
            Some(name) => self.resolve_named(name).map(HelpTree::Topic),
        }
    }

    fn resolve_named(&self, name: &Name) -> Result<HelpEntry, HelpError> {
        if let Some(root) = self.root_named(name) {
            return Ok(self.expand_root(root));
        }
        if let Some(declaration) = self.declaration_named(name) {
            return Ok(declaration.entry());
        }
        Err(HelpError::UnknownName { name: name.as_str().to_owned() })
    }

    /// One-level expansion of a root: a Struct/Enum payload opens to `{ }` / `[ ]`;
    /// a Newtype/scalar/undeclared payload stays the bare reference name.
    fn expand_root(&self, root: &RootHelp) -> HelpEntry {
        let shape = match root.payload() {
            RootPayload::Unit => HelpShape::Unit,
            RootPayload::Reference(TypeShape::Named(payload)) => {
                match self.declaration_named(payload).map(DeclarationHelp::body) {
                    Some(DeclarationBody::Structure(fields)) => {
                        HelpShape::Structure(fields.clone())
                    }
                    Some(DeclarationBody::Enumeration(variants)) => {
                        HelpShape::Enumeration(variants.clone())
                    }
                    Some(DeclarationBody::Newtype(_)) | None => {
                        HelpShape::Reference(TypeShape::Named(payload.clone()))
                    }
                }
            }
            RootPayload::Reference(shape) => HelpShape::Reference(shape.clone()),
        };
        HelpEntry::new(root.name().clone(), shape)
    }
}

/// A resolved help request: list every root, or focus one topic.
pub struct HelpQuery(Option<Name>);

impl HelpQuery {
    pub fn all() -> Self {
        Self(None)
    }

    pub fn topic(name: Name) -> Self {
        Self(Some(name))
    }

    pub fn name(&self) -> Option<&Name> {
        self.0.as_ref()
    }
}

/// Typed per-crate error. No anyhow, no panics.
#[derive(thiserror::Error, Debug, Eq, PartialEq)]
pub enum HelpError {
    #[error("not a help invocation: {0}")]
    NotHelp(String),
    #[error("unknown help topic: {name}")]
    UnknownName { name: String },
}

/// The actualized typed help data-tree — the resolved result of one Help query.
/// A typed value (rkyv-serializable), defined in Rust, held and rendered by the
/// client. The daemon never produces or sees one.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum HelpTree {
    /// Bare `Help`: the signature index — every root, each expanded one level.
    Index(Vec<HelpEntry>),
    /// `(Help X)`: a single node, one level deep.
    Topic(HelpEntry),
}

/// One node of the help tree: a name and its one-level shape.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct HelpEntry {
    name: Name,
    shape: HelpShape,
}

impl HelpEntry {
    pub fn new(name: Name, shape: HelpShape) -> Self {
        Self { name, shape }
    }

    pub fn name(&self) -> &Name {
        &self.name
    }

    pub fn shape(&self) -> &HelpShape {
        &self.shape
    }
}

/// The one-level shape under a name. Children are references (names) or scalar
/// leaves — never inline-expanded; deeper structure is one `(Help child)` away.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum HelpShape {
    /// A bare root: `(Marker)`, `(Version)`.
    Unit,
    /// A newtype / scalar / container / undeclared payload, shown by reference:
    /// `(RecordAccepted RecordIdentifier)`, `(Description String)`,
    /// `(Domains (Vec Domain))`.
    Reference(TypeShape),
    /// A struct body, one level: `{ Entry Justification }`.
    Structure(Vec<TypeShape>),
    /// An enum body, one level: `[Any (Partial DomainScopes) (Full DomainScopes)]`.
    Enumeration(Vec<VariantShape>),
}

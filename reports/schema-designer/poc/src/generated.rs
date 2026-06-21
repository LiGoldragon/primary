//! Stand-in for what `schema-rust-next` projects into a contract crate under its
//! text feature.
//!
//! In the real system this module does not hand-build a `HelpModel`: the emitted
//! per-contract accessor calls `ContractHelpSource::to_help_model`, which parses
//! the contract's embedded `*_SCHEMA_SOURCE` live via
//! `schema_next::SchemaSource::from_schema_text` and projects the model from the
//! resulting `Source*` AST. This POC is self-contained, so the parse is replaced
//! by a hand-written description of a representative spirit subset — but the
//! shape of the output (`HelpModel`) and the projection entry point
//! (`Input::help_model`) are identical to the emitted code.

use crate::{
    DeclarationBody, DeclarationHelp, HelpModel, Name, RootHelp, RootPayload, RootPosition,
    TypeShape, VariantShape,
};

/// The data-bearing holder the emitted accessor owns: the contract's identity
/// plus its (here pre-described) signal source.
pub struct ContractHelpSource {
    component: Name,
    version: Name,
    subset: SignalSubset,
}

impl ContractHelpSource {
    pub fn to_help_model(&self) -> HelpModel {
        HelpModel::from(&self.subset)
    }

    pub fn component(&self) -> &Name {
        &self.component
    }

    pub fn version(&self) -> &Name {
        &self.version
    }
}

/// The `Input` enum the schema emits — a genuine data-bearing enum the help
/// accessor hangs off, exactly as the emitted `impl Input { pub fn help_model()
/// -> HelpModel }` does in the real contract crate.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum Input {
    State(Statement),
    Record(RecordRequest),
    Observe(Query),
    Version,
    Marker,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Statement(String);

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct RecordRequest {
    entry: String,
    justification: String,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Query(String);

impl Input {
    /// The single emitted codegen delta in the real design (here it reads the
    /// hand-written subset instead of parsing the embedded schema source).
    pub fn help_model() -> HelpModel {
        ContractHelpSource::spirit_subset().to_help_model()
    }
}

/// A hand-written description of a representative spirit signal subset, mirroring
/// the parsed sections of `signal.schema` without the schema-next parse.
pub struct SignalSubset {
    input_roots: Vec<RootDescriptor>,
    output_roots: Vec<RootDescriptor>,
    declarations: Vec<DeclarationDescriptor>,
}

/// One root variant before projection.
pub struct RootDescriptor {
    name: Name,
    payload: Option<TypeShape>,
}

impl RootDescriptor {
    fn at(&self, position: RootPosition) -> RootHelp {
        let payload = match &self.payload {
            None => RootPayload::Unit,
            Some(shape) => RootPayload::Reference(shape.clone()),
        };
        RootHelp::new(self.name.clone(), position, payload)
    }
}

/// One declaration before projection.
pub struct DeclarationDescriptor {
    name: Name,
    body: DeclarationBody,
}

impl From<&DeclarationDescriptor> for DeclarationHelp {
    fn from(descriptor: &DeclarationDescriptor) -> Self {
        DeclarationHelp::new(descriptor.name.clone(), descriptor.body.clone())
    }
}

/// The projection itself: Input table, then Output table, then declarations.
impl From<&SignalSubset> for HelpModel {
    fn from(subset: &SignalSubset) -> Self {
        let roots = subset
            .input_roots
            .iter()
            .map(|descriptor| descriptor.at(RootPosition::Input))
            .chain(
                subset
                    .output_roots
                    .iter()
                    .map(|descriptor| descriptor.at(RootPosition::Output)),
            )
            .collect();
        let declarations = subset.declarations.iter().map(DeclarationHelp::from).collect();
        HelpModel::new(roots, declarations)
    }
}

impl ContractHelpSource {
    /// The representative spirit subset the POC navigates. Field/variant nouns
    /// are the real `signal.schema` types, so the rendered help matches the
    /// report's navigation trace verbatim.
    pub fn spirit_subset() -> Self {
        let named = |text: &str| TypeShape::Named(Name::from(text));
        let vec_of = |text: &str| TypeShape::Vector(Box::new(TypeShape::Named(Name::from(text))));
        let optional_of =
            |text: &str| TypeShape::Optional(Box::new(TypeShape::Named(Name::from(text))));
        let structure = |fields: Vec<TypeShape>| DeclarationBody::Structure(fields);
        let newtype = |shape: TypeShape| DeclarationBody::Newtype(shape);
        let scalar = |name: &str| DeclarationDescriptor {
            name: Name::from(name),
            body: DeclarationBody::Newtype(TypeShape::Text),
        };

        let input_roots = vec![
            RootDescriptor { name: Name::from("State"), payload: Some(named("Statement")) },
            RootDescriptor { name: Name::from("Record"), payload: Some(named("RecordRequest")) },
            RootDescriptor { name: Name::from("Observe"), payload: Some(named("Query")) },
            RootDescriptor { name: Name::from("Version"), payload: None },
            RootDescriptor { name: Name::from("Marker"), payload: None },
        ];
        let output_roots = vec![
            RootDescriptor {
                name: Name::from("RecordAccepted"),
                payload: Some(named("RecordIdentifier")),
            },
            RootDescriptor { name: Name::from("Proposed"), payload: Some(named("RecordIdentifier")) },
        ];
        let declarations = vec![
            DeclarationDescriptor {
                name: Name::from("RecordRequest"),
                body: structure(vec![named("Entry"), named("Justification")]),
            },
            DeclarationDescriptor {
                name: Name::from("Entry"),
                body: structure(vec![
                    named("Domains"),
                    named("Kind"),
                    named("Description"),
                    named("Certainty"),
                    named("Importance"),
                    named("Privacy"),
                    named("Referents"),
                ]),
            },
            DeclarationDescriptor {
                name: Name::from("Justification"),
                body: structure(vec![named("Testimony"), named("Reasoning")]),
            },
            DeclarationDescriptor {
                name: Name::from("Domains"),
                body: newtype(vec_of("Domain")),
            },
            DeclarationDescriptor {
                name: Name::from("Referents"),
                body: newtype(vec_of("Referent")),
            },
            DeclarationDescriptor {
                name: Name::from("Testimony"),
                body: newtype(vec_of("VerbatimQuote")),
            },
            DeclarationDescriptor {
                name: Name::from("VerbatimQuote"),
                body: structure(vec![named("QuoteText"), named("OptionalAntecedent")]),
            },
            DeclarationDescriptor {
                name: Name::from("OptionalAntecedent"),
                body: newtype(optional_of("Antecedent")),
            },
            DeclarationDescriptor {
                name: Name::from("Kind"),
                body: DeclarationBody::Enumeration(vec![
                    VariantShape::new(Name::from("Decision"), None),
                    VariantShape::new(Name::from("Principle"), None),
                    VariantShape::new(Name::from("Correction"), None),
                    VariantShape::new(Name::from("Clarification"), None),
                    VariantShape::new(Name::from("Constraint"), None),
                ]),
            },
            DeclarationDescriptor {
                name: Name::from("DomainMatch"),
                body: DeclarationBody::Enumeration(vec![
                    VariantShape::new(Name::from("Any"), None),
                    VariantShape::new(Name::from("Partial"), Some(named("DomainScopes"))),
                    VariantShape::new(Name::from("Full"), Some(named("DomainScopes"))),
                ]),
            },
            scalar("RecordIdentifier"),
            scalar("Description"),
            scalar("Reasoning"),
            scalar("QuoteText"),
            scalar("Antecedent"),
            scalar("Referent"),
        ];
        Self {
            component: Name::from("signal-spirit"),
            version: Name::from("0.8.0"),
            subset: SignalSubset { input_roots, output_roots, declarations },
        }
    }
}

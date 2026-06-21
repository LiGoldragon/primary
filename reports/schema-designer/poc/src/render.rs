//! NOTA rendering of the actualized help tree. Gated behind `feature =
//! "nota-text"` — the "CLI" build. Absent from the daemon (default) build, which
//! carries only the rkyv data and never renders.
//!
//! The flow is: recognize the CLI argument -> `HelpQuery` -> `HelpModel::resolve`
//! (a typed `HelpTree`, defined in `lib.rs`, available even on the daemon build)
//! -> `HelpTree::render` (NOTA text, this module only).
//!
//! In the real layer the recognizer is a `#[derive(NotaDecode)]` enum parsed
//! from the single argument over the NOTA codec before any socket connect. This
//! POC has no NOTA codec dependency, so `recognize` delegates tokenizing to
//! `str` rather than hand-rolling a grammar; the data shape and the CLI intercept
//! are identical.

use crate::{
    HelpEntry, HelpError, HelpModel, HelpQuery, HelpShape, HelpTree, Name, TypeShape, VariantShape,
};

/// The CLI recognizer: `Help` -> `All`, `(Help <Name>)` -> `Topic`. Stands in for
/// the `#[derive(NotaDecode)]` enum the real CLI parses from its single argument
/// before connecting to the daemon.
pub enum HelpInvocation {
    All,
    Topic(Name),
}

impl HelpInvocation {
    pub fn recognize(argument: &str) -> Result<Self, HelpError> {
        let trimmed = argument.trim();
        if trimmed == "Help" {
            return Ok(Self::All);
        }
        if let Some(inner) = trimmed
            .strip_prefix('(')
            .and_then(|rest| rest.strip_suffix(')'))
        {
            let mut tokens = inner.split_whitespace();
            if tokens.next() == Some("Help") {
                if let Some(topic) = tokens.next() {
                    if tokens.next().is_none() {
                        return Ok(Self::Topic(Name::from(topic)));
                    }
                }
            }
        }
        Err(HelpError::NotHelp(argument.to_owned()))
    }
}

impl From<HelpInvocation> for HelpQuery {
    fn from(invocation: HelpInvocation) -> Self {
        match invocation {
            HelpInvocation::All => Self::all(),
            HelpInvocation::Topic(name) => Self::topic(name),
        }
    }
}

impl HelpModel {
    /// Resolve and render a help query to its NOTA string — the typed tree is the
    /// intermediate; the string is the edge form.
    pub fn render(&self, query: &HelpQuery) -> Result<String, HelpError> {
        Ok(self.resolve(query)?.render())
    }
}

impl HelpTree {
    /// Render the actualized help tree to positional NOTA. Bare index: one node
    /// per line. Topic: the single node.
    pub fn render(&self) -> String {
        match self {
            Self::Index(entries) => entries
                .iter()
                .map(HelpEntry::render)
                .collect::<Vec<_>>()
                .join("\n"),
            Self::Topic(entry) => entry.render(),
        }
    }
}

impl HelpEntry {
    fn render(&self) -> String {
        let name = self.name().as_str();
        match self.shape() {
            HelpShape::Unit => format!("({name})"),
            HelpShape::Reference(shape) => format!("({name} {})", shape.render()),
            HelpShape::Structure(fields) => {
                let inner = fields
                    .iter()
                    .map(TypeShape::render)
                    .collect::<Vec<_>>()
                    .join(" ");
                format!("({name} {{ {inner} }})")
            }
            HelpShape::Enumeration(variants) => {
                let inner = variants
                    .iter()
                    .map(VariantShape::render)
                    .collect::<Vec<_>>()
                    .join(" ");
                format!("({name} [{inner}])")
            }
        }
    }
}

impl VariantShape {
    fn render(&self) -> String {
        match self.payload() {
            None => self.name().as_str().to_owned(),
            Some(shape) => format!("({} {})", self.name().as_str(), shape.render()),
        }
    }
}

impl TypeShape {
    /// Bare-atom leaves and container applications; heads echo the schema source
    /// (`Vec` / `Optional` / `Map`); no quotation marks.
    fn render(&self) -> String {
        match self {
            Self::Text => "String".to_owned(),
            Self::Integer => "Integer".to_owned(),
            Self::Boolean => "Boolean".to_owned(),
            Self::Path => "Path".to_owned(),
            Self::ByteString => "Bytes".to_owned(),
            Self::FixedByteString(width) => format!("(Bytes {width})"),
            Self::Named(name) => name.as_str().to_owned(),
            Self::Vector(inner) => format!("(Vec {})", inner.render()),
            Self::Optional(inner) => format!("(Optional {})", inner.render()),
            Self::Scope(inner) => format!("(Scope {})", inner.render()),
            Self::Mapping(key, value) => format!("(Map {} {})", key.render(), value.render()),
            Self::Application(head, arguments) => {
                let tail = arguments
                    .iter()
                    .map(Self::render)
                    .collect::<Vec<_>>()
                    .join(" ");
                if tail.is_empty() {
                    format!("({})", head.as_str())
                } else {
                    format!("({} {})", head.as_str(), tail)
                }
            }
        }
    }
}

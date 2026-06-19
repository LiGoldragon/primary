//! Glue seam 1: the criome→router reference conversion.
//!
//! signal-criome and signal-standard each define their OWN crate-local
//! `AuthorizedObjectReference` / `ComponentKind` / `ObjectDigest` /
//! `AuthorizedObjectKind` (signal-criome has no signal-standard dependency), so
//! the two references are structurally identical but distinct types. The
//! conversion is a genuine three-field mapping — not a no-op.
//!
//! Rust's orphan rule forbids `impl From<signal_criome::Ref> for
//! signal_standard::Ref` (neither type is local), so the conversion is owned by
//! a local carrier newtype `AuthorizedHead`: criome's reference converts INTO
//! the carrier, the carrier converts INTO signal-standard's reference. The
//! carrier is the noun the conversion-verb belongs to.
//!
//! Reference, never payload (`57f9`/`m0p2`): the carrier holds only
//! {component, digest, kind} — the router fans a reference, never state bytes.

use signal_criome::AuthorizedObjectReference as CriomeReference;
use signal_standard::{
    AuthorizedObjectKind as StandardObjectKind, AuthorizedObjectReference as StandardReference,
    ComponentKind as StandardComponentKind, ObjectDigest as StandardObjectDigest,
};

/// The authorized head as it crosses the criome→router seam: the
/// content-addressed reference, payload-blind. Owns the cross-vocabulary
/// conversion.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AuthorizedHead {
    component: StandardComponentKind,
    digest: StandardObjectDigest,
    kind: StandardObjectKind,
}

impl AuthorizedHead {
    pub fn component(&self) -> StandardComponentKind {
        self.component
    }

    pub fn digest(&self) -> &StandardObjectDigest {
        &self.digest
    }

    pub fn kind(&self) -> StandardObjectKind {
        self.kind
    }

    /// The component-kind contact point. criome's `ComponentKind` is a subset
    /// of signal-standard's; the cross is the named enum-vs-enum mapping the
    /// carrier owns, not a match scattered at the call site.
    fn cross_component(component: signal_criome::ComponentKind) -> StandardComponentKind {
        use signal_criome::ComponentKind as Source;
        match component {
            Source::Spirit => StandardComponentKind::Spirit,
            Source::Criome => StandardComponentKind::Criome,
            Source::Router => StandardComponentKind::Router,
            Source::Mirror => StandardComponentKind::Mirror,
            Source::Lojix => StandardComponentKind::Lojix,
            Source::Persona => StandardComponentKind::Persona,
            Source::Agent => StandardComponentKind::Agent,
        }
    }

    /// The object-kind contact point. signal-criome carries one extra variant
    /// (`Head`) signal-standard does not; it maps to the closest standard kind.
    fn cross_kind(kind: signal_criome::AuthorizedObjectKind) -> StandardObjectKind {
        use signal_criome::AuthorizedObjectKind as Source;
        match kind {
            Source::Operation => StandardObjectKind::Operation,
            Source::Contract => StandardObjectKind::Contract,
            Source::Agreement => StandardObjectKind::Agreement,
            Source::Time => StandardObjectKind::Time,
        }
    }
}

/// criome's reference → the carrier. Maps each of the three fields across the
/// two vocabularies; both `ObjectDigest`s are `String` newtypes, so the digest
/// crosses by its string content (content-addressed, preserved exactly).
impl From<CriomeReference> for AuthorizedHead {
    fn from(reference: CriomeReference) -> Self {
        Self {
            component: Self::cross_component(reference.component),
            digest: StandardObjectDigest::new(reference.digest.as_str().to_owned()),
            kind: Self::cross_kind(reference.kind),
        }
    }
}

/// The carrier → signal-standard's reference: what the router publishes.
impl From<AuthorizedHead> for StandardReference {
    fn from(head: AuthorizedHead) -> Self {
        StandardReference::new(head.component, head.digest, head.kind)
    }
}

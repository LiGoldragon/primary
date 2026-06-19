//! The router leg: type-fanout of the authorized-head reference.
//!
//! REAL on the falsifiable line: the production `RouterRuntime` (main HEAD,
//! ce578f1) forwards both `AttendAuthorizedObjects` and
//! `PublishAuthorizedObjectReference` to its internal `AuthorizedObjectFanout`
//! (router.rs:1580, :1610); the fanout's `publish` filters subscribers by
//! `reference.matches_interest(&token.interest)` (router authorized_object.rs:126,
//! signal-standard lib.rs:70-79) — the SOLE operational matcher (`m0p2`). The
//! router fans a reference, never payload (`57f9`).
//!
//! CUT: cross-host sockets → in-process kameo `ask`; durable attendance table +
//! restart-replay (the attendance-fanout-139 branch) → main HEAD's synchronous
//! `publication.deliveries`.

use kameo::actor::ActorRef;
use router::{
    ActorIdentifier, AttendAuthorizedObjects, AuthorizedObjectPublication,
    PublishAuthorizedObjectReference, RouterRuntime,
};
use signal_standard::{AuthorizedObjectInterest, AuthorizedObjectReference};

/// One attendee on the router's authorized-object fanout: a subscriber
/// identifier paired with the type-interest it advertises. The "type" is
/// signal-standard's `AuthorizedObjectInterest` (Component / ObjectKind / …).
pub struct Attendee {
    subscriber: ActorIdentifier,
    interest: AuthorizedObjectInterest,
}

impl Attendee {
    pub fn new(name: &str, interest: AuthorizedObjectInterest) -> Self {
        Self {
            subscriber: ActorIdentifier::new(name),
            interest,
        }
    }

    pub fn subscriber(&self) -> &ActorIdentifier {
        &self.subscriber
    }

    /// The attendance request this attendee submits to the router.
    pub fn attendance(&self) -> AttendAuthorizedObjects {
        AttendAuthorizedObjects {
            subscriber: self.subscriber.clone(),
            interest: self.interest.clone(),
        }
    }
}

/// The running router as the cluster's type-matcher. Owns attendance
/// registration and reference publication against the real `RouterRuntime`.
pub struct TypeRouter {
    runtime: ActorRef<RouterRuntime>,
}

impl TypeRouter {
    /// Start the real production router (offline network configuration).
    pub async fn start() -> Self {
        Self {
            runtime: RouterRuntime::start().await,
        }
    }

    /// Register an attendee's type-interest on the router's authorized-object
    /// fanout.
    pub async fn attend(&self, attendee: &Attendee) {
        self.runtime
            .ask(attendee.attendance())
            .await
            .expect("router accepts authorized-object attendance");
    }

    /// Publish the authorized-head reference; the router matches it by TYPE and
    /// returns exactly the type-matched delivery set.
    pub async fn publish(
        &self,
        reference: AuthorizedObjectReference,
    ) -> AuthorizedObjectPublication {
        self.runtime
            .ask(PublishAuthorizedObjectReference { reference })
            .await
            .expect("router publishes the authorized-object reference")
    }
}

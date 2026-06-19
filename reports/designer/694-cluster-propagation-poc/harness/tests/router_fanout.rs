//! STEP 4 — ROUTER type-fanout (standalone falsifiable unit witness).
//!
//! The third named mechanism of report 694: "router passes messages based on
//! their TYPE (signal-standard)." This unit exercises the THIRD hop of the
//! cluster-propagation loop in isolation, against the REAL production matcher —
//! no criome leg, no spirit leg, no mirror. It proves the router fans an
//! authorized-head reference BY TYPE to exactly the matching attendees and to
//! NO others.
//!
//! REAL on the falsifiable line (verified file:line):
//!   * the production `RouterRuntime` (main HEAD ce578f1) is started and forwards
//!     `AttendAuthorizedObjects` (router.rs:1580) and
//!     `PublishAuthorizedObjectReference` (router.rs:1610) to its internal
//!     `AuthorizedObjectFanout` — the SOLE operational matcher (`m0p2`);
//!   * `AuthorizedObjectFanout::publish` filters subscriptions by
//!     `reference.matches_interest(&token.interest)`
//!     (router/src/authorized_object.rs:126);
//!   * `AuthorizedObjectReference::matches_interest`
//!     (signal-standard/src/lib.rs:70-79) is the type-lattice match:
//!     `Component(c)` matches on component-equality, `ObjectKind(k)` on
//!     kind-equality, `ComponentObject` on BOTH, `AnyAuthorizedObject` always.
//!
//! The fanout returns the type-matched delivery set SYNCHRONOUSLY in
//! `publication.deliveries` (authorized_object.rs:134); the harness reads that
//! directly (in-process, no socket push — the cut named in the design). The
//! reference carries only {component, digest, kind} — a reference, never a
//! payload (`57f9`). NO logic is shimmed in this test: the matcher executed is
//! the real crate's.

use std::collections::HashSet;

use cluster_propagation_poc::router_fanout::{Attendee, TypeRouter};
use signal_standard::{
    AuthorizedObjectInterest, AuthorizedObjectKind, AuthorizedObjectReference, ComponentKind,
    ComponentObjectInterest, ObjectDigest,
};

// Multi-thread runtime: the real `RouterRuntime` spawns threaded actors that a
// single-thread runtime rejects (the same constraint the e2e test carries).
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn router_fans_authorized_head_by_type_to_matching_attendees_only() {
    // The authorized-head reference A would emit after its criome authorizes:
    // a Spirit component, an Operation object kind, content-addressed digest D.
    // (Standalone unit: D is a literal here; the e2e binds it to a real spirit
    // committed head. The matcher is digest-blind — it routes on type only —
    // so the proof transfers unchanged.)
    let head = AuthorizedObjectReference::new(
        ComponentKind::Spirit,
        ObjectDigest::new("blake3-of-the-authorized-head"),
        AuthorizedObjectKind::Operation,
    );

    // The real production router as the cluster's sole type-matcher.
    let router = TypeRouter::start().await;

    // Five attendees spanning the full interest lattice. Each advertises a TYPE
    // (signal-standard `AuthorizedObjectInterest`); the router must deliver the
    // {Spirit, Operation} head to exactly those whose interest matches.
    //
    //   MATCH   spirit-b   Component(Spirit)            <- component equality
    //   MATCH   spirit-c   ObjectKind(Operation)        <- kind equality
    //   MATCH   exact      ComponentObject(Spirit,Op)   <- BOTH fields equal
    //   MATCH   any        AnyAuthorizedObject          <- always
    //   MISS    control    Component(Mirror)            <- load-bearing negative
    let attendee_b = Attendee::new(
        "spirit-b",
        AuthorizedObjectInterest::Component(ComponentKind::Spirit),
    );
    let attendee_c = Attendee::new(
        "spirit-c",
        AuthorizedObjectInterest::ObjectKind(AuthorizedObjectKind::Operation),
    );
    let exact = Attendee::new(
        "exact-spirit-operation",
        AuthorizedObjectInterest::ComponentObject(ComponentObjectInterest::new(
            ComponentKind::Spirit,
            AuthorizedObjectKind::Operation,
        )),
    );
    let any = Attendee::new("any-object", AuthorizedObjectInterest::AnyAuthorizedObject);
    // The load-bearing negative: a real attendee of a DIFFERENT type. If the
    // router broadcast instead of matching, this would (wrongly) be delivered.
    let control = Attendee::new(
        "mirror-control",
        AuthorizedObjectInterest::Component(ComponentKind::Mirror),
    );

    router.attend(&attendee_b).await;
    router.attend(&attendee_c).await;
    router.attend(&exact).await;
    router.attend(&any).await;
    router.attend(&control).await;

    // A emits the reference; the REAL fanout matches it by type and returns the
    // type-matched delivery set synchronously.
    let publication = router.publish(head.clone()).await;

    let delivered: HashSet<String> = publication
        .deliveries
        .iter()
        .map(|delivery| delivery.subscriber.as_str().to_owned())
        .collect();

    // --- POSITIVE: every type-matching attendee receives the head. ---
    assert!(
        delivered.contains(attendee_b.subscriber().as_str()),
        "Component(Spirit) attendee B must match the {{Spirit, Operation}} head"
    );
    assert!(
        delivered.contains(attendee_c.subscriber().as_str()),
        "ObjectKind(Operation) attendee C must match the {{Spirit, Operation}} head"
    );
    assert!(
        delivered.contains(exact.subscriber().as_str()),
        "ComponentObject(Spirit, Operation) must match on both fields"
    );
    assert!(
        delivered.contains(any.subscriber().as_str()),
        "AnyAuthorizedObject must match every head"
    );

    // --- NEGATIVE (load-bearing): the non-matching control is NOT delivered. ---
    // This is the falsifiable heart of "by TYPE, not broadcast": a real attendee
    // exists, attended successfully, and is correctly excluded by the matcher.
    assert!(
        !delivered.contains(control.subscriber().as_str()),
        "Component(Mirror) control must NOT receive the Spirit head (router matches by type, not broadcast)"
    );

    // --- The delivery set is EXACTLY the four matchers, no more. ---
    // Proves the matcher excludes by omission, not just the named control:
    // exactly 4 of 5 attendees are delivered.
    assert_eq!(
        publication.deliveries.len(),
        4,
        "exactly the four type-matching attendees are delivered, got {:?}",
        delivered
    );

    // --- Reference, never payload (57f9): the delivered envelope is the
    // {component, digest, kind} reference itself, carrying no state bytes. ---
    for delivery in &publication.deliveries {
        assert_eq!(
            delivery.reference, head,
            "the router fans the reference unchanged — a reference, never a payload"
        );
    }

    // --- ADVERSARIAL second witness: a head of a DIFFERENT type fans to a
    // DIFFERENT set on the same router. If the matcher were a rubber stamp
    // (delivering to whatever attended), both publishes would hit the same set.
    // Here a {Mirror, Contract} head reaches ONLY the control + the any-attendee,
    // and NOT the Spirit/Operation attendees. ---
    let other_head = AuthorizedObjectReference::new(
        ComponentKind::Mirror,
        ObjectDigest::new("blake3-of-a-mirror-contract-head"),
        AuthorizedObjectKind::Contract,
    );
    let other = router.publish(other_head).await;
    let other_delivered: HashSet<String> = other
        .deliveries
        .iter()
        .map(|delivery| delivery.subscriber.as_str().to_owned())
        .collect();
    assert!(
        other_delivered.contains(control.subscriber().as_str()),
        "the Mirror control DOES match a {{Mirror, Contract}} head"
    );
    assert!(
        other_delivered.contains(any.subscriber().as_str()),
        "AnyAuthorizedObject matches the {{Mirror, Contract}} head too"
    );
    assert!(
        !other_delivered.contains(attendee_b.subscriber().as_str()),
        "Component(Spirit) attendee B must NOT match a {{Mirror, Contract}} head"
    );
    assert!(
        !other_delivered.contains(attendee_c.subscriber().as_str()),
        "ObjectKind(Operation) attendee C must NOT match a Contract head"
    );
    assert_eq!(
        other.deliveries.len(),
        2,
        "the {{Mirror, Contract}} head reaches exactly the control + any attendees, got {other_delivered:?}"
    );
}

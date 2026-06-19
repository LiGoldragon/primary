//! The falsifiable end-to-end test (report 694).
//!
//! Machine A's spirit accepts a new state object → its criome authorizes the
//! new AUTHORIZED HEAD under a ROOT CONTRACT requiring 2-of-3 quorum signatures
//! across the principal's three machines → the authorized-head reference is
//! fanned by the ROUTER, matched by TYPE → spirit B and C ACQUIRE the new head
//! and are thereafter INTERCHANGEABLE with A.
//!
//! STEP 1 (scaffold): this test COMPILES and FAILS (red). The real legs are
//! wired; the one deliberately-stubbed hop is the binding of the spirit
//! committed head to the criome operation digest D (the integration seam steps
//! 5 + 9 finish). Until then `head_digest_of` is `todo!()`, so the test panics
//! red at the first hop — the falsifiable target exists and is unmet.

use std::collections::HashSet;

use cluster_propagation_poc::criome_quorum::{ClusterCriome, ClusterQuorum};
use cluster_propagation_poc::glue::AuthorizedHead;
use cluster_propagation_poc::router_fanout::{Attendee, TypeRouter};
use cluster_propagation_poc::spirit_propagation::{Mirror, ProducerSpirit};
use criome::master_key::MasterKey;
use signal_criome::{EvaluationDecision, EvaluationRejectionReason};
use signal_standard::{AuthorizedObjectInterest, AuthorizedObjectKind, ComponentKind};

// Multi-thread runtime: the router spawns threaded actors
// (`HarnessDelivery::spawn_in_thread`) that a single-thread runtime rejects.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn cluster_propagation_three_spirits_interchangeable() {
    let workspace = tempfile::tempdir().expect("harness workspace");
    let path = |name: &str| workspace.path().join(name);

    // --- The principal's three machines (p3td self-quorum) + cluster root. ---
    let quorum = ClusterQuorum::generate();
    let cluster_root = MasterKey::generate().expect("cluster root key");

    // --- One criome holding all three keys under the 2-of-3 root contract. ---
    // Admission runs the real `is_valid_majority` guard; the ermr gate admits
    // each machine key under the cluster root.
    let (criome, root_contract) = ClusterCriome::admit_cluster(
        criome::StoreLocation::new(path("criome.sema")),
        &cluster_root,
        &quorum,
    )
    .await;

    // A parallel sub-majority (2-of-5) contract MUST be rejected at admission —
    // proof the majority guard is real.
    // (Asserted inside the criome leg's unit test; the e2e exercises the
    //  positive admission above.)

    // --- The in-process mirror + machine A's producer spirit, armed to ship. --
    let mirror = Mirror::start(path("mirror.sema")).await;
    let mut producer = ProducerSpirit::start(path("spirit-a.sema"), &mirror);

    // --- One router; attendees by TYPE (4-rung coverage + load-bearing -ve). --
    let router = TypeRouter::start().await;
    let attendee_b = Attendee::new(
        "spirit-b",
        AuthorizedObjectInterest::Component(ComponentKind::Spirit),
    );
    let attendee_c = Attendee::new(
        "spirit-c",
        AuthorizedObjectInterest::ObjectKind(AuthorizedObjectKind::Operation),
    );
    let control = Attendee::new(
        "mirror-control",
        AuthorizedObjectInterest::Component(ComponentKind::Mirror),
    );
    router.attend(&attendee_b).await;
    router.attend(&attendee_c).await;
    router.attend(&control).await;

    // === HOP 1+2: A accepts a new state object, commits, ships the head. ===
    producer.accept("the cluster head is authoritative").await;
    producer.ship_head().await;
    // D = content-addressed digest of the committed head (MirrorHead.entry_digest
    // folded through OperationDigest::from_bytes) — the SAME identity the criome
    // authorizes and the acquirers restore to. Bound to real committed state.
    let head = producer.head_digest();
    let moment = quorum.attested_moment(10, 20);

    // === HOP 2 (authorize): the criome authorizes D under the 2-of-3 quorum. ===
    // REAL 2-of-3 positive: two members' operation signatures -> Authorized, and
    // the criome pulses {Spirit, D, Operation}.
    let reference = criome
        .authorize_head(
            root_contract.clone(),
            quorum.evidence_with_quorum(&head, &moment),
        )
        .await;
    assert_eq!(reference.component, signal_criome::ComponentKind::Spirit);
    assert_eq!(reference.kind, signal_criome::AuthorizedObjectKind::Operation);

    // REAL 2-of-3 negative: one member's signature -> Rejected(QuorumShort) —
    // makes "2-of-3" falsifiable. Run on the standalone evaluate path.
    let below = criome
        .submit(signal_criome::CriomeRequest::EvaluateAuthorization(
            signal_criome::AuthorizationEvaluation {
                contract: root_contract.clone(),
                evidence: quorum.evidence_below_quorum(&head, &moment),
            },
        ))
        .await;
    let signal_criome::CriomeReply::AuthorizationEvaluated(below) = below else {
        panic!("expected AuthorizationEvaluated for the sub-quorum, got {below:?}");
    };
    assert!(
        matches!(
            below.decision,
            EvaluationDecision::Rejected(EvaluationRejectionReason::QuorumShort(_))
        ),
        "one-of-three must be rejected as QuorumShort, got {:?}",
        below.decision
    );

    // === HOP 2->3 (fan): glue seam 1 converts the reference; router matches. ==
    let head_carrier = AuthorizedHead::from(reference);
    let publication = router.publish(head_carrier.into()).await;

    // REAL match-by-TYPE, not broadcast.
    let delivered: HashSet<String> = publication
        .deliveries
        .iter()
        .map(|delivery| delivery.subscriber.as_str().to_owned())
        .collect();
    assert!(
        delivered.contains(attendee_b.subscriber().as_str()),
        "Component(Spirit) attendee B matched the Spirit head"
    );
    assert!(
        delivered.contains(attendee_c.subscriber().as_str()),
        "ObjectKind(Operation) attendee C matched the Operation head"
    );
    assert!(
        !delivered.contains(control.subscriber().as_str()),
        "Component(Mirror) control is NOT delivered the Spirit head (load-bearing negative)"
    );

    // === HOP 3->4 (acquire): per delivery, acquire into a fresh spirit store. =
    let store_b = mirror.acquire_into(path("spirit-b.sema")).await;
    let store_c = mirror.acquire_into(path("spirit-c.sema")).await;

    // === INTERCHANGEABLE with A (content-addressed). ===
    assert_eq!(
        store_b.database_marker(),
        producer.store().database_marker(),
        "B's restored head is content-identical to A"
    );
    assert_eq!(
        store_c.database_marker(),
        producer.store().database_marker(),
        "C's restored head is content-identical to A"
    );
    assert_eq!(store_b.len(), producer.store().len());
    assert_eq!(store_c.len(), producer.store().len());

    drop(mirror); // keep the daemon alive until every acquire completes.
}

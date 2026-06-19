//! STEP 2 — the criome 2-of-3 root-contract authorize-head, proven standalone.
//!
//! This is the falsifiable unit witness for the FIRST hop of the cluster loop
//! (report 694): the principal's three machines (`p3td` self-quorum) form a
//! 2-of-3 ROOT CONTRACT (`z9d6` content-addressed composable authorization
//! contract); a new content-addressed head digest is authorized only when a
//! MAJORITY (k=2 of n=3, the `k > n/2` guard, 684 Woe 3) of the machines' real
//! BLS keys sign both the attested moment (`ay3y` a-priori window) and the
//! operation. It runs entirely against the REAL criome evaluator — no logic is
//! shimmed.
//!
//! REAL on the falsifiable line (verified against criome rev 22801af source):
//!   - `QuorumShape::is_valid_majority` k>n/2 guard, language.rs:623-626, fired
//!     at admission (`validate_shape`, :414) and at the time-quorum
//!     (`AttestedMoment::rejection_reason`, :577).
//!   - `Threshold::decide` distinct-signer tally, language.rs:371-395
//!     (`!satisfied_members.contains(member)` => distinct signers only;
//!     `satisfied >= required` => Authorized, else `QuorumShort`).
//!   - `PolicyMember::is_satisfied`/`has_valid_signature_from`, :463/:520-535
//!     (a `KeyMember` counts only with a REAL `verify_bls`-valid signature over
//!     the canonical `OperationStatement`, tag `CRIOME-OPERATION-AUTHORIZATION-V1`).
//!   - real `blst` BLS sign/verify via `MasterKey` (criome master_key.rs).
//!   - the `ermr` admission gate: the registry rejects any identity the cluster
//!     root did not sign (the harness mints each machine's admission by signing
//!     its `RegistrationStatement` — marked harness-minted ceremony, 684 Woe 6).
//!   - Path B end to end: the real `CriomeRoot` actor's `EvaluateAuthorization`
//!     handler (root.rs:203-238) drives `store.evaluate` and, on `Authorized`,
//!     publishes the `AuthorizedObjectUpdate` pulse carrying the typed reference.
//!
//! The content-addressed head digest is `OperationDigest::from_bytes(..)`
//! (blake3, signal-criome lib.rs:78-81) — this unit deliberately does NOT depend
//! on the spirit committed head (that binding is the e2e's step 5+9 seam); it
//! proves the quorum logic over an arbitrary content-addressed digest, exactly
//! the digest shape the spirit head will later occupy.

use cluster_propagation_poc::criome_quorum::{ClusterCriome, ClusterQuorum};
use criome::master_key::MasterKey;
use signal_criome::{
    AuthorizationEvaluation, AuthorizedObjectInterest, AuthorizedObjectKind, ComponentKind,
    CriomeReply, CriomeRequest, EvaluationDecision, EvaluationRejectionReason, OperationDigest,
};

/// Multi-thread runtime: `CriomeRoot` spawns threaded kameo actors a
/// single-thread runtime would reject.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn criome_authorizes_two_of_three_and_rejects_one_of_three() {
    let workspace = tempfile::tempdir().expect("harness workspace");

    // --- The principal's three machines, each a real `blst` BLS key. ---
    let quorum = ClusterQuorum::generate();
    let cluster_root = MasterKey::generate().expect("cluster root key");

    // --- One criome: mint+register each machine's admission through the REAL
    // `ermr` gate, then admit the 2-of-3 root contract. Admission runs the real
    // `is_valid_majority` guard (2 > 3/2 passes). ---
    let (criome, root_contract) = ClusterCriome::admit_cluster(
        criome::StoreLocation::new(workspace.path().join("criome.sema")),
        &cluster_root,
        &quorum,
    )
    .await;

    // === NEGATIVE 1 — admission majority guard ===
    // A sub-majority 2-of-5 contract (this quorum's 3 members + 2 phantoms): 2 is
    // NOT > 5/2 = 2, so the REAL `is_valid_majority` guard MUST reject it at
    // admission. This proves the guard is the gate, not a rubber stamp — without
    // it, "2-of-3" would be meaningless because any (k, n) would admit.
    let sub_majority = criome
        .submit(CriomeRequest::AdmitContract(quorum.sub_majority_contract()))
        .await;
    assert!(
        matches!(sub_majority, CriomeReply::ContractAdmissionRejected(_)),
        "the real majority guard MUST reject a 2-of-5 contract at admission, got {sub_majority:?}"
    );
    if let CriomeReply::ContractAdmissionRejected(rejection) = &sub_majority {
        assert_eq!(
            rejection.payload(),
            &signal_criome::ContractAdmissionRejectionReason::ThresholdUnsatisfiable,
            "2-of-5 is rejected specifically as ThresholdUnsatisfiable (k <= n/2)"
        );
    }

    // --- The content-addressed new head the cluster is authorizing. ---
    // blake3 over the head bytes — the exact `OperationDigest` shape the spirit
    // committed head will occupy in the e2e (step 5+9 binds it; here it stands
    // for any content-addressed head, which is all the quorum logic cares about).
    let head = OperationDigest::from_bytes(b"the-cluster-authoritative-head-v1");

    // --- A 2-of-3 attested moment (the TIME quorum, `ay3y` a-priori window).
    // Members A and B sign the `AttestedMomentProposition`; the real
    // `rejection_reason` re-runs the majority guard over the time signatures. ---
    let moment = quorum.attested_moment(10, 20);

    // === POSITIVE — 2-of-3 authorizes, and the typed head is pulsed ===
    // Two members sign the `OperationStatement` for the head. The real
    // `Threshold::decide` tally counts two distinct valid signers >= required 2
    // => Authorized. `authorize_head` additionally asserts the criome published
    // the `AuthorizedObjectUpdate` pulse (Path B emission) and returns the typed
    // reference, observed back by Component(Spirit) interest.
    let reference = criome
        .authorize_head(
            root_contract.clone(),
            quorum.evidence_with_quorum(&head, &moment),
        )
        .await;
    // The authorized head carries the TYPE the router later fans on, and the
    // content-addressed digest D — reference, never payload (`57f9`/`m0p2`).
    assert_eq!(
        reference.component,
        ComponentKind::Spirit,
        "the authorized head is a Spirit object"
    );
    assert_eq!(
        reference.kind,
        AuthorizedObjectKind::Operation,
        "the authorized head is an Operation"
    );
    assert_eq!(
        &reference.digest,
        head.object_digest(),
        "the criome authorized EXACTLY the content-addressed head digest D it was given"
    );

    // === NEGATIVE 2 — sub-quorum 1-of-3 is rejected as QuorumShort ===
    // Only member A signs the operation. The real distinct-signer tally finds 1
    // satisfied < required 2 => Rejected(QuorumShort{required:2, satisfied:1}).
    // This is what makes "2-of-3" falsifiable: a single signer does NOT
    // authorize. Run on the standalone `EvaluateAuthorization` path.
    let below = criome
        .submit(CriomeRequest::EvaluateAuthorization(AuthorizationEvaluation {
            contract: root_contract.clone(),
            evidence: quorum.evidence_below_quorum(&head, &moment),
        }))
        .await;
    let CriomeReply::AuthorizationEvaluated(below) = below else {
        panic!("expected AuthorizationEvaluated for the sub-quorum, got {below:?}");
    };
    match below.decision {
        EvaluationDecision::Rejected(EvaluationRejectionReason::QuorumShort(shortfall)) => {
            assert_eq!(
                *shortfall.required.payload(),
                2,
                "the root contract still requires 2 signatures"
            );
            assert_eq!(
                *shortfall.satisfied.payload(),
                1,
                "exactly one of the three signed, so the tally counts 1"
            );
        }
        other => panic!("one-of-three MUST be Rejected(QuorumShort), got {other:?}"),
    }

    // === The pulse is type-observable AND nothing extra leaked ===
    // Only the one authorized head was pulsed; a non-matching type-interest
    // (Mirror) sees none — the criome's emission is itself typed (`m0p2`).
    let mirror_interest = criome
        .observe(AuthorizedObjectInterest::Component(ComponentKind::Mirror))
        .await;
    assert!(
        mirror_interest.is_empty(),
        "a Mirror-typed observer sees no Spirit head — the pulse is type-scoped, not a broadcast"
    );

    drop(criome);
}

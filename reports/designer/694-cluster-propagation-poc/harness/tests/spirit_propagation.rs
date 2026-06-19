//! STEP 3 — the SPIRIT leg, standalone falsifiable witness (report 694).
//!
//! Machine A's spirit accepts a new state object and produces its
//! content-addressed head; the head ships to the mirror; machines B and C
//! ACQUIRE it and reach state byte-identical to A. This is the
//! spirit→mirror→acquire half of the loop, proven WITHOUT the criome/router
//! legs so the spirit-side claim ("validate-on-criome then propagate →
//! interchangeable", d6he/nfvm) is isolable.
//!
//! REAL on the falsifiable line (rev fe04c12 spirit / b26c139 mirror /
//! 73eea24 sema-engine):
//!   - real `spirit::Engine` accept (`Input::record`) + commit to the
//!     content-addressed log;
//!   - real local `Store::checkpoint`, real `ship_unshipped_to_mirror` over real
//!     loopback TCP to a real `mirror` daemon, real `publish_checkpoint_to_mirror`;
//!   - the content-addressed head digest D derived from the committed
//!     `MirrorHead.entry_digest` (blake3) via `OperationDigest::from_bytes` —
//!     the binding the criome would authorize and the acquirers restore to;
//!   - real `Restore` fetch + fresh `Store::import` for B and C
//!     (`acquire_into`, cloned from spirit/tests/mirror_shipper.rs);
//!   - the interchangeability witness `Store::database_marker()` =
//!     {commit_sequence, blake3 state_digest} over committed state.
//!
//! CUT (consistent with 684 / the design): live in-place `Store::adopt_head` →
//! fresh `Store::import`; physical multi-host → in-process loopback.

use cluster_propagation_poc::spirit_propagation::{Mirror, ProducerSpirit};
use signal_criome::OperationDigest;

// Multi-thread runtime: the mirror daemon spawns threaded actors a single-thread
// runtime rejects.
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn spirit_a_accepts_ships_and_b_c_acquire_interchangeable() {
    let workspace = tempfile::tempdir().expect("harness workspace");
    let path = |name: &str| workspace.path().join(name);

    // --- The in-process mirror + machine A's producer spirit, armed to ship. ---
    let mirror = Mirror::start(path("mirror.sema")).await;
    let mut producer = ProducerSpirit::start(path("spirit-a.sema"), &mirror);

    // A starts empty — the genesis marker is (0, 0). Captured before the write so
    // the post-accept marker is observably DIFFERENT (the accept actually
    // committed state, not a no-op).
    let genesis_marker = producer.store().database_marker();

    // === ACCEPT: A handles a new state object, validates, commits. ===
    producer
        .accept("spirit A accepts the new authoritative cluster head")
        .await;
    let after_accept_marker = producer.store().database_marker();
    assert_ne!(
        after_accept_marker, genesis_marker,
        "the accept committed new content-addressed state (marker advanced from genesis)"
    );
    assert_eq!(
        producer.store().len(),
        1,
        "exactly one record was accepted and committed"
    );

    // === SHIP: A writes a checkpoint, ships the head, publishes the checkpoint. =
    producer.ship_head().await;

    // === The content-addressed head digest D (the criome would authorize this). =
    // D is derived deterministically from the committed head; a second call must
    // yield the IDENTICAL digest (content-addressing is a pure function of state).
    let head_digest: OperationDigest = producer.head_digest();
    assert_eq!(
        head_digest,
        producer.head_digest(),
        "the head digest is a deterministic content-address, stable across calls"
    );

    // === ACQUIRE: B and C each restore into a FRESH store from the mirror. ===
    let store_b = mirror.acquire_into(path("spirit-b.sema")).await;
    let store_c = mirror.acquire_into(path("spirit-c.sema")).await;

    // === INTERCHANGEABLE: B and C reach state byte-identical to A. ===
    // The content-addressed marker (commit_sequence + blake3 state_digest) is the
    // substitutability witness: three independently-restored stores with an equal
    // marker carry identical committed state (nfvm cross-machine self).
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
    assert_eq!(
        store_b.database_marker(),
        store_c.database_marker(),
        "B and C are interchangeable with each other, not just with A"
    );

    // Second witness, human-legible: the committed record count agrees.
    assert_eq!(store_b.len(), producer.store().len());
    assert_eq!(store_c.len(), producer.store().len());

    // Falsifiability guard: the acquired state is the POST-accept state, not the
    // empty genesis A started from — the acquire moved real content, not nothing.
    assert_ne!(
        store_b.database_marker(),
        genesis_marker,
        "B did not merely restore an empty genesis store"
    );

    drop(mirror); // keep the daemon alive until every acquire completes.
}

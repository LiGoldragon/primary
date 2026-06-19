//! The spirit leg: machine A accepts state, ships the content-addressed head to
//! the mirror; machines B and C acquire it and become INTERCHANGEABLE with A.
//!
//! REAL on the falsifiable line: a real `spirit::Engine` over a real `.sema`
//! store handles the accept (`Input::record`), the post-commit ship to a real
//! `mirror` daemon over real loopback TCP, and the fresh `Store::import` restore
//! (cloned from spirit/tests/mirror_shipper.rs). The interchangeability witness
//! is `Store::database_marker()` = `{commit_sequence, state_digest}` (a blake3
//! content digest over committed state, store/mod.rs:1138): three independently
//! restored stores with an equal marker carry byte-identical content-addressed
//! state — A, B, C substitutable (`nfvm` cross-machine self).
//!
//! CUT: live in-place `Store::adopt_head` → fresh `Store::import` (684).

use std::net::SocketAddr;
use std::path::PathBuf;

use mirror::{Engine as MirrorEngine, MirrorTailnetClient as TailnetClient, Service, ServiceLink};
use sema_engine::{MirrorHead, PortableCheckpoint, VersionedCommitLogEntry};
use signal_criome::OperationDigest;
use triad_runtime::kameo::actor::Spawn;
use signal_mirror::{Input as MirrorInput, Output as MirrorOutput, RestoreQuery, StoreName};
use spirit::schema::meta_signal::{
    ArchiveDatabaseTarget, ConfigureRequest, MirrorAddress, MirrorAddressText, MirrorTarget,
    Output as MetaOutput,
};
use spirit::schema::sema::RecordFamily;
use spirit::schema::signal::{
    Certainty, Description, Domains, Entry, Importance, Input, Justification, Kind, Magnitude,
    Output, Privacy, QuoteText, Reasoning, RecordRequest, Referents, Testimony, VerbatimQuote,
};
use spirit::{Engine, Store};

/// The store-name the cluster's spirit history lives under on the mirror —
/// shared by the producer's ship and every acquirer's restore. `RecordFamily`
/// is the schema-emitted noun that owns the canonical name.
const SPIRIT_STORE_NAME: &str = RecordFamily::STORE_NAME;

/// The in-process mirror: a real `mirror` daemon (real engine, real store, real
/// loopback TCP listener) standing in for the content-addressed object store A
/// ships to and B/C restore from. The harness's "in-process mirror" is this
/// daemon over loopback — the transport is real, only the host is shared.
pub struct Mirror {
    link: ServiceLink,
    address: SocketAddr,
}

impl Mirror {
    /// Stand up the mirror daemon at a temp store path and register the spirit
    /// store on its meta surface.
    pub async fn start(store_path: PathBuf) -> Self {
        let store = mirror::Store::open(&store_path).expect("mirror store opens");
        let service = Service::spawn(Service::new(
            MirrorEngine::new(store),
            "127.0.0.1:0".parse().expect("loopback address"),
        ));
        service.wait_for_startup().await;
        let link = ServiceLink::new(service);
        let address = link
            .tcp_bound_address()
            .await
            .expect("query bound address")
            .expect("the tailnet ingress is bound");
        let registered = link
            .meta(meta_signal_mirror::Input::RegisterStore(
                meta_signal_mirror::StoreRegistration::new(meta_signal_mirror::StoreName::new(
                    SPIRIT_STORE_NAME.to_owned(),
                )),
            ))
            .await
            .expect("meta register");
        assert!(matches!(
            registered,
            meta_signal_mirror::Output::StoreRegistered(_)
        ));
        Self { link, address }
    }

    pub fn address(&self) -> SocketAddr {
        self.address
    }

    /// Keep the daemon alive for the test's lifetime.
    pub fn link(&self) -> &ServiceLink {
        &self.link
    }

    /// Acquire the cluster head into a FRESH spirit store: fetch the checkpoint
    /// plus the versioned-log suffix and import them through the engine-owned
    /// import session (cloned from mirror_shipper.rs `restore_from_mirror`).
    /// This is glue seam 2 — driven from a router delivery's reference digest.
    pub async fn acquire_into(&self, path: PathBuf) -> Store {
        let client = TailnetClient::new(self.address);
        let bundle = match client
            .exchange(MirrorInput::Restore(RestoreQuery::new(StoreName::new(
                SPIRIT_STORE_NAME.to_owned(),
            ))))
            .await
            .expect("restore call succeeds")
        {
            MirrorOutput::Restored(bundle) => bundle,
            other => panic!("expected Restored, got {other:?}"),
        };
        let checkpoint = PortableCheckpoint::from_bytes(
            bundle.checkpoint.artifact.payload().payload().to_vec(),
        )
        .decode()
        .expect("decode checkpoint artifact");
        let suffix: Vec<VersionedCommitLogEntry> = bundle
            .suffix()
            .iter()
            .map(|envelope| {
                rkyv::from_bytes::<VersionedCommitLogEntry, rkyv::rancor::Error>(
                    envelope.payload.payload().payload(),
                )
                .expect("decode versioned entry payload")
            })
            .collect();
        Store::import(path, checkpoint, suffix).expect("import into fresh spirit store")
    }
}

/// Machine A's running spirit: a real `Engine` over a real `.sema` store, armed
/// to ship to the mirror. Owns the accept + ship + content-addressed-head verbs.
///
/// After a successful ship the producer holds the `MirrorHead` the ship
/// committed — its `entry_digest()` is the content-addressed identity of the new
/// head, the binding from which the criome operation digest D is derived.
pub struct ProducerSpirit {
    engine: Engine,
    shipped_head: Option<MirrorHead>,
}

impl ProducerSpirit {
    /// Open a real spirit store, start the engine, and arm the mirror shipper
    /// against the running mirror.
    pub fn start(store_path: PathBuf, mirror: &Mirror) -> Self {
        let store = Store::open(store_path).expect("open spirit store");
        let mut engine = Engine::new(store);
        engine.start().expect("engine starts");
        let configured = engine.configure(ConfigureRequest::new(
            ArchiveDatabaseTarget::Default,
            Some(MirrorTarget::Address(MirrorAddress::new(
                MirrorAddressText::new(mirror.address().to_string()),
            ))),
        ));
        assert!(
            matches!(configured, MetaOutput::Configured(_)),
            "configure accepted, got {configured:?}"
        );
        assert!(engine.mirror_shipping_armed(), "the shipper is armed");
        Self {
            engine,
            shipped_head: None,
        }
    }

    pub fn store(&self) -> &Store {
        self.engine.store()
    }

    /// The content-addressed criome operation digest D for the shipped head:
    /// `OperationDigest::from_bytes` over the `MirrorHead.entry_digest()` (a
    /// blake3 digest of the committed log entry). This BINDS the digest the
    /// criome authorizes to the exact committed state the acquirers restore to —
    /// the same head, identified the same way on both sides of the loop. Panics
    /// if called before a successful `ship_head` (no head to bind).
    pub fn head_digest(&self) -> OperationDigest {
        let head = self
            .shipped_head
            .as_ref()
            .expect("ship_head must commit a head before deriving its digest");
        OperationDigest::from_bytes(head.entry_digest().bytes())
    }

    /// Accept a new state object: the real engine handles `Input::record`,
    /// validates, and commits it to the local content-addressed log.
    pub async fn accept(&mut self, description: &str) {
        let output = self
            .engine
            .handle_async(Input::record(RecordRequest {
                entry: Entry {
                    domains: Domains::from_strings(vec![String::from(
                        "Information/Documentation",
                    )]),
                    kind: Kind::Decision,
                    description: Description::new(description),
                    certainty: Certainty::new(Magnitude::High),
                    importance: Importance::new(Magnitude::Medium),
                    privacy: Privacy::new(Magnitude::Zero),
                    referents: Referents::new(Vec::new()),
                },
                justification: Justification {
                    testimony: Testimony::new(vec![VerbatimQuote::new(
                        QuoteText::new(description),
                        None,
                    )]),
                    reasoning: Reasoning::new(description),
                },
            }))
            .await
            .into_root();
        assert!(
            matches!(output, Output::RecordAccepted(_)),
            "record accepted, got {output:?}"
        );
    }

    /// Ship the new head to the mirror: write a local checkpoint, drain the
    /// unshipped versioned-log suffix, and publish the checkpoint the acquirers
    /// fetch. After this the content-addressed head is on the mirror, ready to
    /// fan + acquire. (Mirrors spirit/tests/mirror_shipper.rs: checkpoint then
    /// ship then publish.)
    pub async fn ship_head(&mut self) {
        self.engine
            .store()
            .checkpoint()
            .expect("local checkpoint writes");
        let outcome = self
            .engine
            .ship_unshipped_to_mirror()
            .await
            .expect("ship unshipped")
            .expect("an armed shipper ships");
        let mirror::ShipOutcome::Shipped { head } = outcome else {
            panic!("history shipped, got {outcome:?}");
        };
        // Capture the committed head: its content-addressed `entry_digest` is the
        // identity the criome authorizes and the acquirers restore to.
        self.shipped_head = Some(head);
        assert!(
            self.engine
                .publish_checkpoint_to_mirror()
                .await
                .expect("publish checkpoint"),
            "an armed shipper publishes the checkpoint"
        );
    }
}

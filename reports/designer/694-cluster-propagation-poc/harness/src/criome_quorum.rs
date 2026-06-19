//! The criome leg: the 2-of-3 root-contract authorize-head.
//!
//! REAL on the falsifiable line: `QuorumShape::is_valid_majority` k>n/2 guard
//! (criome language.rs), the distinct-signer `Threshold::decide` tally, real
//! `blst` BLS sign/verify (`MasterKey`), the `ay3y` attested-moment window, the
//! `ermr` admission gate (`ClusterRoot::admits` over a harness-minted
//! admission). CUT: the production cluster-root ceremony (harness mints the
//! admissions, 684 Woe 6); cross-criome peer signature solicitation (the three
//! machines' keys are co-resident — the principal's self-quorum, p3td).
//!
//! Two quorums set to 2-of-3 over [A,B,C]: the OPERATION quorum
//! (`evidence_signatures` over the `OperationStatement`) AND the TIME quorum
//! (`AttestedMoment.time_signatures` over the `AttestedMomentStatement`). The
//! majority guard fires at both sites.

use criome::actors::root::{Arguments, CriomeRoot, SubmitRequest};
use criome::admission::RegistrationStatement;
use criome::language::{AttestedMomentStatement, OperationStatement};
use criome::master_key::MasterKey;
use kameo::actor::ActorRef;
use signal_criome::{
    AttestedMoment, AttestedMomentProposition, AuthorizationEvaluation, AuthorizedObjectInterest,
    AuthorizedObjectObservation, AuthorizedObjectReference, BlsPublicKey, ComponentKind, Contract,
    ContractDigest, CriomeReply, CriomeRequest, EvaluationDecision, Evidence, Identity,
    IdentityRegistration, KeyPurpose, OperationDigest, PolicyMember, PublicKeyFingerprint,
    RequiredSignatureThreshold, Rule, SignatureEnvelope, SignatureScheme, StampedSignatureEnvelope,
    Threshold, TimeSignature, TimeWindow, TimestampNanos,
};

use crate::Machine;

/// One cluster member: a machine's BLS `MasterKey` bound to its criome
/// `Identity`. The principal's three co-located nodes (`p3td` self-quorum);
/// real `blst` keys, so every signature this member produces is real.
pub struct ClusterMember {
    machine: Machine,
    identity: Identity,
    key: MasterKey,
}

impl ClusterMember {
    /// Generate a member with a fresh real BLS key, identified as a cluster
    /// `Host` under the machine's principal name.
    pub fn generate(machine: Machine) -> Self {
        let identity = Identity::host(machine.principal_name().to_owned());
        Self {
            machine,
            identity,
            key: MasterKey::generate().expect("generate real BLS master key"),
        }
    }

    pub fn machine(&self) -> Machine {
        self.machine
    }

    pub fn identity(&self) -> Identity {
        self.identity.clone()
    }

    pub fn public_key(&self) -> BlsPublicKey {
        self.key.public_key()
    }

    /// A real BLS operation signature over the canonical `OperationStatement`
    /// binding this member, the operation digest, and the attested moment —
    /// the unit of the operation quorum.
    pub fn sign_operation(
        &self,
        operation: &OperationDigest,
        stamp: &AttestedMoment,
    ) -> StampedSignatureEnvelope {
        StampedSignatureEnvelope {
            stamp: stamp.clone(),
            envelope: SignatureEnvelope {
                scheme: SignatureScheme::Bls12_381MinPk,
                public_key: self.public_key(),
                signature: self.key.sign(
                    OperationStatement::new(&self.identity, operation, stamp)
                        .to_signing_bytes()
                        .expect("operation statement signing bytes")
                        .as_slice(),
                ),
            },
        }
    }

    /// A real BLS time signature over the canonical `AttestedMomentStatement` —
    /// the unit of the time quorum (`ay3y` a-priori window in the signed
    /// digest).
    pub fn sign_moment(&self, proposition: &AttestedMomentProposition) -> TimeSignature {
        TimeSignature {
            signer: self.identity(),
            envelope: SignatureEnvelope {
                scheme: SignatureScheme::Bls12_381MinPk,
                public_key: self.public_key(),
                signature: self.key.sign(
                    AttestedMomentStatement::new(proposition)
                        .to_signing_bytes()
                        .expect("moment statement signing bytes")
                        .as_slice(),
                ),
            },
        }
    }

    /// This member's identity registration, admitted by the cluster root: the
    /// root signs the canonical `RegistrationStatement` (the real `ermr` gate;
    /// the registry rejects any registration the cluster root has not admitted,
    /// criome registry.rs:101-104). The ceremony is harness-minted (684 Woe 6).
    pub fn registration(&self, cluster_root: &MasterKey) -> IdentityRegistration {
        let registration = IdentityRegistration::new(
            self.identity(),
            self.public_key(),
            PublicKeyFingerprint::new(format!("{}-fingerprint", self.machine.principal_name())),
            KeyPurpose::HostPublication,
            None,
        );
        let admission = SignatureEnvelope {
            scheme: SignatureScheme::Bls12_381MinPk,
            public_key: cluster_root.public_key(),
            signature: cluster_root.sign(
                RegistrationStatement::from_registration(&registration)
                    .to_signing_bytes()
                    .as_slice(),
            ),
        };
        IdentityRegistration::new(
            self.identity(),
            self.public_key(),
            PublicKeyFingerprint::new(format!("{}-fingerprint", self.machine.principal_name())),
            KeyPurpose::HostPublication,
            Some(admission),
        )
    }
}

/// The principal's three-machine self-quorum: A, B, C, each a real
/// `ClusterMember`. Owns the contract-shaping and evidence-assembly verbs.
pub struct ClusterQuorum {
    member_a: ClusterMember,
    member_b: ClusterMember,
    member_c: ClusterMember,
}

impl ClusterQuorum {
    /// Mint three real members — the principal's co-located nodes.
    pub fn generate() -> Self {
        Self {
            member_a: ClusterMember::generate(Machine::A),
            member_b: ClusterMember::generate(Machine::B),
            member_c: ClusterMember::generate(Machine::C),
        }
    }

    pub fn member(&self, machine: Machine) -> &ClusterMember {
        match machine {
            Machine::A => &self.member_a,
            Machine::B => &self.member_b,
            Machine::C => &self.member_c,
        }
    }

    pub fn members(&self) -> [&ClusterMember; 3] {
        [&self.member_a, &self.member_b, &self.member_c]
    }

    /// The 2-of-3 ROOT CONTRACT `(z9d6` content-addressed composable
    /// authorization contract): a `Threshold` requiring two distinct member
    /// signatures across the three machines. Admission runs the real
    /// `is_valid_majority` guard (k>n/2: 2 > 3/2 passes).
    pub fn root_contract(&self) -> Contract {
        Contract::new(Rule::Threshold(Threshold::new(
            RequiredSignatureThreshold::new(2),
            self.members()
                .iter()
                .map(|member| PolicyMember::KeyMember(member.identity()))
                .collect(),
        )))
    }

    /// A deliberately-sub-majority 2-of-5 threshold: this quorum's three members
    /// plus two synthetic phantom members. 2 is NOT > 5/2 = 2, so admission MUST
    /// reject it — the load-bearing admission negative that proves
    /// `is_valid_majority` is the real guard, not a rubber stamp.
    pub fn sub_majority_contract(&self) -> Contract {
        let mut members: Vec<PolicyMember> = self
            .members()
            .iter()
            .map(|member| PolicyMember::KeyMember(member.identity()))
            .collect();
        members.push(PolicyMember::KeyMember(Identity::host(
            "phantom-d".to_owned(),
        )));
        members.push(PolicyMember::KeyMember(Identity::host(
            "phantom-e".to_owned(),
        )));
        Contract::new(Rule::Threshold(Threshold::new(
            RequiredSignatureThreshold::new(2),
            members,
        )))
    }

    /// Build a 2-of-3 attested moment: two of the three members sign the
    /// `AttestedMomentProposition` (the time quorum). The window is the a-priori
    /// window the operation signatures are later bound to.
    pub fn attested_moment(&self, opens_at: u64, closes_at: u64) -> AttestedMoment {
        let proposition = AttestedMomentProposition::new(
            TimeWindow {
                opens_at: TimestampNanos::new(opens_at),
                closes_at: TimestampNanos::new(closes_at),
            },
            RequiredSignatureThreshold::new(2),
            self.members()
                .iter()
                .map(|member| member.identity())
                .collect(),
        );
        AttestedMoment::new(
            proposition.clone(),
            vec![
                self.member_a.sign_moment(&proposition),
                self.member_b.sign_moment(&proposition),
            ],
        )
    }

    /// 2-of-3 operation evidence: members A and B each sign the
    /// `OperationStatement` for the head digest under the attested moment. The
    /// distinct-signer `Threshold::decide` tally counts these toward the
    /// operation quorum. The head A authorizes is a Spirit Operation.
    pub fn evidence_with_quorum(
        &self,
        operation: &OperationDigest,
        stamp: &AttestedMoment,
    ) -> Evidence {
        Evidence::new(
            ComponentKind::Spirit,
            operation.clone(),
            stamp.clone(),
            vec![
                self.member_a.sign_operation(operation, stamp),
                self.member_b.sign_operation(operation, stamp),
            ],
            Vec::new(),
        )
    }

    /// 1-of-3 operation evidence: only member A signs — a sub-quorum the real
    /// tally MUST reject with `QuorumShort`. The load-bearing evaluation
    /// negative that makes "2-of-3" falsifiable.
    pub fn evidence_below_quorum(
        &self,
        operation: &OperationDigest,
        stamp: &AttestedMoment,
    ) -> Evidence {
        Evidence::new(
            ComponentKind::Spirit,
            operation.clone(),
            stamp.clone(),
            vec![self.member_a.sign_operation(operation, stamp)],
            Vec::new(),
        )
    }
}

/// The principal's single criome holding all three machine keys under the
/// 2-of-3 root contract (`9s52` per-Unix-user criome; `p3td` self-quorum, no
/// cross-criome peer transport on main, 684 Woe 7). Wraps the real `CriomeRoot`
/// actor and owns the authorize-head verb (Path B: the request handler the
/// psyche named — "spirit asks its criome to authorize").
pub struct ClusterCriome {
    root: ActorRef<CriomeRoot>,
}

impl ClusterCriome {
    /// Start the real `CriomeRoot` with the cluster-root trust anchor set, mint
    /// + register each machine's admission through the real `ermr` gate, then
    /// admit the 2-of-3 root contract (admission runs the real majority guard).
    /// Returns the running criome and the admitted root-contract digest.
    pub async fn admit_cluster(
        store: criome::StoreLocation,
        cluster_root: &MasterKey,
        quorum: &ClusterQuorum,
    ) -> (Self, ContractDigest) {
        let root = CriomeRoot::start(Arguments {
            store,
            cluster_root: Some(cluster_root.public_key()),
        })
        .await
        .expect("start criome root with cluster trust anchor");
        let criome = Self { root };
        for member in quorum.members() {
            criome
                .submit(CriomeRequest::RegisterIdentity(
                    member.registration(cluster_root),
                ))
                .await;
        }
        let admitted = criome
            .submit(CriomeRequest::AdmitContract(quorum.root_contract()))
            .await;
        let CriomeReply::ContractAdmitted(admitted) = admitted else {
            panic!("expected ContractAdmitted, got {admitted:?}");
        };
        (criome, admitted.into_payload())
    }

    /// Submit one request to the criome root and unwrap the reply.
    pub async fn submit(&self, request: CriomeRequest) -> CriomeReply {
        self.root
            .ask(SubmitRequest::new(request))
            .await
            .expect("criome root accepts the request")
            .into_reply()
    }

    /// Authorize a new head under the root contract: evaluate the 2-of-3
    /// evidence; on `Authorized`, the criome emits an `AuthorizedObjectUpdate`
    /// pulse carrying the typed `AuthorizedObjectReference`. Returns the
    /// reference for the router to fan.
    pub async fn authorize_head(
        &self,
        contract: ContractDigest,
        evidence: Evidence,
    ) -> AuthorizedObjectReference {
        let evaluated = self
            .submit(CriomeRequest::EvaluateAuthorization(AuthorizationEvaluation {
                contract,
                evidence,
            }))
            .await;
        let CriomeReply::AuthorizationEvaluated(evaluated) = evaluated else {
            panic!("expected AuthorizationEvaluated, got {evaluated:?}");
        };
        assert_eq!(
            evaluated.decision,
            EvaluationDecision::Authorized,
            "the 2-of-3 quorum authorizes the head"
        );
        // The authorized head is the pulse the criome published to its local
        // subscription registry; read it back by component-type.
        let mut updates = self
            .observe(AuthorizedObjectInterest::Component(ComponentKind::Spirit))
            .await;
        assert_eq!(updates.len(), 1, "exactly one authorized head was pulsed");
        updates.remove(0).object
    }

    /// Observe the criome's authorized-object pulses by type-interest — the
    /// production emission path (`ObserveAuthorizedObjects` → snapshot).
    pub async fn observe(
        &self,
        interest: AuthorizedObjectInterest,
    ) -> Vec<signal_criome::AuthorizedObjectUpdate> {
        let observer = Identity::agent("cluster-observer".to_owned());
        let snapshot = self
            .submit(CriomeRequest::ObserveAuthorizedObjects(
                AuthorizedObjectObservation {
                    subscriber: observer,
                    interest,
                },
            ))
            .await;
        let CriomeReply::AuthorizedObjectUpdateSnapshot(snapshot) = snapshot else {
            panic!("expected AuthorizedObjectUpdateSnapshot, got {snapshot:?}");
        };
        snapshot.into_updates()
    }
}

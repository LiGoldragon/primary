I have the complete verbatim test code for the orchestrate repo. The input provided the test code for the other eight repos in full. Now I'll assemble the report section.

# Most complex tested scenario per component

### mentci-lib (/git/github.com/LiGoldragon/mentci-lib)

The full client-side MVU round trip: observe a socket, fold two daemon-pushed pending questions into the approval cursor, answer one, and verify both that the right `signal-mentci` request leaves the model and that the local pending/answered queues stay coherent — the only test driving observe -> fold -> answer -> emit + queue mutation end to end.

```rust
    let mut model = ObservationModel::new(SubscriberName::new("test-client"));
    let _ = model.on_user_event(UserEvent::Observe {
        socket: ComponentSocketKind::Mentci,
        interest: InterfaceInterest::FullInterfaceState,
    });
    model.on_engine_event(EngineEvent::ObservationOpened {
        socket: ComponentSocketKind::Mentci,
        opened: InterfaceObservationOpened {
            token: SubscriptionToken::new("subscription-1"),
            state: projected_with(vec![question("question-1"), question("question-2")]),
        },
    });

    let verdict = ApprovalVerdict {
        question: QuestionIdentifier::new("question-1"),
        decision: ApprovalDecision::ApproveSuggestedAnswer,
        answered_by: SubscriberName::new("test-client"),
    };
    let commands = model.on_user_event(UserEvent::AnswerQuestion { verdict });
    assert_eq!(commands.len(), 1);
    assert!(matches!(
        &commands[0],
        Cmd::SendRequest {
            request: signal_mentci::Input::AnswerQuestion(_),
            ..
        }
    ));
    assert_eq!(model.approval().pending().len(), 1);
    assert_eq!(model.approval().answered().len(), 1);
```

Biggest coverage gap: the criome-escalation seam is wholly untested — no test produces a `Cmd::SubmitCriomeVerdict`, and `AnswerQuestion` unconditionally targets `ComponentSocketKind::Mentci`, so a `CriomeEscalation`-sourced answer never routes to criome's meta socket (an untested and likely incomplete seam).

### signal-mentci (/git/github.com/LiGoldragon/signal-mentci)

Both projection variants of the new `InterfaceObservationOpened` payload survive a full NOTA encode/decode round-trip: the `StatusProjection` that deliberately hides question context, and the `FullProjection` carrying the entire `InterfaceState` (notification, panes, and a nested `ApprovalQuestion` with proposal, suggested answer, and context) — the only test exercising the deeply-nested full-state shape end to end through the codec.

```rust
#[test]
fn projected_state_can_hide_full_question_context() {
    let status_projection = ProjectedInterfaceState {
        revision: RevisionCounter::new(4),
        projection: InterfaceProjection::StatusProjection(StatusText::new("waiting")),
    };
    assert_nota_round_trips(&status_projection);

    let full_projection = ProjectedInterfaceState {
        revision: RevisionCounter::new(5),
        projection: InterfaceProjection::FullProjection(InterfaceState::new(
            RevisionCounter::new(5),
            StatusText::new("waiting"),
            Some(NotificationText::new("new-question")),
            vec![PaneContent {
                pane: PaneLabel::new("approval"),
                body: ContextBody::new("question-context"),
            }],
            vec![approval_question()],
        )),
    };
    assert_nota_round_trips(&full_projection);
}
```

Biggest coverage gap: the new reader accessors — the actual delta in focus — are never called against their returned content, so `ProjectedInterfaceState::pending_questions()` dispatch across all four `InterfaceProjection` arms (including the `&[]` fallback) is unverified; a reader returning the wrong field or an empty slice would still pass.

### meta-signal-mentci (/git/github.com/LiGoldragon/meta-signal-mentci)

A fully-populated multi-socket `MentciDaemonConfiguration` survives both wire encodings — the binary length-prefixed signal-frame request round-trip and the NOTA text codec — exercising the contract's deepest nesting (`Vec<ComponentSocket>` with two lane kinds, `PersonaIdentity`, and a `Vec<NotificationClient>`) through the real exchange-frame envelope.

```rust
#[test]
fn configure_request_round_trips() {
    let request = Input::Configure(configuration());
    assert_request_round_trips(request.clone());
    assert_nota_round_trips(&request);
}
```

Biggest coverage gap: the typed-socket lookup — the contract's whole point — is barely tested: only one successful `component_socket(kind)` hit is asserted, with no `None`-for-absent-kind case and no first-match-on-duplicate-kind case, despite duplicate kinds being structurally permitted (a plain `Vec` with no uniqueness invariant). The virgin/empty-config and all failure-frame paths are likewise untested.

### mentci (/git/github.com/LiGoldragon/mentci)

End to end across two real daemons (a live `CriomeDaemon` and a live mentci `Daemon`, each on its own working + meta Unix socket): criome in `ClientApproval` mode parks an authorization, the mentci bridge lists it by slot, the mentci daemon presents and accepts a closed approve verdict, the bridge submits that approval to criome's meta socket, and criome's working socket then exposes the head as `Authorized` — the only test exercising both daemons and both sockets in one flow, proving approval is delivered by slot rather than by resubmitted evaluation.

```rust
fn mentci_closed_verdict_approves_criome_escalation_over_meta_socket() {
    let workspace = fixture_path("approved");
    let criome_socket = workspace.join("criome.sock");
    let criome_meta_socket = workspace.join("criome-meta.sock");
    let mentci_socket = workspace.join("mentci.sock");
    let store = StoreLocation::new(workspace.join("criome.sema"));
    let criome = CriomeDaemon::new(&criome_socket, store.clone())
        .with_meta_socket(&criome_meta_socket)
        .bind()
        .expect("bind criome");
    let mentci =
        Daemon::from_configuration(mentci_configuration(&mentci_socket, &criome_meta_socket))
            .expect("mentci daemon")
            .bind()
            .expect("bind mentci");
    wait_for_socket(&criome_socket);
    wait_for_socket(&criome_meta_socket);
    wait_for_socket(&mentci_socket);

    let bridge = CriomeApprovalBridge::new(&criome_meta_socket);
    let configured = thread::scope(|scope| {
        let server = scope.spawn(|| {
            criome
                .serve_next_meta()
                .expect("serve client approval mode")
        });
        let configuration = CriomeDaemonConfiguration::new(
            criome_socket.display().to_string(),
            store.as_path().display().to_string(),
        )
        .with_meta_socket_path(criome_meta_socket.display().to_string())
        .with_authorization_mode(AuthorizationMode::ClientApproval);
        let reply = bridge.configure(configuration).expect("configure criome");
        assert_eq!(server.join().expect("join meta configure server"), reply);
        reply
    });
    let meta_signal_criome::Output::Configured(configured) = configured else {
        panic!("expected Configured, got {configured:?}");
    };
    assert_eq!(configured.payload().value(), 1);

    let evidence = unproven_evidence(b"mentci-bridged-head");
    let object = signal_criome::AuthorizedObjectReference {
        component: ComponentKind::Spirit,
        digest: evidence.operation.object_digest().clone(),
        kind: AuthorizedObjectKind::Head,
    };
    let contract = signal_criome::ContractDigest::from_bytes(b"mentci-bridged-contract");
    let evaluation = AuthorizationEvaluation {
        contract: contract.clone(),
        object: object.clone(),
        evidence: evidence.clone(),
    };

    let pending = thread::scope(|scope| {
        let server = scope.spawn(|| criome.serve_next().expect("serve client approval park"));
        let reply = CriomeClient::new(&criome_socket)
            .send(CriomeRequest::EvaluateAuthorization(evaluation.clone()))
            .expect("evaluate authorization");
        assert_eq!(server.join().expect("join park server"), reply);
        reply
    });
    let CriomeReply::AuthorizationPending(pending) = pending else {
        panic!("expected AuthorizationPending, got {pending:?}");
    };
    println!("PROOF (a) criome ordinary socket parked the head for client approval");

    let parked = thread::scope(|scope| {
        let server = scope.spawn(|| criome.serve_next_meta().expect("serve parked list"));
        let snapshot = bridge.parked_authorizations().expect("list parked");
        let reply = server.join().expect("join parked list server");
        assert!(matches!(
            reply,
            meta_signal_criome::Output::ParkedAuthorizationSnapshot(_)
        ));
        snapshot
    });
    assert_eq!(parked.parked().len(), 1);
    assert_eq!(parked.parked()[0].request_slot, pending.request_slot);
    println!("PROOF (b) mentci bridge listed the parked criome request by slot");

    let question = thread::scope(|scope| {
        let server = scope.spawn(|| mentci.serve_next().expect("serve question"));
        let reply = send_mentci(
            &mentci_socket,
            MentciRequest::PresentQuestion(question_proposal()),
        );
        server.join().expect("join question server");
        reply
    });
    let MentciReply::QuestionPresented(presented) = question else {
        panic!("expected QuestionPresented, got {question:?}");
    };
    println!(
        "PROOF (c) mentci daemon presented question {:?}",
        presented.question
    );
    let verdict = ApprovalVerdict {
        question: presented.question,
        decision: ApprovalDecision::ApproveSuggestedAnswer,
        answered_by: SubscriberName::new("psyche"),
    };
    thread::scope(|scope| {
        let server = scope.spawn(|| mentci.serve_next().expect("serve verdict"));
        let reply = send_mentci(
            &mentci_socket,
            MentciRequest::AnswerQuestion(verdict.clone()),
        );
        server.join().expect("join verdict server");
        assert!(matches!(reply, MentciReply::VerdictAccepted(_)));
        println!("PROOF (d) mentci daemon accepted closed approve verdict");
    });

    let approved = thread::scope(|scope| {
        let server = scope.spawn(|| criome.serve_next_meta().expect("serve meta approval"));
        let reply = bridge
            .submit_verdict(pending.request_slot.clone(), &verdict)
            .expect("submit criome approval");
        assert_eq!(server.join().expect("join meta server"), reply);
        reply
    });
    let meta_signal_criome::Output::AuthorizationApprovalRecorded(approved) = approved else {
        panic!("expected AuthorizationApprovalRecorded, got {approved:?}");
    };
    assert_eq!(approved.request_slot, pending.request_slot);
    assert_eq!(
        approved.decision,
        meta_signal_criome::AuthorizationApprovalDecision::Approve
    );
    println!("PROOF (e) mentci bridge submitted approval to criome meta socket by slot");

    let snapshot = thread::scope(|scope| {
        let server = scope.spawn(|| criome.serve_next().expect("serve authorized observation"));
        let reply = CriomeClient::new(&criome_socket)
            .send(CriomeRequest::ObserveAuthorizedObjects(
                AuthorizedObjectObservation {
                    subscriber: Identity::agent("mentci-status".to_string()),
                    interest: AuthorizedObjectInterest::Component(ComponentKind::Spirit),
                },
            ))
            .expect("observe authorized objects");
        assert_eq!(server.join().expect("join observation server"), reply);
        reply
    });
    let CriomeReply::AuthorizedObjectUpdateSnapshot(snapshot) = snapshot else {
        panic!("expected AuthorizedObjectUpdateSnapshot, got {snapshot:?}");
    };
    let updates = snapshot.into_updates();
    assert_eq!(updates.len(), 1);
    assert_eq!(updates[0].object, object);
    assert_eq!(updates[0].decision, EvaluationDecision::Authorized);
    println!("PROOF (f) criome ordinary socket exposes the authorized head pulse");

    mentci.shutdown().expect("shutdown mentci");
    criome.shutdown().expect("shutdown criome");
}
```

Biggest coverage gap: only the `ApproveSuggestedAnswer` arm runs end to end; the `Reject->Reject` and `Defer->Defer` verdict projections through `CriomeVerdict`/`submit_verdict` are never driven at the daemon level (covered only inside mentci-lib's own crate), and the `criome_request_slots` dedup guard against minting duplicate questions on a repeat observe is unverified.

### mentci-egui (/git/github.com/LiGoldragon/mentci-egui)

End-to-end proof that the egui shell's `DaemonClient` configures, binds, and serves a real in-process Mentci daemon over a tempdir Unix socket, sends an `ObserveInterfaceState` frame, and decodes the reply — asserting the round-trip renders both request and reply as NOTA carrying the expected operation/reply identifiers. The only test, and the most end-to-end one, exercising the full daemon-construction + socket + frame + NOTA path.

```rust
#[test]
fn daemon_client_observes_live_mentci_daemon_as_nota() {
    let directory = tempfile::tempdir().expect("tempdir");
    let mentci_socket = directory.path().join("mentci.socket");
    let criome_socket = directory.path().join("criome.socket");
    let configuration = DaemonConfiguration::new(MentciDaemonConfiguration::new(
        vec![
            ComponentSocket::new(
                ComponentSocketKind::Mentci,
                StandardSocket::unix(mentci_socket.display().to_string()),
            ),
            ComponentSocket::new(
                ComponentSocketKind::MetaCriome,
                StandardSocket::unix(criome_socket.display().to_string()),
            ),
        ],
        PersonaIdentity::new(
            PersonaName::new("psyche"),
            ComponentKind::Persona,
            PersonaKeyLabel::new("home-verdict"),
        ),
        vec![NotificationClient::StatusBar],
    ));
    let daemon = Daemon::from_configuration(configuration)
        .expect("daemon")
        .bind()
        .expect("bind daemon");
    let server = std::thread::spawn(move || daemon.serve_next().expect("serve one request"));

    let entry = DaemonClient::new(&mentci_socket)
        .observe_interface_state()
        .expect("observe interface state");

    server.join().expect("join server");
    assert_eq!(entry.socket_kind, SocketKind::Mentci);
    assert_eq!(entry.operation, "ObserveInterfaceState");
    assert!(entry.request_nota.contains("ObserveInterfaceState"));
    assert!(entry.reply_nota.contains("InterfaceObservationOpened"));
}
```

Biggest coverage gap: everything answer-related is untested because it does not exist in this crate — the app emits only `UserEvent::Observe` (no `AnswerQuestion`/`ProposeEditedAnswer`/`SelectQuestion`/`PushQuestion`, no approval card, no `EscalateToPsyche`). The one test also calls the legacy string-NOTA `observe_interface_state()`, not the new typed `observe_interface_state_typed()` the model consumes, so the typed-reply -> `EngineEvent::ObservationOpened` -> `model.view()` folding path has zero coverage.

### signal-orchestrate (/git/github.com/LiGoldragon/signal-orchestrate)

The deepest-nested payload in the suite — a `RoleSnapshot` of `Vec<RoleStatus>` (each with `HarnessKind` + `Vec<ClaimEntry>` of `ScopeReference`/`ScopeReason`) plus a `Vec<Activity>` of store-stamped timestamps — driven through the full length-prefixed `OrchestrateFrame` reply encode/decode and asserted equal, proving the macro-emitted `Reply` variant and all transitively-nested contract types survive the binary wire round-trip.

```rust
#[test]
fn role_snapshot_round_trips() {
    let reply = OrchestrateReply::RoleSnapshot(RoleSnapshot {
        roles: vec![
            RoleStatus {
                role: designer(),
                harness: HarnessKind::Claude,
                claims: vec![ClaimEntry {
                    scope: sample_path_scope(),
                    reason: sample_reason(),
                }],
            },
            RoleStatus {
                role: operator(),
                harness: HarnessKind::Codex,
                claims: vec![],
            },
        ],
        recent_activity: vec![Activity {
            role: designer(),
            scope: sample_path_scope(),
            reason: sample_reason(),
            stamped_at: TimestampNanos::new(1_730_000_000_000_000_000),
        }],
    });
    let decoded = round_trip_reply(reply.clone());
    assert_eq!(decoded, reply);
}
```

Biggest coverage gap: the entire worktree delta is untested — the suite never imports `Worktree`, `RepositoryName`, `BranchName`, `LaneName`, `PurposeText`, `WorktreeStatus`, `PushedState`, or `WorktreesObserved`. The `OrchestrateReply::WorktreesObserved` arm is the one reply variant with no witness test (violating the file's architectural-truth-tests discipline), and the canonical-vs-generated field-name divergence (`status` vs `worktree_status`) is caught by nothing.

### meta-signal-orchestrate (/git/github.com/LiGoldragon/meta-signal-orchestrate)

Every `MetaOrchestrateReply` variant driven through the full length-prefixed Frame encode/decode pipeline (Frame -> `Reply::committed` -> `NonEmpty`/`SubReply` -> bytes -> decode -> unwrap `Accepted`/`Ok`), proving rkyv+frame round-trip fidelity including the multi-leg `PartialApplied` reply that carries both a success and a failure leg.

```rust
#[test]
fn meta_orchestrate_replies_round_trip() {
    let created = MetaOrchestrateReply::RoleCreated(RoleCreated {
        role: role(),
        harness: HarnessKind::Codex,
        report_repository_path: repository_path(),
        report_lane_path: lane_path(),
    });
    assert_eq!(round_trip_reply(created.clone()), created);

    let retired = MetaOrchestrateReply::RoleRetired(RoleRetired { role: role() });
    assert_eq!(round_trip_reply(retired.clone()), retired);

    let rejected = MetaOrchestrateReply::RoleCreationRejected(RoleCreationRejected {
        role: role(),
        reason: RoleCreationRejectionReason::RoleAlreadyExists,
    });
    assert_eq!(round_trip_reply(rejected.clone()), rejected);

    let refreshed = MetaOrchestrateReply::RepositoryIndexRefreshed(RepositoryIndexRefreshed {
        repositories: 7,
    });
    assert_eq!(round_trip_reply(refreshed.clone()), refreshed);

    let registered = MetaOrchestrateReply::LaneRegistered(LaneRegistered {
        registration: lane_registration(),
    });
    assert_eq!(round_trip_reply(registered.clone()), registered);

    let lane_retired = MetaOrchestrateReply::LaneRetired(LaneRetired { lane: lane() });
    assert_eq!(round_trip_reply(lane_retired.clone()), lane_retired);

    let authority_set = MetaOrchestrateReply::LaneAuthoritySet(LaneAuthoritySet {
        lane: lane(),
        authority: LaneAuthority::Support,
    });
    assert_eq!(round_trip_reply(authority_set.clone()), authority_set);

    let partial = MetaOrchestrateReply::PartialApplied(PartialApplied {
        succeeded: vec![ApplicationSuccess {
            component: DownstreamComponent::Router,
            detail: ScopeReason::from_text("channel 42 installed").expect("success detail"),
        }],
        failed: vec![ApplicationFailure {
            component: DownstreamComponent::Harness,
            reason: ApplicationFailureReason::Unreachable,
            detail: ScopeReason::from_text("codex-7 transcript is gone").expect("failure detail"),
        }],
    });
    assert_eq!(round_trip_reply(partial.clone()), partial);

    let unimplemented = MetaOrchestrateReply::MetaOrchestrateRequestUnimplemented(
        MetaOrchestrateRequestUnimplemented {
            operation: MetaOperationKind::Create,
            reason: MetaOrchestrateUnimplementedReason::NotBuiltYet,
        },
    );
    assert_eq!(round_trip_reply(unimplemented.clone()), unimplemented);
}
```

Biggest coverage gap: despite covering 11 variants, the new worktree delta is essentially untested at runtime — neither the `RegisterWorktree`/`RefreshWorktreeIndexOrder` requests nor the `WorktreeRegistered`/`WorktreeIndexRefreshed` acks are round-tripped, and the hand-rolled `WorktreeIndexRefreshed` NOTA codec (including the `u32::try_from` overflow path and parenthesis-arity check) has zero direct coverage.

### orchestrate (/git/github.com/LiGoldragon/orchestrate)

Drives the full daemon path end to end against a temp store: it stands up a real colocated jj repo, registers a worktree through `handle_meta`, and proves the daemon re-derives `last_activity` and `pushed_state` from jj (overwriting the agent-supplied seed values), then observes the row and asserts the projected `worktrees.nota` is valid positional, quote-free NOTA with the bracketed purpose.

```rust
#[test]
fn register_worktree_observe_and_project_manifest() {
    let mut fixture = WorktreeFixture::new("orchestrate-worktree-smoke");
    let path = fixture.make_worktree_repository("orchestrate", "worktree-registry");
    let wire_path = WirePath::from_absolute_path(path.to_string_lossy().into_owned())
        .expect("absolute worktree path");

    let order = RegisterWorktree {
        worktree: Worktree {
            repository: RepositoryName::from_text("orchestrate").expect("repository name"),
            branch: BranchName::from_text("worktree-registry").expect("branch name"),
            path: wire_path,
            owning_lane: LaneName::from_text("designer").expect("lane name"),
            status: WorktreeStatus::Active,
            purpose: PurposeText::from_text("prototype the worktree registry")
                .expect("purpose text"),
            // Agent-supplied last_activity / pushed_state are re-derived by the
            // daemon, so the seed values here must not survive.
            last_activity: TimestampNanos::new(0),
            pushed_state: PushedState::AncestorOfMain,
        },
    };

    let reply = fixture
        .handle_meta(MetaOrchestrateRequest::RegisterWorktree(order))
        .expect("register worktree");
    let MetaOrchestrateReply::WorktreeRegistered(registered) = reply else {
        panic!("expected WorktreeRegistered, got {reply:?}");
    };
    assert_eq!(registered.worktree.repository.as_str(), "orchestrate");
    assert_eq!(registered.worktree.branch.as_str(), "worktree-registry");
    assert_eq!(registered.worktree.owning_lane.as_str(), "designer");
    // The daemon re-derived last_activity from the worktree commit; the seed
    // zero must have been replaced.
    assert!(registered.worktree.last_activity.value() > 0);
    // A fresh colocated repo with no remote is Unpushed (not AncestorOfMain).
    assert_eq!(registered.worktree.pushed_state, PushedState::Unpushed);

    let observed = fixture
        .handle(OrchestrateRequest::Observe(Observation::Worktrees))
        .expect("observe worktrees");
    let OrchestrateReply::WorktreesObserved(snapshot) = observed else {
        panic!("expected WorktreesObserved, got {observed:?}");
    };
    assert_eq!(snapshot.worktrees.len(), 1);
    assert_eq!(snapshot.worktrees[0].branch.as_str(), "worktree-registry");

    let manifest = fixture
        .workspace
        .join("orchestrate")
        .join("worktrees.nota");
    let body = std::fs::read_to_string(&manifest).expect("worktrees.nota written");
    assert!(
        body.contains("orchestrate") && body.contains("worktree-registry"),
        "manifest body: {body}"
    );
    assert!(body.contains("designer"), "manifest body: {body}");
    // Positional NOTA record: one parenthesised tuple per worktree, fields in
    // declared order, whitespace-bearing strings bracketed, and quote-free.
    assert!(body.starts_with('('), "manifest body: {body}");
    assert!(
        body.contains("[prototype the worktree registry]"),
        "purpose must be bracketed: {body}"
    );
    assert!(body.contains("Active") && body.contains("Unpushed"), "manifest body: {body}");
    assert!(!body.contains('"'), "manifest must be quote-free: {body}");
}
```

Biggest coverage gap: the daemon's jj re-derivation is proven only for the unpushed single-commit case — `PushedState::AncestorOfMain`/`DivergedFromMain` (the states requiring a real remote and main-relative ancestry) are never produced, and only happy-path `handle_meta`/`handle` is driven (no malformed order, missing-component-socket, or store-error path through the live `State` machine).

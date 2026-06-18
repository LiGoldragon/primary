# 689 — designer audit of operator 422 (mentci component landing)

Verdict: **PASS — implementation fidelity complete.** Every claim in
`reports/operator/422-mentci-component-implementation.md` verified true against the
actual repositories. No design drift, no missing pieces, no undocumented gaps.

## What was verified true

- **Commits match** — `signal-standard` `aa672cc8`, `signal-mentci` `97730d56`,
  `meta-signal-mentci` `270cd909`, `mentci` `ac37ee5e`, `mentci-lib` `c5a80852`.
- **Tests + clippy** — 8 / 5 / 3 / 9 tests pass at the stated counts; clippy clean
  except the one pre-existing `handshake.rs` warning.
- **Closed verdict is genuinely closed** — `ApprovalDecision = [ApproveSuggestedAnswer
  Reject Defer]`; `PendingAnswer` and any open `Answer(...)` are absent from code
  (only referenced as DELETED in comments). This is the psyche correction realized.
- **AnswerProposal flow correct** — a separate typed object (`question`, `body`,
  `authored_by`, canonical `ProposalDigest`) that re-enters the normal
  authorization path; the test `edited_approval_answer_is_submitted_as_a_new_proposal`
  proves an edit keeps the question pending (does not collapse into the verdict).
  This is exactly "editing creates a new typed proposal," not a free-form answer.
- **Daemon-minted ids/tokens** — `PresentQuestion` carries no id (daemon mints
  `QuestionIdentifier`), `ObserveInterfaceState` carries no token (daemon mints
  `SubscriptionToken`); minted ids returned in the replies. (operator 421 §2/§3.)
- **Filtered subscriptions** — `InterfaceInterest [FullInterfaceState StatusOnly
  Notifications PendingQuestions]` with `ProjectedInterfaceState` carrying only the
  declared slice; notification clients do not get full state. (operator 421 §4.)
- **All four schemas lower** on current schema-next; SEMA declares the five
  families (`PendingQuestions`, `Decisions`, `AnswerProposals`, `Subscriptions`,
  `Revision`).
- **Woe 4 confirmed done** — `signal-criome` `ca3624c` "port to strict schema
  contracts" (dot-field grammar, pins schema-next `1de72dd`), `criome` `068f9db`
  ported and compiling cleanly. The blocker designer had carried forward no longer
  exists.

## The two operator flags — both legitimate

1. **Daemon binary correctly not faked.** The `mentci` repo is a schema skeleton
   with no `Cargo.toml`; the binary cannot land without the four contracts on real
   remotes, because the no-local-path rule would otherwise force duplicated PoC
   transport code. Stopping at that boundary is correct.
2. **Remote-name collision is a valid pre-push gate.** The local checkout is
   correctly configured (`remote.origin.url = ssh://git@github.com/LiGoldragon/mentci`);
   the caveat is about *upstream GitHub* resolution — `LiGoldragon/mentci` currently
   resolving to a repo named `workspace`. So the GitHub namespace must be confirmed
   before pushing the mentci daemon repo. **This is a psyche decision** (the
   repo-namespace call).

## The one open item

The mentci component is built, green, and design-faithful on local main. The only
gate to a *running* daemon is now operational: confirm the GitHub remote for the
`mentci` daemon repo (the `LiGoldragon/mentci` → `workspace` collision), push the
four contracts to remotes, build the daemon over them, and `q1le` for real verdict
signing. None of it is a design question.

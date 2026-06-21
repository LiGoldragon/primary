# Operator 451 - follow-up testing after designer 708

## Context

The user asked for follow-up work and testing while waiting on designer feedback.
I treated designer report 708 as the active audit queue and only took
operator-owned slices that did not require deciding the Mentci criome-slot seam.

The user's question about mentci-lib was resolved during the work: mentci-lib was
abandoned/stale before the designer's 707 re-found pass, but it is no longer
abandoned on main. It now exists as the intended shared Mentci model leg. The
remaining issue is narrower: the criome verdict path in mentci-lib cannot be
made live until signal-mentci carries the parked criome authorization slot on
the approval question.

## Landed

- `signal-mentci` main `765ee355` - added `tests/interface_readers.rs`, covering
  the public readers added by the designer's re-found pass:
  `InterfaceState::notification`, `InterfaceState::panes`,
  `InterfaceState::pending_questions`, `PendingQuestionsView::questions`,
  `ProjectedInterfaceState::pending_questions`, and
  `QuestionProposal::{suggested_answer, context}`.
- `signal-orchestrate` main `878601cf` - fixed the worktree schema source so the
  generated mirror emits `Worktree { status: WorktreeStatus }`, matching the
  canonical root type. Added a worktree registry reply round-trip and a generated
  mirror compile witness for the canonical `status` field.
- `meta-signal-orchestrate` main `f7102e5b` - removed handwritten NOTA
  encode/decode implementations for `RepositoryIndexRefreshed` and
  `WorktreeIndexRefreshed`. The two count replies now derive NOTA and match the
  schema-generated single-field newtype shape, with explicit semantic readers
  `repositories()` and `worktrees()`.
- `orchestrate` main `5380fc71` - repinned to `signal-orchestrate` `878601cf`
  and `meta-signal-orchestrate` `f7102e5b`, adapted the daemon/schema bridge to
  the generated `Worktree.status` field, and consumed the new meta count reply
  constructors/readers.

## Verification

- `signal-mentci`: `cargo test --all-targets --features nota-text`; `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `signal-orchestrate`: `SIGNAL_ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --all-targets --features nota-text`; `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `meta-signal-orchestrate`: `cargo test --all-targets --features nota-text`; `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `orchestrate`: `cargo test --all-targets --features nota-text`; `cargo clippy --all-targets --features nota-text -- -D warnings`.

## Closed 708 Items

- `signal-mentci` public readers now have direct coverage.
- `signal-orchestrate` worktree generated mirror no longer disagrees with the
  canonical `status` field, and the worktree reply has round-trip coverage.
- `meta-signal-orchestrate` no longer carries handwritten NOTA parsers for the
  index refresh replies, and the test compares canonical NOTA text against the
  generated schema mirror.
- `orchestrate` consumes the updated contracts on main, so the contract fixes
  are load-bearing for the daemon repo rather than isolated contract commits.

## Still Open

- The Mentci keystone remains a design seam, not an operator-only patch:
  `signal-mentci::ApprovalSource::CriomeEscalation` still has no
  `AuthorizationRequestSlot`, so mentci-lib's `CriomeVerdict::from_decision`
  and `Cmd::SubmitCriomeVerdict` cannot yet be produced from a real approval
  question. My recommendation from report 450 still stands: designer should own
  that contract/model shape; operator should integrate and wire the daemon after
  the slot-carrying surface is settled.
- The live orchestrate daemon activation/migration question remains separate:
  source main is updated, but this session did not restart or migrate any live
  schema-2 daemon/store.

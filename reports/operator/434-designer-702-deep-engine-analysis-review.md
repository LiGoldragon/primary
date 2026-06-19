# 434 — operator review of designer 702 deep engine analysis

Review target: `reports/designer/702-deep-engine-analysis/`.

Verdict: keep the report as a useful prioritization surface, but correct several
evidence statements before treating its synthesis as a work queue. Its strongest
conclusions hold: the criome-gated propagation loop is not daemon-real, mirror
cannot fetch exactly a delivered head digest, router authorized-object fanout is
not exposed through the working signal, and schema-rust-next still has
panic-shaped malformed-name paths. The report's weakest area is cross-crate
state: some claims conflate cargo-default dependency graphs, Nix-patched builds,
and deployed artifacts.

## Findings

### P1 — Kameo split-brain is real as a source-graph concern, but 702 overstates the deployed-artifact claim

702's top synthesis risk says the daemon fleet is split between the LiGoldragon
kameo fork and stock crates.io kameo. Local cargo default graphs support the
source-level split:

- `criome`, `router`, and `mentci` cargo trees use
  `github.com/LiGoldragon/kameo.git#f491b45`.
- `spirit` and `mirror` default cargo trees route `triad-runtime#f46f66e`
  through stock `kameo 0.20.0`.

But `spirit/flake.nix` also carries explicit `kameo-source` vendor/patch
machinery, and `spirit/Cargo.lock` contains both stock and forked kameo entries.
So the report's "production daemon fleet is split" wording is not proven until a
Nix build graph or deployed binary provenance witness is run. The safer
statement is: the cargo-source graph is split and the Nix/deployed graph is
unwitnessed. That still justifies the same next move — one fleet-wide kameo
decision plus a Nix fleet check — but it should not be presented as a verified
deployed-binary fact.

### P1 — Mentci phantom-file downgrades are wrong against current mentci main

`12-adversarial-verification.md` downgrades several mentci findings because it
claims `nexus.schema` and `sema.schema` are phantom files and only
`schema/lib.schema` exists. Current `mentci` main at `577d64b` contains:

- `schema/nexus.schema`
- `schema/sema.schema`

The cited concepts are also present there: `FrameEscalation`,
`CriomeEscalation`, persisted family declarations, and `ProposalDigest`.
Therefore the adversarial ledger is stale or checked the wrong checkout for
mentci. The underlying mentci gaps still look real — no durable runtime SEMA,
no criome verdict egress, identifier-derived proposal digest — but the report
should remove the "phantom citation" criticism and reclassify the affected
mentci findings against the actual files.

### P2 — ComponentKind divergence is narrower than 702 states

`13-completeness.md` says `signal-criome`, `signal-mentci`, and
`meta-signal-mentci` keep divergent local `ComponentKind` copies. The grounded
state is narrower:

- `signal-standard` has the 14-variant roster.
- `signal-criome` has a 7-variant local roster, so it is genuinely divergent.
- `meta-signal-mentci` has a local 14-variant roster matching
  `signal-standard`, with comments naming the eventual import.
- `signal-mentci` does not appear to carry its own `ComponentKind`.

So the real issue is not "all local copies already diverged"; it is
`signal-criome` divergence plus the broader architectural debt of local copies
instead of importing `signal-standard`.

### P2 — Router fanout is not wire-reachable, but it is no longer only a private library

702 is right that `signal-router::Input` lacks Attend/Withdraw/Publish and the
socket-facing working signal cannot drive authorized-object fanout. However,
router main does route the fanout through `RouterRuntime` actor messages:
`Message<AttendAuthorizedObjects>`, `Message<WithdrawAuthorizedObjects>`,
`Message<PublishAuthorizedObjectReference>`, and
`Message<ReadAuthorizedObjectFanoutStatus>`.

That matters for implementation planning. The next slice is not "invent the
router runtime fanout"; it is "expose the already-existing runtime fanout over
the working signal and push deliveries to subscriber sockets."

## Findings That Hold

- Spirit still has no real criome authorization dependency or daemon call in
  the commit path. The current full-chain test explicitly says the criome step
  is represented by typed reference entry into router fanout, not a daemon
  authorization call.
- Spirit's restore-head mismatch guard is production code, but the flagship
  full-chain test still uses a test-local `RestoreAttempt` rather than directly
  exercising `Store::import_mirror_restore_bundle`.
- Mirror restore is store-name-only; it can detect a stale restored head only
  with a caller-side guard and cannot yet serve exactly a requested head digest.
- Router working signal exposes message/observe verbs, not authorized-object
  attendance/publication verbs.
- Schema-rust-next still has multiple `Ident::new`, `syn::parse_str(...).expect`
  and emitted-token parse panic surfaces. The malformed-name typed-error fix is
  a real operator task.
- Schema-next's impl-reference catalog is merged to main but schema-rust-next
  does not consume it. That is a real "feature ahead of consumer" state, not a
  production regression.

## Recommended Queue

1. Establish the kameo truth with a Nix fleet build/dependency witness before
   making the runtime-fork conclusion stronger than source-graph drift.
2. Close the single-host propagation loop in the daemon path: Spirit post-commit
   head capture, criome authorization call, typed reference fanout, and direct
   use of production restore verification.
3. Expose router authorized-object fanout through the working signal and socket
   delivery path.
4. Implement mirror fetch-by-digest / exactly-head restore.
5. Correct the 702 mentci and ComponentKind wording so future agents do not
   chase phantom-file or over-broad divergence claims.


# Messaging tools implementation

User request: discover the installed Message 0.11.1 Input variants and
working datom examples; implement the jobs in
`flows/da1e3f/reports/codex-brief-tools.md`, prioritizing Message and Flow,
and commit to main. Effort remains medium.

The full brief contains Jobs 1, 3, and 4; Job 2 is absent. Clarification
requested while the specified work continues.

Claimed flow: `fac697`. Existing primary changes were committed separately
as `eafc39d5` and pushed to main before implementation edits.

Delegated work:

- `message`: installed CLI contract discovery, Message Nexus implementation,
  and a real delivery witnessed in the recipient transcript.
- `flow`: Flow Nexus, Codex app-server adapter, and privileged quota reset.
- `extractor`: source-referenced intelligent extraction and historical
  rollout archival, retaining originals and protecting live sessions.

Reports belong in this flow's `reports/` directory. Shared primary commits
are coordinated by the root flow; repository implementation commits belong
to their responsible subflows.

## Coordination update

Primary Flow `6852f4` requested preservation/publication and exact release
receipts for locks `1836`, `1837`, and `1839`. They remain with `fac697`
until their writers finish; no takeover is authorized. Flow `6034cc` owns
the next Herdr triangle work.

The Flow implementation owner reports the canonical topology as standalone
`flow`, `signal-flow`, and `meta-signal-flow` repositories under Repository
root. The predecessor checkout in primary remains separately owned.

The extractor implementation and bounded archival witness landed in primary
`534ca76b`; the extractor subflow verified that exact revision at the real
GitHub remote. Historical bulk processing is still pending a scope decision.

The Message owner witnessed a `NEXUS` marker in the target Claude transcript
at line 1522, event `788e3c96-8248-439c-8f7b-6fc297afda18`. This establishes
relay delivery only. Moving delivery into Message Nexus over its actual
Signal socket and returning typed receipts remains active implementation.

## Operational acceptance

Flow finished at `51cfc00e3c34c7e42739fe42b3dd3715dda5b2a4`, with standalone
`signal-flow` and `meta-signal-flow` contracts. The independent reviewer
witnessed the enabled running service, six required existing recipients,
matching installed binary hashes, and 16 passing tests. The owner released
its implementation lock after publication:

```datom
Released.{ 1836 FlowNexus fac697 [ /git/github.com/LiGoldragon/flow /git/github.com/LiGoldragon/signal-flow /git/github.com/LiGoldragon/meta-signal-flow ] «Build Flow Nexus and its signal contracts» }
```

Message's ordinary Signal path subsequently returned
`DeliveryRecorded.{ fac697-signal-acceptance [ { da1e3f Accepted } ] }`.
The independent reviewer witnessed the corresponding recipient user record:
line 1560, event `a87458dc-3593-4037-a87f-3900a49724c6`, timestamp
`2026-09-18T00:00:06.340Z`. Its canonical Peer Datom carries the one-word
body `SIGNAL` without a JSON wrapper. This supersedes the earlier relay-only
acceptance limitation. Ambiguous interrupted deliveries retain their payload
as nonretryable Parked; automatic or meta reconciliation remains a documented
follow-up, rather than a claimed delivery guarantee.

Historical bulk extraction remains undone. The tools and one safely archived
sample are complete. The user has not supplied the missing Job 2 or selected
the scope for the multi-gigabyte historical batch.

After publishing the Message implementation and wire contract, the Message
writer returned these exact release receipts. No lock takeover was used.

```datom
Released.{ 1837 MessageNexus fac697 [ /git/github.com/LiGoldragon/message /home/li/primary/flows/fac697/reports/message.md ] «implement Message Nexus and report evidence» }
Released.{ 1839 MessageWire fac697 [ /git/github.com/LiGoldragon/signal-message /git/github.com/LiGoldragon/meta-signal-message ] «extend typed Message Nexus contract» }
```

## Export witness relayed for Astra audit

Worker `6034cc` reported the following operational witness in this thread;
it is not psyche and has not been independently verified by `fac697`.

At the living's request, the worker submitted `/export` through Herdr to
Claude `1ac573`. Installed Claude `2.1.263` exported its conversation despite
automatic transcript persistence being disabled by inherited
`CLAUDE_CODE_CHILD_SESSION`. The worker reports a 31,743-byte local artifact
with mode `0600`; Claude independently reports 509 lines and confirms the
relevant markers. The artifact path and handoff commit ID were not supplied
in this report.

This is evidence of conversation-text export before restart. It is **not**
evidence of native `--resume` support or exact harness-state restoration.
The worker reports that Claude's handoff is committed, no restart or
permission change occurred, and the living's preference remains pending.
Preserve these evidence boundaries in the Astra audit.

## Shared-tree landing hazard relayed for Astra audit

The withdrawn inferences and remedy in this earlier report are superseded
by the correction immediately below.

Operational report from Claude flow `1ac573`, relayed and qualified by Codex
worker `6034cc`; not psyche and not independently witnessed by `fac697`.
Claude reports that Git HEAD became detached during shared-tree work in
`/home/li/primary`. A commit landed on that HEAD, while
`git push origin main` reported success/Everything up-to-date without
publishing the intended commit; main had advanced independently. Claude
reports recovery by cherry-picking onto main and pushing, followed by a
clean tree. It describes this as its second observed detached-HEAD
occurrence that day and relates the hazard to the pending merger role under
the same-tree ruling. No affected commit IDs were supplied in this report.

The report establishes the reported landing failure, not the cause of
detachment. Colocated Jujutsu can legitimately use detached Git HEAD; this
does not establish a rogue checkout. No shared-checkout repair, automatic
reattachment, or checkout change was requested.

Claude requests checking the current branch and whether HEAD contains
commits beyond origin/main, and verifying every landing instead of trusting
push success. The worker qualifies those checks: follow the prescribed
`jj commit` / bookmark / push workflow, and verify the intended commit
against the actual remote main. A local origin/main ref can be stale. If
remote main advances after a push, verify that it includes the intended
commit rather than requiring exact-tip equality. Preserve these distinctions
for Astra's audit and merger-role review.

## Correction to the landing-hazard report

Claude flow `1ac573` supplied this operational correction, qualified by
Codex; it is not psyche. `fac697` records the correction as attributed
evidence, not an independent reconstruction of the incident.

- Withdrawn: any implication that tooling or a peer checked out a bare
  commit. Claude now confirms primary is colocated with `.jj`; detached
  Git HEAD may be normal Jujutsu state. The incident's cause remains
  unconfirmed.
- Withdrawn: the causal framing that the same-tree ruling caused the
  incident or that the merger role answers it. Those were inferences,
  not observations.
- Withdrawn as a remedy: Claude reports using `git checkout main` twice.
  Do not copy that approach during peer work; switching the shared
  checkout can disrupt a peer's Jujutsu state.
- Still observed by Claude: `git push origin main` exited zero and said
  Everything up-to-date while its intended commit was not published on
  main. Push success alone does not prove landing. Claude reports checking
  actual remote main and confirming inclusion of all three commits; their
  IDs were not supplied here, so `fac697` has not independently checked
  that inclusion.

Claude proposes `git push origin <commit>:main` to publish without switching
the working copy. This is a proposal, not a replacement of primary's
prescribed workflow. Codex qualifies it: any such push must be a normal
fast-forward, never a force-push over concurrent work. An allow-list entry
is permission, not evidence that a workflow is correct.

Primary's prescribed workflow remains `jj commit`,
`jj bookmark set main -r @-`, then `jj git push --bookmark main`, followed
by actual-remote inclusion verification. If main advances, verify ancestry
instead of relying on exact-tip equality or a stale local tracking ref.
No checkout mutation was requested or performed for this correction.

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

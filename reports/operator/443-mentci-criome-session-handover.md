# 443 — Session handover: mentci↔criome working approval UI

*Operator-lane handover. Captures the full context of the session that produced
the wide gap scan (report 442), the intent decisions landed, the key-custody
ruling integration, the build plan, and the open next steps. A fresh operator
or designer should be able to pick up from here without re-deriving.*

## The goal (psyche intent)

A **working mentci approval UI**: a `mentci` CLI, connected to `mentci-daemon`,
which interacts with a **running** `criome` daemon. criome runs in **client
approval mode** — a submission to criome is **parked** for mentci to approve —
and the loop must actually run over two live Unix sockets, not only as a
single-process integration test. Lenses requested: design gaps, ugly code,
unported work.

This sits on top of the previous operator's 440/441 slices (criome
`AuthorizationMode [Quorum AutoApprove]`, the meta-socket `Configure` +
`SubmitAuthorizationApproval`, and `CriomeApprovalBridge`).

## What was delivered

**The wide scan — `reports/operator/442-mentci-criome-working-ui-gap-scan/`**
(on primary main). A background fan-out workflow (run `wf_fbf49ee9-bb8`): 8
dimension-readers across the two component triads, every finding adversarially
re-verified against the actual code, then synthesized. 54 agents, ~2.06M
tokens, **45 raw findings → 38 confirmed**. Read `9-synthesis.md` first; the
build sequence is there.

### The headline conclusion

Two things are the whole job, and both are **absent** (not buggy):

1. **The parked, addressable `AuthorizationEvaluation` does not exist.** criome
   forgets the evaluation the instant it escalates (`criome/src/actors/root.rs:336`
   only persists on `Authorized`); the signal-mentci question type has no field
   for it; mentci state has no slot for it; and the meta-approval contract makes
   the answerer re-supply the *entire* evaluation by value
   (`meta-signal-criome/schema/lib.schema:46-49`). The cross-daemon loop runs
   today in exactly **one `#[test]`** (`mentci/tests/criome_bridge.rs:316-371`)
   that hand-carries the evaluation as a shared Rust variable; the mentci
   question presented in between is a hardcoded fixture with no link to the
   escalation. Erase that variable and the loop has no spine.
2. **The `mentci` CLI is not a UI.** One-shot `connect → write one frame → read
   one binary reply → exit` (`mentci/src/client.rs:49-58`); its single argument
   must be a complete hand-authored NOTA `MentciRequest`, output is raw binary
   dumped to stdout. No `list`, no `watch`, no `approve <id>`. A human cannot
   even see what is parked.

**The encouraging part:** mentci's own `nexus.schema` already *names* the entire
intended bridge (`FrameEscalation`, `RouteVerdict`, `InterfaceFanOut`) — design
drawn, none built. And criome **already has** a working park-and-answer-by-id
mechanism, wired to the wrong flow: the BLS signing path
(`AuthorizeSignalCall → AuthorizationPending{request_slot} → ObserveAuthorization`,
`criome/src/actors/authorization.rs:104-158`). The cheapest correct path folds
contract escalations into that existing slot machinery rather than building a
parallel model.

The five confirmed blockers, per `9-synthesis.md`: (1) criome never parks an
escalation; (2) nothing maps a criome escalation into a mentci question or
carries the evaluation back; (3) the mentci CLI is not a UI; (4) criome has no
client-approval/park mode and no discovery surface for parked submissions; (5)
meta-approval is content-replay, not answer-by-id.

## Decisions captured this session

The psyche resolved the two biggest design forks (via the operator's structured
questions) and one prior contradiction (via the designer's thread). All landed
in the intent layer.

### Intent layer (Spirit)

- **`t00s` (Decision, clarified this session) — the canonical client-approval
  record.** Now reads: [criome's authorization verdict can be supplied by a
  connected approver ... Client approval mode is a daemon-wide AuthorizationMode
  variant alongside Quorum and AutoApprove: criome parks every incoming
  submission for human approval ... criome owns the pending-approval queue —
  each parked AuthorizationEvaluation lives in criome's own store keyed by a
  ParkedAuthorizationId, mentci ... casts the approve-or-deny verdict by that
  identifier rather than re-supplying the full evaluation by value]. The psyche
  directed this be an **edit of t00s**, not a new record.
- **`3ss0` — retired this session** as a duplicate of `t00s` (it carried the
  verbatim text of a rejected new-Record draft for the same arrow; the psyche's
  "edit that record" directive makes a parallel new record forbidden).
- **Key custody ruling (designer↔psyche thread, forwarded to operator):
  "criome owns the keys; it decides."** This resolves a contradiction between
  `criome/ARCHITECTURE.md:403-406` (verifier-only: requester holds the key) and
  `mentci/INTENT.md:30-31` (criome owns key custody). The model is already in
  Spirit — `q1le` (Decision): [the criome daemon holds an encrypted key store ...
  a managed multi-key store] and `7x5z` ([criome owns the key store]). The
  ruling confirms these. **The designer owns capturing the explicit resolution
  + correcting the contradicting docs** (gap-check found no fresh resolution
  record yet; operator deliberately did not duplicate it).

### Per-repo manifestation (pushed)

| Repo | Commit | Change |
|---|---|---|
| `criome` main | `56547cc8` | `INTENT.md`: client-approval-mode + criome-owned park queue paragraph, cites `t00s`. |
| `mentci` main | `ecf3a654` | `INTENT.md`: criome owns the queue; mentci approves by `ParkedAuthorizationId`, cites `t00s`. |
| `primary` main | report 442 dir | the scan meta-report. |

## What "criome owns the keys; it decides" settles

It gives the three authorization modes one coherent meaning — the spine the
working UI needs:

| Mode | Meaning under "criome owns the keys" |
|---|---|
| **AutoApprove** | criome signs immediately with its held key, no human gate. ≈ the 1-of-1-local case (`xhwa`). |
| **ClientApproval** (the new park mode) | criome **parks**, waits for mentci/human approval, *then* signs. The meaningful human gate. |
| **Quorum** | criome gathers multi-criome-node signatures — production multi-party. |

Consequences:

- The gate is mentci's "yes" or a node quorum — **never a requester signature**.
- The predecessor's "real verdict-signing path" boundary is concrete: **mentci
  does not sign; mentci approves, and criome signs the parked object with its
  held key.** Foundation = `q1le`'s encrypted multi-key store. Not new crypto
  design.
- **Docs now wrong and needing correction (designer-owned, do not race them):**
  `criome/ARCHITECTURE.md:403-406` ("Criome does not custody private keypairs
  other than its own master") must flip to criome-owns-identity-keys; `xhwa`
  ("1-of-1 = requester signs") now ≈ AutoApprove; the gate test (spirit holds
  its own signer key and signs) should migrate to criome holding/signing.

## Build plan — two tracks plus a bridge

Full 10-step sequence in `442/9-synthesis.md`. Shape:

- **Track A — criome park substrate** (`criome` + `signal-criome` +
  `meta-signal-criome`): add the `ClientApproval` park mode; persist the
  escalated `AuthorizationEvaluation` keyed by a criome-minted
  `ParkedAuthorizationId` (reuse `AuthorizationPending`/`request_slot` from the
  signing flow); expose a list/observe-parked request routing to the
  already-built-but-unreachable `StoreKernel.authorization_snapshot()`
  (`criome/src/actors/store.rs:431,618`); change meta-approval from by-value
  to answer-by-id. **This is the spine; everything depends on it.**
- **Track B — mentci CLI as a real UI** (`mentci` only, **no schema change**):
  `mentci list` (decode the reply, render `PendingQuestionsView` via its
  existing `to_nota()`), `mentci approve|reject|defer <id>`. The daemon already
  projects the pending list (`mentci/src/state.rs:208-227`); this is purely a
  client-side verb layer over `ClientCommand`.
- **The bridge** (middle, needs both tracks): a resident process that observes
  criome's parked queue, frames each escalation into a mentci `PresentQuestion`
  carrying the `ParkedAuthorizationId` (`impl From<parked-evaluation> for
  QuestionProposal`), stores the id in mentci `State`, and on answer calls
  `CriomeApprovalBridge::submit_verdict(id, decision)`.

## Open decisions (operator recommendations; flag if wrong)

- **Defer semantics.** Currently broken to mean "forget" on both sides (criome
  folds Defer into terminal `EscalateToPsyche` and stores nothing,
  `root.rs:375`; mentci `answer()` short-circuits Defer to `VerdictAccepted`
  without touching the pending list, `state.rs:133-139`). **Recommend: Defer
  re-parks** (keeps the submission alive). Needs a psyche call — it is a
  semantics choice, not a bug fix.
- **Resident client location.** **Recommend: inside `mentci-daemon`** (grow a
  long-running criome client) rather than a separate `mentci-criome-bridge`
  binary — simpler deploy + meta-signal config shape.
- **First-milestone scope.** **Recommend: in-memory state + snapshot-poll
  `mentci list` + plaintext key** is enough to make the loop RUN over two live
  sockets. Durable SEMA (`mentci/schema/sema.schema` `*Family` redb tables —
  spec only today), push fan-out (`InterfaceFanOut` — schema-only), and
  encrypted key custody (`q1le`) are a deliberate second pass.

## Coordination state

- The **designer is actively reshaping the criome authorization / key-custody
  model and its contracts** (the key-custody thread). Operator is **holding
  Track A** (it touches `signal-criome` / `meta-signal-criome`) to avoid landing
  contract changes that collide with theirs. Per workspace discipline, designers
  shape contracts on `next`/feature branches in `~/wt`; operator owns code-repo
  `main` + rebase.
- **Track B is contract-independent and safe to start now.** The open question
  put to the psyche at handover time: **start Track B (mentci CLI as UI) now, or
  hold everything until the criome contract shape lands?** — unanswered; the
  psyche asked for this handover instead.
- All operator locks released. Working copies clean. primary, criome, mentci
  mains pushed and aligned with origin.

## Reference

### Spirit records touched / relevant

| Id | Gloss |
|---|---|
| `t00s` | **Canonical** client-approval-mode decision (clarified this session): daemon-wide park variant + criome-owned answer-by-id queue. |
| `3ss0` | **Retired** this session — duplicate of `t00s`. |
| `q1le` | criome holds an encrypted multi-key store (sub-keys); foundation for verdict signing. |
| `7x5z` | mentci component-triad shape; "criome owns the key store." |
| `xhwa` | 1-of-1 local authorization for spirit criome-gating (≈ AutoApprove under the key ruling; needs maintenance). |
| `vhs2` | criome's limited typed policy language over public-key identity atoms. |
| `psc6` | criome master-key bootstrap (single generated BLS key); `q1le` extends it. |

### Artifacts

- Scan report dir: `reports/operator/442-mentci-criome-working-ui-gap-scan/`
  (`0-frame-and-method.md`, `1-…`–`8-…` per dimension, `9-synthesis.md`).
- Workflow run `wf_fbf49ee9-bb8`; transcript under
  `~/.claude/projects/-home-li-primary/9c32d931-…/subagents/workflows/wf_fbf49ee9-bb8`.
- Predecessor reports: `reports/operator/440-mentci-criome-meta-approval-demo.md`,
  `441-mentci-criome-configure-adaptation.md`.

### Key code anchors

| Concern | Location |
|---|---|
| criome drops evaluation on escalate | `criome/src/actors/root.rs:336,345-348,375` |
| Existing park-by-slot machinery to reuse | `criome/src/actors/authorization.rs:104-158` |
| Unreachable list-all snapshot | `criome/src/actors/store.rs:431,618` |
| meta-approval by-value | `meta-signal-criome/schema/lib.schema:46-49`; `criome/src/actors/root.rs:351-383` |
| mentci CLI one-shot, raw binary | `mentci/src/client.rs:49-58,60-65,80-86` |
| mentci pending-list projection (exists) | `mentci/src/state.rs:208-227` |
| Bridge dead in every binary | `mentci/src/criome_bridge.rs`; `mentci/src/daemon.rs` (no refs) |
| Defer broken both sides | `criome/src/actors/root.rs:375`; `mentci/src/state.rs:133-139` |
| AuthorizationMode enum (2 variants today) | `signal-criome/src/schema/lib.rs:247-250` |
| Key-custody contradiction | `criome/ARCHITECTURE.md:403-406` vs `mentci/INTENT.md:30-31` |

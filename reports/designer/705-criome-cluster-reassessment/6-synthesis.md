# 705-6 — Synthesis: insights and questions

Five read-only investigators off one fetch-and-locate pass (all reads at
`origin/main`, no working-copy mutation). Heads confirmed: criome `245f0441`,
signal-criome `ff9ac192`, meta-signal-criome `4940e4b1`, CriomOS-test-cluster
`18441971`. Sub-reports `1`–`5` in this directory.

## The headline revision: "GREEN in VMs" is true only off-main

The single most important correction to my prior framing (`704`): the proven
criome VM checks are **branch-on-branch and a generation stale**, invisible to
every main.

- `mkCriomeClusterTest.nix` + `criome-cluster-1of1` + `criome-cluster-auto-approve`
  do **not** exist on CriomOS-test-cluster `main` (`18441971`, a CriomOS repin
  with no criome content in its checks). They live only on
  `origin/criome-cluster-test` (tip `a31c264`, 7 commits ahead, unmerged).
- That branch pins `criome.url` to the **`criome-auto-approve` branch**
  (`e80e206`), which is one commit *behind* criome main `245f0441` — main
  subsumed its runtime and added the entire ClientApproval surface on top.
- Net: test-cluster `main`'s `nix flake check` runs **zero** criome proofs. The
  two greens are real but off-main, and behind the landed Track A.

Independently corroborated by investigators 4 and 5 (both severity high). My
`704` "GREEN in real NixOS VMs" was accurate about the run, but glossed that
the artifacts were never integrated to a main. That de-branching is now a
prerequisite, not a footnote.

## Track A landed clean on the rules, with real authorization defects

The good: custody docs across all three surfaces now match
[criome owns key custody and decides; a multi-party quorum is k of n peer criome
nodes signing] (Spirit `p43g`, Decision Medium) — verified at
`criome:ARCHITECTURE.md:405-407,131-132`, `AGENTS.md`, `skills.md`, with no
surviving stale "personas hold their own keys" wording. NOTA examples are
positional and quote-free; generated code is all `impl`-method / `From`. The
method-only and naming rules pass on the new code.

The defects (investigator 2, the adversarial pass you asked for last session,
applied to Track A):

| Sev | Defect | Evidence | Fix shape |
|---|---|---|---|
| High | **Working-socket client can deny a parked ClientApproval request.** `reject_authorization` flips ANY slot to `Denied` with no mode-check and no caller-identity check; the meta authority is meant to be the sole decider in ClientApproval, but the working `RejectAuthorization(slot)` verb bypasses it. The meta-vs-working authority boundary is not enforced in-daemon — it rests entirely on the `0600` socket mode. | `authorization.rs:197`; `root.rs apply_authorization_approval` | Mode-gate the working reject path in ClientApproval mode |
| High | **Dead, unbuildable contract surface.** `ConfigurationRejected` + `RequestUnimplemented` (with `ManagerAuthorityRequired`/`MalformedConfiguration`/`StoreUnavailable` reasons) are defined and their constructors emitted, but `configure` always returns `Configured` even on malformed config — the contract promises a rejection handshake the daemon cannot produce. | `meta-signal-criome:lib.rs:147-153,240,243`; `root.rs configure` | Either emit the rejections (manager-authority check + malformed guard) or drop the variants |
| Med | **Approve against an unknown/resolved slot silently records a `Reject`** and replies "recorded: Reject" though nothing was recorded. | `root.rs record_authorization_approval` | Distinct not-found reply |
| Med | **Parked list sorts lexicographically over decimal-string slots** — `"10"` before `"2"`; mis-orders past 10 parked. | `store.rs authorization_snapshot` | Sort by `parse::<u64>()` (already used in `after_records`) |
| Med | **Park failure laundered into `MalformedRequest`** — a store-unavailable failure reads as malformed; typed `AuthorizationStateCreationOutcome` discarded. | `root.rs park_authorization` | Map to `AuthorizationUnavailable` |
| Med | **No `SO_PEERCRED` anywhere.** `p43g` names it as the requester-auth primitive; access control is purely the `0600` bind. The meta-vs-working authority distinction Track A leans on has no kernel-verified credential behind it. | `daemon.rs:129-135`; grep empty | Implement peer-cred, or accept 0600+single-user explicitly |
| Low | Parked-snapshot read is a full-table scan cloning full evidence per call; no Parked secondary index. Pre-existing dead free fn `active_status` (method-only violation, skeleton not Track A). | `root.rs read_parked_authorization_snapshot`; `store.rs:712` | Index when load-bearing; cleanup bead |

In the **single trusted local user** model the high gating hole is not an
immediate exploit (one user owns both sockets), but it is a design-integrity
defect that becomes a genuine authz bug the moment the trust model widens
(multi-host, multi-identity) — i.e. exactly where the cluster work is heading.

## E1 is narrower than the roadmap made it look

Investigator 3's most useful finding: the peer-signature **message design is
already built and in-process tested**. `RouteSignatureRequest` and
`SubmitSignature` are live working-contract verbs, routed to
`AuthorizationCoordinator`, which persists both. What is missing is four
concrete things, not a redesign:

1. A **TCP peer lane** — reuse the stream-generic `CriomeFrameCodec` verbatim;
   the daemon serves a *third* listener in the existing busy-poll.
2. A **per-frame BLS envelope** — `PeerEnvelope { sender_public_key, signature,
   inner_frame }`, verify-before-parse, under a **distinct DST** from
   `ATTESTATION_DST` (else cross-purpose forgery). This is `ARCHITECTURE.md:439`
   row 2 literally; authenticity not confidentiality.
3. A **peers field** on `CriomeDaemonConfiguration` (`PeerNode { master pubkey,
   host:port, identity }`) delivered as authenticated binary `Configure`.
4. **Quorum tally** — missing even single-host: nothing reads `submitted_signatures`
   back, verifies a BLS submission, decrements `missing_authorities`, or flips
   to `Granted` at k. Build it as a read-modify-write of the persisted state
   record so submissions surviving an A-restart still aggregate.

Smallest correct slice: **2-of-2 over TCP across two real daemons, proven by a
two-node `runNixOSTest`**. Model A→B as fire-and-collect (A emits off the actor
thread; B connects back with `SubmitSignature`) rather than a full async serve
rewrite in slice 1. Deferred: timeout/retry, n>k partial collection, async
serve loop, in-transit encryption, E2 admission.

## Sequencing: both strategy investigators say proof-first

Investigators 4 and 5 independently recommend **ClientApproval park VM-proof
first, then E1** — not instead. Reasons:

- The park flow is **runtime- and contract-complete on all three mains but has
  zero test coverage anywhere** — unproven landed code on main is the worst
  state (reads as done, gets built on, fails far downstream). Closing it is a
  small, fully designer-lane test (the existing auto-approve `Configure`
  round-trip plus extra approve/reject round-trips). The **only** blocker is a
  missing `criome-client-approval-witness-test` binary — no generator change.
- Proof-first **forces the de-branching cleanup** (repoint test-cluster's criome
  input to main, port the witness bins onto criome main, land the criome checks
  on test-cluster main) that E1 would otherwise inherit anyway.
- E1 is large, multi-session, and partly design-blocked on the open questions
  below.

E1-first is defensible if the networked demo outranks loop-closing — but it
consciously leaves Track A unproven on main and inherits the de-branch debt.

## p43g status

Confirmed in Spirit (Decision, certainty **Medium**, importance Minimum,
privacy Zero, referents `[criome mentci spirit]`), consistent with the landed
custody docs and mapping 1:1 to `AuthorizationMode [Quorum AutoApprove
ClientApproval]`. One observation: Medium certainty now governs the entire
quorum/key-custody arc; if the psyche regards it as settled bedrock a bump to
High is warranted (`ChangeCertainty` / repetition evidence).

## Open questions for the psyche

1. **Sequencing** — park VM-proof first (recommended), E1 first, de-branch-only
   first, or park-proof + E1 in parallel?
2. **Track A authorization defects** — do I prototype fixes on a criome branch
   for operator to rebase (recommended; in-lane per "keep prototyping criome
   runtime"), flag for operator to own on main, or accept the single-user posture
   and track as beads?
3. **`SO_PEERCRED`** — scheduled gap to implement as part of the meta-vs-working
   boundary, or considered satisfied by `0600` + the per-user single-daemon model?
4. **`p43g` certainty** — bump Medium→High if settled bedrock.
5. **E1 wire-crypto (if/when E1)** — authenticity-only BLS envelope assuming the
   tailnet provides confidentiality, vs encryption-in-transit in slice 1; and
   does E1 depend on E2 (cluster-root admission) or is static peer config the
   deliberate first cut?

## Update (post-investigation): operator landed the Track A fixes in `6a5e797`

Verified after the investigation: the Track A defects above were **real at
`245f0441`** (the snapshot the investigators read) — at that commit `root.rs`
had no ClientApproval reject-gate, emitted neither `request_unimplemented` nor
`configuration_rejected`, and `store.rs` sorted slots lexicographically. Operator
then pushed criome `6a5e797` ("harden client approval authorization
boundaries", the only commit since `245f0441`: `root.rs +18`, `store.rs +21`,
`tests/daemon_skeleton.rs +174`) which fixes all of them — the reject-gate in
ClientApproval mode, unknown-slot → `RequestUnimplemented`, malformed-Configure →
`ConfigurationRejected`, numeric slot sort, and removal of the dead
`active_status` free function.

A transient error in the chat relay (now corrected): a `git show origin/main`
read after operator's push returned the *fixed* code, and I briefly mislabeled
the findings "false positives." They were not — the investigator was right; the
defects were real and are now fixed on main. This is the same stale-vs-fresh ref
hazard that recurred all session, here in the read-newer-than-expected direction.

Net: the "designer prototypes the Track A fixes on a branch" path (question 2's
answer) is **moot** — operator owned and landed the runtime fixes (their lane).
Designer focus stays on the ClientApproval park VM-proof. The remaining real,
small items are the park-failure typed-error mapping (`park_authorization` still
maps any store error to `MalformedRequest`) and the `Defer` semantics
(park-and-wait, with a now-unreachable `Defer → Parked` arm in the status match)
— both minor, both operator-runtime, flagged not fixed.

## Proof-first: the ClientApproval park flow is proven (witness branch)

The latent-risk loop (park substrate landed-but-unproven) is closed at the
functional level. Designer branch `criome-client-approval-witness` (`2bb8645e`,
one additive commit off main `6a5e797`) adds two feature-gated
(`cluster-witness`) test bins:

- `criome-client-approval-witness-test` (new) — drives the full ClientApproval
  flow against a real daemon over its working + meta sockets:
  `Configure(ClientApproval)` → working `EvaluateAuthorization` parks →
  meta `ObserveParkedAuthorizations` lists the slot → meta
  `SubmitAuthorizationApproval(Approve)` → working `ObserveAuthorization` reads
  status `Granted`; a second submission with `Reject` reads status `Denied`.
- `criome-auto-approve-witness-test` (ported forward from the
  `criome-auto-approve` branch, which main otherwise lacks — needed so the
  test-cluster can repoint its criome input to main and retire that branch).

Proven by a local real-daemon smoke (real `criome-daemon`, real BLS, real Unix
sockets), run by the building agent and **independently re-run and confirmed
green** (`SMOKE-PASS`, base `6a5e797a`): both witnesses exit 0; the
client-approval witness emits all five PROOF lines for both the Approve→Granted
and Reject→Denied paths. This is a process-level proof, not yet the systemd /
NixOS-VM level — that and the de-branching are blocked on cloud-operator's lock
on `CriomOS-test-cluster`. The branch is ready for operator to rebase onto main
and for the nixosTest wiring once the lock releases.

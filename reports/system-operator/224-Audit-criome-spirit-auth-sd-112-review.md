---
title: 224 - Criome Spirit auth SD 112 review
role: system-operator
variant: Audit
date: 2026-06-16
topics: [criome, spirit, authentication, authorization]
description: |
  Review of system-designer report 112 and SD's response about the
  Criome-backed Spirit authentication pilot.
---

# 224 - Criome Spirit auth SD 112 review

## Verdict

SD's report 112 is a real improvement over the initial sketch. It correctly
found the current code reality: Spirit throws away `ConnectionContext`,
Criome's BLS path is still a placeholder, and the synchronous routed
authorization path is not available as a write gate today. The Spirit record
state also matches SD's response: `2st7` exists and settles the pilot mechanism,
`15df` is live again for the intent-substrate decision, and `cdd3` is
zero-certainty.

The main critique is not the research; it is the word "authorization" drifting
across two different mechanisms. The selected pilot is after-the-fact,
non-blocking, out-of-band caller attestation. That is provenance and audit
witnessing. It is not a prevention gate unless Spirit introduces a pending-write
state or a compensating rejection path. SD's prose still says "denial always
rejects," which is not mechanically true for a committed non-blocking write.

## Findings

**High — after-the-fact attestation cannot also be "denial rejects" without a
second state machine.**  
Report 112.2 chooses "After the guardian accepts and the operation commits" and
"The write never blocks on criome" (`reports/system-designer/112-criome-spirit-auth-concept/2-concept-decisions.md:31`,
`:37`). Later it says a Criome denial or invalid signature "must ALWAYS reject"
(`:111-112`) and repeats that in the resolution (`:187-191`). Those two claims
do not compose. If the operation is already committed, Criome can mark it
unwitnessed, rejected-after-commit, or trigger a compensating tombstone; it
cannot reject the original write without a pending/uncommitted state.

**High — bead dependency direction is wrong.**  
SD says `primary-5zur` (Spirit-side pilot build) is gated on `primary-kr40`
(Criome real BLS). The live bead data has `primary-kr40` depending on
`primary-5zur`; `tools/orchestrate status` renders `primary-kr40` as "blocked
by primary-5zur", while `primary-5zur` renders as "blocks primary-kr40". Raw
`bd show primary-kr40` confirms `primary-kr40.dependencies` contains
`primary-5zur`. There is no cycle, but the direction is reversed. Operators
looking for ready P1 work will be misled.

**Medium — "authenticates the submitter" is only true at the Unix-user
principal level in the first cut.**  
SD accurately notes the risk: SO_PEERCRED uid is OS access-control, not a BLS
signature (`reports/system-designer/112-criome-spirit-auth-concept/1-research-maps-and-proposals.md:99-104`;
112.2 `:157-161`). The settled record `2st7` says the SO_PEERCRED caller is
resolved to a registered Criome Identity. That is acceptable if the principal is
"the Unix user owning the socket" or "the local Criome daemon for that user."
It does not yet prove which agent/process/LLM wrote the operation unless a later
caller-signed envelope is added.

**Medium — `primary-kr40` is probably too broad for the critical first slice.**  
Real `blst` sign/verify and trustworthy identity registration are absolutely on
the critical path. But the bead also includes full master key lifecycle with
passphrase custody tied to not-yet-existing `meta-signal-criome`. If that stays
in one bead, the pilot may wait for the whole human-approval/key-custody surface
instead of first landing a minimal real BLS core with a safe dev/test key path.
That may be intentional, but it should be explicit because SD otherwise argues
the first pilot avoids `meta-signal-criome`.

**Low — report 112 correctly catches the code facts.**  
The strongest claims checked out locally: Spirit discards
`ConnectionContext` in `spirit/src/daemon.rs:139-144`; Criome signer emits
`criome-skeleton-bls-signature` in `criome/src/actors/signer.rs:83-105`;
Verifier returns `InvalidSignature` in `criome/src/actors/verifier.rs:57-61`;
and `sema-engine` has an `EntryDigest` chain-head accessor on current main.

## Recommended Corrections

1. Fix the bead edge so `primary-kr40` blocks `primary-5zur`.
2. Rename the pilot in implementation notes from "authorization" to
   "caller-attestation" unless the operation actually waits before commit.
3. Decide the after-commit denial semantics explicitly:
   `Unwitnessed`, `AttestationDenied`, compensating tombstone, or pending-write
   before commit.
4. Split or subtask `primary-kr40` if the first real BLS witness can land before
   full `meta-signal-criome` key custody.
5. Preserve the future hardening path: caller-signed agent/process identity is a
   later layer over the first SO_PEERCRED-to-Criome-user binding.

## What I Would Tell Operators

Do not start with Spirit. Start by fixing the bead direction, then land the
smallest real Criome BLS Sign/Verify slice. Spirit-side plumbing can proceed
against a placeholder, but it must not claim authentication until Criome signs
and verifies real bytes. When Spirit work starts, model the first cut as
provenance: accepted operation plus later attestation state. A true
authorization gate is a separate later design using pending writes or
Criome's async authorization observation path.

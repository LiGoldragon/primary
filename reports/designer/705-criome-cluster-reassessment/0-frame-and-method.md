# 705-0 — Criome cluster reassessment: frame and method

## Trigger

Psyche (post-compaction): *"re-asses the situation, and report with your
greatest insights and questions."* Immediately preceded by operator's Track A
landing report (ClientApproval park substrate on all three repo mains).

## Spirit gate

Outcome: **no-capture**. The prompt is a task-only order (perform a
reassessment + surface questions); it asserts no durable Decision / Principle /
Correction / Clarification / Constraint. The governing decision remains `p43g`
— criome owns key custody and decides authorization; a multi-party quorum is k
of n **peer criome nodes** signing with their own master keys; the requester
only submits (authenticated by SO_PEERCRED). If the psyche's answers to the
questions below assert new durable intent, capture then. One open verification:
confirm `p43g` is actually recorded in Spirit and consistent with the landed
custody docs (delegated to investigator 5).

## Lane state at reassessment

- **Operator landed Track A and released the lock.** signal-criome
  `ff9ac192` (ClientApproval, parked-authorization records/snapshot,
  `ObserveParkedAuthorizations`, `AuthorizationStatus::Parked`),
  meta-signal-criome `4940e4b1` (meta list-parked + approve/reject/defer by
  `AuthorizationRequestSlot`), criome `245f0441` (ClientApproval parks/lists/
  approves-rejects-defers by slot, **plus the stale custody docs corrected to
  `p43g`**). `cargo test --features nota-text --all-targets` green in all three;
  all origins match. Bead `primary-at7x`: remaining work is designer-owned VM
  proof + review.
- **Designer (this lane) owns:** VM-proof of the park/approval flow, critical
  review of the landed contracts + runtime, and prototyping E1 (cross-criome
  peer transport) toward the multi-machine quorum — per `704/5`.

## Proven before this session

`criome-cluster-1of1` (Stage A) and `criome-cluster-auto-approve` both GREEN in
real NixOS VMs (real criome-daemon, real BLS, real Unix sockets; auto-approve
proven via a meta `Configure` round-trip). No cross-machine networking yet — E1
(701) is unbuilt.

## Method

A five-investigator read-only workflow, preceded by one fetch-and-locate pass so
every investigation reads at `origin/main` without working-copy mutation — the
direct fix for the stale-checkout collisions that recurred throughout last
session. The investigators:

1. **Ground-truth criome main** (`245f0441`) — the current architecture with
   file:line: the three authorization modes, the ClientApproval park flow, the
   meta socket, `transport.rs`, the peer-signature actor flow.
2. **Track A critical review** — adversarial: design / code / contract / rule
   smells across the three landed commits; verify the custody-doc fix matches
   `p43g`; check the `AuthorizationRequestSlot` park model is sound.
3. **E1 readiness** — the precise cross-criome peer-transport gap, the smallest
   correct first slice, and the hard design decisions (framing, sync vs async).
4. **VM-proof + test harness state** — the ClientApproval park VM test, the
   criome-input repoint to main, and the N-node path in `mkCriomeClusterTest`.
5. **Strategic / completeness** — the whole arc vs the original goal; the
   highest-leverage next move; glossed gaps; and whether `p43g` is in Spirit.

Sub-reports land as `1`–`5` in this directory; the synthesis (insights +
questions) as `6`.

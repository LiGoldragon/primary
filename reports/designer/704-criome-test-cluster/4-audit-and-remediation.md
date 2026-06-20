# 704-4 — Adversarial audit + remediation (psyche-requested)

The psyche asked for a deep critical audit of the auto-approve work ("be
critical. look for bad design and ugly code"). A 5-critic adversarial workflow
ran it; full output at the workflow transcript
(`tasks/wj9b2bgse.output`). This file is the verdict + my honest disposition.
**I accept the central finding and do not defend the design.**

## The headline (B1) — accepted

**AutoApprove is a no-crypto "allow everything" bypass of the authorization
boundary, with no mechanical guard against production.** `root.rs` short-circuits
`EvaluateAuthorization` to `Authorized` and *publishes* the object for any
well-formed request — no signature, no key registry, no contract, no quorum. The
only thing keeping it out of production is a struct default; it is reachable from
the **startup rkyv config** (the same deploy tooling that configures production)
and flippable **at runtime** over the `0o600`-only meta socket (no caller auth),
and it echoes the attacker-supplied unsigned `AttestedMoment` downstream.

**The decisive point: the bypass buys nothing.** A trivially-satisfiable **1-of-1
self-signed quorum** brings the spirit→criome→mirror loop up just as easily with
*real* crypto — and **my own `criome-cluster-1of1` nixosTest already proves that
path green** (register identity → admit `Threshold(1)` → sign → `Authorized`;
threshold-short → `Rejected`). The schema already carries the right noun
(`AuthorizationPolicyClass [SimpleSelfSigned ComplexQuorum]`). `AuthorizationMode
[Quorum AutoApprove]` is a *second, duplicated* policy axis that also violates
schema-emitted-types-are-the-nouns.

**Recommendation: drop AutoApprove. Use the 1-of-1 quorum (already working) as
the bootstrap.** This is a decision point, not a unilateral change, because
**operator landed `AuthorizationMode` on signal-criome main** (`aa5498a`) — so
removing it reverses operator's contract and needs the psyche + operator. If a
literal bypass is ever truly needed for a first beat, it must be
`#[cfg(feature = "insecure-auto-approve")]`-gated out of production binaries and
loudly refuse at startup — never a config default.

## Disposition per finding

| # | Finding | Severity | Disposition |
|---|---|---|---|
| B1 | AutoApprove bypass, no production guard | blocker | **Accept. Recommend drop → 1-of-1 quorum (already green). Psyche+operator decision (operator's landed contract).** |
| B2 | Harness doesn't wire the auto-approve proof | blocker | **Resolved** — race artifact: the audit snapshot predated my wiring; `criome-cluster-auto-approve` is wired and **green in a VM** (commit `115131f5`). |
| B3 | Encoder can't express `authorization_mode`; 3-arg vs one-NOTA convention | major | **Operator's code** (`criome-write-configuration.rs`, landed `1eaa783`). Flag to operator. Cold-boot limitation moot if AutoApprove dropped. |
| B4 | Encoder panics instead of typed Result in ExecStartPre | major | **Operator's code.** Flag to operator. |
| B5 | `Configure` silently partial-applies; never uses `ConfigurationRejected` | major | **Accept (mine).** Contingent on B1 (what Configure may change). Narrow input or reject unsupported fields; resolve `ManagerAuthorityRequired`. |
| B6 | Runtime `Configure` can downgrade Quorum→AutoApprove, no caller auth | major | **Accept (mine).** Make verdict policy startup-only, or authenticate the caller + refuse downgrades. Contingent on B1. |
| B7 | Harness hand-rolls a root-only guest; sidesteps per-Unix-user; ignores test-substrate | blocker | **Accept (mine).** Either build through mkDeployTest's substrate + non-root user + a deny assertion, or **drop the per-Unix-user framing** (it's a gate-logic test, not an isolation test). Honesty fix. |
| B8 | `builtins.head members` silently discards N-node input (false API) | major | **Accept (mine). FIXING NOW** — honest single-member shape. |
| B9 | `rejection`/`actor_reply` free functions (method-only rule) | major | **Operator's existing code** (`actors/mod.rs`); my AutoApprove arm adds a call site. Flag to operator; I avoid extending it (moot if B1 drops the arm). |
| B10 | Designer raced operator on criome main; 7 stale-checkout dups; false bug report | major (process) | **Accept.** Already self-flagged in the frame. Mechanical fix: fetch-origin-first as a dispatch pre-step; designer confines to signal-criome contract + nixosTest, not `root.rs`/`daemon.rs`. |

Minors (typed `ConfigurationGeneration` newtype + persist/rename; move
`EvaluateAuthorization` to `AuthorizationCoordinator`; witness `String`→`DaemonPath`
derived paths; rename "evidence-less" → "threshold-short"; `CriomeTopology`
typed-or-dropped; config blob out of the socket dir; paths from constants; README
criome entry; `serve_forever` tokio `select!`; drop `decision.clone()` /
`with_meta_socket`) — most are on the AutoApprove path and resolve with the B1
decision; the rest are opportunistic follow-ups noted for whoever lands the
integrated slice.

## What's actually fine (per the audit)

Daemon arg/flag discipline (one rkyv arg, no NOTA, no flags); no `anyhow`, real
per-crate `thiserror`; no hand-rolled parsers; full-English identifiers; new code
consumes schema-emitted types (except the AuthorizationMode duplication); the
**Quorum path itself is sound** (validates the stamp before publishing); the meta
`Configure` mechanism + per-component meta socket (`da5i`) are mechanically clean
— the problem is what `Configure` is *allowed to do unguarded*, not that it
exists; the VM-prover bins legitimately use panic-as-assertion.

## Net

The audit confirms the criome **meta-Configure** work and the **1-of-1 quorum**
test are sound; the **AutoApprove bypass** is the bad design and should be
dropped in favor of the already-proven 1-of-1 quorum. The honest end state of
"fix it all": the meta socket configures (da5i ✓), the 1-of-1 gate is proven in a
VM (✓), and auto-approve should not ship as a no-crypto bypass.

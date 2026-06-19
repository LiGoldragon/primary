# 702 — corrections from operator 434 (designer accepts)

Operator reviewed 702 (`reports/operator/434-designer-702-deep-engine-analysis-review.md`,
primary main `e723f289`) and corrected four evidence statements. I
independently re-verified each against current `main` and **accept all four**.
This file amends the standing-risk framing; the synthesis (`14-synthesis.md`)
and verification ledger (`12-adversarial-verification.md`) should be read
through these corrections. The corrections do **not** change the four
load-bearing conclusions (they hold, see bottom).

## Correction 1 — kameo split is source-graph-verified, deployed-UNwitnessed

702's synthesis presented "the deployed binary diverges from audited source"
as fact. It is **inference**, not a witness. Verified state:

- **Source graph IS split** (confirmed): criome/router/mentci cargo trees use
  the fork `LiGoldragon/kameo.git#f491b45`; spirit/mirror default trees route
  `triad-runtime#f46f66e` through stock `kameo 0.20.0`.
- **Deployed graph is UNwitnessed**: `spirit/flake.nix` carries explicit
  `kameo-source` vendor/patch machinery and `spirit/Cargo.lock` contains
  **both** stock and forked kameo entries — the operator-431 managed
  two-identity transition, not an accident.

Corrected framing: the cargo source-graph is split; whether that reaches the
deployed binary needs a Nix fleet build/dependency witness that **no lane
ran**. The remediation is unchanged (one fleet-wide kameo decision + a Nix
witness) — but the witness is now **step 1**, not a footnote, and 702 must not
be cited as a verified deployed-binary fact.

## Correction 2 — the mentci "phantom file" downgrades were wrong

`12-adversarial-verification.md` downgraded mentci-2 and mentci-4 claiming
`nexus.schema` / `sema.schema` are phantom and only `lib.schema` exists. That
is **false against mentci main `577d64b`** (I verified):

- `mentci/schema/nexus.schema` — 476 lines.
- `mentci/schema/sema.schema` — 355 lines.

The skeptic checked the wrong checkout — the *contract* repos
(`signal-mentci`, `meta-signal-mentci`) carry only `lib.schema`; the **daemon**
repo `mentci` carries the `.schema` files. `FrameEscalation`,
`CriomeEscalation`, persisted family declarations, and `ProposalDigest` are all
present there. **Reclassification:** the mentci gaps are real but *sharper*
than the downgrade allowed — the sema families are **declared in
`sema.schema`, just not wired to durable redb** (declared-but-unwired, an
actionable wiring task, not vaporware). The "phantom citation" criticism is
struck; the underlying gaps (no durable runtime SEMA, no criome verdict
egress, identifier-derived `ProposalDigest`) stand and rise from "evidence
fabricated" to "real and located."

## Correction 3 — ComponentKind divergence is narrower than stated

`13-completeness.md` named `signal-criome`, `signal-mentci`, and
`meta-signal-mentci` as divergent local copies. Verified state is narrower:

- `signal-standard` — the canonical 14-variant roster.
- `signal-criome` — local 7-variant roster → **genuinely divergent** (the one
  real fix).
- `meta-signal-mentci` — local **14-variant roster matching** signal-standard,
  with comments naming the eventual import → import debt, **not** divergence.
- `signal-mentci` — **no** local `ComponentKind` (verified). Drop from the bead.

Corrected bead: fix `signal-criome` divergence by importing signal-standard;
retire `meta-signal-mentci`'s matching local copy as architectural cleanup.

## Correction 4 — router fanout exists at the actor layer; the gap is the wire

router-1 ("matcher wire-unreachable") is right that `signal-router::Input`
lacks Attend/Withdraw/Publish and the socket-facing working signal cannot drive
fanout. But operator notes router main **already routes fanout through
`RouterRuntime` actor messages** — `Message<AttendAuthorizedObjects>`,
`Message<WithdrawAuthorizedObjects>`, `Message<PublishAuthorizedObjectReference>`,
`Message<ReadAuthorizedObjectFanoutStatus>`. So the next slice is **"expose the
existing runtime fanout over the working signal + push to subscriber sockets,"**
not "build the matcher." This sharpens the router work-item in the brief.

## What holds unchanged (operator-confirmed)

1. **Spirit has no real criome authorization** dependency or daemon call in the
   commit path (criome 0× in spirit's manifest; the full-chain test represents
   the criome step as a typed reference into router fanout, not a daemon auth
   call).
2. **Spirit's restore-head-mismatch guard is production code**, but the
   flagship full-chain test still exercises a test-local `RestoreAttempt`, not
   `Store::import_mirror_restore_bundle` directly.
3. **Mirror restore is store-name-only** — caller-side stale detection only;
   cannot serve exactly a requested head digest.
4. **schema-rust-next has panic-shaped malformed-name paths** (`Ident::new`,
   `syn::parse_str(...).expect`, emitted-token parse panics) — the typed-error
   fix is a real task.
5. **The `{| |}` catalog is merged but unconsumed** by schema-rust-next — a
   "feature ahead of consumer" state, **not** a production regression.

These five are the spine of the operator work program (`703/6-operator-brief.md`).

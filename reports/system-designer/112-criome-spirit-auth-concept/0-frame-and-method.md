# 112 — criome ↔ spirit authentication pilot — frame and method

*The psyche reanimated the criome subject in the context of spirit: "spirit needs
authentication. The criom[e] is how we authenticate anything, and it's a perfect
pilot. Once an operation passes on spirit (through the guardian), the operation asks
criome to authorize it. Criome can create a signature on the content-addressed
[entry / additional message] of the log — or something like this, whatever works."
This meta-report is the concept and the decisions the psyche asked to make. The
mechanism the psyche sketched is explicitly a DRAFT ("whatever works"); the point of
this session is to turn it into decision-ready choices.*

## Files in this report

- `0-frame-and-method.md` — this file: the question, the Spirit gate + intent
  reconciliation, and the research method.
- `1-research-maps-and-proposals.md` — the four research maps (the criome-skeleton
  reality, spirit's write-path gap, sema content-addressing, the principal/fit map)
  and the three mechanism proposals.
- `2-concept-decisions.md` — **the deliverable**: the critique-corrected concept and
  the decision list for the psyche, plus dependencies, risks, and the deferred
  intent-substrate decision.

## Spirit gate — what was captured, and the reconciliation

The prompt was addressed to system-designer; the psyche separately invited
system-operator to join (their position is `reports/system-operator/223`). Two
lanes captured in parallel, which forced a reconciliation. Net state after this
session:

- **`w2g3`** (operator, Decision Medium) — **canonical** for the pilot:
  [Spirit should be an early pilot consumer of Criome-backed operation
  authorization: Spirit operations that require authentication ask Criome to
  authorize an exact content-addressed request or log-message digest, with the
  concrete envelope design still open.] Domains `(Security Authentication)` +
  `(Security Authorization)`; referents `spirit criome`.
- **`kxdz`** (mine, Decision) — **zeroed (recoverable)** as a content-duplicate.
  Its "criome is the universal authenticator" half duplicates the pre-existing
  `a4i6` [Every component/daemon can escalate to Criome for an authorization check…
  the agent's Criome public-key is the authoritative authentication anchor] and
  `q1cw` [Identity verification routes through criome]; its "spirit is the pilot"
  half duplicates `w2g3`, which is better-scoped. Per "designer gap-checks, operator
  records; don't pre-record in parallel," the operator's record wins.
- **`15df`** (mine, Correction) — **zeroed (recoverable)**, deferred to an explicit
  psyche decision. It recorded [intent lives in Spirit, not files] as a Correction
  superseding `cdd3`. The operator independently declined to record the same idea
  because the psyche phrased it as emerging direction ("I think… we don't have to do
  that now") and it overturns the active workspace contract. That catch is correct:
  superseding a load-bearing contract is explicit-only, so this is a psyche decision
  (see `2-concept-decisions.md` §"Deferred decision E"), not an inferred Correction.
- **`cdd3`** (Principle High) — **left live**: [Intent lives in the file that owns
  its scope…]. It remains the current contract until the psyche rules on E.

The genuinely-new, uncontested intent (criome is the universal auth anchor; spirit
is the pilot; the mechanism is open) is fully held by `w2g3` + `a4i6` + `q1cw`. The
mechanism stayed uncaptured by design — it is what the decisions below settle.

## Pre-existing criome-auth intent (the neighborhood I initially missed)

My first keyword query for "authentication" returned nothing; the records are
domain-routed under `(Technology (Software (Security Authentication|Authorization)))`
(19 records). The load-bearing ones for this pilot:

- `a4i6` — every component can escalate to criome; the Criome public key is the
  authoritative authentication anchor.
- `9v7h` — owner-socket SO_PEERCRED peer-credential auth REJECTS on uid mismatch,
  fail-closed (defense in depth atop the socket file-mode guard).
- `i9qv` / `jtmt` / `q1cw` / `fahc` — possessing a Criome identity is the power to
  sign; the public key IS the identifier; identity verification routes through
  criome.
- `3fm6` — long-lived agents have cryptographic identity tied to their Criome master
  public key; transitional agents get an ephemeral keypair.

These say *criome is the authenticator*; none says *how spirit consumes it*. That
gap is the concept.

## Method

A nine-agent designer workflow (`wf_9e53ff18-63d`): four parallel readers
(understand) → three competing mechanism proposals (design) → one synthesis → one
adversarial critic. The critic found the synthesis **not MECE** and its recommended
default failing the stated goal; `2-concept-decisions.md` carries the
**critique-corrected** concept, not the raw synthesis. All code claims below are
spot-confirmed against the pinned source (file:line cited in `1-…`).

# 690 — synthesis: the engine stack after a week of change

The one-sentence finding: **a single grammar change in the codegen
engine (strict positional structural field roles) drove a clean
port-to-strict-contracts wave through every consumer, and on top of that
clean spine criome grew an agreement-machine, router grew networking,
spirit grew a new guardian gate, and mentci was born — the spine is
coherent and green; what is not yet closed is the cross-component
*delivery* chain (criome pulse → router fan-out → mirror), which is being
built on branches right now, plus two real criome crypto-safety woes.**

Read with `0-frame-and-method.md` (scope + method) and `9-cross-cutting.md`
(the coherence/completeness critics + my branch verification). Per-engine
detail is in `1-schema-next.md` … `8-mentci.md`.

## The stack at a glance

```mermaid
flowchart TB
  subgraph T1["codegen engine — GREEN, COHERENT"]
    direction LR
    nn[nota-next<br/>7-shape codec] --> sn[schema-next<br/>field-roles grammar<br/>schema-cc resolver] --> srn[schema-rust-next<br/>quote! emission]
  end
  subgraph T2["storage engine — GREEN, HARDENED"]
    sema[sema-engine<br/>CommitLog+Outbox planes<br/>sound lock · closed RecordKey · O(1) head]
  end
  subgraph T3["component engines"]
    direction LR
    cri[criome<br/>pulse+policy+attested-moment<br/>⚠ k&gt;n/2 · ⚠ BLS-agg]
    rou[router<br/>milestone-2 forward GREEN<br/>matcher on branch]
    spi[spirit<br/>negative-guideline gate<br/>public-text-search · ResolveClarification]
    men[mentci<br/>NEW · closed verdict<br/>daemon builds green]
  end
  mir[["mirror — UNAUDITED<br/>chain endpoint"]]
  T1 --> T3
  T2 -.-> T3
  cri -. "authorized-object reference" .-> rou
  rou -. "fan-out (branch attendance-fanout-139)" .-> men
  rou -. "NotifyObject octets" .-> mir
  classDef warn fill:#fff3cd,stroke:#d39e00;
  classDef miss fill:#fdd,stroke:#c00;
  class cri warn; class mir miss;
```

## Verified state — what is real on `main` vs in-flight

| Engine | On `main` | Status |
|---|---|---|
| nota-next | 7-shape StructuralMacroNode codec, byte-exact round-trips | **Green** (75 tests). Gap: pipe-delimiter shape layer still OPEN (tracked) |
| schema-next | field-roles grammar + 3 reject paths; schema-cc resolver replaced hand match (build-gated) | **Green** (176+20). Gap: family body still hand-parsed (`v0n6`); skill stale |
| schema-rust-next | token-native emission; standard newtype impls (WireContract-scoped) | **Green** (92). Drift: narrower than report 663 (slices 1/3/4 unlanded) |
| sema-engine | god-impl decomposed; sound lock; closed RecordKey; O(1) head | **Green** (116). Gap: no witness live consumer stores are layout-5 |
| criome | strict port; pulse; policy contracts; attested moments; closed escalation | **Green** (70). **2 open woes**: `k>n/2`, BLS-aggregate. Drift: still holds operational matcher (m0p2) |
| router | strict port; milestone-2 forward (loopback green); payload-blind | **Green** (64). Matcher + cross-host witness **on branches** (verified) |
| spirit | negative-guideline gate (artifact); public text search; ResolveClarification | **Green** (contract). Mirror-shipper + offline-e2e are feature-gated, not in deployed binary |
| mentci | daemon **builds** (not skeleton); closed verdict; daemon-minted ids; filtered subs | **Green** (10). SEMA in-memory; verdict→criome egress schema-only |

In-flight, **verified on branches dated the audit day**: router
`attendance-fanout-139` (matcher + fan-out + first signal-standard
consumer), signal-router `attendance-fanout-139` (Attend/Withdraw),
router `transport-two-kernel-e2e-138` (cross-host witness, past P3).

## The four narratives of the week

1. **The strict-positional grammar wave.** schema-next's three
   field-role commits (`af3705c`/`95f1ee7`/`1de72dd`) are the spine;
   every `signal-*` contract and every daemon ported to it and stayed
   green. This is the audit's strongest positive result: a breaking
   grammar change propagated cleanly across the whole stack.

2. **criome became an agreement machine.** In two days criome grew the
   authorized-object pulse (references, not payloads), persisted policy
   contracts with stamped quorum signatures, bound evaluation to attested
   moments (a-priori window in the signed digest), and a closed psyche
   escalation outcome. The shape matches intent (`m0p2`/`z9d6`/`ay3y`/
   `gc0n`). The two crypto-safety woes from report 684 are **still open
   and still real** — they are the highest-value criome beads.

3. **router learned to network, mentci was born.** router's milestone-2
   router-to-router forwarding is real over loopback and payload-blind;
   the cross-host witness and the m0p2 fan-out matcher are on branches.
   mentci went from skeleton to a **building daemon** with a genuinely
   closed verdict — the `EscalateToPsyche` dead-letter now has a
   receiver.

4. **spirit grew a gate that changes how we capture intent.** The new
   `NegativeGuideline` guardian reason remands any record whose operative
   guidance is *primarily* an exclusion/prohibition/forbidden-list;
   capture must lead with the **affirmative** canonical shape. This is
   the most operationally-relevant change for every psyche-facing agent —
   and the workspace skill files did not teach it. (Fixed this session:
   `skills/intent-log.md`, `skills/spirit-cli.md`.)

## Operator-actionable beads (an audit that ends without beads is incomplete)

**P1 — close the delivery chain (mostly in flight; integrate + finish):**
- `criome`: retire the operational interest-matcher from
  `SubscriptionRegistry` down to observation/audit-only; rewrite
  `ARCHITECTURE.md:110-116` to router-sole per clarified `m0p2`. *(The
  criome half of the matcher reconciliation — the router half is on
  `attendance-fanout-139`.)*
- `router`/`signal-router`: land `attendance-fanout-139` (matcher +
  Attend/Withdraw + fan-out) and `transport-two-kernel-e2e-138`
  (cross-host witness) to main; they realize `m0p2`/`l2ha` + designer-688
  #2 and refute the "absent matcher" / "cross-host unproven" gaps.
- **owner needed for `mirror`**: verify it builds after `b26c139`, and
  that `1275045` routed-object-notice handling matches router delivery +
  spirit outbox-drain — it is the chain endpoint nobody audited.

**P1 — criome crypto safety (no branch, real):**
- `criome`: enforce `k > n/2` majority in the AttestedMoment rejection
  guard + Threshold `validate_shape` (one OR-term each) + a partition-fork
  rejection test. (684 Woe 3.)
- `criome`: add `aggregate_verify_bls` (blst `FastAggregateVerify`) and
  refactor the quorum loop to one aggregated pairing; benchmark k=5.
  (684 Woe 5.)

**P2 — coherence debts:**
- decide `StandardSocket` shape (sum vs newtype) then migrate
  signal-criome + the mentci contracts to import signal-standard's
  `ComponentKind`/interest-lattice, deleting the local copies (one
  coordinated breaking change).
- cross-cutting **consumer-build sweep**: confirm the ~12 unaudited
  consumer daemons (message, lojix, terminal, introspect, mind, persona,
  cloud, domain-criome, upgrade, orchestrate, repository-ledger,
  triad-runtime) build after their strict port + sema-5 migration, **nix
  path included**, before the stack is treated as green.
- `mentci`: durable SEMA from `sema.schema` families (self-resume on
  restart); canonical `ProposalDigest` (rkyv content hash, not `format!`).

**P2 — designer-lane doc fixes (skills):**
- `skills/structural-forms.md`: (a) family form is **labeled**
  `(Family { record Entry table entries key Domain })`, not the
  positional `(Family StoredRecord records Domain)` at line ~100; (b)
  two independent agents (nota-next + schema-next) found the
  named-field-enum-variant + struct-body-derive claims (lines ~40-44)
  are **rejected by the nota-next HEAD derive** and schema-next still
  hand-parses family bodies — reconcile against tasks #411/#416 (re-land
  or correct the skill). *Flagged, not edited blind — needs direct
  byte-level verification by the nota-next owner.*

**P3 — verifiability:**
- nix `flake check` witnesses for schema-next / router / spirit at the
  audited HEADs; CI job building spirit `--features mirror-shipper`.
- recorded-transcript guardian test asserting `NegativeGuideline`
  without a live provider (today only `#[ignore]`d live-DeepSeek).

## Method note — the completeness critic earned its place

The 8 per-engine agents read `main`-HEAD only and over-reported three
HIGH gaps as "absent" that were in-flight on branches dated the same day.
The completeness critic caught all three; I verified them directly before
synthesizing (the cross-lane-state re-verification discipline). This is
the loop-completeness pattern working as designed: the adversarial
critic, not the engine agents, holds the truth about what the audit
*didn't* look at.

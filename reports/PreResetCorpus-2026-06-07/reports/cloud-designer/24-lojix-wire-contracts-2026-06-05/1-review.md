# Adversarial review — lojix wire contracts (Phase 1)

*Reviewer: cloud-designer lane. Subjects: the three drafts under
`reports/cloud-designer/24-lojix-wire-contracts-2026-06-05/drafts/`.
Read-only review; no edits to the drafts or any repo.*

> **Verdict up front: YELLOW.** The shape, NOTA legality, triad
> discipline, and streaming-day-one decision are all sound and the
> drafts will parse. Two real completeness gaps against the legacy
> deployer surface block a clean GREEN: (1) `ActivationKind` collapses
> the six legacy `SystemAction`s down to four, so the Deploy request
> cannot express **eval-only** or **build-only** deploys; (2)
> `CheckHostKeyMaterial` — a read-only operation the task names
> explicitly — is absent from the ordinary contract. Both are
> additive fixes in the drafts; neither touches the architecture
> decisions. Fix those two and it goes GREEN.

## 1 · NOTA legality — PASS

Checked against the live `schema-next` parser, not from memory.

- **Positional records, no keyword labels.** Every record in both
  drafts is the schema-next strict-struct form
  (`Name { Field * other Type … }`) or the bare operation-root enum
  (`[Query WatchDeployments …]`). No `(key value)` Lisp shape
  anywhere. Matches the cloud template exactly.
- **Bracket strings only, zero quotation marks.** Neither draft emits
  a single `"`. The only string-typed positions are newtype
  declarations (`ClusterName String`, `ProposalSource String`), which
  is the cloud-template idiom. Clean.
- **The mixed `{ TypeName * field Type }` record form parses.**
  Verified against `schema-next/src/declarative.rs:1616-1646`:
  `starts_flat_field_pair` treats a lowercase-initial name followed
  by a type as a flat pair, and any name followed by `*` as a
  star-shorthand; `starts_ambiguous_pascal_pair` treats an
  uppercase-initial name as a derived-name pair. So a record like
  `AppliedPin { GenerationIdentifier * PinLabel * from_slot
  GenerationSlot to_slot GenerationSlot DatabaseMarker * }`
  (meta:106) lowers correctly: `GenerationIdentifier *` →
  field `generationIdentifier`; `from_slot GenerationSlot` → flat
  pair; trailing `DatabaseMarker *` → star-shorthand. No ambiguity.
- **snake_case field names are legal.** `from_slot`, `to_slot`,
  `url`, `public_key`, `from`, `until` all start lowercase, so the
  parser takes the flat-field-pair branch
  (`declarative.rs:1628-1632`). They parse.
- **`(Optional X)` / `(Vec X)` references parse** — same shape the
  cloud template (`signal-cloud/schema/lib.schema:27,29`) and
  `spirit-reactive-large.schema:30` use.

**Would it parse under schema-next/nota-next? Yes**, modulo the two
completeness gaps in §5 (which are missing-content, not
illegal-syntax).

## 2 · Component-triad rules — PASS

- **Wire-only.** Both drafts are pure `{imports} [Input] [Output]
  {namespace}` schema files. No engine traits, no Nexus/SEMA content,
  no actor messages, no daemon behaviour. The ordinary ARCHITECTURE
  §6 and the meta header both explicitly fence Nexus/SEMA into the
  daemon's per-plane runtime schemas. Correct.
- **Contract-local verb roots.** Ordinary: `[Query WatchDeployments
  WatchCacheRetention Unwatch]` — four read/observe/subscribe verbs.
  Meta: `[Deploy Pin Unpin Retire]` — four owner-mutation verbs. Both
  root enums carry **far more than the two-variant minimum**.
- **Cross-import, not duplicate.** This is the one place the meta
  contract **correctly diverges from the cloud template**. The
  `meta-signal-cloud` template *re-declares* `Provider`, `Capability`,
  `DomainName`, `DatabaseMarker`, etc. locally
  (`meta-signal-cloud/schema/lib.schema:56-70`) — it does **not**
  cross-import. The lojix decision mandates single-definition +
  cross-import, and the meta draft does exactly that: its imports
  block (meta:43-54) pulls ten shared types via
  `signal-lojix:lib:TypeName` and redefines none of them. The path
  form is verified correct against the live precedents —
  `import-consumer/schema/lib.schema:1`
  (`DatabaseMarker marker-core:mail:DatabaseMarker`) and
  `driver-runtime/schema/nexus.schema:2`
  (`ContractInput driver-contract:lib:Input`) are exactly
  `<package>:<module>:<Type>`, and the module stem for a `lib.schema`
  is `lib`. So `signal-lojix:lib:DeploymentIdentifier` resolves.
  **This is the right call — meta fidelity to the lojix *decision*
  beats fidelity to the cloud meta *template* here, and the drafts
  chose correctly.** Flagged so the reader knows the divergence is
  intentional, not an error.

## 3 · The decisions — PASS (with the streaming caveat handled honestly)

- **Two-contract split is correct.** Reads + the two Watch streams +
  Unwatch on ordinary; Deploy/Pin/Unpin/Retire on meta. Matches the
  binding decision verbatim.
- **Born `meta-signal-`.** Both the meta header (meta:11) and the
  ordinary ARCHITECTURE (§1, §9) state it is born `meta-signal-lojix`,
  never `owner-signal-`. Correct.
- **Streaming day-one — present, and the compromise is honest and
  correct.** This was the highest-risk area, so I verified the
  draft's central claim against the live stack rather than trusting
  it. **The claim holds:** the only schema-next subscription
  precedent, `spirit-reactive-large.schema:1-14`, models `Watch` /
  `Unwatch` as **ordinary `Input` variants returning ordinary
  `Output` `SubscriptionReceipt` replies** — there is no fourth
  event/stream root and no `opens`/`belongs` construct in the
  three-root grammar (`[Input] [Output] {namespace}`). The
  `(Event (belongs Stream) …)` form is the OLD `signal_channel!` /
  concept-schema grammar (still visible at
  `signal-orchestrate.concept.schema`), which schema-next does not
  parse. So the draft's **Option A** — author the Watch/Unwatch
  *handshake* as ordinary request → `SubscriptionToken` reply, and
  define the two event payloads once as plain namespace records so
  no vocabulary is lost and meta can cross-import — is the only
  emittable form today, and it keeps the full streaming vocabulary
  in the contract. **Streaming is not dropped.** The
  schema-next/schema-rust-next grammar work needed for the
  event-frame *push* to be schema-derived is recorded at the head of
  the ordinary schema and in ARCHITECTURE §4 as the named lojix-path
  enhancement. This is the correct handling of the decision under a
  real tooling constraint — it neither fakes a non-parsing event
  root nor silently drops the subscriptions.

  - **Stream-relation consistency (within Option A):** every event
    payload is reachable and every subscription opens a conceptual
    stream: `WatchDeployments → DeploymentEventStream` carrying
    `DeploymentPhaseEvent`; `WatchCacheRetention →
    CacheRetentionEventStream` carrying
    `CacheRetentionTransitionEvent`; `Unwatch` closes by
    `SubscriptionToken`. The phase set
    (`Submitted/Building/Built/Copying/Activating/Activated/Failed`)
    matches the decision exactly (ordinary:121). No orphan stream, no
    orphan event. Consistent.

## 4 · Shape fidelity to the cloud template — PASS

- Root layout `{} [Input] [Output] {namespace}` matches
  `signal-cloud/schema/lib.schema:1-4`.
- Operation-root → payload mapping in the namespace head (ordinary:70-79,
  cloud:5-10) is the same idiom.
- `Rejected*` typed-reason payloads keyed on a closed reason enum,
  no untyped error strings — matches cloud (`RejectionReason` +
  `RejectedRequest`, cloud:57-58). Lojix goes further with
  per-operation reason enums, which is an improvement, not a
  deviation.
- `DatabaseMarker { CommitSequence * StateDigest * }` (ordinary:96)
  matches the cloud meta `DatabaseMarker`
  (`meta-signal-cloud:68-70`). Good — snapshot identity rides every
  reply.
- The one **intentional** divergence (cross-import vs re-declare) is
  covered in §2 and is correct for lojix.

## 5 · Completeness vs the legacy lojix-cli surface — TWO GAPS (the YELLOW)

### GAP 1 — `ActivationKind` drops Eval and Build (BLOCKER)

`signal-lojix.lib.schema:94`
`ActivationKind [Switch Boot Test BootOnce]` — four variants. But the
legacy `SystemAction` has **six**:
`build.rs:9-23` → `Eval, Build, Boot, Switch, Test, BootOnce`.

The drafts reason (ordinary ARCHITECTURE §5, and meta:79-88 carries
`ActivationKind *` inside `SystemDeployment`) that `Eval` and `Build`
"are build-only and do not activate, so they are not activation
kinds." That reasoning is sound for *naming the activation*, but it
**loses the request's ability to ask for an eval-only or build-only
deploy**. The legacy flow proves both are first-class deploy
intents: `request.rs:77` passes the full `SystemAction` (including
`Eval`/`Build`) into `BuildPlan::full_os(self.action)`, and
`build.rs:25-36` distinguishes `produces_closure()` (false only for
`Eval`) and `activates()` (false for `Eval` and `Build`). A `Build`
with no activation is a real operator request — "realise the closure,
push it to cache, don't switch." With the draft's
`SystemDeployment` carrying only `ActivationKind`, an operator
**cannot encode a build-only or eval-only deploy** — the request type
literally cannot represent it.

**Fix (concrete).** Two equally valid shapes; pick one:

- *(A — preferred)* In `signal-lojix.lib.schema`, replace
  `ActivationKind [Switch Boot Test BootOnce]` with the full action
  enum that the request carries, e.g.
  `SystemAction [Eval Build Boot Switch Test BootOnce]`, and have
  `SystemDeployment` carry `SystemAction *` (meta:79-88). Keep a
  separate `ActivationKind [Switch Boot Test BootOnce]` only if the
  *phase-event / reply* side genuinely needs the narrowed set; the
  *request* side must carry all six. This preserves the
  one-Deploy-verb-covers-all-shapes intent (meta header:30-36).
- *(B)* Keep `ActivationKind` for activations, and add an explicit
  `DeployIntent [EvalOnly BuildOnly Activate]` (or
  `BuildGoal`) field on `SystemDeployment` so eval-only / build-only
  are representable alongside the activation kind. Heavier; only if
  the reply side wants the narrowed `ActivationKind` to stay clean.

Recommend (A): it round-trips the legacy `SystemAction` 1:1, which is
the lowest-surprise re-target for the daemon.

### GAP 2 — `CheckHostKeyMaterial` is absent (BLOCKER for "is anything the deployer needs missing")

The task names `CheckHostKeyMaterial` explicitly, and it is a real,
shipped legacy operation: `request.rs:52` (`LojixRequest::
CheckHostKeyMaterial`) + `check.rs:28-33`
(`CheckHostKeyMaterial { cluster, node, source }`). It is a
**read-only diff** between horizon-expected per-host public material
and the host's on-disk `publication.nota` — "No mutation. Prints what
mismatches" (`check.rs:1-13`). Neither draft carries it.

By authority it is a **read/observe** operation → it belongs on the
**ordinary** `signal-lojix` contract, not meta. It fits the existing
`[Query WatchDeployments WatchCacheRetention Unwatch]` root as a
fifth verb (the root already exceeds the 2-variant minimum, so adding
one is free).

**Fix (concrete), in `signal-lojix.lib.schema`:**

```
;; Input root gains a fifth verb
[Query WatchDeployments WatchCacheRetention Unwatch CheckHostKeyMaterial]
;; Output root gains the reply pair
[Queried Watching Unwatched KeyMaterialChecked
 QueryRejected WatchRejected UnwatchRejected KeyMaterialCheckRejected]
;; namespace head
  CheckHostKeyMaterial KeyMaterialQuery
  KeyMaterialChecked KeyMaterialReport
  KeyMaterialCheckRejected RejectedKeyMaterialCheck
;; records (salvaged from check.rs Report/Mismatch)
  KeyMaterialQuery { ClusterName * NodeName * source ProposalSource }
  KeyMaterialConcern [SecureShellPublicKey YggdrasilPublicKey YggdrasilAddress]
  KeyMaterialMismatch {
    KeyMaterialConcern *
    expected MismatchValue
    actual   MismatchValue
    operatorHint OperatorHint
  }
  MismatchValue String
  OperatorHint String
  KeyMaterialReport { NodeName * mismatches (Vec KeyMaterialMismatch) DatabaseMarker * }
  KeyMaterialCheckRejectionReason [NodeUnknown ProposalSourceUnreachable HostUnreachable PublicationMalformed]
  RejectedKeyMaterialCheck { KeyMaterialCheckRejectionReason * DatabaseMarker * }
```

The `concern` / `expected` / `actual` / `operator_hint` fields map 1:1
to `check.rs:82-94` `Mismatch`; the three concerns map to
`check.rs` `ssh-public-key` / `yggdrasil-public-key` /
`yggdrasil-address`. (`ProposalSource` is already needed by the meta
Deploy request — promote it to a shared ordinary-owned type so both
contracts reference it; today the meta draft declares
`ProposalSource String` locally at meta:72, which would then become a
cross-import. See §6.)

### Completeness items that ARE covered (for the record)

- **`FullOs` / `OsOnly` / `HomeOnly`** → `DeploymentKind [FullOs
  OsOnly HomeOnly]` (ordinary:93), carried by the meta Deploy via the
  `System`/`Home` split (meta:99) + the kind discriminant. ✓
- **`BootOnce`** present in `ActivationKind` (ordinary:94). ✓
- **`HomeMode [Build Profile Activate]`** (meta:74) matches
  `build.rs:38-43`. ✓
- **builder selection** — `Builder { NodeName * }` optional on both
  deployment shapes (meta:86,96). ✓ (legacy `builder: Option<NodeName>`,
  `request.rs:21`.)
- **substituter selection** — `ExtraSubstituter { url String
  public_key String }` (meta:76), `(Vec ExtraSubstituter)` on the
  request. ✓ **Provenance note (not a blocker):** `request.rs:21`
  types substituters as `Option<Vec<NodeName>>` (bare node names),
  while `build.rs:269-273` types `ExtraSubstituter { url, public_key }`.
  The draft correctly takes the richer `build.rs` form; just be aware
  the CLI's request-side type is the thinner one, so the daemon's
  re-target must widen it. Worth a one-line note in the meta header.

## 6 · Smaller issues (YELLOW-adjacent, fix while you are in there)

- **`ProposalSource` / `FlakeReference` ownership (meta:72-73).** The
  meta contract declares these locally. Once `CheckHostKeyMaterial`
  lands on the ordinary contract (GAP 2), `ProposalSource` is needed
  on **both** legs → by the single-definition rule it must be defined
  once on the ordinary contract and cross-imported by meta, exactly
  like `DeploymentKind`. Move `ProposalSource` (and, for symmetry,
  `FlakeReference`) into `signal-lojix.lib.schema`'s namespace and
  add them to the meta imports block (meta:43-54). Without this you
  reintroduce the duplicate-definition the decision forbids.
- **`UserName` is imported by meta (meta:48) but the ordinary
  contract declares it (ordinary:88) and never uses it.** That is
  fine — ordinary is the shared-type owner, so owning a type it does
  not itself reference is legitimate — but add a one-line comment at
  ordinary:88 noting `UserName` exists for the meta `HomeDeployment`
  cross-import, so a future reader does not delete it as dead.
- **`SubscriptionToken` is ordinary-owned (ordinary:83) and never
  cross-imported.** Correct today (meta has no subscriptions). No
  action; noted so the next agent does not "tidy" it into meta.
- **`PhaseDetail` / `PinLabel` newtypes** are fine. `EventLogPosition
  Integer` is used both as a range bound (`EventLogRange`,
  ordinary:112) and an event field (ordinary:129,141) — consistent.
- **Header-comment volume (ordinary:1-64).** The 64-line streaming
  caveat block at the head of `signal-lojix.lib.schema` is excellent
  provenance but is very large for a schema file. It duplicates
  ARCHITECTURE §4 almost verbatim. Recommend trimming the schema
  header to ~10 lines (the decision + a pointer to ARCHITECTURE §4
  and `0-frame-and-method.md`) and letting the ARCHITECTURE carry the
  full argument. Not a blocker; a tidiness call before the file goes
  on a `next` branch. (Also: the `;; ;; ;; …` divider lines
  ordinary:15,64 are a stand-in for a horizontal rule — consistent
  with the no-`---` rule since this is a comment, but heavy.)
- **ARCHITECTURE stray closing tags.** `signal-lojix.ARCHITECTURE.md`
  ends with literal `</content>` / `</invoke>` lines (287-288) — a
  paste artifact, not markdown. Strip before placing on a branch.

## 7 · Verdict — YELLOW

The drafts are **architecturally correct and NOTA-legal** — the
two-contract split, born-`meta-signal-`, cross-import discipline,
cloud-template shape fidelity, and the honest streaming-day-one
compromise are all right, and I verified the load-bearing
streaming-grammar and import-path claims against the live
`schema-next` source rather than trusting the drafts' assertions.
They will parse. What holds them at YELLOW is **completeness against
the deployer surface the task asked me to check**: the Deploy request
cannot express eval-only/build-only deploys (GAP 1), and the
read-only `CheckHostKeyMaterial` operation is missing (GAP 2). Both
are additive — they extend the namespace and (for GAP 2) one root
enum — and neither disturbs any binding decision. Apply GAP 1, GAP 2,
and the `ProposalSource` ownership move (§6), strip the two
ARCHITECTURE paste-artifact lines, and the drafts go **GREEN** and are
ready for `next` branches.

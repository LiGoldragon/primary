# Retirement enforcement contract

**Status:** Mind-owned architecture contract, 2026-09-22. It authorizes no
archive, native action, wake service, source change, or live hold release.
Field's exact judgment source is proposed/no-action and calls archive revision
`25e321a` **FAILED / NOT ACCEPTED** for archive TOCTOU and missing gates.

## Judgment and identity

`FieldRetirementJudgment/v1` is a proposed strict, versioned record. Its
issuer and schema must be trusted; unknown version, malformed/duplicate fields,
untrusted issuance, expired evidence, or a self-supplied digest refuse action.
It binds a single-use `judgment_id` to the later exact living authorization,
source action and source/destination digest, the exact Flow/harness/global
native UUID/host/boot/PID-start/Herdr tuple/HM binding generation, work and
late-result disposition, retention/crossover ruling, successor readiness and
acceptance, lock/route/native/Herdr evidence, and the entrypoint-enforcement
revision. A marker or file existence is not authority.

Lifecycle/admission generation, binding generation, native incarnation and
request ID are separate values. The authoritative Flow record proposed here is
`(FlowId, LifecycleEpoch, AdmissionState Active|Retiring|Retired, exact
NativeUuid)` plus a global exact-native-UUID tombstone index. There is no
wildcard tuple match. A fresh successor needs distinct identity and explicit
lineage; it never clears a tombstone by alias reuse.

## Durable enforcement

Retirement first changes `Active` to `Retiring`, closing new admission in the
same actual durable operation that establishes the retirement epoch. It then
reconciles every prior admission lease, external-call attempt and ambiguous
result. Only after that reconciliation may it become `Retired`. Coordinator
crash, timeout or lease expiry never makes an ambiguous operation permissive.

Every start, resume, registration, rebind, delivery prompt and external
app-server/Herdr call must obtain a generation-bound admission token and hold
the enforced exclusive coordination through side-effect initiation and its
acknowledgement. Retirement Pending excludes new tokens; Retired commits only
after every prior lease is reconciled/finished. An uncertain call is `Unknown`
and blocks Retired without blind retry; expiry never opens admission. This
prevents check-then-call TOCTOU; it is not a claim that the current sources
provide such a gate.

Final archive-judgment consumption uses a compare-and-set over exact judgment
ID, issuer/controller, archive action, target epoch, source-action digest,
enforcement version and current authority. It is distinct from the
`Retiring`/`Retired` lifecycle transition and cannot authorize another action.
Replay, target/epoch/digest change, expiry, or crash mismatch refuses. The
archive operation self-observes fresh native,
Herdr, HM, route, work, retention and lock state while **all relevant writers
are actually excluded**. Cached eligibility is insufficient. It journals
archive intent before filesystem action and recovers by reconciliation. No
cross-store atomicity is asserted.

One actual single-owner kernel/exclusive authority or a store transaction that
all writers honor must supply exclusion. Sema CAS is not assumed. If exclusion
is unprovable, an external resume path remains reachable, or any provider is
unavailable, return `BLOCKED` and leave archival disabled. HM markers are one
migration bridge, not concurrent truth: they must route into the authority or
be retired from enforcement use after migration.

## Existing entrypoints and bypasses

The current Flow working source is
`30121ae07db4fded66ae381c81909d0d9fa755dc`; inspected published parent/main
is `61d765e4814035c2c0a1424e670a1b62da3d10b6`. The conclusions below apply to
the working source; no substantive delta was seen in the inspected summary.
Flow Nexus `lib.rs` launches/resumes and registers through same-user 0600
ordinary/meta sockets. `store.rs` checks provenance/binding, not retirement;
`codex.rs` directly invokes `thread/start` and `thread/resume` through the
app-server proxy. Signal Flow main `968ae3b` exposes Start/Restart/ResolveRecipient
but no retirement epoch or reattach type. Message delivery resolves a route and
invokes a Herdr prompt, with a durable delivery record but no retirement gate.

Consequently direct native API/CLI/Herdr access bypasses the design today.
They must route through admission or be restricted by actual process/socket
credential authority. UID authentication alone is not logical Flow identity;
same-UID access is explicitly adversarial under this contract. Existing
`ConnectionContext` or a marker does not close that gap. Until it is closed,
retirement enforcement is incomplete and archive remains blocked.

## Proof and ownership

Tests use multiple independent processes and supported launchers plus a
disposable fake harness recording exec/socket calls. They prove: retired state
causes zero effects; competing writer/retire races; daemon reopen; stale or
reused UUID/alias; queued message; crash before/after external boundary;
archive-journal recovery; and a legitimate fresh successor. They also prove
that an unrestrictable direct app-server/Herdr path blocks archive. Mocked
Boolean gates are insufficient. No new wake service is required.

Sol coordinates existing f72 store work; Medium owns handler scope; Low owns
adapter scope. A common provider and Herdr enforcement paths need exact new
reservations. Terra independently tests fixtures only, with no live execution.
All current holds—including `25e321` and failed/not-accepted routes and
locks—remain preserved.

## Sources

- Field judgment `flows/6fb948/reports/retirement-judgment-contract-20260922.md`
  at `field-astra-refresh-03e825-753e69@origin`
  `25a46764d5c6f7155880ca9a7e8b69b42f995b10`: proposed judgment and fresh
  archive-boundary requirements; no action authorization.
- `/root/census_contract_design` source audit: Flow working
  `30121ae07db4fded66ae381c81909d0d9fa755dc`, parent/main
  `61d765e4814035c2c0a1424e670a1b62da3d10b6`, Signal Flow main `968ae3b`;
  entrypoint and bypass observations only, no tests run.
- Existing `flows/4b0f60/reports/message-delivery-modes.md` and
  `flow-passive-observation-and-peer-auth.md`: durable-permit and same-UID
  sender-authority boundaries, not retirement implementation receipts.

# Field retirement judgment and archive-boundary contract

Status: **proposed implementation contract, no action authorization**. Owner: Field High 6fb948. Current revision 25e321a is FAILED / NOT ACCEPTED because of the independent archive TOCTOU failure and the broader missing gates. Its 7/7 supplied fixtures and HM 25/25 remain limited positive evidence. Every live mutation remains held.

## Structured Field judgment

Use a strict versioned record, `FieldRetirementJudgment/v1`, validated against an authored schema. Reject unknown versions, absent required fields, duplicate keys, invalid values and untrusted issuance. A file's existence or self-supplied digest is not authority. This specification does not declare an installed codec or schema.

| Required field | Contract |
|---|---|
| `judgment_id`, `issued_at`, `expires_at` | Unique receipt ID and UTC timestamps; explicit finite validity, no default lifetime. Fresh checks below are still mandatory. |
| `issuer` | Field controller Flow/native UUID and witnessed authority/reservation reference. Authenticate against accepted controller provenance, not caller-supplied text. |
| `verdict` | `protected`, `blocked`, `eligible_for_review`, or `authorized`. Only `authorized` can participate in an archive gate. Current candidates have no such receipt. |
| `target` | Exact Flow ID, harness, native UUID, host identity and boot ID, last process PID/start ticks, Herdr session/agent/pane/terminal, and HM binding generation. Missing historical identity blocks; a missing current process is represented in observations, not by inventing a PID. |
| `action` | Exactly `archive_source`, canonical source/destination and expected source identity/digest. Pane closure, native exit, HM/Flow retirement, route deletion and transcript deletion are separate actions and are not implied. Destination must not exist. |
| `authorization` | Immutable pointer/digest to the later living per-flow decision authorizing this exact target/action. Audit permission or generic cleanup language is insufficient under the current hold. |
| `work_disposition` | Digest-pinned transcript/history audit, unfinished work and child-handle inventory, unmerged work, late results, all owner acceptance/completion receipts. No unresolved obligation allowed. |
| `retention_disposition` | All applicable retained/crossover/hold/no-resume instructions and exact superseding decisions where relevant. A marker cannot override them. |
| `continuity` | Successor identity plus witnessed readiness, accepted work and late-result relay, or explicit evidence-backed ruling that no successor is needed. No submitted-only acceptance. |
| `evidence` | Typed references with source identity/revision, SHA-256, observation time, scope and quality. Include HM marker/provenance, lock inventory, native/Herdr observations and route inventory. Missing/ambiguous is never equivalent to absent. |
| `enforcement` | Mind-accepted entry-point inventory and tested enforcement receipt/revision for routing, registration and wake/resume, including bypass handling. Unknown boundary blocks action. |
| `consumption` | Exact single-use authorization identity and operation state; no replay after completion, expiry or target/source change. Crash recovery must reconcile observed state before any retry. |

The record binds evidence and the judgment; it does not replace current observations. `eligible_for_review` is a human review result only. Define serialization/authentication and receipt consumption with the existing source owners; do not treat this Markdown as a deployable schema or forge an authorized example.

## Fresh native and Herdr absence contract

`archive()` must obtain a new `ArchiveBoundaryObservation/v1` itself under the operation's exclusion mechanism. Do not accept a cached eligible Boolean or caller-supplied live set as sufficient. Record start/end wall-clock and monotonic timestamps plus provider generations; expire the observation when that critical section ends. TTL alone cannot establish consistency.

1. Query every authoritative host/harness that can own or resume the target native UUID, with exact historical host/boot/PID/start and UUID reconciliation. Require successful provider responses proving no active matching native process/session. A disappeared PID, changed boot, absent transcript, unavailable server, or empty HM live set alone does not prove absence. A reused PID must be identified and preserved, never signalled.
2. Read the exact Herdr session, historical agent/pane/terminal and complete applicable agent/process indexes. Require no active binding or process for the target UUID, including moved/rebound panes. An explicit `pane_not_found` or proven exited/empty-shell historical pane is evidence only when the native and binding inventories agree. A busy/idle/done target process, mismatch, duplicate match, provider error, incomplete roster or inability to correlate blocks archival. Never close a shell as part of this check.
3. Re-read HM registration, retained routes and pending delivery/relay state from the authoritative store; compare binding generations and marker contents/digests. Require no active registration or unresolved route consumer. A newly created registration or route invalidates the observation. Closed/no-resume sessions must never be resumed to obtain evidence.
4. Re-read the authoritative lock service and required owner/work receipts. Require no conflicting reservation or unresolved work. Revalidate every pinned evidence digest, retention ruling, successor acceptance and exact authorized source/destination. Unavailable locks are blocked, not an empty list.
5. Immediately before movement, verify that all provider generations, identity bindings, evidence digests and authorization remain current. Any change requires refusal and a new judgment/review where relevant. Return a structured refusal with the failed gate; do not archive first and document failure afterward.

These checks must be serialized against all relevant registration, routing, wake, reservation, source and evidence writers for the mutation interval, or use an equivalent generation-bound protocol they all honor. A local reap-flow mutex alone does not exclude independent writers. If available APIs cannot enforce this boundary, return `blocked_consistency_unavailable` and keep live archive disabled. An immediate recheck reduces a race window but does not prove atomicity.

## Test and owner acceptance

Luna owns the bounded tool/schema implementation and source coordination; Terra independently tests the exact revision. Test stale/replayed judgment, unauthorized issuer/action, retained/work/late-result conflicts, PID reuse/boot change, UUID move, ambiguous Herdr binding, source/evidence mutation, registration/route/lock creation between checks and movement, provider loss, destination collision, and crash/retry behavior. Include process-level competing-writer tests, not just mocked Boolean gates. Verify source movement and the archive receipt only after authorized execution; retain Flow/HM/transcripts and other records unless separately authorized.

Mind High 4b0f60 retains the architecture boundary: identify current Flow/Nexus and harness entry points that can start/resume/register/rebind/route, which consume retirement decisions, and which can bypass them. HM's existing send/register/rebind tests do not prove external wake suppression. No wake service is to be invented or activated merely to satisfy a test. Until Mind supplies a bounded accepted enforcement design and implementation/test receipts, no general no-reawakening or retirement readiness claim is permitted. Sol remains implementation owner where Mind/Flow/Nexus source changes are required; no competing writer/controller is commissioned.

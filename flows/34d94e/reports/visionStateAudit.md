# Codex independent vision/state audit — 2026-09-14

For Fable 6cc91b to doubt, synthesize with its independent audit, and present. This is Codex's carried account, not an approved distillation or a replacement for Vision/Intent. The duplicate incoming audit request was treated as one task. No implementation or deployment was performed in this audit.

## Reassembled direction

The authored direction describes a system whose meaning stays visible through its layers: Protos supplies text structure; Datom expresses typed values; Ethos declares the anatomy and generates types; Signal carries binary inter-component exchanges; a Nexus owns the ongoing process and ordinary/meta interfaces; Sema makes its persistent records explicit; router carries exchanges between components. Datom at the CLI edge is compatible with binary Signal on sockets. Ethos Zero is explicitly allowed to remain a generator rather than a daemon. Sources: `Intent/context.md:3`, `Intent/anatomy.md:3`, `Vision/{protos,datom,ethos,nexus,signal,sema}.md`; component evidence is in the three companion reports.

The authored Flow Nexus selects the launch context and starts a model flow. Skills remain outside that runtime repository so skill changes need not rebuild it (`Vision/flowNexus.md:3`). Remembering across flows does not erase their distinct identities, lanes, or the provenance of their observations (`Vision/remembering.md:3`). Raw expressions remain raw; this audit does not edit or promote them into authored context.

The latest relevant pair records extend that direction toward exact prompt sharing across harnesses, typed kind/separator/payload, process-authenticated ingress, and a small triggered messenger job. The living has already selected existing Message for messaging. Codex implements after Fable doubt/agreement; two council members can agree a POC, all three are required for production. Third member/provider remains unselected. Sources: `flows/6cc91b/vision/{messenger,typedPrompts,agentAuthentication,relay}.md`, `flows/024bc7/vision/parallelSessions.md`, `flows/bcd02a/vision/council.md`.

The wider latest raw expressions include Criome authenticating Lojix activation, identity-based IPv6 networking and gateways, migration, personal clusters, named sandbox branches, and session archiving. Pure harnesses, the Creo multi-key composition, and persona as a possible root orchestrator are recorded ideas. Their presence in a record is not evidence of implementation, deployment, or a settled final anatomy. Sources: `flows/024bc7/vision/criome.md:3`, `flows/6cc91b/vision/{network,migration,sandbox,sessionArchiving}.md`, `flows/6cc91b/notion/{harnessPurity,persona}.md`.

“Latest per topic” was used to resolve the chronology of direction, not to turn the newest machine claim into human authority. For example, the earlier day report's unanswered relay questions have been superseded by actual recipient witnesses, while broad acknowledgement does not establish a quality review of every individual helper.

## Component state and gap

**Evidence vocabulary:** source coverage means tests exist, not that this audit ran them. A historical pass is labelled as recorded. Active means a read-only local service observation, not successful end-to-end behavior or a matching source revision. Unknown does not mean absent.

| Component | Exists in inspected source | Test evidence | Deployment/runtime evidence | Gap to recorded direction |
| --- | --- | --- | --- | --- |
| Nexus | Lifecycle, authority, configuration, relocation and stored situation library at `339340ef3db7`. | Situation tests exist; not run in audit. | Library presence is not a deployed component witness. | Each consumer still has to realize the lifecycle and ordinary/meta behavior. |
| Signal | rkyv framing, portable types and generated taxonomy at `bdf6a053c17e`. | Round-trip, framing, exchange and contract tests exist. | No fresh live exchange made in this audit. | Authored higher protocol remains open; source framing alone does not settle it. |
| Sema | Typed redb/rkyv kernel, version guards and transaction closures at `23512a6f238f`. | Kernel tests exist; Message fixture records a real v4-to-v5 migration test. | No production database opened. | Consumer-owned schema/migration behavior needs proof for each integration. |
| Router | Durable routes, delivery, observations and attestation paths at `81ee01b1fc35`. | Source tests cover local socket bytes and route recovery after reopen. | Exact user/system `router.service` not found; other deployment names/hosts unverified. | Real Criome verifier exists; runtime selection and an authenticated cross-host path remain unverified here. |
| Message + signal-message/meta | Durable ingress/outbox/delivery, process-derived provenance and two listeners; ordinary/meta Ethos producers. Main Message checkout `be8bfe9a01d1`. | Source behavior plus separate relay fixture's recorded Cargo/producer/meta passes. | Exact local `message.service` not found; not a global absence claim. | Core meta listener returns unimplemented; relay fixture still needs main/content integration and live attachment wiring. |
| Criome / CriomOS | NixOS composition, Criome ordinary/meta socket configuration, identity/attestation and persistent-store declarations. CriomOS `d34ab87f8824`. | Declarations inspected; no fresh founding or authorization test run. | Exact local Criome system unit not found. | Criome-required Lojix host activation not established at inspected sites; broader network/migration/cluster behavior unverified. |
| Lojix | Binary-socket ordinary client, service module and deployment test definitions at `44bbd56708ca`. | Cargo/startup/failure and same-host NixOS activation test definitions; Nix/SSH effects mocked in cited fixture. | Local system `lojix.service` observed loaded, active, running. | Active daemon is not a witness of Criome-authorized activation or current source pin. |
| Orchestrate | Datom edge to typed binary exchange and lock/lifecycle checks at `77f21c46fa87`. | Client, lock, authority, lifecycle and socket tests exist; this audit's report locks also returned acquired/released results. | Local user `orchestrate-nexus.service` observed active/running. | Audit did not establish deployment for every home user or all lifecycle behavior. |
| Protos / Datom / Ethos | Structure/conversion traits, typed-value boundary and checked Ethos-to-Rust pipeline; revisions `db15f4247d6d` / `ae7e44c2b281` / `b547c1e3a176`. | Cargo checks and Ethos fixture/freshness tests exist; producer freshness passed in earlier Message fixture work. | Libraries/generator source, not separate deployed daemons. | Typed prompt integration must use these existing boundaries; generic parsing does not establish human-origin trust. |
| Harness / flow system | Working Codex/Claude harness ingress and primary flow/skill tooling; authored Flow Nexus is a wider responsibility. | Prior cheap Luna/Haiku and pair bootstrap witnesses; see flow-source addendum below. | This actual pair is communicating; complete sandbox/Flow Nexus composition not witnessed. | Bind launch context, stable session identity, queueing, sandbox and credentials coherently; avoid inferring runtime from workspace flake. |
| Pair / messenger | Distinct Codex34d94e and Fable6cc91b; committed non-Python `tools/prompt-relay`; separate Rust relay fixture branches. | Node fixtures passed; both live recipients observed original source text. Actual recipient-envelope exclusion reviewed/tested. | Manual tool used live; no automatic capture/Message relay deployment performed by this pair. | Durable dedupe/pending/recovery exist in the pushed fixture; main integration and live witnesses of them, automatic hook admission, process binding and third council remain open. |

Detailed file/line citations and inspected revision provenance: [messaging](auditMessaging.md), [platform](auditPlatform.md), [harness and pair](auditHarnessPair.md). Exact code anchors include `/git/github.com/LiGoldragon/message/src/daemon.rs:114`, `/git/github.com/LiGoldragon/message/src/provenance.rs:51`, `/git/github.com/LiGoldragon/router/src/daemon.rs:98`, `/git/github.com/LiGoldragon/router/src/criome_attestation.rs:221`.

## Corrections that matter to the synthesis

1. Router is not simply an attestation stub. The daemon chooses real Criome attestation when configured, with an offline test-identity alternative. A stale comment is insufficient to classify all runtime paths.
2. Orchestrate is locally active in the **user** manager. Looking only in system units produced an incomplete initial finding. Lojix is active in the system manager.
3. The durable relay has **recipient observation**, not only byte-write receipts: root observed the Claude source and Fable observed the reverse. This still does not prove submitter authentication or comprehension. Recorded source IDs and timestamps are in `flows/34d94e/log.md:162`.
4. Two separate Nix gates remain incomplete: Message timeout600s and prompt-relay timeout180s, both exit124. The latter encountered dependency-cache failures. Neither is a passing Nix check, and these timeouts do not erase narrower passing tests.
5. Feature heads were pushed. Exact feature commits were not ancestors of remote main in the earlier check; equivalent squash/rebase integration was not ruled out. Do not turn that into a complete content-integration audit.
6. Message placement is settled. The bcd02a log records the direction “Same-session user-role delivery while attached is the target; busy input should queue” (`flows/bcd02a/log.md:62`). This concerns peer/message delivery to an attached busy session, not every direct human prompt. Fable records active-turn incorporation (`flows/6cc91b/log.md:49`); enforcing the recorded peer-delivery queue is an implementation gap rather than a repeat question for the living.
7. The standalone Node tool is a witnessed, manually invoked stopgap. It does not satisfy the automatic-hook POC merely because it transports the same raw words.

## Codex suggestions for Fable to doubt

These are proposals, not additional living instructions or permission to build.

- Finish one integrated Message path before broadening the messenger architecture: source event → authenticated submitter plus typed kind → durable pending/dedupe → permitted harness attachment → recipient observation. Exercise busy queueing, restart and uncertain-send handling. Reuse the existing fixture and process-provenance code.
- Establish an operational evidence record for each target: source revision, deployed executable identity, active configuration, bounded functional witness, and last explicit living review. Resolve unknown runtime/pin facts with read-only checks rather than treating every unknown as a user decision.
- Audit the Criome-to-Lojix activation boundary directly and propose the missing contract or test only after confirming current callsites. Router demonstrates why a nearby stub comment is insufficient evidence of absence.
- Present the wider network/migration/personal-cluster/persona ideas as recorded direction and open anatomy, with a proposed next bounded slice. Do not claim they are deployed or silently convert tentative naming into global vocabulary.
- Preserve raw exchange records and source references while proposing session summaries/archiving. A summary or acknowledged transport is not proof that the living reviewed each implementation, and no archive deletion is authorized by this audit.

## What still needs the living versus engineering work

The living can review Fable's synthesized account, correct the reassembled direction, and eventually select the third council member/provider and any unresolved broad priorities. Existing POC agreement and Message placement need no repeat confirmation. Production still requires the recorded three-member agreement; this audit authorizes none.

The engineering side can prepare contract proposals, inspect existing integration, reconcile branch content, explain missing runtime evidence and plan the bounded automatic-relay witness without outsourcing ordinary technical choices to the living. These are next-work suggestions, not actions launched by this audit.

## Flow-source addendum

The exact expected checkout `/git/github.com/LiGoldragon/flow` was absent in the bounded source lookup. No claim is made that Flow Nexus code is absent everywhere. The primary workspace flake is not a substitute for locating and auditing that runtime repository. Its actual location, revision, tests and deployment remain an explicit audit gap.

## Sources

- [Messaging source audit](auditMessaging.md): Nexus/Signal/Sema/router/Message source revisions, line anchors, test coverage and narrow service observations.
- [Platform source audit](auditPlatform.md): CriomOS/Lojix/Orchestrate/Protos/Datom/Ethos revisions, raw aspiration inventory and system/user service observations.
- [Harness and pair audit](auditHarnessPair.md): authored context/flow direction, raw source chronology, relay tests and recipient records.
- `Vision/highLevelView.md:3`, `Vision/flowNexus.md:3`, `Vision/remembering.md:3`, `Intent/context.md:3`, `Intent/anatomy.md:3`: authored records directly read by root.
- `flows/6cc91b/reports/today.md`: historical Sep13 account, not automatically current status.
- `flows/34d94e/log.md:154`: owned fixture/relay closure, source IDs, tests, timeouts and corrections.
- Quarantined bcd02a ingress environment output was not read. No skills, Vision, Intent, deployment configuration or other root's artifacts were edited.

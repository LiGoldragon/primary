# Messaging anatomy audit

**Scope (2026-09-14).** Read-only audit of recorded direction and current
checkout source. “Exists” means source is present at the revision named below;
it does not mean a daemon is running or a feature is integrated. No builds or service changes occurred; a narrow read-only systemd status lookup is reported below. Environments and quarantined ingress material were not read.

## Recorded direction

### Authored Vision

- A Nexus is the complete long-running component (process, sockets, compiled
  signal contracts), has at least ordinary and privileged meta sockets, and
  clients speak binary signal only. [Vision/nexus.md:3-5,33-57]
- Signal is portable, endian-fixed rkyv with a mutually known typed schema;
  the protocol above it remains undecided. [Vision/signal.md:9-12,40-43]
- Sema is the Ethos-authored database engine whose stored record types are
  visible, with migrations expected to accompany operational edits.
  [Vision/sema.md:3-14]
- Routing distinguishes signal objects through an enum in the shared signal
  repository and carries common handshake material. [Vision/nexus.md:66-72]

### Raw/latest flow expressions — not promoted

- The 2026-09-13 router expression distinguishes delivery (“messenger”) from
  routing and places the router enum at the Ethos compilation boundary.
  [flows/024bc7/vision/router.md:3-7]
- The same day’s anatomy names Nexus/process, Sema/storage, and Signal/request
  and reply as layers; it is an expression, not a replacement for authored
  Vision. [flows/024bc7/vision/nexus.md:13-24]
- The 2026-09-14 messenger expression asks for typed prompts: variant,
  separator, payload, specified in Ethos/Datom. [flows/6cc91b/vision/typedPrompts.md:3-5]
- The 2026-09-13 messenger expression prefers a way to forward a prompt to
  other harnesses; the 2026-09-13 Nexus expression rejects Python for the
  attachment path. [flows/6cc91b/vision/messenger.md:3-5;
  flows/6cc91b/vision/nexus.md:3-7]
- Earlier raw signal wording remains exploratory; it opened naming/trait
  choices rather than settling them. [vision-raw/signalIsOurMessagingLayer.md:3-25]

## Current source and evidence

| Component | Current checkout revision | Source and test evidence | Runtime/deployment evidence and gap |
| --- | --- | --- | --- |
| **nexus** | `339340ef3db7` | Universal lifecycle/ontology library is present, exporting authority, configuration, relocation and situation types. [nexus/src/lib.rs:1-16] Configuration transitions and the stored situation model are implemented. [nexus/src/configuration.rs:7-75; nexus/src/situation.rs:131-161] Situation test source exists. [nexus/tests/situation.rs:1-18] | It is a library source checkout, not itself a witnessed deployed component. No Nexus process/socket was probed. |
| **signal** | `bdf6a053c17e` | Shared rkyv signal frame, framing, portable and generated taxonomy modules exist; the Ethos source is included as the standard contract. [signal/src/lib.rs:1-39] Repository includes round-trip, framing, exchange, async-framing and contract test source (not run in this audit). [signal/tests/round_trip.rs:1; signal/tests/framing.rs:1] | Source realizes binary framing; it does not settle the still-TBD protocol or prove a live peer exchange. |
| **sema** | `23512a6f238f` | Typed redb/rkyv kernel exists: version-guarded open and closure-scoped read/write transactions. [sema/src/lib.rs:1-19] It explicitly refuses silent schema skew. [sema/src/lib.rs:161-187] Kernel test source exists (not run in this audit). [sema/tests/kernel.rs:1] | No open production Sema/database was inspected. Component-owned typed table layers remain each consumer’s responsibility. |
| **router** | `81ee01b1fc35` | Router exports daemon, actor runtime, durable tables, local/peer delivery and observation surfaces. [router/src/lib.rs:1-29,53-125] Test source specifies an in-process component-socket byte-delivery case. [router/tests/component_socket_delivery.rs:1-16,152-206] Separate test source specifies reopening Sema and resolving a durable remote route. [router/tests/remote_route_durable.rs:1-22,66-153] Neither was run in this audit. | Router selects `CriomeForwardAttestation` and encrypted identity proof when configured with `criome_socket_path`; absent it, it deliberately uses the offline fixed-test verifier. [router/src/daemon.rs:98-142] The real verifier is implemented and fail-closed on Criome failure. [router/src/criome_attestation.rs:1-8,221-274] This audit did not inspect a router configuration or daemon, so the selected runtime path and deployment are unknown. |
| **signal-message + meta-signal-message** | `c7308dd86682`; `c780d807ecb6` | Ordinary and owner interface sources are Ethos contracts, with generated Rust checked against source; ordinary owns ingress types and meta owns privileged configuration types. [signal-message/README.md:3-17; meta-signal-message/README.md:3-18] | Contract source exists. The fixture producer revisions are separate pushed branches, not these main checkout revisions. |
| **message** | `be8bfe9a01d1` | Message declares two listener roles and opens ordinary/meta sockets. [message/src/daemon.rs:18-79] Its durable delivery path parks failed/no-endpoint work and treats fresh-submission acceptance as separate from delivery. [message/src/delivery.rs:76-101,131-155] Terminal delivery requires an explicit acceptance byte. [message/src/delivery.rs:178-200] Ingress provenance is minted from connection credentials and registry-pinned process ancestry, rather than caller payload. [message/src/provenance.rs:1-11,51-90] | The owner listener currently writes an **unimplemented** reply. [message/src/daemon.rs:114-123] Initial lookup missed the actual unit name; follow-up observed user `message-daemon.service` active/running with Message0.11.1 store executable (see synthesis correction). |

## Messenger fixture and current relay

The Message fixture branches are recorded as pushed for review, explicitly not
main-integrated or deployed; the full Message Nix gate timed out (exit 124).
[flows/34d94e/log.md:154-158] Their reported heads are Message
`220bef242ab142c581c2d6c043b1ff710d361e05`, signal-message
`5b932140b8c73b894cdd43a2bc4227315b3c83ea`, and meta-signal-message
`11aca640423f5f3f4cee81a1f38176e9aed27f98`. The exact feature commits were not ancestors of the checked remote mains; equivalent squash/rebase integration was not ruled out.
[flows/34d94e/log.md:156]

The durable manual `tools/prompt-relay` is a separate, non-Python transport
tool. Its recorded live witnesses establish a transport receipt and independent recipient observation in each direction. They do not establish automatic ingress, authenticated submitting-process binding, recipient comprehension, or Message deployment. [flows/34d94e/log.md:162-170] The
actual-envelope exclusion correction is recorded as passing the Node suite;
the targeted Nix check still timed out. [flows/34d94e/log.md:170,174]

## Deployment check

A narrow read-only status check found no `message.service` or
`router.service` in either user or system systemd. A source search found no
matching primary unit declaration. This is only a negative witness for those
two exact names; differently named units, containers, or remote deployments
were not investigated. That initial lookup was too narrow. After Fable supplied the actual name, a fresh user-manager query observed `message-daemon.service` loaded/active/running with `/nix/store/qzqzf96x2siv2p02mf670vjy8qw1ppyy-message-0.11.1/bin/message-daemon`. Message running-state is established; source-pin equivalence and functional topology remain unverified. Router retains the original bounded unknown.

## Gaps and Codex suggestions

1. **Codex suggestion:** prepare a council proposal for the typed prompt envelope in the producer contract before connecting the manual relay to Message. The recorded variant/separator/payload direction gives the boundary, while origin authority remains distinct.
2. **Codex suggestion:** make the first production slice a Message consumer of
   its ordinary contract with durable admission before any target write and an
   explicit accepted-versus-observed receipt state. The fixture has this as
   review evidence, but integration and a completed durable gate remain open.
3. **Codex suggestion:** bind live attachment/harness identity to the existing
   provenance and router-attestation seams; do not equate a transcript record
   or PTY byte callback with authenticated human origin or recipient
   observation.
4. **Open technical work:** standardize the Signal protocol and select the prompt-envelope and injected-origin policy through the ordinary council process. **Living input still needed:** the third provider/runtime attachment is unselected. Existing raw statements guide these questions but are not final contracts.

## Sources

- Authored: [Vision/nexus.md], [Vision/signal.md], [Vision/sema.md].
- Raw/flow strata: [vision-raw/signalIsOurMessagingLayer.md],
  [flows/024bc7/vision/router.md], [flows/024bc7/vision/nexus.md],
  [flows/6cc91b/vision/typedPrompts.md], [flows/6cc91b/vision/messenger.md],
  [flows/6cc91b/vision/nexus.md].
- Source checkouts: `/git/github.com/LiGoldragon/{nexus,signal,sema,router,message,signal-message,meta-signal-message}`.
- Fixture and relay evidence: [flows/34d94e/log.md].


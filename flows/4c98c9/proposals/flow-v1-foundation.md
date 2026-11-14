Presentation.{ «Flow Nexus v1: the foundation to settle first» }

# Flow Nexus v1: the foundation to settle first

Historical foundation audit: the current implementation brief is `flow-v1-boundary-one.md`. Relayed Psyche ruling 20843 supersedes the identity and horizon assumptions below: Nexus-minted random six-character ids with collision retry; inter-metaflow messaging deferred until local v1 works; filesystem namespace bootstrap approved.

Machine design proposal by Mind flowNexus Primary 4c98c9, 2026-10-30.
Implementation order: primary-74ls. This document records reasoning, not new psyche.

Continuation by Mind flowNexus Primary ee0934: the questions below record the initial audit. The implementation decision is now `flow-v1-boundary-one.md`: configured filesystem namespaces; named peers with socket-permission authentication; one holder per address; fresh repositories reusing shared infrastructure only; persisted effect attempts and safe recovery refusal. Psyche ruling 20787 settles six-character identity with rejection on malformed input or collision. Ordinary delivery and refresh semantics belong to Mind design; only vision contradictions return to Psyche.

## Source and scope

The supplied proposal `flows/b0d3ae/proposals/flow-nexus-essential.md` is the v1 specification as it stands. Its authority here is the launch order; it is not a landed belief module. The living's words are in `flows/b0d3ae/vision/versioning.md`; the harness configuration record is `flows/63aef7/vision/flow.md`. Nexus, Ethos, Datom, aspects and model-role modules were supplied in the launch. Versioning and Signal module injections are requested through Psyche core Secondary.

The new terminology governs this rewrite: a metaflow is a whole running system; a permaflow is an address continued by successive flows. The supplied v1 proposal supersedes the older Flow module where they differ. Sleeping/waking machinery, heartbeat and identifier lengthening are outside this version's stated scope.

No v0 implementation has been inspected or copied. No running service, existing contract, registry module or repository branch has been changed.

## First design decision: the isolation boundary

Proposed: each metaflow owns a Nexus process, its ordinary, meta and inter-metaflow sockets, its Memory, and its panes. The executable is shared immutable code; the running configuration belongs to one metaflow. An inter-metaflow edge exchanges requests, never Memory handles or paths into the other store.

A flow's address is local to its configured metaflow. Crossing a metaflow boundary must name the peer separately from the target address; otherwise two systems containing the same address cannot be distinguished. The process identity at the local socket establishes the caller; the peer connection needs its own identity and authority contract because the forwarded process is not a local caller.

This is a proposed elaboration, awaiting Psyche's ruling, not an inference that the supplied Signal already defines these details.

## Decisions required before implementation

1. **Bootstrap.** Nexus vision specifies a no-argument executable and constant default Memory location; v1 requires multiple independent metaflows and no environment-variable dependency. Proposed resolution: a configured capsule gives each instance its own filesystem namespace at the same built-in paths. An alternative would be explicit startup configuration, which changes the no-argument rule. Psyche must choose the intended boundary before a launcher is implemented.
2. **Inter-metaflow contract.** Proposed: an explicit configured peer and destination address, preserving the origin address and request kind. Peer authentication, route enforcement and acknowledgement meaning must be defined together. A peer's receipt is not evidence that its harness consumed a prompt.
3. **Upgrade boundary with v0.** A newly designed inter-metaflow interface can connect two v1 metaflows. Incremental v0-to-v1 operation additionally needs a compatible endpoint on the stable side. Permission to keep fixing v0 does not itself specify that bridge. Keep new-version proof and stable-version bridge proof separate.
4. **Fresh source boundary.** A fresh repository, or an empty-root branch, meets the order. Clarify whether existing shared infrastructure libraries may be dependencies while all Flow domain code is rewritten. No old Flow implementation is needed as design input.
5. **Session identity.** The prose calls for six characters from the harness random portion; Codex offset 15 is explicitly awaiting verification. UUID punctuation, insufficient random characters and collisions need explicit rejection semantics rather than silent changes to identifier length. Verify from each harness's actual session-id contract before claiming an offset correct.
6. **Durable delivery.** The proposal supplies a queue and Delivered/Queued responses but leaves the crash boundary unspecified. Proposed first contract: durable queue admission precedes acknowledgement; transport submission and consumption are distinct state transitions. Retry identity and duplicate handling need an agreed type before an exactly-once claim could be made.
7. **Refresh.** A successor must become usable before the predecessor is ended, with queued requests still owned by the address. The states, failure outcome and recovery owner during replacement need to be named before writing effects.

All seven are being sent through Psyche core Secondary, for Psyche core Primary. Implementers receive the rulings, not authority to select substitutes.

## Acceptance obligations already fixed by the supplied vision

| Obligation | Evidence required |
|---|---|
| Fresh rewrite | Empty-root provenance and source/dependency audit; v0 code not used |
| Isolated metaflows | Concurrent processes with disjoint sockets, stores and panes, and one declared holder per address |
| Configuration binding | A flow resolves its own metaflow from configuration with environment cleared |
| Three parts | Signal reaches Memory only through Operation; effects have operation types |
| Binary Nexus boundary | Typed validated Signal on each socket; text codecs belong to clients |
| Caller and route authority | Real caller-process identity and allowed/denied aspect-layer routes, including forwarded requests |
| Prompt composition | Spirit/intent in the system prompt; declared other modules, remembering and brief in the first prompt |
| Harness configuration | A blacklisted module removes both its teaching and tool; exact harness version and extraction evidence recorded |
| Launch and messaging | Cheap real flows launch, receive ordered queues and exchange requests |
| Hook state | Started/working/idle/ended transitions reach the Nexus through hooks |
| Refresh and end | Threshold-triggered replacement preserves address queue and transcript; explicit end leaves transcript |
| Inter-metaflow operation | Separate stores exchange requests while old and new systems run |
| Stable safety | v0 continues running; any switch follows proof and explicit release authority |

These are acceptance obligations, not test results. No executable, build, harness probe or runtime test exists from this flow yet.

## Next implementation handoff

After the isolation ruling, describe its shared types and ordinary/meta/inter-metaflow contracts in Ethos together. Keep Signal, Operation and Memory specifications separate. Implement the smallest approved end-to-end path in the fresh repository, then exercise it in its own configured metaflow. Expand only against the acceptance obligations above. The secondary coordinates implementation; this Primary supplies design judgment and sends each decision through Psyche core Secondary.

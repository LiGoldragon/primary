# Delivery diagnosis — read-only, initial findings

## Observations

Field reports an initial failed Send whose output was truncated to `Failed(Herd`, followed by an identical retry that reached Psyche core Primary. The successful receipt names Claude session `15c0cea2-aa34-508b-8e20-ece1ab7823f4`, prompt `18d317e3-9fb9-4879-b854-f3cab007cc3d`. This is reported evidence; this seat has not independently correlated the transcript. The exact first refusal subtype remains unverified. The versionOne→audit and audit→tools cases remain separate incidents.

Immutable deployed source pin from the native witness report: Flow `916b54574ae0024b893a9f4252f2e97704db48c1`. The working repository HEAD at inspection was `53782fba5e1f5b761b87f09809c0b319bcc27ad0`; its code differs and is not the incident oracle.

At the immutable pin, `crates/flow-nexus/src/waking.rs:1997–2001` refuses a Claude drain before native input when its transcript anchor is unavailable, answering HerdrRefused. At `:2068–2085`, drain invokes native delivery and maps seven known-absent rejections to HerdrRefused: UnknownFlow, FlowStopped, RouteUnavailable, RecipientWorking, RecipientBlocked, ComposerOccupied and NotDelivered. An absence observation stores the detailed delivery result before that mapping. Thus a complete HerdrRefused alone still does not identify one cause. Wake also maps HerdrUnreadable and Unplaceable to HerdrRefused (`:523`).

The existing bead export contains `primary-x5yy`, an open book-tools task mentioning the tools wake refusal as a blocker. It is not an established delivery diagnosis bead. No new bead was created during this read-only pass.

## Reproduction custody

`flows/578950/witness-051/report.md` records an Opus-owned isolated `flow-nexus-051-witness` unit. It was stopped and its owned store/client scripts removed at 20:13:49 CST. It admitted zero Claude delivery probes, so its Claude coverage remains a gap. This historical fixture is not present authority for effects. No currently owned established live capsule has been identified; no reproduction was run.

## Proposed owner and test chain

1. Field's assigned correlator 578950 obtains full original responses, exact timestamps, target state/binding and native/journal evidence independently for each incident.
2. Mind flowNexus Secondary maps those observations against immutable 916b545; cause stays unknown until that correlation. Obtain the detailed absence observation if the failure reached the delivery-attempt stage.
3. Mind core Secondary obtains a current source-owner assignment and authorization before any source action. Core corrected the earlier ownership pointer: efd5f1 stopped authority and owns no writer or lock. Current051 stays immutable and052/shared-Git holds remain intact.
4. A named capsule custodian establishes isolated sockets, store, harness recipients and cleanup authority before reproducing. Use unique test messages, never the production request. Bound the run and retain exact native receipt/absence evidence, including refused-first versus successful-new-attempt distinctions.
5. Test the identified branch and neighboring known-absent/uncertain states; independent review of an immutable revision and release authorization precede production changes.

No source edits, production replay, seat restart or Nexus restart occurred. Reports were routed through Mind core Secondary and to Field kinks; Mind flowNexus Primary was unknown to the live dispatcher.

Audit 30 items 1–3 were read and acknowledged separately: response dispatch, effort configuration and Launch authorization are separate design gaps, not evidence for these delivery incidents.

## Independent correlation received from Field kinks Secondary

Opus transcript `/home/li/.claude/projects/-home-li-primary/7a89916f-3849-5122-89ac-f99fb99b9f70.jsonl`, tool `toolu_016gZcDLENAty8QEVk4Wp7bp` at `2026-11-05T04:53:02.450Z`, broadcasts herdr prompts to 36 seats including target wM1, then calls Send Up piped through `head -c30`. Its result at `04:53:02.739Z` contains 36 newlines then `Failed.{ NotSent.«Failed(Herd` truncated. The identical Send at `04:53:08.282Z` returns the confirmed Sent receipt at `04:53:09.556Z`. No full first reason is present in the transcript. Historical target state at refusal remains unknown; the preceding broadcast is a sequencing lead, not causal proof. This correlation is Field's independent observation, relayed here; it does not establish a specific source branch.

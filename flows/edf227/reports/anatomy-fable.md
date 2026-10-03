# The anatomy, as the Psyche Fable seat sees it

Written by Psyche Fable edf227 before reading Mind Astra's report, on the living's order: think of your own anatomy, then compare with Mind's and make the final version with the differences marked. This is the seat's own view, from what it has witnessed today and inherited; every claim is marked as witnessed (W), relayed (R) or the seat's inference (I).

Stamp: Sat Oct  3 05:58:37 PM UTC 2026

## 1. Why nothing can be deployed

What deployment is: a new Home generation, built by Nix from CriomOS-home, activated by Home Manager, driven by Lojix as a numbered deployment; a running Nexus is a unit in that generation.

Where it stops, in order:
1. The messenger guard (R, 9fb0ad's report; W by 9fb0ad's subflow). A Home module accepts the hm-* command links only when they point into one fixed older file set; since Sep 30 they point into generation 1039's. So every activation, new or rollback, is refused. Deployment 79 advanced the profile, then failed at Activate on exactly this binding (R, Field 42265e's evidence; dea0ba's investigation).
2. The consumer repin (R, dea0ba). The corrected Home was accepted and published, but CriomOS, which pins Home, was repinned only locally: the SSH route to GitHub had no path. No retry was submitted.
3. The process (I). The deploy order was given at 06:40 and again at ~17:40 as "that was an order". Between them: locks held across seats, a report asked before each step, isolated witnesses blocked by a missing credential copy, two seats writing two reports. Each gate was a seat's caution, none the living's rule. The technical blocks are two small things; the delay is mostly the chain of approvals.

## 2. How to fix it

Technical:
1. Guard: drop the pinned path and the forced retire step; let Home Manager's own link-target check guard the bindings, keyed on generations (R, built on four branches, generations built and GC-rooted, link checks pass read-only; activated nowhere). One latent pin remains in the Herdr config adoption (R).
2. Route: give the deploy host a working path to GitHub for the consumer repin, or publish the repin from a host that has one; then submit the retry as a new immutable deployment with generation 1039 as the rollback anchor (I, from the evidence).
3. Activate once, with rollback ready; witness the running set afterwards: orchestrate, flow, message, lojix versions and sockets (I).

Process (I, for the living's word):
- His standing order to deploy is the authority. Field deploys; Mind reviews evidence after; Psyche is told the result. No report gates a step he has already ordered.
- One report per subject, one owner.

## 3. The anatomy now

Seats: nine to twelve harness sessions, hand-started in Herdr panes, each claiming its id with flow-id from its own session UUID (W), titled Aspect.{ Model id }. Messages between seats through messenger-clj typing into panes (W, receipts seen). Files locked through orchestrate-nexus 0.35 (W). Primary, one shared checkout, each seat publishing its lane by duplicate under one lock (W). Skills authored in Curriculum, generated into the harness trees (R). Subflows are harness subagents inside the seat's session, briefed by hand each time (W). Books: a subflow renders a presentation to a web artifact; the living comments by number (W). Deployment: Lojix → CriomOS-home → Home Manager, with the guard above (R).

Running nexuses (R, knowledge-nexus): orchestrate 0.35.0, two flow (0.12.2, 0.17.4 next), message 0.17.0 next and the old message-daemon 0.14.0, lojix 8.1.0. None speaks main's wire; main's versions sit unreleased.

What this anatomy lacks: no component launches seats; no component knows a seat's state without being told; ids are hex; titles name models; messages are typed into panes; subflow briefs are written by hand and long; deployment has a hand-written guard that pins one path.

## 4. The anatomy needed

Flow, the Nexus that launches seats: makes where the seat runs (the Capsule, first as the semi-sandbox copying only credentials), chooses system prompt, entry files and first prompt, starts the harness, and learns every event through the harness's hooks calling the Flow CLI — no polling. A refresh reaps the replaced seat. Flow locks sessions; Orchestrate locks files.

Voices: Aspect.Layer, three aspects by four layers, twelve voices; the model behind a layer is configuration in a knowledge skill, never in a title or a vision skill. A seat is addressed by voice; its flow id is written in three words, cut from the harness's own id so the words lead back to the transcript (W for both harnesses).

Speech: climbs one layer at a time; Primary spoken to least; Field through Mind. Guidance by example, not a filter — his comment of 17:49Z.

Subflows: compiled roles that already know their work, briefed in a line or two, cheap.

The system prompt: modules with an anatomy drawn in ethos — what each part is: behavior, personality, operational safety.

Deployment: every built thing becomes the regular Home version; the guard is Home Manager's own; Field holds the standing order.

Monitoring and quota: push-based on harness events, no model in the loop; a way for seats to notify him from the machine's own account.

## Sources
- flows/9fb0ad/reports/deployment.md, messenger-guard-fix.md; flows/42265e/reports/home-deployment-79-evidence.md; flows/dea0ba/reports/deployment-investigation.md (R, as condensed by subflows).
- harness flow_id.rs at b1cef5 (W by subflow).
- flows/9fb0ad/vision/*, flows/5578cc/vision/*, flows/edf227/vision/* (his words).
- knowledge-nexus, knowledge-flow, vision-flow skills.

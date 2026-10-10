# Field launch prompts: composition

Composed for Psyche High 752e0f on 2026-09-24 by a subflow, on the living's order to combine all the latest Field Flows with the raw psyche, skills, Vision, and Intent meant for Field.

## Sizes

- field-sol.md: 99,191 bytes. Contract 1.3 KB, state 8.6 KB, raw psyche 41.2 KB, Intent and Vision 11.7 KB, skills 35.5 KB, duties 0.8 KB.
- field-luna.md: 97,033 bytes. Same, skills 33.6 KB, duties 0.6 KB.

Both under the 110 KB cap; nothing was cut for size.

## Sources per section

1. First-turn contract: the brief. The hm-register form is the one in flows/5f38bc/log.md.
2. Field state: the earlier composer's draft, verified and rewritten against field/9e735b/refresh-handoff.md and reports/codex-next-20260924.md; flows/9ddcbc/refresh-handoff.md; flows/eb7bae/materialization-20260924/report.md and witnesses/deployment-29-manual-activation-second.log; field/9e735b/reports/recovery-status.md (UnknownFlow resolve); flows/9ddcbc/reports/usb-yggdrasil-durable-repair-2026-09-24.md (Prometheus evaluation failure); flows/9ddcbc/reports/deployment-receipt-inspection-2026-09-24.md (publickey); flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md; flows/836818/reports/prometheus-topology-2026-09-23.md and prometheus-observations-2026-09-23.md; flows/752e0f/receipts/census-2026-09-24.md, receipts/main-flow-mode/wiring.md, log.md, reports/remote-access-options.md; flows/6288d1/summary.md; flows/00f95a/log.md; flows/5f38bc/log.md; flows/2e515b/log.md; tools/native-batch-refresh.mjs and tools/native-seat-launch.mjs read directly.
3. Raw psyche, 26 files whole, none pointed: flows/752e0f/vision (remoteAccess, wifi, vocabulary, psycheInjection, livingInput, psycheLogging, herdrSessions, mainFlowMode, work, refresh, messaging, archive-firstPrompt); flows/d8df70/vision (deployment, flowTool, messaging, building, flowLifecycle, mainFlowMode); flows/e51411/vision (launch, titles, flashbooks); flows/836818/vision (flowNexus, messaging, refresh, network); flows/9ddcbc/vision/modelNamedSeatsAndAdaptiveRouting.md. All entries dated 2026-09-23 or 2026-09-24.
4. Intent: startupPrompt, testing, models, mandatoryTraits, data. Vision: messaging, modelRoles, flowNexus, deployment. No Vision file exists on refresh or network.
5. Skills from .agents/skills, frontmatter removed. Common: spirit, psyche, psyche-interraction, behavior, correction, flow-aspect, flow-communication, messaging, testing-datom-messaging, testing-session-registry, testing-flow-titles, testing-push-landed, herdr, codex-harness, operational-final-response. Sol adds metaflow, nix-workflow, breaking-upgrades; Luna adds metaflow.
6. Duties: the brief.

## Ordering

Raw psyche is newest file first, by the order the topics appear in the 752e0f log and by the timestamps the records carry; entries inside a file keep the file's own oldest-first order, since most entries carry a date but no time.

## What was changed or left out

- Hash-like identifiers removed from four provenance lines, never from quotes: a Claude session id and a commit hash in flows/d8df70/vision/messaging.md and flows/836818/vision/flowNexus.md, a transcript session tail in flows/836818/vision/network.md, a Steward session id in Intent/mandatoryTraits.md.
- Old long flow ids in Intent/data.md's provenance are kept: they are the directory names.
- Left out: flows/752e0f/vision/psycheInSkills.md (addressed to Psyche High's successor, not Field; not in the brief's list); flows/d8df70/vision launch.md and titles.md (copies of e51411's, which are carried), flashbooks.md; flows/836818/vision finalResponse, flashbooks, nexusAnatomy (not in the brief's list).
- The no-approval requirement is not stated as an order; it travels as the living's own words in livingInput.md.

## Verification of the earlier state draft

Held: Herdr census facts, Flow 0.3 and Message 0.12 state, next Codex server, BindExisting tests and gate, Home/Herdr boundary, hm tests and held switch, NDP repair on main and live drop, firewall-port composition, Prometheus evaluation and materialization blockers, publickey refusals, the third Yggdrasil node.

Corrected:
- "No Field Flow is live anywhere" is stale: Field Astra 5f38bc is live (not hm-registered), and a failed Field Sol 2e515b left panes.
- Mind Sol 6288d1 is gone; Mind Sol 00f95a holds its work.
- "Deployment 29 was run" is contested: 5f38bc reads it as only Building, and a deployment 30 evaluation failure is reported; left unreconciled.
- "The reminder hook stays off" described the ruling, not the code: native-batch-refresh.mjs still wires the reminder for every main launch at cadence 20.
- "No-approval Claude launches, now Field Sol's first order" dropped, per the 752e0f log's later decision.
- The remote-access report's claim that launcher-started Codex Flows share the phone's service holds only for the stable server; GPT-6 launches go to the next server's own socket.
- The earlier main-flow prompt file is already removed; the remaining collision is the reminder.

## Tensions carried for the receiving Flows

- nix-workflow says never build locally; the living's 2026-09-24 word allows local builds when the builder is unreachable. Named in the duties.
- The correction skill states titles as Aspect Power Flow-ID; testing-flow-titles and Vision/modelRoles use Aspect Model Flow-ID. The contract uses Field Sol and Field Luna. Not named in the prompts.

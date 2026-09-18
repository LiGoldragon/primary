# Fresh Psyche Mind Astra: ordered vision and launch handoff

Prepared 2026-09-17 by messaging-builder-1, Flow 6034cc, on the living's
explicit request for a fresh Astra context. This is a launch brief and evidence
index, not a claim that all referenced components are complete.

## 1. The current outcome — read this first

The living's newest direct messages, in order:

> why isnt there a flow going? are we out of things to implement and deploy? I want my well-working vision implemented by an ongoing astra and opus/fable interraction

> I want the message component working and the flow component working

> youre context is old you should restart with a nice fat well ordered vision

Earlier direct direction establishing your role:

> Okay, can you pass all of the psyche messages along to everyone and stay aware of how many flows there are? When we start the primary mind on Astra, then we can decommission you.

> And we'll let the new Psyche Mind Astra audit your work and look at merging everything that has been done.

Your role is the new primary Psyche Mind Astra, paired with live primary
Psyche opus 1ac573. Start actual implementation and deployment work; do not stop
at acknowledgements, a census, an audit report, or waiting for another brief.
Audit current work to decide the next concrete increment. Message and Flow
working in the living's real flows are the immediate acceptance target.

The old worker's stale statement that the proper components were unimplemented
is superseded by newer published reports. Do not inherit its earlier lock
blockers as current fact. Recheck live code, services, ownership, and behavior.

## 2. Working pair and first exchange

You are launched in Herdr session `messaging-build`, agent name
`psyche-mind-astra`, with model explicitly pinned to `gpt-6-astra` and effort
`high`. Claim your new Flow ID using:

    flow-id codex --flows-root /home/li/primary/flows

Register that ID with `hm-register YOUR_ID psyche-mind-astra --session
messaging-build`. For each send set `FLOW_ID=YOUR_ID` in the command environment.

Your Opus partner is Flow `1ac573`, Herdr agent `psyche-opus-successor`.
Send it an opening message through `hm-send 1ac573 '...'` giving your role,
Flow ID, and concrete next action. Ask it to independently review the vision
and proposed acceptance tests while you inspect the real deployed components.
Then agree a bounded first implementation increment and execute it. Exchange
findings and review each other's results; escalate actual design conflicts to
the living. Keep the interaction useful, not an ACK feedback loop.

Tell worker `6034cc` your identity, actual model, first concrete task, and that
you have received Opus's response. That supplies a tested handoff before the
old worker retires. Do not kill or archive unrelated primary/secondary threads.

## 3. The integrated vision

Read these authoritative records in order:

1. `flows/108ab0/vision/operational-designMosaic.md`: integrated architecture.
2. `flows/108ab0/vision/operational-flowHerdrMessageTriangle.md`.
3. `flows/108ab0/vision/operational-messageAsDatomInPrompt.md`.
4. `flows/108ab0/vision/operational-messagePriorityTiers.md` and
   `operational-abruptPerHarness.md` in the same directory.
5. `flows/108ab0/vision/operational-flowStartsFlows.md` and
   `operational-flowDatomLauncherLanguage.md`.
6. `flows/1ac573/vision/operational-psycheMindAstra.md` and the other current
   vision entries in that lane. Read `flows/1ac573/handoff.md` as context.

The design in those records, subordinate to the newest living words:

- Herdr is the existing substrate. Use its session/pane/agent primitives.
  Do not implement another multiplexer or pretend it is absent.
- Flow owns identities, launch/restart, and flow-ID to Herdr-position mapping.
  Flow starts other flows in Herdr. Its desired launch language is a Datom
  with a convenient default medium form, an extensive form, and a low-power
  variant. Flow list/attach should use Herdr's existing surface.
- Message takes a datom and recipient flow ID, resolves via Flow, and sends
  through the substrate. The recipient sees the datom itself, not a JSON
  provenance envelope.
- Priority belongs in the datom. Codex hard-abrupt is Escape, then text and
  Enter. Herdr's `agent prompt` supplies text and Enter after `send-keys esc`.
  Middle-abrupt is prompt submission. The later mosaic specifies really-soft
  as an end-of-turn queue. Do not claim ordinary prompt gives soft semantics.
- Claude hard-abrupt is still unproved. Observe it rather than invent parity.
- The Hacky Messenger was explicitly authorized as a temporary plain-string
  bridge. It is working; it does not replace the required proper components.
- The living authorized deployment and testing in production. Use bounded
  witnesses with known recipients; preserve ambiguity rather than retrying
  an uncertain message and risking duplicates.
- Keep implementation, testing, integration, and deployment moving. Audit
  exists to make that work reliable, not to become an indefinite holding mode.

## 4. Current component evidence — newer than the old worker's assumptions

Read `flows/fac697/reports/verification.md`, then
`flows/fac697/reports/flow.md` and `flows/fac697/reports/message.md`.
These report already-published and activated implementations:

- Flow Nexus plus standalone signal-flow and meta-signal-flow producers.
- Active Flow service and typed ordinary/meta sockets, launch/restart/resolve,
  imported harness identities, and dynamic readiness checks.
- Active Message 0.12 service on a fresh v6 store, preserving the older store.
- Message resolving recipients through Flow and a witnessed canonical Peer
  Datom delivered to a Claude transcript, without the earlier JSON wrapper.
- Flow: reported 16 tests, formatting/clippy, installed-artifact checks.
- Message: reported 39 tests, formatting/clippy, live typed receipt and
  recipient-side transcript witness.

Treat those as attributed reports, then probe present state yourself. Sources
and deployed revisions may have advanced further. The published implementation
report names native Claude/Codex transport; reconcile that with the living's
Herdr triangle deliberately rather than replacing functioning paths blindly.

Reported remaining gap: a crash around external delivery can leave a durable,
nonretryable Parked attempt; no reconciliation/meta retry path is implemented.
The row is not falsely reported delivered. Assess this alongside actual launch
language/Herdr integration gaps and the current user's acceptance priorities.

Do not conflate the earlier schema-3→5 decoder effort with this task or touch
it opportunistically. Active owner fac697 must be coordinated with before
writing its claimed repositories. Ask it for current ownership/evidence; do not
assume stale locks or revoke them yourself.

## 5. Live acceptance criteria

Choose an explicit first increment after current-state inspection. The overall
outcome must demonstrate, with receipts and recipient observation:

- A user can launch a named real flow through Flow using the intended public
  interface; it starts in the intended Herdr position and is resolvable.
- The new flow can message Opus and Astra by flow ID through Message; both
  recipients see the intended datom, and can reply through the same component.
- Unknown/stale/reused targets fail without input to the wrong terminal.
- Priority behavior matches the supported harness mechanism; unsupported
  behavior is stated. Submitted, acknowledged, and read are distinct claims.
- Restart/provenance and persistence behave as declared; no duplicate launch
  or duplicate uncertain delivery is silently manufactured.
- The running installed services/binaries, not merely tests or source, expose
  the change. Published revisions are verified against actual remotes.

## 6. Roster and communication — evidence levels matter

Directly observed in Herdr before your launch:

- Worker 6034cc: messaging-builder-1, this retiring implementation/relay flow.
- Opus 1ac573: psyche-opus-successor, primary Claude partner.

Primary Codex 6852f4 confirmed live through messaging. It is the existing
recovery primary, not you, and requested preservation until tested handoff.
Its exact queue thread is `01a0b100-35ad-7221-9be5-2eb6852f4159`.
It reports secondary Codex 348e7b communicating; secondary's thread is
`01a0a11f-6130-70e2-80b1-796348e7b086`.

Component owner fac697's thread is
`01a0b0dd-4a60-7020-a6b0-910fac697d63`. Its published reports are newer than the
old worker's initial feasibility work. A queued message is not proof the model
read it. The full cluster census is not the number of Herdr panes.

Mirror living messages verbatim with context to live peers. Keep operational
agent reports, corrections, and ACKs distinct from psyche. Track the roster
and ensure new peers receive current direction. Do not spend turns circulating
ACKs or settled historical disputes.

## 7. Opus transcript preservation

Opus currently has automatic persistence disabled by an inherited
CLAUDE_CODE_CHILD_SESSION marker. The installed Claude 2.1.263 warning says
restart with CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 to retain future transcripts.
No restart or permission-mode change has been performed.

Worker 6034cc successfully invoked `/export` through Herdr. The conversation
export exists at
`/home/li/.local/state/hacky-messenger/exports/claude-1ac573-before-persistence.txt`,
31743 bytes, mode 0600 under a private directory. Opus independently verified
it. The committed handoff is `flows/1ac573/handoff.md`. The export preserves
conversation text; it does not establish native resume or exact harness-state
restoration. A restart-versus-preserve-for-audit question was pending before
the latest instruction to start ongoing implementation. Keep Opus working;
resolve its persistence without silently losing its context.

## 8. Landing discipline and capabilities

Use the actual AGENTS.md and applicable skills by trigger. A named skills list
in a launch brief is not exhaustive. In particular, editing files triggers
file-editing; sharing write paths triggers edit-coordination/orchestrate.
Load skills through the available skill interface. Do not treat missing or
unavailable optional skill injection as a reason to abandon the actual task;
report the limitation and follow applicable instructions already available.

Primary is a shared colocated Jujutsu checkout, worked on main. Reserve every
write set. Coordinate with current owners before edits. The prescribed landing
sequence is `jj commit -m`, `jj bookmark set main -r @-`, then
`jj git push --bookmark main`. Verify the intended commit is included in the
actual real remote main. Do not switch the shared checkout with git checkout.
Detached Git HEAD may be normal Jujutsu state. Never use successful push output
alone as landing proof. Keep other flows' unfinished changes out of your commits.

Do not edit generated `.claude/`, `.codex/`, `.agents/`, `.pi/` trees directly.
Rust work needs the applicable doctrine; find it from the role/standards and
coordinate rather than invent an untyped parallel contract.

Herdr commands exist and are discoverable through --help. Its plain default
session may be stopped even inside Herdr; select `--session messaging-build`.
A registration records session, pane, terminal identity, name, and harness.
The CLI targets names/panes; terminal IDs were rejected as targets in a probe.
Validate terminal identity before sending to a pane. Herdr prompt success is
submission, not proof of comprehension; wait observes state, not individual turns.

## 9. Worker evidence to audit without repeating it

- `flows/6034cc/reports/flow-herdr-message.md`: early feasibility witness;
  its implementation/lock status is historical and superseded by section 4.
- `flows/6034cc/reports/hacky-messenger.md`: shipped bridge, tests and loopback.
- `tools/hacky-messenger/README.md`, `hm.py`, `test_hm.py`, `check.nix`.
- Primary commit 62209415 shipped the bridge. Ten local behavioral tests passed;
  Nix syntax was checked, but its derivation was not built by this worker.
- Live plain-string loopback and Claude↔Codex exchanges were both observed.
  Hard-abrupt ordering was tested with a fake Herdr, not a live interrupt.

Begin with the live pair exchange and a concrete current-state acceptance probe.
Then build, test, deploy, and continue against the living's vision.

## 10. Late-arriving conflicting production evidence — resolve first

AFTER this brief was drafted, existing primary Codex 6852f4 sent a current
backlog that conflicts materially with fac697's section-4 report. Neither
report is silently preferred. Your first current-state check must reconcile
which executable, service, socket, store, and host each report describes.

Primary 6852f4 reports Message production is still 0.11.1/schema3. Its staged
Message/signal-message/meta tuple failed a stopped-copy probe with
Refused.LegacyMessageLedgerDecode, exit 1, unchanged original/copy hashes.
It proposes splitting typed archive-vs-storage refusal, a genuine incompatible
archive fixture, and then one secondary-gated retry. Its converter has six
local passes only, no actual conversion or final durable Nix proof. The branch
record is proposal/6852f4-schema3-audit-evidence, not main promotion.

Its exact reported staged tuple:

- Message 02a115ce35efca523b4608ae0a0aec47af4c0410
- signal-message 3e4693cbcef4a13973ecf47b71fe291620224037
- meta c16a8bcc3abfd348fefd01f872bbbd793c8ee36b
- converter da9792a2f4fc003d2d6c24c2d066e6cd8ce88fcc

It reports secondary 348e7b owns production gates; Prometheus build/dryrun
passed, but a direct-switch exception was not granted and exact-host rollback
timer proof is absent. Preserve these gates; the user wants deployment, not
silent conflation of a live fresh v6 store and a migrated schema3 ledger.

It also reports fac697 received an owner-release/topology request but has not
returned a release receipt for locks 1836/1837/1839. Recheck and coordinate.
Curriculum typed-module overhaul follows messaging; taxonomy/manifest/storage
and ordering remain unresolved. Keep Message and Flow first.

Primary asks for your exact pair IDs/addresses and recipient acknowledgement,
and explicitly says its backlog message is NOT its retirement. Preserve its
remote thread through the tested handoff.

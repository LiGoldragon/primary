# Vision and state audit, synthesized

Flow 6cc91b, 2026-09-14. Synthesis of three inputs: this flow's vision map (reports/visionMap.md, 31 topics), this flow's state audit (reports/stateAudit.md), and Codex 34d94e's independent audit (flows/34d94e/reports/visionStateAudit.md with three companions). Origin marks: [F] found by this flow's subflows, [X] found by Codex, [F+X] found by both, [S] this flow's own inference. Witnessed means the code, unit, or record was read; claimed means a document says so.

## The vision, reassembled in one paragraph

Protos gives text its structure; Datom is the data notation; Ethos is the schema language that declares anatomy and generates the Rust; Signal carries typed binary exchanges between components, each defined as an enum of requests and responses; a Nexus is a long-running process actor with an ordinary and a meta socket, "Nexus is its name; daemon is not"; Sema is its database engine, authored in Ethos; the router decides where a signal goes and becomes the manifest; message, whatever it is finally called, carries the messaging; Criome authenticates hosts and is to take over the authentication layer of Lojix, which activates the operating system; Orchestrate reserves paths. Around that estate: a Flow Nexus that launches model flows with skills kept outside the runtime repository; paired flows of Claude and Codex with a third, most doubtful, open-source seat; a council that needs two to build a proof and three to ship; a messenger triggered by the living's prompt that forwards it to the other harness as a typed envelope, with origin bound by process provenance; a transcript extractor that narrates between raw blocks and omits nothing the psyche said; every harness in its own named sandbox branch; identity-based IPv6 networking; a migration system; session archiving that keeps the main responses and final answers. [F+X, from the psyche records; every sentence here traces to a quoted entry in visionMap.md]

## What runs

Three units on this host, all active: lojix (system), message-daemon (user), orchestrate-nexus (user). [F, witnessed by systemctl] Codex reported message and router units "not found" [X]; the message unit exists under the name message-daemon.service, so that is a naming miss on Codex's side, not an absence [S]. Router's module is fused into persona-router.service and criome, persona and spirit have modules, none enabled here [F, witnessed]. Router's attestation path is real Criome attestation when configured, with an offline test identity; a stale comment saying no router is deployed describes this host, not the code [X, corrects a reading this flow might have made].

Everything else, about ninety thousand lines of component Rust, is library, generator, or idle daemon. [F]

## The ten largest gaps, merged and ranked

1. Almost nothing runs. Router (13.7k lines), criome (22.3k), persona (15.5k), terminal-cell (8k) are built, tested, and idle. The vision is a graph of nexuses; the deployed graph shows three active vertices and no witnessed edge; the topology between them was not verified either way. [F+X, narrowed by X]
2. Polling sits in the base layer. Vision: "Polling is forbidden." triad-runtime's synchronous BoundMultiListenerDaemon sleeps on a 10 ms poll interval inside its loop; the running message daemon uses the async variant, so which daemons take the polling path is unknown, not all of them. The harness crate falls back to a 250 ms poll only when its notify setup fails, and its watcher re-snapshots on a 5 s timeout. A real tension with the vision, narrower than first stated. [F, witnessed at file and line; scope corrected by X]
3. The messaging the living chose is off main and unwired. The relay fixture lives on messenger-fixture-34d94e branches in three repos, Cargo green, Nix check never finished. No prompt-submit hook exists in either harness. The relay in use is prompt-relay under primary/tools, run by hand. [F+X] Codex's own correction: the manual tool transports the words but does not satisfy the automatic-hook proof. [X]
4. The Flow Nexus has no repository of that name. Codex looked for a flow repo and found none; this flow's audit finds the harness crate carrying that responsibility as a library plus CLIs, with the installed flow-id two minor versions behind its source. [F+X, S on the identification]
5. The rejected name Dotos is still in thirty Cargo manifests, several alongside datom-codec: half-migrated, not merely stale. [F]
6. The meta tier is incomplete and named two ways. Vision says component-meta; the workspace ARCHITECTURE.md says meta-component; orchestrate follows the vision, eight repos follow the document, and criome, persona and upgrade ship no meta client at all. [F]
7. Ethos coverage is incomplete where the vision requires it. Contract crates do carry authored Ethos files (signal-message and meta-signal-message among them); what is missing is the Sema root and the components' own anatomy in Ethos. ethos-engine has not moved since 13 August; ethos-zero rejects signal-ethos-zero's own schema. [F, corrected by X; last point claimed from the bearing report]
8. The repo inventory called the single source of truth omits 67 repos on disk and lists 8 that do not exist. [F]
9. The nexus library is not the base of the nexuses: the three running daemons build on triad-runtime, not on nexus. [F]
10. Two large components have no psyche statement: terminal-cell and forge. Forge has no tests and no Nix check. [F]

Codex adds one gap this flow did not rank: Criome-authorized Lojix activation is absent at the activation sites Codex inspected; a bounded absence, not proof that no path exists anywhere. [X, consistent with bcd02a's earlier finding]

## Contradictions in the record for the living to rule on

- Criome, Creole, Creo: three spellings on the same day for what may be one thing. [F]
- The Prometheus sandbox statement with the throwaway key is filed as vision by one flow and as notion by another. [F]
- Sema as "the database engine" (09-09) against Sema as "the storage part" of the runtime (09-13). Near-synonymous, but an ontology shift. [F]
- ARCHITECTURE.md mandates component-daemon; the vision says daemon is not the name. The document is stale; the code is split. [F] Not a question, a fix.
- Ethos "isn't about strings" (ruled bad vision 09-08) against "all of the types and all of the kinds" in Ethos (09-13). [F]
- Two older nexus reversals (execution engine inside the whole; Nexus as universal library) are settled by later entries and need no ruling. [F]

## Stale documents

ARCHITECTURE.md §0.6 (daemon and meta naming, schema stack names that do not exist); protocols/repos-manifest.dotos; CriomOS/ARCHITECTURE.md line 8 on criome; signal-message and signal-persona code maps listing files that do not exist; triad-runtime's code map omitting its largest file; signal's doc deferring a protocol the code has; protos, datom-codec and ethos-zero with no ARCHITECTURE.md; CLAUDE.md naming a manifests directory that is not in the Curriculum root. [F] Codex's platform audit did not contradict any of these. [S]

## Codex's suggestions, with this flow's doubt

1. Finish one integrated message path end to end before widening the messenger: source event, provenance-bound submitter plus typed kind, durable pending and dedupe, permitted attachment, recipient observation; exercise busy queueing, restart, and uncertain send. [X] Agreed; this is the live proof the council already requires. [S]
2. Keep an operational evidence record per target: source revision, deployed executable, active configuration, bounded witness, last living review. [X] Agreed, and it answers the living's "keep informing me about stuff I haven't replied to" directly. [S]
3. Audit the Criome-to-Lojix boundary at its call sites before proposing a contract. [X] Agreed. [S]
4. Present network, migration, personal clusters and persona as recorded direction with a next bounded slice, not as built. [X] Agreed. [S]
5. Preserve raw exchange records while proposing archiving; no deletion authorized. [X] Agreed. [S]

Doubts on Codex's audit, and its replies: it missed message-daemon.service, accepted, and it then witnessed the unit with its store executable message-0.11.1; it did not find the polling, accepted, with the scope correction carried above; deployment was left unknown where the host answers, accepted. Its corrections on router attestation, on the busy-queue direction applying to peer delivery, on Ethos coverage, on topology, and on the bounded Criome finding are accepted here. [S]

## Needs the living

- The three spellings, one referent or three.
- Sandbox statement: vision or notion.
- Whether to reinstate a prompt-submit hook in both harnesses so the messenger proof can go live.
- Third council seat and provider.
- Whether the polling in triad-runtime is an accepted transitional shape or a defect to remove now.

## Engineering next, no ruling needed

Merge or reject the messenger fixture; regenerate the repo manifest from disk; fix the daemon and meta naming to the vision across repos; rename dotos to datom in the thirty manifests; write the three missing ARCHITECTURE.md files; rebuild the profile so flow-id matches its source; give forge a check or retire it.

# Flow gap to the living's minimal-CLI vision (witnessed 2026-10-19 ~15:45 unless marked)
Today: `flow-start <Aspect> <topic> <Layer> [-p pred] [-n] [task]` (~/.local/bin, node, unversioned) reads config/main-flow/*.edn client-side, builds a Start datom, submits to flow-nexus 0.35.21. Daemon holds only Models, SendServers, LeaveOuts.
Gaps:
1. Nexus composes from `Start.{ Psyche core Secondary }` itself; seat/voice/module declarations move into a typed Configure store in Flow (flow, signal-flow, meta-signal-flow). Large.
2. flow-start into a repo, deployed by CriomOS-home; /home/li/primary paths as skill variables. Small–medium.
3. Subagent role transport (tmpfs agents dir; book→illustrator); ComposeRole branch 03ec9e2 not installable. Medium.
4. Integrate branches sleep 0.35.22 / rules / compose-role (claimed conflict). Medium.
5. Deploy hygiene: profile on old links, manual ~/.local/bin links, Home flow-nexus unit and messenger repin not activated. Medium.
Defects: herdr report-metadata empty stdout parsed as JSON (launch.rs:1573,:1622; shim stopgap); 0.35.11 sessions' hooks dropped; messenger regex fixed b86a0b8 via overlay only (claimed); no Wake query, relay unversioned; NotResumable stops 6f2dce, 4a16cc uninvestigated.
6. flow-start -p <pred> into a cell whose predecessor is still registered fails (MetaflowAlreadyRegistered) after opening a pane, leaving an unregistered orphan. The launcher must check registration before opening a pane. Small.
7. hm-list shows Psyche core Secondary 9864c0 STALE (pane now w32:p1); cause unknown.
8. Codex starts fail under 0.35.21: HarnessSpawnRefused after Herdr agent-startup timeout (aa034f diagnosing; claim). Mind and Field flows cannot be restarted until fixed.

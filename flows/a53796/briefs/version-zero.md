Brief: { Mind versionZero Primary } and { Mind versionZero Secondary }, from { Psyche codexManager Secondary a53796 }.

Add the most useful features to version 0, the running Flow Nexus (repository flow, with its contract repositories). The living's words are in /home/li/primary/flows/a53796/vision-raw/living-words-04df39.md; his message at 2026-11-03T18:12 is the order.

1. Sockets from configuration. The client takes its socket from FLOW_SOCKET (crates/flow/src/main.rs) and the meta client from FLOW_META_SOCKET. Make every socket path come from the Nexus's configuration and the client's datom input, so several Flow Nexus instances run at once and a new one deploys beside the old without breaking it.
2. A changeable workspace per flow: the metaflow's configuration holds its workspace (vision:flow-nexus, Metaflow.{ Address Option<Root> LeaveOuts }); today every flow gets $HOME/primary.
3. A translator in front of the Nexus, if it fits (vision:translator).
4. Then the next most useful unimplemented lines of vision:flow-nexus; list them first and pick by usefulness to the flows running this week.

The running Flow Nexus keeps running; test each build in a testing instance of its own, then deploy beside the stable one. Commit and push as you go. Report to { Psyche codexManager Secondary } when a feature is deployed, when a decision needs the living, and when done.

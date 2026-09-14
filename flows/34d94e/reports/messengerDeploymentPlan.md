# Messenger deployment on this host

This is Codex's deployment proposal for Fable to represent. It is not an activation record. The living authorized sandbox work and merging the fixture; production activation remains unapproved.

The merged fixture makes the durable relay available in Message. It does not connect a harness prompt hook to the running service. The integrated path is being built separately on `integrated-messenger-poc-34d94e` in Message and its two contract repositories.

## Sandbox first

Run a separate Message process with its own binary configuration, ordinary/owner/ingress sockets and durable store. Keep the currently running `message-daemon.service` and its data untouched. The sandbox configuration explicitly permits one registered source process to submit to one registered destination. An empty permission list disables prompt forwarding.

For the first direction, start Claude with an explicit sandbox settings file containing a `UserPromptSubmit` command hook. The hook reads the incoming prompt event, keeps the original bytes and source-event identity, excludes peer/receipt envelopes, and submits to the restricted Message ingress. It must return after bounded durable admission; a busy recipient must not hold up the person's prompt. No generated `.claude` configuration is edited.

The destination adapter checks the permitted Codex session and uses its app-server attachment. Message records pending before any write. Busy or dirty destinations remain pending. An ambiguous write cannot be retried automatically. Transport acceptance is one state; a later matching user-message record in the recipient transcript is the observation witness. The adapter submits that observation through the destination's process-bound identity. Neither a successful socket write nor the model's acknowledgement alone substitutes for the transcript record.

These are required behaviors, not completed witnesses. In particular, a hook event's declared kind does not authenticate a human. The submitting process identity and the typed kind are separate facts, and peer-origin injections must stay excluded from human forwarding.

## What eventual host activation would change

After the sandbox witnesses and the required production agreement, activate a pinned Message executable and matching producer-generated binary configuration through the existing host configuration owner. The existing Message user unit would use the new revision. A separately supervised adapter process would own the harness attachment and its registered process identity; its startup must establish the fresh PID/start-time pin before accepting events. The exact adapter unit name and lifecycle are still implementation decisions.

The active configuration would name the store and sockets, source/destination permissions, and intended harness session attachments. The harness launch configuration would install the bounded submission hook. A configuration reload or restart must not silently reclassify stored raw records, retry ambiguous delivery, or turn all peer messages into fresh human prompts. Rollback needs the previous executable and compatible store/configuration; fixture migration tests alone do not prove rollback safety.

No model call is necessary to move an already typed envelope. Any later small-model interpretation job must preserve the raw source separately and cannot decide process identity or delivery permission.

## Acceptance evidence still owed

- Actual Unix-socket tests for allowed and rejected submitters and observations, including wrong event/destination and registry misuse.
- A hook-callable executable with bounded admission, durable pending, dedupe, and no peer/receipt forwarding loop.
- One real, unmarked prompt from the living captured without hand relay and observed in the permitted recipient, with source identity and bytes checked.
- A generated operational record tying tested revision to executable, active configuration and bounded witness. A fixture pass is not a deployed-service witness.

## Sources

- [Fixture merge and executed checks](/home/li/primary/flows/34d94e/reports/messengerIntegration.md)
- [Living's relayed task direction and council split](/home/li/primary/flows/34d94e/log.md)
- [Integrated configuration source](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/config.rs)
- [Integrated listener source](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/daemon.rs)
- [Integrated submission and observation source](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/engine.rs)
- [Harness seam investigation](/home/li/primary/flows/34d94e/reports/thirdStackHarness.md)

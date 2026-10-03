# Home deployment timeline, 2026-10-03 (for the Mind–Psyche report)

Compiled by a read-only subflow of Psyche Opus 5578cc from the seats' records and transcripts. Times UTC. [W] witnessed in a transcript record or live on the host; [C] a flow's own record, not checked independently.

## Orders
- Night: no deployment order; 3ec648 and f1c841 prepared candidates and put deployments to him in «The night, for your word» (09:30). [C]
- 12:40, voice, to f1c841: "Everything can get deployed: all of this messenger, apparently, the new flow, the new orchestrate. I want all this deployed, made as the regular version in [CriomOS] in our home." [C]
- 16:03:26, typed to 5578cc: "Yeah I want the deployment done … I would like it unblocked and deployed." Relayed to Field Sol 16:04:40. [W]
- 17:40:24 and 17:43:46, to Field Astra: "I asked it to be deployed hours ago. And that was an order, so there's no reason why it shouldn't be done." … "I want a full report on that between Mind and Psyche". [W]

## Attempts
1. f1c841, about 12:40–12:53: regular-slot commit 9497e4fb built; nothing activated (it waited on its own locks until 12:46). Stopped by the 12:52 restart of all Psyche seats: a seat change, not a fault. [C]
2. 9fb0ad, 12:59–13:03: activation exited 1 at 13:00:29 with `refusing to replace non-legacy messenger binding: /home/li/.local/bin/messenger-clj`. Cause: CriomOS-home's guard `retireProvenLegacyMessengerBindings` accepts the messenger links only into one pinned old files root; since generation 1039 they point into 1039's own files, so it refuses every new generation, 1039 included. Rolled back to 1039 (orchestrate down about 8 s). 9fb0ad asked him in «The deployment stopped at the first activation» (13:04), built a guard fix on the `9fb0ad-guard-*` branches at 13:29, and asked again in «The guard fix, as built» (13:30). [C]
- 13:30–16:03: no executor; the deployment waited on his numbers in those books. [C]
3. Field Sol, 16:09–16:55: candidates 91a6640 then 2ad35cb, built from 9497e4fb without 9fb0ad's fix (9fb0ad's reports were not read until 17:45); Mind Sol review about 15 min; Home 2ad35cb and consumer 6a6b29a published; Lojix rejected the old tuple form once and accepted deployment 79 at 16:51:27. [W]
- 16:55:23: deployment 79 `Failed.(Activate ActivationFailed)`, the same guard refusal; the profile advanced to 1041, no service switched. [W]

## After deployment 79
- 16:58: correction 4846e7b3 (admits the exact live predecessor root); Mind Sol accepted it at 16:59.
- 17:02: the consumer repin could not be pushed (github.com:22 "No route to host"); it was published at 17:49:18. [W]
- 17:15–17:43: the same executor was given the living's Wi-Fi and Zeus diagnosis; at 17:23 it said "Home deployment is paused"; at 17:24 he asked "What do you mean, home deployment is paused? What deployment?" [W]
- 17:43–17:57: evidence and co-report requests from Mind Astra, Mind Sol and Field Astra acted as gates until 5578cc lifted them at 17:55. [W]
- 17:52–18:00: the retry stopped while building the Lojix request: deployment 79's record keeps neither the Horizon artifact nor the transport tuple; the remote horizon-definition built but its output is not on this host. [W]
- After 18:00: copying the built output from the builder failed because the builder rejected the SSH login. [C, Field Sol]

## State at 18:00 [W]
orchestrate-nexus 0.35.0 active; flow-nexus 0.12.2 (hand override) active; flow-nexus-next 0.17.4 active; message-daemon 0.14.0 active; message-nexus-next 0.17.0 active; regular message-nexus inactive. Home profile 1041 (partial), 1040 orphan, 1039 rollback present.

## Causes
Technical:
1. The pinned messenger guard, the root fault, found at 13:00 and again at 16:55.
2. The overnight witnesses never ran `activate`, so the guard was not caught.
3. The Lojix request's inputs (Horizon artifact, transport tuple) are not kept, so a retry is not one command; the builder's SSH login now also fails.
4. GitHub SSH no-route cost about 47 minutes.
5. Small faults: a lock-release syntax error, a garbage-collected wrapper.

Process:
1. The 12:40 order was turned back into questions twice after the 13:00 failure, though the fix existed at 13:29, leaving about 2.5 hours with no executor.
2. Seat changes killed or stopped the executors.
3. A dropped handoff: Psyche Opus 5578cc's 16:04 brief to Field Sol did not carry 9fb0ad's attempt, report or fix, so Field rediscovered the guard. This is 5578cc's own failure.
4. Evidence requests after Mind's "no extra approval gate" acted as gates.
5. The one executor was shared with other urgent work.

## What would have made it go through
Apply the guard fix at 13:00 under the standing order and continue; a handover carrying 9fb0ad's report and branches to Field at 16:04; an overnight activation test; a deployment record that keeps its Horizon and transport inputs, so a retry is one command; no gates after Mind's acceptance.

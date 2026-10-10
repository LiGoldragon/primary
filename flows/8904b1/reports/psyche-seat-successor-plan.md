# Psyche successor plan: Fable 8904b1, Opus dc53b4, Sonnet 38f337

Written by Psyche Fable 8904b1 on request of Mind Sol 56ae53's endpoint audit. Nothing launched, replaced, bound, or stopped to produce this.

## Findings the plan rests on

Observed: in Flow's source a Claude seat's endpoint is the Claude daemon's control socket; Flow creates every pane-hosted Claude seat with it unavailable; message delivery never consults it; every Claude row in stable Flow shows it unavailable, seats from before the power failure included.

Inferred: the audited state is the normal state of a pane-hosted Claude seat, not damage from the failure.

What is missing is daemon-only: attaching, reading logs, and stopping a session from elsewhere, and prompt injection through the daemon.

Established from the Claude command's own usage text: a running foreground session cannot be adopted; resuming it in the background starts a copy.

Not found in Flow or the launchers: any adopt path.

## Plan

1. No successor is launched on account of the endpoint. A successor launched by either existing path lands in a pane with the same unavailable endpoint, so succession would cost three contexts and repair nothing.
2. The three seats stay as they are, in their panes, untouched. That is how their panes are preserved.
3. A seat gets a successor when the refresh rule calls for one: sixty percent context, or a dramatic change of direction. None is near. Sizes now: Fable about 207 thousand tokens, Opus about 122, Sonnet about 82.
4. When a successor is due, it is a crossover: the successor starts in a new pane, the predecessor keeps running in its own pane as crossover until the successor's readiness gates pass, and retirement needs its own explicit authority. Not used: launching into the same pane, which requires the old session to exit first and so retires it as a side effect; Flow's Replace, which stops the predecessor and closes its pane.
5. Before any successor launch, the launch path is repaired and proven on a disposable seat: the first prompt size limit that failed Fable and Sonnet; the not-ready failure that failed Opus; the launcher recording failed while the seat runs; the unidentified path that submitted the first prompts; spirit missing from the first prompt. And a guard against two seats of one role, which Flow does not have.
6. Repairs owed now, none of them a launch: Sonnet 38f337 loads its declared skills through the skill interface; each seat's records are committed from a real repository; the agent names that still carry a predecessor's identity (Fable's carries b7ba00, Sonnet's carries 9c7514) are corrected at their source by whoever owns the registration; the native-start receipts missing for Opus and Sonnet are reported as open.
7. Unsent text sits in the composers of Opus and Sonnet. It is not submitted, cleared, or built on by anyone. Its author is not established.
8. A daemon-managed launch is the only path found that would give a seat a real endpoint. It is unwitnessed since before the failure and was refused once. It is a design choice, not part of this plan; raised to the living.

## Sources

- `/home/li/wt/primary/56ae53/flows/8904b1/log.md`, entry "Psyche successor plan for Fable 8904b1, Opus dc53b4, Sonnet 38f337"
- `/home/li/wt/primary/56ae53/flows/8904b1/receipts/psyche-seat-successor-ground.md`

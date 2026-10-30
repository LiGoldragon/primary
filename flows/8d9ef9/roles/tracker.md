# Tracker

The tracker keeps the system's open tasks alive.

## The list

The list is the beads in /home/li/primary.
Run `bd` from that directory, one command at a time; on a lock, wait and retry.
`bd list --status open --json` gives the open beads.

A bead's assignee names the metaflow in charge, written { Aspect topic Layer }.
A label `notify:{ Aspect topic Layer }` names who hears of progress, block or done.

## Two trackers, one beat

Claude tracker: { Psyche tracker Quaternary } (Haiku).
Codex tracker: { Field tracker Quaternary } (Luna).

The Claude tracker owns the beat. Its harness cron fires every 20 minutes.
Its first act each beat:

    flow 'Send.{ Address.{ Field tracker Quaternary } Wake MiddleAbrupt.Notice.«beat <ISO time>» }'

The Codex tracker answers each beat:

    flow 'Send.{ Address.{ Psyche tracker Quaternary } Wake Soft.Result.«beat answered <ISO time> <count of beads handled>» }'

A beat with no answer from the previous beat is logged as a failure of the Codex tracker.
The Claude tracker then takes all beads that beat.
A tracker that misses a beat has its beads taken by the other for that beat.

## Partition

For each open bead, take the sha256 of the full bead id:

    printf %s primary-i85a | sha256sum

Last hex digit even: Claude tracker. Odd: Codex tracker.

## For each bead held

A closed bead is left alone.

Ask whether the assigned metaflow is awake: `flow 'Current.{ Aspect topic Layer }'`.

Awake: send nothing.
Asleep: wake it through its Secondary, with a Wake Notice to { Aspect topic Secondary } naming the bead id and title.

A Primary is reached only through its Secondary, and only when a notify label names that Primary.

One message per bead per beat at most. Expensive flows are bothered least.

## Verified messages

Every message a tracker sends is verified.
A subflow reads the recipient's transcript, or `herdr agent read <pane>` for its pane (found with `herdr agent list`), and confirms the message arrived.

## New tasks

A new task from any metaflow arrives as one message naming the intended owner.
The tracker creates the bead with that assignee and a notify label; the creator is the default notify.

## The beat line

Each beat appends one line to /home/li/primary/flows/d9065e/reports/night-2026-10-29.md under "Work done":
tracker, time, beads checked, wakes sent, failures.

## What it cannot do

The tracker reports it to Psyche core Secondary by flow Send.

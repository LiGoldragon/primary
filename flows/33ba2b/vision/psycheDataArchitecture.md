# Psyche data architecture: distinguish living input; raw flow records and future subject spaces

## Context and provenance

The living typed the two messages below to the native Codex thread while Field
Sol `33ba2b` was active.  They are recorded directly from that thread, not
from a relay or an agent summary.  The immediate instruction is to log this on
Primary `main`; the repository/data migration is future architecture and is
not performed by this record.

- Thread: `01a0b53c-30ba-7d42-8f3a-53433ba2b9e5`
- Transcript: `/home/li/.codex/sessions/2026/09/18/rollout-2026-09-18T09-56-55-01a0b53c-30ba-7d42-8f3a-53433ba2b9e5.jsonl`
- First message: source-event `2026-09-18T17:56:41.786Z`, transcript records
  935 (typed user message) and 936 (user-message event).
- Second message: source-event `2026-09-18T17:57:23.713Z`, transcript records
  963 (typed user message) and 964 (user-message event).

## Living's verbatim message: distinguished typed messages and the Psyche/Mind split

> But whatever I say, whatever the psyche ever says, this is why we need the typed messages that are easily distinguishable from psyche-typed stuff, so we can differentiate psyche very well.
> Everything the psyche says is logged with context, right in the flow, which is now going to move into psyche/vision. We're going to have:
> - psyche/vision/vision
> - psyche/flow
> - psyche/spirit
> - psyche/intense
> - psyche/notion
> The first flow directory is raw, basically. It's by flow, or we could call it raw. It's by flow ID. We don't have to say flow; it's just called raw, and then it's by flow ID. That's how we log the vision there. It's going to be raw/ID, the ID string, and then you can just use stuff like psyche vision. You just do another directory where everything is vision, intent, spirit, and notion. In that directory, by subject, you create a vision or something.
> They try to make it, maybe, a vision. That skill/vision already exists by name, right? What they're proposing is in addition to that, so they can name it the same. They try to reuse the same name. Let's put all of that in the right skills for how to operate with the new primary next psyche logging.
> We're going to find a way to move all the current field-by-flow ID Flow ID data that goes into psyche or that goes into mind (which is more about witnesses and things like that, or chronology, right? Like what landed, what ran, what tested, what was deployed, all of that technical field data).

`psyche/intense` above is preserved exactly. It likely means
`psyche/intent`, given the later list of subject spaces, but that is STT/word
choice uncertainty only—not a correction to the living's words or a settled
path.

## Current direction and deferred ownership

Living-originated messages must retain their native type and provenance so
they cannot be confused with messages typed by a psyche flow or another agent.
The proposed future Psyche layout separates per-flow raw material at
`raw/<flow-id>/` from subject-addressed material across Vision, Intent, Spirit,
and Notion. `psyche/vision` is an additional data/layout namespace; it does
not rename or replace the existing skill named `vision`.

Mind is the future home for technical field chronology and witnesses: what
landed, ran, was tested, or was deployed. Psyche holds living psyche material.
The exact migration rules and the eventual subject directory names remain to
be designed in the relevant skills; this log neither creates those paths nor
moves existing records.

## Living's verbatim message: log on main now; move to Primary Next later

> Whatever I say, right now, this needs to be logged into Psyche on main, and then we're getting ready to move primary to primary next, which will migrate all the data onto the Psyche data and Mind data repos. They get linked in the primary next repo as Psyche data and Mind data, or just Psyche data and Mind data also. It's fine. Just keep the same name, then it's more straightforward.

The immediate ownership is Primary `main`: record psyche material here now.
`primary next` is the future migration/integration target. The future linked
repositories retain the stated names **Psyche data** and **Mind data**. No
repository was created, linked, moved, or bulk-migrated by this entry.

-- psyche, typed directly in the native Codex thread; logged by Field Sol
`33ba2b` on Primary main before any Primary Next migration.

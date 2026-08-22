# Wave 1 migration rulings

Wave 1 recovered the living psyche's typed words from actual Claude and
Codex transcript files. Flow logs and assistant-authored migration prompts
were used only as search seeds; they do not stand as rulings.

## What the protocol receives

In the 5c8be3ca transcript, the psyche described the subject as:

> I want any artifact that a flow generates which doesn't have a specific,
> anything that isn't going in a specific repository, like anything that
> isn't code being written or a readme being written or something going
> somewhere.

> Anything that a flow generates that the flow isn't sure where to put it.

The same message names reports, ledgers, witnesses, researched material,
the session log and index, and says that a flow's subagents fall under its
flow. Code, READMEs, and material with a specific repository home are the
explicit counterexamples. The initially imagined separate repository was
later narrowed by the psyche to:

> lets make it simple, in workspace for now.

## Origin and home

The chain-of-origin direction began with session-scoped written-psyche
records:

> I think Psyche logging could be done with the short session ID besides
> every records, which would let a later agent verify the entire
> conversation if the session file is still there and would allow that flow
> to possibly get an actually better understanding of what the Psyche was
> saying because he has different perspective and a better focus. So like
> this chain of origin is essentially the concept that is appearing out of
> all of this approach.

The retrofit was then stated directly:

> we could hunt for the origin of every existing record to retrofit them. I
> like that idea

For flow artifacts, the psyche stated:

> the files of that specific flow will go into its own directory, which is
> the short ID, which is named after the short ID of its session.

An explicit per-artifact `Origin:` header was rejected:

> no of course not! the directory gives the flow. only subflows need to
> indicate their id

The later ruling dropped subflow marking because a subflow could not see
its own ID. The resulting home marker is the flow directory itself. The
current flow added the operative evidence boundary:

> origin must be in actual transcript files. unknown origin artifacts will
> not be moved.

> files that are already annotated with their origin sessions obviously
> already have their new home marked

An annotation therefore routes a candidate to `flows/<short-id>/`, but the
referenced session must exist as an actual transcript file. Unannotated
artifacts require transcript tracing; unresolved artifacts remain in place.

## Migration and written psyche

The migration commission in 5c8be3ca was:

> I want a prompt for another flow to migrate all the artifacts that can be
> pinpointed to a session file, along with all the psyche logs, etc.

When the first assistant-authored prompt proposed leaving `psyche/`
topic-keyed, the psyche corrected it:

> no, psyche records that can be traced will also be moved.

The later 15b67974 transcript identifies the current content kind:

> we are loggin psyche, yes, but more specifically we are logging psyche
> *vision*. so we should make it flows/<id>/vision/...

That flow explicitly deferred the broader machinery upgrade and retained
the current skill. Consequently this migration may place transcript-traced
Vision in an origin flow's `vision/<topic>.md`; it does not independently
retire all top-level written-psyche machinery, and it does not infer origins
for Intent or Spirit.

## Execution ruling

The current flow's fifth step was changed verbatim to:

> you can make step 5 "proceed with the migration" - use subflows for all
> work of course

Wave 5 therefore performs the grounded migrations through subflows rather
than stopping at a proposal. No migration occurs before inventory, tracing,
and independent challenge.

## What the transcripts did not rule

- The old assistant-authored prompt proposed a blanket delete-originals
  policy. Wave 1 found no typed psyche ruling independently approving that
  policy for every artifact class.
- The transcripts do not directly classify every legacy directory. In
  particular, `handoffs/`, `agent-outputs/`, `verified/`, and legacy
  `awareness/` contents must be classified artifact by artifact against the
  no-specific-repository-home rule.
- The psyche requested a merge for divergent 15b67974 protocol artifacts,
  but strict-union mechanics and deletion timing came from assistant text.
- Describing `spiritbackup.nota` as old is not origin evidence.
- Removing the top-level written-psyche machinery was explicitly deferred.

## Sources

- Claude transcript `06196cc7-0e13-4c16-9beb-509da55a2bb3.jsonl`, line 716,
  2026-08-14T11:20:27.613Z.
- Claude transcript `fb1008c0-9ffd-4edc-8451-d22705fba991.jsonl`, line 66,
  2026-08-14T12:00:44.437Z.
- Claude transcript `5c8be3ca-3f5c-495c-af78-d063b7c4b337.jsonl`, lines 7,
  237, 286, 562, 688, and 746.
- Claude transcript `15b67974-1fea-4d8c-83d1-46e4e6cd6532.jsonl`, lines 1024,
  1028, and 1060.
- Codex transcript
  `rollout-2026-08-22T17-11-06-01a02a06-87ce-7691-9e87-f28263690b5d.jsonl`,
  user-message record ordinals 93, 147, and 196.
- Subflow returns: `migration_scope`, `origin_rule_history`, and
  `ruling_provenance`, Wave 1 of flow 01a02a06.

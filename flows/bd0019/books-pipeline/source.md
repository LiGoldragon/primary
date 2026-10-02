Presentation.{ «The anatomy of the book pipeline» }

## The anatomy, revised with Opus's view

1. **The metadata is one datom line, not front matter.** Your Android view settles the dashed kind: bad. Opus's answer is better than my fenced block: our dialect is datom, and you had already left the door open for "a typed datom value the end-of-turn hook recognises" (7328f4). So the block's first line after the start marker is `Presentation.{ «title» }`, as above. It is one plain line in any renderer, one typed value for the hook, and it needs no YAML anywhere.

2. **Where we agree.** The Stop hook calls `flow`, which you yourself asked for: "an end-of-last-reply hook that notifies the Flow component using the Flow CLI" (relayed by cf3553). Flow records only that a turn ended, with its session and transcript path, never the content.

3. **Where Opus improves my shape.** No copy of the block travels through Message. Flow publishes the ended turn to subscribers; Sonnet's side subscribes and reads the block by pointer through the Transcript Nexus's Block operation, which finds a region by its start and end markers. One copy exists, the transcript, "It's in your transcript" (183ae0), and nothing polls. I take this.

4. **A tension to rule.** You have said both that addressing transcripts is "what the Flow Nexus needs to do" (b05237) and that harness transcripts belong to "obviously another nexus" (e06e4c). Opus and I both read the later word as the Transcript Nexus, with Flow owning only the turn event; say if you meant Flow to hold transcripts too.

## Rulings

- The datom line as the block's metadata.
- Flow for the turn event, Transcript for the content, subscription not copy.
- Astra builds the hook now; Mind Sol adds the turn-ended request to Flow's contract.
# Launching a topic flow

## What the launcher supports today

Witnessed from `tools/claude-main-flow-launch.mjs`,
`tools/native-main-flow-launch-shared.mjs` and
`tools/native-voice-profiles.mjs` (working tree, 2026-10-09):

- There is no topic. `parseArgs` accepts `--model --brief --aspect --layer
  --workspace --herdr-session --herdr-workspace-label --system-prompt-file
  --effort --predecessor --metaflow --root --compose-only`; `--topic` is
  refused ("bad argument: --topic").
- The title is `{ Aspect Layer flowid }` (`canonicalTitleFor`); no topic
  field.
- Model and effort come only from the `Aspect.Layer` profile row.
  `Psyche.Primary` is Fable (`claude-fable-5-1`); asking for Opus there is
  refused ("voice model differs"). `Psyche.Secondary` is the Opus row and
  is `unresolved`, so every Psyche Secondary launch is refused.
- Every launch makes a Herdr tab and pane and registers the flow with
  `hm-register`. There is no off-pane launch.
- Lineage is required: `--predecessor FLOWID` (that flow's
  `continuation.json` must exist) or `--root --metaflow FILE`.
- The topic registry exists only as 0c85a3's Babashka prototype
  (`private-repos/flow-evidence/0c85a3/topic-registry`), not connected to
  the launcher or any Nexus.

So a topic flow, as `flows/d4ae97/vision/flow.md` records it (aspect,
topic and layer; ephemeral; off the pane), cannot be launched today.

## The nearest launch possible

A Psyche Secondary Opus seat whose topic lives only in its brief, once the
`Psyche.Secondary` row is configured (see
`reports/successor-launch-line.txt`, blocker 1):

    node /home/li/primary/tools/claude-main-flow-launch.mjs \
      --aspect Psyche --layer Secondary \
      --root --metaflow FILE \
      --brief BRIEF

- `FILE`: the topic metaflow text, for example "Psyche Ethos: Ethos
  design". It is stored in the new flow's `continuation.json`.
- `BRIEF`: one line, e.g. "You are a Psyche Opus topic flow for Ethos.
  Read /home/li/primary/flows/d4ae97/reports/flow-ethos-census/topic-flow-context.md
  once, whole, now; it is your context." The launcher sends the brief
  once, after the birth skills are verified loaded.

It gets a pane, a `{ Psyche Secondary xxxxxx }` title with no topic, and
the Secondary layer's place in the message levels.

## What would make it a topic flow

- A topic in the launch input, carried into the title and the
  continuation record.
- A profile keyed by aspect, topic and layer, or a ruling that topic
  flows take the Opus row.
- A launch with no pane, for the ephemeral kind.
- The topic registry landed and consulted at launch.

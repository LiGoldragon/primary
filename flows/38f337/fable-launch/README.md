# Corrected Fable recovery launch packet

This corrects one thing in `flows/56ae53/fable-recovery/`: the composed Claude
first line. Nothing else in that packet is disputed, and this directory does
not replace it. It is not an authorization to Start.

## The refusal

Flow 0.17.x composes a Claude launch as one line and refuses it rather than
truncating it. From `crates/flow-nexus/src/composition.rs` in the `flow`
repository at 0.17.2:

- `ClaudeFirstLine::LIMIT = 800`, counted in UTF-16 code units by
  `text.encode_utf16().count()`.
- `ClaudeCommandStack::LIMIT = 5`.
- `render_claude_line` emits, in order: `/name ` for each of the first five
  skills, `Read <bundle file> for your launch mode`, then, when there are more
  than five skills, `, load <the rest, comma separated> through the Skill tool
  in this order`, then `, then: <instruction_prompt>`, then, when the source
  vector is non-empty, ` Sources: <absolute paths, comma separated>.`
- `LaunchReceipt::footer_for(Claude)` appends
  ` When every skill has loaded, reply once with exactly
  FLOW_LAUNCH_RECEIPT_V2 and nothing else.` on the same line.
- `compose` then returns `ClaudeFirstLineBroken` for any CR or LF and
  `ClaudeFirstLineTooLong(n)` for `n > 800`, before anything is reserved.

The stacked commands are bare skill names, not paths: `format!("/{skill} ")`.
The absolute paths in the line come from two places only — the launch bundle
file, which is fixed and unavoidable, and the source vector, one absolute path
per entry, canonicalized by `LaunchComposer::read`.

The published packet declares five sources. Rendered and comma-joined, those
five canonical paths alone are 281 UTF-16 units of the line. With the packet's
skill order and the instruction below, the line measures 941, against 713 for
the corrected profile: the same instruction, the same skills, one source path
instead of five. 56ae53 independently measured about 932 with its own
instruction text. Either way it is past 800 and Start refuses it before
reservation.

## The correction

Two changes, both in `profile.json` here:

1. The source vector is one entry, `flows/38f337/fable-launch/sources.md`. The
   five original paths and their hashes live inside that file, which the seat
   reads after it is running.
2. The skill order puts the five that must be stacked first:
   `main-flow`, `refresh`, `claude-harness`, `psyche`, `spirit`. The published
   order stacked `testing-flow-titles` and left `claude-harness` at position
   seventeen, where the Skill tool cannot reach it —
   `main-flow`, `refresh` and `claude-harness` carry
   `disable-model-invocation: true` in the `.claude` projection.

## The measured line

713 UTF-16 units, no newline, against the 800 limit. The bundle path is
modelled as `/home/li/.local/state/flow/launch-bundles/launch-<16 hex>.md`,
whose length is fixed by the launch request's short form, so the count does
not move with the request ID.

    /main-flow /refresh /claude-harness /psyche /spirit Read /home/li/.local/state/flow/launch-bundles/launch-0000000000000000.md for your launch mode, load testing-flow-titles, psyche-interraction, psyche-acquisition, psyche-distillation, behavior, correction, vocabulary, testing, subflow, edit-coordination, flow-evidence, prompt-crafting, herdr, messaging, file-editing, operational-final-response through the Skill tool in this order, then: you are the Psyche Fable successor of b7ba00; remember it at depth one; the source names your handoff and packet. Sources: /home/li/primary/flows/38f337/fable-launch/sources.md. When every skill has loaded, reply once with exactly FLOW_LAUNCH_RECEIPT_V2 and nothing else.

87 units of headroom remain. The instruction may grow to 200 units before the
line is refused again; any change to the instruction, the skill list or the
source vector must be remeasured, not estimated.

## What is not established here

- No Start was run, and no composition was produced by the Nexus itself. The
  count above is this flow's own reproduction of `render_claude_line` and the
  Claude footer against the 0.17.2 source, not a Nexus receipt.
- The launch bundle directory is read from the deployed Nexus's state
  directory (`~/.local/state/flow/launch-bundles`). A deployment with another
  state directory changes the count.
- `launch_request_id` is a placeholder. It never enters the line.

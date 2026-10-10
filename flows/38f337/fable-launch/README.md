# Corrected Fable recovery launch packet

This corrects `flows/56ae53/fable-recovery/` on the composed Claude first line,
and then corrects itself on four further defects found after it was first
published at `f444851f`. It is not an authorization to Start. No Start has been
run.

## The refusal this packet exists for

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
- `compose` returns `ClaudeFirstLineBroken` for any CR or LF and
  `ClaudeFirstLineTooLong(n)` for `n > 800`, before anything is reserved.

The published `56ae53` packet declared five sources and stacked the wrong five
skills; its line measured past 800 either way. This packet keeps that
correction: one source path, and the three force-loaded skills
(`main-flow`, `refresh`, `claude-harness`, all
`disable-model-invocation: true` in the `.claude` projection) inside the five
stacked slots.

## What was wrong in this packet at `f444851f`, and is now fixed

1. **Dead generation at depth one.** `remembered_flow_vector` held `b7ba00` at
   depth one and named no `8904b1`. `b7ba00` is the prior Fable generation and
   was never resumed; `8904b1` is the live Fable. The chain is now `8904b1` at
   depth one and `b7ba00` at depth two, and the instruction says the same. The
   depth field is also spelled as the protocol spells it,
   `remembering_depth`, not `depth`.
2. **Wrong launch-bundle directory.** The line's bundle path was modelled as
   `/home/li/.local/state/flow/launch-bundles/launch-<16 hex>.md`, 68
   characters. `flow-nexus-next.service` sets
   `HOME=/home/li/.local/state/flow-next`, so the serving Nexus writes its
   per-launch copies to
   `/home/li/.local/state/flow-next/.local/state/flow/launch-bundles`. Three
   real generated bundles were observed there, each path **91** characters, not
   68. The count below uses the observed 91.
3. **Required field missing.** `system_prompt_bundle_file` was absent
   altogether. `LaunchComposer::validate` requires it to be absolute, to be an
   existing file, and not to be a symlink, or composition fails before anything
   is reserved. It is now
   `/home/li/primary/tools/main-flow-mode/system-prompt.md`
   (`a0cfec76…`), verified absolute, a regular file, and not a symlink. That
   file's bytes are exactly the body of the live generated bundles, which
   differ from it only by the launch section the Nexus appends.
4. **The packet authenticated nothing it carries.** The source vector hashes
   `sources.md`, but `sources.md` only *mentioned* `handoff-fable.md`,
   `successor-prompt-fable.md` and `flows/8904b1/summary.md` by path. Naming a
   path binds no bytes. Those three now carry their SHA-256 inside `sources.md`
   like every other entry, so hashing `sources.md` transitively binds the
   content the packet hands over.

`flows/56ae53/log.md` remains the one entry whose hash is expected to move: it
is a growing log, and its hash here is the one recorded at this correction.

## The measured line

**760 UTF-16 code units against the 800 limit. 40 units of headroom. No CR, no
LF.**

This is not a reproduction. `LaunchComposer::compose` from flow 0.17.2 was run
against this exact profile in a temporary source root, with
`has_canonical_first_prompt()` true, and the temporary source and
launch-bundle-copy paths were then substituted back to the live ones they stand
for — `/home/li/primary/flows/38f337/fable-launch/sources.md` (53 characters)
and the 91-character bundle-copy path above. The count is of that substituted
line.

    /main-flow /refresh /claude-harness /psyche /spirit Read /home/li/.local/state/flow-next/.local/state/flow/launch-bundles/launch-<16 hex>.md for your launch mode, load testing-flow-titles, psyche-interraction, psyche-acquisition, psyche-distillation, behavior, correction, vocabulary, testing, subflow, edit-coordination, flow-evidence, prompt-crafting, herdr, messaging, file-editing, operational-final-response through the Skill tool in this order, then: you are the Psyche Fable successor of 8904b1; remember it at depth one and b7ba00 at depth two; the source names your handoff and packet. Sources: /home/li/primary/flows/38f337/fable-launch/sources.md. When every skill has loaded, reply once with exactly FLOW_LAUNCH_RECEIPT_V2 and nothing else.

The bundle name is the launch request's 16-hex short form
(`ShortensLaunchRequest::SHORT_FORM_LENGTH = 16`), so the count does not move
with the request ID. The 68-character model would have given 737 for these same
inputs; the earlier 713 was the same line with the shorter, wrong instruction
and the 68-character model.

Any change to the instruction, the skill list, the source vector, or the
serving Nexus's HOME must be remeasured, not estimated. The instruction may
grow by 40 units before the line is refused.

## What is still not established here

- No Start was run and no composition was produced by the Nexus itself. The
  count is from the real 0.17.2 composer, run locally against this profile, not
  from a Nexus receipt.
- The bundle directory is the one the currently deployed Flow-next unit serves
  from. A redeploy under another HOME changes the count.
- `launch_request_id` is a placeholder. It never enters the line.

# Book-page overwrite incident, 2026-10-13, flow 33752b

Main flow session: /home/li/.claude/projects/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939.jsonl

Affected URL (overwritten, then restored): https://claude.ai/artifact/7oT2KrfJo2pKff2bJkBP6a
  Original book: «Aspects talk at the same layer, third edition», source flows/33752b/books/14-aspects-same-layer-3.md
  Version 2: overwritten with «Cleaning up the skills» by the publish below
  Version 3: restored from the source above (re-rendered; no .html had been saved beside it)

Fresh URL of «Cleaning up the skills»: https://claude.ai/artifact/SELrh2dGgsSsu1r5WxNBsb (Version 1)
  Page: flows/33752b/books/23-cleaning-skills.html; source: flows/33752b/books/23-cleaning-skills.md

Subflow transcripts (book agent, run inside the main session), in order:
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/ace32980b84822270.output  first «Cleaning up the skills» publish attempt, stopped by me before completion
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a43e1f79224c62f4e.output  the overwriting publish; result reported "Version 2" and the 7oT2Kr URL; local HTML path not reported
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a151862756ad1d8f7.output  «Context modules» publish, fresh (https://claude.ai/artifact/7BDUy7EUpuuPihAi6jtdki); page at scratchpad/context-modules-33752b-24.html
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/aab97691c754c99eb.output  restoration (url passed, Version 3) and fresh republish (file_path, icon "book", label, no url)

Earlier book subflows in this session, for file-name comparison:
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a436d20b19d5491db.output  «Handover and the seat without a shovel», page at scratchpad/page22.html
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a4febc98c9cbf0d4b.output  «Two Field lines without a source», page at flows/33752b/books/21-two-field-lines.html
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a86ac630d8ccb3d7e.output  «Anatomy audit»
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a80c55258ccedceb9.output  «Nuts and bolts, not welding, second edition», page at scratchpad/book-nuts-bolts-2.html
  /tmp/claude-1001/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939/tasks/a7d25d59359b7ff8a.output  «Nuts and bolts, not welding»

The aspects third edition was published 2026-10-12 by an earlier book subflow of this same session (transcript id not retained here; search the main session for 7oT2KrfJo2pKff2bJkBP6a).

Hypothesis (not witnessed): the Artifact tool keys a URL by local file path for the session; a page rendered to a reused name republished to that name's URL.

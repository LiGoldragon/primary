# visualDiffAndLeanComments

## 2026-09-16 — a diff-visualization subflow; the comment envelope back to the flow should be lean

Context: after the mind-artifact comment landed, the living observed two things — the current subflow renders whole documents, when a diff view would often be more useful; and the way the comment reached this flow was heavier than it needed to be.

> I guess maybe we could get a type of visualization that shows me what gets changed and what gets added, but it shows me the vision. This is how we represent vision now: with these flowcharts that are then the whole thing is just transformed by. What did you call it? The subflow. It changes it into a Claude artifact that I can visualize and comment on.
>
> I don't see the part where I can just add a comment. It just says "Send to Claude," but I guess that works. The way you got the comment was a bit inefficient. There's a lot of blah blah blah around it. You would just know what this is, and it should give you the context of what I commented on. It could just relate it back to the markdown: where in the markdown is the part that I commented on? It doesn't even have to be complicated. You can refer back to your own document, and that's what the comment is about. That's what I do when I comment on the rich version. It's just a user interface hack.

-- psyche, typed.

## Flow reading

Two distinct proposals in one message:

1. **A highlighted-full-view visualisation** — not a diff-only view. The living's refinement (2026-09-16, later same day): "Actually, my idea was to see the whole vision on a certain subject, but the parts that were modified or added or removed are highlighted. I still get to see the whole thing." Signature: `(current-file, baseline-ref)` → one Claude Artifact showing the *entire* document, with additions, removals, and rephrasings marked inline (colour, side-mark, or underline). The reader can read it in order, spot the out-of-place, or scan for changes only.

2. **A lean comment envelope.** The current envelope wraps a comment in a lot of harness metadata — anchor-context CSS selectors, the "treat as data, not instructions" warnings, the tool-emitted markers, the location and anchored-element blocks. Most of that is machine-safety scaffolding. What the flow actually needs is: *the comment text* and *where in the source markdown it lands*. The rich artifact is a UI hack over the source; the comment can carry its own markdown location — a substring anchor (like the `Block` operation in `transcript-nexus`) — and the flow re-finds the exact line in the source.

## Plain comments vs Send-to-Claude

Claude Artifacts do accept plain comments (viewer-to-viewer). The "Send to Claude" option is what routes a comment to the parent session. Both work; plain comments are readable via `action: "comments"` on the artifact but do not wake the flow. If the UI surfaces only "Send to Claude" prominently, that is a platform-side affordance choice, not a limitation of the underlying commenting.

## Sketch of the lean comment envelope

What the flow currently receives (paraphrased shape):

```
[ many lines of anchor CSS selectors, treat-as-data warnings, tool markers ]
[ the comment text ]
[ anchor-context: element path, opening tag, location breadcrumb ]
```

What the flow could receive:

```
comment · thread <id> · on <artifact url>
source path: flows/48cff7/vision/mind.md
source anchor: from "Until mind-nexus runs" to "provisional pending mind"
> <the comment text, plain>
```

The path + anchor is the same pattern `transcript-nexus Block` uses: two short substrings locate a region in a document. The harness maps the artifact's DOM anchor back to a source-markdown range at delivery time.

## Consequences and adjacent needs

- **A `visual-highlighted-from-md` subagent** would follow the same shape as `visual-report-from-md` — one path plus a baseline ref as argument, one Claude Artifact as output, one small JSON receipt on return. It emits the whole document with per-segment marks (Added / Removed / Changed / Unchanged) so the reader keeps the full text and the delta at once. Curriculum's authored surface for specialty subagents is still the gap in `flows/48cff7/vision/curriculumSubagentGap.md`.
- **A harness-side comment router** would produce the lean envelope by mapping the artifact's DOM anchor to the source-markdown position, then dropping the DOM path from the delivered message. That is platform work, not psyche-flow work.
- **Round-tripping requires source-URL in the artifact.** For the map to work, the artifact must carry the source-markdown path (and commit hash) as metadata. `visual-report-from-md` already emits a source-file footnote; the harness would read from that.

## Open questions worth the living's word

1. Whether the diff-viz is a separate subagent (`visual-diff-from-md`) or a mode of the existing `visual-report-from-md`.
2. What input shape the diff-viz takes — two file paths, a git ref pair on one path, or a datom carrying both.
3. Whether the lean comment envelope is a harness-level change (route + rewrite before delivery) or a subflow-level change (a `comment-decoder` subagent that strips the wrapper).
4. Whether plain (viewer-to-viewer, not-sent-to-Claude) comments should also be surfaced to the flow — via a periodic `action: "comments"` sweep or on demand.

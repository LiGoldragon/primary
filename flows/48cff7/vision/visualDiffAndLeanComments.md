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

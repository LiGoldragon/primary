# Corrected book proposal forms report

Implementation is commits `c208c14` and `66eec320e95cedeafdeb35ad2ef6a33bebb5153c` on pushed branch `book-proposal-forms`. The isolated worktree is `/home/li/primary/flows/d76b4c/book-builder/makeshift-tools`; primary checkout and `/home/li/primary/tools` stayed untouched.

The corrected form places proposal 6 inside each whole module view. In `vision/aspects.md`, its red removals and one blue moved passage replace the current route block at its actual location; the unchanged blue module no longer repeats that block or passage. An adjacent removed fragment plus move container authenticates a passage that occupied the end of one current source line. A blank before the move retains whole-line behavior. The move is rendered once and heads itself with both source and destination modules. The same proposal number continues in `vision/model-roles.md` and `vision/flow-nexus.md`; `vision/flow-nexus-v1.md` is the whole destination context.

Regression tests now cover the original failure: the moved text occurs exactly once in generated HTML, the in-place section and move occur before the source module closes, a proposal at the first module line retains red margins, and adjacency versus a blank is authenticated differently. Checker tests pass 152/152. Builder tests pass all new assertions; the same three pre-existing tree-sitter highlight assertions remain (417/420 passing). Actual merged-source checker and CLI builder exit 0.

Corrected source: `/home/li/primary/flows/d76b4c/book-builder/roles-merged.md`. Output: `/home/li/primary/flows/d76b4c/book-builder/roles-merged.html`. A direct count finds the moved Field sentence exactly once in the HTML.

Visual inspection: `/home/li/primary/flows/d76b4c/book-builder/roles-merged-corrected.png` shows the red removals and sole blue move inside the aspects module; `roles-merged-lower.png` shows proposal 6 inside model-roles; `roles-merged-replacement-detail.png` shows the word-only replacement inside flow-nexus. Mermaid dark-box label contrast is pre-existing and outside this form change.

Original Fable source, vision, publication service, deployment, and main were not changed. Partial-line source authentication is now explicit by adjacency; no visible presentation syntax was invented beyond the existing signed edit and move container forms.

Presentation.{ «A module begins with one line» }

# A module begins with one line

Created by Fable, from his words of 2026-11-05: in a new flow's first prompt he cannot see where a module begins and ends; he was told lines say so and does not see them; the delimiters should be clear and cheap, and XML, which repeats its tag at the end, is dumb.

What he was told is true and useless: each module is wrapped in `<!-- module: vision:flow-nexus -->` and `<!-- end-module: vision:flow-nexus -->`, HTML comments, which a rendered view hides, so he sees nothing; and it is the XML shape, the name said twice.

### Proposal 1: One visible line opens a module · psyche-belief › vision/belief-modules.md

**Comment** After "A module declares its placement".

  A module declares its placement: the system prompt, or loaded on demand. A skill is the harness's interface for an on-demand module.

+ In a prompt a module opens with one line, its id as a top-level heading, `# vision:flow-nexus`, and ends where the next module opens or the prompt ends; nothing closes it. The line is visible rendered and raw, costs a handful of tokens, and says the name once; a module's own headings start at the second level, so the first level is the module boundary alone.

```text
+ # intent:main-flow
+ You are a main flow: one of the flows that extend the living. …
+
+ # vision:flow-nexus
+ ## What it does
+ …
```

```mermaid
+ flowchart TB
+     p["a prompt"] -- "is a sequence of" --> m["modules"]
+     m -- "each opens with" --> h["one line: # kind:horizon:subject"]
+     h -- "ends at" --> n["the next opening line, or the prompt's end"]
```

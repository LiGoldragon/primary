# Operational: a model that watches for idle flows with reports, archives them, and dispatches illustration

## A model watches for flows that come to idle to see if they ended with a report, makes a backup into the log, creates the flow archive, marks it as main flow or subflow report, and sends a job to the most qualified flow to illustrate it

Context: spoken by the living to primary Psyche opus (Claude, medium, flow
b05237) on 2026-09-18. The living names a watcher model that detects when a
flow goes idle, checks whether it ended with a structured report (the defining
features: structured Markdown, Mermaid flowcharts that will become vector
graphs, animation, and AI-generated images), backs it up into the log, creates
the flow archive, classifies it (main flow or subflow report), and dispatches
an illustration job to the most qualified flow. A hook is the detection
mechanism. The report format should be templated in the skill and progressively
clarified. Logged by the main flow before acting.

> We need a model that watches for flows that come to an idle to see if they ended with a report, like a nicely formatted report, and we'll have a way to make that more and more clear. Maybe we can start to clarify that here and template it in the skill. One of the defining features is that it uses structured Markdown and it has flowcharts, meaning Mermaid graphs that will be turned into vector graphs, animation, and AI-generated images of those graphs and the ideas around them. One hook checks for the report and then finds that it's there and makes a backup of it, maybe into the log. The flow archive is what it is, so he creates the flow archive of it and marks it as what it is: either a main flow or a subflow report, and then can send a job to the most qualified flow to illustrate it.

-- psyche, direct to primary Psyche opus b05237.

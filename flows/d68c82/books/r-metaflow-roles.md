<!-- to-the-living:start -->
Presentation.{ «Metaflow roles, 2nd edition» }

# Metaflow roles

A role says which model sits at one place in a metaflow and what it knows. This book proposes where roles are written down, which helpers a role may call, and how a helper gets its knowledge. The Publisher, on Haiku, calling the Sonnet Illustrator is the first example.

## Proposal 1: psyche-context › skills/vision-flow.md

+ A metaflow's roles are defined in role definition files, written in datom and typed in ethos, as the data that configures the Flow Nexus.
+ They live in a public repository of their own, apart from the cluster data.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

+ A role names the subagent models it may call: by default, those at its own rung and below.
+ A role may name a model above its own rung.
+ The first such exception is the Publisher, on Haiku, which calls the Illustrator, on Sonnet.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-flow.md

+ A subagent is defined in a file of its own and is generated with every context module its definition names.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->

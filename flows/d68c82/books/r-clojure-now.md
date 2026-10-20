<!-- to-the-living:start -->
Presentation.{ «Short-term prototypes: Clojure now?, 2nd edition» }

# Short-term prototypes: Clojure now?

This book is about the short-term prototypes written in Clojure: what a call takes, how the tool that starts flows reads its settings, and what runs the programs. The code and the machine's own rules went to their owner and are not shown.

## Proposal 1: psyche-context › vision/stack.md, a new file

+ ## A Clojure call takes a simple EDN input
+ A Clojure call takes a simple EDN input, and its spec is in Malli.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

+ ## Short term: the configuration of starting flows
+ The short-term tool that starts flows reads its whole configuration from EDN: a shared file, each aspect's file, and each metaflow's file holding what differs.
+ The configuration names every context module a flow starts with, and whether it goes in the system prompt or the user prompt.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › vision/stack.md, a new file

+ ## Babashka first, the Nix-built image when deployed
+ Babashka in first use and testing, the Nix-built image when deployed.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->

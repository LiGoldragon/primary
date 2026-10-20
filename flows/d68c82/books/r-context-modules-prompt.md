<!-- to-the-living:start -->
Presentation.{ «Flow: context modules and the prompt, 2nd edition» }

# Flow: context modules and the prompt

This book is about how a flow's prompt is built from context modules, where those modules live, and how Flow finds them.
It keeps only what is still open from the first edition; what «How a seat gets its context» already proposes is not repeated here.
The code changes went to their owner and are not shown.

## Proposal 1: psyche-context › skills/vision-flow.md

+ The system prompt is not one thing: it is composed of modules of several types, and what a harness calls a skill overlaps with them.
+ Its anatomy is drawn up in ethos from a study of system prompts of every kind, each line placed by what it is and by the kind of guidance it belongs to.
+ Where the harness allows it, a part of a main flow's system prompt is the main flow's alone and is not passed down to its subagents.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-context-modules.md

+ The vocabulary is context, context modules and context building.
+ A skill is the legacy name, one harness name for things that differ, becoming obsolete as harness infrastructure improves.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-psyche.md

- The skills belong in a repository. This is a target shape, not authorization to create or migrate a repository (native desktop record, archive ordinal 1835).
+ The context modules belong in a context repository; Psyche's is psyche-context.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-flow.md

- ## Repository and skills
- The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it, the basic skills included, so that a change to a skill causes no Nix rebuild. The basic skills give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
+ ## Repository and context modules
+ The flow repository holds the machinery of the Flow Nexus and is a runtime repository.
+ Every context module lives outside it, the basic modules included, so that a change to a module causes no Nix rebuild.
+ The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › skills/vision-context-modules.md

+ The role module is a type of its own: it carries a flow's role, and the flow it is given to does not see it as a module.
+ A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.
+ A role module is found by its metaflow: the repository is its aspect, the section its layer, and the file its topic, so the core file in Psyche's Primary section is the Psyche core Primary's role.
+ What is about a topic rather than a role goes in a regular module.
+ Every context repository also holds a subagent section, whose modules make the named subagent definitions.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › skills/vision-flow.md

+ A hook controls what is injected into a flow's prompt and what goes through messaging, for every flow.
+ What has been queued for an idle metaflow, the vision touching its topic among it, is injected with the request that wakes it, so the flow knows it as soon as it wakes.
+ A metaflow is not woken each time something touching its topic accumulates.

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › skills/vision-flow.md

+ The module registry is keyed by subaspect and topic, and holds for each module its containing source, that source's blake3 hash, and the module's path inside the source.
+ To the Nexus, a module's location is nothing but its registry entry.
+ The registry is changed only through the meta signal, and Curriculum gets or checks the hash as each query comes in.
+ Every context module is indexed in such a registry, possibly in more than one place.

Ruling: land, amend, or reject.

## Proposal 8: psyche-context › skills/vision-nexus.md

+ Flow's module registry is configuration of this kind: its entries change only through the meta socket.

Ruling: land, amend, or reject.

## Proposal 9: psyche-context › skills/vision-flow.md

+ Which intent modules enter a flow's system prompt depends on the kind of metaflow it runs; that choice is what specializes a metaflow.
+ Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.

Ruling: land, amend, or reject.

## Proposal 10: psyche-context › vision/ethos.md

- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+ Flow is one of the best current examples of ethos; its ethos lives in the flow-ethos module, which carries the code.

Ruling: land, amend, or reject.

## Proposal 11: psyche-context › skills/vision-flow.md

+ The Flow Nexus's vision stands in this module; its code, the Flow ethos, stands in a module of its own, flow-ethos.
+ When flow-ethos grows too big, the modules about the code part along the code: memory-ethos and signal-ethos, signal first, and flow-ethos for the rest.

Ruling: land, amend, or reject.

## Proposal 12: psyche-context › vision/ethos.md

+ ## Inline imports
+ The in-place form is an inline import.
+ A name imported with a capital first letter pulls directly from the core built-ins, declared in the core library of the language.
+ A name imported with a lowercase first letter pulls from a registry name, which depends on the [ethos] environment loaded.
+ A registry of manifests says where every library lives, the core library and each environment's own.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->

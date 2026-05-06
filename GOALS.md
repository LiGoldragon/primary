# Primary Workspace Goals

## Recreate a Better Gas City

We want our own version of Gas City, built from first principles instead of
copying the current implementation shape.

The first phase is analysis:

- Isolate the primitives Gas City actually uses.
- Identify how Gas City turns code harnesses, CLI commands, runtime providers,
  bead stores, prompts, and event streams into an operational API.
- Separate durable primitives from accidental implementation details.
- Preserve what works: city-as-directory, declarative agents, task-store-backed
  work, and externally observable state.
- Replace what failed under pressure: tight polling loops, ambiguous lifecycle
  metadata, hidden startup ordering, and controller behavior that can amplify
  database load.

The first artifact should be a primitive inventory:

- What is a city?
- What is an agent?
- What is a session?
- What is work?
- What is a harness?
- What is a route from work to an agent?
- What is durable state?
- What is live process state?
- What must be pushed by events instead of polled?

The first engineering target is not a clone. It is a small, inspectable core
that can start one city, register one harness, create one work item, route it
to one agent-like executor, and emit enough events that every state transition
can be observed without polling.


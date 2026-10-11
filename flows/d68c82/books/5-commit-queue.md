<!-- to-the-living:start -->
Presentation.{ «The commit queue» }

# The commit queue

Today every flow publishes to Primary on its own. It takes the PrimaryPublish lock, clones fresh, copies in only its own paths, pushes, and releases. If another flow already holds the lock, the request is refused, not queued. The refused flow asks again, and Core passes turns by hand. On 2026-10-10, main took 86 commits this way, one at a time.

There is no queue tool. `tools/primary-publish.mjs` publishes one caller's paths and passes its tests, but it has no queue and its controller was never built. Earlier, a flow held the lock permanently and published what other flows sent it, as a stopgap; that flow is retired.

```
 flow A ─┐
 flow B ─┼─▶ committer ─▶ fresh clone ─▶ main
 flow C ─┘   one request    copy paths
             at a time      commit, push
                 │
                 ▼
          reply: commit or refusal
```

Field keeps its own route. It publishes pin changes and regenerated skill trees, and it checks every generated file against the source.

## Distillation

### Proposal 1: a committer seat, until the queue runs

File: `field-skills/skills/compensation-temporary.md`. Added as a new paragraph:

Until the commit queue runs, one quaternary committer seat commits and pushes Primary for every flow except Field. A flow sends it the paths in its own directory and the commit message; the committer copies them from a fresh clone, commits one request at a time in arrival order, pushes, and answers each sender with its commit or the reason it refused.

Ruling 1: does this land, and shall I launch the committer seat?

### Proposal 2: the queue, in vision-orchestrate

File: `psyche-skills/skills/vision-orchestrate.md`. Added:

A request to publish to Primary waits its turn in a queue instead of being refused. Requests land one at a time in arrival order, and each requester is answered with its commit.

Ruling 2: does this land? Astra then designs and builds the queue, and its implementation comes back to you as a book.

### Proposal 3: a turn that runs too long

Two of your records differ here. One says a merge slot whose time runs out is investigated. The other says the spot is let go. The queue needs one answer:

1. investigate: the queue stops and tells Core;
2. let go: the turn ends and the next request lands.

Ruling 3: which one?

«The lock queue», an earlier book, proposes a wider queue for every lock. These three proposals cover only publishing to Primary. Ruling 4: does this book replace it, or do both stay open?
<!-- to-the-living:end -->

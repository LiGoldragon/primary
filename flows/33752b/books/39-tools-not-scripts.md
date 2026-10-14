<!-- to-the-living:start -->
Presentation.{ «Tools instead of scripts» }

# Tools instead of scripts

```
   a flow needs a fact
        |
        v
   writes a one-off script
   (python -c, node -e, heredoc)
        |
        v
   parses a transcript, a JSON,
   a derivation, a roster
        |
        v
   the script is gone; the next
   flow writes it again
```

Mind Tools surveyed the transcripts of both harnesses, a relayed count: in the Claude transcripts about two thousand inline Python calls, thirteen thousand heredocs, twelve thousand text-construction commands; in the Codex transcripts twenty-nine thousand executed commands. The counts overlap and measure recurrence, not missing tools. What recurs, by kind: reading transcripts and task outputs; selecting a pane or a profile from a roster; projecting a version or a digest from a derivation or a binary; assembling a page by hand.

## Crystallization

### Proposal 1: one transcript query, across every root

```
  Claude JSONL, Codex rollouts,
  task outputs, three roots
        |  one query: role, tool,
        |  command with its result,
        |  status, flow identity
        v
  the fact, with its source line
        |
        | long term
        v
  transcripts in a Nexus store,
  not files
```

Target: the transcript tool, Mind. The declared transcript shim is Claude-only and absent from the path; the extractor has provenance but not the query. Short term: one query surface over both harnesses and all three roots, returning a command paired with its result, its status, its source line and the flow's public identity from the existing registry. Long term, from your words: transcript data moves into a Nexus database, and files stop proliferating.

### Proposal 2: identity and launch preview through Flow

```
  caller wants a pane, a profile,
  a validation
        |  aspect, topic, layer
        v
  Flow / census observation
  (exists in source)
        |
        v
  the row, or "absent", or
  "ambiguous"; a preview, no launch
```

Target: Flow and the census, Mind Core. The capability exists; what is missing is a callable surface by the public three-field identity, returning ambiguity and absence explicitly, and a validate-or-preview entry that reuses the launcher's parsing with no side effect. Runtime ids stay internal.

### Proposal 3: declared, installed, running: one evidence tool

```
  declared (SKILL_VARIABLES, flake)
        |
        v
  installed (resolved executable,
  digest, version probe)
        |
        v
  running (bounded witness)
        |
        v
  one record per tool; absent and
  stale roots reported outright
```

Target: component-evidence, Field. Give it a tool-inventory input: source path and revision, expected command, resolved executable, version probe, observed digest, active configuration, bounded witness; unknown and missing stated as such. First finding it would have caught: the skill variables declare two Codex transcript roots holding nine old files, while the live root, unnamed anywhere, holds a hundred and ninety-eight.

### Proposal 4: structured task results in the book pipeline

```
  subflow result (text)
        |
        v
  node -e extracts the SVG;
  heredocs assemble the HTML
        |
        v
  the renderer, which already does
  this when given structure
```

Target: the book renderer and publisher, the publication owner. Expose structured task-result retrieval and reusable page assembly in the existing pipeline; the hand assembly witnessed in one of this flow's own book subflows is the case.

### Proposal 5: what is not built

No general safe-edit tool, no generic probe runner, no second identity registry, no blanket script cleanup: ordinary parser tests, apply_patch, shell utilities and the standing publisher cover what the survey saw, and nothing inspected was shown unused.

## Question 1

Mind Tools proposes the order: the transcript query first, then the identity and preview surface, then the evidence tool, the book pipeline where recurrence warrants it. Is that the order, and is the transcript query the short-term shape with the Nexus store as the long term, so it is named short-term and removed when the store lands?

## Question 2

The recurring scripts are a symptom of the question you asked of the flow tool: flows with disparate context re-deriving the same facts. Do these tools get built now by their owners, or does the flow tool come first and the tools follow as the specialized flows reveal what they need?
<!-- to-the-living:end -->

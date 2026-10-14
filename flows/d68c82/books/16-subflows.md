<!-- to-the-living:start -->
Presentation.{ «Subflows: one kind, specialties, a contextualizer» }

# Subflows: one kind, specialties, a contextualizer

```
+------------+        +--------------------+
| the living |        |  context modules   |
+------------+        +--------------------+
      |                   |               |
      | speaks to         | shape         | shape
      v                   v               |
+-------------------------------+         |
|           main flow           |         |
+-------------------------------+         |
   |                |        |            |
   | asks           | writes | briefs     |
   v                |        v            v
+----------------+  |      +----------------+
| contextualizer |  |      |    subflow     |
+----------------+  |      +----------------+
   |                |               |
   | names the      |               | judges
   | context for    |               | and does
   v                v               v
+-----------------------+      +----------+
|      psyche log       |      | the work |
+-----------------------+      +----------+
```

## Crystallization

### Proposal 1: A subflow is its main flow's own kind

File: `psyche-context/skills/vision-flow.md`

```text
  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
- answer; that makes the system asynchronous. Subflows run under their
- own system prompts because they need different prompts.
+ answer; that makes the system asynchronous.
+
+ ## A subflow is the same kind of flow as its main flow
+
+ A subflow is the same kind of flow as its main flow, with the same context. It works and judges, and reaches the living only through its main flow. Its role adds only its specialty.

  ## Subflows are created from the questions and requests a flow ends with
```

Where the statement lands:

1. `vision-flow`, beside how subflows are created and answered.
2. `vision-model-roles`, beside the delegation ceiling.

Ruling: land, amend, or reject.

### Proposal 2: The specialties

Every role below carries the same context; the columns are all it adds.

| Role | Permission | Depth | Claude model | Mark |
|---|---|---|---|---|
| read-trivial | read | trivial | Haiku | keeps |
| read-ordinary | read | ordinary | Sonnet | keeps |
| read-demanding | read | demanding | Opus | keeps |
| write-trivial | write | trivial | Haiku | keeps |
| write-ordinary | write | ordinary | Sonnet | keeps |
| write-demanding | write | demanding | Opus | keeps |
| tester | write | trivial | Haiku | keeps |
| book | write | ordinary | Sonnet | keeps |
| default, explorer, worker | write, read, write | ordinary, ordinary, demanding | Codex only | merge into the grid names |
| book-page | none declared | none declared | Opus | goes: no entry in the role data |
| contextualizer | read | minimal | Haiku, low effort | new |

The merge and the goes marks are the machine's reading: the three Codex roles repeat grid cells under other names, and book-page stands only in the generated agent tree.

File: `Curriculum/roles.datom`, the depths

```text
+   { minimal
+     { claude-haiku-4-5 Some.Low }
+     { gpt-5.6-luna Some.Low } }
  ]
  [ { read trivial
```

File: `Curriculum/roles.datom`, the descriptions

```text
+   { read minimal
+     «One known question, one line back.» }
  ]
  [ { default write ordinary
```

The minimal depth runs at low effort, where every seat otherwise runs at medium:

1. Low, a light effort for a fast, narrow task.
2. Medium, as every seat runs.

The three Codex roles:

1. Merge into read-ordinary, write-ordinary and write-demanding.
2. Keep under their Codex names.

Ruling: land, amend, or reject.

### Proposal 3: Every raw entry carries its context

File: `mind-context/skills/operation-psyche-interraction.md`, Logging

```text
  Log psyche as it is spoken.
  Order each topic log oldest first, with the most recent entry last.
  When the psyche speaks vision, log it before acting on it.
+ Before writing a raw entry, the main flow asks the contextualizer subflow what the entry answers. Its brief carries the entry's first and last few words; it returns the surrounding conversation in one line, which the main flow writes as the entry's context.
  Psyche not logged in the moment is psyche at risk of drift.
```

File: `Curriculum/roles.datom`, the roles

```text
+   { contextualizer read minimal
+     «Name what a raw entry answers.»
+     [ ClaudeAgent CodexAgent ] }
  ]
  [ general-instructions spirit-role
    intent-role subflow-role ]
```

What the contextualizer reads:

1. The calling flow's transcript, where the conversation stands whole.
2. The flow log alone, which holds the flow's account of it.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->

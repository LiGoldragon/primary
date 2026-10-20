Presentation.{ «Role and subagent modules» }

# Role and subagent modules

### Proposal 1: psyche-context › vision/context-modules.md

  A module declares its placement: the system prompt, or loaded on demand. A skill is the harness's interface for an on-demand module.
  
  The vocabulary is context, context modules and context building.
  A skill is the legacy name, one harness name for things that differ, becoming obsolete as harness infrastructure improves.
  
  A context repository holds one folder per module type; no folder is called skills. A file is named by its subject alone, and its folder gives its type.
  
  A module is named by its type and its subject. A directory structure gives each type its own directory; a single-string name without whitespace puts the type first, then a colon, then the subject, as vision:book.
  
  A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.
+ 
+ A role module is named by its layer and its topic: in psyche-context, the core module of the Primary section is the prompt of the Psyche core Primary.
+ 
+ Every context repository holds a subagents section: the modules of each named subagent definition, from which that definition is composed.

```
; mind-context role/ at origin/main, as it stands
role/book-description.md
role/book-page-description.md
role/default-description.md
role/explorer-description.md
role/read-demanding-description.md
role/read-ordinary-description.md
role/read-trivial-description.md
role/tester-description.md
role/worker-description.md
role/write-demanding-description.md
role/write-ordinary-description.md
role/write-trivial-description.md
```

```
; field-context role/ at main, as it stands
role/book-page-procedure.md
role/book-publishing-procedure.md
role/book-reader-description.md
role/book-reader-procedure.md
role/codex-skill-loading.md
role/comment-relay-description.md
role/comment-relay.md
role/contextualizer-description.md
role/general-instructions.md
role/illustrator-description.md
role/illustrator-faithfulness.md
role/illustrator-svg.md
role/psyche-core-tertiary-description.md
role/psyche-core-tertiary.md
role/read-restriction.md
role/scripter-description.md
role/scripter.md
role/subflow-role.md
```

```
; config/main-flow/metaflow/Psyche-Core-Primary.edn
{:aspect :Psyche :topic :Core :layer :Primary
 :modules [:intent-context-modules :spirit-core
  :intent-main-flow :intent-psyche-interaction
  :intent-psyche :vision-book
  :compensation-book-crystallization]
 :raw-psyche-paths [...]
 :first-prompt-template "..."
 :topic-context "..."}
```

```
+------------------------------------------+
| context repository                       |
+------------------------------------------+
        |                      |
      holds                  holds
        v                      v
+----------------+     +------------------+
| role section   |     | subagents        |
| per layer      |     | section          |
+----------------+     +------------------+
        |                      |
     composes               composes
        v                      v
+----------------+     +------------------+
| a flow's       |     | subagent         |
| prompt         |     | definition       |
+----------------+     +------------------+
```

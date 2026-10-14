<!-- to-the-living:start -->
Presentation.{ «The shared Clojure translation pattern» }

# The shared Clojure translation pattern

```
 +------------+          +-------------+
 | Ethos type |          | Datom value |
 +------------+          +-------------+
       |  declares              |  carries
       +-----------+------------+
                   v
       +-----------------------+
       | one construct mapping |
       +-----------------------+
            |              |
     schema |              | value
            v              v
  +--------------+   +-----------+
  | Malli schema |   | EDN value |
  +--------------+   +-----------+
                           |  round trip
                           v
                +----------------------+
                | the same typed value |
                +----------------------+
```

«The Flow Nexus, whole» P3 proposes Ethos parts becoming namespaces, Malli schemas and EDN; «Short-term prototypes: Clojure now?» proposes the entry point, reader and launcher. This adds the shared translation contract inside them.

## Crystallization

### Proposal 1: One mapping keeps the Ethos anatomy

File: `psyche-context/skills/vision-clojure.md`, new

```text
+ ---
+ description: A Clojure prototype represents an Ethos type or a Datom value.
+ dependencies: []
+ ---
+
+ ## Clojure
+
+ The Clojure translation preserves the anatomy declared in Ethos: named types, struct positions, variant identity and payload, and nested containers. One shared construct mapping defines their Malli schemas and EDN representations, including how Datom values become those EDN values. Each representation keeps enough information to recover the same typed value.
```

Where the line lands:

1. `vision-clojure`, holding the Clojure representation of both Ethos and Datom.
2. `vision-ethos`, beside the schema language.

The next book shows the mapping itself, and the choices for variant representation and keyword casing.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->

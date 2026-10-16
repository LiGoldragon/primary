---
name: vision-clojure
description: A Clojure prototype represents an Ethos type or a Datom value.
dependencies: []
---

## Clojure

The Clojure translation preserves the anatomy declared in Ethos: named types, struct positions, variant identity and payload, and nested containers. One shared construct mapping defines their Malli schemas and EDN representations, including how Datom values become those EDN values. Each representation keeps enough information to recover the same typed value.

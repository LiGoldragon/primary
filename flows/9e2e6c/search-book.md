Presentation.{ «A grep index: the new module vision:search» }

# A grep index: the new module vision:search

### Proposal 1: psyche-belief › vision/search.md (new module)

**Comment** A new module, shown whole in green under the path it will have. Its lines are the Mind core Primary's judgment as relayed in Flow 14070: one index over transcripts and records, queried in Datom, answering with exact passages, paths, locations and source revisions. Nothing is implemented; this proposes the vision alone. The grep statistics the judgment rests on are carried from relay 14070 as attributed, not audited.

~~~diff
+ ---
+ description: One Datom-queried index locates written evidence over transcripts and records.
+ ---
+
+ Terms.
+ - Index: the one searchable store built over transcripts and records.
+ - Transcript: the file the harness writes holding one thread from beginning to end.
+ - Record: a psyche record, a belief module or a report kept in a repository.
+ - Query: a Datom value naming what is sought; the index answers it.
+ - Hit: one answer, carrying the exact passage, its path, its location in the file and the source revision it was read at.
+
+ What search is.
+ There is one index over transcripts and records. It is queried in Datom. It returns exact passages, paths, locations and source revisions.
+
+ Written evidence is located by the index, not by a flow's recollection of it. A flow that needs to know what was written asks the index and reads the hit.
+
+ Build-status polling stays outside the index: the index serves written evidence, and a build's state is observed where the build runs.
+
+ Grep statistics.
+ The load that grep put on the living's laptop, as relayed in Flow 14070, is the reason for the index. These statistics are attributed to that relay, not audited.
~~~

```
+----------------------+
| transcripts, records |
+----------------------+
         |
         | are indexed by
         v
+----------------------+
| the one index        |
+----------------------+
         |
         | answers a Datom query with
         v
+----------------------+
| hits: passage, path, |
| location, revision   |
+----------------------+
```

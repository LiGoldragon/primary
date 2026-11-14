Presentation.{ «One flow holds the artifact tools» Proposal }
# One flow holds the artifact tools

Created by Fable 5.1, who wrote this; nothing else helped.

### Proposal 1: One flow holds the artifact tools · psyche-belief › vision/book.md

**Comment** Addition, under "Publishing":

+ ## One flow holds the artifact tools
+
+ One Claude flow, the publisher, holds the artifact tools: it alone publishes a book, edits one, or reads his comments on one. Every other flow reaches a book by messaging the publisher: the source path to publish, or the book's title to recover its comments. The Flow Nexus leaves the artifact feature out of every other flow's launch.
+
+ ```datom
+ ; every permaflow but the publisher:
+ ; Artifact left out of its launch
+ Configure.Permaflow.{
+   { Psyche criomos Opus } None Claude
+   [ Artifact ClaudeMd GitInstructions ] }
+ ; the publisher alone keeps it
+ Configure.Permaflow.{
+   { Psyche book Haiku } None Claude
+   [ ClaudeMd GitInstructions ] }
+ ```

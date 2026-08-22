---
name: flows
description: 'A session is starting, or work has produced something with no home repository. Requires: vocabulary.'
---

One directory per flow: `flows/<short-id>/`, the short id being the
first 8 hex of the session UUID.

    flows/
      index.md
      <short-id>/
        log.md
        annotations.md
        vision/<topic>.md
        witnesses/<subject>.md
        reports/<subject>.md

A psyche record goes in `vision/<topic>.md`, the psyche's words
verbatim. A witness goes in `witnesses/<subject>.md` with its method:
`Method: probe <command>` or `Method: code read <path>`. A report goes
in `reports/<subject>.md` and ends with `## Sources` written as the
report is made: documents and URLs for carried claims, witness records
for own inference, flows by short id.

Files are named by camelCase subject; the log holds the dates; an
artifact's body holds only its subject. A subflow's artifacts go in its
flow's directory.

Earlier work is continued by reading the flows concerned and forming a
fresh view. An edit from outside the flow goes in that flow's
`annotations.md`, its entry headed by the editing flow's short id and
the artifact it concerns.

---
description: A subflow starts inside a flow's lane.
---

Your flow is `FLOW_ID` and `FLOW_DIRECTORY` in your environment. The harness or launcher records the current `THREAD_ID` for transcript and evidence provenance. In a PROVENANCE handoff, you receive only the readable artifact name, match or mismatch, and receipt handle. Until that receipt handoff exists, report unavailable provenance receipt evidence rather than obtaining or relaying the raw thread ID. For completed work, close its Beads with evidence and report their status when returning. Do not create a lane, index entry, or log. Create a report or witness only when the main flow delegates it or a named tool or flow will consume it, and load `flow-evidence` before creating it.

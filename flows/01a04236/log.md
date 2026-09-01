# Codex transcript investigation

This flow is investigating what Codex transcripts contain, what archival does, how subflows are represented and retained, how large hidden command outputs can be, and how important information could remain accessible with much less storage.

Remembered: e06e4c07, cff271af, aa4c7747, 01a03d6e — depth 1 — transcripts were envisioned as a separately searchable nexus; typed intent and nearby responses are the first retrieval surface; compact reviewed distillation links to rather than replaces raw evidence; flow logs expose main points; subflows remain flows with explicit lifecycle identity.

Settled: Codex 0.149.1 archives by moving the rollout and updating SQLite, with separate later cold compression. Parent archival walks its subflow descendants but is best-effort rather than atomic. Direct measurements cover storage, JSONL schema, byte shares, inline command/tool/image duplication, UI history projection, and subflow metadata. A compact design should separate human recall, agent continuation, and exact compressed provenance.

Published: the private Codex Reports hub at https://codex-reports-hub.ligoldragon.chatgpt.site now carries this investigation as its first remotely accessible report and is the durable destination for later flow reports and visuals.

Open: writer flush/rotation and malformed-line durability; exact tool-output truncation and resume requirements; corpus-wide compression/deduplication yield; retention authority, holds, expiry, ACLs, restore latency, and canonical collision-safe flow identity.

Historical child-lane consolidation: archive-lifecycle evidence and compact
retention research now live with this root lane. Their transcript provenance is
the distinct child threads `01a04237-242c-7332-9fa4-52681028c93b` and
`01a04237-6379-76a2-95de-f7e9edfca8ea`; the latter is a transcript identity,
not a separate flow lane.

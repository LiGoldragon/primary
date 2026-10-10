# Compact handoff from b7ba00

`b7ba00` was the Psyche Fable successor of `b860be`, designated integration
head and oracle. It remembered `b860be` at depth one and produced the durable
Psyche design work in its `reports/` and `vision/` directories.

The pre-power-loss registrations and readiness claims are historical only. The
recovery must not resume `b7ba00`, reuse its Message binding, or assume its
old `messaging-build` pane survives. Claim a fresh identity, then establish a
new Flow and Message binding after native acceptance.

The immediate recovery purpose is to restore Psyche's integration authority:
receive Field and Mind reports, preserve the living's latest recovery request,
and coordinate without duplicating the prior Fable. The living asked for nine
restored flows, named Fable and Opus among them, and set all model effort to
medium for this recovery.

Unfinished predecessor work remains durable evidence, not an instruction to
resume blindly: its log records a pending CriomOS integration check and
fast-forward decision, Messenger and Flow recovery sequencing, and the
handoff of integration reporting. Reassess those items after the fresh seat's
route and authority are live.

The living directs recovery through the newer Flow Nexus. Hold this fallback
packet while Flow 0.17.1 and Message 0.17.0 are deployed and proven; prefer
their Start/Bind path when it supplies native acceptance and a live route.

Sources: `flows/b7ba00/log.md`,
`flows/b7ba00/receipts/readiness-announce.md`, and
`flows/b7ba00/vision/modelFlows.md`.

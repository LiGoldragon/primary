# Corrected per-address delta: exact generated wake gap

Independent nonauthor same reviewer/native01a1adff-cafa-77a1-aa73-aa98b4dd4794,23:25:20–23:26:02UTC, proposalSHA6515848c9e12c11b8ce4847aede233c8101afb39f93f9540c8e477abeabbcc24. Flow916b545/meta281f5aa/signalce083f2 and sourceledgerbcb335 pinned unchanged. Read-only/noeffects; parent lands findings.

**GAP — approved wake outcomes are not representable by exact current generated contracts. Declaration bodies held.**

- operation.ethos115–130/generatedoperation.rs140–157 Failed_Data has neither Undeclared nor NotConfigured.
- waking.rs468–488 WakeRefusal has neither direct case. StartRejected(StartRejection) can carry Undeclared but StartRejection signal.ethos505 has no NotConfigured.
- AnswersWakeRefusal496–524 maps StartRejection::Undeclared→Failed_Data::Unstarted, losing exactmeaning. CompositionRefused(Unconfigured) maps a different superseded label, not approved NotConfigured.
- RetryCause can retain WakeRefused(StartRejection::Undeclared) (signal.ethos619–621) only if explicitly journaled on early refusal, but no NotConfigured carrier exists. Public Refusal::NotConfigured/PrivateSendResponse exists; Operation::Wake→Outcome::Failed cannot carry Refusal. sending.rs1326–1328 currently ignores wake outcome.

Exact allocation/design judgment is required for wake-local generated variant/projection through Operation outcome and retry/public boundary; do not extend shared Refusal for symmetry or invent labels. Missing and present-unresolved Wake/Refresh acceptance must prove held native seat+queuedrequests unchanged and no successor/close/drain.

Other corrected rows PASS: Launch/Refresh can already express StartRejection::Undeclared, RefreshRejection::Undeclared and Response::Refused(Refusal::NotConfigured); presentrootNone SourceRoot preserved; profile/NoneOnDemand fallback removal explicit. All prior producer/test omissions nowlisted. Transitivearchives: only ConfigureMetaflow is stored; operation variants wire-only; frozenV5→V6 CONFIG is sole evidencedMemory migration.

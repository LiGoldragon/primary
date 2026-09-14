# Claude prompt identity at hook time

Codex report to Fable, 2026-09-14. This is a throwaway-session witness using synthetic input and a localhost refusal endpoint. No live Fable settings, real provider credentials or production hook were changed.

Fable proposed testing whether the transcript user record already exists when `UserPromptSubmit` runs, before considering a persisted counter. The actual hook ran, but its transcript file did not yet exist. The transcript-first candidate is therefore not supported for this witnessed path.

The same witness exposed a better candidate that the documentation-based investigation missed: this installed runtime includes `prompt_id` in the hook input. A corrected probe retained its value:

- `session_id`: `c1d95bbb-8917-4df2-8db3-08ea1b0ebee1`.
- `prompt_id`: `f162c07f-fa11-4b4d-8990-b31ce13a2673`.
- The hook's prompt exactly matched the synthetic probe phrase.
- The transcript file was absent at hook time; no matching user row was read.

The first probe recorded only input field names and omitted the value of `prompt_id`. Root noticed that field in the report and requested the corrected capture. Two throwaway probes were therefore used, not one; neither implemented the counter fallback. The field's presence in actual runtime input supersedes the earlier inference from the documented schema that no ID is available.

The observer requested exit2. The probe process exited0 and counted two requests to the local refusal endpoint. These facts do not prove that exit2 suppressed every attempted API request, and the report does not claim that. The endpoint used an inert credential and never forwarded requests to a provider.

Codex proposes using `claude/<session_id>/<prompt_id>` as the candidate source-event identity for this pinned runtime, rejecting missing/invalid IDs. This is a proposal based on an observed field, not proof of its stability across retries or its equality with a later transcript record. Those relationships still need a witness before relying on them. Prompt-text hashes and a new counter have not been implemented. The registered process authenticates the submitter, not human authorship of a payload.

## Sources

- [Retained machine-readable witness](/home/li/primary/flows/34d94e/evaluation/hook-ordering/hook-ordering-report.json)
- [Hook observer](/home/li/primary/flows/34d94e/evaluation/hook-ordering/observer.mjs)
- [Isolated probe runner](/home/li/primary/flows/34d94e/evaluation/hook-ordering/probe.mjs)
- [Prior daemon and hook-seam report](/home/li/primary/flows/34d94e/reports/integratedMessengerPoc.md)
- Fable's provenance-labelled council message requesting candidate(a) first, received in this root thread.

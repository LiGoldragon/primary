# Claude prompt identity at hook time

**Superseding interactive evidence:** session plus `prompt_id` is not a unique input-event key on the witnessed Claude Code 2.1.263 runtime. The accepted candidate below must not be activated.

Root ran a real isolated PTY session and then resumed that same session, using an inert key and a localhost endpoint that held requests without forwarding them. The first prompt was active; a different second prompt was visibly queued. Both hook invocations carried session `5d391940-9b0d-4d10-8648-1e1b552b55e1` and prompt ID `4116f28a-132f-450f-88c9-c1ff220f0b73`. The transcript contains the first user row and a separate enqueue operation for the second text. A source-plus-event dedupe contract using this candidate would reject or collapse a legitimate distinct queued prompt.

After SIGTERM and actual `--resume`, the first user turn appeared. The enqueue row remained in the transcript, but the queue was not shown or replayed in the bounded idle observation. No second hook invocation on resume was witnessed. This does not establish all resume behavior; the independently sufficient finding is the collision between two distinct hook inputs before shutdown. Both owned child processes were reaped. Local endpoints counted three start-phase requests and one resume-phase request, with no provider forwarding.

Earlier delegated onboarding attempts did not establish that external authentication was required. One declined the inert key and selected Console OAuth. Root instead used temporary onboarding preferences and inert-key approval, then confirmed trust in the newly created throwaway directory. No real settings, keys or transcripts were changed or fabricated. The retained [interactive witness](/home/li/primary/flows/34d94e/evaluation/hook-ordering/interactive-resume-report.json) and [runner](/home/li/primary/flows/34d94e/evaluation/hook-ordering/interactive-probe.mjs) supersede those route-specific limitations. No replacement event-ID scheme has been silently chosen.

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

## Follow-up: pinned runtime and replay limit

Fable accepted `session_id` plus `prompt_id`, with missing fields rejected and no hash or counter fallback. The witnessed executable is Claude Code **2.1.263**, realpath `/nix/store/zh1h1zpcqrh447252d9gcg96h1fygzb5-claude-code-2.1.263/bin/claude`, SHA-256 `5c45921517d2162c198d52ffc6d7f0e0f624d8f77fee069b7e223f07bb7bb7a4`. The field is an observed runtime extension, not a documented compatibility guarantee.

The corrected stream-input probe submitted two SDK user envelopes with the same input UUID. It recorded one `UserPromptSubmit` event, with session `76757e68-66b9-4a8c-a535-10ae75c9b732` and prompt `95662095-3f34-4597-a5fe-9c2892c40070`. The hook ID differs from the supplied SDK UUID. Exit was zero, stderr empty, and two localhost refusal requests occurred. This is consistent with input deduplication or coalescing, but does **not** witness a second hook invocation retaining the same ID across retry or resume. That requirement remains unproved. Earlier exit-one runs omitted the stream-output `--verbose` flag and discarded stderr; they establish no harness limitation.

The probe uses an appending hook observer, an isolated temporary home and working directory, an inert key, and a localhost server that never forwards. No live human hook is activated. A later upgrade must fail closed if the ID disappears. Readiness and durable-admission work can proceed under the council's bounded POC agreement while this retry limitation stays explicit.

## Sources

- [Replay witness](/home/li/primary/flows/34d94e/evaluation/hook-ordering/hook-replay-report.json)
- [Replay runner](/home/li/primary/flows/34d94e/evaluation/hook-ordering/replay-probe.mjs)
- [Appending observer](/home/li/primary/flows/34d94e/evaluation/hook-ordering/replay-observer.mjs)

- [Retained machine-readable witness](/home/li/primary/flows/34d94e/evaluation/hook-ordering/hook-ordering-report.json)
- [Hook observer](/home/li/primary/flows/34d94e/evaluation/hook-ordering/observer.mjs)
- [Isolated probe runner](/home/li/primary/flows/34d94e/evaluation/hook-ordering/probe.mjs)
- [Prior daemon and hook-seam report](/home/li/primary/flows/34d94e/reports/integratedMessengerPoc.md)
- Fable's provenance-labelled council message requesting candidate(a) first, received in this root thread.

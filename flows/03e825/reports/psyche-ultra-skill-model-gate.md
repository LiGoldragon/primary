# Psyche Ultra skill-model gate

The parent's one guarded `--continue-partial` operation used the published `e2922a21` helper against the existing Claude process in `wD:p8`. It retained the same pane, process, and native session UUID and did not replay provisional rename or `/spirit`. The run artifacts are under `flows/03e825/psyche-ultra-partial-continuation/`; stdout is empty, and no output receipt was produced.

The bounded cursor observation records twelve native skill commands in total, beginning with the earlier `/spirit` and reaching `/main-flow`. The remaining continuation sent `/psyche` through `/main-flow`. It did not send `/refresh`, the source bundle, or `BOOTSTRAP_READY`. The assistant metadata after `/visual-report-from-md` showed `claude-sonnet-5`; the later `/main-flow` response at 21:06:48 UTC showed the exact dated Haiku model again. The helper's line 575 error reported expected `claude-haiku-4-5-20251001/medium` and observed `claude-sonnet-5/medium`. The error likely read the preceding skill turn before the later `/main-flow` response completed; that sequence is an inference from the bounded timeline, not a captured helper cursor trace. A native skill may have its own model override, but this report does not establish its mechanism or change the skill.

The currently observed transcript identity is exact Haiku with medium effort, but the effort value may come from a different turn than the Haiku model. The existing Claude process argv still indicated the expected model and medium effort; process arguments do not establish the transcript-wide model/effort policy. The partial session remains live and must be preserved. There is no complete skill/source delivery, readiness receipt, own Flow claim, final canonical title, HM binding, or Ultra acceptance. No replay, extra input, or source edit was made by this report.

## Sources

- `flows/03e825/psyche-ultra-partial-continuation/manifest.json`: requested exact model, effort, role, title plan, and structured skills.
- `flows/03e825/psyche-ultra-partial-continuation/stdout.json` and `stderr.txt`: empty stdout and exact helper line 575 native identity error.
- `flows/03e825/psyche-ultra-partial-continuation/cursor-observation.json`: bounded command/model timeline, snapshot digest, and latest observed identity; no full transcript copy.
- Parent's direct managed continuation and same-process observation; `flows/03e825/reports/psyche-ultra-partial-bootstrap.md` for the earlier `/spirit` delivery.

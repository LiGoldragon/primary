# Psyche Ultra partial native bootstrap

The parent ran one guarded `bootstrap-running-empty` operation at 2026-09-21 20:33:57 UTC against the existing Haiku process in the retained `wD:p8` pane, using the published `91485ada4` helper. The manifest, empty stdout file, and stderr are retained under `flows/03e825/psyche-ultra-running-bootstrap/`. The running session, native UUID, pane, and process were preserved; no second Claude launch was made.

The parent's direct transcript metadata read showed delivery of the provisional title and the first `/spirit` command with native expansion. The assistant acknowledged and identified the exact dated Haiku model. No tool use was observed. The helper then stopped at its line 487 identity check: manifest expected `claude-haiku-4-5-20251001/medium`, while transcript identity yielded `claude-haiku-4-5-20251001/None` for effort. The earlier process argv contained `--effort medium`; that process argument does not substitute for missing transcript effort metadata. The helper emitted no output receipt.

The parent's bounded `partial-observation.json` stores the observed identity as exact dated model with `effort: null`, provisional titles, the actual `/spirit` command marker, and a transcript snapshot digest. It does not copy the full skill or transcript.

The remaining twelve skills, source bundle, and `BOOTSTRAP_READY` marker were not delivered. The provisional title is not a final canonical title. There is no own Flow claim, HM binding, complete source/skill acceptance, or Ultra readiness. The partial native transcript and running process must be preserved. Do not replay the initial bootstrap into this session; any continuation needs a source-owner plan for the observed effort metadata boundary.

## Sources

- `flows/03e825/psyche-ultra-running-bootstrap/manifest.json`: exact requested model, effort, role, title plan, and structured skills.
- `flows/03e825/psyche-ultra-running-bootstrap/stdout.json`: zero bytes; no successful output receipt.
- `flows/03e825/psyche-ultra-running-bootstrap/stderr.txt`: Python line 487 identity mismatch with observed transcript effort `None`.
- `flows/03e825/psyche-ultra-running-bootstrap/partial-observation.json`: bounded native transcript metadata and digest, with observed effort `null`.
- Parent's direct native transcript metadata read after the single guarded operation: provisional title, `/spirit` command and native expansion, model acknowledgment, no observed tool use; delivery stopped before the rest of the bootstrap.
- `flows/03e825/reports/psyche-ultra-native-bootstrap-gate.md`: prior running-process observation and its distinct evidence grade.

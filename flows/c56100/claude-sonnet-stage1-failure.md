# Claude Sonnet Stage 1 failure witness

- Attempted at 2026-09-27T08:45:20Z using standalone Claude 2.1.280.
- Requested native session UUID: `51ffe00d-27c7-4352-8043-bbd95ffa122e`.
- Requested identity: `claude-sonnet-5`, `medium`.
- CLI was given a positional bootstrap prompt, `-p`, `--dangerously-skip-permissions`, `--session-id`, and `--output-format stream-json`; it was not given `--stdin`.
- Exit status: `1` before output. Exact stderr: `Error: When using --print, --output-format=stream-json requires --verbose`.
- The stream capture was zero bytes. No native transcript, assistant turn, Skill invocation, Skill result, model/effort observation, Flow identity, route, edit, lock, test, build, or Stage 2 continuation was created.

The Stage 1 receipt gate therefore failed. This UUID is not resumable. Do not retry under this authorization; a later authorization would need a fresh UUID and a corrected invocation including `--verbose`, then must independently verify the required native transcript receipts before any Stage 2 work.

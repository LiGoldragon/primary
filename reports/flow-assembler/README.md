# First-prompt assembler prototype

Verdict: a report-only assembler prototype can make the approved refresh inputs explicit without launching a successor.

`tools/flow-prompt-assembler.mjs` accepts one JSON input file and prints one assembled text artifact. It requires the predecessor lane, successor identity, system-prompt file, exactly one user-prompt string, Spirit, relevant Intent and Vision, topic, raw-vision provenance, open log items, and a skills list. It has no socket, scheduler, hook, fan-out, or harness-launch code.

The fixture binds predecessor `692df8` to successor session identity `05c6048e-2e71-4f39-96dc-0937b92969c6` while using its actual lane `flows/05c604`. Its raw-vision source is `flows/692df8/vision/logging.md`. That file identifies the entry as typed, but this checkout contains no transcript path for it; the fixture therefore records `NOT AVAILABLE IN FIXTURE`, rather than inventing provenance.

Run the behavioral witness with:

`node --test tools/flow-prompt-assembler.test.mjs`

The test runs assembly only. It observes the rendered handoff includes both identities, the explicit unavailable-provenance marker, and the selected skills. The prototype contains no harness-launch interface.

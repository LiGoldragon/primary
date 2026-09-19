# PsycheHigh Fable launch plan

The authorized target is a new `PsycheHigh` Fable seat named
`psyche-fable-of-c8d79f`, with predecessor `c8d79f`,
`claude-fable-5-1[1m]`, and medium effort. The protected predecessor remains
untouched until the successor has a native refresh receipt, its acceptance,
and a safe final-reply boundary.

The launch manifest must be produced from the fresh full-source inventory,
not the historical selected manifest at
`flows/b81560/reports/luna-manifest.json`. It must contain every frozen
`{path, sha256}` source, the named native skills, role, model, effort, title,
receipt path, and `cwd`. The same source vector is passed as `system_sources`
so the Claude appended system prompt is assembled from verified authored
material rather than hand-written text.

Execution has two receipt-only phases. First, the controller launches the
guarded native Claude process with persistence forced and the inherited child
marker removed:

```
tools/claude-bootstrap-controller.py --manifest <frozen-manifest.json> \
  --launch-bootstrap --acknowledge-live-launch
```

It persists `bootstrap-created` with the returned UUID and does not activate
the seat. It also writes the UUID into `refresh_manifest_path`, a copy of the
same frozen source manifest. That exact file is given to
`tools/claude-native-seat-refresh.py --refresh
--acknowledge-live-refresh`; that existing helper verifies every source hash,
waits for idle, invokes each native skill, and requires the frozen-payload
acknowledgement. Save its JSON receipt, then record it with
`claude-bootstrap-controller.py --manifest <frozen-manifest.json>
--record-native-refresh <native-refresh-receipt.json>`. Only this matching UUID
receipt changes the controller receipt to `bootstrap-ready`, which permits the
existing activation gate.

This plan is blocked pending the fresh whole-set source manifest and an answer
on the absent requested `flows/b81560/reports/herder-messaging-detailed.md`.
The available lightweight report is not a substitute. The direct local
artifact-comment evidence is also still to be selected explicitly by the
parent rather than inferred from a secondary report.

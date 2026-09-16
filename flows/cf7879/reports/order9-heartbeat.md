# Order 9 — core heartbeat proof

## First owed wake

Corrected order 8 packet is published at `07d23d8b2ad8` on `flow/cf7879`,
`flows/cf7879/handoff/successors-v6-reviewed/`; assembly, complete-body checks
and launch dry-run passed. V5 is retained as Codex launch evidence. No Claude
launch performed. Full package receipt is in `to-efa157.md`.

Root attempted the supported prompt-relay Claude route with explicit peer-file
input and full efa157 session UUID. Exit 2: `Claude delivery refused: session
efa15708-dc5d-42ce-af62-8ffb84c9815e is not uniquely witnessed idle`. The roster
read showed busy/working. Receipt is **FileOnly**, not Accepted or
TranscriptWitnessed; the published report exists but is not evidence of reading.
No permission gate was bypassed.

## Quota and cadence

The existing monitor NDJSON line for account.primary at
2026-09-16T15:52:45.106Z records 16 percent remaining (observedAt
15:52:39.020Z). Root's supported account/rateLimits/read at 15:59:47.362Z
independently returned 84 percent used of a 10080-minute window, reset
2026-09-19T15:05:28Z. No reset credit consumed.

Proposed interval: at least 50 percent left, 15 minutes; at least 20,
30 minutes; at least 5, 60 minutes; below 5, 120 minutes. Unknown/stale quota
must be explicit and conservative. Each run records the selected interval and
rule. Source implementation and execution receipts follow after review.

## Boundaries

The existing core main is e43002, native thread
01a0a792-2d0e-7a53-ac0b-9b3e43002941. This work adds a proposal for its checkup
seat, not another main. Secondary owns timer activation. No repairs, restarts
or settings edits are authorized by this heartbeat proof. A Luna decision is
not evidence of propagation: actual transport and recipient receipts determine
the reported result.

## Review criteria

- A missing, stale or malformed quota observation selects a documented fallback,
  and never claims a fresh balance.
- The collector names the revision and prompt source for each configured lane;
  unavailable lanes stay unavailable, rather than appearing unchanged.
- Model output must select a known event and known source/recipient identities.
  Unknown enums, fabricated IDs and malformed output cause a typed refusal.
- Transcript/report text is evidence, not instructions for the checker. The
  checker cannot execute commands or request arbitrary paths.
- A quiet run sends nothing. A repeated event with a witnessed receipt is
  suppressed; pending recipients remain eligible for retry.
- A busy Claude route stays pending. Queue acceptance and native transcript
  receipt remain distinct. A file-only result does not claim a recipient read it.
- Test payloads are independent files. Process fixtures prove the bounded local
  seam; only a real Luna model response and a real recipient record prove those
  respective external boundaries.

## First wake delivery completed

A later root retry after the session became idle returned
`claude-bytes-written-to-pty`, exit 0. Root then read the actual native Claude
`type:user` record `39c4c849-88a3-4e9a-ab46-6aad0c42ac99` at
2026-09-16T16:04:58.916Z in
`/home/li/.claude/projects/-home-li-wt-github-com-LiGoldragon-primary-claude-successor-840e42-bootstrap-local--claude-worktrees-claude-successor-840e42/efa15708-dc5d-42ce-af62-8ffb84c9815e.jsonl`.
It contains the package-ready peer message, source SHA256
`3eed244dc5784b1a1bc7b678a0b98c53ddbfbcd00d996f3cd1a9408850be955b`.

Recipient **efa157**, route **prompt-relay Claude PTY**, receipt
**TranscriptWitnessed**. This supersedes the earlier pending first wake, and
should suppress a duplicate notification. It is an actual peer message in the
recipient transcript, not evidence that the still-being-built heartbeat sent
it. The existing prompt-relay JSON provenance header remains; replacing it with
a datom head is separate order 10 work, not claimed done here.

## Published proof and execution receipts

Producer: primary `proposal/cf7879-core-heartbeat`, exact revision
`99285db2784c681928016736f64752e57caa934a`. Workspace
`/home/li/wt/github.com/LiGoldragon/primary/heartbeat-cf7879`. The inherited
core-checkup ancestry is not an integration candidate: extract only the heartbeat
tool, adapter/base, fixtures/tests, documentation, example configuration, timer
source and heartbeat-fixtures flake entry. No main or installed unit changed.

What was put together: a five-minute timer poll with persisted quota-based
15/30/60/120-minute gating before model calls; read-only bookmark/report/user
record collection; one restricted ephemeral gpt-5.6-luna call with custom base;
validation of major enum, candidate ID and recipient allowlist; code-built
Codex queue / idle-only Claude prompt-relay argv; per-recipient acceptance state,
transcript witness promotion and retry of still-pending recipients; append-only
report file and atomic state with flock. Typed prototype output is validated
JSON Heartbeat/v1, not yet a generated Ethos/datom contract. Order 10's datom
header replacement remains separate and is not claimed complete.

The private Luna app-server runs in a temporary directory. Empty environments,
dynamic tools and capability roots plus explicit disabled execution/web/apps/
plugins/agent/image/MCP settings remove action surfaces per inspected harness
source. The program discovers only MCP server names internally to disable them;
no credentials enter the model snapshot. The real runs observed only user,
reasoning and assistant items. This is source construction plus bounded run
evidence, not a claim that a read-only sandbox alone hides credentials.

Validation: root ran 8 local tests; the worker ran the exact-revision Nix check
on Prometheus using --max-jobs 0 --no-link: 8 passed, 0 failed. Derivation
`/nix/store/pmsw8r6xa1mf9nn2vmqjifdx8g8mpvff-primary-heartbeat-fixtures.drv`,
output `/nix/store/9lrldwqrxl3xgzsgkq31hrs2yi1gsdn7-primary-heartbeat-fixtures`.
The tests cover real child fixture payload handling, actual transcript record
shapes, wrong-window quota refusal, cadence suppression, per-recipient retries,
unknown decision refusal and restricted-boundary refusal before a model turn.
They do not prove production timer activation.

The first actual Luna attempt accepted thread restrictions but failed because
ephemeral threads reject includeTurns. The adapter now consumes native
item/completed and turn/completed notifications; the subsequent real fixture
call returned successor_ready. Root then ran two real curated cluster snapshots,
the final one with sends enabled. It returned none: the package wake was already
transcript-witnessed, so no duplicate message was sent. This is a real Luna
classification and no-send witness, not a new automatic peer-delivery witness.
The first required package wake has the separate root-executed receipt above.

The final collector observed primary Claude, cf7879 and d9961c bookmark tips and
all six last user records. Configured secondary/core bookmark reads were
unavailable; reports/transcripts remained available. Secondary must supply the
actual active revision pointers before treating this as complete cluster tip
coverage. Claude's next successor is added after actual identity/launch receipt.
Other limitations: local refs are not auto-fetched; long records may exceed the
bounded transcript tail; report/state retention needs activation policy; a crash
in the transport-send/receipt-commit gap remains ambiguous, so exactly-once
propagation is not claimed. Message receiptReport names the final report path;
only prior receipts can honestly be embedded before a send finishes.

Final actual tick receipt:

```json
{
  "directory": "/tmp/heartbeat-cluster-cf7879-1dnJ6T",
  "lanes": [
    {
      "flow": "efa157",
      "status": "observed"
    },
    {
      "flow": "cf7879",
      "status": "observed"
    },
    {
      "flow": "d9961c",
      "status": "observed"
    },
    {
      "flow": "57a7aa",
      "status": "unavailable"
    },
    {
      "flow": "348e7b",
      "status": "unavailable"
    },
    {
      "flow": "e43002",
      "status": "unavailable"
    }
  ],
  "candidates": [
    {
      "id": "e424ae794b8fc0871eca35d73ecb8c6a95af932f4fefb1bd8fda4ce69193a7d1",
      "kind": "lane_tip",
      "flow": "efa157"
    },
    {
      "id": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "kind": "user_turn",
      "flow": "efa157"
    },
    {
      "id": "03f959c87082f86f2af28c455cd14f6343c4343c04ea00d28d94e14fbe025a94",
      "kind": "lane_tip",
      "flow": "cf7879"
    },
    {
      "id": "adfb0505aeb25194da0787b4b0eec03fc92f6d9f85fb367f76425bb169caf4a1",
      "kind": "user_turn",
      "flow": "cf7879"
    },
    {
      "id": "36b6d2d9856f5302198807fa3e952fabfb4d41ac09d1ddbf252495ebb083e450",
      "kind": "lane_tip",
      "flow": "d9961c"
    },
    {
      "id": "e34731a20604c1f42ffb59563dd4bfbe683e4f7f4117fe420d689c2aee91d614",
      "kind": "user_turn",
      "flow": "d9961c"
    },
    {
      "id": "1e855e04c2372786d185a7f577804f5677006affcedcc0a9de36a9516a303bdd",
      "kind": "user_turn",
      "flow": "57a7aa"
    },
    {
      "id": "4fdd83a34cfbc9f9203a43c4d9140c6c96c334cdc43151148090d4a46e646025",
      "kind": "user_turn",
      "flow": "348e7b"
    },
    {
      "id": "ab96056a6c1baa4911bb17a225479a0dbc65fbf9c6d3425b92bb2282906117eb",
      "kind": "user_turn",
      "flow": "e43002"
    }
  ],
  "result": {
    "schema": "heartbeat/v1",
    "at": "2026-09-16T16:19:46.651Z",
    "kind": "heartbeat",
    "interval": {
      "minutes": 60,
      "reason": "quota_observed"
    },
    "quota": {
      "remainingPercent": 16,
      "observedAt": "2026-09-16T15:52:39.020Z"
    },
    "decision": {
      "major": "none",
      "sourceId": null,
      "summary": "No unpropagated major event is supported. The corrected v6 package readiness and dry-run result were already transcript-witnessed by efa157; successor readiness was acknowledged by cf7879. Other evidence describes pending, gated, or already reported work without a distinct new propagation target.",
      "recipients": [],
      "witness": {
        "stage": "completed",
        "boundaryAccepted": true,
        "threadId": "01a0ab04-63e3-7aa2-a3c6-197de9272d7e",
        "turnId": "01a0ab04-641b-7640-8b68-c5e8a22cd78e",
        "model": "gpt-5.6-luna",
        "modelProvider": "openai",
        "observedItemTypes": [
          "userMessage",
          "reasoning",
          "agentMessage"
        ],
        "outputSha256": "d1020d4afb28e5607efc00c376e595a67d80d24105e3701a3007a2bef448241d",
        "outputUtf8Bytes": 358,
        "request": {
          "model": "gpt-5.6-luna",
          "ephemeral": true,
          "sandbox": "read-only",
          "environments": "empty",
          "dynamicTools": "empty",
          "selectedCapabilityRoots": "empty",
          "configKeys": [
            "agents.enabled",
            "features.apps",
            "features.code_mode",
            "features.code_mode_host",
            "features.code_mode_only",
            "features.enable_mcp_apps",
            "features.image_generation",
            "features.multi_agent_v2",
            "features.plugins",
            "features.request_permissions_tool",
            "features.shell_tool",
            "features.view_image",
            "mcp_servers.agent-intercom.enabled",
            "mcp_servers.cua_repl.enabled",
            "mcp_servers.node_repl.enabled",
            "mcp_servers.openaiDeveloperDocs.enabled",
            "tools.experimental_request_user_input.enabled",
            "tools.update_plan.enabled",
            "web_search"
          ],
          "mcpServerCount": 4,
          "baseSha256": "fdcbd7f12711dffdc9f5334a955abb110a83b237cf450539a60c6d133900d517",
          "baseUtf8Bytes": 1008
        }
      }
    },
    "deliveries": [],
    "file_report": {
      "receipt_kind": "file_only"
    },
    "identity": null
  }
}
```

Activation remains secondary-owned. No repairs, restarts, settings edits, reset-credit use or timer activation occurred in this proof.

# Flow CLI POC

This Python-stdlib prototype uses SQLite only as a local test adapter. It does **not** implement production Nexus, Sema, Signal, authentication, provisioning, or Curriculum. The fixture harness is a clearly named mock provision receipt.

`flow.py start 'short goal' [--type ordinary] [--model MODEL]` creates an opaque stable Flow ID and waits on a bounded readiness pipe; `Popen` alone is never reported as running. `restart [ID]` reads the trusted bridge solely from `FLOW_BRIDGE` (no parent/session CLI flags), checks that its stored session resolves to its stated Flow, then checks that Flow against the target. It prints an `accepted` event before the successor is ready and `running` only after readiness. A ready successor retires the old owned process group; failed readiness preserves the prior running generation. Duplicate request keys are idempotent. `--self-restart` is a fixture-only proof that a live fixture can stamp and issue its own restart request.

The bridge JSON must have `flow_id`, `session`, `turn`, `request_key`, and `transcript_ref`. It is cooperative/semi-secure local provenance: a same-user peer can forge its file. Transcript bodies are intentionally absent from the Flow database; only a Mind reference is stored. A missing bridge is explicit; when a harness session exists but lacks a turn it is `missing-turn`, otherwise it is terminal.

Run hermetic tests without repository bytecode artifacts:

```sh
cd tools/flow-cli-poc
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_flow.py
```

The real adapter passes the stored model to Claude stream JSON or Codex exec JSON, captures the native session/thread event, and requires a bounded one-turn completion before readiness. A bounded native `exec` turn is stored as `completed`, even while its receipt supervisor remains live; `show` reports that supervisor liveness separately. Fresh POC Flow IDs are random opaque values; Creo can later preserve aliases and verify them. A `flow-id` Codex adapter should read `CODEX_SESSION_ID`, reject `--parent-session`, normalize UUID hyphens and take characters 23:29, extending on collision; Claude UUIDv4/v5 starts with six characters and extends. Marker lanes need `0700`, markers `0600`, and `flock`; parent reruns return the existing identity. PID signalling verifies `/proc` start identity, but crash recovery, durable external supervision, and cross-host security are intentionally unimplemented.

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const index = JSON.parse(readFileSync(new URL("../codex-lane-index.json", import.meta.url), "utf8"));
const ids = {
  primary: "01a0a715-2d5d-7342-b278-1dbcf78795bd",
  secondary: "01a0a11f-6130-70e2-80b1-796348e7b086",
};
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

test("records a refresh-bound review snapshot", () => {
  assert.equal(index.schema, 1);
  assert.equal(index.snapshot.kind, "refresh-bound lane-index snapshot");
  assert.equal(index.snapshot.freshness, "snapshot only; not live authority");
  assert.match(index.snapshot.observedAt, /^2026-09-16T09:02:07-06:00$/);
  assert.equal(index.snapshot.provenance.sourceFlowId, "efa157");
  assert.equal(index.snapshot.provenance.sourcePath, "flows/efa157/log.md");
  assert.equal(index.snapshot.provenance.claimedSourceRevision, "2265e56a");
});

test("contains exact reviewed UUIDs with lane-index authority", () => {
  for (const [layer, threadId] of Object.entries(ids)) {
    const record = index.layers[layer];
    assert.equal(record.state, "current");
    assert.equal(record.authority.kind, "lane-index");
    assert.equal(record.threadId, threadId);
    assert.match(record.threadId, uuid);
  }
});

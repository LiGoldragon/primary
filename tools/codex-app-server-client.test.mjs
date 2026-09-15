import assert from "node:assert/strict";
import test from "node:test";
import { createAccountClient } from "./codex-app-server-client.mjs";
import { renderSituationReport } from "./quota-situation-report.mjs";

const readings = () => ({
  rateLimits: {
    rateLimits: {
      primary: { usedPercent: 35, windowDurationMins: 10_080, resetsAt: "2026-09-19T15:05:28Z" },
      codex_bengalfox: { fiveHourUsedPercent: 0, weeklyUsedPercent: 0 },
    },
    rateLimitResetCredits: { availableCount: 3 },
  },
  usage: { dailyUsageBuckets: [] },
});

const fakeTransport = (results, calls = []) => ({
  async request(method, params) {
    calls.push(["request", method, params]);
    const result = results[method];
    if (result instanceof Error) throw result;
    return result;
  },
  async notify(method, params) { calls.push(["notify", method, params]); },
});

test("performs the local app-server initialization then reads both exact account methods", async () => {
  const calls = [];
  const fixture = readings();
  const client = createAccountClient({
    transport: fakeTransport({
      initialize: { serverInfo: { name: "app-server" } },
      "account/rateLimits/read": fixture.rateLimits,
      "account/usage/read": fixture.usage,
    }, calls),
    now: () => "2026-09-15T18:32:38Z",
  });

  const input = await client.read();
  assert.deepEqual(calls, [
    ["request", "initialize", { clientInfo: { name: "quota-situation-report", version: "1" } }],
    ["notify", "initialized", {}],
    ["request", "account/rateLimits/read", {}],
    ["request", "account/usage/read", {}],
  ]);
  assert.equal(input["account/usage/read"], fixture.usage);
});

test("rejects malformed percentages from the account endpoint", async () => {
  const fixture = readings();
  fixture.rateLimits.rateLimits.primary.usedPercent = 101;
  const client = createAccountClient({
    transport: fakeTransport({ initialize: {}, "account/rateLimits/read": fixture.rateLimits, "account/usage/read": fixture.usage }),
    now: () => "2026-09-15T18:32:38Z",
  });
  await assert.rejects(client.read(), /rateLimits\.primary\.usedPercent/);
});

test("retains both Spark windows and calculates the primary window from its declared duration", async () => {
  const fixture = readings();
  fixture.rateLimits.rateLimits.primary = { usedPercent: 50, windowDurationMins: 60, resetsAt: "2026-09-15T01:00:00Z" };
  fixture.rateLimits.rateLimits.codex_bengalfox = { fiveHourUsedPercent: 25, weeklyUsedPercent: 75 };
  const input = await createAccountClient({
    transport: fakeTransport({ initialize: {}, "account/rateLimits/read": fixture.rateLimits, "account/usage/read": fixture.usage }),
    now: () => "2026-09-15T00:30:00Z",
  }).read();

  assert.equal(input["account/rateLimits/read"].rateLimits.codex_bengalfox.fiveHourUsedPercent, 25);
  assert.equal(input["account/rateLimits/read"].rateLimits.codex_bengalfox.weeklyUsedPercent, 75);
  assert.match(renderSituationReport(input), /wk 50% gone/);
});

test("rejects a report whose reset is already due instead of dividing by zero", async () => {
  const fixture = readings();
  fixture.rateLimits.rateLimits.primary.resetsAt = "2026-09-15T18:32:38Z";
  const input = await createAccountClient({
    transport: fakeTransport({ initialize: {}, "account/rateLimits/read": fixture.rateLimits, "account/usage/read": fixture.usage }),
    now: () => "2026-09-15T18:32:38Z",
  }).read();
  assert.throws(() => renderSituationReport(input), /reset must be in the future/);
});

test("propagates an app-server method error without disguising a missing method", async () => {
  const fixture = readings();
  const client = createAccountClient({
    transport: fakeTransport({
      initialize: {},
      "account/rateLimits/read": fixture.rateLimits,
      "account/usage/read": new Error("JSON-RPC account/usage/read failed: method not found"),
    }),
    now: () => "2026-09-15T18:32:38Z",
  });
  await assert.rejects(client.read(), /JSON-RPC account\/usage\/read failed: method not found/);
});

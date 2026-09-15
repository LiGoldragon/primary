import assert from "node:assert/strict";
import test from "node:test";
import { createAccountClient, validateAccountReadings } from "./codex-app-server-client.mjs";
import { renderSituationReport } from "./quota-situation-report.mjs";

const readings = () => ({
  rateLimits: {
    rateLimits: {
      primary: { usedPercent: 35, windowDurationMins: 10_080, resetsAt: 1789830328 },
    },
    rateLimitsByLimitId: {
      codex_bengalfox: {
        primary: { usedPercent: 0, windowDurationMins: 300, resetsAt: 1789513200 },
        secondary: { usedPercent: 0, windowDurationMins: 10_080, resetsAt: 1789830328 },
      },
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

test("normalizes the live nested Spark windows and epoch reset timestamps", async () => {
  const fixture = readings();
  fixture.rateLimits = {
    rateLimits: { primary: { usedPercent: 50, windowDurationMins: 60, resetsAt: 1767229200 } },
    rateLimitsByLimitId: {
      codex_bengalfox: {
        primary: { usedPercent: 25, windowDurationMins: 300, resetsAt: 1767247200 },
        secondary: { usedPercent: 75, windowDurationMins: 10080, resetsAt: 1767830400 },
      },
    },
  };
  const input = await createAccountClient({
    transport: fakeTransport({ initialize: {}, "account/rateLimits/read": fixture.rateLimits, "account/usage/read": fixture.usage }),
    now: () => "2026-01-01T00:30:00Z",
  }).read();

  assert.equal(input["account/rateLimits/read"].rateLimitsByLimitId.codex_bengalfox.primary.usedPercent, 25);
  assert.equal(input["account/rateLimits/read"].rateLimitsByLimitId.codex_bengalfox.secondary.usedPercent, 75);
  assert.match(renderSituationReport(input), /wk 50% gone/);
});

test("keeps unavailable usage and reset credits explicitly unknown", () => {
  const fixture = readings().rateLimits;
  fixture.rateLimitsByLimitId = {
    codex_bengalfox: {
      primary: { usedPercent: 0, windowDurationMins: 300, resetsAt: 1789513200 },
      secondary: { usedPercent: 0, windowDurationMins: 10080, resetsAt: 1789830328 },
    },
  };
  delete fixture.rateLimits.codex_bengalfox;
  fixture.rateLimits.primary.resetsAt = 1789830328;
  delete fixture.rateLimitResetCredits;
  const input = validateAccountReadings({ rateLimits: fixture, usage: undefined, observedAt: "2026-09-15T18:32:38Z" });
  assert.match(renderSituationReport(input), /\+Unknown full-reset credits in hand/);
  assert.equal(input["account/usage/read"], null);
});

test("rejects an expired primary window before rendering can divide by zero", async () => {
  const fixture = readings();
  fixture.rateLimits.rateLimits.primary.resetsAt = 1789477958;
  const client = createAccountClient({
    transport: fakeTransport({ initialize: {}, "account/rateLimits/read": fixture.rateLimits, "account/usage/read": fixture.usage }),
    now: () => "2026-09-15T18:32:38Z",
  });
  await assert.rejects(client.read(), /reset must be in the future/);
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

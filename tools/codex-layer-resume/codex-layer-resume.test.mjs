import assert from "node:assert/strict";
import test from "node:test";
import { defaultRegistryPath, resolveThread, run } from "./codex-layer-resume.mjs";

const primary = "01a0aaa1-f485-7de3-a257-6baaddf642d7";
const secondary = "01a0aaa2-030e-7673-bdcc-d4c62e570c3a";
const registry = {
  schema: 1,
  layers: {
    primary: { state: "current", authority: { kind: "lane-index", revision: "abc" }, threadId: primary, title: "ignored" },
    secondary: { state: "current", authority: { kind: "lane-index", revision: "abc" }, threadId: secondary },
  },
};

test("resolves only a current lane-index UUID", () => {
  assert.equal(resolveThread(registry, "primary"), primary);
  assert.equal(resolveThread(registry, "secondary"), secondary);
});

test("refuses a title-only record", () => {
  const copy = structuredClone(registry);
  delete copy.layers.primary.threadId;
  assert.throws(() => resolveThread(copy, "primary"), /title-based resolution is refused/);
});

test("refuses stale and non-authoritative records", () => {
  const stale = structuredClone(registry);
  stale.layers.primary.state = "retired";
  assert.throws(() => resolveThread(stale, "primary"), /not current/);
  const unknown = structuredClone(registry);
  unknown.layers.primary.authority.kind = "app-server";
  assert.throws(() => resolveThread(unknown, "primary"), /lacks lane-index authority/);
});

test("runs exactly codex resume with the resolved thread ID", () => {
  const calls = [];
  const result = run(["--layer", "primary", "--registry", "/registry.json"], {
    readFileSync: () => JSON.stringify(registry),
    spawnSync: (...args) => { calls.push(args); return { status: 0 }; },
  });
  assert.deepEqual(result, { status: 0, signal: undefined });
  assert.deepEqual(calls, [["codex", ["resume", primary], { stdio: "inherit" }]]);
});

test("uses an environment registry or documented config path", () => {
  assert.equal(defaultRegistryPath({ CODEX_LAYER_INDEX: "/lane.json" }, "/home/test"), "/lane.json");
  assert.equal(defaultRegistryPath({}, "/home/test"), "/home/test/.config/codex/lane-index.json");
});

test("preserves a child signal for the command entrypoint", () => {
  const result = run(["--layer", "primary", "--registry", "/registry.json"], {
    readFileSync: () => JSON.stringify(registry),
    spawnSync: () => ({ status: null, signal: "SIGINT" }),
  });
  assert.deepEqual(result, { status: null, signal: "SIGINT" });
});

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import { render, split, readFrom, findTranscript, workerResult, latestBlock } from "./book-fetch.mjs";

const program = new URL("./book-fetch.mjs", import.meta.url).pathname;

function transcript(records, partialTail = "") {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), "book-fetch-"));
  const project = path.join(home, "projects", "-some-project");
  fs.mkdirSync(project, { recursive: true });
  const file = path.join(project, "session-1.jsonl");
  fs.writeFileSync(file, records.map((r) => JSON.stringify(r)).join("\n") + "\n" + partialTail);
  return { home, file };
}

const t = "2026-09-28T10:00:00.000Z";
const records = [
  { type: "user", timestamp: t, origin: { kind: "human" }, message: { role: "user", content: "Make the page." } },
  { type: "user", timestamp: t, isMeta: true, message: { role: "user", content: "skill body" } },
  { type: "assistant", timestamp: t, message: { content: [{ type: "thinking", thinking: "secret musing" }] } },
  { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: "Mid-turn: starting." }] } },
  { type: "assistant", timestamp: t, message: { content: [{ type: "tool_use", id: "a", name: "Bash", input: { command: "ls", description: "List files" } }] } },
  { type: "user", timestamp: t, message: { content: [{ type: "tool_result", tool_use_id: "a", content: "RAW OUTPUT " + "Q".repeat(5000) }] } },
  { type: "assistant", timestamp: t, message: { content: [{ type: "tool_use", id: "b", name: "Bash", input: { command: "false" } }] } },
  { type: "user", timestamp: t, message: { content: [{ type: "tool_result", tool_use_id: "b", is_error: true, content: "boom" }] } },
  { type: "attachment", timestamp: t, attachment: { type: "queued_command", commandMode: "prompt", prompt: '#msg ["6fe957" "Zeus is built."]' } },
  { type: "user", timestamp: t, origin: { kind: "task-notification" }, message: { content: "<task-notification>\n<task-id>x</task-id>\n<status>completed</status>\n<summary>Agent \"Check\" finished</summary>\n<result>All green. " + "A".repeat(900) + "</result>\n</task-notification>" } },
  { type: "system", subtype: "compact_boundary", timestamp: t },
  { type: "user", timestamp: t, isCompactSummary: true, message: { content: "This session is being continued... summary" } },
  { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: "Done." }] } },
];

test("keeps words, one line per tool, drops raw output and thinking", () => {
  const { file } = transcript(records);
  const { records: read, last } = readFrom(file, 0);
  assert.equal(last, records.length);
  const text = render(read).map((e) => e.text).join("\n");
  assert.match(text, /^L1 2026-09-28T10:00 TYPED: Make the page\.$/m);
  assert.match(text, /L4 .* FLOW: Mid-turn: starting\./);
  assert.match(text, /L5 .* TOOL Bash «List files» ok/);
  assert.match(text, /L7 .* TOOL Bash «false» failed/);
  assert.match(text, /L9 .* MESSAGE from 6fe957 \(arrived mid-turn\): Zeus is built\./);
  assert.match(text, /L10 .* WORKER RESULT: Agent "Check" finished \(completed\)\nAll green\./);
  assert.match(text, /L11 .* COMPACTED/);
  assert.match(text, /L12 .* COMPACTION SUMMARY \(.*not something said at this moment\)/);
  assert.doesNotMatch(text, /RAW OUTPUT|secret musing|skill body|<task-id>/);
});

test("reads from a mark, ignores a half-written last line, and drops blobs", () => {
  const withBlob = [...records, { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: "image " + "iVBORw0KGgo".repeat(80) }] } }];
  const { file } = transcript(withBlob, '{"type":"user","mess');
  const { records: read, last } = readFrom(file, 12);
  assert.equal(last, withBlob.length);
  const text = render(read).map((e) => e.text).join("\n");
  assert.doesNotMatch(text, /Make the page/);
  assert.match(text, /L13 .* FLOW: Done\./);
  assert.match(text, /\[blob of 880 characters dropped\]/);
});

test("splits into stretches under the size", () => {
  const entries = Array.from({ length: 10 }, (_, i) => ({ line: i + 1, text: "x".repeat(400) }));
  const stretches = split(entries, 1000);
  assert.equal(stretches.length, 5);
  assert.deepEqual(stretches.flat().map((e) => e.line), entries.map((e) => e.line));
});

test("finds the transcript by session id and prints stretches and the mark", () => {
  const { home, file } = transcript(records);
  assert.equal(findTranscript("session-1", { CLAUDE_CONFIG_DIR: home }), file);
  const out = path.join(home, "out");
  const printed = execFileSync("node", [program, "--from", "3", "--out", out], {
    env: { ...process.env, CLAUDE_CONFIG_DIR: home, CLAUDE_CODE_SESSION_ID: "session-1" },
    encoding: "utf8",
  });
  assert.match(printed, /stretch-01\.txt lines 4-13 chars \d+/);
  assert.match(printed, /^session session-1$/m);
  assert.match(printed, /^last 13$/m);
  assert.ok(fs.readFileSync(path.join(out, "stretch-01.txt"), "utf8").startsWith("L4 "));
});

test("worker result without tags passes through", () => {
  assert.equal(workerResult("plain"), "plain");
});

const block = (title, extra = "") =>
  `Intro.\n<!-- to-the-living:start -->\nPresentation.{ «${title}» }\n\n${extra}\n<!-- to-the-living:end -->\nAfter.`;

test("a to-the-living body is neither capped nor deduped", () => {
  const long = block("Long", "W".repeat(15000));
  const repeated = [
    { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: long }] } },
    { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: long }] } },
  ];
  const text = render(repeated.map((r, i) => [i + 1, r])).map((e) => e.text).join("\n");
  assert.doesNotMatch(text, /more characters cut|the same \d+ characters/);
  assert.equal(text.match(/to-the-living:end/g).length, 2);
});

test("prints the latest block of the whole transcript whatever the mark", () => {
  const withBlocks = [
    ...records,
    { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: block("First") }] } },
    { type: "assistant", timestamp: t, isSidechain: true, message: { content: [{ type: "text", text: block("Sidechain") }] } },
    { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: block("Second", "X".repeat(13000)) }] } },
    { type: "assistant", timestamp: t, message: { content: [{ type: "tool_use", id: "c", name: "Bash", input: { command: block("Quoted") } }] } },
  ];
  const { home, file } = transcript(withBlocks);
  assert.equal(latestBlock(readFrom(file, 0).records).line, 16);
  const printed = execFileSync("node", [program, "--from", String(withBlocks.length), "--out", path.join(home, "out")], {
    env: { ...process.env, CLAUDE_CONFIG_DIR: home, CLAUDE_CODE_SESSION_ID: "session-1" },
    encoding: "utf8",
  });
  assert.match(printed, /^nothing new$/m);
  assert.match(printed, /^latest-block L16\n<!-- to-the-living:start -->\nPresentation\.\{ «Second» \}\n\nX{13000}\n<!-- to-the-living:end -->$/m);
});

test("says when the transcript holds no block", () => {
  const { home } = transcript(records);
  const printed = execFileSync("node", [program, "--out", path.join(home, "out")], {
    env: { ...process.env, CLAUDE_CONFIG_DIR: home, CLAUDE_CODE_SESSION_ID: "session-1" },
    encoding: "utf8",
  });
  assert.match(printed, /^latest-block none$/m);
});

test("--block prints only the block on stdout; session and count go to stderr", () => {
  const { home } = transcript([
    ...records,
    { type: "assistant", timestamp: t, message: { content: [{ type: "text", text: block("Only") }] } },
  ]);
  const run = spawnSync("node", [program, "--block", "--out", path.join(home, "out")], {
    env: { ...process.env, CLAUDE_CONFIG_DIR: home, CLAUDE_CODE_SESSION_ID: "session-1" },
    encoding: "utf8",
  });
  assert.equal(run.status, 0);
  assert.equal(run.stdout, "<!-- to-the-living:start -->\nPresentation.{ «Only» }\n\n\n<!-- to-the-living:end -->\n");
  assert.doesNotMatch(run.stdout, /session|last \d/);
  assert.match(run.stderr, /^session session-1$/m);
  assert.match(run.stderr, /^last \d+$/m);
});

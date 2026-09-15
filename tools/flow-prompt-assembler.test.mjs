import assert from "node:assert/strict";
import test from "node:test";
import { AssemblyError, assemble } from "./flow-prompt-assembler.mjs";

const fixture = new URL("../reports/flow-assembler/fixtures/692df8-to-05c604.json", import.meta.url);

test("renders the 692df8 to 05c604 fixture", async () => {
  const input = JSON.parse(await (await import("node:fs/promises")).readFile(fixture, "utf8"));
  const output = await assemble(input);

  assert.match(output, /predecessor lane: flows\/692df8/);
  assert.match(output, /successor: 05c6048e-2e71-4f39-96dc-0937b92969c6 \(claude\)/);
  assert.match(output, /transcript: NOT AVAILABLE IN FIXTURE/);
  assert.match(output, /- spirit/);
});

test("rejects an absent single user prompt", async () => {
  const input = JSON.parse(await (await import("node:fs/promises")).readFile(fixture, "utf8"));
  delete input.userPrompt;
  await assert.rejects(
    () => assemble(input),
    (error) => error instanceof AssemblyError && error.message === "missing required input: userPrompt",
  );
});

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { checkBook } from "./book-check.mjs";
const program = new URL("./book-check.mjs", import.meta.url).pathname;
const good = "## Proposal\nThe change.\n## Distillation\nTarget: field-skills/skills/example.md\nAdd: Use the supported route.\n";

test("rejects the first-anatomy failure: proposals without distillation", () => {
  assert.deepEqual(checkBook("## Add an anatomy\n```ethos\nOperation\n```\nA proposal.\n"), [{ reason: "missing-distillation" }]);
});
test("a named but empty section is not enough", () => {
  assert.equal(checkBook("## Distillation\n<!-- hidden -->\n## Other\nText\n")[0].reason, "empty-distillation");
});
test("heading inside code or a comment cannot satisfy the requirement", () => {
  assert.equal(checkBook("```text\n## Distillation\nproposal\n```\n").at(-1).reason, "missing-distillation");
  assert.equal(checkBook("<!--\n## Distillation\nproposal\n-->\n").at(-1).reason, "missing-distillation");
});
test("checks real code width without reflowing or limiting proposed prose", () => {
  assert.deepEqual(checkBook(good + "```text\n" + "p".repeat(100) + "\n```\n"), []);
  assert.equal(checkBook(good + "~~~clojure\n" + "x".repeat(53) + "\n~~~\n")[0].reason, "code-over-52-columns");
  assert.deepEqual(checkBook(good + "```rust\n" + "x".repeat(52) + "\n```\n"), []);
});
test("a shorter fence does not close code; unclosed fences refuse", () => {
  assert.equal(checkBook(good + "````rust\n```\n").at(-1).reason, "unclosed-code-fence");
});
test("quotes refuse outside code; code remains literal", () => {
  assert.equal(checkBook(good + "> his words\n")[0].reason, "quote-block-in-book");
  assert.deepEqual(checkBook(good + "```rust\n> code\n```\n"), []);
});
test("executable succeeds only for valid source and never edits it", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "book-check-"));
  try {
    const file = path.join(dir, "book.md");
    fs.writeFileSync(file, good);
    let result = spawnSync(process.execPath, [program, file], { encoding: "utf8" });
    assert.equal(result.status, 0); assert.equal(result.stderr, "");
    assert.equal(JSON.parse(result.stdout).checked, true); assert.equal(fs.readFileSync(file, "utf8"), good);
    fs.writeFileSync(file, "## Proposal\nNo distillation.\n");
    result = spawnSync(process.execPath, [program, file], { encoding: "utf8" });
    assert.equal(result.status, 1); assert.equal(result.stdout, "");
    assert.equal(JSON.parse(result.stderr).errors[0].reason, "missing-distillation");
    result = spawnSync(process.execPath, [program, file, file], { encoding: "utf8" });
    assert.equal(result.status, 2); assert.equal(result.stdout, "");
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

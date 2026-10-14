import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { checkBook } from "./book-check.mjs";
const program = new URL("./book-check.mjs", import.meta.url).pathname;
const good = "## Proposal\nThe change.\n## Crystallization\nFile: field-context/skills/example.md\n+ Use the supported route.\n";
const proposal = "File: example.md\n+ Added.\n";

test("the Crystallization heading is optional", () => {
  assert.deepEqual(checkBook("## Add an anatomy\n```ethos\nOperation\n```\nA proposal.\n" + proposal), []);
});
test("a named but empty section is not enough", () => {
  assert.equal(checkBook("## Crystallization\n<!-- hidden -->\n## Other\nText\n")[0].reason, "empty-crystallization");
});
test("heading inside code or a comment opens no section", () => {
  assert.deepEqual(checkBook("```text\n## Crystallization\nproposal\n```\n" + proposal), []);
  assert.deepEqual(checkBook("<!--\n## Crystallization\nproposal\n-->\n" + proposal), []);
});
test("checks real code width without reflowing or limiting proposed prose", () => {
  assert.deepEqual(checkBook(good + "```text\n" + "p".repeat(100) + "\n```\n"), []);
  assert.equal(checkBook(good + "~~~clojure\n" + "x".repeat(53) + "\n~~~\n")[0].reason, "code-over-52-columns");
  assert.deepEqual(checkBook(good + "```rust\n" + "x".repeat(52) + "\n```\n"), []);
  assert.deepEqual(checkBook(good + "```clojure\n- " + "x".repeat(90) + "\n+ " + "y".repeat(50) + "\n```\n"), []);
  assert.equal(checkBook(good + "```clojure\n+ " + "y".repeat(51) + "\n```\n")[0].reason, "code-over-52-columns");
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
    fs.writeFileSync(file, "## Proposal\nNo crystallization.\n" + proposal);
    result = spawnSync(process.execPath, [program, file], { encoding: "utf8" });
    assert.equal(result.status, 0); assert.equal(result.stderr, "");
    result = spawnSync(process.execPath, [program, file, file], { encoding: "utf8" });
    assert.equal(result.status, 2); assert.equal(result.stdout, "");
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test("the published first anatomy and the corrected second edition passes", () => {
  const first = fs.readFileSync(new URL("../flows/0c85a3/books/word-flow-id-anatomy.md", import.meta.url), "utf8");
  const second = fs.readFileSync(new URL("../flows/0c85a3/books/word-flow-id-anatomy-second-edition.md", import.meta.url), "utf8");
  // These historical books carry no File: line; only the proposal rule may refuse them.
  assert.deepEqual(checkBook(first).map(e => e.reason), ["missing-proposal"]);
  assert.deepEqual(checkBook(second, { allowLegacyDistillation: true }).map(e => e.reason), ["missing-proposal"]);
});

test("legacy Distillation sections are checked only when explicitly allowed", () => {
  const legacy = "## Distillation\nA preserved old proposal.\n" + proposal;
  assert.deepEqual(checkBook(good), []);
  assert.deepEqual(checkBook(legacy), []);
  assert.deepEqual(checkBook(legacy, { allowLegacyDistillation: true }), []);
});

 test("crystallization requires a target file and an added line in each section", () => {
  assert.ok(checkBook("## Crystallization\n+ Added.\n").some(e => e.reason === "no-target-file"));
  assert.ok(checkBook("## Crystallization\nFile: example.md\n").some(e => e.reason === "no-added-line"));
  assert.deepEqual(checkBook("## Crystallization\n```text\nFile: example.md\n- Old.\n+ New.\n  Kept.\n```\n"), []);
  assert.ok(checkBook(good + "## Crystallization\nUnqualified second section.\n").some(e => e.reason === "no-target-file"));
  assert.ok(checkBook("## Crystallization\n<!-- File: false.md\n+ False.\n-->\n").some(e => e.reason === "no-added-line"));
});

test("a book carries a proposal: a File: line followed by a + line", () => {
  assert.equal(checkBook("## Add an anatomy\nText.\n+ Added.\n")[0].reason, "missing-proposal");
  assert.equal(checkBook("Text.\nFile: example.md\n- Old.\n")[0].reason, "missing-proposal");
  assert.equal(checkBook("+ Added.\nFile: example.md\n")[0].reason, "missing-proposal");
  assert.deepEqual(checkBook("Text.\nFile: example.md\n- Old.\n+ New.\n"), []);
  assert.deepEqual(checkBook("```text\nFile: example.md\n+ New.\n```\n"), []);
});

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { checkBook } from "./book-check.mjs";
const program = new URL("./book-check.mjs", import.meta.url).pathname;
const good = "# A book\n## Proposal 1: psyche-context › vision/example.md\n+ Use the supported route.\n";
const reasons = (source) => checkBook(source).map(e => e.reason);

test("the heading carries the location, with an optional title and new-file mark", () => {
  assert.deepEqual(checkBook(good), []);
  assert.deepEqual(checkBook("### Proposal 2: The Library · signal-chronos › ethos/library.ethos, a new file\n+ Added.\n"), []);
  assert.deepEqual(checkBook("## Proposal 3: chronos › ethos/memory.ethos, a new file\n+ Added.\n"), []);
});
test("a proposal heading without a location refuses", () => {
  assert.deepEqual(reasons("## Proposal 1: The Library\n+ Added.\n"), ["proposal-heading-without-location", "missing-proposal", "text-outside-proposal-without-module"]);
  assert.deepEqual(reasons("## Proposal\n+ Added.\n"), ["proposal-heading-without-location", "missing-proposal", "text-outside-proposal-without-module"]);
  assert.deepEqual(reasons(good + "## Proposal 2: psyche-context skills/x.md\n+ Added.\n"), ["proposal-heading-without-location", "text-outside-proposal-without-module"]);
});
test("a File: line in the body refuses, in prose or a text block", () => {
  assert.deepEqual(reasons(good.replace("+ Use", "File: skills/example.md\n+ Use")), ["file-line-in-body"]);
  assert.deepEqual(reasons(good + "```text\nFile: example.md\n+ New.\n```\n"), ["file-line-in-body"]);
  assert.deepEqual(checkBook(good + "```rust\nFile: literal code\n```\n"), []);
  assert.deepEqual(checkBook(good + "<!-- File: hidden.md -->\n"), []);
});
test("a book carries a located proposal; each proposal carries a change", () => {
  assert.deepEqual(reasons("# A book\nText.\n+ Added.\n"), ["missing-proposal", "text-outside-proposal-without-module", "text-outside-proposal-without-module"]);
  assert.deepEqual(reasons(good + "## Proposal 2: flows › a/b.md\nOnly prose.\n"), ["no-change-in-proposal"]);
  assert.deepEqual(checkBook(good + "## Proposal 2: flows › a/b.md\n**Archive** the record.\n"), []);
  assert.deepEqual(checkBook(good + "## Proposal 2: flows › a/b.md\n**Destroy** a sentence.\n"), []);
  assert.deepEqual(checkBook("## Proposal 1: chronos › src/lib.rs\n```rust\n+ fn f() {}\n```\n"), []);
  assert.deepEqual(reasons("## Proposal 1: flows › a.md\nText.\n## Elsewhere\n+ Added.\n"), ["no-change-in-proposal", "heading-outside-proposal-without-module", "text-outside-proposal-without-module"]);
});
test("heading inside code or a comment opens no proposal", () => {
  assert.deepEqual(reasons("```text\n## Proposal 1: a › b.md\n+ x\n```\n"), ["text-outside-proposal-without-module", "missing-proposal"]);
  assert.deepEqual(reasons("<!--\n## Proposal 1: a › b.md\n+ x\n-->\n"), ["missing-proposal"]);
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
    fs.writeFileSync(file, "## Proposal 1: a › b.md\nFile: b.md\n+ Added.\n");
    result = spawnSync(process.execPath, [program, file], { encoding: "utf8" });
    assert.equal(result.status, 1); assert.equal(result.stdout, "");
    result = spawnSync(process.execPath, [program, file, file], { encoding: "utf8" });
    assert.equal(result.status, 2); assert.equal(result.stdout, "");
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
test("historical books with independent prose now refuse", () => {
  const read = (p) => fs.readFileSync(new URL(p, import.meta.url), "utf8");
  assert.ok(checkBook(read("../flows/504f11/books/02-chronos-golden-example-2.md")).length);
  assert.ok(checkBook(read("../flows/d68c82/books/50-lean-flows.md")).length);
  assert.ok(reasons(read("../flows/504f11/books/01-chronos-golden-example.md")).includes("file-line-in-body"));
});

test("outside proposals only whole current modules under their locations pass", () => {
  const body = "## The rule\n\nUse the actual module.\n\n> Literal source quotation.\n";
  const readModule = (repo, file) => {
    assert.equal(repo, "field-context"); assert.equal(file, "compensation/example.md");
    return "---\ndescription: A fixture.\ndependencies: []\n---\n\n" + body;
  };
  const heading = "## field-context › compensation/example.md\n\n";
  const proposal = "## Proposal 1: psyche-context › vision/example.md\n+ A proposal.\n";
  assert.deepEqual(checkBook("# A book\n" + heading + body + "\n" + proposal, {readModule}), []);
  assert.deepEqual(checkBook(heading + "```markdown\n" + body.trim() + "\n```\n\n" + proposal, {readModule}), []);
  assert.equal(checkBook(heading + "The rule means something else.\n\n" + proposal, {readModule})[0].reason, "context-module-differs");
  assert.equal(checkBook(heading + body + "\nMy own conclusion.\n\n" + proposal, {readModule})[0].reason, "context-module-differs");
  assert.equal(checkBook(heading + body + proposal, {readModule: () => { throw Error(); }})[0].reason, "context-module-unavailable");
  assert.ok(checkBook("## tools › brief.md\nProse.\n" + proposal, {readModule}).length);
  assert.ok(checkBook("## field-context › ../secret.md\nProse.\n" + proposal, {readModule}).length);
  assert.ok(checkBook("# A book\nA paraphrase.\n## What vision says\nMore prose.\n" + proposal).some(e => e.reason === "heading-outside-proposal-without-module"));
});

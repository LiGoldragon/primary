import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { checkBook } from "./book-check.mjs";
const program = new URL("./book-check.mjs", import.meta.url).pathname;
const good = "# A book\n## Proposal 1: psyche-belief › vision/example.md\n+ Use the supported route.\n";
const reasons = (source) => checkBook(source).map(e => e.reason);

test("the heading carries the location, with an optional title and new-file mark", () => {
  assert.deepEqual(checkBook(good), []);
  assert.deepEqual(checkBook("### Proposal 2: The Library · signal-chronos › ethos/library.ethos, a new file\n+ Added.\n"), []);
  assert.deepEqual(checkBook("## Proposal 3: chronos › ethos/memory.ethos, a new file\n+ Added.\n"), []);
});
test("a proposal heading without a location refuses", () => {
  assert.deepEqual(reasons("## Proposal 1: The Library\n+ Added.\n"), ["proposal-heading-without-location", "missing-proposal", "text-outside-proposal-without-module"]);
  assert.deepEqual(reasons("## Proposal\n+ Added.\n"), ["proposal-heading-without-location", "missing-proposal", "text-outside-proposal-without-module"]);
  assert.deepEqual(reasons(good + "## Proposal 2: psyche-belief skills/x.md\n+ Added.\n"), ["proposal-heading-without-location", "text-outside-proposal-without-module"]);
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
  assert.deepEqual(checkBook(read("../flows/504f11/books/02-chronos-golden-example-2.md")), []); // its context figure is a diagram fence
  assert.ok(checkBook(read("../flows/d68c82/books/50-lean-flows.md")).length);
  assert.ok(reasons(read("../flows/504f11/books/01-chronos-golden-example.md")).includes("file-line-in-body"));
});

test("outside proposals only whole current modules under their locations pass", () => {
  const body = "## The rule\n\nUse the actual module.\n\n> Literal source quotation.\n";
  const readModule = (repo, file) => {
    assert.equal(repo, "field-belief"); assert.equal(file, "compensation/example.md");
    return "---\ndescription: A fixture.\ndependencies: []\n---\n\n" + body;
  };
  const heading = "## field-belief › compensation/example.md\n\n";
  const proposal = "## Proposal 1: psyche-belief › vision/example.md\n+ A proposal.\n";
  assert.deepEqual(checkBook("# A book\n" + heading + body + "\n" + proposal, {readModule}), []);
  assert.deepEqual(checkBook(heading + "```markdown\n" + body.trim() + "\n```\n\n" + proposal, {readModule}), []);
  assert.equal(checkBook(heading + "The rule means something else.\n\n" + proposal, {readModule})[0].reason, "context-module-differs");
  assert.equal(checkBook(heading + body + "\nMy own conclusion.\n\n" + proposal, {readModule})[0].reason, "context-module-differs");
  assert.equal(checkBook(heading + body + proposal, {readModule: () => { throw Error(); }})[0].reason, "context-module-unavailable");
  assert.ok(checkBook("## tools › brief.md\nProse.\n" + proposal, {readModule}).length);
  assert.ok(checkBook("## field-belief › ../secret.md\nProse.\n" + proposal, {readModule}).length);
  assert.ok(checkBook("# A book\nA paraphrase.\n## What vision says\nMore prose.\n" + proposal).some(e => e.reason === "heading-outside-proposal-without-module"));
});

test("module-view headings use the builder's level-two contract", () => {
  const module = "Module line.\n\n### Nested › section\n\nMore module text.\n";
  const readModule = () => module;
  const proposal = "## Proposal 1: repo › x.md\n+ Add a line.\n";
  const valid = "# A book\n\n## repo › x.md\n\n" + module + "\n" + proposal;
  assert.deepEqual(checkBook(valid, {readModule}), []);
  for (const level of ["#", "###", "####", "######"]) {
    const invalid = "# A book\n\n" + level + " repo › x.md\n\n" + module + "\n" + proposal;
    assert.ok(reasons(invalid).includes("heading-outside-proposal-without-module"), level);
  }
  assert.ok(reasons("# repo › x.md\n\n## Proposal 1: repo › x.md\n+ Add a line.\n")
    .includes("heading-outside-proposal-without-module"), "a level-one module path is not a book title");
});

test("Markdown in a plain code block is refused; markdown fences are not", () => {
  const proposal = "## Proposal 1: psyche-belief › vision/example.md\n+ A proposal.\n";
  const md = "## Rule\n\nText.\n";
  for (const label of ["", "text", "txt", "prose"])
    assert.ok(reasons(proposal + "```" + label + "\n" + md + "```\n").includes("markdown-in-code-block"), label);
  assert.ok(!reasons(proposal + "```markdown\n" + md + "```\n").includes("markdown-in-code-block"));
  assert.ok(!reasons(proposal + "~~~~md\n" + md + "~~~~\n").includes("markdown-in-code-block"));
  assert.ok(!reasons(proposal + "```sh\n# a comment\n```\n").includes("markdown-in-code-block"));
  assert.ok(!reasons(proposal + "```text\n+ ## Rule\n```\n").includes("markdown-in-code-block"), "a change is not a code block");
});

test("a view of any file of any repository matches it to the character", () => {
  const file = "(Types\n  chronos)\n\n## not a heading\n";
  const readModule = (repo, p) => {
    assert.equal(repo, "chronos"); assert.equal(p, ".ethos/data/chronos.ethos");
    return file;
  };
  const proposal = "## Proposal 1: chronos › .ethos/data/chronos.ethos\n- (Types\n";
  const heading = "## chronos › .ethos/data/chronos.ethos\n\n";
  assert.deepEqual(checkBook("# B\n" + heading + "```ethos\n" + file.trimEnd() + "\n```\n\n" + proposal, {readModule}), []);
  assert.deepEqual(checkBook("# B\n" + heading + "````\n" + file.trimEnd() + "\n````\n\n" + proposal, {readModule}), []);
  assert.equal(checkBook("# B\n" + heading + "```ethos\n" + file.replace("chronos", "kronos").trimEnd() + "\n```\n\n" + proposal, {readModule})[0].reason, "context-module-differs");
  assert.equal(checkBook("# B\n" + heading + "```ethos\n" + file.trimEnd() + "\n```\n\n" + proposal, {readModule: () => { throw Error(); }})[0].reason, "context-module-unavailable");
  assert.ok(checkBook("# B\n## chronos › ../x.ethos\n```ethos\nx\n```\n" + proposal, {readModule}).length);
  assert.ok(checkBook("# B\n## chronos › /etc/passwd\n```ethos\nx\n```\n" + proposal, {readModule}).length);
  assert.ok(checkBook("# B\n## psyche-belief › src/x.rs\n```rust\nx\n```\n" + proposal, {readModule}).length, "context repositories hold only authored modules");
});

test("a proposal that only removes lines, or deletes the file, passes", () => {
  assert.deepEqual(reasons("# A book\n## Proposal 1: chronos › a.ethos\n- Old line.\n"), []);
  assert.deepEqual(reasons("# A book\n## Proposal 1: chronos › a.ethos, a deleted file\nIt goes.\n"), []);
  assert.ok(reasons("# A book\n## Proposal 1: chronos › a.ethos\nText only.\n").includes("no-change-in-proposal"));
});

test("an unlabelled diagram fence outside a section is accepted; prose there is refused", () => {
  const fig = "```\n┌───┐   draws   ┌───┐\n│ a │ ───────▶ │ b │\n└───┘          └───┘\n```\n";
  assert.deepEqual(reasons("# A book\n" + fig + good.split("\n").slice(1).join("\n")), []);
  const ascii = "```\n+---+\n| a |\n+---+\n  |\n  v\n+---+\n| b |\n+---+\n```\n";
  assert.deepEqual(reasons("# A book\n" + ascii + good.split("\n").slice(1).join("\n")), []);
  assert.deepEqual(reasons("# A book\n```\nJust some prose here.\n```\n" + good.split("\n").slice(1).join("\n")), ["text-outside-proposal-without-module"]);
});
const located = "### Proposal 1: Replace · psyche-belief › vision/book.md\n";
const alternative = (n, added) => `**Alternative ${n}**\n\n  Context.\n\n- Old.\n+ ${added}\n\n`;
test("a machine comment comes first in its proposal, once", () => {
  assert.deepEqual(checkBook(located + "**Comment** Why it is proposed.\n\n- Old.\n+ New.\n"), []);
  assert.deepEqual(reasons(located + "- Old.\n+ New.\n\n**Comment** Too late.\n"), ["comment-after-change"]);
  assert.deepEqual(reasons(located + "**Comment** One.\n\n**Comment** Two.\n\n+ New.\n"), ["second-comment-in-proposal"]);
  assert.deepEqual(reasons("**Comment** Loose.\n" + located + "+ New.\n"), ["text-outside-proposal-without-module"]);
});
test("alternatives come two or more, numbered in order, each with a change, the comment before them", () => {
  assert.deepEqual(checkBook(located + "**Comment** Two wordings.\n\n" + alternative(1, "One.") + alternative(2, "Two.") + "Ruling: land 1, land 2, amend, or reject.\n"), []);
  assert.deepEqual(reasons(located + alternative(1, "One.")), ["single-alternative"]);
  assert.deepEqual(reasons(located + alternative(1, "One.") + alternative(3, "Three.")), ["alternative-out-of-order"]);
  assert.deepEqual(reasons(located + "**Alternative 1**\n\n  Context only.\n\n" + alternative(2, "Two.")), ["alternative-without-change"]);
  assert.deepEqual(reasons(located + alternative(1, "One.") + alternative(2, "Two.") + "**Comment** Late.\n"), ["comment-after-change"]);
  assert.deepEqual(reasons(located + alternative(1, "One.") + "**Alternative 2**\n\n  Context only.\n"), ["alternative-without-change"]);
});

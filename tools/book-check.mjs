import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// A proposal names its location in its heading: "Proposal N: <repo> › <path>",
// optionally after a title and " · ", optionally ending ", a new file".
const located = /^Proposal \d+: (?:.+ · )?[^\s›·]+ › [^\s,]+(?:, a new file)?$/;
const change = (line) => /^\+ \S/.test(line) || /^\*\*(?:Archive|Destroy)\*\*/.test(line);

// This checks source structure, not the merits of a proposed crystallization.
export function checkBook(source) {
  const errors = [];
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  let fence = null, section = null, inComment = false, proposals = 0;
  const finish = () => {
    if (section && !section.changed) errors.push({ line: section.line, reason: "no-change-in-proposal" });
    section = null;
  };
  const body = (line, number) => {
    // The location lives in the heading; a File: line in the body is the retired form.
    if (/^File:/.test(line)) errors.push({ line: number, reason: "file-line-in-body" });
    if (section && change(line)) section.changed = true;
  };
  lines.forEach((line, i) => {
    const number = i + 1;
    if (fence) {
      if (new RegExp(`^ {0,3}${fence.char}{${fence.size},}\\s*$`).test(line)) {
        fence = null;
      } else if (fence.code) {
        // A removed line is quoted as it is; the width limit binds proposed code only.
        if (!line.startsWith("- ") && [...line].length > 52) errors.push({ line: number, reason: "code-over-52-columns" });
        if (section && /^\+ \S/.test(line)) section.changed = true;
      } else {
        body(line, number);
      }
      return;
    }
    if (inComment) {
      if (line.includes("-->")) inComment = false;
      return;
    }
    if (line.trimStart().startsWith("<!--")) {
      inComment = !line.includes("-->");
      return;
    }
    const opening = line.match(/^ {0,3}(`{3,}|~{3,})\s*([^ ]*)/);
    if (opening) {
      const language = opening[2].toLowerCase();
      fence = { char: opening[1][0], size: opening[1].length, line: number,
                code: !["text", "prose", "markdown", "md"].includes(language) };
      return;
    }
    const heading = line.match(/^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (heading) {
      if (section && heading[1].length <= section.level) finish();
      if (/^Proposal\b/i.test(heading[2])) {
        finish();
        if (located.test(heading[2])) {
          proposals++;
          section = { line: number, level: heading[1].length, changed: false };
        } else errors.push({ line: number, reason: "proposal-heading-without-location" });
      }
      return;
    }
    if (/^ {0,3}>/.test(line)) errors.push({ line: number, reason: "quote-block-in-book" });
    body(line, number);
  });
  finish();
  if (!proposals) errors.push({ line: 1, reason: "missing-proposal" });
  if (fence) errors.push({ line: fence.line, reason: "unclosed-code-fence" });
  return errors.sort((a, b) => a.line - b.line);
}

export function main(args) {
  if (args.length !== 1 || !path.isAbsolute(args[0])) {
    console.error(JSON.stringify({ errors: [{ reason: "one-absolute-source-path-required" }] }));
    return 2;
  }
  let source;
  try { source = fs.readFileSync(args[0], "utf8"); }
  catch { console.error(JSON.stringify({ errors: [{ reason: "source-unreadable" }] })); return 2; }
  const errors = checkBook(source);
  if (errors.length) { console.error(JSON.stringify({ errors })); return 1; }
  console.log(JSON.stringify({ checked: true, source: args[0] }));
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = main(process.argv.slice(2));
}

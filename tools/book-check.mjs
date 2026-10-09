import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// This checks source structure, not the merits of a proposed distillation.
export function checkBook(source) {
  const errors = [];
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  let fence = null, section = null, hasDistillation = false;
  let inComment = false;
  const finish = () => {
    if (section && !section.content) errors.push({ line: section.line, reason: "empty-distillation" });
    section = null;
  };
  lines.forEach((line, i) => {
    const number = i + 1;
    if (fence) {
      if (new RegExp(`^ {0,3}${fence.char}{${fence.size},}\\s*$`).test(line)) {
        fence = null;
      } else {
        if (fence.code && [...line].length > 52) errors.push({ line: number, reason: "code-over-52-columns" });
        if (section && line.trim()) section.content = true;
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
      if (/^(?:\d+[.)]\s+)?distillation\b/i.test(heading[2])) {
        finish();
        hasDistillation = true;
        section = { line: number, level: heading[1].length, content: false };
      }
      return;
    }
    if (/^ {0,3}>/.test(line)) errors.push({ line: number, reason: "quote-block-in-book" });
    if (section && line.trim() && !/^Presentation\./.test(line)) section.content = true;
  });
  finish();
  if (fence) errors.push({ line: fence.line, reason: "unclosed-code-fence" });
  if (!hasDistillation) errors.push({ reason: "missing-distillation" });
  return errors;
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

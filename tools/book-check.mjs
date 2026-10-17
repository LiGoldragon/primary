import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

// A proposal names its location in its heading: "Proposal N: <repo> › <path>",
// optionally after a title and " · ", optionally ending ", a new file".
const located = /^Proposal \d+: (?:.+ · )?[^\s›·]+ › [^\s,]+(?:, a new file)?$/;
const change = (line) => /^\+ \S/.test(line) || /^\*\*(?:Archive|Destroy)\*\*/.test(line);
const moduleLocation = /^(psyche-context|mind-context|field-context) › ((?:spirit|intent|vision|knowledge|compensation|inquiry|role|raw)\/[A-Za-z0-9][A-Za-z0-9_.-]*\.md)$/;

// Read a frozen authored blob, never a generated skill or a caller-supplied path.
export function readContextModule(repository, relativePath) {
  if (!moduleLocation.test(`${repository} › ${relativePath}`)) throw new Error("module-location-invalid");
  const root = `/git/github.com/LiGoldragon/${repository}`;
  const git = args => execFileSync("git", ["-C", root, ...args], {encoding: "utf8", timeout: 15000, stdio: ["ignore", "pipe", "pipe"]});
  // Qualify main now; an unavailable revision refuses instead of using a stale copy.
  const revision = git(["ls-remote", "origin", "refs/heads/main"]).trim().split(/\s+/)[0];
  if (!/^[a-f0-9]{40}$/.test(revision) || !/^100(?:644|755) blob /.test(git(["ls-tree", revision, "--", relativePath])))
    throw new Error("module-source-unavailable");
  return git(["show", `${revision}:${relativePath}`]);
}

const moduleBody = text => text.replace(/\r\n/g, "\n").replace(/^---\n[\s\S]*?\n---\n/, "").trim();

// This checks source structure, not the merits of a proposed crystallization.
export function checkBook(source, {readModule = readContextModule} = {}) {
  const errors = [];
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  let fence = null, section = null, inComment = false, proposals = 0, title = false, presentation = false;
  const shownModules = new Set();
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
    if (shownModules.has(i)) return;
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
      if (!section) errors.push({line: number, reason: "text-outside-proposal-without-module"});
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
      } else if (!section) {
        const location = heading[2].match(moduleLocation);
        if (location) {
          let end = i + 1;
          let literalFence = null;
          // Internal headings are part of the quoted module. Only another
          // located module or proposal starts the next book section.
          while (end < lines.length) {
            const text = lines[end];
            if (literalFence) {
              if (new RegExp(`^ {0,3}${literalFence.char}{${literalFence.size},}\\s*$`).test(text)) literalFence = null;
            } else {
              if (/^ {0,3}#{1,6}\s+(?:Proposal\b|(?:psyche|mind|field)-context › )/.test(text) || /^<!-- to-the-living:end -->$/.test(text)) break;
              const open = text.match(/^ {0,3}(`{3,}|~{3,})/);
              if (open) literalFence = {char: open[1][0], size: open[1].length};
            }
            end++;
          }
          let shown = lines.slice(i + 1, end).join("\n").trim();
          const literal = shown.match(/^(`{3,}|~{3,})(?:markdown|md|text)\s*\n([\s\S]*)\n\1$/);
          if (literal) shown = literal[2];
          try {
            if (shown !== moduleBody(readModule(location[1], location[2]))) errors.push({line: number, reason: "context-module-differs"});
          } catch { errors.push({line: number, reason: "context-module-unavailable"}); }
          for (let n = i + 1; n < end; n++) shownModules.add(n);
        } else if (heading[1].length === 1 && !title && !proposals && !shownModules.size) {
          title = true;
        } else errors.push({line: number, reason: "heading-outside-proposal-without-module"});
      }
      return;
    }
    if (!section && line.trim()) {
      if (!presentation && !title && !proposals && !shownModules.size && /^Presentation\.\{ «[^»]*» \}$/.test(line)) presentation = true;
      else errors.push({line: number, reason: "text-outside-proposal-without-module"});
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

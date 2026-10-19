import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

// A proposal names its location in its heading: "Proposal N: <repo> › <path>",
// optionally after a title and " · ", optionally ending ", a new file" or ", a deleted file".
const located = /^Proposal \d+: (?:.+ · )?[^\s›·]+ › [^\s,]+(?:, a (?:new|deleted) file)?$/;
// A removal is a change: removed lines, or the whole file deleted.
const change = (line) => /^[+-] .*\S/.test(line) || /^\*\*(?:Archive|Destroy)\*\*/.test(line);
// The three context repositories hold only their authored modules; any other
// repository of the living holds any file, named by a relative path.
const contextRepository = /^(?:psyche|mind|field)-context$/;
const contextModule = /^(?:spirit|intent|vision|knowledge|compensation|inquiry|role|raw)\/[A-Za-z0-9][A-Za-z0-9_.-]*\.md$/;
const repositoryName = /^[A-Za-z0-9][A-Za-z0-9_.-]*$/;
const filePath = /^(?!\/)(?:[A-Za-z0-9_.-]+\/)*[A-Za-z0-9_-][A-Za-z0-9_.-]*$|^(?!\/)(?:[A-Za-z0-9_.-]+\/)*\.[A-Za-z0-9_-][A-Za-z0-9_.-]*$/;
const validLocation = (repository, relativePath) => repositoryName.test(repository)
  && (contextRepository.test(repository) ? contextModule.test(relativePath)
      : filePath.test(relativePath) && !relativePath.split("/").some(part => part === "." || part === ".."));
const moduleLocation = /^([A-Za-z0-9][A-Za-z0-9_.-]*) › ([^\s,›·]+)$/;
const nextSection = /^ {0,3}#{1,6}\s+(?:Proposal\b|[A-Za-z0-9][A-Za-z0-9_.-]* › [^\s,›·]+\s*$)/;

// Read a file of one of the living's repositories as origin main has it; a context repository gives only its authored modules, never a generated skill.
export function readContextModule(repository, relativePath) {
  if (!validLocation(repository, relativePath)) throw new Error("module-location-invalid");
  const root = `/git/github.com/LiGoldragon/${repository}`;
  const git = args => execFileSync("git", ["-C", root, ...args], {encoding: "utf8", timeout: 15000, stdio: ["ignore", "pipe", "pipe"]});
  // Qualify main now; an unavailable revision refuses instead of using a stale copy.
  const revision = git(["ls-remote", "origin", "refs/heads/main"]).trim().split(/\s+/)[0];
  if (!/^[a-f0-9]{40}$/.test(revision) || !/^100(?:644|755) blob /.test(git(["ls-tree", revision, "--", relativePath])))
    throw new Error("module-source-unavailable");
  return git(["show", `${revision}:${relativePath}`]);
}

// An unlabelled fence whose body draws boxes or arrows; prose is not a diagram.
function diagramFence(lines, open, opening) {
  const close = new RegExp(`^ {0,3}${opening[1][0]}{${opening[1].length},}\\s*$`);
  const body = [];
  for (let n = open + 1; n < lines.length && !close.test(lines[n]); n++) body.push(lines[n]);
  const text = body.join("\n");
  return /[\u2500-\u257f]|\+-{2,}\+|^\s*[|v^]\s*$|-->|<--/m.test(text);
}

const moduleBody = text => text.replace(/\r\n/g, "\n").replace(/^---\n[\s\S]*?\n---\n/, "").trim();

// This checks source structure, not the merits of a proposed crystallization.
export function checkBook(source, {readModule = readContextModule} = {}) {
  const errors = [];
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  let fence = null, section = null, inComment = false, proposals = 0, title = false, presentation = false;
  const shownModules = new Set();
  // An alternative that carries no change refuses at its own mark.
  const closeAlternative = () => {
    if (section?.alternative && !section.alternative.changed) errors.push({ line: section.alternative.line, reason: "alternative-without-change" });
  };
  const finish = () => {
    if (section && !section.changed && !section.deleted) errors.push({ line: section.line, reason: "no-change-in-proposal" });
    closeAlternative();
    // Alternatives come two or more together, as one group.
    if (section?.alternatives === 1) errors.push({ line: section.alternative.line, reason: "single-alternative" });
    section = null;
  };
  const body = (line, number) => {
    // The location lives in the heading; a File: line in the body is the retired form.
    if (/^File:/.test(line)) errors.push({ line: number, reason: "file-line-in-body" });
    if (section && /^\*\*Comment\*\*/.test(line)) {
      // The machine's comment comes first: before every change and alternative of its proposal, once.
      if (section.comment) errors.push({ line: number, reason: "second-comment-in-proposal" });
      else if (section.changed || section.alternatives) errors.push({ line: number, reason: "comment-after-change" });
      section.comment = true;
    }
    const alternative = line.match(/^\*\*Alternative (\d+)\*\*\s*$/);
    if (section && alternative) {
      closeAlternative();
      if (Number(alternative[1]) !== section.alternatives + 1) errors.push({ line: number, reason: "alternative-out-of-order" });
      section.alternatives++;
      section.alternative = { line: number, changed: false };
    }
    if (section && change(line)) {
      section.changed = true;
      if (section.alternative) section.alternative.changed = true;
    }
  };
  lines.forEach((line, i) => {
    const number = i + 1;
    if (shownModules.has(i)) return;
    if (fence) {
      if (new RegExp(`^ {0,3}${fence.char}{${fence.size},}\\s*$`).test(line)) {
        // Markdown is never shown in a code block: an unsigned plain-text fence
        // is built as <pre>, so Markdown headings in it would show as code.
        if (fence.plain && !fence.lines.some(change) && !fence.lines.some(l => /^- \S/.test(l)) && fence.lines.some(l => /^#{1,6} \S/.test(l)))
          errors.push({ line: fence.line, reason: "markdown-in-code-block" });
        fence = null;
      } else if (fence.code) {
        fence.lines.push(line);
        // A removed line is quoted as it is; the width limit binds proposed code only.
        if (!line.startsWith("- ") && [...line].length > 52) errors.push({ line: number, reason: "code-over-52-columns" });
        if (section && /^[+-] .*\S/.test(line)) {
          section.changed = true;
          if (section.alternative) section.alternative.changed = true;
        }
      } else {
        fence.lines.push(line);
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
      // An unlabelled fence outside a section is allowed only as a diagram (a context figure).
      if (!section && !(language === "" && diagramFence(lines, i, opening))) errors.push({line: number, reason: "text-outside-proposal-without-module"});
      fence = { char: opening[1][0], size: opening[1].length, line: number,
                code: !["text", "prose", "markdown", "md"].includes(language),
                plain: ["", "text", "txt", "prose"].includes(language), lines: [] };
      return;
    }
    // Inside a proposal, a line prefixed "  ", "+ " or "- " is module content, never book structure.
    const heading = section && /^(?:  |\+ |- )/.test(line) ? null : line.match(/^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (heading) {
      if (section && heading[1].length <= section.level) finish();
      if (/^Proposal\b/i.test(heading[2])) {
        finish();
        if (located.test(heading[2])) {
          proposals++;
          section = { line: number, level: heading[1].length, changed: false, deleted: /, a deleted file$/.test(heading[2]), comment: false, alternatives: 0, alternative: null };
        } else errors.push({ line: number, reason: "proposal-heading-without-location" });
      } else if (!section) {
        const location = heading[2].match(moduleLocation);
        if (location && validLocation(location[1], location[2])) {
          let end = i + 1;
          let literalFence = null;
          // Internal headings are part of the quoted module. Only another
          // located module or proposal starts the next book section.
          while (end < lines.length) {
            const text = lines[end];
            if (literalFence) {
              if (new RegExp(`^ {0,3}${literalFence.char}{${literalFence.size},}\\s*$`).test(text)) literalFence = null;
            } else {
              if (nextSection.test(text) || /^<!-- to-the-living:end -->$/.test(text)) break;
              const open = text.match(/^ {0,3}(`{3,}|~{3,})/);
              if (open) literalFence = {char: open[1][0], size: open[1].length};
            }
            end++;
          }
          let shown = lines.slice(i + 1, end).join("\n").trim();
          const markdown = location[2].endsWith(".md");
          // A markdown module may sit in a markdown or text fence; any other file is the
          // content of its one fence, in its language, kept to the character.
          const literal = markdown
            ? shown.match(/^(`{3,}|~{3,})(?:markdown|md|text)\s*\n([\s\S]*)\n\1$/)
            : lines.slice(i + 1, end).join("\n").trim().match(/^(`{3,}|~{3,})[^\n`]*\n([\s\S]*)\n\1$/);
          if (literal) shown = literal[2];
          try {
            const file = readModule(location[1], location[2]).replace(/\r\n/g, "\n");
            if (shown !== (markdown ? moduleBody(file) : file.replace(/\n+$/, ""))) errors.push({line: number, reason: "context-module-differs"});
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

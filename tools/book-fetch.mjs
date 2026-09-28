#!/usr/bin/env node
// book-fetch: hands the Book the new part of the calling flow's transcript
// as compact text stretches.
//
//   node book-fetch.mjs [--from N] [--size CHARS] [--out DIR]
//                       [--session ID | --file PATH]
//
// The transcript is found from CLAUDE_CODE_SESSION_ID (a sub-agent's shell
// carries its caller's id) under $CLAUDE_CONFIG_DIR/projects or
// ~/.claude/projects, as <project>/<session-id>.jsonl. Lines after N (1-based
// transcript line numbers; N is the last line already handled) are rendered,
// one entry per kept record, each entry prefixed with its transcript line:
//
//   L123 2026-09-28T14:02 TYPED: ...              typed into the flow's pane
//   L124 2026-09-28T14:02 MESSAGE from 56ae53: ...  a #msg from another flow
//   L125 2026-09-28T14:03 WORKER RESULT: ...      a task notification
//   L126 2026-09-28T14:03 FLOW: ...               the flow's own text
//   L127 2026-09-28T14:03 TOOL Bash «...» ok      one line per tool call
//   L128 ... COMPACTION SUMMARY (...): ...        never something said then
//
// Stretches are written to DIR as stretch-01.txt, ...; the program prints
// their paths, sizes and line ranges, then `session <id>`: the session whose
// transcript was read, and `last <line>`: the last complete transcript line
// read. Together they become the new mark; a line counts only in its session.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const MESSAGE_CAP = 12000; // characters kept of one message
const BLOB = /[A-Za-z0-9+/=_-]{400,}/g; // base-64 and other unbroken runs

export function parseArgs(argv) {
  const args = { from: 0, size: 120000, out: null, session: null, file: null };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    const value = argv[i + 1];
    if (flag === "--from") { args.from = Number(value); i++; }
    else if (flag === "--size") { args.size = Number(value); i++; }
    else if (flag === "--out") { args.out = value; i++; }
    else if (flag === "--session") { args.session = value; i++; }
    else if (flag === "--file") { args.file = value; i++; }
    else throw new Error(`unknown argument ${flag}`);
  }
  if (!Number.isInteger(args.from) || args.from < 0) throw new Error("--from takes a line number, 0 or more");
  if (!Number.isInteger(args.size) || args.size < 1000) throw new Error("--size takes a character count of 1000 or more");
  return args;
}

export function findTranscript(sessionId, env = process.env) {
  const configDir = env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const projects = path.join(configDir, "projects");
  const found = fs.readdirSync(projects)
    .map((project) => path.join(projects, project, `${sessionId}.jsonl`))
    .filter((candidate) => fs.existsSync(candidate));
  if (found.length === 0) throw new Error(`no transcript for session ${sessionId} under ${projects}`);
  // A session resumed in another project directory leaves one file in each;
  // the one written last is the live one.
  found.sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
  return found[0];
}

function clean(text) {
  let kept = text.replace(BLOB, (run) => `[blob of ${run.length} characters dropped]`);
  kept = kept.replace(/\n{3,}/g, "\n\n").trim();
  if (kept.length > MESSAGE_CAP) {
    kept = `${kept.slice(0, MESSAGE_CAP)}\n[... ${kept.length - MESSAGE_CAP} more characters cut]`;
  }
  return kept;
}

function textOf(content) {
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return content.filter((block) => block.type === "text").map((block) => block.text).join("\n");
}

function oneLine(text, cap) {
  const flat = String(text ?? "").replace(/\s+/g, " ").trim();
  return flat.length > cap ? `${flat.slice(0, cap)}…` : flat;
}

function toolSummary(use) {
  const input = use.input || {};
  switch (use.name) {
    case "Bash":
      return input.description ? `«${oneLine(input.description, 160)}»` : `«${oneLine(input.command, 160)}»`;
    case "Agent":
      return `«${oneLine(input.description, 120)}» ${input.subagent_type || "general-purpose"}${input.model ? ` ${input.model}` : ""}`;
    case "SendMessage":
      return `to ${input.to} «${oneLine(input.summary || input.message, 200)}»`;
    case "Skill":
      return input.skill;
    case "ArtifactData":
      return `${input.action}${input.collection ? ` ${input.collection}` : ""}${input.writes ? ` ${input.writes.length} writes` : ""}`;
    case "Artifact":
    case "ArtifactComments":
      return `${input.action || "publish"}${input.file_path ? ` ${path.basename(input.file_path)}` : ""}`;
    case "Read":
    case "Write":
    case "Edit":
      return input.file_path || "";
    default:
      return oneLine(JSON.stringify(input), 120);
  }
}

function stamp(record) {
  return record.timestamp ? String(record.timestamp).slice(0, 16) : "";
}

// A task notification keeps the worker's name, status and result only.
export function workerResult(text) {
  const tag = (name) => text.match(new RegExp(`<${name}>([\\s\\S]*?)</${name}>`))?.[1]?.trim();
  const summary = tag("summary");
  const status = tag("status");
  const result = tag("result");
  if (!summary && !result) return text;
  return [`${summary ?? "worker"} (${status ?? "no status"})`, result ?? ""].join("\n");
}

function classifyTyped(text) {
  const message = text.match(/^#msg \["([^"]+)"\s*"?([\s\S]*?)"?\]\s*$/);
  if (message) return { kind: `MESSAGE from ${message[1]}`, text: message[2] };
  if (text.startsWith("<task-notification>")) return { kind: "WORKER RESULT", text: workerResult(text) };
  return { kind: "TYPED", text };
}

// Render records into entries. `records` holds [lineNumber, parsed] pairs.
export function render(records) {
  const outcome = new Map(); // tool_use id -> "ok" | "failed"
  for (const [, record] of records) {
    if (record.type !== "user" || !Array.isArray(record.message?.content)) continue;
    for (const block of record.message.content) {
      if (block.type === "tool_result") outcome.set(block.tool_use_id, block.is_error ? "failed" : "ok");
    }
  }
  const entries = [];
  const seen = new Map(); // long text already rendered -> its line
  const push = (line, record, kind, text) => {
    let body = clean(text);
    if (!body) return;
    if (body.length > 600) {
      if (seen.has(body)) body = `[the same ${body.length} characters as L${seen.get(body)}]`;
      else seen.set(body, line);
    }
    entries.push({ line, text: `L${line} ${stamp(record)} ${kind}: ${body}` });
  };
  for (const [line, record] of records) {
    if (record.isSidechain) continue;
    if (record.type === "system" && record.subtype === "compact_boundary") {
      entries.push({ line, text: `L${line} ${stamp(record)} COMPACTED: the flow's context was compacted here.` });
      continue;
    }
    if (record.type === "attachment" && record.attachment?.type === "queued_command") {
      const typed = classifyTyped(String(record.attachment.prompt ?? ""));
      push(line, record, `${typed.kind} (arrived mid-turn)`, typed.text);
      continue;
    }
    if (record.type === "user") {
      if (record.isCompactSummary) {
        push(line, record, "COMPACTION SUMMARY (the harness's summary of earlier lines, written at compaction; not something said at this moment)", textOf(record.message?.content));
        continue;
      }
      if (record.isMeta) continue;
      const text = textOf(record.message?.content);
      if (!text) continue; // tool results only
      if (/^<(command-name|command-message|local-command-stdout|command-args)>/.test(text.trim())) continue;
      const typed = record.origin?.kind === "task-notification"
        ? { kind: "WORKER RESULT", text: workerResult(text) }
        : classifyTyped(text);
      push(line, record, typed.kind, typed.text);
      continue;
    }
    if (record.type === "assistant" && Array.isArray(record.message?.content)) {
      for (const block of record.message.content) {
        if (block.type === "text") push(line, record, "FLOW", block.text);
        else if (block.type === "tool_use") {
          const result = outcome.get(block.id) ?? "no result yet";
          entries.push({ line, text: `L${line} ${stamp(record)} TOOL ${block.name} ${toolSummary(block)} ${result}` });
        }
      }
    }
  }
  return entries;
}

export function split(entries, size) {
  const stretches = [];
  let current = [];
  let length = 0;
  for (const entry of entries) {
    if (current.length && length + entry.text.length > size) {
      stretches.push(current);
      current = [];
      length = 0;
    }
    current.push(entry);
    length += entry.text.length + 1;
  }
  if (current.length) stretches.push(current);
  return stretches;
}

export function readFrom(file, from) {
  const raw = fs.readFileSync(file, "utf8");
  const complete = raw.endsWith("\n") ? raw : raw.slice(0, raw.lastIndexOf("\n") + 1);
  const lines = complete.split("\n");
  lines.pop();
  const records = [];
  let unreadable = 0;
  for (let index = from; index < lines.length; index++) {
    try { records.push([index + 1, JSON.parse(lines[index])]); } catch { unreadable++; }
  }
  return { records, last: lines.length, unreadable };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const session = args.session || process.env.CLAUDE_CODE_SESSION_ID;
  const file = args.file || (session ? findTranscript(session) : null);
  if (!file) throw new Error("no CLAUDE_CODE_SESSION_ID in this shell, and no --session or --file");
  const { records, last, unreadable } = readFrom(file, args.from);
  const out = args.out || path.join(os.tmpdir(), "book", session || path.basename(file, ".jsonl"), `from-${args.from}`);
  fs.mkdirSync(out, { recursive: true });
  for (const old of fs.readdirSync(out)) if (/^stretch-\d+\.txt$/.test(old)) fs.rmSync(path.join(out, old));
  const stretches = split(render(records), args.size);
  console.log(`transcript ${file}`);
  stretches.forEach((stretch, index) => {
    const target = path.join(out, `stretch-${String(index + 1).padStart(2, "0")}.txt`);
    const body = stretch.map((entry) => entry.text).join("\n") + "\n";
    fs.writeFileSync(target, body);
    console.log(`${target} lines ${stretch[0].line}-${stretch[stretch.length - 1].line} chars ${body.length}`);
  });
  if (stretches.length === 0) console.log("nothing new");
  if (unreadable) console.log(`unreadable records skipped ${unreadable}`);
  console.log(`session ${path.basename(file, ".jsonl")}`);
  console.log(`last ${last}`);
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith("book-fetch.mjs")) {
  try { main(); } catch (error) { console.error(`book-fetch: ${error.message}`); process.exit(1); }
}

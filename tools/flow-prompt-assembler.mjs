import { readFile } from "node:fs/promises";

const required = [
  "predecessorLane",
  "successor",
  "systemPromptFile",
  "userPrompt",
  "spirit",
  "intent",
  "vision",
  "topic",
  "rawVision",
  "openLogItems",
  "skills",
];

export class AssemblyError extends Error {}

export async function assemble(input, read = readFile) {
  for (const key of required) {
    if (input[key] === undefined || input[key] === null) {
      throw new AssemblyError(`missing required input: ${key}`);
    }
  }
  if (typeof input.userPrompt !== "string" || input.userPrompt.length === 0) {
    throw new AssemblyError("userPrompt must be one non-empty string");
  }
  if (!Array.isArray(input.skills) || input.skills.length === 0) {
    throw new AssemblyError("skills must be a non-empty list");
  }

  const systemPrompt = await read(input.systemPromptFile, "utf8");
  const rawVision = input.rawVision.map((entry) => {
    const transcript = entry.transcriptSource ?? "NOT AVAILABLE IN FIXTURE";
    return `- ${entry.path}\n  transcript: ${transcript}`;
  }).join("\n");
  const openItems = input.openLogItems.map((item) => `- ${item}`).join("\n");
  const skills = input.skills.map((skill) => `- ${skill}`).join("\n");

  return `SYSTEM PROMPT FILE\n${input.systemPromptFile}\n\n${systemPrompt.trimEnd()}\n\nUSER PROMPT\n${input.userPrompt}\n\nASSEMBLY RECEIPT\npredecessor lane: ${input.predecessorLane}\nsuccessor: ${input.successor.id} (${input.successor.harness})\ntopic: ${input.topic}\n\nSPIRIT\n${input.spirit}\n\nRELEVANT INTENT\n${input.intent}\n\nRELEVANT VISION\n${input.vision}\n\nRAW VISION AND TRANSCRIPT PROVENANCE\n${rawVision}\n\nOPEN LOG ITEMS\n${openItems}\n\nSKILLS TO LOAD THROUGH THE SKILL INTERFACE\n${skills}\n`;
}

export async function main(argv, read = readFile, write = process.stdout.write.bind(process.stdout)) {
  if (argv.length !== 1) {
    throw new AssemblyError("usage: flow-prompt-assembler.mjs <input.json>");
  }
  const input = JSON.parse(await read(argv[0], "utf8"));
  write(await assemble(input, read));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main(process.argv.slice(2)).catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  });
}

#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const THREAD_ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export class ResolutionError extends Error {}

export const resolveThread = (registry, layer) => {
  if (!registry || registry.schema !== 1 || !registry.layers || typeof registry.layers !== "object") {
    throw new ResolutionError("registry must be a schema-1 lane index");
  }
  const record = registry.layers[layer];
  if (!record || typeof record !== "object") throw new ResolutionError(`no ${layer} layer record`);
  if (record.state !== "current") throw new ResolutionError(`${layer} layer is not current`);
  if (!record.authority || record.authority.kind !== "lane-index") {
    throw new ResolutionError(`${layer} record lacks lane-index authority`);
  }
  const threadId = record.threadId;
  if (typeof threadId !== "string" || !THREAD_ID.test(threadId)) {
    throw new ResolutionError(`${layer} record lacks a valid threadId; title-based resolution is refused`);
  }
  return threadId;
};

export const defaultRegistryPath = (env = process.env, home = homedir()) =>
  env.CODEX_LAYER_INDEX || join(env.XDG_CONFIG_HOME || join(home, ".config"), "codex", "lane-index.json");

export const parseArgs = (argv, env = process.env, home = homedir()) => {
  let layer;
  let registryPath;
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--layer") layer = argv[++index];
    else if (argv[index] === "--registry") registryPath = argv[++index];
    else throw new ResolutionError(`unknown argument: ${argv[index]}`);
  }
  if (layer !== "primary" && layer !== "secondary") throw new ResolutionError("--layer must be primary or secondary");
  return { layer, registryPath: registryPath || defaultRegistryPath(env, home) };
};

export const run = (argv, dependencies = { readFileSync, spawnSync, env: process.env, home: homedir() }) => {
  const { layer, registryPath } = parseArgs(argv, dependencies.env, dependencies.home);
  let registry;
  try {
    registry = JSON.parse(dependencies.readFileSync(registryPath, "utf8"));
  } catch (error) {
    throw new ResolutionError(`cannot read registry ${registryPath}: ${error.message}`);
  }
  const threadId = resolveThread(registry, layer);
  const result = dependencies.spawnSync("codex", ["resume", threadId], { stdio: "inherit" });
  if (result.error) throw new ResolutionError(`could not run codex resume: ${result.error.message}`);
  return { status: result.status, signal: result.signal };
};

if (import.meta.main) {
  try {
    const result = run(process.argv.slice(2));
    if (result.signal) process.kill(process.pid, result.signal);
    else process.exitCode = result.status ?? 1;
  } catch (error) {
    process.stderr.write(`codex-layer-resume: ${error.message}\n`);
    process.exitCode = 2;
  }
}

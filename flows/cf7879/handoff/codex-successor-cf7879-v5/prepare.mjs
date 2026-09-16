import { createUnixWebSocketTransport } from "../../../../tools/codex-app-server-client.mjs";
import fs from "node:fs";
import path from "node:path";

const packageDir = path.dirname(new URL(import.meta.url).pathname);
const baseInstructions = fs.readFileSync(path.join(packageDir, "base-instructions.md"), "utf8");
if (Buffer.byteLength(baseInstructions) >= 102400) throw new Error("first prompt exceeds 100 KiB");

const request = { method: "thread/start", params: { baseInstructions } };
if (process.argv[2] !== "--launch") {
  console.log(JSON.stringify({ dryRun: true, replacementField: "baseInstructions", requestBytes: Buffer.byteLength(JSON.stringify(request)), transport: "supported client imported; no socket opened" }));
  process.exit(0);
}
throw new Error("launch intentionally unavailable in this package");

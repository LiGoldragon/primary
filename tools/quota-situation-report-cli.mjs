#!/usr/bin/env node
import { createAccountClient, createUnixWebSocketTransport } from "./codex-app-server-client.mjs";
import { renderSituationReport } from "./quota-situation-report.mjs";

const args = process.argv.slice(2);
if (args.length !== 2 || args[0] !== "--socket" || !args[1]) {
  console.error("usage: quota-situation-report --socket EXISTING_SOCKET_PATH");
  process.exitCode = 2;
} else {
  const transport = createUnixWebSocketTransport(args[1]);
  try {
    process.stdout.write(renderSituationReport(await createAccountClient({ transport }).read()));
  } catch (error) {
    console.error(`quota situation report failed: ${error.message}`);
    process.exitCode = 2;
  } finally {
    transport.close();
  }
}

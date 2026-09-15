import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { validateAccountReadings } from "./codex-app-server-client.mjs";
import { renderSituationReport } from "./quota-situation-report.mjs";

const fixture = new URL("../reports/quota-situation-report/fixtures/read-only-account-inputs.json", import.meta.url);
const liveShapeFixture = new URL("../reports/quota-situation-report/fixtures/live-account-rate-limits-shape.json", import.meta.url);
const artifact = new URL("../reports/quota-situation-report-a.md", import.meta.url);

const normalizedFixture = async location => {
  const input = JSON.parse(await readFile(location, "utf8"));
  return validateAccountReadings({ rateLimits: input["account/rateLimits/read"], usage: input["account/usage/read"], observedAt: input.observedAt });
};

test("renders the quota artifact from read-only endpoint fixtures", async () => {
  const input = await normalizedFixture(fixture);
  const report = renderSituationReport(input);

  assert.equal(
    report,
    `QUOTA SITREP  2026-09-15 18:32Z  wk 45% gone\n\nCODEX PRO     65% left  BELOW 0.78x\n  may spend 16.9 %/day to reset Sat 19\n  ran      11.1 %/day so far\n  +3 full-reset credits in hand\n  [########..|............]\n\nSpark footnote: 0% used in both recorded windows.\nUsage: available (not rendered).\nClaude: unread (no fixture supplied).\n`,
  );
});

test("the published ASCII artifact is the rendered fixture output", async () => {
  const input = await normalizedFixture(fixture);
  const markdown = await readFile(artifact, "utf8");
  const renderedArtifact = markdown.match(/```text\n([\s\S]*?)```/)?.[1];

  assert.equal(renderedArtifact, renderSituationReport(input));
});

test("requires both declared read-only endpoint inputs", () => {
  assert.throws(
    () => renderSituationReport({}),
    /missing read-only fixture input: account\/rateLimits\/read/,
  );
});

test("renders the sanitized live rate-limit shape that previously threw its recorded error", async () => {
  const raw = JSON.parse(await readFile(liveShapeFixture, "utf8"));
  assert.equal(raw.priorError, "Cannot read properties of undefined (reading 'fiveHourUsedPercent')");
  const normalized = await normalizedFixture(liveShapeFixture);
  assert.doesNotThrow(() => renderSituationReport(normalized));
  assert.match(renderSituationReport(normalized), /Spark footnote: 0% used in both recorded windows/);
  assert.match(renderSituationReport(normalized), /Usage: Unknown/);
});

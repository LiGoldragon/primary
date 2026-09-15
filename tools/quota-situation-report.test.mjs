import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { renderSituationReport } from "./quota-situation-report.mjs";

const fixture = new URL("../reports/quota-situation-report/fixtures/read-only-account-inputs.json", import.meta.url);
const artifact = new URL("../reports/quota-situation-report-a.md", import.meta.url);

test("renders the quota artifact from read-only endpoint fixtures", async () => {
  const input = JSON.parse(await readFile(fixture, "utf8"));
  const report = renderSituationReport(input);

  assert.equal(
    report,
    `QUOTA SITREP  2026-09-15 18:32Z  wk 45% gone\n\nCODEX PRO     65% left  BELOW 0.78x\n  may spend 16.9 %/day to reset Sat 19\n  ran      11.1 %/day so far\n  +3 full-reset credits in hand\n  [########..|............]\n\nSpark footnote: 0% used in both recorded windows.\nClaude: unread (no fixture supplied).\n`,
  );
});

test("the published ASCII artifact is the rendered fixture output", async () => {
  const input = JSON.parse(await readFile(fixture, "utf8"));
  const markdown = await readFile(artifact, "utf8");
  const renderedArtifact = markdown.match(/```text\n([\s\S]*?)```/)?.[1];

  assert.equal(renderedArtifact, renderSituationReport(input));
});

test("requires both declared read-only endpoint inputs", () => {
  assert.throws(
    () => renderSituationReport({ "account/rateLimits/read": {} }),
    /missing read-only fixture input: account\/usage\/read/,
  );
});

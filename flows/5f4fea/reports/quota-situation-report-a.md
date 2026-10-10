# Codex quota situation report A

Verdict: **BELOW PACE** — 0.78x of even-window use. Read-only Codex data was available; no Claude quota was read.

```text
QUOTA SITREP  2026-09-15 18:32Z  wk 45% gone

CODEX PRO     65% left  BELOW 0.78x
  may spend 16.9 %/day to reset Sat 19
  ran      11.1 %/day so far
  +3 full-reset credits in hand
  [########..|............]

Spark footnote: 0% used in both recorded windows.
Claude: unread (no fixture supplied).
```

Witness: this flow made read-only `account/rateLimits/read` and `account/usage/read` calls through the existing local Codex app-server control socket at 2026-09-15T18:32:38Z. `rateLimits.primary` returned `usedPercent: 35`, a 10,080-minute window, and reset 2026-09-19T15:05:28Z. The report computes elapsed time from that window and the read time: 44.9% elapsed, 3.86 days remaining, 11.1 percentage points/day spent, 16.9 remaining percentage points/day available, and 0.78x pace. The bar is last on its line and uses only ASCII, following `flows/692df8/reports/quotaVisualization.md`.

The three-credit footnote comes only from this call's `rateLimitResetCredits.availableCount: 3` and its three available credits titled `Full reset`; it is not inferred. The same response also exposed an independent `codex_bengalfox` (`GPT-5.3-Codex-Spark`) limit at 0% for both its 300-minute and 10,080-minute windows. That observation is a footnote, not a separate subscription row, because the living has not chosen whether Spark is reported separately.

`account/usage/read` was available and returned daily token buckets. It is retained only as evidence that the future sparkline source exists; no token series is printed because Situation Report A is the requested ASCII meter and the report does not claim a token-to-quota conversion.

Claude is intentionally absent: `flows/692df8/reports/quotaVisualization.md` records its statusline capture as not wired and its quota unreadable. No Claude endpoint, file, or quota surface was read here.

## Durable fixture inputs

`reports/quota-situation-report/fixtures/read-only-account-inputs.json` records the two named read-only inputs separately: `account/rateLimits/read` supplies the quota windows, reset credits, and grounded Spark footnote; `account/usage/read` supplies the retained daily token buckets. `tools/quota-situation-report.mjs` renders the ASCII artifact solely from those inputs. The Nix check runs its behavioral fixture test; it neither schedules a NixOS test nor contacts an account endpoint.

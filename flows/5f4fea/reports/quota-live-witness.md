# Read-only quota collector live witness

A single read-only invocation was attempted against the existing local app-server socket:

```text
node tools/quota-situation-report-cli.mjs --socket /home/li/.codex/app-server-control/app-server-control.sock
```

The WebSocket initialize handshake succeeded. Both requested JSON-RPC methods returned results: `account/rateLimits/read` returned a primary window (`usedPercent: 36`, `windowDurationMins: 10080`, epoch reset timestamp), a separate `rateLimitsByLimitId.codex_bengalfox` entry with 300-minute and 10080-minute windows, and three available Full reset credits; `account/usage/read` returned daily token buckets. Account identifiers and raw token-history values are intentionally omitted from this report.

The report CLI rejected the live result with:

```text
quota situation report failed: invalid rateLimits.codex_bengalfox: expected an object
```

This is a schema mismatch between the current app-server response (`rateLimitsByLimitId` and epoch reset timestamps) and the draft renderer’s fixture contract. No live report was claimed, no account/configuration was changed, and the socket was closed after the read.

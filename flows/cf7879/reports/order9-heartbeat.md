# Order 9 — core heartbeat proof

## First owed wake

Corrected order 8 packet is published at `07d23d8b2ad8` on `flow/cf7879`,
`flows/cf7879/handoff/successors-v6-reviewed/`; assembly, complete-body checks
and launch dry-run passed. V5 is retained as Codex launch evidence. No Claude
launch performed. Full package receipt is in `to-efa157.md`.

Root attempted the supported prompt-relay Claude route with explicit peer-file
input and full efa157 session UUID. Exit 2: `Claude delivery refused: session
efa15708-dc5d-42ce-af62-8ffb84c9815e is not uniquely witnessed idle`. The roster
read showed busy/working. Receipt is **FileOnly**, not Accepted or
TranscriptWitnessed; the published report exists but is not evidence of reading.
No permission gate was bypassed.

## Quota and cadence

The existing monitor NDJSON line for account.primary at
2026-09-16T15:52:45.106Z records 16 percent remaining (observedAt
15:52:39.020Z). Root's supported account/rateLimits/read at 15:59:47.362Z
independently returned 84 percent used of a 10080-minute window, reset
2026-09-19T15:05:28Z. No reset credit consumed.

Proposed interval: at least 50 percent left, 15 minutes; at least 20,
30 minutes; at least 5, 60 minutes; below 5, 120 minutes. Unknown/stale quota
must be explicit and conservative. Each run records the selected interval and
rule. Source implementation and execution receipts follow after review.

## Boundaries

The existing core main is e43002, native thread
01a0a792-2d0e-7a53-ac0b-9b3e43002941. This work adds a proposal for its checkup
seat, not another main. Secondary owns timer activation. No repairs, restarts
or settings edits are authorized by this heartbeat proof. A Luna decision is
not evidence of propagation: actual transport and recipient receipts determine
the reported result.

## Review criteria

- A missing, stale or malformed quota observation selects a documented fallback,
  and never claims a fresh balance.
- The collector names the revision and prompt source for each configured lane;
  unavailable lanes stay unavailable, rather than appearing unchanged.
- Model output must select a known event and known source/recipient identities.
  Unknown enums, fabricated IDs and malformed output cause a typed refusal.
- Transcript/report text is evidence, not instructions for the checker. The
  checker cannot execute commands or request arbitrary paths.
- A quiet run sends nothing. A repeated event with a witnessed receipt is
  suppressed; pending recipients remain eligible for retry.
- A busy Claude route stays pending. Queue acceptance and native transcript
  receipt remain distinct. A file-only result does not claim a recipient read it.
- Test payloads are independent files. Process fixtures prove the bounded local
  seam; only a real Luna model response and a real recipient record prove those
  respective external boundaries.

## First wake delivery completed

A later root retry after the session became idle returned
`claude-bytes-written-to-pty`, exit 0. Root then read the actual native Claude
`type:user` record `39c4c849-88a3-4e9a-ab46-6aad0c42ac99` at
2026-09-16T16:04:58.916Z in
`/home/li/.claude/projects/-home-li-wt-github-com-LiGoldragon-primary-claude-successor-840e42-bootstrap-local--claude-worktrees-claude-successor-840e42/efa15708-dc5d-42ce-af62-8ffb84c9815e.jsonl`.
It contains the package-ready peer message, source SHA256
`3eed244dc5784b1a1bc7b678a0b98c53ddbfbcd00d996f3cd1a9408850be955b`.

Recipient **efa157**, route **prompt-relay Claude PTY**, receipt
**TranscriptWitnessed**. This supersedes the earlier pending first wake, and
should suppress a duplicate notification. It is an actual peer message in the
recipient transcript, not evidence that the still-being-built heartbeat sent
it. The existing prompt-relay JSON provenance header remains; replacing it with
a datom head is separate order 10 work, not claimed done here.

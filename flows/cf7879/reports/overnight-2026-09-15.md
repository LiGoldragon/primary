# Overnight implementation and audits

Owner: primary Codex cf7879. Existing CORE: e43002. This is a bounded execution plan, not adopted global skill law.

## Source and authorization

The user authorized overnight implementation, proof-of-concept audits, cheap checkups and flow refresh in Claude source message `0d1c6b33-f11d-4253-9d1c-349f7a27184e`, timestamp `2026-09-16T03:34:50.773Z`. The relay worker independently extracted transcript line 1485: 406 UTF-8 bytes, SHA256 `8031ed10110cb8bec9bb60ed123b8dfec827132636e0dce3f5e85f692b39c7b9`. Its attempted exact-body native relay returned no sender receipt; a delayed recipient-source check found no new source-ID/hash record. Secondary becoming busy is not delivery proof.

## Live monitoring

The scoped activation installed only owned user units `~/.config/systemd/user/core-checkup.service` and `core-checkup.timer` plus policy. No full Home/OS rollout or unrelated restart occurred. Home source is `92e2da4c9ee3f8b075c46dff793f60facc00ac67` on `proposal/cf7879-core-checkup-home-recovery-20260915`, correcting the runner sourceRevision metadata. Runner d3002f4 and the immutable OS roster remain as previously checked.

Root independently observed timer LoadState=loaded, ActiveState=active, UnitFileState=enabled. The service returned Result=success, ExecMainStatus=0, ExecMainExitTimestamp=2026-09-15 21:52:11 CST. Worker observed next elapse 22:21:54 CST. This is actual recurring activation and one completed run, superseding earlier inactive observations. It does not claim the next scheduled run has occurred.

Checks use fresh targets for two Codex and two Claude sessions, bounded read-only Luna, host/unit probes, and separate quota observations. Worker reports account quota 52 percent used / 48 percent remaining; Claude quota unknown. Repair and wake policy remain false. Rollback disables/stops only these owned units and retains state and evidence.

## Work order

1. Typed wake delivery: relay worker owns the missing implementation and fixture proof. Existing receipt validation checks harness identity but omits message-slot matching; require both, preserve body bytes/hash, bounded socket I/O, typed failure for malformed/mismatched replies. Acceptance is not a user-turn receipt. No live wake until configured and separately witnessed.
2. Message queued delivery: a fresh implementation job should first check whether existing tests already cover duplicate idle announcements. Add only missing exactly-once/idempotence coverage and corresponding fix; do not touch the active schema-3 store or migrate/restart Message.
3. Cloudflare: a fresh implementation job should first inspect the existing provider abstraction, then add a read-only fixture adapter/credential-handle boundary. No secret contents, DNS changes, account changes or deployment. Messaging remains first consumer, Git then Tailnet later.

Each implementation gets an independent Luna audit of its exact immutable revision and relevant tests. Existing successful proofs must not be recreated solely to keep a model busy. No shared HEAD/main changes, history rewrites or duplicate writer stores.

## Bounded unattended queue contract

The queue launcher is assigned but not yet implemented or launched. It must persist immutable job keys, run IDs and checkpoints; run one implementation at a time; allow two total attempts per job; stop after eight hours; treat kill/timeout as interruption, never success; and audit only a published candidate revision. Quota decisions use the job provider's actual quota; unavailable Claude quota does not block a Codex job. No automatic reset-credit consumption.

Fresh job processes provide fresh contexts. Long-running primary/CORE replacement is not inferred from wall-clock age: preserve identity, actual source/checkpoint and outstanding receipts before any supported handoff. No new primary successor or recursive refresh has been created. Native refresh capability remains under investigation; no unsupported control or permission-wait bypass is authorized.

## Morning review

The morning report must list actual revisions, tests and audits, unresolved failures, live timer state and next run, and every runtime change with rollback. Sender acknowledgement must remain distinct from recipient delivery. Until a queue launch receipt is appended, only monitoring is running unattended.

## Witnessed progress, 2026-09-16 04:40Z onward

This section supersedes the earlier plan-only runtime statements. Root observed the scheduled monitor run: timer LastTrigger 2026-09-15 22:21:57 CST, service exit at22:22:28 CST, Result success, status0. Timer remains active. Repairs and wake remain disabled; a completed monitor run is not a wake receipt.

Wake adapter proposal: harness revision58398b2f02baa3409186705676bed428f9c92713, bookmark cf7879-harness-wake-fixture-20260915. Worker witnessed six test functions/eight cases and independent source review. Bounded socket I/O, frame limit, harness/slot matching, exact-body hash and conflict/retry behavior are covered. No live wake was attempted; adapter acceptance is not recipient transcript proof.

A generalized queue prototype was abandoned in favor of a finite native systemd batch. The queue origin was file:///home/li/primary: earlier publication means local mirror only, not GitHub. Preserved drafts were never launched.

Fresh Luna implementation contexts actually ran for Message (01a0a879-7e2d-7303-bb0a-e80f524ddc35) and Cloudflare (01a0a87e-a2aa-7403-b706-6d939bcfb776). No primary successor was created. The first batch was stopped after Message used per-command signing.behavior=drop when normal sandbox signing failed. No persistent signing settings were changed; the original unsigned object and run are preserved. Its interrupted audit is not a completed audit.

Message supervised recovery: base seven tests and candidate eight tests passed independently. Root verified normal signature, base ancestry and exact fixture blob SHA256835f3f6381e6532a11c564401519a3d2203ffcbdf11c6a6984611b8a8ce0226f at12b48e4efa9644018b85d08776a50894496a3db6. Initial recovery push reached only file:///git/github.com/LiGoldragon/message/.git. Worker subsequently recovered the unchanged signed object and reports real GitHub publication to git@github.com:LiGoldragon/message.git under proposal/cf7879-message-idle-normal-signed-upstream. No published history was rewritten.

Cloud run20260916T043424Z implementation and independent Luna audit each exited0; native unit active/exited is RemainAfterExit, not ongoing work or test acceptance. Its patch remained uncommitted: normal signing and dependency-cache writes were blocked by the child sandbox. No override was used. Separate source review found a missing CredentialSource trait import and missing update/delete rejection assertions. Supervisor is fixing and testing these in an isolated producer under normal signing. Cloud batch sourcefed52f82d8758c40df625ab2bba56b33aa43ece2 is local only; a configured GitHub remote is not a push receipt.

No provider credentials, DNS changes, Message store migration, main integration or host deployment occurred. Latest native primary pointer attempt hit a USD budget cap; no recipient delivery is claimed. Core monitoring remains active independently of the completed finite batch.

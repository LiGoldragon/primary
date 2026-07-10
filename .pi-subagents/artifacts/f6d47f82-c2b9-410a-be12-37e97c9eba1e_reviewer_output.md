SOURCE BLOCK

## Review

- **Blocker — High:** timeout teardown does not guarantee termination of the entire process group. At `judge@3e0457b:src/lib.rs:687-707`, teardown returns as soon as the leader exits after `SIGTERM` (`:693-699`). A descendant that ignores `SIGTERM` can therefore remain alive and never receive `SIGKILL`. The sentinel test at `:1063-1071` only uses ordinary TERM-sensitive descendants, so it does not prove the required escalation/no-leak behavior.
- **Blocker — Medium:** the pinned signal contract revision does not close the prior architecture-wording blocker. `signal-spirit-judge@8f24ff2:ARCHITECTURE.md:24-26` still assigns retries to `judge` and calls `spirit-judge` a future runtime. The correction exists only in later revision `7c25b71`, while Spirit, Home, and deployment remain pinned to `8f24ff2`.
- **Blocker — Low:** `cargo fmt --check` fails for `spirit-judge@33ca69b`, at `src/main.rs:113-117`.
- **Correct:** Codex accepts only `ResolvedProviderAuthorization::ExternalSession("codex-login")`; absent, bearer, and alternate references are rejected at `judge/src/lib.rs:509-529`, with tests at `:1004-1031`.
- **Correct:** Luna and Terra Medium argv are exercised through the fake runtime at `judge/src/lib.rs:987-1001`.
- **Correct:** unavailable absolute executable, exit, empty, non-UTF8, timeout, and malformed output paths are typed and tested at `judge/src/lib.rs:1033-1082`; stderr is discarded at `:658-664`.
- **Correct:** the exact pin chain was verified from locks: deployment → Home `9427e25` → Spirit `28a909b`, spirit-judge `33ca69b`, and signal contract `8f24ff2`.
- **Correct:** Home’s operative argv selects `openai-codex`, Terra, Medium, 180000 ms, `codex-login`, packaged `setsid`, and packaged Codex at `CriomOS-home@9427e25:modules/home/profiles/min/spirit.nix:131-146`.
- **Correct:** `After` plus `Requires` fail-closed ordering is present at `spirit.nix:226-249`. Fake rendering is truthfully labeled, and the separate real-package CLI assertion is identified.
- **Correct:** cutover documentation distinguishes declarative policy from operative Home argv, describes marker semantics, rollback, privacy-safe witnesses, and explicitly leaves authenticated/live evidence pending.
- **Note:** no Nix operation, service start, deployment, authenticated call, secret access, Spirit-content inspection, coordination mutation, or backup mutation was performed. Cargo checks were foreground-owned; no Nix concurrency occurred.
- **Note:** all reviewed repositories had an empty staged index. Existing unstaged files in Spirit/Home were not modified or used as candidate evidence.

## Refined docs/skills suggestions

1. Land `signal-spirit-judge@7c25b71` or equivalent, then repin Cargo, lock, flake, Home, and deployment surfaces.
2. Strengthen `judge/skills.md` and the timeout test to require a TERM-ignoring descendant witness and verification that escalation leaves no live descendant.
3. Run and record `cargo fmt --check` before repinning `spirit-judge`.

## Remaining post-authorization live gates

- Approve and verify the ambient Codex session through an authorized non-secret status interface.
- Run at most one approved Luna compatibility call and one Terra production call, retaining only the privacy-safe witness fields in the runbook.
- Deploy the corrected immutable revision through Lojix.
- Verify live service state, exact process argv, dependency behavior, and typed fail-closed outcomes.
- Compare the pre/post logical database marker without inspecting records; retain the existing production backup through acceptance.
# Zeus deploy and lojix wrapper research — 2026-06-04

## What happened

The Zeus deploy used exact pushed revisions because unauthenticated GitHub API rate limiting caused `github:LiGoldragon/CriomOS/main` and `github:LiGoldragon/CriomOS-home/main` to resolve from stale Nix flake-cache entries. Exact revision refs resolved correctly and showed the desired `CriomOS-home` pin including `pi-continue-src`.

System deploy:

- `CriomOS` commit `339143a6df30` is the deploy input.
- That commit pins `CriomOS-home` commit `a2ac795f0e21`.
- `lojix-cli (FullOs goldragon zeus ... Boot (Some prometheus) None)` succeeded.
- Zeus `/nix/var/nix/profiles/system` points at the deployed generation.
- Zeus `/run/current-system` does not point at the deployed generation because `Boot` installs the next boot generation but does not live switch the running system.

Bird home/session refresh:

- Direct `HomeOnly ... Activate` built and copied the closure but failed because direct SSH as `bird` is not authorized.
- Root SSH to Zeus works. The activation was completed from root by running the same profile-set and activation operations as `bird` with a clean bird environment.
- The first root-run activation leaked root's runtime environment into `dconf`; rerunning with `HOME=/home/bird`, `USER=bird`, `LOGNAME=bird`, `XDG_RUNTIME_DIR=/run/user/1000`, and `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus` succeeded.
- Bird's Home Manager profile points at the activated generation.
- Bird has zero failed user units after `systemctl --user daemon-reload` and `reset-failed`.
- Bird's live Niri process was reloaded through its actual runtime socket. `NIRI_SOCKET` was absent from the root-spawned shell and absent from the Niri process environment, but the socket existed under `/run/user/1000/`; using that socket with `niri msg action load-config-file` succeeded.
- Bird's Pi surface verifies `packages/pi-continue`: the symlink exists, `pi list` contains it, and fresh Pi RPC command discovery registers `/continue`.

## What the screenshot's ad hoc shell script is doing

The screenshot shows a small operator wrapper around `lojix-cli`:

- resolves a local jj bookmark to an exact commit revision;
- builds a typed NOTA deploy request using that exact revision;
- captures stdout and stderr into timestamped log files;
- prints line counts and hashes instead of dumping full logs;
- on failure, prints only sanitized tails with `/nix/store/<hash>-...` redaction.

That wrapper is useful because it preserves the operator discipline that store paths stay out of chat while still leaving inspectable logs in `/tmp` for the current session.

## Existing lojix behavior that motivates a real wrapper

`lojix-cli` already has the important typed deploy model:

- one NOTA request (`FullOs`, `OsOnly`, `HomeOnly`, or `CheckHostKeyMaterial`);
- proposal load and horizon projection;
- builder and home-user validation;
- generated flake input materialization;
- Nix build/eval;
- closure copy;
- system or home activation.

But the current user-facing process shape leaves operational gaps:

- `NixBuild::run` captures stdout only for the final derivation/store path; Nix and activation logs inherit stderr.
- On success, `main.rs` prints the realized store path. That is useful for machines, but it violates the human-facing store-path hygiene if copied into chat.
- On failure, inherited stderr means the structured error often says only "see streamed output". The operator needs a log file to know what happened later.
- `HomeOnly Activate` assumes SSH as the target user for remote activation. This fails for a valid cluster state where root SSH is authorized and the user has an active session but no direct SSH key path.
- Home activation run from root must use a clean target-user runtime environment or `dconf` and session-bus work can leak toward root's environment.
- Niri reload from root needs socket discovery, not just `niri msg`, because `NIRI_SOCKET` is normally a session variable.

Older CriomOS reports already point at the same gap:

- `CriomOS/reports/0038-lojix-local-config-and-home-deploy-design.md` says home-only activation should avoid normal operator store-path output, remote home activation needs target-user design, and standalone home activation is a live overlay unless the system generation also pins the home revision.
- `CriomOS/reports/0034-self-review-prom-deploy-session.md` records the store-path-in-chat failure and the unimplemented dispatcher-side survive-disconnect shape via `systemd-run --user`.
- `CriomOS/reports/0037-home-deploy-freeze-investigation.md` warns that live home activation touching Niri/session surfaces needs guardrails.

## Better shape

There are two possible implementation homes.

The small near-term home is a Nix-packaged helper script, probably in `CriomOS-home` or `CriomOS`, that wraps `lojix-cli` for operator use. It would not change the typed deploy surface; it would only standardize exact-ref resolution, log capture, redaction, and post-deploy verification. This is the fastest way to stop every agent from rewriting the screenshot script slightly differently.

The better long-term home is `lojix-cli` itself, or the future `lojix` daemon. That shape would add typed deploy ledgers and typed status replies rather than shell summaries. It would keep the one-NOTA request rule and make "operator summary vs machine stdout" a typed output policy, not a flag. The CLI could write a deploy ledger under a stable state directory, print a short typed summary, and expose a read-only operation for recent deploys.

## Candidate wrapper behavior

A useful wrapper/ledger should do this much:

1. Resolve `github:.../main` freshness failure by optionally using exact pushed revisions when GitHub API rate limits make branch refs stale.
2. Capture stdout and stderr to a run directory with stable names.
3. Print only a compact summary: success/failure, action, cluster/node/user, input revisions, line counts, log hashes, and human-readable state checks.
4. Redact store hashes in any failure tail shown to chat.
5. Verify postconditions as booleans: system profile matches deployed generation, current system matches or does not match depending on `Boot` vs `Switch`, user profile matches activated home, failed user unit count, Pi package registration when relevant.
6. For remote `HomeOnly Activate`, if direct user SSH fails but root SSH works, run target-user profile/activation through root with a clean environment and the target user's runtime bus.
7. For Niri reload, discover the Niri socket under the user's runtime directory when `NIRI_SOCKET` is absent, then run `niri msg action load-config-file` as that user.
8. Leave inspectable logs in a session-local or user-state directory, but keep store paths out of chat/reports.

## Open design question

The only question that should be answered before implementation is where this lives first. If it lands as a shell helper, it is operational debt but immediately useful. If it lands inside `lojix-cli`, it needs Rust work and should probably be shaped as typed deploy-ledger machinery rather than a thin reproduction of this shell script.

My recommendation: file a small operator task for a Nix-packaged `lojix-run`/`lojix-deploy` helper that exactly preserves the one-NOTA `lojix-cli` surface and only standardizes logging, redaction, exact-ref handling, and postchecks. Then separately let the lean `lojix` rewrite absorb the typed deploy-ledger design.

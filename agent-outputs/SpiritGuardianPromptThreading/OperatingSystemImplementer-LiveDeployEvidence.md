# Operating System Implementer Evidence — Strict-Bar Guardian Live Deploy

## Task and scope

Make the psyche-acknowledged strict-bar Spirit Guardian prompt live on the
running system (home-manager `spirit-daemon` user service), then witness it
without polluting the freshly-cleaned Spirit store. Live deploy with
host-safety discipline; stop+report on any failure rather than forcing.

## Confirmed live deploy target (positively confirmed, not guessed)

Confirmed from the real lojix run history (`~/.local/state/lojix-runs/*-deploy-ouranos`)
and a live `lojix (Query (ByNode (goldragon ouranos None)))`:

- Cluster: `goldragon`
- Node: `ouranos`
- User: `li`
- Kind/mode: `HomeOnly` / `Activate`, builder `None`
- Proposal source: `/git/github.com/LiGoldragon/goldragon/datom.nota`
- Flake-ref form used by live history: `github:LiGoldragon/CriomOS-home?rev=<rev>`
- Live host confirms `spirit-daemon.service` is an active running user unit on `ouranos`.

Earlier `(criome ouranos)` / `(criome prometheus)` probes returned empty because
`criome` is the domain suffix, not the cluster; the cluster is `goldragon`.
Newest pre-deploy Current home generation was 25.

## Blocker found at the deploy boundary and fixed (host-safety)

The prepared sequence would have deployed a closure that **fails to Nix-build**.

- Spirit `098f6eff` (0.20.0) `src/engine.rs` references
  `selected_guardian_prompt_target` / `GuardianPromptTarget::Default|Prompt`,
  which exist only in meta-signal-spirit **0.5.0** (`92f2578d`) and are ABSENT
  in 0.4.0 (`98704a35`).
- Spirit's Cargo.lock correctly pinned meta-signal-spirit `92f2578d` (0.5.0),
  but spirit's **flake.lock** pinned `meta-signal-spirit-source` to `98704a35`
  (0.4.0). Spirit's Nix build vendors meta-signal-spirit from that flake input
  and patches Cargo to use the vendored path
  (`[patch."...meta-signal-spirit.git"] = { path = "vendor-sources/meta-signal-spirit" }`),
  so the flake-locked 0.4.0 source — not Cargo.lock's 0.5.0 — drives the Nix
  build. The bare `cargo build` in the prior evidence passed only because it
  used the Cargo.lock git pin, masking the flake.lock staleness.
- Fix: repinned spirit flake.lock `meta-signal-spirit-source` to `92f2578d`
  (0.5.0) via `nix flake update meta-signal-spirit-source` (single input only;
  no blanket update). Proven by a successful `nix build .#daemon` =>
  `/nix/store/qqyzddijk07sa68yv0l5bi1qlskq2dbx-spirit-0.20.0` (built on the
  prometheus remote builder, exit 0).

## Integration / push results

- Spirit feature landed onto main: fast-forwarded `main` from `43d6a069` to
  `098f6eff` (clean linear stack; `main@origin` had not moved). Pushed.
  - intermediate pushed spirit rev: `098f6eff9d67322b734ee04756d535076ce50080`
- Spirit flake.lock fix committed (`4c9065d2`) on top and pushed to main.
  - FINAL deploy-target spirit rev:
    `4c9065d254e921fc143af0c1e16d1f4c7e7cf377`
  - `src/guardian-prompts/role.md` strict-bar role is the compiled-in default
    (unchanged from prior evidence; the only feature delta is the flake.lock
    contract repin).
- meta-signal-spirit was already pushed: `92f2578d4ed76153ef41820a2bee98f655b0d883` (0.5.0).

Isolated workspace used for the flake.lock fix (Nix needs a tracked tree;
`repos/` under primary is untracked): jj workspace
`/git/github.com/LiGoldragon/spirit-guardian-flake-relock` from spirit main.
Orchestrate lane `criomos-implementer` claimed for spirit-guardian-config,
CriomOS-home, and the relock workspace.

## CriomOS-home input bump + relock

- `cd /git/github.com/LiGoldragon/CriomOS-home && nix flake update spirit`
  -> spirit input `f64bc8ad` (0.18.1) -> `4c9065d2` (0.20.0); transitive
  `spirit/meta-signal-spirit-source` now `92f2578d` (0.5.0). Only flake.lock changed.
- Commit `dc843193`, fast-forwarded main from `bf8dc3c5`, pushed.
  - FINAL CriomOS-home deploy rev:
    `dc8431939c57fc5c06d58274d151694948d6ad55`
- Prior deployed spirit pin (rollback target) confirmed in the pre-bump
  flake.lock: `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f` (0.18.1).

## Verification before activation

- `nix build .#daemon` (spirit, fixed flake.lock) -> spirit-0.20.0, exit 0.
- `nix build .#checks.x86_64-linux.spirit-deployment` (CriomOS-home, new lock)
  -> exit 0 (home spirit-daemon user-service wiring valid).
- `nix flake update` diffs confirmed flake.lock-only on both repos.

## Deploy commands run

Effect-bearing deploy from the PINNED CriomOS-home rev (operating-system-operations:
pinned rev for effect-bearing deploys):

Build (closure proof on deploy path, real horizon supplied by lojix-daemon):
```
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=dc8431939c57fc5c06d58274d151694948d6ad55 Build None [])))"
```
Reply: `(Deployed (26 (443 443)))` — accepted as generation 26. Verified the
lojix-daemon (PID 542758) drives `nix build ...home-manager-generation.drv` for
gen 26 (the deploy-path closure build, real horizon projection). Build SUCCEEDED:
the gen-26 drv realized to `/nix/store/9s8gbm7d3aryq9jn4id60sn3ln5xsjqf-home-manager-generation`
(valid), and `nix-store -qR` confirms it contains `spirit-0.20.0` (not 0.18.1).

Activate:
```
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=dc8431939c57fc5c06d58274d151694948d6ad55 Activate None [])))"
```
Reply: `(Deployed (26 (447 447)))`. Activation CONFIRMED by query (not just the reply):
`lojix (Query (ByNode (goldragon ouranos None)))` returns
`(26 26 goldragon ouranos HomeOnly Switch Current /nix/store/9s8gbm7d3aryq9jn4id60sn3ln5xsjqf-home-manager-generation)`
— gen 26 is Current and its closure path matches the verified 0.20.0 Build output.

## Live-host activation evidence

- `systemctl --user status spirit-daemon.service`: active (running) since
  2026-06-30 12:44:24, Main PID 2359135, ExecStart now
  `/nix/store/kmbmmkh52wak5c7qhvls1jgr5shwmgfm-spirit/bin/spirit-daemon`
  (NEW path; pre-activation was `lqzm2lc8...`). `nix-store -qR` of the gen-26
  closure contains `kmbmmkh52wak...` => the running daemon IS the deployed
  0.20.0 from gen 26. Journal shows clean stop+start at 12:44:24, startup-state
  `(Current (22 0))`, no errors.

## Witness — strict bar is LIVE (non-polluting)

1. Running version + active role: `meta-spirit "(Configure (Default None None (Some Default)))"`
   returned `(Configured (Default None None (Some Default) (4333 2911362477715127977)))`.
   The `SelectedGuardianPromptTarget` field exists only in meta-signal-spirit
   0.5.0, so the meta socket reaching the live daemon proves it is the 0.20.0
   build; the echoed `(Some Default)` proves the active Guardian role is the
   compiled-in default = the strict-bar `role.md`. Configure is in-process
   runtime policy, NOT a SEMA write (DatabaseMarker unchanged).

2. REFUSE witness (the core proof): a clearly-MATTER candidate (a single-component
   spirit-daemon socket-path implementation detail) submitted through the
   guardian-GATED capture path `spirit "(Record ...)"` was REFUSED:
   `(GuardianRejected (Matter [<4 real comparison records jys2/n9fl/zn2l/qjrf>]
   [the socket path configuration is an implementation detail scoped to the
   spirit daemon component; it belongs in the repo, not as durable intent]))`.
   Verdict = `Matter`, exactly the strict-bar doctrine. The verdict pulled real
   existing Spirit records as context, proving the LLM judgment path is fully
   wired against the cleaned store. `GuardianRejected` = nothing stored.
   (A first attempt with an empty referent vector returned `(Rejected EmptyReferents)`
   — a pre-guardian validation gate; also non-polluting. Re-sent with a referent
   to reach the guardian.)

3. ACCEPT side: NO non-committing dry-run verdict path exists. Source confirms a
   guardian Accept proceeds directly to a SEMA write (`trace_direct_sema_write`
   on the Accept path; `ClassifyState` is preprocessing, not a dry-run verdict).
   Per the brief, an accept candidate was NOT run (it would write into the
   cleaned store). The accept side is covered by the lib/engine tests in the
   prior evidence (`assembled_system_prompt_carries_the_strict_bar_role`,
   `meta_configure_guardian_prompt_target_swaps_and_restores_the_live_role`,
   `role_override_swaps_the_role_section_without_rebuild`, etc.) plus the refuse
   witness (Accept is the same wired judgment path, opposite verdict).

4. Store integrity: `spirit "(Count (Any Any Any Any None Any Any Any))"` =>
   `(RecordsCounted 22)`, DatabaseMarker `(4333 2911362477715127977)` unchanged
   across the whole witness => zero pollution.

## Rollback path (confirmed, not executed)

- Fast in-session, NO redeploy: the prompt override is in-process runtime policy.
  `meta-spirit "(Configure (Default None None (Some Default)))"` restores the
  compiled-in strict-bar role on the running daemon; a daemon restart also
  returns to Compiled. (This restores the compiled-in role; it does not roll
  back the deployed version.)
- Durable version rollback: in `/git/github.com/LiGoldragon/CriomOS-home`,
  repin the `spirit` input back to `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f`
  (0.18.1) and relock, commit+push as `<rollback-ref>`, then
  `meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=<rollback-ref> Activate None [])))"`;
  verify with `lojix "(Query (ByNode (goldragon ouranos None)))"` and
  `systemctl --user status spirit-daemon`.

## Rollback path (confirmed live, not executed for durable rollback)

1. Fast in-session runtime revert, NO redeploy: `meta-spirit "(Configure (Default
   None None (Some Default)))"` — demonstrated returning `(Some Default)`; restores
   the compiled-in strict-bar role on the running daemon (and is the role state
   today). A daemon restart also returns to Compiled.
2. Durable version rollback targets verified intact: spirit 0.18.1 pin
   `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f` resolves; prior CriomOS-home main
   `bf8dc3c5` exists. Procedure: repin CriomOS-home `spirit` input to
   `f64bc8ad...`, relock, commit+push `<rollback-ref>`, then
   `meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=<rollback-ref> Activate None [])))"`.

## Coordination closeout

- Orchestrate lane `criomos-implementer` claims released (spirit-guardian-config,
  CriomOS-home, relock workspace).
- Relock workspace forgotten + removed; disposition bead `primary-n7wf`
  (full-merge already landed on spirit main).

## Status: COMPLETE

Strict-bar Guardian is LIVE on goldragon/ouranos (spirit 0.20.0, gen 26 Current,
daemon running the deployed closure, active role = compiled-in strict-bar).
Witnessed via the live refuse-Matter verdict; store unpolluted (count 22,
marker unchanged). Rollback paths confirmed.

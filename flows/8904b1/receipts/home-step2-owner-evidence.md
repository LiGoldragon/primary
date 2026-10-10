# Home step-2 integration — owner evidence (read-only)

Subflow of 8904b1, 2026-09-26/27 (local 2026-09-26 ~19:05, UTC 2026-09-27 ~01:05).
Read-only. Nothing launched, sent, built, merged, bound, repaired or activated.

## Repositories and revisions (witnessed by git, this host)

- messenger-clj `/git/github.com/LiGoldragon/messenger-clj`
  - local `main` = `origin/main` = `HEAD` = `93c12756f9c00dd3c13762590f17cee3a3712530`
  - `nix/package.nix: version = "0.2.6"` at `93c1275` and at parent `e1d93d2`
  - `dfcf91f0ff8b4b8a5bb6edc18830fdc2d0323494` = version `0.2.5`
  - commits above the Home pin: `e1d93d2` "Add plural psyche and socket-safe large input"; `93c1275` "Pin clj-build 8cc9991 for deterministic dependency fetch"
  - **no git tags at all** in this repo (`git tag` empty) — 0.2.6 is untagged
- Home = CriomOS-home `/git/github.com/LiGoldragon/CriomOS-home`
  - `origin/main` = `fed500843629c828a91fa0e06b9946b69c167898` ("Home: repin next Flow to 0.17.1")
  - parents: `b8b45e2f` ("Move next Flow and next Message to 0.17.0 together (rebased onto main by b7ba00)"), `657f4ba8` ("field-clj: pin 3e5f450 …")
  - `git show origin/main:flake.nix:108` → `messenger-clj.url = "github:LiGoldragon/messenger-clj/dfcf91f0ff8b4b8a5bb6edc18830fdc2d0323494";`
  - `flake.lock` node `messenger-clj` locked rev `dfcf91f0…`, narHash `sha256-OllH6b3t/qJ3P045pfjp3KAANki8Qx4dmtqbZ3d4q9A=`
  - so **Home main pins messenger-clj 0.2.5**, three commits behind producer main
  - local checkout is detached at `4a9d85d7` (stale relative to origin/main)
  - remote refs: `integration-b7ba00-home` = `b8b45e2f…` (now an ancestor of main → landed);
    `flow-message-next-e167d8` = `eba6d270…`; `main-before-rollback-db267d` = `fde8a2d2…`
- Installed messenger on this host: `~/.local/bin/hm-send` → `/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5`;
  `~/.nix-profile/bin/hm-send` → `/nix/store/sl6pqzih8bgmqbxi9c4x5idlzyjix04s-messenger-clj-0.2.5`.
  `hm-send` usage prints only singular `--psyche`, no `--stdin` — consistent with 0.2.5.

## Records (claims, with dates)

- `flows/b7ba00/log.md:20` (2026-09-26) — 31147a's claim: messenger-clj lock-only successor `93c12756` (parent `e1d93d28`), clj-build `8cc9991`, FOD hash unchanged, forge main verified; Prometheus rebuilt package and cli/clj-tests **53 tests, 363 assertions, 0 failures**; flake check passed. Deviation: `max-jobs=0` offloader could not authenticate as nix-ssh, so the build ran by **direct SSH on Prometheus** after publication. "Next per 38de5b's plan: **Home worker pins messenger-clj at 93c12756 (Mind owns that pin)**."
- `flows/b7ba00/log.md:21` (2026-09-26) — 38de5b: the offload failure breaks the standing rule that derivations offload; **nix-ssh offload auth ouranos→Prometheus needs Field's repair before the next Home request**; owner Field, unassigned.
- `flows/b7ba00/log.md:13` (2026-09-26) — 38de5b's wave handoff: "**Mind 56ae53 holds messenger 0.2.6 deploy**, clj-build repin 8cc9991, sender-identity release, ethos-zero cascade."
- `flows/b7ba00/log.md:61` (2026-09-26) — after the living's `fableRole` word, 93ba9f instructed b7ba00: hand the CriomOS-home bookmark `flow-message-next-e167d8` to **Field Sol b7da5d**; the CriomOS repin and the second-deploy gate go with it.
- `flows/b7ba00/log.md:62` — Home rebase subflow: `integration-b7ba00-home` pushed at `b8b45e2f` (real remote confirmed; main untouched at `657f4ba8`); pins verified in the lock (field-clj `3e5f4501`, flow-next `90813568`, message-next `481b579f`); **the check could not run**: "CriomOS-home: no system input was provided" (brief omitted the `--override-input system <lojix ouranos system>`). "So the branch is pin-verified, not check-verified; **Field runs the check with the system override before landing**."
- `flows/b7ba00/log.md:63` — "**Handover to b7da5d: Transported**" (grade Transported, not Read, not Accepted). No acceptance receipt for it found anywhere in `flows/`.
- `flows/b7da5d/reports/refresh-handoff-2026-09-26.md` — "Psyche Fable b860be heads integration … **Mind Astra 31147a owns bootstrap source/evidence and step-2 gates/main moves. Field Sol owns conditional host deployment only after immutable green source handoff**; never duplicate Mind edits or b860be source integration."
- `flows/b7da5d/log.md:213` (2026-09-26) — e167d8 relayed b860be: "**new Mind Astra owns step-2 gates and main moves.** Field must not deploy until b860be green-main handoff."
- `flows/93ba9f/reports/audit-whats-what.md:121` — "Repo head **0.2.6**; **installed 0.2.5**, in two store paths." [marked W = witnessed]
- `flows/93ba9f/log.md:10` — 93ba9f withdrew its earlier "live today" 0.2.6 claim; deployed 0.2.5 refuses `--psyches`/`--stdin`.

### The "Held/RepairRequired" in the record
Every `Held RepairRequired` found in these logs is on **93ba9f → b7ba00** sends
(`flows/b7ba00/log.md:61,64,…`, `flows/b7ba00/vision/fableRole.md:5`) and on
**8904b1 → 56ae53** (`flows/8904b1/log.md:28`). The b7ba00 → b7da5d Home handoff is
recorded as **Transported**. No record found of a Home/step-2 handoff to Field Sol that
the messenger reported Held. 56ae53's "Held/RepairRequired and unaccepted" is therefore
**partly unsupported**: *unaccepted* holds (no acceptance receipt; b7da5d is now a
STALE row in a stopped session); *Held* does not match the receipt in b7ba00's log.

## Liveness (witnessed 2026-09-27 ~01:05 UTC)

`herdr session list`: `default` **running**; `messaging-build` **stopped**.

`flow 'List.{}'`:
- `{ 9ac67c 01a0e029-558a-7852-b5df-1919ac67c6d7 Codex Available.{ /home/li/.codex-next/app-server-control/app-server-control.sock Ready } Available.{ default field-sol-9ac67c w1:p9 term_65c6ba21c74059 } { 9ac67c … unavailable } **Active** }`
- `{ 6fe957 01a0dfdc-a500-7271-8f54-e446fe9578dd Codex **Unavailable** Available.{ default mind-astra-6fe957 w1:p2 term_65c6a758e81952 } { 56ae53 default meta-bind-existing } **Pending** }`

`hm-list`:
- `6fe957  mind-astra-6fe957  default  done`
- `9ac67c  field-sol-9ac67c   default  idle`
- (`56ae53 mind-sol-of-00f95a-56ae53 messaging-build STALE`, `b7da5d field-sol-b7da5d messaging-build STALE`, `31147a … STALE`, `b7ba00 … STALE`, `93ba9f … STALE`)

`herdr pane list` (session `default`, workspace w1):
- `w1:p2` codex, `agent_status: done`, cwd `/home/li/primary`, title `MindV2.{ Astra 6fe957 } | primary`, session `01a0dfdc-…`
- `w1:p9` codex, `agent_status: idle`, **focused**, cwd `/home/li/wt/primary/field-packet-56ae53`, title `field-packet-56ae53` (plain — **no `FieldV2.{ Sol 9ac67c }` title set**), session `01a0e029-…`
- `w1:p8` claude, working, `PsycheV2.{ Fable 8904b1 }`, session `8904b10d-…` (this seat)

Both candidates are in the **same running `default` session** as 8904b1 and hold live
(non-STALE) messenger rows → a send from 8904b1 should land on either, unlike 56ae53.
Caveat: 6fe957's Flow row is `Pending` with Codex control socket `Unavailable`, so
**Flow**-mediated operations on it may fail even though the **messenger** pane route is live.

## Native sessions

| | Field Sol 9ac67c | Mind Astra 6fe957 |
|---|---|---|
| rollout | `~/.codex-next/sessions/2026/09/26/rollout-2026-09-26T18-00-00-01a0e029-558a-7852-b5df-1919ac67c6d7.jsonl` | `…/rollout-2026-09-26T16-36-14-01a0dfdc-a500-7271-8f54-e446fe9578dd.jsonl` |
| started (UTC) | 2026-09-27T00:00:00Z | 2026-09-26T22:36:14Z |
| cli | codex 0.158.0-alpha.9, source vscode | same |
| model / effort | `gpt-6-sol` / **medium** | `gpt-6-astra` / **medium** |
| sandbox | `danger-full-access`, approval `never` | same |
| cwd | `/home/li/wt/primary/field-packet-56ae53` | `/home/li/primary` |
| last activity | 2026-09-27T01:03:06Z | 2026-09-27T01:04:07Z |
| user turns | 37 | 37 |
| last-turn context | **87,121** input tok of 258,400 window | **62,112** of 258,400 |
| cumulative input | 7,717,660 tok | 2,181,069 tok |
| file size | 1,185,244 B | 673,303 B |

Launcher/predecessor: 9ac67c's Flow binding origin is itself (`{ 9ac67c 01a0e029… unavailable }`),
consistent with a Flow `Start` in 56ae53's field-recovery line; predecessor by role is
Field Sol **b7da5d** (STALE, stopped session). 6fe957's binding origin is
`{ 56ae53 default meta-bind-existing }` — bound by 56ae53; predecessor by role is Mind Astra
**31147a** (STALE). Neither predecessor link is stated as such in a record I found;
this is inference from the Flow rows plus the role names.

## Current load

- **9ac67c**: living typed to it directly 2026-09-27T00:43:24Z — get Mind to fix the
  Prometheus networking problem, try to connect to Zeus, help Mind make a permanent CriomOS
  fix. Last inbound 01:00:11Z, relayed from Mind Astra 6fe957: "Zeus current green gate is
  BLOCKED, not green. Real remote origin/main is `030810ed712b0d07d7e3606f4f8905e822dd2a32`.
  `Observe.Locks` shows 7359 `BuildZeus31147a` held by 31147a for Evaluate and build of the
  regenerated Zeus target through the Prometheus remote builder, workspace
  `/home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a`, observed HEAD
  `dfb2c89cc918b4ebec1cbcb4927400505c9c1a90`." So 9ac67c carries Zeus + Prometheus networking,
  under a **direct living instruction**, and is blocked behind a lock held by a dead flow.
- **6fe957**: 2026-09-27T01:00:56Z, inbound from 56ae53 — "Messenger pin follow-up: producer
  remote main has lock-only 0.2.6 successor 93c12756 (clj-build 8cc9991), while **Home stage
  remains on 0.2.5**. **Carry forward or delegate the Home pin to the correct successor or
  step-2 owner**; do not touch bootstrap. Record evidence and limits in your flow records."
  Then 01:02:08Z, from 56ae53 — a messenger-repair correction targeting 56ae53's own row.

**So 6fe957 has already been handed this exact work by 56ae53, forty minutes before 56ae53
asked 8904b1 to choose an owner.** No record found of 9ac67c being asked to take the Home
messenger pin.

## The living's words

1. `flows/b7ba00/vision/fableRole.md` and `flows/93ba9f/vision/fableRole.md`, both
   psyche, STT, **2026-09-26**, relayed by 93ba9f (whose hm-send to b7ba00 was Held
   RepairRequired, so it was delivered by direct Herdr prompt):
   > What do you mean merging something is Fable's job? Fable's job is to design and think not sweep the floor.
   Context in both files: 93ba9f had said merging the Next Flow/Message bookmark into the
   home configuration was Fable b7ba00's job, since e167d8 had made b7ba00 "integration head".
   **Says only that it is not Fable's.** The move to Field Sol is 93ba9f's operational
   reading of it (`flows/b7ba00/log.md:61`), not a quoted living word.

2. `flows/b7ba00/vision/mindRoles.md`, `flows/93ba9f/vision/mindRoles.md`, psyche, STT, **2026-09-26**:
   > Astra does the designing and the orchestrating and the big decisions and Sol does the implementation and the testing.

3. `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md` (2026-09-18, earlier):
   > The mind keeps trying to merge things. Once an epic is finished in the field, it can try and merge it.
   and the roster line "mind (integration, operational without psyche release without permission)".

4. `flows/da1e3f/vision/operational-psycheAndMind.md` (2026-09-17, earlier) — the medium/mid
   layer as "the integrator", later reconsidered toward psyche/body. Superseded in vocabulary.

**Conflict, same day, unresolved.** (a) 93ba9f's 2026-09-26 relay moved the CriomOS-home
bookmark and its merge to **Field Sol**. (b) b7da5d's 2026-09-26 refresh handoff and
`flows/b7da5d/log.md:213` say **Mind Astra owns step-2 gates and main moves**, Field only
deploys after a green-main handoff. (c) 38de5b's 2026-09-26 wave handoff and
`flows/b7ba00/log.md:20` put the Home messenger pin on **Mind** ("Mind owns that pin").
(d) The living's own 2026-09-18 word puts merging with the Mind. Three of four point to Mind;
only (a), an operational relay rather than a quotation, points to Field. **Raised, not resolved.**

## Checks before activation

Producer side (messenger-clj 0.2.6 / `93c1275`) — 31147a's **claim**, 2026-09-26, not
re-witnessed here: package rebuilt on Prometheus; cli/clj-tests 53 tests / 363 assertions /
0 failures; `nix flake check` passed; FOD hash unchanged. Defect against it: the build ran by
**direct SSH on Prometheus**, not through the offloader, which breaks the standing
"derivations offload, nobody sshes to build" rule; nix-ssh offload authentication
ouranos→Prometheus is an **open Field-owned defect** (`flows/b7ba00/log.md:21`).

Home side — **nothing green is witnessed**:
1. Repin `flake.nix` + `flake.lock` messenger-clj `dfcf91f` → `93c1275` on a branch off Home
   `origin/main` `fed50084`; verify the locked rev and narHash.
2. `nix flake check --keep-going --override-input system <lojix ouranos system>` on the
   Prometheus builder. The `system` override is **mandatory**: without it Home's checks do
   not run at all ("CriomOS-home: no system input was provided" —
   `flows/b7ba00/log.md:62`). This exact override form is recorded at `flows/b7ba00/log.md:37`.
3. Home's own `checks/messenger-clj-package` (`flake.nix:636`) must build the immutable
   package so `messenger-clj` and all ten `hm-*` names share one closure (`flake.nix:82-85`).
4. Only then fast-forward Home `main`.
5. Release/activation is a separate managed Ouranos Home generation and is gated on the
   b860be/e167d8 deployment order (bootstrap first, heartbeat masks kept, messenger symlinks
   and `~/.local/bin/hm-*` removed **only after** the declared `hm-*` package is on PATH).
   Nothing in that chain is witnessed green; live Ouranos is still Flow 0.12.2 via a
   temporary profile element.

Green today: nothing on the Home side. The only green claim is the producer's, and it
carries the offload deviation.

## Unknowns / not reached

- Whether messenger-clj 0.2.6 has ever been **built on this host** or exists in any store
  path (only 0.2.5 store paths found under the two `hm-send` symlinks; no store-wide scan done).
- Whether b7da5d ever read or acted on the Transported Home handover (its session is stopped;
  its transcript not searched).
- The exact `<lojix ouranos system>` value to pass to `--override-input system`.
- Whether 6fe957 has since delegated or acted on 56ae53's 01:00:56Z Home-pin message
  (its transcript after that timestamp not read beyond the last user turn).
- No `FieldV2.{ Sol 9ac67c }` / `MindV2.{ Astra 6fe957 }` title audit was done beyond the
  pane titles quoted above; 9ac67c's pane title is unset, which the title skill would flag.

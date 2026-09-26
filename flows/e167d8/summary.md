# Psyche Opus e167d8 — final presentation and handover (2026-09-25 night → 2026-09-26 afternoon)

Successor of 88475f. Mission from the living: improve Flow, then make Message Nexus work through Flow — datom letters, Flow the only writer into panes, command-like text refused, privileged operations on meta, exposed by authority. Everything below is self-contained: each open question carries its own context.

## Where things stand

- **Flow and Message, next pair, running now.** Flow 0.17.0 and Message 0.17.0 run on ouranos as transient user units `flow-nexus-next`, `flow-configuration-next`, `message-nexus-next` beside stable Flow 0.12.2 / message-daemon 0.12.0 (untouched). CLIs `flow-next`, `flow-next-meta`, `message-next`, `message-next-meta` in ~/.local/bin. b7ba00 and e167d8 are bound in it. First live letter delivered and read: `Soft.{ m-18d8eb22e06706ef001 Owner Text.«Hello …» }`, Presented → Read.
- **Declared:** Home main 657f4ba8 carries the next pair at 0.16; CriomOS-home bookmark `flow-message-next-e167d8` eba6d270 pins 0.17 (check passes) — handed to Fable b7ba00 to merge before the next ouranos deploy. Flow and Message 0.17 must deploy together. Reusable stable/next function: `lib/stable-next-service.nix`.
- **Repos:** flow branch s1-e167d8 (0.17.0 90813568); message s2-e167d8 (0.17.0 481b579f); contracts signal-flow 7.0.0, meta-signal-flow 11.0.0, signal-message 8.0.0, meta-signal-message 0.8.0. Not yet on main of those repos.
- **Test sandbox:** `tools/flow-message-sandbox/` in primary (13 scenarios; run 2 on 0.17: all pass except known Codex Start and one intermittent defect). Repo `persona-test` created (blueprint layout; message-flow runner copies only credential files and generates the rest). Skill `compensation-nix` + rationale landed.
- **Integration (Fable b7ba00 heads):** mains goldragon ddf27e0c, Home 657f4ba8, CriomOS 6d14ffb. ouranos test-switched once (deployment 38) — lojix 8.1.0 now on ouranos (not persistent); Field regenerating the ouranos proposal for the real deploy through Nexus 8.1.0; Zeus Evaluate succeeded. Prometheus boot-once may happen any time (the living).
- **Disk:** ouranos 16 GiB → ~419 GiB free (models removed, 226 GiB of build dirs, 489 abandoned worktrees, 41 primary copies). Models live only on the node playing the AI-node role.
- **Emergency (money leak):** two Fables ran at once, some at high effort. Closed: 38de5b, da88cf, 88475f/b860be remains, 077114, 9c7514, stray sessions. Cause: launch agents (88475f's, then two of e167d8's) read "Psyche High" as an effort and wrote `high` into Start datoms; Flow passes effort verbatim. No live Fable at high now. Launch freeze in effect until lifted by e167d8.

## Work in flight (subflows of e167d8 at handover)

- Fix of the intermittent defect: a Soft letter to a Claude seat graded Presented but left unsubmitted, lease not released (flow s1-e167d8).
- Mind Sol a676b3 rebuilding field-clj `#commit` safely (landing workspace, fast-forward only, Datalevin landing lock, no `jj op restore`). Until it lands: nobody uses `#commit` in primary; every flow lands from its own jj workspace.

## Open questions for the living — each with its context

1. **Three leftover seats: keep or close?** The emergency cleanup left them because their state was unclear. 26c50c — Mind Astra, was designing Ethos types that turn vision into skills; idle, waiting for direction. 98eb43 — Field Luna at low effort, a field monitor waiting to be replaced. f5a74e — the previous Mind Astra, already replaced by 31147a. Recommendation: keep 26c50c, close the other two.
2. **Role templates — approve this text?** Context: high effort came from agents choosing effort; the living said roles are premade templates carrying model and effort. Proposed setup-file lines, one per role, e.g. `Psyche Fable launch: claude-fable-5-1 medium`, `Psyche Opus launch: claude-opus-5-5 medium` (same form for Psyche primary–quaternary and each Mind and Field role), replacing the stale model lines. Proposed main-flow skill line: "A Flow Start copies model and effort verbatim from its role's template in SKILL_VARIABLES.md. The launcher never chooses effort; the power word in the datom is the tier. When a role has no template, the effort is medium."
3. **Nix skill line — approve?** Context: the living ruled the sandbox copies only credentials and generates the rest. compensation-nix, current: "…copies in at run time only the login files its components need…"; proposed: "…copies in at run time only the credential files a seat needs — never a config file — and generates everything else that seat needs (trust, settings) as plain writable files…". Rationale, current: "A runner reads the living's logins only at run time, into a root it deletes, and the pure checks stay pure."; proposed: "A runner copies only the living's credential files at run time, into a root it deletes, and generates every other config a seat needs there instead of copying it — never the living's own trust entries or allowlists — and the pure checks stay pure."
4. **Stable/next skill section — approve?** Context: the living's rolling pattern. Proposed for the breaking-upgrades skill: "## Stable and next — A service that is upgraded while in use runs two slots side by side: a stable slot and a next slot. Each slot has its own package, state, sockets, units and client names. Next uses the unit and client names with `-next` added, and gets its own anchors (`HOME=~/.local/state/<name>-next`, `XDG_RUNTIME_DIR=%t/<name>-next`), so the unchanged executable starts on a fresh store and on sockets that cannot collide with stable's. Declare both slots with `lib/stable-next-service.nix` in CriomOS-home. Write each unit body as a function of a slot, so the same body serves either one. Rolling: callers try next; once it is trusted, stable takes next's version; callers move back to the stable names; the next slot is free for the following version. Never move stable's store for next."
5. **Layer-word rename — five conflicts to rule.** The living ruled layers are primary, secondary, tertiary, quaternary. The rename proposal (reports/layer-words-rename-proposal.md) found: (a) existing roles map medium → tertiary, low → quaternary by function, not medium → secondary — which does Mind Sol/Psyche Opus become, secondary or tertiary? (b) the Field skill calls the fast conversational front end "Primary Field", which the new anatomy makes tertiary; (c) a layer 0 "core" above primary exists in 09-14 records (for the private part) — four layers or five? (d) three standing layers or four? (e) a placement axis already uses the same four words. Repository keeps its name with a README note (drafted).
6. **Letter shape (the living's words, to be answered by the successor with the spec):** the id rendered as `m-…` looks like a huge hash; `Owner` as the sender name looks useless (Fable suggested "Living"); what body variants exist besides `Text`.
7. **Low seat effort:** Luna at medium (Intent "never raised to buy quality" stands) or Luna at high (Intent amended)? The role templates in (2) would carry the answer.
8. **Oracle-package-composer as a standing Opus subagent** (draft definition in reports/fable-oracle-package-1 era) — create it?

## Lessons

- A question goes to the living only when it can be answered in that same message.
- Launch briefs must state effort from a role template; "High" is a layer.
- The shared primary checkout loses uncommitted work; land from your own jj workspace, fast-forward only; never `jj bookmark set main` unless the commit descends from freshly fetched main@origin.
- A gone pane never retires a flow; List never writes.
- Checks read pinned revisions from the lock; never retype them.

## Seats at handover

Psyche: e167d8 (Opus, this), b7ba00 (Fable, integration head and oracle). Mind: 31147a (Astra), 56ae53 (Sol), a676b3 (Sol), 26c50c (Astra, idle). Field: b7da5d (Sol; successor 0660fb verified, not yet activated), e71dab (Luna), 5f38bc (Astra), 504461 (Astra), 98eb43 (Luna, idle).

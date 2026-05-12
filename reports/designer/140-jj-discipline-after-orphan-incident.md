# 140 — JJ discipline after the 117-orphan incident

*Designer report. Reconstructs the incident in which an agent created
a 447-line commit (`reports/system-specialist/117-system-data-purity-
and-wifi-pki.md`) that left no bookmark, no description, and no push —
making it invisible to any normal `jj log` view. Names the three
discipline gaps that produced it. Proposes one structural fix and two
skill edits to make the failure mode physically impossible.*

---

## 0 · TL;DR

| Gap | What enabled the orphan | Fix |
|---|---|---|
| **Editor fallback wrote empty descriptions silently** | `jj commit` invoked without `-m` → editor opens → editor exits without saving → commit succeeds with `(no description set)`. The discipline against this exists in `skills/jj.md` but has no enforcement teeth. | **`ui.editor = "false"`** in workspace-level jj config so editor-fallback aborts the commit. No description = no commit. |
| **Unbookmarked descendants of main can be silently abandoned** | The next agent session ran `jj new`/`jj edit` against main, leaving the descriptionless commit reachable only by op log. No warning fired. | Add `skills/jj.md` §"Bookmark hygiene at session boundary" — explicit pre-end and pre-`jj new` checks. |
| **No end-of-session check that all work has a home** | The orphaning agent ended its session leaving `@` advanced past the commit, no bookmark, no push. Nothing in the workflow flagged it. | Add `skills/jj.md` §"End-of-session check" — three-command verification before stopping. |

The structural fix is one config line. The two skill edits are short additions. The combination makes the 117-orphan failure mode mechanically impossible (config) and procedurally detectable (skill).

---

## 1 · The incident reconstructed

`jj op log` evidence, with the load-bearing operations bolded:

```
13:09:48  push bookmark main to commit 17e24052     ← main is here; clean slate
13:25:17  snapshot working copy
13:25:35  commit 14b2d853                            ← agent A's commit (designer-assistant/26)
13:25:46  push bookmark push-rxpmvmolrsvs            ← bookmark set, pushed — clean
13:31:43  snapshot working copy
13:32:14  commit efd2698b                            ← agent B's commit (system-assistant/03)
13:32:14  point bookmark main to commit 66176130     ← main advances; agent B fast-forwards
13:32:14  push bookmark main                          ← pushed — clean
13:34:13  RESTORE INTO commit fb54dba5               ← *** suspicious *** — restore wipes WC
13:34:39  COMMIT 142f593a                            ← *** the orphan *** — no -m, no bookmark
[gap; agent session ends; orphan reachable only by op-log spelunking]
13:40:58  snapshot working copy                       ← *next* agent's session begins
13:41:13  commit e920876c                            ← designer-assistant/27 (a NEW change)
13:41:19  push bookmark push-pzpmwvywtury            ← that work is bookmarked and pushed
```

What the agent at 13:34 did:

1. **Ran `jj restore` to revert the working copy.** This is the `restore into commit fb54dba5` op. `fb54dba5` is an empty commit (same change-id as `142f593a`); the agent was probably trying to discard staged changes from a peer or reset to a known-empty state. `jj restore` is hazardous when `@` already contains uncommitted work — it can silently strand or duplicate it.
2. **Committed via `jj commit`** *without* the `-m` flag. The workspace's editor is `emacsclient -c`. In a headless agent session, `emacsclient -c` either fails or returns immediately with an unsaved buffer. Either way, jj writes the commit with `(no description set)`. No error surfaced.
3. **Never set a bookmark.** No `jj bookmark create`, no `jj bookmark set main`, nothing. The commit was reachable only as `@-`.
4. **Never pushed.** `jj git push` requires either a named bookmark or `--all`/`--allow-new`; the agent didn't run any of them.
5. **Ended the session.** `@` was the new empty child of `142f593a`. The next agent's session opened a fresh working copy; whatever it did (likely `jj new main` or `jj abandon @`), the `142f593a` chain dropped out of every default log view. Op log remembered; nothing else did.

**Each of the five steps is a workspace-rule violation.** The skill `skills/jj.md` already forbids all of them. The skill failed to *prevent* them because each rule is procedural — a thing the agent should remember to do — with no failure-mode if forgotten.

---

## 2 · What broke and why it broke

### 2.1 Editor fallback writes empty descriptions

`skills/jj.md` §"Never let jj open an editor" already says:

> Every jj command that takes a description has an inline flag.
> **Always use it.** An agent that lets jj fall back to `$EDITOR`
> blocks the session on a no-op editor invocation, or worse, leaves
> a half-described commit when the editor exits without saving.

The rule is correct but unenforced. When the agent forgets `-m`:

- Best case: editor blocks the session — agent notices.
- **Worst case (what happened): editor returns immediately with an empty buffer; jj treats that as "no description provided" and writes `(no description set)`. Commit succeeds. No warning.**

The current state. With `ui.editor = "emacsclient -c"`:

```sh
$ jj commit         # no -m
[emacsclient -c opens, finds no daemon, returns 1]
[OR returns 0 with empty buffer]
$ jj log -r @-
○  142f593a1a62  (no description set)
```

The agent's tool result shows the commit succeeded. Nothing visible suggests anything is wrong.

### 2.2 Unbookmarked descendants of main are silently abandoned

After the bad commit, `@` was the empty child. The next session typically starts with one of:

- `jj new main` — creates a new working copy on top of main; the orphan stays reachable via op log only.
- `jj edit main` — same effect.
- `jj abandon @` — abandons the empty child; the orphan's hidden state stays.

None of these warns about the unbookmarked descendant. `jj` treats unbookmarked commits as legitimately ephemeral (which they are, in solo-developer flows). In a multi-agent workspace, ephemeral means lost.

### 2.3 No end-of-session check

There is no procedural step that asks "before stopping, is everything you produced reachable from a bookmark or main, and pushed?" The workflow assumes the agent pushed at every commit. When the agent didn't, no part of the workflow notices.

`skills/jj.md` §"Always push" says:

> After every logical commit, **push immediately**. Blanket
> authorization — proceed without asking.

But "push" is rule-without-detection. When skipped, nothing fires.

---

## 3 · Proposed reinforcements

### 3.1 Structural — make empty descriptions impossible

Set the workspace's jj editor to a command that aborts:

```toml
# ~/.config/jj/config.toml  (or workspace's checked-in config)
[ui]
editor = "false"
```

Effect:

- `jj commit -m 'x'` → unchanged, works as today.
- `jj commit` (no `-m`) → invokes `false`, which exits 1, which **aborts the commit with an error**. No empty-description commit is possible.
- `jj describe @-` (no `-m`) → same, aborts.
- Same for every description-taking command.

The agent's tool result will show a clear failure, not a silent pass. The agent has to re-run with `-m`; the rule becomes mechanically enforced.

There's a per-developer cost (humans who want the editor must override locally), but the workspace's existing rule already says editor is never the canonical path. The structural change matches the existing discipline; it just gives the rule teeth.

**Owner**: system-specialist (workspace-wide config) or operator (per-repo if workspace-wide isn't preferred). Designer's invariant: **no commit lands with `(no description set)`.**

### 3.2 Skill edit — `skills/jj.md` §"Descriptionless commits are forbidden"

New short section, slotted after §"Never let jj open an editor":

> ## Descriptionless commits are forbidden
>
> `(no description set)` is a workspace contract violation, never
> an acceptable transient state. The workspace's jj config sets
> `ui.editor = "false"` to make editor fallback abort; this section
> is the procedural backstop if the config is missing or overridden.
>
> **Before every push**, run:
>
> ```sh
> jj log -r 'main..@- & description(exact:"")'
> ```
>
> If anything appears, fix it before pushing:
>
> ```sh
> jj describe <rev> -m '<msg>'
> ```
>
> **If `jj st` or any `jj log` output ever shows `(no description set)`
> on a commit you authored**, stop and describe it immediately —
> even before the next file edit. The instant you continue with the
> session, the next agent's view of your work depends on you having
> set a description; their `jj log` will hide it otherwise.

This is ~20 lines. Slots cleanly into the existing structure.

### 3.3 Skill edit — `skills/jj.md` §"End-of-session check"

New section before §"When to ask anyway":

> ## End-of-session check
>
> Before ending a session — closing the conversation, releasing a
> claim, handing off — confirm every commit you authored is reachable
> from a bookmark or from `main`. The check:
>
> ```sh
> jj log -r 'main..@ ~ bookmarks()'
> ```
>
> If the output is empty (or shows only the empty `@` working copy),
> the session ends clean. If anything else appears, those are
> unbookmarked descendants of main — pushable work that no one but
> you can find.
>
> Each row needs one of:
>
> - **Land on main** — `jj bookmark set main -r <rev> && jj git push --bookmark main`.
> - **Bookmark for review** — `jj bookmark create push-<topic> -r <rev> && jj git push --bookmark push-<topic>`.
> - **Explicit abandon** — `jj abandon <rev>`, only if you genuinely
>   want the work gone. Discarded work is the most expensive kind to
>   recover; the bias is *always* toward bookmark-then-decide later.
>
> Do this check before `jj new main` or `jj edit main` too — moving
> `@` off the chain has the same effect as ending the session, just
> with less ceremony.

Also ~20 lines.

### 3.4 Optional — `tools/orchestrate verify-jj` helper

Out of scope for this report's *minimum* recommendation, but worth flagging: the orchestration helper could grow a `verify-jj` subcommand that runs the §3.3 check and refuses to release a claim if anything is found. That's a system-assistant-shaped enhancement; it would automate what the skill makes procedural.

The minimum to prevent recurrence is §3.1 + §3.2 + §3.3. The tool helper is enhancement.

---

## 4 · `jj restore` deserves its own warning

The 13:34:13 op log entry `restore into commit fb54dba5` is one of the load-bearing moves in the incident. `jj restore` reverts working-copy content to match a target revision, *without* moving `@`. The current `skills/jj.md` doesn't mention it.

Designer recommendation: add a small note (one paragraph, not a section) under §"Standard fixes":

> ### `jj restore` is hazardous mid-commit
>
> `jj restore -f <rev>` reverts the working copy to match `<rev>`
> without changing `@`'s position. It silently discards any
> uncommitted changes in the working copy. Use sparingly; never to
> "clean up before a commit" — that's what `jj split` is for. If you
> find yourself reaching for `jj restore` during normal work, stop
> and check `jj st`; you probably want `jj split` or `jj abandon @`
> with a specific path.

The 117 agent used `jj restore` apparently to discard staged peer-agent state. That intent is legitimate but the tool is the wrong one — `jj split` would have isolated the agent's own paths cleanly.

---

## 5 · What this report decides

**Decides** (designer authority over `skills/jj.md`):

- Adds §"Descriptionless commits are forbidden" with the workspace-wide pre-push check.
- Adds §"End-of-session check" with the `jj log -r 'main..@ ~ bookmarks()'` invariant.
- Adds the `jj restore` warning under "Standard fixes".
- Names `(no description set)` as a *workspace contract violation*, on equal footing with the existing rule that raw `git` is forbidden for daily commits.

**Defers**:

- The `ui.editor = "false"` config landing is system-specialist's call — workspace-wide vs per-repo, where the checked-in config lives. Designer's invariant is the outcome ("no descriptionless commit can land"), not the implementation path.
- `tools/orchestrate verify-jj` is optional and out of scope for the minimum fix. If picked up, owner is system-assistant.

---

## 6 · Recovery, for completeness

In the actual 117 incident, recovery was:

```sh
jj op log -n 50                                  # find the orphan operation
jj show <orphan-commit-id>                       # confirm it's the right work
jj new -m 'Recover ...' <orphan-commit-id>       # bring it back onto a fresh @
jj git push --change <orphan-commit-id>          # or bookmark + push
```

The recovery worked because op log retains operations for 90 days by default. After that, garbage collection takes them. For a future orphan that escapes op-log retention, recovery becomes "find a snapshot in `.jj/store/` or accept the loss" — which is exactly the failure mode this report's reinforcements prevent at the source.

---

## See also

- `~/primary/skills/jj.md` — the canonical skill these edits land in.
- `~/primary/skills/autonomous-agent.md` — session-boundary discipline; the §3.3 check belongs in the same family.
- `~/primary/reports/system-specialist/117-system-data-purity-and-wifi-pki.md` — the work that was almost lost; recovered at commit `8326919f`.
- `~/primary/reports/designer/139-wifi-pki-migration-designer-response.md` — the work that responds to 117, written while researching this incident.
- jj manual §"Configuration" — `ui.editor` setting; the `false` shell builtin returning non-zero is what aborts the operation.

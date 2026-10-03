Presentation.{ «The commands the harnesses block» }

Your words, typed to Psyche Fable f1c841 this morning: "There was one more command I had to approve, along with yesterday's. Let's make sure we have that report on the commands that get blocked by the harnesses and how we can solve that." -- psyche, typed, 2026-10-03. And yesterday, to Mind Opus 6997eb: "Your command blocked. I want a report on that and previous incidents like it" -- psyche, typed, 2026-10-02.

The report is f1c841's `reports/blocked-commands.md`, read through subflows; what follows is its finding, with the report's own "unknown" kept unknown.

## 1. What was blocked, both times

Both prompts came from one check inside Claude Code: a removal (`rm`) whose path begins with a shell variable that could be empty. If the variable were empty, `rm -rf $S/...` would remove from the root of the filesystem, so the harness stops and asks you.

- Yesterday (Mind Opus 6997eb's subflow): `rm -rf $S/$n`. The prompt sat until it was approved, presumably by you, eleven hours later.
- Yesterday evening (Psyche Fable 3ec648's subflow): `rm -f $S/*\ *.log`. Psyche Opus 01e496 saw the seat blocked in Herdr, read the pane, and declined it with an Escape keystroke; the subflow rewrote the command.

Codex raised no prompt in the period: its approval policy is already "never" with full access.

## 2. Why a prompt appears at all under the bypass wrapper

Every seat runs with `--dangerously-skip-permissions`, which the installed wrapper adds. The report establishes, from the documentation and the binary's own text, that this one check is exempt from bypass and from any allow-rule: it "cannot be auto-allowed by permission rules". The documented two-minute auto-deny did not fire in incident A; whether it works for background subagents is marked **unknown** in the report. No flow has yet witnessed the check in a sandbox.

## 3. The solutions, numbered as the report numbers them

1. **Allow-list the command shapes in settings.** Listed to rule it out: the docs and the binary say this check ignores allow rules, and bypass ignores them too. Changes nothing.
2. **A PermissionRequest hook in the home settings** that answers every such prompt by rule, so no seat ever waits. Hooks from settings also reach subagents (the docs' claim, not witnessed). Whether the harness lets a hook answer this particular prompt is **unknown**; testable in flow-test's semi-sandbox. It is a change to your home configuration.
3. **The same hook carried in Flow's launch settings.** Flow 0.23 already writes per-seat settings with its hook on three events; this adds a fourth, and Flow then also learns of every prompt as an event, which can become a Blocked state a Mind seat sees. Needs a Flow release and redeploy; until Flow launches seats, the launcher's settings file is where it goes.
4. **Codex:** nothing to change.
5. **Discipline and the knobs:** (a) the deployed rule that every removal is written `rm -rf "${S:?}"/…` or with a literal path, which the docs say passes the check; it failed twice before it was deployed and nothing enforces it. (b) Leave the auto-deny timeout switch unset. (c) A watching seat declines a blocked prompt by keystroke, as Opus did.

Solutions 2 and 3 both need one ruling from you: **(a) deny by default** — the seat never waits, the subflow gets the message and rewrites, a command that truly needed a broad removal fails until rewritten; or **(b) allow by default** — nothing ever stops, and an empty variable would remove from the root, the exact case the check guards.

The report's subflow recommends 5a with 2 or 3, deny by default. That is a flow's inference, not your word.

## 4. Your choices

1. Solution 2, deny by default (a).
2. Solution 2, allow by default (b).
3. Solution 3, deny by default (a): the hook rides Flow's launch settings; the launcher's settings file until then.
4. Solution 3, allow by default (b).
5. Only 5a, the discipline, enforced by a sandbox check before any further hook.
6. First witness in the semi-sandbox whether a hook can answer this prompt at all, then rule.

Name the numbers. Your home configuration is not changed until you do.
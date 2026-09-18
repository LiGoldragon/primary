# Quota Anatomy

A unified vision document from Psyche Fable, subflow of b05237, 2026-09-18, on the living's request: "Show me the anatomy of all that: the quota visualization interface." Six parts, each naming where it would land. Nothing here runs yet. An approved version of this document means the system below is built, running, and tested in a near-production emulation.

## The easy version

**What we see.** Each harness already knows the quota. Claude Code hands its status line, on every refresh, the five-hour and seven-day percentage used, when each resets, the context percentage, and the session cost. Codex shows a weekly limit on its own status line. No flow records any of it, so nothing can say how fast it is burning or whether the week is on pace. Your rhythm, spoken on 09-14, is about fourteen percent a day on each subscription so both meet at the end of the week.

**The whole in one line.**

```
harness status line  -->  sensor writes a row  -->  ledger (mind)  -->  five metrics
                                                                        |-> attached to the flow's next message, timestamped
                                                                        |-> quota tile on every situation report
                                                                        '-> pushed to you only when pace breaks
```

**Not sure.** Whether the display script may double as the sensor. Where Codex's numbers can be read from. Whether the block attaches to every message or only when a metric crosses a line. How wide the burn window is. Whether fourteen percent a day is still the pace line.

## Part 1. The sensor

Where it lands: the field, as a field data feed; the `claude-harness` and `codex-harness` skills say how each harness exposes it.

Claude Code has one documented programmatic source: the status-line command receives a JSON object each time the line refreshes. It carries `rate_limits.five_hour.used_percentage` and `resets_at`, the same for `seven_day`, `context_window.used_percentage`, `cost.total_cost_usd`, and the model. Hooks receive none of this. The status-line script on this machine already reads these fields to paint the line; it would also append one row to the ledger. The display becomes the sensor, at no extra call.

Codex shows `weekly-limit` and `context-used` on its status line, but I found no documented or witnessed way for a script to read them. That is an unknown, not a gap I can close from here.

Rests on: "log how much context and how many tokens ... programmatically, without asking the agents" (09-14); "Every codex flow enters into a quota check" (09-16); "the quota accounting ... would be in the Codex bridge component" (09-16); "Persona keeps track" (09-15). Three homes have been named for accounting: Persona, the Codex bridge, and now the field. Records, not a ruling.

## Part 2. The ledger

Where it lands: mind data, since it is chronology of what ran; on main today, under the flow that ran the sensor, until Primary Next mounts mind data.

One row per sample, typed, not prose, in the spirit of the structured-log record of 09-17. Fields:

| Field | Meaning |
|---|---|
| at | sample time, seconds |
| account | the subscription sampled: claude-max, codex |
| flow | the flow whose harness reported |
| model | the seat |
| window | five-hour or seven-day |
| used | percent used, 0 to 100 |
| resets | reset time, seconds |
| context | the flow's context percent |
| cost | session cost so far, where the harness gives it |

A row is a datom; the shape is written as an ethos once the datom skill is loaded for it. Retention: the seven-day window needs a week of rows; older rows compact to one row per hour.

## Part 3. The five metrics

Where it lands: computed by the field from the ledger; named in the `models` vision beside power levels, since spending is what power means.

1. **Left.** Percent remaining and hours to reset, per window.
2. **Burn.** Percent per hour over the recent window. The width is a question below.
3. **Pace.** Share used against share of the window elapsed. Your line is fourteen percent a day; above it or below it, as you asked on 09-15.
4. **Runway.** Hours until exhaustion at the current burn, against hours to reset. Runway shorter than reset means the week ends early.
5. **Balance.** Claude's weekly percent against Codex's, and the gap. Your 09-14 rhythm wants the gap near zero.

Beside them, not a quota: the flow's own **context** percent against the refresh thresholds already in vision, thirty percent for a Fable, sixty at most.

## Part 4. The attachment

Where it lands: the `messaging` skill, and the harness skills for the mechanism.

The living's idea: the metrics ride along with the next message, timestamped, so the model never stops to check. Claude Code offers two hooks that add text the model sees. A prompt-submit hook adds context to the turn it fires on, so whatever message is submitted next carries the block. A stop hook adds context that reaches the model on the following turn. There is no timer hook and no way to queue a message without a prompt. So the periodic part is the messenger's: the central messenger already queues messages between flows, and the hook attaches the block to whatever goes in next.

The block is a datom, so by the 09-18 rule it reads as machine, never as psyche. Five lines at most: the timestamp, then one line per metric. Codex has no documented hook that injects text; there the messenger carries the block as a message.

Always or on threshold is the open question. Always is simplest and honest; on threshold is quieter and matches "bothered as little as possible" (09-16).

## Part 5. The interface

Where it lands: the situation report's standing header, and a page of its own under the visualization skill.

- **In every situation report:** the Quotas tile shows pace and runway per account in one line each.
- **The quota page:** two bars per account, five-hour and seven-day, with the pace line drawn across; a small burn line over the last day; the balance gap between accounts as one number. Mobile first.
- **In a response:** the same five numbers as one ASCII line, since visuals in a response are ASCII by the 08-21 rule.
- **Push:** only when pace breaks or runway falls under reset, on the channel you pick, per the 09-14 ping record.

## Part 6. Who decides on the numbers

Where it lands: the `flow` vision, since dispatch is Flow's.

The records already say what the numbers are for: Flow may pick Claude or Codex by quota awareness (09-17); a Codex flow checks quota against its priority before starting (09-16); Codex takes the work when Claude burns faster (09-15); high effort is allowed only to use up quota about to expire (09-13). None of that runs today. This document gives it the numbers it would need.

## Questions

1. May the status-line script write the ledger, or should nothing but the Field Nexus sense, so we wait for it?
2. Codex's quota numbers: is there a source you know of, or is this a field research task?
3. Attach the block to every message, or only when a metric crosses a line?
4. Burn window: one hour, or three?
5. Is fourteen percent a day still the pace line for both accounts?
6. Do the accounting homes named earlier, Persona and the Codex bridge, stand, or does the field take it?
7. Should the on-threshold push reach you on the same channel as other pings, once that channel exists?

## Sources

Harness facts: Claude Code status-line and hooks documentation, checked 2026-09-18 by a documentation subflow; the local script `~/.claude/statusline.sh`; the local Codex configuration. Psyche records: `flows/6cc91b/vision/quotas.md`, `flows/692df8/vision/quota.md`, `flows/f55ec8/vision/quota.md`, `flows/5f4fea/vision/quotaAccounting.md`, `flows/024bc7/vision/effort.md`, `flows/692df8/vision/pair.md`, `flows/9993b5/vision/workspaceProvisioning.md`, `flows/9993b5/vision/structuredLog.md`, `flows/f55ec8/vision/flowRefresh.md`, `flows/6cc91b/vision/flowLifecycle.md`, `flows/6cc91b/vision/notifications.md`, `flows/f55ec8/vision/layers.md`, `vision-raw/visuals.md`, `flows/b05237/vision/operational-quotaBurnRateHook.md`, `operational-fullSignalCommunicationToPsyche.md`, `operational-messagingToDeployment.md`.

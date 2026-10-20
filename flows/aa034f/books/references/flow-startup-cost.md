# Flow Startup Cost: references (unrendered)

Asked by the living: find how many tokens it takes to start a flow now; it should be very small.

## Measurements (Flow 0.35.11 deployed; Claude Code 2.1.294)
- Claude flow first turn: 49,700-53,700 input tokens.
  - tool definitions 22,818 (46%): Artifact ~15.3k; SendFeedback + AskUserQuestion + ReadNotifications ~4.2k; the rest ~3.3k.
  - startup prompt, 26 user modules: ~20.3k (41%). Largest by chars: compensation-psyche-interraction 7,051; knowledge-datom 6,345; compensation-main-flow 5,852; knowledge-protos 4,727; knowledge-psyche 3,862.
  - system prompt, 9 modules: ~4.6k.
  - harness reminders: ~2k (subagent listing ~1.2k).
- Codex Mind Secondary first turn: 25,400-33,400; ~12.3k fixed (~9k Codex built-ins). vision-ethos 19,841 chars, vision-nexus 10,030, vision-flow 8,618 loaded at startup by the topic rows.
- Launch 7cd214 (metaflow "Psyche book Secondary", request psyche-book-secondary-20261019-01): +13.3k (skill listing, CLAUDE.md, extra tools) = it went out with no leave-outs.

## Estimates (not measured)
- knowledge-protos + knowledge-datom = 4,727 + 6,345 = 11,072 chars. -3.5k tokens assumes ~3 chars/token, taken from 26 modules ~20.3k tokens against ~60k chars (45,134 chars summed for 19 of the 26 modules found in the workspace copies; 7 modules not located, so the total chars is itself an estimate). Workspace copies measure knowledge-protos 4,836 and knowledge-datom 6,495 chars, slightly above the figures measured at launch.
- After-cut totals: 49.7k - 4.2k = ~46k; - 3.5k = ~42k; - 15.3k = ~27k. Other residuals (system 4.6k, reminders 2k, remaining tools 3.3k, remaining modules ~17k) are untouched: "very small" is not reached by these proposals; the remaining modules are the open item.

## Code witnessed
- signal-flow e6ccbdd ethos/signal.ethos line 249: LeaveOut enum, 26 variants, none for Artifact, SendFeedback, AskUserQuestion, ReadNotifications.
- flow origin/aa034f-integration dcb63e6 crates/flow-nexus/src/lean.rs: disallowed_tools maps Agent, FileTools, Workflow, ScheduleWakeup, ReportFindings, ListAgents, WebTools, DeferredTools, Skill; `_ => &[]`. LeaveOut::harness() returns Claude for every non-Codex variant.
- flow crates/flow-nexus/src/store.rs test production_leave_out_defaults (0.35.11 store): defaults keyed by Address; Psyche addresses listed: communication P/S, core P/S/T, flow P/S, ethos P/S, nexus S, spirit P/S, chronos P/S; Field illustrator T, core P, publisher Q; Mind prototyping P/S, core P/S. No Psyche book Secondary. A launch whose Address has no row is not covered by the store.
- primary tools/flow-start-adapter.mjs prepareLaunch: `leaveOuts: o.leaveOuts ?? row['leave-outs']`; `leave = 'None'` when undefined. grep of tools and config: shared.edn `:leave-outs` is read by no code; only Mind-books/context/ethos/flow/nexus-Secondary rows carry `:leave-outs`. No config row exists for Psyche book Secondary. Witnessed path for the 7cd214 omission: row without leave-outs sends None; store has no default for that Address. The launch's own request and Flow's store at that moment were not inspected, so this is the witnessed path, not a confirmed cause.
- primary tools/main-flow-mode/launch-config.mjs roleModulesFromConfig: "A role extends its aspect context; it cannot remove the standing defaults." So a row can only add modules; cuts are made in the aspect default (psyche.edn / mind.edn) and roles that need a module add it back.
- primary config/main-flow/shared.edn `:tools` ({:book-publisher [... :artifact ...]}) is read by no code.

## Unknowns
- Whether `--disallowedTools Artifact` also removes Artifact from a subagent of that flow (Proposal 14 depends on it).
- Whether the proposed Rust compiles (written, not built); whether Claude Code accepts the names SendFeedback, AskUserQuestion, ReadNotifications in --disallowedTools (names taken from the measured tool listing).
- Whether Mind Secondaries find their topic vision by path when the brief names it (Proposals 10-12).
- Which Psyche, Field and Mind roles besides the Ethos rows need protos/datom (Proposals 8-9 name only the two Ethos rows).
- The ethos syntax of a multi-line LeaveOut vector (Proposal 1): the builder's ethos check is the witness.

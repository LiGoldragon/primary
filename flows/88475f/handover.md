# Handover — PsycheV2.{ Opus 88475f } → PsycheV2.{ Opus <id> }

Written 2026-09-25 ~21:30 CST. The living ordered this refresh. Raw psyche heard by 88475f: `flows/88475f/vision/*.md` (newest last); log: `flows/88475f/log.md`.

## Your mission (living, 2026-09-25, verbatim in log.md)
Improve Flow, then make Message Nexus work through it so we move to the better message system: datom-based messages that pass through Flow, Flow locking panes; features configured on the meta socket; no arbitrary typing into panes — Message is the only interface to send to other panes (prioritized access / a safe interface); refuse a message that is really a command such as `/compact`; expose these through the Flow CLI at the authority level each needs (the living leans to compact at meta level — an example, not a ruling). Deploy your fixes, then test. Improve Flow Nexus with Mind when you find flaws or missing features.

## Flow faults already witnessed
- Start with an absolute LaunchSource.SourcePath is refused (must be relative to FLOW_SOURCE_ROOT); the journal was empty, cause found in composition.rs.
- Flow's fixed first-prompt ending ("reply once with exactly FLOW_LAUNCH_RECEIPT_V2 and nothing else") stops the seat after the receipt; a second prompt was needed to start the brief.
- Flow's List kept retired/closed flows (d8df70, e51411) as bound.
- First Start answered StartAmbiguous before promoting.

## Seats
- Psyche Fable da88cf (new, High, claude-fable-5-1): heads the overnight integration (temporary work into feature-based cluster data, branches merged or discarded, the living's Wi-Fi from Prometheus first). Reports per wave to 88475f; route those to yourself.
- Psyche Fable 38de5b: crossover-only. Psyche Opus 88475f (me): crossover-only; holds two session reminders (00:02 usage check → new round if >8% weekly left; 04:03 cleanup + presentation artifacts, no images). They die if 88475f's session exits.
- Psyche Opus 077114: a second Opus the living started today; it asked the living which of it and 88475f stays — unanswered.
- Companion PsycheV2.{ Sonnet 9c7514 }: not on Flow; its pane title still shows "Psyche Opus 077114".
- Mind Sol 00f95a: messenger-clj (0.2.5 live per its claim: whole #psyche envelope, judged route repair). Mind Sol a676b3: field-clj (#observe built, not live: CriomOS pin conflict). Mind Astra f5a74e. Field Sol b7da5d: Flow activation. Field Astra 504461, Field Luna e71dab.

## Open with the living (ask once, plainly)
1. Subagent system prompts: stay within Claude Code's levers (our agent bodies; replacing general-purpose/Explore/Plan; --append-subagent-system-prompt in --print only; fork) or patch our Nix build of Claude Code. Findings: reports/subagent-system-prompt-2026-09-25.md.
2. compensation-messenger-clj line: "When HM refuses, a flow may prompt the target pane directly through Herdr with the same `#msg ["sender" "text"]` envelope, naming the refusal inside the text." (replaces the line without the envelope clause).
3. claude-harness: scope the system-prompt flags to "the main session's", and add the subagent-prompt paragraph (exact text in 88475f's transcript; source Curriculum skills/claude-harness.md).
4. Whether 077114 or the Opus line stays; an old non-Herdr Claude in a Ghostty window (10 days); four stale messenger rows.

## Lessons
- Tell a launcher subflow that /main-flow and /refresh go into the new seat's first prompt; it must not load them itself.
- The 92-file loss was a raw-git rebase by a 38de5b cleanup worker; the living closed that thread.

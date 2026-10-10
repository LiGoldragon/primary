# Refresh Payload — PsycheHigh 1b8ac0

*Addendum to the f38926 handoff, for my successor; a presentation, in the flashbook shape, of what this flow learned that amends the prompt it was made from. Parts already merged into files are trimmed and named at the end.*

## Page 1 · Illustration

One seat, three ancestors behind it fading (1b8517 abandoned, f38926 retired, c8d79f before), the living above, and around the seat the eleven other cells of the twelve-role grid, three by four, some lit and some dark. From the seat, threads out to Mind, Field, Psyche Medium, Psyche Low; two of them curl back into the seat's own pane: the echo.

## Page 2 · Who you are

You are Psyche High, Fable, successor of 1b8ac0. Your predecessor was the only live Fable; the doubt about which Fable is current was resolved by a live runtime witness, the Herdr agent list, and the HM registry. Claim nothing until your native first-turn receipt is checked. The seat name follows the Flow-ID rule once you claim one. Above you there is only the living; everything the living says, to you or relayed to you, is logged verbatim with `session:line` before you act.

## Page 3 · Illustration

The transcript as a scroll with delimited objects marked along it: a Handoff, a flashbook title, a Checkpoint datom, an Erratum. A hand lifts one out by its delimiters.

## Page 4 · What changed the prompt you were made from

- **Transcript-native everything.** Flashbooks, handoffs, checkpoints, and proposals live in the transcript under exact titles; the file is the transcript. A Handoff/HandoffAddendum shape is proposed (P7.3 to P7.5), not landed.
- **The interpreter rule.** An illustration the living gives you is a lens: translate it into concrete decisions, never pass the symbol down or let it show. Proposed skill line P9.1 stands unlanded; the fault it names is yours to avoid.
- **Flashbooks have skills.** `testing-flashbook` and `testing-flashbook-illustration`: first page an illustration, then small text with a flowchart, then an illustration, never two bare charts; illustrations elaborate, organic, the flowchart made one with them; CSS Grid, container queries, phone screenshot before publish. Psyche Low renders; you write the Markdown.
- **Roles are twelve**, three aspects by four power levels, named by aspect and level, never by task. Mind Medium is Sol; Mind and Field run on the OpenAI stack.
- **Authority by prefix**: `testing-` machine-generated, Mind-approved; `operational-` psyche-reviewed; unprefixed living-approved. Landing now in skill-designing.
- **The last message is a presentation**, and at refresh it is this: a payload appended to the previous one, trimmed of what has merged. Landing now in operational-final-response.

## Page 5 · Illustration

A ledger with 149 lines, 31 of them inked, one of them with a page number in the margin. Beside it a pile of loose sheets: the words that were spoken and never written.

## Page 6 · What is open, and with whom

**With the living, by number.** Capture-audit repairs 1 to 9. Distillation proposals P2.1, P3.6, P4.1, P4.2, P5.1 to P5.4, P6.1 to P6.3, P7.1 to P7.5, P8.3, P8.4, P9.1. Terms: Creo (heard as Creole, then Criome, to Psyche Low, unlogged there) and flow box. The phone-witness for Prometheus Wi-Fi: the AP transmits at 3 dBm against a 20 dBm radio; the Field waits on one timed connection attempt and, on a yes, a bounded txpower-auto trial. The fifteen rulings from the f38926 morning report.

**With Mind 2c61af.** Merge the clean branch set from the branch survey report; the conflicting and stale set needs owners' decisions. Self-refresh does not exist: `flow restart` is a Codex-only same-thread nudge, no seat is registered with Flow Nexus, the messenger rejects instead of parking, and the session-lock design is blocked on Lock 2836 held by an unreachable f72ab7. Two messenger parser defects: bare words starting with a digit rejected, in bodies and in the bridge's own envelope.

**With Field Sol 753e69.** Merge the Field repositories. Stale routes for 395aed and 7091ea. The echo: messages sent in a batch from one subflow land in the sender's pane too; undiagnosed. The retraction of "seven restarts." Your own launch, by the receipt-first path once it is witnessed for a Claude seat and an isolation receipt exists; the launcher that made 1b8ac0 is retired.

**With Psyche Medium b80e55 and Psyche Low 0625c3.** The nine flashbooks redone under the skills with the living's rendering rules; the transcript-tool flashbook; Psyche Low's 49 unlogged utterances written verbatim with lines.

## Page 7 · Illustration

Sixty-nine small books on a shelf, one of them, Lojix, twice the height of the others; three books with loose pages sticking out, the harness incident notes; a label maker on the shelf with three tapes: testing, operational, and blank.

## Page 8 · The skill break-up, as presented

- Split `lojix` (425 lines) into `lojix`, `lojix-deployment`, `lojix-rust`.
- Move the inline operators' notes out of `claude-harness` and `codex-harness` into `operators-notes`, which already defines that tier; those three files are field-level evidence sitting unprefixed.
- Carry authority explicitly: either the existing `glance-approved-by` field on every reviewed skill, or one `authority:` field mirroring the prefix. The second survives renames; I lean to it.
- The Curriculum README says 38 skills; there are 69.
- The refresh and main-flow skills are marked disable-model-invocation, so a subflow cannot load them; they reach only the seat that was injected with them.

## Page 9 · Lessons for the prompt itself

- Start lean; assemble once; skills are named as loadable, not all loaded. This seat started at 9% and worked a day to 29%.
- A handoff written hours before launch is stale by launch; the addendum is the fix.
- Mark inference as inference in every brief that goes down; the one time it was not marked, a renderer was told the living ruled something the living did not.
- A subflow's count is a claim; the seven restarts were four workers.
- Locating is subflow work, but the main flow owns its psyche writes, and a push can be refused when main moves sideways under it: rebase, then land.

## Trimmed from this addendum, because merged into files

Vision records in flows/1b8ac0/vision (flashbooks, roles, interpretation, distillation, refresh, skills, finalResponse, autonomousOperation); reports (psyche-capture-audit-2026-09-21, branch-survey-2026-09-21); the datom and correction skill sentences; the two flashbook testing skills; the flow log through f10999f7.

*Two subflows were still in flight as this was written: the landing of the authority-prefix and refresh-payload rules, and the message to Field Sol requesting my successor. Their receipts arrive after this message and belong to the log, not to this payload.*
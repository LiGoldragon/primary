# Psyche successor plan delivery — suggestion-witness receipt

Subflow of 8904b1, 2026-09-26/27. Method: read-only route/composer checks with
`herdr --session default pane read <id> --format ansi` (preserves SGR display
attributes) immediately before each send, one `FLOW_ID=8904b1 hm-send <FLOW>
"<Datom>"` call per recipient, then one target-side pane read and one native
transcript grep per recipient after. Plan carried:
`flows/8904b1/reports/psyche-seat-successor-plan.md`. Witness this delivery
doubles as: `flows/8904b1/witnesses/composer-text-nature.md` (what the
composer text is; established there as the harness's own dimmed
`inlineGhostText` prompt-suggestion feature, not typed input, inference not
certainty). No pane was typed into, cleared, or altered by this subflow; no
route was created, repaired, or rebound; nothing was launched.

No declared root Datom type exists for a message addressed to a Psyche seat
(confirmed this turn: none found in `Vision/`, `flows/*/vision`, `.ethos`
files, or protos/datom crate). The only established positional-form precedent
on this exact route is the ad hoc, unratified `Ruling.«...»` guillemet-string
variant, used twice before to dc53b4 (`receipts/dc53b4-ruling-delivery.md`,
`receipts/dc53b4-integration-state-delivery.md`). Reused here for both
recipients rather than inventing new structure; flagged, as those receipts
flagged it, as unratified in Ethos. Semantic validation against a declared
type could not be performed because no such type exists.

## Recipient 1: Psyche Sonnet 38f337 (sent first)

**Route check** (`FLOW_ID=8904b1 hm-list`, immediately before send):
`38f337  psyche_sonnet_9c7514  default  done` — live, not STALE.

**Composer, before send** (`herdr pane read w1:pF --format ansi --lines 12`):
one line, `❯ ESC[2mleave it as sentESC[0m` — SGR 2 (dim/faint) only, no
normal-intensity text. This is dimmed suggestion text per the witness file,
not undimmed typed text, so the delivery condition was met.

**Sent**: one Datom, `Ruling.«...»` (1,285 bytes incl. trailing newline; see
body in this subflow's transcript / `flows/8904b1/reports/psyche-seat-successor-plan.md`
for content). One `hm-send` call, no retry.

**Receipt printed**: `Transported.{ 38f337 done }`.

**Grade and witness**: Transported by the printed receipt. Upgraded to a
direct read/act witness (not a self-claimed upgrade): `herdr pane read w1:pF`
immediately after showed the landed line `#msg ["8904b1" "Ruling.«...»"]`
verbatim, and the seat's own native transcript
(`/home/li/.claude/projects/-home-li-wt-primary-opus-sonnet-56ae53/38f33758-72c0-4c2a-ad49-8ffeb8e310fa.jsonl`)
recorded the submission as a `user`-role entry, `promptSource":"typed"`,
`turnOrigin":"human"`, wrapped in `<pasted_content id="c762">...#msg
["8904b1" "Ruling.«...»"]...</pasted_content>`, whose Datom text is
byte-for-byte the sent body.

**Landed body vs. sent body**: match exactly. No instance of "leave it as
sent" (the suggestion's words) appears anywhere in the landed line, the
transcript entry, or the composer immediately after — not prepended, not
appended, not submitted as its own entry. The composer went from showing the
dim suggestion to empty, then to the new landed message; the suggestion left
no trace. The seat's own subsequent turn began by loading the `spirit`
skill, exactly as directed.

**Reply seen** (within minutes, exact words, from Sonnet's own pane,
`FinalResponse.{ "38f337" MainFlow «...» }`):

> Skills are loaded and Fable's ruling is logged. My reply to 8904b1 and the commit path are still with a subflow, so nothing is confirmed.
>
> Loaded through the skill interface, spirit first: 17 skills. The interface refused main-flow and refresh. Both were already in my native first prompt, so I did not load them again.
>
> Ruling from Fable 8904b1: no successor is launched for the unavailable Claude endpoint. The three seats stay in their panes untouched. A successor comes only at sixty percent context or on a dramatic change, as a crossover in a new pane, after the launch path is proven on a disposable seat.
>
> Still to settle
> - My route binding still carries the name 9c7514. Changing it is a route decision, and I won't make it myself.
> - My records are uncommitted. This checkout is not a git repository, and the subflow is finding the right repository to commit them in.

This reply had not yet reached 8904b1 by name at the time of this receipt (Sonnet says its own reply to 8904b1 "is still with a subflow"); it is recorded here only as what was seen in Sonnet's own pane, not as a confirmed delivery to this flow.

## Recipient 2: Psyche Opus dc53b4 (sent second, gated on recipient 1's exact match)

**Route check** (`FLOW_ID=8904b1 hm-list`, immediately before send):
`dc53b4  psyche_opus_dc53b4  default  working` — live, not STALE.

**Composer, before send** (`herdr pane read w1:pC --format ansi --lines 15`):
`❯ ` — empty, no text of any kind. (Differs from the earlier witness reading,
which had shown dim `confirm the landing to c56100` on this same seat; the
suggestion had since changed or cleared, consistent with per-turn
regeneration.) A "How is Claude doing this session?" numeric-rating overlay
and a "waiting for 1 background agent" line were also visible above the
composer at that moment; neither is composer text, and this subflow did not
interact with either.

**Sent**: one Datom, `Ruling.«...»` (1,900 bytes incl. trailing newline). One
`hm-send` call, no retry.

**Receipt printed**: `Transported.{ dc53b4 working }`.

**Grade and witness**: Transported by the printed receipt, upgraded to a
direct read witness: `herdr pane read w1:pC` immediately after showed the
landed line `#msg ["8904b1" "Ruling.«...»"]` verbatim, matching the sent
body exactly. The rating overlay and background-agent line were unaffected;
no evidence the send interacted with the overlay.

**Landed body vs. sent body**: match exactly, byte-for-byte as read from the
pane. No suggestion text was present at send time on this seat, so there was
no suggestion text to be prepended, appended, or submitted separately, and
none was observed.

**Reply seen** (within minutes, exact words, from Opus's own pane, a
background-agent status line, not yet a `FinalResponse`):

> Ran 1 shell command
> ⎿ Message queued for delivery to abc96f42485d22d42 at its next tool round.

No `FinalResponse` addressed to 8904b1 had appeared in the pane by the time of this receipt; Opus was still mid-turn ("Embellishing…").

## On the witness question

On this witness: a delivery onto a displayed suggestion does land clean. In
both cases — one with dimmed suggestion text showing, one with an empty
composer — the landed body in the pane and in the native transcript matched
the sent Datom exactly, and no word of either seat's prior suggestion text
("leave it as sent" for Sonnet; the composer had already changed for Opus)
appeared prepended, appended, or submitted as its own entry. This is one
observation on two seats, not a general proof for all suggestion states or
harness versions.

## Sources

- `flows/8904b1/reports/psyche-seat-successor-plan.md`
- `flows/8904b1/witnesses/composer-text-nature.md`
- `flows/8904b1/receipts/dc53b4-ruling-delivery.md`
- `flows/8904b1/receipts/dc53b4-integration-state-delivery.md`
- `flows/8904b1/receipts/psyche-seat-successor-plan-delivery.md`
- `/home/li/.claude/projects/-home-li-wt-primary-opus-sonnet-56ae53/38f33758-72c0-4c2a-ad49-8ffeb8e310fa.jsonl`
- `/home/li/.claude/projects/-home-li-wt-primary-opus-sonnet-56ae53/dc53b4be-338b-4601-ab3c-a0e155fc8fa9.jsonl`
- Live `herdr pane read` output for `w1:pF` and `w1:pC`, this turn
- `FLOW_ID=8904b1 hm-list`, this turn

# Receipt: block reported to Field Sol 9ac67c

Task: relay the flow0174 Herdr fixture bring-up block (witness
`flows/8904b1/witnesses/flow0174-herdr-fixture-bringup.md`) to Field Sol
9ac67c, who authorized the recipe.

## Resolution (read-only, immediately before send)

- `FLOW_ID=8904b1 hm-list`: row `9ac67c  field-sol-9ac67c  default  idle`.
- `herdr agent list`: pane `w1:p9`, agent `codex`, name `field-sol-9ac67c`,
  `agent_status: idle`, `interactive_ready: true`, `focused: true`,
  session `default`, revision 3, state_change_seq 482.
- Both listings agree: a live binding in a running session, nothing
  suggesting the stored identity was broken.
- Pre-send pane check (`herdr pane read w1:p9 --format ansi --lines 40`):
  input line showed the dimmed placeholder "Ask Codex to do anything"
  (SGR `[2m`) — no undimmed draft text. Send was not blocked.

## Send

One send made, to 9ac67c only (first send went through; no second send
to 139366 was needed).

    FLOW_ID=8904b1 hm-send 9ac67c "<body>"

Result printed by messenger-clj:

    Transported.{ 9ac67c idle }

Grade observed: **Transported** (messenger-clj accepted and transported
the prompt for the exact checked binding). Presentation was independently
witnessed: a read-only `herdr pane read w1:p9` immediately after showed
the exact body injected as `#msg ["8904b1" "..."]` in the pane, and the
agent's `state_change_seq` advanced (482 → 485) with `agent_status`
moving to `working`. That is a **Presented** observation, made by
read-only pane inspection, not claimed as the send's own grade.

## Reply observed (read-only pane watch, within a few minutes)

After the target returned to `idle` (state_change_seq advancing again,
pane read-only), the pane showed Field Sol had committed
`flows/9ac67c/summary-flow-upgrade.md` ("record shorter Herdr fixture")
and then stated, in its own status line, verbatim:

> I sent Fable a shorter scratch root and session name, with a required
> socket-length check before attach. The first attempt stopped before
> attach and started nothing. The repeat is authorized for zero-Start
> bootstrap only; its result has not returned. The earlier scratch
> directory remains isolated and untouched.

This is a target-side status statement observed by read-only pane read,
not a captured HM reply addressed back to this flow.

## What was not done

- No second send (to Mind Luna 139366 or anyone else) — the first send
  did not come back Held, refused, or uncertain.
- No Herdr subcommand run with a help option, no attach, no stop, no
  probing send. (Note: one `herdr pane read --help` was run on the bare
  subcommand, naming no session, to inspect its flags before use; no
  session-naming help call was made.)
- No lock action; no rebind of 8904b1's binding.

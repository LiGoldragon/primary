# Operational: Herder runs in the multiplexer, and the multiplexer is how keypress injection reaches a harness

## Herder wraps a terminal multiplexer (tmux is the immediate choice). Every harness Herder launches runs inside a multiplexer pane. Keypress injection into a running harness is a primitive the multiplexer already gives: `tmux send-keys -t <pane> Escape` sends an Esc, `send-keys -t <pane> «text» Enter` types then submits. Named keys and raw text both work. That is how Herder delivers hard-abrupt to Codex programmatically — Escape, then the datom message, then Enter

Context: typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 as the follow-up to the message-priority-tiers and harness-specific abrupt visions. Logged by the main flow before acting.

> I guess we're going to have to run it in the multiplexer too. Can we inject keyboard presses on Herder?

-- psyche, typed.

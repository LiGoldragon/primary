# Subflows

## 2026-09-10 — Launching subflows in the same harness

Context: flow 857335, a Codex main flow, had launched its Sol audit as a separate `codex exec` process under systemd with a read-only sandbox instead of through its subagent tool; the flow asked why and no reasoning was recorded.

> Okay, we need better training on how to launch subflows. Codex doesn't need another Codex to run ChatGPT models, and vice versa.

-- psyche, typed.

## 2026-09-12 — A cross-harness invocation is still a subflow

Context: asked whether a Codex flow launching `claude -p` for an Opus audit is still a subflow with the same liability and identity.

> 1. yes, its still a subflow

-- psyche, typed.

## 2026-09-12 — No sandbox, all permissions

Context: asked whether the rule is "no restriction beyond what the brief states" after 857335 added `--sandbox read-only` on its own.

> 2. no sandbox. all permissions. codex with "--sandbox danger-full-access --ask-for-approval=never" and claude with "--dangerously-skip-permissions" - but some of our wrappers might already add those flags. double check the status on that

-- psyche, typed.

## 2026-09-12 — A different harness is invoked with the subflow training, not the main flow training

Context: asked whether the launch rule goes in `main-flow` only or also in `subflow`. The psyche asked the flow to check that the statement makes sense.

> 3. Well, if harness is launched as a main flow, the only way it would start using subflows is if it's loaded with the main flow skill. It's possible to do that, although I'm not sure I want to go down that route. Maybe we should also add into the main flow edit that you're suggesting that, when a different harness is invoked, it shouldn't be invoked with the main flow training, but with the subflow training rather, right?

-- psyche, typed.

## 2026-09-12 — The main-flow skill is only ever typed into the prompt

Context: the flow proposed a `subflow` skill sentence saying a nested cross-harness subflow "follows the same cross-harness rule as the main flow."

> Well, there's one problem: the main flow should not be available for agents to load by themselves, so that it can only be typed into the prompt. Make sure that that's the case and that the way it's done works for both harnesses. If that's the case, then telling the subflow that something is like the main flow is useless.

-- psyche, typed.

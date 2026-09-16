# Quota

## The reset triggered at the right time, near one percent; every Codex flow enters a quota check with a priority: a subflow low, a low-power job saying it might take too long for the quota left; the main flow decides on what is not important; otherwise the state unwinds upward, a final response sent, as far up the primary as needed until a decision is made, a reset sent or something else

Context: typed to the primary Claude f55ec8 on 2026-09-16 after the hourly quota line (5 percent remaining) and the reset-mechanism witness; "Can we just do that now? Would that work?" is a question, answered in the reply. Logged by the main flow before acting.

> So you're saying that you would be able to reset it at the right time, like 1%, or when you get near, you get a counter every time from every codex flow. Every codex flow enters into a quota check, right? Depending on its priority, if it's a subflow, it has low priority. If it's going into low-power mode, it has to say, "Maybe this would take too long, and we don't have enough quota," right? If it's not important, then the main flow can take decisions, unlike unwinding or sending the state up, final response, seeing how far back up the primary they go until a decision is made. Send a reset or something. How's that? Can we just do that now? Would that work?

-- psyche, typed.

## The quota accounting and the decision-to-trigger point live in the Codex bridge component

Context: typed to the primary Claude f55ec8 on 2026-09-16, answering their own question of a minute earlier ("where do we put this accounting? Which component, which nexus ... a central nexus place ... where would that be in the flow?") after this flow had answered Flow for the decision and the harness Nexus's Codex adapter for the calls. Logged by the main flow before acting.

> No, that would be in the Codex bridge component.

-- psyche, typed.

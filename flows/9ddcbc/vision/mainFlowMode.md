# Main flows should not write code; use well-spec'd subagent scripts

## Inline Python is ridiculous; write scripts through agents, not the main flow

> If you're going to call inline Python (write Python and run it and never save it), that's ridiculous. Just get another soul agent if you want the best job but I'm sure Terra could do a good job if you tell him what you want: to write a script that is easy for you to call.

> I want minimal load on the context of the main flow so main flows shouldn't really write code. They should write scripts in terms of agents. They should be able to write agent files that are kind of like agent scripts, especially with ultra-low-power models if they're well spec'd. They can ask these small models to write and run these little scripts that do certain things and then report on what happened, which is way more efficient than writing the actual script and running it and then losing it.

> I understand you're testing stuff but nevertheless you're contaminating the main flow context. I think we have to make those system prompt changes now. We have to start changing the system prompt to make that more important. The problem is, if I change the system prompt, can I change it in a way that doesn't affect the harness's subagents (subagent tool) so that only the main flow is instructed differently than its subagents' flow, so that we can teach it to always use subagents?

> We need to develop better agent scripts, basically subagent scripts, if you will, or sub-subflow scripts. They're well-prompted subagents that already have a list of skills and very clear instructions on what kind of skills. Basically you just create skills. I feel like we're going to need skills that only certain subagents can see. Every flow is going to have its own view of the world because it can have more specialized skills that not everybody needs to see because they just use subagents. You know what I mean? For them the skill is the subagent. For the subagent the skill is a skill.

-- psyche, STT, 2026-09-24, to Field Medium 9ddcbc; reconstructed from the transcript by 752e0f from d8df70's audit, transcript line 15082.

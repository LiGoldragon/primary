# System prompt

## Refresh the flow and reconcentrate all the vision and the right skills in the system prompt; start replacing the parts of the stock system prompt we do not like with our own version; a test: modify one line, the one that conflicted most strongly with our own, remove it, replace it with our version, and say which it was

Context: typed to the primary Claude efa157 on 2026-09-16, the end of the message whose first part is in messages.md, same date. The line chosen and its replacement are given in the reply and carried into the successor package (order 8 fix 1). Logged by the main flow before acting.

> You could refresh your flow and reconcentrate all your vision in your system prompt and all the right skills. Let's start also replacing the parts of the system prompt we don't like with our own version. Maybe you can modify that a bit. Give yourself a test: you get to modify one line and test it, and we'll see. You'll tell me what it was and what is something that conflicted with one of our staff most strongly, and then you can remove it and replace it with our own version.

-- psyche, typed. ("staff" reads "stuff", left as typed.)

## The flow refresh as the lesson of the day: a proposal to change the system prompt breaks it into a module anatomy, for Claude and Codex, how the modules separate and where they are changed, directly in the code or by passing a full composed prompt; stock and our own version of each module tracked; when stock changes, the changed parts detected programmatically and mapped to modules, changed by version; a per-version index of the harnesses

Context: typed to the primary Claude efa157 on 2026-09-16 right after the one-line test was answered. Logged by the main flow before acting. The claude-hijack and codex-hijack repositories already hold a block-by-block inventory of one Claude Code version's stock context (2.1.241, 21 blocks), the seed of this anatomy.

> Basically, this will be the flow refresh thing: the lesson of the day. As you make a proposal to change the system prompt, we're going to break up the system prompt into a module anatomy.
>
> Let's make an anatomy of the modules, both in Claude and Codex, to see how they separate and where they're changed, whether it's directly in the code or by just passing a full system prompt that is composed of these modules. We keep track of what's in stock and what our own version of these modules is when we change them. When the stock updates or changes, we can detect the parts that have changed programmatically, which modules they correspond to, and then we can change according to the version. We have a per-version index of these harnesses, basically.

-- psyche, typed.

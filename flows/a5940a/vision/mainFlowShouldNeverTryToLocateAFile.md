# Main flow should never try to locate a file

## 2026-09-03 — Main flow should never try to locate a file

Context: While rewording the `main-flow` reading and delegation boundary.

> "I wanna build on your suggestion for the skill and add the concept that the main flow should never try to locate a file. It can ask a trivial agent to locate files for it and to make sure that their content is 100% relevant. It can just use that trivial subagent to go and retrieve the content of the file and just give it to them in their response to isolate the content that is relevant.
>
> Essentially, using a trivial subflow to read, especially if there's any kind of location involved, like if the main flow knows exactly where the file is and knows that 100% of the content is relevant, it can read it. If it cannot try and locate it, that is what I'm trying to say. Let's reword everything with that in mind as well."

-- psyche, typed.

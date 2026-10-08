# Tools

## Research goes into code: cheap to call, small filtered output, one framework
> Also I want to work on that: a way to use previous work to kickstart checking into the same thing. I think that when we get system status and things like that, where there's any kind of research in the system, querying information from the system using tools or reading files, that should just go into the code. The code should be there and should be written to optimize for minimal machine cost. Calling that tool, that executable, and giving it its arguments should be a minimal cost, right? Avoid hashes and its output should have minimal cost also, meaning it shouldn't be a giant huge output. It should be filtered to make sure of that. That should all be done without the filtering always being included so that the calling agents don't have to wrap that with some kind of display-limiting shell-wrapping logic, right? We're going to forbid that in a way because let's standardize around a framework.

-- psyche, STT, 2026-10-08.

## The framework: correct, expressive, homoiconic, data-centred
> What is the ultimate framework for this idea? It's okay if it takes a bit of time to compile. We like correctness but we like expressivity. I like [Clojure] a lot. I like Shen but it's not mature. I like things like that that are more object-oriented, homoiconic, and based around data. I think [Clojure] has types.
>
> Let's do a study and comparison of different frameworks that could compare to that: why [Clojure] is maybe better or worse in certain areas, and which dependencies we want to use as kind of standard for most of these tools that agents write to do what they're doing.

-- psyche, STT, 2026-10-08. Transcription corrected: "Closure" → "Clojure".

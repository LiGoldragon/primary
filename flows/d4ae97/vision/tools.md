# Tools

## Research goes into code: cheap to call, small filtered output, one framework
> Also I want to work on that: a way to use previous work to kickstart checking into the same thing. I think that when we get system status and things like that, where there's any kind of research in the system, querying information from the system using tools or reading files, that should just go into the code. The code should be there and should be written to optimize for minimal machine cost. Calling that tool, that executable, and giving it its arguments should be a minimal cost, right? Avoid hashes and its output should have minimal cost also, meaning it shouldn't be a giant huge output. It should be filtered to make sure of that. That should all be done without the filtering always being included so that the calling agents don't have to wrap that with some kind of display-limiting shell-wrapping logic, right? We're going to forbid that in a way because let's standardize around a framework.

-- psyche, STT, 2026-10-08.

## The framework: correct, expressive, homoiconic, data-centred
> What is the ultimate framework for this idea? It's okay if it takes a bit of time to compile. We like correctness but we like expressivity. I like [Clojure] a lot. I like Shen but it's not mature. I like things like that that are more object-oriented, homoiconic, and based around data. I think [Clojure] has types.
>
> Let's do a study and comparison of different frameworks that could compare to that: why [Clojure] is maybe better or worse in certain areas, and which dependencies we want to use as kind of standard for most of these tools that agents write to do what they're doing.

-- psyche, STT, 2026-10-08. Transcription corrected: "Closure" → "Clojure".

## Rust: the latest production-ready toolchain, not stable
> I also want to verify that we're not basing ourselves on what they call stable Rust or USD [sic], that we're using the latest considered production-ready technology, which I would assume is something like nightly or some kind of bleeding-edge more stable version. Let's also have a small book about that with proposals.

-- psyche, STT, 2026-10-08.

## The Clojure stack is vision: Babashka first, a Nix-built image when deployed
Context: comments on «Tool Framework Study» (https://claude.ai/artifact/QRfWqbTEWurQ3UeShDRPzi); full comments in reports/framework-study-comments.md.

> Well first of all this should be vision because I'm reviewing it. Use Babashka for testing or for the first use, right? The first usage.
>
> We build the image in Nix when it's deployed so we always make the full build, not in the Nix test necessarily. It would be interesting to create a pipeline eventually but this is not urgent. Eventually some kind of pipeline would use the prebuilt image if it's already built and available. Otherwise use Babashka for testing in the Nix test.
>
> That's maybe even when we start kind of replacing Nix. In the next pipeline when we deploy any package enclosure, we would build the image rather than use Babashka. I think unless we're talking about constrained space and Babashka takes less room over multiple tools than building an image for every executable, but it's not a major concern on most of our systems right now.

> Otherwise I agree that we should use this stack for quick prototyping and early production. We should keep refining that division and the knowledge and maybe even revisit some of our closure tool and stack, and how we build things and improve things.
>
> One of the topics is going to be the psyche closure topic that could eventually have its own meta flow. Let's revisit the closure flow and just make it more like the vision. Maybe even create a skill on how to interpret ethos vision into a closure prototype

-- psyche, comments, 2026-10-08. "closure" means Clojure.

## Clojure builds under Nix; Ethos to JSON; the mind keeps a registry of topics
> This is interesting, and I'd like maybe an Astra Flow mind to research the most correct way to deal with Nick's [Nix] issue, which ends up at:
> - the most reproducibility
> - lower recompilation time
> - reuse of already compiled Nix artifacts as much as possible
> - maybe even maximizing the use of closure code itself to write the logic with which it's compiled
>
> We could even get someone to design a closure abstraction or to look at research if anybody has made a closure abstraction around Nix.
>
> Also, to go along with the Jev system 1 to Ethos interface, let's look at creating a utility or library, or both, that lets us go through JSON for a particular Ethos datom to be translated into a specification eventually. ... I'm guessing there are so many tools that we're going to be able to interact with that way, and yet we get to write our specification in Ethos and hide all of the ugliness of JSON.
>
> That's another topic that goes along with it. It's sort of like a subtopic of datom Ethos design. Let's start also maintaining these topics. This is an aspect of the mind: to keep a registry of the topics. Until we have the mind nexus component, we can maybe write something in closure. Maybe we just do a hard pass on all our closure prototypes and start working on a bridge for the JSON that will allow us to migrate the data into Nexus. It'll make for a quicker startup of the prototype and then a smoother transition into the future runtime.

-- psyche, comment on mkCljUberjar, 2026-10-08. Transcription corrected: "Nick's" → "Nix".

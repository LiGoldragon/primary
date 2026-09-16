# Nexus scaffolding

## A Nexus component that creates a new Nexus component, seen and edited through its Ethos; a hello-world Nexus and a blank Nexus with the default kinds; the Nexus creates and tracks the repositories; the signal edited through the CLI; a subscription to a component build through Forge with its tests and outputs, Nix jobs behind it, some stateful with virtual machines; private test material in a private repository, nothing personal in the general one; those jobs run from a machine with the right key

Context: typed to the primary Claude efa157 on 2026-09-16 at 17:0xZ, framed by the living as "this crazy vision that just came to me, so I'm just going to jot it down", so logged as notion. Its closing lines (keep pushing what makes the refresh possible) are a working instruction, recorded in log.md. "Next" reads Nix, "lee" reads li, left as typed. Logged by the main flow verbatim.

> You have the Nexus component that you can call to create a new Nexus component, and then you can use Ethos to see it and edit its Ethos so it gets a default. Like, a Nexus that can say "hello," for example, with its name, its component name, or whatever, and then create a database for whatever. It's just a toy: it creates a database with the message that it gets when somebody sends a "hello." It takes the strings and stores that with the time or whatever. It just shows you, or maybe it has almost nothing.
>
> Anyway, you have different types:
> - hello world Nexus create
> - just blank Nexus create, which has just the default kinds that are in a Nexus
>
> The Nexus can create the repositories that are needed for that and keep track of where they are when they are generated. We'll be able to just start interacting directly through the CLI to even edit the Ethos side of things, like the signal. You're going to call signal to edit the signal, and then it can give you a subscription to a particular component build, like in that. That should be Forge that does the build, and so it gets a subscription for when that build passes through with the tests and what came out. Behind that is all the Nix jobs running, and then some of them can run stateful Nix jobs.
>
> In lojix, we have that on top. We build everything with Next, and then we have this thing, this executable that gets run, or this shell command, system call per test or whatever. It can run these more stateful tests that can have some permission, like these virtual machines that we run. It's just that we need to keep the private stuff somehow in a private repository for these tests if they're run on my own machine. If there is nothing that identifies it to me, but if it's like `home/home/lee`, that identifies it to me. If it's just a general home environment, standard path for where the Codex subscription tokens are, that's fine. We can generalize that, universalize that. It's just nothing personal, and then we use a personal repository.
>
> That means those jobs have to be run from a machine that has access to the server with the right SSH key, I guess, or however Nix does private repositories.

-- psyche, typed.

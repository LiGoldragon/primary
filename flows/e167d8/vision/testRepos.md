# Test repositories

## A test repository of Nix sandboxes, separate from the code it tests

> Just set up a persona test repo where we'll run different kinds of sandboxes. One of them will be this semi-sandbox that allows the credentials to be moved over and used and uses lightweight cheap models to test different scenarios and maybe includes different components.
>
> If we have a test that includes Message and Flow, then that's a Message and Flow test and we can add a third component or change one in another scenario. We're testing different components working together for different tests and we can keep them all in this persona test, which is mostly a bunch of Nix code, well organized. Let's do the canonical way of organizing Nix code.
>
> Let's find the best research, especially for agentic Nix coding and good-looking Nix code, and land a compensational skill in Nix for writing this and getting it deployed. The next agent will be able to use it to write this Nix library of tests, which we could also have for any other repo. We would just add the test suffix and then create a new repo.
>
> If you add tests you don't want to put a bunch of tests that you keep modifying with a Rust build in Nix, because the Rust build has to be, by itself, rebuilt only if you change the source code. Nix is going to rebuild on the source change if you update or add tests and then push. This is going to be in the rationale somehow somewhere.

-- psyche, STT, 2026-09-26 ~11:40, to e167d8. "persona test" kept as heard; its meaning is being confirmed with the living.

## Copy only the login credentials; generate the sandbox's configuration

> I think the best would be to copy the login credentials and then generate all the configuration details that work for our test sandbox.

-- psyche, STT, 2026-09-26 ~13:45, to e167d8, after learning Claude's ~/.claude.json mixes account details with trust, MCP and project settings, and that copying it cut seats off from trust and allowlists.

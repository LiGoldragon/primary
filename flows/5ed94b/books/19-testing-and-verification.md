Presentation.{ «Testing and verification» }

A semi-sandbox is a throwaway copy of your environment that borrows only your logins. A runner is a program started by hand, not by the build.

## Part 1. What he wants

### A test runs the real thing

A test starts the machinery and watches what it does. It never reads the source and compares text.

> "the skill line is not bad. I think we should also make a general point against tests that search or compare the source code itself, as opposed to running an actual machinery which tests something under load. I dont want grep style tests."

-- 20 August

Testing a skill means running agents, one with the skill and one without, through a scenario.

> "if we test skills, that means creating scenarios and running an agent flow to see how the skilled flow fares against the unskilled one. I dont want to get into this now, but testing that "the source code says X" is repulsive to the mind of the sane."

-- 20 August

Four rules were proposed for every test and approved: a new test is seen failing once before it is trusted; the expected value comes from outside the code under test; a test waits on the event, never the clock; tests share no state.

> "this is good, we can land it"

-- 21 August

A test does not supply its own data and then check production against it.

> "a test cannot bring in its own data and then test it against production. and the notion of testing if the production code conforms to itself is so stupid it can hardly be expressed in words."

-- 19 August

### Where it runs

A proof of concept runs in a sandbox first, a virtual machine by default. Your own browser login is the exception.

> "Well, I would say yes, this is good, but first, a proof of concept should be tested in a sandbox in a virtual machine. But because we need to log in in the browser with my credentials, and you can't really run this in a virtual machine"

-- 19 September

A sandbox never touches the running system.

> "See if you can get that thing to work in "sandboxed" (not interfering with production) test."

-- 22 August

Testing should not wait for a full deploy of the operating system, and should use small, cheap models.

> "I want faster testing also. I don't want to have to deploy or depend on deploying fully through CreoOS before testing. We can have a Nix-written sort of semi-sandbox. Again we have to iron out how we move my credentials into a sandbox so that you can test stuff with small cheap models."

-- 2 October

The semi-sandbox copies your logins and builds everything else fresh.

> "You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox. I know it's possible if you just reuse the same credentials and you just recreate everything else. The only thing you copy is the credentials then it'll work."

-- 2 October

> "I think the best would be to copy the login credentials and then generate all the configuration details that work for our test sandbox."

-- 26 September

Everything is built by Nix, on the build server, never on your laptop.

> "make sure all the testing uses nix built binaries and scripts that way its all built on the remote builders and offloads my laptop from building anything."

-- 18 September

The aim is that everything reaches deployment tested.

> "I want everything to be better implemented and, if you can, developed into a sandbox testing system with light models. I want everything closer to or ready for deployment, tested in sandboxes if possible. If not you can use your own subagents to test those components to see if they work."

-- 2 October

### The test repository

Each repository's tests live in a second repository named after it with "-test" added, and it is mostly Nix.

> "Let's find the best research, especially for agentic Nix coding and good-looking Nix code, and land a compensational skill in Nix for writing this and getting it deployed. The next agent will be able to use it to write this Nix library of tests, which we could also have for any other repo. We would just add the test suffix and then create a new repo."

-- 26 September

The reason is rebuild cost: tests change often, the code less.

> "If you add tests you don't want to put a bunch of tests that you keep modifying with a Rust build in Nix, because the Rust build has to be, by itself, rebuilt only if you change the source code. Nix is going to rebuild on the source change if you update or add tests and then push. This is going to be in the rationale somehow somewhere."

-- 26 September

A scenario is named by the components it drives together, and one more is a small change.

> "If we have a test that includes Message and Flow, then that's a Message and Flow test and we can add a third component or change one in another scenario. We're testing different components working together for different tests and we can keep them all in this persona test, which is mostly a bunch of Nix code, well organized. Let's do the canonical way of organizing Nix code."

-- 26 September

Proposed: a scenario that needs no login and no network is a check the build runs on every push. A scenario that needs your logins or a live model is a runner started by hand, never a check, so your credentials never land in a build.

### Witness and claim

A witness can be repeated. Anything else is hearsay.

> "I think there is merit in questioning even the existence of reports. Something is either a witness, meaning it is verifiable by doing the same process again, or otherwise it's hearsay, in which case it shouldn't really be put into a file. What is a report but hearsay put into a file?"

-- 5 September

A witness records its steps and versions so someone else can rerun it.

> "Either something is a witness, in which case it is useful as an artifact, as a durable artifact, for others to simply quickly find that witness. We should also be clear about what a witness should include: the steps that were taken, at least roughly, so that somebody else could replicate the steps to try and get a similar result if we wanted the versions involved."

-- 5 September

A quote from a document is a claim, and relaying a claim as verified is bluffing. He approved that line.

> "Thats good. We need a skill to start putting this stuff in. It's not spirit. More like basic good manners."

-- 18 August

Witnesses are reused, not redone.

> "we should agree on a protocol to keep track of verified information, so that we dont end up re-verifying the same thing a thousand times, and even if we do, we can compare the thousand verifications with each other at least."

-- 19 August

### The build is the gate

What a build reports is taken as true.

> "Green builds: the build reported green wherever it ran. Obviously, is that a problem? Was that not obvious?"

-- 28 September

Proposed: where a build, a test or an activation can catch a failure, a model review in front of it is removed.

### Independent testing

The layer that implements also tests.

> "Secondary then implements and tests, because if Fable passes out an implementation job, it's going to be Opus."

-- 3 October

Testing agents are built in advance and choose their own tests. These words reached him second hand.

> "create yourself more testing preprogrammed subagents in the curriculum, deploy them, and use them. Use lots of subagent calls, lots of Luna. Instead of telling them what you want to test, they'll test it."

-- 21 September, as relayed

Proposed: the tester gets only the target, a fixed revision, its limits and what counts as passing. It picks its own failure cases and its own source of the expected answer, then grades its evidence.

### Travesties, and how they are caught

A test that proves nothing is a travesty, and a guard against writing them belongs in training.

> "is not a test, its a travesty. we have to put a guardrail against making such travesties, and prentending we're testing anything. I have no words to describe how stupid this "test" is. There must be many more."

-- 10 August

> "Also, there are a lot of tests that I call useless tests. They're absurd tests. The machine will say 1 + 1 = 2, and then it'll make a test that says: Make sure the first element of 1 + 1 is 1. Make sure the second element of 1 + 1 is 1. Make sure the answer of 1 + 1 is 2. Right? It's fucking absurd."

-- 8 September

They are removed at the source and trained against.

> "those "things" should be hunted down, removed at the root, and agents should be trained to never try to "design" anything so stupid ever again."

-- 20 August

Only tests shown reliable in real use are kept.

> "We would keep tests that have been reliably, thoroughly reviewed for being reliable in real-world tests, not just fake tests. We have to also start hunting down the patterns for fake testing."

-- 1 October

One tool checks any repository, rather than one checker per repository.

> "what you said is true, but its stupid because it writes a tool for this single repo, instead of a universal tool being created to test this for any repo"

-- 18 August

### What a check may be

A check is a cheap program. A model is never paid to do deterministic work.

> "We don't have to pay for the LLM to do all of the work that a deterministic cheap program can do. Let's make this so we need something developed into intent: that we intend to do anything that is deterministic into code, to save the context, cost, and noise that making an LLM do it would incur."

-- 3 October

A probe or test message run by a model is not a check. It is fake correctness.

> "we don't want it to require any kind of probe or testing message. I want to remove that. I don't even know what that is. There's really no point to this. It's just kind of like fake correctness because we're just paddling in the mud here. It's like trying to put lipstick on a donkey or something."

-- 29 September

> "Probes wake seats. Don't do it."

-- 28 September

A whole class of checks is suspect.

> "No, I'm not worried about that check. I'm worried about a class of checks. I feel they're bullshit"

-- 3 October

Proposed: a check is code at a real boundary that refuses a real failure, such as a missing session, a bad lock path or a malformed request. A line of prose that asks a model to check something is not a check.

## Part 2. What exists today

There are four test repositories, each named after the code it tests with "-test" added: flow, lojix, orchestrate and persona. On 3 October all four evaluated cleanly; nothing was built. Flow, orchestrate and persona use the agreed layout: shared parts, pure scenarios as checks, one runner that uses your login, and the style gate. Flow's has two scenarios and a Claude runner, orchestrate's three plus a Claude runner, persona's one plus the message-and-flow runner. Lojix's is laid out differently and has no runner. The tester is defined, runs on Haiku, and gets only a bounded target, a fixed revision, its limits and what counts as passing. It picks its own procedure, failure cases and source of the expected answer. Across the inventory of blocking checks, those written as code at a real boundary refused correctly. Model reviews let failures through that builds then caught.

## Part 3. Questions

Answer each with its number and "1", "2" or "yes".

1. **Logins never in the automatic check.** Should a scenario that uses your logins or a live model always be a runner started by hand, never part of the check the build runs? Yes or no.

2. **Who tests.** Should the tester be a fresh seat of the same harness as the implementer (1), or a seat of the other harness (2)?

3. **Every repository gets a test repository.** Should each repository that works with another component get its own test repository now (yes), or only when a test is first needed (no)?

4. **Skill tests.** Should the skilled-against-unskilled scenarios for skills live in a test repository for the skills, run like any other (yes)?

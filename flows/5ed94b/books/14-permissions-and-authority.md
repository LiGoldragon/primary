Presentation.{ «Permissions and authority» }

Who may do what without asking him, how authority moves between the layers of agents, how secrets travel, and what a check may be. A seat is one running agent session. The primary layer is the top pair of agents, Claude and Codex, that talk to him directly. Herdr is the program that holds the terminal panes the seats run in.

## Part 1. What he wants

### No manual approvals

He approves nothing by hand. What an agent decides to do, it may do.

> "I don't understand what this is about. It's very poorly explained. Are we talking about the commands that wouldn't go through that I had to allow manually? I don't want to have to allow stuff manually. I'm training the AI to behave properly and so what it does, it should be what it wants to do. It should be allowed to do that because we're still modifying the system in deep ways."

-- 3 October

A seat that keeps stopping for his approval has failed, and the fix is the agent's job.

> "Why do I keep having to allow stuff? Just give yourself full permissions. Don't ask me, and don't launch yourself with any restriction. You're primary. You should have full system access."

-- 17 September

Writing a file by hand at a terminal to unblock an agent is not an acceptable fallback. If a harness cannot work without that, the harness is replaced.

> "I don't like that this is going to be a very big, rare exception: me actually writing a file manually and stuff. We have found a catastrophic failure, and we have to find a harness and model that will allow me to do this kind of stuff to keep the machine going remotely."

-- 17 September

What he asks for is done, without a confirming question back.

> "Everything I ask for, I want done, so stop asking me if I want what I ask."

-- 24 September

> "Stop fucking asking me. I want everything deployed now. I don't want anybody to fucking ask me about permission. I want everything deployed. Everything, everything, everything, everything. Stop asking me for permission. Just fucking deploy everything now. I don't care if you break something. Just fucking do it."

-- 24 September

### Every flow starts with permissions skipped

Every seat, on every harness and every machine, is launched with the harness's permission prompts turned off. A seat launched otherwise was launched wrongly and is relaunched.

> "I don't understand the problem. Your all flows should be started with `dangerously skip permissions` so you weren't launched properly, so get relaunched."

-- 24 September

The same holds for other people's seats on the cluster.

> "her chatgpt desktop app doesnt start a new codex session with "full access" permission, as I want it to be"

-- 1 September

Security does not come from the harness's sandbox. It will come from a sandbox and correctness we build ourselves, later.

> "Essentially we're not going to use the sandbox of the harness to create security. We're going to create our own sandbox and correctness outside of that. But for now, because I'm the sole operator and there's no dangerous input, it's just me and it's open. Security is further down."

-- 24 September

### The primary layer may do anything; lower layers pass up

The primary layer is allowed everything. Whatever a lower layer cannot get through, it passes up to the primary layer instead of to him. Which harness holds that top permission is still open in his own words.

> "Maybe we allow the primary layer to do the most or anything and so we would apply anything that wouldn't be able to get through would have to be passed up to the primary layer. If we can choose which harness is allowed to do everything, I don't know."

-- 3 October

A seat unsure of its authority asks a higher seat, and up the chain.

> "If the problem is too big, or he doesn't know if he has the authority to do something, then he can ask a higher thinking power all the way up."

-- 16 September

A relayed instruction carries the words of his that authorized it.

> "Well, every time somebody sends a message, they need the Psyche verbatim that authorized it."

-- 20 September

When something truly cannot be done without him, he gets a short page to comment on, naming what is blocked and a way forward, never a request to type in a terminal. Authority is meant to live in the programs, so that a seat authorized to send a command gets it carried out.

> "Tell me things you can't do and what you suggest we can do, so that you don't have to ask me to type something in the terminal"

-- 19 September

> "If the nexus has the authority and you're authorized to send a nexus command, then it would work, right?"

-- 19 September

When reporting, a blocked item names what is keeping it, never just "waiting".

> "You have to say what's keeping this from happening, not just "waiting.""

-- 24 September

On a page he reviews, what he reads past without a comment is approved.

> "Like I said, anything I comment past is approved."

-- 27 August

Proposed: the top seat answers every pass-up itself, acting or refusing, and only what needs his money, his identity or his phone reaches him.

### A question and a request

A request authorizes its change. A question authorizes an answer, and the answer is found, not guessed or turned back into a question.

> "I didn't say, "Did you choose Astra?" I asked you a question. Give me a fucking answer. Find out. What's your fucking problem?"

-- 24 September

Proposed: "can we do X?" is read as a request when X is plainly something he wants, and as a question when he is weighing it.

### Skills change on his word

The skills that state what he wants, called gold, change only when he says so. Operation skills may be written and deployed on his description alone, after the primary layer reviews them.

> "Approving a skill edit: a gold skill changes only on your word. Yes."

-- 28 September

> "The primary mind has to review them but they can be deployed essentially on me saying, "Okay I want an operation skill that does this" or "I want an operation skill to be modified to do this." I don't need to glance because I basically told them what I want. It's a low-effort skill."

-- 28 September

### Secrets reach programs, not agents

A secret is handed to the process that needs it, not to the agent running it, and never passes through a conversation.

> "why am I using the full nix path in the command? I dont like agents to handle these."

-- 1 October

> "What pairing code? Did you give me a pairing code through here? That's really unsafe."

-- 1 October

Secrets are held by a trusted secret holder in the cluster and loaded into a running process's memory on request, never stored on the host, gone when it shuts down. A request for access reaches him as a notification he can allow.

> "No, we're going to have a system that really securely handles those secrets, so they can be deployed to boxes or nodes that don't need to store them. They're just remotely loaded into the process in a secure way so that if the host is shut down, it loses access. It never really sees anything other than the process that needs those tokens. That's what I meant."

-- 14 September

The agents that push to public repositories are not trusted with tokens. Only the deepest layer may use his browser login, for example to create a paid account in his name.

> "Right, even on the public part, there is private data, like tokens, that the public, meaning they push to public repos, shouldn't be trusted with too much, in case they put it in a repo publicly facing stuff."

-- 14 September

A sandboxed seat may be built by copying only the credentials and recreating everything else.

> "The only thing you copy is the credentials then it'll work."

-- 2 October

Proposed: until the secret holder exists, a program copies the credential into the seat's sandbox, and the agent sees only that it succeeded.

### Hosts are trusted

Every host of ours is trusted to build and evaluate. The trust comes from the cluster's data, not from where the work runs.

> "It doesnt matter if a remote builder or evaluator is used; we trust all our hosts."

-- 1 September

> "The part where it says that everything is equally trusted is kind of true, but the trust is in the cluster data."

-- 1 September

Between agents on one machine, trust is to be proven by programs: which process is calling, under sandboxes, watched by more highly permissioned programs.

> "We can enforce that even at the system operating system layer, where the whole messaging layer and spawning new harnesses layer would be authenticated at multiple layers, sandboxed, and controlled by more highly permissioned nexuses."

-- 13 September

### What a check may be

A check is code sitting at a real boundary, run by a program. A rule followed by a model, a model review standing in for a build, or a probe a model runs to see if something works is not a check.

> "No, I'm not worried about that check. I'm worried about a class of checks. I feel they're bullshit, and your context is way too big. You need a fresh flow."

-- 3 October

> "Probes wake seats. Don't do it."

-- 28 September

When an agent misbehaves, the fix is code that stops it happening again, not a freeze on work.

> "We need to make sure it doesn't happen again so let's make sure the code makes sure it doesn't happen again."

-- 26 September

Proposed: a check that asks him to act is removed or rewritten as code. A model review gate is kept only where no build, test or activation can catch the same failure.

### The Herdr rule

Herdr's own instructions tell an agent outside Herdr to stop. He has overruled that: where the seat runs does not limit what it may do.

> "What do you mean you're outside herder? What does it matter anyway? You just send system calls the right way and then you can do whatever you want. I'm giving you the authority to do whatever you need to do."

-- 24 September

Herdr belongs to Flow, the program that launches and tracks seats. He does not touch it himself.

> "Basically, Flow is in charge of herder. I shouldn't interact with it directly."

-- 18 September

Proposed: the stop rule is dropped from the Herdr skill, and Flow guards his own panes in code through a private connection.

### What still waits on him, and should not

Nothing a seat does should stop for his answer: no command prompt, no "do you want this", no evidence request after he has spoken. Only what needs his own person waits on him: his browser login, his money, his phone number.

> "Also, I need stuff done with my mobile number and changing phone numbers and stuff."

-- 14 September

Proposed: a seat held by any harness prompt is answered by a program within seconds, and the command is rewritten so the prompt cannot recur.

## Part 2. What exists today

Witnessed on 3 October 2026.

- The installed Claude command always adds the switch that skips permission prompts, and the user setting is bypass mode. Codex is set never to ask, with full access.
- Claude's own guard on risky deletions asks anyway, in every mode. It held one seat 11 h 20 m until approved, and another 54 min until a peer agent dismissed it. No hook or setting answers it; the only hook runs at session start.
- The Herdr stop rule is prose in Herdr's instructions; the program does not enforce it.
- Model review gates missed a build failure and two failed activations. The build and the activation caught them.

## Part 3. Questions

Answer each with its number and "1" or "2", or "yes".

1. **A harness prompt holds a seat.** Should a program answer it at once (1), or rewrite the command before it runs so the prompt never appears (2)? Yes means both.

2. **Which harness may do everything?** Both primary agents, Claude and Codex (1), or one chosen harness that the other passes up to (2)?

3. **Model gates.** Should every model review that guards something a build, test or activation could catch be replaced by that code and removed? Yes or no.

4. **The Herdr rule.** Should the "outside Herdr, stop" rule be removed from the Herdr skill, with Flow guarding your panes in code? Yes or no.

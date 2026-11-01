# 484897 { Psyche core Primary }, 2026-11-01 — flow-nexus

## Focus, ruled

"I really want to focus on fixing the flow, the current one, maybe improving it. I don't know. Maybe it feels brittle to work on but we don't have much of a choice. We can then continue to work on version 1 so we can get the hell out of this horrible situation we are in."

## Flags and rehearsal, ruled

"I think it would be cool to have a feature on Flow Nexus that could show a dry-run launch… If we wanted to tweak stuff that the Flow Nexus doesn't support, we could get an agent to just modify that base system call." "the returned rehearsed would just be a string because if there's anything in there that has a space, I guess a command-line interface cannot use an argument with a space."

Mind flowNexus reports the exact launch command exists only after launch creates the reserved FlowId, the pane, the prompt memfd path and the Codex thread; the Primary ruled that Rehearse shows those as named placeholders, <flow-id> <pane> <prompt-fd> <thread>, and creates nothing; HarnessFlags.String is tokenized shell-style, each word quoted on render. Build pending at Mind flowNexus.

## Launching without the Artifact tool

Witnessed: an interactive Claude flow launched with --disallowedTools "Artifact*" has no Artifact tool and none of its guidance in the base context. Until HarnessFlags is built, the recipe is: write "permissions": { "deny": ["Artifact*"] } into /home/li/primary/.claude/settings.local.json, launch, remove it. His words: "Let's just have that setting put in, relaunch you, and then it can be taken out."

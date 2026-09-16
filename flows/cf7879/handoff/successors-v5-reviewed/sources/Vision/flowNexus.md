# Flow Nexus

## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

## Repository and skills

The flow repository holds the machinery of the Flow Nexus and is a
runtime repository. Every skill lives outside it, the basic skills
included, so that a change to a skill causes no Nix rebuild. The
basic skills give our own take on how an agent behaves in a harness,
replacing the prompt the harnesses build in.

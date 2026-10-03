<!-- to-the-living:start -->
Presentation.{ «Answers on how Flow launches a seat» }

# Answers on how Flow launches a seat

Answers to your comments on «How Flow launches a flow and builds its prompt». Everything here was checked: by reading Flow's code, and by running Claude Code and Codex in a scratch folder.

## 1. Why Claude and Codex get their ids differently

**Claude** lets the launcher choose the session id. Claude is started with `--session-id` and an id we pick, and its transcript is named after it. So Flow picks the id, turns it into the flow id, and only then starts Claude.

**Codex** does not. It makes up its own id when a conversation is created, and nothing in Codex accepts one from outside, neither the command line nor its server.

**But Codex can still be known before it does any work.** Flow can create the Codex conversation empty, with no message yet. It reads the id Codex gave it, turns that into the flow id, and only then sends the first prompt. Today's test showed exactly that: an empty conversation with an id and no turns. So for both harnesses, the flow id can exist before the model reads a word.

## 2. Who works out the flow id, and when

- **Flow, Claude seats:** Flow puts `FLOW_ID` into the pane before Claude starts. The seat never computes it.
- **Flow, Codex seats:** Flow never gives the seat its flow id. That is a gap.
- **Today's launcher script:** the script does compute the id. But each seat is also told by its startup skill to run the `flow-id` program in its first turn, and gets the same answer. That is the waste you named: a model spending a turn on something a program already did.

So your rule applies directly. The launcher puts the id into the seat's first prompt and environment, for Codex too, and the startup skill stops asking the seat to compute it.

## 3. Your rule, as Intent

You asked for this to become Intent. Proposed wording:

> Whatever a deterministic program can do is done by code, never by a model. A model's turn costs context, money and noise; it is spent only on judgment.

## 4. What a launch request carries

This is the request Flow takes today, in ethos (from Flow's message definitions):

```
LaunchProfile.{ LaunchRequestId
                Vector<LaunchSource>
                Vector<SkillName>
                FlowAspect
                PowerLevel
                HarnessKind
                ModelName
                Effort
                Option<FlowId>
                Vector<RememberedFlow>
                HerdrSessionName
                SystemPromptBundleFile
                InstructionPrompt }
LaunchSource.{ SourcePath SourceSha256 }
RememberedFlow.{ FlowId RememberingDepth }
FlowAspect.[ Psyche Mind Field ]
PowerLevel.[ High Medium Low UltraLow ]
HarnessKind.[ Codex Claude ]
```

Each part, in order:

1. a name for this request;
2. source files, each with its fingerprint;
3. the skills to load;
4. the aspect;
5. the old power level (not yet your layers);
6. Claude or Codex;
7. the model and its effort;
8. the predecessor flow, if any;
9. remembered flows;
10. which Herdr session the pane opens in;
11. the system-prompt file;
12. the brief.

A filled example, as datom, from Flow's own code:

```
Start.{ { request-7
          [ { Vision/flowNexus.md 54c08e71… } ]
          [ spirit main-flow ]
          Field High Codex gpt-6-astra medium
          Some.836818
          [ { 1b8ac0 1 } ]
          messaging-build
          /tmp/flow-system-prompt.md
          «Carry this bounded launch request.» }
        { fac697 session-1 turn-2 } }
```

The last group says who asked: the requesting flow, its session and its turn.

**"Finds the skills"** means this. Before Flow sends the first message, it looks up each named skill's file and records a fingerprint of it.
- If a skill is missing, the launch stops before anything is sent.
- The fingerprint is how Flow later proves the seat loaded exactly that file, and notices if it changed.

## 5. Can part of the system prompt stay with the main seat only?

**Yes, and it already does.** In a test with Claude Code 2.1.284, a marker word placed in the main seat's system prompt never reached its subagents. That held both for a replaced and for an added-to system prompt. Each subagent gets its own system prompt, from its agent type.

**CLAUDE.md is different:** it does reach ordinary subagents. An agent type can be set to leave it out (`omitClaudeMd`), and the built-in search and planning agents already do.

So instructions for the main seat alone belong in its system prompt. Not yet tested: a "fork" subagent, which copies the main seat's conversation.

## 6. A system prompt built from modules

Your design goes to Mind Astra through Fable: study many system prompts, give the system prompt an anatomy in ethos (what each part is: behavior, personality, operational safety, what kind of guidance), and let Flow assemble a seat's system prompt from typed modules, some overlapping with skills.

## Your answer

Comment "3 ok", or give your wording for the Intent.
<!-- to-the-living:end -->

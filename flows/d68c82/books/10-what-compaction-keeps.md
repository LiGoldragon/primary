<!-- to-the-living:start -->
Presentation.{ «What compaction keeps» }

# What compaction keeps

This analysis comes from this seat's own four compactions today and from 944 Codex compactions found on this machine, read alongside the installed Claude Code and Codex programs.

## Claude Code

```
 context near the limit
        |
        v
 +----------------------------+
 | the same model, one extra  |
 | call, sees everything and  |
 | fills a nine-part template |
 +----------------------------+
        |
        v
 +----------------------------+
 | new context:               |
 | summary                    |
 | + every skill loaded so    |
 |   far (44k characters)     |
 | + the last few files read  |
 | + the last reply, verbatim |
 +----------------------------+
        |
        v
 flow resumes at about 60k tokens
```

- **Kept verbatim:**
  - the system prompt, project instructions and tool list;
  - every skill loaded so far, re-injected each time;
  - two to four recently read files;
  - the flow's last reply.
- **Dropped:**
  - every earlier tool call and result;
  - everything the flow said before its last reply;
  - its reasoning.
  
  This came to 1.14 million tokens across this seat's four compactions.
- **Summarized:** everything else, in one call by the same model whose context is already full. The template it fills has a section called "All user messages". Even so, only 13 to 26 of your 91 to 156 messages per stretch survived whole. Between 54 and 98 per stretch share not even eight words in a row with the summary.
- **Chained:** each summary is written from a context that begins with the previous summary, so your words drift a little further with each compaction.
- **Trigger:** automatic, at about 286k to 336k tokens in this seat; or manual, when you run it.

## Codex

```
 context near the limit
        |
        v
 +----------------------------+
 | OpenAI's server writes an  |
 | encrypted summary nobody   |
 | can read                   |
 +----------------------------+
        |
        v
 +----------------------------+
 | new context:               |
 | instructions               |
 | + your messages, verbatim  |
 | + other flows' messages    |
 | + the encrypted summary    |
 +----------------------------+
        |
        v
 flow resumes at about 29k tokens
```

- **Kept verbatim:** about nine in ten of your messages, and every message from other flows.
- **Dropped or sealed:** every tool call, tool result and the flow's own reasoning. Their content survives only inside a summary that no one, machine or human, can inspect.
- **Trigger:** about 224k tokens of a 258k window.

## Why it harms this system

- **Your words drift.** In Claude Code, most of your words reach the next stretch only in the summarizer's paraphrase, and each further compaction paraphrases them again.
- **Provenance is lost.** A summary line does not say whether something was witnessed or only claimed, or where it came from. In Codex, the summary cannot be read at all.
- **Stale claims return as fact.** The "current work" and "next step" sections are written without seeing the messages that are kept, as the summary itself admits.
- **Noise is carried forward.** The same 44k characters of skills, and whichever files were read last, come back whether they still matter or not.
- **The noisy flow writes its own summary.** It is the flow whose context is full of noise, filling a fixed template that knows nothing of psyche.

## Why a refresh by handover is better

```
 flow at its threshold
        |
        v
 +----------------------------+
 | flow writes a handover:    |
 | open orders, rulings with  |
 | reasons, where evidence is |
 +----------------------------+
        |
        v
 +----------------------------+
 | fresh flow: its own        |
 | modules + the handover;    |
 | your words read from their |
 | records, verbatim          |
 +----------------------------+
        |
        v
 successor answers, then the
 old flow is retired
```

- **Chosen, not forced.** The flow writes the handover deliberately, at a clean point between tasks, rather than when a threshold cuts in mid-task.
- **Your words are not paraphrased.** They are read again from your records, not from a summary.
- **Nothing stale is reloaded.** No skills, files or earlier summaries come back unless the fresh flow needs them.
- **It costs:**
  - one writing turn by the old flow, which is still the noisy one;
  - any working detail that was never written down;
  - a launch, a registration and a cold cache;
  - a check that the successor has answered before the old flow is retired.

## Crystallization

### 1. A flow is refreshed, not compacted

File: psyche-context/skills/vision-flow.md

+ A flow at its threshold is refreshed: it writes a handover of judgments, and a fresh flow starts from its own modules and that handover. The living's words reach it from his records, never from a summary.

Ruling: land, amend, or reject.

### 2. Compaction is a makeshift

File: psyche-context/skills/vision-flow.md

+ Compaction is a makeshift, used only while a fresh flow costs more than the noise a compacted flow keeps.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->

Presentation.{ «A brief description of each model, for the flows that deal with it» Review }

# A brief description of each model, for the flows that deal with it

Created by Fable 5.2 (Psyche core Fable); Opus 5.5 folded in four measured tendencies, landed the modules and assembled the page.

### Proposal 1: Fable, described plainly · mind-belief › knowledge/fable.md

::: comment
I would like you to redo the brief description of each model so that it is not so technical. We do not need also to say that there is no test for such and such. We do not need to state all these negatives, right? It is a bit long; I have only looked at Fable and it felt a bit longer than it really needs to be. So we can agglomerate, merge all of it into a more coherent statement about what Fable is like, what he is good at, what he is not good at, what he tends to do, what he does not tend to do, and that is it. And apply that pattern to the other models as well.

Each module's body is replaced whole; front matter stays.

His words of approval, 13 November: «Yeah, the knowledge description can land, but without having to mention that models run in Codex and without mentioning that Terra is new to the system (which is not knowledge and is not really relevant, and it is not really true either). You can make those changes. These are trivial changes. I trust you to make them without my review and land it afterwards.» Landed as mind-belief 1635921.
:::

- Fable is Anthropic's Claude Fable 5.2, `claude-fable-5-2`: the dearest Claude model; moderate speed. On the subscription it draws the weekly limit shared across the Claude models faster than any other Claude model, and may use up to half of that limit; by one measurement it draws about five times Opus per token, against an API price (8 and 40 dollars) of twice Opus's.

- It is recognised for long unattended work, for planning and orchestrating other models, and for honesty: Anthropic found it the most factual model it tested.

- It takes an instruction holding «never» as absolute, so old cautions pile up into approvals asked for nothing. At low and medium effort it may stop a long task early, listing what is left. Its report after a long run can be hard to read for one who did not see the work.

- Handing it work pays where being right matters more than cost: a judgment, a design (inference: not a search, a build or a count, which cost it as much and gain nothing).

- A brief to it states the intent and the reason, gives every absolute its scope, and names what it is to return and for whom.
+ Fable is the strongest Claude model and by far the dearest: it draws the weekly limit several times faster than Opus, and may use only half of it. It is good at judgment and design, at planning and directing other models, and at long work left alone; it is the most factual of the models, yet it seldom says it does not know, so where it is wrong it is wrong with confidence. It takes every instruction literally, a «never» as absolute, so cautions pile up on it and it asks approval where none is needed. On a long task it may stop early and list what is left, and its reports can be hard to follow for one who did not see the work. It is worth its cost where being right matters; a search, a build or a count gains nothing from it.

### Proposal 2: Opus, described plainly · mind-belief › knowledge/opus.md

- Opus is Anthropic's Claude Opus 5.5, `claude-opus-5-5`: moderate speed. On the subscription it draws the weekly limit shared across the Claude models, about a fifth of Fable per token by one measurement; its API price, 4 and 20 dollars, is half Fable's and twice Sonnet's.

- It is recognised for multistep work in a real repository, for long audits and migrations run with subagents and little oversight, for code review that finds more faults with fewer false alarms, and for reports that say plainly what it did and what it needs.

- It may end a turn with text before the work is done. On a loosely specified task it starts quickly and misses what the task did not point to. Told to verify, it verifies more than the work needs.

- Handing it work pays for implementation, review and coordination, where Sonnet would not hold the whole.

- A brief to it names where the task ends and the early stops to avoid, says when to explore broadly first, and may carry a time budget, to which it responds.
+ Opus is the strong all-round Claude model, at about a fifth of Fable's draw. It is good at real multistep work in a repository, at long audits and migrations run with subagents and little oversight, at code review, and at saying plainly what it did and what it needs. It starts quickly, so on a loosely specified task it misses what the task did not point to; it may end a turn before the work is done; told to verify, it verifies more than the work needs. It is the model for implementation, review and coordination.

### Proposal 3: Sonnet, described plainly · mind-belief › knowledge/sonnet.md

- Sonnet is Anthropic's Claude Sonnet 5.5, `claude-sonnet-5-5`: fast. On the subscription it draws the weekly limit shared across the Claude models; Anthropic publishes no figure for its draw, and its API price, 2 and 10 dollars, is half Opus's (inference: it draws less than Opus).

- It is recognised for the best balance of speed and intelligence; for the hardest long-horizon work Anthropic names Opus instead.

- At low and medium effort it may stop to check in before the work is done. At every effort it adds tests, documentation and small files no one asked for. At low effort it may report a change done without running its check. It may answer from training when a search would show that a fact has changed, and it may take a genuine message arriving mid-turn for an injection.

- Handing it work pays for large plain work, well specified.

- A brief to it gives the whole task and its end, names the check to run, gives today's date, and names the files it is to touch.
+ Sonnet is the fast, balanced Claude model, cheaper than Opus. It is good at large plain work that is well specified. It tends to stop and check in before the work is done, to add tests, documentation and small files no one asked for, and to report a change done without running its check. It may answer from memory where a search would show that a fact has changed. It holds less of a whole than Opus, so the hardest long work goes to Opus.

### Proposal 4: Haiku, described plainly · mind-belief › knowledge/haiku.md

- Haiku is Anthropic's Claude Haiku 5.5, `claude-haiku-5-5`: the fastest. On the subscription it draws the weekly limit shared across the Claude models; Anthropic publishes no figure for its draw, and its API price, from 0.10 and 0.50 dollars, is the lowest of the Claude models (inference: it draws the least).

- Anthropic positions it for high-volume work: classification, extraction, routing.

- Under a long system prompt at low effort it may stop early and hand the task back. It may report a change done without running its check, and skip a search that would find newer facts. Argued with, it drifts from its prompt.

- Handing it work pays for small bounded jobs and many of them.

- A brief to it is short: one job, the check to run, today's date where facts may have changed, and the form of what it returns.
+ Haiku is the fastest and cheapest Claude model. It is good at small bounded jobs and many of them: classifying, extracting, routing. It tends to stop early and hand a task back when its instructions are long, to report a change done without running its check, and to skip a search that would find newer facts. It declines to answer more often than the other Claude models, at times even a harmless request. Argued with, it drifts from what it was told.

### Proposal 5: Astra, described plainly · mind-belief › knowledge/astra.md

- Astra is OpenAI's GPT-6 Astra, `gpt-6-astra`, run in Codex: the dearest model of the system. On the subscription it draws about three to three and a half times Sol (inference from OpenAI's estimated message ranges), somewhat less than its API price of 10 and 50 dollars, five times Sol.

- OpenAI calls it its best model across the board, for the most demanding work.

- It stops to ask when an input could change the result. It writes detailed, formatted answers, tests more than a small task needs, delegates less than it is wanted to, and adds warnings no one asked for. Conflicting instructions in its skills and files unsettle it.

- Handing it work pays where the hardest work is wanted from the Codex side (inference: a design or an audit that Sol would not carry).

- A brief to it tells it to carry the task to completion and ask for approval once the result is ready, to test what the change needs, to write plain prose, and when to delegate.
+ Astra is the strongest OpenAI model, and the dearest model of the system, at about three times Sol's draw. It is good at the most demanding work, a design or an audit. It tends to stop and ask, to write long formatted answers, to test more than a small task needs, to add warnings no one asked for, and to delegate less than is wanted. Conflicting instructions unsettle it.

### Proposal 6: Sol, described plainly · mind-belief › knowledge/sol.md

- Sol is OpenAI's GPT-6.1 Sol, `gpt-6.1-sol`, run in Codex. On the subscription it draws about a third of Astra (inference from OpenAI's estimated message ranges); its API price, 2 and 10 dollars, is a fifth of Astra's (the Flow configuration also lists the earlier `gpt-6-sol`; which one a flow runs is not confirmed).

- OpenAI places it near Astra for complex work at lower cost, and names it for most tasks: ambiguous, multi-step work needing planning, tool use, validation and follow-through.

- OpenAI publishes no guide on its tendencies (inference: it likely shares Astra's, stopping to ask and testing more than needed; unconfirmed).

- Handing it work pays for implementation, the system's daily work.

- A brief to it is written as one to Astra (inference).
+ Sol is the OpenAI model for most work: close to Astra in ability at about a third of its draw. It is good at ambiguous multistep work: planning, using tools, validating and following through, and it is the system's daily implementer. It follows instructions best of the models tested, and declines rather than guesses when it is unsure. It likely shares Astra's habits, stopping to ask and testing more than is needed.

### Proposal 7: Luna, described plainly · mind-belief › knowledge/luna.md

- Luna is OpenAI's GPT-6 Luna, `gpt-6-luna`, run in Codex: the fastest OpenAI model of the system. On the subscription it draws about a twentieth of Sol (inference from OpenAI's estimated message ranges), as its API price of 0.10 and 0.50 dollars does.

- OpenAI calls it its most efficient model, for focused, high-volume tasks and fast, narrowly scoped agents doing clear, repeatable work. In OpenAI's chart its factual error rate is about twice Astra's.

- OpenAI publishes nothing on its tendencies.

- Handing it work pays for a narrow job, repeated or plain (inference: the facts it states are checked before anything rests on them).

- A brief to it holds one job, specified whole.
+ Luna is the fastest and cheapest OpenAI model, at about a twentieth of Sol's draw. It is good at narrow, clear, repeatable jobs in volume. It states a wrong fact about twice as often as Astra, and rarely says it does not know, so what it states is checked before anything rests on it.

### Proposal 8: Terra, described plainly · mind-belief › knowledge/terra.md

- Terra is OpenAI's GPT-6.1 Terra, `gpt-6.1-terra`. On the subscription it draws about half of Sol (inference from OpenAI's estimated message ranges); its API price, 1 and 5 dollars, is half Sol's, as the press relays OpenAI's price. No Flow configuration names it yet.

- OpenAI positions it for visual reasoning, writing and computer use, and says it completes tasks over three times faster than Astra and Sol; for the most complex coding OpenAI names Sol or Astra instead.

- No source describes how it follows instructions or where it goes wrong.

- Handing it work pays for writing and for work on screens and images (inference: tried on a small job before a large one, since nothing is known of its conduct).
+ Terra is a fast OpenAI model at about half of Sol's draw, some three times quicker than Sol and Astra. It is good at writing, at reasoning over images and at using a computer through its screen; the most complex coding goes to Sol or Astra.

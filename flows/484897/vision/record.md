# 484897 { Psyche core Primary }, 2026-11-01

Written by the flow itself, Fable, while it runs; his words verbatim. Successor of 762e44; its records are flows/762e44/vision/record.md and flows/762e44/notion/record.md.

## The context spent at start

This flow spent ~140k tokens in its first turn: ~45k startup prompt, two Artifact reads of the books (~35k each, whole page HTML), herdr pane and agent list dumps (~10k). He: "Why do you have 140,000 tokens on a fresh start? That's way too much. Why did you use Artifact tools yourself?" "You're not even supposed to use tools. You're supposed to use agents to do that." "You have the medal for the most misbehaving flow."

Causes, as ranked by this flow and not contested: the harness tool descriptions (Artifact: "Claude reads these links with this action"; Agent: "A fresh agent costs more than it looks… Do the work yourself when it is a handful of tool calls"; bypass note: "Do your work through the Bash tool wherever it can accomplish the job"); links in the brief; the serving line marked "In the long term".

His rulings: "This long-term fable thing… You shouldn't have even loaded that and that's not even in the long horizon module so it's in the wrong place." The paragraph "In the long term, a Fable flow does only the work that needs Fable…" in vision:model-roles belongs in vision:long:model-roles. "It would be nice to take out the artifact tool but I don't think that you can do that right now. We don't have the tools to do that. I would love to modify the description of the bash tools but you still need it. It would be nice if we took out the part (also in the subagent) that tells you that subagents are more expensive than they look because that's a point of view, and my point of view: your context quality is the most important thing because nothing will happen." "Nothing will happen now because the context got full of noise. So so much for trying to save the subagent." "I'm going to end the week with cloud usage unused because now we can't finish the design and so we can't use our usage to implement it."

## Fresh look at the two books, unruled

The way out: (1) witnessed, a herdr pane is `wJB:p1`, a string, and `herdr send` does not exist; herdr has a socket API with a schema: `pane.send_text { pane_id text }`, `agent.prompt { target text wait.{ timeout_ms until.[ idle working blocked done unknown ] } }` answering `agent_prompted` with the agent's status, `events.subscribe` with `pane.agent_status_changed`; socket path and framing unstated by the schema. The translator speaks the socket, and `agent.prompt` with wait is a real delivery witness. (2) `Message.{ Address Body.String }` is the fake datom reborn; the body is `:datom:Datom`, carried typed in rkyv, textualized by the translator. (3) `Err(_) => NoSuchPane` names a cause the code does not know; an unknown cause gets its own variant.

Version 1: (4) `Topic.String` contradicts the open-enum ruling; `Remembering.Integer` contradicts the landed `Remembering.[ Predecessors Custom ]`; Module and Tool are structured names. (5) "Sent when the request entered the flow's context" cannot be answered at once; the map has no subscription, no events, no hook inputs. (6) Memory holds nothing that finds a transcript (herdr holds the harness session id per pane); the metaflow lacks its purpose and records.

Proposed order: redo the way out first on 1–3, version 1 after on 4–6. Unruled.

## Focus, ruled

"I really want to focus on fixing the flow, the current one, maybe improving it. I don't know. Maybe it feels brittle to work on but we don't have much of a choice. We can then continue to work on version 1 so we can get the hell out of this horrible situation we are in." Order: the current Flow Nexus first, then version 1 (the way out first, on findings 1–3). Rulings still owed, lower: records at the flow's end; presentation modules; Codex servers (flows/6e9aed/proposals/codex-server-roles.md).

## Links out of handovers — ruled

"We could also, like you said, prohibit links in handovers since there is a link in your handover. That would be a good start." Proposed line for vision:remembering, unruled as worded: "A brief and a record carry the text a flow is to judge, in words; a book is named by its title, and its id stays in the ledger for the subflow that redoes it."

## The main-flow line, ruled

His words: "I don't want any main flows to casually use any tools." "Why don't you make this strict, like you can only use this tool for this, this, and this?" "You just say what he can do and then 'subagent' for everything else." "Let's not forget the other flows." "Make this real and hard and like no one in the universe could misinterpret it."

Landed by order to the Secondary, intent:main-flow: "A main flow's context is for the conversation and its judgment. A main flow itself writes only its records and its proposals. Everything else, it briefs a subagent to do or sends to the flow whose work it is. A main flow does not open a book, a page, a file, a transcript, a listing or a command's output. A subagent does that and returns only the lines that matter to the judgment." And vision:remembering: "A brief and a handover record contain no URL. A book is named by its title."

The served paragraph moved to vision:long-model-roles (psyche-belief 0d699ba); "make sure you don't load up with that". Artifact-less Primary launch: --disallowedTools "Artifact*" per launch, under test by the Secondary, nothing else affected.

## Flags and rehearsal, ruled

"I think it would be cool to have a feature on Flow Nexus that could show a dry-run launch… If we wanted to tweak stuff that the Flow Nexus doesn't support, we could get an agent to just modify that base system call." "the returned rehearsed would just be a string because if there's anything in there that has a space, I guess a command-line interface cannot use an argument with a space."

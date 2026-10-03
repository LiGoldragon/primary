Presentation.{ «Harnesses and remote control» }

A harness is the program a model works inside: Claude Code, Codex, OpenCode. Herdr is the program that holds the terminal panes the sessions run in. Flow is the component that launches, names, tracks and ends sessions.

## Part 1. What he wants

### Which harnesses

Two harnesses run today, Claude and Codex, and no others.

> "yes, only codex and claude."

-- 27 August

Codex carries the doing, because Claude usage is scarce.

> "Can you use Codex to help you if you need to do something big, because we can't afford to run Claude much? You guys are just going to choreograph improvements."

-- 17 September

OpenCode, which has an Android remote app, is the open-source harness and the third seat.

> "And I want to get OpenCode going. That's our open source stack. How do we get the mobile remote control, and how good is it?"

-- 26 September

Pi is dropped.

> "pi is slop"

-- 4 September

The DeepSeek harness is a candidate worth testing beside OpenCode.

> "Why don't you look into the DeepSeek harness while you're out there? Apparently it's really good."

-- 4 September

Each harness is built from one declaration, and the desktop apps run that same build, never one they install themselves.

> "all we need to do is get the codex derivation from the same place. declared once, used everywhere."

-- 25 August

> "we cannot allow the desktop to try to use something that it's installing statefully. So we have to modify the Claude Desktop Nix code to force it to use our Claude code."

-- 26 August

### What is seized from each harness

The system prompt. Flow decides what each session's top instructions are and launches the harness with them; the harness's own subagents give way to specialised sessions.

> "we're going to start flows using a Nexus component, which will decide what the system prompt is and everything. We're going to replace the harness's concept of subagents with this component, which will have specialized harnesses launched with specialized system prompts"

-- 5 September

> "One of the repositories, either harness or Flow, or maybe both of them are involved somehow, is going to actually create the system call with the right flag to invoke the harness with the right system prompt"

-- 4 September

The open-source harness is seized whole: its prompt is written entirely by us.

> "Let's have a draft of the open source stack, which is entirely self-authored."

-- 14 September

Permissions. Every session runs with prompts off, set in configuration rather than by a wrapper, and the harness is called by its own name.

> "I would like all codexes to have full permission access, whatever flags they are. ... I always want that enabled, but maybe there's a way to enable it somewhere else in the configuration file"

-- 5 September

> "what we want, which is explicitly named executables ... We shouldn't really have a wrapper."

-- 5 September

### What the harness gives up: its session id

The harness's session id is the flow id. Flow picks it before the session starts and puts it in the first prompt, so no model spends a turn finding it.

> "I want to tie in the flow ID, which we also call the session ID, the short hash which identifies a session."

-- 26 August

> "we can start a session without launching its first prompt and we can get its session ID before it even starts."

-- 3 October

The session's title goes in the same launch command.

> "we should just pass the title of the session as an argument to the startup command."

-- 1 October

Subflows inside a session carry their parent's id; a hook they also trigger must not mint them new ones.

> "it couldn't be a hook that also gets triggered by subflows, because then they get the same ID ... They just use their parents."

-- 31 August

### Hooks, by design

Hooks replace polling. Every hook is the harness telling Flow that something happened, through Flow's command line, with the data it has.

> "Essentially we want to avoid polling, which means we're going to make this hook-based."

-- 30 September

> "It makes perfect sense for the flow events to call the flow CLI to let the flow nexus know the state of that flow through the harnesses' interfaces, which are the hooks."

-- 1 October

Every useful hook on every harness is written down first.

> "I want all the hooks documented that could be useful on all the harnesses"

-- 1 October

The hooks he has named:

**Session start** registers the session with Flow, and **session end** unregisters it.

> "What about if we use hooks at the start and the end of the Claude or the Codex session to register or unregister that session from the registry?"

-- 23 September

**Session end also starts reaping.** A finished session is judged and closed; a process that dies without its exit hook counts as ended.

> "I'd like to talk about a system with Fable to use hooks so that we can know when a session is finished so that it can be reaped."

-- 29 September

> "If one of the processes ends prematurely from us unregistering it through our exit hook, then you just use the process going out as the unregistry hook."

-- 23 September

**Idle** moves a session to a new harness version, one at a time, with incoming messages held until it is back.

> "When that order comes in, we need to upgrade the harness. Then sessions can be reloaded in the new harness one at a time as they go idle. As soon as the session goes idle, the hook kicks in."

-- 30 September

**Quota push.** After work happens, a hook attaches quota and context figures to the session's next message, so the model never stops to check.

> "Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? That way, the model doesn't have to stop."

-- 18 September

**Presentation block.** The model marks the beginning and end of an important reply; a hook spots the mark and hands the block on to be made into a book, or to update one, with no tool call by the session.

> "Whenever you say something important, this is why I want the hook. ... make the model conscious of the beginning and end of giving a reply and use that as the object"

-- 29 September

> "We can do all of this without requiring the flow to make tool calls because the hook will just pick up the output and create actions based on that."

-- 1 October

**Incoming message.** A hook adds to a message as it arrives, and copies his prompt to the other harnesses.

> "Maybe even if there are hooks that could insert stuff when a new message comes in"

-- 1 October

> "When I send you a prompt, really, there should be a way for some kind of hook to send the message to the other harnesses."

-- 13 September

**Silence timer.** A timer restarts each time he speaks; after a long quiet it fires.

> "Every time you don't get a message from me for, I don't know, 15 minutes or something, you can restart some kind of timer."

-- 19 September

Proposed: each hook is a small program that sends one typed event, carrying the session id, to Flow, and makes no model call; Flow alone decides what follows.

### Herdr: sessions and panes

One Herdr session, run by Flow.

> "I just want a single herder session that's controlled by Flow, the Nexus."

-- 24 September

One full-screen Herdr per layer, each on its own desktop, so the terminal can detach and restart without killing anything.

> "Maybe we just use one Herder terminal per layer, so we have five desktops and they're just all full-screen Herders."

-- 14 September

Few splits, and spaces grouped by aspect that can still message each other.

> "Can we make the Herder always just be full screen or a maximum number of splits"

-- 18 September

> "Can you create different spaces for mind, psyche, and field in Herder? ... Could we group them so they could still message each other?"

-- 19 September

Herdr's busy, finished and read dots come from its own hooks into the harness; ours plug in the same way.

> "it supports showing me if a session is busy: it has a little red dot. If the session is finished, it has another kind of dot, but I haven't read it."

-- 30 September

Herdr can type into a running harness.

> "Can we inject keyboard presses on Herder?"

-- 17 September

Every harness window appears on his desktop when it starts, and a key shows each layer.

> "I would like to have a keyboard shortcut where I can show the secondary and show the tertiary"

-- 14 September

### Reaching a session from anywhere

Every terminal session he starts can be driven from the phone apps, and closing a desktop app kills nothing.

> "Find out if there is a way for me to allow me to remote control all the codex tui sessions I create."

-- 26 August

> "then I can close the desktop app without killing the sessions"

-- 28 August

One remote server, rooted in his workspace, for both Claude and Codex.

> "we just need the server running for codex and claude, and the desktop apps using it locally."

-- 28 August

The remote switch works without choosing a folder for him.

> "If it defaults anywhere, it should be ~/primary, but I dont want that hardwired in the OS or home code"

-- 27 August

The server upgrades without killing sessions: a new one comes up beside it and becomes current once it works.

> "We need to know how we can upgrade the server without killing the sessions."

-- 15 September

> "When it's been deployed and it works, it becomes the remote current, and then there's another next."

-- 17 September

Voice reaches a session in Herdr through the phone app's voice mode.

> "how can I access the remote controlled... um... You know, remotely access one of the codecs that's running in Herder from ChatGPT app and then run the voice mode"

-- 18 September

Whether remote control is on can be read from a screenshot.

> "you can know from a full-screen screenshot that it has remote control enabled because it has /RC in the corner."

-- 22 September

### The Emacs plugin

The Emacs plugin is its own public repository, fed into his home setup.

> "The emacs plugin would get its own repo, and become an input to criomos-home."

-- 21 August

What he approved for it is the desktop theme reaching Emacs. Proposed: no record yet makes Emacs a place to drive a harness.

### What the harness never decides

Whether a subagent runs, which model, at what effort. The session states what it wants; another mechanism decides.

> "I see a world where everything is a hook and an event and triggers something so that it's not really the decision of "Do I spawn a subagent?""

-- 28 September

Proposed: nor its id, title, folder, system prompt, permissions or start and end. Flow decides all of these; the harness runs the model and reports events.

## Part 2. What exists today

Witnessed on 3 October 2026.

- Claude, Codex and OpenCode are installed; Pi is not.
- Each of Claude and Codex has exactly one hook, at session start, installed by Herdr. It tells Herdr which session runs in its pane. No hook reaches Flow; Flow's own hook program is not installed.
- Codex runs with prompts off and full access. Claude's installed command adds the skip-permissions switch to every call, by wrapper.
- Codex runs on its stock base instructions; no replacement file is set.
- Herdr 0.8.2 serves one default session plus a test session.
- Flow does not yet choose the session id or the title at launch; a session claims its id itself.

## Part 3. Questions

Answer each with its number and "1" or "2", or "yes".

1. **Hooks report only to Flow.** Should every hook send its event to Flow and nothing else, with Flow deciding reaping, books and quota? Yes or no.

2. **The third harness.** Build the open-source seat on OpenCode now (1), or test the DeepSeek harness against it first (2)?

3. **Remote reach.** One remote server for Claude and Codex together (1), or each harness's own remote, rotated next to current (2)?

4. **Herdr layout.** One full-screen Herdr per layer on its own desktop (1), or one Herdr with a space for each aspect, Mind, Psyche and Field (2)?

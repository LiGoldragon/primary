Presentation.{ «Voice input and front-ends» }

How his words enter the system, how they are read, and the screens through which the machine shows itself to him and hears his answer. Listener is the speech service. Mentci is the mind tool behind every screen. Unity is the screen people hold.

## 1. What he wants

### He speaks; nobody types

Voice is the input. No step in the system waits on a human typing into a window.

> Tell everyone the humans are not going to type on the keyboards anymore.

-- 24 September 2026

### Wispr Flow now, his own speech service later

Wispr Flow is paid for because it works on his phone, and the same subscription should serve the desktop.

> I need Wispr Flow because I need it on Android. That's it. That's the only reason they're getting my business, and because I'm paying, I want to use it on my desktop.

-- 2 September 2026

In the end the speech-to-text is his own, trained on his voice.

> We need to integrate the speech-to-text into our own system to improve the voice model to recognize my voice because it's going to be personalized. We're going to post-train our own model and run them locally or in the cloud.

-- 13 September 2026

### Listener carries every transcription

Listener is the one service his speech passes through. Wispr is one provider behind it, not the front door.

> In the end we still want to just get my credentials from wherever the Wispr application is putting them and use Wispr through my own Listener Nexus.

-- 1 September 2026

Providers are interchangeable, tried in an order set in data, and a failure tells him.

> Could you confidently implement a first-choice with fallback(s), which would be data-configured in a meta-listener operation, so that a failing Wispr Flow API would send the transcription to OpenAI, with a notification telling me about a failing provider?

-- 29 August 2026

The provider's credentials sit in the secret store under a name that is the same on every machine.

> That way, we can have it securely stored in a secure secret storage place, and Listener would use that to load the credentials whenever necessary.

-- 2 September 2026

Listener has two kinds of request: live speech, streamed, and a recording already on disk.

> We would add streaming capability to the Listener, and these would be different operations, so they would be initiated using a different message for a Listener. It could support both modes.

-- 1 September 2026

The result goes to the clipboard and a history, never typed into a window by itself.

> I never use Listener to automatically inject the text. ... Inserting into the clipboard and history suffices for now.

-- 1 September 2026

### How recording feels

One key starts and stops; nothing is held down, and it sits under one hand on his Colemak layout.

> Favor ease of one-hand reach on my layout, Colemak, over letter-based mnemonics.

-- 1 September 2026

> if meta+x isnt taken use that instead

-- 4 September 2026

He sees that the microphone hears him.

> It would be great if the widget also could show more feedback, like a spectrogram and some kind of waveform showing me that there's noise hitting the microphone, so that I know.

-- 5 September 2026

He sees the words appear while he speaks.

> Can they stream the transcription as well in real time so that we could somehow maybe have some kind of visual showing us that real-time transcription while it's happening?

-- 1 September 2026

Long speech is cut into pieces, and the machine warns him to pause when a cut is near.

> Maybe only make that widget notify us somehow that we've entered the cutoff window for the chunks, so that there's a need to leave an obvious pause soon.

-- 1 September 2026

### Noctalia, the desktop shell

All of this lives in Noctalia's status bar, not in floating windows.

> This floating Wispr status thing is kind of inappropriate for my kind of desktop. It should just be a widget in the status bar

-- 1 September 2026

Noctalia yields the theme to the system's own setting.

> noctalia shouldnt be in charge of deciding the light/theme anywhere, it should be yielding to chroma's effects

-- 19 August 2026

Nothing in the voice stack depends on X11.

> I don't want X11 in my stack. ... It's good to have it installed. It's a good fallback, and I just don't want to have to rely on it.

-- 1 September 2026

### His words are read for meaning

Speech-to-text fails, and he has no time to check it. A reader who sees the plain meaning acts on it without stopping to ask.

> There should be a skill teaching you to be reminded to stay aware that speech-to-text is what the psyche uses to type, that it will have mistakes, and that the psyche doesn't have time to read everything and correct everything.

-- 21 September 2026

> You're taking my speech-to-text way too literally. What else can you do? The speech-to-text is failing horribly. Sometimes I don't finish sentences.

-- 24 September 2026

A question he implies is still a question, and is gathered with the others.

> I want my questions to be assembled together, even if the speech-to-text misses the fact that I'm asking a question.

-- 1 October 2026

### Corrected before it travels, marked in brackets

Quoting a misheard word is misquoting him.

> I never said that; the speech-to-text made the mistake. So you're actually misquoting me if you write r-e-s-t.

-- 28 August 2026

His words are corrected before they are passed on or written down, and the correction is shown in square brackets.

> We shouldn't pass around verbatim speech to text that has not been corrected for speech-to-text errors because then it's going to create a huge hell.
>
> Even when they're logged, the psyche should be corrected and we just put the correction in. I don't know, what's canonically done: do we put square brackets around the part that was corrected for clarity?

-- 24 September 2026

Words that come back wrong are listed and taught to the recognizer.

> We could make a list as words come up that get mispronounced, add it to the speech-to-text vocabulary possible correction mode, and look into how we can maybe use that data to better inform Wispr Flow.

-- 21 September 2026

The first correction is done by the lowest, fastest layer, before the others hear it.

> The fourth layer is like the firewall. This is the layer that filters stuff out, corrects this speech-to-text, or pre-reflex, gut reflex, instinctive reflex.

-- 16 September 2026

### Mentci, the mind tool

Mentci is the service behind every screen. It holds the logic; the screens only show it.

> Mentci is the input device of our world, right? Mentci is the mind tool, and Unity is just a client to it.

-- 18 September 2026

> Mentci talks to persona. There is no "instead"

-- 19 September 2026

### Unity, the face people hold

Unity is the name people know: the app.

> People are just going to make their own Mentci, but our Unity is basically the term people are going to be more aware of, which is the client. ... Anything could become a Mentci client.

-- 18 September 2026

It is first a web app on a trusted machine on the private network, then a native app that asks his laptop to accept its key.

> Your first proposal is basically just a Unity Web app, which is a server running somewhere. We would run the server on a trusted node, and then Tailnet authentication, I guess. Maybe that's easier.

-- 18 September 2026

The web app speaks to Mentci in the system's own message language and holds no logic.

> Unity web talks signal to mentci. All logic goes through mentci Nexus operations

-- 19 September 2026

What arrives through Unity is known to be his.

> Talking through unity would mark the message as psyche

-- 19 September 2026

At heart it is a structured conversation with the right flow, and commenting is a click and a spoken sentence.

> Annotating means I click, and then I speak using my Wispr Flow speech-to-text. It's like click, click, 300 ms.

-- 5 September 2026

Live voice belongs in Unity too, with a fast second pass that fixes what was misheard.

> I can see it going really far if we just implement it ourselves in Unity, in our own user interface, and connect it to whatever voice/audio input/output. ... Then get a second pass on it with this lower model to unify the meaning, correct errors, and correct speech-to-text oopsies.

-- 24 September 2026

### Mobile

On the phone, Unity is a thin client: a small system that keeps the connection alive and runs no model.

> Let's just make a Mentci app that basically embeds a very minimal CriomOS. ... You're not going to run an LLM on your phone.

-- 1 October 2026

### The machine's own account

The machine writes to him from an account of its own, so that his phone actually rings.

> The machine would need to have its own account so that it actually gives me a notification. If I message myself I don't think, in most systems, that it would notify me. I would probably favor something that we can self-host but we don't have to self-host right away.

-- 3 October 2026

It is two-way from the start, and carries rich documents he can comment on.

> Yeah two-way is better from the start. We need something that's two-way and maybe rich also: rich documents. Something that would support commenting on the artifact itself would be the best.

-- 3 October 2026

Proposed: until Unity carries this channel, the machine's account lives on an existing two-way messenger, and his replies are corrected and marked like any other speech.

### What is never done with his voice

Proposed, gathered from the above: it is never typed into a window on its own; never quoted with its mishearings; never passed on uncorrected; never made to wait on a confirmation he must type; never routed through X11 by necessity.

## 2. What exists today

Listener runs on his desktop as a background service. It sends speech to OpenAI only; Wispr is not yet one of its providers. It carries a personal vocabulary list, including Mentci and Noctalia. The Wispr Flow desktop app runs separately, packaged for Linux in his own repository.

Noctalia is his running desktop shell, with a Wispr status widget and a Listener level widget in its bar.

Mentci exists as a daemon with a thin command-line client that observes and answers questions. A Mentci Web draft exists on an unmerged branch, rendering flashbooks. The old Mentci desktop app is deprecated.

Unity has no repository; only a test draft of a Unity Web page was found. No Unity mobile app exists. The Element messenger is installed, but no machine-owned account for notifying him was found.

## 3. Questions

1. Is the web screen called Unity Web, with the existing Mentci Web draft renamed to it? Answer yes.
2. Should Listener take Wispr as its first provider now, with OpenAI as fallback? Answer yes.
3. Which carries the machine's own account first: 1 Matrix with Element, 2 XMPP, 3 Unity itself? Answer with the number.
4. Should every spoken message pass the lowest layer's correction before any flow reads it? Answer yes.

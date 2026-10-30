# Translator

## 2026-10-30 — A datom-to-signal translator shared by Nexuses and the CLI; a Nexus emits a typed output signal, never a command string, and the translator makes the system call
Context: the living, in the Psyche core Primary chat b0d3ae, after Mind reported the flowNexus pair being declared.

Perfect you can send. Let's see if, even when we do the Flow Nexus version 1, we can also implement the concept. Oh geez I'm going to have to get into this but you're welcome to draft the first version and use that for the first prototype.

We would have this other component. I don't know if you call it a nexus because it's very different and we might have multiple nexuses using the same one. It's essentially a datom-to-signal translator that takes a target, whether it's going in or out, to or from signal or datom, whichever side you want to look at it from.

A nexus could send datom in. In the case of the Flow Nexus I'm guessing that when Flow sends a message into a herder pane, what it's really doing is composing a system call. Am I right? This translator, if that's the case, could be used to create a system call, obviously not any system call. There would have to be a spec for it because I don't want the Flow Nexus to have to type `herdr` as a string.

It would just be a certain signal type that is made specifically for that. Maybe it's like a new type of ethos. It's like an output type or a signal output type because it's not something that returns to this. It's not an object that you get back from a CLI call. I would even see a situation where the CLI itself is a user of this transcriber component.

Let's see if you follow what I'm saying up to here, just in the chat here.

## 2026-10-30 — Many translators run at once, one per version in use; each is named by a hash of the whole set of signal contracts it reads and writes
Context: the living, same chat, continuing the translator.

Well you could have multiple transcribers running at the same time because if we are updating stuff and we need the stable version to still be running, it needs to keep its transcriber (or translator) running. The new version would need its own translator because the signals change or because we change the translator or whatever.

There could potentially be many of those so they would have to have some kind of unique suffix or prefix so that we can (maybe some kind of hash derived from the totality of all of the signal contracts that it's able to read and write, or something like that).

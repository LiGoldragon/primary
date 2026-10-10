Presentation.{ «Voice input and front-ends» }

How his words enter the system, how they are read, and the screens through which the machine shows itself to him. He speaks and nobody types. Say "yes" to a number to land it; for several texts, name the number.

**1. He speaks; nobody types**
Kind: intent. Module: voice. Action: create.
> Voice is the input. No step waits on a human typing into a window, and his voice is never routed through X11 by necessity.

Rests on: 24 Sep, 1 Sep.

**2. Listener takes Wispr first**
Kind: vision. Module: voice. Action: edit.
> Every transcription passes through Listener. Wispr is its first provider, with OpenAI as fallback, set in data. A failing provider sends him a notification.

Rests on: 1 Sep, 29 Aug.

**3. The result goes to the clipboard**
Kind: vision. Module: voice. Action: edit.
> A transcription goes to the clipboard and a history, never typed into a window by itself.

Rests on: 1 Sep.

**4. One key**
Kind: vision. Module: voice. Action: edit.
> One key starts and stops recording; nothing is held down. It sits under one hand on his Colemak layout.

Rests on: 1 Sep, 4 Sep.

**5. He sees it hear him**
Kind: vision. Module: voice. Action: edit.
> A widget in Noctalia's status bar, not a floating window, shows that the microphone hears him and shows his words appearing as he speaks. It warns him to pause when a cut in long speech is near.

Rests on: 5 Sep, 1 Sep.

**6. His words are read for meaning**
Kind: spirit. Module: psyche-interraction. Action: edit.
> His speech-to-text will have mistakes and he has no time to correct them. Read the plain meaning and act on it without stopping to ask. A question he implies is still a question and is gathered with the others.

Rests on: 21 Sep, 24 Sep, 1 Oct.

**7. Corrected before it travels**
Kind: spirit. Module: psyche-interraction. Action: edit.
> Never quote a misheard word. Correct his words before passing them on or writing them down, and show the correction in square brackets.

Rests on: 28 Aug, 24 Sep.

**8. The lowest layer corrects first**
Kind: vision. Module: vision-flow. Action: edit.
> Every spoken message passes the lowest layer's correction before any flow reads it.

Rests on: 16 Sep, "The fourth layer is like the firewall."

**9. Misheard words are taught**
Kind: knowledge. Module: vocabulary. Action: edit.
> Words that come back wrong are listed and added to his speech-to-text vocabulary, so the recognizer learns them.

Rests on: 21 Sep.

**10. Mentci and Unity**
Kind: vision. Module: mentci. Action: create.
> Mentci is the mind tool behind every screen; it holds the logic and talks to persona. Unity is the app people hold, a client to it. Unity Web is the web screen, run on a trusted machine on the private network; the existing Mentci Web draft is renamed to it. A message that arrives through Unity is known to be his.

Rests on: 18 Sep, 19 Sep.

**11. Unity on the phone**
Kind: vision. Module: mentci. Action: edit.
> On the phone, Unity is a thin client: a minimal system that keeps the connection alive and runs no model.

Rests on: 1 Oct.

**12. The machine's own account**
Kind: vision. Module: mentci. Action: edit.
Text 1:
> The machine writes to him from an account of its own on Matrix, through the Element messenger already installed. It is two-way from the start and carries rich documents he can comment on.

Text 2:
> The same account, on XMPP.

Text 3:
> The same account lives in Unity itself.

Rests on: 3 Oct. Until Unity carries it, an existing two-way messenger is proposed.

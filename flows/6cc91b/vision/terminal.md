# Terminal

## 2026-09-14 — The attached view glitches on incoming messages; a command to hide or kill all the terminal windows; Ghostty memory runaway; keep the close confirmation

Context: "Maybe harder is better" is left as transcribed. The living asks whether Claude keeps running with all windows closed.

> There's a glitch on the terminal cell, I guess, which is what we're using to show Claude right now. I'm watching it, and when the message comes in, the colors are wrong, I think, too, compared to how it looks when I run it in a standard terminal in Claude. Maybe harder is better.
>
> I guess the continuity of the codex is because it's running on the server, but have we done that with Claude? Can I close all the windows, and will Claude still keep running? That would, I think, be better and more reliable. Is that what's happening now?
>
> Let's make the recall of all this and stuff easy so that I can turn them all off or turn them off individually, right? I could have a command where they all hide, basically, so all the terminal windows are killed, which allows me to actually restart the terminal.
>
> Ghost tty sometimes starts to go crazy. It still has memory runaway glitches. Maybe we want to look at better terminal candidates, but I do like how it asks me if I'm sure before closing a terminal if there is a program running.

-- psyche, STT.

## 2026-09-14 — One Herder terminal per layer, five full-screen desktops; Herder keeps the process alive; a systemd container per layer

Context: "Herder" is the living's name for a terminal session keeper; the earlier search found nothing by that name on the machine, so the flow asks which tool it is.

> For Claude and Codex, maybe we just use Herder. That could be a good idea. Maybe we just use one Herder terminal per layer, so we have five desktops and they're just all full-screen Herders. How does that sound? I think that's smarter. We don't have to worry about how to render everything with our own homemade terminal multiplexer, and we can detach and restart the terminal. It's more reliable too for production. The Herder process keeps it alive more reliably, and I guess we'd use a systemd container system since we're running systemd, right? Just going to use that

-- psyche, STT.

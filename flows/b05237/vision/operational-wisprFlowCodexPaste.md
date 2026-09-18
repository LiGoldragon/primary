# Operational: Wispr Flow speech-to-text uses Ctrl-V to paste, but Codex needs Ctrl-Shift-V — find a fix without breaking everything else

## My speech-to-text does Control-V to inject text. Codex doesn't work with that — it tries to paste an image. You need Control-Shift-V, but I don't want to break everything else

Context: living request to Field Sol flow 33ba2b, relayed verbatim to
primary Psyche opus (Claude, medium, flow b05237) on 2026-09-18. The living
uses Wispr Flow for speech-to-text, which injects text via Ctrl-V. Codex's
UI intercepts this as an image paste instead of text. Ctrl-Shift-V works for
text, but changing the keybinding would break other applications. The living
asks for a fix that makes Codex accept the Wispr Flow paste. Logged by the
main flow before acting.

> Also, can you find out how we can make it so that, because the way my speech-to-text works now is that it does Control-V to inject my speech text when I'm done with my Wispr Flow recording, we can make that go into Codex's UI? It doesn't seem to work. It tries to paste an image or something, and it doesn't paste the text. You need Control-Shift-V for that, but I don't want to break everything else just for that. Maybe we can make Codex work with that.

-- psyche, to Field Sol 33ba2b, relayed to primary Psyche opus b05237.

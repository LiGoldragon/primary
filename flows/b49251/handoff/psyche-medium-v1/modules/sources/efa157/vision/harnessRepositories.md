# Harness repositories

## The Claude and Codex hijack repositories get less aggressive names; they are the harness-specific parts of the code, like the CLI for the harness; the name is deterministic: the name of the TUI being plugged into plus signal, or Claude harness, Claude Connect, Claude MCP

Context: typed to the primary Claude efa157 on 2026-09-16, resuming after the speech-to-text recording stopped; the first sentence completes the message in subflowDispatch.md ("query ... the transcript files automatically"). The questions at the end (is that what it is called from inside the harness; is only part of it on the MCP) are answered in the reply; "let's ... rename those repos" is a working instruction, recorded in log.md. Logged by the main flow before acting.

> We had this Claude hijack, but maybe a Codex hijack-type repo already. I don't know exactly what they were called, but let's use less aggressive terminology and rename those repos. They're just the Claude- and Codex-specific parts of the code, like the CLI for this harness.
>
> Whatever we call it, maybe we just call it whatever. Make it deterministic, so it's just the name of the TUI that we're plugging into Claude, plus something-signal, right, because we're using signal-type system communication or datom, or just Claude signal. You're interacting with the Claude harness, or the Claude harness, or Claude Connect, or Claude MCP, or is that what we call it from inside the harness? Or do we have just part of it on the MCP?

-- psyche, typed.

## The launch and reset commands belong in the right CLI: adapters per harness, a Codex bridge and a Claude bridge, addressed by flow id; the Nexus asks Flow where the files or the socket are and sends a typed command into the harness; anything big, a reset, sits on the meta CLI, given permissions later, so the security model is stratified from the start

Context: typed to the primary Claude efa157 on 2026-09-16 at 17:3xZ, after the launch had to be handed to the living as shell commands. "What would you decide to call these adapters?" is answered in the reply. Logged by the main flow before acting.

> We should put these commands in the right CLI. This would be like a Codex, whatever we did. What would you decide to call these adapters? Codex adapter with the right flow ID, I guess, we would address them. I'm not sure, and then maybe the Codex bridge. Nexus communicates with the Flow to figure out where the right files are, or the socket, or whatever it is he needs to send the command, which is like a typed command in the harness, which he can send. That's what the Codex or the Claude bridge CLI is there for.
>
> Obviously, if it spits something big, like using a reset, it would be on the Meta CLI, which can then be given permissions later on, so we already stratify our security model.

-- psyche, typed.

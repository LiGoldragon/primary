# Datom MCP

## 2026-09-14 — Should we just start the message Nexus with a simple Signal Datom syntax; the simplest MCP server, a single Datom string in and out

Context: comment on the gap "the messaging you chose is off main and unwired", after asking about left-behind branches. Framed as questions and "I know that...might be", so logged as notion; the request to present unreviewed branch ideas is in the log.

> Should we just start this messenger, our message component Nexus, and use that with a really simple Signal Datom syntax for agents to use? Would it be more efficient to create a really, really simple MCP server that can call certain components? Internally, it would just call the CLI for that component and then pass the string, because the MCP server call would be really simple: such component with such payload. Basically, you could almost just make it a single field and use Datom to contain all the data, so it's the most simple MCP server ever. It's just a string. That's the spec, and it contains the Datom, and it returns a single string too, which is the Datom, which is going to also contain errors and everything.
>
> I know that a bash call, calling the CLI, and passing the Datom string might be more complicated than making this really simple MCP server. Call it Datom MCP or Signal MCP, or maybe something else.

-- psyche, typed, artifact comment.

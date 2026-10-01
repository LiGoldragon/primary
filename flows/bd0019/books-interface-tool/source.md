Presentation.{ «Books as the interface, rendered by a tool» }

## Books as the interface, rendered by a tool

1. **Rendering needs no model.** What Sonnet does today is already mechanical except three things: drawing the illustrations, choosing the four points, and its agree-or-disagree notes. Extracting the block, building the page shell and shooting the phone-size check are scripts. The renderer to adopt is a small Rust library, pulldown-cmark, pure and offline, whose event stream splits one point per page and gives every paragraph an anchor your comment can attach to; pandoc only when you want an ePub. A text-only book then costs nothing, as you said: "there's a version of this that only needs nothing because there's no illustration."

2. **The display Nexus.** A minimal one, by our convention `display-nexus` with `signal-display` and `meta-signal-display`: it subscribes to presentations, takes a `Point` into a transcript or a `Present` with pushed content, renders, keeps the book in its own store, serves it, and takes `Comment` back as typed signal, with the book, the paragraph and your words, forwarded to the source seat. Your records already name this thing: "That's Mentci Web. Why don't we just make Mentci Web?" (STT, 21 September) and "Unity is just a client to it" (4a2502). One tension for you: the same record also calls Unity "basically a Mentci server"; I read the Nexus as Mentci and Unity as one client of it.

3. **The client, first and later.** First, a web app the Nexus serves over the tailnet: no model call, best phone reflow, offline through a service worker, lowest cost, reachable only inside the tailnet. Unity later, as a second client of the same feed: it renders text well but has no Markdown of its own, so the Nexus would translate for it, and it carries the engine's runtime and licence. A native Android app sits between the two. Matrix delivers links and takes replies but not typed comments.

4. **The remote control.** Witnessed: six sessions here run with remote control on, three Claude and three Codex. The vendor says it only polls outward and opens no inbound port, and that transcripts, tool activity included, are stored on its servers. The surface you name is real: the relay is a command channel into every session that opted in, and several of these run with permissions skipped. The display Nexus on the tailnet removes that surface only once remote control is switched off; a compromised display reads books and returns comments and reaches no shell.

## Rulings

- pulldown-cmark as the renderer, inside the display Nexus.
- The display Nexus is Mentci; Unity is a client of it.
- The tailnet web app first; and whether remote control is switched off on seats once it stands.
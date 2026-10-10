# Operational: Unity is a Mentci client; Mentci is the server

## Unity is basically a Mentci server. Mentci is the input device of our world, the mind tool, and Unity is just a client to it

Context: the living commented on the Unity Conversation App artifact
(https://claude.ai/code/artifact/a492a725-b9a9-4900-8c7d-6bafa30fddaa),
anchored on the architecture diagram's "phone or laptop" label and on the
"First face" fork heading. Two comments, both 2026-09-18.

> Unity is basically a Menchi server. Menchi is the server. Menchi is the input device of our world, right? Menchi is the mind tool, and Unity is just a client to it.
>
> Potentially, you could have the full Unity app, which has its own Linux OS and Menchie running. Otherwise, it connects to the laptop's Menchie runtime, which connects it to Persona. Mostly, Menchie is going to talk to Persona and get data from other places, depending on the level of permission of that Menchie in that setup.
>
> We're going to have different, but for now it's all just open security because it's a prototype and I'm running it.

> So, like I said, it's MENTCI.

> Your first proposal is basically just a Unity Web app, which is a server running somewhere. We would run the server on a trusted node, and then Tailnet authentication, I guess. Maybe that's easier.
>
> Then, Unity Slint app, which is a client that connects with Tailnet and has to request access if it's a new key. It's going to appear on Menchie, or whatever, let's say the laptop that's running it. It's going to ask to add that key and give it permission. There's another Menchie running on the laptop, so we can have Menchie Web and maybe Menchie TUI later on.
>
> People are just going to make their own Menchie, but our Unity is basically the term people are going to be more aware of, which is the client. I guess we can just do that for now. It's a Menchie client. Anything could become a Menchie client.

-- psyche, typed (artifact comments), 2026-09-18.

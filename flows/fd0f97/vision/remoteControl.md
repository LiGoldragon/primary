# Remote control

## An asymmetry: Codex launches sessions as part of its server; the server must be upgradable without killing sessions; maybe two servers, maybe Flow launches from the upgraded server; a hard cut and switch would be bad for subflows

Context: typed to the primary Claude fd0f97 after it reported that its process descends from Codex's remote-control app-server. Questions are answered in the reply. Logged directly by the main flow before acting.

> We have an asymmetry of architecture here because Codex launches them as part of the server, and this is also creating a problem. We need to know how we can upgrade the server without killing the sessions. Otherwise, we're going to have to find a way to make this upgrade happen smoothly. Maybe the way Flow chooses to launch from the upgraded server, but can we have two servers? Aren't we going to create a number of different servers for the remote access to make this difficult? Do we need a hard cut and switch, which would be really bad for subflows, especially, I think, to restart all these subflows?

-- psyche, typed.

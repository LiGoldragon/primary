From Psyche Fable c8d79f (w4:p7) to Mind Astra 0ab019. The living, typed in my terminal 2026-09-19: "Get me a unity web poc from mind astra".

Outcome wanted: the living opens Unity Web in a browser on ouranos, sees the live flows from Herder, opens one and reads its real conversation from its transcript, types a message, and the message lands in that flow's pane. Running, witnessed by you, with the exact command or URL to open it. A POC: synthetic data is out, the real roster and a real transcript are in.

The living's rulings today, verbatim in flows/c8d79f/vision/: "Unity web would also talk to the daemon, but could run next to it." "Mentci talks to persona. There is no 'instead'." "Talking through unity would mark the message as psyche."

Consequences you build to: Unity Web is a client of the Mentci daemon, co-located is fine. The data path is Unity Web -> Mentci -> Persona; Mentci does not read Herder or transcripts itself. For the POC, the Persona seat is the thinnest thing that answers roster and history from Herder and transcripts, labelled as the POC Persona seat; Persona's repository is github.com/LiGoldragon/Persona and the living calls it stale, so do not wait on it, but put the seam where Persona goes. A message sent through Unity is psyche input: mark it so on the way in, and the messenger's typed-message rule applies to everything else.

Fork 7 is still unruled by the living. My assumption for the POC, stated to the living and overturnable: the backend is a fresh minimal Mentci daemon on the current contracts carrying only roster, conversation, and send, plus the web surface. No migration of the old daemon, no backward pins, no Criome, open security. If the living rules migration later, the POC daemon is the first slice of that or is discarded; either is acceptable for a POC.

Network: localhost on ouranos until Field enrolls the host on the Tailnet; do not block on the Tailnet.

Reuse the landed Unity Web draft at flows/0ab019/unity-web-draft/ as the client; replace its synthetic adapter with the real one. Delegate to Mind Sol as you see fit; exact locks on every write. Report to me at w4:p7 with: how to open it, what you witnessed working end to end, and what is stubbed.

# remote control all the codex tui sessions I create

## 2026-08-26T20:19:21+02:00

The living asked for an investigation into a desired Codex interaction:

> Find out if there is a way for me to allow me to remote control all the codex tui sessions I create. Right now, it doesnt allow me to connext to sessions that have an "active writer", but I am able to do it with claude code, by enabling remote control in that session, then my remote messages just appear in the terminal session. I would like to do the same with codex

## 2026-08-26T20:32:10+02:00

The living clarified that remote control means the Codex app on the phone, not a generic local message-ingress mechanism:

> No, I don't know if you understand what I'm saying. I'm trying to use the remote control feature in the Codex app on my phone, and right now I cannot connect to a session that is essentially running in a terminal somewhere. So I think you misunderstood what I want from your last comment.

## 2026-08-26T23:09:40+02:00

After being shown the proposed Nix-owned anatomy—an always-running Home Manager app-server service using the single existing Codex derivation, with no standalone installer or updater, every terminal TUI connecting to it, and ChatGPT remaining independent while sharing the derivation—the living approved realization and expanded the deployment scope:

> ok, lets do that. and then also deploy the updated criomos to zeus (in addition to ouranos and/or my profile), and make sure bird's profile is updated on zeus.

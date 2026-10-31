# Deployment

## 2026-10-29 — Builds run on Prometheus, the builder, not the laptop
Context: the living, in the Psyche core Primary chat d9065e, during the night orders.

And I hear my laptop fan run a lot, but I don't hear Prometheus's fan running. You have this giant beast of a builder over there, so make sure it's in use.

## 2026-10-29 — No cargo on the laptop: a Nix-heavy workflow, enforced; without Nix the files move to Prometheus and run there
Context: the living, same chat, after being told the laptop load was the harnesses and local nix evaluation.

Make sure we're not running cargo on the laptop. Just use a Nix-heavy workflow and make it enforced so that anyone who wants to test anything cannot just change the belief without my approval. Make this a simple edit if you need to, if it's not already like that.

I want a Nix-heavy workflow so that we use Nix to build stuff and we don't load the localhost. I really don't want to be running the Rust compiler on a laptop that's barely keeping up with the number of agents running. That's why we have the remote builder. If someone wants to do something without Nix, they can always move the files over and just run everything remotely.

Let's maximize this huge host that has a massive amount of RAM and CPUs because my laptop is just running hot and barely keeping up.

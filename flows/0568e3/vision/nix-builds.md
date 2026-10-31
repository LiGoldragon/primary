# Nix builds

## 2026-10-30 — Efficient Rust builds in Nix, where dependencies are not recompiled, a holy grail of his for years; a side conversation opened
Context: the living, same chat, same message.

I'd also like to start a tiny side conversation on efficient Rust builds in Nix, which we might not even be anywhere close to. Maybe somebody has done it. Maybe nobody has but it's been a holy grail of mine for many years. If someone could create a system that does efficient compilation, where, if you know, all the dependencies don't have to be recompiled. Hopefully we're using something at least halfway there.

## 2026-10-30 — The most efficient build system: modular compilation, so a changed dependency does not recompile everything
Context: the living, in the Psyche core Primary chat 0568e3, after the Primary described crane's one-derivation dependencies and crate2nix's per-crate derivations.

Well let's use the most efficient system. I think that if we use the system that compiles all the dependencies together, then when a dependency changes we have to recompile everything. That's not very efficient so I would prefer a system that has more modular compilation logic.

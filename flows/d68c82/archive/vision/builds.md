Landed, in psyche-context/vision/nix-builds.md f81b7b.
## 2026-10-16 11:14 One registry of builds; recency- and frequency-based collection

"I don't want a bunch of Nix builds laying around everywhere. We should only have a single registry of Nix builds, which could be made by a single Nix profile. We don't need to keep any of those builds actually. Then we can have sane recency- and usage-frequency-based garbage collection on the remote store. That's a lot more sane. We don't even need to create any links except the profiles that are in use on the machine."
-- psyche, STT.

Landed, in psyche-context/intent/main-flow.md 228c47e.
## 2026-10-29 — The implementation-detail line is removed from main-flow
Context: the living, comment on the book Modules by role and function, 18:42, on proposal 1, at "A main flow is the manager of the flows it delegates to. It stays out of implementation-level detail."

I see some very potentially harmful ghost effects here from saying that a main flow does not in any way get involved in implementation-level details, which could lead to designer flow refusing to design. This is a really puzzling line and I don't even remotely remember approving anything like this. Let's start by removing it and then we can explore maybe the intent or any possibly valuable intent that it was trying to express (which I can sort of kind of see a glimpse of). But there's very little gold to be mined out of this ore, I think, if it hasn't been mined already in the rest of the module.

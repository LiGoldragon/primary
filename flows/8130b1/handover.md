# Handover, flow 8130b1 (Psyche book Haiku)

**Pursuing:** publishing books for Psyche core Opus: a1uw (versions and types of belief), g5e0 (intent-universal), 74jr (types of belief as it stands).

**Where it stands**
- «Vision is a series of versions» (versions.md) republished unchanged at https://claude.ai/artifact/F7Xm41biFdr1S2nVKD9REp (version 6).
- «The types of belief»: republished at https://claude.ai/artifact/HosUvmBsEwH6xpD3t6Hzxg (version 8) from /home/li/primary/flows/4fb10a/proposals/types-of-belief.md; the build passes. Link sent to Opus. Not verified that every settlement of order k5wf is on the page as Opus meant it. Proposal 6 and the excerpt placement were the blockers; resolved in the build by moving the dependency sentence under Proposal 1 and by the excerpt placement that now passes. Opus has not confirmed.
- «Intent holds what every flow needs»: published at https://claude.ai/artifact/VFJKBGMvr1PZ6Xw5wq7d5U from flows/350f85/proposals/intent-universal.design.md. Link sent to Opus. Comment thread 15283df3 asks for all other comments on the page; auto-reply stands; thread left OPEN, not resolved.
- Older pages (The system always moves, Each version vision in its own module, Who audits who holds the code who is asked, The Living Nexus, Permaflows): none republished by this flow.

**What works**
- Build: `bb /git/github.com/LiGoldragon/makeshift-tools/book-build.clj <src>.md <out>.html --figures <dir>`; run it and read the exit status; output is empty on success.
- Mid-line moves in a proposal: the checker reconstructs a move only at its own place; a removed line directly followed by a move container (no blank between) is completed by the move's content, which is how a mid-line sentence leaves one place and enters another without duplicating.
- A bare `-` after a move carries a blank line.
- A `::: shown` excerpt sitting as unmarked text in a module view is read as module text and fails; keep it out of the view.

**What does not work**
- Flow Nexus Result and Done replies to predecessor orders (cv3w, a1uw, jlg0) are refused Unresolved; `Answer` returns AnswerRejected.Open. Those orders were answered by Notice to Opus instead; cv3w and a1uw remain formally open.
- Sending from this flow with a Result is not possible for the predecessor's requests.

**Next step:** on the next order from Opus, check the build first. Answer the open comment thread on intent-universal only if its author needs more than the posted reply.

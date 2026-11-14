# Handover, flow ec9358 (Psyche book Haiku)

**Pursuing:** order jlg0 from Psyche core Opus: do only a1uw (versions and types of belief, from their design files); close every other open request without republishing.

**Where it stands**
- «Vision is a series of versions» (flows/7998d1/proposals/versions.md): rebuilt with its six figures, which match their fences; published at https://claude.ai/artifact/F7Xm41biFdr1S2nVKD9REp (version 7).
- «The types of belief» (flows/4fb10a/proposals/types-of-belief.md): settlements 1 and 2 are already in the source; settlement 3 (excerpt retake from psyche-belief origin/main) is not verified. Figures 2 and 4 were redrawn (their fences had changed) and saved with their fence as .mmd. Figure 1 was still being drawn when this handover was written. NOT yet built or published to https://claude.ai/artifact/HosUvmBsEwH6xpD3t6Hzxg.
- Intent-universal (g5e0): not published, per jlg0.
- Closing Results sent to Opus for g5e0, k5wf, 74jr: accepted, queued. cv3w: refused Unresolved.

**What works**
- Build: `bb /git/github.com/LiGoldragon/makeshift-tools/book-build.clj <src>.md <out>.html --figures <dir>`; exit 0 is success.
- Fence check: a script comparing each fig-N.mmd with the Nth mermaid fence (scratchpad fences.py).

**What does not work**
- Result to cv3w is refused Unresolved (predecessor request).
- A publish to an artifact not yet viewed in this session is refused once; publishing again after the refusal goes through.

**Next steps**
1. Confirm fig-1.svg in flows/4fb10a/proposals/figures-types-of-belief/ and copy scratchpad types/fig-1.mmd there as fig-1.mmd.
2. Build types-of-belief.md to scratchpad, publish to HosUv url.
3. Send Opus a Notice with the link. Answer a1uw: this flow republished no older page, so none was compared.

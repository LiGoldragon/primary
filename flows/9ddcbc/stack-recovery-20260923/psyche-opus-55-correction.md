# Psyche Opus 5.5 selector correction

Observed 2026-09-23 on the retained native session `d8df703d-d083-4c29-9597-6b32e7411b75`, Herdr `messaging-build/wD:pD/term_65c2be0c1adcd62`, claimed Flow `d8df70`. No second session or pane was created.

## Cause and preserved evidence

The source packet at `flows/9ddcbc/stack-recovery-20260923/source-packet.md` lines 8–12 mapped the living's requested “Opus 5.5” seat to `claude-opus-5`. That mapping propagated to `psyche-opus-5.profile.json`, `psyche-opus-5.manifest.json`, the retained failed state, the generated receipt manifest, and the partial observation. Those failed-attempt records remain unchanged as evidence. The original process command requested `--model claude-opus-5 --effort medium`; its first transcript responses reported `claude-opus-5`.

## Supported correction and readback

The retained session opened Claude's native `/model` selector. The selector visibly offered “Opus 5.5” as its own entry while marking “Opus 5” as the current model. The session-only choice was selected and the native confirmation read: `Set model to Opus 5.5 for this session only`. The footer independently read `Opus 5.5·medium`.

A bounded no-tool witness turn replied only `MODEL_SELECTION_WITNESS`. Its exact assistant transcript record reports model identifier `claude-opus-5-5`. Transcript: `/home/li/.claude/projects/-home-li-primary/d8df703d-d083-4c29-9597-6b32e7411b75.jsonl`; SHA-256 at this observation: `75160d3b9e6d7d7631d31f6378c921970cdf1b69c0250ba11c5d309df4e956a8`.

The owning source profile and launch manifest now select exact `claude-opus-5-5`. There is no alias or fallback to Opus 5.

## Remaining gate

The retained session contains useful work and is preserved, but its bootstrap began on Opus 5 and the full-skill/source receipt was interrupted. It is therefore **not a clean Opus 5.5 launch acceptance**. The old failed state and partial observation must not be relabeled as 5.5. A future continuation needs a verifier that treats the explicit native model transition as provenance and proves all post-switch required context, or a separately authorized replacement after preserving this session. No duplicate launch, restart, retirement, HM registration, or predecessor change occurred in this correction.

# Psyche.{ Fable f5a6e9 }

- Launched as Psyche Primary (designer), successor of Psyche Fable b27767, from flows/d4ae97/reports/fable-context-modules-brief.md, read whole. Brief's reading list (context modules, flow and metaflow, ethos and datom) read whole. Secretary: Psyche Opus d4ae97.
- Told d4ae97 the three books and their order: context modules; Flow and the metaflow; stored type and datom form. Transported.
- d4ae97: the Intent/contextModules.md line is already before the living in its book «Context modules, into Intent»; book 1 designs on it, does not propose it again.
- Dispatched: witness of Curriculum skill types, dependencies, startup skills and Flow's launch composition; witness of how a hook can measure context size from transcripts.
- Witnessed (harness placement): Flow launches Claude with --system-prompt-file (herdr/launch.rs:1367) and a first prompt of ≤800 chars opening with up to five stacked /skill tokens (composition.rs:604-630); Codex keeps the stock base and gets skill input items plus the bundle text in the first turn (codex.rs:~755-785). A skill is hidden from the model by disable-model-invocation (Claude) or allow_implicit_invocation: false (Codex, not in use in Primary); a hidden skill still enters by /name at the prompt head or a skill input item.

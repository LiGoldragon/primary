# Persona stranded branch evidence

Status: proposal evidence only. The Persona draft was based on remote `main` at `9469b0a154d1049545968ff0878b265718c31774`. The reviewed `09ee526cbde8dd6a9dc54b1b3583e2a034d0e063` is a descendant path with 21 commits and a 59-file `+3208/-2879` delta; it was not merged or selected as the draft base. This is migration risk evidence, not an observed breakage.

The isolated catalog proposal was pushed as `flow/5f4fea-minimal-persona` at `b6f6ef0aedbffb1dd09d49bba20eb1c40a75d27b`, directly verified against `git@github.com:LiGoldragon/persona.git`. It contains a trait-oriented in-memory engine catalog, desired/observed generation and stale-observation handling, independent fixture engines, and quota reset/pace fixtures. `cargo fmt --check` passed and `cargo test` passed three tests. The Nix check was defined but its input fetch stalled; it is not claimed green.

The later anatomy ruling sharpens the draft boundary: Nexus receives Signal only; CLI translates inline datom; Flow roster belongs to Orchestrate. A future proposal may use separate Persona Nexus ordinary/meta sockets and closed `signal-persona` / `meta-signal-persona` Ethos vocabularies, with launch assembling the first prompt and handing it to the harness in one call. The catalog commit does not implement that anatomy and must not be represented as deployed or activated.

Quota review requirement remains open for a successor draft: reset must invalidate an old-window sample; a future timestamp or zero remaining interval must yield an explicit unknown rather than a misleading per-day value. No subscription target or live engine count was guessed, and no socket, process, provider, VM, or system activation occurred.

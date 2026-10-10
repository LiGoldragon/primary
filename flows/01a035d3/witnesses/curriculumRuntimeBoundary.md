# Curriculum runtime boundary

Method: code read `/git/github.com/LiGoldragon/Curriculum/src/assembly.rs`

The typed generator request already carries a source root, workspace root, manifest path, and mode. The engine reads DOTOS manifests and Markdown skill modules beneath the supplied source root while it runs, then renders or checks consumer files. Check mode compares existing consumer files and does not write them.

No `include_str!`, `include_bytes!`, build script, or equivalent compile-time content inclusion was found in the Rust code. Authored curriculum is runtime input to the engine, not Rust source generated or embedded during compilation.

Generated outputs include consumer-owned `.agents/skills`, `.claude/skills`, role packets under `.claude/agents`, `.codex/agents`, and `.pi/agents`, and the consumer inventory `skills/generated-role-outputs.dotos`.

The coupling occurs in `/git/github.com/LiGoldragon/Curriculum/flake.nix`: one filtered source is used both as the Rust package source and as `SKILLS_SOURCE_ROOT` for the runtime wrappers.

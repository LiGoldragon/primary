# Lojix timeout removal implementation boundary

Method: code read `/git/github.com/LiGoldragon/lojix`,
`/git/github.com/LiGoldragon/CriomOS`, the active flow vision, and the
authored Curriculum Lojix instructions.

The active written-psyche record states:

> what timeout? I never approved any timeout

> get rid of that timeout and resume your goal

The effect deadline is a typed, positional startup-archive field, not an
operational service-manager limit. In the producer it is read by the
configuration writer and carried by `DaemonConfiguration` into
`EffectExecution`; this is the point where elapsed wall time can fail an
otherwise active Nix, SSH, or activation effect. In CriomOS the
`services.lojix.effectTimeoutSeconds` option and PersonaDevelopment projection
produce that positional writer field. The Lojix README and authored
`Curriculum/skills/lojix.md` describe the same shape.

The required end shape is consequently one incompatible contract: no
`effect_timeout_seconds` configuration member, no timeout positional writer
input, and no elapsed-wall-clock execution branch. Every typed writer producer
and consumer must use the shorter configuration object. Test evidence must
exercise an effect that remains active beyond a controlled synchronization
point and succeeds when released, without a real-time delay or a source-text
assertion.

The producer must land and be pushed before its CriomOS flake consumer is
updated to its immutable ref. No deployment, activation, daemon restart,
closure copy, or runtime-state operation has occurred in this subflow.

Method: remote-ref and check evidence reported by isolated Lojix, Curriculum,
and CriomOS workspaces.

The pushed producer `main@origin` is
`edbb53aab003a071ffbb0f6643e8d29c0bf9b691`; its package version is `0.18.0`.
The pushed CriomOS `main@origin` is
`a4322cd144821119936283339b1bc5926b97a738`, and its Lojix lock pin is the same
producer revision. The producer source was first pushed as a feature ref and
then fast-forwarded to main before the consumer candidate was landed. This
ordering prevents a consumer lock from referencing an unlanded producer.

The producer's Cargo and remote-builder checks, the Curriculum generation and
remote-builder checks, and the applicable no-input CriomOS checks are reported
passed. CriomOS whole-system evaluation/build remains unattempted because its
typed projection inputs were intentionally absent; its repository forbids
making them up.

## Sources

- [current timeout ruling](../vision/zeusUpdate.md)
- [timeout provenance](lojixEffectTimeout.md)
- `/git/github.com/LiGoldragon/lojix/src/lib.rs`
- `/git/github.com/LiGoldragon/lojix/src/bin/lojix-write-configuration.rs`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix-persona-development.nix`
- `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md`

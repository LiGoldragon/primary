# Psyche Ultra Low exact model amendment

The canonical one-seat launch manifest now requests `claude-haiku-4-5-20251001`, matching the model currently written in the Field-owned Ultra profile. The manifest change is only that model string: session `messaging-build`, workspace `wD`, profile path, Ultra seat, and `medium` effort remain as before. The profile owner 753e69 still holds its exact-model source/test lock; this matching read is not its final committed profile receipt or a managed validation result.

The lifecycle is split by ownership: 753e69 owns the canonical profile, model catalog, and profile test; 03e825 owns this manifest amendment and any authorized managed execution; 6db4fe owns launcher continuation repair under lock 4090. The prior second attempt remains failed with a retained `wD:p8` shell, terminal, and reserved native UUID, but no Claude process or delivered startup prompt. Its preflight and state, and the original first-attempt state, are unchanged by this amendment. No native identity, HM route, title readback, readiness receipt, or acceptance has been established for Psyche Ultra Low.

No launch or retry was run for this amendment. After the manifest was pushed, the parent ran the supported batch `validate` command from its real managed `w0:p3` shell with `HERDR_ENV=1`. Parent readback was `valid: true`, one seat, session `messaging-build`, workspace `wD`; the controller's source validation completed. This is a validation result, not a start, native receipt, or acceptance. The launcher continuation gate remains separately owned by 6db4fe.

## Sources

- `flows/753e69/psyche-haiku-native/launch-manifest.json`: exact model and unchanged one-seat workspace/effort fields; scoped working-copy diff inspected before commit.
- `flows/753e69/psyche-haiku-native/profile.json`: current matching model read; owner lock 4127 observed, so this is not a landed profile receipt.
- `flows/03e825/psyche-ultra-native-attempt2/state.json` and `flows/03e825/reports/psyche-ultra-retry.md`: retained failed attempt and evidence boundary.
- `orchestrate 'Observe.Locks'`: lock 4128 for manifest amendment, lock 4127 for profile/test, and lock 4090 for launcher source observed before commit.
- Parent's direct managed-shell `native-batch validate` readback after the manifest push: `valid: true`, one seat, `messaging-build`, `wD`; no start was called.

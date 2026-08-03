# Independent Spirit Runtime Verification

Scope: independent, read-only verification of the Spirit recovery deployment on
`goldragon/ouranos`. This lane does not deploy, activate, restart, stop, or edit
runtime state. Corpus bodies and secrets are excluded.

## Baseline before approved activation

Observed at `2026-08-03T18:55:15+02:00`:

- **Stale:** `spirit-judge.service` was `failed/failed`, result
  `start-limit-hit`. Its generated fragment was loaded, but an unmanaged
  `override.conf` was also effective. That drop-in replaced `ExecStart` with a
  collected `spirit-judge-daemon-service` target; the last attempt ended
  `203/EXEC`.
- **Wired but unavailable:** `spirit-daemon.service` was `inactive/dead`. Its
  effective unit still had both `Requires=spirit-judge.service` and
  `After=spirit-judge.service`, so the judge failure correctly prevented the
  daemon from remaining active.
- **Stale filesystem state:** the main and meta Spirit socket nodes existed,
  but no matching listening Unix sockets were reported. The judge socket node
  was absent. Therefore the two existing nodes were not treated as availability
  witnesses.
- **Baseline failed units:** three pre-existing transient Ghostty scopes plus
  `spirit-judge.service`. These three scopes are the comparison set for the
  post-activation unrelated-failure regression check.
- **Missing witness:** the read-only Lojix node query returned an empty result at
  marker `(9 9)`. Post-state verification is gated on the approved executor's
  explicit report that the intended deployment is `Current`.

## Post-activation acceptance protocol

After the executor reports Lojix `Current`, independently verify:

1. the approved deployment identity and current slot;
2. absence of the obsolete judge drop-in and absence from effective
   `DropInPaths`;
3. effective judge and daemon commands come from the maintained Spirit service
   bundle, while `Requires` and `After` remain intact;
4. both services are `active/running` with successful results;
5. all three expected Unix sockets have live listeners;
6. deployed Spirit version/provenance matches the approved maintained inputs;
7. a bounded read and Marker operation are available without printing corpus
   bodies; and
8. no new obvious unrelated failed user units appeared relative to baseline.

Rollback conditions are any `Current` deployment with failed/inactive services,
a remaining obsolete drop-in, wrong service provenance, fewer than three live
listeners, unavailable read/Marker operations, or a new obvious unrelated
failed-unit regression. Any such condition is reported immediately to the root
and approved executor; this verifier does not execute rollback.

## Post-activation evidence

Observed independently beginning at `2026-08-03T19:05:01+02:00`, after the
approved executor explicitly opened the post-state gate:

- **Current:** the read-only Lojix generation query reported deployment `1`,
  generation `1`, `UserEnvironment`, `LiveActivation`, `Current`, exact
  immutable CriomOS revision
  `e658bf55bb0f06af012c8edf429d519c3b238c93`, and query marker `(19 19)`.
- **Wired and running:** `spirit-judge.service` and
  `spirit-daemon.service` were both `active/running`, result `success`, with
  zero main-process status. The daemon retained both
  `Requires=spirit-judge.service` and `After=spirit-judge.service`.
- **Migration effective:** the historical
  `spirit-judge.service.d/override.conf` was absent, and the judge's effective
  `DropInPaths` was empty. The daemon also had no drop-ins.
- **Maintained derivation provenance:** effective unit commands were the
  `spirit-judge-daemon-service` and `spirit-daemon-service` bundle wrappers.
  Their live processes resolved respectively to `spirit-judge-0.1.0` and
  `spirit-0.25.1`. Wrapper references contained the maintained judge,
  judge-config, provider, daemon, and generated daemon-configuration
  components. The deployed immutable flake graph locked Spirit to
  `eabe6c6d96112b46d15443e1c1a29d940605785f` and Home to
  `d2d02bb61eb3557594b2c302e2862e5e0f58fb86`.
- **Three live channels:** the process-aware Unix-socket query reported exactly
  three expected listeners: judge, working Spirit, and owner/meta Spirit. The
  judge process owned the judge listener; the daemon owned the working and
  meta listeners.
- **Bounded logical reads:** `Version` returned `0.25.1`; a read-only `Count`
  returned `24`; and `Marker` returned
  `(974 7784350440604474991)`. Count and Marker disclose no corpus bodies.
- **Marker preserved:** the executor supplied the private isolated-copy
  pre-activation witness `(974 7784350440604474991)`. The independently read
  live marker matched it exactly. This verifier did not open the private copy.
- **No failed-unit regression:** the post-state user failed-unit count was
  zero. The pre-existing failed judge and three transient Ghostty scopes were
  all absent from the failed set; no new unrelated failed user unit appeared.

## Conclusion

**Accepted.** Every requested runtime witness is observed rather than inferred:
the intended immutable deployment is Current, both services and all three
channels are live, the stale override is gone, the effective processes trace to
the maintained Spirit composition, bounded read/Marker operations work without
corpus bodies, the marker is preserved, and no obvious unrelated failed-unit
regression exists. No rollback condition was observed.

The verifier performed no activation, restart, stop, write request, corpus
inspection, restore, or rollback action.

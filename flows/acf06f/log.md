# Flow log

- Remembered: 4e296a — depth 1. Relevant facts: prior recovery kept microphone inactive; passive state was idle; the living later reported that recording continued after the status widget changed from red to gray and that `Meta+X` worked only while held. Prior flow did not witness recording, shortcut, or microphone behavior.
- Working instruction: implement the faulty-functionality fix and add visible microphone input feedback, drawing on the Listener widget's approach where appropriate.
- Provider landed: `wispr-flow-linux` main `033231a1255024447c6a4183c41f4ea9c1fa063f` publishes v2 heartbeat, truthful hands-free state, and sample-sequenced scalar microphone activity; independent exact-tip checks passed.
- Home candidate: `d9bec96c54146c59b83c6cefde7a58b77d44a9a4` adds the v2 Noctalia five-bar meter and passed implementation gates; independent landing review is pending.
- Deployment safety: prior Lojix deployment 190 partially advanced the Home profile but not the running Codex unit, and discarded actionable activation failure detail. `primary-cod` tracks that discovered defect. CriomOS `1523375b073eff4a6ff6c20bf4f81d804a389cc9` corrects the partial-activation procedure; this flow may realize but must not activate across the changed Codex unit.
- Landed consumers: CriomOS-home main `d9bec96c54146c59b83c6cefde7a58b77d44a9a4`; CriomOS main `f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`, including the corrected recovery procedure and ownership invariant.
- Realized: Lojix UserEnvironment deployment/generation 191 terminally succeeded at state marker 4993 from immutable CriomOS `f3d8b2ca3405bb81a0af7c2ac91fe84f6ac5e359`. No activation occurred; ledger Current remains 189.
- Remaining: `primary-vx3` carries continuity-independent activation and live non-private microphone/UI witness, blocked by `primary-cod` diagnostic retention.

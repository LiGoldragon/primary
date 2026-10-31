# Night upkeep — 2026-10-31

**Speech:** the running Wispr app is still `.11`; its shipped bundle lacks the recording-admission repair present in `.12`. Home's committed pin also predates that repair. This proves a deployment gap, not the cause of every failed dictation. The existing Field/Home route has the witness; no app was restarted and no activation was attempted. The recurring speech bug stays open.

**Other problems listed:** suspend battery drain and harness-written narration both have open bugs. The raw-record hunt also found recurring Zeus connectivity and communication latency complaints, without a current closure witness. Older Flow complaints are retained for tomorrow's design, with the cutover unchanged.

**Builds/code:** this machine already configures Prometheus as a substituter. Cache hits and per-crate rebuild isolation remain unwitnessed. A possible removal of duplicated Flow build policy was sent to Mind core Primary for judgment; its toolchain/filter differences need checking first. No speculative repair was added: **production code removed 0 / added 0**.

Evidence and exact outstanding issues: [upkeep-evidence.md](upkeep-evidence.md). Tracking: `primary-po9k`, speech `primary-swaf.1`, existing speech deployment `primary-bie3.6.3`.

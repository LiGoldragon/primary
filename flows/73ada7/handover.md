# 73ada7 handover — Psyche Secondary, topic Nexus and Message

## Role
Psyche Secondary for the Nexus topic: Message, the messaging Nexus, designed to use Flow. There is no Primary above this flow. It reports to Psyche Core Secondary 445410. Flow-side questions go to f5a6e9 (Flow Primary) through its secretary 9fed42. A Mind counterpart at the same layer may message directly about implementation. Field reaches this flow only through Mind.

## Governing state
- **Message design:** primary main commit `d9703b5210299bab596cc5d85ae4a84bc4ee32bc`, path `flows/73ada7/reports/build/message-design.md`, blob `7e4db1625f87abdd43003890b9f8c7beeaec6d30`. Readable copy: `flows/73ada7/reports/message-design-d9703b.md`.
- **Message Ethos drafts:** `flows/73ada7/reports/message-flow/` holds `message_library.ethos`, `message.signal.ethos`, `message.meta.signal.ethos`, `message.operation.ethos`, `message.memory.ethos` and `notes.md`. Each file passes ethos-zero Check on its own. They cannot be checked together, because ethos-zero cannot check across files. Their imports resolve only against signal-flow `a991c149` (Signal 12 leaf), not against Flow 0.25's published pins (signal-flow `068f0e`, meta-signal-flow `88f375`, flow `962ad12`). That is finding X5.
- **Flow design, f5a6e9's:** `flows/f5a6e9/reports/flow-buildable-design.md`; the newest commit seen is `439dc64b4`. f5a6e9's next publish drops the forgotten-Key text at lines 710–711; 9fed42 will send its revision.
- **Refusal map:** `flows/73ada7/reports/refusal-map.md`, Identify, Lock and Deliver against six Flow refusals. Of Astra's six, all are unreachable except NoLayer, which is reachable at Lock and at Deliver. A publish setting row 16 (Deliver × NoLayer) to reachable was in flight at handover; confirm it reached main.
- **message-test:** github `LiGoldragon/message-test` at `76ce7da88d15fb01f0537fe6a541cab3b2cbd2d4`.
  - Design pins: Flow design `9b006dd2`, blob `c443d8a87b9f41afecad2b55729cbc2f2b12bac6`; Message design `be5c2e5b`, blob `e3ea98727000a16981c5cdc28dd1a160b180305c`. Both are behind the governing designs.
  - Code pins: flow `962ad12`, message `6fa4d0c`, message-old `6fa4d0c`, nixpkgs `0e251e2`, blueprint `8be7524`.
  - The no-build evaluation passes. Every VM check stops at the first Configure.Model, because the pinned Flow 0.25 refuses the design's payload.
- **Reports:**
  - `reports/astra-runtime.md` — Astra's runtime questions.
  - `reports/trusted-origin.md` — the trusted-origin chain.
  - `reports/runner-packet.md` — the runner source packet for Field.
  - `reports/test25-merge-packet.md` — the test-25 merge packet.
  - `reports/audit-0004.md` — the shared-tree audit.
  - `reports/package/` — the context package: presentation guidance and missed context.

## Open items
- **Books before the living, awaiting rulings** (445410 tracks them in «Open books»). The meta-owner book and «Who works out where send up goes» are not watched by any session.
  - Who keeps a waiting request — https://claude.ai/artifact/CRAsUpx25thKrmy6JrF1TD
  - Which socket carries the lock — https://claude.ai/artifact/DGD77NWPCpHrw9kPNNdoqk
  - What happens to a refused send — https://claude.ai/artifact/UiE6ASxdjRDvySP7vW539w
  - Who works out where send up goes — https://claude.ai/artifact/UWSaBbYV8EGUA18u914utG
  - How Message learns who is calling — https://claude.ai/artifact/SAJ5X7ME6hRxKKRAW5BYwZ
  - Who may send besides a voice — https://claude.ai/artifact/87aZt1cq6Uy1rhJuk4aXsq
  - How a metaflow is named on the wire — https://claude.ai/artifact/JyL9DpeoJ3XqutJcXfpFko
  - How long Flow's lock lasts — https://claude.ai/artifact/WDiViWdyJaekjnrJRuZ2ni
  - What Message remembers of what it sent — https://claude.ai/artifact/ExCJJRtNkqp8Cp9BFaFmbh
  - When Field may answer Psyche — https://claude.ai/artifact/LKEK65nvAnTJNVnqs2cNGH
  - How Message's meta socket knows its owner — https://claude.ai/artifact/CQU2Mcpo89xibaGpPrfBEX
  - What the new Message does with the old store — https://claude.ai/artifact/HA9wcza7qh1r9gTYS1jvG3. The 2026-09-24 record rules out migration, but rests on "not even live yet".
- **message-test re-pin:** move it to Message `d9703b5` and to Flow's next commit (after `439dc64`). Heavy checks run on Prometheus once Mind publishes a Flow and a Message built to the designs.
- **Test 25, the Flow stand-in:** Mind's candidate is `13378c44`; Field merges it from `reports/test25-merge-packet.md`, then locks the signal-flow and signal inputs. It still needs a check file.
- **Test 24:** the reaped-peer test, written. Pid-reuse resistance rests on kernel source citations K1–K6 and has not been witnessed by a reuse test.
- **Stray file `v`:** remove it from the message-test tree once test 25 lands.
- **Skill variables:** the runner's 16 variables stay held. Field will add them once Flow's typed configuration read exists.
- **Proposed line for compensation-primary-commit,** owned by Field: "The independent clone's origin is the GitHub remote, never the shared working copy; run jj bookmark track main@origin after the first fetch, before jj git push --bookmark main."
- **Stray commits:** this flow's local commits in the shared checkout (`845a88`, `0b74bf`, `04ad8e5`, `c8d5ab`) are left for Field's reconciliation.

## Standing limits
- Publish only `flows/73ada7/`, from a full GitHub clone under the PrimaryPublish lock, held only for commit and push. Before each push, abort if any path outside the directory changes or main's file count drops. Never commit in the shared working copy.
- Every reported design commit carries its full 40-character commit hash, its full blob hash and a readable copy path.
- Heavy builds and tests run on Prometheus through Nix, against pushed revisions, with no local fallback.
- The harness's safety classifier refuses process-tracing helpers (the test-30 execve helper, the test-24 supervisor) and stopped the test-25 stand-in work. Report such a refusal once and never retry it in another form.
- The living's words travel only as psyche messages. Send only messages that require action, deliver an awaited result, or report a blocker.

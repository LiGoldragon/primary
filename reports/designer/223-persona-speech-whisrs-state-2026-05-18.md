# 223 — Persona speech / Whisrs state (2026-05-18)

*Topic compendium for the speech-to-text / persona-transcription /
Whisrs arc. Part of the 2026-05-18 workspace state-of-art series.
Master index lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

Whisrs is the current speech-to-text path on CriomOS (deployed via
`CriomOS-home/packages/whisrs`, branch `criomos` on
`LiGoldragon/whisrs`, OpenAI REST backend, JSON-over-Unix-socket IPC,
three-state daemon Idle/Recording/Transcribing). It is **memory-first
with a post-failure recovery spool**, not durable-first: the only
complete recording lives in a process `Vec<i16>` until stop; durability
only kicks in after the backend rejects upload. This shape produced the
2026-05-17 incident (14:14 recording, 27.3 MiB in-memory WAV, OpenAI
25 MiB rejection, ffmpeg stdin hang in `audio/recovery.rs`). Whisrs
also **violates the Persona component triad** (JSON IPC instead of
Signal; no typed artifact identity; no attempt ledger; no Signal
contract crate).

Research stance (second-system-assistant/1 and /2, both 2026-05-17):
keep Whisrs for CriomOS Niri/uinput/Nix fit but redesign around a
durable `RecordingSession` object; when this lands in Persona, build
**`persona-transcription` first** as a triad (daemon + thin CLI +
`signal-persona-transcription`); keep TTS as a future
`persona-speech-synthesis` / `persona-utterance` component; reserve the
broader `persona-speech` for a true full-duplex coordinator only if
earned. Audio bytes are an explicit data-plane carve-out from Signal
frames.

**No implementation has started.** A short-lived Opus-encoding
experiment was rolled back to `f4531fe6` on 2026-05-17 18:15 after a
live ffmpeg deadlock; production runs the pre-Opus generation.

---

## 2 · Load-bearing reports

| Path | Carries |
|---|---|
| `reports/second-system-assistant/1-whisrs-durable-first-stt-research-2026-05-17.md` | Current Whisrs analysis + durable-first redesign sketch (CriomOS wiring, Whisrs internals, external comparisons, recommended shape, immediate work order). |
| `reports/second-system-assistant/2-persona-speech-component-brainstorm-2026-05-17.md` | Canonical component-shape proposal (`persona-transcription` / `persona-speech-synthesis` / `persona-speech`). Needs user decision before retiring. |

Both stay until the seven open questions resolve.

---

## 3 · Open user decisions (sec-SA/2 §"Open Questions For The User")

All seven block implementation start.

1. **First product surface**: dictation into the active desktop, or Persona-native voice input to agents? (Decides whether clipboard/typing or transcript-events/message-submission is the integration path.)
2. **Raw recorded human audio retention**: retain by default, or only until transcript acceptance? (Retention policy for the durable-first invariant.)
3. **Generated Persona speech retention**: retain as durable artifacts, or regenerate from text/settings?
4. **Full-duplex conversation**: first-version requirement or future requirement? (Decides whether a speech coordinator / shared device policy is needed day one.)
5. **Echo cancellation and barge-in ownership**: `persona-speech` (local audio policy) or harness/router (conversation policy)?
6. **Local-first vs cloud-normal**: transcription/synthesis mandatory local-first with cloud as opt-in, or cloud-normal for quality? (Affects Nix closures, model packaging, secrets, latency, cost.)
7. **Typed transcript target**: message recipient, mind thought, active desktop insertion, or all three as explicit modes? (Must be typed, not inferred from focus.)

---

## 4 · Beads state

| Bead | Priority | Status | Title | Notes |
|---|---|---|---|---|
| `primary-51pn` | **P0** | OPEN | Whisrs: service restart while recording drops in-memory audio | Mitigation patch landed and **rolled back on 2026-05-17 18:15**; live Whisrs is back to pre-mitigation generation. Bug remains open for durable-first / shutdown-safe handling. **Live on the user's machine.** |
| `primary-6m8u` | P1 | OPEN | Whisrs: encode dictation as Opus before transcription upload | Patch landed but **rolled back same day** after live ffmpeg deadlock on a ~93s recording. Experimental work preserved on `whisrs-opus-sandbox` (commit `cb87fe83`). |
| `primary-kyhs` | P1 | OPEN | Whisrs: close ffmpeg stdin before recovery spool wait | Narrow encoder deadlock; root cause visible at `whisrs/src/audio/recovery.rs:162`. Fix sketched but not landed. **Independent of the architecture**; could land without resolving the seven open questions. |
| `primary-ipjx` | P1 | OPEN epic | Rethink speech-to-text recording as durable-first infrastructure | Architectural parent of the three above. Both second-SA reports linked in bead's NOTES. **Blocked on the seven user decisions.** |

---

## 5 · Implementation state

**None.** All deliverables are research. Two short implementation
passes (shutdown-spool guard for primary-51pn; Opus upload for
primary-6m8u) landed and were **rolled back the same day** (2026-05-17
18:15). Production runs the pre-mitigation Whisrs generation
(`LiGoldragon/whisrs` `criomos` @ `f4531fe6`; CriomOS-home main @
`eb1ca6f6`). The mitigation work survives only on the
`whisrs-opus-sandbox` branch. No `persona-transcription` crate,
daemon, CLI, or Signal contract exists. The P0 bug `primary-51pn` is
live on the user's machine.

---

## 6 · Recommendations for context maintenance

- **Keep both second-SA reports as-is** until the seven user decisions land. They are the only durable record of the durable-first analysis and the component-shape proposal; retiring before decision would force re-research.
- **Beads need user attention, not just sweeping**:
  - `primary-51pn` is **P0 and live** — needs either re-applied mitigation or a deliberate "accept the risk" decision.
  - The seven open questions in sec-SA/2 should be resolved (or marked deferred with reason) so `primary-ipjx` can move from epic-as-research to scoped work.
  - `primary-kyhs` is a narrow bug independent of architecture; could be landed without resolving the seven questions.
- **Do not retire** any of the four beads on a routine sweep — every one is open, P0/P1, and tied to live audio reliability.
- When `persona-transcription` design starts, sec-SA/2's contract sketch (§"Contract Sketch") and recommended shape (§"First slice: `persona-transcription`") are the seeds; both should be quoted into the new `persona-transcription/ARCHITECTURE.md` rather than re-derived.
- `/git/github.com/LiGoldragon/whisrs` is on branch `criomos` @ `f4531fe6` (production-aligned); no `AGENTS.md`/`ARCHITECTURE.md` in the repo, so CriomOS-home's `skills.md` is the effective local contract per sec-SA/1.

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master.
- `reports/designer/217-component-triad-mutate-authority-state-2026-05-18.md` — adjacent: `persona-transcription` will be a fresh triad implementation; data-plane carve-out (audio bytes) is the relevant invariant.

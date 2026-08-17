# First prompt: agent — bring Spirit back online; intent becomes spirit

You are a fresh agent working with the psyche on the Spirit system. Two
missions, one bead: **primary-7z3**.

## Mission 1: revive Spirit

The spirit daemon has been down since 2026-07-24. The operating system is
declarative: system source is `/git/github.com/LiGoldragon/CriomOS`, user
environment `/git/github.com/LiGoldragon/CriomOS-home`. Diagnose why the
daemon is down and bring it back through the declarative sources (never
overlay managed environments with unmanaged state — that law is absolute).

Then replay the offline queue `spiritbackup.nota` in the primary workspace:
one PendingCapture is queued (2026-08-01) with capture wording the psyche
approved verbatim. Verify the Operation envelope against the live spirit
CLI schema before replay — the queuing agent guessed the envelope shape and
said so in the file's comments. Adjust the envelope if the schema differs;
never alter the quoted capture text. On acceptance, mark the entry Sent with
the returned id per the file's replay procedure.

## Mission 2: the vocabulary port — intent becomes spirit

Psyche ruling 2026-08-01
(`design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md`, rulings
1-2): everything that touches Spirit and was called "intent" is renamed
**spirit**. What Spirit contains is spirit — the computer representation of
the psyche's spirit, a living thing agents never access directly and can
only infer, as with vision. The rename deliberately frees the word "intent"
for later reintroduction with its ordinary meaning (intention, what the
psyche wants), which is distinct from spirit and must not be conflated
again.

Surfaces to port, each through its owning source:

- The workspace `AGENTS.md` Intent section (propose new wording to the
  psyche first).
- The intent-log skill and any other skill naming "intent" in the Spirit
  sense — sources live in LiGoldragon/Curriculum; every skill edit is
  approval-gated through the psyche; never edit generated copies under
  .agents/, .claude/, .codex/, .pi/.
- Spirit-operation documentation and the spirit daemon's own vocabulary if
  it surfaces the word.

Do not mass-rename mechanically: at each occurrence judge whether the word
meant Spirit-content (rename to spirit) or ordinary intention (leave for
the psyche's future reintroduction). Bring ambiguous cases to the psyche.

## Also worth raising with the psyche

Agents have not been consulting Spirit ("it's sort of fallen by the
wayside" — his words). Once it is back online and renamed, propose how
agents should consult it in ordinary work, as a small concrete design, for
his review.

## Context sources

The current management session
`~/.claude/projects/-home-li-primary/0f9d1436-0f9a-4cb0-9c08-60027d8cbc6e.jsonl`
(his verbatim words on spirit vs intent and the correctness capture),
`design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md`,
`spiritbackup.nota`, and `AGENTS.md`.

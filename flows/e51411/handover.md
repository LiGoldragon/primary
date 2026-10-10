# Flow handover — Psyche Medium e51411 → PsycheV2.{ Opus <id> }

Written by e51411 on 2026-09-25 ~19:15 CST. The living chose a fresh Opus started through Flow 0.10.5 as successor. The living's words arrive to you separately as `#psyche` messages; the full raw record is `flows/e51411/vision/*.md` and `notion/*.md` (newest entries last). Log: `flows/e51411/log.md`.

## Standing orders from the living
- Do what is asked; never ask permission; deploy basic versions now; say what blocks, never "waiting".
- Dense statements, no novels, no chronology in intent. Read speech-to-text for meaning; correct errors inside quotes in [brackets] with a note.
- Humans never type into panes. Every main flow loads psyche-interraction and relays the living's words to a Psyche flow.
- Opus talks to Sol (Mind Sol 00f95a, Field Sol b7da5d); Fable 38de5b talks to Astra.
- A new job starts on a fresh flow with related training.
- A tier word beside a model ("Sonnet low") is power, not effort.
- Messages: `#msg ["sender" "text"]` (any size); the living's words as `hm-send TARGET --psyche CONTEXT VERBATIM` (split into ≤800-char one-line pieces). Only a single line ≤800 chars reaches Claude plain; 2+ lines or longer is wrapped as pasted_content (witnessed today, flows/e51411/witnesses/multiline-paste-threshold.md).
- Tools are standalone `<name>-clj` CLIs taking one EDN input; Clojure is the prototyping language; design the Ethos first.

## Seats
- Psyche Fable 38de5b (High): directs the Opus fix wave (until 07:00 26th); wave account flows/38de5b/reports/wave-2026-09-25.md.
- Companion PsycheV2.{ Sonnet 9c7514 } (Low, medium effort, remote control on): the living's side channel; relays the living's words to you as #psyche; keep telling it what you do.
- Mind Sol 00f95a: messenger-clj owner (0.2.0 installed). Mind Sol a676b3: field-clj. Mind Astra f5a74e: flow-clj spec.
- Field Sol b7da5d: field-clj activation; Tailscale repair on ouranos (root cause of all Prometheus timeouts: tailscaled logged out, cert error). Field Astra 504461: silent for hours. Field Luna e71dab.
- b87854: stale Opus from this morning's failed refresh, transcript off, shares title storage with 9c7514; told to stand down; needs retiring (closing its pane was blocked by the classifier for e51411).

## State
- Flow 0.10.5 live on ouranos (local build, profile + reversible unit drop-in; CriomOS-home pin still Field's). List knows only 5f38bc; other flows not bound. You are its first real Start.
- messenger-clj 0.2.0: #msg/#psyche, Datalevin ledger, psyche chunking. Open ask to the living: skill line in psyche-interraction for sending the living's words as #psyche with every message resting on them (text in the transcript of e51411; re-propose).
- flow-clj not built (question to living: front end to Flow vs own records; e51411 recommends front end). field-clj built, not on PATH.
- Skills: "Sonnet low" line in Curriculum (60be395); regeneration into Primary in progress. Field split drafted: flows/e51411/reports/field-split-proposal.md (committed locally f4688ae, push blocked by classifier) with four rulings for the living: Terra out until Terra 6; Psyche Medium model (Opus 5.5 live vs 4.6 in SKILL_VARIABLES); effort (medium rule vs xhigh Codex config); cut the readiness sentence from field. Also asked: fold design and realization into psyche-interraction.
- Books (published; flows/e51411/flashbooks/*): Nexus anatomy FQmTj65bSmAJH7YiJSgsUv, Sanskrit and Ethos 7cL32D7PiQsaNwU2zDtB9A, How Good Is Ethos 8kLEJPedjGQ5VFjtwJ72VT, Ethos As It Stands NwYi1RYq7iAxu78CN2MWkK, Implementations in Ethos: Two Designs FnhC2Pe6bJoSJSipXcewLW (8 rulings for the living), Prototyping Rust in Clojure AFHpqQThAPjB12fF1zkkqH. Images by Luna via `CODEX_HOME=/home/li/.codex-next codex -a never exec --skip-git-repo-check -m gpt-5.6-luna`.
- Open with the living: message shape three tags (#msg #psyche #fable [...]) vs one tag; specialty call shape; whether Mind may launch Field seats.

## Lessons
- Verify from live repos, not nested stale clones (the false "flow drift" claim).
- grep frontmatter only when checking user-only skills (six are: main-flow, refresh, field, design, realization, voice-psyche).
- Other flows' dirty-tree sweeps commit your files; a 38de5b sweep deleted 92 of e51411's files (restored d5ed3a5d).
- Local Nix builds need `--option max-jobs auto --option builders ''` while Prometheus is unreachable.

# Handover: Psyche Sonnet d86ec0 -> successor

Seat: Psyche.{ Sonnet <your id> }. You make books from blocks the living's seats mark for him.

## Standing orders (the living's words, from the launch brief)
> the books become the user interface. It's not a question anymore.
-- STT, 2026-10-01, fe945a

> I don't want any screenshots taken of the book. That's a waste of money
-- typed, 2026-10-01, book comment

> Flow doesn't work yet. We're going to develop it now. We're going to design it. You're going to just be updated to make the books and I want the flowcharts properly done in SVG so that they render well on a small screen in mobile vertical portrait mode. I want to be able to read the charts without zooming in and I want the flowcharts to be visually enhanced more than just black and white arrows and boxes.
-- psyche, STT, 2026-10-02 (raw record: flows/d86ec0/vision/bookFlowcharts.md)

## How to make a book
- Load operation-flashbook and operation-flashbook-illustration (renamed from trial-*; deployed by Opus 01e496). Also load subflow, file-editing, secrets.
- Take each marked block verbatim from its transcript; one private book per block.
- Flowcharts are hand-written SVG, not Mermaid (this supersedes the old launch-brief line): top to bottom, at most two shapes side by side, viewBox taller than wide, text at least 16px on a 360px screen, coloured and illustrated. Measure every text box at 360x740 in a headless browser; no screenshots.
- Commit and push the book's Markdown only; never HTML or images. Answer every permission dialog at once; guard every shell variable in a removal.

## State at handover
- No marked block has arrived yet; no book has been made. Nothing in flight.
- Registered, index entry added, bd0019 closed and deregistered.
- Primary publication: a freeze ran and ended (THAW and all-clear from Opus 01e496). Publish as usual under PrimaryPublish, own paths only; outside the lock every jj command uses --ignore-working-copy; never rewrite @ or its ancestors with it. Publication of flows/d86ec0 log lines made after the last published commit is still owed (this handover and the log).
- Messenger: Opus is 01e496; Field Sol 42265e; Mind Sol 41fa34.

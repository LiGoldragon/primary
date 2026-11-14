# Handover, flow 643abe (Psyche book Haiku)

Role: publishes books and presentations ordered by Psyche core Fable, Psyche core Opus and Mind flowNexus Opus. Checks each source with the book checker, builds it with the book builder, draws its figures through Illustrator, publishes with Artifact, and sends the title and link back.

## Open-books record

`/home/li/primary/flows/book/open-books.datom`: 19 rows, Watched and Unwatched. The Watched rows are the books whose comments go to Psyche core Fable. The successor must check the live watch listing first, since watches end on the cap and when this session stops.

## Watches

The session holds at most 10 artifact watches. Watches end when displaced by a newer watch, or when stopped. A publish arms auto-replies only when the page's link came from this session's own publish, so a page published by someone else needs its own republish to get comments. Stopping a watch leaves its auto-replies stopped; a publish does not re-arm them.

## Flow messaging

The `flow` CLI on this machine could not reach the Flow Nexus at the end of this session ("No such file or directory"). Replies were typed into the recipient pane through herdr, after checking the pane's session. Panes move: look up the session with `herdr agent list` before each send.

## Standing rules

- Figures: each Mermaid fence becomes `fig-N.svg`, drawn by the Illustrator agent. Redraw whenever the fence text changes (`fig-N.mmd`).
- Source form: a bare `+` line becomes a blank line; a nested fence inside a markdown fence uses four backticks.
- Account and Review sources need a `Presentation.{ «title» Account }` line; a scratch copy takes it, the flow's file stays as made.
- Never change proposed wording; a source whose content is wrong goes back to its author.

## Open at handover

- Watches were ended for the reboot (see the order this handover answers). Re-arm the Watched rows by republishing from their sources, or by `watch` with the url if the living asks.
- Two books were displaced from the cap during the session: the implementing-flow page and the Signal page. The record reflects this.
- Comment threads on "Nothing is built twice" stay open and not activated for Claude; a writer must send them to Claude.

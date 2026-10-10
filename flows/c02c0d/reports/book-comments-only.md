# The page works by comments only: sentences to replace

Ruling of the living, record c02c0d-1 in this flow's vision/presentation.md: the pages carry no buttons and no note fields; the living comments, and nothing else.

Done on 2026-09-28 by a subflow of c02c0d: the standing page was republished without any control that writes; the explanation page was corrected. No row was changed.

Witnessed by that subflow: no write from the page ever landed in the database. The rows that carry answers were written by the page's sub-agent from the living's comments. A flow can read the living's comment threads; it cannot reply to or resolve one, since none is activated for Claude.

What follows was found by reading and is proposed, not landed.

## subagents/book.md

| Present sentence | Replace with |
|---|---|
| `options` (list of short strings, the real choices, each a button) | ... each shown as plain text |
| `answer` (`null`, or `{option, note}` written by the page ...) and both `answeredAt` (written by the page) | written by you from the living's comments |
| `approvedAs` (a kind, set by the page when the living said ...) | set by you when the living's comment says ... |
| `pageReadAt` (ISO time of your last read of the page's answers and comments) | ... of the page's comments |
| An answered `waiting` row stays ... | A `waiting` row you answered from a comment stays ... |
| Never write `answer`, `answeredAt` or `approvedAs` except to clear them ... | Write them only from the living's comments; never invent them. |
| A pinned write that fails means the living changed that row while you worked | ... means another seat changed that row; the living changes no row. |
| what the living answered or commented on the page | what the living commented on the page |

## flows/8904b1/specs/book.md

| Present sentence | Replace with |
|---|---|
| Changed: the living's note is the correction | the living's comment is the correction |
| after the type `Answer.[ None Chosen.{ Option Note } ]` | add: An Answer is written by the Book from the living's comment; the page carries no controls. |
| what the living answered on the page since last time | what the living commented on the page since last time |

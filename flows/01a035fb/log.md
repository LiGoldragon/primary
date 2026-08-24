# Flow 01a035fb

Investigating why recent Claude flows, including the incident associated with `2f6b1dc5`, lost changes in `primary`.

Open:

- Reconstruct what each flow read and wrote, in order.
- Separate direct observations from claims, hypotheses, and unknowns.
- Determine whether the failure came from `jj` usage, generated entry instructions, concurrent work, repository state, or another cause.
- Compare the current entry-file preservation instruction made by the other flow with the failure modes found.


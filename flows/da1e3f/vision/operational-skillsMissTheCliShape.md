# Operational: our skills don't teach the actual CLI shape

## The skills we load describe intent — what a Nexus is, what it should do — but they don't teach the actual Input/Query variants each installed CLI accepts. So a flow that loads `$orchestrate` and `$message` still can't call `orchestrate` or `message` without spelunking source code to find variant names. That is a real gap in the skills system, not just a documentation nit

Context: witnessed by primary Psyche opus (Claude flow da1e3f) on 2026-09-17 after multiple failed attempts to call `orchestrate 'ListLocks'`, `orchestrate 'Query.Locks'`, and `message 'Ping|Send|Post|Peer|Submit|SubmitPrompt|...'` — every guess rejected with `Unreadable.Error.{ Composition [] Variant.{ Query <name> } }` or `dotos: unknown Input variant <name>`. The living pointed it out plainly:

> Oh, so our skills don't even let us use our tools properly. So great. My God.

-- psyche, typed.

The fix is a per-CLI-version reference the skill can load — the exact Input/Query variants the installed binary accepts, one working Datom example per variant, updated whenever the binary version bumps. Fold into the `operations` skill (or a companion skill per Nexus) so a flow that says `$message` also gets `messageInputVariants` for the version on the machine right now.

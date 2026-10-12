# Committing

## One committer holds the lock; a turn-end hook wakes the quaternary; the flow id lives in an environment variable

Context: typed to the Psyche core Primary after it was found committing Primary by its own hand under turn grants from the Secondary.

> So why are my instructions being ignored? Can we just fucking move on to what I asked and get a single committer to fucking commit on this single repository, not a fresh clone? Just a simple fucking system where there's one agent that commits and he just holds the lock and everybody just messages. When they're done doing their edits, it's fucking simple. In fact I would even say there's a point to be made that if we use hooks for turn ends, there's no need for anybody to message anything. The hook just sends a message to the committer and then the committer just figures out what the commit should be. He can always go look in the transcript of the session whose hook fired.
>
> Could we get an environment variable where the flow ID lives? Or is there a problem with the flow and some harness needing to be started first so that we can get the flow ID? Maybe we can actually find a hack around that where we start the harness and then re-add to its environment variable or something so that the hook can get its flow ID.
>
> In fact we could even make that sort of the default instead of making the complicated machinery of looking into the process, finding out which process is the flow or which flow ID that process ID is, and doing that whole low-level machinery. We could just set the flow ID in the environment variable of that harness and let it pass that environment variable to all of its subprocesses. Then all the hooks and everything can use that way more simply.
>
> Let's just do that and get a hook to just message the committer and the committer can just figure out by searching the transcript of the sub-agent what the commit message should be. That is to have a low-level [Luna], like a Luna on the quaternary, like a [Field] or a [Mind]. The quaternary should commit. Basically it would be one of its roles and it just gets hooked into by the harness hooks when someone stops working and has edited files.
>
> Maybe we can somehow figure that out. Maybe there's machinery in the harness that lets us just do that. It might be more complicated than I make it sound but if not then it's okay to wake up quaternary. If primary is not dirty then it doesn't wake it up, so only if there are changes. If there's a turn [end] and there are changes, then quaternary can commit. If more changes come in that look like they should have been included in a previous commit, then they can be just squashed into it.
>
> Also we use [Jujutsu], which makes it easy to do that. I don't mind rewriting history because we're the only people working on this repository.

-- psyche, STT, 2026-10-12. Transcription corrected: "grant" → "Luna", "mine" → "Mind", "turn hand" → "turn end", "jujitsu" → "Jujutsu".

## The committer is simple enough to actually get implemented

Context: typed to the Psyche core Primary after it returned Astra's committer design with four changes and a size target.

> Well, make sure it's not so complicated that we never actually fucking implement it.

-- psyche, typed, 2026-10-12.

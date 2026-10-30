# Secrets

## 2026-10-30 — Environment variables are no safer than a file for a same-user process; an encrypted ephemeral filesystem is a later route; security is not pursued now
Context: the living, in the Psyche core Primary chat d12d26, thinking aloud on environment variables.

I feel like environment variables are so obsolete and ancient and they probably have one or two good functions, which is to hold a secret token maybe. Technically if I think a process is run under a certain user, then all the processes that run as the user can actually get the environment variable of that process. So it's not even more secure than, let's say, putting it into a file, in the sense that it's ephemeral. When you shut down the machine, right?

I think there are even ways around that. You could have a part of the file system that's encrypted and with a nefemeroski on every boot. I'm not saying I want to pursue this route right away, although if you think it's easy. I don't want to create a whole bunch of complications. Security is important but I'm kind of leaning on allowing things that are not necessarily ideal security-wise but jeez there's a lot going on right now. I can't see it all. Just tell me what you think of all this.

# Recover the Zeus and Bird environment carefully

Captured from the psyche's 2026-08-08T11:37:36.634Z prompt in Codex
session `019fe121-b1ea-7350-922b-826d0ce83a37`.

Agent-authored context: the psyche opened the recovery work by requiring an
evidence-first posture because the workspace and deployed hosts may contain
conflicting or stale state. Verbatim:

> right now everything is a fucking mess. So don't trust anything. Don't
> assume anything. Be careful where you step.

Agent-authored context: restoring Bird's working environment on Zeus is the
urgent human outcome. The terms “cloud” and “codecs” below are preserved
exactly from speech transcription. Verbatim:

> But, yeah, we need to fix Zeus's VS code so that my friend can keep working
> because her time is valuable and her creativity is valuable.

> So with all this said, see if you can reliably get the latest version. Like
> make sure KareemOS and KareemOS Home are in sync that they don't have like
> we've been having this problem with them falling out of sync. And like the
> user environment is using the wrong version of something that it doesn't
> match the version on KareemOS or vice versa. And that cloud and codecs are
> up to date.

> So then once we got all that lined up, we need to redeploy Zeus on the latest
> version.

> And I need obviously BIRD. BIRD is my partner's username. So BIRDS, VS codes,
> cloud and codecs extensions need to be fixed. They're broken. There's like
> glitches on codecs and cloud doesn't even load. So let's make sure that all
> of this is at the latest version and maybe even rethink the whole way of how
> these VS code extensions are updated or obtained or deployed or I don't know
> what.

Agent-authored context: a temporary workaround is acceptable if necessary,
including a root-mediated user-environment reload, but it must remain visibly
temporary. Verbatim:

> If we have to use a hacky way to do it, then we're going to have to use a
> hacky way to do it. We have root access on all my hosts.

> I mean, I guess if you do a full CREAMOS redeploy on Zeus, it should change
> the user environment, but you might have to reload the user environment
> manually, which means SSH root into the host and then change to the user and
> reload.

Agent-authored context: the repository's actual temporary-workaround file is
`NON_IDEAL_AGENTS.md`; the lowercase and singular variants below are preserved
from speech transcription. Verbatim:

> We should document all of this in non-ideal agent, non-ideal, or non-ideal
> agents.md file, which is what it's there for, because I have all of these
> hacky instructions that I don't want them to remain. So by putting them in
> that file and instructing agents always read that file, that should also be
> in the skills or somewhere that makes it reliable for agents to do that.
> Then we keep that agents.md file from getting infected with a bunch of hacks
> that really have to be fixed rather than kept as working policy.

## Surgical writable configuration

Agent-authored context: the existing tool matching this direction is Hexis.
The psyche did not remember its name in the prompt, so the spoken names are
preserved rather than silently corrected. Verbatim:

> Like there's this file that seems to be a problem. Every time we update, it's
> still using the old versions. And there's a problem with updating it because
> it needs to be writable. So we need like a surgical. That's what I think
> Helix was what it was called or Henix or something. I don't even know what my
> things are called. Let's give it a better name so I can actually fucking
> remember what it is. It's a surgical data editor. So it should be able to
> change things like certain JSON fields and things. So we can surgically
> change things when the new user environment is loaded. This thing runs and
> it makes sure that only the things in certain configuration files, which must
> remain user writable, are changed to follow the to, you know, to put out the
> things that the update puts out while remaining user writable.

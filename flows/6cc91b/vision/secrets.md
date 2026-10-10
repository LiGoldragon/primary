# Secrets

## 2026-09-14 — Secrets remotely loaded into the process, never stored on the host; a Creo-based decision to allow access

Context: comment on the "vision or notion?" card about the Prometheus sandbox and the throwaway key. Rules it: neither as filed; this is what was meant. "Creo" is left as the living wrote it here; the same day they ruled the spelling criome.

> No, we're going to have a system that really securely handles those secrets, so they can be deployed to boxes or nodes that don't need to store them. They're just remotely loaded into the process in a secure way so that if the host is shut down, it loses access. It never really sees anything other than the process that needs those tokens. That's what I meant.
>
> That could be part of the cryptographic component that I was talking about. It can send secrets, obviously, because it's encrypting the communication. It could have that feature too, where it can send a secret to a particular service on another host. These requests could come in when the host starts and needs to open something or get access. It would come in as a notification, potentially all the way through the interface, which, for now, is your process, basically your user interface. This remote cloud will become the Unity app, and you'll get notified that something needs to get access.
>
> It'll be a Creo-based decision to allow the access. Whatever node holds secrets in the cluster, the trusted secret holder (there could be more than one), is going to be able to send that signal for the service on that node to get access to get that secret loaded into the process. It would use, like I said, throwaway memory salt in the process itself so that there's nothing to recover. The computer shuts down, and nothing is stored locally. It's only the process that has it while it's running, and it's going to be sandboxed in a way that other processes can't read its environment variable, obviously.

-- psyche, typed, artifact comment.

# Domains

## The domain is criome, criome.net on the public web; the domain part of the configuration is abstracted so anyone can fork the repository or add their own; a federation of cluster-controlled domains getting DNS from each other; the web firewalled by default except some XMPP domains, per cluster; xmpp.goldragon.criome internally, .net for public access

Context: typed by the living on 2026-09-16 as a comment on the Decisions Board artifact, anchored to the row asking for the XMPP domain name. "golddragon" is a transcription of goldragon, the cluster's name; corrected in the quote. Logged by the main flow before acting.

> The XMPP domain: we have the criome, right? Internally, criome OS is represented on the public web by criome.net right now. We're going to abstract out that part of the configuration so anyone can grab the repository and fork it, or potentially even add their own. There's a federation of different domains that are controlled by these clusters. Essentially, we're going to get DNS from each other, right?
>
> If you want to have the public presence, you can use a Cloudflare cache if you want, of course, but for stuff like XMPP, you're going to decide if you want a firewall. I would probably firewall all of the web by default, except for some XMPP domains, and it would be per cluster. It would be like xmpp.goldragon.criome internally. You could do that, but for public access, you put .net.

-- psyche, typed.

# Live installation image

## A USB disk for installing

> I would like to develop a different kind of node for creating a USB disk for installing, which would also hold the allowed SSH keys, maybe SOPs, and an encrypted default login non-root password. That one is just for manually opening the terminal, so it wouldn't have any graphical user interface. It would just be TTY and very minimal so that it's fast to build the image.

-- psyche, STT.

## Review what they are

> We would only use tools that we could potentially revise. There are probably too many tools in the environment by default. These have just accumulated through the years, and I never really took the time to sort them out, maybe organize them better, and figure out how to comment each of these tools, at least so that I can review what they are. Maybe we could categorize them by broad category of what they are, or by how big they are, what stack they use, or something like that.

-- psyche, STT.

## Deterministically named and added on to the cluster synthetically

> It would be a node that is deterministically named and added on to the cluster synthetically, so it's not in the cluster data itself. When the horizon is rendered, it appears there and has this name that would never really be a problem, like x86464 minimal live image, live installation image, or something like it. It doesn't even have to be a short name, just be winded. You could also have different versions, like the minimal and full graphical, etc.

-- psyche, STT.

## An external additional input to Lojix

Transcription correction: the living explicitly corrected “logics” to “lojix”. Capitalization follows the repository name. “RiomoS” elsewhere in the originating request was likewise corrected to “criomos”.

> I'm not sure where the additional node would come from, but I don't want to hardcode this into Lojix or anything. It would come in as an external additional input to Lojix that defines the default nodes for any cluster, so that it's maybe just merged, and then we would add this node type.

-- psyche, STT.

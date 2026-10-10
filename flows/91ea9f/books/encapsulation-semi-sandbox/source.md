`Presentation.{ «The encapsulation component and the semi-sandbox» }`

## 1. What the component is, from your words

Not the harness. The harness is the vendor's program (Claude Code, Codex) and our typed abstraction over it — a repository already named `harness`, built, not running. The thing you want named is what you described on 13–14 September:

> "Establish a coherent system here where you're going to figure out a way to start a new process, maybe with this harness component that you need to describe anatomically well. ... Just start a full sandbox. ... Can we copy the token into another host so that my codex and Claude log in? ... with only the process that needs the token having it."

-- STT, 2026-09-13, 024bc7

> "a light sandbox, which is basically a sandbox of my home environment, and it can reuse my login, but with a different user environment. Container for the codex, the code, or whatever harness we decide on."

-- STT, 2026-09-14, 6cc91b

> "It would involve one of our components, which takes care of containerization, which is what Nix does: it creates a container."

-- typed, 2026-09-14, 6cc91b

My reading of its anatomy: it makes the enclosure a seat runs in — the home and user environment, the sandbox boundary, and the credentials that reach only that process. Flow decides *that* a seat starts and with what prompt; this component makes *where* it runs. It does not run the model process and it is not security (you said on 24 September security is further down).

## 2. The name

You asked me. **Capsule.** Encapsulation yields a capsule; a seat runs inside one; it is one word, a noun, and fits the Nexus naming (`capsule-nexus`, `capsule`, `capsule-meta`). The close second is **Habitat**: it says home environment and login reuse more strongly, but less the boundary. I'd avoid Enclave and Sandbox: Enclave claims a trust boundary you have put further down, and a sandbox is only one thing a capsule can be.

## 3. Faster testing: the semi-sandbox is already ruled, and it is the first Capsule

On 26 September you ruled it:

> "Just set up a persona test repo where we'll run different kinds of sandboxes. One of them will be this semi-sandbox that allows the credentials to be moved over and used and uses lightweight cheap models to test different scenarios"

> "I think the best would be to copy the login credentials and then generate all the configuration details that work for our test sandbox."

-- STT, 2026-09-26, e167d8

State today: the persona-test repository exists with one runner (Flow + Herdr + Message), but that runner copies no credentials — it demands an already-isolated Codex home from whoever calls it. The credential-moving part is the piece never built, so every test still rides the full deployment (push, bump the pin, remote build, activate through Lojix, rotate stable and Next).

The fork on credentials, and my proposal:
- **(a) Copy the login files into a throwaway home at run time**, generate the rest, cheapest model only, remove on exit. This is exactly your 26 September ruling; it is small and lands now. *My proposal.*
- **(b) The volatile-key design** from 14 September (loaded remotely into the process, unreadable by other processes, lost on shutdown). The end shape, but it is the security layer you put further down.

If (a), the join with point 2 is that this runner is the first embodiment of Capsule, and Capsule grows from it rather than being designed on paper first.

## 4. For your word
- Capsule, Habitat, or another name?
- Credentials route (a) now, with (b) as the later shape?
- Where did the "harness" discussion with Opus happen? If it was spoken and never logged, say so and I'll log what you tell me now.

Eight rulings 6997eb presented to you were never answered; they wait for the next presentation so this one stays small.

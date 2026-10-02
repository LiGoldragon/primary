# The encapsulation component and the semi-sandbox: context

## Summary

**The component's job.** No transcript records the discussion with fe945a where "harness" was the tentative name. fe945a's transcript has no typed or spoken word from the living on it, and neither do 6997eb, bd0019, 01e496 or the Codex sessions since 10-01. So fe945a never described it, and the nearest psyche comes from 13 and 14 September. There he asks for "this harness component that you need to describe anatomically well", which starts a seat's process in a sandbox and holds its token. He also calls a flow "a composition, which we call a harness today", with a "container for the harness" that reuses his login under a different user environment. This is my reading, not confirmed: the component wraps a seat. It holds the seat's environment, the sandbox around it, and the credentials that reach it. It does not run the model process itself.

**The existing "harness".** It is `/git/github.com/LiGoldragon/harness`, the "Typed harness abstraction for Persona": identity, lifecycle, transcript events and adapters for Codex, Claude and Pi, with the `harness`, `meta-harness` and `harness-daemon` binaries and the `flow-id` helper. It is pinned in CriomOS-home (harness-0.3.4 is on the Flow service's PATH), but its daemon is not running.

**Sandbox state.**
- `persona-test` is the only Persona `<repo>-test` repository, with one pure check and one semi-sandbox runner, `message-flow` (Flow 0.17.4 + Herdr + Message, last commit c1a2370, 2026-09-27).
- That runner copies no credentials. It requires an already-isolated Codex executable, home and socket from its caller. So "how my credentials move into the sandbox" is still unsolved, though he ruled the method on 09-26: copy only the login credentials, generate the rest.
- `compensation-nix` already prescribes what he asked for: a `nix run .#<scenario>` runner with a fresh `mktemp -d` root, credentials copied at run time, the cheapest model (Haiku or Luna), and removal on exit. No runner yet does the credential-copying part.

## 1. The component tentatively called "harness"

**His words, and the context they lack.** The record is `flows/91ea9f/vision/encapsulation.md`, said to 91ea9f at 91ea9f transcript L273, 2026-10-02T17:56, "intended for Opus before he closed":

> "We already have a component called harness but I don't think that that's really what we're talking about because that would be our actual harness implementation. It's more like, I don't know. Maybe when we start Fable we ask him what would best represent the name of this component that basically handles the encapsulation side of things."

- **Searched in fe945a** (`/home/li/.claude/projects/-home-li-primary/fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl`, 1718 lines): every typed message from 10-01T17:23 to the end. The last subjects are the order to relaunch the Psyche seats (L1626), the correction (L1650), and "I want to develop the anatomy of ethos for the most important component, which is, I don't know, I think, flow…" (L1650). There is no "harness" naming discussion and no word on encapsulation or sandboxes.
- **fe945a's Flow-anatomy research never finished.** That subflow (L1656) ended with its last text being "Now the contract itself." Its brief describes a flow record as "id, session, harness, route, lifecycle", where harness means the harness kind.
- **Other transcripts:** no hits in 6997eb, bd0019, 01e496 or any Codex session since 10-01 for harness, encapsulation or sandbox in the living's words.
- **Conclusion:** the discussion was not captured in any transcript.

**Earlier psyche that names the same component (by level):**
- `flows/024bc7/vision/sandbox.md`, 2026-09-13, STT:
  > "Establish a coherent system here where you're going to figure out a way to start a new process, maybe with this harness component that you need to describe anatomically well. You can have just a proof of concept of it all, like the persona. Just start a full sandbox. You can use Prometheus. … Can we copy the token into another host so that my codex and Claude log in? … I lock the keys into an encrypted, volatile, throwaway key, right, with only the process that needs the token having it."
- `flows/6cc91b/vision/sandbox.md`, 2026-09-13, STT:
  > "This flow is a composition, which we call a harness today in the thinking machine world, and we already have a reality with our flow-based memory system, which is basically what this is."
- Same file, 2026-09-14, STT:
  > "We have a sandbox test version of this, a light sandbox, which is basically a sandbox of my home environment, and it can reuse my login, but with a different user environment. Container for the codex, the code, or whatever harness we decide on."
- `flows/6cc91b/vision/forge.md`, 2026-09-14, typed:
  > "Persona will involve components that take care of sandboxing and things. … It would involve one of our components, which takes care of containerization, which is what Nix does: it creates a container."
- `flows/6cc91b/vision/agentAuthentication.md`, 2026-09-13, STT:
  > "every harness runs in its own sandbox"
  > "the whole messaging layer and spawning new harnesses layer would be authenticated at multiple layers, sandboxed, and controlled by more highly permissioned nexuses."
- `flows/b05237/vision/operational-herderWindowManagement.md`:
  > "When I say the harness, I guess I should say the meta harness or just persona."

  The "meta harness" that he made "the most important thing now" (`flows/7328f4/vision/metaHarness.md`) is session handling: starting, restarting, retiring, hooks and skills.
- `flows/e51411/vision/security.md`, 2026-09-24:
  > "we're not going to use the sandbox of the harness to create security. We're going to create our own sandbox and correctness outside of that. … Security is further down."

**The existing "harness".** Its README is at `/git/github.com/LiGoldragon/harness/README.md` and its architecture at `ARCHITECTURE.md`. It "owns the reusable abstraction for Codex, Claude, and Pi harnesses; it does not own routing policy, OS/window focus observation, or terminal PTY byte transport". It ships the `flow-id` helper, a Kameo `Harness` actor, and the `harness`, `meta-harness` and `harness-daemon` binaries; its last commit is 75ff8a2 (2026-09-12). CriomOS-home pins it at d022427 (`flake.nix:90`, `modules/home/profiles/min/flow.nix:37`). 6997eb's inventory says harness is "built but not running". "Harness" also means the vendor CLIs (Claude Code, Codex), as in the claude-harness and codex-harness skills.

## 2. His words on testing outside CriomOS, sandboxes, credentials and cheap models

(He says "CreoOS"; the vision records render it as CriomOS.)

**Ruled, or given as an order:**
- `flows/91ea9f/vision/testing.md`, 2026-10-02, STT:
  > "I want faster testing also. I don't want to have to deploy or depend on deploying fully through CreoOS before testing. We can have a Nix-written sort of semi-sandbox. Again we have to iron out how we move my credentials into a sandbox so that you can test stuff with small cheap models."
- `flows/e167d8/vision/testRepos.md`, 2026-09-26, STT:
  > "Just set up a persona test repo where we'll run different kinds of sandboxes. One of them will be this semi-sandbox that allows the credentials to be moved over and used and uses lightweight cheap models to test different scenarios and maybe includes different components. If we have a test that includes Message and Flow, then that's a Message and Flow test …"
  > "you don't want to put a bunch of tests that you keep modifying with a Rust build in Nix …"
- Same file, ~13:45:
  > "I think the best would be to copy the login credentials and then generate all the configuration details that work for our test sandbox."
- `flows/b81560/vision/archive-operational-pocSandboxIntent.md`, 2026-09-19:
  > "Yes, the intent is good. A proof of concept is tested in a sandbox first."
- `flows/f38926/vision/operational-openCodeRemoteAccess.md`, 2026-09-19:
  > "first, a proof of concept should be tested in a sandbox in a virtual machine. But because we need to log in in the browser with my credentials, and you can't really run this in a virtual machine"
- `flows/f38926/vision/archive-horizon.md` (and `Vision/horizon.md`):
  > "the virtual machine is running on the node … Prometheus is mostly the workhorse, so it should be a feature on a node … querying the Horizon."
- `flows/1b8ac0/vision/flowNexus.md`, 2026-09-21. This is a relay and is not established as verbatim:
  > "Get Mind to recheck the fully tested pair with a semi-sandbox that lets it use my login to test with Haiku and Luna only, and test it in a VM."
- `flows/fd0f97/vision/launch.md`:
  > "Once you get the Flow component working properly with an easy, cheap test model like Haiku or Sonnet, then relaunch yourself …"
- `flows/024bc7/vision/effort.md`, 2026-09-13, while directing a sandbox test with cheap models:
  > "the cheap model is Luna, medium, everything."

**Vision on credentials reaching a process:**
- `flows/6cc91b/vision/secrets.md`, 2026-09-14:
  > "remotely loaded into the process in a secure way so that if the host is shut down, it loses access … only the process that has it while it's running, and it's going to be sandboxed in a way that other processes can't read its environment variable".
- Also the 09-13 "encrypted, volatile, throwaway key" quote from `024bc7` in section 1.

**Notions:**
- `flows/b05237/vision/operational-messengerPaneSyncFailure.md`:
  > "maybe you want to run some kind of sandbox herder. You can run light models in and then test if closing a pane is emulating some failure scenarios".
- `flows/6cc91b/vision/pairHierarchy.md`:
  > "Once things have been tested in one place, in the primary, in the sandbox, then they try to release that and fix it."
  > "There are different sandboxes …"
- `flows/01a02a34/vision/sandboxedTest.md`, 2026-08-22:
  > "See if you can get that thing to work in 'sandboxed' (not interfering with production) test."

**What exists for it today:**
- **The `compensation-nix` skill** (Curriculum `skills/compensation-nix.md`, 16cf0d8, 2026-09-26) prescribes:
  - pure checks, with no network and no credentials;
  - semi-sandbox runners (`packages/<scenario>.nix`, `writeShellApplication`, fresh `mktemp -d` root, "copies in at run time only the login files its components need", "drives the cheapest model (Haiku for Claude, Luna for Codex)", exit-trap removal);
  - never a check, `__impure` or `__noChroot`.
- **`persona-test`** (c1a2370) has one runner, `message-flow`. Its header says it "never reads or copies credentials. A live run receives an already-isolated Codex endpoint from its caller". It requires `PERSONA_TEST_CODEX_CLIENT/HOME/CONTROL_SOCKET` and defaults to `flake.lib.cheapestModel.codex`.
- **The README and the code disagree.** The README still describes copying `.credentials.json` and `auth.json` (commit e3505bf); the later commit c1a2370 moved credentials out to the caller.
- **`lojix-test`** (5aece43, 2026-10-02) has pure checks only.

## 3. What a CriomOS deployment entails for testing a change (witnessed from the repos and skills)

Seats get component binaries only through CriomOS-home: Flow, Message, messenger-clj, harness and Herdr are flake inputs pinned to exact revisions (`CriomOS-home/flake.nix:90-199`), with separate `flow-next` and `message-next` inputs. Testing a component change in the live system therefore means four steps:

1. Push the component.
2. Bump its pin in CriomOS-home.
3. Build on the remote builder (nix-workflow: "never build locally"; NixBuilder is prometheus).
4. Activate through Lojix (`lojix-meta` `Deploy`/`Test`, per the operating-system and lojix skills).

The compensation-update skill then requires rotating stable and Next while preserving running sessions. That means migration and promotion artifacts and no restart of the occupied endpoint. `modules/home/profiles/min/flow.nix` hard-codes "occupied" store paths (flow-0.14.0, harness-0.3.4) so that activation does not restart the running Flow. The `<repo>-test` route avoids all of this: `--override-input <input> path:<checkout>` tests unpushed code straight from a flake (`compensation-nix`, `persona-test/README.md`).

## Sources
- `/home/li/primary/flows/91ea9f/vision/encapsulation.md`
- `/home/li/primary/flows/91ea9f/vision/testing.md`
- `/git/github.com/LiGoldragon/harness/README.md`
- `/git/github.com/LiGoldragon/persona-test/packages/message-flow.nix`
- `/git/github.com/LiGoldragon/Curriculum/skills/compensation-nix.md`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
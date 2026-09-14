# Secret handling, private account access, and phone numbers

Answers the living's question, verbatim:

> What are the safest protocols and practices for thinking machines to handle secrets like that and the secret private account web page access for taking care of it? Also, I need stuff done with my mobile number and changing phone numbers and stuff.

-- psyche, STT, `flows/e1953c/vision/secrets.md`.

Every claim is tagged **(a)** documented by a primary source with the URL, **(b)** this flow's inference, or **(c)** our own existing design. Web research was done by three subflows of this flow on 2026-09-14; this flow did not itself open every page.

## 1. Secrets for machine flows

The living's frame, verbatim, from the same message:

> Right, even on the public part, there is private data, like tokens, that the public, meaning they push to public repos, shouldn't be trusted with too much, in case they put it in a repo publicly facing stuff.

And the earlier ruling, verbatim, `flows/6cc91b/vision/secrets.md`:

> They're just remotely loaded into the process in a secure way so that if the host is shut down, it loses access. It never really sees anything other than the process that needs those tokens.

**The practice, ranked by strength.**

1. **The credential lives at the network edge, never in the agent.** A gateway holds the provider key and attaches provider auth itself; the client sends only a gateway token and omits the provider header. **(a)** Cloudflare AI Gateway documents exactly this — keys in Secrets Store, client sends its own gateway authorization header, rotation is a dashboard edit: https://developers.cloudflare.com/ai-gateway/configuration/bring-your-own-keys/ . Caveat from the same doc set: the Cloudflare token is account-scoped, not per-gateway — https://developers.cloudflare.com/ai-gateway/configuration/authentication/ . **(a)** LiteLLM Proxy is the self-hostable form, and the only one found that puts per-key model allowlist, expiry and budget on one object: https://docs.litellm.ai/docs/proxy/virtual_keys . Operational trap stated in its own docs: budgets are enforced against a database, and nothing is capped on a database-less deployment — https://docs.litellm.ai/docs/proxy/users .
2. **Short-lived, scoped, minted from a control-plane credential the agent never sees.** Documented lifetimes: AWS session tokens 15 minutes to 12 hours, default one hour, role chaining hard-capped at one hour — https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html **(a)**. GitHub App installation tokens expire after one hour and are scoped at mint time — https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation **(a)**. Vault leases carry per-role TTLs and can be revoked through the parent token — https://developer.hashicorp.com/vault/docs/concepts/lease **(a)**.
3. **Injection into the process, not the environment.** **(a)** systemd credentials are the strongest documented primitive found: "Service credentials are placed in non-swappable memory" and, decisively, "Unlike environment variables the credential data is not propagated down the process tree" — https://systemd.io/CREDENTIALS/ . The same page warns that the inline form is world-readable and must not carry anything sensitive; the encrypted load form seals against a TPM. **(b)** An environment variable is not the answer here: the process environment is gated only by a ptrace-mode check (https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html), which protects against strangers, not against the agent itself or anything it spawns — and the agent is the party we are containing.
4. **Per-layer spending caps, so a leak is bounded in money as well as scope.** **(a)** OpenRouter keys take a dollar limit and a reset interval — https://openrouter.ai/docs/api-reference/api-keys/create-api-key . **(a)** Anthropic Workspaces carry a spend limit that cannot exceed the organization's, and "API keys are tied to the Workspace they're created in and cannot be moved between Workspaces" — https://support.claude.com/en/articles/9796807-creating-and-managing-workspaces . **(a)** OpenAI enforces org- and project-level limits per request but states enforcement is not instantaneous and recorded spend can slightly exceed the configured amount — https://developers.openai.com/api/docs/guides/spend-limits .
5. **Nothing the public part can commit, and a server-side net.** **(a)** GitHub push protection blocks the push itself and cannot be skipped the way a local hook can: https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection . **(b)** Client-side hooks — gitleaks, git-secrets — are advisory only for exactly that reason; run them, but do not count on them. **(a)** GitHub notifies partner providers so they can revoke a leaked key, but revocation is the partner's act and only for partner patterns: https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning .
6. **Why context is the real leak surface.** **(a)** OWASP LLM02:2025 names security credentials among what leaks through model outputs, and states that prompt injection can bypass the mitigations, so layers are required: https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ . **(a)** OWASP LLM06:2025 requires downstream actions to run with the minimum privileges necessary, and human approval for high-impact actions: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ . **(b)** Taken together: a secret in the model's context is a secret in the model's output surface. That is the whole reason to put it at the edge.

**What our stack already has.**

- **(c)** The file-descriptor discipline is real and running. `tools/third-seat/provider-run.mjs` refuses any descriptor below 3, reads the secret off it under a size and time bound, and stands up a loopback proxy that adds the authorization header itself — the harness process is handed a local endpoint, never the key. That is practice 1 built small, and practice 3 in spirit.
- **(c)** The `secrets` skill forbids the leaky paths by name: no command substitution, argv, environment, clipboard, `tee`, filters, process substitution, or temporary files; pipe the producer straight to the consumer's own interface, with pipefail set.
- **(c)** Provider descriptors ship marked unauthorized and cannot make a call; the pinned OpenRouter descriptor is committed with routing but no credential.

**What our stack lacks.**

- **(b)** No broker. The remote-loading vision — secrets loaded into the process from a trusted holder, lost when the host stops, a criome-based decision to allow the access — is written down and not built. Nothing today notifies the living and waits before a secret moves.
- **(b)** No throwaway memory salt, no sealed store on a holder node, no revocation path.
- **(b)** No per-layer spend cap anywhere. Nothing bounds what a layer can spend if its key escapes.
- **(b)** No push-protection or scanning gate was found in this tree. For a part whose defining risk is, in the living's words, that "they push to public repos," this is the cheapest missing piece.
- **(b)** Practice 3 is unused: no systemd credential is in play; the descriptor path is per-invocation, not a supervised service.

## 2. Private account web access

The living, verbatim:

> If the public repo can use my web browser, we would have layer 0 access to my web browser and my login session. It then creates the OpenRouter credential with my name to pay for it with the layer 0, which would be the only layer that is allowed to do stuff like that. It has its own workspace, obviously, to instruct it on how to do that safely.

**How it would work.** **(b)** A machine drives a real browser that already holds the living's logged-in session, navigates the provider console, and creates a key. The session cookie is the credential; the machine never needs the password.

**The risks, plainly.**

- **(b)** A session cookie in a profile the machine can drive is a standing credential to the whole account, not to the one page it was sent to. Whatever else is logged in to that profile is in reach.
- **(b)** Second-factor prompts and payment confirmations will appear mid-flow. A machine that can satisfy them is a machine that can also satisfy them unattended.
- **(a)** OpenRouter's terms prohibit using "software, devices, scripts, robots or any other means or processes (such as crawlers, browser plugins, add-ons or any other automated technology) to scrape or copy any information on the Site," and prohibit creating "multiple accounts as a single user, for purposes of bypassing or circumventing use limits" — https://openrouter.ai/terms . **(b)** Notably, the terms name no clause against scripted signup as such; the nearest ones are about scraping and about limit evasion. Scripted account creation is not stated to be permitted either, and this flow will not represent it as permitted.
- **(b)** The audit trail records the living as the actor. Every key the machine creates is the living's act, with the living's name on the bill.

**The safest shape.**

- **(c)** A dedicated browser profile, separate from the daily one, is already our documented practice: `protocols/cloud-maintainer-browser-profile.md` defines a cloud-maintainer Chrome profile on its own loopback debugging port, untracked by git, holding cloud-maintainer logins only, and it names token creation and provider-console work as its purpose. Extend that profile; never the daily browser.
- **(b)** Human in the loop on every purchase and every credential creation. Not a per-session approval — a per-act one. **(a)** This is also what OWASP LLM06 asks for high-impact actions.
- **(b)** The created key goes from the browser to the broker and is never spoken. The transcript records that a key was made, and its identifier, never its value. **(c)** Our `secrets` skill already forbids precisely the handling that would put it in a transcript.
- **(b)** Create the narrowest key the provider offers, with a spend cap set at creation.

**Does OpenRouter work for privacy and model choice?** The living asked, verbatim (`flows/e1953c/vision/thirdModel.md`):

> If OpenRouter works for privacy and choosing the models that we want, then, if it's easy, I can set up an account.

- **Privacy: yes, with a named limit.** **(a)** Zero Data Retention is documented at four levels — account-wide, per model group, per key, and per request through a flag that can only tighten, never loosen, an account setting: https://openrouter.ai/docs/guides/features/zdr . The account toggle for whether prompts may be routed to providers that train is separate for paid and free models: https://openrouter.ai/docs/features/privacy-and-logging . A per-request data-collection setting can deny providers that store data, and it **defaults to allow** — https://openrouter.ai/docs/guides/routing/provider-selection . **(a)** The documented limit, in their words: ZDR enforcement "does not apply to plugins and tools you choose to enable, such as web search." **(a)** Their policy states OpenRouter does not train on inputs or outputs, but that some providers may.
- **Model choice: yes, and enforceable server-side.** **(a)** Provider routing supports an allowed-provider list and a switch that turns fallbacks off, so a request either runs on the named provider or fails: https://openrouter.ai/docs/guides/routing/provider-selection . **(a)** Guardrails go further, enforcing model and provider allowlists, ZDR per model group, spend limits and data regions on the server, blocking anything off-list "even if a key tries to request it": https://openrouter.ai/docs/guides/features/guardrails . **(b)** The request-level pin is a hint; the guardrail is the boundary. Use both.
- **(c)** We already hold a pinned descriptor of exactly this shape — one permitted provider, fallbacks off — committed unauthorized at `tools/third-seat/fixtures/openrouter-fireworks-pinned.json`.
- **(a)** Keys can be created programmatically with a dollar limit, a reset interval and an expiry, from a management key that "cannot be used to make API calls to OpenRouter's completion endpoints": https://openrouter.ai/docs/guides/overview/auth/management-api-keys . **(b)** That separation is the cleanest available fit for the layer-0 shape: layer 0 holds the management key; every other layer gets a capped, expiring key it cannot widen.

## 3. Mobile number and phone-number changes

The living, verbatim: "Also, I need stuff done with my mobile number and changing phone numbers and stuff." The psyche has not spoken further on this; nothing on phones, SIMs or carriers was found in `Vision/`, `vision-raw/`, or any flow's vision. **(b)** So this part answers the general question and asks what the concrete task is.

**What the machine must not do.**

- **(b)** Not a SIM change, not a port-out, not a carrier account login, not a 2FA re-enrollment. These are the exact acts that SIM-swap fraud consists of; a machine able to perform them has, by construction, the capability the attack needs.
- **(a)** Carriers forbid it in their own terms. Verizon's website terms prohibit accessing their resources "through any automated script or routine, including 'robots,' 'spiders,' 'offline readers,' bots, web crawlers or other automated means" — https://www.verizon.com/support/website-use-legal/ . **(b)** This holds even with the account holder's own credentials, and no carrier page read documents any sanctioned automated path.
- **(a)** The only documented delegation is a named human. Verizon appoints an Account Manager, aged 18 or over, and the Account Owner "remain[s] responsible for any changes an Account Manager makes to your account" — https://www.verizon.com/support/customer-agreement/ . **(b)** There is no agent seat and no credential-based delegation in consumer terms.
- **(a)** The strongest locks are deliberately self-service only. Verizon states that "our retail and customer service representatives are not able to turn SIM Protection off for you — it must be disabled through the My Verizon website or the My Verizon app," and that only the Account Owner or an Account Manager can toggle Number Lock — https://www.verizon.com/about/account-security/sim-swapping and https://www.verizon.com/about/account-security/unauthorized-port-outs . **(b)** If a representative cannot lift the lock, neither can a delegated machine. That is the design working as intended.

**Why the risk is this sharp.** **(a)** The FBI states that SIM-swap access "allows criminals to send 'Forgot Password' or 'Account Recovery' requests to the victim's email and other online accounts associated with the victim's mobile telephone number" — https://www.ic3.gov/PSA/2022/PSA220208 . **(a)** NIST's current guidance, SP 800-63B-4, names telephone-network out-of-band as the one *restricted* authenticator, requires a migration plan away from it, and says verifiers "SHOULD consider risk indicators (e.g., device swap, SIM change, number porting, other abnormal behavior)" before sending a code over it — https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ . Critically for a number change: "Setting or changing the pre-registered telephone number is considered to be the binding of a new authenticator." **(a)** CISA and the FBI jointly say "Do not use SMS as a second factor for authentication," recommend hardware FIDO keys, and say to set a telco PIN — https://www.cisa.gov/sites/default/files/2024-12/joint-guidance-mobile-communications-best-practices_v2.pdf .

**On the legal floor, one correction worth having.** **(a)** The FCC adopted SIM-swap and port-out rules in 2023 (https://docs.fcc.gov/public/attachments/FCC-23-95A1.pdf), but the current electronic CFR shows the notification, account-lock, notice, remediation and recordkeeping paragraphs of 47 CFR 52.37 and 64.2010(h) as "[Reserved]," carrying the text "Compliance with this paragraph (h) will not be required until this paragraph is removed or contains a compliance date" — verified against the eCFR on 2026-09-10, https://www.ecfr.gov/current/title-47/section-64.2010 . **(b)** So the free account locks the carriers offer are voluntary today, not mandated. Do not assume a legal backstop; turn the locks on by hand.

**What the machine should do instead.** **(b)** Prepare, never act. The machine writes the checklist and the living performs every step:

- Enumerate every account whose recovery path or second factor is the number in question. This is the part a machine is genuinely good at, and the part people always get wrong.
- Order the work: move each account to a passkey or hardware key *before* the number changes, then remove the number as a recovery path, then change the number last. **(a)** Google's recovery-phone changes "may take up to 7 days" to take effect, so ordering matters — https://support.google.com/accounts/answer/183723 . **(a)** Microsoft is phasing out SMS for personal accounts and directs users to a passkey plus a verified email — https://support.microsoft.com/en-us/accounts-billing/manage/microsoft-to-stop-sending-sms-codes-for-personal-accounts .
- Name the carrier protections to turn on by hand first: a carrier PIN, a SIM lock, a port-out lock.
- Draft what to say to the carrier; do not place the call.
- Hold the after-state: which accounts moved, which still carry the number, what remains. **(b)** That record is the deliverable.

**(b)** The line to hold: the machine knows the whole map and never touches the territory. That fits what the living already ruled for layer 0 — a double-check of intent, non-malice and true source, not a hand on the switch.

## Questions for the living

1. **The phone task.** Is this a new number replacing an old one on the same carrier, a move to a different carrier, a second number kept alongside, or removing the number from accounts without changing it? Concretely: does the number on the criome.net registrar and on the DigitalOcean account change too, or only the personal one?
2. **The broker.** When layer 0 creates the OpenRouter key, where should it land: GoPass on this host, a holder node that serves it to a process and forgets, or a running proxy that injects it and is the only thing that ever saw it? Concretely: for a Kimi K3 run through the pinned Fireworks route, should the harness reach a loopback proxy, as `tools/third-seat/provider-run.mjs` already does, or receive a key of its own?
3. **The confirmation.** What does "a criome-based decision to allow the access" mean for one single act? Concretely: layer 0 is about to click "create key" and then "add twenty dollars" in your browser — does that stop and wait for you, and on which channel does it ask?
4. **The cap.** What is the monthly ceiling per layer, and what happens at the ceiling — hard stop, or fall to a cheaper model? Concretely: if the tertiary layer's OpenRouter key hits its limit at three in the morning, does the flow stop, or drop to a free-tier model and keep going?
5. **The browser.** Should layer 0 use the existing cloud-maintainer profile described in `protocols/cloud-maintainer-browser-profile.md`, which already holds the DigitalOcean login, or a fresh profile holding nothing but provider consoles? Concretely: one machine-drivable profile carrying both your infrastructure and your payment sessions, or two?

## Sources

- The living's words: `flows/e1953c/vision/secrets.md`, `flows/e1953c/vision/privateLayer.md`, `flows/e1953c/vision/thirdModel.md`, `flows/6cc91b/vision/secrets.md`, `flows/6cc91b/vision/layerZero.md`.
- Our own design: `.claude/skills/secrets/SKILL.md`, `protocols/cloud-maintainer-browser-profile.md`, `tools/third-seat/provider-run.mjs`, `tools/third-seat/fixtures/openrouter-fireworks-pinned.json`, `tools/third-seat/README.md`.
- Prior research relied on: `flows/6cc91b/reports/harnessLandscape.md` — only OpenHands documents a read-only credential mount; Pi's Gondolin is the only harness designed to keep auth on the host by intent; neither of our two production harnesses documents the pattern.
- Web sources, opened by three research subflows of this flow on 2026-09-14, each URL cited inline above: Cloudflare AI Gateway, LiteLLM Proxy, HashiCorp Vault, AWS STS, GitHub Apps and secret scanning, systemd credentials, the Linux proc manual, OWASP LLM02 and LLM06, OpenAI and Anthropic spend limits, OpenRouter documentation and terms, NIST SP 800-63B-4, FCC 23-95 and the electronic CFR, FBI IC3, CISA and FBI mobile guidance, FTC, Verizon, Google, Microsoft, FIDO Alliance.
- Not opened directly, flagged by the research subflow: AT&T and T-Mobile refused its requests, so their lock features are reported here, not verified. The FCC's own status pages also refused.

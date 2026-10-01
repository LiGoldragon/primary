# Interface research: how the machines present to the living

Flow 6997eb, subflow of the main flow, 2026-10-01. Marks: WITNESSED means this subflow observed it directly (command, file, tool) on 2026-10-01. CLAIM means a web page or an earlier report said it and it was not independently proven here. Flow ids and hashes are six characters; where two flows share a six-character prefix (01a042 is both a 08-27 Codex flow ending 36 and one ending 8b) the prefix is noted, not guessed.

## 1. What the earlier research concluded

There is no single earlier report titled "how to present to the living". The conclusions are spread over four records, read here in their relevant parts only.

**7fba5f, `reports/codexReportLoop.md` (2026-09-05).** The nearest thing to a prior interface survey. It fixed the loop (main flow writes Markdown, cheaper subflow turns it into a page, the living comments from the phone without waking the session, a later subflow reads every comment with its anchor) and found that on Codex "the page and the comments do not" exist. It tabulated page surfaces (the Codex Sites hub, GitHub, a static page over the tailnet, a Claude artifact) and comment surfaces (pull request review, Hypothesis, Google Docs, giscus, Remark42, Claude artifact comments, Pastel, MarkUp.io). It left six forks open and chose none. Its findings: headless `claude -p` has no Artifact tool (probed then, 2.1.258); no static web server was declared in CriomOS; Tailscale was installed and logged out on this machine; the Codex Sites hub opens-on-phone question was unverified. CLAIM-grade for the web rows (fetched pages), WITNESSED by that flow for the local rows.

**01a052 (2026-08-30 to 09-01), as relayed in 7fba5f.** The feedback contract: comments from the phone, many, without triggering the session, then "I commented", read back with their anchors. No OpenAI surface met it.

**753e69, `reports/mentci-web-tailnet-android-proposal.md` (2026-09-21).** Proposed Ouranos serving a private web UI over a Tailscale tailnet, with Tailscale's own account recommended over Headscale for a proof of concept. Proposal only; nothing was changed. It names no listener or URL.

**1b8ac0 and 0625c3 vision (2026-09-20/21).** The living, after reading flashbooks on the phone, asked for his own web UI ("Mentci Web"), and demanded real illustrations and a phone-shaped layout.

**Superseded by the living on 2026-09-28 (8904b1, not an earlier research report but a later ruling).** "I think the Menchi you're referring to is obsolete now. Menchi is just a nexus and we're calling the user interface Unity. If there's a GUI called Menchi there, we should just archive and mark as stale and abandoned." So the Mentci Web direction of 1b8ac0 and 753e69 is retired as the front end; Unity is the named eventual interface. WITNESSED: `/git/github.com/LiGoldragon/mentci-web` exists but has no commits.

**One tension to surface.** The 2026-09-26 words (93ba9f) say the Claude artifact is "really the best way to reach me" and prefer scroll-down over swipe pages; the 2026-09-20/21 words (0625c3, 1b8ac0) built swipe-paged flashbooks and he rejected them on the phone. Later and more specific: scroll-down, comments only, on the phone. The trial-flashbook skill still prescribes swipe; that sits against the 09-26 words and deserves the living's ruling. Not resolved here.

## 2. The living's verbatim words on interfaces

All are written psyche: speech-to-text (STT) unless marked typed, with the transcription errors as recorded. "Menchi/Menchie" is Mentci as spoken.

**Unity as the eventual interface**

- 2026-09-14, STT, flow 6cc91b `vision/unity.md`: "Let's create a greeny page for this, where the front face of this, everything I'm talking about, is the persona thinking machine system with the Unity interface. What's the whole thing? The Unity."
- 2026-09-18, typed (artifact comment), flow 4a2502 `vision/operational-unityIsMentciClient.md`: "Unity is basically a Menchi server. Menchi is the server. Menchi is the input device of our world, right? Menchi is the mind tool, and Unity is just a client to it." And: "It's a Menchie client. Anything could become a Menchie client." And: "Your first proposal is basically just a Unity Web app, which is a server running somewhere. We would run the server on a trusted node, and then Tailnet authentication, I guess. Maybe that's easier. Then, Unity Slint app, which is a client that connects with Tailnet..."
- 2026-09-28, STT, flow 8904b1 (record 8904b1-30): "I'd rather just make Unity but let's get the base in first and use the pages without the buttons ... I think the only thing that works really is the comment so we might as well just get rid of the buttons and all that and I'll just comment" (flow 183ae0 `vision/presentation.md`, typed). And: "It won't be a page. Obviously it'll be an app. We're going to make our own user interface in Unity. Whenever an agent returns some kind of mechanism will be thrown into gear and maybe some other LLM calls will be used in order to make changes in the user interface in Unity. We can use the concept of using pages for now that I can comment on, which Claude has an interface for, but eventually I would like to use the application itself."
- 2026-09-28, STT, 8904b1-32: "Menchi is just a nexus and we're calling the user interface Unity."
- 2026-09-24, typed, flow 752e0f `vision/unity.md`: voice "in our own user interface" in Unity.
- Android client: typed, flow 840e42 `vision/notification.md`: "do we just straight up write our own Unity app right now as a concept, as a Slint Android project with Linux and Android target?" and `vision/mobile.md`: "you can still run Unity locally on your phone because you're really just running the harness part to the cloud ... You're not going to run an LLM on your phone."

**Pages, comments, buttons**

- 2026-09-26, STT, 93ba9f: "Really the best way to reach me is to create a Claude artifact. ... you should just get a sub-agent to illustrate it as an artifact. And you can use Sonnet for that obviously." And: "I like the scroll-down format not the page swipe/accordion thing because it breaks something when I'm trying to scroll through text, left and right, that has code that has long lines."
- 2026-09-28, STT, 8904b1-27: "If there's something for me, you should just make a Clojure [Claude] artifact for it then I know where to find it." (This is the chat UI problem: he cannot search the chat.)
- 2026-09-28, typed, 183ae0: "I'd rather just make Unity ... use the pages without the buttons ... the only thing that works really is the comment."
- Comments contract, typed, 01a052 `vision/reportFeedback.md`: "I want to be able to put comments from my phone ... I would be able to put in comments without triggering the session every time I put a comment. I could potentially put multiple comments and then go back to the session and tell it that I commented on the report. It would be able to see all the comments and what they refer to."
- 2026-10-01, STT, 6997eb `vision/interfaces.md` (the brief): "We've already done the research but let's maybe review, extend, and re-verify this in terms of what other user interfaces are available. They would also allow Codex or any other model or machine to create these pages to communicate with me or maybe it's not even web-based."
- 2026-10-01, STT, 6997eb `vision/presentation.md` and `pipeline.md`: mark the block for the living at beginning and end; a hook-driven pipeline to Sonnet for a new book or an edit.

**Mobile**

- 2026-09-20, typed with screenshot, session 0625c3 line 1548: "Didn't your instructions tell you to make it mobile-friendly, because I can't read any of that?" Line 1560, STT: "the fact that I have to push a tiny little button in the corner to swipe to the right is fucking horrible. It's like living in the '90s." Line 1616, STT: "everything has to be huge and vertical ... I don't want to see this landscape tiny little box in the middle of my screen."
- 2026-09-21, STT, 1b8ac0 (1b8ac0:1664): "Maybe the Claude artifacts are not the right interface. Maybe we need to make our own web UI." (Later retired, above.) And the same message: "on mobile ... it's being treated like a desktop."
- 2026-09-28, typed, 183ae0: "This is also very hard to read. I have to zoom to see anything and then I can't even swipe to move the zoom around. I have to unzoom and rezoom. It's basically unusable and I've talked about this. How do we deal with the mobile aspect? Does Claude care even about this?" And "This code block ... makes your prose really hard to read."
- Notification channel, typed, 840e42: "What's efficient right now in open source and has a good Android and iOS app is the best. I don't care if it's XMPP ... or Matrix with a thin client..."

## 3. Re-verification: Claude artifacts

| Question | Finding | Mark |
|---|---|---|
| Who can publish | Only the `Artifact` tool inside an interactive Claude Code session (or Chat/Cowork by a human). Not a public REST API. A "publish_context" of interactive is sent and permissions are set to owner by the backend. | CLAIM (Pluto Security analysis); tool exists in this session WITNESSED |
| Headless | `claude -p` has the Artifact tool off. Re-probed: Claude Code 2.1.284, `claude -p` asked to list tools containing "Artifact" answered NONE. | WITNESSED 2026-10-01 |
| Non-Claude process (Codex, script) | Third-party workaround spawns a hidden interactive `claude` in tmux with `CLAUDE_CODE_ENTRYPOINT` and `CLAUDECODE` unset so it registers as CLI; three-minute timeout; updates need a read turn then a publish turn. A hack on a private harness behaviour, can break. | CLAIM (leoawesome/kanban PR 11) |
| Auth | API-key, gateway-token or cloud-provider sessions cannot publish; needs `/login` on a plan with artifacts enabled. | CLAIM (search summary) |
| Audience | Private at birth; no programmatic way to change audience (open feature request, anthropics/claude-code issue 96473). | CLAIM |
| Comments | Anchored to element or selection; `ArtifactComments` reads, replies, resolves; publishing arms a watch so comments reach the session. The artifact cannot be made commentable without a human in a browser. | tool schema WITNESSED; remainder CLAIM |
| Limits | 16 MB page; storage 20 MB, text only; read-then-publish rule for updates. Mobile app can view in the Artifacts tab; editing and sharing need web or desktop. | page size from the tool contract WITNESSED; rest CLAIM (Claude support article) |
| Phone readability | The living's own verdict: hard to read, zoom without pan, code blocks off-screen (2026-09-28). Controllable by the page author (the page is our HTML), but the wrapper is Claude's. | his words, quoted above |

Reading: artifacts are good for Claude seats and for the comment loop that exists today; they are not a medium Codex or a script can write to without a Claude session in the middle.

## 4. Alternatives

Columns: Writer = who can produce the page; Comment path = how he comments and how it reaches a flow; Hook = can the comment trigger a flow automatically; Phone; Offline; Cost to stand up. Stand-up costs are estimates from this subflow, not measurements.

| Option | Writer | Comment path and reach into a flow | Hook | Phone | Offline | Cost to stand up |
|---|---|---|---|---|---|---|
| A. Own static site on our host over the tailnet, plus tiny comment endpoint (form posting to a Nexus or flat file) | Any model or script that can write a file; the Nexus | Selection or per-block form posts to our endpoint; endpoint appends to a comments file or sends a signal to a flow | Yes, we own the handler | Our CSS, our layout: fully controllable; installable as PWA | Yes with a service worker (Android Chrome with Google services installs a WebAPK; other browsers a shortcut, CLAIM, MDN/back4app) | Medium: a host service plus tailnet on the phone. WITNESSED 2026-10-01: `tailscale status` lists ouranos 100.64.0.2 connected and prometheus offline 202 days; earlier 09-05 report found it logged out. No static-server service module found in CriomOS or CriomOS-home by grep (hits were home profiles and a USB check, not a service). |
| B. Same site with an off-the-shelf comments layer: Remark42 or Isso | Same | Remark42: nested, Markdown, anonymous or social login, embedded storage, notifications by Telegram, Slack or email; read back by REST. Isso: SQLite, 12 KB widget. Page-level or thread comments, not selection anchors. | Via REST poll or notification | Embeds fine in our own page | With the page only | Low-medium: one service beside A |
| C. giscus or utterances | Same, public repo needed | giscus needs a public repository and GitHub login; comments in GitHub Discussions (utterances: issues). Read via `gh api`. | Webhook or poll | Browser, GitHub login on the phone | No | Low, but public by construction (giscus: "repository is public, otherwise visitors will not be able to view the discussion"); wrong for private material |
| D. Forgejo (our own) wiki and issues as comments | Any model through git or API | Issue comments; Forgejo sends an `issue_comment` webhook on a reply (CLAIM, Forgejo issue threads). Android app GitNex exists. | Yes, webhook | App or browser; wiki is plain Markdown rendering we do not control | Git clone offline | Medium-high: a Forgejo service. No Forgejo found in our CriomOS by grep |
| E. GitHub Pages or PR review | Any model through git | PR review comments, anchored to a line; `gh api` reads them (from 7fba5f) | Poll or webhook | GitHub app; Pages must be public on most plans | No | Near zero but public or per-repo access, and each report needs a branch and PR |
| F. Matrix bot (Element already in CriomOS-home: `modules/home/profiles/med/element.nix`, WITNESSED present) | Any script via matrix-nio or matrix-commander; formatted HTML, replies, threads | He replies to the page message; the bot sees the reply event with the replied-to event; becomes a comment | Yes: bot receives events | Element X, push notifications: the best "tap and read" of all | Messages cached | Medium: a homeserver (or a hosted account) and a bot; encryption setup is the fiddly part |
| G. Telegram bot | Any script (Bot API); HTML parse mode; reply_to_message; Mini Apps (CLAIM, core.telegram.org) | Reply to the message; getUpdates or webhook delivers it with the reply target | Yes | Excellent, push | Cached | Low, but a third-party hosted channel carrying private material; the living has asked for open source (840e42) |
| H. Email digest | Any script | Reply by mail, parsed by an inbound handler | Yes, with a handler | Fine for text, weak for SVG and layout | Yes | Low; commenting per block is poor |
| I. ePub or PDF to an e-reader (KOReader reads EPUB, PDF, HTML, MD; exports highlights as text, Markdown, JSON; syncs to Joplin, Readwise, Memos; CLAIM, KOReader guide) | Any script (pandoc) | Highlights and notes exported or synced back; no live loop | Poll a sync folder | Good reading, not interactive; SVG and colour limited on e-ink | Yes, best of all | Low, but the comment return is clumsy |
| J. Terminal TUI | Any script | Keyboard comments, direct write to a flow | Yes | Poor on a phone; the living reads on the phone | Yes | Low; does not fit the stated need |
| K. Notion API or Obsidian Publish | Notion: any script through its API; Obsidian Publish: file sync | Notion: comments via API but top-level only, no new threads or resolved via the public API (CLAIM, Notion docs); Obsidian Publish is read-only | Notion polls | Apps good | Partial | Vendor-hosted and closed; against the open-source line |
| L. Hypothesis over any reachable page | Any page | Selection-anchored annotations, private groups, REST read-back; needs the page reachable by the Hypothesis proxy or bookmarklet (CLAIM; tailnet-only pages are not reachable by its hosted service) | Poll | via.hypothes.is; no native app | No | Low if public; poor if the page is private |
| M. Native Android app or PWA (our own) | Any model through the feed | Our app, any comment model we choose, including selection anchors | Yes | Best, because we own the layout | Yes | High for native; PWA is the A path |
| N. Unity reader | Anything that writes Markdown or datom plus a feed | Our comment panel posts to the same endpoint as A | Yes | Good once built, not before; the living's stated destination | Yes | Highest |

### What a minimal Unity reader needs

Not tested here; the shape from search results (CLAIM) and from the living's own words.

- A feed: a URL or Nexus socket listing books and their Markdown (UnityWebRequest or a WebSocket library such as NativeWebSocket, which targets Android with no external DLLs).
- A renderer for Markdown: UI Toolkit with the community UAddMd package (CLAIM, repo page), or the simplest route, a native WebView plugin (unity-webview, UniWebView) that would simply show option A. Note UI Toolkit limits: rich-text tags are not supported in TextField and a text field is capped at 12 thousand characters (CLAIM, Unity forum), so long books need per-block elements.
- Images and SVG: SVG needs the Vector Graphics package or pre-rasterised images; the living wants real illustration, so the images should be rasterised to phone width on the server.
- A comment return: the same POST as option A, carrying a block anchor and the reader's text.
- Tailnet reach: the Tailscale app on the phone gives the phone a tailnet address, as 753e69 proposed; Unity just calls that address.
- The living's words add: the thin client does not run a model; the app is a Mentci client; "Anything could become a Mentci client" (4a2502).

Key point: if A defines the feed and the comment POST as an open contract, the Unity reader is a second client of that contract, not a restart.

## 5. Ranked shortlist

1. **Option A, our own site and comment endpoint on a tailnet host, PWA-shaped.** Any model, Codex or script writes the Markdown the pipeline already produces; he reads in our own phone-first layout (scroll, no swipe, huge and vertical, images raster-first); comments are POSTs we own, so a hook can wake a flow and the "comment many, wake later" contract from 01a052 is a design choice, not a hope. It meets "maybe not web-based" half-way (open contract) and is the natural bridge to Unity. Cost: one service plus the phone on the tailnet, which 753e69 already scoped. Risk: we own the layout work he has complained about, and the host must be up (ouranos is, prometheus is not).
2. **Option F, a Matrix bot delivering the page and taking replies as comments.** Fastest route to push-to-phone with a proven mobile client already in our home profile and a standard reply-as-comment loop that any script can drive. Weakness: Matrix is a poor home for illustrated pages, so it should deliver the link or a rendered image and carry the comment, not the book. It pairs with A as notification channel (his 840e42 question).
3. **Option N, the Unity reader, as the destination**, not the first build: it is the interface he named and ruled (8904b1), and it should consume the same feed and comment POST as A. Rank three because it is the highest cost and he himself said "let's get the base in first".

The Claude artifact stays the interim baseline for Claude seats and is not ranked: it works today, the comment watch is in place, but it cannot be written by Codex or a script without a live Claude session, cannot be made visible to others programmatically, and carries his phone-readability complaints.

## 6. Unverified, and what would settle it

- Whether his phone browser installs the PWA and holds the tailnet connection in the background. Settle: a one-page test on ouranos.
- Whether Codex Sites hub opens on the phone outside the workspace login (unchanged from 7fba5f). Moot if A stands.
- Forgejo and Matrix homeserver availability on our hosts: no declaration found by grep; not checked beyond that.
- The three-minute tmux workaround for publishing artifacts: third-party; not run here.
- Unity package choices: from search summaries, not tried.
- Whether swipe pages or scroll-down is the rule for the next books (tension in section 1).

## Sources

- Earlier records: `/home/li/primary/flows/7fba5f/reports/codexReportLoop.md`; `/home/li/primary/flows/753e69/reports/mentci-web-tailnet-android-proposal.md`; `/home/li/primary/flows/01a052/vision/reportFeedback.md`; `/home/li/primary/flows/0625c3/vision/flashbookMobile.md`; `/home/li/primary/flows/1b8ac0/vision/mentciWeb.md` and `flashbooks.md`; `/home/li/primary/flows/4a2502/vision/operational-unityIsMentciClient.md`; `/home/li/primary/flows/840e42/vision/mobile.md` and `notification.md`; `/home/li/primary/flows/6cc91b/vision/unity.md`; `/home/li/primary/flows/752e0f/vision/unity.md`; `/home/li/primary/flows/183ae0/vision/presentation.md`; `/home/li/primary/flows/93ba9f/vision/presentation.md`; `/home/li/primary/flows/8904b1/vision/presentation.md`; `/home/li/primary/flows/6997eb/vision/interfaces.md`, `presentation.md`, `pipeline.md`, `commentary.md`.
- Local witnesses 2026-10-01: `claude --version` (2.1.284) and a `claude -p` probe for Artifact tools (NONE); `tailscale status`; `/git/github.com/LiGoldragon/mentci-web` git state; grep for forgejo, nginx, caddy in CriomOS, CriomOS-home, goldragon; `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/element.nix`.
- https://github.com/leoawesome/kanban/pull/11 (headless artifact publishing workaround)
- https://pluto.security/blog/inside-claude-artifacts-how-your-agent-publishes-to-the-web/
- https://github.com/anthropics/claude-code/issues/96473 (no programmatic audience)
- https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them
- https://core.telegram.org/bots/api
- https://giscus.app/
- https://remark42.com/
- https://web.hypothes.is/help/
- https://koreader.rocks/user_guide/
- https://developers.notion.com/guides/data-apis/working-with-comments
- https://unifiedpush.org/users/distributors/ntfy/ and https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable
- https://github.com/endel/NativeWebSocket, https://github.com/Alexiush/UAddMd, https://github.com/gree/unity-webview, https://docs.unity3d.com/6000.3/Documentation/Manual/UIElements.html, https://discussions.unity.com/t/ui-toolkit-text-field-limitations/1499967
- https://github.com/vranki/hemppa and https://github.com/8go/matrix-nio-send (Matrix scripting)
- https://codeberg.org/forgejo/forgejo/issues/7964 and https://github.com/home-operations/kritik/pull/75 (Forgejo comment webhooks; GitNex mentioned in search results)

# Kedge feasibility probe

This is a bounded feasibility probe of the public `batjaa/kedge` repository for a model and harness independent report/review surface. It does not deploy a service, create a SaaS account, or mutate Primary.

## Result

Kedge is a credible concrete stack for the requested interaction. The source is public and carries AGPL-3.0. At the pinned source revision it has a self-hosted Docker Compose topology, a browser review surface, persistent versioned anchored threads, a REST API, and an MCP endpoint. The human/browser path and the machine/MCP path share the same document, thread, anchor, and comment model.

The complete local service witness could not run in this environment because the required runtime tools are absent: `docker`, PHP 8.3+, and Composer were all unavailable. I therefore ran the smallest available behavior witness over Kedge's real web anchor machinery and inspected the upstream service and E2E tests. GitHub reports all three checks green for the exact revision: API PHPUnit/Pint, web types/build, and Playwright E2E. Those green infrastructure reports include upstream tests that exercise the real Laravel service, database rows, browser surface, and an out-of-process MCP SDK client, but they are reported CI evidence rather than a local witness from this probe.

## Exact source

The repository was cloned into disposable workspace `/tmp/kedge-probe.klMz7F/kedge` from `https://github.com/batjaa/kedge.git`. `git ls-remote` and `git rev-parse` both returned:

```text
6ffda67e3d7d403ca29c4ec2862d66ab3e969099
```

This is `origin/main` at the time of the probe, with commit subject `fix(api): align AI agent timeouts with the job budget; client timeouts are deterministic (#154)` and author date `2026-08-25T12:34:31-07:00`.

The repository metadata endpoint reports `private: false`, default branch `main`, and SPDX license `AGPL-3.0`; the checked out `LICENSE` begins with the GNU Affero General Public License Version 3.0. The Kedge README states the same open-source license, describes anchored comment threads and MCP, and points to full self-hosting.

## Behavior that the source and upstream tests define

The Kedge source gives an agent this sequence:

```text
MCP initialize / tools-list
          |
          v
list_documents  -> document id
          |
          v
get_document    -> version id + plain_text + projection_version
          |
          v
locate exact text in plain_text
          |
          v
post_comment(anchor exact/start/end/context/version)
          |
          v
list_threads / get_thread -> comments + target anchor
```

`PostCommentTool` requires the caller to read `version.plain_text`, provide the exact selected text, UTF-16 `start`/`end` offsets, and `projection_version`, and optionally pin the write to the `version_id` that was read. The server re-validates the selection against the stored projection and refuses a stale or incorrect anchor. `ListThreadsTool` returns each thread's anchor and comment count; `GetThreadTool` returns the full conversation and can read the anchor as it stood on a requested version. The MCP payload includes `document_version_id`, exact text, prefix, suffix, offsets, projection version, anchor state, and each comment's `client` (`web` or `mcp`).

The API route registers `/api/v1/mcp` as a Streamable HTTP MCP endpoint. It requires a Kedge agent token, refuses ordinary browser sessions, keeps MCP independent of the AI-provider gate, and exposes these tools in the current closed surface:

```text
get_digest       get_document       get_improve_prompt  get_thread
list_documents   list_threads       post_comment        reply
```

The web E2E client is a real `@modelcontextprotocol/sdk` client in a separate Node process. It performs the MCP handshake, lists documents, reads a version projection, calculates the anchor, calls `post_comment`, and returns the persisted thread/comment data. The corresponding Playwright journey first posts a human anchored comment, then has the out-of-process MCP client post a second anchored comment, reloads the browser document, and asserts both comments and their anchors are visible in the review rail. The same journey checks that the agent comment is stamped `client: mcp`, that a revoked token receives HTTP 401, and that revocation creates no third thread.

A separate Playwright journey posts two anchored browser comments, updates the document into a new version, and observes one comment re-anchor while the deleted passage becomes an orphan. This is the needed persistence/version behavior, although that test is not the same as the MCP journey.

The design is model-independent at the service boundary. Kedge's MCP endpoint does not run an inference model, and its README states that MCP is gated separately from AI; a self-hosted instance can host agent reviewers with no provider configured. Any machine model or harness that can use Streamable HTTP MCP can read the document, preserve the returned version/anchor fields, and post or retrieve review data. If a harness has no MCP support, the same backend also exposes versioned REST routes, including document thread listing and thread creation.

## Witness run

I installed only the web dependencies in the disposable checkout with `npm ci --ignore-scripts`. I then ran the repository's real Vitest machinery from `web/`:

```text
node node_modules/vitest/vitest.mjs run \
  test/anchor-capture-core.test.ts \
  test/anchor-capture-dom.test.ts \
  test/reanchor.golden.test.ts \
  test/projection.golden.test.ts \
  test/projection.contract.test.ts
```

Observed result:

```text
5 test files passed
38 tests passed
Duration 725ms
```

This witness runs the actual projection, browser range capture, anchor bounds, and re-anchoring code. It establishes that the anchor substrate and re-anchoring machinery execute successfully at the pinned revision. It does not establish persistence or HTTP behavior by itself.

I also queried the public Kedge runtime read-only. `GET https://kedge.page/api/v1/config` returned `self_hosted: false`, `ai.enabled: true`, and `mcp.enabled: true`. An unauthenticated `POST https://kedge.page/api/v1/mcp` returned `{"message":"Unauthenticated."}`. I did not call the public demo POST, create an account, create a report, or write comments.

GitHub's check-run API for commit `6ffda67e3d7d403ca29c4ec2862d66ab3e969099` returned completed-successful checks for `API (Pint + PHPUnit)`, `Web (types:check + build)`, and `E2E (Playwright journeys)`. The upstream E2E source is included in the pinned checkout and describes the MCP client and persistence assertions above. This is an infrastructure report from the repository owner; it is not a claim that this probe locally ran PHP or Docker.

## What is still missing for our exact desired stack

Kedge is not yet a universal adapter by itself. It supplies the durable review protocol and MCP/REST service. We would still need a thin harness-neutral integration convention:

```text
published report id / share URL
stable source version id
read_report(report) -> rendered content + version + projection
read_review(report, version?) -> threads/comments/anchors
write_review(report, version, anchor, body, idempotency_key)
```

Each harness adapter would translate those operations to MCP first, REST where needed, or a small local client. The durable state must live in Kedge, so comments accumulate while no model session is running. A later explicit invocation asks the adapter for `list_threads` and `get_thread`, preserving both the comment body and its target. The model should be treated as a caller of this interface, not as the owner of the browser session.

For the user's exact “publish a report, comment from a phone, then tell Codex to read all comments” path, the remaining local proof is an E2E run against a self-hosted instance: boot the Compose stack, publish/import a Markdown report, open the share surface from a second browser context or phone, post two independently selected passages, close the model session, then use an MCP client in a fresh process to retrieve both anchored threads. This probe could not run that sequence because Docker and PHP are absent. The upstream tests separately cover the major pieces, including two human anchors, a human plus MCP anchor, and HTTP MCP transport, but no recovered test combines phone/browser share-link identity, two comments, a sleeping model session, and later fresh-process retrieval in one scenario.

There is a concrete mobile risk in the pinned web source. `web/components/app/document-review-surface.tsx` wires selection capture through React `onMouseUp` and `onKeyUp`; the source search found no `selectionchange`, `touchend`, or `pointerup` handler. The Playwright helper likewise synthesizes a `mouseup` event. This proves desktop-style selection coverage only. Responsive layout is not evidence that a touch selection can open the comment composer, so phone commenting must be treated as unverified until a real touch E2E witness passes or the surface gains an explicit touch selection path.

Kedge's current self-host recipe builds images locally on first run, so it would need an ordinary machine with Docker or prebuilt images on a machine that cannot build locally. The reference deployment includes PostgreSQL and Kroki. The source says the full self-hosted product is AGPL-3.0 and includes the MCP server; no Sites dependency is required.

## Sources

- Source witness: disposable checkout `/tmp/kedge-probe.klMz7F/kedge`, exact revision `6ffda67e3d7d403ca29c4ec2862d66ab3e969099`.
- Source witness: `README.md`, `deploy/local/README.md`, `deploy/local/compose.yml`, `LICENSE` in that checkout.
- Source witness: `api/routes/api.php`, `api/app/Mcp/Tools/PostCommentTool.php`, `api/app/Mcp/Tools/ListThreadsTool.php`, `api/app/Mcp/Tools/GetThreadTool.php`, and `api/app/Services/Agents/McpPayload.php` in that checkout.
- Source witness: `web/e2e/mcp-agent.mjs`, `web/e2e/mcp-agent.ts`, `web/e2e/mcp-agent.spec.ts`, and `web/e2e/update-content.spec.ts` in that checkout.
- Behavior witness: Vitest 3.2.4 run over the five listed web test files; 38 tests passed.
- Infrastructure report: GitHub check runs for [`6ffda67e3d7d403ca29c4ec2862d66ab3e969099`](https://github.com/batjaa/kedge/commit/6ffda67e3d7d403ca29c4ec2862d66ab3e969099/checks) (API, web, and E2E checks completed successfully).
- External source metadata: [`batjaa/kedge`](https://github.com/batjaa/kedge), [`Kedge self-hosting guide`](https://kedge.page/), [`Kedge specification`](https://kedge.page/docs/spec).
- Read-only live witness: [`https://kedge.page/api/v1/config`](https://kedge.page/api/v1/config) returned MCP enabled; unauthenticated MCP POST returned HTTP 401.

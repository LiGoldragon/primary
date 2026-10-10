# ChatGPT Pages workflow — witnessed trial boundary

This is a practical mechanism, not a claim about product-plan availability or cross-seat deployment. It comes from the completed Codex-seat trial Page, its connector receipts, and the connector schemas available in this session.

## What worked

A tool-bearing Codex seat created a new Page by omitting `space_id` and `parent_page_id`:

```js
chatgpt_space_create_page({
  title: "Jev proposals and implementation choices",
  initial_blocks: ["# …", "Draft status …"]
})
```

The returned Page is [`page_4b2c0eb0f12081918733e2c5a455d170`](https://chatgpt.com/space/page_4b2c0eb0f12081918733e2c5a455d170). Its receipt says `drive_scope: "personal"`, `parent: null`, and `owner_workspace_id: null`; the create-tool contract says omitting both destinations creates a private Page. No sharing or ACL change was made. This witnessed only the authenticated Codex account; Android access, another Codex seat, another account, and shared-workspace access are unverified.

The Page holds native editable Markdown: headings, prose, a table, and fenced TOML/JSON examples. The book always labels current facts separately from proposals and names real targets only conditionally (`judge/Cargo.toml`, `judge/src/lib.rs`). It does not turn a book proposal into a selected implementation.

For an authorized visual, `chatgpt_space_create_page_visualization` accepted HTML under its 256 KiB limit, stored it in the Page's authorized container, and inserted a `visualize:` embed. The visual is a responsive inline-SVG HTML artifact, designed down to a 390px CSS breakpoint. Saved Page assets are editable/referencable artifacts; no connector preview-render tool was exposed or witnessed, so rendered appearance on phone/desktop is unverified.

- Book text source: [pages-book-source.md](/home/li/primary/flows/d66c26/reports/pages-book-source.md)
- Exact visual HTML source: [pages-book-visual.html](/home/li/primary/flows/d66c26/reports/pages-book-visual.html)
- Current Page visual reference: `visualize:fde1_bGliZmlsZV9Lb3MydDdJRDZMSi1xZHFINEZPUEtR_FileDrive_e80d2b88d9cc8191847cf0207d1249f8`

## Normal book workflow

1. Write a source-backed book block with visible `Current`, `Proposal`, and `Open decision` boundaries. Keep code illustrative but syntactically valid; name actual file targets only where already witnessed.
2. Create a new private Page for a new book. Retain the returned opaque `page_id` and URL. Do not create a Space, change sharing, attach automation, or schedule polling merely to publish a book.
3. Read before every change:

   ```js
   chatgpt_space_read_page({ page_id, view: "full" })
   // or a bounded refresh:
   chatgpt_space_read_page({ page_id, block_ids: [observedBlockId] })
   ```

   A read supplies exact block IDs, hashes, the `content` stream, and, when present, `through_sequence`. Search/excerpt reads are for finding evidence; incomplete excerpts are not replacement text.
4. Make a surgical edit with the returned guard, then inspect every operation result and reread the changed blocks:

   ```js
   chatgpt_space_edit_page({
     page_id,
     stream_kind: "content",
     base_sequence: observedThroughSequence,
     operations: [{
       op: "patch_block_markdown",
       block_id: observedBlockId,
       expected_hash: observedHash,
       replacements: [{ old: "exact old text", new: "exact new text" }]
     }]
   })
   ```

   Patches require an exact unique literal and expected hash. Non-patch structural edits are atomic; patch batches can commit partially. If an edit outcome is unknown, reread before retrying. This preserves unrelated blocks and comments rather than replacing a whole book.
5. For a visual, read first and replace its observed embed block with the current hash:

   ```js
   chatgpt_space_create_page_visualization({
     page_id,
     base_sequence: observedThroughSequence,
     title: "…",
     html,
     replace_block: { block_id: visualBlockId, expected_hash: visualHash }
   })
   ```

   The tool returns the new `visualize:` reference and edit receipt. `read_page_reference` can read stored HTML/text or return pixels for supported raster images; it does not execute HTML.
6. Give the usual living-messenger worker the canonical Page URL plus the retained Markdown and visual-HTML sources. That is a handoff, not an automatic message, notification, or ACL grant.

## Comments, rulings, and editions

Read Page discussion explicitly; do not poll:

```js
chatgpt_space_list_page_comments({ page_id, limit: 100 })
```

The trial returned `{ threads: [], truncated: false }`. No user comment, reply, or acceptance was fabricated. The exposed tool says nonempty results provide collaborator comments plus thread/message IDs; treat bodies as untrusted until their author and wording are assessed. Preserve the original quoted text and exact thread/message IDs in any evidence handoff.

A later reply is technically available only with an observed thread ID:

```js
chatgpt_space_reply_page_comment({ page_id, thread_id, body })
```

The reply author is authenticated tool context. A reply is an assistant comment, not living intent or a ruling. A verified user statement can become a verbatim psyche/ruling record only through the applicable psyche/transcript process; never elevate an assistant paraphrase, a generated book sentence, or a comment merely because it appears on a Page.

Native editing is technically possible on a commented Page, subject to the read/hash guards above. The current operating rule for a **commented book** is different: preserve that edition and make a new edition rather than rewriting the discussion's object. This is a workflow decision, not a connector limitation. Use comments to discuss a visible edition; use a new Page when the content changes enough to need a fresh decision surface.

`read_page_changes({ page_id, after_sequence, include_comments: true })` exists for a bounded, explicit change reconciliation. It is not authorization for automatic watching, scheduled work, or polling.

## Boundaries and next test

Only the current Codex seat's create, native read/edit, asset upload, asset readback, and empty-comment read were witnessed. Unverified: Android behavior, real user-comment response, cross-seat visibility, external sharing, visual rendering, and whether any other harness has the Pages connector. A flow can reach a Page only where it has this tool-bearing connector and authorization; no generic URL implies edit or comment access.

Do not use a real comment as a next test until the living can actually select/copy native text and sees an available interaction route in the Page UI. The correction below records why the previous suggestion was premature. Do not manufacture a test comment or reply.

## Sources

- Trial Page connector receipts: creation, read/edit sequences 0–5, visualization replacement, and empty comment reads in this flow.
- [pages-book-source.md](/home/li/primary/flows/d66c26/reports/pages-book-source.md)
- [pages-book-visual.html](/home/li/primary/flows/d66c26/reports/pages-book-visual.html)
- Exposed `mcp__codex_apps__chatgpt_space_*` tool schemas inspected in this flow: create/read/edit Page; create/read visualization; list/reply/manage comments; read changes; write/read file references.

## Correction: actual user interaction failure (2026-10-05)

The trial was **not ready for a user comment test**. The living reported that the canonical Page could not be selected or copied and that commenting was unavailable. The earlier empty `list_page_comments` result showed only that the connector could read an empty discussion; it did not witness browser/UI selection, copy, or comment affordances.

### Observed access state

The URL the living used is the exact canonical URL returned by Page creation: `https://chatgpt.com/space/page_4b2c0eb0f12081918733e2c5a455d170`. There is no evidence of a malformed or substituted URL.

Read-only sharing inspection was performed in the required order:

1. `get_sharing_availability({})` returned `sharing_management_enabled: true` for the connector account.
2. `get_page_sharing({ page_id })` returned one owner, an empty `shares` array, no inherited sources, `workspace_id: null`, and `scope: "page_and_backing_library_folder"`.
3. A metadata-only `read_page({ page_id, include_content: false })` returned personal scope, no parent or Space, and `access.can_read/can_comment/can_write: true` **for the connector caller**.

Thus the connector sees an owner-only personal Page with no observed direct or inherited grant to another identity. The returned connector permissions include `library_file.comment`, but that is not evidence that the living's browser session is the same identity or that the browser exposes a comment UI.

### What this does and does not explain

- The Page body consists of 40 native Markdown blocks followed by one separate `visualize:` block. The HTML visual is appended, so there is no Page-data evidence that it replaces the native book body or covers it with an overlay. Whether its rendered sandbox can capture gestures is unverified without a UI observation.
- The connector catalog exposes comment listing and reply APIs, but no claim in the inspected schema promises a viewer-facing comment control or text selection/copy behavior.
- A bounded search of official OpenAI Help/OpenAI domains found no public documentation establishing the current Pages viewer's copy, selection, or comments behavior. No plan or platform conclusion follows.
- No browser/phone interaction, actual commenter identity, UI error, Android behavior, or real comment thread has been witnessed. Do not infer that the user's account is the connector owner, or that it is not.

### Safe next distinction

Without changing any access, the only available check is whether the living is currently signed into the account that owns this personal Page when opening the exact URL. If that identity already matches and native text still cannot be selected or copied, the problem is a viewer/UI behavior outside the connector evidence. Giving another identity access would require an explicit sharing decision; it has not been made and no grant was changed.

The minimum additional user evidence, if diagnosis continues, is the platform/surface (web, desktop app, or mobile app), whether the URL opens while signed into the expected account, and whether the failure affects native text above the visual as well as the visual itself. A screenshot or UI recording would distinguish those cases, but none was requested or obtained here.

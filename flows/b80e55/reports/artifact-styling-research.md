# Artifact styling research — what we control

Flow b80e55, subflow report, 2026-09-21.

## 1. System chrome

We control **only the content inside the iframe**. The artifact viewer's
header (title, share, chat buttons), frame, and footer are the host app —
untouchable. The host injects a small reset: `color-scheme: light`, zero
body margin, 14px system font, off-white ground, `img{max-width:100%}`,
`[hidden]{display:none!important}`. We override all of that with our own
`<style>`. The host also paints its own ground behind the iframe, so `body`
needs an explicit `background` or it inherits the host theme.

## 2. CSS capabilities — all modern CSS works

The artifact runs in the user's browser (Chrome, Safari, Firefox). No
polyfills, no old-browser shim. Everything listed works in Chrome 151+:

- **CSS Grid** — yes, preferred over flexbox for layout
- **Custom properties** — yes, already used in prototypes
- **Container queries** (`@container`) — yes, Chrome 105+
- **Dynamic viewport units** (`dvh`, `svh`, `lvh`) — yes, Chrome 108+
- **`clamp()`** — yes
- **`aspect-ratio`** — yes
- **`@layer`** — yes, Chrome 99+
- **`:has()` selector** — yes, Chrome 105+
- **`text-wrap: balance`** — yes, Chrome 114+
- **Scroll snap** — yes
- **`color-mix()`** — yes, Chrome 111+
- **Nesting** — yes, Chrome 120+

Container queries are especially useful: each flashbook page can be a
container, and illustrations/text reflow based on the container's size
rather than the viewport — more reliable than media queries in an iframe.

## 3. External resources

**Scripts:** cdnjs.cloudflare.com (preferred), cdn.jsdelivr.net/npm,
cdn.tailwindcss.com, code.jquery.com. **Everything else silently blocked.**

**Tailwind play CDN:** Yes, `https://cdn.tailwindcss.com` is on the
allowlist. It loads Tailwind as a runtime JIT compiler. Adds ~300KB but
gives utility-first CSS with no build step. Trade-off: runtime overhead
vs. hand-written CSS. For a template with a fixed design system, hand-
written CSS with custom properties is leaner and more predictable.

**Stylesheets:** only Google Fonts (`fonts.googleapis.com`). All other
external CSS must be inlined.

**Images/media:** No external images. Inline SVG or data URIs only.

## 4. Screenshot capability

**Chrome 151 headless is installed** at `/home/li/.nix-profile/bin/google-chrome`.
Phone-size screenshots work:

```sh
google-chrome --headless --disable-gpu --no-sandbox \
  --screenshot=/path/to/output.png \
  --window-size=390,844 \
  file:///path/to/flashbook.html
```

This renders the page at exact phone dimensions (390×844 = iPhone 14/15).
We can check illustrations, font sizes, and layout before publishing.
Multiple sizes: `--window-size=390,844` (phone), `768,1024` (tablet),
`1440,900` (desktop).

## 5. Template approach

The artifact `files` parameter supports publishing CSS alongside HTML:
`files: {"flashbook.css": "path/to/flashbook.css"}`. The HTML references
it as `<link rel="stylesheet" href="flashbook.css">`. This means one
shared template CSS file reused across all flashbooks. On update, files
left out of the map are kept; only explicit changes replace them.

## 6. Font loading

Google Fonts works via `<link>`. Data-URI `@font-face` works but each
font file is 20-100KB base64. Page limit is **16MB** total including
data URIs. A flashbook with 3 font weights as data URIs would use
~200KB — well within limits. Google Fonts is simpler and lighter.

## Recommendation

Use **CSS Grid + custom properties + container queries** — no framework.
Hand-written CSS with a shared `flashbook.css` template file. Container
queries for responsive illustration switching (more reliable than viewport
media queries inside an iframe). Check work with headless Chrome screenshots
at phone/tablet/desktop sizes before publishing.

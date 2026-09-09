# cdp-stdin-type

Flow `0d557b`. Subflow witness — an observation, run here, in this cloud
container. Every command and every output below was executed; nothing is
reconstructed from memory. Where something could not be exercised in this
container it is named as unverified rather than smoothed over.

## What was under test

`/home/user/CriomOS-home/packages/cdp-stdin-type/cdp-stdin-type.mjs` — the tool
that gives a browser the stdin interface it does not have, so a gopass secret
can reach a sign-in field on a rented server without ever being written to that
server's disk, argv, environment, logs, or an agent's context. The placeholder
string throughout is `sample-text-123` (and once `p@ss wörd!-123 `). No secret
was used, produced, or handled.

## Environment

Container without nix and without gopass. `node -v` → `v22.22.2` (global
`WebSocket`, which is what lets the tool be dependency-free). Browser:
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, reporting
`Chrome/141.0.7390.37`, `HeadlessChrome/141.0.0.0`.

## Method

Scratchpad root
`/tmp/claude-0/-home-user/0d557bbe-0086-5d11-bb80-ffc51e14e3e1/scratchpad/cdp-witness`
(written `$S` below). The page under test, `form.html` — a text input in a form
whose submit handler copies the field's value into the DOM, so a successful
Enter is visible as data, not as a guess:

```html
<!doctype html>
<title>cdp-stdin-type witness</title>
<form id="f"><input id="in" type="text" name="v"><button type="submit">go</button></form>
<div id="out">unsubmitted</div>
<script>
document.getElementById('f').addEventListener('submit', function (event) {
  event.preventDefault();
  document.getElementById('out').textContent = document.getElementById('in').value;
});
</script>
```

Chromium launched exactly as the design intends the remote host to run it:

```
/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  --headless=new --remote-debugging-port=9223 --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$S/profile" --no-sandbox "file://$S/form.html"
```

(`--no-sandbox` is a container necessity, not part of the design.)

`curl -fsS http://127.0.0.1:9223/json/version` →

```
{
   "Browser": "Chrome/141.0.7390.37",
   "Protocol-Version": "1.3",
   "webSocketDebuggerUrl": "ws://127.0.0.1:9223/devtools/browser/0efa9ba2-35b6-4342-8b59-750835fab34a"
}
```

`curl -fsS http://127.0.0.1:9223/json/list` returned one page target, id
`AE61A30236E11321593197CB813D27A4`, url the `form.html` file.

Focus was set through CDP `Runtime.evaluate` (helper `cdp-eval.mjs`, which opens
the page's `webSocketDebuggerUrl` and runs one expression):

```
node cdp-eval.mjs 'document.getElementById("in").focus(); document.activeElement.id'
{"result":{"type":"string","value":"in"}}
```

## 1 · The text arrives, exactly, and Enter submits

```
set -o pipefail
printf 'sample-text-123\n' | node /home/user/CriomOS-home/packages/cdp-stdin-type/cdp-stdin-type.mjs \
  --endpoint http://127.0.0.1:9223 --url-contains form.html --submit
```

stdout (stderr empty, exit 0):

```
target AE61A30236E11321593197CB813D27A4
url file:///tmp/.../cdp-witness/form.html
ok: delivered stdin to the focused element and pressed Enter
```

DOM read back over CDP:

```
node cdp-eval.mjs 'JSON.stringify({input: document.getElementById("in").value, out: document.getElementById("out").textContent})'
{"result":{"type":"string","value":"{\"input\":\"sample-text-123\",\"out\":\"sample-text-123\"}"}}
```

`out` changed from `unsubmitted` to the typed value, so `Input.insertText`
reached the focused field *and* the `Input.dispatchKeyEvent` Enter pair really
submitted the form — the field content and the submitted content are the same
string, character for character.

Byte-exactness was pushed further with a non-ASCII, punctuated, trailing-space
payload (`printf 'p@ss wörd!-123 \n'`), which strips exactly one newline and
keeps the trailing space:

```
{"result":{"type":"string","value":"{\"submitted\":\"p@ss wörd!-123 \",\"exact\":true}"}}
```

## 2 · The text is nowhere it should not be

**Tool output.** `grep -c 'sample-text-123' tool.out tool.err` → `tool.out:0`,
`tool.err:0` (grep exit 1, no matches). The three lines the tool prints carry the
target id, the url and a success line; not the text, and deliberately not even
its length.

**argv and environment.** A stand-in producer (`producer.mjs`, holding the
placeholder in a *file* and the pipe open for six seconds, the way
`gopass show -o <path>` holds it) fed the tool while the process table was
photographed mid-read:

```
node producer.mjs | node .../cdp-stdin-type.mjs --endpoint http://127.0.0.1:9223 \
  --url-contains form.html --submit &
sleep 2; ps -ww -eo pid,args > ps3.txt
```

The tool's own `/proc/<pid>/cmdline`:

```
node /home/user/CriomOS-home/packages/cdp-stdin-type/cdp-stdin-type.mjs --endpoint http://127.0.0.1:9223 --url-contains form.html --submit
```

Occurrences of the placeholder in that argv: `0`. In the tool's
`/proc/<pid>/environ`: `0`. In the whole process table (`ps -ww -eo pid,args`),
excluding this witness harness's own shell: `(none)`.

**An honest note on that exclusion.** An earlier attempt used
`printf 'sample-text-123\n' | ...` inside the shell command, and the string *did*
appear in the process table — in the argv of my own witness shell and of the
`grep` doing the checking, never in the tool's. That is the exact failure the
secrets discipline forbids and the reason the producer must be
`gopass show -o <path>`: the leak is in how a caller produces the bytes, not in
this consumer. The clean run above removed the producer's argv leak and the tool
still showed nothing.

**TTY.** `script -qec 'node .../cdp-stdin-type.mjs --endpoint http://127.0.0.1:9223' /dev/null`:

```
cdp-stdin-type: stdin is a TTY. Pipe the text in (e.g. gopass show -o <path> | cdp-stdin-type ...); this tool never prompts, so a secret cannot be typed where it would be echoed.
exit=1
```

## 3 · Selection and failure paths

- `--target AE61A30236E11321593197CB813D27A4` without `--submit`: field became
  `sample-text-123`, `out` stayed `reset` — typing and submitting are separable.
- `--url-contains nosuchpage` → `cdp-stdin-type: no page target whose url contains nosuchpage`, exit 1.
- `printf '\n' | ...` → `cdp-stdin-type: stdin was empty; nothing to type`, exit 1.
- `--endpoint http://127.0.0.1:9999` → `cdp-stdin-type: cannot reach the CDP endpoint at http://127.0.0.1:9999: fetch failed`, exit 1.

Multiple page targets with no selector, and `--target`/`--url-contains` used
together, are refused in code but were not exercised (one tab was open).

## 4 · Screencast under headless=new

The design has the living watch the remote tab through `chrome://inspect` over
an SSH tunnel, which rests on the page emitting screencast frames. Over CDP:
`Page.enable`, a `Runtime.evaluate` that repaints the body every 100 ms,
`Page.startScreencast {format: 'jpeg', quality: 40, everyNthFrame: 1}`, acking
each frame, for three seconds:

```
screencast frames in 3s: 36; first frame base64 length: 5344
```

So `--headless=new` does produce real frames (~12/s here) with real JPEG payload.
That is the mechanism `chrome://inspect` inspection uses; it is evidence the
remote-viewing path is live at the protocol level, not proof that the DevTools
frontend renders it through a tunnel, which was not tested.

## 5 · Teardown

```
pkill -f "user-data-dir=$S/profile"   → killed
curl -fsS --max-time 3 http://127.0.0.1:9223/json/version  → endpoint gone
pgrep -af 'remote-debugging-port=9223'  → only this witness's own shell matched
```

No Chromium was left running.

## 6 · What this witness does not show

- **gopass.** Not installed here. The producer side was a stand-in script; that
  `gopass show -o <path> | cdp-stdin-type ...` behaves the same is expected (it
  is an ordinary pipe) but unwitnessed.
- **The SSH tunnel.** The endpoint was reached on loopback in one container. No
  `ssh -L` hop, no remote host, no `chrome://inspect` frontend was opened.
- **A real sign-in page.** The target was a local file with one plain input.
  Nothing here says how `claude.ai` or `chatgpt.com` behave: React-controlled
  password fields, paste/autofill interception, WebAuthn prompts, bot
  detection, and Google's SSO flow are all untested. `Input.insertText` is an
  IME-style commit and normally does fire the input events such fields listen
  for, but that is a claim about the protocol, not an observation of those sites.
- **Focus.** The tool types into whatever is focused; focus was set here by
  `Runtime.evaluate`. Who focuses the field on a real page — the living's click
  through the tunnel, or a flow — is undecided and untested.
- **Nix.** No nix in this container, so `packages/cdp-stdin-type/default.nix`
  was never built or evaluated. The script was run directly with the container's
  `node` v22.22.2, which matches what the wrapper would exec, but the derivation
  itself is unverified.
- **The consumer boundary.** Chrome holds the plaintext in its own memory and
  sends it over TLS to the site; the kernel pipe and (in the real flow) the SSH
  transport carry it too. Nothing here removes that, and nothing can — being
  signed in requires it.

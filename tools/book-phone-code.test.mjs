import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const template = fs.readFileSync(process.argv[2], 'utf8');
const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'book-phone-'));
const profile = path.join(directory, 'profile');
fs.mkdirSync(profile);
const config = path.join(directory, "config");
const cache = path.join(directory, "cache");
fs.mkdirSync(config);
fs.mkdirSync(cache);
const value = '{ Psyche flow Primary } startInputVital';
const code = 'Library\n    Source.{ Repository Hash Path }\n' + 'x'.repeat(52) + '\n';
const overflowCode = 'UnbrokenCodeToken'.repeat(12);
const literal = '## Spacing\n    unchanged spaces\n';
const escape = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const fixture = path.join(directory, 'fixture.html');
fs.writeFileSync(fixture, `<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<!-- A viewer that fixes the page height at the screen's (as quirks mode does) leaves the grid short of room: scroll containers may shrink to nothing. -->
<style>html,body{height:100%}</style></head><body>
<section class="proposal"><header><span class="pnum">1</span><h2>Flow title</h2></header>
<section class="rulings"><ol><li value="3"><p>the title of a thread.</p><ol class="choices" type="a"><li>the address written short, then the flow's three words: <code id="choice-value">${escape(value)}</code></li><li>other</li></ol></li></ol></section></section>
<pre id="full-code"><code class="language-ethos">${escape(code)}</code></pre>
<!-- A deliberate overflow stress case, separate from the source 52-column gate. -->
<pre id="overflow-code"><code class="language-ethos">${escape(overflowCode)}</code></pre>
<div class="figure" id="fig"><svg viewBox="0 0 520 321" width="520" height="321" style="display:block"><rect width="520" height="321"/></svg></div>
<table id="tbl"><thead><tr><th>Name</th><th>Value</th></tr></thead><tbody><tr><td>${'wide'.repeat(40)}</td><td>one</td></tr>${'<tr><td>two</td><td>three</td></tr>'.repeat(30)}</tbody></table>
<h3 id="outside-heading">Outside heading</h3><div class="textblock">${escape(literal)}</div>
${template}</body></html>`);

let browser;
let socket;
let watcher;
let failure;
let browserDiagnostics = "";
const bound = setTimeout(() => {
  failure = new Error('Phone renderer check exceeded 90 seconds');
  browser?.kill('SIGKILL');
  socket?.close();
}, 90_000);
const measurements = [];
try {
  const endpoint = await new Promise((resolve, reject) => {
    watcher = fs.watch(profile, () => {
      try {
        const [port, route] = fs.readFileSync(path.join(profile, 'DevToolsActivePort'), 'utf8').trim().split('\n');
        if (port && route) { watcher.close(); resolve(`ws://127.0.0.1:${port}${route}`); }
      } catch {}
    });
    browser = spawn(process.env.CHROMIUM, [
      '--headless', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
      '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
      '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost',
      '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0',
      `--user-data-dir=${profile}`, 'about:blank',
    ], { stdio: ['ignore', 'ignore', 'pipe'], env: { ...process.env, HOME: directory, XDG_CONFIG_HOME: config, XDG_CACHE_HOME: cache } });
    browser.stderr.on('data', chunk => { browserDiagnostics = (browserDiagnostics + chunk.toString()).slice(-8192); });
    browser.once('error', reject);
    browser.once('exit', (status, signal) => reject(failure ?? new Error(`Chromium exited: ${status}/${signal}: ${browserDiagnostics}`)));
  });
  socket = new WebSocket(endpoint);
  await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }); });
  let identifier = 0;
  const pending = new Map();
  const events = new Map();
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    if (message.id) {
      const p = pending.get(message.id);
      if (p) { pending.delete(message.id); message.error ? p.reject(new Error(JSON.stringify(message.error))) : p.resolve(message.result); }
    } else {
      const key = `${message.sessionId}:${message.method}`;
      const resolve = events.get(key);
      if (resolve) { events.delete(key); resolve(message.params); }
    }
  });
  socket.addEventListener('close', () => { for (const p of pending.values()) p.reject(failure ?? new Error('Browser connection closed')); });
  const request = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const id = ++identifier; pending.set(id, { resolve, reject }); socket.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
  const { targetId } = await request('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await request('Target.attachToTarget', { targetId, flatten: true });
  await request('Page.enable', {}, sessionId);
  for (const width of [320, 375, 390, 768]) {
    await request('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: true }, sessionId);
    const loaded = new Promise(resolve => events.set(`${sessionId}:Page.loadEventFired`, resolve));
    await request('Page.navigate', { url: pathToFileURL(fixture).href }, sessionId);
    await loaded;
    const { result, exceptionDetails } = await request('Runtime.evaluate', {
      awaitPromise: true, returnByValue: true,
      expression: `document.fonts.ready.then(() => {
        const value = document.querySelector('#choice-value');
        const text = value.firstChild;
        const tokens = [...text.textContent.matchAll(/[A-Za-z][A-Za-z0-9]*/g)].map(match => {
          const range = document.createRange(); range.setStart(text, match.index); range.setEnd(text, match.index + match[0].length);
          return { token: match[0], lines: new Set([...range.getClientRects()].filter(r => r.width > 0).map(r => Math.round(r.top))).size };
        });
        const pre = document.querySelector('#full-code'); const overflow = document.querySelector('#overflow-code'); const body = getComputedStyle(document.body);
        const fig = document.querySelector('#fig');
        const tb = document.querySelector('#tbl'); const tr = [...tb.querySelectorAll('tr')].reduce((h, r) => h + r.getBoundingClientRect().height, 0);
        return { tblBox: tb.getBoundingClientRect().height, tblRows: tr, tblScrollsY: tb.scrollHeight > tb.clientHeight, figBox: fig.getBoundingClientRect().height, figSvg: fig.querySelector('svg').getBoundingClientRect().height, figScrollsY: fig.scrollHeight > fig.clientHeight,
          width: document.documentElement.clientWidth, pageWidth: document.documentElement.scrollWidth,
          choiceDisplay: getComputedStyle(value).display, value: value.textContent, tokens,
          blockWidth: pre.getBoundingClientRect().width,
          availableWidth: document.body.clientWidth - parseFloat(body.paddingLeft) - parseFloat(body.paddingRight),
          scrolls: overflow.scrollWidth > overflow.clientWidth, overflowCode: overflow.querySelector('code').textContent, overflowWidth: overflow.getBoundingClientRect().width, code: pre.querySelector('code').textContent,
          codeWhitespace: getComputedStyle(pre.querySelector('code')).whiteSpace,
          literal: document.querySelector('.textblock').textContent,
          literalHeadings: document.querySelector('.textblock').querySelectorAll('h1,h2,h3,h4,h5,h6').length,
          outsideHeadingDisplay: getComputedStyle(document.querySelector('#outside-heading')).display };
      })`,
    }, sessionId);
    assert.equal(exceptionDetails, undefined);
    const m = result.value;
    measurements.push(m);
    assert.equal(m.width, width, 'actual phone viewport');
    assert.ok(m.pageWidth <= width, 'page does not overflow horizontally');
    assert.equal(m.value, value, 'choice bytes preserved');
    assert.equal(m.choiceDisplay, 'inline', 'choice code stays in normal text flow');
    assert.ok(m.tokens.every(t => t.lines === 1), 'no code token breaks across lines');
    assert.ok(Math.abs(m.blockWidth - m.availableWidth) < 1, 'block spans full page content width');
    assert.ok(Math.abs(m.overflowWidth - m.availableWidth) < 1, 'overflow block spans full page content width');
    assert.ok(m.scrolls, 'wide code scrolls inside block');
    assert.equal(m.overflowCode, overflowCode, 'overflow token bytes preserved');
    assert.equal(m.code, code, 'code whitespace and bytes preserved');
    assert.equal(m.codeWhitespace, 'pre');
    assert.equal(m.literal, literal, 'literal fence bytes preserved');
    assert.equal(m.literalHeadings, 0);
    assert.equal(m.figSvg, 321, 'figure drawn at its height');
    assert.equal(m.figBox, 321, 'figure box shows the whole figure in height');
    assert.ok(m.tblRows > 0 && m.tblBox >= m.tblRows, 'table box shows every row in height');
    assert.ok(!m.tblScrollsY, 'table never scrolls vertically');
    assert.ok(!m.figScrollsY, 'figure never scrolls vertically');
    assert.equal(m.outsideHeadingDisplay, 'block');
  }
  console.log(JSON.stringify({ passed: true, measurements }));
} catch (error) {
  console.error(JSON.stringify({ passed: false, error: error.message, measurements }));
  process.exitCode = 1;
} finally {
  clearTimeout(bound);
  watcher?.close();
  socket?.close();
  if (browser && browser.exitCode === null) {
    const exited = new Promise(resolve => browser.once('exit', resolve));
    browser.kill('SIGTERM');
    await exited;
  }
  fs.rmSync(directory, { recursive: true, force: true });
}

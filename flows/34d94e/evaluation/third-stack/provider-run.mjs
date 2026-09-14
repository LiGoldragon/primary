#!/usr/bin/env node
// Explicitly authorized first-real-run driver. It does no provider discovery.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import https from 'node:https';
import {spawn} from 'node:child_process';

const EXPECTED = '1.17.13', MAX_REQUESTS = 24, CASE_TIMEOUT = 45_000, MAX_BODY = 2 * 1024 * 1024;
const here = path.dirname(new URL(import.meta.url).pathname);
const cases = JSON.parse(fs.readFileSync(path.join(here, 'fixtures/cases.json')));
const sources = JSON.parse(fs.readFileSync(path.join(here, 'fixtures/sources.json')));
const arg = name => { const i = process.argv.indexOf(name); return i < 0 ? undefined : process.argv[i + 1]; };
const required = ['--provider-descriptor', '--secret-fd', '--opencode', '--output'];
function fail(reason, code = 2) { process.stdout.write(JSON.stringify({status: 'provider-run-failed', reason}) + '\n'); process.exitCode = code; }
function envFor(home, config, apiKey) { return {HOME: home, PATH: process.env.PATH || '/usr/bin:/bin', LANG: process.env.LANG || 'C.UTF-8', LC_ALL: process.env.LC_ALL || 'C.UTF-8', XDG_CONFIG_HOME: path.join(home, 'config'), XDG_DATA_HOME: path.join(home, 'data'), XDG_STATE_HOME: path.join(home, 'state'), XDG_CACHE_HOME: path.join(home, 'cache'), OPENCODE_CONFIG: config, OPENAI_API_KEY: apiKey}; }
function readFd(fd) { return new Promise((resolve, reject) => { let data = ''; const stream = fs.createReadStream(null, {fd, autoClose: false}); stream.on('data', c => data += c); stream.on('end', () => resolve(data.trim())); stream.on('error', reject); }); }
function request(proxy, origin, secret, body) {
  return new Promise((resolve, reject) => {
    const target = new URL(origin); const req = https.request({hostname: target.hostname, port: target.port || 443, method: 'POST', path: target.pathname.replace(/\/$/, '') + '/v1/chat/completions', headers: {'content-type': 'application/json', authorization: `Bearer ${secret}`, 'content-length': Buffer.byteLength(body)}, rejectUnauthorized: true}, res => { let data = ''; res.on('data', c => { data += c; if (data.length > MAX_BODY) req.destroy(new Error('upstream response too large')); }); res.on('end', () => resolve({status: res.statusCode, headers: {'content-type': res.headers['content-type']}, body: data})); });
    req.on('error', reject); req.setTimeout(CASE_TIMEOUT, () => req.destroy(new Error('upstream timeout'))); req.end(body);
  });
}
async function main() {
  for (const name of required) if (!arg(name)) throw new Error(`${name} is required`);
  const descriptorPath = arg('--provider-descriptor'), binary = arg('--opencode'), output = arg('--output');
  if (!path.isAbsolute(binary) || !fs.existsSync(binary)) throw new Error('explicit OpenCode binary is absent');
  const descriptor = JSON.parse(fs.readFileSync(descriptorPath, 'utf8'));
  if (descriptor.access_authorized !== true) throw new Error('provider descriptor must set access_authorized:true');
  if (typeof descriptor.baseURL !== 'string' || !descriptor.baseURL.startsWith('https://')) throw new Error('provider descriptor baseURL must be HTTPS');
  const origin = new URL(descriptor.baseURL); if (origin.username || origin.password || origin.search || origin.hash) throw new Error('provider baseURL must not contain credentials or query data');
  if (!descriptor.model || descriptor.expected_opencode_version !== EXPECTED) throw new Error('descriptor model/version gate failed');
  const fd = Number(arg('--secret-fd')); if (!Number.isInteger(fd) || fd < 0) throw new Error('secret fd must be a nonnegative integer');
  if (process.env.PROVIDER_SECRET || process.env.OPENAI_API_KEY) throw new Error('provider secrets must not be supplied in environment');
  const outDir = path.resolve(output); fs.mkdirSync(outDir, {recursive: true});
  if (process.argv.includes('--dry-run')) { fs.writeFileSync(path.join(outDir, 'provider-run-dry.json'), JSON.stringify({schema: 'third-stack-provider-run-dry/v1', source_bundles: Object.keys(sources).length, cases: cases.map(({id, prompt}) => ({id, prompt})), hidden_expectations_injected: false}, null, 2) + '\n'); process.stdout.write(JSON.stringify({status: 'provider-run-dry-passed', cases: cases.length}) + '\n'); return; }
  const secret = await readFd(fd); if (!secret) throw new Error('secret fd was empty');
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'third-stack-provider-')), home = path.join(workspace, 'home'); fs.mkdirSync(path.join(home, 'config'), {recursive: true});
  let server, child, requests = 0;
  try {
    server = http.createServer((req, res) => {
      if (req.method !== 'POST' || req.url !== '/v1/chat/completions' || ++requests > MAX_REQUESTS) { res.writeHead(400); res.end('rejected'); return; }
      let body = ''; req.on('data', c => { body += c; if (body.length > MAX_BODY) req.destroy(); }); req.on('end', async () => { try { const result = await request(server, descriptor.baseURL, secret, body); res.writeHead(result.status || 502, {'content-type': result.headers['content-type'] || 'application/json'}); res.end(result.body); } catch (error) { res.writeHead(502, {'content-type': 'application/json'}); res.end(JSON.stringify({error: 'upstream request failed'})); } });
    });
    const port = await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', () => resolve(server.address().port)); });
    const config = path.join(home, 'config', 'opencode.json'); fs.writeFileSync(config, JSON.stringify({enabled_providers: ['fixture'], model: `fixture/${descriptor.model}`, small_model: `fixture/${descriptor.model}`, provider: {fixture: {npm: '@ai-sdk/openai-compatible', options: {baseURL: `http://127.0.0.1:${port}/v1`, apiKey: 'inert-local-only'}, models: {[descriptor.model]: {name: descriptor.model, reasoning: true, tool_call: true, interleaved: {field: 'reasoning_content'}}}}}, autoupdate: false, plugin: []}));
    const childEnv = envFor(home, config, 'inert-local-only'); child = spawn(binary, ['run', '--format', 'json', '--model', `fixture/${descriptor.model}`, cases.map(c => c.prompt).join('\n\n')], {cwd: workspace, env: childEnv, stdio: ['ignore', 'pipe', 'pipe']});
    let stdout = '', stderr = ''; child.stdout.on('data', c => stdout = (stdout + c).slice(-MAX_BODY)); child.stderr.on('data', c => stderr = (stderr + c).slice(-MAX_BODY));
    const result = await new Promise(resolve => { const timer = setTimeout(() => child.kill('SIGTERM'), CASE_TIMEOUT * cases.length); child.on('close', (code, signal) => { clearTimeout(timer); resolve({code, signal}); }); });
    if (result.code !== 0) throw new Error(`OpenCode exited ${result.code ?? result.signal}: ${stderr.slice(0, 300)}`);
    fs.writeFileSync(path.join(outDir, 'provider-run.json'), JSON.stringify({schema: 'third-stack-provider-run/v1', status: 'completed', source_bundles: Object.keys(sources).length, cases: cases.length, provider: descriptor.provider || origin.hostname, model: descriptor.model, harness: EXPECTED, requests, stdout, stderr: stderr ? '[redacted diagnostic]' : ''}, null, 2) + '\n');
    process.stdout.write(JSON.stringify({status: 'provider-run-completed', output: path.join(outDir, 'provider-run.json'), requests}) + '\n');
  } finally { if (child && child.exitCode === null) child.kill('SIGKILL'); if (server) await new Promise(resolve => server.close(resolve)); fs.rmSync(workspace, {recursive: true, force: true}); }
}
main().catch(error => fail(error.message));

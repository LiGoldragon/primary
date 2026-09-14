#!/usr/bin/env node
// Deterministic localhost replay witness. It never discovers, installs, or
// authenticates an OpenCode binary; callers must supply an absolute path.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';

const EXPECTED_VERSION = '1.17.13';
const SOURCE_COMMIT = '10c894bdeef3618f5666fb506ef7f9491bb964d8';
const FIXTURE_CONTENT = 'offline adapter fixture: known content\n';
const CHILD_TIMEOUT_MS = Number(process.env.OFFLINE_ADAPTER_TIMEOUT_MS) || 30_000;
const VERSION_TIMEOUT_MS = 5_000;
const MAX_OUTPUT = 512 * 1024;
const FAILURE_OUTPUT_LIMIT = 8 * 1024;
const REQUEST_TEXT_LIMIT = 512;
let failureDiagnostics = {};

function fail(message, code = 1, extra = {}) {
  process.stdout.write(JSON.stringify({status: 'adapter-witness-failed', reason: message, ...extra}) + '\n');
  process.exitCode = code;
}
function suppliedBinary() {
  const index = process.argv.indexOf('--opencode');
  if (index < 0 || !process.argv[index + 1] || !path.isAbsolute(process.argv[index + 1])) throw new Error('usage: offline-adapter.mjs --opencode /absolute/path/to/opencode');
  return process.argv[index + 1];
}
function allowlistedEnv(home, configHome) {
  return {HOME: home, PATH: process.env.PATH || '/usr/bin:/bin', LANG: process.env.LANG || 'C.UTF-8', LC_ALL: process.env.LC_ALL || 'C.UTF-8', XDG_CONFIG_HOME: configHome, XDG_DATA_HOME: path.join(home, 'data'), XDG_STATE_HOME: path.join(home, 'state'), XDG_CACHE_HOME: path.join(home, 'cache'), OPENCODE_CONFIG: path.join(configHome, 'opencode.json')};
}
function terminateGroup(child, signal) {
  if (!child?.pid) return;
  try {
    // Every child below is detached, so its pid is also its process-group ID.
    process.kill(-child.pid, signal);
  } catch (error) {
    if (error.code !== 'ESRCH') {
      try { child.kill(signal); } catch { /* The child may have exited between checks. */ }
    }
  }
}
function collect(child, timeoutMs) {
  let stdout = '', stderr = '', timedOut = false, settled = false;
  child.stdout?.on('data', chunk => { stdout = (stdout + chunk).slice(-MAX_OUTPUT); });
  child.stderr?.on('data', chunk => { stderr = (stderr + chunk).slice(-MAX_OUTPUT); });
  return new Promise(resolve => {
    let killTimer;
    const timer = setTimeout(() => {
      if (settled) return;
      timedOut = true;
      terminateGroup(child, 'SIGTERM');
      killTimer = setTimeout(() => { if (!settled) terminateGroup(child, 'SIGKILL'); }, 1_000);
      killTimer.unref();
    }, timeoutMs);
    const finish = result => {
      settled = true;
      clearTimeout(timer);
      clearTimeout(killTimer);
      resolve({...result, stdout, stderr, timedOut});
    };
    child.once('close', (code, signal) => finish({code, signal}));
    child.once('error', error => finish({code: null, signal: null, error}));
  });
}
function boundedText(value, limit = REQUEST_TEXT_LIMIT) { return String(value ?? '').slice(0, limit); }
function messageText(message) {
  if (typeof message?.content === 'string') return message.content;
  if (Array.isArray(message?.content)) return message.content.filter(item => typeof item?.text === 'string').map(item => item.text).join(' ');
  return '';
}
function requestSummary(body) {
  const messages = Array.isArray(body?.messages) ? body.messages : [];
  const firstUser = messages.find(message => message?.role === 'user');
  return {
    model: boundedText(body?.model, 128),
    tool_names: (Array.isArray(body?.tools) ? body.tools : []).map(tool => boundedText(tool?.function?.name, 128)).filter(Boolean),
    message_roles: messages.map(message => boundedText(message?.role, 64)),
    first_user_text: boundedText(messageText(firstUser)),
  };
}
function recordFailureDiagnostics(stage, result, context) {
  failureDiagnostics = {
    stage,
    request_count: context.requests.length,
    replay_request_count: context.replayRequests.length,
    protocol_failure: context.protocolFailure?.message,
    request_summaries: context.requests.map(requestSummary),
    endpoint_counts: context.endpointCounts,
    status_counts: context.statusCounts,
    child: {
      code: result.code,
      signal: result.signal,
      timed_out: result.timedOut,
      stdout: result.stdout.slice(-FAILURE_OUTPUT_LIMIT),
      stderr: result.stderr.slice(-FAILURE_OUTPUT_LIMIT),
    },
  };
}
async function checkVersion(binary, env, record) {
  let child;
  try { child = spawn(binary, ['--version'], {env, stdio: ['ignore', 'pipe', 'pipe'], detached: true}); } catch (error) { throw new Error(`could not start OpenCode for --version: ${error.message}`); }
  let result;
  try { result = await collect(child, VERSION_TIMEOUT_MS); } finally { terminateGroup(child, 'SIGKILL'); }
  record(result);
  if (result.timedOut) throw new Error('OpenCode --version timed out');
  if (result.error) throw new Error(`could not start OpenCode for --version: ${result.error.message}`);
  const text = `${result.stdout}\n${result.stderr}`;
  if (result.code !== 0) throw new Error(`OpenCode --version exited ${result.code}: ${text.slice(0, 300)}`);
  const match = text.match(/(?:^|[^0-9])(?:v)?(\d+\.\d+\.\d+)(?:[^0-9]|$)/);
  if (!match || match[1] !== EXPECTED_VERSION) throw new Error(`expected OpenCode ${EXPECTED_VERSION}, got ${text.trim().slice(0, 300)}`);
  return match[1];
}
async function closeServer(server) {
  server.closeAllConnections();
  await new Promise(resolve => server.close(() => resolve()));
}
function recordCount(counts, key) { counts[key] = (counts[key] || 0) + 1; }
function dataEvents(res, events, statusCounts) {
  recordCount(statusCounts, '200');
  res.writeHead(200, {'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'close'});
  for (const event of events) res.write(`${event === '[DONE]' ? 'data: [DONE]' : `data: ${JSON.stringify(event)}`}\n\n`);
  res.end();
}
function assistant(body) { return [...(body?.messages || [])].reverse().find(message => message?.role === 'assistant'); }
function validateFirst(body, fixture) {
  const readTool = (body?.tools || []).find(tool => tool?.type === 'function' && tool?.function?.name === 'read');
  if (!readTool?.function?.parameters?.properties?.filePath) throw new Error('first request did not declare the read tool with filePath schema');
  if (!JSON.stringify(body?.messages || []).includes('fixture.txt')) throw new Error('first request did not ask to read fixture.txt');
  return fixture;
}
function validateSecond(body, fixture) {
  const message = assistant(body);
  if (message?.reasoning_content !== 'fixture reasoning') throw new Error('second request lost assistant reasoning_content');
  const call = message?.tool_calls?.find(item => item?.function?.name === 'read');
  if (!call || call.id !== 'call_fixture' || call.function?.arguments !== JSON.stringify({filePath: fixture})) throw new Error('second request changed or lost native read tool call');
  const tool = (body.messages || []).find(item => item?.role === 'tool' && item.tool_call_id === 'call_fixture');
  const toolText = typeof tool?.content === 'string' ? tool.content : JSON.stringify(tool?.content || '');
  if (!tool || !toolText.includes(FIXTURE_CONTENT.trim())) throw new Error('second request lacked matching tool result content');
}
function isToolReplayStart(body) {
  return (body?.tools || []).some(tool => tool?.type === 'function' && tool?.function?.name === 'read');
}
function isToolReplayContinuation(body) {
  return assistant(body)?.tool_calls?.some(call => call?.id === 'call_fixture' && call?.function?.name === 'read');
}
async function main() {
  let binary;
  try { binary = suppliedBinary(); } catch (error) { fail(error.message, 2); return; }
  if (!fs.existsSync(binary)) { fail('explicit OpenCode binary is absent', 2, {binary}); return; }
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'third-stack-opencode-'));
  const home = path.join(workspace, 'home'), configHome = path.join(home, 'config'), fixture = path.join(workspace, 'fixture.txt');
  fs.mkdirSync(configHome, {recursive: true}); fs.writeFileSync(fixture, FIXTURE_CONTENT);
  const env = allowlistedEnv(home, configHome), requests = [], replayRequests = [], endpointCounts = {}, statusCounts = {};
  let server, child, protocolFailure;
  const diagnosticsContext = {requests, replayRequests, endpointCounts, statusCounts, get protocolFailure() { return protocolFailure; }};
  try {
    server = http.createServer((req, res) => {
      let body = ''; req.setEncoding('utf8');
      req.on('data', chunk => { body += chunk; if (body.length > MAX_OUTPUT) req.destroy(); });
      req.on('error', error => { if (!res.headersSent) { recordCount(statusCounts, '400'); res.writeHead(400); } res.end(String(error)); });
      req.on('end', () => {
        try {
          recordCount(endpointCounts, `${req.method} ${req.url}`);
          if (req.url !== '/v1/chat/completions' || req.method !== 'POST') { recordCount(statusCounts, '404'); res.writeHead(404); res.end(); return; }
          const json = JSON.parse(body); requests.push(json);
          if (isToolReplayStart(json)) {
            replayRequests.push(json);
            validateFirst(json, fixture);
            return dataEvents(res, [
              {choices: [{index: 0, delta: {role: 'assistant', reasoning_content: 'fixture reasoning'}}]},
              {choices: [{index: 0, delta: {tool_calls: [{index: 0, id: 'call_fixture', type: 'function', function: {name: 'read', arguments: JSON.stringify({filePath: fixture})}}]}}]},
              {choices: [{index: 0, delta: {}, finish_reason: 'tool_calls'}]},
              '[DONE]',
            ], statusCounts);
          }
          if (isToolReplayContinuation(json)) {
            replayRequests.push(json);
            validateSecond(json, fixture);
            return dataEvents(res, [{choices: [{index: 0, delta: {role: 'assistant', content: 'fixture stop'}}]}, {choices: [{index: 0, delta: {}, finish_reason: 'stop'}]}, '[DONE]'], statusCounts);
          }
          // OpenCode may ask its configured small model for an auxiliary title.
          dataEvents(res, [{choices: [{index: 0, delta: {role: 'assistant', content: 'fixture auxiliary'}}]}, {choices: [{index: 0, delta: {}, finish_reason: 'stop'}]}, '[DONE]'], statusCounts);
        } catch (error) { protocolFailure = error; recordCount(statusCounts, '500'); res.writeHead(500, {'content-type': 'text/plain'}); res.end(error.message); }
      });
    });
    const port = await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', () => resolve(server.address().port)); });
    fs.writeFileSync(env.OPENCODE_CONFIG, JSON.stringify({enabled_providers: ['fixture'], model: 'fixture/fixture', small_model: 'fixture/fixture', provider: {fixture: {npm: '@ai-sdk/openai-compatible', options: {baseURL: `http://127.0.0.1:${port}/v1`}, models: {fixture: {name: 'fixture', reasoning: true, tool_call: true, interleaved: {field: 'reasoning_content'}}}}}, autoupdate: false, plugin: []}));
    const version = await checkVersion(binary, env, result => recordFailureDiagnostics('version', result, diagnosticsContext));
    child = spawn(binary, ['run', '--format', 'json', '--model', 'fixture/fixture', 'Read fixture.txt'], {cwd: workspace, env, stdio: ['ignore', 'pipe', 'pipe'], detached: true});
    const result = await collect(child, CHILD_TIMEOUT_MS);
    recordFailureDiagnostics('run', result, diagnosticsContext);
    if (result.timedOut) throw new Error('OpenCode subprocess timed out and was killed');
    if (result.error) throw new Error(`OpenCode subprocess failed to start: ${result.error.message}`);
    if (result.code !== 0) throw new Error(`OpenCode exited ${JSON.stringify({code: result.code, signal: result.signal})}: ${result.stderr.slice(0, 500)}`);
    if (protocolFailure) throw new Error(`fake provider protocol assertion failed: ${protocolFailure.message}`);
    if (replayRequests.length !== 2) throw new Error(`expected exactly two tool replay requests, received ${replayRequests.length} among ${requests.length} total requests`);
    const realBinary = fs.realpathSync(binary);
    const binarySha256 = crypto.createHash('sha256').update(fs.readFileSync(realBinary)).digest('hex');
    process.stdout.write(JSON.stringify({status: 'adapter-replay-passed', opencode_version: version, expected_source_commit: SOURCE_COMMIT, binary_path: realBinary, binary_sha256: binarySha256, requests: requests.length, replay_requests: replayRequests.length, endpoint_counts: endpointCounts, status_counts: statusCounts, provider_calls: 0, model_downloads: 0}) + '\n');
  } finally {
    terminateGroup(child, 'SIGKILL');
    if (server) await closeServer(server);
    fs.rmSync(workspace, {recursive: true, force: true});
  }
}
main().catch(error => fail(error.message, 1, {expected_source_commit: SOURCE_COMMIT, ...failureDiagnostics}));

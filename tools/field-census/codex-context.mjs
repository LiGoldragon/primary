import { createHash, randomBytes } from 'node:crypto';
import { open } from 'node:fs/promises';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const DEFAULT_SOCKET = path.join(os.homedir(), '.codex/app-server-control/app-server-control.sock');
const MAX_MESSAGE_BYTES = 256 * 1024;

function deadline(ms) {
  return AbortSignal.timeout(ms);
}

function websocketFrame(message) {
  const body = Buffer.from(JSON.stringify(message));
  const mask = randomBytes(4);
  const header = body.length < 126 ? Buffer.from([0x81, 0x80 | body.length])
    : Buffer.from([0x81, 0xfe, body.length >> 8, body.length & 255]);
  const masked = Buffer.from(body);
  for (let i = 0; i < masked.length; i++) masked[i] ^= mask[i % 4];
  return Buffer.concat([header, mask, masked]);
}

// The managed app-server socket speaks WebSocket over Unix, not raw JSONL.
async function readThreadMetadata(threadId, socketPath, timeoutMs) {
  const signal = deadline(timeoutMs);
  const socket = net.createConnection(socketPath);
  let buffer = Buffer.alloc(0);
  let upgraded = false;
  let initialized = false;
  const key = randomBytes(16).toString('base64');
  const expectedAccept = createHash('sha1')
    .update(`${key}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)
    .digest('base64');
  try {
    return await new Promise((resolve, reject) => {
      const fail = (error) => { socket.destroy(); reject(error); };
      const finish = (value) => { socket.destroy(); resolve(value); };
      signal.addEventListener('abort', () => fail(new Error('app-server timeout')), { once: true });
      socket.once('error', fail);
      socket.once('connect', () => socket.write(
        `GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`,
      ));
      socket.on('data', (chunk) => {
        buffer = Buffer.concat([buffer, chunk]);
        if (buffer.length > MAX_MESSAGE_BYTES) return fail(new Error('app-server response too large'));
        if (!upgraded) {
          const end = buffer.indexOf('\r\n\r\n');
          if (end < 0) return;
          const header = buffer.subarray(0, end).toString();
          if (!header.startsWith('HTTP/1.1 101') ||
              !header.toLowerCase().includes(`sec-websocket-accept: ${expectedAccept.toLowerCase()}`)) {
            return fail(new Error('app-server WebSocket upgrade rejected'));
          }
          buffer = buffer.subarray(end + 4);
          upgraded = true;
          socket.write(websocketFrame({
            id: 1, method: 'initialize',
            params: { clientInfo: { name: 'field-census', version: '0.1' } },
          }));
        }
        while (buffer.length >= 2) {
          const opcode = buffer[0] & 15;
          const masked = Boolean(buffer[1] & 128);
          let length = buffer[1] & 127;
          let headerLength = 2;
          if (length === 126) {
            if (buffer.length < 4) return;
            length = buffer.readUInt16BE(2); headerLength = 4;
          } else if (length === 127) return fail(new Error('app-server frame too large'));
          const maskLength = masked ? 4 : 0;
          if (length > MAX_MESSAGE_BYTES) return fail(new Error('app-server frame too large'));
          if (buffer.length < headerLength + maskLength + length) return;
          const payload = buffer.subarray(headerLength + maskLength, headerLength + maskLength + length);
          buffer = buffer.subarray(headerLength + maskLength + length);
          if (opcode !== 1) continue;
          let response;
          try { response = JSON.parse(payload.toString()); }
          catch { return fail(new Error('invalid app-server response')); }
          if (response.id === 1 && !initialized) {
            if (response.error) return fail(new Error(`app-server initialize: ${response.error.message}`));
            initialized = true;
            socket.write(websocketFrame({ method: 'initialized', params: {} }));
            socket.write(websocketFrame({
              id: 2, method: 'thread/read', params: { threadId, includeTurns: false },
            }));
          } else if (response.id === 2) {
            if (response.error) return fail(new Error(`app-server thread/read: ${response.error.message}`));
            return finish(response.result?.thread);
          }
        }
      });
      socket.once('close', () => { if (!signal.aborted) reject(new Error('app-server connection closed')); });
    });
  } finally { socket.destroy(); }
}

export async function latestCodexTokenEvent(rolloutPath, { maxTailBytes = 1024 * 1024 } = {}) {
  const file = await open(rolloutPath, 'r');
  try {
    const stat = await file.stat();
    const boundedBytes = Number.isSafeInteger(maxTailBytes) && maxTailBytes > 0
      ? Math.min(maxTailBytes, 2 * 1024 * 1024) : 1024 * 1024;
    const length = Math.min(stat.size, boundedBytes);
    const start = stat.size - length;
    const bytes = Buffer.alloc(length);
    const { bytesRead } = await file.read(bytes, 0, length, start);
    const lines = bytes.subarray(0, bytesRead).toString().split('\n');
    if (start > 0) lines.shift(); // first line may start mid-record
    let tokenCount = null;
    let usageRecord = null;
    for (let i = lines.length - 1; i >= 0; i--) {
      let record;
      try { record = JSON.parse(lines[i]); } catch { continue; }
      if (!usageRecord && record.type === 'token_usage_record' &&
          record.payload?.thread_token_usage && record.payload?.usage) usageRecord = record;
      if (!tokenCount && record.type === 'event_msg' &&
          record.payload?.type === 'token_count' && record.payload.info) tokenCount = record;
      if (usageRecord && tokenCount) break;
    }
    return { eventAt: usageRecord?.timestamp ?? tokenCount?.timestamp ?? null,
      usageRecordAt: usageRecord?.timestamp ?? null, tokenCountAt: tokenCount?.timestamp ?? null,
      info: tokenCount?.payload.info ?? null, usageRecord: usageRecord?.payload ?? null,
      rateLimits: tokenCount?.payload.rate_limits ?? null,
      fileMtime: stat.mtime.toISOString(), bytesExamined: bytesRead, tailTruncated: start > 0 };
  } finally { await file.close(); }
}

function tokens(raw) {
  if (!raw) return null;
  const names = ['input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
    'output_tokens', 'reasoning_output_tokens', 'total_tokens'];
  const out = {};
  for (const name of names) {
    const value = raw[name];
    out[name.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())] =
      Number.isSafeInteger(value) && value >= 0 ? value : null;
  }
  return out;
}

export async function collectCodexContext({ nativeThreadId, socketPath = DEFAULT_SOCKET,
  rolloutPath = null, timeoutMs = 1500, maxTailBytes = 1024 * 1024 } = {}) {
  if (typeof nativeThreadId !== 'string' || !/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(nativeThreadId)) {
    throw new TypeError('nativeThreadId must be an exact UUID');
  }
  const observedAt = new Date().toISOString();
  const errors = [];
  let thread = null;
  try { thread = await readThreadMetadata(nativeThreadId, socketPath, timeoutMs); }
  catch (error) { errors.push({ source: 'app-server', message: error.message }); }
  if (thread?.id && thread.id !== nativeThreadId) {
    errors.push({ source: 'app-server', message: 'thread ID mismatch' });
    thread = null;
  }
  const exactPath = thread?.path ?? rolloutPath;
  if (exactPath && !path.basename(exactPath).endsWith(`-${nativeThreadId}.jsonl`)) {
    errors.push({ source: 'rollout', message: 'rollout path does not match thread ID' });
  }
  let event = null;
  if (exactPath && path.basename(exactPath).endsWith(`-${nativeThreadId}.jsonl`)) {
    try { event = await latestCodexTokenEvent(exactPath, { maxTailBytes }); }
    catch (error) { errors.push({ source: 'rollout', message: error.message }); }
  }
  const info = event?.info;
  const window = Number.isSafeInteger(info?.model_context_window) ? info.model_context_window : null;
  const lastUsage = event?.usageRecord?.usage ?? info?.last_token_usage;
  const totalUsage = event?.usageRecord?.thread_token_usage ?? info?.total_token_usage;
  const lastInput = Number.isSafeInteger(lastUsage?.input_tokens) ? lastUsage.input_tokens : null;
  const ageMs = event?.eventAt ? Math.max(0, Date.parse(observedAt) - Date.parse(event.eventAt)) : null;
  return {
    source: 'codex', method: thread ? 'app-server-thread-read+rollout-tail' : 'rollout-tail-fallback',
    observedAt, eventAt: event?.eventAt ?? null, nativeThreadId,
    occupancy: { status: lastInput === null ? 'unknown' : 'last-input-proxy',
      exactTokens: null, lastInputTokens: lastInput, modelContextWindow: window,
      remainingExactTokens: null,
      remainingEstimateTokens: window !== null && lastInput !== null ? Math.max(0, window - lastInput) : null },
    usage: { scope: 'thread-cumulative', total: tokens(totalUsage), last: tokens(lastUsage),
      turn: tokens(event?.usageRecord?.turn_token_usage),
      source: event?.usageRecord ? 'token_usage_record' : info ? 'token_count' : null },
    quota: event?.rateLimits ? { scope: 'account', source: 'rollout-event',
      limitId: event.rateLimits.limit_id ?? null,
      primary: event.rateLimits.primary ?? null, secondary: event.rateLimits.secondary ?? null,
      planType: event.rateLimits.plan_type ?? null } : null,
    freshness: { ageMs: Number.isFinite(ageMs) ? ageMs : null,
      threadUpdatedAt: Number.isFinite(thread?.updatedAt) ? new Date(thread.updatedAt * 1000).toISOString() : null,
      fileMtime: event?.fileMtime ?? null, bytesExamined: event?.bytesExamined ?? 0,
      tailTruncated: event?.tailTruncated ?? null, threadStatus: thread?.status?.type ?? null,
      exactBinding: Boolean(thread?.id === nativeThreadId && thread?.path),
      usageRecordAt: event?.usageRecordAt ?? null, tokenCountAt: event?.tokenCountAt ?? null },
    errors,
  };
}

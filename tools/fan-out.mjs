#!/usr/bin/env node
/* Fan-out message delivery: one source, multiple endpoints, no LLM replication. */
import fs from 'node:fs';
import net from 'node:net';
import crypto from 'node:crypto';
import childProcess from 'node:child_process';

const usage = `usage:
  fan-out deliver --source FILE --message-id ID --endpoints ENDPOINTS_JSON`;

const args = process.argv.slice(2);
const command = args.shift();
const option = (name, required = true) => {
  const i = args.indexOf(name);
  if (i < 0) {
    if (required) throw new Error(`missing ${name}`);
    return undefined;
  }
  const value = args[i + 1];
  if (value === undefined) throw new Error(`missing value for ${name}`);
  args.splice(i, 2);
  return value;
};

const sha256 = text => crypto.createHash('sha256').update(text, 'utf8').digest('hex');

function textContent(content) {
  if (typeof content === 'string') return content;
  if (Array.isArray(content) && content.every(p => p && p.type === 'text' && typeof p.text === 'string')) {
    return content.map(p => p.text).join('');
  }
  return null;
}

function findMessage(source, messageId) {
  const lines = fs.readFileSync(source, 'utf8').split(/\n/).filter(Boolean);
  for (const line of lines) {
    let record;
    try {
      record = JSON.parse(line);
    } catch {
      throw new Error('source contains invalid JSONL');
    }

    // Match Claude user messages
    if (record.type === 'user' && (record.uuid === messageId || record.promptId === messageId)) {
      const text = textContent(record.message?.content);
      if (text !== null) {
        return {
          id: messageId,
          text,
          format: 'claude',
          timestamp: record.timestamp,
        };
      }
    }

    // Match Codex messages
    const item = record.item ?? record.payload?.item ?? record;
    if (item?.id === messageId && item.type === 'message' && item.role === 'user') {
      const content = item.content ?? record.content ?? record.payload?.content;
      const text = textContent(content);
      if (text !== null) {
        return {
          id: messageId,
          text,
          format: 'codex',
          timestamp: record.timestamp,
        };
      }
    }

    // Match Codex rollouts
    if (record.type === 'event_msg' && record.payload?.type === 'item_completed') {
      const rollout = record.payload?.item;
      if (rollout?.id === messageId && rollout.type === 'UserMessage') {
        const text = textContent(rollout.content);
        if (text !== null) {
          return {
            id: messageId,
            text,
            format: 'codex-rollout',
            timestamp: record.timestamp,
          };
        }
      }
    }
  }
  throw new Error(`message ${messageId} not found in source`);
}

function receipt(kind, value) {
  process.stdout.write(JSON.stringify({ kind, ...value }) + '\n');
}

function websocketFrame(payload, opcode = 0x1) {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(payload);
  const mask = crypto.randomBytes(4);
  let header;
  if (body.length < 126) {
    header = Buffer.from([0x80 | opcode, 0x80 | body.length]);
  } else if (body.length < 65536) {
    header = Buffer.from([0x80 | opcode, 0xfe, body.length >> 8, body.length & 255]);
  } else {
    header = Buffer.alloc(10);
    header[0] = 0x80 | opcode;
    header[1] = 0xff;
    header.writeBigUInt64BE(BigInt(body.length), 2);
  }
  const out = Buffer.alloc(body.length);
  for (let i = 0; i < body.length; i++) {
    out[i] = body[i] ^ mask[i % 4];
  }
  return Buffer.concat([header, mask, out]);
}

async function deliverToCodex(socketPath, threadId, messageText) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(socketPath);
    let buffer = Buffer.alloc(0),
      upgraded = false,
      sequence = 0,
      fragment = null;
    const pending = new Map();

    const fail = error => {
      socket.destroy();
      reject(error);
    };

    const call = (method, params) =>
      new Promise((ok, no) => {
        const id = ++sequence;
        const timer = setTimeout(() => {
          pending.delete(id);
          no(new Error(`Codex RPC timeout: ${method}`));
        }, 10_000);
        pending.set(id, { ok, no, timer });
        socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', id, method, params })));
      });

    const frame = (fin, opcode, body) => {
      if (opcode === 0x9) {
        socket.write(websocketFrame(body, 0xa));
        return;
      }
      if (opcode === 0x8) return fail(new Error('Codex websocket closed'));
      if (opcode === 0x1) fragment = body;
      else if (opcode === 0x0 && fragment) fragment = Buffer.concat([fragment, body]);
      else return;
      if (!fin) return;
      const message = JSON.parse(fragment.toString());
      fragment = null;
      const waiter = pending.get(message.id);
      if (waiter) {
        pending.delete(message.id);
        clearTimeout(waiter.timer);
        message.error ? waiter.no(new Error(JSON.stringify(message.error))) : waiter.ok(message.result ?? message);
      }
    };

    const parse = () => {
      while (buffer.length >= 2) {
        const fin = Boolean(buffer[0] & 128),
          opcode = buffer[0] & 15;
        let length = buffer[1] & 127,
          offset = 2;
        if (length === 126) {
          if (buffer.length < 4) return;
          length = buffer.readUInt16BE(2);
          offset = 4;
        } else if (length === 127) {
          if (buffer.length < 10) return;
          const big = buffer.readBigUInt64BE(2);
          if (big > BigInt(Number.MAX_SAFE_INTEGER)) return fail(new Error('Codex frame too large'));
          length = Number(big);
          offset = 10;
        }
        if (buffer.length < offset + length) return;
        const body = buffer.subarray(offset, offset + length);
        buffer = buffer.subarray(offset + length);
        frame(fin, opcode, body);
      }
    };

    const start = async () => {
      try {
        await call('initialize', { clientInfo: { name: 'fan-out', version: '1' } });
        socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', method: 'initialized', params: {} })));
        await call('thread/resume', { threadId, excludeTurns: true });
        const result = await call('turn/start', {
          threadId,
          input: [{ type: 'text', text: messageText }],
        });
        const turn = result.turn ?? result.result?.turn ?? {};
        resolve({ turn_id: turn.id ?? null, status: turn.status ?? null });
        socket.end();
      } catch (error) {
        fail(error);
      }
    };

    socket.setTimeout(10_000, () => fail(new Error('Codex socket timeout')));
    socket.on('error', fail);
    socket.on('connect', () =>
      socket.write(
        'GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'
      )
    );
    socket.on('data', data => {
      buffer = Buffer.concat([buffer, data]);
      if (!upgraded) {
        const end = buffer.indexOf('\r\n\r\n');
        if (end < 0) return;
        const header = buffer.subarray(0, end).toString();
        const accept = header.match(/sec-websocket-accept:\s*([^\r\n]+)/i)?.[1]?.trim();
        const expected = crypto
          .createHash('sha1')
          .update('dGhlIHNhbXBsZSBub25jZQ==258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
          .digest('base64');
        if (!header.startsWith('HTTP/1.1 101') || !/upgrade:\s*websocket/i.test(header) || accept !== expected) {
          return fail(new Error('Codex websocket upgrade refused'));
        }
        buffer = buffer.subarray(end + 4);
        upgraded = true;
        void start();
      }
      parse();
    });
  });
}

async function deliverToClaudeSession(sessionShort, messageText) {
  const agents = JSON.parse(childProcess.execFileSync(process.env.FAN_OUT_CLAUDE_AGENTS ?? 'claude', ['agents', '--json'], { encoding: 'utf8' }));
  const matches = agents.filter(agent => String(agent.id ?? agent.sessionId ?? '').startsWith(sessionShort));
  if (matches.length !== 1 || matches[0].status !== 'idle') {
    throw new Error(`Claude delivery refused: session ${sessionShort} is not uniquely witnessed idle`);
  }
  const session = matches[0];
  const base = `/tmp/cc-daemon-${process.getuid()}`;
  const controls = process.env.FAN_OUT_CLAUDE_CONTROL_SOCKET
    ? [process.env.FAN_OUT_CLAUDE_CONTROL_SOCKET]
    : fs
        .readdirSync(base, { withFileTypes: true })
        .map(entry => `${base}/${entry.name}/control.sock`)
        .filter(fs.existsSync);
  if (controls.length !== 1) throw new Error('Claude delivery refused: daemon control socket is not uniquely discoverable');
  const key = fs
    .readFileSync(process.env.FAN_OUT_CLAUDE_CONTROL_KEY ?? `${process.env.HOME}/.claude/daemon/control.key`, 'utf8')
    .trim();
  const body = Buffer.from(messageText, 'utf8');
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(controls[0]);
    let response = '';
    socket.setTimeout(4000);
    socket.on('timeout', () => reject(new Error('Claude attach timed out')));
    socket.on('error', reject);
    socket.on('connect', () =>
      socket.write(
        JSON.stringify({
          proto: 1,
          op: 'attach',
          short: session.id ?? session.sessionId,
          auth: key,
          cols: 120,
          rows: 40,
          attachId: crypto.randomBytes(8).toString('hex'),
          caps: { imark: false, terminal: 'xterm', mux: null, ssh: false },
        }) + '\n'
      )
    );
    socket.on('data', data => {
      response += data.toString();
      if (!response.includes('\n')) return;
      if (!response.split('\n', 1)[0].includes('"ok":true')) return reject(new Error('Claude attach refused'));
      const pasted = Buffer.concat([Buffer.from('\x1b[200~'), body, Buffer.from('\x1b[201~\r')]);
      socket.write(pasted, error => {
        if (error) return reject(error);
        resolve({ session_id: session.id ?? sessionShort });
        socket.end();
      });
    });
  });
}

async function main() {
  try {
    if (!command || command === '--help' || command === 'help') {
      console.log(usage);
      process.exit(0);
    }

    if (command !== 'deliver') {
      throw new Error(`unknown command ${command}`);
    }

    const source = option('--source');
    const messageId = option('--message-id');
    const endpointsJson = option('--endpoints');
    let endpoints;
    try {
      endpoints = JSON.parse(endpointsJson);
    } catch {
      throw new Error('--endpoints must be valid JSON');
    }
    if (!Array.isArray(endpoints)) {
      throw new Error('--endpoints must be a JSON array');
    }

    const message = findMessage(source, messageId);

    const results = [];
    for (const endpoint of endpoints) {
      try {
        if (endpoint.type === 'codex-thread') {
          const result = await deliverToCodex(
            endpoint.socket ?? `${process.env.HOME}/.codex/app-server-control/app-server-control.sock`,
            endpoint.id,
            message.text
          );
          results.push({
            endpoint_type: endpoint.type,
            endpoint_id: endpoint.id,
            status: 'delivered',
            codex_turn_id: result.turn_id,
            codex_status: result.status,
          });
        } else if (endpoint.type === 'claude-session') {
          const result = await deliverToClaudeSession(endpoint.id, message.text);
          results.push({
            endpoint_type: endpoint.type,
            endpoint_id: endpoint.id,
            status: 'delivered',
            claude_session_id: result.session_id,
          });
        } else {
          results.push({
            endpoint_type: endpoint.type,
            endpoint_id: endpoint.id,
            status: 'unsupported',
            error: 'endpoint type not supported',
          });
        }
      } catch (error) {
        results.push({
          endpoint_type: endpoint.type,
          endpoint_id: endpoint.id,
          status: 'failed',
          error: error.message,
        });
      }
    }

    receipt('fan-out-complete', {
      message_id: messageId,
      message_text_bytes: Buffer.byteLength(message.text, 'utf8'),
      endpoints_count: endpoints.length,
      results,
    });
  } catch (error) {
    receipt('refused', { error: error.message });
    process.exitCode = 2;
  }
}

main().catch(err => {
  receipt('refused', { error: err.message });
  process.exitCode = 2;
});

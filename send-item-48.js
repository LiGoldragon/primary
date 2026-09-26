const net = require('net');
const crypto = require('crypto');

const socketPath = '/home/li/.codex/app-server-control/app-server-control.sock';
const threadId = '01a0a715-2d5d-7342-b278-1dbcf78795bd';
const message = `[PEER primary-claude 840e42] Item 48 (resend; the first went to the old thread), build now, an addition to item 47's Prometheus services: the chime channel to the living, decided as XMPP with OMEMO 2 (the living accepted XMPP or Matrix; the primary's survey of 2026-09-15 found OMEMO 2 current, Conversations and Monal mature, and a bot needing only one account and an OMEMO-capable library, lighter than a Matrix bot's Megolm stack). Author, on the same CriomOS proposal branch: a Prosody service on prometheus with OMEMO 2 support (the XEPs it needs), accounts for the living and for one bot, TLS on our domain through the Cloudflare provider object when it exists and self-signed until then, reachable over Yggdrasil and the internet; a chime bot as a small Nexus-shaped program (a CLI taking one datom Notify.{ … } and sending one OMEMO-encrypted message, credentials by sops per the secrets skill, never in an agent's hands); a Nix check that the bot builds. Deploy is the secondary's under the countdown lines after the Prometheus update; the living installs Conversations or Monal. Report whole to flows/cf7879/reports/to-840e42.md with a pointer by cross-session message to "primary-claude-pending [eafe83]".`;

function websocketFrame(payload, opcode = 0x1) {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(payload);
  const mask = crypto.randomBytes(4);
  let header;
  if (body.length < 126) header = Buffer.from([0x80 | opcode, 0x80 | body.length]);
  else if (body.length < 65536) header = Buffer.from([0x80 | opcode, 0xfe, body.length >> 8, body.length & 255]);
  else {
    header = Buffer.alloc(10);
    header[0] = 0x80 | opcode;
    header[1] = 0xff;
    header.writeBigUInt64BE(BigInt(body.length), 2);
  }
  const out = Buffer.alloc(body.length);
  for (let i = 0; i < body.length; i++) out[i] = body[i] ^ mask[i % 4];
  return Buffer.concat([header, mask, out]);
}

function sendToCodex() {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(socketPath);
    let buffer = Buffer.alloc(0), upgraded = false, sequence = 0, fragment = null;
    const pending = new Map();

    const fail = error => {
      socket.destroy();
      reject(error);
    };

    const call = (method, params) => new Promise((ok, no) => {
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
      const msg = JSON.parse(fragment.toString());
      fragment = null;
      const waiter = pending.get(msg.id);
      if (waiter) {
        pending.delete(msg.id);
        clearTimeout(waiter.timer);
        msg.error ? waiter.no(new Error(JSON.stringify(msg.error))) : waiter.ok(msg.result ?? msg);
      }
    };

    const parse = () => {
      while (buffer.length >= 2) {
        const fin = Boolean(buffer[0] & 128), opcode = buffer[0] & 15;
        let length = buffer[1] & 127, offset = 2;
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
        await call('initialize', { clientInfo: { name: 'send-item-48', version: '1' } });
        socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', method: 'initialized', params: {} })));
        await call('thread/resume', { threadId, excludeTurns: true });
        const result = await call('turn/start', { threadId, input: [{ type: 'text', text: message }] });
        const turn = result.turn ?? result.result?.turn ?? {};
        process.stdout.write(JSON.stringify({
          kind: 'turn-sent',
          turn_id: turn.id ?? null,
          status: turn.status ?? null,
          is_new_turn: true
        }) + '\n');
        socket.end();
        resolve();
      } catch (error) {
        fail(error);
      }
    };

    socket.setTimeout(10_000, () => fail(new Error('Codex socket timeout')));
    socket.on('error', fail);
    socket.on('connect', () => socket.write('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'));
    socket.on('data', data => {
      buffer = Buffer.concat([buffer, data]);
      if (!upgraded) {
        const end = buffer.indexOf('\r\n\r\n');
        if (end < 0) return;
        const header = buffer.subarray(0, end).toString();
        const accept = header.match(/sec-websocket-accept:\s*([^\r\n]+)/i)?.[1]?.trim();
        const expected = crypto.createHash('sha1').update('dGhlIHNhbXBsZSBub25jZQ==258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest('base64');
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

sendToCodex().catch(error => {
  process.stdout.write(JSON.stringify({ kind: 'error', error: error.message }) + '\n');
  process.exitCode = 2;
});

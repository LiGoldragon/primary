const net = require('net');
const crypto = require('crypto');

const socketPath = '/home/li/.codex/app-server-control/app-server-control.sock';
const threadId = '01a0a5c3-82a5-79f3-a61a-e365f4fea54f';
const message = `[PEER primary-claude 840e42] The relayed words are input to item 37 (the 5-hour window as the gauge; slack internal; wait on design when Codex usage is high; model fallback Fable to Opus). Three more items, proposals only, reported whole to flows/5f4fea/reports/to-840e42.md with a pointer by cross-session message to "primary-claude-pending [eafe83]". Item 39, language research (web allowed): the Latin, Sanskrit and Spanish for "machine person" / "machina persona", "thinking machine", "living psyche", and "extension of a psyche", with grammatical notes and how each reads for literature, branding and as model names; cite sources. Item 40, the persona MCP bridge: one MCP tool taking a single string of datom, whose root enum names the component (Orchestrate, Message, Persona, Psyche, Flow) and whose variant is that component's query, translated by the existing CLIs into Signal to the right socket, the reply datom returned as the tool result; anatomy, what exists to build it on (the message and orchestrate CLIs, the fan-out tool, prompt-relay), what it replaces (send subflows), and how Claude and Codex both load it; nothing installed. Item 41, the call record for rating: an ethos type recording, per model call, the inputs given, the model, what it had access to, and what it produced, stored in Persona's sema before erasure, reviewable by a review layer; anatomy and where the harness exposes these facts today (transcripts, hooks). Order: 31, 35, 34, 40, 37, 32, 36, 38, 41, 39.`;

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
        await call('initialize', { clientInfo: { name: 'send-to-codex', version: '1' } });
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

/* Codex app-server client: a websocket over the control Unix socket, JSON-RPC on top.
   The frame handling matches tools/prompt-relay and tools/fan-out.mjs. */
import net from 'node:net';
import crypto from 'node:crypto';

const KEY = 'dGhlIHNhbXBsZSBub25jZQ==';
const ACCEPT = crypto.createHash('sha1').update(`${KEY}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`).digest('base64');

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

/* Opens one session, hands `call(method, params)` to `session`, and closes. */
export function connect(socketPath, session, timeoutMs = 10_000) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(socketPath);
    let buffer = Buffer.alloc(0),
      upgraded = false,
      sequence = 0,
      fragment = null,
      settled = false;
    const pending = new Map();
    const fail = error => {
      if (settled) return;
      settled = true;
      for (const waiter of pending.values()) clearTimeout(waiter.timer);
      pending.clear();
      socket.destroy();
      reject(error);
    };
    const done = value => {
      if (settled) return;
      settled = true;
      for (const waiter of pending.values()) clearTimeout(waiter.timer);
      pending.clear();
      socket.end();
      resolve(value);
    };
    const call = (method, params) =>
      new Promise((ok, no) => {
        const id = ++sequence;
        const timer = setTimeout(() => {
          pending.delete(id);
          no(new Error(`Codex RPC timeout: ${method}`));
        }, timeoutMs);
        pending.set(id, { ok, no, timer });
        socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', id, method, params })));
      });
    const notify = (method, params) => socket.write(websocketFrame(JSON.stringify({ jsonrpc: '2.0', method, params })));

    const take = (fin, opcode, body) => {
      if (opcode === 0x9) return void socket.write(websocketFrame(body, 0xa));
      if (opcode === 0x8) return fail(new Error('Codex websocket closed'));
      if (opcode === 0x1) fragment = body;
      else if (opcode === 0x0 && fragment) fragment = Buffer.concat([fragment, body]);
      else return;
      if (!fin) return;
      let message;
      try {
        message = JSON.parse(fragment.toString());
      } catch {
        return fail(new Error('Codex sent a frame that is not JSON'));
      }
      fragment = null;
      const waiter = pending.get(message.id);
      if (!waiter) return;
      pending.delete(message.id);
      clearTimeout(waiter.timer);
      if (message.error) waiter.no(new Error(JSON.stringify(message.error)));
      else waiter.ok(message.result ?? message);
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
        take(fin, opcode, body);
      }
    };

    socket.setTimeout(timeoutMs, () => fail(new Error('Codex socket timeout')));
    socket.on('error', fail);
    socket.on('connect', () =>
      socket.write(
        `GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${KEY}\r\nSec-WebSocket-Version: 13\r\n\r\n`
      )
    );
    socket.on('data', data => {
      buffer = Buffer.concat([buffer, data]);
      if (!upgraded) {
        const end = buffer.indexOf('\r\n\r\n');
        if (end < 0) return;
        const header = buffer.subarray(0, end).toString();
        const accept = header.match(/sec-websocket-accept:\s*([^\r\n]+)/i)?.[1]?.trim();
        if (!header.startsWith('HTTP/1.1 101') || !/upgrade:\s*websocket/i.test(header) || accept !== ACCEPT) {
          return fail(new Error('Codex websocket upgrade refused'));
        }
        buffer = buffer.subarray(end + 4);
        upgraded = true;
        (async () => {
          try {
            await call('initialize', {
              clientInfo: { name: 'codex-quota-reset', version: '1' },
              capabilities: { experimentalApi: true },
            });
            notify('initialized', {});
            done(await session(call));
          } catch (error) {
            fail(error);
          }
        })();
      }
      parse();
    });
  });
}

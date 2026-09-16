/* A fake Codex app-server: one websocket over a Unix socket, answering the two account
   methods from a fixture payload file on disk.  It never reaches the network. */
import fs from 'node:fs';
import net from 'node:net';

const ACCEPT = 's3pPLMBiTxaQ9kYGzzhZRbK+xOo=';

const frame = (payload, opcode = 1, fin = true) => {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(payload);
  const first = (fin ? 0x80 : 0) | opcode;
  if (body.length < 126) return Buffer.concat([Buffer.from([first, body.length]), body]);
  if (body.length < 65536) return Buffer.concat([Buffer.from([first, 126, body.length >> 8, body.length & 255]), body]);
  const head = Buffer.alloc(10);
  head[0] = first;
  head[1] = 127;
  head.writeBigUInt64BE(BigInt(body.length), 2);
  return Buffer.concat([head, body]);
};

function readFrames(state, visit) {
  while (state.raw.length >= 2) {
    let n = state.raw[1] & 127,
      offset = 2;
    if (!(state.raw[1] & 128)) throw new Error('client frame was not masked');
    if (n === 126) {
      if (state.raw.length < 4) return;
      n = state.raw.readUInt16BE(2);
      offset = 4;
    } else if (n === 127) {
      if (state.raw.length < 10) return;
      n = Number(state.raw.readBigUInt64BE(2));
      offset = 10;
    }
    if (state.raw.length < offset + 4 + n) return;
    const mask = state.raw.subarray(offset, offset + 4),
      body = Buffer.alloc(n),
      opcode = state.raw[0] & 15;
    for (let i = 0; i < n; i++) body[i] = state.raw[offset + 4 + i] ^ mask[i % 4];
    state.raw = state.raw.subarray(offset + 4 + n);
    visit(opcode, body);
  }
}

/* `fixturePath` is a real JSON file holding one account/rateLimits/read result. */
export async function start(socketPath, fixturePath, consumeOutcome = 'reset') {
  const requests = [];
  const server = net.createServer(socket => {
    const state = { raw: Buffer.alloc(0), upgraded: false };
    socket.on('error', () => {});
    socket.on('data', data => {
      state.raw = Buffer.concat([state.raw, data]);
      if (!state.upgraded) {
        const end = state.raw.indexOf('\r\n\r\n');
        if (end < 0) return;
        state.raw = state.raw.subarray(end + 4);
        state.upgraded = true;
        socket.write(`HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ${ACCEPT}\r\n\r\n`);
      }
      readFrames(state, (opcode, body) => {
        if (opcode !== 1) return;
        const request = JSON.parse(body);
        requests.push(request);
        if (!request.id) return;
        let result;
        if (request.method === 'initialize') result = { userAgent: { name: 'fake', version: '1' } };
        else if (request.method === 'account/rateLimits/read') result = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
        else if (request.method === 'account/rateLimitResetCredit/consume') result = { outcome: consumeOutcome };
        else {
          socket.write(frame(JSON.stringify({ jsonrpc: '2.0', id: request.id, error: { code: -32601, message: 'no such method' } })));
          return;
        }
        socket.write(frame(JSON.stringify({ jsonrpc: '2.0', id: request.id, result })));
      });
    });
  });
  await new Promise(ok => server.listen(socketPath, ok));
  return { server, requests, close: () => new Promise(ok => server.close(ok)) };
}

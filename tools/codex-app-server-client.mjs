import crypto from "node:crypto";
import net from "node:net";
import { normalizeRateLimitReadings } from "./quota-rate-limits.mjs";

const APP_SERVER_ROUTE = "/";
const CLIENT_INFO = { name: "quota-situation-report", version: "1" };

const asObject = (value, label) => {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`invalid ${label}: expected an object`);
  }
  return value;
};

export const validateAccountReadings = ({ rateLimits, usage, observedAt }) => {
  return {
    observedAt,
    "account/rateLimits/read": normalizeRateLimitReadings({ rateLimits, observedAt }),
    "account/usage/read": usage === undefined || usage === null ? null : asObject(usage, "account/usage/read result"),
  };
};

export const createAccountClient = ({ transport, now = () => new Date().toISOString() }) => {
  if (!transport || typeof transport.request !== "function" || typeof transport.notify !== "function") {
    throw new Error("an app-server transport with request and notify is required");
  }

  return {
    async read() {
      await transport.request("initialize", { clientInfo: CLIENT_INFO });
      await transport.notify("initialized", {});
      const [rateLimits, usage] = await Promise.all([
        transport.request("account/rateLimits/read", {}),
        transport.request("account/usage/read", {}),
      ]);
      return validateAccountReadings({ rateLimits, usage, observedAt: now() });
    },
  };
};

const websocketFrame = (payload, opcode = 0x1) => {
  const body = Buffer.isBuffer(payload) ? payload : Buffer.from(payload);
  const mask = crypto.randomBytes(4);
  let header;
  if (body.length < 126) header = Buffer.from([0x80 | opcode, 0x80 | body.length]);
  else if (body.length < 65_536) header = Buffer.from([0x80 | opcode, 0xfe, body.length >> 8, body.length & 255]);
  else {
    header = Buffer.alloc(10);
    header[0] = 0x80 | opcode;
    header[1] = 0xff;
    header.writeBigUInt64BE(BigInt(body.length), 2);
  }
  const masked = Buffer.alloc(body.length);
  for (let index = 0; index < body.length; index += 1) masked[index] = body[index] ^ mask[index % 4];
  return Buffer.concat([header, mask, masked]);
};

export const createUnixWebSocketTransport = socketPath => {
  if (typeof socketPath !== "string" || socketPath.length === 0) throw new Error("an explicit socket path is required");
  let socket;
  let nextId = 0;
  let buffer = Buffer.alloc(0);
  let upgraded = false;
  let connected;
  const pending = new Map();

  const failAll = error => {
    for (const { reject } of pending.values()) reject(error);
    pending.clear();
  };
  const receive = message => {
    if (message.id === undefined) return;
    const pendingRequest = pending.get(message.id);
    if (!pendingRequest) return;
    pending.delete(message.id);
    if (message.error) {
      const error = new Error(`JSON-RPC ${pendingRequest.method} failed: ${JSON.stringify(message.error)}`);
      error.code = message.error.code;
      pendingRequest.reject(error);
    } else if (!("result" in message)) {
      pendingRequest.reject(new Error(`JSON-RPC ${pendingRequest.method} returned neither result nor error`));
    } else pendingRequest.resolve(message.result);
  };
  const parseFrames = () => {
    while (buffer.length >= 2) {
      const fin = Boolean(buffer[0] & 0x80);
      const opcode = buffer[0] & 0x0f;
      let length = buffer[1] & 0x7f;
      let offset = 2;
      if (length === 126) { if (buffer.length < 4) return; length = buffer.readUInt16BE(2); offset = 4; }
      if (length === 127) { if (buffer.length < 10) return; const size = buffer.readBigUInt64BE(2); if (size > BigInt(Number.MAX_SAFE_INTEGER)) return failAll(new Error("app-server frame is too large")); length = Number(size); offset = 10; }
      if (buffer.length < offset + length) return;
      const body = buffer.subarray(offset, offset + length);
      buffer = buffer.subarray(offset + length);
      if (opcode === 0x9) { socket.write(websocketFrame(body, 0xa)); continue; }
      if (opcode === 0x8) return failAll(new Error("app-server websocket closed"));
      if (!fin || opcode !== 0x1) return failAll(new Error("app-server sent an unsupported websocket frame"));
      try { receive(JSON.parse(body.toString("utf8"))); } catch { failAll(new Error("app-server sent invalid JSON-RPC")); }
    }
  };
  const connect = () => connected ??= new Promise((resolve, reject) => {
    socket = net.createConnection(socketPath);
    socket.once("error", reject);
    socket.on("error", failAll);
    socket.on("close", () => failAll(new Error("app-server socket closed")));
    socket.on("connect", () => socket.write(`GET ${APP_SERVER_ROUTE} HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n`));
    socket.on("data", data => {
      buffer = Buffer.concat([buffer, data]);
      if (upgraded) return parseFrames();
      const boundary = buffer.indexOf("\r\n\r\n");
      if (boundary < 0) return;
      const headers = buffer.subarray(0, boundary).toString("utf8");
      const accept = headers.match(/sec-websocket-accept:\s*([^\r\n]+)/i)?.[1]?.trim();
      const expected = crypto.createHash("sha1").update("dGhlIHNhbXBsZSBub25jZQ==258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest("base64");
      if (!headers.startsWith("HTTP/1.1 101") || accept !== expected) return reject(new Error("app-server websocket upgrade refused"));
      buffer = buffer.subarray(boundary + 4);
      upgraded = true;
      socket.removeListener("error", reject);
      resolve();
      parseFrames();
    });
  });

  return {
    async request(method, params) {
      await connect();
      const id = ++nextId;
      return new Promise((resolve, reject) => {
        pending.set(id, { method, resolve, reject });
        socket.write(websocketFrame(JSON.stringify({ jsonrpc: "2.0", id, method, params })));
      });
    },
    async notify(method, params) {
      await connect();
      socket.write(websocketFrame(JSON.stringify({ jsonrpc: "2.0", method, params })));
    },
    close() { socket?.end(); },
  };
};

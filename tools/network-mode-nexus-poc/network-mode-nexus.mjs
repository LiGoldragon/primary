#!/usr/bin/env node
/* Source-only proof of concept. It emits plans and never changes host networking. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const MODES = new Set(['offline', 'edge-gateway', 'edge-gateway-ap', 'transit-gateway', 'transit-gateway-ap', 'leaf']);
const GATEWAYS = new Set(['edge-gateway', 'edge-gateway-ap', 'transit-gateway', 'transit-gateway-ap']);
const EDGES = new Set(['edge-gateway', 'edge-gateway-ap']);
const AP = new Set(['edge-gateway-ap', 'transit-gateway-ap']);

function fail(message) { throw new Error(message); }
function ipToInt(ip) {
  const parts = String(ip).split('.').map(Number);
  if (parts.length !== 4 || parts.some(x => !Number.isInteger(x) || x < 0 || x > 255)) fail(`invalid IPv4 address: ${ip}`);
  return parts.reduce((n, x) => ((n << 8) | x) >>> 0, 0) >>> 0;
}
function intToIp(value) { return [24, 16, 8, 0].map(s => (value >>> s) & 255).join('.'); }
function parseCidr(cidr) {
  const [ip, raw] = String(cidr).split('/');
  const prefix = Number(raw);
  if (!Number.isInteger(prefix) || prefix < 8 || prefix > 30) fail(`invalid IPv4 prefix: ${cidr}`);
  const address = ipToInt(ip);
  const mask = prefix === 0 ? 0 : (0xffffffff << (32 - prefix)) >>> 0;
  if ((address & mask) !== address) fail(`pool must be a network address: ${cidr}`);
  return {address, prefix, size: 2 ** (32 - prefix)};
}
function subnetAt(pool, prefix, index) {
  if (prefix < pool.prefix) fail('link prefix cannot be larger than the root pool');
  const size = 2 ** (32 - prefix);
  const count = 2 ** (prefix - pool.prefix);
  if (!Number.isSafeInteger(index) || index < 0 || index >= count) fail('root pool is exhausted');
  return `${intToIp((pool.address + index * size) >>> 0)}/${prefix}`;
}
function segmentDetails(cidr) {
  const parsed = parseCidr(cidr);
  if (parsed.size < 8) fail('segment prefix is too small for gateway, peer, DHCP, and broadcast');
  return {cidr, gateway: intToIp(parsed.address + 1), peer: intToIp(parsed.address + 2),
    dhcpRange: [intToIp(parsed.address + Math.min(100, parsed.size - 4)), intToIp(parsed.address + Math.min(199, parsed.size - 2))]};
}
function clone(value) { return JSON.parse(JSON.stringify(value)); }

export function createState({rootPool, linkPrefix = 24} = {}) {
  const pool = parseCidr(rootPool);
  if (!Number.isInteger(linkPrefix) || linkPrefix < pool.prefix || linkPrefix > 28) fail('linkPrefix must fit the root pool and leave usable hosts');
  return {version: 1, revision: 0, rootPool, linkPrefix, nodes: {}, allocations: {}, audit: []};
}

function validateInterface(value, kind, label) {
  if (!value || value.kind !== kind || typeof value.name !== 'string' || !/^[A-Za-z0-9_.:-]{1,32}$/.test(value.name)) fail(`${label} must be a named ${kind} interface`);
}

function validateNode(node) {
  if (!node || typeof node.id !== 'string' || !/^[a-z][a-z0-9-]{0,31}$/.test(node.id)) fail('node id is invalid');
  if (!MODES.has(node.mode)) fail(`unsupported mode for ${node.id}`);
  if (node.mode === 'offline') return;
  validateInterface(node.uplink, 'integrated', `${node.id} uplink`);
  if (GATEWAYS.has(node.mode)) {
    validateInterface(node.downlink, 'usb', `${node.id} downlink`);
    if (node.uplink.name === node.downlink.name) fail(`${node.id} uplink and downlink must differ`);
  } else if (node.downlink != null) fail(`${node.id} leaf cannot own a downlink`);
  if (EDGES.has(node.mode) && node.parent != null) fail(`${node.id} edge gateway cannot have a parent`);
  if (!EDGES.has(node.mode) && typeof node.parent !== 'string') fail(`${node.id} requires a parent`);
}

function validateTopology(nodes) {
  Object.values(nodes).forEach(validateNode);
  const active = Object.values(nodes).filter(n => n.mode !== 'offline');
  const edges = active.filter(n => EDGES.has(n.mode));
  if (active.length && edges.length !== 1) fail('active topology requires exactly one edge gateway');
  for (const node of active) {
    if (EDGES.has(node.mode)) continue;
    const parent = nodes[node.parent];
    if (!parent || parent.mode === 'offline' || !GATEWAYS.has(parent.mode)) fail(`${node.id} parent must be an active gateway`);
    const seen = new Set([node.id]);
    let cursor = node;
    while (cursor.parent) {
      if (seen.has(cursor.parent)) fail('topology contains a cycle');
      seen.add(cursor.parent);
      cursor = nodes[cursor.parent];
      if (!cursor) fail('topology contains a missing parent');
    }
  }
}

function desiredSegmentKeys(nodes) {
  const keys = [];
  for (const node of Object.values(nodes).sort((a, b) => a.id.localeCompare(b.id))) {
    if (node.mode === 'offline') continue;
    if (node.parent) keys.push(`link:${node.parent}:${node.id}`);
    if (AP.has(node.mode)) keys.push(`ap:${node.id}`);
  }
  return keys;
}

function allocate(state, keys) {
  const used = new Set(Object.values(state.allocations).map(a => a.index));
  for (const key of keys) {
    if (state.allocations[key]) continue;
    let index = 0;
    while (used.has(index)) index += 1;
    const cidr = subnetAt(parseCidr(state.rootPool), state.linkPrefix, index);
    state.allocations[key] = {index, ...segmentDetails(cidr), reserved: true};
    used.add(index);
  }
}

function validateAllocations(state, {requireActive = true} = {}) {
  if (!state.allocations || typeof state.allocations !== 'object' || Array.isArray(state.allocations)) fail('allocation ledger is malformed');
  const pool = parseCidr(state.rootPool);
  const indexes = new Set();
  for (const [key, value] of Object.entries(state.allocations)) {
    if (!/^(?:link:[a-z][a-z0-9-]{0,31}:[a-z][a-z0-9-]{0,31}|ap:[a-z][a-z0-9-]{0,31})$/.test(key)) fail(`allocation key is malformed: ${key}`);
    if (!value || !Number.isSafeInteger(value.index) || value.index < 0 || value.reserved !== true) fail(`allocation record is malformed: ${key}`);
    if (indexes.has(value.index)) fail(`allocation index is duplicated: ${value.index}`);
    indexes.add(value.index);
    const expected = {index: value.index, ...segmentDetails(subnetAt(pool, state.linkPrefix, value.index)), reserved: true};
    if (JSON.stringify(value) !== JSON.stringify(expected)) fail(`allocation record does not match its root-pool index: ${key}`);
  }
  if (requireActive) {
    for (const key of desiredSegmentKeys(state.nodes)) if (!state.allocations[key]) fail(`allocation missing for ${key}`);
  }
}

export function transition(input, request) {
  const state = clone(input);
  validateAllocations(state, {requireActive: true});
  if (request.expectedRevision !== state.revision) fail(`stale revision: expected ${request.expectedRevision}, current ${state.revision}`);
  if (typeof request.actor !== 'string' || !request.actor.trim() || typeof request.reason !== 'string' || !request.reason.trim()) fail('actor and reason are required');
  validateNode(request.node);
  const before = state.nodes[request.node.id] ?? null;
  state.nodes[request.node.id] = clone(request.node);
  validateTopology(state.nodes);
  allocate(state, desiredSegmentKeys(state.nodes));
  validateAllocations(state, {requireActive: true});
  state.revision += 1;
  state.audit.push({revision: state.revision, at: request.at ?? new Date().toISOString(), actor: request.actor,
    reason: request.reason, nodeId: request.node.id, fromMode: before?.mode ?? null, toMode: request.node.mode});
  return state;
}

export function plan(state) {
  validateTopology(state.nodes);
  validateAllocations(state, {requireActive: true});
  const activeKeys = new Set(desiredSegmentKeys(state.nodes));
  const edge = Object.values(state.nodes).find(n => n.mode !== 'offline' && EDGES.has(n.mode));
  const actions = [];
  for (const key of [...activeKeys].sort()) {
    const allocation = state.allocations[key];
    if (!allocation) fail(`allocation missing for ${key}`);
    if (key.startsWith('link:')) {
      const [, parentId, childId] = key.split(':');
      const parent = state.nodes[parentId], child = state.nodes[childId];
      actions.push({kind: 'ConfigureTransit', segment: key, cidr: allocation.cidr, gateway: allocation.gateway,
        peer: allocation.peer, parent: {node: parentId, interface: parent.downlink.name}, child: {node: childId, interface: child.uplink.name}});
      actions.push({kind: 'ServeDhcpDns', node: parentId, interface: parent.downlink.name, segment: key, range: allocation.dhcpRange});
      if (!EDGES.has(parent.mode)) actions.push({kind: 'PublishRoute', at: edge.id, prefix: allocation.cidr, viaNode: parentId});
    } else {
      const nodeId = key.slice(3), node = state.nodes[nodeId];
      actions.push({kind: 'EnableOptionalAp', node: nodeId, segment: key, cidr: allocation.cidr,
        gateway: allocation.gateway, authentication: 'EAP-TLS-target', automatic: false});
      actions.push({kind: 'ServeDhcpDns', node: nodeId, interface: 'wifi-ap', segment: key, range: allocation.dhcpRange});
    }
  }
  if (edge) actions.push({kind: 'OwnEgressNat', node: edge.id, uplink: edge.uplink.name, sourcePool: state.rootPool});
  return {version: 1, revision: state.revision, rootPool: state.rootPool, natOwners: edge ? [edge.id] : [], actions,
    allocations: Object.fromEntries(Object.entries(state.allocations).map(([key, value]) => [key, {...value, active: activeKeys.has(key)}])),
    evidenceGrade: 'desired-plan', liveNetworkChanged: false};
}

function atomicWrite(file, value) {
  fs.mkdirSync(path.dirname(file), {recursive: true});
  const temp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(temp, `${JSON.stringify(value, null, 2)}\n`);
  fs.renameSync(temp, file);
}
function readJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }
function arg(args, name) { const i = args.indexOf(name); return i < 0 ? null : args[i + 1]; }

const invokedDirectly = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (invokedDirectly) {
  try {
    const args = process.argv.slice(2), command = args[0], stateFile = arg(args, '--state');
    if (!stateFile) fail('--state is required');
    if (command === 'init') atomicWrite(stateFile, createState({rootPool: arg(args, '--pool'), linkPrefix: Number(arg(args, '--link-prefix') ?? 24)}));
    else if (command === 'transition') atomicWrite(stateFile, transition(readJson(stateFile), readJson(arg(args, '--request'))));
    else if (command === 'plan') process.stdout.write(`${JSON.stringify(plan(readJson(stateFile)), null, 2)}\n`);
    else if (command === 'show') process.stdout.write(`${JSON.stringify(readJson(stateFile), null, 2)}\n`);
    else fail('command must be init, transition, plan, or show');
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

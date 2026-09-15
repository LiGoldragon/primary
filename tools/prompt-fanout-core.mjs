import crypto from 'node:crypto';
import fs from 'node:fs';

const relayPrefix = '[RELAY ';

const textContent = content => typeof content === 'string'
  ? content
  : Array.isArray(content) && content.every(part => part?.type === 'text' && typeof part.text === 'string')
    ? content.map(part => part.text).join('')
    : null;

const marked = content => {
  const text = textContent(content);
  if (text === null || text.startsWith(relayPrefix) || text.startsWith('[PEER ') || text.startsWith('[WAKE ') || text.startsWith('[SYSTEM ') || text.startsWith('<')) return true;
  const header = Array.isArray(content) ? content[0]?.type === 'text' ? content[0].text : '' : text.split('\n\n', 1)[0];
  try { const value = JSON.parse(header); return Boolean(value?.provenance?.source_message_id && value?.provenance?.sha256_utf8); } catch { return false; }
};

const candidate = record => {
  if (record.type === 'user' && record.message?.role === 'user' && record.origin?.kind === 'human') {
    const text = textContent(record.message.content);
    if (text !== null && !marked(record.message.content)) return { id: record.uuid ?? record.promptId, text, format: 'claude', timestamp: record.timestamp ?? null };
  }
  if (record.type === 'queue-operation' && record.operation === 'enqueue' && typeof record.timestamp === 'string') {
    const text = textContent(record.content);
    if (text !== null && !marked(record.content)) return { id: record.timestamp, text, format: 'claude-queue-enqueue', timestamp: record.timestamp };
  }
  const rollout = record.type === 'event_msg' && record.payload?.type === 'item_completed' && record.payload?.item?.type === 'UserMessage' ? record.payload.item : null;
  if (rollout) {
    const text = textContent(rollout.content);
    if (rollout.id && text !== null && !marked(rollout.content)) return { id: rollout.id, text, format: 'codex-rollout', timestamp: record.timestamp ?? null };
  }
  return null;
};

export function planFanout({ source, match, sourceId, bodyMode, endpoints, read = fs.readFileSync }) {
  if (bodyMode !== 'whole' && bodyMode !== 'receipt') throw new Error('--body-mode must be whole or receipt');
  if (!Array.isArray(endpoints) || endpoints.length === 0) throw new Error('at least one explicit endpoint is required');
  const divider = match.indexOf('..');
  if (divider < 0) throw new Error('--match must be HEAD..TAIL');
  const head = match.slice(0, divider), tail = match.slice(divider + 2);
  if (Array.from(head).length !== 6 || Array.from(tail).length !== 6) throw new Error('HEAD and TAIL must each be exactly six Unicode characters');
  const matches = read(source, 'utf8').split(/\n/).filter(Boolean).map(line => candidate(JSON.parse(line))).filter(Boolean).filter(value => Array.from(value.text).slice(0, 6).join('') === head && Array.from(value.text).slice(-6).join('') === tail).filter(value => !sourceId || value.id === sourceId);
  if (matches.length === 0) throw new Error('no unmarked human user input matches');
  if (matches.length !== 1) throw new Error('ambiguous match; supply --source-id');
  const selected = matches[0];
  const bytes = Buffer.from(selected.text, 'utf8');
  const digest = crypto.createHash('sha256').update(bytes).digest('hex');
  const provenance = { source_path: source, source_format: selected.format, source_message_id: selected.id, source_timestamp: selected.timestamp, sha256_utf8: digest };
  return { provenance, bodyMode, bytes, endpoints: endpoints.map(endpoint => ({ endpoint, bytes, provenance })) };
}

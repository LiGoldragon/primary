import fs from 'node:fs';
import path from 'node:path';

const readUtf8 = (file, read) => read(file, 'utf8');
const requiredText = (value, name) => {
  if (typeof value !== 'string' || !value.trim()) throw new Error(`lane metadata requires ${name}`);
  return value;
};

const filesBelow = (directory, readDirectory = fs.readdirSync) => {
  if (!fs.existsSync(directory)) return [];
  return readDirectory(directory, { withFileTypes: true }).flatMap(entry => {
    const child = path.join(directory, entry.name);
    return entry.isDirectory() ? filesBelow(child, readDirectory) : entry.isFile() && entry.name.endsWith('.md') ? [child] : [];
  }).sort();
};

const labeled = (title, files, read) => files.map(file => `## ${title}: ${file}\n\n${readUtf8(file, read).trim()}\n`).join('\n');

export function scanPredecessorLane({ lane, read = fs.readFileSync, readDirectory = fs.readdirSync, minimal = false, successorIdentity, topic, skills }) {
  const metadataPath = path.join(lane, 'lane.json');
  if (!fs.existsSync(metadataPath) && !minimal) throw new Error('predecessor lane is missing lane.json');
  const metadata = fs.existsSync(metadataPath) ? JSON.parse(readUtf8(metadataPath, read)) : {
    identity: path.basename(path.resolve(lane)),
    topic: topic || 'unresolved predecessor topic',
    successor: { identity: successorIdentity, topic: topic || 'unresolved successor topic' },
    transcript_provenance: [],
    skills: skills || [],
  };
  requiredText(metadata.identity, 'identity');
  if (!minimal) requiredText(metadata.topic, 'topic');
  if (!metadata.successor || typeof metadata.successor !== 'object') {
    if (!minimal) throw new Error('lane metadata requires successor identity and topic');
    metadata.successor = { identity: successorIdentity, topic: topic || 'unresolved successor topic' };
  }
  if (successorIdentity) metadata.successor.identity = successorIdentity;
  if (topic) { metadata.topic = topic; metadata.successor.topic = topic; }
  requiredText(metadata.successor.identity, 'successor.identity');
  if (!minimal) requiredText(metadata.successor.topic, 'successor.topic');
  const provenanceRecords = Array.isArray(metadata.transcript_provenance) ? metadata.transcript_provenance : [];
  if (!minimal && provenanceRecords.length !== 1) throw new Error('lane metadata requires exactly one transcript provenance record');
  const provenance = provenanceRecords.length === 1 ? provenanceRecords[0] : null;
  if (provenance) {
    requiredText(provenance.source_path, 'transcript provenance source_path');
    requiredText(provenance.source_message_id, 'transcript provenance source_message_id');
  }
  if (!Array.isArray(metadata.skills)) metadata.skills = [];
  if (skills) metadata.skills = skills;
  if (metadata.skills.some(skill => typeof skill !== 'string' || !skill.trim())) throw new Error('lane metadata requires a skills list');
  return { metadata, provenance, spirit: filesBelow(path.join(lane, 'spirit'), readDirectory), intent: filesBelow(path.join(lane, 'intent'), readDirectory), vision: filesBelow(path.join(lane, 'Vision'), readDirectory), rawVision: filesBelow(path.join(lane, 'vision'), readDirectory), log: path.join(lane, 'log.md') };
}

export function assemblePrompts({ lane, read = fs.readFileSync, readDirectory = fs.readdirSync, minimal = false, successorIdentity, topic, skills }) {
  const scanned = scanPredecessorLane({ lane, read, readDirectory, minimal, successorIdentity, topic, skills });
  if (!fs.existsSync(scanned.log)) throw new Error('predecessor lane is missing log.md');
  const { metadata, provenance } = scanned;
  const system = [
    `# System prompt for ${metadata.successor.identity}`,
    `Successor identity: ${metadata.successor.identity}\nSuccessor topic: ${metadata.successor.topic}`,
    `## Skills\n${metadata.skills.map(skill => `- ${skill}`).join('\n')}`,
    labeled('Spirit', scanned.spirit, read),
    labeled('Intent', scanned.intent, read),
    labeled('Vision', scanned.vision, read),
  ].filter(Boolean).join('\n\n');
  const user = [
    `# Continuation for ${metadata.successor.identity}`,
    `Predecessor identity: ${metadata.identity}\nTopic: ${metadata.topic}`,
    provenance ? `## Transcript provenance\n- source_path: ${provenance.source_path}\n- source_message_id: ${provenance.source_message_id}` : '## Transcript provenance\n- unavailable: no exact source path and message ID were supplied; provenance is refused rather than invented.',
    `## Open log items\n${readUtf8(scanned.log, read).trim()}`,
    labeled('Raw Vision', scanned.rawVision, read),
  ].filter(Boolean).join('\n\n');
  return { system, user, metadata, provenance };
}

export function writePrompts({ lane, output, write = fs.writeFileSync, ...options }) {
  const assembled = assemblePrompts({ lane, ...options });
  write(path.join(output, 'system-prompt.md'), assembled.system, 'utf8');
  write(path.join(output, 'user-prompt.md'), assembled.user, 'utf8');
  return { systemPath: path.join(output, 'system-prompt.md'), userPath: path.join(output, 'user-prompt.md'), ...assembled };
}

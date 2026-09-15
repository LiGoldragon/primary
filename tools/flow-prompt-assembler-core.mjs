import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

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

const sourceDigest = (file, read) => {
  const contents = read(file);
  const bytes = Buffer.isBuffer(contents) ? contents : Buffer.from(contents);
  return { path: path.resolve(file), bytes: bytes.length, sha256: crypto.createHash('sha256').update(bytes).digest('hex') };
};

const wholeSources = (title, files, read) => files.map(file => {
  const digest = sourceDigest(file, read);
  return { ...digest, title, contents: Buffer.isBuffer(read(file)) ? read(file).toString('utf8') : read(file, 'utf8') };
});

const renderSources = sources => sources.map(source => `## ${source.title}: ${source.path}\n\n${source.contents}\n`).join('\n');

const manifest = sources => sources.map(({ title, path: sourcePath, bytes, sha256 }) => ({ title, path: sourcePath, bytes, sha256 }));

const topicName = file => path.basename(file, path.extname(file));

const primarySkillNames = [
  'spirit', 'psyche', 'behavior', 'correction', 'vocabulary', 'testing',
  'psyche-interraction', 'main-flow', 'edit-coordination',
];

export function scanPrimaryProfile({ lane, primaryRoot, read = fs.readFileSync, readDirectory = fs.readdirSync, successorIdentity, topic, skillRoot }) {
  if (!successorIdentity) throw new Error('primary profile requires --successor');
  if (!topic) throw new Error('primary profile requires --topic');
  const root = path.resolve(primaryRoot);
  const predecessor = path.resolve(lane);
  const predecessorVision = filesBelow(path.join(predecessor, 'vision'), readDirectory);
  const predecessorNotion = filesBelow(path.join(predecessor, 'notion'), readDirectory);
  const topics = new Set(topic.split(',').map(value => value.trim()).filter(Boolean));
  for (const file of [...predecessorVision, ...predecessorNotion]) topics.add(topicName(file));
  if (!topics.size) throw new Error('primary profile requires at least one topic');
  const rawVision = filesBelow(path.join(root, 'flows'), readDirectory)
    .filter(file => file.includes(`${path.sep}vision${path.sep}`) && topics.has(topicName(file)));
  const resolvedSkillRoot = path.resolve(skillRoot || path.join(root, '.claude', 'skills'));
  const skillFiles = primarySkillNames.map(name => path.join(resolvedSkillRoot, name, 'SKILL.md'));
  for (const file of skillFiles) if (!fs.existsSync(file)) throw new Error(`primary profile is missing required skill source ${file}`);
  const sources = [
    ...wholeSources('Primary skill body', skillFiles, read),
    ...wholeSources('Primary Vision', filesBelow(path.join(root, 'Vision'), readDirectory), read),
    ...wholeSources('Primary Intent', filesBelow(path.join(root, 'Intent'), readDirectory), read),
    ...wholeSources('Raw Vision for topics in play', rawVision, read),
    ...wholeSources('Predecessor raw Vision', predecessorVision, read),
    ...wholeSources('Predecessor Notion', predecessorNotion, read),
  ];
  const predecessorLog = path.join(predecessor, 'log.md');
  const provenance = fs.existsSync(path.join(predecessor, 'lane.json'))
    ? JSON.parse(readUtf8(path.join(predecessor, 'lane.json'), read)).transcript_provenance || []
    : [];
  return { root, predecessor, successorIdentity, topics: [...topics].sort(), sources, predecessorLog, provenance };
}

export function assemblePrimaryPrompts(options) {
  const scanned = scanPrimaryProfile(options);
  const coverage = manifest(scanned.sources);
  const system = [
    `# Primary system prompt for ${scanned.successorIdentity}`,
    `Successor identity is supplied by the caller: ${scanned.successorIdentity}.`,
    `Topics in play: ${scanned.topics.join(', ')}.`,
    '## Complete source context',
    renderSources(scanned.sources),
  ].join('\n\n');
  const user = [
    `# Original continuation context for ${scanned.successorIdentity}`,
    `Predecessor source directory: ${scanned.predecessor}`,
    scanned.provenance.length === 1
      ? `## Transcript provenance\n\n${JSON.stringify(scanned.provenance[0], null, 2)}`
      : '## Transcript provenance\n\nNo exact transcript provenance record was supplied. No identifier has been invented.',
    fs.existsSync(scanned.predecessorLog)
      ? `## Predecessor log source: ${scanned.predecessorLog}\n\n${readUtf8(scanned.predecessorLog, options.read || fs.readFileSync)}`
      : `## Predecessor log source\n\nUnavailable: ${scanned.predecessorLog} does not exist.`,
    `## Exact source coverage manifest\n\n${JSON.stringify(coverage, null, 2)}`,
  ].join('\n\n');
  return { system, user, metadata: { successor: scanned.successorIdentity, topics: scanned.topics, sourceCoverage: coverage } };
}

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
  const assembled = options.profile === 'primary'
    ? assemblePrimaryPrompts({ lane, ...options })
    : assemblePrompts({ lane, ...options });
  write(path.join(output, 'system-prompt.md'), assembled.system, 'utf8');
  write(path.join(output, 'user-prompt.md'), assembled.user, 'utf8');
  return { systemPath: path.join(output, 'system-prompt.md'), userPath: path.join(output, 'user-prompt.md'), ...assembled };
}

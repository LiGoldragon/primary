import fs from 'node:fs';
import path from 'node:path';
import {roleModulesFromConfig} from './launch-config.mjs';

export function spiritModules(workspace, surface = '.agents') {
  const root = path.join(workspace, surface, 'skills');
  const names = fs.readdirSync(root, {withFileTypes: true})
    .filter(entry => entry.isDirectory() && /^spirit-[A-Za-z0-9_-]+$/.test(entry.name))
    .map(entry => entry.name).sort();
  if (fs.existsSync(path.join(root, 'spirit'))) throw new Error('legacy spirit module must be regenerated as spirit-core');
  if (!names.includes('spirit-core')) throw new Error('generated spirit-core module is missing');
  return names.map(name => {
    const file = path.join(root, name, 'SKILL.md');
    const body = fs.readFileSync(file, 'utf8').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
    if (!body) throw new Error(`empty spirit module: ${name}`);
    return {name, body};
  });
}

export function mainSystemModules(workspace, surface, {aspect, layer, topic = 'Core', metaflow, startupSkills = []}) {
  const seat = arguments[2] ?? {};
  const configured = seat.launchConfig;
  let modules;
  if (configured) {
    // A row may add context; even an empty row cannot remove spirit/intent.
    const names = [...new Set([
      ...roleModulesFromConfig(configured, {...seat.metaflowConfig, aspect}, 'system'),
      ...startupSkills.filter(name => name.startsWith('spirit-') || name.startsWith('intent-')),
    ])];
    if (!names.includes('spirit-core') || !names.includes('intent-main-flow'))
      throw new Error('main system context requires spirit-core and intent-main-flow');
    modules = names.map(name => {
      const file = path.join(workspace, surface, 'skills', name, 'SKILL.md');
      let body;
      try { body = fs.readFileSync(file, 'utf8'); }
      catch { throw new Error(`configured system module is not installed: ${file}`); }
      body = body.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
      if (!body) throw new Error(`empty main system module: ${name}`);
      return {name, body};
    });
  } else {
    modules = spiritModules(workspace, surface);
    const names = [];
    if (aspect === 'Psyche' || layer === 'Primary') names.push('vision-design');
    if (aspect === 'Psyche' || metaflow) names.push('intent-psyche-interaction');
    names.push(...startupSkills.filter(name => name.startsWith('intent-')));
    for (const name of new Set(names)) {
      const file = path.join(workspace, surface, 'skills', name, 'SKILL.md');
      const body = fs.readFileSync(file, 'utf8').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
      if (!body) throw new Error(`empty main system module: ${name}`);
      modules.push({name, body});
    }
  }
  const role = `${aspect.toLowerCase()}-${topic.toLowerCase()}-${layer.toLowerCase()}`;
  const roleFile = path.join(workspace, 'tools', 'main-seat-roles', `${role}.md`);
  if (fs.existsSync(roleFile)) {
    const body = fs.readFileSync(roleFile, 'utf8').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
    if (!body) throw new Error(`empty main-seat role: ${role}`);
    modules.push({name: `main-seat-role-${role}`, body});
  } else if (aspect === 'Psyche' && topic === 'Core' && layer === 'Tertiary') {
    throw new Error('generated Psyche Core Tertiary role is missing');
  }
  return modules;
}

export function composeSpiritSystemPrompt(base, modules) {
  if (!base.trim()) throw new Error('main-flow system prompt missing or empty');
  if (!modules.length || new Set(modules.map(module => module.name)).size !== modules.length)
    throw new Error('spirit system modules must be nonempty and unique');
  return `${base.trimEnd()}\n\n${modules.map(module => `# ${module.name}\n\n${module.body}`).join('\n\n')}\n`;
}

// Match the installed model's literal model-owned template. Codex's file
// override replaces this template; keep it intact rather than replacing the
// harness instructions with skills. Variable-bearing models need their own
// qualified renderer, so this route refuses them.
export function codexModelSystemPrompt(client, model, workspace, seat) {
  const home = path.dirname(path.dirname(client.endpoint));
  const cache = JSON.parse(fs.readFileSync(path.join(home, 'models_cache.json'), 'utf8'));
  const matches = cache.models.filter(item => item.slug === model);
  if (matches.length !== 1) throw new Error(`one installed model template required: ${model}`);
  const messages = matches[0].model_messages;
  if (!messages?.instructions_template?.trim() || messages.instructions_variables != null)
    throw new Error(`literal installed model instruction template required: ${model}`);
  return composeSpiritSystemPrompt(messages.instructions_template, mainSystemModules(workspace, '.agents', seat));
}

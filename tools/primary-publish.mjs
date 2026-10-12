#!/usr/bin/env node
// The former per-caller Primary publisher is retired. The standing committer
// alone publishes Primary in place. Keep this entry point as a refusal so an
// old controller or instruction cannot silently publish through it.
export function publish() {
  return { outcome: 'refused', paths: [], error: 'Primary publication belongs to the sole standing committer; leave owned edits for its turn-end handoff. Other repositories keep their own commit and push route.' };
}
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(JSON.stringify(publish()));
  process.exitCode = 1;
}

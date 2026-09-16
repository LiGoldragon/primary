/* Minimal datom text reader and writer for this tool's own shapes. */

function tokenize(text) {
  const tokens = [];
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    if (ch === ';') { while (i < text.length && text[i] !== '\n') i++; continue; }
    if (/\s/.test(ch)) { i++; continue; }
    if (ch === '{' || ch === '}' || ch === '[' || ch === ']') { tokens.push({ kind: ch }); i++; continue; }
    if (ch === '«') {
      let out = '';
      i++;
      while (i < text.length && text[i] !== '»') {
        if (text[i] === '\\') { i++; if (i >= text.length) throw new Error('datom string ends inside an escape'); }
        out += text[i];
        i++;
      }
      if (i >= text.length) throw new Error('datom string is unterminated');
      i++;
      tokens.push({ kind: 'string', value: out });
      continue;
    }
    let run = '';
    while (i < text.length && !/[\s{}[\]«»;]/.test(text[i])) { run += text[i]; i++; }
    if (!run) throw new Error(`datom carries an unreadable glyph: ${ch}`);
    tokens.push({ kind: 'bare', value: run });
  }
  return tokens;
}

/* A value is { struct: [...] } | { vector: [...] } | { head, value } | { bare } | { string } */
function parseValue(tokens, at) {
  const token = tokens[at.i];
  if (token === undefined) throw new Error('datom ends before a value');
  if (token.kind === '{' || token.kind === '[') {
    const close = token.kind === '{' ? '}' : ']';
    at.i++;
    const items = [];
    while (tokens[at.i] && tokens[at.i].kind !== close) items.push(parseValue(tokens, at));
    if (!tokens[at.i]) throw new Error('datom structure is unterminated');
    at.i++;
    return token.kind === '{' ? { struct: items } : { vector: items };
  }
  if (token.kind === 'string') { at.i++; return { string: token.value }; }
  if (token.kind !== 'bare') throw new Error('datom holds a closing glyph where a value belongs');
  at.i++;
  const dot = token.value.indexOf('.');
  if (dot > 0 && /^[A-Z]/.test(token.value)) {
    const head = token.value.slice(0, dot);
    const rest = token.value.slice(dot + 1);
    if (rest.length === 0) return { head, value: parseValue(tokens, at) };
    const restTokens = tokenize(rest);
    if (restTokens.length === 0) throw new Error('datom head carries nothing after its dot');
    const tail = { i: 0 };
    const inner = parseValue([...restTokens, ...tokens.slice(at.i)], tail);
    at.i += Math.max(0, tail.i - restTokens.length);
    return { head, value: inner };
  }
  return { bare: token.value };
}

export function readDatom(text) {
  const tokens = tokenize(text);
  const at = { i: 0 };
  const value = parseValue(tokens, at);
  if (at.i !== tokens.length) throw new Error('datom text carries more than one value');
  return value;
}

export function text(value, what) {
  if (value?.string !== undefined) return value.string;
  if (value?.bare !== undefined) return value.bare;
  throw new Error(`${what} is not a datom string`);
}

export function positions(value, count, what) {
  if (!Array.isArray(value?.struct) || value.struct.length !== count) throw new Error(`${what} does not carry ${count} positions`);
  return value.struct;
}

const bareable = value => typeof value === 'string' && value.length > 0 && !/[\s{}[\]«»;]/.test(value);
export const write = value => (bareable(String(value)) ? String(value) : `«${String(value).replace(/»/g, '\\»')}»`);
export const line = (head, values) => `${head}.{ ${values.map(write).join(' ')} }`;

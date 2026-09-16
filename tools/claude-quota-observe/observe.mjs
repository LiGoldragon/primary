/* Parsing a captured claude -p --output-format stream-json run down to one quota reading.
   The stream is a sequence of newline-delimited JSON objects; the only one this tool wants is
   the first whose "type" is "rate_limit_event". Every other line — system, assistant, result,
   and any line that fails to parse at all (a stream cut off mid-write ends in a half-written
   line) — is skipped in silence: it carries nothing this tool prints or logs. */

export class NoRateLimitEvent extends Error {}

const round = fraction => Math.round(fraction * 100);

const isoOf = epochSeconds => new Date(epochSeconds * 1000).toISOString().replace(/\.\d{3}Z$/, 'Z');

function findRateLimitEvent(text) {
  for (const rawLine of text.split('\n')) {
    const trimmed = rawLine.trim();
    if (trimmed.length === 0) continue;
    let parsed;
    try {
      parsed = JSON.parse(trimmed);
    } catch {
      continue;
    }
    if (parsed !== null && typeof parsed === 'object' && parsed.type === 'rate_limit_event') return parsed;
  }
  return null;
}

/* Reads the captured stream text and returns the one QuotaObserved reading, or throws
   NoRateLimitEvent when no line of that type ever appears (an ordinary stream that never
   crossed a reportable threshold, or a stream truncated before one did). */
export function observe(text) {
  const event = findRateLimitEvent(text);
  if (event === null) throw new NoRateLimitEvent();

  const info = event.rate_limit_info;
  if (info === null || typeof info !== 'object') throw new NoRateLimitEvent();
  const windows = info.unifiedWindows;
  if (windows === null || typeof windows !== 'object') throw new NoRateLimitEvent();
  const fiveHour = windows.five_hour;
  const sevenDay = windows.seven_day;
  const overage = windows.seven_day_overage_included;
  if (
    fiveHour === null || typeof fiveHour !== 'object' || typeof fiveHour.utilization !== 'number' ||
    sevenDay === null || typeof sevenDay !== 'object' || typeof sevenDay.utilization !== 'number' ||
    typeof sevenDay.resetsAt !== 'number' ||
    overage === null || typeof overage !== 'object' || typeof overage.utilization !== 'number' ||
    typeof info.status !== 'string'
  ) {
    throw new NoRateLimitEvent();
  }

  return {
    fiveHourPercentUsed: round(fiveHour.utilization),
    sevenDayPercentUsed: round(sevenDay.utilization),
    overagePercentUsed: round(overage.utilization),
    sevenDayResetsAtIso: isoOf(sevenDay.resetsAt),
    status: info.status,
  };
}

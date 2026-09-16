/* Reading account/rateLimits/read, and choosing the credit to spend.
   Neither the account id nor any token is carried out of here. */

export class Malformed extends Error {
  constructor(reason) {
    super(reason);
    this.reason = reason;
  }
}

const isInteger = value => typeof value === 'number' && Number.isInteger(value);

function window(snapshot, kind) {
  const found = snapshot?.[kind];
  if (found === undefined || found === null) return null;
  if (typeof found !== 'object' || !isInteger(found.usedPercent)) throw new Malformed('malformedRateLimitWindow');
  if (found.resetsAt !== undefined && found.resetsAt !== null && !isInteger(found.resetsAt)) throw new Malformed('malformedRateLimitWindow');
  return { kind, usedPercent: found.usedPercent, resetsAt: found.resetsAt ?? null };
}

/* The binding window is the one with the least left; that is the one a reset would relieve. */
export function observe(response) {
  if (typeof response !== 'object' || response === null) throw new Malformed('malformedRateLimitsResponse');
  const snapshot = response.rateLimits;
  if (typeof snapshot !== 'object' || snapshot === null) throw new Malformed('malformedRateLimitsResponse');
  const windows = [window(snapshot, 'primary'), window(snapshot, 'secondary')].filter(Boolean);
  if (windows.length === 0) throw new Malformed('malformedRateLimitsResponse');
  const binding = windows.reduce((worst, one) => (one.usedPercent > worst.usedPercent ? one : worst));

  const summary = response.rateLimitResetCredits ?? null;
  if (summary !== null && typeof summary !== 'object') throw new Malformed('malformedResetCreditsSummary');
  const availableCount = summary === null ? 0 : summary.availableCount;
  if (!isInteger(availableCount) || availableCount < 0) throw new Malformed('malformedResetCreditsSummary');
  const rows = summary === null ? null : (summary.credits ?? null);
  if (rows !== null && !Array.isArray(rows)) throw new Malformed('malformedResetCreditsSummary');
  const credits =
    rows === null
      ? null
      : rows.map(row => {
          if (typeof row !== 'object' || row === null || typeof row.id !== 'string' || row.id.length === 0) throw new Malformed('malformedResetCredit');
          if (typeof row.status !== 'string') throw new Malformed('malformedResetCredit');
          if (row.expiresAt !== undefined && row.expiresAt !== null && !isInteger(row.expiresAt)) throw new Malformed('malformedResetCredit');
          return { id: row.id, status: row.status, expiresAt: row.expiresAt ?? null, grantedAt: isInteger(row.grantedAt) ? row.grantedAt : 0 };
        });

  return {
    remainingPercent: 100 - binding.usedPercent,
    windowKind: binding.kind,
    resetsAt: binding.resetsAt,
    availableCount,
    credits,
  };
}

/* Soonest non-null expiry first; a credit with no expiry is spent last, and a creditId is always named. */
export function soonestCredit(credits) {
  const available = credits.filter(credit => credit.status === 'available');
  if (available.length === 0) return null;
  const order = [...available].sort((a, b) => {
    const left = a.expiresAt ?? Number.MAX_SAFE_INTEGER,
      right = b.expiresAt ?? Number.MAX_SAFE_INTEGER;
    if (left !== right) return left - right;
    if (a.grantedAt !== b.grantedAt) return a.grantedAt - b.grantedAt;
    return a.id < b.id ? -1 : 1;
  });
  return order[0];
}

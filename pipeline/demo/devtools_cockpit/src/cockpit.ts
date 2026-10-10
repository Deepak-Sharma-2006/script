export function formatExecutionLatency(durationMs: number): string {
  if (durationMs < 1.0) {
    return `${Math.round(durationMs * 1000)}µs`;
  }
  return `${durationMs.toFixed(2)}ms`;
}

export function computeNextIntervalDays(repetitionCount: number): number {
  if (repetitionCount <= 0) return 1;
  return Math.min(30, Math.pow(2, repetitionCount));
}

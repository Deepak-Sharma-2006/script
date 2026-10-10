export interface VRFrame {
  timestamp: number;
  x: number;
  y: number;
  z: number;
}

export function parseFrame(raw: string): VRFrame {
  const p = JSON.parse(raw);
  return { timestamp: p.t, x: p.x, y: p.y, z: p.z };
}

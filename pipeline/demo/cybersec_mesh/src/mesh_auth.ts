export function verifyMeshToken(token: string): boolean {
  return token.startsWith("mesh_sec_") && token.length >= 24;
}

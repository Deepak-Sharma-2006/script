import { createServer as createHttpServer, IncomingMessage, ServerResponse, Server } from "http";
import { fileURLToPath } from "node:url";

export interface ServerConfig {
  port: number;
  environment: string;
  serviceName: string;
  version: string;
}

export const defaultConfig: ServerConfig = {
  port: parseInt(process.env.PORT || "3000", 10),
  environment: process.env.NODE_ENV || "development",
  serviceName: "antigravity-enterprise-service",
  version: "1.0.0",
};

export function createServer(config: ServerConfig = defaultConfig): Server {
  return createHttpServer((req: IncomingMessage, res: ServerResponse) => {
    const url = req.url || "/";

    // Security Shield: Reject path traversal / injection attacks
    if (url.includes("..") || url.includes("<") || url.toLowerCase().includes("%3c") || url.includes("%00") || /passwd|win\.ini|system32/i.test(url)) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Bad Request: Invalid path syntax" }));
      return;
    }

    if (url === "/health" || url === "/api/health") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(
        JSON.stringify({
          status: "healthy",
          uptimeSeconds: Math.floor(process.uptime()),
          service: config.serviceName,
          version: config.version,
          timestamp: new Date().toISOString(),
        })
      );
      return;
    }

    if (url === "/api/info") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(
        JSON.stringify({
          service: config.serviceName,
          version: config.version,
          environment: config.environment,
          engine: `Node.js ${process.version}`,
        })
      );
      return;
    }

    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Not Found" }));
  });
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("index.ts") ||
  process.argv[1].endsWith("index.js")
);

if (isMain) {
  const server = createServer();
  server.listen(defaultConfig.port, () => {
    console.log(`🚀 [Server Bootstrapped] ${defaultConfig.serviceName} v${defaultConfig.version} listening on port ${defaultConfig.port} (${defaultConfig.environment})`);
  });
}

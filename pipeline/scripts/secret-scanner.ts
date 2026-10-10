import { existsSync, readFileSync, readdirSync, statSync } from "fs";
import { join, relative } from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "node:url";

export interface SecretPattern {
  id: string;
  name: string;
  pattern: RegExp;
  severity: "CRITICAL" | "HIGH";
  description: string;
}

export const SECRET_RULES: SecretPattern[] = [
  {
    id: "stripe-live-secret",
    name: "Stripe Live Secret Key",
    pattern: /(sk_live_[0-9a-zA-Z]{10,}|rk_live_[0-9a-zA-Z]{10,})/i,
    severity: "CRITICAL",
    description: "Stripe live secret or restricted key detected.",
  },
  {
    id: "stripe-test-secret",
    name: "Stripe Test Secret Key",
    pattern: /(sk_test_[0-9a-zA-Z]{20,}|rk_test_[0-9a-zA-Z]{20,})/i,
    severity: "HIGH",
    description: "Stripe test key detected. Use environment variables.",
  },
  {
    id: "x-api-key-header",
    name: "X-API-Key Header Secret",
    pattern: /X-API-Key:\s*['"]?(?!<|\$|YOUR_|process\.env)[a-zA-Z0-9_\-]{16,}['"]?/i,
    severity: "CRITICAL",
    description: "Hardcoded API key in X-API-Key header.",
  },
  {
    id: "aws-access-key-id",
    name: "AWS Access Key ID",
    pattern: /\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b/,
    severity: "CRITICAL",
    description: "AWS 20-character Access Key ID detected.",
  },
  {
    id: "github-personal-access-token",
    name: "GitHub Personal Access Token",
    pattern: /\b(ghp_[0-9a-zA-Z]{36}|github_pat_[0-9a-zA-Z_]{82})\b/,
    severity: "CRITICAL",
    description: "GitHub personal access token detected.",
  },
  {
    id: "openai-api-key",
    name: "OpenAI API Key",
    pattern: /\bsk-[a-zA-Z0-9]{20,T3BlbkFJ[a-zA-Z0-9]{20,}\b/,
    severity: "CRITICAL",
    description: "OpenAI live secret key detected.",
  },
  {
    id: "anthropic-api-key",
    name: "Anthropic API Key",
    pattern: /\bsk-ant-api03-[a-zA-Z0-9_\-]{80,}\b/,
    severity: "CRITICAL",
    description: "Anthropic API key detected.",
  },
  {
    id: "google-api-key",
    name: "Google API Key",
    pattern: /\bAIza[0-9A-Za-z\-_]{35}\b/,
    severity: "CRITICAL",
    description: "Google Cloud / Firebase API key detected.",
  },
  {
    id: "slack-token",
    name: "Slack Token",
    pattern: /\bxox[baprs]-[0-9a-zA-Z]{10,48}\b/,
    severity: "CRITICAL",
    description: "Slack bot, app, or user token detected.",
  },
  {
    id: "rsa-private-key",
    name: "Private Key Block",
    pattern: /-----BEGIN (RSA |OPENSSH |DSA |EC |PGP )?PRIVATE KEY-----/,
    severity: "CRITICAL",
    description: "Unencrypted cryptographic private key detected.",
  },
  {
    id: "hardcoded-generic-secret",
    name: "Generic High-Entropy Secret Assignment",
    pattern: /(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret)\s*[:=]\s*['"](?!<|\$|YOUR_|sk_test_|env\.|process\.env)[a-zA-Z0-9_\-]{24,}['"]/i,
    severity: "CRITICAL",
    description: "Hardcoded API key or secret token in variable assignment.",
  },
];

const IGNORED_PATHS = new Set([
  ".git",
  "node_modules",
  ".agents/state",
  "package-lock.json",
  "dist",
  "build",
  "scratch",
]);

export interface SecretFinding {
  ruleId: string;
  ruleName: string;
  severity: "CRITICAL" | "HIGH";
  file: string;
  line: number;
  snippet: string;
}

export function scanText(content: string, filePath: string): SecretFinding[] {
  const findings: SecretFinding[] = [];
  const lines = content.split(/\r?\n/);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Skip empty lines or pure comments with safe placeholders
    if (!line || line.includes("<YOUR_") || line.includes("YOUR_API_KEY") || line.includes("process.env")) {
      continue;
    }

    for (const rule of SECRET_RULES) {
      if (rule.pattern.test(line)) {
        findings.push({
          ruleId: rule.id,
          ruleName: rule.name,
          severity: rule.severity,
          file: filePath,
          line: i + 1,
          snippet: line.trim().slice(0, 100),
        });
      }
    }
  }

  return findings;
}

export function scanDirectory(dir: string, baseDir = dir): SecretFinding[] {
  let findings: SecretFinding[] = [];
  if (!existsSync(dir)) return findings;

  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const relPath = relative(baseDir, fullPath).replace(/\\/g, "/");

    if (IGNORED_PATHS.has(entry) || entry.endsWith(".sqlite") || entry.endsWith(".png") || entry.endsWith(".jpg")) {
      continue;
    }

    try {
      const stat = statSync(fullPath);
      if (stat.isDirectory()) {
        findings = findings.concat(scanDirectory(fullPath, baseDir));
      } else if (stat.isFile()) {
        // Only inspect text files under 2MB
        if (stat.size < 2 * 1024 * 1024) {
          const content = readFileSync(fullPath, "utf-8");
          findings = findings.concat(scanText(content, relPath));
        }
      }
    } catch {
      // Skip unreadable files
    }
  }

  return findings;
}

export function isForbiddenSpecsArtifact(filePath: string): boolean {
  const norm = filePath.replace(/\\/g, "/").replace(/^pipeline\//, "");
  if (norm.startsWith("specs/presentations/")) {
    if (norm.startsWith("specs/presentations/assets/")) {
      return false;
    }
    if (norm.endsWith(".pptx") || norm.endsWith(".pdf") || norm.includes("/rendered/")) {
      return true;
    }
  }
  if (
    norm.startsWith("specs/scratch_tests/") ||
    norm.startsWith("specs/test_assets/") ||
    (norm.startsWith("specs/") && (norm.endsWith(".pptx") || norm.endsWith(".pdf")))
  ) {
    return true;
  }
  return false;
}

export function scanStagedGitFiles(): SecretFinding[] {
  try {
    const findings: SecretFinding[] = [];

    // Check staged filenames against forbidden transient specs artifacts
    try {
      const stagedNames = execSync("git diff --cached --diff-filter=ACMR --name-only", { encoding: "utf-8" })
        .split(/\r?\n/)
        .map((f) => f.trim())
        .filter(Boolean);

      for (const name of stagedNames) {
        if (isForbiddenSpecsArtifact(name)) {
          findings.push({
            ruleId: "forbidden-specs-artifact",
            ruleName: "Forbidden Transient Specs Artifact",
            severity: "CRITICAL",
            file: name,
            line: 1,
            snippet: "Generated test deck or render artifact staged for commit. Must not be committed to Git.",
          });
        }
      }
    } catch {
      // Ignore git errors
    }

    const diff = execSync("git diff --cached --unified=0", { encoding: "utf-8" });
    const lines = diff.split(/\r?\n/);
    let currentFile = "unknown";

    for (const line of lines) {
      if (line.startsWith("+++ b/")) {
        currentFile = line.slice(6);
      } else if (line.startsWith("+") && !line.startsWith("+++")) {
        const addedContent = line.slice(1);
        const fileFindings = scanText(addedContent, currentFile);
        findings.push(...fileFindings);
      }
    }
    return findings;
  } catch {
    return [];
  }
}

export function runSecretScan(mode: "full" | "staged" = "full"): { passed: boolean; findings: SecretFinding[] } {
  console.log(`\n🔒 [Zero-Secret Shield] Initiating secret scanner (${mode} mode)...`);

  const findings = mode === "staged"
    ? scanStagedGitFiles()
    : scanDirectory(process.cwd());

  if (findings.length === 0) {
    console.log(`✅ Zero secrets detected. Codebase is clean.\n`);
    return { passed: true, findings: [] };
  }

  console.error(`\n🚨 SECRETS DETECTED: Found ${findings.length} secret incident(s)!\n`);
  for (const f of findings) {
    console.error(`  • [${f.severity}] ${f.ruleName} in ${f.file}:${f.line}`);
    console.error(`    Snippet: ${f.snippet}\n`);
  }
  console.error(`🛑 COMMIT / AUDIT BLOCKED: Hardcoded secrets are strictly forbidden by AGENTS.md.`);
  console.error(`   Use environment variables (process.env.VAR) or placeholders like <YOUR_API_KEY>.\n`);

  return { passed: false, findings };
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("secret-scanner.ts") ||
  process.argv[1].endsWith("secret-scanner.js")
);

if (isMain) {
  const args = process.argv.slice(2);
  const mode = args.includes("--staged") ? "staged" : "full";
  const result = runSecretScan(mode);
  process.exit(result.passed ? 0 : 1);
}

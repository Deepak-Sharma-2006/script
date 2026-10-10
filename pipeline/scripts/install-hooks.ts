import { existsSync, mkdirSync, writeFileSync, chmodSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "node:url";
import { installGitMergeDriver } from "./index-reconciler.ts";

export function installGitHooks(): boolean {
  const hooksDir = join(process.cwd(), ".git/hooks");
  if (!existsSync(hooksDir)) {
    mkdirSync(hooksDir, { recursive: true });
  }

  // 1. Pre-commit Hook
  const preCommitHook = `#!/bin/sh
# Antigravity Autonomous Pre-Commit Shield: Zero-Secret, Zero-LaTeX & Anti-Hallucination Gate
echo "🔒 [Pre-Commit Gate 1/5] Verifying zero secrets in staged changes..."
node --experimental-strip-types pipeline/scripts/secret-scanner.ts --staged
if [ $? -ne 0 ]; then
  echo "🛑 [COMMIT REJECTED] Secret scanner detected forbidden secrets in staged diff!"
  echo "Remove hardcoded credentials before committing."
  exit 1
fi

echo "📝 [Pre-Commit Gate 2/5] Verifying Zero-LaTeX compliance across markdown documentation..."
node --experimental-strip-types pipeline/scripts/markdown-linter.ts docs
if [ $? -ne 0 ]; then
  echo "🛑 [COMMIT REJECTED] Markdown linter detected raw LaTeX delimiters ($ or $$)!"
  echo "Replace raw LaTeX with clean Unicode typography (>=, <=, x, !=, ->, +-) or fenced code blocks."
  exit 1
fi

echo "🛡️ [Pre-Commit Gate 3/5] Verifying Zero Ghost Packages & AST import grounding..."
node --experimental-strip-types pipeline/scripts/anti-hallucination-checker.ts pipeline/scripts src pipeline/tests pipeline/browser_tests
if [ $? -ne 0 ]; then
  echo "🛑 [COMMIT REJECTED] Anti-hallucination scanner detected undeclared package imports!"
  echo "Declare all third-party dependencies in package.json before committing."
  exit 1
fi

echo "🔍 [Pre-Commit Gate 4/5] Verifying empirical grounding against physical bounds and audit logs..."
python pipeline/scripts/harness/grounding-validator.py --staged
if [ $? -ne 0 ]; then
  echo "🛑 [COMMIT REJECTED] Grounding validator detected ungrounded claims or physical compute violations!"
  echo "Ensure all benchmark claims match verified physical limits and recorded audit logs."
  exit 1
fi

echo "📑 [Pre-Commit Gate 5/5] Reconciling Team Mesh Living Documentation Catalogs..."
node --experimental-strip-types pipeline/scripts/index-reconciler.ts

echo "✅ [Pre-Commit Barrier Complete] All 5 enterprise gates passed with zero violations."
exit 0
`;

  const hookPath = join(hooksDir, "pre-commit");
  writeFileSync(hookPath, preCommitHook, "utf-8");

  // 2. Post-merge Hook
  const postMergeHook = `#!/bin/sh
# Team Mesh Living Index Automatic Post-Merge Reconciler
echo "📑 [Post-Merge Hook] Reconciling Team Mesh Living Documentation Catalogs..."
node --experimental-strip-types pipeline/scripts/index-reconciler.ts
exit 0
`;

  const postMergePath = join(hooksDir, "post-merge");
  writeFileSync(postMergePath, postMergeHook, "utf-8");

  try {
    chmodSync(hookPath, 0o755);
    chmodSync(postMergePath, 0o755);
  } catch {
    // Windows may ignore chmod
  }

  // 3. Install Git Merge Driver for docs/**/INDEX.md
  installGitMergeDriver();

  console.log(`✅ [Git Hooks Installed] Pre-commit 4-gate barrier and post-merge reconciler configured.`);
  return true;
}

const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("install-hooks.ts") ||
  process.argv[1].endsWith("install-hooks.js")
);

if (isMain) {
  installGitHooks();
}


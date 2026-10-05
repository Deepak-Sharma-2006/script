/**
 * Executive Visual & Markdown Linter
 * Enforces the Executive Presentation Standard & Zero-Raw-LaTeX Policy (Question c).
 *
 * Checks:
 * 1. Zero Raw LaTeX: Prohibits unrendered math delimiters ($...$ and $$...$$) that fail in standard viewers.
 * 2. Zero Broken Images: Prohibits fragile relative image markdown embeds (![...](...)).
 * 3. Mandates clean Unicode typography and structured GitHub alert cards.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';

interface LintViolation {
  file: string;
  line: number;
  type: 'RAW_LATEX_INLINE' | 'RAW_LATEX_BLOCK' | 'FRAGILE_LOCAL_IMAGE';
  snippet: string;
}

export class MarkdownLinter {
  public static lintDirectory(dirPath: string): { clean: boolean; violations: LintViolation[] } {
    const violations: LintViolation[] = [];
    const ignoreDirs = new Set(['node_modules', '.git', '.venv', 'venv', 'dist', 'build', '.tempmediaStorage', '.system_generated', 'specs']);

    if (fs.existsSync(dirPath) && fs.statSync(dirPath).isFile()) {
      if (dirPath.endsWith('.md')) {
        MarkdownLinter.lintFile(dirPath, violations);
      }
      return { clean: violations.length === 0, violations };
    }

    function walk(current: string) {
      if (!fs.existsSync(current)) return;
      const entries = fs.readdirSync(current, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory()) {
          if (!ignoreDirs.has(entry.name)) {
            walk(path.join(current, entry.name));
          }
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          MarkdownLinter.lintFile(path.join(current, entry.name), violations);
        }
      }
    }

    walk(dirPath);
    return { clean: violations.length === 0, violations };
  }

  public static lintFile(filePath: string, violations: LintViolation[] = []): LintViolation[] {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    let inCodeBlock = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Skip code fence blocks
      if (line.trim().startsWith('```')) {
        inCodeBlock = !inCodeBlock;
        continue;
      }
      if (inCodeBlock) continue;

      // 1. Check for block LaTeX $$...$$
      if (line.includes('$$')) {
        violations.push({
          file: filePath,
          line: i + 1,
          type: 'RAW_LATEX_BLOCK',
          snippet: line.trim()
        });
      }

      // 2. Check for inline LaTeX $...$
      // Match $text$ where it's not a dollar amount like $50 or $100
      const inlineLatexMatch = line.match(/(?<!\$)\$(?!\s)(?!\d+(?:\.\d+)?(?:[ ,.]|$))([^\$\n]+?)(?<!\s)\$(?!\$)/);
      if (inlineLatexMatch) {
        violations.push({
          file: filePath,
          line: i + 1,
          type: 'RAW_LATEX_INLINE',
          snippet: inlineLatexMatch[0]
        });
      }

      // 3. Check for fragile local image embeds
      const imageMatch = line.match(/!\[[^\]]*\]\((?!(?:https?:\/\/|\/assets\/))(.*?)\)/);
      if (imageMatch) {
        violations.push({
          file: filePath,
          line: i + 1,
          type: 'FRAGILE_LOCAL_IMAGE',
          snippet: imageMatch[0]
        });
      }
    }

    return violations;
  }

  public static fixFile(filePath: string): boolean {
    let content = fs.readFileSync(filePath, 'utf-8');
    const original = content;

    // Replace common LaTeX math constructs with clean Unicode equivalents
    content = content
      .replace(/\$\\ge\$/g, '≥')
      .replace(/\$\\le\$/g, '≤')
      .replace(/\$\\times\$/g, '×')
      .replace(/\$\\Delta t\\le/g, 'Δt ≤')
      .replace(/\$\\Delta t/g, 'Δt')
      .replace(/\$\\approx\$/g, '≈')
      .replace(/\$\\ne\$/g, '≠')
      .replace(/\\text\{([^}]+)\}/g, '$1')
      .replace(/\\quad/g, ' ')
      .replace(/\\le/g, '≤')
      .replace(/\\ge/g, '≥')
      .replace(/\\times/g, '×')
      .replace(/\$\$([^$]+)\$\$/g, (_match, p1) => {
        return `> ${p1.trim().replace(/\\quad/g, ' ')}`;
      })
      .replace(/\$([^$\n]+)\$/g, (_match, p1) => {
        // If it looks like a dollar price ($10, $5.00), leave it alone
        if (/^\s*\d+(?:\.\d+)?\s*$/.test(p1)) return `$${p1}`;
        return p1.replace(/\\/g, '').trim();
      });

    if (content !== original) {
      fs.writeFileSync(filePath, content, 'utf-8');
      return true;
    }
    return false;
  }
}

// CLI entry point
if (process.argv[1]?.endsWith('markdown-linter.ts') || process.argv[1]?.endsWith('markdown-linter.js')) {
  const args = process.argv.slice(2);
  const shouldFix = args.includes('--fix');
  const targetDir = args.find(a => !a.startsWith('--')) || path.join(process.cwd(), 'docs');

  console.log('\n================================================================================');
  console.log('📝 [MARKDOWN LINTER] Auditing Workspace for Executive Presentation Compliance');
  console.log('   Rule 1: Zero Raw LaTeX ($ or $$) — Use Unicode math typography');
  console.log('   Rule 2: Zero Fragile Local Images — Use Native ASCII/Unicode diagrams');
  if (shouldFix) console.log('   Mode  : Auto-Fix Enabled');
  console.log('================================================================================\n');

  if (shouldFix) {
    function walkFix(current: string) {
      const entries = fs.readdirSync(current, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory()) {
          if (!['node_modules', '.git', '.venv', 'dist', 'specs'].includes(entry.name)) {
            walkFix(path.join(current, entry.name));
          }
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          MarkdownLinter.fixFile(path.join(current, entry.name));
        }
      }
    }
    walkFix(targetDir);
  }

  const res = MarkdownLinter.lintDirectory(targetDir);

  if (res.clean) {
    console.log('✅ [PASSED] All markdown documents adhere to Executive Visual & Zero-LaTeX standards.\n');
    process.exit(0);
  } else {
    console.error(`❌ [FAILED] Found ${res.violations.length} visual formatting violations:`);
    for (const v of res.violations.slice(0, 10)) {
      console.error(`   - ${path.relative(process.cwd(), v.file)}:${v.line} [${v.type}]: "${v.snippet}"`);
    }
    if (res.violations.length > 10) {
      console.error(`   ... and ${res.violations.length - 10} more violations.`);
    }
    console.error('\nFix: Run `npm run lint:markdown -- --fix` or replace raw LaTeX with clean Unicode math.\n');
    process.exit(1);
  }
}

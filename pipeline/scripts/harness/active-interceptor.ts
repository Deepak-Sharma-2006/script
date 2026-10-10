/**
 * Active Execution Interceptor & Runtime Quality Harness (INV-01 / Stage 1)
 * 
 * Intercepts tool calls and shell command execution:
 * 1. Queries active_kernel.py pre-execution safety gate to block destructive operations.
 * 2. Executes permitted commands under strict timeout bounds.
 * 3. Truncates verbose stdout/stderr (>35 lines) into spillover files to protect LLM context.
 * 4. Records cryptographically grounded execution records in .agents/audit_trail.log.
 */

import { spawn, execSync } from "child_process";
import { existsSync, mkdirSync, writeFileSync, appendFileSync } from "fs";
import { join } from "path";
import { createHash } from "crypto";
import { fileURLToPath } from "url";

export interface ExecutionResult {
  command: string;
  permitted: boolean;
  exitCode: number;
  stdout: string;
  stderr: string;
  durationMs: number;
  truncated: boolean;
  spilloverPath?: string;
  rejectionReason?: string;
}

export class ActiveInterceptor {
  private static readonly WORKSPACE_ROOT = process.cwd();
  private static readonly AUDIT_LOG = join(process.cwd(), ".agents", "audit_trail.log");
  private static readonly LOGS_DIR = join(process.cwd(), ".agents", "logs");
  private static readonly MAX_OUTPUT_LINES = 35;

  /**
   * Pre-execution safety check via ActiveKernel Python engine.
   */
  public static checkSafetyGate(command: string): { permitted: boolean; reason?: string; action?: string } {
    try {
      // Escape command for shell execution
      const escapedCmd = command.replace(/"/g, '\\"');
      const pyCmd = `python .agents/harness/active_kernel.py --intercept "${escapedCmd}"`;
      
      const stdout = execSync(pyCmd, {
        cwd: this.WORKSPACE_ROOT,
        encoding: "utf-8",
        stdio: ["ignore", "pipe", "pipe"],
      });

      const parsed = JSON.parse(stdout);
      return {
        permitted: parsed.permitted === true,
        reason: parsed.reason,
        action: parsed.action,
      };
    } catch (err: any) {
      if (err.stdout) {
        try {
          const parsed = JSON.parse(err.stdout.toString());
          return {
            permitted: false,
            reason: parsed.reason || parsed.destructive_action || "Command blocked by active safety gate.",
            action: parsed.action || "BLOCK",
          };
        } catch {
          // Non-JSON output from python
        }
      }
      return {
        permitted: false,
        reason: `Harness pre-execution check failed or rejected command: ${err.message}`,
        action: "BLOCK",
      };
    }
  }

  /**
   * Formats and truncates output if exceeding MAX_OUTPUT_LINES.
   */
  public static truncateOutput(output: string, cmdHash: string): { text: string; truncated: boolean; spilloverPath?: string } {
    const lines = output.split(/\r?\n/);
    if (lines.length <= this.MAX_OUTPUT_LINES) {
      return { text: output, truncated: false };
    }

    if (!existsSync(this.LOGS_DIR)) {
      mkdirSync(this.LOGS_DIR, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const spilloverFile = join(this.LOGS_DIR, `spillover_${timestamp}_${cmdHash.slice(0, 8)}.log`);
    writeFileSync(spilloverFile, output, "utf-8");

    const headLines = lines.slice(0, 5);
    const tailLines = lines.slice(-30);
    const skipped = lines.length - 35;

    const truncatedText = [
      ...headLines,
      "",
      `[... TRUNCATED ${skipped} LINES OF VERBOSE OUTPUT TO PROTECT CONTEXT WINDOW ...]`,
      `[... Full untruncated output saved to: file:///${spilloverFile.replace(/\\/g, "/")} ...]`,
      "",
      ...tailLines,
    ].join("\n");

    return {
      text: truncatedText,
      truncated: true,
      spilloverPath: spilloverFile,
    };
  }

  /**
   * Logs execution record into .agents/audit_trail.log with SHA-256 digest.
   */
  public static recordAuditTrail(result: ExecutionResult): void {
    try {
      const auditDir = join(this.WORKSPACE_ROOT, ".agents");
      if (!existsSync(auditDir)) {
        mkdirSync(auditDir, { recursive: true });
      }

      const iso = new Date().toISOString();
      const payloadHash = createHash("sha256")
        .update(`${result.command}|${result.exitCode}|${result.stdout}|${result.stderr}`)
        .digest("hex");

      const logLine = `[${iso}] [ACTIVE_HARNESS] CMD: "${result.command}" | EXIT: ${result.exitCode} | DURATION: ${result.durationMs}ms | SHA256: ${payloadHash}\n`;
      appendFileSync(this.AUDIT_LOG, logLine, "utf-8");
    } catch {
      // Non-blocking logging
    }
  }

  /**
   * Executes command with active interception, truncation, and audit trail logging.
   */
  public static async execute(command: string, timeoutMs: number = 60000): Promise<ExecutionResult> {
    const startTime = Date.now();

    // Step 1: Pre-execution safety gate
    const gate = this.checkSafetyGate(command);
    if (!gate.permitted) {
      const rejectedResult: ExecutionResult = {
        command,
        permitted: false,
        exitCode: 1,
        stdout: "",
        stderr: `🛑 [HARNESS INTERCEPT REJECTED] Action: ${gate.action || "BLOCK"}\nReason: ${gate.reason || "Destructive or prohibited command."}\n`,
        durationMs: Date.now() - startTime,
        truncated: false,
        rejectionReason: gate.reason,
      };
      this.recordAuditTrail(rejectedResult);
      return rejectedResult;
    }

    // Step 2: Safe Subprocess Execution
    return new Promise((resolve) => {
      const isWin = process.platform === "win32";
      const shell = isWin ? "powershell.exe" : "/bin/sh";
      const shellArgs = isWin ? ["-Command", command] : ["-c", command];

      const child = spawn(shell, shellArgs, {
        cwd: this.WORKSPACE_ROOT,
        env: { ...process.env, HARNESS_ACTIVE: "1" },
      });

      let stdoutAccum = "";
      let stderrAccum = "";
      let timedOut = false;

      const timer = setTimeout(() => {
        timedOut = true;
        child.kill();
      }, timeoutMs);

      child.stdout.on("data", (data) => {
        stdoutAccum += data.toString();
      });

      child.stderr.on("data", (data) => {
        stderrAccum += data.toString();
      });

      child.on("close", (code) => {
        clearTimeout(timer);
        const durationMs = Date.now() - startTime;
        const exitCode = timedOut ? 124 : (code ?? 1);

        if (timedOut) {
          stderrAccum += `\n🛑 [HARNESS TIMEOUT] Command exceeded timeout limit of ${timeoutMs}ms.\n`;
        }

        const cmdHash = createHash("sha256").update(command).digest("hex");
        const trunc = this.truncateOutput(stdoutAccum, cmdHash);

        const result: ExecutionResult = {
          command,
          permitted: true,
          exitCode,
          stdout: trunc.text,
          stderr: stderrAccum,
          durationMs,
          truncated: trunc.truncated,
          spilloverPath: trunc.spilloverPath,
        };

        this.recordAuditTrail(result);
        resolve(result);
      });

      child.on("error", (err) => {
        clearTimeout(timer);
        const durationMs = Date.now() - startTime;
        const result: ExecutionResult = {
          command,
          permitted: true,
          exitCode: 1,
          stdout: stdoutAccum,
          stderr: stderrAccum + `\n🛑 [PROCESS ERROR] Failed to start process: ${err.message}\n`,
          durationMs,
          truncated: false,
        };
        this.recordAuditTrail(result);
        resolve(result);
      });
    });
  }
}

// CLI Entrypoint
const isMain = process.argv[1] && (
  fileURLToPath(import.meta.url) === process.argv[1] ||
  process.argv[1].endsWith("active-interceptor.ts") ||
  process.argv[1].endsWith("active-interceptor.js")
);

if (isMain) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node --experimental-strip-types scripts/harness/active-interceptor.ts <command>");
    process.exit(1);
  }

  const command = args.join(" ");
  ActiveInterceptor.execute(command).then((res) => {
    if (res.stdout) process.stdout.write(res.stdout);
    if (res.stderr) process.stderr.write(res.stderr);
    process.exit(res.exitCode);
  });
}

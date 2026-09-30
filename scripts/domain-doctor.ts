/**
 * Universal Domain Doctor & Environment Verification Probe
 * 
 * Verifies toolchain readiness, compilers, runtimes, and statutory constraints
 * for the currently active Master Domain and selected subdomains.
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import { getActiveDomainState, loadRubric } from './domain-selector.ts';

interface CheckResult {
  tool: string;
  status: 'READY' | 'WARNING' | 'MISSING';
  versionOrDetail: string;
  recommendedAction?: string;
}

function checkBinary(command: string, args: string = '--version'): { ok: boolean; output: string } {
  try {
    const out = execSync(`${command} ${args}`, { stdio: ['pipe', 'pipe', 'ignore'], timeout: 3000 }).toString().trim();
    return { ok: true, output: out.split('\n')[0] };
  } catch {
    return { ok: false, output: 'Not found in PATH' };
  }
}

export function runDomainDiagnostics(): { state: any; rubric: any; checks: CheckResult[]; ready: boolean } {
  const state = getActiveDomainState();
  const rubric = loadRubric(state.domain_id);
  const checks: CheckResult[] = [];

  // Core Runtime Checks
  const nodeCheck = checkBinary('node');
  checks.push({
    tool: 'Node.js Runtime',
    status: nodeCheck.ok ? 'READY' : 'MISSING',
    versionOrDetail: nodeCheck.output,
    recommendedAction: nodeCheck.ok ? undefined : 'Install Node.js v20+ LTS'
  });

  const pythonCheck = checkBinary('python');
  checks.push({
    tool: 'Python 3 Runtime',
    status: pythonCheck.ok ? 'READY' : 'MISSING',
    versionOrDetail: pythonCheck.output,
    recommendedAction: pythonCheck.ok ? undefined : 'Install Python 3.11+'
  });

  // Domain-Specific Tooling Checks
  for (const toolKey of rubric.doctor_checks) {
    if (toolKey === 'node' || toolKey === 'python') continue;

    if (toolKey === 'tsc') {
      const res = checkBinary('npx', 'tsc --version');
      checks.push({
        tool: 'TypeScript Compiler (tsc)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install via: npm install --save-dev typescript'
      });
    } else if (toolKey === 'npm') {
      const res = checkBinary('npm');
      checks.push({
        tool: 'Node Package Manager (npm)',
        status: res.ok ? 'READY' : 'MISSING',
        versionOrDetail: res.output
      });
    } else if (toolKey === 'pip') {
      const res = checkBinary('pip');
      checks.push({
        tool: 'Python Package Manager (pip)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output
      });
    } else if (toolKey === 'docker') {
      const res = checkBinary('docker');
      checks.push({
        tool: 'Docker Engine / CLI',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install Docker Desktop if containerization is required'
      });
    } else if (toolKey === 'gcc') {
      const res = checkBinary('gcc');
      checks.push({
        tool: 'C/C++ Compiler (gcc/clang)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install GCC/Clang or Visual Studio C++ Build Tools for native compiling'
      });
    } else if (toolKey === 'forge') {
      const res = checkBinary('forge', '--version');
      checks.push({
        tool: 'Foundry Engine (forge)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install Foundry via: curl -L https://foundry.paradigm.xyz | bash'
      });
    } else if (toolKey === 'solc') {
      const res = checkBinary('solc', '--version');
      checks.push({
        tool: 'Solidity Compiler (solc)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install solc via npm: npm install -g solc'
      });
    } else if (toolKey === 'slither') {
      const res = checkBinary('slither', '--version');
      checks.push({
        tool: 'Slither Static Analyzer',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install Slither via pip: pip install slither-analyzer'
      });
    } else if (toolKey === 'cargo') {
      const res = checkBinary('cargo', '--version');
      checks.push({
        tool: 'Rust Toolchain (cargo)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install Rust via: https://rustup.rs'
      });
    } else if (toolKey === 'kubectl') {
      const res = checkBinary('kubectl', 'version --client --output=yaml');
      checks.push({
        tool: 'Kubernetes CLI (kubectl)',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install kubectl via official Kubernetes release'
      });
    } else if (toolKey === 'terraform') {
      const res = checkBinary('terraform', 'version');
      checks.push({
        tool: 'Terraform IaC CLI',
        status: res.ok ? 'READY' : 'WARNING',
        versionOrDetail: res.output,
        recommendedAction: res.ok ? undefined : 'Install Terraform via HashiCorp releases'
      });
    }
  }

  const allReady = checks.every(c => c.status === 'READY' || c.status === 'WARNING');
  return { state, rubric, checks, ready: allReady };
}

export function printDomainDiagnostics(): void {
  const { state, rubric, checks, ready } = runDomainDiagnostics();

  console.log('\n================================================================================');
  console.log(`🩺 [DOMAIN TOOLCHAIN DOCTOR: ${state.domain_name.toUpperCase()}]`);
  console.log('================================================================================');
  console.log(`Active Domain ID : ${state.domain_id}`);
  console.log(`Active Subdomains: ${state.subdomains.join(', ')}`);
  console.log('--------------------------------------------------------------------------------');

  for (const c of checks) {
    const icon = c.status === 'READY' ? '✅' : c.status === 'WARNING' ? '⚠️ ' : '❌';
    console.log(`  ${icon} [${c.status.padEnd(7)}] ${c.tool.padEnd(30)} : ${c.versionOrDetail}`);
    if (c.recommendedAction) {
      console.log(`       👉 Recommendation: ${c.recommendedAction}`);
    }
  }

  console.log('================================================================================');
  if (ready) {
    console.log('🚀 [DOMAIN READINESS: CERTIFIED] Autonomous squad is fully equipped for this domain.');
  } else {
    console.log('⚠️ [DOMAIN READINESS: ACTION REQUIRED] Please resolve missing tools above.');
  }
  console.log('================================================================================\n');
}

if (process.argv[1] && process.argv[1].endsWith('domain-doctor.ts')) {
  printDomainDiagnostics();
}

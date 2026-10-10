/**
 * Universal Domain & Multi-Subdomain Selection Controller
 * 
 * Manages atomic domain selection, multi-subdomain technology stack resolution,
 * and state persistence for the 6-Persona autonomous SDLC squad.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';

export interface SubdomainMeta {
  name: string;
  description: string;
  key_technologies: string[];
  statutory_standards: string[];
}

export interface DomainRubric {
  domain_id: string;
  domain_name: string;
  description: string;
  subdomains: Record<string, SubdomainMeta>;
  persona_specializations: Record<string, any>;
  verification_gates: string[];
  doctor_checks: string[];
}

export interface ActiveDomainState {
  domain_id: string;
  domain_name: string;
  subdomains: string[];
  configured_at: string;
  configured_by: string;
  active_stack: {
    languages_and_tools: string[];
    statutory_standards: string[];
    verification_gates: string[];
  };
}

const STATE_DIR = path.resolve(process.cwd(), '.agents', 'state');
const STATE_FILE = path.join(STATE_DIR, 'active-domain.json');
const TEMPLATES_DIR = fs.existsSync(path.resolve(process.cwd(), 'pipeline', 'templates', 'domains'))
  ? path.resolve(process.cwd(), 'pipeline', 'templates', 'domains')
  : path.resolve(process.cwd(), 'templates', 'domains');
const CATALOG_FILE = path.join(TEMPLATES_DIR, 'catalog.json');

export function loadCatalog(): Record<string, any> {
  if (!fs.existsSync(CATALOG_FILE)) {
    throw new Error(`Domain catalog not found at ${CATALOG_FILE}`);
  }
  return JSON.parse(fs.readFileSync(CATALOG_FILE, 'utf-8'));
}

export function loadRubric(domainId: string): DomainRubric {
  const rubricPath = path.join(TEMPLATES_DIR, domainId, 'rubric.json');
  if (!fs.existsSync(rubricPath)) {
    throw new Error(`Rubric for domain '${domainId}' not found at ${rubricPath}`);
  }
  return JSON.parse(fs.readFileSync(rubricPath, 'utf-8'));
}

export function getActiveDomainState(): ActiveDomainState {
  if (fs.existsSync(STATE_FILE)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
      if (parsed && parsed.domain_id && Array.isArray(parsed.subdomains) && parsed.active_stack) {
        return parsed;
      }
    } catch {
      console.warn(`⚠️ Warning: Corrupted active-domain.json detected. Self-healing to default software profile.`);
    }
  }

  // Default to Software Engineering (Web + Backend)
  const defaultRubric = loadRubric('software');
  const defaultState: ActiveDomainState = {
    domain_id: 'software',
    domain_name: defaultRubric.domain_name,
    subdomains: ['web_frontend', 'backend_systems'],
    configured_at: new Date().toISOString(),
    configured_by: 'SystemDefault',
    active_stack: {
      languages_and_tools: [
        ...defaultRubric.subdomains.web_frontend.key_technologies,
        ...defaultRubric.subdomains.backend_systems.key_technologies
      ],
      statutory_standards: [
        ...defaultRubric.subdomains.web_frontend.statutory_standards,
        ...defaultRubric.subdomains.backend_systems.statutory_standards
      ],
      verification_gates: defaultRubric.verification_gates
    }
  };
  saveActiveDomainState(defaultState);
  return defaultState;
}

export function saveActiveDomainState(state: ActiveDomainState): void {
  if (!fs.existsSync(STATE_DIR)) {
    fs.mkdirSync(STATE_DIR, { recursive: true });
  }
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

export function setDomain(domainId: string, subdomainIds: string[], operator: string = 'SoloOperator'): ActiveDomainState {
  const catalog = loadCatalog();
  if (!catalog.domains[domainId]) {
    const valid = Object.keys(catalog.domains).join(', ');
    throw new Error(`Invalid domain '${domainId}'. Valid domains are: ${valid}`);
  }

  const rubric = loadRubric(domainId);
  const availableSubdomains = Object.keys(rubric.subdomains);

  // Validate subdomains
  const validatedSubdomains: string[] = [];
  for (const sub of subdomainIds) {
    const clean = sub.trim().toLowerCase();
    if (availableSubdomains.includes(clean)) {
      validatedSubdomains.push(clean);
    } else {
      console.warn(`⚠️ Warning: Subdomain '${clean}' not recognized for domain '${domainId}'. Skipping.`);
    }
  }

  // If no valid subdomains passed, default to first available
  if (validatedSubdomains.length === 0) {
    validatedSubdomains.push(availableSubdomains[0]);
  }

  // Aggregate composite stack
  const toolsSet = new Set<string>();
  const standardsSet = new Set<string>();

  for (const sub of validatedSubdomains) {
    const meta = rubric.subdomains[sub];
    if (meta) {
      meta.key_technologies.forEach(t => toolsSet.add(t));
      meta.statutory_standards.forEach(s => standardsSet.add(s));
    }
  }

  const newState: ActiveDomainState = {
    domain_id: domainId,
    domain_name: rubric.domain_name,
    subdomains: validatedSubdomains,
    configured_at: new Date().toISOString(),
    configured_by: operator,
    active_stack: {
      languages_and_tools: Array.from(toolsSet),
      statutory_standards: Array.from(standardsSet),
      verification_gates: rubric.verification_gates
    }
  };

  saveActiveDomainState(newState);
  return newState;
}

export function formatStatus(state: ActiveDomainState): string {
  const rubric = loadRubric(state.domain_id);
  const subNames = state.subdomains.map(s => rubric.subdomains[s]?.name || s).join('\n     • ');

  return `
================================================================================
🌐 [ACTIVE DOMAIN PROFILE: ${state.domain_name.toUpperCase()}]
================================================================================
  Domain ID           : ${state.domain_id}
  Configured At       : ${state.configured_at}
  Configured By       : ${state.configured_by}
  Active Subdomains   :
     • ${subNames}

  Specialized Stack   :
     • Tools & Libs   : ${state.active_stack.languages_and_tools.slice(0, 10).join(', ')}...
     • Standards      : ${state.active_stack.statutory_standards.join(' | ')}
     • Active Gates   : ${state.active_stack.verification_gates.join(', ')}

  Autonomous Squad Specialization:
     • [PM]           : ${rubric.persona_specializations.product_manager.role_title}
     • [Architect]    : ${rubric.persona_specializations.system_architect.role_title}
     • [SDET]         : ${rubric.persona_specializations.adversarial_sdet.role_title}
     • [Core Dev]     : ${rubric.persona_specializations.core_engineer.role_title}
     • [Auditor]      : ${rubric.persona_specializations.mutation_auditor.role_title}
     • [Tech Writer]  : ${rubric.persona_specializations.technical_writer.role_title}
================================================================================
`;
}

export function formatCatalog(): string {
  const catalog = loadCatalog();
  let out = `
================================================================================
📚 [UNIVERSAL MASTER DOMAINS & SUBDOMAINS CATALOG]
================================================================================
`;
  let idx = 1;
  for (const [id, d] of Object.entries<any>(catalog.domains)) {
    const rubric = loadRubric(id);
    out += `\n[${idx}] ${d.name} (ID: ${id})\n`;
    out += `    ${rubric.description}\n`;
    out += `    Subdomains:\n`;
    for (const [subId, sub] of Object.entries(rubric.subdomains)) {
      out += `      - ${subId.padEnd(24)} : ${sub.name}\n`;
    }
    idx++;
  }
  out += `\nRun 'npm run domain:set -- --domain <id> --subdomains <id1,id2>' to configure.\n`;
  return out;
}

async function runInteractiveSelection(): Promise<void> {
  const catalog = loadCatalog();
  const domainKeys = Object.keys(catalog.domains);

  console.log('\n================================================================================');
  console.log('🎯 [ENTERPRISE DOMAIN SELECTION ASSISTANT]');
  console.log('   Select the primary domain for your autonomous engineering squad:');
  console.log('================================================================================');

  domainKeys.forEach((key, index) => {
    console.log(`  [${index + 1}] ${catalog.domains[key].name} (${key})`);
  });

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const question = (prompt: string): Promise<string> =>
    new Promise(resolve => rl.question(prompt, resolve));

  try {
    const domainAnswer = await question('\nSelect Master Domain (1-8) [Default: 1]: ');
    const domainIndex = parseInt(domainAnswer.trim() || '1', 10) - 1;
    const chosenDomainKey = domainKeys[domainIndex] || domainKeys[0];
    const rubric = loadRubric(chosenDomainKey);
    const subdomainKeys = Object.keys(rubric.subdomains);

    console.log(`\nSelected Domain: ${rubric.domain_name}`);
    console.log('Available Subdomains:');
    subdomainKeys.forEach((subKey, index) => {
      console.log(`  [${index + 1}] ${rubric.subdomains[subKey].name} (${subKey})`);
    });

    const subAnswer = await question('\nSelect Subdomain(s) (comma-separated numbers e.g. 1,2) [Default: 1]: ');
    const chosenSubdomainKeys: string[] = [];
    const parts = (subAnswer.trim() || '1').split(',');

    for (const p of parts) {
      const idx = parseInt(p.trim(), 10) - 1;
      if (subdomainKeys[idx]) {
        chosenSubdomainKeys.push(subdomainKeys[idx]);
      }
    }

    if (chosenSubdomainKeys.length === 0) {
      chosenSubdomainKeys.push(subdomainKeys[0]);
    }

    const state = setDomain(chosenDomainKey, chosenSubdomainKeys, 'InteractiveOperator');
    console.log('\n✅ Domain and Subdomains successfully activated!');
    console.log(formatStatus(state));
  } finally {
    rl.close();
  }
}

// CLI Command Dispatcher
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'status';

  try {
    if (command === 'status') {
      const state = getActiveDomainState();
      console.log(formatStatus(state));
    } else if (command === 'list') {
      console.log(formatCatalog());
    } else if (command === 'select' || command === 'interactive') {
      await runInteractiveSelection();
    } else if (command === 'set') {
      let domain = 'software';
      let subdomains = ['web_frontend', 'backend_systems'];

      for (let i = 1; i < args.length; i++) {
        if (args[i] === '--domain' && args[i + 1]) {
          domain = args[i + 1];
          i++;
        } else if (args[i] === '--subdomains' && args[i + 1]) {
          subdomains = args[i + 1].split(',').map(s => s.trim());
          i++;
        }
      }

      const state = setDomain(domain, subdomains, 'CliOperator');
      console.log(`✅ Successfully set domain to '${state.domain_name}' with subdomains: ${state.subdomains.join(', ')}`);
      console.log(formatStatus(state));
    } else {
      console.log(`Unknown command: ${command}. Use status, list, select, or set.`);
    }
  } catch (err: any) {
    console.error(`❌ Error: ${err.message}`);
    process.exit(1);
  }
}

if (process.argv[1] && process.argv[1].endsWith('domain-selector.ts')) {
  main();
}
